#!/usr/bin/env python3
"""Mix lesson narration over a Suno BGM bed with timeline-driven ducking.

Sidechain compression pumps the music up in every pause between words. This mixer instead
reads the speech and transition times from resolved-timeline.json and draws one smooth gain
envelope for the bed:

  * narration: 80 Hz high-pass, light presence lift, normalised to --voice-lufs (-14 LUFS)
  * bed under speech: --duck-db (-18 dB) with a --pocket-db (-3 dB) dip at --pocket-hz
    (1.5 kHz) carving a vocal pocket; the bed reaches that level --preroll (0.3 s) before
    speech starts and stays there through ordinary pauses, so it never pumps
  * bed in full_swell transitions, the intro and the outro: ramps to --swell-db (-2 dB) with
    the dip released, then back down before the next words
  * final mix: linear gain to --target-lufs (-14) under a --true-peak (-1 dBTP) ceiling

Levels are relative to the bed after normalising it to --bgm-ref-lufs, so a loud Suno master
and a quiet one sit the same way. The bed is offset by --bgm-offset (default: the timeline's
bgm.offset from extract-video-timing.py --merge-into, else 0); positive trims its head.

Usage:
  python3 mix-voice-and-bgm.py master-narration.wav bgm.wav resolved-timeline.json master-audio.wav \\
      [--duck-db -18] [--swell-db -2] [--loop-bgm] [--dry-run]

Needs FFmpeg on PATH. Writes 48 kHz 24-bit stereo WAV. Refuses to overwrite without --force.
Prints the measured loudness and true peak of the result; a printed level is not a listening
check.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RATE = 48000


def fail(message: str):
    raise SystemExit(f"error: {message}")


def ffmpeg(args: list[str], what: str) -> str:
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args], capture_output=True, text=True)
    if proc.returncode:
        fail(f"FFmpeg failed while {what}:\n{proc.stderr.strip()[-2000:]}")
    return proc.stderr


def measure(inputs: list[str], chain: str, what: str) -> tuple[float, float]:
    """Integrated loudness (LUFS) and true peak (dBTP) after a filter chain."""
    log = ffmpeg([*inputs, "-filter_complex", f"{chain}ebur128=peak=true", "-f", "null", "-"], what)
    summary = log[log.rfind("Summary:"):]
    loudness = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summary)
    peak = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary)
    if not loudness or not peak:
        fail(f"could not read loudness while {what}")
    value = float(loudness.group(1)) if loudness.group(1) != "-inf" else -120.0
    if value < -60:
        fail(f"the audio is silent or nearly so while {what} ({value:g} LUFS)")
    return value, float(peak.group(1)) if peak.group(1) != "-inf" else -120.0


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        fail(f"cannot read the duration of {path}")


def num(x: float) -> str:
    return f"{x:.6f}".rstrip("0").rstrip(".") if x != int(x) else str(int(x))


def piecewise(points: list[tuple[float, float]]) -> str:
    """FFmpeg expression for a piecewise-linear curve through (time, value) points.

    A flat sum of gated terms rather than nested if() calls, so long envelopes stay within
    the expression parser's nesting limit.
    """
    (t0, v0), (tn, vn) = points[0], points[-1]
    terms = [f"lt(t,{num(t0)})*({num(v0)})"]
    for (ta, va), (tb, vb) in zip(points, points[1:]):
        if tb > ta:
            slope = (vb - va) / (tb - ta)
            terms.append(f"gte(t,{num(ta)})*lt(t,{num(tb)})*({num(va)}+({num(slope)})*(t-{num(ta)}))")
    terms.append(f"gte(t,{num(tn)})*({num(vn)})")
    return "+".join(terms)


def envelope(timeline: dict, total: float, a) -> list[tuple[float, float]]:
    """Bed gain keyframes in dB: ducked by default, swelling only inside transition regions."""
    duck, swell = a.duck_db, a.swell_db
    points = [(0.0, duck)]
    for region in sorted(timeline["transitions"], key=lambda r: r["start"]):
        kind = region["kind"]
        rise_from = region["start"] if kind == "intro" else region["start"] + a.release
        fall_to = min(region["end"], total) if kind == "outro" else region["end"] - a.preroll
        if fall_to - rise_from <= 0.05:
            continue  # too short to swell without touching the words around it
        up = 0.0 if kind == "intro" else a.ramp_up  # the intro starts already swelled
        down = 0.0 if kind == "outro" else a.ramp_down  # the outro never ducks again
        room = fall_to - rise_from
        if up + down <= room:
            seq = [(rise_from, duck), (rise_from + up, swell), (fall_to - down, swell), (fall_to, duck)]
        else:  # no room for full ramps: rise and fall at their normal rates and turn where they meet
            turn = rise_from + room * up / (up + down)
            reach = (turn - rise_from) / up if up else room / down
            seq = [(rise_from, duck), (turn, duck + (swell - duck) * min(reach, 1.0)), (fall_to, duck)]
        if kind == "intro":
            seq = seq[1:]
        if kind == "outro":
            seq = seq[:-1]
        points += seq
    points.sort(key=lambda p: p[0])  # stable: a later keyframe at the same time wins below
    merged = []
    for t, v in points:
        if merged and abs(merged[-1][0] - t) < 1e-6:
            merged[-1] = (t, v)
        else:
            merged.append((t, v))
    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("narration", type=Path, help="master-narration.wav from generate-tts-and-cues.py")
    ap.add_argument("bgm", type=Path, help="the selected Suno bed (wav, mp3, m4a ...)")
    ap.add_argument("timeline", type=Path, help="resolved-timeline.json")
    ap.add_argument("output", type=Path, help="master-audio.wav")
    ap.add_argument("--duck-db", type=float, default=-18.0, help="bed level under speech (-18)")
    ap.add_argument("--swell-db", type=float, default=-2.0, help="bed level in swells, intro and outro (-2)")
    ap.add_argument("--pocket-db", type=float, default=-3.0, help="vocal-pocket dip while ducked (-3)")
    ap.add_argument("--pocket-hz", type=float, default=1500.0, help="vocal-pocket centre (1500)")
    ap.add_argument("--preroll", type=float, default=0.3, help="bed is fully ducked this long before speech (0.3)")
    ap.add_argument("--release", type=float, default=0.25, help="wait after speech before a swell rises (0.25)")
    ap.add_argument("--ramp-up", type=float, default=0.8, help="swell rise time (0.8)")
    ap.add_argument("--ramp-down", type=float, default=0.5, help="duck fall time before speech (0.5)")
    ap.add_argument("--voice-lufs", type=float, default=-14.0)
    ap.add_argument("--bgm-ref-lufs", type=float, default=-14.0, help="bed loudness the dB levels refer to (-14)")
    ap.add_argument("--target-lufs", type=float, default=-14.0)
    ap.add_argument("--true-peak", type=float, default=-1.0)
    ap.add_argument("--bgm-offset", type=float, help="seconds trimmed from the bed head (negative delays it)")
    ap.add_argument("--fade-out", type=float, default=2.0, help="bed fade at the very end (2)")
    ap.add_argument("--loop-bgm", action="store_true", help="loop a bed shorter than the lesson (hard loop)")
    ap.add_argument("--dry-run", action="store_true", help="print the envelope and filter graph, render nothing")
    ap.add_argument("--force", action="store_true", help="overwrite the output")
    a = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        fail("FFmpeg and FFprobe must be on PATH")
    for path in (a.narration, a.bgm, a.timeline):
        if not path.exists():
            fail(f"{path} does not exist")
    if a.output.exists() and not a.force and not a.dry_run:
        fail(f"{a.output} exists; pass --force to replace it")
    if a.duck_db >= a.swell_db:
        fail("--duck-db must be below --swell-db")
    if min(a.preroll, a.release, a.ramp_up, a.ramp_down, a.fade_out) < 0:
        fail("times must not be negative")
    try:
        timeline = json.loads(a.timeline.read_text())
        timeline["transitions"], timeline["duration"]
    except (ValueError, KeyError) as exc:
        fail(f"{a.timeline} is not a resolved timeline: {exc}")

    total = duration(a.narration)
    if abs(total - timeline["duration"]) > 0.05:
        print(f"warning: narration lasts {total:.3f} s but the timeline says {timeline['duration']:.3f} s; "
              "the narration audio wins", file=sys.stderr)
    offset = a.bgm_offset if a.bgm_offset is not None else (timeline.get("bgm") or {}).get("offset", 0.0)
    bed_length = duration(a.bgm) - offset
    if bed_length < total and not a.loop_bgm:
        print(f"warning: the bed covers {max(bed_length, 0):.1f} s of {total:.1f} s; the rest is silent. "
              "Extend it in Suno or pass --loop-bgm", file=sys.stderr)

    points = envelope(timeline, total, a)
    ducked = [(t, (a.swell_db - v) / (a.swell_db - a.duck_db)) for t, v in points]  # 1 = fully ducked
    gain_db, weight = piecewise(points), piecewise(ducked)
    dipped = f"pow(10,({gain_db})/20)*({weight})"
    flat = f"pow(10,({gain_db})/20)*(1-({weight}))"

    # The closing fade never starts under the last words, however short the outro is.
    last_word = max((seg.get("speech_end", 0.0) for seg in timeline.get("segments", [])), default=0.0)
    fade_start = min(max(total - a.fade_out, last_word), total - 0.01)
    voice_chain = (f"[0:a]aformat=sample_fmts=fltp:sample_rates={RATE}:channel_layouts=mono,"
                   "highpass=f=80,equalizer=f=3500:t=q:w=1.0:g=2,pan=stereo|c0=c0|c1=c0")
    if offset >= 0:
        shift = f"atrim=start={num(offset)},asetpts=PTS-STARTPTS"
    else:
        shift = f"adelay=delays={int(round(-offset * 1000))}:all=1"
    bed_chain = (f"[1:a]aformat=sample_fmts=fltp:sample_rates={RATE}:channel_layouts=stereo,{shift},"
                 f"apad,atrim=end={num(total)}")
    loop = ["-stream_loop", "-1"] if a.loop_bgm else []
    inputs = ["-i", str(a.narration), *loop, "-i", str(a.bgm)]

    if a.dry_run:
        print("bed envelope (time s, dB):", ", ".join(f"({t:.2f}, {v:g})" for t, v in points))
    voice_lufs, _ = measure(inputs[:2], voice_chain + ",", "measuring the narration")
    bgm_lufs, _ = measure(inputs, bed_chain + ",", "measuring the bed")
    voice_gain, bed_gain = a.voice_lufs - voice_lufs, a.bgm_ref_lufs - bgm_lufs
    graph = ";".join([
        f"{voice_chain},volume={num(voice_gain)}dB[v]",
        f"{bed_chain},volume={num(bed_gain)}dB,asetnsamples=n=256:p=0,asplit=2[bd][bf]",
        f"[bd]equalizer=f={num(a.pocket_hz)}:t=q:w=1:g={num(a.pocket_db)},volume='{dipped}':eval=frame[b1]",
        f"[bf]volume='{flat}':eval=frame[b2]",
        f"[b1][b2]amix=inputs=2:normalize=0,afade=t=out:st={num(fade_start)}:d={num(total - fade_start)}[b]",
        "[v][b]amix=inputs=2:duration=first:normalize=0[mix]",
    ])
    if a.dry_run:
        print(f"narration {voice_lufs:.1f} LUFS -> gain {voice_gain:+.1f} dB; bed {bgm_lufs:.1f} LUFS -> gain {bed_gain:+.1f} dB")
        print("filter graph:", graph)
        return 0

    with tempfile.TemporaryDirectory() as work:
        premix = Path(work) / "premix.wav"
        ffmpeg([*inputs, "-filter_complex", graph, "-map", "[mix]", "-c:a", "pcm_f32le", "-ar", str(RATE),
                "-t", num(total), str(premix)], "mixing")
        mix_lufs, _ = measure(["-i", str(premix)], "[0:a]", "measuring the premix")
        ceiling = 10 ** ((a.true_peak - 0.5) / 20)  # sample-peak limiter, half a dB under the true-peak ceiling
        master = (f"[0:a]volume={num(a.target_lufs - mix_lufs)}dB,"
                  f"alimiter=limit={num(ceiling)}:level=disabled:latency=1:attack=5:release=80")
        a.output.parent.mkdir(parents=True, exist_ok=True)
        ffmpeg(["-y", "-i", str(premix), "-filter_complex", master, "-c:a", "pcm_s24le", "-ar", str(RATE),
                str(a.output)], "mastering")
    final_lufs, final_peak = measure(["-i", str(a.output)], "[0:a]", "verifying the master")
    swells = len(timeline["transitions"])
    print(f"wrote {a.output}: {total:.2f} s, {final_lufs:.1f} LUFS integrated, {final_peak:.1f} dBTP true peak")
    print(f"  narration {voice_lufs:.1f} -> {a.voice_lufs:g} LUFS; bed {bgm_lufs:.1f} LUFS referenced to {a.bgm_ref_lufs:g}; "
          f"bed {a.duck_db:g} dB under speech, {a.swell_db:g} dB in {swells} swell regions; offset {offset:g} s")
    if abs(final_lufs - a.target_lufs) > 0.5:
        print(f"warning: {final_lufs:.1f} LUFS misses the {a.target_lufs:g} target by more than 0.5 LU "
              "(the limiter took off more than expected)", file=sys.stderr)
    if final_peak > a.true_peak:
        print(f"warning: true peak {final_peak:.1f} dBTP exceeds {a.true_peak:g}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
