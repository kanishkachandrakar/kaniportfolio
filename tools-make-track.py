"""Compose the track the hero portrait spins to.

Generated rather than licensed. A commercial song on a public GitHub Pages
site is somebody else's rights problem waiting to happen, and the rest of the
media here follows the same rule: the site carries nothing it does not own.

What it is: a slow D major loop at 56bpm, I-vi-IV-V with sevenths on
everything, which is about the most reliably calming progression in western
music and resolves back to its own first chord. A sustained pad underneath, a
sparse arpeggio over it, one bass note a bar. Nothing percussive, nothing that
moves quickly, nothing that asks for attention - it is meant to be put on
behind a problem you are already stuck on.

It loops without a seam. The piece is rendered longer than the loop and the
overflowing tail is folded back onto the start, so the notes still decaying at
the end carry across the join instead of being cut off at it.

The wav it writes is the master and is not committed - it is 1.5MB. Encode it
and ship that:

    python3 tools-make-track.py
    afconvert -f m4af -d aac -b 64000 audio/track.wav audio/track.m4a

Which comes out around 200KB for 34 seconds, and the <audio> element on the
home page already points at that filename.
"""

import math
import os
import struct
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "audio", "track.wav")

RATE = 22050
BPM = 56.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT

# D major. Sevenths throughout: a plain triad is brighter and more declarative
# than this wants to be.
def note(semitones_from_a4):
    return 440.0 * (2 ** (semitones_from_a4 / 12.0))

D3, A3 = note(-19), note(-12)
G3, B3 = note(-14), note(-10)

CHORDS = [
    # root for the bass, then the voicing the pad and arpeggio draw from
    (D3, [note(-7), note(-3), note(0), note(5)]),    # Dmaj7
    (B3 / 2, [note(-10), note(-3), note(2), note(5)]),   # Bm7
    (G3, [note(-5), note(-1), note(2), note(7)]),    # Gmaj7
    (A3, [note(-7), note(0), note(4), note(7)]),     # A7sus4
]

# Eight bars: the progression twice, the second pass an octave up on the
# arpeggio so the loop has somewhere to go before it comes back.
BARS = 8
LOOP = BARS * BAR
TAIL = 4.0                      # rendered past the end, then folded back


def pluck(buf, start, freq, gain, decay=2.4):
    """A soft plucked voice: quick in, long out, two quiet harmonics."""
    n = int(RATE * decay)
    i0 = int(RATE * start)
    for i in range(n):
        j = i0 + i
        if j >= len(buf):
            break
        t = i / RATE
        a = min(1.0, t / 0.006) * math.exp(-t * (3.2 / decay))
        v = math.sin(2 * math.pi * freq * t)
        v += 0.38 * math.sin(4 * math.pi * freq * t)
        v += 0.16 * math.sin(6 * math.pi * freq * t)
        buf[j] += v * a * gain


def pad(buf, start, freq, gain, length):
    """A sustained voice, detuned against itself so it breathes a little."""
    n = int(RATE * (length + 1.2))
    i0 = int(RATE * start)
    for i in range(n):
        j = i0 + i
        if j >= len(buf):
            break
        t = i / RATE
        a = min(1.0, t / 0.9)                      # slow in
        if t > length:
            a *= math.exp(-(t - length) * 2.2)     # slow out
        v = math.sin(2 * math.pi * freq * t)
        v += math.sin(2 * math.pi * freq * 1.004 * t)   # the detune
        v += 0.22 * math.sin(4 * math.pi * freq * t)
        buf[j] += v * a * gain * 0.5


def bass(buf, start, freq, gain):
    n = int(RATE * 3.2)
    i0 = int(RATE * start)
    for i in range(n):
        j = i0 + i
        if j >= len(buf):
            break
        t = i / RATE
        a = min(1.0, t / 0.02) * math.exp(-t * 1.1)
        v = math.sin(2 * math.pi * freq * t) + 0.18 * math.sin(4 * math.pi * freq * t)
        buf[j] += v * a * gain


def build():
    total = int(RATE * (LOOP + TAIL))
    buf = [0.0] * total

    for b in range(BARS):
        t0 = b * BAR
        root, voicing = CHORDS[b % 4]
        second_pass = b >= 4

        bass(buf, t0, root / 2, 0.20)
        for f in voicing:
            pad(buf, t0, f / 2, 0.085, BAR * 0.96)

        # Arpeggio: four notes a bar on the off-eighths, which keeps it from
        # sounding metronomic, and an octave up on the second pass.
        pattern = [0, 2, 1, 3] if not second_pass else [3, 1, 2, 0]
        for k, idx in enumerate(pattern):
            f = voicing[idx] * (2 if second_pass else 1)
            pluck(buf, t0 + k * BEAT + BEAT * 0.5, f, 0.15)
            # one quiet echo, half a beat later, for depth without reverb
            pluck(buf, t0 + k * BEAT + BEAT * 1.0, f, 0.045, decay=1.6)

    # Fold the tail back onto the beginning so decaying notes cross the join.
    loop_n = int(RATE * LOOP)
    for i in range(total - loop_n):
        buf[i] += buf[loop_n + i]
    buf = buf[:loop_n]

    peak = max(abs(v) for v in buf) or 1.0
    scale = 0.72 / peak

    frames = bytearray()
    for i, v in enumerate(buf):
        v *= scale
        # a few milliseconds of taper at each end, so the join cannot click
        edge = int(RATE * 0.004)
        if i < edge:
            v *= i / edge
        elif i > loop_n - edge:
            v *= (loop_n - i) / edge
        frames += struct.pack("<h", int(max(-1.0, min(1.0, v)) * 32767))

    with wave.open(DST, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(frames))
    print("wrote %s (%.1fs)" % (DST, loop_n / RATE))


if __name__ == "__main__":
    build()
