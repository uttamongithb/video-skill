#!/usr/bin/env python3
"""Voice-over pipeline: trim -> tempo -> loudnorm -> 48k stereo, then lay out the timeline.

The target length is NOT hardcoded here: it is read from the script's own
section timestamps (SCRIPT_START/SCRIPT_END in the caller) -> 0..52 s.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VO = ROOT / "assets" / "vo"
OUT = VO / "wav"
OUT.mkdir(parents=True, exist_ok=True)

# Sections come from assets/vo/sections.json. The target length is OPTIONAL: when the source script
# has no timestamps, the VO is simply measured and the picture is cut to it. Nothing is hardcoded.
_SPEC = json.loads((ROOT / "assets" / "vo" / "sections.json").read_text())
SCRIPT_SECTIONS = [(s["id"], s["label"], None, None) for s in _SPEC["sections"]]
TARGET = _SPEC.get("script_target")          # None -> no tempo compression at all
LEAD_IN = 0.20
TAIL = 0.70
GAP = 0.24


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"FAILED: {' '.join(cmd)}\n{p.stderr[-2000:]}")
    return p


def dur(path):
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return float(p.stdout.strip())


# ---- pass 1: trim lead/trailing silence only ---------------------------------
trimmed = {}
for name, *_ in SCRIPT_SECTIONS:
    src = VO / f"{name}.mp3"
    dst = OUT / f"{name}_trim.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af",
         "silenceremove=start_periods=1:start_silence=0.02:start_threshold=-42dB:"
         "detection=peak,areverse,"
         "silenceremove=start_periods=1:start_silence=0.02:start_threshold=-42dB:"
         "detection=peak,areverse",
         "-ar", "48000", "-ac", "2", str(dst)])
    trimmed[name] = dur(dst)

raw_sum = sum(trimmed.values())
gaps = GAP * (len(SCRIPT_SECTIONS) - 1)
if TARGET:
    budget = TARGET - gaps - LEAD_IN - TAIL
    factor = raw_sum / budget
else:
    budget = raw_sum
    factor = 1.0            # measured, not compressed: the script had no timestamps to hit

print(f"trimmed total {raw_sum:.3f}s | budget {budget:.3f}s | factor {factor:.4f}")
assert factor <= 1.40, f"speed-up {factor:.2f}x exceeds 1.40x — cut words instead"
factor = min(round(factor, 4), 1.40)

# ---- pass 2: tempo + loudness ----------------------------------------------
timeline = []
t = LEAD_IN
for name, label, s0, s1 in SCRIPT_SECTIONS:
    dst = OUT / f"{name}.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(OUT / f"{name}_trim.wav"), "-af",
         f"atempo={factor},loudnorm=I=-16:TP=-1.5:LRA=7",
         "-ar", "48000", "-ac", "2", str(dst)])
    d = dur(dst)
    timeline.append({
        "id": name, "label": label,
        "script_start": s0, "script_end": s1,
        "start": round(t, 3), "dur": round(d, 3), "end": round(t + d, 3),
        "file": f"assets/vo/wav/{name}.wav",
    })
    t = round(t + d + GAP, 3)

root_dur = round(timeline[-1]["end"] + TAIL, 3)
data = {
    "tempo_factor": factor,
    "lead_in": LEAD_IN,
    "tail": TAIL,
    "gap": GAP,
    "script_target": TARGET,
    "root_duration": root_dur,
    "sections": timeline,
}
(ROOT / "assets" / "vo" / "timeline.json").write_text(json.dumps(data, indent=2))
print(json.dumps(data["sections"], indent=1))
print(f"ROOT DURATION -> {root_dur}s" + (f" (script declares {TARGET}s)" if TARGET else " (measured from the VO)"))
