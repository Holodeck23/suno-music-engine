# Music-video direction, reference craft and quality resets

Read for an ambitious reference-led video, a rejected draft, or developing a song and film together. Pair with `music-video-production.md` for timing/export and `story-world-video.md` when narrative continuity matters. These are decision aids, not a house style or a promise of reference-level quality.

## Recover the meaning before choosing the metaphor

Use the selected recording, lyric sheet, latest user clarifications and production history. Distinguish the song's subject, the speaker's perspective and the change the audience should feel. If it adapts a lesson or transcript, establish the teaching before literalising a lyric; label an uncertain source identity as uncertain. Keep private source material in production storage.

A recipe metaphor can represent learning a method, adapting it and judging the result. It need not mean recipes are bad or that a magic machine supplies understanding. Test the ending against the premise: a small object appearing is not automatically a satisfying demonstration of agency or mastery. Write the visible action and its consequence, not only the explanatory message.

## Study the reference as moving filmmaking

The agent owns the breakdown. Search existing production records and saved references before asking the user to repeat it or downloading again. Confirm the exact video, available streams and creator credits. One creator may use different engines on different films. Record separately what the creator credits, what is visible, and what implementation you infer. A video-only download cannot establish sound/edit relationships.

Use a whole-film contact sheet to locate useful passages, then closely study one representative short sequence in motion, with sound where available. Sparse frames and automated scene-change counts miss performance, transitions and musical phrasing. Make a compact timecoded table:

| Record | What to establish |
|---|---|
| Shot and sound | In/out, duration, phrase or accent, whether a cut anticipates or follows it |
| Composition | Hero subject, silhouette, scale, lens/perspective, foreground/background and negative space |
| Action | Anticipation, contact, resistance, follow-through, settle; what changes and why |
| Surface and light | Shape detail, roughness, contact shadows, reflections, light direction and depth cues |
| Edit and reveal | Where attention starts, where it lands, transition motivation, joke/setup/payoff |

Extract a few transferable techniques and apply them to an original shot. Do not copy a channel's signature layout wholesale or replace analysis with adjectives such as cinematic. If inspection is limited to stills, state that limit and leave motion conclusions unverified.

## Prove the difficult part cheaply

Choose a representative shot that exposes the biggest risk: character acting, tactile object interaction, a transition, or type integrated with motion. A quiet logo loop is a poor proxy for a film whose promise is physical comedy. A few seconds may be enough; extend only when the action needs context.

Judge a frame at delivery scale, then the moving action at intended speed with its audio excerpt. Ask whether the subject is distinctive, the action legible, contact and weight convincing for the chosen style, and the reveal worth watching. Detail, realism, cutting speed and simulated activity are not quality scores. A minimal graphic treatment can work; generic primitives may fail when promoted to hero close-ups. Hands and object contact are especially exposed.

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

## Carry the lesson into the complete film

If a viewer cannot tell what the object is doing, its name in the treatment does not solve the screen problem. Establish a recurring subject, destination or visible trigger, then show consequences across sections. A look/motion pilot can be useful without proving narrative clarity. When the user delegates completion, apply that feedback and finish within the authorized scope; do not add repeated approval rounds.

Benchmark representative final-resolution frames after enabling the intended optics and motion settings. Separate shader warm-up from steady rendering, account for shared GPU contention, and state ETA as an estimate including encoding/review. Reuse probes only when source, audio, analysis and render settings match the final intent. Preserve the matched source snapshot and checkpoint before the expensive run.
