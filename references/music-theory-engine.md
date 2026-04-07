# Instrumental Music Framework

Cross-genre analysis of 60+ acclaimed instrumental tracks distilled into actionable composition parameters. This is the music theory engine that powers every compositional decision.

## Table of Contents
1. Key-to-Mood Mapping
2. Modal Characteristics and Usage
3. BPM Ranges by Genre
4. Structural Archetypes
5. Tension-Release Mechanics (Neuroscience-Backed)
6. Seven Techniques for Holding Attention Without Vocals
7. Harmonic Progressions That Work
8. Instrument Role Architecture
9. Dynamic Range as Narrative
10. Track Length and Structural Density
11. Compositional Techniques for Emotional Impact

---

## 1. Key-to-Mood Mapping

The single most impactful parameter in any Suno prompt. Key choice shapes all harmonic possibilities and emotional character. Community power users describe specifying key as "the single most impactful thing you can add."

### By Target Emotion

| Target Emotion | Key/Mode | Suno Mood Descriptors | Reference Tracks |
|---|---|---|---|
| Pensive, uncertain | D Dorian | brooding, reflective, atmospheric, jazz-influenced | Miles Davis "So What" |
| Tragic, devastating | C# minor or Bb minor | melancholic, devastating, cinematic, adagio | Beethoven Moonlight Sonata, Barber Adagio for Strings |
| Dreamy, wonder, lift | Lydian mode (any root) | ethereal, floating, shimmering, cinematic | Satriani leads, John Williams scores |
| Dark, aggressive | E minor or A minor | dark, aggressive, driving, heavy | Metallica "Orion," most metal instrumentals |
| Exotic, edgy | Harmonic minor (any root) | exotic, mysterious, intense, Middle Eastern influence | Polyphia "G.O.A.T.," neoclassical metal |
| Uplifting, triumphant | D major or G major | triumphant, euphoric, anthemic, soaring | Major-key rock anthems |
| Nostalgic warmth | F major or Bb major | warm, nostalgic, intimate, vintage | Jazz standards, warm film scores |
| Endless, unresolved | Modal ambiguity (Am-Em-G-D) | cinematic, expansive, building, unresolved | Hans Zimmer "Time" from Inception |
| Bright progressive complexity | E Lydian | luminous, expansive, progressive, wide-eyed | The raised A# on guitar-friendly root |
| Melancholic beauty | D minor | dark but beautiful, atmospheric, emotional | Classical and cinematic tradition |
| Bluesy, earthy | A Mixolydian or E Mixolydian | warm, groovy, bluesy, earthy | Blues-rock, Celtic reels |

### By Genre Convention

- **Guitar instrumentals**: E minor, A minor, B minor dominate because open strings resonate sympathetically and common chord shapes fall naturally under the fingers. Metallica's "Orion," Steve Vai's "Tender Surrender," Polyphia's "Playing God," and Explosions in the Sky's "Your Hand in Mine" all center on E minor or E major.
- **Jazz**: Flat keys dominate because trumpets and saxophones are Bb and Eb transposing instruments. F major leads the Real Book with 221 entries, followed by C (191), Eb (159), Bb (141).
- **Electronic**: Strongest minor-key bias of any genre. Deadmau5's "Strobe" sits in G# minor, Daft Punk leans E minor and G minor, Boards of Canada average across F#m, Am, C#m.
- **Classical emotional**: Spans wider range but favors sharps/flats at extremes. Beethoven Moonlight Sonata C# minor, Barber Adagio Bb minor, Chopin Nocturne Eb major.
- **Film/cinematic**: Deliberate modal ambiguity. Zimmer's "Time" is analyzed variously as G major, E minor, A Dorian, or D Mixolydian — the Am-Em-G-D loop never resolves to a clear tonic, creating what analysts call a plagal sound that never ends.
- **Celtic**: D major, G major, A Mixolydian, E Dorian. Modal inflections (Mixolydian flat 7th, Dorian raised 6th) distinguish Celtic from generic major/minor.
- **Spotify global data**: G major (10.7%) and C major (10.2%) are the two most common keys across 30 million songs. But among emotionally powerful instrumentals, minor keys dominate roughly 2:1.

### Key Pairing Rule

Always pair key specification with matching mood descriptors in the style prompt. "D minor" + "happy, bright" creates contradiction that confuses Suno. "D minor" + "dark, brooding, atmospheric" aligns all signals. Alignment produces coherent output; contradiction produces mush.

---

## 2. Modal Characteristics and Usage

Great instrumental composers rarely stick to plain major or natural minor — they exploit modes for specific emotional colorations. Dorian appears in more acclaimed instrumentals than any other non-major/minor mode.

### Mode Reference

**Dorian** (minor with raised 6th)
- Sound: Brooding but warm. Pensive. Ambiguous between sadness and hope.
- Why: The raised 6th (B natural in D Dorian instead of Bb) adds unexpected warmth to a minor foundation.
- Use in: Jazz, Celtic folk, funk, atmospheric rock, anything "thoughtful dark."
- Reference: Miles Davis "So What" — the landmark that defined modal jazz.
- Suno descriptors: brooding, reflective, atmospheric, jazz-influenced, warm minor

**Mixolydian** (major with flat 7th)
- Sound: Bluesy, earthy, grounded. Major but with gravity.
- Why: The flat 7th pulls the brightness of major toward the earth.
- Use in: Blues-rock, Celtic reels, classic rock solos, roots music.
- Suno descriptors: bluesy, warm, earthy, groovy, classic rock feel

**Lydian** (major with raised 4th)
- Sound: Dreamy, bright, otherworldly. The "wonder" mode.
- Why: The raised 4th creates a floating, unresolved brightness. It's major but stranger, more luminous.
- Use in: Film scores (John Williams), progressive rock, guitar virtuoso (Satriani), cinematic wonder.
- The raised 4th IS the emotional detonation point — when composing climaxes in Lydian, call this note out explicitly in metatags.
- Suno descriptors: ethereal, floating, shimmering, luminous, cinematic, dreamy

**Phrygian** (minor with flat 2nd)
- Sound: Spanish, dark, exotic, intense. The "threat" mode.
- Why: The flat 2nd creates immediate tension against the root.
- Use in: Flamenco-influenced metal, Middle Eastern textures, dark ambient.
- Suno descriptors: dark, exotic, Spanish-influenced, intense, Middle Eastern

**Harmonic minor** (natural minor with raised 7th)
- Sound: Exotic tension, dramatic, neoclassical. The "villain" scale.
- Why: The augmented 2nd interval (between flat 6th and raised 7th) creates instantly recognizable exotic flavor.
- Use in: Neoclassical metal, dramatic compositions, Eastern European/Middle Eastern fusion.
- Reference: Polyphia "G.O.A.T." uses harmonic minor for its exotic edge.
- Suno descriptors: exotic, mysterious, intense, neoclassical, dramatic

**Aeolian (natural minor)** — Standard minor. Straightforward darkness. The default when you want "sad" or "dark" without specific color.

---

## 3. BPM Ranges by Genre

### Detailed Genre Corridors

| Genre | BPM Range | Sweet Spot | Reference Points |
|---|---|---|---|
| Guitar virtuoso ballad | 58-95 | 85-95 | Vai "For the Love of God" 95, Beck "Cause We've Ended as Lovers" 58 |
| Post-rock | 70-100 | 75-85 | Slow enough for gradual builds |
| Ambient/drone | 50-80 | 60-70 | Or no discernible tempo |
| Downtempo/trip-hop | 70-100 | 80-90 | Massive Attack, Boards of Canada |
| Progressive rock/metal | 100-160 | 120-140 | Tool sweet spot |
| Metal (groove) | 100-140 | 115-130 | Pantera groove territory |
| Metal (thrash) | 140-220 | 160-180 | Speed is the point |
| Guitar shred | 130-200 | 140-167 | Satriani "Surfing with the Alien" 167 |
| House/deep house | 118-132 | 124-128 | DJ mixing standard |
| Techno | 125-150 | 130-140 | Harder = faster |
| Progressive house | 122-132 | 126-128 | Deadmau5 "Strobe" territory |
| Trance | 128-150 | 136-140 | Uplifting pushes 140+ |
| Drum and bass | 160-180 | 170-174 | Half-time feels common |
| IDM/glitch | 80-160 | Variable | Aphex Twin — tempo is compositional |
| Jazz/fusion | 80-200 | 100-136 | "So What" ~136 |
| Celtic folk | 80-160 | 100-130 | Jigs 120+, airs 80-100, reels 130+ |
| Film/cinematic | 40-120 | 70-90 | Barber Adagio 40-50, action 100+ |
| Psytrance | 135-150 | 140-145 | Shpongle at the lower end |

### Universal Sweet Spot: ~120 BPM (doubled resting heart rate, natural walking pace)

### Overlap Zones for Hybrid Compositions

When blending genres, find the BPM where both feel natural:
- Electronic + rock: 125-135
- Jazz + electronic: 90-110
- Metal + electronic: 128-140
- Ambient + post-rock: 65-80
- Film score + rock: 85-100
- Psytrance + metal: 135-145
- Celtic + electronic: 100-120

### Half-Time Perception

A track at 130 BPM can feel like 65 BPM in half-time sections. Powerful compositional tool — specify "half-time feel" or "double-time energy" in metatags when needed.

---

## 4. Structural Archetypes

Five models account for virtually all acclaimed instrumental music.

### The Crescendo Arc
**Used by**: Post-rock (Explosions in the Sky, Mogwai, GY!BE), cinematic scores
**Pattern**: Quiet/sparse → gradual layering → massive climax → denouement
**Duration**: 6-20 min. Needs time for the build to earn the payoff.
**Key technique**: Each repetition adds one element. Patience is the instrument. The listener barely notices each addition, but the cumulative effect is devastating.
**Harmonic approach**: Simple diatonic chords, often major keys. Power comes from dynamics and texture, not harmonic complexity.
**Metatag sequence**: `[Sparse Intro]` → `[Verse]` (repeat with additions) → `[Build]` → `[Climactic Chorus]` → `[Quiet Outro]`
**Critical rule**: Start at 1 and build to 10. Don't start at 4.

### The Suite Form
**Used by**: Progressive metal (Metallica "Orion"), progressive rock, neoclassical
**Pattern**: Multiple distinct sections with contrasting quiet middle. Resembles classical sonata form.
**Duration**: 6-10 min.
**Key technique**: Each section has its own identity but shares harmonic DNA. Metallica's "Orion" quiet bass interlude before climax — contrast makes eruption devastating.
**Metatag sequence**: `[Intro]` → `[Verse 1]` (riff A) → `[Bridge]` (contrast) → `[Verse 2]` (riff B) → `[Interlude]` (quiet) → `[Final Chorus]` (climactic return)

### The EDM Break Routine
**Used by**: All electronic dance genres
**Pattern**: Full groove → breakdown (strip elements) → build-up → drop (restore groove)
**Duration**: 5-10 min. "Strobe" at 10:37 demonstrates extended form.
**Key technique**: Breakdown creates absence. Drop fills it. Research confirms this creates peak-pleasurable emotional responses.
**Critical insight**: Even within this rigid framework, emotional power can come from an ambient intro. Consider 2-3 minutes of ambient opening before first build (the "Strobe" model).
**Metatag sequence**: `[Ambient Intro]` → `[Build]` → `[Drop]` → `[Breakdown]` → `[Build]` → `[Final Drop]` → `[Outro]`

### Head-Solo-Head
**Used by**: Jazz, fusion, jam-oriented instrumentals
**Pattern**: State melody → improvise over form → restate melody
**Duration**: 5-12 min.
**Metatag sequence**: `[Intro]` → `[Verse]` (melody) → `[Instrumental Break]` (solo sections) → `[Final Chorus]` (melody return) → `[Outro]`

### Theme and Variation
**Used by**: Classical, film scores, ambient, minimalist
**Pattern**: State theme → vary it → develop → full statement → quiet restatement
**Duration**: 4-15 min.
**Key technique**: Each variation changes one parameter while preserving theme identity.
**Brian Eno approach**: "Music for Airports" tape loops of incommensurable lengths — mechanical theme-and-variation creating infinite novelty from finite material.
**Metatag sequence**: `[Intro]` (theme) → `[Verse 1]` (variation 1) → `[Verse 2]` (variation 2) → `[Build]` (development) → `[Climactic Chorus]` (full statement) → `[Outro]` (quiet restatement)

### Combining Archetypes
The best compositions combine elements — a suite with crescendo arc within one section, an EDM track with theme-and-variation melody, a post-rock piece with jazz head-solo-head in its build. Use archetypes as building blocks, not prisons.

---

## 5. Tension-Release Mechanics (Neuroscience-Backed)

A 2026 BioRxiv study demonstrated musical tension patterns directly predict neural coupling fluctuations. UC Press research identifies tension-release as THE core mechanism of instrumental engagement.

### Six Features Driving Perceived Tension

1. **Loudness** — Dynamic range between sections
2. **Pitch height** — Higher = more tension. Climbing melodies build; descending release.
3. **Tonal tension** — Dissonance, unresolved harmony, chromaticism
4. **Roughness** — Distortion, overtone density. Overdrive = tension. Clean = release.
5. **Tempo** — Largest single share of tension arousal (ηp² = 0.344 across 750 excerpts)
6. **Onset frequency** — New sounds per second. Busy = tense. Sparse = relaxed.

### Practical Rules

- Build tension through DENSITY not just volume. Add instruments, rhythmic complexity, harmonic dissonance.
- Release through SUBTRACTION. Remove elements, simplify harmony, reduce tempo, clean up distortion.
- Biggest release requires biggest preceding tension. Plan the valley.
- **Silence is the most powerful tension tool.** A 2-beat gap before a drop beats any build. Specify in metatags.
- Repeated tension-release cycles with ESCALATION sustain long instrumentals. Each cycle peaks slightly higher.
- The asymmetric arc: up-plateau-drop-climb higher-peak-gentle descent. Second rise exceeds the first.
- **Barber's Adagio technique**: Build to devastating climax → SILENCE → quiet restatement on unresolved dominant. Silence after climax is as important as climax itself.

---

## 6. Seven Techniques for Holding Attention Without Vocals

### 1. Melodic Identity Replaces the Vocal Hook
Lead instrument must function as a singer. Beck's no-pick technique creates vocal quality through volume swells and whammy bar. Satriani composes "singable" guitar melodies. Zimmer's deliberately spare two-note piano voicings. The test: could someone hum the lead line?

### 2. Dynamic Range IS the Narrative
Without lyrics, volume and intensity arc become the story. Post-rock's near-silence to wall of sound creates catharsis through contrast. The louder you want the climax, the quieter the preceding section must be.

### 3. Repetition with Subtle Variation
The Steve Reich principle. Eno's tape loops never exactly repeat. Deadmau5 builds on loops with incremental filter automation. Formula: comfort (pattern recognition) + surprise (novelty). Change ONE element each cycle.

### 4. Timbral Evolution Substitutes for Lyrical Narrative
Changing tones, effects, instruments creates a journey through sonic space. Post-rock guitars as "tools for texture" through EBow, looping, effects. Electronic filter automation creates movement within static harmony. Each section should transform at least one timbral element.

### 5. Structural Surprise
Breaking established patterns at key moments. 4/4 shifting to 7/8. Clean interrupted by distortion. Expected resolution going elsewhere. Must feel MUSICAL — inevitable in retrospect.

### 6. Spatial Movement
Panning, reverb depth, stereo width changes create 3D sonic environment. Twin guitars in L/R channels. Moving close/dry to distant/reverberant creates physical journey. Vangelis CS-80 through Lexicon 224 creates cavernous depth. Boards of Canada VHS degradation creates temporal distance.

### 7. The Planted Motif
Introduce a simple idea casually early. Develop gradually. Transform into climax melody. Listener doesn't consciously notice the planting but feels the coherence when it blossoms. A descending figure can invert to become a soaring ascending climax — same notes, opposite direction, completely different impact.

---

## 7. Harmonic Progressions That Work

### Universal Power Progressions
- **I-V-vi-IV** — Most versatile. Triumphant, melancholic, or anthemic depending on arrangement.
- **Am-Em-G-D** (modal ambiguity) — Zimmer "Time." Never resolves. Endless forward motion.
- **i-VII-VI-VII** — Dark but forward-moving. Metal and post-rock.
- **I-vi-IV-V** — Nostalgic, warm, circular.
- **Plagal motion (IV-I)** — Gentle resolution. Peaceful, "amen" quality.

### Critical Finding
Harmonic complexity and emotional impact do NOT correlate linearly. Zimmer's "Time" = four diatonic chords. Barber's Adagio = stepwise ascending melody. Simple harmony with masterful dynamics beats complex harmony with flat dynamics every time.

### Extended Harmony (When Needed)
- 7th chords: Color without dissonance
- 9th chords: Jazz sophistication
- Suspended chords: Unresolved tension/ambiguity
- Altered dominants: Maximum tension before resolution
- Pedal tones: Holding bass while chords change above. Extremely effective in cinematic and post-rock.

---

## 8. Instrument Role Architecture

### Four Roles (all must be filled every section)

**Melodic Lead** (replaces singer): Must be singable. Expressive techniques create vocal quality.

**Textural Bed** (harmonic support): Sustained pads, arpeggios, drones. Felt more than heard.

**Rhythmic Anchor** (groove): Drums + bass locked together. Carries more weight in instrumentals than vocal music because no vocals to anchor attention. Must be compositionally interesting — ghost notes, fills, polyrhythm, dynamics.

**Color Elements** (spice): Field recordings, granular synthesis, effects, secondary instruments. Appear and disappear. Prevent fatigue.

### The Role-Swap Principle
WHICH instruments fill each role should change across sections. Guitar: melody in verse 1, textural bed in verse 2. Bass: anchor in verse, melodic counterpoint in chorus. Drums: timekeeping in verse, melodic lead (tuned toms) in interlude. Role-swapping creates variety from reconfiguration rather than accumulation.

---

## 9. Dynamic Range as Narrative

### The Dynamic Map (plan before writing prompts)

```
Example — post-rock crescendo:
Intro:       ░░ (2)
Verse:       ░░░ (3)
Verse 2:     ░░░░ (4)
Build:       ░░░░░░░ (7)
Breakdown:   ░ (1)       ← the valley
Build 2:     ░░░░░░░░░ (9)
Climax:      ░░░░░░░░░░ (10)
Resolution:  ░░░ (3)
```

### Rules
- Never three consecutive sections at same energy
- Climax must be preceded by the lowest post-opening point
- Each energy increase must be EARNED by preceding decrease or sustained plateau
- The second rise exceeds the first (asymmetric arc)

### Translating to Suno
Don't write "energy 7." Describe what creates it:
- Level 1-2: Single instrument, sparse, quiet, space
- Level 3-4: 2-3 instruments, gentle, clean tones
- Level 5-6: Full band restrained, some distortion, steady groove
- Level 7-8: Full power, distortion, complex drumming, multiple layers
- Level 9-10: Maximum everything, wall of sound, screaming leads

---

## 10. Track Length and Structural Density

### Duration by Genre
- Guitar virtuoso: 4-6 min (adapted verse-chorus)
- Metal instrumental: 7-9 min (multi-section suite)
- Post-rock: 8-22 min (crescendo needs patience)
- Jazz: 6-9 min (multiple solo choruses)
- Electronic club: 5-7 min (DJ-mixable)
- Electronic progressive: 8-12 min (Strobe at 10:37)
- Ambient: No upper bound (Eno 9-17 min per track)
- Film score: 2-8 min (scene-dependent)

### Critical Insight
Instrumental music succeeds at LONGER durations than vocal music because absence of lyrics requires more time for development. A 2-min instrumental feels incomplete. 5 min breathes. 10 min is a full journey.

---

## 11. Compositional Techniques for Emotional Impact

### Motif Development
- **Inversion**: Descending → ascending. Down = dissolution. Up = becoming.
- **Augmentation**: Same notes at half speed. Gravity and weight.
- **Diminution**: Same notes at double speed. Urgency and excitement.
- **Fragmentation**: Only part of the motif. Memory/echo effect.
- **Reharmonization**: Same melody, different chords. Changes meaning completely.

### Twin Guitar Architecture (or any paired leads)
Design the RELATIONSHIP as a multi-act structure:
1. **Parallel harmony** — Fixed interval (thirds, sixths, octaves). Thin Lizzy/Iron Maiden. Implies unity.
2. **Call and response** — One plays, other answers. Conversation, independence.
3. **Orbit** — One sustains, other moves around it. Stillness vs motion tension.
4. **Reunification** — Lock back into unison/harmony for climax. Reunion powerful because of separation.

### The Organic/Digital Blur (for hybrid compositions)
- Start ambiguous (can't tell guitar from synth)
- Separate so listeners identify each world
- Merge back together at the end
- Last sound being unidentifiable = conceptual resolution

### Key Modulation as Emotional Shift
- Up a half step: Classic final chorus lift
- Up a whole step: Bigger, more dramatic
- Dorian → Lydian: Darkness to brightness, brooding to wonder
- Minor → major: Sadness to triumph
- Major → minor: Subverts expectations
- Modal shift without root change: Landscape changes while you stand still

### The Mirror Ending
Return to opening elements in resolution. Same instruments, patterns, key. But listener has been changed by the journey. Same sounds, different emotional weight. Barber's Adagio does this. Creates completeness — a circle closed.

### Production Technique Translations

| Source Sound | Origin | Suno Translation |
|---|---|---|
| Vangelis Blade Runner warmth | CS-80 through Lexicon 224 | warm analog, vintage synth pads, cavernous reverb, lush |
| Boards of Canada nostalgia | VHS degradation, detuned oscillators | lo-fi warmth, slightly detuned, tape-saturated, vinyl feel, nostalgic |
| Post-rock immensity | Long reverb tails, delay chains, sparse arrangement | spacious, reverb-drenched, wide stereo, atmospheric depth, cathedral reverb |
| Modern electronic clarity | Precise transients, clean reverb, sidechain | crisp digital clarity, clean mix, punchy drums, sidechain compression |
| Zimmer cinematic weight | Simple harmony, massive orchestration, sub-bass | cinematic, epic, minimal harmony, massive orchestral, sub-bass foundation |
| Jeff Beck vocal guitar | No pick, volume swells, whammy | expressive guitar, vocal quality, legato, dynamic swells |
| Tool rhythmic complexity | Polyrhythmic patterns, odd meter, precise | intricate polyrhythmic drumming, odd-time grooves, precise and powerful |
