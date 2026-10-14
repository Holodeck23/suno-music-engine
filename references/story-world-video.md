# Story-world music videos: a place, someone in it, consequences

Read this after `music-video-production.md` when the user wants the video to tell a story or "create worlds" rather than illustrate lyrics, or when a lyric-driven cut has been judged clever but lifeless. Everything in the main guide (audio as timing authority, word timing, scored events, deterministic export) still applies.

## Why a polished lyric video can feel dead

A cut that gives every line its own visual pun is a sequence of slides: nothing carries over, nobody lives there, and nothing that happens has a consequence. Viewers read that as motion graphics, however well made. The videos that land as a *world* have three things a slide cut lacks: a persistent place, someone in it, and events that change it for good. Adding effects does not fix this. A story pass does.

## Order of work: story before shot list

1. **Treatment, one page.** Logline (one sentence: who, what they want, what changes). The world. One protagonist. The rules the film obeys. The story mapped onto the song's *measured* sections, one verb per section. Write it before any code and keep it in the production folder.
2. **Beat board.** One still per story beat across the whole song, rendered from the real engine, not drawn. This is where the story is judged cheaply.
3. **Animatic.** The whole song in motion, rough but in sync, scrubbable in the preview so notes are about story, not polish.
4. **Look development, then the final render.**

Skipping steps 1–3 is how a production polishes easily but never gets a story. In one production the slide cut reached its full render with no treatment; the story pass that followed started from the treatment and had a 27-shot beat board covering the full song in a single working session.

## Rules that make it read as one world

- **One place, travelled, not cut between.** The camera moves through a single connected space (a room inside a building inside a city) instead of cutting between unrelated diagrams. A continuous move that crosses spaces (pulling back down a street, through a window, behind the character) does more than any transition effect.
- **Memory as dated events.** Model the story as events with times: a sign switched on, a sweep reaching it at `t0 + distance / speed`, a reboot, a final kill. The state at time `t` is "every event at or before t", computed from `t` alone. The world remembers (what was killed stays dead) and every frame still renders out of order, which the deterministic exporter requires.
- **Words inside the world, never on top of it.** Lyrics go on surfaces: building faces, a monitor typing them, window glass, the street, banners across the road, ink on the ground. Each surface obeys word timing, so a word appears where it lives at the moment it is sung.
- **Colour story with exactly one meaning per colour.** For example, loud saturated colours mean the thing being rejected, one accent colour means the thing chosen, and a warm colour is held back for the ending. Introduce the held-back colour once, late.
- **An act break can invert the whole palette.** Draining a night city into a white paper world, where the character becomes an ink silhouette, marked the bridge more strongly than any cut.
- **The ending answers the opening.** The first and last shots should frame the same place, now changed.

## ALIVE: a checklist, each item a pure function of time

When the user says the video must feel *alive*, turn it into named systems, not adjectives:

- **A crowd** on sidewalks: position = phase + speed × t, wrapped along a lane. Give them a state the story can change: heads down with lit phones while the hype holds, heads up after the protagonist's act.
- **Traffic** as paired head/tail lights on lanes, braking (tail lights flaring) on the kick.
- **Weather.** Rain anchored to the world and wrapped around the camera (`x = camX − B/2 + mod(seedX·B − camX, B)`), tinted by the light it falls through.
- **Other lives in windows.** Some lit windows switch on and off on their own slow clock; a few flicker like a TV.
- **Things that move on their own.** Drones on orbits, which can fall when the story hits them (a free fall from the event time) and stay where they fell.
- **The character never freezes.** Breath, weight shift, slow head turns under every pose.
- **A camera with a body.** Layered-sine handheld drift, a small shove on the kick, and moves that ease in and settle.
- **Signs animate.** Pulse, LED rows, glitch tears. Nothing is a static poster.

## A procedural character that holds up

A jointed figure of capsules (hips, spine, chest, neck, head, two-segment limbs) posed by blending named poses (stand, type, lean back, sit) plus a procedural walk cycle driven by distance walked is enough, **if it is lit as a silhouette.** Posture carries the acting. Faces are not needed.

- Rim term around `pow(1 − N·V, 4)` at low gain. A strong or wide rim turns the figure into a glowing mannequin; this happened and read as a toy.
- On a light ground, render the figure as flat ink with a soft blob shadow.

## Failures observed, and what fixed them

- **Grid cities hide the faces a street camera needs.** Looking down an avenue, every billboard mounted flat on a facade is seen edge-on or blocked by the block in front. Fix: blade signs hung out from side faces and facing along the street, and banners strung across the road for lyrics. Also open a view corridor (lower the blocks directly in front of a hero window) so the character looks *out* over the city rather than into a wall 12 m away.
- **Check the camera's line of sight against its own building.** A camera on a roof looking down at targets in the street saw only the roof surface and rendered a black frame. Move it to the edge.
- **Window grids too big, too many and too bright read as a toy city.** Keep lit windows to about 15 percent, small, dim and varied (cool and warm, ribbon offices and punched homes), with near-black facades.
- **Coloured spill painted onto whole facades looks fake.** Keep facade spill under about 0.5 percent of the light's colour. Put strong spill only on wet ground, rain and the character's rim.
- **Volumetric shapes made of transparent geometry look like boxes.** An additive cylinder meant as a sweeping wave of light rendered as a solid blue block. Put the event on surfaces instead: a thin scan line where the wave's radius meets facades and ground. A facade facing the wave's centre lights all at once, so keep the line's glow short (a flash), not a lingering band.
- **Sung words blown out to white.** Use a pale tint of the accent for the active word, not white, and keep panel glow multipliers around 1 to 2 under bloom.
- **Wrapped lines broke mid-phrase.** Lay out each lyric line as its own row and wrap within it; never flow a multi-line lyric as one word stream.

## Probing cheaply

Render four or so stills across the riskiest shots first, tile them into one image, fix, and only then render the full beat board (one still per shot). Each probe takes about a minute, so the bad first draft happens where the user never sees it.

Report states honestly: a beat board is stills. It does not show whether motion, sync or pacing work. Say what has and has not been seen in motion.

## Renderer choice: test it on the same frame before switching

Before moving a production to a heavier renderer, export the exact world and camera and render the same frame in both. One such test (1080p, Apple M5, a night city of plain box towers, about 500 signs):

- Blender EEVEE at 32 samples: about 2 s per frame after shader compilation, so a three-minute film renders in hours.
- Blender Cycles at 256 samples on the Metal GPU: about 3 minutes per frame, which is hundreds of hours for a full song. That only makes sense for stills or a few hero shots.
- On identical box geometry, neither Blender render looked better than the browser renderer. Better light has nothing to catch on flat boxes. The step up comes from modelled assets (recessed windows, ledges, rooftop clutter, a rigged character), and those can also be loaded as glTF into a browser engine.
- Blender-specific traps seen in that test: the AgX view transform turns saturated neon pastel (Khronos PBR Neutral or Standard keeps the hue); an area light placed just in front of a sign blows it out; world-volume haze over-scatters fast (density around 0.002 to 0.003 at city scale); depth of field at a wide aperture blurs the nearest signage text.

## Measure the reference before polishing: pace, palette, close-ups

Before an art pass, pull the reference video's frames at a fixed interval (one every five seconds, tiled) and compare them side by side with your own contact sheet. In one production this showed three gaps that no amount of polish to existing shots would have closed:

- **Pace.** The reference cut every three to five seconds. The first story pass averaged about seven seconds a shot, with some running over fourteen. A cheap fix that keeps continuity: add *inserts* with an explicit `[from, to)` window over the running shot. The underlying shot keeps its own clock, so cutting back lands where the move would have been anyway. About 30 inserts took a 188-second film from 27 to about 57 cuts.
- **Close-ups of objects, with depth of field.** The reference keeps cutting to tactile things (a mug, a phone screen, notes, a button), each with a soft background. Inserts like the monitor's text, hands on the keyboard, a lamp's bulb catching, steam off a plate, ink being written and a sign dying gave the world scale and texture that wide shots alone never did. Enable depth of field only in shots that name a focus distance.
- **A deliberate palette.** The reference is saturated (one dominant hue, one accent, light in haze). The first pass was dark grey with coloured dots. What fixed it: haze tinted by the light sources instead of black fog, a split-tone grade (cool shadows, warm or hot highlights), a little more saturation, and lighting that has to *read*, not just exist.

## Beams and other visible light

- Rooftop searchlights and lasers read as "the city is shouting" better than more signs do. Put the sources on mid-height roofs at moderate elevation so the beams cross the frame; beams from the tallest roofs aimed steeply up stay above every shot.
- Soft beam edges from the view angle need correct normals on a stretched instance: use the inverse-transpose (`M · S⁻² · n`), or a cone renders as a hard flat slab. Fade beams out within a few metres of the camera.
- Additive light disappears on a white ground. If lasers must appear in a light world, darken the world for that section. That can itself be the story beat: the noise drags darkness back over a blank canvas, and the next downbeat cuts back to clean white.
- Check a beam's gradient direction against the geometry's UVs with one debug frame at high intensity before tuning brightness, rather than guessing which end is which.

## Characters and crowds

- A rigged, animated stock character (for example the X Bot mannequin from the three.js examples, which comes from Mixamo; check the licence for your use) driven at an explicit clip time (`action.time = f(t)`, then `mixer.update(0)`) stays deterministic. Pin the hips' root motion so the story owns position. Seated, typing or leaning poses can be laid over the idle clip as per-bone local rotations, with signs found by test renders.
- Crowds by level of detail: rigged clones (`SkeletonUtils.clone`) for the dozen or so people nearest the camera, simple silhouettes for everyone else. Capsule people look crude only up close.
