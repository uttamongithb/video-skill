# 🎬 Editorial Reel Video Skill (v7 Engine)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Format: 9:16](https://img.shields.io/badge/Format-9%3A16%20Vertical%20Reel-blue.svg)](#)
[![Stack: HyperFrames%20%7C%20Playwright%20%7C%20FFmpeg](https://img.shields.io/badge/Stack-HyperFrames%20%7C%20Playwright%20%7C%20FFmpeg-success.svg)](#)
[![Zero Paid APIs](https://img.shields.io/badge/APIs-100%25%20Free%20%26%20Open%20Source-green.svg)](#)

A production-proven AI agent skill for generating **viral, high-retention technical explainer reels and vertical videos (1080×1920)** for **ANY subject** (Tor Onion routing, networking, databases, system architecture, Git, AI) directly from an expression-annotated voiceover script.

Built on **HyperFrames**, **Playwright**, and **FFmpeg** with strict adherence to Swiss editorial typography, invariant anchor grids, dynamic skewed wipes, topic-specific animated diagrams, and professional broadcast audio mastering.

---

## 🌟 Key Architecture & The Seven Laws

1. **One Anchor Grid, Bottom-Fixed**:
   - `Anchor 1 (Kicker)`: Category/context pill (`Y = 0.0667`) with accent dash.
   - `Anchor 2 (Hero)`: High-impact condensed display word (1–3 words) in `Anton` at `Y = 0.1006`.
   - `Anchor 3 (Proof Body)`: Dynamic proof card (`A: card-led`), odometer (`B: stat-led`), or 2-line statement (`C: type-led`) at `Y = 0.3010`.
   - `Anchor 4 (The Chip)`: Spoken sentence capsule at `Y = 0.5875` with accent dot. **Never moves across scenes.**
   - `Anchor 5 (The Presenter)`: Character cutout cropped by frame edge at `Y = 0.6340` with adaptive halo glow. **Never moves across scenes.**
2. **The Hero is a Word, The Chip is the Line, The Card is the Detail**:
   - Hero: 1–3 words (`Anton`, 17–25% of frame width, line-height 0.88).
   - Chip: 3–6 words (the line a muted viewer reads on mobile).
   - Card: The concrete proof (packet circuit, layer stripping, security matrix, live terminal log).
3. **Six-Field Color Cycle**:
   - `accent (#6F0017) → ground (#EDE3D6) → ink (#0C0A0B) → secondary (#CEDBD1) → tertiary (#0A172A) → quaternary (#DCD5E1)`.
   - No two consecutive scenes ever share a background color.
4. **Proof, Not Decoration**:
   - Every card displays real technical proof (network hops, encryption unpeeling, terminal code execution). Zero floral ornaments or meaningless clip art.
5. **Frame 0 is a Poster (`data-cover="1"`)**:
   - Scene 1 is composed at `t = 0.0s`: kicker, hero, card, and presenter already visible. Zero empty intro frames.
6. **Signature Skewed Dual-Band Wipe Transition (`wipe.html`)**:
   - Dual-band sweep skewed at `-11°` (`transform: skewX(-11deg)`).
   - Arriving scene's field background (`#w-main`) + 120px accent edge stripe (`#w-edge`), alternating direction (`flip: 0` vs `flip: 1`) on every cut.
7. **Master Audio & Sound Design**:
   - Voiceover normalized to **`-16 LUFS`** (`loudnorm=I=-16:TP=-1.5:LRA=7`).
   - Loop-safe instrumental music bed mixed at **`0.15` volume** (= **`-29 LUFS`**, exactly 13 LU below voice).
   - Procedural SFX: `pop.wav` on every cut (`0.50`), `riser.wav` 0.3s before big turns (`0.28`), `click.wav` on UI element landings (`0.40`), `chime.wav` on CTA/reveal (`0.38`).
   - Master export: **`-14 LUFS integrated`**, True Peak **`<= -1.0 dBTP`**.

---

## 🎙️ Viral Voiceover & TTS Execution Blueprint

Designed for AI agents with built-in TTS engines (Edge-TTS, ElevenLabs, Azure Neural, OpenAI):

| Expression Tag | Delivery Tone & Energy | Cadence & Pace | SSML / Parameter Injection | Presenter Pose Pairing |
| :--- | :--- | :--- | :--- | :--- |
| **`[curious]`** | Intriguing, questioning, hooked | Fast opening (**210–220 WPM**, `rate: +32%`) | `<prosody rate="+32%" pitch="+8%">...?</prosody>` | `p1_shrug.png` (raised palms, wide eyes) |
| **`[explaining]`** | Measured, crisp, authoritative | Clear (**195–205 WPM**, `rate: +28%`) | `<prosody rate="+28%" pitch="+3%">...</prosody>` | `p4_chin.png` (chin tap) or `p3_present.png` |
| **`[dramatic]`** | Intense, heavy contrast beat | Staccato (**175–185 WPM**, `rate: +18%`) | `<break time="120ms"/><prosody rate="+18%" pitch="-4%">...</prosody>` | `p8_point.png` or `p2_facepalm.png` |
| **`[confident]`** | Resonant, decisive, expert | Forward-driving (**205–215 WPM**, `rate: +30%`) | `<prosody rate="+30%" pitch="+4%">...</prosody>` | `p3_present.png` (chest out, ta-da) |
| **`[excited]`** | Thrilled, breakthrough energy | High velocity burst (**215–230 WPM**, `rate: +35%`) | `<prosody rate="+35%" pitch="+8%">...</prosody>` | `p6_thumbs.png` (big thumbs up, thrilled grin) |
| **`[playful]` / `[laughing]`** | Friendly banter, cheeky | Conversational (**200–210 WPM**, `rate: +30%`) | `<prosody rate="+30%" pitch="+5%">...</prosody>` | `p7_cta.png` (pointing at viewer, wink) |

---

## 📁 Repository Structure

```
.
├── README.md
├── .gitignore
└── skills/
    ├── editorial-reel-video/              # Production Skill Package
    │   ├── SKILL.md                       # Main instruction entry point
    │   ├── references/
    │   │   ├── voice_audio_and_cutout_guide.md    # Vocal direction, SSML, LUFS, 9 poses
    │   │   ├── v7_layout_and_transitions_guide.md # Mathematical layout & wipe mechanics
    │   │   ├── animation_and_transitions_guide.md # Physics, transitions & tempo scaling
    │   │   ├── concept_animation_guide.md         # Tor, DB, AI, Git diagram recipes
    │   │   └── design_system.md                   # Colors, safe zones, typography specs
    │   ├── resources/
    │   │   ├── assets/
    │   │   │   ├── fonts/                 # Anton, Archivo Black, Space Mono TTFs
    │   │   │   └── sfx/                   # Procedural SFX (pop, click, riser, chime, etc.)
    │   │   ├── components/                # Modular HTML proof cards (network, terminal, etc.)
    │   │   ├── compositions/              # wipe.html & base composition templates
    │   │   └── PARAMS.json                # Single source of truth design parameters
    │   ├── scripts/                       # Audio slicing, indexing & QC tools
    │   └── examples/                      # Annotated sample scripts (Tor explainer, etc.)
    │
    └── reel-from-script-v7/               # Canonical 33-file v7 reference archive
```

---

## 🚀 Quick Start for AI Agents & Users

### 1. Script Format (With Expression Tags)
```text
[HOOK — 0–7 sec | Curious + mysterious]
[curious] "Bhai, kabhi socha hai Tor Browser tumhari identity hide kaise karta hai? Tum website open karte ho, lekin tumhari request seedha website tak nahi jaati!"

[ROUTE SELECTION — 7–16 sec | Excited + explanatory]
[explaining] "Instead, Tor apne network se teen computers select karta hai — Guard Node, Middle Node aur Exit Node. Aur in teeno se milkar banta hai tumhara secret route!"
```

### 2. Execution Pipeline
```bash
# 1. Parse sections, extract expressions, map presenter poses
python skills/editorial-reel-video/scripts/process_vo.py

# 2. Validate design against the 7 Laws & write tokens
python skills/editorial-reel-video/scripts/prepare.py

# 3. Assemble scenes and compile master index.html
python skills/editorial-reel-video/scripts/build_index.py

# 4. Mix VO (-16 LUFS) with bed (-29 LUFS) & SFX, and mux final video
python skills/editorial-reel-video/scripts/mix_audio.py
python skills/editorial-reel-video/scripts/qc.py
```

---

## 📄 License
MIT License. Free for commercial, personal, and educational use.
