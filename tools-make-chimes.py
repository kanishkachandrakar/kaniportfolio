"""Synthesise the two chimes the contact thread plays.

Generated rather than sampled, for the same reason the rest of the media here
is: the site carries nothing it does not own, and the one sound everybody
would reach for is a recording of somebody else's operating system.

`sent` is a short rising blip with a fast attack, which is what a message
leaving sounds like. `reply` is the same shape upside down, two notes falling,
so the two are recognisably a pair without being the same noise twice.

Both are mono at 22.05kHz and under a quarter of a second, because they play
on a keypress and download on a page nobody visits for the audio.

    python3 tools-make-chimes.py  ->  audio/sent.wav, audio/reply.wav
"""

import math
import os
import struct
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
RATE = 22050


def env(i, n, attack):
    """Fast in, slow out. A slow attack on a UI sound reads as a mistake."""
    a = int(n * attack)
    if i < a:
        return i / a
    t = (i - a) / (n - a)
    return math.exp(-4.5 * t)


def tone(dst, notes, seconds, attack, gain=0.32):
    n = int(RATE * seconds)
    frames = bytearray()
    for i in range(n):
        t = i / RATE
        p = i / n
        # glide between the notes rather than stepping, so it is one gesture
        idx = p * (len(notes) - 1)
        lo = int(idx)
        hi = min(lo + 1, len(notes) - 1)
        f = notes[lo] + (notes[hi] - notes[lo]) * (idx - lo)
        v = math.sin(2 * math.pi * f * t)
        v += 0.28 * math.sin(4 * math.pi * f * t)      # one harmonic for body
        v *= env(i, n, attack) * gain
        frames += struct.pack("<h", int(max(-1.0, min(1.0, v)) * 32767))
    with wave.open(dst, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(frames))
    print("wrote %s (%d frames)" % (dst, n))


if __name__ == "__main__":
    out = os.path.join(HERE, "audio")
    tone(os.path.join(out, "sent.wav"), [660, 1320], 0.16, 0.02)
    tone(os.path.join(out, "reply.wav"), [880, 587], 0.22, 0.05, gain=0.26)
