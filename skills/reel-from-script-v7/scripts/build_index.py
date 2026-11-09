#!/usr/bin/env python3
"""
build_index.py — writes index.html (the root document) from what is on disk.

WHY THIS EXISTS
  Hand-writing the root is where new sessions broke: a second data-composition-id in the root
  folder makes HyperFrames refuse to render ("multiple_root_compositions"), mounts drift out of
  sync with the VO, and a missing wipe leaves a black frame between scenes. The root is
  mechanical, so it is generated, never typed.

WHAT IT DOES
  1. finds compositions/s*.html  (sorted: s1, s2, ... s10 — numeric, not lexical)
  2. reads durations from assets/vo/timeline.json when it exists; otherwise splits the total
     evenly, which is only for previewing before the VO is recorded
  3. fires a wipe 0.36 s before each cut, colour = the field of the scene that is arriving
  4. writes index.html with the root mount, the scene mounts and the wipe mounts

Usage:
  python3 scripts/build_index.py                 # uses assets/vo/timeline.json
  python3 scripts/build_index.py --even 42       # preview only: 42 s split evenly
  python3 scripts/build_index.py --dry-run       # print, write nothing
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIPE_LEAD = 0.36      # wipe starts this long before the cut (measured from the delivered reel)
WIPE_DUR = 0.62
TAIL = 1.15           # picture runs this long after the last word


def die(msg: str) -> "None":
    print(f"FAIL  {msg}")
    sys.exit(1)


def nat_key(p: Path):
    m = re.match(r"s(\d+)", p.name)
    return (int(m.group(1)) if m else 999, p.name)


scenes = sorted((f for f in (ROOT / "compositions").glob("s*.html")), key=nat_key)
if not scenes:
    die("no compositions/s*.html found — copy compositions/_scene-base.html.tmpl first")

# ---- durations -------------------------------------------------------------------------------
tl_path = ROOT / "assets/vo/timeline.json"
argv = sys.argv[1:]
if "--even" in argv:
    total = float(argv[argv.index("--even") + 1])
    d = total / len(scenes)
    spans = [(i * d, (i + 1) * d) for i in range(len(scenes))]
    source = f"--even {total}s (preview timing, not the real VO)"
elif tl_path.exists():
    tl = json.loads(tl_path.read_text())
    secs = tl["sections"]
    if len(secs) != len(scenes):
        die(f"{len(scenes)} scenes on disk but {len(secs)} sections in timeline.json.\n"
            f"      Each scene must own exactly one VO section: either add the missing scene,\n"
            f"      or re-run scripts/process_vo.py so the timeline matches the picture.")
    spans = [(s["start"], s["end"]) for s in secs]
    source = f"assets/vo/timeline.json ({len(secs)} sections, root {tl['root_duration']}s)"
else:
    die("no assets/vo/timeline.json — record the VO first, or pass --even <seconds> to preview")

# ---- no blank frames between scenes ----
# The VO has 0.30 s gaps and a 0.35 s lead-in; if each mount only covered its own section the gaps
# would render as black. Scenes are contiguous: 0 -> cut -> cut -> ... -> root.
root_dur = round(spans[-1][1] + TAIL, 3)
spans = [(0.0 if i == 0 else spans[i][0], 0.0) for i in range(len(spans))]
for i in range(len(spans)):
    end = spans[i + 1][0] if i + 1 < len(spans) else root_dur
    spans[i] = (spans[i][0], round(end, 3))
if tl_path.exists() and "--even" not in argv:
    root_dur = json.loads(tl_path.read_text()).get("root_duration", root_dur)

# ---- fields (wipe colour = the field of the scene that is arriving) --------------------------
fields = []
for f in scenes:
    m = re.search(r'data-field="([a-z]+)"', f.read_text())
    fields.append(m.group(1) if m else "ink")

acc = json.loads((ROOT / "PARAMS.json").read_text())["palette"]


def colour(field: str) -> str:
    v = acc.get(field, acc["ink"])
    return acc[v] if v in acc else v


# ---- emit ------------------------------------------------------------------------------------
lines = []
lines.append('<!doctype html>')
lines.append('<html lang="en">')
lines.append('<head>')
lines.append('  <meta charset="UTF-8" />')
lines.append(f'  <meta name="viewport" content="width={acc and json.loads((ROOT / "PARAMS.json").read_text())["format"]["w"]}, '
             f'height={json.loads((ROOT / "PARAMS.json").read_text())["format"]["h"]}" />')
lines.append('  <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>')
lines.append('  <style>')
lines.append('    * { margin: 0; padding: 0; box-sizing: border-box; }')
lines.append('    html, body { overflow: hidden; background: #000; }')
lines.append('    #root { position: relative; overflow: hidden; }')
lines.append('    .host { position: absolute; inset: 0; }')
lines.append('  </style>')
lines.append('</head>')
lines.append('<body>')
fmt = json.loads((ROOT / "PARAMS.json").read_text())["format"]
lines.append(f'  <div id="root" data-composition-id="main" data-start="0" data-duration="{root_dur}" '
             f'data-width="{fmt["w"]}" data-height="{fmt["h"]}">')
lines.append('')
for i, (f, (a, b)) in enumerate(zip(scenes, spans), start=1):
    dur = round(b - a, 3)
    lines.append(f'    <!-- scene {i} · {f.name} · field {fields[i-1]} · {a:.3f}s → {b:.3f}s -->')
    lines.append(f'    <div id="host{i}" class="host" style="z-index:{i}"')
    lines.append(f'         data-composition-id="{f.stem}" data-composition-src="compositions/{f.name}"')
    lines.append(f'         data-start="{a:.3f}" data-duration="{dur}" data-width="{fmt["w"]}" data-height="{fmt["h"]}"')
    lines.append(f'         data-track-kind="graphics"></div>')
    lines.append('')
lines.append('    <!-- wipes: one before every cut, colour taken from the arriving scene -->')
for i in range(1, len(scenes)):
    scene_dur = spans[i][1] - spans[i][0]
    dur = round(min(WIPE_DUR, max(0.34, scene_dur * 0.42)), 2)   # a 1.4 s scene cannot hold a 0.62 s wipe
    lead = round(min(WIPE_LEAD, dur * 0.6), 3)
    start = round(max(0.0, spans[i][0] - lead), 3)
    flip = 1 if i % 2 == 0 else 0
    lines.append(f'    <div id="wipe{i}" class="host" style="z-index:{100 + i}"')
    lines.append(f'         data-composition-id="wipe{i}" data-composition-src="compositions/wipe.html"')
    lines.append(f'         data-variable-values=\'{{"wipe-color":"{colour(fields[i])}","flip":"{flip}"}}\'')
    lines.append(f'         data-start="{start}" data-duration="{dur}" data-width="{fmt["w"]}" data-height="{fmt["h"]}"')
    lines.append(f'         data-track-kind="graphics"></div>')
    lines.append('')
lines.append('  </div>')
lines.append('  <script>window.__timelines["main"] = gsap.timeline({ paused: true });</script>')
lines.append('</body>')
lines.append('</html>')

out = "\n".join(lines) + "\n"
if "--dry-run" in argv:
    print(out)
else:
    (ROOT / "index.html").write_text(out)
    print(f"index.html written — {len(scenes)} scene(s) + {max(0, len(scenes) - 1)} wipe(s), root {root_dur}s")
    print(f"timing source: {source}")
