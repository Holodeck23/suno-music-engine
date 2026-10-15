# YouTube Lesson Engine

A platform-agnostic Agent Skill that turns AI and tech lessons, AI releases, news and GitHub architectures into high-retention, faceless YouTube videos scored with custom Suno background music and music-video-grade visuals. The portable definition builds adapters for Claude Code and OpenAI Codex and orchestrates six steps:

1. **Topic → manifest** — Research primary sources, write in the Dave Dark structure (a 15-second Hook with zero fluff, 3–4 Mechanism blocks, real Proof, a high-signal Verdict) and compile a validated `lesson-manifest.json`
2. **BGM** — Loopable instrumental Suno beds (dark synthwave, prog-metal/electronic, post-rock, 85–126 BPM) that leave the voice its 300 Hz–3 kHz band
3. **Voice and timing** — ElevenLabs narration with word timestamps, or a local voiceover aligned with Whisper; BGM beats and the hook-drop offset merged into one resolved timeline
4. **Mix** — Timeline-driven ducking that never pumps between words, a vocal pocket, −14 LUFS mastering
5. **Render and verify** — Four programmatic visual states (`vibe_drop`, `code_focus`, `architecture_graph`, `artifact_pan`) on tested rendering, determinism, legibility and export-verification lessons
6. **Package** — Curiosity-gap titles, three-word thumbnails, chapters from the timeline, pinned comments, Suno rights and AI disclosure

This engine grew out of `suno-music-engine`. It keeps the instrumental Suno knowledge and every video-production lesson. The vocal songwriting, album and personal-translation modes were retired; they remain in the `main` branch history.

---

## Quick start

```bash
# 1. Validate the manifest (Python 3.8+, standard library only)
python3 scripts/validate-lesson-manifest.py lesson-manifest.json --strict

# 3. Narrate and compile the timeline (or --provider local-audio --audio-file voiceover.wav)
ELEVENLABS_API_KEY=... python3 scripts/generate-tts-and-cues.py lesson-manifest.json \
    --out-dir build --provider elevenlabs

#    Merge the bed's beats; rerun with the suggested --bgm-offset to land the hook drop on a downbeat
uv run --python 3.12 --with librosa python scripts/extract-video-timing.py bgm.wav build/bgm-timing.json \
    --beats --merge-into build/resolved-timeline.json

# 4. Mix and master
python3 scripts/mix-voice-and-bgm.py build/master-narration.wav bgm.wav \
    build/resolved-timeline.json build/master-audio.wav
```

Requires FFmpeg and FFprobe on PATH. `references/lesson-manifest.example.json` is a complete 3-minute lesson on Git's object database, with real terminal output in its Proof segments.

## Install with Polyskill

```bash
git clone https://github.com/Holodeck23/suno-music-engine.git
cd suno-music-engine
polyskill validate
polyskill install
```

By default, Polyskill installs the generated adapters to `~/.claude/skills/youtube-lesson-engine` and `~/.agents/skills/youtube-lesson-engine`. Use `polyskill install --target claude` or `polyskill install --target codex` for one runtime.

Copy `USER-CONCEPTS.template.md` to `USER-CONCEPTS.md` inside the installed skill to keep a private channel profile, pronunciation list and series ideas. That file is ignored by Git.

---

## Structure

```
youtube-lesson-engine/
├── definition.md                          ← Portable source of truth: the six-step orchestrator
├── polyskill.yaml                         ← Claude and Codex build targets
├── README.md                              ← This file
├── USER-CONCEPTS.template.md              ← Template for a private channel profile
├── references/
│   ├── script-and-retention-engine.md     ← Dave Dark structure, retention, TTS writing, manifest contract, timeline
│   ├── lesson-manifest.schema.json        ← Machine-readable manifest schema
│   ├── lesson-manifest.example.json       ← Complete valid example lesson
│   ├── bgm-suno-scoring.md                ← Instrumental Suno beds, loops, voice pocket, mixer levels
│   ├── visual-lesson-production.md        ← Four visual states + every timing, rendering and world-building lesson
│   ├── video-direction-and-quality.md     ← Mobile legibility, reference craft, motion proofs, camera jumps
│   └── youtube-release.md                 ← Titles, thumbnails, chapters, pinned comments, rights, AI disclosure
├── scripts/
│   ├── validate-lesson-manifest.py         ← Schema + Dave Dark structure validator
│   ├── generate-tts-and-cues.py            ← ElevenLabs / local narration → master-narration.wav + resolved-timeline.json
│   ├── extract-video-timing.py             ← Embedded cues, audio identity; --beats for BGM beats and the drop offset
│   ├── mix-voice-and-bgm.py                ← Timeline-driven ducking and mastering → master-audio.wav
│   └── align-lyric-words.py                ← Whisper word alignment (lyrics or narration)
├── docs/
│   ├── video-capabilities.md              ← Coverage and implementation inventory
│   └── v6-upgrade.md                      ← Suno v6 audit
└── dist/
    ├── claude/youtube-lesson-engine/      ← Generated Claude Code adapter
    └── codex/youtube-lesson-engine/       ← Generated OpenAI Codex adapter
```

The GitHub repository keeps its original name, `suno-music-engine`. The skill it builds is `youtube-lesson-engine`.

---

## Reusable vs Personal

The methodology in `definition.md` and `references/` is generic. Generated runtime files are build artifacts: edit the portable source and rebuild rather than hand-editing `dist/`.

Lesson media (narration, BGM takes, renders) belongs in a durable production folder per lesson, never in this repository. `USER-CONCEPTS.md` is your private scratch space for a channel profile, pronunciations and series ideas.

---

## Usage Examples

- "Turn this GitHub repo into a 5-minute lesson: script, manifest and BGM"
- "Write a Dave Dark hook for the new model release, no fluff"
- "Validate my lesson-manifest.json and fix the trigger words"
- "Give me a dark synthwave loop bed at 104 BPM that sits under narration"
- "Narrate this manifest with my ElevenLabs voice and mix it under the synthwave bed"
- "Align my recorded voiceover to the manifest and give me the chapters"
- "Pilot the hook and first mechanism block as a rendered video"
- "Write the title, thumbnail brief, description and pinned comment, and tell me what to disclose"
