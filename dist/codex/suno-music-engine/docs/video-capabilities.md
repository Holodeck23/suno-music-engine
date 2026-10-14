# Video capabilities shipped with Suno Music Engine

Reviewed 2026-10-14 against the canonical skill, both installed adapters and the Soft Parts, Rectify, Ignition Syntax and All Signal production records. This inventory describes reusable capability coverage, not acceptance or publication of any particular film.

## Included in Git and both runtime adapters

| Capability | Source |
|---|---|
| Selected-audio identity, embedded cue extraction, timing flags | `scripts/extract-video-timing.py` and `references/music-video-production.md` |
| Vocal-stem word timing, cue-window matching and interpolation labels | `scripts/align-lyric-words.py` and the main video guide |
| Held-first-word correction, prompt bleed, added ad-libs and repeated lines | Main video guide; corrections require inspection and are not all automated by the helper |
| Reference-video study, visual system, kinetic type and one idea per line | Main video guide |
| Scored-event measurement, absent silences and failed section detection | Main video guide and `references/instrumental-video-production.md` |
| Form/phrase/beat/texture mapping, tempo drift, stem leakage and noise floors | Instrumental video guide |
| Musical-time curves, deterministic seeking and simulation checkpoints | Instrumental video guide |
| Pilot, style frames, full-song shot coverage and frame/range review | Main video guide |
| HDR/type legibility, light-ground grading, layer order, fit-to-width and burn pacing | Main video guide |
| GPU verification, chunked export, grain cost, large-file hashing and render identity | Main video guide |
| Titles, descriptions, channel bios, rights and AI disclosure | `references/youtube-release.md` |

## Helper prerequisites and limits

- `extract-video-timing.py AUDIO OUTPUT.json`: Python 3 plus FFmpeg/FFprobe on PATH. Refuses to overwrite its output. Extracted cues are explicitly unverified.
- `align-lyric-words.py TIMING.json VOCALS.wav OUTPUT.json`: the implementation uses `mlx-whisper` on compatible Apple hardware (see its usage docstring). A first model run may download weights; audio transcription stays local. It writes a raw transcript sidecar and reuses it if present. Use a fresh output basename for different audio/model inputs to avoid stale transcript reuse. It currently assumes English lyrics; other languages need an adapted transcription/normalization path.
- Word interpolation and a high matched count are not proof of sync. Inspect repeated choruses, first-word holds and unmatched passages against playback.

## Project implementations are separate

The skill ships production methods and the two helpers above. It is not a bundled video editor or universal renderer. Bespoke scenes, review applications, stem-analysis scripts and renderers remain in the corresponding video projects. Do not claim `scripts/analyze.py`, `scripts/prepare.sh` or `scripts/render.mjs` exists in an installed skill.

The local projects inspected were under `/Users/Shared/repos/content/`: `soft-parts-video`, `rectify-video`, `ignition-syntax-video` and `all-signal-video`. These are local provenance pointers, not portable dependencies. The generalized analysis work in the latter projects has not been consolidated into the skill; copying it would require an explicit implementation review and validation, rather than treating a documentation audit as a tested code migration.

Song audio, stems, rendered videos, private notes and artist-specific release copy belong in durable production storage. They are not reusable skill resources and are not included in its Git repository. The renderer and archive locations can differ by machine; inspect current project configuration rather than reusing a hardcoded personal path.

## Maintenance check

Edit `definition.md` and source references/scripts. Validate and rebuild with Polyskill, compare generated adapters with installed copies, and verify the Git remote commit. Generated `dist/` files must not be the only location of a new workflow. Keep this inventory consistent when new helpers are actually shipped.
