# -*- coding: utf-8 -*-
"""Música synthwave procedural (100% original, sin copyright) + efectos de sonido."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100


def _lp(x, fc, order=2):
    return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)


def _hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def _bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def saw(freq, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((t * freq + phase) % 1.0) - 1


def synthwave(duration, bpm=100, root=57, seed=0, style=0):
    """Genera una pista de fondo de `duration` segundos."""
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    out_pad = np.zeros(n)
    out_bass = np.zeros(n)
    out_arp = np.zeros(n)
    out_drum = np.zeros(n)
    beat = 60.0 / bpm
    bar = 4 * beat
    progs = [
        [(0, "m"), (-4, "M"), (3, "M"), (-2, "M")],   # i VI III VII
        [(0, "m"), (-2, "M"), (-4, "M"), (-2, "M")],  # i VII VI VII
        [(0, "m"), (5, "m"), (-4, "M"), (-2, "M")],   # i iv VI VII
    ]
    prog = progs[style % len(progs)]
    nbars = int(np.ceil(duration / bar)) + 1

    # --- percusión precalculada
    kl = int(0.35 * SR)
    tk = np.arange(kl) / SR
    kick = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-tk * 30)) / SR) * np.exp(-tk * 9)
    sl = int(0.25 * SR)
    ts = np.arange(sl) / SR
    snare = (_bp(rng.standard_normal(sl), 800, 7000) * 0.7 + 0.4 * np.sin(2 * np.pi * 190 * ts)) * np.exp(-ts * 18)
    hl = int(0.06 * SR)
    th = np.arange(hl) / SR
    hat = _hp(rng.standard_normal(hl), 7000) * np.exp(-th * 70)

    def add(buf, sig, start):
        s = int(start * SR)
        if s >= n:
            return
        e = min(n, s + len(sig))
        buf[s:e] += sig[: e - s]

    for b in range(nbars):
        t0 = b * bar
        off, q = prog[b % 4]
        third = 3 if q == "m" else 4
        chord = [root + off, root + off + third, root + off + 7]
        # pad: sierra desafinada
        L = int(bar * SR) + int(0.3 * SR)
        env = np.minimum(1, np.arange(L) / (0.25 * SR)) * np.minimum(1, (L - np.arange(L)) / (0.3 * SR))
        pad = np.zeros(L)
        for m in chord:
            f = mtof(m)
            for d in (-0.12, 0.0, 0.12):
                pad += saw(f * 2 ** (d / 12), L, rng.random())
        add(out_pad, pad * env / 9.0, t0)
        # bajo en corcheas
        bf = mtof(root + off - 24)
        for k in range(8):
            ln = int(beat / 2 * SR * 0.9)
            tt = np.arange(ln) / SR
            note = saw(bf, ln) * np.exp(-tt * 6)
            add(out_bass, note, t0 + k * beat / 2)
        # arpegio en semicorcheas
        arp_notes = [chord[0] + 12, chord[1] + 12, chord[2] + 12, chord[1] + 24]
        for k in range(16):
            m = arp_notes[k % 4]
            ln = int(0.22 * SR)
            tt = np.arange(ln) / SR
            f = mtof(m)
            tone = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 14)
            add(out_arp, tone, t0 + k * beat / 4)
        # batería (entra en el compás 1)
        if b >= 1 or style == 2:
            for k in range(4):
                add(out_drum, kick * 0.9, t0 + k * beat)
                if k in (1, 3):
                    add(out_drum, snare * 0.45, t0 + k * beat)
            for k in range(8):
                add(out_drum, hat * (0.18 if k % 2 else 0.1), t0 + k * beat / 2)

    out_pad = _lp(out_pad, 1800)
    out_bass = _lp(out_bass, 500)
    # delay en el arpegio (corchea con puntillo)
    dl = int(beat * 0.75 * SR)
    delayed = np.zeros(n)
    delayed[dl:] = out_arp[:-dl] * 0.35
    out_arp = _lp(out_arp + delayed, 4000)

    mix = 0.55 * out_pad + 0.7 * out_bass + 0.22 * out_arp + 0.6 * out_drum
    # fade in/out
    fi = int(0.4 * SR)
    fo = int(1.5 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)
    mix[-fo:] *= np.linspace(1, 0, fo)
    mix /= np.max(np.abs(mix)) + 1e-9
    return (mix * 0.9).astype(np.float32)


def whoosh(seed=0, dur=0.45):
    rng = np.random.default_rng(seed)
    L = int(dur * SR)
    t = np.linspace(0, 1, L)
    noise = rng.standard_normal(L)
    # barrido: mezcla de bandas que sube de grave a agudo
    lo = _bp(noise, 300, 1500)
    hi = _bp(noise, 2000, 8000)
    sig = lo * (1 - t) + hi * t
    env = np.sin(np.pi * np.clip(t, 0, 1)) ** 2
    sig = sig * env
    return (sig / (np.max(np.abs(sig)) + 1e-9) * 0.6).astype(np.float32)


def impact(seed=0):
    L = int(0.5 * SR)
    t = np.arange(L) / SR
    boom = np.sin(2 * np.pi * np.cumsum(40 + 80 * np.exp(-t * 25)) / SR) * np.exp(-t * 7)
    rng = np.random.default_rng(seed)
    crack = _hp(rng.standard_normal(L), 3000) * np.exp(-t * 40) * 0.3
    s = boom + crack
    return (s / np.max(np.abs(s)) * 0.8).astype(np.float32)


def pop():
    L = int(0.08 * SR)
    t = np.arange(L) / SR
    s = np.sin(2 * np.pi * (900 - 4000 * t) * t) * np.exp(-t * 60)
    return (s * 0.35).astype(np.float32)
