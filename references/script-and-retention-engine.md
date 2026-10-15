# Script and Retention Engine: From Topic to `lesson-manifest.json`

Methodology for turning a technical concept, an AI release or a GitHub repository into a 3–6 minute faceless lesson, and the strict manifest every script compiles into. The manifest is the hand-off between writing and production: narration goes to TTS, `bgm_mode` drives the music automation (`bgm-suno-scoring.md`), and `visual_state` / `visual_payload` drive the renderer (`music-video-production.md`).

Validate every manifest before production:

```bash
python3 scripts/validate-lesson-manifest.py lesson-manifest.json            # human report + timeline estimate
python3 scripts/validate-lesson-manifest.py lesson-manifest.json --strict   # warnings also fail (use before render)
python3 scripts/validate-lesson-manifest.py lesson-manifest.json --json     # machine-readable report
```

The machine-readable schema is `references/lesson-manifest.schema.json`. A complete, valid example lesson is `references/lesson-manifest.example.json`.

---

## 1. Intake: What Is the Lesson Actually About?

Write a one-sentence **thesis** before anything else: the architectural problem or industry shift, stated so a viewer who stops at 0:15 still learns something. If it cannot be said in one sentence, the lesson is not ready.

Then research by input type. Separate documented fact from inference, and never fabricate technical data.

| Input | Primary sources | What to extract |
|---|---|---|
| **Technical concept** | Specifications, original papers, maintainers' documentation | The mechanism in 3–4 parts, the common misconception, a runnable demonstration |
| **AI release** | The vendor's announcement, model or system card, API docs, changelog | What changed, what it costs or replaces, what is confirmed vs. marketing, the release date |
| **GitHub repository** | The code itself: entry points, core modules, data flow, tests, recent commits; the README second | The architecture as it is implemented, one real execution path, its real output |

- **Run it.** The Proof block shows real terminal output, real code from the repository or a benchmark with its source and conditions. If something cannot be run, show the code path and say so. Never stage output.
- **Date-stamp perishable claims** (prices, limits, versions, benchmark rankings) in the research notes with the date checked. A lesson about a release ages, and the notes are what let a future update find what changed.
- **Flag inference.** "The repository appears to cache embeddings per file" is an inference until a code path confirms it. Narration states only what the evidence supports.
- **Cross-reference conflicts.** When sources disagree on a number, report the range or the authoritative source, not the most exciting figure.

---

## 2. The Dave Dark Structure

Every lesson follows four phases in this order. The validator enforces the order and counts.

### Phase 1: The Hook (`0:00–0:15`)
- **Zero fluff.** No "hey guys", no "welcome back", no "in this video", no channel introduction. The first words state the problem or the shift.
- Narration runs over a **building BGM intro** (`bgm_mode: "full_swell"`) and ends on a **3-second visual drop**. The drop is implicit: the renderer schedules it from the hook's last word and lands it on a measured BGM downbeat (`bgm-suno-scoring.md` §12).
- Budget: **at most 12 s of narration**, which is 30 words at 150 wpm, so that narration plus the 3 s drop finishes by 0:15.
- One segment, `visual_state: "vibe_drop"`. Open a loop the Verdict will close: a claim that sounds wrong, a cost nobody mentions, a mechanism people misdescribe.

### Phase 2: The Mechanism (3–4 blocks)
- Break the concept into **3–4 concrete technical blocks**, each one idea with one visual. Order them so each block needs only the previous ones.
- Each block opens with a one-line claim, then the evidence, then the visual payoff, timed to a trigger word.
- A block may span several segments (for example a diagram followed by code). Consecutive mechanism segments that share a slug form one block: `seg_03_mechanism_cache` + `seg_04_mechanism_cache` is one block.
- `bgm_mode: "ducked"`. Dense explanation and a full-level bed compete for the same band.

### Phase 3: The Proof / Code
- The **actual implementation, terminal flow or benchmark reality**: real commands with their real output, the code path in the repository, a benchmark with its conditions.
- Usually `code_focus` (code or terminal) or `artifact_pan` (a paper figure, a repository page, a benchmark table). Not a vibe shot.
- `bgm_mode: "ducked"`.

### Phase 4: The Verdict
- A **high-signal takeaway**: what to do differently, what to stop believing, when this matters and when it does not. Close the hook's open loop.
- Usually `vibe_drop` or `artifact_pan` with a headline. `bgm_mode: "full_swell"` lets the bed rise under the closing line and end card.
- No recap of every block, and no "thanks for watching" padding. A short call to action, if any, belongs after the takeaway, never before it.

### Word budgets at 150 wpm

| Phase | Typical length | Words | Segments |
|---|---|---|---|
| Hook | ≤ 12 s + 3 s drop | ≤ 30 | exactly 1 |
| Mechanism | 25–60 s per block | 60–150 per block | 3–4 blocks |
| Proof | 30–90 s | 75–225 | 1 or more |
| Verdict | 20–40 s | 50–100 | 1 or more |
| **Whole lesson** | **3–6 min** | **≈ 450–900** | at least 6 |

Estimates come from word counts. The **rendered narration audio is the timing authority** (§6), so check the real duration after TTS.

---

## 3. Retention Mechanics

- **Something changes on screen at least every 20–40 seconds.** A new segment or a highlight trigger counts. The validator warns when a segment averages more than 40 s per visual beat. Treat this as a diagnostic, not a quota: cut counts do not measure quality, and calmer passages can hold a single, developing visual.
- **The visual payoff lands on the word.** Triggers reveal the code line or diagram node at the moment the narration names it. A reveal that arrives early spoils it; one that arrives late reads as lag.
- **One idea per sentence.** Short declarative sentences survive TTS and keep pace without rushing.
- **Name the misconception, then break it.** "Branches are not containers" teaches faster than a neutral definition.
- **Concrete over abstract.** A real hash, a real command, a real number with its source.
- **Pay off the hook.** If the Verdict does not answer the question the Hook raised, the viewer feels cheated even when every block was correct.
- **No filler anywhere.** Each sentence must earn its seconds. Cut "basically", "essentially", "as you can see", "let's dive in".

---

## 4. Writing Narration for TTS

- **Write for the ear.** Spell out what a voice should say: "dot git folder" instead of `.git`, "hello dot t x t" instead of `hello.txt`, "forty" or "40" (test the voice), "SHA-1" (most voices handle it).
- **Never read code aloud verbatim.** Code goes in `visual_payload.code_snippet`; narration describes what it does. The validator warns about backticks, braces, angle brackets, underscores, pipes, backslashes and URLs in narration.
- **Acronyms:** decide letter-by-letter vs. spoken ("K V cache" vs. "kay-vee cache") and keep it consistent across the channel. Record pronunciations in `USER-CONCEPTS.md`.
- **Numbers:** round in speech, keep exact values on screen. "About two hundred milliseconds" is spoken; "198 ms (p50, n=1,000)" is shown.
- **Trigger words must exist verbatim** in the narration, and should be distinctive. "Tree" fires on the first "tree" after the previous trigger, so pick words that occur where the reveal belongs.

---

## 5. The Manifest: `lesson-manifest.json`

### Exact shape

```json
{
  "title": "String",
  "bgm_track": "path/to/suno_stem.mp3",
  "voice_id": "elevenlabs_voice_id",
  "segments": [
    {
      "id": "seg_01_hook",
      "narration": "Exact spoken text for TTS...",
      "visual_state": "vibe_drop | code_focus | architecture_graph | artifact_pan",
      "bgm_mode": "ducked | full_swell",
      "visual_payload": {
        "headline": "Optional overlay text",
        "code_snippet": "Optional code/terminal block",
        "diagram_nodes": ["Node A -> Node B"],
        "highlight_triggers": [
          {"word": "exact_word_in_narration", "action": "reveal_line_2"}
        ]
      }
    }
  ]
}
```

No other fields are allowed at any level. Unknown keys are errors, so a typo cannot silently drop data.

### Top-level fields

| Field | Type | Rule |
|---|---|---|
| `title` | string | 1–100 characters (YouTube's title limit). Warning above ~70, where search results often truncate |
| `bgm_track` | string | Path to the selected BGM stem, relative to the production folder (`bgm-suno-scoring.md`) |
| `voice_id` | string | The TTS voice identifier (an ElevenLabs voice ID) |
| `segments` | array | At least 6 segments: Hook, 3 Mechanism blocks, Proof, Verdict |

### Segment fields

| Field | Type | Rule |
|---|---|---|
| `id` | string | `seg_<NN>_<phase>[_<slug>]`. `NN` runs 01, 02, … in order. `phase` is `hook`, `mechanism`, `proof` or `verdict`. `slug` is lowercase `[a-z0-9_]` |
| `narration` | string | Exact text sent to TTS. Must contain spoken words |
| `visual_state` | enum | `vibe_drop`, `code_focus`, `architecture_graph`, `artifact_pan` |
| `bgm_mode` | enum | `ducked`, `full_swell` |
| `visual_payload` | object | Required (may be `{}`). Fields below are optional unless the visual state requires them |

### `visual_payload` fields

| Field | Type | Meaning |
|---|---|---|
| `headline` | string | Overlay text: display face, accent colour. Required by `show_headline` |
| `code_snippet` | string | Code or terminal block, lines separated by `\n`. Required by `code_focus` |
| `diagram_nodes` | string[] | Each entry is a node label or a chain `A -> B -> C`. The renderer merges entries into one graph, deduplicating nodes by label. Required by `architecture_graph` |
| `highlight_triggers` | object[] | `{"word", "action"}` pairs, matched in array order (§5, "Trigger semantics") |

### Visual states

| State | Shows | Typical phase | Requires |
|---|---|---|---|
| `vibe_drop` | Atmospheric motion and type: headline, music-driven light, the drop | Hook, Verdict | Nothing; a headline is usual |
| `code_focus` | Code or terminal block with progressive reveal and line highlights | Mechanism, Proof | `code_snippet` |
| `architecture_graph` | Node/edge diagram revealed node by node | Mechanism | `diagram_nodes` |
| `artifact_pan` | Slow pan across a real artifact: paper figure, repository page, benchmark table, release note | Proof, Verdict | The artifact image comes from the production folder by segment id. A headline is usual |

### BGM modes

| Mode | Meaning |
|---|---|
| `ducked` | The bed sits well under the narration: EQ pocket plus a gain reduction (start near −12 dB) and sidechain ducking keyed from the voice |
| `full_swell` | The bed plays at full level. Sidechain ducking stays active, so any words in the segment still cut through. Used for the hook build and drop, and the verdict and end card |

Ramp between modes over about 0.3–0.5 s, landing on a measured downbeat where the timeline allows (`bgm-suno-scoring.md` §12).

### Trigger actions

| Action | Effect |
|---|---|
| `reveal_line_<n>` | Reveals `code_snippet` lines 1 through `n`, like a terminal printing output. With no reveal triggers the whole snippet shows at segment start |
| `highlight_line_<n>` | Moves the accent highlight to line `n` |
| `reveal_node_<n>` | Reveals the `n`th `diagram_nodes` entry. Entries without a reveal trigger are visible from segment start |
| `highlight_node_<n>` | Accents the `n`th `diagram_nodes` entry |
| `show_headline` | Brings in the headline. Without this trigger the headline shows at segment start |
| `drop` | An extra visual drop inside a `vibe_drop` segment. The hook's 3-second drop is implicit and needs no trigger |

Indices are 1-based. The validator rejects indices past the end of the snippet or diagram, and warns when snippet lines are never revealed.

### Trigger semantics
- Triggers are matched **in array order**. Each matches the **first occurrence of its word after the previous trigger's match**, so a repeated word ("tree", then "tree" again) can drive two triggers.
- Matching is **exact and case-sensitive** against narration tokens with surrounding punctuation removed ("works." matches `works`). The validator points out case-only mismatches.
- The trigger fires at the **start time of that spoken word** in the rendered narration (§6).

### Validator rules beyond the schema

Errors (these block production):
- Duplicate ids; `NN` out of sequence.
- Phases out of order; not exactly one Hook; fewer than 3 or more than 4 Mechanism blocks; no Proof; no Verdict.
- Hook not first, not `vibe_drop`, over the word cap (30 at 150 wpm), or opening with greeting or filler.
- `code_focus` without `code_snippet`; `architecture_graph` without `diagram_nodes`; a chain with an empty side of `->`.
- A trigger word not found after the previous trigger; a line or node index out of range; `show_headline` without a headline; `drop` outside `vibe_drop`.
- Narration with no spoken words.

Warnings (`--strict` makes these fail):
- Hook not `full_swell`; Mechanism or Proof at `full_swell`; Proof shown as `vibe_drop`.
- Estimated runtime outside 3–6 minutes; more than 40 s per visual beat in a segment; snippet lines never revealed.
- Symbols or URLs in narration that TTS reads literally; a title over about 70 characters.

---

## 6. From Manifest to Timeline

The production lessons in `music-video-production.md` apply with narration in place of lyrics.

1. **The rendered narration audio is the timing authority.** Render TTS per segment (or as one file with known segment boundaries), keep each file's SHA256 beside the manifest, and measure real durations. Word-count estimates are for planning only.
2. **Word timing from the TTS provider first.** ElevenLabs offers a text-to-speech endpoint with timestamps that returns character-level start/end times for the synthesized audio (verify the current endpoint and fields against its API docs). Group characters into words and resolve each trigger to its word's start time.
3. **Fallback alignment:** when the provider gives no timestamps, run `scripts/align-lyric-words.py` on the narration audio with a timing file holding one cue per segment (`{"lyrics": [{"start", "end", "text"}]}`). Narration is clean speech, so no stem separation is needed. The helper accepts a heard word only within `--window` seconds after its cue's start (default 30), so set `--window` to at least the longest segment's duration. It uses `mlx-whisper` on Apple hardware; substitute any Whisper build that returns word timestamps elsewhere. Report the matched/total word count, and check interpolated words against playback.
4. **Assemble the timeline:** segment start = previous segment end (plus any deliberate pause); the hook's drop starts at its last word's end and lasts 3.0 s; then apply `bgm_mode` automation per segment.
5. **Align the BGM:** offset the hook-intro stem so its measured drop downbeat lands on the drop time (`bgm-suno-scoring.md` §12). Never time the drop from the prompt BPM.
6. **Render deterministically:** every frame evaluates from absolute time. Keep a pilot-first workflow, contact sheets plus motion review, and export verification (`music-video-production.md`).

---

## 7. Delivery States and Checklist

Report only the states actually reached:

`script drafted` → `manifest valid (--strict)` → `narration rendered and timed` → `BGM selected and aligned` → `pilot rendered` → `motion and audio reviewed` → `full lesson exported and verified` → `user accepted` → `published`

Before handing a manifest to production:
1. The thesis is one sentence, and the Hook states it in the first words.
2. Every Mechanism block is one idea with one visual. There are 3–4 blocks.
3. The Proof shows real output or real code from a cited source, and nothing is staged.
4. The Verdict closes the Hook's loop with a concrete takeaway.
5. `validate-lesson-manifest.py --strict` passes. State its runtime estimate.
6. Perishable claims are date-stamped in the research notes, and inferences are labelled.
