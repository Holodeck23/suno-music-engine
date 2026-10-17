#!/usr/bin/env python3
"""Quantified visual-look gate: measure median brightness, hot-pixel fraction (>128),
dominant quantised ground colours, and mean top-400 most-saturated accent colour.

Converts 'it doesn't look right' into numbers that can be compared directly against
a reference film's frames before shipping a look or starting a long render.

Reference benchmark (LGTM, 3TNpOD6bov8, chorus frames, measured 2026-10-16):
  median pixel value : 18 - 24
  pixels > 128       : 1.8% - 4.6%
  ground (quantised) : #000010 - #101020 (blue-dominant dark carbon)
  accent (top-400)   : #38EE82

Usage:
  python3 scripts/measure-frame-look.py FRAME.png [FRAME2.png ...]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from pathlib import Path


def load_rgb_bytes(path: Path, width: int = 480, height: int = 270) -> bytes:
    """Decode any image or single video frame to raw rgb24 via ffmpeg (no PIL/numpy dependency required)."""
    cmd = [
        "ffmpeg", "-v", "error", "-i", str(path),
        "-vf", f"scale={width}:{height}",
        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ]
    return subprocess.check_output(cmd, timeout=30)


def measure_image(path: Path) -> dict[str, object]:
    raw = load_rgb_bytes(path)
    n_px = len(raw) // 3
    if n_px == 0:
        raise ValueError(f"decoded 0 pixels from {path}")

    all_channels: list[int] = list(raw)
    all_channels.sort()
    mid = len(all_channels) // 2
    median_val = (
        all_channels[mid]
        if len(all_channels) % 2 == 1
        else 0.5 * (all_channels[mid - 1] + all_channels[mid])
    )
    above_128 = sum(1 for v in all_channels if v > 128) / len(all_channels) * 100.0

    quant_counts: Counter[tuple[int, int, int]] = Counter()
    sat_pixels: list[tuple[int, int, int, int]] = []  # (sat_score, r, g, b)

    for i in range(0, len(raw), 3):
        r, g, b = raw[i], raw[i + 1], raw[i + 2]
        qr = (r >> 4) << 4
        qg = (g >> 4) << 4
        qb = (b >> 4) << 4
        quant_counts[(qr, qg, qb)] += 1
        mx = max(r, g, b)
        mn = min(r, g, b)
        sat_pixels.append((mx - mn, r, g, b))

    top_ground = [
        f"#{r:02X}{g:02X}{b:02X} ({cnt / n_px * 100:.1f}%)"
        for (r, g, b), cnt in quant_counts.most_common(3)
    ]

    sat_pixels.sort(key=lambda x: x[0], reverse=True)
    top_k = sat_pixels[:400]
    ar = round(sum(p[1] for p in top_k) / len(top_k))
    ag = round(sum(p[2] for p in top_k) / len(top_k))
    ab = round(sum(p[3] for p in top_k) / len(top_k))
    accent_hex = f"#{ar:02X}{ag:02X}{ab:02X}"

    return {
        "file": path.name,
        "median": median_val,
        "pct_gt_128": above_128,
        "ground": top_ground,
        "accent": accent_hex,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", type=Path, help="Image file(s) or directory of PNG/JPG stills")
    args = ap.parse_args()

    paths: list[Path] = []
    for p in args.inputs:
        if p.is_dir():
            paths.extend(sorted(x for x in p.iterdir() if x.suffix.lower() in {".png", ".jpg", ".jpeg"}))
        else:
            paths.append(p)

    if not paths:
        print("no image files found", file=sys.stderr)
        return 1

    print(f"{'FILE':22s} | {'MEDIAN':>6s} | {'%>128':>6s} | {'ACCENT':>7s} | TOP QUANTISED GROUND COLOURS")
    print("-" * 92)
    for p in paths:
        m = measure_image(p)
        g_str = ", ".join(m["ground"])  # type: ignore[arg-type]
        print(f"{m['file']:22s} | {m['median']:6.1f} | {m['pct_gt_128']:5.1f}% | {m['accent']:>7s} | {g_str}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
