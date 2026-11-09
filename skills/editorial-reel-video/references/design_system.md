# Editorial Reel Video: Design System & Visual Specification

This document provides the exact empirical design specifications extracted from high-performing viral reels/videos formatted in the **Swiss Editorial Typography & Anime Character** aesthetic.

---

## 1. Canvas & Layout Dimensions
- **Resolution**: 1280x720 (16:9 Landscape) or 1080x1920 (9:16 Vertical Reel/Short).
- **Framerate**: 30 FPS (or 60 FPS for extra fluidity).
- **Left Safe Zone**: Margin left: `80px` - `110px`.
- **Top Safe Zone**: Margin top: `60px` - `100px`.
- **Composition Grid**:
  - **Left 60%**: Left-aligned headline stack & badge callouts.
  - **Right 40%**: Presenter character sticker anchor (lower-right aligned).
  - **Upper Corners**: Sakura blossom vector ornaments (`width: 140px; top: 10px; left/right: 15px`).

---

## 2. Color System & Scene Inversion Sequence
High viewer retention is achieved by rotating background themes every **2.5 to 4 seconds**:

| Theme Name | Background Color | Primary Text Color | Keyword Badge Box |
| :--- | :--- | :--- | :--- |
| **A. Crimson Wine** | `#790A15` / `#800C1B` | Cream `#FAF5EA` | Cream `#FAF5EA` with Black text (`#111111`) |
| **B. Notebook Graph Grid**| `#F4EFEA` (28px grid) | Jet Black `#111111` | Crimson `#790A15` with Cream text (`#FAF5EA`) |
| **C. Midnight Slate** | `#0D1522` / `#0A111C` | Cream `#FAF5EA` | Crimson `#790A15` with Cream text |
| **D. Studio Pale Sage/Gray**| `#D9E2DC` / `#ECE8EE` | Jet Black `#111111` | Crimson `#790A15` or Cream Badge |
| **E. Pitch Black Minimalist**| `#0B0B0B` | Cream `#FAF5EA` | Crimson `#790A15` (Used for Strong CTA / Outro) |

---

## 3. Typographic Hierarchy & Styling
All text is **UPPERCASE** (`text-transform: uppercase`).

### Level 1: Kicker / Pre-header
- **Role**: Context tag, series tag, or conversational primer ("AAJ HAI", "BHAI,", "AI FOR COLLEGE STUDENTS", "KE LIYE").
- **Font Size**: `24px` - `30px`.
- **Font Weight**: `700` (Bold).
- **Letter Spacing**: `0.18em` to `0.25em` (wide tracking).
- **Margin Bottom**: `8px` - `14px`.

### Level 2: Body / Headline Stack
- **Role**: Spoken sentence context ("HAR", "COMPANY", "MEIN SAME", "KO JOB KE", "ACCORDING").
- **Font Size**: `54px` - `68px`.
- **Font Weight**: `900` (Black / Ultra-Bold).
- **Letter Spacing**: `-0.015em` (tight tracking for punchy impact).
- **Line Height**: `1.05` to `1.1` (tight vertical stack).

### Level 3: Hero Keyword Badge
- **Role**: The 1-2 critical words that the eye snaps to immediately ("RESUME", "CUSTOMIZE", "DAY 15", "REZI AI", "ATS SCORE", "DM", "FOLLOW").
- **Badge Container**: Rectangular box with `0px` border-radius (sharp Swiss poster look).
- **Padding**: `4px 18px 6px 18px`.
- **Font Size**: `64px` - `90px` (equal to or larger than headline stack).
- **Colors**:
  - In Crimson/Dark themes: Cream background (`#FAF5EA`) + Black text (`#111111`).
  - In Grid/Light themes: Crimson background (`#790A15`) + Cream text (`#FAF5EA`).

---

## 4. Masked Slide-Up Motion Animation
Unlike standard fade-ins or blurry wipes, each text line slides up from behind an invisible horizontal mask (`overflow: hidden`):
- **Initial State**: `transform: translateY(110%)`
- **Active State**: `transform: translateY(0%)`
- **Duration**: `0.25s` - `0.33s` (7 to 10 frames at 30fps)
- **Ease Curve**: `cubic-bezier(0.16, 1, 0.3, 1)` or GSAP `back.out(1.3)` / `power2.out`
- **Timing**: Snapped directly to audio word triggers.

---

## 5. Avatar / Character Posing Guidelines
Place an expressive 2D/anime character cutout in the lower-right quadrant (~28-35% width of canvas):
- **Pose 1: Conversational / Open Mouth**: For hooks and general narration.
- **Pose 2: Thumbs Up / Wink**: For milestones, tips, and confidence ("Day 15", "Easy trick").
- **Pose 3: Stressed / Holding Head**: For problem statements ("Isiliye reject ho raha hai!").
- **Pose 4: Open Hands / Presenter**: For showcasing website / tool demos.
- **Pose 5: Pointing Down / Finger Heart**: For call to action ("Comment RESUME", "Follow kar lena").
