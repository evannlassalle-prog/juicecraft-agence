#!/bin/bash
cd "$(dirname "$0")"
export VIDEO_HTML=video30.html AD_URL=juicecraft.fr
rm -f final30.done final30.fail
for spec in "16x9 1920 1080 land" "9x16 1080 1920 port"; do
  set -- $spec; name=$1; W=$2; H=$3; fmt=$4; dir=final30_$fmt
  rm -rf $dir; mkdir -p $dir
  # frames 0 .. 9.7 s are identical to the 15 s cut: reuse them
  for i in $(seq 0 1163); do ln -s "$PWD/final_$fmt/$(printf %05d $i).png" "$dir/$(printf %05d $i).png"; done
  pids=()
  for seg in "9.7 14.775" "14.775 19.85" "19.85 24.925" "24.925 30"; do
    set -- $seg
    node render.js seq $W $H $dir 60 2 $1 $2 > $dir.log_$1 2>&1 &
    pids+=($!)
  done
  for p in "${pids[@]}"; do wait $p; done
  n=$(ls $dir | wc -l)
  if [ "$n" -ne 3600 ]; then echo "frames manquantes: $n" > final30.fail; exit 1; fi
  ./encode30.sh $dir 60 2 audio/soundtrack30.wav out/juicecraft_pub_30s_$name
done
echo OK > final30.done
