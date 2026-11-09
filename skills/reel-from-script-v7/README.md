# reel-from-script v7

A skill **plus the working files**, where the design lives in one `PARAMS.json`, a validator refuses to let it
produce a bad frame, and one command builds and checks the whole reel.

Proven on two shipped reels:
52 s · 1080×1920 · 30 fps · −14.0 LUFS (Entire / Trails) and 32 s · 1080×1920 · 30 fps · −14.0 LUFS
(Rezi AI resume tailor, rebuilt from a 16:9 reference).

```
PARAMS.json            the only design file you edit
build.sh               VO → scenes → lint → render → mix → mux → QC
scenes.sh              every scene, reproducibly
components/            7 card bodies: file-list · keyword-chips · browser · upload · jd-paste ·
                       match-meter · comment-dm
scripts/               process_vo · prepare · new_scene · build_index · mix_audio ·
                       make_deliverables · qc · cutout · gen_sfx
compositions/          _scene-base.html.tmpl (the skeleton) · wipe.html · example-*.html
assets/                fonts · 9 presenter poses · vo/sections.json · sfx/cues.json · music bed
```

## Start a new reel

```bash
export PATH=/home/user/node22/bin:$PATH

# 1. write the script, one beat per section (Devanagari for the voice, Latin for the screen)
$EDITOR assets/vo/sections.json

# 2. generate one VO clip per section -> assets/vo/vo1.mp3 … voN.mp3, then measure
python3 scripts/process_vo.py

# 3. art direction: palette, format, grid, type floor
$EDITOR PARAMS.json
python3 scripts/prepare.py --check-only        # read the report; fix what it names

# 4. one line per scene in scenes.sh, then the whole build + gate
./build.sh --from render
```

Result: `renders/final.mp4` + `.srt` + thumbs, and `scripts/qc.py` printing PASS/FAIL on ten gates.

## In a fresh chat, say this

> Read `SKILL.md` (§1 the seven laws, §3 the pipeline, §6 the design playbook). The script is in
> `assets/vo/sections.json`; the look is `PARAMS.json`. Build the scenes in `scenes.sh` using the
> components, run `./build.sh`, and do not hand over the render until `scripts/qc.py` passes and you have
> looked at the contact sheet. Here is my script: …

## The one thing to understand

`PARAMS.json` is freedom, `prepare.py` is the floor, `qc.py` is the gate. Anything that could produce an
unreadable, colliding or silent frame is checked before a frame is rendered — which is why the layout can be
completely parameterised and still never come out bad.

Seed values are measured, not invented: at 1080×1920 the grid reproduces margin 60 px, card 960×470,
chip 1128/86, presenter 1217/795 — the geometry of the shipped reels — and every value is a ratio, so
`format` → 1080×1350 re-lays the same design in 4:5.
