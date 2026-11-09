---
name: editorial-reel-video
description: >-
  Create viral, high-retention technical explainer videos and reels with bold Swiss editorial typography, keyword badge callouts, clean tech aesthetics (zero floral ornaments), dynamic scene transitions, strict timing/speed scaling (e.g., exact 60-second reels), presenter cutouts mapped to vocal expressions, professional audio mixing (-14 LUFS), and topic-specific animated diagrams (e.g., Tor Onion network flows, packet routing with layer stripping, terminal executions, architecture stacks) directly from a voiceover script. Built on HyperFrames, Playwright, and FFmpeg with zero paid APIs.
---

# Concept & Editorial Reel Video Skill

This skill teaches agents how to produce viral, high-retention technical and educational explainer videos for **ANY subject** (e.g., Tor Onion routing, networking, databases, system architecture, Git, AI) strictly adhering to target pacing (e.g. 60-second reels) with rich scene transitions, vocal expression mapping, presenter cutouts, and continuous technical animations.

---

## 1. Key Principles & Production Requirements

### A. Strict Pacing & Duration Adherence (The 60-Second Rule)
- If a script designates scene timestamps (e.g. `0–7 sec`, `7–16 sec`, `16–27 sec`, `27–42 sec`, `42–50 sec`, `50–60 sec`), the agent **MUST enforce exact target durations**.
- Default TTS speeds are often too slow (~110 WPM). The generator must scale audio playback speed using FFmpeg `atempo` (pitch-preserved) to reach viral reel velocity (**160–180 WPM**) and lock to the exact designated 60-second runtime.

### B. Agent TTS Execution & Vocal Expression Standards (Viral Retention Blueprint)
Agents equipped with built-in TTS engines (e.g. Edge-TTS, ElevenLabs, Azure Speech, OpenAI) MUST NOT use default flat/monotonic settings. Default TTS (110–120 WPM) loses short-form viewers within the first 2 seconds. The agent must inject viral pacing parameters:
- **Velocity & Cadence**: Enforce viral reel velocity (**160–180 WPM** or `rate: +15%` to `+20%`).
- **Pitch & Inflection**: Inject expressive pitch excursions (`pitch: +4Hz` to `+8Hz`) on questions and hooks.
- **Micro-Breaks**: Insert 100–180ms tactical pauses (`<break time="180ms"/>`) directly before punchline words (e.g., before *"teen envelopes!"*).
- **Expression Tag Mapping**:
  - **`[curious]`**: Fast opening (170 WPM), questioning terminal lift (`pitch: +8%`), conspiratorial intrigue.
  - **`[explaining]`**: Measured (155–165 WPM), crisp articulation, 60ms pauses before technical terms.
  - **`[dramatic]`**: Slower pace (145 WPM), pitch drop to chest voice (`-5%`), punchy staccato emphasis.
  - **`[confident]`**: Forward-driving clip (165 WPM), resonant chest tone, upward terminal lift.
  - **`[excited]`**: High velocity (180 WPM), pitch lift (`+10%`), sharp rhythmic punch on nouns.
  - **`[playful]` / `[laughing]`**: Conversational clip (165 WPM), audible chuckle / breath smile, cheeky tone.
- **Word-Level Captions**: Extract word timestamps from TTS to power dancing word-by-word highlights (`.word-active` yellow glow `#FFE600`) on the bottom chip.
- **Master Audio Blueprint**:
  - Voiceover leveled to **`-16 LUFS`** with `loudnorm=I=-16:TP=-1.5:LRA=7`.
  - Instrumental Music Bed set to volume **`0.15`** (= **`-29 LUFS`**, exactly **13 LU below the voice**). Zero sidechain ducking (the 13 LU gap is the duck).
  - Sound Effects Bus (`0.20 gain`): `pop.wav` on every scene cut (`0.50 gain`), `riser.wav` 0.3s before big scene turns (`0.28 gain`), `click.wav` on UI element landings (`0.40 gain`), `chime.wav` on reveals (`0.38 gain`), `notify.wav` on CTA (`0.35 gain`).
  - Master Export: **`-14 LUFS integrated`**, True Peak **`<= -1.0 dBTP`**.
  - Consult [`references/voice_audio_and_cutout_guide.md`](references/voice_audio_and_cutout_guide.md) for full SSML snippets and engine-specific configs.

### C. Presenter Cutout Architecture (Anchor 5)
Every scene features an expressive presenter character cutout anchored at the bottom right (`top: 63.4%`, `x: 20.7%` from right, waist cropped by frame edge, sitting below the chip). Poses are directly mapped to vocal expression tags:
- `[curious]` ➔ `p1_shrug.png` (raised palms, wide eyes, excited grin)
- `[frustrated]` ➔ `p2_facepalm.png` (palm to forehead, grimace)
- `[confident]` ➔ `p3_present.png` (arms open wide, ta-da pose, proud smile)
- `[explaining]` ➔ `p4_chin.png` (chin tap, sly half-smile, teaching pose)
- `[analogy]` / `[recalling]` ➔ `p5_memory.png` (scratching head, small aha)
- `[excited]` / `[numbers]` ➔ `p6_thumbs.png` (big thumbs up, huge thrilled grin)
- `[playful]` / `[laughing]` / `[cta]` ➔ `p7_cta.png` (pointing at viewer, cheeky grin)
- `[dramatic]` / `[look]` ➔ `p8_point.png` (direct finger point off-screen)
- `[revelation]` ➔ `p9_idea.png` (lightbulb finger up, wide eyes)
- Consult [`references/voice_audio_and_cutout_guide.md`](references/voice_audio_and_cutout_guide.md) for full image generation prompts and alpha-matting instructions.

### D. Dynamic Scene Transitions (No Stiff Cuts)
Every scene transition must use an active motion transition:
- **Skewed Dual-Band Wipe (`wipe.html`)**: Signature `-11deg` angled sweep with arriving field background + 120px accent edge stripe, alternating horizontal direction (`flip: 0` vs `flip: 1`).
- **Camera Push-In**: Zoom transition into network nodes or architecture layers (`scale: 0.85 -> 1.0`).
- **Terminal Glitch Flash**: Quick chromatic flash when entering code/terminal environments.
- Consult [`references/v7_layout_and_transitions_guide.md`](references/v7_layout_and_transitions_guide.md) for full geometry and GSAP timeline specs.

### E. Continuous Topic-Specific Animations
Never show static diagrams. All visual components must feature continuous, reactive motion:
- **Packet Routing & Layer Stripping**: In Tor and networking explainers, show animated packets physically traveling through nodes, stripping encryption layers (Green Guard shell, Yellow Middle shell, Red Exit shell) as they progress.
- **Reactive Node Lighting**: Nodes glow, pulse, and toggle status badges (`WAITING` → `ACTIVE` → `DECRYPTED`) as packets traverse them.
- **Interactive Terminal Windows**: Live typing command execution, real-time circuit logs, and blinking block cursors.

### F. Swiss Editorial Typography System
- Strictly left-aligned with clean margins.
- 3-tier hierarchy: Wide-tracked kicker (`#`), massive stacked headline, and high-contrast rectangular keyword badge pills (`[...]`).
- Masked slide-up animations (`overflow: hidden`).
- Zero floral ornaments. Clean, minimalist top technical header bar.

---

## 2. Quick Start: Voice Script to Video

Whenever the user provides a script formatted with expressions:

```text
[HOOK — 0–7 sec | Curious + mysterious]
[curious] "Bhai, kabhi socha hai Tor Browser tumhari identity hide kaise karta hai? Tum website open karte ho, lekin tumhari request seedha website tak nahi jaati!"

[ROUTE SELECTION — 7–16 sec | Excited + explanatory]
[explaining] "Instead, Tor apne network se teen computers select karta hai — Guard Node, Middle Node aur Exit Node. Aur in teeno se milkar banta hai tumhara secret route!"
```

The agent executes the pipeline:
```bash
# 1. Parse sections, extract expressions, map presenter poses
python scripts/process_vo.py

# 2. Validate design against the 7 Laws & write tokens
python scripts/prepare.py

# 3. Assemble scenes and compile master index.html
python scripts/build_index.py

# 4. Render deterministic frames at 30 FPS
python scripts/render_video.py

# 5. Mix VO (-16 LUFS) with bed (-29 LUFS) & SFX, and mux
python scripts/mix_audio.py
python scripts/qc.py
```

---

## 3. The V7 Production Architecture: Layouts & Transitions

The skill adopts the production-proven **v7 Reel Pipeline** (`PARAMS.json` -> `prepare.py` -> `new_scene.py` -> `build_index.py` -> `mix_audio.py` -> `qc.py`):

### A. The Seven Laws of Layout & Motion
1. **One Anchor Grid, Bottom-Fixed**:
   - `Anchor 1 (Kicker)`: Category/context tag at `Y = 0.0667` with accent dash `<i></i>`.
   - `Anchor 2 (Hero)`: High-impact condensed display word (1–3 words) in `Anton` at `Y = 0.1006`.
   - `Anchor 3 (Proof Body)`: Dynamic proof card (`A: card-led`), odometer (`B: stat-led`), or 2-line statement (`C: type-led`) at `Y = 0.3010`.
   - `Anchor 4 (The Chip)`: Spoken sentence capsule at `Y = 0.5875` with accent dot `<b></b>`. **Never moves between scenes.**
   - `Anchor 5 (The Presenter)`: Character cropped by frame edge at `Y = 0.6340` with adaptive halo glow (`#sX-glow`). **Never moves between scenes.**
2. **The Hero is a Word, The Chip is the Line, The Card is the Detail**:
   - Hero: 1–3 words (`Anton`, 17–25% of frame width, line-height 0.88).
   - Chip: 3–6 words (the line a muted mobile viewer reads).
   - Card: The concrete proof (file list, keyword diff, terminal, upload progress, score meter).
3. **Six-Field Color Cycle**:
   - `accent → ground → ink → secondary → tertiary → quaternary`. No two consecutive scenes may share a background.
4. **Proof, Not Decoration**:
   - Every card must display real proof (4–6 rows or mockup filling ≥ 55% of the card). If there is no proof, use `type-led` (Anchor 3C) and omit the card.
5. **Frame 0 is a Poster (`data-cover="1"`)**:
   - Scene 1 is composed at `t = 0.0s`: kicker, hero, card, and presenter already visible. Chip lands at `0.65s`. Zero empty intro frames.
6. **Transform-Only Motion with Early Landing**:
   - Entrances land in the first third of each beat (`0.24s – 0.34s`, `power3.out`). Never tween text content or innerHTML.
   - Long scenes feature a subtle continuous drift (`tl.to("#sX-hero", { y: -14, duration: 0.7 })`) to maintain visual life.
7. **Sound as Punctuation**:
   - Procedural SFX (`pop` on every cut, `click`/`key` on UI rows, `chime` on reveals, `notify` on CTA). Mastered to `-14 LUFS` and `<= -1 dBTP`.

### B. The Dual-Band Skewed Wipe Transition (`wipe.html`)
- **Geometry**: Dual-band angled sweep skewed at `-11deg` (`transform: skewX(-11deg)`).
- **Structure**: `#w-main` (the arriving scene's background color) + `#w-edge` (120px accent stripe).
- **Direction Alternation**: Flips horizontally on each scene (`flip: 0` left-to-right, `flip: 1` right-to-left).
- **Scheduling**: Fired automatically `0.36s` before each cut by `build_index.py`, with duration adaptively scaled (`0.34s – 0.62s`) to fit the scene length.

---

## 4. References & Documentation
- [`references/voice_audio_and_cutout_guide.md`](references/voice_audio_and_cutout_guide.md): Vocal direction for expressions, master LUFS targets, bed mixing, and the 9-pose presenter cutout system.
- [`references/v7_layout_and_transitions_guide.md`](references/v7_layout_and_transitions_guide.md): The full mathematical layout spec, token derivation formulas, and skewed wipe transition mechanics.
- [`references/animation_and_transitions_guide.md`](references/animation_and_transitions_guide.md): Transition physics catalog, layer-stripping packet recipes, and audio tempo scaling rules.
- [`references/design_system.md`](references/design_system.md): Exact CSS colors, fonts, line-heights, and safe zones.
- [`references/concept_animation_guide.md`](references/concept_animation_guide.md): How to design animations for Tor, databases, AI, Git, networking, and system design.
