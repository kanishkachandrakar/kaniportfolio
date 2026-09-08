"""Synthesise the placeholder track the hero portrait spins to.

Generated rather than borrowed, for the same reason the artwork is: the site
carries nothing it does not own. It is a slow four-chord loop on a soft
plucked tone - something to check the player against, meant to be replaced.

The loop is built to close on itself. Its length is a whole number of bars and
the last chord resolves back to the first, so <audio loop> repeats it without
a seam or a click.

    python3 tools-make-track.py  ->  audio/track.wav
"""

import math
import os
import struct
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "audio", "track.wav")

RATE = 22050          # plenty for a placeholder, and a quarter the size of 44k
BAR = 2.4             # seconds
CHORDS = [            # i - VI - III - VII in A minor, one per bar
    (220.00, 261.63, 329.63),
    (174.61, 220.00, 261.63),
    (261.63, 329.63, 392.00),
    (196.00, 246.94, 293.66),
]


def pluck(t, freq):
    """One note: a decaying sine with a little of its own second harmonic."""
    env = math.exp(-2.6 * t)
    return env * (math.sin(2 * math.pi * freq * t)
                  + 0.22 * math.sin(4 * math.pi * freq * t))


def main():
    total = int(RATE * BAR * len(CHORDS))
    frames = bytearray()
    for n in range(total):
        t = n / float(RATE)
        bar = int(t / BAR) % len(CHORDS)
        into = t - bar * BAR
        v = 0.0
        for i, freq in enumerate(CHORDS[bar]):
            # the notes of each chord land one after another, not together
            start = i * 0.18
            if into >= start:
                v += pluck(into - start, freq) * 0.30
        # a low root underneath, held for the whole bar
        v += 0.16 * math.sin(2 * math.pi * CHORDS[bar][0] / 2 * into) \
            * math.exp(-0.5 * into)
        # ease the very start and end of the loop to zero so it can join up
        edge = min(t, total / float(RATE) - t)
        if edge < 0.04:
            v *= edge / 0.04
        frames += struct.pack("<h", int(max(-1.0, min(1.0, v)) * 26000))

    with wave.open(DST, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(frames))
    print("wrote %s  %.1fs  (%dKB)"
          % (os.path.relpath(DST, HERE), total / float(RATE),
             os.path.getsize(DST) // 1024))


if __name__ == "__main__":
    main()
