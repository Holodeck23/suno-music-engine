# Suno Music Engine

A Claude Code / Claude.ai skill for AI music production with Suno. Covers the full pipeline:

1. **Mapping** — Reverse-engineer existing songs into timestamp-indexed structural blueprints
2. **Song Creation** — Write original vocal songs formatted for Suno (style prompt + bracketed lyrics)
3. **Instrumental Composition** — Compose vocal-free tracks grounded in cross-genre music theory
4. **Album Architecture** — Plan, sequence, and maintain sonic consistency across cohesive albums and EPs
5. **Genre Fusion** — Blend genres with intent (the Daft Punk / Radiohead / Kendrick playbook)
6. **Personal Translation** — Turn a person's life patterns and emotional landscape into mapped instrumental architecture

Reference files cover Suno-specific formatting, music theory backbone (key/BPM/mode/structure), album sequencing psychology, and personal-context-to-music translation methodology.

---

## Install

```bash
git clone <this-repo> ~/.claude/skills/suno-music-engine
cp ~/.claude/skills/suno-music-engine/USER-CONCEPTS.template.md ~/.claude/skills/suno-music-engine/USER-CONCEPTS.md
```

The skill auto-triggers when Claude Code or Claude.ai detects Suno-related intent (song mapping, instrumentals, album planning, etc.).

---

## Structure

```
suno-music-engine/
├── SKILL.md                              ← Skill entry point + routing table
├── README.md                             ← This file
├── USER-CONCEPTS.template.md             ← Blank template for personal scratch space
├── USER-CONCEPTS.md                      ← Your personal seeds/examples (gitignored)
└── references/
    ├── suno-formatting.md                ← Suno prompt engineering: style, brackets, troubleshooting
    ├── music-theory-engine.md            ← Key/mode/BPM/structure/dynamics framework
    ├── album-architecture.md             ← Sequencing, arc psychology, master prompt system
    └── personal-context-translation.md   ← Translating a life into instrumental architecture
```

---

## Reusable vs Personal

The methodology in `SKILL.md` and `references/` is fully generic. No personal info, no project bias — fork it freely.

`USER-CONCEPTS.md` is your private scratch space. It's gitignored so your concept seeds, worked examples, and personal mappings stay local. When you fork this repo, copy `USER-CONCEPTS.template.md` to `USER-CONCEPTS.md` and fill it in with your own material.

---

## Usage Examples

- "Map 'Witchcraft' by Pendulum — give me the full structural breakdown"
- "Write me a Suno-ready song in the same architecture as that map"
- "Plan a 10-track concept album about [theme]"
- "Make me an instrumental in D Dorian, 126 BPM, that blurs organic guitars and digital synths"
- "Translate my life into an instrumental — I'll give you the context"

---

## Credits

Synthesized from academic sequencing research, analysis of 470+ commercially successful albums, virtuoso production philosophies (Vai, Townsend), genre-transcendence case studies (Daft Punk, Radiohead, Kendrick), and Suno AI-specific community techniques.
