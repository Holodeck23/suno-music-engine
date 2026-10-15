---
identity:
  name: youtube-lesson-engine
  description:
    full: >
      Turn AI and tech lessons, AI releases, news and GitHub architectures into high-retention faceless
      YouTube videos scored with custom Suno background music. Use for lesson scripts, the Dave Dark
      hook/mechanism/proof/verdict structure, lesson-manifest.json cue files, TTS narration timing and
      code or architecture visuals. Also use for loopable instrumental Suno BGM (dark synthwave,
      prog-metal/electronic, post-rock at 85-126 BPM) that leaves room for narration, ducking and
      loudness, music-driven and kinetic-type animation, deterministic browser/Blender rendering,
      export verification, and YouTube titles, thumbnails, chapters, rights and AI disclosure. Ships
      ElevenLabs TTS with word timestamps, BGM beat extraction and a timeline-driven ducking mixer.
      Replaces suno-music-engine.
activation:
  triggers: []
  auto_invoke: true
  user_invoke: true
  context_isolation: false
dependencies:
  mcp: []
  bash: []
  env: []
resources:
  scripts: []
  references: []
  assets: []
behavior:
  dynamic_injections: []
constraints:
  max_body_lines: 500
  recommended_body_tokens: 5000
---

# YouTube Lesson Engine

The master orchestrator for a programmatic pipeline that turns a technical concept, an AI release or a GitHub repository into a 3–6 minute faceless YouTube lesson. The six steps run in order: a researched script in the Dave Dark structure, compiled into a strict `lesson-manifest.json`; a custom Suno bed; narration with word-level timing; a ducked mix; music-video-grade programmatic visuals; and YouTube packaging.

## Routing: What Does The User Need?

Most lessons pass through every step in order. A request can also enter at any step.

| User Intent | Step | Primary Reference / Tool |
|---|---|---|
| "Turn this topic / release / repo into a video" | **All six, in order** | This file §1 |
| "Write the script / the hook / an outline", "build or check the manifest" | **1. Topic → manifest** | `references/script-and-retention-engine.md` + `scripts/validate-lesson-manifest.py` |
| "Make background music / a Suno prompt for this lesson", "edit one part of a BGM take" | **2. BGM** | `references/bgm-suno-scoring.md` + this file §4 |
| "Narrate it / generate the voice / align my voiceover / sync highlights to words" | **3. Voice and timing** | `scripts/generate-tts-and-cues.py` + `scripts/extract-video-timing.py` |
| "Mix the voice and music / duck the bed / master the audio" | **4. Audio mix** | `scripts/mix-voice-and-bgm.py` + `references/bgm-suno-scoring.md` §12 |
| "Animate / render the lesson", "this draft looks cheap", "match this reference" | **5. Render and verify** | `references/visual-lesson-production.md` + `references/video-direction-and-quality.md` |
| "Title / thumbnail / chapters / description / pinned comment / rights / AI disclosure" | **6. Package and release** | `references/youtube-release.md` |

Always read the relevant reference files BEFORE producing. They hold the detail: structure budgets, the manifest contract, Suno prompt rules, mixing levels, rendering lessons, legibility rules and verification steps.

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

**Pipeline outputs** (state the measured values):
1. `generate-tts-and-cues.py` ran on the validated manifest. For local audio, state the heard/total word count and spot-check interpolated words.
2. `bgm.hookDrop.error` is 0 after applying the suggested offset, or the drop is a deliberate hard cut on a measured downbeat.
3. The `mix-voice-and-bgm.py` master reports about −14 LUFS and a true peak at or below −1 dBTP. A printed level is not a listening check; say whether the mix was actually heard.
4. The export passes the checks in `visual-lesson-production.md` Part 1, including `freezedetect` and every mobile-legibility rule.

**Publishing copy** uses `references/youtube-release.md` instead. Do not apply composition tags or field limits to titles and descriptions.

If any check fails, fix it and re-check BEFORE delivering. Do not deliver and apologise afterwards.

---

## §1: THE SIX-STEP PIPELINE

**Step 1: Topic or repository analysis → `lesson-manifest.json`.** Identify the input type and write a one-sentence thesis. Research primary sources: for a repository, read and run the code paths. Separate fact from inference and date-stamp perishable claims. Write the script in the Dave Dark structure (§2) for the ear, compile it into the manifest, and run `scripts/validate-lesson-manifest.py --strict` (`script-and-retention-engine.md`).

**Step 2: BGM selection and prompting.** Generate three parts from one palette (hook intro, loop bed, verdict swell) in dark synthwave, prog-metal/electronic or post-rock at 85–126 BPM, with the 300 Hz–3 kHz band left for the voice. Select the takes, keep their hashes and Suno IDs, and cut loops on measured downbeats (`bgm-suno-scoring.md`).

**Step 3: Voice synthesis and timestamp alignment.**
```bash
ELEVENLABS_API_KEY=... python3 scripts/generate-tts-and-cues.py lesson-manifest.json --out-dir build --provider elevenlabs
#   or: --provider local-audio --audio-file voiceover.wav   (Whisper alignment; add --restitch to apply the pauses)
uv run --python 3.12 --with librosa python scripts/extract-video-timing.py bgm.wav build/bgm-timing.json \
    --beats --merge-into build/resolved-timeline.json
#   then rerun with --bgm-offset <bgm.hookDrop.suggestedOffset> --force-merge to land a downbeat on the drop
```
The rendered narration is the timing authority. The timeline holds word and trigger times, gapless slots, transitions, `camera_move` events and chapters.

**Step 4: Audio mixing.**
```bash
python3 scripts/mix-voice-and-bgm.py build/master-narration.wav bgm.wav build/resolved-timeline.json build/master-audio.wav
```
The voice is high-passed at 80 Hz, lightly presence-lifted and set to −14 LUFS. The bed sits at −18 dB with a −3 dB pocket at 1.5 kHz, fully ducked 0.3 s before speech, and rises to −2 dB only in transitions, the intro and the outro, so it never pumps between words. The master lands at −14 LUFS under a −1 dBTP ceiling.

**Step 5: Programmatic video rendering and quality verification.** Render the four visual states from the timeline as pure functions of absolute time, at a locked frame rate. Pilot the Hook, the drop and one Mechanism block first. Enforce the mobile-legibility rules, review contact sheets and real-time playback, run `freezedetect`, then mux `master-audio.wav` and verify the export (`visual-lesson-production.md`, `video-direction-and-quality.md`).

**Step 6: YouTube metadata and packaging.** Write a curiosity-gap title the video pays off, a three-word high-contrast thumbnail, the description with `chapters.txt` and dated sources, and a pinned comment. Set the AI disclosure correctly: synthetic narration requires it (`youtube-release.md`). A finished render is not a publication.

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

## §3: THE MANIFEST CONTRACT AND VISUAL STATES (SUMMARY)

`lesson-manifest.json` holds `title`, `bgm_track`, `voice_id` and `segments[]`. Each segment has `id` (`seg_<NN>_<phase>[_<slug>]`), `narration`, `visual_state`, `bgm_mode` (`ducked | full_swell`) and `visual_payload` (`headline`, `code_snippet`, `diagram_nodes`, `highlight_triggers[]`). Triggers pair an exact narration word with an action: `reveal_line_<n>`, `highlight_line_<n>`, `reveal_node_<n>`, `highlight_node_<n>`, `show_headline` or `drop`. Code lines are limited to 45 columns.

| Visual state | What renders |
|---|---|
| `vibe_drop` | Full-screen audio-reactive visualizer driven by the bed; transitions (3–5 s), intros and the 3-second hook drop |
| `code_focus` | Visualizer at 15–20% opacity behind dark-mode, syntax-highlighted code or terminal output revealed on word timestamps |
| `architecture_graph` | Node/pipeline diagram whose active components glow and pulse on their spoken trigger words |
| `artifact_pan` | Dark-mode viewport over a real README, release note or benchmark chart, with zoom and highlight boxes on narration cues |

Full field rules, trigger semantics and validator checks are in `references/script-and-retention-engine.md` §5. The schema is `references/lesson-manifest.schema.json`; `references/lesson-manifest.example.json` is a complete valid lesson.

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

**User provides a topic, release or repo →** Confirm the input and audience → Step 1 → Propose the thesis and Hook → Deliver the script and a validated manifest → Continue through Steps 2–6 as authorized

**User wants the script only →** Apply §2 → Deliver the narration by phase with word counts and a runtime estimate

**User provides a manifest →** Run the validator with `--strict` → Fix or explain each finding → Re-deliver the complete manifest, not fragments

**User wants BGM →** Read bgm-suno-scoring → Pick the family, key and BPM → Deliver the hook intro, loop bed and verdict swell with stated counts

**User has narration or BGM takes →** Run Step 3 (generate-tts-and-cues, extract-video-timing with --merge-into) → Step 4 (mix-voice-and-bgm) → Report measured loudness, the drop alignment and anything interpolated

**User wants the video →** Read visual-lesson-production and the direction guide → Pilot the Hook, drop and one Mechanism block → Expand within the authorized direction → Verify the export

**User wants to release →** Read youtube-release → Deliver the title, thumbnail brief, description with chapters, and pinned comment → Explain rights and AI disclosure without claiming publication

**User wants to iterate →** Always re-deliver the COMPLETE artifact (the whole manifest, or the whole style prompt plus metatags), so it can be pasted or run directly

---

## Reference Files

- **`references/script-and-retention-engine.md`** — Intake and research rules, the Dave Dark structure with word budgets, retention mechanics, narration for TTS, the exact `lesson-manifest.json` contract with trigger semantics and validator rules, and manifest-to-timeline compilation. **Read before any script or manifest work.**
- **`references/lesson-manifest.schema.json`** / **`references/lesson-manifest.example.json`** — The machine-readable schema, and a complete valid example lesson.
- **`references/bgm-suno-scoring.md`** — Instrumental Suno prompt formatting for loopable narration beds: style formula, genre templates (85–126 BPM), hook-intro, loop-bed and verdict-swell metatags, vocal prevention, clinical metatags, v6 controls, and the mixer's levels with tested manual FFmpeg recipes. **Read before any BGM work.**
- **`references/visual-lesson-production.md`** — The lesson renderer (the four visual states, render contract, transitions, camera moves, export checks), plus every retained timing, design, rendering, music-driven-motion, world-building and renderer lesson from the music-video productions.
- **`references/video-direction-and-quality.md`** — Mobile legibility (minimum sizes, 45-column code, a change every 6–8 s), close reference study, motion proofs, renderer provenance, rejection handling, camera-jump prevention and bounded iteration.
- **`references/youtube-release.md`** — Curiosity-gap titles, three-word thumbnails, chapters from the timeline, description and pinned-comment templates, Suno commercial-use rights by plan at creation time, and YouTube AI disclosure for synthetic narration and AI music.
- **`docs/video-capabilities.md`** — What the bundled scripts do, what remains project-specific, and the recorded production outcomes.
- **Scripts:** `validate-lesson-manifest.py` (manifest rules), `generate-tts-and-cues.py` (ElevenLabs or local narration → `master-narration.wav`, `resolved-timeline.json`, `chapters.txt`), `extract-video-timing.py` (embedded cues; `--beats` for BGM beats, envelopes and the drop offset), `mix-voice-and-bgm.py` (timeline-driven ducking and mastering), `align-lyric-words.py` (Whisper word alignment shared with local narration).
