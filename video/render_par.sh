#!/bin/bash
# usage: render_par.sh W H outdir fps sub procs
W=$1; H=$2; OUT=$3; FPS=$4; SUB=$5; NP=${6:-4}
cd "$(dirname "$0")"; mkdir -p "$OUT"
seg=$(python3 -c "print(15.0/$NP)")
pids=()
for ((k=0;k<NP;k++)); do
  a=$(python3 -c "print(round($k*$seg,6))"); b=$(python3 -c "print(round(($k+1)*$seg,6))")
  node render.js seq $W $H "$OUT" $FPS $SUB $a $b > "$OUT.log$k" 2>&1 &
  pids+=($!)
done
for p in "${pids[@]}"; do wait $p; done
cat "$OUT".log*; ls "$OUT" | wc -l
