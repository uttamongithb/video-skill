# REEL-FROM-SCRIPT · v7

A skill for making a 9:16 reel that looks art-directed and cannot come out broken — from a script you did not
write, a reference you have to reverse-engineer, and a fresh chat with no memory of the last one.

v5 shipped layouts and hardcoded the design into them. v6 moved every number into `PARAMS.json` and put a
validator in front of the render. **v7 is what two real reels taught v6** — the six-colour field cycle, the
cover poster, per-scene card animation, contiguous scene spans, adaptive wipes, the audio traps, and a single
`./build.sh` + `scripts/qc.py` that refuses to hand over a bad deliverable.

> **The promise:** the only file a human edits is `PARAMS.json`. The only thing allowed to say *no* is
> `prepare.py` / `qc.py`. Everything else is generated, and every generated thing is reproducible from one
> command.

---

## 0 · If you are new here: the first 10 minutes

```bash
export PATH=/home/user/node22/bin:$PATH        # Node >= 22
cd <project> && ./build.sh --from render        # or follow §3 from the top
```

Then read, in this order: §1 (how the look is built) → §3 (the pipeline) → §6 (design playbook) →
§9 (failure catalogue). Do not invent a layout: the skeleton is the design.

**Never do these four things:** type a duration (measure the VO), paste a hex or a px into a composition
(change `PARAMS.json`), hand-write `index.html` (generate it), or ship without looking at the contact sheet.

---

## 1 · Why the output looks designed (the seven laws)

These are the actual decisions behind every good frame in this series. They are rules, not taste.

**1. One anchor grid, bottom-fixed.** Kicker → hero → body → **chip** → **presenter**. The bottom half never
moves: the chip always sits at the same y, the presenter is always cropped by the frame at the same place.
Only the top half re-composes. That is why nine different scenes read as one film.

**2. The hero is a word, not a sentence.** 1–3 words, set in a condensed display face at ~17–25 % of the frame
width, tight line-height (0.88). The full line goes in the **chip** (3–6 words, the thing a muted viewer reads),
the detail goes in the **card**. If you can't say it in 3 words, the beat is two beats.

**3. Every beat gets a different background.** Six fields (cream / maroon / near-black / sage / navy / lavender)
cycled so no two neighbours match. The colour change *is* the transition's other half. `prepare.py` fails the
build if two scenes in a row share a field.

**4. Proof, not decoration.** A card exists to show the thing: a file list, a diff, a browser, an upload, a
meter. If a beat has no artefact, it is `type-led` and has no card. A card with two rows in it looks broken;
four to six rows looks deliberate (or a mockup filling ≥ 55 % of the card).

**5. The first frame is a poster.** Scene 1 is composed at t=0 (`data-cover="1"`): kicker, hero, card and
character already on screen, chip landing at 0.65 s. A reel that opens on an empty field loses the scroll.

**6. Motion is transform only, and it lands early.** Entrances are 0.24–0.34 s, `power2/3/4.out`, and they
finish in the first half of the beat. Never animate text content, never tween a number, never let a 1.5 s scene
spend 0.6 s wiping. A slow drift on the hero keeps the final second alive.

**7. Sound is punctuation, not wallpaper.** ≤ 1 cue per second: a pop on every cut, key ticks on UI, a riser on
the two biggest turns, a chime on the reveal, a notify/ping on the CTA. Bed at 0.15 under a −16 LUFS VO;
master −14 LUFS / ≤ −1 dBTP.

---

## 2 · The contract: what is fixed, what is yours

**Invariant — validated, not editable by vibes**

| Invariant | Enforced by |
|---|---|
| Every text/background pair readable | WCAG ≥ 4.5:1 on 10 rendered pairs + 6 field pairs |
| Hero is a hero and always fits | ≥ 120 px, derived size, must fit `--hero-lines` in `--hero-band` |
| Hero clears the kicker, never touches the card | derived band + `--gap`, hard fail |
| Body copy readable on a phone | ≥ 24 px and ≥ `bodyMin` |
| Nothing hides under platform UI | chip bottom ≤ safe-zone bottom, ≥ 55 % usable |
| Chip can never collide with the card | `cardTop + cardHmax ≤ chipTop` |
| Presenter cropped by the frame, never over the chip | `presenterTop + h > 1.0`, `presenterTop ≥ chipBottom` |
| Two scenes in a row never share a field | `data-field` read from every composition |
| Frame 0 is a cover | `data-cover` + a snapshot gate |
| A different pose in every scene | one pose file per scene, checked at review |
| Deliverable is playable and loud enough | `qc.py`: resolution, fps, frames, LUFS, true peak, silent holes |

**Variable — genuinely yours:** palette values (6 fields + 4 paper tones, contrast permitting) · format
(9:16, 4:5, 1:1, 720p) · safe-zone insets · every grid and type ratio inside the floor · archetype per scene ·
scene count · words · duration · pose set · cue sheet · fonts on disk.

If you want a layout the validator cannot check, you change the skeleton **and** add the check. That is the
price of the freedom, and it is why the output cannot be bad.

---

## 3 · The pipeline (order is not negotiable)

| # | Step | Command | Why here |
|---|---|---|---|
| 0 | **Reverse-engineer the reference** | §4 | you cannot match a look you have not measured |
| 1 | Facts | — | a claim that arrives late forces a re-record |
| 2 | Script → sections | `assets/vo/sections.json` | one idea per beat, 1.2–9 s |
| 3 | **VO first** | `python3 scripts/process_vo.py` | `timeline.json` is the clock; the picture is cut to it |
| 4 | Look | `PARAMS.json` | palette, format, grid, type floor |
| 5 | **Gate** | `python3 scripts/prepare.py` | fails on contrast / type / collision / field rhythm |
| 6 | Scenes | `./scenes.sh` | one `new_scene.py` call per beat, tokens injected |
| 7 | Root | `python3 scripts/build_index.py` | contiguous spans, adaptive wipes, no hand-typed index.html |
| 8 | Lint | `npx --yes hyperframes@0.9.19 lint` | **0 errors is a gate** |
| 9 | Look at it | `npx … snapshot --at "0,1.5,4,…"` | the only step that catches "correct but ugly" |
| 10 | Render | `npx … render --output renders/_raw.mp4` | ~1 m 45 s for 32 s at 1080×1920, software GL |
| 11 | Mix | `python3 scripts/mix_audio.py` | VO + bed + cues → `renders/master.wav` (−14 LUFS) |
| 12 | Mux + deliver | `build.sh` step 6–7 | mp4 + `.srt` + thumbs, then `qc.py` |

`./build.sh` runs 3 → 12 in one go. `./build.sh --from render` skips the VO when it is already measured.

### Step 3 in detail — VO is the clock

```bash
# one clip per section, named vo1.mp3 … voN.mp3 in assets/vo/
python3 scripts/process_vo.py
```

It trims silence, applies `atempo` **only if** `script_target` is set, loudnorms each take to −16 LUFS, then
writes `assets/vo/timeline.json`: start/dur/end per section + `root_duration`. Nothing downstream is allowed to
know a duration that is not in this file.

Write `say` in Devanagari with English tech words in Latin (`resume`, `job description`, `ATS score`, `DM`) — a
hi-IN voice gets the prosody right and still says the English words. `caption` is what the `.srt` shows.

### Step 7 in detail — the root is mechanical

`build_index.py` finds `compositions/s*.html` in numeric order, reads the measured spans, makes them
**contiguous** (0 → cut → cut → … → root, so no black hole appears where the VO has a 0.30 s gap), fires a
wipe 0.36 s before each cut in the colour of the arriving scene, and holds the last scene through the audio
tail. A wipe is shortened to 34–62 % of a short scene's length — a 1.4 s scene cannot hold a 0.62 s wipe.

### Step 11 in detail — the two audio traps

* `alimiter` has `level=true` **by default**: it auto-levels back up to the ceiling, so your "limiter" becomes a
  compressor + make-up gain and the mix lands at −12.5 LUFS while you aim at −14. Always `level=false`.
* `loudnorm` in one linear pass overshoots. Measure with `ebur128`, move by exactly `target − measured`, then
  limit. Arithmetic you can verify beats a filter that guesses.

---

## 4 · Phase 0 — reverse-engineering a reference video

When the brief is "watch this and match it", measure it. Ten minutes, five commands:

```bash
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate,codec_type -of default=nw=1 ref.mp4
ffmpeg -i ref.mp4 -vf "fps=1,scale=400:-1,tile=6x6" -frames:v 1 sheet.jpg      # the whole film as one image
python3 - <<'P'                                                                 # the field palette, per second
from PIL import Image; import glob
for f in sorted(glob.glob("frames/f_*.jpg"))[::2]:
    im = Image.open(f).convert("RGB"); w,h = im.size
    print(f[-7:-4], im.getpixel((3,3)), im.getpixel((w-4,3)))
P
ffmpeg -i ref.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav                  # for the script
```

Read out of that: **duration and cut rhythm** (how long each beat is), **the field palette** (sample corners,
not the middle), **type behaviour** (condensed caps? word-by-word builds? highlight boxes?), **layout**
(where the character sits, where the text block sits), **UI artefacts** (which mockups), **sound** (cue
density). Those six numbers are the whole art direction.

If the brief gave you a reference but no script, the reference *is* the script: transcribe the audio
(`faster-whisper`, int8, `base` model → ~7 s for 32 s of Hinglish) and read the on-screen copy off the frames.
Do not rewrite the copy — a series has a voice.

**Translate, don't copy.** The reference here was 1280×720; the deliverable was 1080×1920. Same palette, same
type, same mockups — but the hero band, chip anchor and presenter crop were re-derived as ratios. In 9:16 the
reference's 8–10 word blocks fall below the 24 px body floor, so the copy is split differently: hero 1–3 words,
chip the line, card the detail.

---

## 5 · Files

```
PARAMS.json                      the only design file
tokens.css                       generated receipt (do not edit)
index.html                       generated by build_index.py (do not edit)
SKILL.md · COMPONENTS.md · README.md
build.sh                         the whole pipeline
scenes.sh                        every scene, reproducibly
components/                      7 card bodies you can pass with --card-body @…
compositions/
  _scene-base.html.tmpl          THE skeleton — zero literal hex, zero literal px
  wipe.html                      the only transition
  sN-*.html                      generated by new_scene.py
  _examples/                     three worked scenes (not mounted: build_index only reads compositions/s*.html)
scripts/
  process_vo.py                  VO → timeline.json
  prepare.py                     the gate: floor + token injection
  new_scene.py                   base template → a correct scene
  build_index.py                 timeline + scenes → root
  mix_audio.py                   VO + bed + cues → master.wav
  make_deliverables.py           .srt + thumbs
  qc.py                          one command, PASS/FAIL on 10 gates
  cutout.py · gen_sfx.py         assets
assets/{fonts,presenter,vo,sfx,music}/
```

---

## 6 · Design playbook (what to actually choose)

**Beat → archetype.** Proof → `card-led`. A number → `stat-led` (odometer, `--digits`). A statement, a
transition, a brand card → `type-led`. Hook and CTA are almost always `card-led` because both need an artefact
(the file list that proves the problem; the comment thread that proves the CTA).

**Beat → field.** Alternate warm and cool; never repeat. A practical cycle for six fields:
`accent → ground → ink → secondary → tertiary → quaternary`. Dark fields (`ink`, `tertiary`) make the presenter
vanish, so the halo goes 0.20 → 0.42 there (the skeleton does this from `data-field`); use them for the tool
reveal and the "AI does the work" beat, where the drama helps.

**Beat → pose.** Same character, same outfit, one pose per scene, matched to the emotion of the line:
shrug (a question) · facepalm (the problem) · present (the offer) · chin (curious) · memory (recall) ·
thumbs (the win) · point (a step) · idea (the aha) · CTA (the ask). Generate a missing pose from the base image
and matte it with `cutout.py`; keep the white ground rule and mid-thigh crop so they cut out cleanly.

**Words on screen.** Hero: the emotional verb or the number (`SAME RESUME?`, `CUSTOMIZE KARO`, `TAILOR`,
`ATS SCORE`). Chip: the sentence a muted viewer needs (`har company mein bhej rahe ho?`). Card title: what the
artefact is (`applied / 12 companies`). Card meta: a small true fact (`this week`, `matched 3 of 7`).

**When a beat is too short to design (1–2 s).** Keep the scene, drop the second layer: hero + chip + presenter,
`type-led`, one reveal. Do not squeeze a card and a staggered list into 1.4 s — it reads as a glitch.

**When a beat is long (8–9 s, usually the CTA).** Stage three reveals 1.8–2 s apart (comment → DM → link) and
let a slow drift carry the tail. An 8 s static frame is the single most common "it looks cheap" cause.

**Transitions.** One wipe, 0.34–0.62 s, colour = the arriving scene's field, alternating direction. No other
transition type: consistency is what makes eight cuts feel authored.

**The last second.** The final frame must be a designed frame with the handle and the site on it — the viewer
who pauses there should be able to act.

---

## 7 · Audio playbook

| Moment | Cue | Gain |
|---|---|---|
| every cut | `pop` | 0.50 |
| the two biggest turns | `riser` 0.3 s before the cut | 0.28–0.30 |
| a UI element landing | `click`, `key` | 0.38–0.45 |
| a list ticking in | `key` ×N, 0.12 apart | 0.40 |
| a reveal / score | `chime` | 0.36–0.42 |
| CTA | `notify`, then `ping` 1.7 s later | 0.32–0.40 |
| wrong / rejected | `error` (sparingly — it reads as comedy only once) | 0.30 |

Cue **offsets are section-relative** in `assets/sfx/cues.json` (`"vo7+1.68"`), so a re-recorded VO does not
invalidate the design. Never land a cue on a word's first syllable; a tick belongs 20–60 ms *after* the visual.

### 7.1 The bed — how the track is chosen, and how it is set

The bed is not "background music". It covers the gaps between cues so the reel never sounds like a slideshow,
and it is the one element that can destroy a VO. Choose in this order, five minutes:

1. **Instrumental only.** Any vocal competes with the narrator, and a 32 s reel has no room to duck around it.
2. **Loop-safe texture** — the same 1–2 bar idea running through the whole track. A build, a drop or a key
   change cannot be looped under nine beats; you will hear the seam on the third loop.
3. **Mid-tempo, ~90–120 BPM, thin top end.** The cut rhythm and the cue sheet supply the rhythm; busy hats and
   arpeggios turn 37 cues into noise.
4. **Neutral-to-dark mood.** Triumphant or comic music argues with a flat Hinglish delivery.
5. **A licence you can name.** CC0 or CC-BY with an author to credit. The bed used here is
   incompetech.com — Kevin MacLeod, CC-BY (*Neon Laser Horizon*, *Voltaic*); freepd.com is the fallback.
   Credit in every caption (§10) — this is a legal requirement, not a courtesy.
6. **Audition it under the VO, never solo.** Play VO1 + the bed at 0.15 and ask one question: can I hear every
   consonant? If not, the bed loses, not the VO.

Then set it — these are measured, not taste:

| Knob | Value | What it actually means |
|---|---|---|
| `bed.volume` | **0.15** (= −16.5 dB) | this track is −12.5 LUFS raw → **−29.0 LUFS** in the mix, i.e. **≈13 LU under the −16 LUFS VO** |
| target gap | −28…−30 LUFS effective | re-measure if you change the track (`ffmpeg -i bed.mp3 -af "volume=0.15,ebur128" -f null -`); do not carry 0.15 over blind |
| `cues` bus | **0.20** (= −14 dB) | the pop on each cut sits ~25 dB above the bed, so a cut reads as an event without a duck |
| `fadeIn` / `fadeOut` | **0.8 s / 1.6 s** | the outro fade must *finish* before the file ends; a cut-off tail is the giveaway |
| looping | `-stream_loop -1` + trim to `ROOT_DUR` | `mix_audio.py` does this; keep `PARAMS.audio.tail` ≥ 1.15 s so the fade has somewhere to land |
| ducking | **none** | at a 13 LU gap a sidechain is inaudible and only adds pumping — the level is the duck |

---

## 8 · QC gates — what to look at, in this order

`python3 scripts/qc.py renders/final.mp4` runs the mechanical half. The other half is eyes:

1. **Frame 0** — is it a poster? (`snapshot --at 0`)
2. **The contact sheet** — 9 panels: a different pose in each, no two fields alike, one line of type per idea.
3. **Collisions** — nothing touching the chip, no hero on the kicker, no card over the presenter.
4. **Fit** — every card's last row visible; no clipped chip; no orphan word on its own line.
5. **Dead frames** — no black gap at a cut, no blank final second.
6. **The rendered file** (not the snapshot): `-ss` five frames across the film and look at them.
7. **Audio** — `ffmpeg -ss T -t 1 -i final.mp4 -af volumedetect -f null -` at each scene: no window under −45 dB.
8. **Sync** — does the cut land within ~0.1 s of the VO's first syllable for that beat?

Mechanical gates (all must be PASS): quality floor · lint 0 errors · resolution · fps · frames = duration ·
−14 LUFS ±0.5 · true peak ≤ −1.0 dBTP · no silent holes.

**Accepted lint warnings** (do not "fix"): `line_unread` on odometer strips · `container_overflow` on the
presenter/halo (the crop is the design) · `canvas_overflow` on digit strips. Never accept
`first_frame_empty`, `missing_local_asset`, or a `timeline_id_mismatch`.

---

## 9 · Failure catalogue (symptom → cause → fix)

| Symptom | Cause | Fix |
|---|---|---|
| Black gap at a cut, or a black lead-in | each mount covered only its VO section | `build_index.py` makes spans contiguous and starts scene 1 at 0 |
| Frame 0 is empty | entrances start at 0.04–0.5 s | `data-cover="1"` on scene 1 composes it at t=0 (card rows included) |
| Chip's dot sits on its first letter | `--chip-pad` misshero, a card and the character
- [ ] every scene: a different pose, a chip, a field that differs from its neighbour
- [ ] no card under half full; no clipped row; no hero touching the kicker or the card
- [ ] the last second is a designed CTA frame with handle + site
- [ ] `qc.py` → all gates PASS (1080×1920 · 30 fps · frames = duration · −14 LUFS · ≤ −1 dBTP · no holes)
- [ ] `.srt` cues all ≥ 0.62 s and not split mid-phrase
- [ ] `REVIEW.md` lists every deviation from the reference, with the measured number
