# Story-world music videos: a place, someone in it, consequences

Read this after `music-video-production.md` for narrative continuity. For a rejected draft or ambitious reference, also read `video-direction-and-quality.md`. The city and character experiments below produced technical lessons, but their full-film result was not creatively accepted. Audio timing and deterministic export still apply.

## Why a polished lyric video can feel dead

A cut with a separate pun for every line can feel like slides when nothing carries over. Narrative continuity can come from a character, recurring object, connected places or consequences that persist. A treatment helps expose missing causality, but cannot guarantee strong imagery or performance. A busy world can still feel lifeless if shots lack a designed subject.

## Order of work: story before shot list

0. **Study the target.** Reuse saved references and closely inspect a useful moving sequence. A contact sheet helps compare subject, palette and scale, but misses acting and transitions. Keep observations beside the production board.
1. **Treatment.** State who or what changes, the visible attempt and its consequence, and the intended feeling. Map dramatic beats to measured sections, or draft song and story together if the recording is still open. Save it in the production folder.
2. **Beat board.** Sketch or render key beats cheaply. Real-engine stills verify feasibility; drawings can answer story questions before assets exist. Do not confuse either with motion proof.
3. **Risky shot and animatic.** Prove the hardest representative action early. Assemble rough timing across the song to assess setup, escalation, quiet and payoff before expanding final assets. Choose the order around the actual risk rather than requiring a full rendered animatic first.
4. **Look development and final render.** Expand the direction supported by the evidence and authorized by the user. Rejection calls for a creative reset, not automatic completion of the same premise.

## Options for narrative continuity

- **Connected places or recurring subjects.** A camera travelling through a connected space can establish geography; motivated cuts between different places can also carry a story. Choose around the action rather than imposing a one-room or continuous-camera rule.
- **Memory as dated events.** Model the story as events with times: a sign switched on, a sweep reaching it at `t0 + distance / speed`, a reboot, a final kill. The state at time `t` is "every event at or before t", computed from `t` alone. The world remembers (what was killed stays dead) and every frame still renders out of order, which the deterministic exporter requires.
- **Type with a role.** Diegetic words can live on signs, screens, glass or ink; stage typography or overlays can also suit the film. Keep sung words timed and legible without making every scene an explanatory card.
- **Deliberate colour development.** A limited palette or a held-back colour can support a turn. The story need not assign exactly one meaning to every hue.
- **An act break can invert the whole palette.** Draining a night city into a white paper world, where the character becomes an ink silhouette, marked the bridge more strongly than any cut.
- **The ending pays off the setup.** Reframing the opening place after a change is one option; a new image can also complete the arc.

## Optional world systems, each a pure function of time

Select only systems the shot needs. Crowd, traffic and weather increased activity in one experiment without establishing a compelling film. Performance and consequences deserve priority over adding simulation layers:

- **A crowd** on sidewalks: position = phase + speed × t, wrapped along a lane. Give them a state the story can change: heads down with lit phones while the hype holds, heads up after the protagonist's act.
- **Traffic** as paired head/tail lights on lanes, braking (tail lights flaring) on the kick.
- **Weather.** Rain anchored to the world and wrapped around the camera (`x = camX − B/2 + mod(seedX·B − camX, B)`), tinted by the light it falls through.
- **Other lives in windows.** Some lit windows switch on and off on their own slow clock; a few flicker like a TV.
- **Things that move on their own.** Drones on orbits, which can fall when the story hits them (a free fall from the event time) and stay where they fell.
- **Character movement.** Breath and weight shifts can sustain a held pose; motivated stillness can be stronger than constant idle movement.
- **Camera weight.** Easing, settling and restrained drift can support action; a locked camera may better stage a reveal. Do not add a shove to every kick by default.
- **Signs.** Pulse, LED rows or glitch tears when motivated. A static sign can leave attention on the action.

## A procedural character that holds up

A jointed capsule figure with blended poses and a distance-driven walk cycle can serve a distant silhouette or intentionally graphic style. It is not a general solution for hero acting, hands or tactile close-ups. Test posture, silhouette, contact and weight at the intended shot scale; use authored shapes, a suitable rig or another style when the proxy fails.

- Rim term around `pow(1 − N·V, 4)` at low gain. A strong or wide rim turns the figure into a glowing mannequin; this happened and read as a toy.
- On a light ground, render the figure as flat ink with a soft blob shadow.

## Local technical failures and attempted corrections

The following fixes address specific rendering defects. They did not establish creative acceptance of the resulting film. Numerical values depend on the scene's scale, exposure and materials.

- **Grid cities hide the faces a street camera needs.** Looking down an avenue, every billboard mounted flat on a facade is seen edge-on or blocked by the block in front. Fix: blade signs hung out from side faces and facing along the street, and banners strung across the road for lyrics. Also open a view corridor (lower the blocks directly in front of a hero window) so the character looks *out* over the city rather than into a wall 12 m away.
- **Check the camera's line of sight against its own building.** A camera on a roof looking down at targets in the street saw only the roof surface and rendered a black frame. Move it to the edge.
- **Window grids too big, too many and too bright read as a toy city.** Keep lit windows to about 15 percent, small, dim and varied (cool and warm, ribbon offices and punched homes), with near-black facades.
- **Coloured spill painted onto whole facades looks fake.** Keep facade spill under about 0.5 percent of the light's colour. Put strong spill only on wet ground, rain and the character's rim.
- **Volumetric shapes made of transparent geometry look like boxes.** An additive cylinder meant as a sweeping wave of light rendered as a solid blue block. Put the event on surfaces instead: a thin scan line where the wave's radius meets facades and ground. A facade facing the wave's centre lights all at once, so keep the line's glow short (a flash), not a lingering band.
- **Sung words blown out to white.** Use a pale tint of the accent for the active word, not white, and keep panel glow multipliers around 1 to 2 under bloom.
- **Wrapped lines broke mid-phrase.** Lay out each lyric line as its own row and wrap within it; never flow a multi-line lyric as one word stream.

## Probing cheaply

Probe a few risky frames before a large batch; measure cost on the current scene. Use an early short motion render for acting and contact, which stills cannot validate. Save both the probe and its conclusion so a later session does not repeat it.

Report states honestly: a beat board is stills. It does not show whether motion, sync or pacing work. Say what has and has not been seen in motion.

## Renderer choice: isolate cost and image quality

An identical-world/camera comparison can isolate renderer differences, while a target-native representative shot tests the candidate's strengths. One same-frame test (1080p, Apple M5, a night city of plain box towers, about 500 signs) observed the following; remeasure rather than reuse these as budget estimates:

- Blender EEVEE at 32 samples: about 2 s per frame after shader compilation.
- Blender Cycles at 256 samples on the Metal GPU: about 3 minutes per frame. That test would be expensive to expand; it does not establish a universal Cycles cost.
- On that box geometry, neither Blender still showed a persuasive quality improvement. This is evidence about the test, not the engine's ceiling. Modelled detail and suitable materials give lighting more to describe; glTF assets can also be used in a browser engine. Acting, composition and editing remain separate decisions.
- Blender-specific traps seen in that test: the AgX view transform turns saturated neon pastel (Khronos PBR Neutral or Standard keeps the hue); an area light placed just in front of a sign blows it out; world-volume haze over-scatters fast (density around 0.002 to 0.003 at city scale); depth of field at a wide aperture blurs the nearest signage text.

## Measure the reference before polishing: pace, palette, close-ups

Compare existing reference and draft sheets to identify scale, palette and pace gaps, then examine the relevant moving shots. In one production this motivated the following interventions. The later full export was still judged unsatisfactory, so these are attempted improvements rather than a proven quality recipe:

- **Pace.** Sparse reference sampling suggested frequent changes, roughly three to five seconds; it was not a frame-accurate edit map. The first story pass averaged about seven seconds a shot, some over fourteen. Inserts with an explicit `[from, to)` window keep the underlying shot's clock continuous when cutting back. About 30 inserts took a 188-second film from 27 to about 57 cuts; more cuts alone did not solve its quality gap.
- **Close-ups of objects, with depth of field.** The reference keeps cutting to tactile things (a mug, a phone screen, notes, a button), each with a soft background. Inserts like the monitor's text, hands on the keyboard, a lamp's bulb catching, steam off a plate, ink being written and a sign dying gave the world scale and texture that wide shots alone never did. Enable depth of field only in shots that name a focus distance.
- **A deliberate palette.** Studied reference frames used saturated light and clear subjects; the first pass was dark grey with coloured dots. The attempt added source-tinted haze, a split-tone grade and saturation. These changed the image, but did not establish that the film met the reference standard.

## Beams and other visible light

- Rooftop searchlights and lasers read as "the city is shouting" better than more signs do. Put the sources on mid-height roofs at moderate elevation so the beams cross the frame; beams from the tallest roofs aimed steeply up stay above every shot.
- Soft beam edges from the view angle need correct normals on a stretched instance: use the inverse-transpose (`M · S⁻² · n`), or a cone renders as a hard flat slab. Fade beams out within a few metres of the camera.
- Additive light disappears on a white ground. If lasers must appear in a light world, darken the world for that section. That can itself be the story beat: the noise drags darkness back over a blank canvas, and the next downbeat cuts back to clean white.
- Check a beam's gradient direction against the geometry's UVs with one debug frame at high intensity before tuning brightness, rather than guessing which end is which.

## Characters and crowds

- A rigged, animated stock character (for example the X Bot mannequin from the three.js examples, which comes from Mixamo; check the licence for your use) driven at an explicit clip time (`action.time = f(t)`, then `mixer.update(0)`) stays deterministic. Pin the hips' root motion so the story owns position. Seated, typing or leaning poses can be laid over the idle clip as per-bone local rotations, with signs found by test renders.
- Crowds by level of detail: rigged clones (`SkeletonUtils.clone`) for nearby people, simpler silhouettes further away. Test the actual camera; distance does not automatically make a crude pose convincing.
