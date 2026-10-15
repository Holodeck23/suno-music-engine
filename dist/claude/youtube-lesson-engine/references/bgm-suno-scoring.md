# BGM Scoring with Suno: Loopable Instrumental Beds Under Narration

Prompt and post-production reference for the background music in a lesson video. The output is always instrumental: a Suno style prompt plus a lyrics field that contains only bracketed metatags. Vocal songwriting is out of scope for this engine. Official Suno capabilities are kept separate from field-tested heuristics, and anything not yet auditioned is labelled as a proposal.

Read `script-and-retention-engine.md` for the segment timeline the bed has to serve (`bgm_mode`, the hook drop). Read `instrumental-video-production.md` for beat, tempo-drift and stem-analysis lessons. Read `youtube-release.md` before publishing for Suno commercial-use rights.

## Table of Contents
1. What a Narration Bed Has to Do
2. How Suno Reads Input
3. Style Prompt Construction
4. Genre Templates (85–126 BPM)
5. Metatag Structures: Hook Intro, Loop Bed, Verdict Swell
6. Preventing Vocals and Vocal-Like Textures
7. Clinical Metatags and the Copyright Filter
8. What Suno Hears vs Ignores
9. Production Descriptors That Work
10. Controlling Contrast Across a Generation
11. Suno v6 Controls for BGM
12. From Selected Take to Loopable, Voice-Safe Stem
13. Common Failure Modes and Fixes
14. Output Format and Pre-Delivery Checklist

---

## 1. What a Narration Bed Has to Do

- **Leave the voice its band.** Spoken narration carries its intelligibility in roughly **300 Hz–3 kHz**. The bed keeps that band clear: weight lives in the sub/low end (below ~250 Hz) and air in the top (above ~4 kHz). No lead melody, vocal chop or busy midrange part competes with the words.
- **Loop without an audible seam.** A 3–6 minute lesson outlasts most single takes. Generate long, steady sections and loop them in post on measured downbeats (§12).
- **Stay in 85–126 BPM.** This is the engine's working range for narrated technical content at about 150 spoken words per minute. Slower beds tend to drag under fast explanation; faster grooves race the voice. Treat these as house limits, not acoustic law.
- **Carry the lesson's arc through the edit, not the take.** The Dave Dark structure needs a building intro under the hook, a 3-second drop, a steady ducked bed through Mechanism and Proof, and a swell under the Verdict. Suno cannot place those events precisely, so generate *parts* (hook intro, loop bed, verdict swell) and let the manifest's `bgm_mode` automation shape them.

A narration bed is supposed to be flat. The "valley before the climax" and "never three sections at the same energy" rules of song composition do not apply to the loop bed. Its job is consistency, and the edit supplies the dynamics.

---

## 2. How Suno Reads Input

### Style prompt (Style/Genre field)
- A single-line, comma-separated string that sets the **global** sonic character: genre, mood, instrumentation, production, key and tempo.
- **Operational ceiling: 1,000 characters** (carried forward from the pre-v6 interface). **Target: under 300.** Suno's v6 launch materials do not restate this limit, so verify against the live UI if input is rejected or truncated.
- **Left-to-right priority.** The first terms carry the most weight. Put the dominant subgenre first.
- Never include artist names or song titles. Suno may attempt to clone instead of create.

### Lyrics field (metatags only)
- For instrumentals it holds **only** `[bracketed directions]`. Any text outside brackets may be sung.
- **Operational ceiling: ~5,000 characters**, carried forward from the pre-v6 interface. **Budget 4,000.**
- Brackets are moment-to-moment hints, and weak ones. Every scored event (intro length, build, drop, hard stop) must be measured in the selected take before the edit relies on it (§12).

---

## 3. Style Prompt Construction

### The formula for a narration bed

```
[specific subgenre], [mood pair], instrumental, no vocals, no spoken words,
[low-end instrument with character], [high/air instrument with character],
[midrange restraint terms], [production quality], [spatial term], [key], [BPM]
```

### Hard rules (carried forward)

- **Under 300 characters total.** Suno silently truncates and deprioritises terms in long prompts.
- **5–8 core descriptors.** Fewer than 4 gives you generic defaults. More than 10 sends conflicting signals and the result turns to mush.
- **Subgenres beat base genres.** "Dark synthwave" works better than "electronic", and "cinematic post-rock" better than "rock".
- **"Pop" is gravitational.** Nearly everything drifts toward pop unless excluded. Add "no pop hooks" if a bed starts sounding like a single.
- **Always include "professional studio quality" or "polished production".** Suno does not default to high quality.
- **No contradictions.** "Lo-fi polished" or "aggressive and peaceful" cancel out.
- **Always state key and BPM**, and pair the key with matching mood words. "A minor" + "brooding" aligns. "A minor" + "happy, bright" contradicts.
- **Triple-lock against vocals** (§6).

### BGM-specific rules

- **State midrange restraint explicitly:** `sparse midrange`, `no lead melody`, `no guitar solo`. These are field heuristics that bias the arrangement. They do not guarantee a clear voice band. The pocket is guaranteed by the post-production EQ and ducking in §12.
- **Place weight low and air high:** `sub-bass`, `analog sub-bass`, `airy high pads`, `high delayed guitar harmonics`.
- **Avoid descriptors that invite a midrange wall in the loop bed:** `epic`, `massive`, `wall of sound`, `soaring lead`, `choir`, `vocal chops`. Reserve size words for the verdict swell, where narration is absent or brief.
- **Prefer groove words that hold still:** `driving`, `pulsing`, `hypnotic`, `steady`.

### Key and tempo choices for the three bed families

| Family | BPM (house range) | Suggested keys | Notes |
|---|---|---|---|
| Dark synthwave | 92–118 | A minor, F# minor, G minor | Electronic music has the strongest minor-key bias of any genre |
| Prog-metal / electronic | 110–126 with `half-time feel` | E minor, D minor | The metal + electronic overlap zone sits at 128–140, so use half-time feel to stay inside 126 |
| Post-rock | 85–100 | D major, B minor, E minor | The post-rock corridor is 70–100. The engine's floor is 85 |

A track at 120 BPM can feel like 60 in half-time sections. Use `half-time feel` to get prog/metal weight without a racing pulse.

Bar length in 4/4 is `240 / BPM` seconds: 2.82 s at 85, 2.31 s at 104, 2.03 s at 118, 1.90 s at 126. Use it to size the hook build (§5), but schedule edits from the **measured** beat grid, never from the prompt BPM.

---

## 4. Genre Templates (85–126 BPM)

Each template is under 300 characters, single-line, with no artist names and no em dashes. Swap the key/BPM within the family's range. The character counts below are for the exact strings shown.

### Dark synthwave (229 chars)
```
Dark synthwave, brooding and driving, instrumental, no vocals, no spoken words, pulsing analog sub-bass, gated drum machine, airy high pads, sparse midrange, no lead melody, professional studio quality, spacious, A minor, 104 BPM
```

### Prog-metal / electronic (273 chars)
```
Progressive metal with electronic elements, tense and focused, instrumental, no vocals, no spoken words, low-tuned palm-muted guitar, deep sub-bass, glitch percussion, half-time feel, no guitar solo, sparse midrange, polished production, wide stereo field, E minor, 118 BPM
```
Distorted guitar fills the voice band by nature. Expect to attenuate the guitar stem under narration, or keep this family for `full_swell` passages and hook intros.

### Post-rock (245 chars)
```
Cinematic post-rock, patient and expansive, instrumental, no vocals, no spoken words, high delayed guitar harmonics, warm sub-bass, soft brushed drums, reverb-drenched pads, sparse midrange, professional studio quality, spacious, D major, 90 BPM
```
Post-rock guitars live in the midrange even when asked to stay high. Plan on the §12 EQ pocket.

### Fusion within the family
Put the dominant genre first, keep the production and spatial descriptors constant across every bed in a channel, and describe the *feel* of the blend: "dark synthwave with post-rock guitar textures" rather than "synth rock".

---

## 5. Metatag Structures: Hook Intro, Loop Bed, Verdict Swell

Generate the three parts as separate takes from the **same style prompt** (or the same prompt with one or two variations) so they share a palette. One compound sentence per bracket, one focus per section, clinical wording only (§7). Every bracket carries direction, and every structure ends with `[End]`.

### Hook intro: build, drop, settle (490 chars)
Serves `0:00–0:15`: a building intro under the hook narration, then the 3-second visual drop on a downbeat, then a groove that can hand off to the loop bed.
```
[Intro: instrumental only, no singing, filtered pads and sub-bass pulse, low energy, no drums, 4 bars]
[Build: drum machine enters, sixteenth-note hi-hats, filter opening, rising energy, 2 bars]
[Drop: full groove on the downbeat, kick on every beat, sub-bass locked to kick, sparse midrange, no lead melody]
[Verse: steady groove, same pattern, no fills, no new instruments]
[Verse: steady groove, same pattern, minimal variation]
[Outro: groove continues, hard stop on the downbeat]
[End]
```
At 104 BPM, 6 bars of intro and build are about 13.9 s, which puts the scored drop near the end of the hook. Suno treats bar counts as hints. **Measure where the drop actually lands** and align it in the edit (§12, "Aligning the hook drop").

### Loop bed: steady body (399 chars)
Serves `ducked` segments through Mechanism and Proof. No events, no fades, a long steady body to cut loops from.
```
[Intro: instrumental only, no singing, full groove from the first beat, no fade-in]
[Verse: steady energy, sub-bass and drum machine, airy high pads, sparse midrange, no lead melody]
[Verse: same pattern, same energy, no fills]
[Verse: same tempo and energy, pads change chord, no new instruments]
[Verse: same pattern, same energy]
[Outro: groove continues at full energy, no fade, hard stop]
[End]
```

### Verdict swell: rise and land (288 chars)
Serves the `full_swell` verdict and end card.
```
[Intro: instrumental only, no singing, sustained pads, low energy, no drums]
[Build: drums enter, energy rising, layers added one at a time]
[Chorus: full arrangement, wide stereo, sub-bass and drums at full energy, no lead melody]
[Outro: final chord, hard stop, short reverb tail]
[End]
```

### Reliable section tags (carried forward)

| Tag | Reliability | Notes |
|---|---|---|
| `[Intro]` | UNRELIABLE alone | Describe it fully, including "no fade-in" or "no drums" |
| `[Verse]` | High | Use for steady instrumental sections, with modifiers |
| `[Build]` | Moderate | Describe the crescendo mechanism |
| `[Chorus]` | High | Use for the full-energy section of a swell |
| `[Breakdown]` | High | List what is removed AND what remains |
| `[Outro]` | High | State the ending type explicitly |
| `[End]` | ESSENTIAL | Always the final tag. It stops auto-extension |

Tag stacking (3–4 tags before a section) can force stricter compliance: `[Verse | steady groove | sparse midrange | no lead melody]`.

---

## 6. Preventing Vocals and Vocal-Like Textures

Use the triple lock:
1. Style prompt: `instrumental, no vocals, no spoken words`.
2. First metatag: `instrumental only, no singing`.
3. No text outside brackets in the lyrics field.

If vocals still bleed through, add `no vocal harmonies, no humming, no choir` to the style prompt and regenerate. Vocal casting is partly random. Under narration, **vocal-like textures are as harmful as vocals**: choir pads, vocal chops, formant-swept leads and "vox" synth presets all sit in the voice band and blur the narration. Exclude them by name when they appear.

---

## 7. Clinical Metatags and the Copyright Filter

"Your lyrics contain copyrighted material" can appear on an instrumental. Suno scans the lyrics field with a **fuzzy lyric-matcher**. Vivid, poetic or title-like phrases inside brackets get matched against its corpus and rejected, even with no sung text. Confirmed triggers include similes ("hard body hits like fists"), metaphors ("weight not relief"), phrases that are song titles ("weightless", "torn to pieces") and famous quotes.

**Fix:** write metatags CLINICAL, using technique, dynamics, tempo and mix words only. Strip every simile, metaphor and lyric-like phrase. Being terse is not enough; the wording must be non-poetic. Emotion comes from the musical choices (key, mode, dynamics, technique), not from evocative words Suno cannot play. **Backstop:** flip the Instrumental toggle ON. It stops Suno scanning the lyrics box but discards the structural tags, so push the arrangement into the style prompt.

---

## 8. What Suno Hears vs Ignores

**Responds well to:** genre labels, mood words, instrument names with character descriptors, BPM, key, production quality terms, spatial terms, "instrumental / no vocals", structural tags with description.

**Partially processes:** exact durations and bar counts (approximate), dynamic contrast language, specific drum pattern descriptions.

**Largely ignores:** prompts past ~300 characters (deprioritised), abstract poetry in brackets, specific mixing dB or Hz values, references to other songs or artists, contradictory terms.

So `cut 300 Hz to 3 kHz by 4 dB` in a prompt does nothing reliable. Ask for the arrangement (`sparse midrange`, `no lead melody`) and do the EQ in post.

---

## 9. Production Descriptors That Work

**Spatial (HIGH reliability):** spacious (the most reliable separation word), wide stereo field, cavernous reverb, cathedral reverb, separated instruments, detailed mix.

**Texture (HIGH reliability):** warm analog, crisp digital clarity, tape-saturated, lo-fi tape hiss, polished radio-ready, vinyl crackle.

**Tempo feel (HIGH reliability):** driving groove, pulsing, hypnotic, relentless, half-time feel.

**Dynamic (MODERATE reliability):** crescendo, building intensity, stripped back, sparse arrangement. Use these in the hook intro and verdict swell, not in the loop bed.

**Production-sound translations useful for beds:**

| Target sound | Suno translation |
|---|---|
| Vintage analog synth warmth | warm analog, vintage synth pads, cavernous reverb, lush |
| VHS / nostalgic haze | lo-fi warmth, slightly detuned, tape-saturated, vinyl feel |
| Post-rock immensity | spacious, reverb-drenched, wide stereo, atmospheric depth |
| Modern electronic clarity | crisp digital clarity, clean mix, punchy drums, sidechain compression |
| Cinematic weight | cinematic, minimal harmony, sub-bass foundation |
| Precise prog rhythm | intricate polyrhythmic drumming, precise and powerful |

---

## 10. Controlling Contrast Across a Generation

The style prompt is **global**. Suno averages it into one feel across the whole generation and does not read "quiet opening that explodes" as a timeline. That global feel can override section brackets.

- **Neutral global + aggressive local.** Keep the style field range-declaring ("dynamic, building, sparse to full"), and put the specific dynamics and instrumentation in per-section metatags (`[Intro: no drums, filtered pads]` then `[Drop: full groove]`). Contrast through instrumentation and dynamics is reliable within one generation.
- **One generation cannot:** render a requested time signature (odd-meter prompts are unreliable; Studio's time-signature grid is an editing surface, not a generation control), lock an exact BPM ("118 BPM" is guidance, not a metronome), or force a precise key change.
- **Multi-pass Extend** is the reliable way to change key, genre or tempo. Generate Pass 1 without `[End]`, then Extend and swap in a new style prompt for Pass 2. State the preservation boundary and the new target explicitly. Use this to build a bed that changes family at a lesson's act break.
- **Modes and technique words:** naming a mode (Dorian, Phrygian, harmonic minor, Lydian) biases the colour. Naming playing or synthesis technique (palm-mute, tremolo, arpeggiated, sidechain, wavetable morphing, supersaw, portamento) changes the sound more reliably than scale names.

---

## 11. Suno v6 Controls for BGM

Suno released the v6 family on 2026-09-09 and retired all earlier generation models. Verify current labels in the live UI.

| Model | Access | Use for beds |
|---|---|---|
| **v6-mini** | All users | Fast, cheap sketches of a bed family |
| **v6-wild** | Pro and Premier | Exploring textures for a new channel palette |
| **v6** | Pro and Premier | The final hook intro, loop bed and verdict swell |

- **Variety: set to 0** for beds. Variety rewrites the style prompt, and a bed depends on authored constraints (`no vocals`, `sparse midrange`, `no lead melody`). If you raise it, inspect the rewritten prompt.
- **Max Mode** spends extra credits on consistency and fidelity. Recommend it for beds over two minutes and for keeping the three parts consistent. Standard mode is fine for sketches. Standard generations return two songs for 10 credits.
- **Atomic edits:** when one section of a good take fails (a fill, a fade), deliver `TARGET / PRESERVE / CHANGE / RESULT` as one natural-language edit instead of regenerating.
- **Audio reference / hero bed:** once one bed defines a channel's sound, use it as the audio seed for later beds. That is the most effective consistency technique available.
- **Stems:** Suno's stem export (or Demucs, §12) lets you attenuate the stem that intrudes on the voice band rather than EQ the whole mix harder.
- Proposed model and slider settings are **untested until auditioned**. Say so in the delivery, and do not assume paid features are available.

---

## 12. From Selected Take to Loopable, Voice-Safe Stem

All commands below were run against synthetic test audio with FFmpeg 6.1. The numbers are **starting points to audition**, not mastering rules.

### Preserve and measure
1. Keep the selected take's original file, its SHA256 and the Suno song ID in the lesson's production folder. Never loop or mix from a lossy re-encode of a re-encode.
2. Measure the actual duration and a beat/downbeat grid (Beat This! or librosa). **Do not trust the prompt BPM.** One take drifted from about 129 to 132 BPM, and a grid at the requested 128 BPM matched only 29% of measured kicks (`instrumental-video-production.md`).
3. Record each scored event (intro end, drop, hard stop) as **located** (time and evidence) or **absent**. A drop that does not exist is not faked: cut hard to the visual drop on a measured downbeat instead.

### Cut a loop on downbeats
Choose a steady section of at least 8 bars. Cut on two measured downbeats `A` and `B`, then join copies with a short equal-power crossfade. Each join shortens the result by the crossfade length.
```bash
ffmpeg -i bed.wav -af "atrim=start=A:end=B,asetpts=PTS-STARTPTS" body.wav
ffmpeg -i body.wav -i body.wav -filter_complex "[0][1]acrossfade=d=0.5:c1=qsin:c2=qsin" loop2.wav
```
Use roughly one beat for `d` (0.5 s at 120 BPM). Long reverb tails make hard (uncrossfaded) loops audibly drop out. Fewer, longer loops (made with Extend) hide seams better than many short ones. **Listen to every seam.** A level meter cannot judge a groove hiccup.

### Carve the voice pocket
A broad, gentle bell centred on the voice band. 950 Hz is the geometric centre of 300 Hz–3 kHz, and 3.3 octaves spans it.
```bash
ffmpeg -i bed.wav -af "equalizer=f=950:t=o:w=3.3:g=-4" bed_eq.wav
```
If one stem (lead synth, distorted guitar) still masks the voice, attenuate that stem before the EQ rather than deepening the cut.

### Duck under the narration
`sidechaincompress` **stops when its key input ends**. In testing, an unpadded 12 s narration key truncated a 20 s bed to 12 s. Pad the key with `apad`.
```bash
ffmpeg -i bed_eq.wav -i narration.wav -filter_complex \
 "[1:a]aformat=channel_layouts=stereo,apad,asplit=2[key][voice]; \
  [0:a][key]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[duck]; \
  [duck][voice]amix=inputs=2:duration=first:normalize=0[mix]" \
 -map "[mix]" premaster.wav
```
`amix` divides input levels unless `normalize=0` is set. These settings pulled the synthetic bed about 19 dB down while the voice was active. Tune `threshold` to the real narration level.

### Automate `bgm_mode` per segment
Segment boundaries come from the rendered TTS timeline (`script-and-retention-engine.md`). Apply bed gain per segment with short ramps. This expression ducks by 12 dB between 3 s and 9 s with 0.4 s ramps (verified at exactly −12 dB inside the window):
```bash
ffmpeg -i bed.wav -af "volume='1-(1-pow(10,-12/20))*min(1,max(0,min((t-3)/0.4,(9-t)/0.4)))':eval=frame" bed_auto.wav
```
Generate one such term per `ducked` span from the manifest timeline. `full_swell` spans stay at unity, and the sidechain still protects any words inside them. Land ramps on downbeats where the timeline allows.

### Hit the loudness target
YouTube turns loud uploads down toward a reference near −14 LUFS. That figure is widely measured, not an official specification. Master the final mix to **−14 LUFS integrated, true peak at or below −1 dBTP**. Single-pass `loudnorm` missed its −14 target by 1.9 LU on the test mix, while measuring with `ebur128` and applying linear gain landed at −14.0:
```bash
ffmpeg -nostats -i premaster.wav -af ebur128 -f null -   # read "I:" under Integrated loudness
ffmpeg -i premaster.wav -af "volume=<-14 minus measured>dB" master.wav
ffmpeg -nostats -i master.wav -af ebur128=peak=true -f null -   # verify I and true peak
```
If the true peak exceeds −1 dBTP after the gain, add `alimiter`, then measure again. As a starting balance, sit the ducked bed roughly 10–15 LU below the narration's short-term loudness and adjust by ear on the actual voice.

### Aligning the hook drop
Let `D` be the measured drop downbeat in the hook-intro stem, and `H` the timeline time where the hook narration plus its pause ends (the drop moment, at most 12 s, so that the 3 s drop finishes by 0:15). Offset the stem by `D − H`: trim that much from its head when positive. When negative, the stem's build is too short. Pick another take or extend the intro rather than starting the lesson on silence. The visual drop is scheduled at `H` and lasts 3.0 s.

---

## 13. Common Failure Modes and Fixes

| Failure | Fix |
|---|---|
| Vocals, humming or choir bleed in | Triple lock (§6), exclude by name, regenerate; Instrumental toggle as backstop |
| "Copyrighted material" on an instrumental | Rewrite metatags clinical (§7) |
| A lead melody fights the narration | `no lead melody`; attenuate that stem; EQ pocket (§12) |
| Distorted guitar wall in the voice band | Half-time, low-tuned, `sparse midrange`; keep for swells; attenuate the stem under words |
| Bed fades in or out | Loop from the steady body. Ignore the generated intro and outro |
| Scored drop absent or late | Measure; offset the stem (§12); otherwise hard cut on a measured downbeat |
| Tempo drifts across the take | Loop from a stable region; schedule from the measured grid |
| Bed drifts toward pop | `no pop hooks`; a more specific subgenre first |
| Bed too busy to sit under speech | Fewer descriptors; remove size words; `minimal arrangement` |
| Seams audible | Longer loops via Extend; crossfade about one beat; cut only on measured downbeats |

---

## 14. Output Format and Pre-Delivery Checklist

Deliver each part as one block the user can paste directly into Suno:

```
TITLE: [bed name]
ROLE: hook-intro | loop-bed | verdict-swell
STYLE PROMPT:
[single-line comma-separated style string]
METATAGS:
[bracketed metatags only, ending with [End]]
MODEL / CONTROLS (proposed, untested until auditioned): [model], Variety 0, Max Mode [yes/no]
COUNTS: style [N] chars, metatags [M] chars
```

Before delivering, verify and state the counts:
1. Style prompt under 300 characters (ceiling 1,000). State the count.
2. Metatags under 4,000 characters (ceiling 5,000). State the count.
3. `instrumental, no vocals, no spoken words` is in the style prompt AND `instrumental only, no singing` is in the first metatag.
4. Key and BPM are present, BPM is within 85–126, and the mood words match the key.
5. Midrange restraint is stated (`sparse midrange` / `no lead melody`) and the §12 pocket plan is noted.
6. Every bracket contains direction, all of it clinical (no simile, metaphor or lyric-like phrase). The final tag is `[End]`.
7. No artist or song names, no em dashes, and the style prompt is single-line and comma-separated.

If any check fails, fix it and re-count before delivering.
