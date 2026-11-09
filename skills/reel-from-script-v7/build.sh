#!/usr/bin/env bash
# build.sh — the whole pipeline, in the only order that works. Stop at the first red step.
#
#   python3 scripts/process_vo.py    VO -> assets/vo/timeline.json (measured; the picture is cut to this)
#   ./scenes.sh                      scenes + tokens + root
#   npx hyperframes lint             must be 0 errors
#   npx hyperframes render           960 frames at 1080x1920
#   python3 scripts/mix_audio.py     VO + bed + cues -> renders/master.wav  (-14 LUFS)
#   ffmpeg mux                       picture + master -> renders/final.mp4
#   python3 scripts/qc.py            the gate; exits non-zero if the deliverable is not acceptable
#
# Usage:  ./build.sh                 full build
#         ./build.sh --from render   skip the VO stage (already measured)
set -euo pipefail
cd "$(dirname "$0")"

export PATH="${NODE_BIN:-/home/user/node22/bin}:$PATH"
export TMPDIR="${TMPDIR:-/home/user/tmp}"
mkdir -p "$TMPDIR" renders

OUT="renders/final.mp4"

if [[ "${1:-}" != "--from" ]]; then
  echo "== 1/7 VO"; python3 scripts/process_vo.py
fi
echo "== 2/7 scenes"; ./scenes.sh

echo "== 3/7 lint"; npx --yes hyperframes@0.9.19 lint | tee /tmp/hf-lint.log
grep -q "0 errors" /tmp/hf-lint.log || { echo "STOP: lint errors"; exit 1; }

echo "== 4/7 render"; npx --yes hyperframes@0.9.19 render --output renders/_raw.mp4

echo "== 5/7 mix";  python3 scripts/mix_audio.py

echo "== 6/7 mux"
ffmpeg -y -v error -i renders/_raw.mp4 -i renders/master.wav -map 0:v -map 1:a \
       -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"

echo "== 7/7 deliverables + QC"
python3 scripts/make_deliverables.py "$OUT"
python3 scripts/qc.py "$OUT"
