#!/usr/bin/env bash
# scenes.sh — every scene in the reel, reproducibly, in one file.
#
# WHY THIS EXISTS: in a fresh chat the fastest way to break a build is to "just make one scene" by hand.
# Regenerating is safe: nothing is hand-tuned inside a composition (that is what the token block is for),
# so this file is the single source of the picture. Edit it, re-run it, re-render.
#
# THE SHAPE OF A GOOD SET
#   * one scene per VO section, same order as sections.json
#   * field must differ from the previous scene (prepare.py fails if it does not)
#   * a different pose in every scene, matched to the beat
#   * archetype by beat: card-led = proof, stat-led = a number, type-led = a statement
#   * hero 1-3 words, chip 3-6 words, the card carries the detail
#   * scene 1 is the cover (new_scene sets data-cover="1"), so it must look finished at frame 0
set -e
cd "$(dirname "$0")"
NS="python3 scripts/new_scene.py --force"

# ---- replace everything below with your own beats -------------------------------------------------
$NS --n 1 --name hook     --arch card-led --field accent     --pose p1_shrug.png \
    --kicker "ai for college students" --hero "same resume?" --chip "har company mein bhej rahe ho?" \
    --card-title "applied / 12 companies" --card-meta "this week" --card-body @components/file-list.html

$NS --n 2 --name problem  --arch card-led --field ground     --pose p2_facepalm.png \
    --kicker "isiliye reject" --hero "customize karo" --chip "job ke according" \
    --card-title "job description / keywords" --card-meta "matched 3 of 7" --card-body @components/keyword-chips.html

$NS --n 3 --name tool     --arch type-led --field ink        --pose p3_present.png \
    --kicker "ye website try karo" --hero "rezi ai" --chip "free tool" \
    --line1 "resume tailor" --line2 "ats score checker"

$NS --n 4 --name intro    --arch card-led --field secondary  --pose p4_chin.png \
    --kicker "ai for college students" --hero "rezi.ai" --chip "the website" \
    --card-title "rezi.ai" --card-meta "live" --card-body @components/browser.html

$NS --n 5 --name upload   --arch card-led --field quaternary --pose p8_point.png \
    --kicker "pehla step" --hero "resume upload" --chip "bas apna resume" \
    --card-title "step 1 / upload" --card-meta "pdf, docx" --card-body @components/upload.html

$NS --n 6 --name jd       --arch card-led --field accent     --pose p5_memory.png \
    --kicker "dusra step" --hero "jd paste karo" --chip "job description" \
    --card-title "step 2 / paste jd" --card-meta "razorpay" --card-body @components/jd-paste.html

$NS --n 7 --name tailor   --arch card-led --field tertiary   --pose p9_idea.png \
    --kicker "ai karta hai baaki" --hero "tailor" --chip "us job ke according" \
    --card-title "tailor result" --card-meta "3 keywords added" --card-body @components/match-meter.html

$NS --n 8 --name ats      --arch stat-led --field secondary  --pose p6_thumbs.png \
    --kicker "bonus check" --hero "ats score" --chip "score dekho" --digits 94 \
    --support "keywords add karo, score dekho, dobara check karo"

$NS --n 9 --name cta      --arch card-led --field accent     --pose p7_cta.png \
    --kicker "comment karo — resume" --hero "main dm kar dunga" --chip "follow kar lena" \
    --card-title "comments / 214" --card-meta "link in bio" --card-body @components/comment-dm.html

# ---- always last: tokens into every composition, then the root ------------------------------------
python3 scripts/prepare.py
python3 scripts/build_index.py
