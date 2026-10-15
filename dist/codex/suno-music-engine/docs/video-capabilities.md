# Video capabilities shipped with Suno Music Engine

Reviewed 2026-10-15 against the canonical skill and the Soft Parts, Rectify, Ignition Syntax and All Signal production records, including the rejected Blender kitchen sample. This inventory describes reusable capability coverage, not acceptance or publication of any particular film. Rebuild and verify both runtime installations after changing these sources.

## Included in Git and both runtime adapters

| Capability | Source |
|---|---|
| Selected-audio identity, embedded cue extraction, timing flags | `scripts/extract-video-timing.py` and `references/music-video-production.md` |
| Vocal-stem word timing, cue-window matching and interpolation labels | `scripts/align-lyric-words.py` and the main video guide |
| Held-first-word correction, prompt bleed, added ad-libs and repeated lines | Main video guide; corrections require inspection and are not all automated by the helper |
| Reference discovery, exact-video credits, close motion breakdown and observed/inferred boundaries | `references/video-direction-and-quality.md` |
| Song meaning, visible setup/payoff, joint song/story development and remapping the selected take | Direction and quality guide; co-development is proposed, not proven by a completed production |
| Visual systems, optional kinetic type, phrase-led or line-led shots | Main video guide |
| Scored-event measurement, absent silences and failed section detection | Main video guide and `references/instrumental-video-production.md` |
| Form/phrase/beat/texture mapping, tempo drift, stem leakage and noise floors | Instrumental video guide |
| Musical-time curves, deterministic seeking and simulation checkpoints | Instrumental video guide |
| Pilot, style frames, full-song shot coverage and frame/range review | Main video guide |
| HDR/type legibility, light-ground grading, layer order, fit-to-width and burn pacing | Main video guide |
| GPU verification, chunked export, grain cost, large-file hashing and render identity | Main video guide |
| Story treatment, boards/animatics, world memory as dated events, optional diegetic type and world systems | `references/story-world-video.md` |
| Representative motion proofs, acting/contact risks, rejection handling and bounded iteration | Direction and quality guide |
| Camera-boundary prevention, known-failure regression cases, shutter interpolation, contiguous preview editing and jitter diagnosis | Direction and quality guide; the camera-audit implementation is project-specific |
| Browser/Blender comparisons, actual renderer provenance, snapshot versus animated scene | Story-world and direction guides; renderer implementations remain project-specific |
| Titles, descriptions, channel bios, rights and AI disclosure | `references/youtube-release.md` |

## Helper prerequisites and limits

- `extract-video-timing.py AUDIO OUTPUT.json`: Python 3 plus FFmpeg/FFprobe on PATH. Refuses to overwrite its output. Extracted cues are explicitly unverified.
- `align-lyric-words.py TIMING.json VOCALS.wav OUTPUT.json`: the implementation uses `mlx-whisper` on compatible Apple hardware (see its usage docstring). A first model run may download weights; audio transcription stays local. It writes a raw transcript sidecar and reuses it if present. Use a fresh output basename for different audio/model inputs to avoid stale transcript reuse. It currently assumes English lyrics; other languages need an adapted transcription/normalization path.
- Word interpolation and a high matched count are not proof of sync. Inspect repeated choruses, first-word holds and unmatched passages against playback.

## Project implementations are separate

The skill ships production methods and the two helpers above. It is not a bundled video editor or universal renderer. Bespoke scenes, review applications, stem-analysis scripts and renderers remain in the corresponding video projects. Do not claim `scripts/analyze.py`, `scripts/prepare.sh` or `scripts/render.mjs` exists in an installed skill.

The local projects inspected were under `/Users/Shared/repos/content/`: `soft-parts-video`, `rectify-video`, `ignition-syntax-video`, `all-signal-video` and `crumbs-in-the-kernel-video`. These are local provenance pointers, not portable dependencies. Their analysis/rendering and camera-audit implementations have not been consolidated into the skill; copying them requires implementation review and validation, rather than treating documentation coverage as a tested code migration.

Song audio, stems, rendered videos, private notes and artist-specific release copy belong in durable production storage. They are not reusable skill resources and are not included in its Git repository. The renderer and archive locations can differ by machine; inspect current project configuration rather than reusing a hardcoded personal path.

## Production outcomes and open craft gap

The latest review distinguished a liked Ignition Syntax pilot from unverified acceptance of its full export. Soft Parts export/decode evidence does not establish whole-song sync or approval of every later version. Rectify had analysis and partial visual code, rather than a verified finished video.

All Signal full-v2 used three.js/browser rendering; its Blender comparisons were still tests. The later kitchen sample actually rendered in Blender EEVEE and passed technical export checks, but the user explicitly rejected it as cheap and unimpressive. A renderer switch, extra inserts, saturated lighting and a treatment did not close the creative gap. Preserve those outcomes in the production records; do not promote the kitchen code to a reusable production baseline.

The next proposed craft step is close study of a strong reference sequence followed by an original, representative motion shot. That step has not yet demonstrated a reference-level result. This skill captures the procedure and failed attempts honestly; it does not claim the missing artistic knowledge has already been acquired.

Crumbs in the Kernel later produced a technically verified 20-second Cycles pilot. The user judged it better, with room for improvement, identified a camera jump and asked what was happening. That supports continuing the direction, not claiming a finished or accepted film. Full-film work added a visible recurring fragment, camera-boundary checks with the actual failed poses as a regression case, smoothed controls and shutter-time camera keys. Its complete-film outcome remains pending until export and review; shader/renderer benchmarks do not establish artistic success.

## Maintenance check

Edit `definition.md` and source references/scripts. Validate and rebuild with Polyskill, compare generated adapters with installed copies, and verify the Git remote commit. Generated `dist/` files must not be the only location of a new workflow. Keep this inventory consistent when new helpers are actually shipped.
