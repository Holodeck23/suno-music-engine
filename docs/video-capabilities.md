# Video capabilities shipped with YouTube Lesson Engine

Reviewed 2026-10-15 against the canonical skill and the Soft Parts, Rectify, Ignition Syntax and All Signal production records, including the rejected Blender kitchen sample. This inventory describes reusable capability coverage, not acceptance or publication of any particular film. The lesson-engine refactor (also 2026-10-15) kept every video lesson. The music-video, instrumental-video and story-world references were merged into `references/visual-lesson-production.md` (Parts 2–4, line-verified against the originals), and only the songwriting, album and personal-translation references were retired. In this table, "Main video guide" means Part 2 of that file, "Instrumental video guide" means Part 3, and "Narrative-continuity section" means Part 4. Rebuild and verify both runtime installations after changing these sources.

## Included in Git and both runtime adapters

| Capability | Source |
|---|---|
| Selected-audio identity, embedded cue extraction, timing flags | `scripts/extract-video-timing.py` and `references/visual-lesson-production.md` |
| Vocal-stem word timing, cue-window matching and interpolation labels | `scripts/align-lyric-words.py` and the main video guide |
| Held-first-word correction, prompt bleed, added ad-libs and repeated lines | Main video guide; corrections require inspection and are not all automated by the helper |
| Reference discovery, exact-video credits, close motion breakdown and observed/inferred boundaries | `references/video-direction-and-quality.md` |
| Song meaning, visible setup/payoff, joint song/story development and remapping the selected take | Direction and quality guide; co-development is proposed, not proven by a completed production |
| Visual systems, optional kinetic type, phrase-led or line-led shots | Main video guide |
| Scored-event measurement, absent silences and failed section detection | Main video guide and instrumental video guide |
| Form/phrase/beat/texture mapping, tempo drift, stem leakage and noise floors | Instrumental video guide |
| Musical-time curves, deterministic seeking and simulation checkpoints | Instrumental video guide |
| Pilot, style frames, full-song shot coverage and frame/range review | Main video guide |
| HDR/type legibility, light-ground grading, layer order, fit-to-width and burn pacing | Main video guide |
| GPU verification, chunked export, grain cost, large-file hashing and render identity | Main video guide |
| Story treatment, boards/animatics, world memory as dated events, optional diegetic type and world systems | Narrative-continuity section |
| Representative motion proofs, acting/contact risks, rejection handling and bounded iteration | Direction and quality guide |
| Camera-boundary prevention, known-failure regression cases, fractional cut indexing, actual FCurve interpolation, independent shutter-path checks, contiguous preview editing and jitter diagnosis | Direction and quality guide; the camera-audit implementation is project-specific |
| Browser/Blender comparisons, actual renderer provenance, snapshot versus animated scene | Narrative-continuity section and the direction guide; renderer implementations remain project-specific |
| Titles, descriptions, channel bios, rights and AI disclosure; curiosity-gap titles, three-word thumbnails, chapters and pinned comments for lessons | `references/youtube-release.md` |
| Lesson manifest contract, Dave Dark structure checks, trigger word/target validation and runtime estimates | `scripts/validate-lesson-manifest.py`, `references/lesson-manifest.schema.json` and `references/script-and-retention-engine.md` |
| ElevenLabs narration with character-to-word timestamps, request stitching, response caching and retries | `scripts/generate-tts-and-cues.py --provider elevenlabs`; tested against a local mock of the endpoint, not the live API |
| Local voiceover or TTS alignment, first-word onset correction, segment-aware interpolation, optional re-stitching | `scripts/generate-tts-and-cues.py --provider local-audio`; tested with transcript sidecars, Whisper itself not run in the build environment |
| Resolved timeline: word and trigger times, gapless slots, transitions, camera-move events for the 6–8 second rule, YouTube chapters | `scripts/generate-tts-and-cues.py` and `references/script-and-retention-engine.md` §6 |
| BGM beats, kick-phase correction, estimated downbeats, measured tempo range, absolute envelopes, per-stem analysis, hook-drop offset | `scripts/extract-video-timing.py --beats --merge-into`; tested on synthetic beds, including a drifting take |
| Timeline-driven ducking without pumping, vocal pocket, voice chain, loudness and true-peak mastering | `scripts/mix-voice-and-bgm.py`; manual FFmpeg recipes in `references/bgm-suno-scoring.md` §12 |
| Four programmatic visual states, render contract, transitions, camera moves, freeze detection | Part 1 of `references/visual-lesson-production.md`; the renderer itself is project-specific |
| Mobile legibility: minimum sizes, 45-column code, contrast, phone-scale test | `references/video-direction-and-quality.md`; the 45-column limit is enforced by the manifest validator |

## Helper prerequisites and limits

- `extract-video-timing.py AUDIO OUTPUT.json`: Python 3 plus FFmpeg/FFprobe on PATH. Refuses to overwrite its output. Extracted cues are explicitly unverified.
- `align-lyric-words.py TIMING.json VOCALS.wav OUTPUT.json`: the implementation uses `mlx-whisper` on compatible Apple hardware (see its usage docstring). A first model run may download weights; audio transcription stays local. It writes a raw transcript sidecar and reuses it if present. Use a fresh output basename for different audio/model inputs to avoid stale transcript reuse. It currently assumes English lyrics; other languages need an adapted transcription/normalization path.
- `validate-lesson-manifest.py MANIFEST [--wpm 150] [--strict] [--json]`: Python 3.8+ standard library only; reads the schema from `references/` beside it. Writes nothing. Exit 0 valid, 1 errors (or warnings with `--strict`), 2 unreadable input. Its durations are word-count estimates; rendered narration audio remains the timing authority.
- `generate-tts-and-cues.py MANIFEST --out-dir DIR --provider elevenlabs|local-audio`: Python 3.8+ standard library plus FFmpeg/FFprobe. The ElevenLabs provider needs `ELEVENLABS_API_KEY` and sends only segment text and voice settings to the API. `wav_44100`/`pcm_44100` output needs the Pro tier, and the default is `mp3_44100_128`. The local provider needs `mlx-whisper` (Apple silicon) or `faster-whisper` unless a transcript is supplied. Refuses to overwrite its outputs without `--force`.
- `extract-video-timing.py AUDIO OUT.json --beats [--stem NAME=PATH] [--merge-into TIMELINE --bgm-offset S]`: `--beats` needs `librosa` (`uv run --python 3.12 --with librosa ...`). Downbeats are estimated from low-end energy and assume 4/4 with the kick on the beat. `--merge-into` replaces only the timeline's `bgm` key, atomically.
- `mix-voice-and-bgm.py NARRATION BGM TIMELINE OUT.wav`: Python 3.8+ standard library plus FFmpeg. It writes 48 kHz 24-bit stereo, refuses to overwrite without `--force`, and `--dry-run` prints the envelope and filter graph. The limiter works on sample peaks, so check the reported true peak.
- Word interpolation and a high matched count are not proof of sync. Inspect repeated choruses, first-word holds and unmatched passages against playback.

## Project implementations are separate

The skill ships production methods and the five scripts above. It is not a bundled video editor, universal renderer or stem separator. Bespoke scenes, review applications, stem-analysis scripts and renderers remain in the corresponding video projects. Do not claim `scripts/analyze.py`, `scripts/prepare.sh` or `scripts/render.mjs` exists in an installed skill.

The local projects inspected were under `/Users/Shared/repos/content/`: `soft-parts-video`, `rectify-video`, `ignition-syntax-video`, `all-signal-video` and `crumbs-in-the-kernel-video`. These are local provenance pointers, not portable dependencies. Their analysis/rendering and camera-audit implementations have not been consolidated into the skill; copying them requires implementation review and validation, rather than treating documentation coverage as a tested code migration.

Song audio, stems, rendered videos, private notes and artist-specific release copy belong in durable production storage. They are not reusable skill resources and are not included in its Git repository. The renderer and archive locations can differ by machine; inspect current project configuration rather than reusing a hardcoded personal path.

## Production outcomes and open craft gap

The latest review distinguished a liked Ignition Syntax pilot from unverified acceptance of its full export. Soft Parts export/decode evidence does not establish whole-song sync or approval of every later version. Rectify had analysis and partial visual code, rather than a verified finished video.

All Signal full-v2 used three.js/browser rendering; its Blender comparisons were still tests. The later kitchen sample actually rendered in Blender EEVEE and passed technical export checks, but the user explicitly rejected it as cheap and unimpressive. A renderer switch, extra inserts, saturated lighting and a treatment did not close the creative gap. Preserve those outcomes in the production records; do not promote the kitchen code to a reusable production baseline.

The next proposed craft step is close study of a strong reference sequence followed by an original, representative motion shot. That step has not yet demonstrated a reference-level result. This skill captures the procedure and failed attempts honestly; it does not claim the missing artistic knowledge has already been acquired.

Crumbs in the Kernel later produced a technically verified 20-second Cycles pilot. The user judged it better, with room for improvement, identified a camera jump and asked what was happening. That supports continuing the direction, not claiming a finished or accepted film. Full-film work added a visible recurring fragment, camera-boundary checks with the actual failed poses as a regression case, smoothed controls and shutter-time camera keys. Fractional-frame audits then caught incorrect cut indices and Bezier interpolation hidden by the analytic evaluator; the corrected path passed those numerical checks. Only camera/focus transforms, lens and fragment location were baked, so this is not evidence of complete object-motion blur. The 1080p EEVEE full pass is rendering; its complete-film outcome remains pending until export and review. Shader/renderer benchmarks do not establish artistic success.

## Maintenance check

Edit `definition.md` and source references/scripts. Validate and rebuild with Polyskill, compare generated adapters with installed copies, and verify the Git remote commit. Generated `dist/` files must not be the only location of a new workflow. Keep this inventory consistent when new helpers are actually shipped.
