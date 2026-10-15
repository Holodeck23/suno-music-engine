# Suno Music Engine

A platform-agnostic Agent Skill for AI music production with Suno v6. The portable definition builds optimized adapters for Claude Code and OpenAI Codex and covers the full pipeline:

1. **Mapping** — Reverse-engineer existing songs into timestamp-indexed structural blueprints
2. **Song Creation** — Write original vocal songs formatted for Suno (style prompt + bracketed lyrics)
3. **Instrumental Composition** — Compose vocal-free tracks grounded in cross-genre music theory
4. **Album Architecture** — Plan, sequence, and maintain sonic consistency across cohesive albums and EPs
5. **Genre Fusion** — Blend genres with intent (the Daft Punk / Radiohead / Kendrick playbook)
6. **Personal Translation** — Turn a person's life patterns and emotional landscape into mapped instrumental architecture
7. **V6 Editing and Multi-Input Workflows** — Make atomic section/lyric edits, mash up authorized sources, and compose from text, audio, images, or video
8. **Music Videos** — Develop song and story together, study references, prove demanding actions, and build/verify videos against the selected recording
9. **YouTube Releases** — Prepare titles, descriptions and channel bios with grounded rights and AI disclosure guidance

Reference files cover Suno formatting, music theory, album sequencing, personal translation, video direction and quality resets, lyric-driven and instrumental production, rendering lessons, and YouTube release preparation. See [video capabilities](docs/video-capabilities.md) for bundled tools, implementation boundaries and observed outcomes.

---

## Install with Polyskill

```bash
git clone https://github.com/Holodeck23/suno-music-engine.git
cd suno-music-engine
polyskill validate
polyskill install
```

By default, Polyskill installs the generated adapters to `~/.claude/skills/suno-music-engine` and `~/.agents/skills/suno-music-engine`. Use `polyskill install --target claude` or `polyskill install --target codex` for one runtime.

Copy `USER-CONCEPTS.template.md` to `USER-CONCEPTS.md` inside the installed skill if you want private local concept seeds. That file is ignored by Git.

---

## Structure

```
suno-music-engine/
├── definition.md                         ← Portable source of truth
├── polyskill.yaml                        ← Claude and Codex build targets
├── README.md                             ← This file
├── USER-CONCEPTS.template.md             ← Blank template for personal scratch space
├── references/
│   ├── suno-formatting.md                ← Suno prompt engineering: style, brackets, troubleshooting
│   ├── music-theory-engine.md            ← Key/mode/BPM/structure/dynamics framework
│   ├── album-architecture.md             ← Sequencing, arc psychology, master prompt system
│   ├── personal-context-translation.md   ← Translating a life into instrumental architecture
│   ├── music-video-production.md         ← Audio timing, animation, rendering and verification
│   ├── instrumental-video-production.md  ← Stems, tempo drift and music-driven animation
│   ├── story-world-video.md              ← Story pass: a world, a character, consequences
│   ├── video-direction-and-quality.md    ← Reference craft, motion proofs, rejection and song/story co-development
│   └── youtube-release.md                ← Publishing copy, commercial-use rights and AI disclosure
├── scripts/
│   ├── extract-video-timing.py            ← Embedded lyric cues and audio identity
│   └── align-lyric-words.py               ← Vocal-stem word alignment
├── docs/video-capabilities.md            ← Coverage and implementation inventory
└── dist/
    ├── claude/suno-music-engine/         ← Generated Claude Code adapter
    └── codex/suno-music-engine/          ← Generated OpenAI Codex adapter
```

---

## Reusable vs Personal

The methodology in `definition.md` and `references/` is generic. Generated runtime files are build artifacts; edit the portable source and rebuild rather than hand-editing `dist/`.

`USER-CONCEPTS.md` is your private scratch space. It's gitignored so your concept seeds, worked examples, and personal mappings stay local. When you fork this repo, copy `USER-CONCEPTS.template.md` to `USER-CONCEPTS.md` and fill it in with your own material.

---

## Usage Examples

- "Map 'Witchcraft' by Pendulum — give me the full structural breakdown"
- "Write me a Suno-ready song in the same architecture as that map"
- "Plan a 10-track concept album about [theme]"
- "Make me an instrumental in D Dorian, 126 BPM, that blurs organic guitars and digital synths"
- "Translate my life into an instrumental — I'll give you the context"
- "Write the YouTube description and channel bio for my Suno music video"

---

## Credits

Synthesized from academic sequencing research, analysis of 470+ commercially successful albums, virtuoso production philosophies (Vai, Townsend), genre-transcendence case studies (Daft Punk, Radiohead, Kendrick), and Suno AI-specific community techniques.
