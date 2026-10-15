# Music-driven animation and instrumental videos

Read alongside `music-video-production.md` for instrumentals or vocal videos whose motion should follow instruments as well as lyrics. Missing subtitle streams are normal for an instrumental; do not invent lyric timing or require a transcription stage.

## Let the recording determine the structure

Preserve the selected audio and its identity. Measure actual duration, then derive the visual treatment from four timescales:

| Timescale | Audio evidence | Visual role |
|---|---|---|
| Form | Sections, repeated motifs, changes in instrumentation | Worlds, palette evolution, major transformations |
| Phrase | Downbeats, phrase starts, builds and drops | Camera moves, reveals, anticipation and cuts |
| Beat | Beat events and individual stem onsets | Impacts, pulses, sparks and brief light changes |
| Texture | Per-stem level, envelopes and spectral brightness | Density, mass, speed, roughness and colour |

Give stems distinct jobs: drums can drive impacts, bass can drive mass or camera weight, and melodic content can drive form or colour. When an instrument drops out, its layer should empty. A single full-mix volume envelope cannot represent that distinction.

## Offline analysis contract

Archive measured events and sampled feature curves beside the selected audio. The renderer should evaluate them at any absolute time without live audio input.

1. Create a documented analysis derivative without replacing the original. Separate stems where the visual treatment benefits from them. The production experiments used Demucs `htdemucs_ft` and `htdemucs_6s`; model names are choices, not a guarantee of clean isolation.
2. Detect beats and downbeats, then cross-check against drum onsets across the whole recording. Beat This! and librosa were used in the experiments. Treat median BPM as a summary, not a fixed animation clock: one take drifted from about 129 to 132 BPM, and a grid at the requested 128 BPM matched only 29% of measured kicks.
3. Propose sections from novelty/chroma/MFCC analysis and inspect per-bar stem energy. Machine boundaries remain proposals until checked. A novelty kernel sign error once collapsed an entire song into one section; even a corrected detector later produced an unhelpful 92-second block. Use stems, words where present, and playback to resolve boundaries.
4. Compute per-stem level, smoothed attack/release envelopes, onset strength and spectral brightness at an explicit control rate. The existing project pipeline uses 120 Hz, interpolated to video timestamps. Record rate, frame count, curve names, numeric dtype and layout; validate byte length before loading a binary feature file.
5. Keep raw beat events and any corrections separately. Record located versus absent scored events using the main video guide. Do not turn requested silences, intro lengths or bar counts into measured facts.

Inspect stem leakage. A six-stem "guitar" output contained a distorted synth in a guitar-free intro; it was useful as a mid-range lead layer, not evidence of an isolated guitar. A "vocals" stem can contain effects and separation residue on an instrumental.

Retain an absolute noise floor when normalizing. Per-track percentile scaling can inflate an absent instrument's residue into full motion. Test whether the stem is actually present, gate inactive layers, and record the thresholds used. Check onset thresholds and minimum separation so one attack does not become several impacts.

## Reproducible musical motion

Use measured beat/bar events for phase. A precomputed monotone musical-time curve, the integral of a smoothed energy curve, lets motion accelerate with the music while remaining a function of absolute time. Seed procedural randomness and use time-indexed event lookup rather than advancing a cursor on every preview frame.

History-dependent fluids or particle advection need fixed-step simulation and saved checkpoints, or a closed-form approximation. A seek must restore a checkpoint and replay deterministically rather than inherit the previous preview state. Test timestamps in a non-sequential order before parallel rendering.

Anticipation can use the known future drop: tighten framing or reduce light in the preceding phrase. This is a creative choice, not a rule that every cut must land on a downbeat.

## Treatment and rendering choices

Map motifs to musical layers and an evolution across the track. Keep the representative motion proof and whole-film review workflow from the main guide. For a demanding reference or rejected draft, use `video-direction-and-quality.md`; synchronized feature curves alone do not establish compelling imagery. Do not add a new approval gate when the user has delegated direction and completion.

Choose effects for the aesthetic. HDR materials, selective bloom, volumetric light, instancing, reaction-diffusion and raymarched forms are possible techniques, not a mandatory stack. Some remained proposals in the instrumental approach notes; do not describe them all as implemented or tested.

Optional offline motion blur averages deterministic subframes across a shutter interval in linear HDR before tonemapping. Supersampling can improve fine geometry and type but increases cost. Benchmark a short representative range first. Paper/ink treatments need the light-ground rules in the main guide instead of blindly applying a dark-scene filmic grade.

## Tooling boundary

The skill currently ships embedded-cue extraction and lyric-word alignment helpers. It does **not** ship a general stem-analysis or rendering executable. The existing video projects contain `prepare.sh`, `analyze.py`, feature samplers and renderers; consult the capability inventory in `docs/video-capabilities.md` before assuming a command is installed with this skill.

When adapting those implementations, parameterize source and output paths, preserve their provenance, verify dependencies against the target machine, and validate on known synthetic events plus a representative real recording. Keep toolchain recommendations separate from a claim that every dependency is already installed.
