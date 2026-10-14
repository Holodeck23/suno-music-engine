# From a selected song to a code-driven music video

Use this mode when the user wants an animated video for an accepted song. It is separate from using a video as a musical reference in Suno. Preserve the user's chosen recording and visual direction; do not regenerate the song to simplify animation.

## Audio is the timing authority

Keep the original audio, its SHA256, generation identifier if present, accepted lyrics and timing source in the durable production folder. Inspect codecs, duration, metadata and subtitle streams before proposing transcription or an external API. Some Suno M4A downloads contain a timed `mov_text` lyric track, even if the actual audio codec is Opus.

Run `python3 scripts/extract-video-timing.py AUDIO OUTPUT.json` from the skill directory when FFmpeg and FFprobe are available. The helper does not overwrite outputs or upload media. It separates bracketed section directions from singable lyric cues and flags unusual durations. Embedded timing is a starting point, not independent verification: check it against playback. Preserve raw cue times. A very short isolated caption may need a longer display hold for readability; record the adjustment separately, never overlap the next sung cue, and do not alter the audio or claim improved transcription accuracy. Missing subtitles are a reason to arrange transcription or manual alignment, not to invent exact timestamps from drafted bars or BPM.

A browser-compatible AAC playback derivative may be useful when the source uses an unsupported codec. Preserve the source and document the conversion. Do not assume an M4A extension implies AAC. Measure the actual track duration; genre/BPM and bar lengths in a generation prompt are targets, not a measured beat grid.

## Word-level timing for kinetic type

Embedded Suno cues are line-level, their end times are often a flat placeholder, and their start times can drift far from the recording. In one observed song the final-chorus cue ran 24 seconds early and the sung bridge was 10 seconds late. Kinetic typography needs each word.

1. Separate stems (for example `demucs -n htdemucs_ft`) and use the vocal stem.
2. Run `scripts/align-lyric-words.py TIMING.json VOCALS.wav WORDS.json`. It transcribes with word timestamps, aligns the known lyric to the heard words, accepts a match only near its own cue, and interpolates the rest. Report the matched/total count.
3. Read the raw transcript for lines the sheet lacks: repeated ad-libs, a sung bridge, a closing repeat. Add them from transcript word times and record each addition.
4. Whisper stretches a phrase's first word back across the preceding silence. Pull only that first word's start toward its end. Long later words are usually genuinely held notes; shifting them hides the word for most of its sung duration.
5. Expect the transcript to "hear" prompt lyrics over a long instrumental intro when the lyric is supplied as a prompt. The cue window is what keeps those out.

## Study the reference, then set a design system

When the user points to videos they admire, inspect actual frames before designing: a contact sheet at one frame per 8 seconds, a few full frames, and a measured cut rate (`select='gt(scene,0.3)'`). The channel the user studied (Claude-made music videos, credited three.js/TypeScript and Blender/Python) works through:

- **Typography as the main image.** Words appear as they are sung, with the active word in the accent colour, upcoming words dim or absent and sung words settled. This requires word timing.
- **One visual idea per lyric line.** Each line becomes a diagram, interface or object that literalises a double meaning, for example a spending line rendered as tokens with token IDs. Captions over an illustrated scene are weaker than type that carries the scene.
- **A strict system.** One dark ground, one accent colour, a display face plus a monospace face for small interface labels, and consistent framing chrome. The accent can carry the arc (cold before a turn, warm after).
- **Density.** A new idea every 2 to 4 seconds in busy passages (measured 1.8 to 3.5 seconds average shot length). Calmer pieces use moves and morphs instead of hard cuts.
- **A review editor built for the project.** The creator watches drafts and marks frames and ranges for change.

Lyric-driven type and music-driven motion are complementary, not alternatives. Let words drive the typography and per-line ideas. Let stems and the beat grid drive light, camera, impacts, particles and any interface readouts. Readouts that show real values (bar count, drum envelope as pressure, bass envelope as torque) make the frame look like it is listening.

## Pilot before full-song production

Write a brief that establishes palette, characters, props, world, focal actions and transitions. Map the opening pilot to actual cue times. Around 20-30 seconds is a useful first scope, not a universal requirement. Build something the user can watch and critique before filling the whole song. Once the user accepts the experiment or delegates the artistic choices and asks you to finish, proceed with the full film without imposing another approval round.

Choose tools for the intended look: three.js for procedural 3D, Canvas/p5 for drawn 2D, Blender/Python when offline scene rendering is preferable. A toolkit or instruction document can help, but no particular plugin, external image model or video API is inherently required.

Evaluate every frame from absolute audio time. Avoid accumulated simulation state and unseeded randomness. Seeking away and returning to a timestamp should reproduce the frame. Drive reactive movement from an archived audio envelope or a measured beat grid rather than a live input unavailable to the offline renderer.

Contact sheets catch framing and composition; motion playback catches unreadable actions, accidental freezes, bad cuts and synchronization. Use both. A passed build or attractive still image does not establish that the video works at playback speed.

Render style frames across the pilot before any motion render; they are cheap and catch most look problems. Problems observed on the first style pass of an HDR pipeline, with the fixes that worked:

- **Bloom swallows the type.** Push only accent-coloured pixels into HDR, set the bloom threshold at true overexposure (1.0), and keep white and neutral type below it.
- **Particles near the lens become a white blob.** Cap point size and keep emitters out of the near field. Use moderate additive intensity.
- **Busy backgrounds kill legibility.** Put a dark halo (shadow blur) behind display type and dim the background layer during text-heavy shots.
- **Long rows overflow.** Fit each row to a maximum width using its full eventual text, not only the words sung so far.
- **An additive flash before tonemapping reads as a grey frame.** Keep impact flashes short and strong.
- **Layer order hides props.** If interface chrome sits on a layer composited above the type, an opaque dialog or darkening panel on that layer covers the words. Put opaque props on the type layer beneath the words, and erase chrome rather than painting black over it.
- **Eased burns finish before the eye catches them.** Use linear progress for destruction effects that should be watched.

## Extending a pilot to the full song

Write a shot table that covers every second: one shot per sung line, plus music-driven shots for instrumental stretches (intro, solo, breaks). Instrumental shots can visualise real analysis: an engine firing on drum onsets, a live stem mixer, a scrolling trace of the lead stem. Carry an arc across the film: a colour story (cold before the turn, warm after) and an ending that answers the opening. Render a style frame from every shot across the whole song, in one contact sheet, before the long render.

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

## Improve the skill from the experiment

Record demonstrated failures and the correction that worked. Add portable guidance after observing behavior; keep song-specific media, private stories and generation logs out of reusable skill references. For song deliveries, include the selected model and a proposed control preset, conditional on controls actually available. Identify suggested slider values as untested starting points until auditioned.
