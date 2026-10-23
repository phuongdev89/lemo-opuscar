"""Whiteboard Audio Mixer for Tuoi Me Con:
Foley (procedural marker squeaks, strokes, taps, cap pops) + Voiceover + Minimalist clockwork score -> out/mix.wav
"""
import sys, os, json, numpy as np, soundfile as sf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from core.audio.sfx import SR, bp, lp, hp, noise, add, compress, limit

HERE = os.path.dirname(os.path.abspath(__file__))
ev_data = json.load(open(os.path.join(HERE, 'events.json')))
E = ev_data['ev']
DUR = ev_data['dur']

rng = np.random.default_rng(42)
NS = int((DUR + 1.5) * SR)
fol = np.zeros((NS, 2), np.float32)
room = np.zeros((NS, 2), np.float32)
vo = np.zeros((NS, 2), np.float32)
music = np.zeros((NS, 2), np.float32)

tt = lambda d: np.arange(int(d * SR)) / SR
def dec(d, tau): return np.exp(-tt(d) / tau)

# 1. Foley: dry-erase marker synthesis
_band = {}
def band(n, lo, hi):
    k = (lo, hi)
    if k not in _band:
        _band[k] = bp(rng.standard_normal(SR * 8), lo, hi, 2).astype(np.float32)
    b = _band[k]
    i = int(rng.integers(0, len(b) - n - 1))
    return b[i:i + n]

def marker(dur, length, kind, pen):
    d = max(0.03, dur)
    n = int(d * SR)
    u = np.linspace(0, 1, n)
    v = 1 - 0.8 * np.cos(2 * np.pi * u)
    a = (v / 1.8) ** 0.8 * np.minimum(1, u * d / 0.006) * np.minimum(1, (1 - u) * d / 0.012)
    br = {'k': 1.0, 'b': 0.92, 'r': 1.15, 'g': 0.95}.get(pen, 1.0)
    hiss = band(n, 2200 * br, 7500 * br) * (0.55 + 0.45 * v / 1.8)
    body = band(n, 500 * br, 1500 * br) * 0.45
    grain = (rng.random(n) < 0.004 * (1 + v)) * rng.standard_normal(n) * 0.8
    x = (hiss + body + bp(grain, 1500, 6000)) * a

    # Squeak on longer strokes
    if kind != 'dash' and length > 120 and rng.random() < 0.25:
        s0 = rng.uniform(0.15, 0.55) * d
        sd = min(d - s0, rng.uniform(0.06, 0.15))
        if sd > 0.03:
            m = int(sd * SR)
            ts = np.arange(m) / SR
            f0 = rng.uniform(1600, 2500) * br
            f = f0 * (1 + 0.03 * np.sin(2 * np.pi * rng.uniform(8, 12) * ts))
            sq = np.sin(2 * np.pi * np.cumsum(f) / SR)
            sq *= np.sin(np.pi * ts / sd) ** 1.5 * 0.3
            i0 = int(s0 * SR)
            x[i0:i0 + m] += sq[:len(x) - i0]

    # Nib landing tick
    tick_len = int(0.004 * SR)
    x[:tick_len] += bp(rng.standard_normal(tick_len), 2500, 6500) * np.linspace(1, 0, tick_len) * 1.2
    return x * 0.28

def tap():
    n = int(0.03 * SR)
    x = bp(rng.standard_normal(n), 1800, 6000) * dec(0.03, 0.004) * 1.2
    return x * 0.25

def cap_pop():
    d = 0.25
    x = np.zeros(int(d * SR))
    sl = bp(rng.standard_normal(int(0.07 * SR)), 1200, 5000) * np.linspace(0.2, 1, int(0.07 * SR)) * 0.35
    x[:len(sl)] += sl
    t = tt(d - 0.07)
    p = np.sin(2 * np.pi * 1750 * t) * np.exp(-t / 0.03) * 0.8
    x[len(sl):len(sl) + len(p)] += p
    return x * 0.6

def cap_on():
    d = 0.2
    x = np.zeros(int(d * SR))
    c = bp(rng.standard_normal(int(0.006 * SR)), 2500, 9000) * np.linspace(1, 0, int(0.006 * SR))
    x[:len(c)] += c
    t = tt(0.06)
    r = np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.015) * 0.4
    x[:len(r)] += r
    return x * 0.7

print("Synthesizing foley...")
# Marker cap off at start
add(fol, cap_pop(), at=0.3, gain=0.6, pan=-0.2)

# Generate foley for every stroke
for e in E:
    t = e.get('t', 0)
    typ = e.get('type')
    if typ in ('stroke', 'write'):
        dur = e.get('dur', 0.2)
        length = e.get('len', 100)
        pen = e.get('pen', 'k')
        pan = (e.get('x', 960) - 960) / 1400.0
        pan = max(-0.8, min(0.8, pan))
        s = marker(dur, length, typ, pen)
        add(fol, s, at=t, gain=0.85, pan=pan)
    elif typ == 'tap':
        add(fol, tap(), at=t, gain=0.6, pan=0.0)

# Marker cap on at end
add(fol, cap_on(), at=33.2, gain=0.7, pan=0.2)

# Room tone
rt = lp(rng.standard_normal(NS), 350) * 0.008
room[:, 0] += rt
room[:, 1] += rt

# 2. Voiceover (VO)
print("Adding voiceover...")
vo_timings = [
    ("line_1", 0.5),
    ("line_2", 7.6),
    ("line_3", 14.6),
    ("line_4", 21.0),
    ("line_5", 25.8),
    ("line_6", 32.2)
]

for lid, t_start in vo_timings:
    wav_file = os.path.join(HERE, 'voices', f"{lid}.wav")
    if os.path.exists(wav_file):
        y, sr = sf.read(wav_file)
        if sr != SR:
            import soxr
            y = soxr.resample(y, sr, SR)
        # Gentle voice compression
        y = compress(y, thr=0.2, ratio=3.0) * 1.3
        add(vo, y, at=t_start, gain=1.0, pan=0.0)

# 3. Minimalist Clockwork Score (D Major / A Major, 112 BPM)
print("Synthesizing score...")
BPM = 112.0
BEAT = 60.0 / BPM

def synth_bell(freq, dur, vel=0.6):
    t = np.arange(int(dur * SR)) / SR
    # Additive harmonics with fast initial decay
    env = np.exp(-t / 0.45)
    sig = np.sin(2 * np.pi * freq * t) * 0.6
    sig += np.sin(2 * np.pi * freq * 2 * t) * 0.25 * np.exp(-t / 0.25)
    sig += np.sin(2 * np.pi * freq * 3 * t) * 0.12 * np.exp(-t / 0.15)
    return sig * env * vel

def synth_wood(freq, dur=0.05, vel=0.4):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t / 0.012)
    sig = np.sin(2 * np.pi * freq * t) * env * vel
    return sig

def synth_pizz(freq, dur=0.8, vel=0.5):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t / 0.35)
    sig = np.sin(2 * np.pi * freq * t) * 0.7
    sig += np.sin(2 * np.pi * freq * 2 * t) * 0.25 * np.exp(-t / 0.2)
    return sig * env * vel

# Chords progression: D -> G -> A -> D (D major)
# Frequencies
PITCH = {
    'D3': 146.83, 'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
    'D4': 293.66, 'E4': 329.63, 'F#4': 369.99, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C#5': 554.37, 'D5': 587.33, 'E5': 659.25, 'F#5': 739.99, 'A5': 880.00
}

total_beats = int(DUR / BEAT) + 2
for b in range(total_beats):
    t_b = b * BEAT
    if t_b > DUR + 0.5: break

    # Woodblock clock tick on every beat
    w_freq = 950 if (b % 4 == 0) else (780 if (b % 2 == 0) else 820)
    w_gain = 0.35 if (b % 2 == 0) else 0.22
    add(music, synth_wood(w_freq, vel=w_gain), at=t_b, gain=0.45, pan=0.25)

    # Pizzicato bass on beat 1 and 3 of every measure
    bar = b // 4
    beat_in_bar = b % 4
    chord_roots = ['D3', 'G3', 'A3', 'D3']
    root = chord_roots[bar % len(chord_roots)]

    if beat_in_bar in (0, 2):
        freq = PITCH[root] if beat_in_bar == 0 else PITCH[root] * 1.5
        add(music, synth_pizz(freq, dur=0.6, vel=0.55), at=t_b, gain=0.6, pan=-0.1)

    # Marimba / Bell pattern (8th notes)
    pattern = ['D4', 'F#4', 'A4', 'F#4', 'D5', 'A4', 'F#4', 'A4']
    note = pattern[b % len(pattern)]
    add(music, synth_bell(PITCH[note], dur=0.5, vel=0.45), at=t_b + 0.5 * BEAT, gain=0.5, pan=0.15)

# Duck music under voiceover
vo_rms = lp(np.abs(vo.mean(axis=1)), 8)
duck = np.clip(1.0 - vo_rms * 2.2, 0.25, 1.0)
music[:, 0] *= duck
music[:, 1] *= duck

# Master mix
print("Balancing and mastering mix...")
mix = vo * 0.85 + fol * 0.60 + music * 0.35 + room
mix[:, 0] = limit(mix[:, 0], ceil=0.75)
mix[:, 1] = limit(mix[:, 1], ceil=0.75)

out_dir = os.path.join(HERE, 'out')
os.makedirs(out_dir, exist_ok=True)
mix_path = os.path.join(out_dir, 'mix.wav')
sf.write(mix_path, mix, SR)
print(f"Mix saved to {mix_path} ({DUR}s)")
