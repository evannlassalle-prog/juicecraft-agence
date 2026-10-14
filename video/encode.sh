#!/bin/bash
# usage: encode.sh framesdir fps sub audio.wav out_basename
# sub=2 -> 2 sub-frames per output frame are averaged (180° shutter motion blur)
D=$1; FPS=$2; SUB=$3; AUD=$4; OUT=$5
IN_RATE=$((FPS*SUB))
if [ "$SUB" -gt 1 ]; then
  W="1"; for ((k=1;k<SUB;k++)); do W="$W 1"; done
  BLUR="tmix=frames=$SUB:weights='$W',select='eq(mod(n\,$SUB)\,$((SUB-1)))',setpts=N/$FPS/TB,"
else BLUR=""; fi
VF="${BLUR}scale=out_color_matrix=bt709:out_range=tv:flags=lanczos+accurate_rnd+full_chroma_int,format=yuv420p"
COL="-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv"
AUDARGS=(); [ -f "$AUD" ] && AUDARGS=(-i "$AUD" -map 0:v -map 1:a -c:a aac -b:a 320k -ar 48000)
# master: high quality
ffmpeg -y -loglevel error -framerate $IN_RATE -i "$D/%05d.png" "${AUDARGS[@]}" -vf "$VF" -r $FPS \
  -c:v libx264 -preset slow -crf 15 -profile:v high -level 4.2 $COL -movflags +faststart -t 15 "${OUT}_master.mp4"
# web/social: lighter file
ffmpeg -y -loglevel error -framerate $IN_RATE -i "$D/%05d.png" "${AUDARGS[@]}" -vf "$VF" -r $FPS \
  -c:v libx264 -preset slow -crf 20 -maxrate 14M -bufsize 28M -profile:v high -level 4.2 $COL -movflags +faststart -t 15 "${OUT}.mp4"
for f in "${OUT}_master.mp4" "${OUT}.mp4"; do
  ffprobe -v error -show_entries format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,pix_fmt,color_space -of compact "$f"
done
