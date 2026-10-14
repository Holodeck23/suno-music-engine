---
name: suno-music-engine
description: >-
  The complete AI music production system — from mapping existing songs into structural blueprints, to composing original vocal tracks and instrumentals for Suno AI, to architecting cohesive albums
  and…
metadata:
  short-description: The complete AI music production system — from mapping
---

# Suno Music Engine

A unified music production system covering four domains: (1) song mapping, (2) vocal song creation, (3) instrumental composition, and (4) album/EP architecture — all optimized for Suno AI output.

## Routing: What Does The User Need?

Read the request and route to the appropriate mode. Multiple modes can be combined in a single session.

| User Intent | Mode | Primary Reference |
|---|---|---|
| "Break down / map / analyse this song" | **MAPPING** | This file §1 |
| "Write me a song / create lyrics / Suno prompt with vocals" | **SONG CREATION** | This file §2 + `references/suno-formatting.md` |
| "Make an instrumental / beat / backing track / composition" | **INSTRUMENTAL** | This file §3 + `references/music-theory-engine.md` + `references/suno-formatting.md` |
| "Plan an album / sequence tracks / concept album / EP" | **ALBUM** | This file §4 + `references/album-architecture.md` |
| "I want consistent sound across multiple tracks" | **ALBUM** (consistency system) | `references/album-architecture.md` §3 |
| "Blend genres / make something that transcends X and Y" | **GENRE FUSION** | This file §5 |
| "Write something about me / my life / my journey / who I am" | **PERSONAL TRANSLATION** | `references/personal-context-translation.md` |
| "Edit / replace / fix one part of this song" | **V6 EDITING** | This file §7 + `references/suno-formatting.md` |
| "Mash up / sample / combine these songs, clips, images, or video" | **V6 MULTI-INPUT** | This file §7 |
| "Animate this song / make a music video / add a video component" | **MUSIC VIDEO** | `references/music-video-production.md` |
| "Write a YouTube description / channel bio / can I release this Suno track?" | **YOUTUBE RELEASE** | `references/youtube-release.md` |

Always read the relevant reference files BEFORE composing. The reference files contain the deep technical detail — key-to-mood mappings, BPM ranges, structural archetypes, Suno-specific syntax, album sequencing psychology, and production descriptor libraries.

---

## MANDATORY PRE-DELIVERY SELF-CHECK

Before delivering Suno composition prompts or lyrics, run this checklist. State the verified counts in the delivery so the user can audit. YouTube titles, descriptions, channel bios and release guidance use `references/youtube-release.md` instead; do not apply composition tags or lyric-field limits to publishing copy.

**Operational ceilings carried forward from the pre-v6 interface:**
- Style prompt field: **1,000 characters maximum** (target: 200–300 for clarity)
- Lyrics field (incl. brackets): **5,000 characters maximum** (target: under 4,000 to leave margin)
- Single-shot generation length: **8 minutes maximum** (use Extend for longer)

Suno's v6 launch materials do not restate these field limits. Treat them as conservative working
limits, verify against the live UI if a field rejects or truncates input, and update this skill when
Suno publishes v6-specific limits.

**Pre-delivery checklist:**
1. Count the style prompt characters. Confirm under 1,000. State the count.
2. Count the lyrics field characters (including brackets). Confirm under 4,000 (hard limit 5,000). State the count.
3. Verify every bracket contains production direction. No bare `[Chorus]` or `[Verse]`.
4. Verify final tag is `[End]`.
5. Verify no artist or song names appear in the style prompt.
6. Verify no em dashes anywhere in the output.
7. Verify the style prompt is single-line and comma-separated.
8. If instrumental: verify "instrumental, no vocals, no spoken words" appears in style prompt AND first metatag.
9. Keep metatags CLINICAL. Suno's copyright filter is a fuzzy lyric-matcher: vivid/poetic/title-like phrases (similes, metaphors, "weightless," "torn to pieces," famous quotes) get matched as copyrighted lyrics and rejected even inside brackets. Use technique/dynamics/tempo language only. Emotion comes from the musical CHOICES, not evocative words Suno cannot play. See `references/suno-formatting.md` §9 and §17.

If any check fails, fix it and re-count BEFORE delivering. Do not deliver and apologise after — fix it first.

---

## Song-to-video handoff

For video production from a selected song, read `references/music-video-production.md`.
The accepted audio determines timing; inspect embedded lyric tracks before arranging
transcription. Deliver a watchable pilot and support timestamped feedback before
building the entire video. `scripts/extract-video-timing.py` provides local extraction;
`scripts/align-lyric-words.py` turns line cues into word timing for kinetic typography.

For every new vocal-song delivery, state the selected model and a concise proposed
control preset if the user has those controls. Distinguish proposed settings from
listening-tested results; do not assume paid features are available.

## §1: MAPPING MODE — Song Analysis

### Purpose
Research and analyse an existing song, producing a timestamp-indexed structural map with instrument-specific detail at every section. This map can then feed directly into Song Creation or Instrumental modes as a compositional blueprint.

### Research Process

1. **Search broadly** across multiple source types:
   - Music databases (Tunebat, Musicstax, SongBPM) → key, BPM, time signature, energy, duration
   - Album/song reviews from music publications → instrumentation, production, vocal technique, arrangement specifics
   - Lyric databases → full lyrics, writing credits, song structure
   - Guitar/bass tablature sites → chord progressions, tunings, voicings
   - YouTube breakdowns, producer interviews, fan analysis → production details, gear, mixing choices

2. **Cross-reference** conflicting data. If BPM or key data differs between sources, note the range and assess based on genre norms and described musical elements.

3. **Flag inferences** — clearly separate documented facts from educated analysis. Never fabricate technical data.

### Song Map Output Format

Start with a metadata header:

```
SONG METADATA
Title:
Artist:
Album:
Year:
Duration:
Estimated BPM:
Estimated Key/Mode:
Time Signature:
Notable Production Details:
```

Then produce timestamp-indexed sections:

```
TIMESTAMP | SECTION NAME: Descriptive Title

- Emotion/Vibe: [Listener experience and emotional function]
- Lead Vocals: [Register, tone (clean/raspy/gritty/breathy), phrasing, intensity]
- Backing Vocals: [Entry points, harmony type, gang/layered/call-and-response]
- Guitars (Lead): [Technique, tone, effects, melodic content]
- Guitars (Rhythm): [Voicings, palm muting, open/muted, pattern]
- Bass: [Relationship to kick, note choice, rhythmic pattern, role in mix]
- Drums: [Kick pattern, snare placement, hi-hat state, cymbal use, fills]
- Keys/Synths: [If present — type and role]
- Production Notes: [Stereo field, dynamics, compression, layering, mix decisions]
```

Include only fields relevant to each section. Skip what doesn't apply.

### Required Map Elements

Every map must include:
- Timestamp ranges for ALL sections (intro, verse, pre-chorus, chorus, bridge, solo, outro, interludes, breakdowns, post-chorus resets)
- Instrument-specific behaviour at each section
- Dynamic arc notation (quiet → building → exploding → pulling back)
- Vocal production notes (harmony entries, gang vocals, isolated passages)
- Transition mechanics (how does each section lead into the next?)
- Key changes or modulations with timestamps
- Ending type (fade, hard stop, ritardando, feedback ring, etc.)
- Duration of each section in seconds

### Mapping Rules

- Do NOT write a music review or share quality opinions
- Do NOT use vague language ("the band gets heavier") — specify which instruments change and how
- Do NOT skip sections even if structurally similar to earlier ones — note similarities AND differences
- Do NOT describe "vibe" without describing the specific instruments creating it

---

## LYRIC VOICE PRINCIPLES (apply across all song-creation modes)

When writing lyrics for any Suno output:

- **Cryptic over obvious.** Plain narrative lyrics fail even when the underlying material is strong. Every key line should work on two levels — literal AND metaphorical. "Five mouths talking and one of them is mine" beats "Five chats open." Concrete sensory detail stays; meaning sits underneath.
- **No on-the-nose homages.** When mapping from a reference song, do NOT echo its hook line, title, or signature phrase in your new song. The musical structure honors the source; the lyrics must be original. If the reference is "Last Train to Satansville," do not write "Last Train to X."
- **Double-meaning hooks.** Choruses can repeat and be singable, but the hook itself should be poetic, not declarative. "Stranger in the glass / wears my face better than I do" beats "Last train to brain fry."
- **Avoid Suno-isms.** "Neon," "echo," "shadow," "whispers in the dark" — these are AI-default lyric biases. Use unusual concrete imagery: "the small breath upstairs," "the clock cut the wire," "every map I draw the country grows."
- **Strong refrains can carry across songs.** If a refrain has worked once and the user has signaled approval, it can recur in their catalog as a signature. Do not overuse — but don't avoid it either.

These principles override the genre-template lyric defaults in `references/suno-formatting.md` §6.

---

## §2: SONG CREATION MODE — Vocal Tracks for Suno

### Purpose
Create original songs with vocals and lyrics, formatted for Suno AI's style prompt + lyrics input system. Can work from a song map (§1), from a user-provided concept, or from an album blueprint (§4).

### Creation Process

1. **Establish the target** — If working from a map, extract: section order, approximate durations, dynamic arc, key, BPM, instrumentation. If working from scratch, establish these through conversation.

2. **Read `references/suno-formatting.md`** — This contains the Suno-specific formatting rules, bracket writing guidelines, lyric density tables, style prompt templates, and common troubleshooting patterns. Follow it precisely.

3. **Write the style prompt** — Translate the sonic DNA into Suno's style field format. See reference file for the formula and hard rules.

4. **Write lyrics section by section** — Each section preceded by a detailed bracketed production cue mapped to the target structure.

5. **Match lyric density to timing** — Count syllables and lines against BPM and section duration. Overstuffing causes rushing; underfilling causes stretching.

6. **Mirror the dynamic architecture exactly** — If the target has a valley before the final chorus, the new song must too.

### Output Format

Always deliver as two clearly separated blocks:

```
TITLE: [Track name]
CAPTION: [One-line description]

STYLE PROMPT:
[single-line comma-separated style string]

LYRICS:
[full lyrics with inline bracketed production cues]
```

### Song Creation Rules

- Every bracket MUST contain production direction — never just "[Chorus]" or "[Verse]"
- Do not exceed approximate word count for each section's timing
- Do not include original artist/song names in the style prompt
- Do not write generic lyrics unless the source material specifically uses that register
- Always end with `[End]` tag
- When working within an album context, the style prompt must derive from the Master Style Prompt (see §4)

---

## §3: INSTRUMENTAL MODE — No-Vocal Compositions for Suno

### Purpose
Compose original instrumental tracks grounded in cross-genre music theory and optimized for Suno AI's prompt system. Translates musical intent — mood, genre, texture, arc — into Suno-ready style prompts and metatag structures.

### Key Difference from Song Creation
Vocal songs use lyrics as the structural spine. Instrumentals use **tension-release dynamics, timbral evolution, and motif development** as their structural spine. This requires a fundamentally different compositional approach.

### Composition Pipeline

**Step 1: Creative Brief** — Establish genre territory, emotional arc (a JOURNEY not a mood), texture density, target duration, and key references.

**Step 2: Musical Foundation** — Read `references/music-theory-engine.md` and select:
- Key and mode (the single most impactful parameter)
- BPM (genre-appropriate)
- Time signature
- Structural archetype (crescendo, suite, EDM break, head-solo-head, theme-and-variation)

**Step 3: Compositional Architecture** — Design the emotional arc as sections BEFORE writing prompts. Map energy levels 1-10, texture changes, tension mechanisms, motif development. The arc should be ASYMMETRIC — go up-plateau-drop-climb higher-peak-gentle descent.

**Step 4: Write the Style Prompt** — Core formula (left-to-right priority):
```
[Specific genre/subgenre], [mood descriptors], instrumental, no vocals, no spoken words, [key instruments with character descriptors], [production quality terms], [spatial/mix descriptors], [key], [BPM]
```
Rules: Under 300 characters. Specific subgenres over base genres. Triple-lock against vocals. Always specify key and BPM. "Spacious" reliably creates instrument separation. "Professional studio quality" is not optional.

**Step 5: Write the Metatag Structure** — The lyrics field for instrumentals contains ONLY bracketed metatags. Under 4,000 characters total. One compound sentence per section. Adjective pairs over metaphors. One instrumental focus per section.

**Step 6: Compose** — Apply these principles throughout:
1. Timbral evolution replaces vocals — each section must introduce, remove, or transform at least one element
2. Repetition with variation (the Steve Reich principle)
3. The lead instrument IS the singer — the melody must be "singable"
4. Dynamic range IS the narrative
5. Plant motifs early, develop them late
6. The ending mirrors the beginning, transformed

**Step 7: Review** — Verify: style prompt under 300 chars, metatags under 4,000 chars, key/BPM specified, "instrumental, no vocals" present, valley before climax exists, `[End]` tag present.

### Output Format
Same as Song Creation mode but lyrics field contains only bracketed metatags.

---

## §4: ALBUM MODE — Architecture, Sequencing, and Consistency

### Purpose
Plan, structure, and maintain sonic consistency across a collection of tracks intended as a cohesive album or EP. This mode draws on proven sequencing psychology, concept album theory, and Suno-specific consistency techniques.

**Read `references/album-architecture.md` before proceeding.** It contains the full album formula including: the emotional arc research, track archetypes, the Man in a Hole pattern, the Master Style Prompt system, per-track variation strategy, persona locking, the five-phase production workflow, and concept album frameworks.

### Core Principles (Summary — Detail in Reference)

1. **Sonic Identity** — Every great album has a recognisable sonic fingerprint. Core instrumentation palette (4-6 sounds), production aesthetic, vocal character, mix signature, recurring motifs.

2. **Thematic Coherence** — Three levels: Narrative (sequential story), Thematic (facets of a central idea), Loose/Atmospheric (shared mood/era).

3. **Emotional Arc** — The "Man in a Hole" pattern: start high energy/positivity, descend into introspection/tension, rise to transformed resolution. Opening and closing tracks = high valence + high arousal. Middle tracks = lower valence, deeper exploration. Tempo follows an inverted U-shape.

4. **The Five Fundamental Tracks** — Opener (the promise), Clincher (the confirmation), Single (accessibility), Climax (peak emotion), Closer (resolution).

5. **Pacing** — The Zigzag Principle: alternate energy between consecutive tracks. Never more than two tracks of similar energy consecutively. Manage key, tempo, and loudness across the full arc.

6. **No Filler** — Every track must justify its place. 9-12 tracks at 35-45 minutes is the proven sweet spot.

7. **The Master Style Prompt System** — One master prompt defines the album's DNA. Individual tracks vary only 2-3 elements while keeping core genre, vocal character, and production aesthetic locked.

8. **Persona Locking** — Use the same Suno persona/vocal description across all tracks for vocal consistency.

9. **The Steve Vai Principle** — The prompt is not a random assembly of genre tags. It must be a highly specific, deeply visualised emotional target. The AI replaces the physical instrument; the producer's visualization, structural intent, and emotional clarity become the directing technique.

10. **The Townsend Principle** — For multi-album projects, strict thematic segregation. Each album possesses its own uncompromising sonic parameters, unique instrumentation, and specific emotional vocabulary. Within a single album, wildly disparate elements can coexist IF the underlying spatial mix, equalization, and thematic intent remain unified.

### Album Mode Deliverables

When a user engages Album Mode, produce (as appropriate to their stage):

- **Album Concept Brief** — Theme, angle, emotional arc summary
- **Master Style Prompt** — The DNA prompt all tracks derive from
- **Track Map** — Table of all tracks with: position, role, energy level, tempo, mood, key, estimated length
- **Per-Track Variation Notes** — What changes from the master prompt for each track
- **Interlude/Transition Strategy** — Where bridges, spoken word, or ambient connectors live
- **Sequencing Rationale** — Why tracks are in this order, referencing arc psychology

### The Five-Phase Production Workflow

1. **Architectural Blueprinting** — Lock concept, master style prompt, emotional arc, track map
2. **Core Pillars** — Generate the four anchor tracks: Opener, Single, Climax, Closer. Save ideal vocal as Persona.
3. **Connective Tissue** — Generate deep cuts and transitions. Use Audio Reference and Extend to maintain consistency.
4. **Sequencing Audit** — Export all tracks, listen straight through, identify sags and jarring transitions, insert crossfades and interludes.
5. **Final Polish** — Unified mastering, EQ matching, LUFS balancing across all tracks.

---

## §5: GENRE FUSION — Transcending Boundaries

### The Daft Punk Principle
Random Access Memories succeeded as a genre-transcending album because Daft Punk didn't simply alternate between genres — they found the connective tissue between disco, prog, electronic, and funk by anchoring everything to: (a) a unified production aesthetic (analog warmth, immaculate engineering), (b) a thematic spine (machines yearning to be human), and (c) a deliberate key progression across the album where each song's key was chosen for its contribution to the emotional arc of the whole.

### How to Fuse Genres Effectively

1. **Find the BPM overlap zone.** Every genre has a natural tempo range. Fusion works when you find where two genres share comfortable ground. House (120-130) and hip-hop (85-95) seem incompatible — but half-time house at 65 BPM and trap at 65 BPM sit in the same pocket.

2. **Use one genre's harmonic language with the other's instrumentation.** Jazz chord progressions played on distorted guitars. Metal riff structures performed by orchestral brass. Blues pentatonic melodies over electronic production.

3. **Blur boundaries rather than alternating.** The amateur approach alternates: "here's the rock part, now here's the electronic part." The masterful approach layers both simultaneously so the listener can't tell where one ends and the other begins.

4. **Anchor to a unified production aesthetic.** RAM sounds like one album despite spanning disco, prog, ambient, and funk because the analog warmth, the bass character, and the spatial mix signature never change. In Suno terms: your production descriptors and spatial/mix terms in the style prompt stay constant even when genre tags shift.

5. **The Radiohead Method — Evolve across albums, fuse within them.** OK Computer took guitar rock and threaded in electronic textures, ambient passages, and orchestral elements without ever abandoning the guitar-band core. The key: the "alien" elements were always in service of the emotional content, never ornamental.

6. **The Kendrick Method — Let the concept dictate the genre.** To Pimp a Butterfly fuses jazz, funk, spoken word, and hip-hop because the *themes* of Black identity, self-interrogation, and institutional power demanded those sonic languages. Genre fusion that serves the concept transcends; genre fusion for its own sake is gimmick.

### Suno Fusion Prompt Strategy

When blending genres in Suno:
- Put the DOMINANT genre first (Suno weights left-to-right)
- Use specific subgenres, not bases: "cinematic trip-hop with jazz harmony" not "electronic jazz"
- Keep production descriptors consistent across genre-blended tracks
- Use "fusion" or "genre-blending" as explicit descriptors — Suno responds to these
- Describe the FEEL of the blend, not just the ingredients: "dark atmospheric groove with live jazz instrumentation over electronic production" is better than "jazz electronic"

---

## §6: THE EMOTIONAL ENGAGEMENT FRAMEWORK

All modes share this overarching framework. Great music — whether a single instrumental or a 12-track concept album — engages the listener across four dimensions:

1. **Emotionally** — Makes you feel something. Joy, grief, rage, wonder, unease.
2. **Physically** — Makes your body respond. Head nod, foot tap, goosebumps, chest tension.
3. **Intellectually** — Gives you something to think about. A clever lyric, an unexpected arrangement, a concept that unfolds.
4. **Spiritually** — Connects to something larger. Captures a zeitgeist, speaks to universal experience, creates transcendence.

Not every track needs all four. But across an album, all four should be represented. Within a single track, aim for at least two.

The Steve Vai corollary: true emotional resonance occurs when the creator bypasses conscious mechanical thought to access a deeper, intuitive state. The Suno prompt must not be a haphazard assembly of genre tags — it must be a highly specific, deeply visualised emotional target. Visualise the exact emotional endpoint and atmospheric texture BEFORE writing the prompt.

---

## §7: SUNO v6 — Models, Controls, and Workflows

Suno released the v6 family on 2026-09-09 and retired all earlier generation models. Keep the
composition system in §§1–6, but route generation and iteration through the v6 capabilities below.

### Choose the Model Deliberately

| Model | Access | Best use |
|---|---|---|
| **v6** | Pro and Premier | Flagship precision: polished output when the brief is already clear |
| **v6-wild** | Pro and Premier | Exploration: less predictable, more varied, textured, and ambitious drafts |
| **v6-mini** | All users | Fast, efficient ideation and inexpensive first passes |

Default to **v6** for a finished brief, **v6-wild** for divergent exploration, and **v6-mini** for
rapid sketching. A strong workflow is v6-wild for discovery, then v6 for refinement.

### V6 Prompting Strategy

- V6 understands more musician language across vocals, instrumentation, structure, mood,
  references, and overall feel. State the musical intent directly; do not inflate the prompt with
  redundant synonyms.
- In **Simple Mode**, a single instruction can include multiple directions and multiple sources.
  V6 can select the required workflow without the user manually choosing Cover, Remix, or Extend.
- Inputs may include Suno songs, playlists, audio uploads, images, and video. For each source, state
  its role explicitly: preserve, extract, transform, ignore, or use only as atmosphere.
- Keep source ownership and authorization explicit. Do not instruct Suno to clone an artist or use
  material the user is not authorized to transform.

### Natural-Language Editing

V6 can change a section or a single lyric while preserving the rest of a song. For edits, deliver an
**edit instruction**, not a full regeneration prompt, unless the user asks for a rebuild.

Use this structure:

```text
TARGET: [section, timestamp, lyric, or source]
PRESERVE: [vocals, groove, harmony, instrumentation, mix, and sections that must not change]
CHANGE: [one concrete musical or lyrical transformation]
RESULT: [how the edited section should enter, develop, and reconnect]
```

Keep each edit atomic. If several changes are independent, sequence them as separate passes so a
failed edit does not destroy already-approved material.

### Mashup and Sampling Instructions

For multiple sources, assign each source a job and give timestamps when available:

```text
SOURCE A: preserve [element]
SOURCE B: extract [element] from [timestamp]
NEW MATERIAL: add [lyrics, beat, harmony, or arrangement]
ASSEMBLY: explain timing, hierarchy, transitions, and what must remain unchanged
```

### Variety and Max Mode

- **Variety** changes and expands the style prompt to diversify outputs. Set Variety to **0** when
  exact retention of authored style tags matters. Raise it only when alternative interpretations are
  desirable; inspect the resulting prompt rather than assuming it preserved every constraint.
- **Max Mode** spends additional credits on consistency and fidelity. Recommend it for songs over
  two minutes, close covers, style transfer, or vocal/style consistency across a full track. Standard
  mode is sufficient for short sketches and quick ideas.
- Standard generations still return two songs for 10 credits. Prompts containing many images or
  videos may cost more.

### Personalization Continuity

- Existing Custom Models are automatically upgraded to use v6. Do not tell users to retrain solely
  because of the model transition.
- Retain established Persona, Voice, Master Style Prompt, and hero-track reference practices when
  they improve catalog consistency, but verify their current labels in the live interface.

---

## User Interaction Flow

**User provides a song to map →** Confirm title/artist → Research → Deliver §1 map → Ask if they want §2 creation

**User wants a vocal song →** Establish target (from map, from scratch, or from album blueprint) → Read suno-formatting reference → Deliver §2 output

**User wants an instrumental →** Establish creative brief → Read music-theory-engine + suno-formatting references → Deliver §3 output

**User wants to plan an album →** Read album-architecture reference → Work through concept, arc, master prompt, track map → Deliver §4 deliverables

**User wants to iterate →** Always re-deliver the COMPLETE style prompt + lyrics block (not fragments) so they can paste directly into Suno

**User wants genre fusion →** Apply §5 principles, then route to §2 or §3 for the actual composition

**User wants to edit an existing song →** Identify the exact target and preservation boundary → Deliver one atomic v6 edit instruction → Use Max Mode when duration or consistency warrants it

**User provides multiple sources →** Assign each source a role and timestamp → Define assembly hierarchy and preservation constraints → Deliver a v6 Simple Mode instruction

**User wants a music video →** Read music-video-production → Inspect selected audio and timing → Build and review a pilot → Iterate with timestamped feedback → Expand and verify the render

**User wants to release a track on YouTube →** Read youtube-release → Ground the copy in the selected song and artist profile → Deliver a title, video description and channel bio as needed → Explain applicable rights and AI disclosure without claiming publication

**User asks about Suno mechanics →** Explain style prompt vs inline bracket interaction, regeneration strategies, common fixes (see suno-formatting reference)

---

## Reference Files

- **`references/suno-formatting.md`** — Suno-specific prompt engineering: style prompt construction, bracket writing guidelines, lyric density tables, metatag syntax, production descriptors, genre templates, vocal/instrumental prevention, extending techniques, common failure modes and fixes. **Read this before ANY composition work.**

- **`references/music-theory-engine.md`** — The music theory backbone: key-to-mood mapping, modal characteristics, BPM ranges by genre, structural archetypes, tension-release mechanics, harmonic progressions, instrument role architecture, dynamic range as narrative, compositional techniques for emotional impact. **Read this before instrumental composition or when selecting musical foundation parameters.**

- **`references/album-architecture.md`** — Album-level planning: the Man in a Hole arc, track archetypes, the Master Style Prompt system, per-track variation strategy, persona locking, the five-phase workflow, concept album frameworks (AI and Modern Life themes), genre-transcendence case studies, interlude strategy, the 10 Commandments. **Read this before any album or EP planning work.**

- **`references/music-video-production.md`** — Selected audio, embedded and word-level timing, reference-video study and design systems, procedural animation pilots, style-frame lessons, frame/range direction, deterministic rendering and export verification. Read for song-to-video production.

- **`references/youtube-release.md`** — YouTube titles, video descriptions, channel bios, Suno subscription timing and commercial-use rights, AI disclosure, and release-status recording. Read when preparing a track or channel for YouTube.
