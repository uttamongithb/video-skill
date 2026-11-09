# Script Parsing & Scene Segmentation Guide

This guide explains how an AI agent converts a raw script or voiceover transcript into the **Editorial Reel** format.

---

## 1. Segmentation Principles
1. **Pacing**: Every scene covers **2.0 to 4.0 seconds** of speech.
2. **Word Density**: 4 to 8 words maximum per scene. Never overwhelm the screen with paragraph text.
3. **Typographic Breakdown**:
   - Identify **1 Kicker** (optional pre-header context, 1-3 words).
   - Identify **Context Words** (stacked 1-2 words per line).
   - Identify **1 Keyword Badge** (the primary hook word that gets boxed).
4. **Theme Sequencing**: Alternate background themes across consecutive scenes:
   - Scene 1: Crimson Wine (`theme-crimson`)
   - Scene 2: Grid Paper (`theme-grid-paper`)
   - Scene 3: Midnight Slate (`theme-slate`)
   - Scene 4: Studio Sage/Gray with Device Mockup (`theme-studio`)
   - Scene 5: Pitch Black (`theme-black`) for CTA

---

## 2. Example Conversion Walkthrough

### Raw Voiceover Script:
> "Har company me same resume bhej rahe ho? Bhai, resume ko job ke according customize karna bhi zaroori hai. Ye website try karo. Aaj hai day pandrah of AI for college students aur website hai Rezi AI. Bas apna resume upload karo, job description paste karo, aur ye tumhare resume ko us job ke according tailor karne me help karega. Saath hi ATS score bhi check kar sakte ho. Link aur mera resume tailoring prompt chahiye to comment karo 'RESUME' main DM kar dunga. Aur aise hi useful AI tools ke liye follow kar lena!"

### Parsed Scene Architecture:

#### Scene 1 (0.0s - 3.2s) - Problem Hook
- **Theme**: `theme-crimson`
- **Kicker**: `""`
- **Lines**:
  - `HAR`
  - `COMPANY`
  - `MEIN SAME`
- **Keyword Badge**: `[RESUME]` (Cream Badge)
- **Subline**: `BHEJ RAHE HO?`
- **Character Pose**: `conversational`

#### Scene 2 (3.2s - 8.4s) - Solution Pivot
- **Theme**: `theme-crimson` (or transition to Sage)
- **Kicker**: `BHAI,`
- **Keyword Badge 1**: `[RESUME]` (Cream Badge)
- **Lines**:
  - `KO JOB KE`
  - `ACCORDING`
- **Keyword Badge 2**: `[CUSTOMIZE]` (Cream Badge)
- **Subline**: `KARNA BHI [ZAROORI]`
- **Character Pose**: `thinking / stressed`

#### Scene 3 (8.4s - 12.0s) - Series Milestone
- **Theme**: `theme-grid-paper`
- **Kicker**: `AAJ HAI`
- **Headline**: `DAY`
- **Keyword Badge**: `[15]` (Crimson Badge)
- **Subline**: `OF AI FOR COLLEGE STUDENTS`
- **Character Pose**: `thumbs_up`

#### Scene 4 (12.0s - 17.5s) - Tool Reveal
- **Theme**: `theme-slate`
- **Kicker**: `AI FOR COLLEGE STUDENTS · WEBSITE HAI`
- **Headline**: `REZI [AI]` (Crimson Badge)
- **Subline**: `RESUME TAILOR · ATS SCORE · JOB MATCH`
- **Character Pose**: `presenter_hands_open`

#### Scene 5 (17.5s - 22.7s) - Feature / Demo Mockup
- **Theme**: `theme-studio` (with floating app browser window mockup)
- **Left Captions**:
  - `JOB`
  - `[DESCRIPTION]` (Cream Badge)
  - `PASTE`
  - `[KARO,]` (Crimson Badge)
- **Bottom Subline**: `AUR YE TUMHARE [RESUME] KO US JOB KE ACCORDING [TAILOR] KARNE MEIN HELP KAREGA`
- **Device UI**: Screen recording or high-res snapshot of dashboard.

#### Scene 6 (22.7s - 27.7s) - Engagement / Lead Magnet Hook
- **Theme**: `theme-crimson`
- **Kicker**: `LINK AUR MERA`
- **Lines**: `RESUME`
- **Keyword Badge**: `[TAILORING]` (Cream Badge)
- **Callout**: `COMMENT KARO ["RESUME"]`
- **Character Pose**: `pointing_down`

#### Scene 7 (27.7s - 31.5s) - Outro / CTA
- **Theme**: `theme-black`
- **Kicker**: `KE LIYE`
- **Keyword Badge**: `[FOLLOW]` (Crimson Badge)
- **Headline**: `KAR LENA!`
- **Character Pose**: `finger_heart_or_wink`
