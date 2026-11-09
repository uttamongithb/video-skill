# Animation, Transitions & Pacing Guide for Viral Tech Reels

This reference guide establishes the motion design standards, scene transition catalog, dynamic SVG particle/packet flows, and strict audio-timing synchronization rules for high-retention technical explainers.

---

## 1. Strict Target Duration & Audio Speed Scaling (The 60-Second Rule)

### The Problem
Raw Text-to-Speech (TTS) engines speak at a relaxed conversational tempo (~110–120 words per minute). A 160-word script will naturally take **90–95 seconds** if uncalibrated, causing viewer drop-off. Modern technical reels and shorts require an energetic, punchy delivery of **160–180 words per minute** and must adhere strictly to the creator's target duration (e.g., exactly 60.0 seconds).

### The Solution: Pitch-Preserving Audio Tempo Scaling
When script annotations contain target time ranges (e.g., `0–7 sec`, `7–16 sec`, `16–27 sec`, `27–42 sec`, `42–50 sec`, `50–60 sec`), the agent must calculate the required speed factor per scene:

$$\text{tempo\_factor} = \frac{\text{raw\_audio\_duration}}{\text{target\_duration}}$$

Using FFmpeg's `atempo` audio filter, speed is increased with **zero pitch alteration** (no chipmunk effect):

```bash
# Example: Scaling a 12.9s raw audio file into a punchy 7.0s hook window
ffmpeg -y -i raw_hook.mp3 -filter:a "atempo=1.843" -vn scene1_hook_7s.mp3
```

> [!TIP]
> If `atempo > 2.0`, FFmpeg requires chaining multiple filters (e.g., `atempo=1.5,atempo=1.45`), because a single `atempo` filter operates between `0.5` and `2.0`.

---

## 2. Dynamic Scene Transition Catalog

Never jump cut between major scenes on a technical reel. Use purposeful, high-energy transitions that carry visual momentum:

| Transition Name | Mechanism | When to Use | Code Recipe (GSAP / CSS) |
| :--- | :--- | :--- | :--- |
| **1. Horizontal Push Slide** | Outgoing scene slides left (`x: -100%`), Incoming scene slides in from right (`x: 0%`) simultaneously. | Transitioning between sequential pipeline steps or locations. | `transform: translateX(100% -> 0%)` with `cubic-bezier(0.16, 1, 0.3, 1)` |
| **2. Camera Push-In / Zoom** | Outgoing scene zooms in (`scale: 1.0 -> 1.3, opacity: 0`); incoming scene arrives from `scale: 0.85 -> 1.0`. | Stepping deeper inside a concept (e.g., zooming from network overview into internal encryption layers). | `.scene-zoom-in { animation: zoomIn 0.45s ease-out; }` |
| **3. Terminal Glitch Flash** | 2-frame white strobe flash (`opacity: 0.8 -> 0`) paired with horizontal slice displacement. | Transitioning into a live terminal, code execution, or hacking sequence. | `@keyframes glitchFlash { 0% { filter: invert(1); } 100% { filter: invert(0); } }` |
| **4. Scale-Swap Morph** | Central visual container compresses down to `scale: 0.9` then springs open as the new interface at `scale: 1.0`. | Transitioning between two dashboard cards or architecture diagrams. | `ease: "back.out(1.5)"`, duration: `0.35s` |
| **5. Vertical Curtain Wipe** | Solid contrast panel wipes vertically (`translateY(100% -> 0% -> -100%)`). | Major chapter breaks (e.g. Moving from problem explanation to solution reveal). | `clip-path: inset(0 0 0 0)` to `clip-path: inset(100% 0 0 0)` |

---

## 3. High-Energy Topic Animations (E.g. Tor Onion Routing)

Static cards are forbidden. Technical components must exhibit continuous, reactive motion:

### A. The 3-Layer Onion Packet Flow
In network routing explainers, data packets must visually reflect their cryptographic state:
1. **Packet Anatomy**:
   - Concentric SVG rings: Outer Green (`Guard Key`), Middle Yellow (`Middle Key`), Inner Red (`Exit Key`).
   - Center payload: Glowing data token.
2. **Layer Stripping Animation**:
   - As the packet reaches **Node 1 (Guard)**, the outer green ring expands and dissolves (`scale: 1.8, opacity: 0`), leaving only 2 layers.
   - As it reaches **Node 2 (Middle)**, the yellow ring expands and pops off, leaving only 1 layer.
   - As it reaches **Node 3 (Exit)**, the final red shell unwraps, revealing the raw cyan HTTP packet that enters the website!
3. **Motion Path**:
   - The packet travels along an SVG bezier path (`offset-path: path(...)`) with animated glowing trails behind it.

### B. Reactive Node Lighting
Nodes along the path must react in real time:
- **Idle State**: Muted border (`#334155`), opacity `0.6`.
- **Active / Receiving State**: Border flares bright (`box-shadow: 0 0 30px rgba(56, 189, 248, 0.8)`), node scales up to `1.08`.
- **Processed / Decrypted State**: Checkmark badge activates (`✓ LAYER DECRYPTED`), status changes from `WAITING` to `TRANSMITTING`.

### C. Live Terminal Execution
For terminal and code scenes:
- Commands type in character-by-character with a realistic staggered cadence.
- Blinking block cursor (`@keyframes cursorBlink 0.7s infinite`).
- Real-time status lines append below with green checkmarks (`[✓] Handshake with Guard: 185.220.101.5`).

---

## 4. Typography Choreography & Kinetic Text

- **Word-by-Word Active Glow**: Important keyword badges spring in with a `scale: 0.85 -> 1.08 -> 1.0` elastic snap.
- **Masked Slide-Up**: Every text line remains strictly masked (`overflow: hidden`), entering with a snappy `0.25s - 0.35s` slide up.
- **Kicker Stagger**: The small tracking kicker arrives 100ms before the headline stack to anchor the eye.
