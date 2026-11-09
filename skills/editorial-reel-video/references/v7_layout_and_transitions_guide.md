# V7 Layout & Transitions Engineering Guide

This guide details the exact layout mechanics, transition physics, and motion rules reverse-engineered from production reels in **REEL-FROM-SCRIPT v7**.

---

## 1. The Invariant 5-Anchor Grid Layout

In high-retention 9:16 vertical video, visual chaos causes viewer fatigue. The v7 layout achieves cohesion by **locking the bottom half of the frame across all scenes** while allowing the top half to dynamically re-compose.

```
+-------------------------------------------------------------+  Y = 0.00
| SAFE ZONE TOP (8.75% / 168px)                               |
| [ANCHOR 1: KICKER]  --- CONTEXT / TAG                       |  Y = 0.0667 (128px)
| [ANCHOR 2: HERO]    MASSIVE WORD (1-3 words)                |  Y = 0.1006 (193px)
|                                                             |
| [ANCHOR 3: PROOF BODY / CARD]                               |  Y = 0.3010 (578px)
|   +-----------------------------------------------------+   |
|   | .bar  [Title / File]                 [Meta / Status]|   |
|   | .body [Real Data / UI Rows / Odometer / Terminal]   |   |
|   +-----------------------------------------------------+   |
|                                                             |
| [ANCHOR 4: CHIP]    (•) SPOKEN SUBTITLE / CAPTION LINE      |  Y = 0.5875 (1128px)
|                                                             |
| [ANCHOR 5: PRESENTER]                                       |  Y = 0.6340 (1217px)
|                     +---------------+                       |
|                     | [CHARACTER]   | (cropped by frame)    |
| SAFE ZONE BOTTOM    +---------------+                       |  Y = 0.7810 (1500px)
+-------------------------------------------------------------+  Y = 1.00 (1920px)
```

### The Invariants:
1. **Anchor 4 (`#sX-chip`)**:
   - Sits at `top: 1128px` (`58.75%` of height) with `height: 86px`.
   - Full pill radius (`border-radius: 999px`).
   - Accent dot: `<b></b>` (`16px x 16px`, circular).
   - Uppercase bold text (`Space Mono` or sans), 3–6 words.
   - **Crucial Rule**: The proof card above it clips at `max-height: 470px`, guaranteeing that the card NEVER collides with or overlaps the chip.
2. **Anchor 5 (`#sX-char` + `#sX-glow`)**:
   - Sits at `top: 1217px` (`63.4%` of height), `left: 224px`.
   - Cropped waist-up by the frame boundary (`presenterTop + h > 1.0`).
   - Soft circular halo (`#sX-glow`): `width: 700px`, `height: 700px`.
   - **Adaptive Contrast Rule**: On light fields (`ground`, `secondary`, `quaternary`), halo opacity is `0.20`. On dark fields (`ink`, `tertiary`), halo opacity automatically boosts to `0.42` (`--glow-alpha: 0.42`) so dark silhouettes never blend into the dark background.

---

## 2. Dynamic Top-Half Archetypes

Anchor 3 adapts to the beat's editorial purpose:

| Archetype | Key | Role | Elements | Typical Reveal Timing |
| :--- | :--- | :--- | :--- | :--- |
| **Card-Led** | `A` | **Proof Beats**: Mockup, diff, terminal, upload, file list | `.bar` header + `.body` with hard offset shadow (`14px 16px 0`) | Card enters at `0.45s` (`bodyAt`), rows stagger by `0.12s` |
| **Stat-Led** | `B` | **Number Beats**: Metrics, benchmark, score | `#sX-odo` (odometer digit strips) + `#sX-support` line | Digits spin `0.55s - 1.5s`, support text enters at `1.25s` |
| **Type-Led** | `C` | **Statement Beats**: Hook, pivot, tool reveal | `#sX-lines` (massive 2-line condensed statement, no card) | Lines enter at `0.45s` with `power4.out` |

### The Odometer Physics (Archetype B):
```html
<div id="sX-odo">
  <div class="col" data-digit="9">
    <span class="strip"><span>0</span><span>1</span>...<span>9</span></span>
  </div>
  <div class="col" data-digit="4">
    <span class="strip"><span>0</span><span>1</span>...<span>9</span></span>
  </div>
</div>
```
- Each column is strictly `width: calc(var(--size-hero) * 0.58)` and `height: var(--size-hero)`.
- Each digit span is `height: 1em; line-height: 1em;`.
- GSAP animates: `tl.to(col.querySelector(".strip"), { y: "-=" + digit + "em", duration: 0.95 - i*0.05, ease: "power2.inOut" })`.

---

## 3. The Dual-Band Skewed Wipe Transition (`wipe.html`)

Instead of standard crossfades or slide pushes, v7 uses a custom geometric angled wipe that gives every transition high production energy.

### CSS Geometry
```css
#root { position: absolute; inset: 0; overflow: hidden; }

/* The skewed band traverses diagonally across the viewport */
.band {
  position: absolute;
  top: -260px;
  left: 0;
  height: 2440px;
  width: 1560px;
  transform: skewX(-11deg);
  transform-origin: 50% 50%;
}

/* Wide background cover colored with the arriving scene's field */
#w-main {
  background: var(--wipe-color, var(--ink, #16110f));
}

/* 120px accent edge stripe that leads/trails the main wipe */
#w-edge {
  background: var(--accent, #6F0017);
  width: 120px;
}
```

### GSAP Animation & Alternating Direction
```javascript
const vars = window.__hyperframes.getVariables ? window.__hyperframes.getVariables() : {};
const flip = String(vars.flip || "0") === "1";
const sign = flip ? -1 : 1;
const tl = gsap.timeline({ paused: true });

// Initial off-screen positions
gsap.set("#w-main", { x: sign * -1780 });
gsap.set("#w-edge", { x: sign * -1900 });

// Sweep across screen
tl.to("#w-main", { x: sign * 1240, duration: 0.52, ease: "power2.inOut" }, 0);
tl.to("#w-edge", { x: sign * 1240, duration: 0.52, ease: "power2.inOut" }, 0.05);

window.__timelines["wipe"] = tl;
```

### Scheduling Logic in `build_index.py`
1. **Pre-Cut Lead Time**: The wipe starts **0.36 seconds before the cut** (`WIPE_LEAD = 0.36`), so the sweep is at maximum occlusion exactly when the audio beat transitions.
2. **Adaptive Duration**:
   ```python
   scene_dur = spans[i][1] - spans[i][0]
   dur = round(min(0.62, max(0.34, scene_dur * 0.42)), 2)
   lead = round(min(0.36, dur * 0.6), 3)
   start = round(max(0.0, spans[i][0] - lead), 3)
   flip = 1 if i % 2 == 0 else 0
   ```
   Short scenes (e.g. 1.2s) automatically receive shorter wipes (0.34s) so they don't get obscured.
3. **Arriving Field Color**: The wipe takes the exact color token of the arriving scene (`colour(fields[i])`).

---

## 4. The Six-Field Dopamine Reset Rhythm

The skill enforces a strict color cycling invariant:
```json
"fieldCycle": ["accent", "ground", "ink", "secondary", "tertiary", "quaternary"]
```
- **Rule**: `prepare.py` inspects every scene's `data-field` attribute and **hard-fails** if two consecutive scenes share the same field.
- The visual color flip *is* half of the transition.

---

## 5. Frame 0 Cover Poster Rule (`data-cover="1"`)

A common mistake in AI video generation is having elements animate in from opacity 0 on frame 0, resulting in a blank initial frame that loses viewer retention.
- **Scene 1 has `data-cover="1"`**:
  - `gsap.set(["#s1-kicker", "#s1-hero", "#s1-char", "#s1-glow"], { opacity: 1, x: 0, y: 0, scale: 1 })`
  - Card rows are rendered immediately (`bodyAt = 0.05`).
  - Only the chip animates in at `0.65s` to provide motion punctuation.
- Result: Frame 0 is a pristine, publication-ready cover poster.
