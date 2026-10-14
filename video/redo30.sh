#!/bin/bash
# re-render only 16.0 s -> 25.0 s (S8 texte + S9 prix), puis ré-encodage
cd "$(dirname "$0")"
export VIDEO_HTML=video30.html AD_URL=juicecraft.fr RESUME=1
rm -f redo30.done redo30.fail
for spec in "16x9 1920 1080 land" "9x16 1080 1920 port"; do
  set -- $spec; name=$1; W=$2; H=$3; fmt=$4; dir=final30_$fmt
  pids=()
  for seg in "16.0 18.25" "18.25 20.5" "20.5 22.75" "22.75 25.0"; do
    set -- $seg
    node render.js seq $W $H $dir 60 2 $1 $2 > redo_${fmt}_$1.log 2>&1 &
    pids+=($!)
  done
  for p in "${pids[@]}"; do wait $p; done
  n=$(ls $dir | wc -l)
  if [ "$n" -ne 3600 ]; then echo "frames manquantes: $n" > redo30.fail; exit 1; fi
  ./encode30.sh $dir 60 2 audio/soundtrack30.wav out/juicecraft_pub_30s_$name
done
echo OK > redo30.done
