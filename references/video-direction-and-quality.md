# Music-video direction, reference craft and quality resets

Read for an ambitious reference-led video, a rejected draft, or developing a song and film together. Pair with `music-video-production.md` for timing/export and `story-world-video.md` when narrative continuity matters. These are decision aids, not a house style or a promise of reference-level quality.

## Recover the meaning before choosing the metaphor

Use the selected recording, lyric sheet, latest user clarifications and production history. Distinguish the song's subject, the speaker's perspective and the change the audience should feel. If it adapts a lesson or transcript, establish the teaching before literalising a lyric; label an uncertain source identity as uncertain. Keep private source material in production storage.

A recipe metaphor can represent learning a method, adapting it and judging the result. It need not mean recipes are bad or that a magic machine supplies understanding. Test the ending against the premise: a small object appearing is not automatically a satisfying demonstration of agency or mastery. Write the visible action and its consequence, not only the explanatory message.

## Study the reference as moving filmmaking

The agent owns the breakdown. **Pull the actual reference, never a sibling:** when the operator names a video as the bar, download that exact video before any study and state its video ID in the study (see `~/second-brain/recipes/2026-10-14-pull-reference-video-frames-for-comparison.md` for mechanics). Three previous films on this machine (*All Signal*, *Crumbs in the Kernel*, *Soft Parts*) were all studied against *Drop the Prompt* (`YyXGHYvFqlE`) because the named target, *LGTM* (`3TNpOD6bov8`), had never been downloaded (caught 2026-10-16). Confirm the exact video ID, available streams and creator credits. One creator may use different engines on different films. Record separately what the creator credits, what is visible, and what implementation you infer. A video-only download cannot establish sound/edit relationships.

Use a whole-film contact sheet to locate useful passages, then closely study one representative short sequence in motion, with sound where available. Sparse frames and automated scene-change counts miss performance, transitions and musical phrasing. Make a compact timecoded table:

| Record | What to establish |
|---|---|
| Shot and sound | In/out, duration, phrase or accent, whether a cut anticipates or follows it |
| Composition | Hero subject, silhouette, scale, lens/perspective, foreground/background and negative space |
| Action | Anticipation, contact, resistance, follow-through, settle; what changes and why |
| Surface and light | Shape detail, roughness, contact shadows, reflections, light direction and depth cues |
| Edit and reveal | Where attention starts, where it lands, transition motivation, joke/setup/payoff |

Extract a few transferable techniques and apply them to an original shot. Do not copy a channel's signature layout wholesale or replace analysis with adjectives such as cinematic. If inspection is limited to stills, state that limit and leave motion conclusions unverified.

### Quantified reference gates and craft rules (2026-10-16)

1. **Measure the reference numerically (quantified look gate).** Convert "it doesn't look right" into numbers before shipping a look (`python3 scripts/measure-frame-look.py FRAME_OR_DIR`):
   - **Palette:** sample ~15 frames across the film; `ground` = most common quantised colours, `accent` = mean of the 400 most-saturated pixels.
   - **Brightness:** median pixel value (0–255) and fraction of pixels above `128`.
   - **Verified benchmark (2026-10-16):** *LGTM* (`3TNpOD6bov8`) chorus frames sit at **median `18–24`**, **`1.8–4.6%` of pixels above `128`**, ground blue-dominant (`#000010–#101020`, accent `#38EE82`). A draft `"Which One of You"` frame that felt wrong measured **median `34`**, **`14.3%` above `128`**, ground green-dominant — roughly twice as bright with 3–8× the hot pixels.
   - **Gate:** Before shipping a look, measure your rendered frame against the reference's and state both numbers side by side.
2. **Cut density is a target, not a feeling.** *LGTM* (`3TNpOD6bov8`) cuts or switches sub-plates every **2–4 seconds**. A 26-second pilot built as two held screens fails no matter how good each screen is (`"Which One of You"` `pilot-01`, 2026-10-16). Measure the reference's cut rate from a 1 fps contact sheet, state your own pilot's cut rate, and compare both numbers before building past the pilot.
3. **Readability outranks the gag.** On a 2026-10-16 draft frame, a speech-bubble gag covered the hero lyric word at the exact moment it was sung. The reference's own rule is that every lyric line stays readable and karaoke highlighting never runs ahead of the voice.
4. **One accent plus one rare alarm.** A draft frame carrying green, white, amber and red cards simultaneously reads as rainbow; the reference holds a single accent per world and spends its alarm colour once.
5. **Linear-RGB shader mix & alarm-wash calibration (2026-10-17).** When scenes render in linear RGB before sRGB conversion (`toSRGB` in post), a seemingly small background shader mix such as `mix(C_INK, C_INK2, 0.42)` plus `coreGlow * 0.18` or an alarm wash `vec3(0.11, 0.008, 0.016)` lifts sRGB pixel values (`0.11^(1/2.2) ≈ 94/255`) so dark frames fail `measure-frame-look.py` at **median `34–55`** (`5–15% > 128`) instead of the *LGTM* benchmark (**median `18–24`**, `1.8–4.6% > 128`). Calibrate dark-world background shaders to `mix(C_INK, C_INK2, 0.20)`, keep radial `coreGlow` under `0.025 + 0.045 * kick`, cap red `sev1` alarm washes at linear `vec3(0.035, 0.005, 0.010)` (`mix <= 0.45`), and limit 2D bokeh particles to `14–16` so every dark plate stays inside `median 18–26`.
6. **3D `TextPlane` frustum sizing & dual-layer lyric safety (2026-10-17).** At camera distance `d` and vertical `fov`, the visible world height is `2 * d * tan(fov / 2)` and visible width is `height * (16 / 9)`. At `d = 6.8, fov = 34°`, visible width is `7.39` world units; a 21-character string at `capH = 0.44` (`~6.65` units wide) clips the left and right screen borders as soon as the camera orbits (`yaw != 0`) or dollies in (`d < 6`). Size 3D `TextPlane`s from camera frustum width (`capH <= 0.28` for 20+ char headers at `d ≈ 6.8`, `capH <= 0.22` for close-ups at `d ≈ 4–5`), keep 3D `TextPlane` vertical coordinates at `y >= 1.8` whenever a 2D subtitle bar is active at `y = H - 118` so world-space text never collides with screen-space subtitles, and stagger multi-gate corridor `TextPlane` visibility so only the nearest gate's text is visible at once.
7. **GLSL SDF Raymarching: isotropic 3D gyroid displacement & `L + V = 0` half-vector singularity prevention (2026-10-17).**
   - **No polar `atan(z, x)` on 3D spheres:** Displacing a raymarched sphere with `cos(atan(p.z, p.x) * m)` creates an unbounded gradient singularity (`|∇d| -> ∞`) along the Y pole (`x = 0, z = 0`), producing a visible polar pinch and raymarch step-overshoot ripples. Use a 100% isotropic 3D **Gyroid wave field** (`dot(sin(p * k), cos(p.yzx * k)) / 3.0`) multiplied by a Lipschitz safety factor (`0.72`) so `|∇d| <= 1` everywhere on $S^2$.
   - **Never evaluate Blinn-Phong `H = normalize(L + V)` on a central sphere from an internal origin point light:** When `lightPos` is at the origin `(0, 0, 0)` inside the central core (`MAT_CORE`) to illuminate surrounding monoliths, the light vector `L = normalize(lightPos - p)` on the front center of the core points straight away from the camera (`L = -V`). Thus `L + V -> 0`, turning `H = normalize(L + V)` into a `0/0` singularity that amplifies microscopic raymarching termination steps into concentric bullseye contour rings. Always shade a central core's specular highlights from external directional key/rim lights (`L_key`, `L_rim`), and use $C^\infty$ analytical closest-approach volumetric integrals + sub-LSB interleaved gradient noise dithering (`±0.85 / 255.0`) before 8-bit quantization.
8. **RFC 6455 WebSocket continuation-frame reassembly (`FIN=0` + `opcode=0x00`) on `1080p60` render pipes (2026-10-17).** When streaming `1920x1080` JPEG (`quality: 0.96`) frames from headless Chrome over a raw Node `http` `upgrade` WebSocket receiver, high-detail frames exceeding `131,072` bytes (`128 KB`) are fragmented by Chromium into an initial frame (`FIN=0, opcode=0x02`) followed by continuation frames (`FIN=0/1, opcode=0x00`). A minimal WebSocket parser that checks only `opcode === 0x02` and ignores `FIN` / `opcode === 0x00` truncates `>128 KB` JPEGs (`[mjpeg] overread 8 / Invalid data found`) and drops frames. Always accumulate `FIN=0` chunks across `opcode === 0x00` continuation frames until `FIN=1` before reading the 4-byte sequence index and writing to `ffmpeg`.

## Move the needle on every film: reuse the engine plumbing, never clone the visual kit (2026-10-17)

When `"All Signal"` (`full-v3`) was built by copying the `"Which One of You"` codebase, it added three new 3D setpieces (the Grandmaster Chessboard, the Blank Canvas Bridge, and the Warm Kitchen Table) but carried over the previous song's exact graphic kit (`drawBot` terracotta blocky characters with speech bubbles, `drawTerminalCard` macOS terminal windows, `drawRubberStamp`, and additive wireframe boxes on `#05070C`). The operator's immediate verdict: *"pretty much the exact same style as the last one. good - but i want every attempt to move the needle... change something, improve something, try something."*

Separate **engine plumbing** from **visual vocabulary**:

- **Always reuse engine plumbing:** deterministic 60 fps `window.__renderFrame(t)` clock, WebSocket binary JPEG frame pipe (`quality: 0.96`), headless Chrome Metal GPU flags, precomputed `audio.json` / stem RMS & spectral envelopes, quantified look/cut-density gates, and lossless/high-bitrate `ffmpeg` encoding.
- **Never reskin the previous song's visual kit (`drawBot`, `drawTerminalCard`, `drawRubberStamp`, or its signature HUD/card layout)** unless the user explicitly asks for a direct sequel in that exact style.
- **Every new video must introduce at least one genuine visual/technical leap** suited to the track's genre and sonic architecture — for example:
  - Custom GLSL raymarched SDF / ferrofluid / volumetric light-shaft shaders driven by spectral centroid and sub-bass pressure;
  - High-density GPU-instanced megastructures (`THREE.InstancedMesh` with custom vertex/fragment displacement shaders, 10,000–100,000 reactive instances);
  - Physical/topographical audio landscapes, cymatic fluid/particle fields, or silhouette/cel-shaded/brutalist architectural worlds;
  - Kinetic typography or diegetic world-space projection mapping that looks nothing like a 2D code editor card deck.
- **Never inherit a rejected visual metaphor when changing renderers (2026-10-17):** Rewriting a scene from offline Blender to real-time GLSL SDF raymarching does not change the film if both versions depict the same rejected premise (e.g., an 8-piece dark shell opening around an orange/copper core surrounded by floating debris). The viewer judges the subject and metaphor on screen, not the shader pipeline behind it. When a previous attempt on a track was rejected, throw away its metaphor, silhouette, and colour palette completely.
- **Negative space outranks visual busyness (2026-10-17):** Stacking a displaced core + segmented shell + spinning torus rings + 700 flying debris shards + floor rings + corner HUD text + oscilloscope in the same frame reads as cluttered screensaver noise. Pick **one** hero visual mechanism with bold negative space (`60–80%` calm dark ground) so every musical change reads at a glance.
- **State the visual leap up front** before writing scene code: name what this film is doing that the previous film did not, and prove that leap in a short 20–30 second 1080p60 pilot before committing to a full-length render.

## Prove the difficult part cheaply

Choose a representative shot that exposes the biggest risk: character acting, tactile object interaction, a transition, or type integrated with motion. A quiet logo loop is a poor proxy for a film whose promise is physical comedy. A few seconds may be enough; extend only when the action needs context.

Judge a frame at delivery scale, then the moving action at intended speed with its audio excerpt. Ask whether the subject is distinctive, the action legible, contact and weight convincing for the chosen style, and the reveal worth watching. Detail, realism, cutting speed and simulated activity are not quality scores. A minimal graphic treatment can work; generic primitives may fail when promoted to hero close-ups. Hands and object contact are especially exposed.

A generated direction board records the intended composition, not the renderer's achieved construction. For a physical interaction, inspect actual rendered frames before, at and after contact from the shot cameras. In one copper-key sample, a dais hid the solid key just before it reached the socket, leaving only a detached luminous edge; moving the socket and plinth to meet the floor channel repaired the action. Test object clearance and occlusion in screen space as well as world coordinates before committing a long pass. This is a contact-shot check, not a requirement to use a dais or a specific visual style.

Thin emissive details also need a cut-pair check with the intended shutter setting. In that same sample, Eevee smeared the key's glowing edge at a hard cut despite correctly baked transforms. With slow rigid motion and no free debris, disabling motion blur removed the artefact. Do not carry that setting over to fast particles or other scenes without their own playback check.

Choose the renderer after identifying that risk. Compare the same frame to isolate a rendering difference, but also test a shot authored for the candidate engine's strengths. Moving identical box geometry to Blender does not test Blender's artistic ceiling. Record actual engine/version, source, scene/evaluator, settings and output; a `.blend` still test does not mean the delivered film used Blender. A scene snapshot is not a baked animation.

Keep each pass to a stated hypothesis, a bounded excerpt and an observable comparison. Reuse audio analysis, source assets and verified timing. If the result is explicitly rejected as cheap or the wrong direction, stop expanding or polishing that direction. Diagnose the missing craft and change the premise, assets or action before another costly render. Do not impose repeated approval rounds when the user has delegated completion, but do not reinterpret a rejected sample as acceptance.

## Develop song and story together when the song is still open

This is a proposed workflow, not a demonstrated cure for weak visuals. It gives music and film room to support the same turns:

1. Define the emotional premise and a visible setup/change/payoff. Draft a short treatment and song structure together.
2. Map sections to dramatic jobs: establish, complicate, attempt, reverse, resolve. Let recurring hooks bring a changed meaning or visual consequence. Leave musical space for actions and reactions when useful.
3. Keep the filmmaking treatment separate from Suno input. Translate musical needs into concise playable production directions; do not send camera directions as if Suno could execute them.
4. Test one useful musical passage and one rough visual action before committing to a full film, within the user's generation budget. Evaluate the pair together.
5. Once a take is selected, measure its actual events and remap the film. Requested breaks, tempo and section lengths are not guarantees. Preserve the selected recording; changing it later is a creative decision, not an animation shortcut.

For an already accepted song, work from its actual structure. Do not regenerate it merely because co-development might have been easier.

## Preserve outcomes without inventing success

Technical verification, agent aesthetic assessment and human acceptance are separate records. Log the exact version and verdict. A liked pilot does not accept a later full export or another direction. A build, decode, contact sheet or new engine cannot establish creative success.

Observed failed approaches included a busy procedural city with weak shot subjects, and a Blender kitchen sample with generic props, explanatory cards and an unconvincing action/payoff. More inserts, stronger colour and a renderer change did not establish reference-level quality. These are evidence about those executions, not bans on cities, kitchens, cards or procedural animation. The proposed remedy is close craft study followed by an original motion proof; label it unproven until that proof exists and is reviewed.

Keep a compact production checkpoint: selected audio/hash; current render and source identity; latest user verdict; unresolved craft problem; next bounded test; render cost measured on this machine. Preserve failed samples as evidence. Avoid repeating analysis or a full render when only the manifest or one shot needs repair.

## Prevent camera jumps before a long render

An observed pilot changed camera position, aim point and lens at about 4.57 seconds between very similar framings. It read as a glitch. Deterministic seeking and regular 24 fps timestamps both passed; neither test detects a poorly authored transition.

- Make shot boundaries and transition intent explicit. Continuous moves need continuous position, orientation, lens and focus; inspect velocity changes too. Intentional cuts can jump, but should have a readable editorial purpose.
- Compare camera states immediately before/after every boundary. Flag near-matching views with abrupt position, focus or framing changes for review. Angle/scale thresholds are diagnostics for that production, not universal cinematography rules. Keep a regression case using the actual failed poses so the gate demonstrably catches the known mistake.
- Render paired boundary frames and a contiguous motion probe spanning the risky transition before launching the full film. A whole-film board proves coverage, not transition quality. Check the frame before and after each worker/chunk seam too.
- For shutter blur, an absolute-time evaluator needs shutter-time transforms. Bake or sample the relevant motion, use quaternion interpolation with consistent signs where Euler wrapping could spin the camera, and prevent blur from interpolating across hard cuts. Do not claim every moving object has blur when only camera or selected transforms were keyed.
- Smooth fast control curves before applying them to global position/scale. Small, rapid movements can read as jitter in a macro shot. Also consider temporal sampling noise and thin-line aliasing. Constant frame cadence alone does not establish smooth imagery; assess playback when rendering is not competing for the GPU.

A rushed preview can create a new fault: one assembled WIP retained only seven frames of a shot before jumping to a later excerpt. Prefer a contiguous excerpt, or cut partial excerpts at sensible shot boundaries. Label discontinuous previews and do not use their pacing as evidence about the complete edit.

For a fractional cut time in a frame-sampled Blender film, the first new-shot frame is `ceil(cut_seconds * fps)`. Using `round()` can assign the cut key to the previous shot and let shutter interpolation sweep between cameras. Bake the sampled poses, keep adjacent quaternion signs consistent, and disable shutter blur around the discontinuity. Set interpolation on the actual FCurve key points: in the tested Blender build, Python-inserted keys remained Bezier despite a Linear UI preference.

Audit the baked paths at fractional frames on both sides of each cut **without calling the analytic evaluator**. The evaluator can overwrite a faulty baked camera and make a broken shutter path appear correct. In the observed regression, the faulty path deviated by about 5.4 metres; explicit Linear keys and corrected cut indices reduced the audited maximum position/focus error to about 0.000058 metres. These values describe that scene, not portable acceptance tolerances. Keep the contiguous encoded motion probe as a separate visual check.

## Design the key images before building the engine

The default failure of a code-driven music video is not technical. Two observed films were built engine-first — geometry, simulation and camera authored first, with the treatment written afterwards to describe whatever the engine produced. Both passed every technical gate and both drew the same verdict from the viewer: it does not look like anything. In the second case the treatment named a protagonist fragment that a reader could not find in a frame sample, because no frame had ever been composed to carry it.

An engine-first film has no referent. Nothing can be compared against anything, so "does it look right" is unanswerable and every check collapses into "does it render", which always passes.

Invert the order:

1. **Write the story and its key moments first**, as a small set of specific beats — eight to twelve for a five-minute film — each stating what the viewer must understand at that moment, not what the geometry does.
2. **Generate a target still for each key moment** before any engine work, using an image model. These are the referents. They fix subject, scale, framing, palette and what the shot is *about*, cheaply and in minutes, at the stage where changing your mind costs nothing.
3. **Review the stills as a sequence** against the song. If the story does not read as a strip of eight stills, it will not read as five minutes of motion. Fix it here, where a fix is one regenerated image.
4. **Then build the engine to reproduce those frames**, treating each target still as the acceptance test for its shot.
5. **Verify every shot against its own target image**, as a comparison, never as an inspection of the render on its own terms. Looking at your own output and judging it good passes every time and answers a question nobody asked.

The generated stills are direction, not footage. They are not expected to appear in the film, and the engine does not need to match them exactly — they exist so that "right" is defined by something outside the renderer before the renderer runs.

This also repairs the gate order. Technical export verification, cut measurement and encode checks are all downstream; they protect a film that is already worth watching and can do nothing for one that is not. Establish the images first, then spend the render budget.

## Measure cut harshness, not just cut correctness

The section above makes cuts technically correct: continuous transforms, no shutter sweep across a discontinuity, audited baked paths. A cut can pass every one of those checks and still read to a viewer as the picture glitching.

An observed five-minute film carried 34 hard cuts, one roughly every nine seconds, each alternating an extreme warm close-up against a wide shot on near-black. Measured as mean per-frame luma difference, the film sat at 1.8 and every cut landed between 29 and 90 — sixteen to fifty times baseline. A viewer reported six separate timestamps as "glitches"; three were cuts, and the reported ones were not the worst. One was the mildest of all 34.

- Before encoding, compute the per-frame luma delta across the whole film and rank the cuts against the film's own mean. `tblend=all_mode=difference,signalstats` over the sequence gives this in one pass on the encoded file. The ratio is the diagnostic, not the absolute number.
- A cut whose delta is tens of times baseline is a brightness slam. It is legitimate editorially, but it must be a choice someone made, not a number nobody looked at. Full-frame orange to mostly black in one frame reads as a blip whatever the treatment says.
- Where the slam is unintended, a three-to-four-frame cross-dissolve removes it without touching content or the edit's rhythm. Frames are enough; no re-render is needed.
- Cluster viewer reports before fixing anything. Reports arriving as a list of timestamps usually collapse into two or three mechanical classes. Classify each by measurement, confirm the classes predict the remaining reports, and fix the class.

## A named limitation is not a discharged defect

The same film's code review recorded, accurately and in advance, that only camera, focus, lens and hero location carried shutter keys, and that other moving geometry had no complete object motion blur. It then approved the render. The unblurred geometry was small fast debris, which at 24 fps strobes: three of the viewer's six reported "glitches" were exactly that, in the region carrying the densest debris.

Writing a limitation into a review does not convert it into an accepted trade-off. Either fix it, or get the limitation accepted by the person who will watch the film, by name, before the long render starts. A limitation the viewer has not agreed to is a defect with documentation attached.

To check before shipping: sample three consecutive frames in the densest motion region, crop and magnify. Smoothly moving geometry shows small displacements with softened leading edges. Strobing shows large displacements with perfectly crisp edges. Synthetic shutter by temporal blending of adjacent frames can soften it afterwards from the frame sequence, at some cost in global sharpness.

## The encoded file is a derivative; the frames are the master

Treat the rendered PNG sequence as the deliverable and the video file as one lossy projection of it. Keeping the frames means a quality complaint can be answered by re-encoding in minutes rather than re-rendering in hours.

An observed export encoded h264 `yuv420p` at about 4.9 Mbit/s. Measured against the surviving lossless frames, the red channel had SSIM 0.693 while green and blue held 0.977 and 0.963. The film was copper on dark blue, so most of its fine detail lived in red chroma, and 4:2:0 subsampling discards half of it. Every existing check passed: full decode, frame count, duration, hashes. None of them looks at colour.

- For saturated single-hue material, verify the encode per channel against the source frames, not as a single average. `ssim` and `psnr` reporting R, G and B separately will expose this; an overall figure hides it.
- The cause is subsampling, not bitrate. Re-encoding the same content as 10-bit 4:2:0 moved red only from 0.693 to 0.722; 4:4:4 at identical file size moved it to 0.984. Spending more bits on the wrong chroma format does not recover the detail.
- Expect 4:4:4 masters to be rejected by some players. Keep it as the archival and upload master, and make a subsampled copy only for casual viewing.
- Do not predict artefacts without testing for them. Banding was expected in this film's dark regions from 8-bit at low bitrate; amplifying the shadows showed the dark areas were true black with no gradient present, so there was nothing to band.

Verify a re-encode as carefully as a render. In an observed attempt, `-shortest` silently trimmed four frames and clipped the film's closing beat, and `-c:a copy` from an `.m4a` propagated Opus into an MP4 container, because the wrapper's extension did not match its codec. Probe the output's frame count, duration and audio codec against the source before replacing anything.

## Carry the lesson into the complete film

If a viewer cannot tell what the object is doing, its name in the treatment does not solve the screen problem. Establish a recurring subject, destination or visible trigger, then show consequences across sections. A look/motion pilot can be useful without proving narrative clarity. When the user delegates completion, apply that feedback and finish within the authorized scope; do not add repeated approval rounds.

Benchmark representative final-resolution frames after enabling the intended optics and motion settings. Separate shader warm-up from steady rendering, account for shared GPU contention, and state ETA as an estimate including encoding/review. Reuse probes only when source, audio, analysis and render settings match the final intent. Preserve the matched source snapshot and checkpoint before the expensive run.
