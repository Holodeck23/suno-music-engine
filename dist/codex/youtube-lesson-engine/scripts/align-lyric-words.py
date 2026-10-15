#!/usr/bin/env python3
"""Word-level lyric timing for kinetic typography.

Suno's embedded lyric track is line-level, and its cue times can run well ahead of the
recording (over 20 s late in the song in one observed case). Kinetic type needs every word.
This transcribes an isolated vocal stem with word timestamps, then aligns the KNOWN lyric
(from extract-video-timing.py output, never the transcript's spelling) onto the heard words.
Words that cannot be matched are interpolated inside their line and marked "interp".
generate-tts-and-cues.py reuses norm(), transcribe(), heard_words() and matched_pairs()
to align lesson narration the same way.

Usage:
  uv run --python 3.12 --with mlx-whisper python align-lyric-words.py \
      TIMING.json VOCALS.wav OUTPUT.json [--window 30] [--model mlx-community/whisper-large-v3-turbo]

TIMING.json: output of extract-video-timing.py (uses its "lyrics" cues).
VOCALS.wav:  an isolated vocal stem (e.g. demucs htdemucs_ft). The full mix works worse.
Writes OUTPUT.json plus OUTPUT.raw.json (the raw transcript, reused on reruns).
Refuses to overwrite OUTPUT.json without --force. Runs locally; uploads nothing.
Uses mlx-whisper on Apple silicon; elsewhere run with `--with faster-whisper` instead, which
maps the model name to its faster-whisper equivalent (large-v3-turbo by default).
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower().replace("’", "'"))


def transcribe(audio: Path, model: str, prompt: str, language: str = "en") -> dict:
    """Whisper word timestamps as {"segments": [{"words": [{"word", "start", "end"}]}]}."""
    try:
        import mlx_whisper
    except ImportError:
        mlx_whisper = None
    if mlx_whisper is not None:
        return mlx_whisper.transcribe(
            str(audio), path_or_hf_repo=model, word_timestamps=True,
            initial_prompt=prompt, language=language,
            condition_on_previous_text=False,
        )
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit("transcription needs mlx-whisper (Apple silicon) or faster-whisper, e.g. "
                         "uv run --python 3.12 --with faster-whisper python ...")
    name = model.rsplit("/", 1)[-1]
    name = name[len("whisper-"):] if name.startswith("whisper-") else name
    segments, _ = WhisperModel(name).transcribe(
        str(audio), word_timestamps=True, initial_prompt=prompt, language=language,
        condition_on_previous_text=False,
    )
    return {"segments": [{"text": s.text, "words": [{"word": w.word, "start": w.start, "end": w.end}
                                                    for w in s.words or []]} for s in segments]}


def heard_words(raw: dict) -> list[dict]:
    return [{"n": norm(w["word"]), "start": float(w["start"]), "end": float(w["end"])}
            for seg in raw["segments"] for w in seg.get("words", []) if norm(w["word"])]


def matched_pairs(known: list[str], heard: list[str]):
    """Yield (known index, heard index) for each word difflib aligns, in order."""
    sm = difflib.SequenceMatcher(a=known, b=heard, autojunk=False)
    for blk in sm.get_matching_blocks():
        for i in range(blk.size):
            yield blk.a + i, blk.b + i


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("timing", type=Path)
    ap.add_argument("vocals", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--window", type=float, default=30.0,
                    help="seconds after a Suno cue in which a heard word may match it")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if a.output.exists() and not a.force:
        print(f"refusing to overwrite {a.output} (use --force)", file=sys.stderr)
        return 1
    cues = json.loads(a.timing.read_text()).get("lyrics") or []
    if not cues:
        print("no lyric cues in timing file", file=sys.stderr)
        return 1

    raw_path = a.output.with_suffix(".raw.json")
    if raw_path.exists():
        raw = json.loads(raw_path.read_text())
    else:
        raw = transcribe(a.vocals, a.model, " ".join(c["text"] for c in cues))
        raw_path.write_text(json.dumps(raw, indent=1, default=float))

    heard = heard_words(raw)
    known = [{"w": tok, "n": norm(tok), "line": li}
             for li, c in enumerate(cues) for tok in c["text"].split() if norm(tok)]

    for ki, hi in matched_pairs([k["n"] for k in known], [h["n"] for h in heard]):
        k, h = known[ki], heard[hi]
        # The prompt can make Whisper "hear" later lyrics over an instrumental intro, and
        # repeated choruses invite cross-matches. Only accept words near their own cue.
        if cues[k["line"]]["start"] - 3.0 <= h["start"] <= cues[k["line"]]["start"] + a.window:
            k.update(start=h["start"], end=h["end"], src="whisper")

    lines = []
    for li, c in enumerate(cues):
        ws = [k for k in known if k["line"] == li]
        nxt = cues[li + 1]["start"] if li + 1 < len(cues) else c["start"] + 6
        lo, hi = c["start"], min(c.get("end", nxt), nxt)
        anchors = [(-1, lo)] + [(i, w["start"]) for i, w in enumerate(ws) if "start" in w] + [(len(ws), hi)]
        for (ia, ta), (ib, tb) in zip(anchors, anchors[1:]):
            for j in range(ia + 1, ib):
                ws[j].update(start=ta + (tb - ta) * (j - ia) / (ib - ia), src="interp")
                ws[j]["end"] = ws[j]["start"] + 0.25
        for i, w in enumerate(ws[:-1]):
            w["end"] = max(w["start"] + 0.08, min(w["end"], ws[i + 1]["start"]))
        lines.append({"text": c["text"], "start": ws[0]["start"] if ws else c["start"],
                      "end": ws[-1]["end"] if ws else c["start"],
                      "words": [{k: w[k] for k in ("w", "start", "end", "src")} for w in ws]})

    matched = sum(1 for k in known if k.get("src") == "whisper")
    a.output.write_text(json.dumps({"model": a.model, "vocals": a.vocals.name, "matched": matched,
                                    "total": len(known), "lines": lines}, indent=1))
    print(f"wrote {a.output}: {matched}/{len(known)} words matched, rest interpolated")
    print("Check the raw transcript for sung lines the sheet lacks (ad-libs, repeats).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
