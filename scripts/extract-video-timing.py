#!/usr/bin/env python3
"""Extract embedded lyric timings without uploading or transcribing the audio."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


def run(args):
    return subprocess.check_output(args, text=True, timeout=60)


def seconds(value):
    h, m, s = value.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('audio', type=Path)
    parser.add_argument('output', type=Path, help='Durable production-folder JSON path')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; preserve it or choose a revision filename.')
    metadata = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(args.audio)]))
    streams = [s for s in metadata['streams'] if s.get('codec_type') == 'subtitle']
    cues, sections = [], []
    if streams:
        srt = run(['ffmpeg', '-v', 'error', '-i', str(args.audio), '-map', f"0:{streams[0]['index']}", '-f', 'srt', '-'])
        for block in re.split(r'\n\s*\n', srt.strip()):
            lines = block.splitlines()
            if len(lines) < 3 or ' --> ' not in lines[1]:
                continue
            start, end = [seconds(t.strip()) for t in lines[1].split(' --> ')]
            text = ' '.join(lines[2:]).strip()
            if text.startswith('['):
                sections.append({'start': start, 'text': text})
            elif end > start and text:
                cues.append({'start': start, 'end': end, 'text': text, 'verified': False})
    digest = hashlib.sha256()
    with args.audio.open('rb') as audio:
        for chunk in iter(lambda: audio.read(1024 * 1024), b''):
            digest.update(chunk)
    result = {
        'audioSha256': digest.hexdigest(),
        'duration': float(metadata['format']['duration']),
        'timingSource': 'embedded subtitles' if cues else 'no usable embedded subtitles',
        'timingVerified': False,
        'lyrics': cues,
        'sectionCues': sections,
        'reviewFlags': [c for c in cues if c['end'] - c['start'] < .5 or c['end'] - c['start'] > 7],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects against a concurrent writer after the check.
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(f"{len(cues)} lyric cues; {len(result['reviewFlags'])} timing flags; wrote {args.output}")


if __name__ == '__main__':
    main()
