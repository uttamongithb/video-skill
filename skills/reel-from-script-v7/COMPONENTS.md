# COMPONENTS — the card bodies, as files you can pass straight to a scene

A card is the proof of a beat: a file list, a keyword match, a browser, an upload, a JD, a match meter, a
comment thread. They live in `components/` as real HTML so a scene is one command, not a copy-paste session:

```bash
python3 scripts/new_scene.py --n 4 --name intro --arch card-led --field secondary --pose p4_chin.png \
  --kicker "the website" --hero "rezi.ai" --chip "live" \
  --card-title "rezi.ai" --card-meta "live" --card-body @components/browser.html
```

## The rules every component follows

1. **No literal colours, no literal pixel sizes.** Only `var(--token)` and `calc()` against tokens. That is what
   makes a palette change a one-file edit.
2. **No element is visible at rest** (`opacity: 0`), and one `<script>` block reveals them. The block pushes a
   function onto the per-scene tween queue — it runs after the scene timeline exists:
   ```html
   <script>
   window.__sceneTweens = window.__sceneTweens || [];
   window.__sceneTweens.push(function (tl) { tl.fromTo(".row", {...}, {...}, .45); });
   </script>
   ```
3. **Never animate text content.** Animate `transform` and `opacity` only — a counter written from the timeline
   freezes on the first frame. Numbers are odometer strips (`--digits`) or a static figure.
4. **Fill the card.** 4–6 rows, or a mockup that occupies ≥ 55 % of the card height. A card with one line reads
   as broken. If the beat has no proof, use `type-led` instead and delete the card.
5. **Content must fit `--card-h`.** The card clips at `max-height`. If a row disappears, shorten the copy —
   never shrink type below `--size-body`.

## Catalogue

| File | Use it when the line is… | Reveal rhythm |
|---|---|---|
| `file-list.html` | …about the same thing being sent everywhere ("same resume, 12 companies") | rows tick in, 0.12 stagger |
| `keyword-chips.html` | …about what a job wants vs what you have | chips pop 0.07 apart, caption last |
| `browser.html` | …introducing a website (URL bar, headline, CTA button) | url → h1 → sub → button |
| `upload.html` | …"upload / paste / drop a file" | dropzone → progress fill → "ready" |
| `jd-paste.html` | …a job description, a role, requirements | role block slides, bullets stagger |
| `match-meter.html` | …a score, a match, before/after | bar grows, rows stagger, number static |
| `comment-dm.html` | …the CTA (comment → DM → link) | bubble 1 → bubble 2 (+1.85 s) → link pill |

## Card chrome you get for free

`new_scene.py` wraps the body in the standard card: `paper` surface, ink border, hard offset shadow, a title bar
(`--card-title` left, `--card-meta` right, mono, uppercase) and `.body` padding. Inside, these variables are
already on the stack and are all you should need:

`--size-body` · `--size-hero` · `--bar-gap` · `--card-pad` · `--card-radius` · `--border-w` ·
`--paper` `--paper-ink` `--paper-muted` `--paper-bar` · `--ink` `--accent` `--secondary` `--on-accent` ·
`--font-display` `--font-slab` `--font-mono`

## Writing a new one

Copy the nearest file, change the copy, keep the reveal block. Then check it the way everything else is
checked — `prepare.py` for the floor, a snapshot for the fit:

```bash
npx --yes hyperframes@0.9.19 snapshot --at "<scene start + 1.5>"
```
