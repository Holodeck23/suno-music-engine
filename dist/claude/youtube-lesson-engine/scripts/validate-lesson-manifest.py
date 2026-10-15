#!/usr/bin/env python3
"""Validate a lesson-manifest.json against its schema and the Dave Dark structure.

Field names, enums and patterns come from references/lesson-manifest.schema.json, the single
source of truth for structure. This script adds the rules a JSON Schema cannot express:
segment numbering and phase order, 3-4 Mechanism blocks, the 15-second hook budget, filler
openers, trigger words that must occur in the narration, and trigger targets that must exist.

Usage:
  python3 validate-lesson-manifest.py lesson-manifest.json [--wpm 150] [--strict] [--json]

Durations are word-count estimates for planning only; the rendered narration audio is the
timing authority. Reads the manifest and schema, writes nothing, uses no network.
Exit status: 0 valid (warnings allowed), 1 errors (or warnings with --strict), 2 unreadable input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = Path(__file__).resolve().parent.parent / "references" / "lesson-manifest.schema.json"
PHASES = ("hook", "mechanism", "proof", "verdict")
HOOK_SECONDS, DROP_SECONDS = 15.0, 3.0
MIN_MINUTES, MAX_MINUTES = 3.0, 6.0
MAX_SECONDS_PER_VISUAL_BEAT = 40.0
FILLER = re.compile(r"^\W*(hey|hi|hello|yo|what'?s up|welcome|in (this|today'?s) video|today,? (we|i)\b"
                    r"|so,? today|before we (start|begin|get started))", re.I)
TTS_HAZARDS = re.compile(r"[`{}<>_\\|]|https?://")
STRIP = "\"'.,;:!?()[]{}“”‘’…"


def schema_errors(value, schema, root, path="$"):
    """Yield (path, message) for the JSON Schema keywords the lesson schema uses."""
    if "$ref" in schema:
        schema = root["$defs"][schema["$ref"].rsplit("/", 1)[-1]]
    kind = schema.get("type")
    if kind and not isinstance(value, {"object": dict, "array": list, "string": str}[kind]):
        yield path, f"expected {kind}"
        return
    if "enum" in schema and value not in schema["enum"]:
        yield path, f"must be one of: {', '.join(schema['enum'])}"
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            yield path, "must not be empty"
        if len(value) > schema.get("maxLength", float("inf")):
            yield path, f"longer than {schema['maxLength']} characters"
        pattern = schema.get("pattern")
        # JSON Schema's "$" means end of string; Python's also matches before a final newline.
        if pattern and not re.search(pattern[:-1] + r"\Z" if pattern.endswith("$") else pattern, value):
            yield path, f"does not match {pattern}"
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            yield path, f"needs at least {schema['minItems']} items"
        for i, item in enumerate(value):
            yield from schema_errors(item, schema.get("items", {}), root, f"{path}[{i}]")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                yield path, f"missing required field '{key}'"
        props = schema.get("properties", {})
        for key, item in value.items():
            if key not in props:
                if schema.get("additionalProperties") is False:
                    yield f"{path}.{key}", "unknown field"
            else:
                yield from schema_errors(item, props[key], root, f"{path}.{key}")


def words(text: str) -> list[str]:
    return [t.strip(STRIP) for t in text.split() if any(c.isalnum() for c in t)]


def clock(seconds: float) -> str:
    return f"{int(seconds // 60)}:{seconds % 60:04.1f}"


def check(manifest: dict, wpm: float):
    errors, warnings = [], []
    segs = manifest["segments"]
    hook_cap = int((HOOK_SECONDS - DROP_SECONDS) * wpm / 60)
    rank, seen, blocks, last_block = -1, set(), 0, None
    counts = dict.fromkeys(PHASES, 0)
    timeline, t = [], 0.0

    for i, seg in enumerate(segs):
        sid, payload = seg["id"], seg["visual_payload"]
        err = lambda msg: errors.append((sid, msg))
        warn = lambda msg: warnings.append((sid, msg))
        number, phase, slug = re.fullmatch(r"seg_(\d{2})_([a-z]+)_?(.*)", sid).groups()
        if sid in seen:
            err("duplicate segment id")
        seen.add(sid)
        if int(number) != i + 1:
            err(f"segment number {number} out of sequence (expected {i + 1:02d})")
        if PHASES.index(phase) < rank:
            err(f"'{phase}' after '{PHASES[rank]}': order must be hook, mechanism, proof, verdict")
        rank = max(rank, PHASES.index(phase))
        counts[phase] += 1
        if phase == "mechanism" and (not slug or slug != last_block):
            blocks += 1
        last_block = slug if phase == "mechanism" else None

        narration, state, mode = seg["narration"], seg["visual_state"], seg["bgm_mode"]
        n = len(words(narration))
        if not n:
            err("narration has no spoken words")
        if TTS_HAZARDS.search(narration):
            warn("narration contains symbols or a URL the voice will read literally; spell it out")

        code, nodes = payload.get("code_snippet"), payload.get("diagram_nodes")
        if state == "code_focus" and not code:
            err("code_focus needs visual_payload.code_snippet")
        if state == "architecture_graph" and not nodes:
            err("architecture_graph needs visual_payload.diagram_nodes")
        for entry in nodes or []:
            if "->" in entry and not all(part.strip() for part in entry.split("->")):
                err(f"diagram entry '{entry}' has an empty node around '->'")

        tokens, cursor = words(narration), 0
        triggers = payload.get("highlight_triggers", [])
        for trig in triggers:
            word, action = trig["word"].strip(STRIP), trig["action"]
            hit = next((j for j in range(cursor, len(tokens)) if tokens[j] == word), None)
            if hit is None:
                near = any(tok.lower() == word.lower() for tok in tokens[cursor:])
                err(f"trigger word '{word}' not found in narration after the previous trigger"
                    + (" (case differs)" if near else ""))
            else:
                cursor = hit + 1
            target = re.fullmatch(r"(?:reveal|highlight)_(line|node)_(\d+)", action)
            if target:
                kind, idx = target.group(1), int(target.group(2))
                have = len(code.splitlines()) if kind == "line" and code else len(nodes or []) if kind == "node" else 0
                if idx > have:
                    source = "code_snippet lines" if kind == "line" else "diagram_nodes entries"
                    err(f"'{action}' targets {kind} {idx} but there are {have} {source}")
            elif action == "show_headline" and not payload.get("headline"):
                err("'show_headline' needs visual_payload.headline")
            elif action == "drop" and state != "vibe_drop":
                err("'drop' is only valid in a vibe_drop segment")
        revealed = [int(t["action"].rsplit("_", 1)[1]) for t in triggers if t["action"].startswith("reveal_line_")]
        if code and revealed and max(revealed) < len(code.splitlines()):
            warn(f"code lines {max(revealed) + 1}-{len(code.splitlines())} are never revealed")

        seconds = n * 60 / wpm
        if phase == "hook":
            if i:
                err("the hook must be the first segment")
            if state != "vibe_drop":
                err("the hook must use visual_state 'vibe_drop' (it ends on the 3-second visual drop)")
            if mode != "full_swell":
                warn("the hook normally rides the building BGM intro ('full_swell')")
            if n > hook_cap:
                err(f"hook narration is {n} words; at {wpm:g} wpm the cap is {hook_cap} "
                    f"({HOOK_SECONDS - DROP_SECONDS:g} s plus the {DROP_SECONDS:g} s drop)")
            if FILLER.search(narration):
                err("the hook opens with greeting or filler; state the problem in the first words")
            seconds += DROP_SECONDS
        elif phase in ("mechanism", "proof") and mode == "full_swell":
            warn("full_swell under dense explanation competes with the voice; prefer 'ducked'")
        if phase == "proof" and state == "vibe_drop":
            warn("Proof should show the implementation, terminal flow or benchmark, not a vibe shot")
        if seconds / (1 + len(triggers)) > MAX_SECONDS_PER_VISUAL_BEAT:
            warn(f"about {seconds:.0f} s with {len(triggers)} triggers; nothing changes on screen for "
                 f"over {MAX_SECONDS_PER_VISUAL_BEAT:g} s at a time; add a trigger or split the segment")
        timeline.append({"id": sid, "start": round(t, 1), "end": round(t + seconds, 1), "words": n})
        t += seconds

    if counts["hook"] != 1:
        errors.append(("manifest", f"needs exactly one hook segment (found {counts['hook']})"))
    if not 3 <= blocks <= 4:
        errors.append(("manifest", f"needs 3-4 Mechanism blocks (found {blocks}); consecutive "
                                   "mechanism segments sharing a slug form one block"))
    for phase in ("proof", "verdict"):
        if not counts[phase]:
            errors.append(("manifest", f"needs at least one {phase} segment"))
    if not MIN_MINUTES * 60 <= t <= MAX_MINUTES * 60:
        warnings.append(("manifest", f"estimated runtime {clock(t)} is outside "
                                     f"{MIN_MINUTES:g}-{MAX_MINUTES:g} minutes at {wpm:g} wpm"))
    if len(manifest["title"]) > 70:
        warnings.append(("manifest", "titles over about 70 characters are often truncated in search"))
    return errors, warnings, timeline, t


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--schema", type=Path, default=SCHEMA)
    ap.add_argument("--wpm", type=float, default=150.0, help="narration rate for estimates (default 150)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--json", action="store_true", help="print a machine-readable report")
    a = ap.parse_args()
    if a.wpm <= 0:
        ap.error("--wpm must be positive")
    try:
        schema = json.loads(a.schema.read_text())
        manifest = json.loads(a.manifest.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read input: {exc}", file=sys.stderr)
        return 2

    errors = [(p, m) for p, m in schema_errors(manifest, schema, schema)]
    warnings, timeline, total = [], [], 0.0
    if not errors:  # structural checks passed, so the semantic pass can rely on field shapes
        errors, warnings, timeline, total = check(manifest, a.wpm)
    failed = bool(errors or (a.strict and warnings))

    if a.json:
        print(json.dumps({
            "valid": not failed,
            "errors": [{"where": w, "message": m} for w, m in errors],
            "warnings": [{"where": w, "message": m} for w, m in warnings],
            "estimate": {"wpm": a.wpm, "total_seconds": round(total, 1), "segments": timeline},
        }, indent=2))
        return int(failed)
    for label, items in (("ERROR", errors), ("WARN ", warnings)):
        for where, message in items:
            print(f"{label} {where}: {message}")
    plural = lambda n, word: f"{n} {word}{'' if n == 1 else 's'}"
    print(f"{a.manifest}: {plural(len(errors), 'error')}, {plural(len(warnings), 'warning')}")
    if timeline:
        print(f"estimate at {a.wpm:g} wpm (the rendered narration audio is the timing authority): {clock(total)}")
        for row in timeline:
            print(f"  {row['id']:<32} {clock(row['start']):>7} - {clock(row['end']):<7} {row['words']:>4} words")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
