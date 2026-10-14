#!/bin/bash
# re-render 22.0 s -> 25.5 s (S9 : prix sans TTC, "/mois" visible, mentions TVA et engagement), puis ré-encodage
cd "$(dirname "$0")"
export VIDEO_HTML=video30.html AD_URL=juicecraft.fr RESUME=1
rm -f redo30b.done redo30b.fail
for spec in "16x9 1920 1080 land" "9x16 1080 1920 port"; do
  set -- $spec; name=$1; W=$2; H=$3; fmt=$4; dir=final30_$fmt
  pids=()
  for seg in "22.0 23.1666667" "23.1666667 24.3333333" "24.3333333 25.5"; do
    set -- $seg
    node render.js seq $W $H $dir 60 2 $1 $2 > redo30b_${fmt}_$1.log 2>&1 &
    pids+=($!)
  done
  for p in "${pids[@]}"; do wait $p; done
  n=$(ls $dir | wc -l)
  if [ "$n" -ne 3600 ]; then echo "frames manquantes: $n" > redo30b.fail; exit 1; fi
  ./encode30.sh $dir 60 2 audio/soundtrack30.wav out/juicecraft_pub_30s_$name
done
echo OK > redo30b.done
