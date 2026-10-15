#!/usr/bin/env python3
"""Narrate a lesson manifest and compile its resolved timeline.

Both providers write the same outputs into --out-dir:
  master-narration.wav    mono 48 kHz 16-bit narration, the timing authority for the lesson
  resolved-timeline.json  word, trigger, segment, transition, camera-move and chapter times
  chapters.txt            YouTube description chapters derived from the timeline

--provider elevenlabs
    POSTs each segment to /v1/text-to-speech/{voice_id}/with-timestamps (ELEVENLABS_API_KEY),
    decodes the base64 audio, turns the character alignment into word times, and stitches the
    segments with --pause between ordinary segments and --transition-pause around full_swell
    segments (the hook drop and the verdict swell). Neighbouring narration is sent as
    previous_text/next_text for continuous prosody. Responses are cached in
    OUT/tts-cache/, so a rerun with unchanged text, voice and settings is not billed again.
--provider local-audio --audio-file VOICE
    Aligns a recorded voiceover or local TTS file to the manifest narration with the matching
    logic of align-lyric-words.py (Whisper word timestamps; mlx-whisper on Apple silicon,
    faster-whisper elsewhere). The transcript is kept in OUT/narration.raw.json and reused on
    reruns; --transcript supplies one directly. The recording's own pauses are kept unless
    --restitch re-cuts it per segment and applies the configured pauses.

Usage:
  ELEVENLABS_API_KEY=... python3 generate-tts-and-cues.py lesson-manifest.json --out-dir build \\
      --provider elevenlabs [--model-id eleven_multilingual_v2] [--output-format mp3_44100_128]
  uv run --python 3.12 --with mlx-whisper python generate-tts-and-cues.py lesson-manifest.json \\
      --out-dir build --provider local-audio --audio-file voiceover.wav [--restitch]

The manifest must pass validate-lesson-manifest.py first. Needs FFmpeg and FFprobe on PATH.
Refuses to overwrite outputs without --force. Only the elevenlabs provider sends anything over
the network: the segment text and voice settings, to the configured API base.
"""
from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import wave
from array import array
from pathlib import Path

HERE = Path(__file__).resolve().parent
RATE = 48000
sys.dont_write_bytecode = True  # importing the helper scripts must not litter an installed skill
DROP_SECONDS = 3.0
MIN_CHAPTER_SECONDS = 10.0
MIN_SWELL_SECONDS = 0.5  # shorter lead-in or tail silence is not an intro or outro
OUTPUTS = ("master-narration.wav", "resolved-timeline.json", "chapters.txt")


def load_helper(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_helper("lesson_validator", "validate-lesson-manifest.py")
aligner = load_helper("lyric_aligner", "align-lyric-words.py")


def fail(message: str):
    raise SystemExit(f"error: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tokens(text: str) -> list[dict]:
    """Spoken tokens with character spans; same tokens, same order as the validator's words()."""
    found = []
    for match in re.finditer(r"\S+", text):
        raw = match.group()
        if not any(c.isalnum() for c in raw):
            continue
        core = raw.strip(validator.STRIP)
        start = match.start() + len(raw) - len(raw.lstrip(validator.STRIP))
        found.append({"w": core, "c0": start, "c1": start + len(core)})
    return found


def decode(path: Path, raw_rate: int = 0) -> array:
    """Decode any audio FFmpeg reads to mono 48 kHz signed 16-bit samples."""
    source = ["-f", "s16le", "-ar", str(raw_rate), "-ac", "1"] if raw_rate else []
    proc = subprocess.run(["ffmpeg", "-v", "error", *source, "-i", str(path), "-f", "s16le",
                           "-ac", "1", "-ar", str(RATE), "-"], capture_output=True)
    if proc.returncode:
        fail(f"FFmpeg could not decode {path}: {proc.stderr.decode(errors='replace').strip()}")
    samples = array("h")
    samples.frombytes(proc.stdout)
    if sys.byteorder == "big":
        samples.byteswap()
    return samples


def write_wav(path: Path, samples: array):
    data = array("h", samples)
    if sys.byteorder == "big":
        data.byteswap()
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(data.tobytes())


def fill_gaps(times: list, lo: float, hi: float, owner: list | None = None, nominal: float = 0.3) -> list:
    """Time each run of unheard words from its heard neighbours.

    Inside one segment the run is spread evenly between its neighbours. A run that crosses a
    segment boundary (``owner`` gives each word's segment) is packed against the neighbour in
    the same segment at about ``nominal`` seconds a word, so a missed first word lands just
    before the speech it belongs to instead of in the pause before it.
    """
    times = list(times)
    owner = owner or [0] * len(times)
    i = 0
    while i < len(times):
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < len(times) and times[j] is None:
            j += 1
        left = times[i - 1][1] if i else lo
        right = max(times[j][0] if j < len(times) else hi, left)
        left_seg = owner[i - 1] if i else None
        right_seg = owner[j] if j < len(times) else None
        run = list(range(i, j))
        if left_seg == right_seg:
            head, tail, middle = [], [], run
        else:
            head = [k for k in run if owner[k] == left_seg]
            tail = [k for k in run if owner[k] == right_seg]
            middle = [k for k in run if owner[k] not in (left_seg, right_seg)]
        step = min(nominal, (right - left) / len(run)) if head or tail else 0.0
        for n, k in enumerate(head):
            times[k] = (left + n * step, left + (n + 1) * step, "interp")
        for n, k in enumerate(reversed(tail)):
            times[k] = (right - (n + 1) * step, right - n * step, "interp")
        lo_mid, hi_mid = left + len(head) * step, right - len(tail) * step
        for n, k in enumerate(middle):
            width = (hi_mid - lo_mid) / len(middle)
            times[k] = (lo_mid + n * width, lo_mid + (n + 1) * width, "interp")
        i = j
    return times


def tidy(times: list, duration: float) -> list[dict]:
    """Clamp to the clip, keep starts monotonic and give every word a visible minimum length."""
    words, last = [], 0.0
    for start, end, src in times:
        start = min(max(start, last, 0.0), duration)
        end = min(max(end, start + 0.02), duration)
        words.append({"start": start, "end": end, "src": src})
        last = start
    return words


# ---------------------------------------------------------------- elevenlabs provider

def elevenlabs_request(args, key: str, voice: str, payload: dict, label: str) -> dict:
    query = urllib.parse.urlencode({"output_format": args.output_format})
    url = (f"{args.api_base.rstrip('/')}/v1/text-to-speech/{urllib.parse.quote(voice, safe='')}"
           f"/with-timestamps?{query}")
    body = json.dumps(payload).encode()
    for attempt in range(args.retries + 1):
        request = urllib.request.Request(url, data=body, method="POST", headers={
            "xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                payload_text = response.read()
            try:
                return json.loads(payload_text)
            except ValueError:
                fail(f"ElevenLabs returned a non-JSON response for {label}")
        except urllib.error.HTTPError as exc:
            detail = exc.read()[:400].decode(errors="replace")
            retryable = exc.code == 429 or exc.code >= 500
            if not retryable or attempt == args.retries:
                fail(f"ElevenLabs returned HTTP {exc.code} for {label}: {detail}")
        except OSError as exc:  # URLError, connection resets and socket timeouts
            if attempt == args.retries:
                fail(f"could not reach ElevenLabs for {label}: {exc}")
        wait = 2 ** (attempt + 1)
        print(f"  {label}: retrying in {wait} s", file=sys.stderr)
        time.sleep(wait)
    raise AssertionError("unreachable")


def alignment_times(text: str, toks: list[dict], alignment: dict, duration: float) -> list[dict]:
    chars, starts, ends = [], [], []
    for char, start, end in zip(alignment["characters"], alignment["character_start_times_seconds"],
                                alignment["character_end_times_seconds"]):
        for c in char:
            chars.append(c)
            starts.append(float(start))
            ends.append(float(end))
    spoken = "".join(chars)
    index = list(range(len(text))) if spoken == text else [None] * len(text)
    if spoken != text:  # the provider altered the text; map characters through a diff
        for block in difflib.SequenceMatcher(a=text, b=spoken, autojunk=False).get_matching_blocks():
            for k in range(block.size):
                index[block.a + k] = block.b + k
    times = []
    for tok in toks:
        mapped = [index[c] for c in range(tok["c0"], tok["c1"]) if index[c] is not None]
        times.append((starts[mapped[0]], ends[mapped[-1]], "elevenlabs") if mapped else None)
    return tidy(fill_gaps(times, 0.0, duration), duration)


def synthesize(args, manifest: dict, seg_tokens: list, out: Path):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        fail("set ELEVENLABS_API_KEY for --provider elevenlabs")
    fmt = args.output_format.split("_")
    if fmt[0] not in ("mp3", "wav", "pcm"):
        fail("--output-format must be an mp3_*, wav_* or pcm_* format")
    settings = json.loads(args.voice_settings) if args.voice_settings else None
    cache = out / "tts-cache"
    cache.mkdir(parents=True, exist_ok=True)
    segs, clips = manifest["segments"], []
    for i, seg in enumerate(segs):
        payload = {"text": seg["narration"], "model_id": args.model_id}
        if not args.no_context:
            if i:
                payload["previous_text"] = segs[i - 1]["narration"]
            if i + 1 < len(segs):
                payload["next_text"] = segs[i + 1]["narration"]
        if settings:
            payload["voice_settings"] = settings
        if args.seed is not None:
            payload["seed"] = args.seed
        identity = json.dumps({"voice": manifest["voice_id"], "format": args.output_format,
                               "payload": payload}, sort_keys=True)
        cached = cache / f"{seg['id']}-{hashlib.sha256(identity.encode()).hexdigest()[:16]}.json"
        if cached.exists():
            response = json.loads(cached.read_text())
            print(f"  {seg['id']}: cached")
        else:
            response = elevenlabs_request(args, key, manifest["voice_id"], payload, seg["id"])
            if not response.get("audio_base64") or not response.get("alignment"):
                fail(f"ElevenLabs response for {seg['id']} lacks audio_base64 or alignment")
            cached.write_text(json.dumps(response))
            print(f"  {seg['id']}: synthesized")
        audio = cached.with_suffix("." + ("raw" if fmt[0] == "pcm" else fmt[0]))
        audio.write_bytes(base64.b64decode(response["audio_base64"]))
        samples = decode(audio, int(fmt[1]) if fmt[0] == "pcm" else 0)
        duration = len(samples) / RATE
        words = alignment_times(seg["narration"], seg_tokens[i], response["alignment"], duration)
        clips.append({"samples": samples, "words": words})
    meta = {"provider": "elevenlabs", "voice_id": manifest["voice_id"], "model_id": args.model_id,
            "output_format": args.output_format, "context_stitching": not args.no_context}
    return clips, meta


# ---------------------------------------------------------------- local-audio provider

def voice_onset(samples: array, start: float, end: float, floor_db: float = -45.0,
                min_silence: float = 0.16) -> float | None:
    """Where the voice resumes after the last real pause in [start, end), in 40 ms RMS windows.

    Returns None when the span holds no pause of at least ``min_silence`` before voice, so a
    word that genuinely starts at ``start`` (or only has a short stop-consonant closure) is
    left alone. Speech from the previous word leaking into the span is skipped.
    """
    window = int(0.04 * RATE)
    floor = 32768 * 10 ** (floor_db / 20)
    voiced = []
    for pos in range(int(start * RATE), int(end * RATE) - window + 1, window):
        chunk = samples[pos:pos + window]
        voiced.append((pos, math.sqrt(sum(x * x for x in chunk) / window) > floor))
    onset, quiet = None, 0
    for pos, loud in voiced:
        if not loud:
            quiet += 1
        else:
            if quiet * window >= min_silence * RATE:
                onset = pos / RATE
            quiet = 0
    return onset


def align_recording(args, manifest: dict, seg_tokens: list, out: Path):
    if not args.audio_file:
        fail("--provider local-audio needs --audio-file")
    samples = decode(args.audio_file)
    duration = len(samples) / RATE
    sidecar = out / "narration.raw.json"
    if args.transcript:
        raw = json.loads(args.transcript.read_text())
    elif sidecar.exists():
        raw = json.loads(sidecar.read_text())
        print(f"  reusing transcript {sidecar}")
    else:
        prompt = " ".join(s["narration"] for s in manifest["segments"])
        raw = aligner.transcribe(args.audio_file, args.whisper_model, prompt, args.language)
        sidecar.write_text(json.dumps(raw, indent=1, default=float))
    heard = aligner.heard_words(raw)
    flat = [(i, j) for i, toks in enumerate(seg_tokens) for j in range(len(toks))]
    times = [None] * len(flat)
    for ki, hi in aligner.matched_pairs([aligner.norm(seg_tokens[i][j]["w"]) for i, j in flat],
                                        [h["n"] for h in heard]):
        times[ki] = (heard[hi]["start"], heard[hi]["end"], "whisper")
    matched = sum(t is not None for t in times)
    if matched < args.min_match * len(flat):
        fail(f"only {matched}/{len(flat)} narration words were heard in {args.audio_file}; "
             "is this the recording of this manifest?")
    words = tidy(fill_gaps(times, 0.0, duration, [i for i, _ in flat]), duration)
    per_seg = [[] for _ in seg_tokens]
    for (i, _), word in zip(flat, words):
        per_seg[i].append(word)
    for i, seg_words in enumerate(per_seg):
        first = seg_words[0]
        # Whisper stretches a phrase's first word back over the silence before it. Move the
        # start to where the voice actually begins (40 ms RMS against a fixed floor); a word
        # whose energy is already present at its start is left alone.
        if first["src"] == "whisper":
            floor = max(first["start"], per_seg[i - 1][-1]["end"] if i else 0.0)
            onset = voice_onset(samples, floor, first["end"])
            if onset is not None and onset > first["start"] + 0.02:
                first.update(start=onset, src="whisper+onset")
    meta = {"provider": "local-audio", "source_audio": str(args.audio_file),
            "source_sha256": sha256(args.audio_file), "whisper_model": args.whisper_model,
            "matched": matched, "total": len(flat)}
    if not args.restitch:
        return samples, per_seg, meta
    clips = []
    for i, seg_words in enumerate(per_seg):
        first, last = seg_words[0]["start"], seg_words[-1]["end"]
        prev_mid = (per_seg[i - 1][-1]["end"] + first) / 2 if i else 0.0
        next_mid = (last + per_seg[i + 1][0]["start"]) / 2 if i + 1 < len(per_seg) else duration
        lo, hi = max(prev_mid, first - 0.15), min(next_mid, last + 0.3)
        clip = samples[int(lo * RATE):int(hi * RATE)]
        clips.append({"samples": clip, "words": [dict(w, start=w["start"] - lo, end=w["end"] - lo)
                                                 for w in seg_words]})
    return clips, None, meta


# ---------------------------------------------------------------- timeline

def is_transition(segs: list, i: int) -> bool:
    return segs[i]["bgm_mode"] == "full_swell" or segs[i + 1]["bgm_mode"] == "full_swell"


def stitch(clips: list, segs: list, args):
    """Concatenate clips with configured pauses; return samples and per-segment absolute words."""
    out = array("h", bytes(2 * int(args.lead_in * RATE)))
    per_seg = []
    for i, clip in enumerate(clips):
        offset = len(out) / RATE
        out.extend(clip["samples"])
        per_seg.append([dict(w, start=w["start"] + offset, end=w["end"] + offset) for w in clip["words"]])
        if i + 1 < len(clips):
            gap = args.transition_pause if is_transition(segs, i) else args.pause
            out.extend(array("h", bytes(2 * int(gap * RATE))))
    out.extend(array("h", bytes(2 * int(args.outro * RATE))))
    return out, per_seg


def chapter_list(manifest: dict, segments: list, slots: list, duration: float) -> list[dict]:
    groups, block, last_slug = [], 0, None
    for seg in segments:
        phase, slug = seg["phase"], seg["block"]
        if phase == "mechanism":
            if not slug or slug != last_slug:
                block += 1
            key = ("mechanism", block)
        else:
            key = (phase, 0)
        last_slug = slug if phase == "mechanism" else None
        if not groups or groups[-1]["key"] != key:
            groups.append({"key": key, "segments": [seg]})
        else:
            groups[-1]["segments"].append(seg)
    starts = {slot.get("id"): slot["start"] for slot in slots}
    chapters = []
    for n, group in enumerate(groups):
        first = group["segments"][0]
        before = next((s for s in slots if s.get("before") == first["id"]), None)
        # The hook drop closes the hook's chapter; a swell opens the chapter it leads into.
        start = 0.0 if not n else before["end"] if before and before["kind"] == "drop" else \
            (before or {"start": starts[first["id"]]})["start"]
        headline = next((s["headline"] for s in group["segments"] if s.get("headline")), None)
        phase = group["key"][0]
        fallback = {"hook": "The problem", "proof": "The proof", "verdict": "The verdict"}.get(
            phase, (first["block"] or f"part {group['key'][1]}").replace("_", " ").capitalize())
        chapters.append({"time": float(int(start)), "title": headline or fallback})
    merged = True
    while merged and len(chapters) > 1:  # YouTube needs every chapter to last 10 s or more
        merged = False
        for k, chapter in enumerate(chapters):
            end = chapters[k + 1]["time"] if k + 1 < len(chapters) else duration
            if end - chapter["time"] < MIN_CHAPTER_SECONDS:
                if k == 0:  # the next chapter takes over 0:00
                    chapters[1]["time"] = 0.0
                del chapters[k]
                merged = True
                break
    return chapters if len(chapters) >= 3 else []


def clock(seconds: float, hours: bool) -> str:
    s = int(seconds)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if hours else f"{s // 60}:{s % 60:02d}"


def build_timeline(manifest: dict, seg_tokens: list, per_seg: list, duration: float, args) -> dict:
    segs = manifest["segments"]
    segments = []
    for seg, toks, words in zip(segs, seg_tokens, per_seg):
        number, phase, slug = re.fullmatch(r"seg_(\d{2})_([a-z]+)_?(.*)", seg["id"]).groups()
        cursor, triggers = 0, []
        for trig in seg["visual_payload"].get("highlight_triggers", []):
            target = trig["word"].strip(validator.STRIP)
            hit = next((j for j in range(cursor, len(toks)) if toks[j]["w"] == target), None)
            if hit is None:  # only reachable with --skip-validate
                print(f"warning: {seg['id']}: trigger word '{target}' not found; skipped", file=sys.stderr)
                continue
            cursor = hit + 1
            triggers.append({"word": trig["word"], "action": trig["action"], "word_index": hit,
                             "time": round(words[hit]["start"], 3)})
        segments.append({
            "id": seg["id"], "phase": phase, "block": slug, "visual_state": seg["visual_state"],
            "bgm_mode": seg["bgm_mode"], "headline": seg["visual_payload"].get("headline"),
            "speech_start": round(words[0]["start"], 3), "speech_end": round(words[-1]["end"], 3),
            "words": [{"w": t["w"], "start": round(w["start"], 3), "end": round(w["end"], 3),
                       "src": w["src"]} for t, w in zip(toks, words)],
            "triggers": triggers,
        })

    slots, transitions, cursor = [], [], 0.0
    if segments[0]["speech_start"] >= MIN_SWELL_SECONDS:
        transitions.append({"kind": "intro", "start": 0.0, "end": segments[0]["speech_start"],
                            "before": segments[0]["id"]})
        cursor = segments[0]["speech_start"]
    for i, seg in enumerate(segments):
        if i + 1 < len(segments):
            nxt = segments[i + 1]
            if is_transition(segs, i):
                kind = "drop" if seg["phase"] == "hook" else "swell"
                transitions.append({"kind": kind, "start": seg["speech_end"], "end": nxt["speech_start"],
                                    "after": seg["id"], "before": nxt["id"]})
                if kind == "drop":
                    transitions[-1]["drop_end"] = round(min(seg["speech_end"] + DROP_SECONDS,
                                                            nxt["speech_start"]), 3)
                end = seg["speech_end"]
            else:
                end = round((seg["speech_end"] + nxt["speech_start"]) / 2, 3)
        else:
            end = seg["speech_end"] if duration - seg["speech_end"] >= MIN_SWELL_SECONDS else duration
        slots.append({"kind": "segment", "id": seg["id"], "visual_state": seg["visual_state"],
                      "start": round(cursor, 3), "end": round(end, 3)})
        cursor = end
        if transitions and transitions[-1].get("after") == seg["id"]:
            cursor = transitions[-1]["end"]
    if duration - segments[-1]["speech_end"] >= MIN_SWELL_SECONDS:
        transitions.append({"kind": "outro", "start": segments[-1]["speech_end"], "end": round(duration, 3),
                            "after": segments[-1]["id"]})
    for tr in transitions:
        slots.append({"kind": tr["kind"], "visual_state": "vibe_drop", "start": tr["start"], "end": tr["end"],
                      **{k: tr[k] for k in ("after", "before") if k in tr}})
    slots.sort(key=lambda s: s["start"])

    events = [{"time": s["start"], "type": "slot", "kind": s["kind"], "visual_state": s["visual_state"],
               **({"segment": s["id"]} if "id" in s else {})} for s in slots]
    events += [{"time": t["time"], "type": "trigger", "segment": seg["id"], "word": t["word"],
                "action": t["action"]} for seg in segments for t in seg["triggers"]]
    events.sort(key=lambda e: e["time"])
    # Mobile legibility: something on screen must change at least every max_static seconds.
    moves, marks = [], [e["time"] for e in events] + [duration]
    for a, b in zip(marks, marks[1:]):
        extra = math.ceil((b - a) / args.max_static) - 1
        moves += [round(a + (b - a) * k / (extra + 1), 3) for k in range(1, extra + 1)]
    for t in moves:
        slot = next(s for s in reversed(slots) if s["start"] <= t)
        events.append({"time": t, "type": "camera_move", "visual_state": slot["visual_state"],
                       **({"segment": slot["id"]} if "id" in slot else {})})
    events.sort(key=lambda e: (e["time"], e["type"] != "slot"))

    chapters = chapter_list(manifest, segments, slots, duration)
    return {"segments": segments, "transitions": transitions, "slots": slots, "events": events,
            "chapters": chapters, "camera_moves": len(moves)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--provider", choices=("elevenlabs", "local-audio"), required=True)
    ap.add_argument("--pause", type=float, default=0.4, help="seconds between ordinary segments (0.4)")
    ap.add_argument("--transition-pause", type=float, default=3.5,
                    help="seconds before and after full_swell segments, incl. the 3 s hook drop (3.5)")
    ap.add_argument("--lead-in", type=float, default=0.0, help="silence before the hook (0)")
    ap.add_argument("--outro", type=float, default=4.0, help="silence after the verdict for the BGM outro (4)")
    ap.add_argument("--max-static", type=float, default=7.0,
                    help="longest time without a visual change before a camera move is inserted (7)")
    ap.add_argument("--wpm", type=float, default=150.0, help="narration rate for manifest validation")
    ap.add_argument("--skip-validate", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs")
    el = ap.add_argument_group("elevenlabs provider")
    el.add_argument("--model-id", default="eleven_multilingual_v2")
    el.add_argument("--output-format", default="mp3_44100_128",
                    help="mp3_*, wav_* or pcm_*; wav_44100/pcm_44100 need the Pro tier")
    el.add_argument("--voice-settings", help='JSON, e.g. \'{"stability": 0.5, "similarity_boost": 0.75}\'')
    el.add_argument("--seed", type=int)
    el.add_argument("--no-context", action="store_true", help="do not send previous_text/next_text")
    el.add_argument("--api-base", default="https://api.elevenlabs.io")
    el.add_argument("--timeout", type=float, default=120.0)
    el.add_argument("--retries", type=int, default=3)
    loc = ap.add_argument_group("local-audio provider")
    loc.add_argument("--audio-file", type=Path)
    loc.add_argument("--transcript", type=Path, help="Whisper JSON with word timestamps to use instead")
    loc.add_argument("--whisper-model", default=aligner.DEFAULT_MODEL)
    loc.add_argument("--language", default="en")
    loc.add_argument("--min-match", type=float, default=0.6, help="minimum share of words heard (0.6)")
    loc.add_argument("--restitch", action="store_true", help="re-cut the recording and apply --pause values")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            fail(f"{tool} is not on PATH")
    if min(args.pause, args.transition_pause, args.lead_in, args.outro) < 0 or args.max_static <= 0:
        fail("pauses must be zero or more and --max-static positive")
    if args.transition_pause < DROP_SECONDS:
        print(f"warning: --transition-pause under {DROP_SECONDS:g} s cuts the hook drop short", file=sys.stderr)
    try:
        manifest = json.loads(args.manifest.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read manifest: {exc}")
    schema = json.loads(validator.SCHEMA.read_text())
    structural = list(validator.schema_errors(manifest, schema, schema))
    errors, warnings = (structural, []) if structural else validator.check(manifest, args.wpm)[:2]
    for where, message in warnings:
        print(f"warning: {where}: {message}", file=sys.stderr)
    for where, message in errors:
        print(f"ERROR {where}: {message}", file=sys.stderr)
    if structural or (errors and not args.skip_validate):
        fail("the manifest is invalid; fix it with validate-lesson-manifest.py "
             "(--skip-validate bypasses structure rules only, never schema errors)")

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    existing = [name for name in OUTPUTS if (out / name).exists()]
    if existing and not args.force:
        fail(f"{', '.join(existing)} already exist in {out}; choose a fresh --out-dir or pass --force")

    seg_tokens = [tokens(s["narration"]) for s in manifest["segments"]]
    print(f"{args.provider}: {len(seg_tokens)} segments")
    if args.provider == "elevenlabs":
        clips, meta = synthesize(args, manifest, seg_tokens, out)
        samples, per_seg = stitch(clips, manifest["segments"], args)
    else:
        result, per_seg, meta = align_recording(args, manifest, seg_tokens, out)
        if per_seg is None:
            samples, per_seg = stitch(result, manifest["segments"], args)
        else:
            samples = result
            short = int(args.outro * RATE) - (len(samples) - int(per_seg[-1][-1]["end"] * RATE))
            if short > 0:  # leave room for the BGM outro after the last word
                samples.extend(array("h", bytes(2 * short)))
    duration = len(samples) / RATE

    narration_path = out / OUTPUTS[0]
    write_wav(narration_path, samples)
    parts = build_timeline(manifest, seg_tokens, per_seg, duration, args)
    manifest_dir = args.manifest.resolve().parent
    timeline = {
        "version": 1,
        "generated_by": "generate-tts-and-cues.py",
        "title": manifest["title"],
        "manifest": {"path": str(args.manifest), "sha256": sha256(args.manifest)},
        "bgm_track": str((manifest_dir / manifest["bgm_track"]).resolve()),
        "narration": dict(meta, path=OUTPUTS[0], sha256=sha256(narration_path), sample_rate=RATE,
                          duration=round(duration, 3)),
        "settings": {k: getattr(args, k) for k in ("pause", "transition_pause", "lead_in", "outro", "max_static")},
        "duration": round(duration, 3),
        **{k: parts[k] for k in ("segments", "transitions", "slots", "events", "chapters")},
        "bgm": None,
    }
    (out / OUTPUTS[1]).write_text(json.dumps(timeline, indent=1) + "\n")
    hours = duration >= 3600
    (out / OUTPUTS[2]).write_text("".join(f"{clock(c['time'], hours)} {c['title']}\n" for c in parts["chapters"]))

    kinds = [t["kind"] for t in parts["transitions"]]
    print(f"wrote {narration_path} ({clock(duration, hours)}), {out / OUTPUTS[1]}, {out / OUTPUTS[2]}")
    print(f"  transitions: {', '.join(kinds) or 'none'}; camera moves inserted: {parts['camera_moves']}; "
          f"chapters: {len(parts['chapters']) or 'none (YouTube needs 3+ of at least 10 s)'}")
    if "matched" in meta:
        print(f"  {meta['matched']}/{meta['total']} words heard; the rest interpolated. Check them against playback.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
