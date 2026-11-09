#!/usr/bin/env python3
"""prepare.py — the mechanism that makes a flexible skill safe.

1. VALIDATES PARAMS.json against the quality floor (contrast, type floor, safe zone, palette, density).
   Hard failures exit non-zero. Nothing renders until this passes.
2. WRITES the token block into every composition between the @tokens markers, so palette and grid
   live in exactly one place and no composition can drift from the series.

Usage:  python3 scripts/prepare.py [--check-only]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = json.loads((ROOT / "PARAMS.json").read_text())

fails, warns = [], []


def hex2rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = lum(hex2rgb(a)), lum(hex2rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


W, H = P["format"]["w"], P["format"]["h"]
SHORT = min(W, H)
pal, grid, typ = P["palette"], P["grid"], P["type"]

# ---------------------------------------------------------------- palette
for k in ("ground", "ink", "accent", "secondary", "tertiary", "quaternary",
          "paper", "paperInk", "paperMuted", "paperBar"):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", pal.get(k, "")):
        fails.append(f"palette.{k} is not a #RRGGBB hex")
for name in pal["fieldCycle"]:
    if name not in pal:
        fails.append(f"fieldCycle references unknown colour '{name}'")
cyc = pal["fieldCycle"]
if len(cyc) > 1 and any(cyc[i] == cyc[(i + 1) % len(cyc)] for i in range(len(cyc))):
    fails.append("fieldCycle repeats a colour back-to-back")

# text pairs that actually occur on screen -> WCAG
PAIRS = [("ink", "ground"), ("ink", "secondary"), ("onAccent", "accent"), ("onInk", "ink"),
         ("onTertiary", "tertiary"), ("ink", "quaternary"),
         ("paperInk", "paper"), ("paperMuted", "paper"), ("paperInk", "paperBar"),
         ("onInk", "ink"), ("ink", "paper"), ("paper", "ink")]
def resolve(name):                     # palette values may be an alias to another key ("onInk": "ground")
    v = pal.get(name, "")
    return pal[v] if v in pal else v


for fg, bg in PAIRS:
    if fg in pal and bg in pal:
        c = contrast(resolve(fg), resolve(bg))
        if c < 4.5:
            (fails if c < 3.0 else warns).append(f"contrast {fg} on {bg} = {c:.2f}:1 (floor 4.5)")

# text that sits on each background field — the field cycle is only legal if every combination reads
FIELD_FG = {"ground": "ink", "accent": "onAccent", "ink": "onInk", "secondary": "ink",
            "tertiary": "onTertiary", "quaternary": "onQuaternary"}
FIELD_CHIP = {"ground": ("ink", "onInk"), "accent": ("ink", "onInk"),
              "ink": ("accent", "onAccent"), "secondary": ("ink", "onInk"),
              "tertiary": ("ground", "ink"), "quaternary": ("ink", "onInk")}
for field, fg in FIELD_FG.items():
    c = contrast(resolve(fg), resolve(field))
    if c < 4.5:
        (fails if c < 3.0 else warns).append(f"text {fg} on a {field} scene = {c:.2f}:1 (floor 4.5)")
    bg, fg2 = FIELD_CHIP[field]
    c2 = contrast(resolve(fg2), resolve(bg))
    if c2 < 4.5:
        (fails if c2 < 3.0 else warns).append(f"chip {fg2} on {bg} over a {field} scene = {c2:.2f}:1")

# ---------------------------------------------------------------- type
hero_min_px = typ["heroMin"] * W
hero_max_px = typ["heroMax"] * W
body_px = typ["bodyMin"] * SHORT
if hero_min_px < 120:
    fails.append(f"heroMin = {hero_min_px:.0f}px — a hero word below 120px reads as body copy")
if hero_max_px > 0.34 * W:
    fails.append(f"heroMax = {hero_max_px:.0f}px — above 34% of width it clips")
if body_px < 24:
    fails.append(f"bodyMin = {body_px:.0f}px — below 24px is unreadable on a phone")
for f in typ["files"].values():
    if not (ROOT / f).exists():
        warns.append(f"font file missing: {f} (text will silently fall back to DejaVu)")

# ---------------------------------------------------------------- safe zone / grid
usable_top = P["safeZone"]["top"]
usable_bottom = 1 - P["safeZone"]["bottom"]
if usable_bottom - usable_top < 0.55:
    fails.append("safeZone leaves less than 55% of the frame usable")
chip_bottom = grid["chipTop"] + grid["chipH"]
if chip_bottom > usable_bottom:
    fails.append(f"chip ends at {chip_bottom:.3f} but the safe zone ends at {usable_bottom:.3f} "
                 f"— it will sit under the platform UI")
if grid["cardTop"] + grid["cardHmax"] > grid["chipTop"]:
    fails.append("card overlaps the chip — the bottom half must stay fixed")
pres_bottom = grid["presenterTop"] + grid["presenterHmax"]
if P["presenter"]["enabled"] and pres_bottom < 1.0 and P["presenter"]["cropByFrame"]:
    fails.append(f"presenter ends at {pres_bottom:.3f}: cropByFrame is on, so it must exceed 1.0")
if P["presenter"]["enabled"] and grid["presenterTop"] < chip_bottom - 1e-3:
    fails.append("presenter starts above the chip — they will collide")

# ---------------------------------------------------------------- vertical stack (derived, not trusted)
# heroTop and hero size are two independent ratios, but they must physically agree: the hero has to
# clear the kicker above it and fit in the band above the card. Rather than trusting the numbers,
# derive what actually fits and only fail when even the smallest legal hero cannot.
kicker_px = typ["kicker"] * W
kicker_bottom = grid["kickerTop"] * H + kicker_px * 1.95      # cap height + ascender + breathing room
fix = "--fix" in sys.argv
if grid["heroTop"] * H < kicker_bottom - 0.5:
    need = (kicker_bottom + 2) / H
    if fix:
        grid["heroTop"] = round(need, 4)
        warns.append(f"heroTop raised to {grid['heroTop']} so the hero clears the kicker "
                     f"(run without --fix to make this permanent in PARAMS.json)")
    else:
        fails.append(f"heroTop {grid['heroTop']} puts the hero at {grid['heroTop']*H:.0f}px, "
                     f"inside the kicker (which ends at {kicker_bottom:.0f}px) — "
                     f"set grid.heroTop >= {need:.4f} or run with --fix")

gap_px = grid.get("gap", 0.02) * H          # the hero band stops short of the card: no touching boxes
avail_h = (grid["cardTop"] * H - grid["heroTop"] * H - gap_px) * 0.94   # 6% slack for Anton descenders
lh = typ["lineHeight"]
hero_max_px = typ["heroMax"] * W
# prefer the largest size that still fits two lines; fall back to one line if two would go under the floor
hero_lines, hero_px = 2, min(hero_max_px, avail_h / (2 * lh))
if hero_px < typ["heroMin"] * W:
    hero_lines, hero_px = 1, min(hero_max_px, avail_h / lh)
if hero_px < typ["heroMin"] * W:
    fails.append(f"only {avail_h:.0f}px of band between the kicker and the card — that allows a "
                 f"{hero_px:.0f}px hero, below the {typ['heroMin']*W:.0f}px floor. "
                 f"Raise grid.cardTop or lower grid.heroTop.")
if hero_px < 120:
    fails.append(f"derived hero is {hero_px:.0f}px — under 120px it stops being a hero")
if avail_h <= 0:
    fails.append("cardTop is above heroTop — the card is eating the hero band")

# ---------------------------------------------------------------- archetype
if P["archetype"] not in ("auto", "card-led", "type-led", "stat-led"):
    fails.append("archetype must be auto | card-led | type-led | stat-led")

# ---------------------------------------------------------------- field cycle (read from the scenes)
scene_files = sorted(f for f in (ROOT / "compositions").glob("s*.html") if f.name != "wipe.html")
fields = []
for f in scene_files:
    m = re.search(r'data-field="([a-z]+)"', f.read_text())
    if not m:
        warns.append(f"{f.name}: no data-field attribute — wipe colour falls back to 'ink'")
        fields.append(None)
    else:
        fields.append(m.group(1))
        if m.group(1) not in FIELD_FG:
            fails.append(f"{f.name}: data-field='{m.group(1)}' is not one of {', '.join(FIELD_FG)}")
for i in range(len(fields) - 1):
    if fields[i] and fields[i] == fields[i + 1]:
        fails.append(f"{scene_files[i].name} and {scene_files[i+1].name} share the field '{fields[i]}' "
                     f"— two scenes in a row on the same background read as one long scene")
if len(set(f for f in fields if f)) < 2 and len(fields) > 1:
    warns.append("every scene uses the same field colour — the reel has no visual rhythm")


# ---------------------------------------------------------------- report
print(f"format   {W}x{H} @ {P['format']['fps']}fps · platform {P['format']['platform']}")
print(f"safe     y {usable_top:.3f} - {usable_bottom:.3f}  ({int(usable_bottom*H-usable_top*H)}px usable)")
print(f"type     hero {hero_px:.0f}px / {hero_lines} line(s) in a {avail_h:.0f}px band "
      f"(bounds {hero_min_px:.0f}-{hero_max_px:.0f}) · body floor {body_px:.0f}px · chip {typ['chip']*W:.0f}px")
for fg, bg in PAIRS:
    if fg in pal and bg in pal:
        print(f"contrast {fg}/{bg:<12} {contrast(resolve(fg), resolve(bg)):.2f}:1")

for w in warns:
    print(f"  WARN  {w}")
for f in fails:
    print(f"  FAIL  {f}")
if fails:
    print(f"\n{len(fails)} hard failure(s) — fix PARAMS.json before building.")
    sys.exit(1)

# ---------------------------------------------------------------- write tokens
def px(v, base=W):
    return f"{v * base:.1f}px"


card_h = (grid["cardHmin"] + grid["cardHmax"]) / 2
pres_h = (grid["presenterHmin"] + grid["presenterHmax"]) / 2

tokens = f"""/* @tokens:start — generated by scripts/prepare.py from PARAMS.json. Do not edit by hand. */
:root {{
  --w: {W}px; --h: {H}px;
  --ground: {pal['ground']}; --ink: {pal['ink']};
  --accent: {pal['accent']}; --secondary: {pal['secondary']};
  --tertiary: {pal['tertiary']}; --quaternary: {pal['quaternary']};
  --on-ink: {resolve('onInk')}; --on-accent: {resolve('onAccent')};
  --on-tertiary: {resolve('onTertiary')}; --on-quaternary: {resolve('onQuaternary')};
  --paper: {pal['paper']}; --paper-ink: {pal['paperInk']}; --paper-muted: {pal['paperMuted']}; --paper-bar: {pal['paperBar']};
  --font-display: "{typ['display']}"; --font-slab: "{typ['slab']}"; --font-mono: "{typ['mono']}";

  --margin-x: {px(grid['marginX'])};
  --kicker-top: {px(grid['kickerTop'], H)};
  --hero-top: {px(grid['heroTop'], H)};
  --card-top: {px(grid['cardTop'], H)};
  --card-w: {px(grid['cardW'])};
  --card-h: {px(card_h, H)};
  --card-radius: {grid['cardRadius']}px;
  --chip-top: {px(grid['chipTop'], H)};
  --chip-h: {px(grid['chipH'], H)};
  --chip-radius: {grid['chipRadius']}px;
  --chip-pad: {W * 0.0352:.1f}px;
  --presenter-top: {px(grid['presenterTop'], H)};
  --presenter-h: {px(pres_h, H)};
  --presenter-x: {px(grid['presenterX'])};

  --size-hero: {hero_px:.0f}px;
  --odo-step: {hero_px:.0f}px;  /* one digit cell = 1em at --size-hero, so '5em' is exactly 5 digits */
  --hero-lines: {hero_lines};          /* how many lines fit — do not exceed */
  --hero-band: {avail_h:.1f}px;
  --gap: {gap_px:.2f}px;
  --size-hero-max: {hero_max_px:.0f}px;
  --size-kicker: {typ['kicker']*W:.1f}px;
  --size-chip: {typ['chip']*W:.1f}px;
  --size-body: {body_px*1.0:.1f}px;
  --lh-display: {typ['lineHeight']};
  --tracking-label: {typ['trackingLabel']}em;
  --halftone: {grid['halftone']};
  /* chrome — derived from W so a 4:5 or 720x1280 render keeps the same proportions.
     Not in PARAMS.json: nobody should be hand-tuning these. */
  --border-w: {W * 0.00278:.1f}px;
  --dot-pitch: {W * 0.00648:.1f}px;
  --dot-r: {max(1.0, W * 0.00102):.2f}px;
  --bar-h: {W * 0.0574:.1f}px;
  --bar-pad: {W * 0.0204:.1f}px;
  --bar-gap: {W * 0.0130:.1f}px;
  --card-pad: {W * 0.0222:.1f}px;
  --dash-w: {W * 0.0426:.1f}px;
  --dash-h: {W * 0.00463:.1f}px;
  --dash-gap: {W * 0.0167:.1f}px;
  --glow: {W * 0.648:.1f}px;
  --glow-alpha: 0.20;
  --hard-shadow: {grid['hardShadow']};
  --safe-top: {usable_top * 100:.2f}%;
  --safe-bottom: {usable_bottom * 100:.2f}%;
}}
/* @tokens:end */"""

if fix:
    P["grid"] = grid
    (ROOT / "PARAMS.json").write_text(json.dumps(P, indent=2) + "\n")
    print("\n--fix: PARAMS.json rewritten with the corrected values.")

if "--check-only" not in sys.argv:
    patched = 0
    for f in sorted((ROOT / "compositions").rglob("*.html")):
        s = f.read_text()
        if "@tokens:start" not in s:
            continue
        s = re.sub(r"/\* @tokens:start.*?@tokens:end \*/", tokens, s, flags=re.S)
        f.write_text(s)
        patched += 1
    (ROOT / "tokens.css").write_text(tokens.replace(":root {", ":root {", 1) + "\n")
    print(f"\nOK — tokens written into {patched} composition(s) + tokens.css")
else:
    print("\nOK — params valid (check-only, nothing written)")
