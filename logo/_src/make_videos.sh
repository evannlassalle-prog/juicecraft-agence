#!/bin/bash
set -e
cd "$(dirname "$0")"; A=../animation; F=/tmp/lf; mkdir -p $F
enc_mp4() { ffmpeg -y -loglevel error -framerate 60 -i "$1/%04d.png" -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart "$2"; }
# 1) fond sombre 16:9
node render_anim.js juicecraft_logo-anime_fond-sombre.svg $F/dark 1920 1080 0.58 "#131116" 60 3.6
enc_mp4 $F/dark $A/juicecraft_logo-anime_fond-sombre_1920x1080.mp4
# GIF (depuis les mêmes images)
ffmpeg -y -loglevel error -framerate 60 -i "$F/dark/%04d.png" -vf "fps=30,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 $A/juicecraft_logo-anime_fond-sombre_960px.gif
# 2) fond clair 16:9
node render_anim.js juicecraft_logo-anime_fond-clair.svg $F/light 1920 1080 0.58 "#F2F2EF" 60 3.6
enc_mp4 $F/light $A/juicecraft_logo-anime_fond-clair_1920x1080.mp4
# 3) icône seule, carré 1080 sur encre
node render_anim.js juicecraft_logo-anime_icone.svg $F/icon 1080 1080 0.36 "#131116" 60 3.2
enc_mp4 $F/icon $A/juicecraft_logo-anime_icone_1080x1080.mp4
# 4) transparents (pour monter par-dessus ses propres images)
for v in fond-clair fond-sombre; do
  node render_anim.js juicecraft_logo-anime_$v.svg $F/t_$v 1920 1080 0.58 transparent 60 3.6
  ffmpeg -y -loglevel error -framerate 60 -i "$F/t_$v/%04d.png" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 22 -auto-alt-ref 0 $A/juicecraft_logo-anime_${v}_transparent.webm
  ffmpeg -y -loglevel error -framerate 60 -i "$F/t_$v/%04d.png" -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -vendor apl0 $A/juicecraft_logo-anime_${v}_transparent_ProRes4444.mov
done
echo VIDEOS_OK
