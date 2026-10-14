#!/bin/bash
# usage: ./add_url.sh votre-domaine.fr
# Re-rend uniquement les deux passages qui affichent l'adresse (barre d'URL 3,5-5,12 s et carte finale 12,3-15 s), puis ré-encode.
URL="$1"; [ -z "$URL" ] && { echo "usage: ./add_url.sh votre-domaine.fr"; exit 1; }
cd "$(dirname "$0")"; export AD_URL="$URL"
rr() { # dir W H from to
  local len; len=$(python3 -c "print(($5-$4)/4)"); local pids=()
  for k in 0 1 2 3; do
    a=$(python3 -c "print(round($4+$k*$len,6))"); b=$(python3 -c "print(round($4+($k+1)*$len,6))")
    node render.js seq $2 $3 $1 60 2 $a $b > /dev/null 2>&1 &
    pids+=($!)
  done
  for p in "${pids[@]}"; do wait $p; done
}
for spec in "16x9 1920 1080 land" "9x16 1080 1920 port"; do
  set -- $spec
  rr final_$4 $2 $3 3.5 5.12
  rr final_$4 $2 $3 12.3 15
  ./encode.sh final_$4 60 2 audio/soundtrack.wav out/juicecraft_pub_$1
done
echo "OK : vidéos mises à jour avec $URL"
