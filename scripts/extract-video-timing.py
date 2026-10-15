#!/usr/bin/env python3
"""Extract timing from a selected recording without uploading or transcribing it.

By default this reads embedded lyric cues (Suno M4A downloads can carry a timed mov_text
track), section cues, the measured duration and the audio SHA256.

--beats adds music timing for the visual engine: beats, estimated downbeats, onsets, the
measured tempo range and an RMS envelope in dBFS (absolute, so a quiet layer stays quiet).
--stem NAME=PATH (repeatable) adds onsets and an envelope per separated stem.
--merge-into TIMELINE writes those markers into a resolved-timeline.json from
generate-tts-and-cues.py, in program time (BGM time minus --bgm-offset). It also records each
slot's nearest beat, and the offset that would land a downbeat exactly on the hook drop.

Usage:
  python3 extract-video-timing.py AUDIO OUTPUT.json
  uv run --python 3.12 --with librosa python extract-video-timing.py BGM.wav BGM-TIMING.json --beats \\
      [--stem drums=drums.wav --stem bass=bass.wav] \\
      [--merge-into build/resolved-timeline.json --bgm-offset 2.5]

Needs FFmpeg and FFprobe; --beats also needs librosa. Refuses to overwrite OUTPUT.json.
--merge-into replaces only the timeline's "bgm" key, atomically, and will not replace an
existing one without --force-merge. Downbeats are estimated from low-frequency energy, and
every extracted cue or beat is unverified until checked against playback.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ANALYSIS_RATE = 22050
SNAP_SECONDS = 0.12


def run(args, timeout=60):
    return subprocess.check_output(args, text=True, timeout=timeout)


def seconds(value):
    h, m, s = value.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as audio:
        for chunk in iter(lambda: audio.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def decode(path):
    """Mono float samples at ANALYSIS_RATE, decoded by FFmpeg (any format it reads)."""
    import numpy as np
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '1',
                          '-ar', str(ANALYSIS_RATE), '-'], capture_output=True, timeout=900, check=True).stdout
    return np.frombuffer(pcm, dtype='<f4').astype('float32')


def envelope(y, rate_hz):
    import librosa
    import numpy as np
    hop = int(round(ANALYSIS_RATE / rate_hz))
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
    dbfs = 20 * np.log10(np.maximum(rms, 1e-4))  # floor at -80 dBFS
    return {'rate': round(ANALYSIS_RATE / hop, 4), 'dbfs': [round(float(v), 1) for v in dbfs]}


def onset_times(y):
    import librosa
    times = librosa.onset.onset_detect(y=y, sr=ANALYSIS_RATE, hop_length=512, units='time')
    return [round(float(t), 3) for t in times]


def analyse(path, rate_hz):
    import librosa
    import numpy as np
    y = decode(path)
    hop = 512
    strength = librosa.onset.onset_strength(y=y, sr=ANALYSIS_RATE, hop_length=hop)
    _, frames = librosa.beat.beat_track(onset_envelope=strength, sr=ANALYSIS_RATE, hop_length=hop)
    spectrum = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
    low = spectrum[librosa.fft_frequencies(sr=ANALYSIS_RATE, n_fft=2048) < 150].sum(axis=0)
    at = lambda f: low[np.clip(np.asarray(f, dtype=int), 0, low.size - 1)]
    shifted = False
    if len(frames) >= 8:
        # A tracker can lock onto off-beat hats. In these 4/4 bed styles the kick sits on the
        # beat, so if the low end peaks half a beat later the whole grid moves by half a beat.
        half = int(round(float(np.median(np.diff(frames))) / 2))
        if at(frames + half).mean() > 1.5 * at(frames).mean():
            frames, shifted = frames + half, True
    beats = librosa.frames_to_time(frames, sr=ANALYSIS_RATE, hop_length=hop)
    downbeats, phase = [], None
    if len(beats) >= 8:  # the beat phase with the most low-end (kick) energy is taken as beat one
        phase = max(range(4), key=lambda p: float(at(frames[p::4]).mean()))
        downbeats = beats[phase::4]
    # Beat times are quantised to the analysis hop (23 ms), so single intervals alternate around
    # the true period. A least-squares slope over several beats recovers it.
    period = lambda t: float(np.polyfit(np.arange(len(t)), t, 1)[0])
    bpm = [60.0 / period(beats[k:k + 9]) for k in range(0, max(len(beats) - 8, 0), 4)]
    return {
        'tempo': round(60.0 / period(beats), 2) if len(beats) >= 2 else None,
        'tempoRange': [round(min(bpm), 2), round(max(bpm), 2)] if bpm else None,
        'beats': [round(float(t), 3) for t in beats],
        'beatPhaseShifted': shifted,
        'downbeats': [round(float(t), 3) for t in downbeats],
        'downbeatsEstimated': True,
        'downbeatPhase': phase,
        'onsets': onset_times(y),
        'envelope': envelope(y, rate_hz),
    }


def merge(timeline_path, audio, analysis, offset, force):
    timeline = json.loads(timeline_path.read_text())
    if timeline.get('bgm') and not force:
        raise SystemExit(f'{timeline_path} already has a "bgm" block; pass --force-merge to replace it')
    total = timeline['duration']
    program = lambda times: [round(t - offset, 3) for t in times if 0 <= t - offset <= total]

    def window(env):
        rate, values = env['rate'], env['dbfs']
        first = int(round(offset * rate))
        count = int(total * rate) + 1
        padded = [-80.0] * max(-first, 0) + values[max(first, 0):]
        return {'rate': rate, 'dbfs': (padded + [-80.0] * count)[:count]}

    beats = program(analysis['beats'])
    snap = []
    for i, slot in enumerate(timeline['slots']):
        near = min(beats, key=lambda b: abs(b - slot['start']), default=None)
        snap.append({'slot': i, 'start': slot['start'],
                     'beat': near if near is not None and abs(near - slot['start']) <= SNAP_SECONDS else None})
    bgm = {
        'path': str(audio), 'sha256': analysis['audioSha256'], 'offset': offset,
        'tempo': analysis['tempo'], 'tempoRange': analysis['tempoRange'],
        'beats': beats, 'downbeats': program(analysis['downbeats']), 'downbeatsEstimated': True,
        'onsets': program(analysis['onsets']), 'envelope': window(analysis['envelope']),
        'stems': {name: {'sha256': s['sha256'], 'onsets': program(s['onsets']), 'envelope': window(s['envelope'])}
                  for name, s in analysis.get('stems', {}).items()},
        'slotBeats': snap,
    }
    drop = next((t for t in timeline['transitions'] if t['kind'] == 'drop'), None)
    if drop and analysis['downbeats']:
        # Offset = D - H: a downbeat D in the stem lands on the drop time H. Prefer downbeats at or
        # after H so the stem's build plays under the hook rather than being trimmed away.
        candidates = [d for d in analysis['downbeats'] if d >= drop['start']] or analysis['downbeats']
        best = min(candidates, key=lambda d: abs(d - (drop['start'] + offset)))
        bgm['hookDrop'] = {'time': drop['start'], 'nearestDownbeat': round(best - offset, 3),
                           'error': round(best - offset - drop['start'], 3),
                           'suggestedOffset': round(best - drop['start'], 3)}
    timeline['bgm'] = bgm
    tmp = timeline_path.with_name(timeline_path.name + '.tmp')
    tmp.write_text(json.dumps(timeline, indent=1) + '\n')
    os.replace(tmp, timeline_path)
    return bgm


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('audio', type=Path)
    parser.add_argument('output', type=Path, help='Durable production-folder JSON path')
    parser.add_argument('--beats', action='store_true', help='add beats, downbeats, onsets and an envelope (librosa)')
    parser.add_argument('--stem', action='append', default=[], metavar='NAME=PATH',
                        help='separated stem to analyse too (implies --beats)')
    parser.add_argument('--envelope-rate', type=float, default=30.0, help='envelope samples per second (30)')
    parser.add_argument('--merge-into', type=Path, metavar='TIMELINE', help='resolved-timeline.json to update')
    parser.add_argument('--bgm-offset', type=float, default=0.0,
                        help='seconds trimmed from the BGM head (negative delays it), as the mixer uses')
    parser.add_argument('--force-merge', action='store_true')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; preserve it or choose a revision filename.')
    stems = {}
    for item in args.stem:
        name, sep, path = item.partition('=')
        if not sep or not name or not Path(path).exists():
            parser.error(f'--stem expects NAME=PATH to an existing file, got {item!r}')
        stems[name] = Path(path)
    beats = args.beats or bool(stems) or bool(args.merge_into)
    if args.merge_into:
        if not args.merge_into.exists():
            parser.error(f'{args.merge_into} does not exist')
        if json.loads(args.merge_into.read_text()).get('bgm') and not args.force_merge:
            parser.error(f'{args.merge_into} already has a "bgm" block; pass --force-merge to replace it')
    if not 1 <= args.envelope_rate <= 200:
        parser.error('--envelope-rate must be between 1 and 200')
    if beats:
        try:
            import librosa  # noqa: F401
        except ImportError:
            parser.error('--beats needs librosa: uv run --python 3.12 --with librosa python extract-video-timing.py ...')

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
    result = {
        'audioSha256': sha256(args.audio),
        'duration': float(metadata['format']['duration']),
        'timingSource': 'embedded subtitles' if cues else 'no usable embedded subtitles',
        'timingVerified': False,
        'lyrics': cues,
        'sectionCues': sections,
        'reviewFlags': [c for c in cues if c['end'] - c['start'] < .5 or c['end'] - c['start'] > 7],
    }
    if beats:
        result.update(analyse(args.audio, args.envelope_rate))
        if stems:
            result['stems'] = {}
            for name, path in stems.items():
                y = decode(path)
                result['stems'][name] = {'path': str(path), 'sha256': sha256(path), 'onsets': onset_times(y),
                                         'envelope': envelope(y, args.envelope_rate)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects against a concurrent writer after the check.
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(f"{len(cues)} lyric cues; {len(result['reviewFlags'])} timing flags; wrote {args.output}")
    if beats:
        span = result['tempoRange']
        print(f"tempo {result['tempo']} BPM (measured range {span[0]}-{span[1]})" if span else f"tempo {result['tempo']} BPM",
              f"; {len(result['beats'])} beats, {len(result['downbeats'])} estimated downbeats, {len(result['onsets'])} onsets")
    if args.merge_into:
        bgm = merge(args.merge_into, args.audio, result, args.bgm_offset, args.force_merge)
        print(f"merged {len(bgm['beats'])} beats into {args.merge_into} at offset {args.bgm_offset:g} s")
        if 'hookDrop' in bgm:
            h = bgm['hookDrop']
            print(f"hook drop at {h['time']:.3f} s: nearest downbeat {h['error']:+.3f} s away; "
                  f"--bgm-offset {h['suggestedOffset']:g} lands one exactly")


if __name__ == '__main__':
    main()
