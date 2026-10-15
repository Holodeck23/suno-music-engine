---
name: youtube-lesson-engine
description: >
  Turn AI and tech lessons, AI releases, news and GitHub architectures into high-retention faceless YouTube videos scored with custom Suno background music. Use for lesson scripts, the Dave Dark
  hook/mechanism/proof/verdict structure, lesson-manifest.json cue files, TTS narration timing and code or architecture visuals. Also use for loopable instrumental Suno BGM (dark synthwave,
  prog-metal/electronic, post-rock at 85-126 BPM) that leaves room for narration, ducking and loudness, music-driven and kinetic-type animation, deterministic browser/Blender rendering, export
  verification, and YouTube rights and AI disclosure. Replaces suno-music-engine.
---

# YouTube Lesson Engine

A programmatic pipeline that turns a technical concept, an AI release or a GitHub repository into a 3–6 minute faceless YouTube lesson: a researched script in the Dave Dark structure, compiled into a strict `lesson-manifest.json`, narrated by TTS, scored with a custom Suno background bed, and rendered with music-video-grade visuals.

## Routing: What Does The User Need?

Read the request and route to the appropriate mode. Most lessons pass through several modes in order.

| User Intent | Mode | Primary Reference |
|---|---|---|
| "Turn this topic / release / repo into a video" | **LESSON PIPELINE** | This file §1, then each mode below |
| "Write the script / the hook / an outline for this lesson" | **SCRIPT** | `references/script-and-retention-engine.md` §1–4 |
| "Build / compile / check the manifest or cue sheet" | **MANIFEST** | `references/script-and-retention-engine.md` §5 + `scripts/validate-lesson-manifest.py` |
| "Make background music / a Suno prompt for this lesson" | **BGM SCORING** | `references/bgm-suno-scoring.md` |
| "Loop, duck, EQ or master the music under the narration" | **BGM POST** | `references/bgm-suno-scoring.md` §12 |
| "Time the narration / sync the highlights to the words" | **TIMING** | `references/script-and-retention-engine.md` §6 + `references/music-video-production.md` |
| "Animate / render the lesson visuals" | **VISUALS** | `references/music-video-production.md` + `references/instrumental-video-production.md` |
| "This draft looks cheap / match this reference / make it feel alive" | **DIRECTION** | `references/video-direction-and-quality.md` + `references/music-video-production.md` |
| "Edit one part of a BGM take" | **V6 EDITING** | This file §4 + `references/bgm-suno-scoring.md` §11 |
| "Title / description / can I use this Suno track / AI disclosure" | **RELEASE** | `references/youtube-release.md` |

Always read the relevant reference files BEFORE producing. They hold the detail: structure budgets, the manifest contract, Suno prompt rules, mixing commands, rendering lessons and verification steps.

---

## MANDATORY PRE-DELIVERY SELF-CHECK

**Scripts and manifests:**
1. Run `python3 scripts/validate-lesson-manifest.py MANIFEST --strict` and fix every error and warning. State the result and the runtime estimate.
2. The Hook states the problem in its first words, with no greeting or channel filler.
3. The Proof shows real output or real code from a cited source. Nothing is staged or invented.
4. Perishable claims (prices, limits, versions, rankings) carry the date they were checked in the research notes. Inferences are labelled as inferences.

**Suno BGM prompts** (state the verified counts in the delivery so the user can audit):
1. Style prompt under 300 characters (operational ceiling 1,000). State the count.
2. Metatags under 4,000 characters (operational ceiling 5,000). State the count.
3. `instrumental, no vocals, no spoken words` is in the style prompt AND `instrumental only, no singing` is in the first metatag. There is no text outside brackets.
4. Key and BPM are stated, BPM is within 85–126, and the mood words match the key.
5. Midrange restraint is stated (`sparse midrange`, `no lead melody`), with the post-production voice pocket noted.
6. Every bracket carries clinical direction (technique, dynamics, tempo, mix). Suno's copyright filter fuzzy-matches poetic or title-like phrases even inside brackets. The final tag is `[End]`.
7. No artist or song names, no em dashes, and the style prompt is single-line and comma-separated.

The 1,000 / 5,000-character ceilings and the 8-minute single-generation length are carried forward from the pre-v6 interface. Treat them as conservative working limits and verify against the live UI if a field rejects or truncates input.

**Publishing copy** uses `references/youtube-release.md` instead. Do not apply composition tags or field limits to titles and descriptions.

If any check fails, fix it and re-check BEFORE delivering. Do not deliver and apologise afterwards.

---

## §1: THE LESSON PIPELINE

1. **Intake.** Identify the input type (concept, AI release, GitHub repo) and write a one-sentence thesis: the problem or shift a viewer should understand by 0:15.
2. **Research.** Use primary sources. For a repository, read the code paths and run them. Separate documented fact from inference and date-stamp perishable claims (`script-and-retention-engine.md` §1).
3. **Script.** Write in the Dave Dark structure (§2) with narration written for the ear (`script-and-retention-engine.md` §2–4).
4. **Compile and validate.** Emit `lesson-manifest.json` exactly as specified (`script-and-retention-engine.md` §5), then run the validator with `--strict`.
5. **Score.** Generate three BGM parts from one palette (hook intro, loop bed, verdict swell). Select the takes, measure their beat grids and the actual drop, cut loops on downbeats and carve the 300 Hz–3 kHz voice pocket (`bgm-suno-scoring.md`).
6. **Narrate and time.** Render TTS with the manifest's `voice_id`. The rendered narration audio is the timing authority. Resolve every highlight trigger to its spoken word's start time (`script-and-retention-engine.md` §6).
7. **Visualise.** Pilot the Hook plus one Mechanism block at full quality before the whole lesson. Every frame evaluates from absolute time, and review uses contact sheets plus motion playback (`music-video-production.md`).
8. **Mix and master.** Apply `bgm_mode` automation and sidechain ducking, align the hook drop to the measured downbeat, and master to −14 LUFS integrated with true peak at or below −1 dBTP (`bgm-suno-scoring.md` §12).
9. **Export and verify.** Check dimensions, frame rate, audio/video duration, decode success and representative frames, and bind the output hash to the manifest, narration and BGM hashes (`music-video-production.md`).
10. **Release.** Title, description, Suno commercial-use rights and AI disclosure (`youtube-release.md`). A finished render is not a publication.

### Where the work lives

Keep two homes and never mix them. Renderer code lives in its own version-controlled repository. Everything a lesson makes or consumes lives in one durable production folder per lesson: research notes, script, manifest, narration audio and hashes, BGM takes and hashes, analysis, timing, every render pass, contact sheets and the production log. Copy renders out of any tool's scratch directory into the production folder in the same turn. Machine-specific workspace rules take precedence over this paragraph.

---

## §2: THE DAVE DARK STRUCTURE

| Phase | Time / size | Job | Visual | BGM |
|---|---|---|---|---|
| **The Hook** | `0:00–0:15`; ≤ 30 words at 150 wpm plus a 3 s drop | State the architectural problem or industry shift immediately. Zero "hey guys" fluff | `vibe_drop`, ending on the 3-second visual drop | `full_swell`: a building intro, then the drop |
| **The Mechanism** | 3–4 concrete technical blocks | One idea per block: claim, evidence, visual payoff on the word | `architecture_graph`, `code_focus` | `ducked` |
| **The Proof / Code** | 30–90 s | The actual implementation, terminal flow or benchmark reality | `code_focus`, `artifact_pan` | `ducked` |
| **The Verdict** | 20–40 s | A high-signal takeaway that closes the Hook's open loop | `vibe_drop`, `artifact_pan` | `full_swell` |

Whole lesson: 3–6 minutes, about 450–900 narrated words at 150 wpm. Something on screen changes at least every 20–40 seconds (a segment change or a highlight trigger). That is a diagnostic, not a quota.

---

## §3: THE MANIFEST CONTRACT (SUMMARY)

`lesson-manifest.json` holds `title`, `bgm_track`, `voice_id` and `segments[]`. Each segment has `id` (`seg_<NN>_<phase>[_<slug>]`), `narration`, `visual_state` (`vibe_drop | code_focus | architecture_graph | artifact_pan`), `bgm_mode` (`ducked | full_swell`) and `visual_payload` (`headline`, `code_snippet`, `diagram_nodes`, `highlight_triggers[]`). Triggers pair an exact narration word with an action: `reveal_line_<n>`, `highlight_line_<n>`, `reveal_node_<n>`, `highlight_node_<n>`, `show_headline` or `drop`.

The full field rules, trigger semantics and validator checks are in `references/script-and-retention-engine.md` §5. The machine-readable schema is `references/lesson-manifest.schema.json`, and `references/lesson-manifest.example.json` is a complete valid lesson to copy from.

---

## §4: SUNO v6 FOR BACKGROUND MUSIC

Suno released the v6 family on 2026-09-09 and retired all earlier generation models.

| Model | Access | Best use for beds |
|---|---|---|
| **v6-mini** | All users | Fast, inexpensive sketches of a bed family |
| **v6-wild** | Pro and Premier | Exploring a new channel palette: less predictable, more textured |
| **v6** | Pro and Premier | Final hook intro, loop bed and verdict swell |

- **Variety at 0** keeps authored constraints (`no vocals`, `sparse midrange`, `no lead melody`) intact. If it is raised, inspect the rewritten prompt.
- **Max Mode** spends additional credits on consistency and fidelity. Recommend it for beds over two minutes and for keeping the three parts consistent.
- **Multiple inputs:** v6 accepts Suno songs, playlists, audio uploads, images and video in one Simple Mode request. Give each source a role (preserve, extract, transform, ignore, atmosphere only) and timestamps where available. Keep ownership and authorization explicit.
- **Hero bed:** once one bed defines the channel's sound, use it as the audio reference for later beds.

### Natural-Language Editing

V6 can change one section while preserving the rest. Deliver an edit instruction, not a regeneration prompt:

```text
TARGET: [section or timestamp]
PRESERVE: [groove, tempo, instrumentation, mix and sections that must not change]
CHANGE: [one concrete musical transformation]
RESULT: [how the edited section should enter, develop and reconnect]
```

Keep each edit atomic. Sequence independent changes as separate passes, so a failed edit cannot destroy approved material.

For every BGM delivery, state the selected model and a concise proposed control preset if the user has those controls. Label proposed settings as untested until auditioned, and do not assume paid features are available.

---

## §5: HONEST STATE REPORTING

Distinguish and report only the states actually reached: script drafted, manifest valid, narration rendered and timed, BGM selected and aligned, pilot rendered, motion and audio reviewed, full lesson exported and verified, user accepted, published. Do not claim to have listened when only metadata or a waveform was inspected. Technical verification, the agent's aesthetic assessment and human acceptance are separate records. A liked pilot does not accept a later full export.

---

## User Interaction Flow

**User provides a topic, release or repo →** Confirm the input and the audience → Research from primary sources → Propose the thesis and Hook → Deliver the script and a validated manifest

**User wants the script only →** Apply §2 → Deliver the narration by phase with word counts and a runtime estimate

**User provides a manifest →** Run the validator with `--strict` → Fix or explain each finding → Re-deliver the complete manifest, not fragments

**User wants BGM →** Read bgm-suno-scoring → Pick the family, key and BPM → Deliver the hook intro, loop bed and verdict swell with stated counts

**User has selected BGM takes →** Measure the grid and the drop → Cut loops, carve the pocket and set the ducking → Report the measured facts and the commands used

**User wants the video →** Read music-video-production and the relevant direction guide → Time the narration → Pilot the Hook plus one block → Expand within the authorized direction and verify the export

**User wants to release →** Read youtube-release → Deliver the title and description → Explain rights and AI disclosure without claiming publication

**User wants to iterate →** Always re-deliver the COMPLETE artifact (the whole manifest, or the whole style prompt plus metatags), so it can be pasted or run directly

---

## Reference Files

- **`references/script-and-retention-engine.md`** — Intake and research rules, the Dave Dark structure with word budgets, retention mechanics, narration for TTS, the exact `lesson-manifest.json` contract with trigger semantics and validator rules, and manifest-to-timeline compilation. **Read before any script or manifest work.**
- **`references/lesson-manifest.schema.json`** / **`references/lesson-manifest.example.json`** — The machine-readable schema, and a complete valid example lesson.
- **`references/bgm-suno-scoring.md`** — Instrumental Suno prompt formatting for loopable narration beds: style formula, genre templates (85–126 BPM), hook-intro, loop-bed and verdict-swell metatags, vocal prevention, clinical metatags, v6 controls, and tested FFmpeg loop, EQ-pocket, ducking and loudness recipes. **Read before any BGM work.**
- **`references/music-video-production.md`** — Timing authority, word-level timing, scored-event measurement, design systems, pilots, style-frame and HDR legibility lessons, light-ground grading, deterministic rendering, chunked export, delivery size, verification, and the narrative-continuity, world-system and renderer lessons. Includes how each applies to lesson videos.
- **`references/instrumental-video-production.md`** — Form/phrase/beat/texture mapping, stem leakage, tempo drift, the offline feature contract, musical time and music-driven motion. Read when the BGM drives the visuals.
- **`references/video-direction-and-quality.md`** — Close reference study, motion proofs, renderer provenance, rejection handling, camera-jump prevention and bounded iteration. Read for ambitious references or a draft judged cheap.
- **`references/youtube-release.md`** — Titles, descriptions, channel bios, Suno commercial-use rights by plan at creation time, and YouTube AI disclosure.
- **`docs/video-capabilities.md`** — What the bundled helpers do, what remains project-specific, and the recorded production outcomes.
- **`scripts/validate-lesson-manifest.py`**, **`scripts/extract-video-timing.py`**, **`scripts/align-lyric-words.py`** — Manifest validation, embedded-cue extraction with audio identity, and Whisper word alignment (lyrics or narration).
