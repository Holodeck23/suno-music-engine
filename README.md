# YouTube Lesson Engine

A platform-agnostic Agent Skill that turns AI and tech lessons, AI releases, news and GitHub architectures into high-retention, faceless YouTube videos scored with custom Suno background music and music-video-grade visuals. The portable definition builds adapters for Claude Code and OpenAI Codex and covers the full pipeline:

1. **Research** — Primary sources first. Read and run the repository, date-stamp perishable claims, and label inference
2. **Script** — The Dave Dark structure: a 15-second Hook with zero fluff, 3–4 Mechanism blocks, real Proof, a high-signal Verdict
3. **Manifest** — Compile the script into a strict `lesson-manifest.json` and validate it before production
4. **BGM Scoring** — Loopable instrumental Suno beds (dark synthwave, prog-metal/electronic, post-rock, 85–126 BPM) that leave the voice its 300 Hz–3 kHz band
5. **Narration Timing** — TTS audio as the timing authority, with word-level triggers for code and diagram reveals
6. **Visuals** — Code, architecture and vibe states built on tested rendering, legibility, determinism and export-verification lessons
7. **Mix and Release** — Ducking, loudness, YouTube copy, Suno commercial-use rights and AI disclosure

This engine grew out of `suno-music-engine`. It keeps the instrumental Suno knowledge and every video-production lesson. The vocal songwriting, album and personal-translation modes were retired; they remain in the `main` branch history.

---

## Quick start

```bash
# Validate a lesson manifest (Python 3.8+, standard library only)
python3 scripts/validate-lesson-manifest.py references/lesson-manifest.example.json --strict
```

The example is a complete 3-minute lesson on Git's object database, with real terminal output in its Proof segments.

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
├── definition.md                          ← Portable source of truth
├── polyskill.yaml                         ← Claude and Codex build targets
├── README.md                              ← This file
├── USER-CONCEPTS.template.md              ← Template for a private channel profile
├── references/
│   ├── script-and-retention-engine.md     ← Dave Dark structure, retention, TTS writing, manifest contract
│   ├── lesson-manifest.schema.json        ← Machine-readable manifest schema
│   ├── lesson-manifest.example.json       ← Complete valid example lesson
│   ├── bgm-suno-scoring.md                ← Instrumental Suno beds, loops, voice pocket, ducking, loudness
│   ├── music-video-production.md          ← Timing, design systems, rendering, verification, world-building lessons
│   ├── instrumental-video-production.md   ← Stems, tempo drift and music-driven animation
│   ├── video-direction-and-quality.md     ← Reference craft, motion proofs, quality resets, camera jumps
│   └── youtube-release.md                 ← Publishing copy, commercial-use rights and AI disclosure
├── scripts/
│   ├── validate-lesson-manifest.py         ← Schema + Dave Dark structure validator
│   ├── extract-video-timing.py             ← Embedded cues and audio identity
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
- "Duck the bed under my narration and master to −14 LUFS"
- "Pilot the hook and first mechanism block as a rendered video"
- "Write the YouTube title and description, and tell me what to disclose"
