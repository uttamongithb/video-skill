# Concept-Driven Animation Guide for Explainer Videos

This reference guide teaches agents how to parse **ANY educational or technical voiceover script** and automatically pair it with synchronized, topic-accurate motion graphics and diagrams (such as Tor Onion routing, API request/response cycles, database caching, Git branching, or system architecture).

---

## 1. Core Principle: Visual Matching to Spoken Content

Every scene in a concept video must provide **dual reinforcement**:
1. **Typographic Anchor (Left / Top)**: High-impact Swiss poster typography summarizing the concept with punchy kickers, stacked headlines, and rectangular keyword badges.
2. **Dynamic Animated Graphic (Right / Center)**: An animated diagram, network flow, terminal, or architecture stack that visually demonstrates what the narrator is explaining in real time.

> [!IMPORTANT]
> Never use generic filler graphics or floral ornaments for technical explainers. Every visual element must directly illustrate the technical mechanism described in the voiceover.

---

## 2. The 6 Visual Archetypes

When parsing a script beat, map the concept to one of these 6 archetypes:

### Archetype 1: Network & Pipeline Flow (`network_flow`)
- **Use Cases**: Tor routing, HTTP request/response, OAuth handshakes, microservice event queues, CI/CD pipelines.
- **Visual Structure**:
  - Horizontal or curved SVG path connecting sequential nodes (`User` → `ISP` → `Entry Relay` → `Middle Relay` → `Exit Relay` → `Website`).
  - Animated traveling data packet (`offset-path` or GSAP path motion) carrying concentric encryption layers.
  - Nodes light up and update their status tags as the packet passes through them.
- **Pre-built Component**: [`resources/components/network_flow.html`](../resources/components/network_flow.html)

### Archetype 2: Terminal & CLI Execution (`terminal_window`)
- **Use Cases**: Coding tutorials, shell commands, penetration testing, configuration files, Git commands.
- **Visual Structure**:
  - Sleek dark macOS/Linux terminal with traffic-light buttons and window title.
  - Animated typing command with blinking cyan/white cursor (`@keyframes cursorBlink`).
  - Color-coded execution outputs (green success checks, yellow warnings, red highlights).
- **Pre-built Component**: [`resources/components/terminal_window.html`](../resources/components/terminal_window.html)

### Archetype 3: Layered Architecture Stack (`architecture_stack`)
- **Use Cases**: Multi-layer encryption, OSI model, clean architecture, tech stacks, onion routing layers.
- **Visual Structure**:
  - Vertical stacked cards with colored accent borders (`Outer Shell`, `Middle Shield`, `Inner Core`).
  - Staggered slide-in animations revealing each layer's role.
- **Pre-built Component**: [`resources/components/architecture_stack.html`](../resources/components/architecture_stack.html)

### Archetype 4: Side-by-Side Comparison (`comparison_split`)
- **Use Cases**: Normal Web vs. Tor, HTTP vs. HTTPS, SQL vs. NoSQL, Client-side vs. Server-side.
- **Visual Structure**:
  - Split canvas with two contrasting cards.
  - Left: Unprotected/Conventional flow (red accents, visible data leakage).
  - Right: Secure/Modern flow (green accents, end-to-end encrypted).

### Archetype 5: Metrics & Benchmarks (`stat_bars`)
- **Use Cases**: Speed tests, latency comparisons, privacy ratings, adoption statistics.
- **Visual Structure**:
  - Animated progress bars (`scaleX` tween), numeric counters, or radar rings.

### Archetype 6: Hero Keyword & Conceptual Focus (`hero_editorial`)
- **Use Cases**: Hook questions, milestone announcements, summaries, strong calls to action.
- **Visual Structure**:
  - Massive bold editorial headline with prominent rectangular color badges, clean dark canvas.

---

## 3. Case Study: Tor Onion Routing Explainer

### Spoken Script Breakdown & Visual Mapping

| Timestamp | Voiceover Line | Typographic Focus | Visual Archetype & Graphic Content |
| :--- | :--- | :--- | :--- |
| **0.0s - 3.5s** | "Internet par kuch bhi browse karte ho, to tumhara ISP sab dekhta hai!" | Kicker: `#PRIVACY ALERT`<br>Headline: `TUMHARA ISP SAB`<br>Badge: `[DEKHTA HAI]` | Direct connection: User Laptop → Red glowing beam directly into ISP Surveillance database. |
| **3.5s - 8.0s** | "Lekin Tor Network request ko 3 alag-alag relays ke through bhejta hai." | Kicker: `#THE SOLUTION`<br>Headline: `TOR SENDS DATA`<br>Badge: `[3 ENCRYPTED RELAYS]` | Archetype 1 (`network_flow`): User → ISP → Guard Relay → Middle Relay → Exit Relay. |
| **8.0s - 14.0s** | "Pehle Entry Guard ko jata hai, jise sirf tumhara IP pata hai par destination nahi." | Kicker: `#STEP 1`<br>Headline: `ENTRY RELAY`<br>Badge: `[KNOWS IP ONLY]` | Packet reaches Guard node. Outer green encryption layer is peeled off. |
| **14.0s - 20.0s** | "Fir Middle Relay ko, jise na tumhara IP pata hai na website ka!" | Kicker: `#STEP 2`<br>Headline: `MIDDLE RELAY`<br>Badge: `[TOTAL ISOLATION]` | Packet moves to Middle Relay. Yellow middle layer peeled off. |
| **20.0s - 26.0s** | "Aur finally Exit Relay request ko destination website tak pahunchata hai!" | Kicker: `#STEP 3`<br>Headline: `EXIT RELAY`<br>Badge: `[DELIVERS REQUEST]` | Packet arrives at Exit Relay. Final red layer unwrapped, plain request reaches website. |
| **26.0s - 30.0s** | "Aise hi tech concepts ko simplify karne ke liye follow kar lena!" | Kicker: `#LEARN TECH`<br>Badge: `[FOLLOW]`<br>Headline: `FOR MORE DEEP DIVES!` | Minimalist Obsidian Dark CTA screen with glowing cyan/green tech accents. |

---

## 4. Script Tagging Directives for Agents

When generating scripts, agents can explicitly tag visual components using the `@visual:` directive:

```text
# PRIVACY HOOK
NORMAL BROWSING MEIN
[ISP SAB DEKHTA HAI]
@visual: comparison
---
# HOW IT WORKS
TOR USES 3 RELAYS
[ENTRY -> MIDDLE -> EXIT]
@visual: network_flow
---
# STEP 1
GUARD RELAY ONLY KNOWS
[YOUR IP ADDRESS]
@visual: architecture_stack
---
# COMMAND
RUN TOR SOCKS PROXY
[PORT 9050]
@visual: terminal
---
# CTA
FOR MORE DEEP DIVES
[FOLLOW]
KAR LENA!
@visual: hero_editorial
```
