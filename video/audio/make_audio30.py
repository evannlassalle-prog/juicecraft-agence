#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
juicecraft -- "des sites qui ont du jus" -- 15 s spot soundtrack
=================================================================

Fully procedural: numpy + scipy only (matplotlib is used for the overview
plot when available, with a PIL fallback).  Deterministic: every random
source is seeded from a fixed string tag through zlib.crc32.

Outputs (next to this script):
    soundtrack.wav         48 kHz / 24-bit PCM / stereo / exactly 720 000 samples
    stems/music.wav        music bus, same format
    stems/sfx.wav          SFX bus, same format
    spectrogram.png        waveform + spectrogram + loudness, cue times marked

Signal flow
-----------
  oscillators/envelopes/filters -> instruments & SFX
    -> buses (dry + plate / room / hall / ping-pong delay sends)
  music: per-instrument kick sidechain pump, SFX-keyed ducking (2-4 dB)
  MUSIC + SFX -> HPF 22 Hz -> mono below 140 Hz -> glue compressor
             -> soft saturation (4x oversampled) -> true-peak lookahead limiter
             -> integrated loudness trim to -14 LUFS (BS.1770-4, own code)
             -> TPDF dither -> 24-bit WAV
  Stems = bus x (the exact master gain automation), so music + sfx sums
  back to the master (minus the gentle saturation colour).

Musical frame: F minor, 120 BPM, beat 0.5 s.  From the drop (3.0 s) one chord
per 2 s bar: Fm9 - Dbmaj9 - Ab(add9) - Eb(add9), back to Fm for the arp build,
Eb swell (12.5-13.0) resolving to an Ab(add9) final chord (relative major).
Signature motif: 1 - b3 - 5 (F - Ab - C), heard dark in the hook, as the
three UI notification blips, in the rising arp and (major) in the final bells.
"""
from __future__ import annotations

import json
import os
import sys
import time
import wave
import zlib

import numpy as np
from scipy import signal
from scipy.ndimage import minimum_filter1d, uniform_filter1d

# =============================================================================
# 0. GLOBALS
# =============================================================================
SR = 48_000
DUR = 30.0
N = int(round(DUR * SR))                     # 720 000 samples
BPM = 120.0
BEAT = 60.0 / BPM                            # 0.5 s
BAR = 4 * BEAT                               # 2.0 s
S16 = BEAT / 4                               # 0.125 s

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.dirname(HERE)
CUE_PATH = os.path.join(VIDEO_DIR, "cues30.json")
STEM_DIR = os.path.join(HERE, "stems")

TARGET_LUFS = -14.0
LIMIT_CEIL_DBTP = -1.25                      # limiter ceiling (spec: <= -1.0 dBTP)
CUT_T = 2.98                                 # hard cut before the drop
DROP_T = 3.0
STOP_T = 27.5                                # drums stop
FINAL_T = 28.0                               # final hit
SILENT_T = 29.95                             # silence from here
CUT2_T = 21.98                               # hard cut before the 2nd drop
DROP2_T = 22.0
BRK_T = 16.0                                 # breakdown (methode) starts

EVENT_LOG: list[dict] = []                   # for sync verification


# =============================================================================
# 1. SMALL UTILITIES
# =============================================================================
def ns(sec: float) -> int:
    """seconds -> samples (sample-accurate rounding)."""
    return int(round(sec * SR))


def tvec(n: int) -> np.ndarray:
    return np.arange(n, dtype=np.float64) / SR


def db2lin(d):
    return 10.0 ** (np.asarray(d, dtype=np.float64) / 20.0)


def lin2db(x):
    return 20.0 * np.log10(np.maximum(np.abs(x), 1e-12))


_PC = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
       "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10,
       "Bb": 10, "B": 11}


def note_hz(name: str) -> float:
    """'Ab4' -> 415.30 Hz (A4 = 440, equal temperament)."""
    pc, octave = name[:-1], int(name[-1])
    midi = 12 * (octave + 1) + _PC[pc]
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


def rng_for(tag: str) -> np.random.Generator:
    """Deterministic RNG per sound (independent of call order)."""
    return np.random.default_rng(zlib.crc32(tag.encode("utf-8")))


def norm_peak(x: np.ndarray, peak: float = 1.0) -> np.ndarray:
    m = float(np.max(np.abs(x))) if x.size else 0.0
    return x * (peak / m) if m > 0 else x


def pan_gains(p):
    """Equal-power pan; centre = unity per channel."""
    th = (np.clip(p, -1.0, 1.0) + 1.0) * (np.pi / 4.0)
    return np.cos(th) * np.sqrt(2.0), np.sin(th) * np.sqrt(2.0)


def to_stereo(x: np.ndarray, pan=0.0) -> np.ndarray:
    gl, gr = pan_gains(pan)
    if x.ndim == 2:
        return np.stack([x[0] * gl, x[1] * gr])
    return np.stack([x * gl, x * gr])


def mix_at(dst: np.ndarray, src: np.ndarray, offset_s: float, gain: float = 1.0):
    """Add src into dst at offset (seconds). Works for mono/stereo dst & src."""
    i0 = ns(offset_s)
    if i0 >= dst.shape[-1]:
        return
    m = min(src.shape[-1], dst.shape[-1] - i0)
    if dst.ndim == 2 and src.ndim == 1:
        dst[:, i0:i0 + m] += gain * src[:m]
    else:
        dst[..., i0:i0 + m] += gain * src[..., :m]


def smooth_noise(n: int, rate: float, rng: np.random.Generator) -> np.ndarray:
    """Band-limited random control signal in [-1, 1] (cosine-interpolated)."""
    m = int(np.ceil(n / SR * rate)) + 3
    pts = rng.uniform(-1.0, 1.0, m)
    x = np.arange(n) / SR * rate
    i = np.floor(x).astype(int)
    w = 0.5 - 0.5 * np.cos(np.pi * (x - i))
    return pts[i] * (1.0 - w) + pts[i + 1] * w


# =============================================================================
# 2. ENVELOPES
# =============================================================================
def fade_edges(x: np.ndarray, fin: float = 0.0015, fout: float = 0.003) -> np.ndarray:
    """Raised-cosine fade in/out (declicking). First and last samples are 0."""
    x = np.array(x, dtype=np.float64, copy=True)
    n = x.shape[-1]
    a = min(ns(fin), n // 2)
    b = min(ns(fout), n // 2)
    if a > 0:
        x[..., :a] *= 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
    if b > 0:
        x[..., n - b:] *= (0.5 - 0.5 * np.cos(np.pi * np.arange(1, b + 1) / b))[::-1]
    return x


def env_perc(n: int, attack: float = 0.002, tau: float = 0.1, hold: float = 0.0) -> np.ndarray:
    """Percussive envelope: raised-cosine attack, optional hold, exponential decay."""
    t = tvec(n)
    e = np.exp(-np.maximum(t - attack - hold, 0.0) / tau)
    if attack > 0:
        e = e * np.where(t < attack, 0.5 - 0.5 * np.cos(np.pi * t / attack), 1.0)
    return e


def adsr(n: int, a: float, d: float, s: float, r: float, gate: float) -> np.ndarray:
    """Exponential ADSR (concave attack, RC-style decay/release), gate = note-off (s)."""
    t = tvec(n)
    ka = 3.0
    a = max(a, 1e-4)
    d = max(d, 1e-4)
    r = max(r, 1e-4)
    att = (1.0 - np.exp(-ka * np.clip(t / a, 0.0, 1.0))) / (1.0 - np.exp(-ka))
    dec = s + (1.0 - s) * np.exp(-np.maximum(t - a, 0.0) * 5.0 / d)
    e = np.where(t < a, att, dec)
    if gate < a:
        lg = (1.0 - np.exp(-ka * gate / a)) / (1.0 - np.exp(-ka))
    else:
        lg = s + (1.0 - s) * np.exp(-(gate - a) * 5.0 / d)
    rel = lg * np.exp(-np.maximum(t - gate, 0.0) * 6.9 / r)
    e = np.where(t >= gate, rel, e)
    return fade_edges(e, 0.0, 0.003)


def gate_curve(points) -> np.ndarray:
    """Piecewise raised-cosine automation over the whole timeline.
    points: list of (time_s, value); holds first/last value outside."""
    g = np.empty(N)
    ts = [p[0] for p in points]
    vs = [p[1] for p in points]
    g[:ns(ts[0])] = vs[0]
    for (t0, v0), (t1, v1) in zip(points[:-1], points[1:]):
        i0, i1 = ns(t0), ns(t1)
        if i1 <= i0:
            continue
        w = 0.5 - 0.5 * np.cos(np.pi * np.arange(i1 - i0) / (i1 - i0))
        g[i0:i1] = v0 + (v1 - v0) * w
    g[ns(ts[-1]):] = vs[-1]
    return g


# =============================================================================
# 3. OSCILLATORS (band-limited)
# =============================================================================
def phase_acc(freq, n: int, ph0: float = 0.0):
    f = np.broadcast_to(np.asarray(freq, dtype=np.float64), (n,))
    inc = f / SR
    ph = ph0 + np.concatenate(([0.0], np.cumsum(inc[:-1])))
    return ph, inc


def osc_sine(freq, n: int, ph0: float = 0.0) -> np.ndarray:
    ph, _ = phase_acc(freq, n, ph0)
    return np.sin(2.0 * np.pi * ph)


def _polyblep(t: np.ndarray, dt: np.ndarray) -> np.ndarray:
    y = np.zeros_like(t)
    m = t < dt
    x = t[m] / dt[m]
    y[m] = x + x - x * x - 1.0
    m2 = t > 1.0 - dt
    x = (t[m2] - 1.0) / dt[m2]
    y[m2] = x * x + x + x + 1.0
    return y


def osc_saw(freq, n: int, ph0: float = 0.0) -> np.ndarray:
    """PolyBLEP sawtooth (alias-suppressed)."""
    ph, dt = phase_acc(freq, n, ph0)
    t = np.mod(ph, 1.0)
    return 2.0 * t - 1.0 - _polyblep(t, dt)


def osc_square(freq, n: int, ph0: float = 0.0) -> np.ndarray:
    """PolyBLEP square = difference of two half-period-offset BLEP saws."""
    ph, dt = phase_acc(freq, n, ph0)
    t1 = np.mod(ph, 1.0)
    t2 = np.mod(ph + 0.5, 1.0)
    return 0.5 * ((2 * t1 - 1 - _polyblep(t1, dt)) - (2 * t2 - 1 - _polyblep(t2, dt)))


def supersaw(freq, n: int, rng: np.random.Generator, voices: int = 5,
             detune_cents: float = 12.0, width: float = 0.8) -> np.ndarray:
    """Detuned unison saw stack with stereo spread -> (2, n)."""
    out = np.zeros((2, n))
    f = np.broadcast_to(np.asarray(freq, dtype=np.float64), (n,))
    offs = np.linspace(-1.0, 1.0, voices) if voices > 1 else np.zeros(1)
    pans = offs.copy()
    rng.shuffle(pans)                         # decorrelate pan from detune
    for i in range(voices):
        cents = detune_cents * offs[i] * (1.0 + 0.1 * rng.standard_normal())
        v = osc_saw(f * 2.0 ** (cents / 1200.0), n, rng.random())
        gl, gr = pan_gains(pans[i] * width)
        out[0] += gl * v
        out[1] += gr * v
    return out / np.sqrt(voices)


def bell(f0: float, dur: float, partials=None) -> np.ndarray:
    """Additive inharmonic bell (exp. decays per partial)."""
    if partials is None:
        partials = ((1.0, 1.0, 1.0), (1.0027, 0.35, 0.8), (2.0, 0.42, 0.5),
                    (2.756, 0.24, 0.3), (4.07, 0.12, 0.17), (5.404, 0.07, 0.09))
    n = ns(dur)
    x = np.zeros(n)
    for ratio, amp, tau in partials:
        f = f0 * ratio
        if f < 0.45 * SR:
            x += amp * osc_sine(f, n) * env_perc(n, 0.001, tau)
    return fade_edges(x, 0.001, 0.01)


def bloop(f0: float, ratio: float, rise_tau: float, amp_tau: float,
          dur: float = 0.12, h2: float = 0.15) -> np.ndarray:
    """Bubble 'bloop': sine whose pitch rises exponentially (Minnaert-like)."""
    n = ns(dur)
    t = tvec(n)
    f = f0 * ratio ** (1.0 - np.exp(-t / rise_tau))
    x = osc_sine(f, n) + h2 * osc_sine(2.0 * f, n)
    return fade_edges(x * env_perc(n, 0.0015, amp_tau), 0.001, 0.004)


# =============================================================================
# 4. FILTERS
# =============================================================================
def sos(kind: str, fc, order: int = 2):
    if np.ndim(fc):
        fc = [min(float(f), 0.45 * SR) for f in fc]
    else:
        fc = min(float(fc), 0.45 * SR)
    return signal.butter(order, fc, btype=kind, fs=SR, output="sos")


def filt(x: np.ndarray, kind: str, fc, order: int = 2) -> np.ndarray:
    return signal.sosfilt(sos(kind, fc, order), x, axis=-1)


def svf(x: np.ndarray, fc, q=0.707, mode: str = "lp") -> np.ndarray:
    """Zavalishin/Simper TPT state-variable filter with per-sample cutoff.
    Stable under fast modulation (used for every sweep in the piece)."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 2:
        return np.stack([svf(x[c], fc, q, mode) for c in range(x.shape[0])])
    n = len(x)
    fcs = np.clip(np.broadcast_to(np.asarray(fc, dtype=np.float64), (n,)), 5.0, 0.45 * SR)
    g = np.tan(np.pi * fcs / SR)
    k = 1.0 / np.broadcast_to(np.asarray(q, dtype=np.float64), (n,))
    a1 = 1.0 / (1.0 + g * (g + k))
    a2 = g * a1
    a3 = g * a2
    X, A1, A2, A3 = x.tolist(), a1.tolist(), a2.tolist(), a3.tolist()
    lp = [0.0] * n
    bp = [0.0] * n
    ic1 = ic2 = 0.0
    for i in range(n):
        v3 = X[i] - ic2
        v1 = A1[i] * ic1 + A2[i] * v3
        v2 = ic2 + A2[i] * ic1 + A3[i] * v3
        ic1 = 2.0 * v1 - ic1
        ic2 = 2.0 * v2 - ic2
        lp[i] = v2
        bp[i] = v1
    lp = np.asarray(lp)
    bp = np.asarray(bp)
    if mode == "lp":
        return lp
    if mode == "bp":
        return bp * k                         # unity gain at centre
    if mode == "hp":
        return x - k * bp - lp
    raise ValueError(mode)


def resonator(x: np.ndarray, f: float, tau: float) -> np.ndarray:
    """2-pole resonator, ~unity peak gain, ring time constant tau."""
    r = np.exp(-1.0 / (tau * SR))
    w = 2.0 * np.pi * f / SR
    b = [(1.0 - r) * 2.0 * np.sin(w)]
    a = [1.0, -2.0 * r * np.cos(w), r * r]
    return signal.lfilter(b, a, x)


# =============================================================================
# 5. TIME-BASED EFFECTS (reverb IRs, ping-pong delay)
# =============================================================================
def make_ir(rt60: float, length: float, seed: str, predelay: float = 0.012,
            hf: float = 0.45, early: int = 8, buildup: float = 0.010) -> np.ndarray:
    """Synthetic stereo IR: decorrelated noise, 5 bands each with its own
    exponential decay (HF dies faster), diffusion build-up, early reflections."""
    rng = rng_for(seed)
    n = ns(length)
    t = tvec(n)
    bands = [("lowpass", 250.0, 1.15), ("bandpass", (250.0, 1000.0), 1.0),
             ("bandpass", (1000.0, 3500.0), 0.85), ("bandpass", (3500.0, 8000.0), 0.62),
             ("highpass", 8000.0, hf)]
    ir = np.zeros((2, n))
    for c in range(2):
        z = rng.standard_normal(n)
        for kind, fc, mult in bands:
            rt = rt60 * mult
            ir[c] += filt(z, kind, fc, 2) * 10.0 ** (-3.0 * t / rt)
        ir[c] *= 1.0 - np.exp(-t / buildup)
        for _ in range(early):                       # sparse early reflections
            dt = rng.uniform(0.004, 0.045)
            ir[c, ns(dt)] += rng.uniform(0.4, 1.0) * rng.choice([-1.0, 1.0]) * 6.0 * np.exp(-dt / 0.05)
    ir = fade_edges(ir, 0.0, 0.05)
    ir /= np.sqrt(np.sum(ir ** 2) / 2.0)             # unit energy per channel
    pad = np.zeros((2, ns(predelay)))
    return np.concatenate([pad, ir], axis=1)


def reverb_return(send: np.ndarray, ir: np.ndarray, hp: float = 180.0, lp: float = 9500.0) -> np.ndarray:
    wet = np.stack([signal.fftconvolve(send, ir[c], mode="full")[:len(send)] for c in range(2)])
    wet = filt(wet, "highpass", hp, 2)
    return filt(wet, "lowpass", lp, 2)


def pingpong(send: np.ndarray, delay_s: float, fb: float = 0.45, taps: int = 4,
             lp: float = 3800.0, hp: float = 350.0) -> np.ndarray:
    """Tempo-synced ping-pong delay; every repeat is darker (cumulative LP)."""
    n = len(send)
    out = np.zeros((2, n))
    d = ns(delay_s)
    tap = filt(send, "highpass", hp, 2)
    for k in range(1, taps + 1):
        tap = filt(tap, "lowpass", lp, 1)
        shift = k * d
        if shift >= n:
            break
        out[(k - 1) % 2, shift:] += fb ** (k - 1) * tap[:n - shift]
    return out


# =============================================================================
# 6. BUSES
# =============================================================================
class Bus:
    """Stereo dry buffer + mono effect sends."""

    def __init__(self, name: str):
        self.name = name
        self.dry = np.zeros((2, N))
        self.sends: dict[str, np.ndarray] = {}

    def add(self, sig: np.ndarray, t0: float, gain: float = 1.0, pan=0.0,
            sends: dict | None = None, duck: np.ndarray | None = None) -> int:
        st = to_stereo(np.asarray(sig, dtype=np.float64), pan) * float(gain)
        i0 = ns(t0)
        if i0 < 0:
            st = st[:, -i0:]
            i0 = 0
        i1 = min(N, i0 + st.shape[1])
        m = i1 - i0
        if m <= 0:
            return i0
        seg = st[:, :m]
        if duck is not None:
            seg = seg * duck[i0:i1]
        self.dry[:, i0:i1] += seg
        if sends:
            mono = 0.5 * (seg[0] + seg[1])
            for key, lvl in sends.items():
                if key not in self.sends:
                    self.sends[key] = np.zeros(N)
                self.sends[key][i0:i1] += lvl * mono
        return i0

    def render(self, fx: dict) -> tuple[np.ndarray, np.ndarray]:
        wet = np.zeros((2, N))
        for key, buf in self.sends.items():
            if np.any(buf):
                wet += fx[key](buf)
        return self.dry, wet


def pump_env(times, depth: float, release: float = 0.22, attack: float = 0.003) -> np.ndarray:
    """Kick sidechain gain curve (classic pump): fast dip, raised-cos recovery."""
    g = np.ones(N)
    a, r = ns(attack), ns(release)
    shape = np.concatenate([0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a),
                            (0.5 + 0.5 * np.cos(np.pi * np.arange(r) / r)) ** 1.3])
    seg = 1.0 - depth * shape
    for tk in times:
        i0 = ns(tk) - a
        i1 = min(N, i0 + len(seg))
        g[i0:i1] = np.minimum(g[i0:i1], seg[:i1 - i0])
    return g


# =============================================================================
# 7. DRUMS
# =============================================================================
def kick() -> np.ndarray:
    """Sine kick: 150 -> 43.65 Hz (F1, in key) pitch env, click, saturation."""
    rng = rng_for("kick")
    n = ns(0.46)
    t = tvec(n)
    f = note_hz("F1") + 106.0 * np.exp(-t / 0.034) + 90.0 * np.exp(-t / 0.0035)
    body = osc_sine(f, n) * env_perc(n, 0.001, 0.13, hold=0.04)
    click = filt(rng.standard_normal(n), "bandpass", [1800.0, 7500.0], 2) * env_perc(n, 0.001, 0.0025)
    beater = osc_sine(1350.0, n) * env_perc(n, 0.001, 0.004)
    x = body + 0.35 * click + 0.2 * beater
    x = np.tanh(1.8 * x) / np.tanh(1.8)
    return fade_edges(norm_peak(x), 0.001, 0.02)


def clap(seed: str) -> np.ndarray:
    """Three micro-hits ~10 ms apart + body tail, band-passed noise, slight stereo."""
    rng = rng_for(seed)
    n = ns(0.32)
    t = tvec(n)
    out = np.zeros((2, n))
    for c in range(2):
        z = rng.standard_normal(n)
        bp = filt(z, "bandpass", [1000.0, 3200.0], 2)
        air = filt(z, "highpass", 4500.0, 2)
        env = np.zeros(n)
        for k, (off, amp) in enumerate([(0.0, 0.8), (0.0105, 0.9), (0.0205, 1.0)]):
            off += 0.0006 * c * (k + 1)                 # tiny L/R skew = width
            tau = 0.0045 if k < 2 else 0.065
            seg = np.where(t >= off, np.exp(-np.maximum(t - off, 0) / tau), 0.0)
            seg *= np.clip((t - off) / 0.0008, 0.0, 1.0)
            env += amp * seg
        out[c] = (bp + 0.4 * air) * env
    return fade_edges(norm_peak(out), 0.001, 0.02)


def hat(seed: str, open_: bool = False) -> np.ndarray:
    rng = rng_for(seed)
    n = ns(0.28 if open_ else 0.08)
    t = tvec(n)
    metal = np.zeros(n)
    for f in (205.3, 304.4, 369.6, 522.7, 540.0, 800.0):    # 808-style ratios
        metal += osc_square(f * 2.0 * (1 + 0.003 * rng.standard_normal()), n, rng.random())
    z = rng.standard_normal(n)
    x = filt(0.35 * metal + 0.9 * z, "highpass", 6200.0, 4)
    x += 0.3 * filt(z, "bandpass", [7500.0, 11000.0], 2)
    x = filt(x, "lowpass", 12500.0, 2)
    x *= env_perc(n, 0.001, 0.06 if open_ else 0.013)
    return fade_edges(norm_peak(x), 0.001, 0.006)


def cymbal(dur: float, seed: str, tau: float = 0.8, hp: float = 4500.0) -> np.ndarray:
    rng = rng_for(seed)
    n = ns(dur)
    out = np.zeros((2, n))
    for c in range(2):
        metal = np.zeros(n)
        for f in (205.3, 304.4, 369.6, 522.7, 540.0, 800.0):
            metal += osc_square(f * 1.5 * (1 + 0.004 * rng.standard_normal()), n, rng.random())
        metal = filt(metal, "bandpass", [3000.0, 12000.0], 2)
        z = filt(rng.standard_normal(n), "highpass", hp, 2)
        out[c] = 0.45 * metal + 0.9 * z
    out = filt(filt(out, "highpass", hp * 0.8, 2), "lowpass", 13000.0, 2)
    out *= env_perc(n, 0.001, tau)
    return fade_edges(norm_peak(out), 0.001, 0.05)


# =============================================================================
# 8. TONAL INSTRUMENTS
# =============================================================================
def pluck(freqs, dur: float, seed: str, voices: int = 3, detune: float = 7.0,
          fc_base: float = 350.0, fc_amt: float = 3500.0, fc_tau: float = 0.08,
          q: float = 0.9, amp_tau: float = 0.25, attack: float = 0.002,
          width: float = 0.6, sq_mix: float = 0.0, scoop: float = 0.0) -> np.ndarray:
    """Poly pluck/stab: detuned BLEP saws (+ square) -> TPT low-pass with
    exponential filter envelope -> percussive amp envelope. Returns (2, n)."""
    rng = rng_for(seed)
    n = ns(dur)
    t = tvec(n)
    pm = 2.0 ** (scoop * np.exp(-t / 0.018) / 12.0) if scoop else 1.0
    raw = np.zeros((2, n))
    for f in freqs:
        raw += supersaw(f * pm, n, rng, voices, detune, width)
        if sq_mix:
            raw += sq_mix * osc_square(f * pm, n, rng.random())[None, :]
    fc = fc_base + fc_amt * np.exp(-t / fc_tau)
    y = svf(raw, fc, q, "lp")
    y *= env_perc(n, attack, amp_tau)
    return fade_edges(y, 0.001, 0.006)


def pad(freqs, dur: float, seed: str, a: float = 0.25, r: float = 0.35,
        fc: float = 1200.0, voices: int = 5, detune: float = 12.0,
        width: float = 0.9, lfo_rate: float = 0.35) -> np.ndarray:
    """Warm detuned pad with slowly breathing TPT low-pass. Returns (2, n)."""
    rng = rng_for(seed)
    n = ns(dur + r)
    t = tvec(n)
    raw = np.zeros((2, n))
    for f in freqs:
        raw += supersaw(f, n, rng, voices, detune, width)
    cut = fc * 2.0 ** (0.35 * np.sin(2 * np.pi * lfo_rate * t + rng.uniform(0, 6.28)))
    y = svf(raw, cut, 0.8, "lp")
    y = filt(y, "highpass", 120.0, 2)
    return fade_edges(y * adsr(n, a, 0.4, 0.85, r, dur), 0.002, 0.01)


def sub_bass(segments, t_start: float, t_end: float) -> np.ndarray:
    """Phase-continuous sine sub following chord roots (15 ms glide),
    with a touch of 2nd/3rd harmonic so small speakers hear the line."""
    n = ns(t_end - t_start)
    t = tvec(n) + t_start
    f = np.zeros(n)
    for (s, e, nm) in segments:
        f[(t >= s) & (t < e)] = note_hz(nm)
    f = uniform_filter1d(f, ns(0.015), mode="nearest")
    ph, _ = phase_acc(f, n)
    w = 2 * np.pi * ph
    x = np.sin(w) + 0.16 * np.sin(2 * w) + 0.06 * np.sin(3 * w)
    x = np.tanh(1.3 * x) / np.tanh(1.3)
    return fade_edges(x, 0.003, 0.012)


def mid_bass(f0: float, seed: str, dur: float = 0.21) -> np.ndarray:
    """'Juicy' offbeat bass: saw+square, resonant TPT LP 'bwow' + upward scoop."""
    rng = rng_for(seed)
    n = ns(dur)
    t = tvec(n)
    f = f0 * 2.0 ** (-1.0 * np.exp(-t / 0.012) / 12.0)
    raw = 0.7 * osc_saw(f, n, rng.random()) + 0.45 * osc_square(f, n, rng.random())
    fc = 160.0 + 1500.0 * (np.exp(-t / 0.055) - np.exp(-t / 0.006))
    y = svf(raw, fc, 2.6, "lp")
    y = filt(y, "highpass", 55.0, 2)
    y *= env_perc(n, 0.002, 0.11, hold=0.03)
    return fade_edges(norm_peak(y), 0.001, 0.01)


def riser(dur: float, seed: str = "riser") -> tuple[np.ndarray, np.ndarray]:
    """Noise filter sweep + pitch-rising detuned tone with tempo-synced gate
    accelerating 8ths -> 16ths -> 32nds. Returns (noise, tone) stereo."""
    rng = rng_for(seed)
    n = ns(dur)
    t = tvec(n)
    u = t / dur
    fc = 280.0 * (14000.0 / 280.0) ** (u ** 1.55)
    z = rng.standard_normal((2, n))
    nz = svf(z, fc, 1.7, "bp") + 0.35 * svf(z, fc * 0.7, 0.7, "lp")
    nz *= db2lin(-30.0 * (1.0 - u) ** 1.25)
    semis = 24.0 * u ** 1.6
    f = note_hz("F3") * 2.0 ** (semis / 12.0)
    tone = supersaw(f, n, rng, 5, 22.0, 0.8) + 0.6 * supersaw(f * 1.5, n, rng, 3, 15.0, 0.9)
    tone = svf(tone, 600.0 + 7000.0 * u ** 2, 0.9, "lp")
    rate = np.where(u < 0.3378, 4.0, np.where(u < 0.6757, 8.0, 16.0))
    ph = np.concatenate(([0.0], np.cumsum(rate[:-1]) / SR))
    gate = 0.3 + 0.7 * (0.5 + 0.5 * np.cos(2 * np.pi * ph)) ** 2
    tone *= gate * db2lin(-26.0 * (1.0 - u) ** 1.2)
    return fade_edges(nz, 0.002, 0.002), fade_edges(tone, 0.002, 0.002)


def final_chord() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Ab(add9) final: 7-voice supersaw stack w/ closing filter, major-motif
    bells (Ab-C-Eb, strummed), Ab1 bass boom."""
    rng = rng_for("final_chord")
    dur = SILENT_T - FINAL_T
    n = ns(dur)
    t = tvec(n)
    notes = ["Ab2", "Eb3", "Ab3", "C4", "Eb4", "Bb4", "C5", "Eb5"]
    saw = np.zeros((2, n))
    for nm in notes:
        saw += supersaw(note_hz(nm), n, rng, 7, 17.0, 1.0)
    saw = svf(saw, 1700.0 + 7500.0 * np.exp(-t / 0.45), 0.75, "lp")
    saw = filt(saw, "highpass", 90.0, 2)
    env = (0.6 * np.exp(-t / 0.33) + 0.4 * np.exp(-t / 1.4)) * np.clip(t / 0.003, 0, 1)
    saw = fade_edges(saw * env, 0.001, 0.01)
    bells = np.zeros((2, n))
    for k, (nm, p) in enumerate([("Ab5", -0.4), ("C6", 0.0), ("Eb6", 0.4)]):
        mix_at(bells, to_stereo(bell(note_hz(nm), dur - 0.02 * k - 0.01), p), 0.016 * k)
    fb = note_hz("Ab1") * (1.0 + 1.0 * np.exp(-t / 0.022))
    ph, _ = phase_acc(fb, n)
    bass = np.sin(2 * np.pi * ph) + 0.25 * np.sin(4 * np.pi * ph)
    bass += 0.35 * filt(osc_saw(note_hz("Ab1"), n, 0.3), "lowpass", 320.0, 2)
    bass = fade_edges(bass * env_perc(n, 0.002, 0.9, hold=0.05), 0.002, 0.01)
    return saw, bells, bass


def reverse_swell(chord: np.ndarray, ir_hall: np.ndarray, dur: float = 0.5) -> np.ndarray:
    """Reverse cymbal + reversed hall tail of the final chord, peaking at the hit."""
    m = ns(dur)
    u = np.linspace(0.0, 1.0, m)
    cym = cymbal(1.6, "rev_cymbal", tau=0.75, hp=3500.0)[:, ::-1][:, -m:]
    cym = norm_peak(cym) * u ** 1.1
    src = 0.5 * (chord[0] + chord[1])[:ns(0.3)]
    lead = int(np.argmax(np.abs(ir_hall[0]) > 0))
    wet = np.stack([signal.fftconvolve(src, ir_hall[c, lead:])[:ns(2.2)] for c in range(2)])
    wet = filt(wet, "highpass", 250.0, 2)
    rw = norm_peak(wet[:, ::-1][:, -m:]) * u ** 1.6
    return fade_edges(0.55 * cym + 0.85 * rw, 0.003, 0.0015)


# =============================================================================
# 9. SFX
#    Each returns a peak-normalised signal; sample 0 is the cue (transient).
# =============================================================================
def sfx_pop(target_hz: float, seed: str) -> np.ndarray:
    rng = rng_for(seed)
    n = ns(0.2)
    t = tvec(n)
    f = target_hz * (1.0 + 2.6 * np.exp(-t / 0.009))
    body = osc_sine(f, n) * env_perc(n, 0.001, 0.05)
    body += 0.22 * osc_sine(2.0 * f, n) * env_perc(n, 0.001, 0.018)
    thump = osc_sine(70.0 + 150.0 * np.exp(-t / 0.012), n) * env_perc(n, 0.001, 0.035)
    click = filt(rng.standard_normal(n), "bandpass", [2500.0, 9000.0]) * env_perc(n, 0.001, 0.0018)
    x = np.tanh(1.4 * (body + 0.6 * thump + 0.22 * click))
    return fade_edges(norm_peak(x), 0.001, 0.01)


def sfx_sad_blip() -> np.ndarray:
    """Deflating slide C5 -> ~B3 (a hair flat of an octave), widening wobble,
    vowel-ish resonant LP tracking the pitch."""
    rng = rng_for("sad_blip")
    dur = 0.5
    n = ns(dur)
    t = tvec(n)
    u = t / dur
    semis = -12.6 * u ** 1.7
    vib = (0.06 + 0.5 * u) * np.sin(2 * np.pi * 6.2 * t)
    f = note_hz("C5") * 2.0 ** ((semis + vib) / 12.0)
    src = 0.6 * osc_saw(f, n, rng.random()) + 0.4 * osc_square(f, n, rng.random())
    voc = svf(src, 2.6 * f, 2.2, "lp")
    x = 0.5 * voc + 0.65 * osc_sine(f, n)
    x = filt(x, "highpass", 180.0, 2)
    x *= env_perc(n, 0.002, 10.0) * (1.0 - u) ** 1.1
    pre = filt(rng.standard_normal(n), "bandpass", [1500.0, 6000.0]) * env_perc(n, 0.001, 0.002)
    return fade_edges(norm_peak(x + 0.15 * pre), 0.001, 0.02)


def whoosh(dur: float, f_start: float, f_peak: float, f_end: float, peak: float = 0.3,
           q: float = 1.0, pan0: float = -0.5, pan1: float = 0.5, seed: str = "whoosh",
           body: float = 0.0, width: float = 0.35, tail: float = 1.6, rise: float = 1.0) -> np.ndarray:
    """Band-passed noise with moving centre frequency + stereo pan travel."""
    rng = rng_for(seed)
    n = ns(dur)
    t = tvec(n)
    u = t / dur
    a = np.clip(u / peak, 0.0, 1.0)
    b = np.clip((u - peak) / (1.0 - peak), 0.0, 1.0)
    lf = np.where(u < peak,
                  np.log(f_start) + (np.log(f_peak) - np.log(f_start)) * np.sin(0.5 * np.pi * a),
                  np.log(f_peak) + (np.log(f_end) - np.log(f_peak)) * (1.0 - np.cos(0.5 * np.pi * b)))
    fc = np.exp(lf)
    env = np.where(u < peak, np.sin(0.5 * np.pi * a) ** (2.0 * rise), (1.0 - b) ** tail)
    common = rng.standard_normal(n)
    out = np.zeros((2, n))
    for c in range(2):
        z = np.sqrt(1.0 - width) * common + np.sqrt(width) * rng.standard_normal(n)
        y = svf(z, fc, q, "bp")
        if body > 0.0:
            y = y + body * svf(z, np.maximum(fc * 0.3, 40.0), 0.6, "lp")
        out[c] = y
    pan = pan0 + (pan1 - pan0) * (0.5 - 0.5 * np.cos(np.pi * u))
    gl, gr = pan_gains(pan)
    out[0] *= gl
    out[1] *= gr
    return fade_edges(norm_peak(out * env), 0.001, 0.004)


def onset_tick(seed: str, n: int, f: float = 3200.0, amp: float = 1.0) -> np.ndarray:
    """Tiny transient used to give soft SFX (whooshes) a sample-accurate onset."""
    rng = rng_for(seed)
    t = tvec(n)
    x = filt(rng.standard_normal(n), "highpass", 2500.0, 2) * env_perc(n, 0.001, 0.0015)
    x += 0.5 * osc_sine(f, n) * env_perc(n, 0.001, 0.004)
    return amp * fade_edges(x, 0.001, 0.003) * (t >= 0)


def sfx_whoosh_in() -> np.ndarray:
    """Two plates (top / bottom) start moving: servo 'release' thunk at 2.00,
    then two converging whooshes crescendo into the slam at 2.35."""
    dur = 0.36
    n = ns(dur)
    t = tvec(n)
    a = whoosh(dur, 220.0, 2600.0, 2600.0, peak=0.97, q=1.1, pan0=-0.8, pan1=-0.05,
               seed="whin_a", body=0.5, tail=1.0, rise=1.4)
    b = whoosh(dur, 180.0, 2100.0, 2100.0, peak=0.97, q=1.1, pan0=0.8, pan1=0.05,
               seed="whin_b", body=0.5, tail=1.0, rise=1.4)
    thunk = osc_sine(95.0 + 110.0 * np.exp(-t / 0.01), n) * env_perc(n, 0.001, 0.03)
    clank = onset_tick("whin_tick", n, 1900.0)
    x = 0.8 * (a + b) + to_stereo(0.55 * thunk + 0.35 * clank)
    return fade_edges(norm_peak(x), 0.001, 0.012)


def sfx_heavy_impact() -> np.ndarray:
    rng = rng_for("heavy_impact")
    n = ns(1.0)
    t = tvec(n)
    sub = osc_sine(36.0 + 95.0 * np.exp(-t / 0.045), n) * env_perc(n, 0.001, 0.2, hold=0.02)
    knock = osc_sine(90.0 + 260.0 * np.exp(-t / 0.008), n) * env_perc(n, 0.001, 0.045)
    z = rng.standard_normal(n)
    crunch = np.tanh(5.0 * filt(z, "bandpass", [350.0, 3800.0])) * env_perc(n, 0.001, 0.07)
    crunch = filt(crunch, "lowpass", 7000.0, 2)
    core = sub + 0.6 * knock + 0.45 * crunch
    out = np.zeros((2, n))
    dens = 900.0 * np.exp(-t / 0.09)
    for c in range(2):                                 # crackle of breaking UI
        imp = (rng.random(n) < dens / SR) * rng.uniform(0.3, 1.0, n) * rng.choice([-1.0, 1.0], n)
        cr = norm_peak(filt(imp, "bandpass", [1500.0, 7500.0])) * env_perc(n, 0.001, 0.14)
        out[c] = np.tanh(1.5 * (core + 0.35 * cr))
    return fade_edges(norm_peak(out), 0.001, 0.02)


def sfx_squish_splash() -> np.ndarray:
    """Squeeze (2.40-2.85): wandering resonant noise squelch with wet flutter,
    rising-pitch bubble bloops, high splash."""
    rng = rng_for("squish")
    dur = 0.45
    n = ns(dur)
    t = tvec(n)
    u = t / dur
    out = np.zeros((2, n))
    lfo = smooth_noise(n, 22.0, rng)
    flutter = 0.55 + 0.45 * smooth_noise(n, 38.0, rng)
    fc = 750.0 * 2.0 ** (1.3 * lfo + 0.6 * (1 - u))
    shape = env_perc(n, 0.002, 10.0) * (1.0 - u) ** 1.4
    for c in range(2):
        z = rng.standard_normal(n)
        sq = svf(z, fc, 5.0, "bp") + 0.45 * svf(z, fc * 0.5, 1.0, "lp")
        spl = filt(rng.standard_normal(n), "highpass", 2600.0) * env_perc(n, 0.002, 0.09)
        spl += 0.4 * filt(rng.standard_normal(n), "bandpass", [900.0, 4000.0]) * env_perc(n, 0.002, 0.05)
        out[c] = norm_peak(sq * flutter * shape) + 0.55 * norm_peak(spl)
    times = np.sort(rng.uniform(0.01, 0.37, 11))
    times[0] = 0.0
    for k, tb in enumerate(times):
        b = bloop(rng.uniform(260.0, 620.0), rng.uniform(1.8, 3.0), rng.uniform(0.015, 0.03),
                  rng.uniform(0.015, 0.03), 0.08)
        mix_at(out, to_stereo(b, rng.uniform(-0.6, 0.6)), float(tb),
               rng.uniform(0.45, 0.9) * (1.0 - 0.6 * tb / dur))
    return fade_edges(norm_peak(out), 0.001, 0.02)


def sfx_drop_impact() -> np.ndarray:
    """THE DROP: sub boom (to F1), noise burst, bright juicy double bloop."""
    rng = rng_for("drop_impact")
    n = ns(1.6)
    t = tvec(n)
    sub = osc_sine(note_hz("F1") + 85.0 * np.exp(-t / 0.05), n) * env_perc(n, 0.001, 0.42, hold=0.03)
    knock = osc_sine(120.0 + 300.0 * np.exp(-t / 0.007), n) * env_perc(n, 0.001, 0.04)
    out = np.zeros((2, n))
    for c in range(2):
        z = filt(filt(rng.standard_normal(n), "lowpass", 9000.0), "highpass", 150.0)
        out[c] = 0.5 * z * (env_perc(n, 0.001, 0.035) + 0.15 * env_perc(n, 0.001, 0.25))
    core = np.tanh(1.3 * (sub + 0.6 * knock))
    out += core
    b1 = bloop(280.0, note_hz("C6") / 280.0, 0.022, 0.075, 0.3, 0.25)
    b2 = bloop(420.0, note_hz("F6") / 420.0, 0.018, 0.05, 0.25, 0.2)
    mix_at(out, to_stereo(b1, -0.1), 0.0, 0.55)
    mix_at(out, to_stereo(b2, 0.25), 0.065, 0.38)
    return fade_edges(norm_peak(out), 0.001, 0.03)


def sfx_liquid_whoosh() -> np.ndarray:
    rng = rng_for("liquid_whoosh")
    dur = 0.6
    n = ns(dur)
    base = whoosh(dur, 2600.0, 1700.0, 380.0, peak=0.16, q=2.2, pan0=0.6, pan1=-0.6,
                  seed="liqwh", body=0.4)
    base *= 0.6 + 0.4 * smooth_noise(n, 28.0, rng)
    slosh = filt(rng.standard_normal(n), "bandpass", [400.0, 2500.0]) * env_perc(n, 0.001, 0.02)
    out = base + to_stereo(0.6 * norm_peak(slosh))
    for k, (tb, f0) in enumerate([(0.0, 700.0), (0.07, 600.0), (0.15, 520.0), (0.24, 450.0), (0.33, 380.0)]):
        mix_at(out, to_stereo(bloop(f0, 2.2, 0.02, 0.025, 0.08), 0.5 - 0.25 * k), tb, 0.5 - 0.06 * k)
    return fade_edges(norm_peak(out), 0.001, 0.01)


def sfx_notif(f0: float, seed: str) -> np.ndarray:
    """Bright two-partial UI blip (fundamental + octave) with a pop-like settle."""
    rng = rng_for(seed)
    n = ns(0.45)
    t = tvec(n)
    f = f0 * (1.0 + 0.06 * np.exp(-t / 0.004))
    x = osc_sine(f, n) * env_perc(n, 0.001, 0.13)
    x += 0.45 * osc_sine(2.0 * f, n) * env_perc(n, 0.001, 0.045)
    x += 0.12 * filt(rng.standard_normal(n), "highpass", 4000.0) * env_perc(n, 0.001, 0.0012)
    return fade_edges(norm_peak(x), 0.001, 0.01)


def sfx_swish(seed: str, direction: float, low: bool = False) -> np.ndarray:
    if low:
        dur = 0.34
        w = whoosh(dur, 260.0, 1500.0, 450.0, peak=0.2, q=0.8, pan0=0.55 * direction,
                   pan1=-0.55 * direction, seed=seed, body=0.6, tail=1.8)
        w += to_stereo(onset_tick(seed + "_t", ns(dur), 1500.0, 0.25))
    else:
        dur = 0.17
        w = whoosh(dur, 1300.0, 6500.0, 2800.0, peak=0.16, q=0.9, pan0=-0.7 * direction,
                   pan1=0.7 * direction, seed=seed, tail=1.8)
        w += to_stereo(onset_tick(seed + "_t", ns(dur), 3400.0, 0.3))
    return fade_edges(norm_peak(w), 0.001, 0.006)


def sfx_click(pitch: float, seed: str) -> np.ndarray:
    rng = rng_for(seed)
    n = ns(0.06)
    t = tvec(n)
    hi = filt(rng.standard_normal(n), "bandpass", [3000.0, 7500.0]) * env_perc(n, 0.001, 0.0012)
    tick = osc_sine(2100.0 * pitch, n) * env_perc(n, 0.001, 0.006)
    clunk = osc_sine(230.0 * pitch, n) * env_perc(n, 0.001, 0.012)
    return fade_edges(norm_peak(hi + 0.6 * tick + 0.5 * clunk), 0.001, 0.005)


def sfx_whir_up() -> np.ndarray:
    """Gauge 0 -> 98: motor whir rising Ab2 -> Eb5 (lands under the Eb6 ding),
    accelerating counter ticks."""
    rng = rng_for("whir")
    dur = 0.75
    n = ns(dur)
    t = tvec(n)
    u = t / dur
    f = note_hz("Ab2") * (note_hz("Eb5") / note_hz("Ab2")) ** (u ** 1.35)
    raw = 0.7 * osc_saw(f, n) + 0.5 * osc_square(0.5 * f, n)
    tone = svf(raw, np.minimum(4.0 * f, 12000.0), 1.4, "lp")
    ph = np.cumsum(20.0 + 45.0 * u) / SR
    tone *= 0.62 + 0.38 * np.sin(2 * np.pi * ph) ** 2
    air = svf(rng.standard_normal(n), 2.5 * f, 3.0, "bp")
    x = norm_peak(tone) + 0.3 * norm_peak(air)
    x *= (0.45 + 0.55 * u ** 1.2)
    ticks = np.zeros(n)
    cnt = np.cumsum(9.0 + 36.0 * u) / SR
    idx = np.nonzero(np.diff(np.floor(cnt)) > 0)[0] + 1
    tk = onset_tick("whir_tick", ns(0.02), 4200.0)
    for i in np.concatenate(([0], idx)):
        m = min(len(tk), n - i)
        ticks[i:i + m] += tk[:m] * (1.6 if i == 0 else 0.55)
    x = x * np.clip(t / 0.012, 0, 1) + 0.35 * ticks
    return fade_edges(norm_peak(x), 0.001, 0.008)


def sfx_ding() -> np.ndarray:
    rng = rng_for("ding")
    x = bell(note_hz("Eb6"), 1.2, ((1.0, 1.0, 0.55), (1.0027, 0.35, 0.45), (2.0, 0.42, 0.3), (2.756, 0.24, 0.2), (4.07, 0.12, 0.12), (5.404, 0.07, 0.07)))
    n = len(x)
    x += 0.2 * filt(rng.standard_normal(n), "highpass", 6000.0) * env_perc(n, 0.001, 0.0008)
    return fade_edges(norm_peak(x), 0.001, 0.02)


def metal_burst(freqs, taus, rng: np.random.Generator, n: int) -> np.ndarray:
    exc = rng.standard_normal(n) * env_perc(n, 0.001, 0.0012)
    y = np.zeros(n)
    for f, tau in zip(freqs, taus):
        y += resonator(exc, f, tau) * rng.uniform(0.6, 1.0)
    return y + 0.25 * norm_peak(filt(exc, "highpass", 2000.0)) * np.max(np.abs(y))


def sfx_lock_clack() -> np.ndarray:
    """Shackle snap: two metallic resonant hits 34 ms apart + low thunk."""
    rng = rng_for("lock")
    n = ns(0.35)
    t = tvec(n)
    h1 = norm_peak(metal_burst([2380, 3710, 5230, 7480, 9900], [0.05, 0.04, 0.03, 0.02, 0.012], rng, n))
    h2 = norm_peak(metal_burst([1980, 3130, 4620, 6940], [0.04, 0.03, 0.025, 0.015], rng, n))
    thunk = osc_sine(150.0 + 200.0 * np.exp(-t / 0.005), n) * env_perc(n, 0.001, 0.025)
    out = to_stereo(h1, -0.15) + to_stereo(0.6 * thunk)
    mix_at(out, to_stereo(h2, 0.15), 0.034, 0.75)
    return fade_edges(norm_peak(out), 0.001, 0.01)


def key_click(rng: np.random.Generator, p: float, heavy: bool = False) -> np.ndarray:
    n = ns(0.05)
    t = tvec(n)
    thock = svf(rng.standard_normal(n), 1150.0 * p * (0.7 if heavy else 1.0), 1.8, "bp") * env_perc(n, 0.001, 0.005)
    body = osc_sine(330.0 * p * (0.75 if heavy else 1.0), n) * env_perc(n, 0.001, 0.009)
    top = filt(rng.standard_normal(n), "highpass", 4500.0) * env_perc(n, 0.001, 0.0012)
    return fade_edges(norm_peak(thock) + 0.55 * body + 0.3 * norm_peak(top), 0.001, 0.004)


def sfx_typing() -> np.ndarray:
    """14 soft key clicks over 0.47 s, humanised timing/pitch/velocity."""
    rng = rng_for("typing")
    out = np.zeros((2, ns(0.56)))
    times = np.linspace(0.0, 0.47, 14) + np.concatenate(([0.0], rng.uniform(-0.007, 0.007, 13)))
    times = np.sort(np.clip(times, 0.0, 0.5))
    for i, tk in enumerate(times):
        v = 1.0 if i == 0 else rng.uniform(0.55, 1.0)
        c = key_click(rng, rng.uniform(0.88, 1.12), heavy=(i == 13))
        mix_at(out, to_stereo(c, rng.uniform(-0.25, 0.25)), float(tk), v)
    return fade_edges(norm_peak(out), 0.001, 0.01)


def sfx_soft_pop(f0: float, seed: str, brightness: float = 0.18) -> np.ndarray:
    rng = rng_for(seed)
    n = ns(0.3)
    t = tvec(n)
    f = f0 * (1.0 + 0.5 * np.exp(-t / 0.008))
    x = osc_sine(f, n) * env_perc(n, 0.0015, 0.06)
    x += brightness * osc_sine(2.0 * f, n) * env_perc(n, 0.0015, 0.025)
    x += 0.25 * osc_sine(110.0 + 90.0 * np.exp(-t / 0.01), n) * env_perc(n, 0.0015, 0.03)
    x += 0.05 * filt(rng.standard_normal(n), "highpass", 5000.0) * env_perc(n, 0.001, 0.001)
    return fade_edges(norm_peak(x), 0.001, 0.01)


def sfx_big_whoosh() -> np.ndarray:
    dur = 0.8
    n = ns(dur)
    t = tvec(n)
    hi = whoosh(dur, 320.0, 4200.0, 900.0, peak=0.16, q=0.8, pan0=-0.85, pan1=0.85,
                seed="bigwh_hi", body=0.3, width=0.5)
    lo = whoosh(dur, 70.0, 260.0, 90.0, peak=0.14, q=0.7, pan0=0.0, pan1=0.0,
                seed="bigwh_lo", body=1.0)
    whomp = osc_sine(45.0 + 60.0 * np.exp(-t / 0.03), n) * env_perc(n, 0.002, 0.09)
    puff = onset_tick("bigwh_t", n, 900.0, 0.6)
    x = hi + 0.55 * lo + to_stereo(0.45 * whomp + 0.35 * puff)
    return fade_edges(norm_peak(x), 0.001, 0.01)


def sfx_tick(pitch: float, seed: str) -> np.ndarray:
    rng = rng_for(seed)
    n = ns(0.06)
    x = osc_sine(2900.0 * pitch, n) * env_perc(n, 0.001, 0.007)
    x += 0.4 * osc_sine(5800.0 * pitch, n) * env_perc(n, 0.001, 0.003)
    x += 0.35 * filt(rng.standard_normal(n), "highpass", 5000.0) * env_perc(n, 0.001, 0.0008)
    return fade_edges(norm_peak(x), 0.001, 0.005)


def sfx_tick_accent() -> np.ndarray:
    n = ns(0.5)
    t = tvec(n)
    x = np.zeros(n)
    x[:ns(0.06)] += sfx_tick(1.12, "tick_acc")
    x += 0.7 * osc_sine(note_hz("F6"), n) * env_perc(n, 0.001, 0.2)
    x += 0.3 * osc_sine(note_hz("C7"), n) * env_perc(n, 0.001, 0.09)
    x += 0.6 * osc_sine(60.0 + 90.0 * np.exp(-t / 0.012), n) * env_perc(n, 0.001, 0.04)
    return fade_edges(norm_peak(x), 0.001, 0.02)


def sfx_drip_fall() -> np.ndarray:
    """Drop detaches ('plip' at 12.50) and falls: whistle gliding 2.3 kHz -> 330 Hz,
    getting closer (crescendo), gone at 12.95."""
    rng = rng_for("drip")
    dur = 0.45
    n = ns(dur)
    t = tvec(n)
    u = t / dur
    plip = bloop(650.0, 2100.0 / 650.0, 0.012, 0.025, 0.08, 0.1)
    f = 2300.0 * (330.0 / 2300.0) ** (u ** 1.8)
    f = f * (1.0 + 0.006 * np.sin(2 * np.pi * 9.0 * t))
    wh = osc_sine(f, n) + 0.12 * osc_sine(2.0 * f, n)
    breath = svf(rng.standard_normal(n), f, 8.0, "bp")
    whistle = (wh + 0.25 * norm_peak(breath)) * np.clip((t - 0.02) / 0.06, 0, 1) * (0.25 + 0.75 * u ** 1.5)
    out = to_stereo(0.55 * whistle, 0.25 * (1.0 - u))
    mix_at(out, to_stereo(plip, 0.25), 0.0, 0.8)
    return fade_edges(norm_peak(out), 0.001, 0.012)


def sfx_final_hit() -> np.ndarray:
    rng = rng_for("final_hit")
    n = ns(1.9)
    t = tvec(n)
    boom = osc_sine(note_hz("Ab1") + 110.0 * np.exp(-t / 0.06), n) * env_perc(n, 0.001, 0.55, hold=0.04)
    knock = osc_sine(110.0 + 320.0 * np.exp(-t / 0.007), n) * env_perc(n, 0.001, 0.05)
    core = np.tanh(1.3 * (boom + 0.55 * knock))
    out = np.zeros((2, n))
    for c in range(2):
        z = rng.standard_normal(n)
        burst = filt(filt(z, "lowpass", 10000.0), "highpass", 100.0)
        burst *= env_perc(n, 0.001, 0.045) + 0.2 * env_perc(n, 0.001, 0.3)
        crunch = np.tanh(4.0 * filt(z, "bandpass", [300.0, 3500.0])) * env_perc(n, 0.001, 0.06)
        splash = filt(rng.standard_normal(n), "highpass", 2200.0) * env_perc(n, 0.004, 0.16)
        out[c] = core + 0.45 * norm_peak(burst) + 0.3 * crunch + 0.35 * norm_peak(splash)
    mix_at(out, to_stereo(bloop(300.0, note_hz("Eb6") / 300.0, 0.02, 0.08, 0.3, 0.2), 0.0), 0.0, 0.4)
    for k in range(6):
        tb = float(rng.uniform(0.02, 0.3))
        b = bloop(rng.uniform(350.0, 900.0), rng.uniform(1.8, 2.8), 0.02, 0.025, 0.08)
        mix_at(out, to_stereo(b, rng.uniform(-0.7, 0.7)), tb, rng.uniform(0.15, 0.3))
    return fade_edges(norm_peak(out), 0.001, 0.03)


# SFX table: generator, gain (dB, on peak-normalised sound), pan, sends,
# music duck depth (dB) and hold (s).
def sfx_render(kind: str, idx: int):
    if kind == "pop":
        return sfx_pop(note_hz("F4") if idx == 0 else note_hz("Ab4"), f"pop{idx}")
    if kind == "sad_blip":
        return sfx_sad_blip()
    if kind == "whoosh_in":
        return sfx_whoosh_in()
    if kind == "heavy_impact":
        return sfx_heavy_impact()
    if kind == "squish_splash":
        return sfx_squish_splash()
    if kind == "drop_impact":
        return sfx_drop_impact()
    if kind == "liquid_whoosh":
        return sfx_liquid_whoosh()
    if kind == "notif_pop":                         # F5 -> Ab5 (3rd) -> C6 (5th)
        return sfx_notif(note_hz(["F5", "Ab5", "C6"][idx % 3]), f"notif{idx}")
    if kind == "swish":
        return sfx_swish(f"swish{idx}", 1.0 if idx % 2 == 0 else -1.0)
    if kind == "swish_low":
        return sfx_swish(f"swishlow{idx}", 1.0 if idx % 2 == 0 else -1.0, low=True)
    if kind == "click":
        return sfx_click(1.0 + 0.12 * idx, f"click{idx}")
    if kind == "whir_up":
        return sfx_whir_up()
    if kind == "ding":
        return sfx_ding()
    if kind == "lock_clack":
        return sfx_lock_clack()
    if kind == "typing":
        return sfx_typing()
    if kind == "result_pop":
        return sfx_soft_pop(note_hz("G5"), "result_pop", 0.25)
    if kind == "big_whoosh":
        return sfx_big_whoosh()
    if kind == "tick":
        return sfx_tick(1.0 + 0.06 * idx, f"tick{idx}")
    if kind == "tick_accent":
        return sfx_tick_accent()
    if kind == "drip_fall":
        return sfx_drip_fall()
    if kind == "final_hit":
        return sfx_final_hit()
    if kind == "soft_pop":
        return sfx_soft_pop(note_hz(["Eb5", "Ab5"][idx % 2]), f"soft_pop{idx}")
    if kind == "step_pop":
        return sfx_soft_pop(note_hz(["C5", "Eb5", "F5", "Ab5", "C6"][idx % 5]), f"step_pop{idx}", 0.22)
    return None


SFX_MIX = {
    #  kind            gain_dB  pan    sends                          duck_dB hold
    "pop":           (-2.0,  0.0,  {"plate": 0.10},               2.0, 0.08),
    "sad_blip":      (-4.0,  0.0,  {"plate": 0.18},               2.5, 0.35),
    "whoosh_in":     (-2.0,  0.0,  {"room": 0.10},                2.0, 0.30),
    "heavy_impact":  (0.0,   0.0,  {"room": 0.35},                4.0, 0.20),
    "squish_splash": (-3.0,  0.0,  {"room": 0.25},                3.0, 0.28),
    "drop_impact":   (2.0,   0.0,  {"room": 0.25, "plate": 0.12}, 3.0, 0.12),
    "liquid_whoosh": (2.0,   0.0,  {"plate": 0.12},               2.0, 0.35),
    "notif_pop":     (-1.0,  0.0,  {"plate": 0.22},               1.5, 0.10),
    "swish":         (0.0,   0.0,  {"plate": 0.08},               1.0, 0.10),
    "swish_low":     (0.0,   0.0,  {"plate": 0.08},               1.5, 0.20),
    "click":         (3.0,   0.0,  {"room": 0.10},                1.0, 0.04),
    "whir_up":       (2.0,   0.0,  {"plate": 0.08},               2.0, 0.70),
    "ding":          (-3.0,  0.0,  {"plate": 0.25},               2.0, 0.25),
    "lock_clack":    (2.0,   0.0,  {"room": 0.20},                2.0, 0.10),
    "typing":        (0.0,   0.0,  {"room": 0.08},                1.5, 0.48),
    "result_pop":    (1.0,   0.0,  {"plate": 0.18},               1.5, 0.10),
    "big_whoosh":    (2.0,   0.0,  {"plate": 0.10},               3.0, 0.35),
    "tick":          (0.0,   0.0,  {"plate": 0.08},               1.0, 0.04),
    "tick_accent":   (1.0,   0.0,  {"plate": 0.20},               2.0, 0.12),
    "drip_fall":     (-6.0,  0.0,  {"plate": 0.15},               2.0, 0.42),
    "final_hit":     (4.0,   0.0,  {"room": 0.20, "hall": 0.30},  3.5, 0.25),
    "soft_pop":      (-3.0,  0.0,  {"plate": 0.25},               1.5, 0.08),
    "step_pop":      (-1.0,  0.0,  {"plate": 0.28},               1.5, 0.08),
}


# =============================================================================
# 10. ARRANGEMENT
# =============================================================================
# (start, end, sub root, pad voicing, stab voicing (rootless, common C/Eb), mid-bass)
_FM = ("F1", ["F3", "C4", "Eb4", "Ab4"], ["Ab3", "C4", "Eb4", "G4"], "F2")
_DB = ("Db2", ["Db3", "Ab3", "C4", "F4"], ["F3", "Ab3", "C4", "Eb4"], "Db3")
_AB = ("Ab1", ["Ab2", "Eb3", "Ab3", "C4"], ["Ab3", "C4", "Eb4", "Bb4"], "Ab2")
_EB = ("Eb2", ["Eb3", "Bb3", "Eb4", "G4"], ["G3", "Bb3", "Eb4", "F4"], "Eb3")
# (start, end, sub root, pad voicing, stab voicing, mid-bass)
CHORDS = [
    (3.0, 5.0) + _FM, (5.0, 7.0) + _DB, (7.0, 9.0) + _AB, (9.0, 10.0) + _EB,       # 9-10: short bar into the new scene
    (10.0, 12.0) + _FM, (12.0, 14.0) + _DB, (14.0, 16.0) + _AB,                      # realisations (groove)
    (16.0, 18.0) + _EB, (18.0, 20.0) + _FM, (20.0, 22.0) + _DB,                      # methode (breakdown)
    (22.0, 24.0) + _AB, (24.0, 26.0) + _EB,                                          # offres + site reel (groove)
    (26.0, 27.5, "F1", ["F3", "C4", "Eb4", "Ab4"], None, "F2"),                      # Fm (arp)
]
WINDOWS = [(DROP_T, BRK_T), (DROP2_T, STOP_T)]                                       # drums on


def up_oct(nm: str) -> str:
    return nm[:-1] + str(int(nm[-1]) + 1)


def chord_at(t: float):
    for c in CHORDS:
        if c[0] <= t + 1e-9 < c[1]:
            return c
    return CHORDS[-1]


def build_music(irs: dict):
    pre, brk, grv, end = Bus("music_pre"), Bus("music_break"), Bus("music_groove"), Bus("music_end")
    kicks = [DROP_T + BEAT * k for k in range(26)] + [DROP2_T + BEAT * k for k in range(11)]
    pump_sub = pump_env(kicks, 0.88, 0.20)
    pump_pad = pump_env(kicks, 0.55, 0.26)
    pump_stab = pump_env(kicks, 0.30, 0.18)
    pump_light = pump_env(kicks, 0.18, 0.15)

    # ---------------- HOOK 0-2.98 (unchanged) --------------------------------
    hp_ = pad([note_hz(x) for x in ("Ab3", "C4", "F4", "G4", "C5")], 2.7, "hook_pad",
              a=0.9, r=0.3, fc=1100.0, voices=5, detune=10.0)
    hp_ = filt(hp_, "highpass", 220.0, 2)
    pre.add(hp_, 0.0, db2lin(-20.0), sends={"plate": 0.3})
    rng = rng_for("air")
    air = filt(rng.standard_normal((2, ns(2.98))), "bandpass", [5000.0, 12000.0], 2)
    air *= (0.6 + 0.4 * smooth_noise(ns(2.98), 0.8, rng)) * np.linspace(0, 1, ns(2.98)) ** 0.7
    pre.add(fade_edges(air, 0.01, 0.002), 0.0, db2lin(-40.0))
    motif = [(0.0, "F4"), (0.75, "Ab4"), (1.25, "C5"), (1.75, "Db5")]
    for k, (tn, nm) in enumerate(motif):
        p = pluck([note_hz(nm)], 0.75, f"hook_pluck{k}", voices=3, detune=6.0,
                  fc_base=260.0, fc_amt=1500.0 + 300 * k, fc_tau=0.09, q=1.1,
                  amp_tau=0.32, width=0.3, sq_mix=0.25)
        pre.add(p, tn, db2lin(-9.0), pan=[-0.15, 0.15, -0.1, 0.1][k],
                sends={"delay": 0.55, "plate": 0.3})
    rz, rt = riser(CUT_T - 1.5)
    pre.add(rz, 1.5, db2lin(-8.0), sends={"plate": 0.12})
    pre.add(rt, 1.5, db2lin(-8.0), sends={"plate": 0.15})
    EVENT_LOG.append(dict(type="riser_start(music)", cue=1.5, start=1.5, onset=1.5, peak=None))

    # ---------------- GROOVE (two windows) -----------------------------------
    k_sig = kick()
    for tk in kicks:
        grv.add(k_sig, tk, db2lin(-4.5))
    claps = [clap(f"clap{i}") for i in range(3)]
    clap_t = [DROP_T + 0.5 + k for k in range(13)] + [DROP2_T + 0.5 + k for k in range(5)]
    for i, tc in enumerate(clap_t):
        grv.add(claps[i % 3], tc, db2lin(-6.0), sends={"room": 0.35})
    for i, (tc, v) in enumerate(zip([27.0, 27.125, 27.25, 27.375], [-20.0, -16.0, -13.0, -10.0])):
        grv.add(claps[i % 3], tc, db2lin(v), sends={"room": 0.3})             # final build roll
    oh = [hat(f"ohat{i}", True) for i in range(4)]
    ch = [hat(f"chat{i}", False) for i in range(4)]
    rng = rng_for("hat_vel")
    for w0, w1 in WINDOWS:
        for k in range(int(round((w1 - w0) / BEAT))):                          # offbeat open hats
            th = w0 + 0.25 + BEAT * k
            grv.add(oh[k % 4], th, db2lin(-10.5 + rng.uniform(-1.2, 1.2)), pan=0.12)
        t16, k = w0, 0
        while t16 < w1 - 1e-9:                                                 # 16th ghosts
            if k % 4 in (1, 3):
                base = -20.5 if t16 < 5.0 else -17.5
                if t16 >= 26.0:
                    base += 5.0 * (t16 - 26.0) / 1.5
                grv.add(ch[k % 4], t16, db2lin(base + rng.uniform(-2.0, 1.0)), pan=-0.2)
            k += 1
            t16 = w0 + k * S16
    grv.add(cymbal(2.2, "crash", tau=0.7, hp=3500.0), DROP_T, db2lin(-12.0), sends={"plate": 0.1})
    grv.add(cymbal(2.2, "crash2", tau=0.7, hp=3500.0), DROP2_T, db2lin(-11.0), sends={"plate": 0.1})

    segs = [(c[0], c[1], c[2]) for c in CHORDS]
    for w0, w1 in WINDOWS:
        sub = sub_bass(segs, w0, w1)
        grv.add(sub, w0, db2lin(-13.5), duck=pump_sub)
        for k in range(int(round((w1 - w0) / BEAT))):
            tb = w0 + 0.25 + BEAT * k
            c = chord_at(tb)
            last_in_bar = abs(((tb - c[0]) % BAR) - 1.75) < 1e-6
            f0 = note_hz(c[5]) * (2.0 if last_in_bar else 1.0)
            grv.add(mid_bass(f0, f"mb{w0:.0f}_{k}"), tb, db2lin(-11.0 if not last_in_bar else -13.0),
                    duck=pump_light)

    # pads: pumped in the groove, wide and unpumped in the breakdown
    for i, c in enumerate(CHORDS):
        in_brk = BRK_T <= c[0] < DROP2_T - 1e-9
        if in_brk:
            p = pad([note_hz(x) for x in c[3]], min(c[1], CUT2_T) - c[0], f"pad{i}", a=0.6,
                    r=0.25, fc=2600.0, voices=5, detune=14.0)
            brk.add(p, c[0], db2lin(-14.5), sends={"plate": 0.3})
        else:
            p = pad([note_hz(x) for x in c[3]], c[1] - c[0], f"pad{i}",
                    a=0.03 if c[0] in (3.0, DROP2_T) else 0.08, r=0.25, fc=2200.0, voices=5, detune=13.0)
            grv.add(p, c[0], db2lin(-19.0), sends={"plate": 0.15}, duck=pump_pad)

    # syncopated rootless stabs
    steps = [2, 5, 10, 13]
    rng = rng_for("stab_vel")
    hit = 0
    for c in CHORDS:
        if c[4] is None or not (5.0 <= c[0] < BRK_T or DROP2_T <= c[0] < 26.0):
            continue
        st_steps = [2, 5] if c[1] - c[0] < 1.5 else steps + ([15] if c[0] in (14.0, 24.0) else [])
        for s_ in st_steps:
            ts = c[0] + s_ * S16
            long_ = s_ in (5, 13)
            st = pluck([note_hz(x) for x in c[4]], 0.42 if long_ else 0.3, f"stab{hit}",
                       voices=5, detune=11.0, fc_base=700.0, fc_amt=5000.0,
                       fc_tau=0.07 if long_ else 0.05, q=0.85,
                       amp_tau=0.17 if long_ else 0.11, width=0.85)
            grv.add(st, ts, db2lin(-8.0 + rng.uniform(-1.0, 0.0) - (2.0 if s_ == 15 else 0.0)),
                    sends={"plate": 0.22, "delay": 0.12}, duck=pump_stab)
            hit += 1

    # ---------------- BREAKDOWN 16-21.98 (methode) ----------------------------
    sub = sub_bass([(c[0], min(c[1], CUT2_T), c[2]) for c in CHORDS if BRK_T <= c[0] < DROP2_T - 1e-9],
                   BRK_T, CUT2_T)
    brk.add(sub, BRK_T, db2lin(-15.0))
    pat = [0, 1, 2, 3, 2, 1, 2, 3]
    for c in CHORDS:
        if not (BRK_T <= c[0] < DROP2_T - 1e-9):
            continue
        notes = [up_oct(x) for x in c[3]]
        for j in range(8):
            ta = c[0] + j * 0.25
            if ta > CUT2_T - 0.2:
                continue
            boost = 4.0 * max(0.0, (ta - 20.0) / 2.0)
            a = pluck([note_hz(notes[pat[j]])], 0.45, f"barp{c[0]:.0f}_{j}", voices=2, detune=6.0,
                      fc_base=450.0 + 90.0 * j, fc_amt=1900.0, fc_tau=0.07, q=1.0,
                      amp_tau=0.2, width=0.4, sq_mix=0.3)
            brk.add(a, ta, db2lin(-15.0 + boost), pan=0.3 if j % 2 else -0.3,
                    sends={"plate": 0.25, "delay": 0.2})
    rng = rng_for("brk_hats")
    t = BRK_T + 0.25
    kk = 0
    while t < CUT2_T - 0.1:
        brk.add(ch[kk % 4], t, db2lin(-17.0 + 2.5 * max(0.0, t - 20.0) + rng.uniform(-1.0, 1.0)), pan=0.15)
        kk += 1
        t += BEAT
    rz2, rt2 = riser(CUT2_T - 20.0, "riser2")
    brk.add(rz2, 20.0, db2lin(-8.0), sends={"plate": 0.12})
    brk.add(rt2, 20.0, db2lin(-8.0), sends={"plate": 0.15})
    EVENT_LOG.append(dict(type="riser_start(music)", cue=20.0, start=20.0, onset=20.0, peak=None))
    for i in range(8):                                                          # clap roll into drop 2
        brk.add(claps[i % 3], 21.0 + i * 0.125, db2lin(-24.0 + 14.0 * i / 7.0), sends={"room": 0.3})

    # ---------------- final build: rising arp + noise (26.0-27.5) -------------
    arp = ["F4", "Ab4", "C5", "F5", "Ab4", "C5", "F5", "Ab5", "C5", "F5", "Ab5", "C6"]
    for k, nm in enumerate(arp):
        ta = 26.0 + k * S16
        a = pluck([note_hz(nm)], 0.3, f"arp{k}", voices=2, detune=6.0,
                  fc_base=500.0 + 140.0 * k, fc_amt=2200.0 + 350.0 * k, fc_tau=0.05,
                  q=1.0, amp_tau=0.1, width=0.4, sq_mix=0.35)
        grv.add(a, ta, db2lin(-10.0 + 5.0 * k / 11.0), pan=0.3 if k % 2 else -0.3,
                sends={"plate": 0.2, "delay": 0.15}, duck=pump_light)
    rng = rng_for("build_noise")
    bn_n = ns(1.5)
    u = np.linspace(0, 1, bn_n)
    bn = svf(rng.standard_normal((2, bn_n)), 900.0 * (11000.0 / 900.0) ** u, 1.2, "bp")
    bn *= db2lin(-26.0 * (1.0 - u))
    grv.add(fade_edges(bn, 0.01, 0.003), 26.0, db2lin(-21.0))

    # ---------------- END CARD ------------------------------------------------
    saw, bells, bass = final_chord()
    sw = reverse_swell(saw, irs["hall"], FINAL_T - STOP_T)
    end.add(sw, STOP_T, db2lin(1.0))
    end.add(saw, FINAL_T, db2lin(-7.5), sends={"hall": 0.55})
    end.add(bells, FINAL_T, db2lin(-10.0), sends={"hall": 0.6})
    end.add(bass, FINAL_T, db2lin(-7.0))
    return pre, brk, grv, end


def build_sfx(cues: dict):
    pre, pre2, post = Bus("sfx_pre"), Bus("sfx_break"), Bus("sfx_post")
    counts: dict[str, int] = {}
    duck_events = []
    for cue in cues["sfx"]:
        kind, t0 = cue["type"], float(cue["t"])
        if kind == "riser_start":
            continue                                  # rendered by the music bus
        idx = counts.get(kind, 0)
        counts[kind] = idx + 1
        sig = sfx_render(kind, idx)
        if sig is None:
            print(f"  ! no generator for {kind}")
            continue
        gain_db, pan, sends, duck_db, hold = SFX_MIX[kind]
        if kind == "notif_pop":                       # badges pop in at different spots
            pan = [-0.25, 0.25, 0.0][idx % 3]
        elif kind in ("click", "tick"):
            pan = [0.12, -0.12][idx % 2]
        bus = pre if t0 < CUT_T else (pre2 if BRK_T <= t0 < CUT2_T else post)
        i0 = bus.add(sig, t0, db2lin(gain_db), pan, sends)
        env = np.max(np.abs(sig), axis=0) if sig.ndim == 2 else np.abs(sig)
        pk = env.max()
        on = int(np.argmax(env >= 0.1 * pk))
        EVENT_LOG.append(dict(type=kind, cue=t0, start=i0 / SR, onset=(i0 + on) / SR,
                              peak=(i0 + int(np.argmax(env))) / SR))
        duck_events.append((t0, duck_db, hold))
    return pre, pre2, post, duck_events


def duck_curve(events, attack: float = 0.006, release: float = 0.2) -> np.ndarray:
    """SFX-keyed music ducking (dB automation, min over overlapping events)."""
    g = np.zeros(N)
    a, r = ns(attack), ns(release)
    for t0, depth, hold in events:
        h = ns(hold)
        shape = np.concatenate([0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a), np.ones(h),
                                0.5 + 0.5 * np.cos(np.pi * np.arange(r) / r)])
        i0 = ns(t0) - a
        i1 = min(N, i0 + len(shape))
        g[i0:i1] = np.minimum(g[i0:i1], -depth * shape[:i1 - i0])
    return db2lin(g)


# =============================================================================
# 11. MEASUREMENT (BS.1770-4 loudness, true peak)
# =============================================================================
def k_weight(x: np.ndarray) -> np.ndarray:
    b1 = [1.53512485958697, -2.69169618940638, 1.19839281085285]
    a1 = [1.0, -1.69065929318241, 0.73248077421585]
    b2 = [1.0, -2.0, 1.0]
    a2 = [1.0, -1.99004745483398, 0.99007225036621]
    return signal.lfilter(b2, a2, signal.lfilter(b1, a1, x, axis=-1), axis=-1)


def _block_power(x: np.ndarray, win: float, hop: float):
    y = k_weight(x)
    blk, hp = ns(win), ns(hop)
    cs = np.concatenate([np.zeros((y.shape[0], 1)), np.cumsum(y ** 2, axis=1)], axis=1)
    starts = np.arange(0, y.shape[1] - blk + 1, hp)
    ms = (cs[:, starts + blk] - cs[:, starts]) / blk
    return ms.sum(axis=0), starts


def lufs_integrated(x: np.ndarray) -> float:
    z, _ = _block_power(x, 0.4, 0.1)
    lk = -0.691 + 10 * np.log10(np.maximum(z, 1e-20))
    g1 = lk > -70.0
    if not np.any(g1):
        return -np.inf
    rel = -0.691 + 10 * np.log10(np.mean(z[g1])) - 10.0
    g2 = g1 & (lk > rel)
    return float(-0.691 + 10 * np.log10(np.mean(z[g2])))


def loudness_curve(x: np.ndarray, win: float = 0.4, hop: float = 0.02):
    z, starts = _block_power(x, win, hop)
    return (starts + ns(win) / 2) / SR, -0.691 + 10 * np.log10(np.maximum(z, 1e-20))


def true_peak_db(x: np.ndarray) -> float:
    up = signal.resample_poly(x, 4, 1, axis=-1)
    return float(lin2db(np.max(np.abs(up))))


# =============================================================================
# 12. MIX BUS + MASTER
# =============================================================================
def shelf_sos(f0: float, gain_db: float, high: bool = True, slope: float = 0.8) -> np.ndarray:
    """RBJ-cookbook shelving biquad as a 1-section SOS."""
    A = 10.0 ** (gain_db / 40.0)
    w0 = 2.0 * np.pi * f0 / SR
    cw, sw = np.cos(w0), np.sin(w0)
    alpha = sw / 2.0 * np.sqrt((A + 1.0 / A) * (1.0 / slope - 1.0) + 2.0)
    sa = 2.0 * np.sqrt(A) * alpha
    sg = 1.0 if high else -1.0
    b0 = A * ((A + 1) + sg * (A - 1) * cw + sa)
    b1 = -2.0 * sg * A * ((A - 1) + sg * (A + 1) * cw)
    b2 = A * ((A + 1) + sg * (A - 1) * cw - sa)
    a0 = (A + 1) - sg * (A - 1) * cw + sa
    a1 = 2.0 * sg * ((A - 1) - sg * (A + 1) * cw)
    a2 = (A + 1) - sg * (A - 1) * cw - sa
    return np.array([[b0 / a0, b1 / a0, b2 / a0, 1.0, a1 / a0, a2 / a0]])


def lin_pre(x: np.ndarray) -> np.ndarray:
    """Linear bus prep (identical on stems): 22 Hz HPF (DC/rumble), +1 dB
    'air' shelf at 9 kHz, mono below 140 Hz (M/S)."""
    x = signal.sosfilt(sos("highpass", 22.0, 2), x, axis=-1)
    x = signal.sosfilt(shelf_sos(9000.0, 1.0, True), x, axis=-1)
    m, s = 0.5 * (x[0] + x[1]), 0.5 * (x[0] - x[1])
    s = signal.sosfilt(sos("highpass", 140.0, 2), s)
    return np.stack([m + s, m - s])


def glue_comp(x: np.ndarray, thr_db: float = -15.0, ratio: float = 2.0, knee: float = 6.0,
              att: float = 0.012, rel: float = 0.14, win: float = 0.008):
    p = uniform_filter1d(np.max(x ** 2, axis=0), ns(win))
    lvl = 10 * np.log10(np.maximum(p, 1e-20))
    over = lvl - thr_db
    slope = 1.0 / ratio - 1.0
    gr = np.where(over <= -knee / 2, 0.0,
                  np.where(over >= knee / 2, slope * over, slope * (over + knee / 2) ** 2 / (2 * knee)))
    dec = 16
    m = len(gr) // dec
    tgt = gr[:m * dec].reshape(m, dec).min(axis=1)
    aa = np.exp(-dec / (att * SR))
    ar = np.exp(-dec / (rel * SR))
    out = np.empty(m)
    s = 0.0
    for i, v in enumerate(tgt.tolist()):
        c = aa if v < s else ar
        s = c * s + (1.0 - c) * v
        out[i] = s
    g_db = np.interp(np.arange(len(gr)), np.arange(m) * dec + dec / 2, out)
    g = db2lin(g_db)
    return x * g, g


def soft_sat(x: np.ndarray, drive: float = 1.35, mix: float = 0.6) -> np.ndarray:
    """Gentle tanh saturation at 4x oversampling (alias-free warmth)."""
    up = signal.resample_poly(x, 4, 1, axis=-1)
    y = mix * np.tanh(drive * up) / drive + (1.0 - mix) * up
    return signal.resample_poly(y, 1, 4, axis=-1)[:, :x.shape[1]]


def limiter(x: np.ndarray, ceil_db: float, lookahead: float = 0.003, release: float = 0.07):
    """Lookahead brickwall limiter, true-peak aware (4x oversampled detector).
    Gain: centred min-hold over +-L, instant attack/smooth release, then an
    L-long moving average => ramps reach full reduction exactly at the peak."""
    c = db2lin(ceil_db)
    up = signal.resample_poly(x, 4, 1, axis=-1)
    pk = np.max(np.abs(up), axis=0)[:4 * x.shape[1]].reshape(-1, 4).max(axis=1)
    pk = np.maximum(pk, np.max(np.abs(x), axis=0))
    req = np.minimum(1.0, c / np.maximum(pk, 1e-12))
    L = ns(lookahead)
    hold = minimum_filter1d(req, size=2 * L + 1, mode="nearest")
    ar = np.exp(-1.0 / (release * SR))
    g = np.empty_like(hold)
    s = 1.0
    for i, v in enumerate(hold.tolist()):
        s = v if v < s else ar * s + (1.0 - ar) * v
        g[i] = s
    g = uniform_filter1d(g, size=L, mode="nearest")
    g = np.minimum(g, hold)
    return x * g, g


def master(music: np.ndarray, sfx: np.ndarray):
    mus, fx = music, sfx                                 # already lin_pre'd per bus
    mix = mus + fx
    l0 = lufs_integrated(mix)
    g_pre = float(db2lin(-18.0 - l0))
    x = mix * g_pre
    x, g_comp = glue_comp(x)
    x = soft_sat(x)
    g_out = float(db2lin(TARGET_LUFS - lufs_integrated(x)))
    for _ in range(8):
        y, g_lim = limiter(x * g_out, LIMIT_CEIL_DBTP)
        L = lufs_integrated(y)
        if abs(L - TARGET_LUFS) < 0.01:
            break
        g_out *= float(db2lin(TARGET_LUFS - L))
    tp = true_peak_db(y)
    trim = 1.0
    if tp > -1.05:                                       # safety, never expected
        trim = float(db2lin(-1.05 - tp))
        y = y * trim
    y[:, ns(SILENT_T):] = 0.0
    G = g_pre * g_comp * g_out * g_lim * trim
    stem_m = mus * G
    stem_s = fx * G
    stem_m[:, ns(SILENT_T):] = 0.0
    stem_s[:, ns(SILENT_T):] = 0.0
    info = dict(comp_gr_max_db=float(-lin2db(g_comp.min())),
                comp_gr_mean_db=float(-np.mean(lin2db(g_comp[ns(3.0):ns(27.5)]))),
                lim_gr_max_db=float(-lin2db(g_lim.min())),
                lim_gr_mean_db=float(-np.mean(lin2db(g_lim[ns(3.0):ns(27.5)]))))
    return y, stem_m, stem_s, info


# =============================================================================
# 13. FILE I/O
# =============================================================================
def write_wav24(path: str, x: np.ndarray, seed: str = "dither"):
    """24-bit PCM WAV via stdlib wave, TPDF dither, hard clip guard."""
    rng = rng_for(seed)
    q = 8388607.0
    d = (rng.random(x.shape) - rng.random(x.shape))     # TPDF, +-1 LSB
    ints = np.clip(np.round(x * q + d), -8388608, 8388607).astype("<i4")
    inter = ints.T.reshape(-1)
    raw = inter.view(np.uint8).reshape(-1, 4)[:, :3].tobytes()
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(3)
        w.setframerate(SR)
        w.writeframes(raw)


def read_wav24(path: str) -> tuple[np.ndarray, int]:
    with wave.open(path, "rb") as w:
        sr, nch, sw, nfr = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(nfr)
    assert sw == 3
    b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
    v = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
    v = np.where(v >= 1 << 23, v - (1 << 24), v)
    return (v.reshape(-1, nch).T / 8388608.0), sr


# =============================================================================
# 14. OVERVIEW PLOT
# =============================================================================
def plot_overview(path: str, y: np.ndarray, mus: np.ndarray, fx: np.ndarray, cues: dict, stats: dict):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return plot_overview_pil(path, y, cues)
    mono = 0.5 * (y[0] + y[1])
    f, tt, Z = signal.stft(mono, fs=SR, nperseg=2048, noverlap=2048 - 240, boundary=None)
    S = 20 * np.log10(np.abs(Z) + 1e-9)
    S -= S.max()
    fl = np.geomspace(25.0, 20000.0, 420)
    Sl = np.stack([np.interp(fl, f, S[:, j]) for j in range(S.shape[1])], axis=1)

    fig = plt.figure(figsize=(20, 11.5), facecolor="#111014")
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 2.6, 1.1], hspace=0.06)
    axw = fig.add_subplot(gs[0])
    axs = fig.add_subplot(gs[1], sharex=axw)
    axl = fig.add_subplot(gs[2], sharex=axw)
    for ax in (axw, axs, axl):
        ax.set_facecolor("#16141b")
        ax.tick_params(colors="#c9c5d1", labelsize=9)
        for sp in ax.spines.values():
            sp.set_color("#3a3542")
    hop = ns(0.005)
    nb = N // hop
    t_env = (np.arange(nb) + 0.5) * hop / SR
    for ch, col in ((0, "#FFB21A"), (1, "#EE2A7B")):
        seg = y[ch, :nb * hop].reshape(nb, hop)
        axw.fill_between(t_env, seg.min(axis=1), seg.max(axis=1), color=col, alpha=0.55, lw=0)
    axw.set_ylim(-1.05, 1.05)
    axw.set_ylabel("master", color="#c9c5d1")
    axs.imshow(Sl, origin="lower", aspect="auto", cmap="magma", vmin=-95, vmax=0,
               extent=[tt[0] + 1024 / SR, tt[-1] + 1024 / SR, 0, len(fl)])
    ticks = [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    axs.set_yticks([np.interp(np.log(v), np.log(fl), np.arange(len(fl))) for v in ticks])
    axs.set_yticklabels([f"{v//1000}k" if v >= 1000 else str(v) for v in ticks])
    axs.set_ylabel("Hz (log)", color="#c9c5d1")
    for sig, lab, col in ((y, "master", "#F3F1F5"), (mus, "music stem", "#7B3FF2"), (fx, "sfx stem", "#1FA971")):
        tl, ll = loudness_curve(sig)
        axl.plot(tl, ll, color=col, lw=1.4, label=lab)
    axl.axhline(TARGET_LUFS, color="#FF5A1F", lw=0.8, ls=":")
    axl.set_ylim(-50, -2)
    axl.set_ylabel("momentary LUFS", color="#c9c5d1")
    axl.set_xlabel("time (s)", color="#c9c5d1")
    axl.legend(loc="lower left", fontsize=9, facecolor="#16141b", labelcolor="#c9c5d1", edgecolor="#3a3542")
    axl.set_xlim(0, DUR)
    axl.set_xticks(np.arange(0, 15.5, 0.5))
    for s in cues["sections"]:
        for ax in (axw, axs, axl):
            ax.axvline(s["start"], color="#5BD1FF", lw=1.6, alpha=0.9)
        axw.text(s["start"] + 0.03, 0.92, s["name"], color="#5BD1FF", fontsize=10, fontweight="bold",
                 transform=axw.get_xaxis_transform(), va="top")
    for k, (t_, lab) in enumerate(((CUT_T, "cut 2.98"), (STOP_T, "drums stop 12.5"),
                                   (FINAL_T, "FINAL 13.0"), (SILENT_T, "silence 14.95"))):
        for ax in (axw, axs, axl):
            ax.axvline(t_, color="#FF5A1F", lw=1.2, ls="--", alpha=0.9)
        axl.text(t_ + 0.02, -4.0 - 4.0 * (k % 2), lab, color="#FF5A1F", fontsize=8, va="top")
    plt.setp(axw.get_xticklabels(), visible=False)
    plt.setp(axs.get_xticklabels(), visible=False)
    for c in cues["sfx"]:
        for ax in (axw, axs):
            ax.axvline(c["t"], color="#FFFFFF", lw=0.6, ls=(0, (2, 2)), alpha=0.55)
        axs.text(c["t"] + 0.01, len(fl) - 3, c["type"], color="#FFFFFF", fontsize=6.5, rotation=90,
                 va="top", ha="left", alpha=0.85)
    fig.suptitle(f"juicecraft 15 s spot -- {stats['lufs']:.2f} LUFS integrated, "
                 f"{stats['tp']:.2f} dBTP true peak, 48 kHz / 24-bit / {N} samples",
                 color="#F3F1F5", fontsize=13, y=0.93)
    fig.savefig(path, dpi=110, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def plot_overview_pil(path: str, y: np.ndarray, cues: dict):
    from PIL import Image, ImageDraw
    W, H = 1800, 900
    img = Image.new("RGB", (W, H), (17, 16, 20))
    dr = ImageDraw.Draw(img)
    mono = 0.5 * (y[0] + y[1])
    f, tt, Z = signal.stft(mono, fs=SR, nperseg=2048, noverlap=2048 - 240)
    S = 20 * np.log10(np.abs(Z) + 1e-9)
    S -= S.max()
    fl = np.geomspace(25, 20000, 600)
    Sl = np.stack([np.interp(fl, f, S[:, j]) for j in range(S.shape[1])], axis=1)
    v = np.clip((Sl + 95) / 95, 0, 1)[::-1]
    rgb = (np.stack([v ** 0.8, v ** 2.2, 0.35 * v + 0.15 * v ** 4], axis=-1) * 255).astype(np.uint8)
    img.paste(Image.fromarray(rgb).resize((W, 600)), (0, 300))
    hop = N // W
    for x in range(W):
        seg = mono[x * hop:(x + 1) * hop]
        dr.line([(x, 150 - seg.max() * 140), (x, 150 - seg.min() * 140)], fill=(255, 178, 26))
    for c in cues["sfx"]:
        x = int(c["t"] / DUR * W)
        dr.line([(x, 0), (x, H)], fill=(200, 200, 200))
    for s in cues["sections"]:
        x = int(s["start"] / DUR * W)
        dr.line([(x, 0), (x, H)], fill=(91, 209, 255), width=3)
        dr.text((x + 4, 4), s["name"], fill=(91, 209, 255))
    img.save(path)


# =============================================================================
# 15. MAIN
# =============================================================================
def main():
    t_start = time.time()
    with open(CUE_PATH, "r", encoding="utf-8") as fh:
        cues = json.load(fh)
    assert abs(cues["bpm"] - BPM) < 1e-9 and abs(cues["duration_s"] - DUR) < 1e-9, "cues30.json mismatch"
    os.makedirs(STEM_DIR, exist_ok=True)

    print("building reverbs ...")
    irs = {"plate": make_ir(1.15, 1.6, "ir_plate", predelay=0.018, hf=0.45),
           "room": make_ir(0.45, 0.7, "ir_room", predelay=0.006, hf=0.5),
           "hall": make_ir(2.3, 3.0, "ir_hall", predelay=0.025, hf=0.4)}
    fx_music = {"plate": lambda b: 0.55 * reverb_return(b, irs["plate"], 220.0, 9000.0),
                "room": lambda b: 0.45 * reverb_return(b, irs["room"], 300.0, 9000.0),
                "hall": lambda b: 0.7 * reverb_return(b, irs["hall"], 160.0, 8500.0),
                "delay": lambda b: 0.5 * pingpong(b, 0.375, 0.45, 4, 3800.0, 350.0)}
    fx_sfx = {"plate": lambda b: 0.5 * reverb_return(b, irs["plate"], 250.0, 10000.0),
              "room": lambda b: 0.5 * reverb_return(b, irs["room"], 200.0, 9000.0),
              "hall": lambda b: 0.6 * reverb_return(b, irs["hall"], 150.0, 9000.0)}

    print("rendering music ...")
    m_pre, m_brk, m_grv, m_end = build_music(irs)
    print("rendering sfx ...")
    s_pre, s_pre2, s_post, duck_events = build_sfx(cues)

    print("bus processing ...")
    cut_gate = gate_curve([(CUT_T - 0.002, 1.0), (CUT_T, 0.0)])           # hard cut at 2.98
    stop_dry = gate_curve([(STOP_T - 0.004, 1.0), (STOP_T, 0.0)])         # drums stop at 12.5
    stop_wet = gate_curve([(STOP_T, 1.0), (STOP_T + 0.12, 0.0)])
    cut2_gate = gate_curve([(CUT2_T - 0.002, 1.0), (CUT2_T, 0.0)])         # hard cut at 21.98
    # lin_pre (HPF + mono lows) runs per bus BEFORE the gates so that no
    # filter ringing can leak through the hard cut / the stop.
    d, w = m_pre.render(fx_music)
    music = lin_pre(d + w) * cut_gate
    d, w = m_brk.render(fx_music)
    music += lin_pre(d + w) * cut2_gate
    d, w = m_grv.render(fx_music)
    music += lin_pre(d) * stop_dry + lin_pre(w) * stop_wet
    d, w = m_end.render(fx_music)
    music += lin_pre(d + w)
    d, w = s_pre.render(fx_sfx)
    sfx = lin_pre(d + w) * cut_gate
    d, w = s_pre2.render(fx_sfx)
    sfx += lin_pre(d + w) * cut2_gate
    d, w = s_post.render(fx_sfx)
    sfx += lin_pre(d + w)

    music *= duck_curve(duck_events)                                       # SFX cut through
    end_fade = gate_curve([(29.15, 1.0), (SILENT_T, 0.0)])
    music *= end_fade
    sfx *= end_fade
    music_gain = db2lin(0.0)
    sfx_gain = db2lin(0.0)

    print("mastering ...")
    y, stem_m, stem_s, minfo = master(music * music_gain, sfx * sfx_gain)

    lufs = lufs_integrated(y)
    tp = true_peak_db(y)
    write_wav24(os.path.join(HERE, "soundtrack30.wav"), y, "dither_master")
    write_wav24(os.path.join(STEM_DIR, "music30.wav"), stem_m, "dither_music")
    write_wav24(os.path.join(STEM_DIR, "sfx30.wav"), stem_s, "dither_sfx")

    # ------------------------------------------------------------------ verify
    yr, sr = read_wav24(os.path.join(HERE, "soundtrack30.wav"))
    stats = dict(lufs=lufs_integrated(yr), tp=true_peak_db(yr), sr=sr, samples=yr.shape[1],
                 peak_dbfs=float(lin2db(np.max(np.abs(yr)))),
                 dc=[float(np.mean(yr[0])), float(np.mean(yr[1]))],
                 clipped=int(np.sum(np.abs(yr) >= 0.99999)))
    print("\n=== MASTER ===")
    print(f"  samples {stats['samples']} @ {stats['sr']} Hz  ({stats['samples'] / sr:.6f} s)")
    print(f"  integrated loudness {stats['lufs']:.2f} LUFS   true peak {stats['tp']:.2f} dBTP   "
          f"sample peak {stats['peak_dbfs']:.2f} dBFS")
    print(f"  DC L/R {stats['dc'][0]:.2e} / {stats['dc'][1]:.2e}   clipped samples {stats['clipped']}")
    print(f"  glue comp GR max {minfo['comp_gr_max_db']:.2f} dB (mean groove {minfo['comp_gr_mean_db']:.2f})"
          f"   limiter GR max {minfo['lim_gr_max_db']:.2f} dB (mean groove {minfo['lim_gr_mean_db']:.2f})")
    print(f"  silence after {SILENT_T}s: max |x| = {np.max(np.abs(yr[:, ns(SILENT_T):])):.2e}")
    gap = yr[:, ns(CUT_T):ns(DROP_T)]
    print(f"  pre-drop gap 2.98-3.00: max |x| = {np.max(np.abs(gap)):.2e}")
    print("\n=== SYNC (onset = first sample >= -20 dB of the event's peak) ===")
    worst = 0.0
    for e in EVENT_LOG:
        err = (e["onset"] - e["cue"]) * 1000.0
        worst = max(worst, abs(err))
        pk = f"{e['peak']:.4f}" if e["peak"] is not None else "   -  "
        print(f"  {e['cue']:6.3f}s  {e['type']:<20s} start {e['start']:.4f}  onset {e['onset']:.4f} "
              f"({err:+5.2f} ms)  peak {pk}")
    print(f"  worst onset error: {worst:.2f} ms")

    print("\n=== MUSICAL BOUNDARIES (measured on the rendered files) ===")
    mr, _ = read_wav24(os.path.join(STEM_DIR, "music30.wav"))
    absy = np.max(np.abs(yr), axis=0)
    loud_pre = np.nonzero(absy[:ns(DROP_T)] > db2lin(-60.0))[0]
    print(f"  hard cut   : last sample > -60 dBFS before the drop at {loud_pre[-1] / SR:.4f} s (cue {CUT_T})")
    seg = np.max(np.abs(mr[:, ns(2.99):ns(3.1)]), axis=0)
    t_drop = (ns(2.99) + int(np.argmax(seg >= 0.1 * seg.max()))) / SR
    print(f"  drop       : music onset {t_drop:.4f} s (cue {DROP_T})")
    low = filt(mr, "lowpass", 160.0, 4)
    lo_env = np.max(np.abs(low[:, ns(27.0):ns(27.8)]), axis=0)
    last = ns(27.0) + int(np.nonzero(lo_env > 0.05 * lo_env.max())[0][-1])
    print(f"  drums stop : last kick/bass energy > -26 dB at {last / SR:.4f} s (cue {STOP_T})")
    seg = absy[ns(27.99):ns(28.1)]
    t_fin = (ns(27.99) + int(np.argmax(seg >= 0.5 * seg.max()))) / SR
    print(f"  final hit  : master reaches -6 dB of hit peak at {t_fin:.4f} s (cue {FINAL_T})")
    nz = np.nonzero(absy > db2lin(-90.0))[0]
    print(f"  silence    : last sample > -90 dBFS at {nz[-1] / SR:.4f} s (cue {SILENT_T})")
    for name, tm in (("music", stem_m), ("sfx", stem_s)):
        print(f"  stem {name}: {lufs_integrated(tm):.2f} LUFS, TP {true_peak_db(tm):.2f} dBTP")

    plot_overview(os.path.join(HERE, "spectrogram30.png"), yr, stem_m, stem_s, cues, stats)
    print(f"\ndone in {time.time() - t_start:.1f} s")
    return stats


if __name__ == "__main__":
    main()
