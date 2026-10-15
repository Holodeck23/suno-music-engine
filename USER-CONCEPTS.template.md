# User Concept Library (Template)

This is your personal scratch space. Copy this file to `USER-CONCEPTS.md` and fill it in. `USER-CONCEPTS.md` is gitignored, so your channel details stay local.

The reusable methodology lives in `SKILL.md` and `references/`. Keep channel-specific decisions here so the methodology stays portable for anyone else.

---

## How to Use This File

Four kinds of content live here:

1. **Channel Profile** — Audience, voice and visual identity the engine should hold constant across lessons.
2. **Pronunciation List** — How the TTS voice should say acronyms, product names and symbols. Keep it consistent across the channel.
3. **BGM Palette** — The bed family, keys, tempos and hero bed that define the channel's sound.
4. **Lesson Seeds and Worked Lessons** — Topics waiting to be made, and what you learned from the ones you shipped.

Delete any sections you don't need. Add new ones freely.

---

## Channel Profile

- **Channel name:**
- **Audience** (who, and what they already know):
- **Promise** (what a viewer gets from every lesson):
- **Voice ID and settings** (the ElevenLabs voice ID, model, and `--voice-settings` JSON such as stability, similarity_boost and speed):
- **Visual system** (ground colour, one accent colour, display face, monospace face):
- **Words and phrases we never use:**

---

## Pronunciation List

| Written | Spoken (narration text) | Notes |
|---|---|---|
| (e.g.) `.git` | dot git | |
| (e.g.) KV cache | K V cache | letter by letter |
| | | |

---

## BGM Palette

- **Bed family** (dark synthwave / prog-metal-electronic / post-rock / blend):
- **Master style prompt** (the DNA all beds derive from):
- **Keys and BPM range in use:**
- **Hero bed** (Suno song ID and production-folder path of the reference bed):
- **Mix settings that worked** (`mix-voice-and-bgm.py` flags: `--duck-db`, `--swell-db`, `--pocket-db`, ramps):

---

## Lesson Seed Template

Duplicate this block for each lesson idea.

### Lesson Seed: [Working Title]

- **Input type:** concept / AI release / GitHub repo
- **Thesis (one sentence):**
- **Hook's open loop:** the claim or question the Verdict will close
- **Mechanism blocks (3–4):**
- **Proof:** the real command, code path or benchmark to show
- **Primary sources:**

---

## Worked Lesson Template

Duplicate this block for each lesson you've shipped.

### Worked Lesson: [Title]

- **Manifest and production folder:**
- **Validator result and real runtime:**
- **What held retention, and where viewers dropped** (from YouTube analytics):
- **What worked / what didn't:** the gap between the plan and the result, and what to change next time
