# Suno v6 Upgrade Audit

Audited 2026-09-11 against Suno's official v6 announcement and FAQ.

## Verdict

The engine's composition, mapping, lyric, and album frameworks remain useful. Its model-selection,
slider, editing, and product-workflow guidance required an upgrade because Suno retired every model
before v6.

## Confirmed v6 changes incorporated

- Model routing for v6, v6-wild, and v6-mini
- Natural-language section edits and single-lyric replacement
- Mashups, sampling, and multi-source requests
- Text, Suno song, playlist, audio, image, and video inputs in one prompt
- Simple Mode workflow selection
- Variety slider behavior, including 0 for strict authored style tags
- Max Mode guidance and its additional-credit tradeoff
- Automatic migration of existing Custom Models to v6
- Retirement of all pre-v6 generation models

## Intentionally retained

- Structural mapping and timestamp discipline
- Style-prompt and bracketed-lyrics output formats
- Musical-foundation, dynamic-arc, album-sequencing, and genre-fusion frameworks
- Conservative 1,000-character style, 5,000-character lyrics, and 8-minute generation ceilings

The v6 launch sources do not restate those field and duration limits. They are labeled as
pre-v6 operational constraints, not newly confirmed v6 specifications, and should be checked
against the live product if Suno rejects or truncates an input.

## Sources

- [Suno: Introducing v6](https://suno.com/blog/introducing-v6), published 2026-09-09
- [Suno Help: v6 FAQ](https://help.suno.com/en/articles/13924481), published 2026-09-09
