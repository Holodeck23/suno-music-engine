---
name: suno-music-engine
description: >
  The complete AI music production system — from mapping existing songs into structural blueprints, to composing original vocal tracks and instrumentals for Suno AI, to architecting cohesive albums and EPs with proven sequencing psychology. Use this skill whenever the user mentions Suno, AI music, song creation, instrumentals, album planning, song mapping, music production, beat making, track breakdowns, concept albums, album sequencing, EP structure, or any request involving turning musical ideas into Suno-ready output. Also trigger when the user says things like "map this song," "write me a song like X," "create a Suno prompt," "make an instrumental," "plan an album," "help me sequence my tracks," "I want to make something that sounds like," "compose something," "write me a track," or describes any sonic vision they want realised through AI music generation. This skill replaces and unifies the former suno-song-architect and suno-instrumental-composer skills into a single comprehensive system. It covers the full pipeline from analysis through composition through album-level architecture.
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

Always read the relevant reference files BEFORE composing. The reference files contain the deep technical detail — key-to-mood mappings, BPM ranges, structural archetypes, Suno-specific syntax, album sequencing psychology, and production descriptor libraries.

---

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

## User Interaction Flow

**User provides a song to map →** Confirm title/artist → Research → Deliver §1 map → Ask if they want §2 creation

**User wants a vocal song →** Establish target (from map, from scratch, or from album blueprint) → Read suno-formatting reference → Deliver §2 output

**User wants an instrumental →** Establish creative brief → Read music-theory-engine + suno-formatting references → Deliver §3 output

**User wants to plan an album →** Read album-architecture reference → Work through concept, arc, master prompt, track map → Deliver §4 deliverables

**User wants to iterate →** Always re-deliver the COMPLETE style prompt + lyrics block (not fragments) so they can paste directly into Suno

**User wants genre fusion →** Apply §5 principles, then route to §2 or §3 for the actual composition

**User asks about Suno mechanics →** Explain style prompt vs inline bracket interaction, regeneration strategies, common fixes (see suno-formatting reference)

---

## Reference Files

- **`references/suno-formatting.md`** — Suno-specific prompt engineering: style prompt construction, bracket writing guidelines, lyric density tables, metatag syntax, production descriptors, genre templates, vocal/instrumental prevention, extending techniques, common failure modes and fixes. **Read this before ANY composition work.**

- **`references/music-theory-engine.md`** — The music theory backbone: key-to-mood mapping, modal characteristics, BPM ranges by genre, structural archetypes, tension-release mechanics, harmonic progressions, instrument role architecture, dynamic range as narrative, compositional techniques for emotional impact. **Read this before instrumental composition or when selecting musical foundation parameters.**

- **`references/album-architecture.md`** — Album-level planning: the Man in a Hole arc, track archetypes, the Master Style Prompt system, per-track variation strategy, persona locking, the five-phase workflow, concept album frameworks (AI and Modern Life themes), genre-transcendence case studies, interlude strategy, the 10 Commandments. **Read this before any album or EP planning work.**
