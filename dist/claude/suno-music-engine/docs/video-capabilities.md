# Video capabilities shipped with Suno Music Engine

Reviewed 2026-10-17 against the canonical skill and the Soft Parts, Rectify, Ignition Syntax, All Signal, Crumbs in the Kernel and Which One of You production records. This inventory describes reusable capability coverage, not acceptance or publication of any particular film. Rebuild and verify both runtime installations after changing these sources.

## Included in Git and both runtime adapters

| Capability | Source |
|---|---|
| Selected-audio identity, embedded cue extraction, timing flags | `scripts/extract-video-timing.py` and `references/music-video-production.md` |
| Vocal-stem word timing, cue-window matching and interpolation labels | `scripts/align-lyric-words.py` and the main video guide |
| Mechanical verbatim-lift gate (3/4/5/6-gram substantive overlap vs reference) | `scripts/check-lift.py` and `SKILL.md` pre-delivery checklist item 10 |
| Numerical reference/render look comparison (median luma, % > 128, quantised ground, top-400 accent) | `scripts/measure-frame-look.py` and `references/video-direction-and-quality.md` |
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
| Camera-boundary prevention, known-failure regression cases, fractional cut indexing, actual FCurve interpolation, independent shutter-path checks, contiguous preview editing and jitter diagnosis | Direction and quality guide; the camera-audit implementation is project-specific |
| Browser/Blender comparisons, actual renderer provenance, snapshot versus animated scene | Story-world and direction guides; renderer implementations remain project-specific |
| Titles, descriptions, channel bios, rights and AI disclosure | `references/youtube-release.md` |

## Helper prerequisites and limits

- `extract-video-timing.py AUDIO OUTPUT.json`: Python 3 plus FFmpeg/FFprobe on PATH. Refuses to overwrite its output. Extracted cues are explicitly unverified.
- `align-lyric-words.py TIMING.json VOCALS.wav OUTPUT.json`: the implementation uses `mlx-whisper` on compatible Apple hardware (see its usage docstring; where `mlx-whisper` fails to build, use `whisper-cli -m ggml-small.en.bin` via `whisper-cpp` or `mexicat/pdoom-video`'s `analysis/align.py`). A first model run may download weights; audio transcription stays local. It writes a raw transcript sidecar and reuses it if present. Use a fresh output basename for different audio/model inputs to avoid stale transcript reuse. It currently assumes English lyrics; other languages need an adapted transcription/normalization path.
- `check-lift.py REFERENCE.(txt|vtt|srt) CANDIDATE.txt`: Python 3 stdlib only. Strips bracket tags and VTT/SRT cue headers, expands contractions, compares substantive 3/4/5/6-grams (<2 function words), and exits non-zero on any substantive 3-gram overlap.
- `measure-frame-look.py FRAME_OR_DIR [...]`: Python 3 plus FFmpeg on PATH. Prints median pixel value, `% > 128`, top-400 most-saturated accent hex, and top quantised ground hex colours for direct numerical comparison against reference frames.
- Word interpolation and a high matched count are not proof of sync. Inspect repeated choruses, first-word holds and unmatched passages against playback.

## Project implementations are separate

The skill ships production methods and the helpers above. It is not a bundled video editor or universal renderer. Bespoke scenes, review applications, stem-analysis scripts and renderers remain in the corresponding video projects. Do not claim `scripts/analyze.py`, `scripts/prepare.sh` or `scripts/render.mjs` exists in an installed skill.

The local projects inspected were under `/Users/Shared/repos/content/`: `soft-parts-video`, `rectify-video`, `ignition-syntax-video`, `all-signal-video`, `crumbs-in-the-kernel-video` and `which-one-of-you`. These are local provenance pointers, not portable dependencies. Their analysis/rendering and camera-audit implementations have not been consolidated into the skill; copying them requires implementation review and validation, rather than treating documentation coverage as a tested code migration.

Song audio, stems, rendered videos, private notes and artist-specific release copy belong in durable production storage. They are not reusable skill resources and are not included in its Git repository. The renderer and archive locations can differ by machine; inspect current project configuration rather than reusing a hardcoded personal path.

## Production outcomes and open craft gap

The latest review distinguished a liked Ignition Syntax pilot from unverified acceptance of its full export. Soft Parts export/decode evidence does not establish whole-song sync or approval of every later version. Rectify had analysis and partial visual code, rather than a verified finished video.

All Signal full-v2 used three.js/browser rendering; its Blender comparisons were still tests. The later kitchen sample actually rendered in Blender EEVEE and passed technical export checks, but the user explicitly rejected it as cheap and unimpressive. A renderer switch, extra inserts, saturated lighting and a treatment did not close the creative gap. Preserve those outcomes in the production records; do not promote the kitchen code to a reusable production baseline.

Crumbs in the Kernel later produced a technically verified 20-second Cycles pilot. The user judged it better, with room for improvement, identified a camera jump and asked what was happening. That supports continuing the direction, not claiming a finished or accepted film. Full-film work added a visible recurring fragment, camera-boundary checks with the actual failed poses as a regression case, smoothed controls and shutter-time camera keys. Fractional-frame audits then caught incorrect cut indices and Bezier interpolation hidden by the analytic evaluator; the corrected path passed those numerical checks. Only camera/focus transforms, lens and fragment location were baked, so this is not evidence of complete object-motion blur.

Which One of You (`pilot-01` → `pilot-02` → `pilot-03` → `full-v1`, 2026-10-16 to 2026-10-17) tested three 26-second pilots on the `mexicat/pdoom-video` architecture (`Pre-Chorus 1` + `Chorus 1`). The user selected `pilot-03` (hybrid 3D `CameraRig3D` + additive `LineBatch` wireframes + world-space 3D `TextPlane`s + Canvas2D isometric terracotta agent bots, terminal cards and rubber stamps) as the best pass and authorized full-song expansion. On 2026-10-17, the full `260.014 s` (`15,601`-frame, 1080p60, 54-sub-plate) video (`renders/full-v1/which-one-of-you-full.mp4`) was built with constant-BPM linear-regression beat fitting (`116.990 BPM`, `18.9 ms` RMS residual, `DB_OFF = 0` section-boundary assertions), clamped + harmonic-envelope-warped word timing, linear-RGB shader calibration verified by `measure-frame-look.py` (`median 18–26` dark world / `231` paper-white world), and 3D frustum-sized `TextPlane`s. The user reviewed and accepted the completed full-length film ("that looks fucking AMAZING dude. nice work").

## Maintenance check

Edit `definition.md` and source references/scripts. Validate and rebuild with Polyskill, compare generated adapters with installed copies, and verify the Git remote commit. Generated `dist/` files must not be the only location of a new workflow. Keep this inventory consistent when new helpers are actually shipped.
