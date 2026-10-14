export const meta = {
  name: 'juicecraft-ad-sound',
  description: 'Compose and master the synced 15 s soundtrack + SFX for the juicecraft ad',
  phases: [
    { title: 'Compose', detail: 'synthesize music + sound design from the cue sheet (numpy/scipy)' },
    { title: 'QA', detail: 'measure loudness, peaks, sync of transients; fix and re-render' },
  ],
}

const CUES = '/home/user/juicecraft/video/cues.json'
const DIR = '/home/user/juicecraft/video/audio'

phase('Compose')
const comp = await agent(`You are a senior sound designer and music producer making the soundtrack for a 15-second premium advertising spot for "juicecraft", a French studio that builds custom websites ("des sites qui ont du jus" — websites with juice). The visuals are slick motion design: kinetic typography, glossy liquid juice (orange / berry / mango), a website being squeezed like a fruit, UI demos. Your audio must feel like a top-tier agency spot: tight, punchy, modern, warm, "juicy" — NOT chiptune, NOT 8-bit, NOT cheesy stock music.

INPUT: read the cue sheet ${CUES} (sections with music direction + timed SFX list). Every SFX transient and every musical section boundary must land within ±5 ms of its cue time. Tempo 120 BPM, 4/4, beat = 0.5 s; bar 1 starts at t=0.

DELIVERABLES (write into ${DIR}/):
1. make_audio.py — a single self-contained Python 3 script (numpy + scipy only; both are installed) that synthesizes everything procedurally and writes the files below. It must be deterministic (fixed RNG seeds). Structure it with clear functions: oscillators, envelopes, filters, each instrument, each SFX type, the arrangement, the mix bus, the master.
2. soundtrack.wav — 48 kHz, stereo, 24-bit PCM, EXACTLY 15.000 s (720000 samples).
3. stems/ music.wav and sfx.wav (same format) so the mix can be rebalanced later.
4. spectrogram.png — a spectrogram + waveform overview (matplotlib may not be installed; if not, pip install matplotlib, or draw it with PIL) with the cue times marked as vertical lines.

SOUND QUALITY REQUIREMENTS (these are what separate pro from amateur):
- Band-limited oscillators (PolyBLEP saw/square or additive) — no aliasing fizz. Detuned unison (3–7 voices) + stereo spread for pads/stabs.
- Proper ADSR envelopes with exponential curves; no clicks: every sound starts/ends with ≥1–2 ms fades.
- Filters: scipy.signal butter/sosfilt, and for sweeps process in short blocks with smoothly interpolated cutoff (or a TPT state-variable filter in numpy) — filter-sweep riser, lowpassed plucks.
- Kick: sine with fast pitch envelope (~150 Hz → 45 Hz), click transient, slight saturation. Clap: layered filtered noise bursts (3 micro-hits ~10 ms apart) + short reverb. Hats: high-passed noise, short, offbeats, small velocity variation.
- Sub bass in F minor following the chord roots (F, Db, Ab, Eb — one per bar of 2 s from the drop at 3.0 s), sidechain-ducked by the kick (classic pump).
- Chord stabs / plucks: warm, slightly detuned, lowpassed, with tasteful reverb send. A short memorable 3–4 note "juicy" motif is welcome.
- Riser 1.5→3.0 s: white-noise filter sweep + pitch-rising tone, ending in a hard cut at ~2.98 s, then the DROP at 3.0.
- SFX palette: "pop" (short sine blip with fast pitch drop + tiny noise click), "sad_blip" (downward slide, deflating), whooshes (bandpassed noise with moving center freq + stereo pan movement), heavy_impact (sub thump + noise crunch + short room), squish_splash (wet: modulated filtered noise + bubbly sine "bloops" with rising pitch), drop_impact (big: sub boom + noise burst + bright bloop), liquid_whoosh, notif_pop (bright two-partial blip, pitches rising in thirds/fifths over the 3 cues), swish, clicks, whir_up (rising tone), ding (bell: inharmonic partials, exponential decay), lock_clack (metallic: short resonant bandpassed noise bursts, two hits), typing (14 soft key clicks with slight random timing/pitch), result_pop, big_whoosh, ticks, drip_fall (falling pitch pluck/whistle), final_hit (huge: sub boom + impact + bright chord), soft_pop.
- Reverb: Schroeder/Freeverb-style network or convolution with a synthetic exponentially-decaying stereo noise IR (~1.2–2.5 s for the final hit). Keep the groove section fairly dry and punchy.
- Arrangement per the cue sheet: HOOK sparse and tense (no drums), riser, DROP at 3.0 with full groove, light build with an arp in 11.0–12.5, drums stop at 12.5, reverse swell 12.5→13.0, FINAL HIT at 13.0 with long ring-out, silence (fade) by 14.95 s.
- Mix: SFX must cut through the music (they are the sync points the viewer feels) — duck the music by 2–4 dB under the big SFX. Music bus and SFX bus summed, gentle glue compression, soft saturation, then a lookahead brickwall limiter.
- Master: integrated loudness ≈ −14 LUFS (implement the ITU-R BS.1770 K-weighting + gating measurement yourself in numpy, or pip install pyloudnorm), true-peak ≤ −1.0 dBTP (check with 4× oversampling). No DC offset. No clipping.

Run the script, verify the output duration and sample rate with python (and ffprobe), look at your spectrogram.png with the Read tool to sanity-check that the structure matches the cue sheet (silence/sparse intro, riser, drop at 3 s, stop at 12.5 s, final hit at 13 s, decay). Iterate until it is genuinely good.

Return a short report: file paths, measured LUFS and true peak, and a bullet list of what each section contains.`, { label: 'composer', phase: 'Compose' })

phase('QA')
const qa = await agent(`You are the mastering engineer and QA lead for a 15-second ad soundtrack. A composer has produced ${DIR}/make_audio.py which renders ${DIR}/soundtrack.wav (+ stems/ and spectrogram.png) from the cue sheet ${CUES}. The composer's report:
---
${comp}
---
Audit it rigorously and FIX anything that fails, by editing make_audio.py and re-running it (never hand-edit the wav). Checks — measure each one with code, don't eyeball:
1. Format: 48 kHz, stereo, 24-bit PCM, exactly 720000 samples.
2. Loudness: integrated ≈ −14 LUFS (±1 LU) per ITU-R BS.1770-4 (pip install pyloudnorm if needed to cross-check); true peak ≤ −1.0 dBTP measured with 4× oversampling; no sample at or above full scale; DC offset < 0.001.
3. Sync: compute an onset envelope (e.g. spectral flux on the SFX stem and on the full mix) and confirm a clear transient within ±5 ms of each cue time for the percussive cues (pop, sad_blip, heavy_impact, drop_impact, notif_pop, swish, click, ding, lock_clack, result_pop, tick, final_hit, soft_pop) and the kick grid starting exactly at 3.000 s. Report the measured offset for each cue in a table.
4. Structure: no kick before 3.0 s; riser ends with a hard cut right before 3.0; drums absent after 12.5 s; final hit at 13.0; level below −60 dBFS for the last 30 ms (clean end, no truncation click).
5. Artifacts: no clicks/pops at note boundaries (look for sample-to-sample jumps far above the local RMS), no aliasing (spectrogram shouldn't show fold-back mirror lines), no harsh resonances; stereo image sane (correlation > 0 overall, mono-compatible low end below 120 Hz).
6. Musical quality: read the code critically as a producer. If anything is likely to sound cheap (raw naive sawtooth, unenveloped noise, clap that is a single noise burst, flat dynamics, SFX buried under the music), improve it.
Re-render after fixes, regenerate spectrogram.png, view it with the Read tool, and re-run all measurements.

Return a final report: what you measured before/after, the sync table, what you changed, and final file paths.`, { label: 'mastering-qa', phase: 'QA' })

return { compose: comp, qa }
