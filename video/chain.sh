#!/bin/bash
cd "$(dirname "$0")"
# attend la fin du rendu 9:16 (1800 images, plus aucun processus de rendu), évite l'encodage redondant, puis ajoute le domaine
until [ "$(ls final_port | wc -l)" -ge 1800 ] && ! pgrep -f "render.js seq" >/dev/null; do sleep 5; done
pkill -f final.sh; pkill ffmpeg; sleep 2
./add_url.sh juicecraft.fr
echo CHAIN_DONE
