# Visual Lesson Production: Programmatic Visuals for Narrated Lessons

This guide merges and replaces the former music-video and instrumental-video guides. Part 1 is the lesson renderer: four visual states driven by `lesson-manifest.json` and `resolved-timeline.json`. Parts 2–4 keep every timing, design, rendering and verification lesson from the music-video productions, unchanged. When applying them to a lesson, read "song", "lyrics" and "selected audio" as "lesson", "narration" and "the rendered narration plus the selected BGM take".

Read `video-direction-and-quality.md` for reference craft, quality resets, camera-jump prevention and the mobile-legibility rules. Read `script-and-retention-engine.md` for the manifest and `bgm-suno-scoring.md` for the bed. For bundled helpers and project-specific implementations, see `../docs/video-capabilities.md`.

## Part 1: The Lesson Renderer

### Inputs and the render contract

| Input | Producer | Used for |
|---|---|---|
| `lesson-manifest.json` | The script (validated) | Payloads: headline, code, diagram entries, trigger actions |
| `resolved-timeline.json` | `scripts/generate-tts-and-cues.py` | Gapless `slots`, word and trigger times, `transitions`, `camera_move` events, `chapters` |
| Its `bgm` block | `scripts/extract-video-timing.py --merge-into` | Beats, estimated downbeats, onsets, absolute dBFS envelopes (per stem too), the hook-drop alignment |
| `master-audio.wav` | `scripts/mix-voice-and-bgm.py` | The only audio muxed into the export |
| `artifacts/<segment id>.png` + `.json` | Captured in the production folder | `artifact_pan` images and their highlight regions |

- **Every frame is a pure function of absolute time.** At time `t` the renderer looks up the active slot, every trigger at or before `t`, the camera moves around `t`, and the bed's envelope and beats at `t`. It keeps no accumulated state, so seeking away and back reproduces the frame and chunks can render in any order (Part 2, "Pilot before full-song production").
- **Lock the frame rate.** Choose one fixed rate for the whole lesson (24, 30 or 60 fps) and evaluate frame `n` at exactly `n / fps`. Never advance time by measured frame durations.
- **Never re-time.** Triggers fire at their word's start time, slots change at their start, and camera moves begin at their event time. The word-count estimates in the manifest validator are for planning only; the timeline comes from the rendered narration.
- **Slots are gapless.** Segment slots alternate with transition slots (`intro`, `drop`, `swell`, `outro`), and every second of the lesson belongs to exactly one slot, so no second falls through to an accidental fallback.
- **One design system.** One dark ground, one accent colour, a display face plus a monospace face, consistent framing chrome. The accent can carry the arc. The HDR, halo, fit-to-width and layer-order rules in Part 2 apply to code and diagram type as they do to lyrics.
- **Mobile legibility is a hard requirement.** Minimum text sizes, the 45-column code limit and the 6–8 second change rule are in `video-direction-and-quality.md`. The timeline already inserts a `camera_move` event wherever nothing else would change for more than 7 s.

### State 1: `vibe_drop`

A full-screen, audio-reactive visualizer or shader driven by the Suno bed.

- **Used for:** the transition slots (intro, the hook drop, swells before the Verdict, the outro), typically 3–5 seconds, and `vibe_drop` segments (the Hook, usually the Verdict).
- **Driven by measured audio:** `bgm.envelope.dbfs` and the per-stem envelopes for intensity, mass and colour; `bgm.beats` for pulses; `bgm.downbeats` for larger accents. Map dBFS through a fixed floor, never per-track percentile scaling, so an absent instrument stays dark (Part 3, "Offline analysis contract"). Downbeats are estimates; check them against playback.
- **The hook drop:** the impact lands at the `drop` transition's start, which `extract-video-timing.py` aligns to a measured downbeat (`bgm.hookDrop`), and lasts until `drop_end` (3 s). A `drop` trigger adds another impact inside a `vibe_drop` segment. Keep impact flashes short and strong; an additive flash before tonemapping reads as a grey frame (Part 2).
- **With narration over it:** show the headline (at its `show_headline` trigger, or at segment start) with a dark halo, and dim the visualizer while text is on screen.

### State 2: `code_focus`

- **Background:** the same visualizer keeps running underneath at **15–20% opacity**, so the music still has a visible pulse but never competes with the code.
- **Foreground:** dark-mode, syntax-highlighted code or terminal output in the monospace face. Use a fixed highlighting theme so every render tokenises identically. In terminal blocks, distinguish the `$` command lines from their output.
- **Reveal on the word:** `reveal_line_<n>` shows lines 1 through `n` at the trigger word's start time. `highlight_line_<n>` moves the accent bar to line `n`. A snippet with no reveal triggers is fully visible from the start of the segment. A typing animation is optional, but each line must finish within about 0.3 s of its word so the reveal never lags the narration.
- **Fit:** the validator rejects code lines over 45 columns (tabs count as 4). Size the block so its longest line fits the frame at or above the minimum code size; never scroll a line off a phone screen.

### State 3: `architecture_graph`

- **Graph:** `diagram_nodes` entries are node labels or chains (`A -> B -> C`). Merge them into one graph by label. Compute the layout once per segment and deterministically: a layered left-to-right layout in chain order, or a seeded force layout. Never lay it out per frame.
- **Reveal and activity:** `reveal_node_<n>` brings in entry `n` and its edges on the word. `highlight_node_<n>` makes those components active: they glow in the accent colour and pulse on `bgm.beats`, while inactive components dim. The spoken trigger decides *what* is active; the beat only decides *how* it pulses.
- **Flow:** animate edge direction as a function of absolute time (dash offset = speed × t). Push only accent pixels into HDR, so labels never bloom (Part 2).

### State 4: `artifact_pan`

- **Artifact:** a clean, dark-mode viewport framing a real artifact: a repository README, a release note, a paper figure, a benchmark chart. Store the capture as `artifacts/<segment id>.png` in the production folder. Record its source URL and capture date in `artifacts/<segment id>.json`. Show real artifacts only; never mock up a benchmark, chart or release note.
- **Regions:** in an `artifact_pan` segment, `diagram_nodes` lists the artifact's named regions in order. Their boxes live in the sidecar as `"regions": [{"box": [x, y, w, h]}]`, in 0–1 image coordinates, in the same order. `reveal_node_<n>` zooms to region `n`; `highlight_node_<n>` draws the accent box around it and dims the rest. The validator then keeps every region index in range.
- **Motion:** a slow programmatic pan and zoom, eased on absolute time, moving between regions on their trigger words. Zoom until the highlighted text meets the mobile minimum size; text inside screenshots rarely does at full frame.

### Transitions and camera moves

- Cut or morph at slot boundaries. Every boundary gets the camera-state comparison and paired-frame checks in `video-direction-and-quality.md`; near-matching views with abrupt changes read as glitches.
- A `camera_move` event starts a gentle, continuous move: a slow push-in, a lateral drift or a re-frame, eased over 1–2 seconds. It never jumps. Smooth fast control curves before applying them to global position or scale.
- Motion intensity follows `bgm_mode`. In `ducked` segments motion stays calm so the explanation leads; in `vibe_drop` slots the bed drives light, camera weight and impacts (Part 3).

### Pilot, review and export for a lesson

1. **Pilot** the Hook, the drop and the first Mechanism block at full quality with the mixed `master-audio.wav`. Review a contact sheet and real-time playback, and check that every reveal lands on its word.
2. **Expand** to the full lesson only within the direction the pilot established or the user delegated (Part 2).
3. **Export** by muxing `master-audio.wav`, never the narration alone, with the rendered frames. Check dimensions, frame rate, decode success, and video and audio duration against `resolved-timeline.json`.
4. **Check for dead stretches:** `ffmpeg -i lesson.mp4 -vf freezedetect=n=-60dB:d=8 -map 0:v -f null -` reports every stretch of 8 seconds or more without visible change. It catches dead frames, not meaningful change; a dimmed visualizer that keeps moving passes it, so it backs up the camera-move events rather than replacing review.
5. **Bind** the export's hash to the manifest, narration, BGM take, timeline and renderer source revision. Report only the states actually reached (Part 2, "Export and verify").

## Part 2: Timing, Design and Rendering Lessons

Use this mode when the user wants an animated video for an accepted song. It is separate from using a video as a musical reference in Suno. Preserve the user's chosen recording and visual direction; do not regenerate the song to simplify animation.

### Where the work lives

Keep two homes and never mix them. The renderer's code goes in its own version-controlled repository (initialise it with the first file). Everything the production makes or consumes goes in one durable production folder per song: the selected audio and its hash, the song sheet, stems, analysis, timing, every render pass, contact sheets, treatment and production log. The repository links to that folder (symbolic links for the audio and analysis) rather than copying media into itself, and build output stays ignored. A render finished in any tool's own output or scratch directory is copied into the production folder's `renders/<pass-name>/` in the same turn, and the log records where it is. When a machine has its own workspace rules for these locations, they take precedence over this paragraph.

### Audio is the timing authority

Keep the original audio, its SHA256, generation identifier if present, accepted lyrics and timing source in the durable production folder. Inspect codecs, duration, metadata and subtitle streams before proposing transcription or an external API. Some Suno M4A downloads contain a timed `mov_text` lyric track, even if the actual audio codec is Opus.

Run `python3 scripts/extract-video-timing.py AUDIO OUTPUT.json` from the skill directory when FFmpeg and FFprobe are available. The helper does not overwrite outputs or upload media. It separates bracketed section directions from singable lyric cues and flags unusual durations. Embedded timing is a starting point, not independent verification: check it against playback. Preserve raw cue times. A very short isolated caption may need a longer display hold for readability; record the adjustment separately, never overlap the next sung cue, and do not alter the audio or claim improved transcription accuracy. Missing subtitles are a reason to arrange transcription or manual alignment, not to invent exact timestamps from drafted bars or BPM.

A browser-compatible AAC playback derivative may be useful when the source uses an unsupported codec. Preserve the source and document the conversion. Do not assume an M4A extension implies AAC. Measure the actual track duration; genre/BPM and bar lengths in a generation prompt are targets, not a measured beat grid.

### Word-level timing for kinetic type

Embedded Suno cues are line-level, their end times are often a flat placeholder, and their start times can drift far from the recording. In one observed song the final-chorus cue ran 24 seconds early and the sung bridge was 10 seconds late. Kinetic typography needs each word.

1. Separate stems (for example `demucs -n htdemucs_ft`) and use the vocal stem.
2. Run `scripts/align-lyric-words.py TIMING.json VOCALS.wav WORDS.json`. It transcribes with word timestamps, aligns the known lyric to the heard words, accepts a match only near its own cue, and interpolates the rest. Report the matched/total count.
3. Read the raw transcript for lines the sheet lacks: repeated ad-libs, a sung bridge, a closing repeat. Add them from transcript word times and record each addition.
4. Whisper stretches a phrase's first word back across the preceding silence. Pull only that first word's start toward its end. Long later words are usually genuinely held notes; shifting them hides the word for most of its sung duration. A long first word can also be held, so do not apply a blanket length rule: check the vocal stem's energy (40 ms RMS against a fixed floor) for each long first word and move its start to where the voice actually begins. On one track two of six long first words were genuinely held and a blanket rule would have hidden them.
5. Expect the transcript to "hear" prompt lyrics over a long instrumental intro when the lyric is supplied as a prompt. The cue window is what keeps those out.

### Scored events: measure each one, then mark it located or absent

Suno treats bracket directions as weak hints. Silences, breaks, strips, builds, intro lengths and outro hits written into the lyric field frequently do not exist in the take, or exist somewhere else. Before designing, test each scored event against the audio and record it as located fact (start, end, evidence) or absent:

- Scan the mix at 20 ms RMS for genuine dropouts; a "silence" that the mix never reaches is not a silence.
- Tabulate per-bar RMS for each stem against the downbeats. Strips, drum dropouts and bass drops show up as one stem falling 40 dB or more for a bar while the mix barely moves.
- Zoom (100 ms windows, beats marked) on every region the brackets describe.
- Read the transcript for sections the sheet does not have: post-chorus ad-libs, an added hook at the top of a final chorus, a spoken bridge that keeps its drums.

Then design to the located facts. An absent event is not faked with a visual: on one track the scored 2-beat silence before the final chorus did not exist, so the edit used a hard cut to clean frame on the downbeat instead, and the "stripped" bridge kept its drums, so the visual valley went to the 3 s where the band really dropped out. Novelty-based section detection can also fail outright (one 92 s block); stems plus word times gave a usable map.

### Study the reference, then set a design system

When the user points to videos they admire, inspect the exact reference and its credits. A sparse contact sheet and scene-change detector help locate passages; close motion study establishes how they work. Follow `video-direction-and-quality.md` for that breakdown. Different films by one creator can use different engines. Record creator-confirmed tools separately from inferred techniques.

The following are options observed in lyric-led reference work, not requirements for every film:

- **Typography as the main image.** Words appear as they are sung, with the active word in the accent colour, upcoming words dim or absent and sung words settled. This requires word timing.
- **Line-led visual ideas.** A line can become a diagram, interface or object that carries a double meaning. This can suit a graphic treatment; a film that promises acting or narrative needs actions that develop across lines. Literalising every line can become a slide deck.
- **A strict system.** One dark ground, one accent colour, a display face plus a monospace face for small interface labels, and consistent framing chrome. The accent can carry the arc (cold before a turn, warm after).
- **Density.** Some studied busy passages changed ideas every 2 to 4 seconds. Use the selected reference and musical phrase to judge pace; cut counts are diagnostic, not a quality target. Calmer pieces can use sustained action, moves and morphs.
- **A review editor built for the project.** The creator watches drafts and marks frames and ranges for change.

Lyric-driven type and music-driven motion can complement each other. Where the treatment uses them, let words drive type and measured musical events motivate light, camera and impacts. Real analysis can drive interface readouts, but explanatory graphics and constant beat pulses do not substitute for compelling shot design.

### Pilot before full-song production

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

### Extending a pilot to the full song

Write a shot table covering every second, including instrumental stretches. Shots can span multiple lines or split a phrase according to the action; one shot per line is an option for graphic treatments. Make coverage gapless so no second falls through to an accidental fallback. Give each shot an optional style-frame time for its key reveal and emit a whole-film contact sheet. Instrumental passages may use performance, story action or analysis-driven imagery. Carry a deliberate arc and a payoff that follows from the premise. Check the whole-film board and rough timing before the expensive render, while retaining early motion proofs for risky shots.

### Make direction specific and portable

A local preview can offer play/pause, scrubbing, frame stepping, shot selection, subtitle offset and frame/range annotations. Feedback should identify:

- Target timestamp or range and object/shot.
- What to preserve.
- One concrete change.
- How to tell the revision worked.

Bind exported notes to the source-audio hash and any subtitle offset. Browser storage is convenient persistence, not the durable archive: export feedback beside the song. Render user notes as text rather than raw HTML.

### Export and verify

Use the same scene evaluation and typography in preview and export. Confirm the headless browser renders on the GPU before estimating render time: query `WEBGL_debug_renderer_info`. On macOS, Playwright with the installed Chrome channel and ANGLE Metal reported the Apple GPU, while the bundled headless shell may be missing. Pipe frames to the encoder in resumable chunks rather than storing full-resolution PNG sequences. With headless browser screenshots, wait for fonts and compositor paint after rendering, especially after viewport changes. Test identical timestamps in non-sequential order. A scene may be deterministic while screenshots still capture stale browser paint.

Mux the accepted audio with rendered frames and check output dimensions, frame rate, video/audio duration, decode success and representative frames. Bind the output hash to the audio hash, timing file, caption offset and source revision or file hashes. Preserve intermediates needed to reproduce or investigate the export.

Distinguish these states: pilot built, browser checks passed, render exported, playback visually/audibly reviewed, user accepted, full song complete. Report only states actually reached. Do not claim to have listened when only metadata or subtitles were inspected.

### Large renders, resumability and delivery size

Measure encoding cost in the pilot. High-strength per-pixel animated grain made one 41-second pilot about 1 GB; coarser 2x2 grain at lower strength plus CRF 18 reduced the later master to about 399 MB. Those are observations from different pilot passes, not a controlled benchmark. Tune grain and inspect motion before sacrificing the whole image to more compression. Keep a master and a smaller review derivative, clearly labeled; CRF 18 and 24 were useful starting points in this production, not universal settings.

Render chunks to temporary names and mark them complete only after successful encoding. Resume only chunks whose source/audio/analysis identity, frame range, dimensions and encoding settings match the current render. File existence alone is insufficient after code or timing changes. Keep concurrent workers within the machine's measured capacity.

Stream or chunk SHA256 hashing for large media. Reading a multi-gigabyte video into a single Node buffer failed after a successful 2.9 GB export. Separate manifest generation from rendering so a failed bookkeeping step can be repaired without rerendering the film. A repaired manifest must identify the source revision actually rendered, not silently bind the video to newer source files.

Preserve the selected original audio as the mux source; do not compound lossy encoding by using the browser playback derivative. If delivery compatibility requires transcoding, derive it from the original and record the codec conversion. Check final-frame coverage and audio/video endpoints on the encoded output, allowing for documented frame rounding.

## Part 3: Music-Driven Motion

Use this part when motion should follow the bed's instruments as well as the narration, or for instrumental and vocal music videos. Missing subtitle streams are normal for an instrumental; do not invent lyric timing or require a transcription stage.

### Let the recording determine the structure

Preserve the selected audio and its identity. Measure actual duration, then derive the visual treatment from four timescales:

| Timescale | Audio evidence | Visual role |
|---|---|---|
| Form | Sections, repeated motifs, changes in instrumentation | Worlds, palette evolution, major transformations |
| Phrase | Downbeats, phrase starts, builds and drops | Camera moves, reveals, anticipation and cuts |
| Beat | Beat events and individual stem onsets | Impacts, pulses, sparks and brief light changes |
| Texture | Per-stem level, envelopes and spectral brightness | Density, mass, speed, roughness and colour |

Give stems distinct jobs: drums can drive impacts, bass can drive mass or camera weight, and melodic content can drive form or colour. When an instrument drops out, its layer should empty. A single full-mix volume envelope cannot represent that distinction.

### Offline analysis contract

Archive measured events and sampled feature curves beside the selected audio. The renderer should evaluate them at any absolute time without live audio input.

1. Create a documented analysis derivative without replacing the original. Separate stems where the visual treatment benefits from them. The production experiments used Demucs `htdemucs_ft` and `htdemucs_6s`; model names are choices, not a guarantee of clean isolation.
2. Detect beats and downbeats, then cross-check against drum onsets across the whole recording. Beat This! and librosa were used in the experiments. Treat median BPM as a summary, not a fixed animation clock: one take drifted from about 129 to 132 BPM, and a grid at the requested 128 BPM matched only 29% of measured kicks.
3. Propose sections from novelty/chroma/MFCC analysis and inspect per-bar stem energy. Machine boundaries remain proposals until checked. A novelty kernel sign error once collapsed an entire song into one section; even a corrected detector later produced an unhelpful 92-second block. Use stems, words where present, and playback to resolve boundaries.
4. Compute per-stem level, smoothed attack/release envelopes, onset strength and spectral brightness at an explicit control rate. The existing project pipeline uses 120 Hz, interpolated to video timestamps. Record rate, frame count, curve names, numeric dtype and layout; validate byte length before loading a binary feature file.
5. Keep raw beat events and any corrections separately. Record located versus absent scored events using Part 2. Do not turn requested silences, intro lengths or bar counts into measured facts.

Inspect stem leakage. A six-stem "guitar" output contained a distorted synth in a guitar-free intro; it was useful as a mid-range lead layer, not evidence of an isolated guitar. A "vocals" stem can contain effects and separation residue on an instrumental.

Retain an absolute noise floor when normalizing. Per-track percentile scaling can inflate an absent instrument's residue into full motion. Test whether the stem is actually present, gate inactive layers, and record the thresholds used. Check onset thresholds and minimum separation so one attack does not become several impacts.

### Reproducible musical motion

Use measured beat/bar events for phase. A precomputed monotone musical-time curve, the integral of a smoothed energy curve, lets motion accelerate with the music while remaining a function of absolute time. Seed procedural randomness and use time-indexed event lookup rather than advancing a cursor on every preview frame.

History-dependent fluids or particle advection need fixed-step simulation and saved checkpoints, or a closed-form approximation. A seek must restore a checkpoint and replay deterministically rather than inherit the previous preview state. Test timestamps in a non-sequential order before parallel rendering.

Anticipation can use the known future drop: tighten framing or reduce light in the preceding phrase. This is a creative choice, not a rule that every cut must land on a downbeat.

### Treatment and rendering choices

Map motifs to musical layers and an evolution across the track. Keep the representative motion proof and whole-film review workflow from Part 2. For a demanding reference or rejected draft, use `video-direction-and-quality.md`; synchronized feature curves alone do not establish compelling imagery. Do not add a new approval gate when the user has delegated direction and completion.

Choose effects for the aesthetic. HDR materials, selective bloom, volumetric light, instancing, reaction-diffusion and raymarched forms are possible techniques, not a mandatory stack. Some remained proposals in the instrumental approach notes; do not describe them all as implemented or tested.

Optional offline motion blur averages deterministic subframes across a shutter interval in linear HDR before tonemapping. Supersampling can improve fine geometry and type but increases cost. Benchmark a short representative range first. Paper/ink treatments need the light-ground rules in Part 2 instead of blindly applying a dark-scene filmic grade.

### Tooling boundary

The skill ships embedded-cue and BGM beat/onset/envelope extraction (`extract-video-timing.py --beats`), word alignment, narration and timeline compilation, and the envelope mixer. It does **not** ship a stem-separation or rendering executable. The existing video projects contain `prepare.sh`, `analyze.py`, feature samplers and renderers; consult the capability inventory in `docs/video-capabilities.md` before assuming a command is installed with this skill.

When adapting those implementations, parameterize source and output paths, preserve their provenance, verify dependencies against the target machine, and validate on known synthetic events plus a representative real recording. Keep toolchain recommendations separate from a claim that every dependency is already installed.

## Part 4: Narrative Continuity, World Systems and Renderer Lessons

Read this part for narrative continuity, world-building, rendered characters or renderer choice; for a rejected draft or ambitious reference, also read `video-direction-and-quality.md`. The city and character experiments below produced technical lessons, but their full-film result was not creatively accepted. Audio timing and deterministic export still apply.

### Why a polished lyric video can feel dead

A cut with a separate pun for every line can feel like slides when nothing carries over. Narrative continuity can come from a character, recurring object, connected places or consequences that persist. A treatment helps expose missing causality, but cannot guarantee strong imagery or performance. A busy world can still feel lifeless if shots lack a designed subject.

### Order of work: story before shot list

0. **Study the target.** Reuse saved references and closely inspect a useful moving sequence. A contact sheet helps compare subject, palette and scale, but misses acting and transitions. Keep observations beside the production board.
1. **Treatment.** State who or what changes, the visible attempt and its consequence, and the intended feeling. Map dramatic beats to measured sections, or draft song and story together if the recording is still open. Save it in the production folder.
2. **Beat board.** Sketch or render key beats cheaply. Real-engine stills verify feasibility; drawings can answer story questions before assets exist. Do not confuse either with motion proof.
3. **Risky shot and animatic.** Prove the hardest representative action early. Assemble rough timing across the song to assess setup, escalation, quiet and payoff before expanding final assets. Choose the order around the actual risk rather than requiring a full rendered animatic first.
4. **Look development and final render.** Expand the direction supported by the evidence and authorized by the user. Rejection calls for a creative reset, not automatic completion of the same premise.

### Options for narrative continuity

- **Connected places or recurring subjects.** A camera travelling through a connected space can establish geography; motivated cuts between different places can also carry a story. Choose around the action rather than imposing a one-room or continuous-camera rule.
- **Memory as dated events.** Model the story as events with times: a sign switched on, a sweep reaching it at `t0 + distance / speed`, a reboot, a final kill. The state at time `t` is "every event at or before t", computed from `t` alone. The world remembers (what was killed stays dead) and every frame still renders out of order, which the deterministic exporter requires.
- **Type with a role.** Diegetic words can live on signs, screens, glass or ink; stage typography or overlays can also suit the film. Keep sung words timed and legible without making every scene an explanatory card.
- **Deliberate colour development.** A limited palette or a held-back colour can support a turn. The story need not assign exactly one meaning to every hue.
- **An act break can invert the whole palette.** Draining a night city into a white paper world, where the character becomes an ink silhouette, marked the bridge more strongly than any cut.
- **The ending pays off the setup.** Reframing the opening place after a change is one option; a new image can also complete the arc.

### Optional world systems, each a pure function of time

Select only systems the shot needs. Crowd, traffic and weather increased activity in one experiment without establishing a compelling film. Performance and consequences deserve priority over adding simulation layers:

- **A crowd** on sidewalks: position = phase + speed × t, wrapped along a lane. Give them a state the story can change: heads down with lit phones while the hype holds, heads up after the protagonist's act.
- **Traffic** as paired head/tail lights on lanes, braking (tail lights flaring) on the kick.
- **Weather.** Rain anchored to the world and wrapped around the camera (`x = camX − B/2 + mod(seedX·B − camX, B)`), tinted by the light it falls through.
- **Other lives in windows.** Some lit windows switch on and off on their own slow clock; a few flicker like a TV.
- **Things that move on their own.** Drones on orbits, which can fall when the story hits them (a free fall from the event time) and stay where they fell.
- **Character movement.** Breath and weight shifts can sustain a held pose; motivated stillness can be stronger than constant idle movement.
- **Camera weight.** Easing, settling and restrained drift can support action; a locked camera may better stage a reveal. Do not add a shove to every kick by default.
- **Signs.** Pulse, LED rows or glitch tears when motivated. A static sign can leave attention on the action.

### A procedural character that holds up

A jointed capsule figure with blended poses and a distance-driven walk cycle can serve a distant silhouette or intentionally graphic style. It is not a general solution for hero acting, hands or tactile close-ups. Test posture, silhouette, contact and weight at the intended shot scale; use authored shapes, a suitable rig or another style when the proxy fails.

- Rim term around `pow(1 − N·V, 4)` at low gain. A strong or wide rim turns the figure into a glowing mannequin; this happened and read as a toy.
- On a light ground, render the figure as flat ink with a soft blob shadow.

### Local technical failures and attempted corrections

The following fixes address specific rendering defects. They did not establish creative acceptance of the resulting film. Numerical values depend on the scene's scale, exposure and materials.

- **Grid cities hide the faces a street camera needs.** Looking down an avenue, every billboard mounted flat on a facade is seen edge-on or blocked by the block in front. Fix: blade signs hung out from side faces and facing along the street, and banners strung across the road for lyrics. Also open a view corridor (lower the blocks directly in front of a hero window) so the character looks *out* over the city rather than into a wall 12 m away.
- **Check the camera's line of sight against its own building.** A camera on a roof looking down at targets in the street saw only the roof surface and rendered a black frame. Move it to the edge.
- **Window grids too big, too many and too bright read as a toy city.** Keep lit windows to about 15 percent, small, dim and varied (cool and warm, ribbon offices and punched homes), with near-black facades.
- **Coloured spill painted onto whole facades looks fake.** Keep facade spill under about 0.5 percent of the light's colour. Put strong spill only on wet ground, rain and the character's rim.
- **Volumetric shapes made of transparent geometry look like boxes.** An additive cylinder meant as a sweeping wave of light rendered as a solid blue block. Put the event on surfaces instead: a thin scan line where the wave's radius meets facades and ground. A facade facing the wave's centre lights all at once, so keep the line's glow short (a flash), not a lingering band.
- **Sung words blown out to white.** Use a pale tint of the accent for the active word, not white, and keep panel glow multipliers around 1 to 2 under bloom.
- **Wrapped lines broke mid-phrase.** Lay out each lyric line as its own row and wrap within it; never flow a multi-line lyric as one word stream.

### Probing cheaply

Probe a few risky frames before a large batch; measure cost on the current scene. Use an early short motion render for acting and contact, which stills cannot validate. Save both the probe and its conclusion so a later session does not repeat it.

Report states honestly: a beat board is stills. It does not show whether motion, sync or pacing work. Say what has and has not been seen in motion.

### Renderer choice: isolate cost and image quality

An identical-world/camera comparison can isolate renderer differences, while a target-native representative shot tests the candidate's strengths. One same-frame test (1080p, Apple M5, a night city of plain box towers, about 500 signs) observed the following; remeasure rather than reuse these as budget estimates:

- Blender EEVEE at 32 samples: about 2 s per frame after shader compilation.
- Blender Cycles at 256 samples on the Metal GPU: about 3 minutes per frame. That test would be expensive to expand; it does not establish a universal Cycles cost.
- On that box geometry, neither Blender still showed a persuasive quality improvement. This is evidence about the test, not the engine's ceiling. Modelled detail and suitable materials give lighting more to describe; glTF assets can also be used in a browser engine. Acting, composition and editing remain separate decisions.
- Blender-specific traps seen in that test: the AgX view transform turns saturated neon pastel (Khronos PBR Neutral or Standard keeps the hue); an area light placed just in front of a sign blows it out; world-volume haze over-scatters fast (density around 0.002 to 0.003 at city scale); depth of field at a wide aperture blurs the nearest signage text.

### Measure the reference before polishing: pace, palette, close-ups

Compare existing reference and draft sheets to identify scale, palette and pace gaps, then examine the relevant moving shots. In one production this motivated the following interventions. The later full export was still judged unsatisfactory, so these are attempted improvements rather than a proven quality recipe:

- **Pace.** Sparse reference sampling suggested frequent changes, roughly three to five seconds; it was not a frame-accurate edit map. The first story pass averaged about seven seconds a shot, some over fourteen. Inserts with an explicit `[from, to)` window keep the underlying shot's clock continuous when cutting back. About 30 inserts took a 188-second film from 27 to about 57 cuts; more cuts alone did not solve its quality gap.
- **Close-ups of objects, with depth of field.** The reference keeps cutting to tactile things (a mug, a phone screen, notes, a button), each with a soft background. Inserts like the monitor's text, hands on the keyboard, a lamp's bulb catching, steam off a plate, ink being written and a sign dying gave the world scale and texture that wide shots alone never did. Enable depth of field only in shots that name a focus distance.
- **A deliberate palette.** Studied reference frames used saturated light and clear subjects; the first pass was dark grey with coloured dots. The attempt added source-tinted haze, a split-tone grade and saturation. These changed the image, but did not establish that the film met the reference standard.

### Beams and other visible light

- Rooftop searchlights and lasers read as "the city is shouting" better than more signs do. Put the sources on mid-height roofs at moderate elevation so the beams cross the frame; beams from the tallest roofs aimed steeply up stay above every shot.
- Soft beam edges from the view angle need correct normals on a stretched instance: use the inverse-transpose (`M · S⁻² · n`), or a cone renders as a hard flat slab. Fade beams out within a few metres of the camera.
- Additive light disappears on a white ground. If lasers must appear in a light world, darken the world for that section. That can itself be the story beat: the noise drags darkness back over a blank canvas, and the next downbeat cuts back to clean white.
- Check a beam's gradient direction against the geometry's UVs with one debug frame at high intensity before tuning brightness, rather than guessing which end is which.

### Characters and crowds

- A rigged, animated stock character (for example the X Bot mannequin from the three.js examples, which comes from Mixamo; check the licence for your use) driven at an explicit clip time (`action.time = f(t)`, then `mixer.update(0)`) stays deterministic. Pin the hips' root motion so the story owns position. Seated, typing or leaning poses can be laid over the idle clip as per-bone local rotations, with signs found by test renders.
- Crowds by level of detail: rigged clones (`SkeletonUtils.clone`) for nearby people, simpler silhouettes further away. Test the actual camera; distance does not automatically make a crude pose convincing.

## Release Handoff and Improving the Skill

### YouTube release handoff

Once the user wants to publish the finished video, read `youtube-release.md` for title, description, channel bio, Suno rights and YouTube AI disclosure. A completed render or upload is not evidence of a public release. Keep the artist-specific copy and actual publication status beside the durable release materials.

### Improve the skill from the experiment

Record the failed version, attempted correction, technical result and latest user verdict separately. Label a proposed remedy as unproven until reviewed; technical improvement does not imply creative acceptance. Keep song-specific media, private stories and generation logs out of reusable skill references. For song deliveries, include the selected model and a proposed control preset, conditional on available controls. Identify suggested slider values as untested until auditioned.
