#!/usr/bin/env python3
"""
make_deliverables.py — captions + thumbnails, derived from the same timeline.json that cuts the picture.

A caption can never describe a frame that is not there. Cue rules learned from three iterations of hand
written .srt files: one cue per phrase, never split mid-phrase, never a cue under 0.62 s, <= 2 lines of
38 characters, and pad 0.06 s inside the VO so the text is already up when the word starts.

Usage: python3 scripts/make_deliverables.py [renders/final.mp4]
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TL = json.loads((ROOT / "assets/vo/timeline.json").read_text())
SPEC = json.loads((ROOT / "assets/vo/sections.json").read_text())
VID = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "renders/REZI-AI-resume-tailor-1080x1920.mp4"
if not VID.is_absolute():
    VID = ROOT / VID
STEM = VID.stem
CAPTION = {s["id"]: s.get("caption") or s.get("on_screen") or "" for s in SPEC["sections"]}


def wrap(text, width=38):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cue_split(text, start, end, min_dur=0.62):
    dur = end - start
    if dur < 2.4 or len(text) < 46:
        return [(start, end, text)]
    cuts = [i for i, ch in enumerate(text) if ch in ",."]
    if not cuts:
        return [(start, end, text)]
    pivot = min(cuts, key=lambda i: abs(i - len(text) // 2))
    a, b = text[:pivot + 1].strip(), text[pivot + 1:].strip()
    if len(a) < 12 or len(b) < 12:
        return [(start, end, text)]
    split_t = round(start + dur * len(a) / (len(a) + len(b)), 2)
    return [(start, max(split_t, start + min_dur), a),
            (min(split_t + 0.04, end - min_dur), end, b)]


def ts(t):
    h, r = divmod(max(0.0, t), 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


cues = []
for sec in TL["sections"]:
    text = CAPTION[sec["id"]]
    if not text:
        continue
    for a, b, part in cue_split(text, sec["start"] + 0.06, sec["end"] - 0.06):
        cues.append((a, b, part))

srt = [f"{i}\n{ts(a)} --> {ts(b)}\n" + "\n".join(wrap(part)) + "\n" for i, (a, b, part) in enumerate(cues, 1)]
out = ROOT / "renders" / f"{STEM}.srt"
out.write_text("\n".join(srt))
print(f"SRT : {len(cues)} cues -> {out.name}")

if VID.exists():
    (ROOT / "renders/thumbs").mkdir(parents=True, exist_ok=True)
    for name, vf in [("thumb_9x16.jpg", None), ("thumb_16x9.jpg", "scale=1280:-2,crop=1280:720")]:
        cmd = ["ffmpeg", "-y", "-v", "error", "-ss", "0.6", "-i", str(VID), "-frames:v", "1"]
        if vf:
            cmd += ["-vf", vf]
        subprocess.run(cmd + [str(ROOT / "renders/thumbs" / name)], check=True)
    print("THUMBS: 9:16 + 16:9")
else:
    print(f"THUMBS: skipped (no {VID.name})")
