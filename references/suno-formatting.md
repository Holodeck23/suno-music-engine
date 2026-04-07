# Suno Formatting Reference

Complete prompt engineering reference for Suno AI — covering vocal songs, instrumentals, and album-level consistency. Every technique tested, every behavior documented.

## Table of Contents
1. How Suno Reads Input
2. Style Prompt Construction
3. Bracket / Metatag Writing Guidelines
4. Lyric Density Guidelines (Vocal Tracks)
5. Instrumental Metatag Rules
6. Lyric Writing By Section Type
7. Production Descriptors That Work
8. What Suno Hears vs Ignores
9. Preventing Unwanted Vocals (Instrumentals)
10. Building Longer Compositions
11. Style Prompt Templates By Genre
12. Common Failure Modes and Fixes
13. Album Consistency: The Master Style Prompt System
14. Persona Locking and Audio Referencing
15. The Extension and Post-Production Workflow
16. Advanced Techniques

---

## 1. How Suno Reads Input

Suno processes two distinct inputs:

### Style Prompt (Style/Genre Field)
- A comma-separated string defining the global sonic character
- Sets the overall palette: genre, tempo, key, instrumentation, vocal type, production qualities
- Sweet spot: 15-30 descriptive terms (5-8 core descriptors minimum)
- Do NOT exceed ~50 words / ~300 characters — Suno deprioritises terms in long prompts
- Do NOT include artist names or song titles — Suno may attempt to clone rather than create
- Specific genre terminology works better than generic ("Scandinavian melodic hard rock" > "rock")
- **Left-to-right priority** — Suno weights the first terms heaviest. Put the dominant genre first.

### Lyrics with Inline Bracketed Instructions
- Standard text = lyrics that Suno will sing
- `[Text in square brackets]` = production/arrangement cues that Suno interprets as directions
- Brackets are the primary moment-to-moment control tool
- For instrumentals: the lyrics field contains ONLY bracketed metatags
- More specific, evocative language produces better results than generic terms
- **Hard limit: ~5,000 characters** for the lyrics field. Budget 4,000 for metatags to leave margin.

---

## 2. Style Prompt Construction

### The Formula

**For vocal songs:**
```
[Specific genre/subgenre], [mood descriptors], [BPM], [time signature], [key],
[vocal character with delivery style], [core instrument 1 with character],
[core instrument 2], [production aesthetic], [spatial/mix terms], [duration], [ending type]
```

**For instrumentals:**
```
[Specific genre/subgenre], [mood descriptors], instrumental, no vocals, no spoken words,
[key instruments with character descriptors], [production quality terms],
[spatial/mix descriptors], [key], [BPM]
```

### Hard Rules

- **Under 300 characters total.** Suno silently truncates and deprioritises terms in long prompts.
- **5-8 descriptors is the sweet spot.** Fewer than 4 = generic (Suno fills gaps with defaults). More than 10 = conflicting signals producing "mush."
- **First descriptor carries most weight.** Put the dominant genre first. If blending, the first genre dominates.
- **Subgenres dramatically outperform base genres.** "Synth-pop" >> "pop." "Melodic techno" >> "electronic." "Doom metal" >> "metal." "Math rock" >> "rock."
- **"Pop" is gravitational.** Nearly every genre drifts toward pop unless excluded. This is one of the most important community discoveries.
- **Always include "professional studio quality" or "polished production."** Suno does NOT default to high quality. This is not optional.
- **No contradictions.** "Lo-fi polished," "aggressive and peaceful," "fast and slow" cancel each other out.
- **Always specify key and BPM.** These two parameters anchor more musical decisions than anything else.
- **Always pair key with matching mood descriptors.** "D minor" + "happy, bright" creates contradiction. "D minor" + "dark, brooding" aligns all signals.

### Descriptor Categories (pick 1-2 from each relevant category)

**Genre anchors**: progressive instrumental rock, dark ambient electronic, cinematic orchestral, jazz fusion, melodic post-metal, atmospheric downtempo, neo-classical, melodic hard rock, arena anthem, synth-pop, trip-hop, etc.

**Mood/energy**: melancholic, euphoric, brooding, ethereal, triumphant, haunting, luminous, expansive, intimate, aggressive, contemplative, ecstatic, atmospheric, intense, vulnerable, defiant

**Vocal character** (songs only): powerful male tenor with rasp, breathy female alto, gravelly baritone, soaring soprano, spoken word narrative, whispered intimate delivery, gang vocal harmonies, close-mic ASMR-like

**Instrument character** (not just names): warm fretless bass, screaming distorted guitar, shimmering clean arpeggios, deep sub-bass drone, soaring lead synth, haunting cello, crisp acoustic piano, thundering double kick, palm-muted power chord riff, tape-warped Rhodes

**Production quality**: professional studio quality, polished production, warm analog recording, crisp digital clarity, live room acoustics, lo-fi tape hiss, vintage vinyl warmth, tape-saturated warmth

**Spatial/mix**: spacious (MAGIC WORD — reliably creates instrument separation), wide stereo field, intimate close-mic, cavernous reverb, detailed mix, separated instruments, cathedral reverb, bedroom recording feel

---

## 3. Bracket / Metatag Writing Guidelines

### What To Include In Every Bracket

| Element | Example |
|---------|---------|
| Specific instruments and behaviour | "palm-muted power chord riff," "clean arpeggiated guitar" |
| Vocal register and tone (songs) | "mid-register raspy vocal," "upper tenor, full-throated" |
| Drum pattern specifics | "closed hi-hats, kick on 1 and 3, snare on 2 and 4" |
| Guitar technique | "wide open un-muted power chords filling stereo field" |
| Bass behaviour | "bass locked to kick drum pulsing eighth notes" |
| Dynamic level | "restrained controlled energy," "maximum intensity every instrument at peak" |
| Duration cue | "4 bars," "13 seconds," "brief 2-bar transition" |
| Emotional/spatial language | "arena-sized singalong," "intimate and exposed," "wall of sound explosion" |

### Bracket Quality Spectrum

**Bad (too generic):**
```
[Chorus]
```

**Better (has direction but lacks specifics):**
```
[Chorus: Big and loud, full band, gang vocals]
```

**Best (mapped to the blueprint):**
```
[Chorus: Massive wall of sound explosion, lead vocal upper tenor register, thick multi-tracked gang vocal harmonies on major intervals, wide open un-muted power chords filling stereo field, crash cymbals on every downbeat, rimshot snares at maximum crack, bass pounding root notes, arena-sized singalong]
```

### Reliable Section Tags

| Tag | Behavior | Reliability | Notes |
|---|---|---|---|
| `[Intro]` | Opens the track | UNRELIABLE alone | Use `[Short Instrumental Intro]` or describe fully |
| `[Verse]` / `[Verse 2]` | Standard section | High | Add modifiers: `[Verse 2: add intensity, heavier drums]` |
| `[Pre-Chorus]` | Transitional build | High | Stack with energy descriptors |
| `[Chorus]` | Hook section | High | Always add dynamics and instrumentation |
| `[Bridge]` | Contrast section | Moderate | Describe what changes from surrounding sections |
| `[Guitar Solo]` | Lead instrument | Moderate | ALWAYS specify duration or it gets cut short |
| `[Outro]` | Closing section | High | Describe the ending type explicitly |
| `[Breakdown]` | Stripped section | High | List what's removed AND what remains |
| `[Build]` | Rising intensity | Moderate | Describe the crescendo mechanism |
| `[End]` | Terminates generation | ESSENTIAL | Always include as final tag |

### Tag Stacking (Advanced)
Place 3-4 specific meta-tags before a section to force strict compliance:
```
[Chorus | explosive dynamics | distorted wall of sound | desperate vocal belting]
```

---

## 4. Lyric Density Guidelines (Vocal Tracks)

Lyric count must match section duration at the target BPM. Overstuffed = rushing/skipping. Underfilled = stretching/improvising.

### At 120-140 BPM

| Section Type | Typical Duration | Suggested Lines | Words Per Line |
|-------------|-----------------|----------------|---------------|
| Intro (instrumental) | 8-15 seconds | 0 (brackets only) | — |
| Verse | 15-20 seconds | 4 lines | 6-10 words |
| Pre-Chorus | 10-12 seconds | 2-3 lines | 6-10 words |
| Chorus | 20-25 seconds | 5-6 lines | 5-8 words |
| Bridge | 8-12 seconds | 2 lines | 6-10 words |
| Post-Chorus/Interlude | 3-6 seconds | 0 (brackets only) | — |
| Outro/Chant | 8-15 seconds | 2-4 short phrases | 3-5 words |

### Total Song Budget
- ~3 minute song: approximately 150-200 words of lyrics (excluding brackets)
- ~4 minute song: approximately 200-280 words
- Brackets add to processing but not to sung duration

---

## 5. Instrumental Metatag Rules

For instrumentals, the lyrics field contains ONLY bracketed metatags — no sung text.

- **Total metatag structure must be under 4,000 characters.** Hard limit.
- **One compound sentence per section.** Not paragraphs. Architectural cues.
- **Adjective pairs over metaphors.** "Triumphant and overwhelming" does the same work as "like standing inside a sunrise" in fewer characters.
- **Duration cues only where critical.** Intros and solos benefit from duration. Verses usually don't.
- **One instrumental focus per section.** Don't stack multiple solos — pick one lead per section.
- **Describe dynamics as narrative.** "Quiet intimate opening building to massive explosive climax" not "high dynamic range."
- **Evocative spatial language works.** "Cathedral reverb," "wide stereo field," "instruments emerging from fog" — Suno processes these as mix directives.
- **Always end with `[End]`** to prevent auto-extending.

---

## 6. Lyric Writing By Section Type

### Verses
- Short, rhythmic, punchy lines. Monosyllabic and disyllabic words dominate.
- Lines feel locked to the beat — rhythmic delivery over melodic sweep.
- Narrative or scene-setting function.

### Pre-Chorus
- Ascending emotional intensity. Lines slightly longer than verses.
- Build momentum with imagery and action words.
- Anaphoric structures often work ("Through the storm... Through the walls...")

### Chorus
- The hook lives here. Core phrase: 6 words or fewer for singability.
- Anaphoric structures work well (repeated parallel openings).
- Gang vocal sections need universally singable, simple words.
- Directness wins — avoid complex metaphors.

### Bridge
- Vulnerable, stripped back. Fewer words, more space.
- Often the only section with genuine emotional exposure.
- Contrast with surrounding sections is critical.

### Outro/Chant
- Distill the chorus to its shortest possible phrase. 3-5 words maximum, repeated 2-4 times.
- Designed for crowd singalong.

---

## 7. Production Descriptors That Work

Tested across thousands of Suno generations — these descriptors reliably produce the described effect:

**Spatial (HIGH reliability):**
spacious, wide stereo field, cavernous reverb, intimate close-mic, cathedral reverb, separated instruments, detailed mix

**Texture (HIGH reliability):**
warm analog, crisp digital clarity, tape-saturated, lo-fi tape hiss, polished radio-ready, vinyl crackle, bedroom recording feel

**Dynamic (MODERATE reliability):**
crescendo, building intensity, explosive, stripped back, sparse arrangement, wall of sound, massive

**Tempo Feel (HIGH reliability):**
driving groove, laid-back swing, pulsing, hypnotic, relentless, stuttering

---

## 8. What Suno Hears vs Ignores

**Suno responds well to:** Genre labels, mood words, instrument names with character descriptors, BPM, key, production quality terms, spatial terms, "instrumental/no vocals," structural tags with description

**Suno partially processes:** Exact duration requests (approximate, not precise), dynamic contrast language, specific drum pattern descriptions

**Suno largely ignores:** Very long prompts past ~300 chars (deprioritised), abstract poetry in brackets, specific mixing dB values, references to other songs/artists, contradictory terms

---

## 9. Preventing Unwanted Vocals (Instrumentals)

Triple-lock approach:
1. Style prompt: include "instrumental, no vocals, no spoken words"
2. First metatag: include "instrumental only, no singing"
3. Do NOT include any text outside of brackets in the lyrics field

If vocals still bleed through: add "no vocal harmonies, no humming, no choir" to style prompt. Regenerate — vocal casting is partly random.

---

## 10. Building Longer Compositions

For tracks over 4 minutes, use Suno's **Extend** function rather than cramming everything into one generation:

1. Generate a strong initial section (intro + first verse/section)
2. Extend from the precise endpoint to build the next section
3. Extending at 00:00 can duplicate the sonic texture for a variation
4. Extending at the tail of a chorus can force a bridge shift
5. Use **Replace Section** for localized corrections without destroying the instrumental bed

---

## 11. Style Prompt Templates By Genre

### Arena/Melodic Hard Rock
```
Melodic hard rock, arena anthem, [BPM], 4/4, [KEY], powerful [male/female] [tenor/alto] vocals [with rasp], multi-tracked gang vocal harmonies, high-gain [palm-muted/crunchy] guitar riff, driving [snare-heavy] drums, tight bass locked to kick, modern polished rock production, [DURATION], [ENDING TYPE]
```

### Power Ballad
```
Power ballad, melodic rock, [BPM], 4/4, [KEY], emotional [male/female] vocals clean and expressive, acoustic guitar opening building to full band, soaring vocal harmonies, orchestral strings, gradual dynamic build from intimate to massive, [DURATION]
```

### Modern Metal / Alt-Metal
```
Modern metal, aggressive, [BPM], 4/4, [KEY] minor, heavy down-tuned guitar riffs, screamed and clean vocal contrast, double kick drums, palm-muted breakdowns, atmospheric bridge sections, dense compressed production, [DURATION]
```

### Electronic / Synth-Based
```
[Subgenre: synth-pop / darkwave / melodic techno / ambient], [mood], [BPM], [KEY], [synth type] lead, [bass type], [drum machine style], [production aesthetic], spacious, [DURATION]
```

### Cinematic / Orchestral Instrumental
```
Cinematic orchestral, [mood], instrumental, no vocals, no spoken words, [lead instrument], sweeping strings, [brass/woodwind], dynamic percussion, professional studio quality, spacious, [KEY], [BPM]
```

### Genre Fusion Template
```
[Dominant genre] with [secondary genre] elements, [mood], [vocal or instrumental tag], [instrument from genre A with character], [instrument from genre B with character], [unified production aesthetic], spacious, [KEY], [BPM]
```

---

## 12. Common Failure Modes and Fixes

### Vocal enters too early over intro
**Fix:** `[Intro: Driving drum groove with palm-muted power chord riff, 13 seconds, no vocals, instrumental only]`

### Guitar solo too short or skipped
**Fix:** Specify duration and describe style: `[Guitar Solo: Melodic pentatonic lead, expressive bends with wide vibrato, 16 seconds, full band maintains heavy groove underneath]`

### Dynamics too flat
**Fix:** Use explicit contrast: `[Verse: Restrained, controlled energy, guitars thin and muted]` then `[Chorus: FULL explosion, maximum intensity, wall of sound]`

### Wrong vocal timbre
**Fix:** Be specific in BOTH style prompt AND first vocal bracket. Also: regenerate. Vocal casting is partly random.

### Song runs too long or short
**Fix:** Adjust lyric density. More words = longer. Also specify duration in style prompt.

### Key change doesn't happen
**Fix:** Explicit separate bracket: `[Key Change: Modulate up one whole step, big drum fill into final chorus]`

### Ending fades instead of hard stop
**Fix:** `[Outro: Synchronized staccato power chord stabs, final hard stop on root chord, cymbal ring trailing to silence] [End]`

### "Suno-isms" — overuse of words like "neon," "echo," "shadow"
**Fix:** Use highly concrete, specific imagery in lyrics. Replace abstract terms with sensory detail. The AI defaults to its training biases when given vague input.

---

## 13. Album Consistency: The Master Style Prompt System

### Creating the Master Prompt

One master prompt defines the album's sonic DNA. All tracks derive from this base.

**Formula:**
```
[primary genre], [subgenre], [mood descriptor 1], [mood descriptor 2],
[vocal character], [core instrument 1], [core instrument 2], [core instrument 3],
[production aesthetic], [mix descriptor], [tempo range]
```

### Per-Track Variation Strategy

For each track, modify the master prompt by adjusting 2-3 elements MAXIMUM:

| What to vary | How |
|---|---|
| Mood descriptors | "atmospheric and intense" → "haunting and vulnerable" for a deep cut |
| Tempo | 120 BPM → 85 BPM for a ballad |
| Energy level | Add "sparse arrangement" or "stripped back" for quieter moments |
| Specific instruments | Add "acoustic guitar, piano" while keeping core palette |
| Production cues | Add "reverb-heavy, ambient" or "dry and intimate" to shift space |

### What NEVER varies (album consistency anchors):
- Primary genre tag
- Vocal character description
- Core production aesthetic
- Fundamental "feel" descriptors

---

## 14. Persona Locking and Audio Referencing

### Persona Locking
Once Suno yields the ideal vocal tone for your album, save it as a Persona. Apply that Persona to ALL subsequent tracks. This ensures biological vocal characteristics stay consistent whether the track is a whispered ballad or a screaming climax.

**Persona locks vocals only** — it does NOT guarantee instrumental or mix cohesion. Use the Master Style Prompt system for that.

### Audio Referencing
Upload a 6-to-60-second audio seed (a drum groove, a synth drone, a chord progression) as the foundational template. This anchors generated tracks to the same ambient space, EQ curves, and mix signature. It effectively tricks the algorithm into producing cohesive output mimicking a single studio session.

### Vocal Consistency Prompt Pattern
```
[gender] vocals, [tone descriptor], [delivery style], [register range],
[emotional quality], [technical quality]
```
Example: `male vocals, rich baritone with grit, passionate delivery, mid-low register with powerful high notes, raw emotional intensity, clear diction`

---

## 15. The Extension and Post-Production Workflow

### The Generative Audio Workstation (GAW) Approach
Never rely on "one-shot" generations. Treat Suno as a compositional tool, not a slot machine.

1. Generate a strong initial section (intro + first verse)
2. Extend from precise timestamps to build subsequent sections
3. Use Replace Section for localized fixes without destroying the instrumental bed
4. Export stems (Suno's 12-track extraction) into a DAW
5. In the DAW: remove AI artifacts, replace weak drum hits, apply cohesive mastering

### Album-Level Post-Production
- Standardize EQ curves across all tracks
- Apply cohesive bus compression
- Balance LUFS (Loudness Units relative to Full Scale) across the album
- Insert precise silence gaps or crossfades between tracks
- Master for target platform (streaming = -14 LUFS, CD = -9 LUFS)

---

## 16. Advanced Techniques

### Negative Prompting / Exclusions
Prevent Suno from utilizing default biases: "no pop hooks, no EDM drops, no autotune" can steer output away from unwanted territory.

### IPA for Pronunciation
Use International Phonetic Alphabet to force correct pronunciation of unusual or complex words, preventing immersion-breaking vocal glitches.

### Mixing and Mastering Descriptors in Lyrics
Adding mixing/mastering descriptors at the START of the lyrics field can influence audio quality:
```
[Mix: warm, balanced, wide stereo, punchy low end, crisp highs]
```

### Structural Consistency via Metatags
Use consistent section labeling language across all album tracks. If your album uses `[Verse] [Pre-Chorus] [Chorus]` patterns, maintain that vocabulary. This trains Suno to produce structurally similar outputs.

### The Core Reference Song Method
Generate one "hero track" that perfectly captures your sound. Use its audio as the reference seed for all subsequent tracks. This is the single most effective consistency technique available.
