#!/bin/bash
cd "$(dirname "$0")"
set -e
for fmt in "16x9 1920 1080 land" "9x16 1080 1920 port"; do
  set -- $fmt
  rm -rf final_$4; ./render_par.sh $2 $3 final_$4 60 2 4 | tail -3
  ./encode.sh final_$4 60 2 audio/soundtrack.wav out/juicecraft_pub_$1
done
echo ALL_DONE
