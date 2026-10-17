# From a selected song to a code-driven music video

Use this mode when the user wants an animated video for an accepted song. It is separate from using a video as a musical reference in Suno. Preserve the user's chosen recording and visual direction; do not regenerate the song to simplify animation.

For instrumentals or detailed per-stem animation, also read `instrumental-video-production.md`. For narrative continuity, read `story-world-video.md`. For ambitious references, a rejected draft or developing music and film together, read `video-direction-and-quality.md` before designing another pass. For bundled helpers and project-specific implementations, see `../docs/video-capabilities.md`.

## Where the work lives

Keep two homes and never mix them. The renderer's code goes in its own version-controlled repository (initialise it with the first file). Everything the production makes or consumes goes in one durable production folder per song: the selected audio and its hash, the song sheet, stems, analysis, timing, every render pass, contact sheets, treatment and production log. The repository links to that folder (symbolic links for the audio and analysis) rather than copying media into itself, and build output stays ignored. A render finished in any tool's own output or scratch directory is copied into the production folder's `renders/<pass-name>/` in the same turn, and the log records where it is. When a machine has its own workspace rules for these locations, they take precedence over this paragraph.

## Audio is the timing authority

Keep the original audio, its SHA256, generation identifier if present, accepted lyrics and timing source in the durable production folder. Inspect codecs, duration, metadata and subtitle streams before proposing transcription or an external API. Suno `.m4a` exports carry a timed `mov_text` lyric track off Suno's own synthesis grid, even when the audio stream is Opus:

```bash
ffprobe -v error -show_streams song.m4a | grep -E "codec_name|codec_type"   # look for mov_text
ffmpeg -v error -i song.m4a -map 0:s:0 lyrics.srt
```

On a 4:20 Suno v6 track (`"Which One of You"`, 2026-10-16), extracting stream `0:s:0` yielded 96 cues with exact line timings off Suno's synthesis grid, including the bracketed production tags as section markers. This removes transcription and forced alignment for the line layer entirely (while word-level timing within a line still requires acoustic alignment; see below). You can also run `python3 scripts/extract-video-timing.py AUDIO OUTPUT.json` from the skill directory when FFmpeg and FFprobe are available; it separates bracketed section directions from singable lyric cues and flags unusual durations without overwriting outputs or uploading media. Verify embedded cues against playback: preserve raw cue times, record any display-hold adjustment separately without overlapping the next sung cue, and never claim transcription accuracy from subtitle extraction alone.

A browser-compatible AAC playback derivative may be useful when the source uses an unsupported codec. Preserve the source and document the conversion. Do not assume an M4A extension implies AAC.

**Fit a constant beat grid, and assert section downbeats rather than trusting the onset-energy heuristic:**
- Machine-generated Suno tracks do not drift in tempo. Fit a single constant BPM and phase to the detected beats rather than using per-beat detection directly (`"Which One of You"`, 2026-10-16: fitted `116.990 BPM` with `18.9 ms` RMS residual across `504` detected beats).
- Do not trust the downbeat-offset heuristic (picking the modulo-4 beat phase with maximum mean onset energy) unverified. On `"Which One of You"` (2026-10-16), the onset-energy heuristic chose the wrong phase (`DB_OFF = 2`) and placed the Chorus 1 cut at `71.036 s` against a `72.048 s` section start — `1.012 s` early, cutting mid-word through the end of the pre-chorus.
- **Required data-generator assertion:** Every musical section boundary's chosen downbeat must lie within `±120 ms` of the section start and must fall **after** the last word of the preceding line (`abs(downbeat - section.start) <= 0.120` and `downbeat >= prev_line.words[-1].end`). Fail loudly with an assertion error if any boundary violates either condition.

## Word-level timing for kinetic type

Character-weighted word distribution within a Suno line cue is adequate only for a rough structural pilot and is **wrong for kinetic typography**, which is the entire genre. In addition, embedded Suno cue end times are often flat placeholders (or equal to the next cue's start), and in some takes cue start times can drift across repeated sections. Kinetic typography requires acoustic alignment of every word:

1. **Full-film required pipeline (`mexicat/pdoom-video` `analysis/align.py`):** Isolate the vocal stem with Demucs (`htdemucs_ft`), run CTC forced alignment from two independent acoustic models, and cross-check word boundaries against Whisper timestamps. Treat this acoustic alignment pipeline as a mandatory step before rendering any full film.
2. **Known CTC failure mode on gang vocals (2026-10-16):** CTC forced alignment collapses on stacked gang vocals (e.g., repeated shouted answers in a chorus). Clamp CTC alignment windows to **2-bar windows per line** and snap shouted gang-vocal onsets to the **16th-note grid**.
3. **Suno `mov_text` runaway cue windows & vocal harmonic-envelope warping (2026-10-17):** Embedded `mov_text` cues on Suno v6 tracks frequently set a line's `end` timestamp to the start of the *next section* across an instrumental break or outro valley (on `"Which One of You"`, `"It is handled. I have got thirty of them on it."` at `8.86 s` had raw cue end `30.40 s` across the 16-second slap-bass break; `"Anyone. Anyone still running."` had raw cue end `238.48 s`; and the final `"I have gone ahead and"` had a `47 s` window). Distributing words across unclamped cue windows smears words across instrumental breaks at 1–3 seconds per word. Always clamp each spoken/sung line's active alignment window to `min(next_line.start - 0.04, start + min(2 * bar_sec, max(1.6, n_chars * 0.072)))` before word distribution, warp word boundaries onto the `280–3400 Hz` bandpass vocal harmonic envelope (`200 fps`), and snap repeated gang-vocal shouts (`"I did, I did, I did"`) directly to the 16th-note grid (`step = beat_sec / 4`).
4. **Lightweight single-model fallback (`scripts/align-lyric-words.py`):** When running `scripts/align-lyric-words.py TIMING.json VOCALS.wav WORDS.json`, it aligns the known lyric sheet to heard Whisper words within a cue window and interpolates unmatched words. Report the matched/total count, read the raw transcript for ad-libs or closing repeats missing from the sheet, and inspect long phrase-initial words against vocal-stem RMS energy (40 ms window) so Whisper's pre-silence stretch is trimmed without hiding genuinely held notes.

## Scored events: measure each one, then mark it located or absent

Suno treats bracket directions as weak hints. Silences, breaks, strips, builds, intro lengths and outro hits written into the lyric field frequently do not exist in the take, or exist somewhere else. Before designing, test each scored event against the audio and record it as located fact (start, end, evidence) or absent:

- Scan the mix at 20 ms RMS for genuine dropouts; a "silence" that the mix never reaches is not a silence.
- Tabulate per-bar RMS for each stem against the downbeats. Strips, drum dropouts and bass drops show up as one stem falling 40 dB or more for a bar while the mix barely moves.
- Zoom (100 ms windows, beats marked) on every region the brackets describe.
- Read the transcript for sections the sheet does not have: post-chorus ad-libs, an added hook at the top of a final chorus, a spoken bridge that keeps its drums.

Then design to the located facts. An absent event is not faked with a visual: on one track the scored 2-beat silence before the final chorus did not exist, so the edit used a hard cut to clean frame on the downbeat instead, and the "stripped" bridge kept its drums, so the visual valley went to the 3 s where the band really dropped out. Novelty-based section detection can also fail outright (one 92 s block); stems plus word times gave a usable map.

## Study the reference, then set a design system

When the user points to videos they admire, download and inspect the exact reference video and its credits before any design work (see `video-direction-and-quality.md`).

**Scene detection under-reports on dark films — and `-v error` silently kills `showinfo` (2026-10-16):**
- Running `ffmpeg -vf "select='gt(scene,0.15)',showinfo"` on *LGTM* (`3TNpOD6bov8`) found only **19 changes in 305 s** (mean gap `15.0 s`) because the film holds one near-black ground across cuts; on dark-ground motion graphics, `gt(scene,0.15)` is a floor, not a cut count.
- Separately, `showinfo` logs at `info` level, so passing `-v error` suppresses its output completely and returns nothing — which reads as "no cuts." Never combine `showinfo` with `-v error`, and judge cut pace from contact sheets (`fps=1` over a 30–60 s excerpt, or `sheet --cuts`), not scene-score thresholds.

**Engine lineage — and the conflation to avoid (2026-10-16):**
- **`mexicat/pdoom-video`** (MIT, 2,805 stars, TypeScript + Three.js + Canvas2D + GLSL) is the genre's base architecture: it ships `docs/TREATMENT.md` as the style-bible format, one scene module per plate (`app/src/scenes/*.ts`), an offline renderer (`app/scripts/render.ts`, headless Chrome → `ffmpeg`) with adaptive per-tile motion-blur sampling, a `sheet --cuts` contact-sheet mode, and the Demucs + dual-CTC + Whisper alignment pipeline (`analysis/align.py`).
- **`JohnHeibel/ClaudeAnimationBase`** (1,190 stars) is a **different lineage** — `p5.js` hand-painted cartoons — and was conflated with `pdoom-video` in a research brief on 2026-10-16. Keep them distinct.
- **No public repository exists for *LGTM* (`3TNpOD6bov8`) itself:** any claim about *LGTM*'s internal code structure is reconstruction unless read directly off its frames or closing credits (`04:46`).

The following are options observed in lyric-led reference work, not requirements for every film:

- **Typography as the main image.** Words appear as they are sung, with the active word in the accent colour, upcoming words dim or absent and sung words settled. This requires acoustic word timing.
- **Line-led visual ideas.** A line can become a diagram, interface or object that carries a double meaning. This can suit a graphic treatment; a film that promises acting or narrative needs actions that develop across lines. Literalising every line can become a slide deck.
- **A strict system.** One dark ground, one accent colour, a display face plus a monospace face for small interface labels, and consistent framing chrome. The accent can carry the arc (cold before a turn, warm after).
- **Density.** *LGTM* cuts or switches sub-plates every 2 to 4 seconds. Measure the reference's cut rate and state your own before building past the pilot (`video-direction-and-quality.md`).
- **A review editor built for the project.** The creator watches drafts and marks frames and ranges for change.

Lyric-driven type and music-driven motion can complement each other. Where the treatment uses them, let words drive type and measured musical events motivate light, camera and impacts. Real analysis can drive interface readouts, but explanatory graphics and constant beat pulses do not substitute for compelling shot design.

## Pilot before full-song production

Write a brief that establishes meaning, palette, characters, props, world, focal actions and transitions. Map the pilot to actual audio events. Choose a short scope that proves the riskiest action; a few seconds may suffice, while an arc may need 20–30 seconds or neighbouring sections. Avoid padding to a fixed duration. Build something watchable before filling the song. Once the user accepts that direction or delegates completion, proceed without imposing another approval round. Acceptance applies to the version and scope reviewed; an explicit rejection stops expansion of that direction.

Choose tools for the intended look: three.js for procedural 3D, Canvas/p5 for drawn 2D, Blender/Python when offline scene rendering is preferable. A toolkit or instruction document can help, but no particular plugin, external image model or video API is inherently required.

Evaluate every frame from absolute audio time. Avoid accumulated simulation state and unseeded randomness. Seeking away and returning to a timestamp should reproduce the frame. Drive reactive movement from an archived audio envelope or a measured beat grid rather than a live input unavailable to the offline renderer.

Contact sheets catch framing and composition; motion playback catches unreadable actions, accidental freezes, bad cuts and synchronization. Use both. A passed build or attractive still image does not establish that the video works at playback speed.

Before a long render, audit camera states at shot/chunk boundaries and test risky transitions in a contiguous motion probe. Keep a regression case for any observed camera jump. See `video-direction-and-quality.md` for boundary checks, shutter-time interpolation, global-control jitter and partial-preview pitfalls.

Use style frames to catch framing and surface problems cheaply, then test motion early enough to expose weak acting, contact and transitions. Problems observed on the first style pass of an HDR pipeline, with local technical fixes:

- **Bloom swallows the type.** Push only accent-coloured pixels into HDR, set the bloom threshold at true overexposure (1.0), and keep white and neutral type below it.
- **Particles near the lens become a white blob.** Cap point size and keep emitters out of the near field. Use moderate additive intensity.
- **Busy backgrounds kill legibility.** Put a dark halo (shadow blur) behind display type and dim the background layer during text-heavy shots.
- **Long rows overflow.** Fit each row to a maximum width using its full eventual text, not only the words sung so far.
- **An additive flash before tonemapping reads as a grey frame.** Keep impact flashes short and strong.
- **Layer order hides props.** If interface chrome sits on a layer composited above the type, an opaque dialog or darkening panel on that layer covers the words. Put opaque props on the type layer beneath the words, and erase chrome rather than painting black over it.
- **Eased burns finish before the eye catches them.** Use linear progress for destruction effects that should be watched.
- **Fit-to-width must know the alignment.** Measure the room a row actually has (left-aligned: right margin minus x; right-aligned: x minus left margin; centred: twice the distance to the nearer margin), not one global maximum. A renderer with only left and centre modes silently centres "right-aligned" rows on their anchor and pushes them off frame.
- **Two rows sharing a baseline collide as soon as they fit properly.** Stack lyric rows vertically instead of pairing them left and right.

Light-ground (paper) systems need their own versions of the HDR rules:
- Skip filmic tonemapping (ACES greys the paper); roll off only values above about 0.9.
- Push only the accent hue into HDR (for example `blue - max(red, green)`), so ink and paper never bloom.
- Halos behind type are ground-coloured, not dark.
- Put noise or static on the world layer under the type layer, never in the final pass over the words.
- An impact flash or dark section is a luma-only inversion (`col + (1 - 2Y)`): paper goes black, ink goes white, and the accent keeps its hue. A full RGB negative turns a blue accent yellow and breaks the one-accent rule.
- Small mono labels need a ground-coloured halo too; static eats them otherwise.

## Extending a pilot to the full song

Write a shot table covering every second, including instrumental stretches. Shots can span multiple lines or split a phrase according to the action; one shot per line is an option for graphic treatments. Make coverage gapless so no second falls through to an accidental fallback. Give each shot an optional style-frame time for its key reveal and emit a whole-film contact sheet. Instrumental passages may use performance, story action or analysis-driven imagery. Carry a deliberate arc and a payoff that follows from the premise. Check the whole-film board and rough timing before the expensive render, while retaining early motion proofs for risky shots.

**Parallel scene-module fan-out (`"Which One of You"`, 2026-10-17):** When expanding an approved `pdoom-video` pilot to a full multi-minute track, lock shared 3D/2D primitives (`_3d.ts`, `_kit.ts`, `_hud.ts`), `timeline.ts`, and `data/*.json` first, parameterize repeated structural sections (`board.ts` via `preIndex`, `chorus.ts` via `chorusIndex`, `postchorus.ts` via `postIndex`), and fan out disjoint scene modules in parallel (`intro.ts`+`outro.ts`, `verse1.ts`+`verse2.ts`, `postchorus.ts`+`bridge.ts`) with strict file-isolation boundaries. Immediately follow completion with `bunx tsc --noEmit`, a 36-frame whole-film contact sheet (`sheet --from 0 --to <dur> --n 36`), and a multi-still `measure-frame-look.py` audit before launching the full video render.

## Make direction specific and portable

A local preview can offer play/pause, scrubbing, frame stepping, shot selection, subtitle offset and frame/range annotations. Feedback should identify:

- Target timestamp or range and object/shot.
- What to preserve.
- One concrete change.
- How to tell the revision worked.

Bind exported notes to the source-audio hash and any subtitle offset. Browser storage is convenient persistence, not the durable archive: export feedback beside the song. Render user notes as text rather than raw HTML.

## Export and verify

Use the same scene evaluation and typography in preview and export. Confirm the headless browser renders on the GPU before estimating render time: query `WEBGL_debug_renderer_info`. On macOS, Playwright with the installed Chrome channel and ANGLE Metal reported the Apple GPU, while the bundled headless shell may be missing. Pipe frames to the encoder in resumable chunks rather than storing full-resolution PNG sequences. With headless browser screenshots, wait for fonts and compositor paint after rendering, especially after viewport changes. Test identical timestamps in non-sequential order. A scene may be deterministic while screenshots still capture stale browser paint.

Mux the accepted audio with rendered frames and check output dimensions, frame rate, video/audio duration, decode success and representative frames. Bind the output hash to the audio hash, timing file, caption offset and source revision or file hashes. Preserve intermediates needed to reproduce or investigate the export.

Distinguish these states: pilot built, browser checks passed, render exported, playback visually/audibly reviewed, user accepted, full song complete. Report only states actually reached. Do not claim to have listened when only metadata or subtitles were inspected.

## Large renders, resumability and delivery size

Measure encoding cost in the pilot. High-strength per-pixel animated grain made one 41-second pilot about 1 GB; coarser 2x2 grain at lower strength plus CRF 18 reduced the later master to about 399 MB. Those are observations from different pilot passes, not a controlled benchmark. Tune grain and inspect motion before sacrificing the whole image to more compression. Keep a master and a smaller review derivative, clearly labeled; CRF 18 and 24 were useful starting points in this production, not universal settings.

**Measured 1080p60 `-tune grain` throughput (2026-10-17):** In the `pdoom-video` offline renderer (`app/scripts/render.ts video`), `ffmpeg` encodes with `-c:v libx264 -tune grain`. On Apple Silicon at `1920x1080 @ 60fps` (`--crf 18 --preset medium --workers 3`), the 3 headless Chrome Metal GPU workers are bottlenecked by `x264 -tune grain` on the CPU and sustain **`22.7–23.2 fps` overall (`687.6 s` / `11m 27s` for `15,601` frames / `260.014 s`, `1.2 GB` output)**. State ETAs from this ~2.6× real-time full-pipeline throughput (~11–12 minutes for a 4.5-minute 60fps track), never from GPU-only frame render times (~3 minutes).

Render chunks to temporary names and mark them complete only after successful encoding. Resume only chunks whose source/audio/analysis identity, frame range, dimensions and encoding settings match the current render. File existence alone is insufficient after code or timing changes. Keep concurrent workers within the machine's measured capacity.

Stream or chunk SHA256 hashing for large media. Reading a multi-gigabyte video into a single Node buffer failed after a successful 2.9 GB export. Separate manifest generation from rendering so a failed bookkeeping step can be repaired without rerendering the film. A repaired manifest must identify the source revision actually rendered, not silently bind the video to newer source files.

Preserve the selected original audio as the mux source; do not compound lossy encoding by using the browser playback derivative. If delivery compatibility requires transcoding, derive it from the original and record the codec conversion. Check final-frame coverage and audio/video endpoints on the encoded output, allowing for documented frame rounding.

## Toolchain gotchas (verified 2026-10-16 & 2026-10-17)

- **`timeout` does not exist on macOS by default.** Every command prefixed with `timeout` fails with exit 127 and produces empty stdout when stderr is suppressed or piped, which then reads as an empty finding. Six scans were reported as results on 2026-10-16 before this was caught.
- **`mlx-whisper` and `faster-whisper` fail to build here** (dependency conflicts; the `av` wheel fails to compile). `brew install whisper-cpp` works reliably — use `whisper-cli -m ggml-small.en.bin`.
- **`librosa` 1.0's `beat_track` returns an `ndarray` for `tempo`** rather than a Python float; wrap it in `float(np.atleast_1d(x)[0])`. When `librosa` is not installed in system Python, run data-generation scripts via `uv run --with librosa python3 tools/make-data.py`.
- **The `pdoom-video` engine's GLSL `fbm` helper requires an explicit octave count:** call `fbm(uv, 3)`, never `fbm(uv)`.
- **Returning `shake: undefined` from a scene's `PostOverrides` crashes the post stage** (`engine.ts` destructures `[sx, sy]`); always return a concrete tuple `shake: [number, number]` (or omit the key).
- **`app/scripts/render.ts stills` takes `--t`, not `--at`:** passing `--at 2.5,6.5,...` is silently ignored and renders only `t = 0.00 s` (`f_0000.00.png`). Always pass `--t 2.5,6.5,...`.

## YouTube release handoff

Once the user wants to publish the finished video, read `youtube-release.md` for title, description, channel bio, Suno rights and YouTube AI disclosure. A completed render or upload is not evidence of a public release. Keep the artist-specific copy and actual publication status beside the durable release materials.

## Improve the skill from the experiment

Record the failed version, attempted correction, technical result and latest user verdict separately. Label a proposed remedy as unproven until reviewed; technical improvement does not imply creative acceptance. Keep song-specific media, private stories and generation logs out of reusable skill references. For song deliveries, include the selected model and a proposed control preset, conditional on available controls. Identify suggested slider values as untested until auditioned.
