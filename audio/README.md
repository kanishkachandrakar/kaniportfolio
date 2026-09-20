# audio

`track.m4a` is what the hero portrait spins to. It is composed by
`tools-make-track.py` rather than licensed: a commercial song on a public
GitHub Pages site is somebody else's rights problem waiting to happen, and the
repo carries nothing it does not own.

A slow D major loop at 56bpm, I-vi-IV-V with sevenths, a sustained pad, a
sparse arpeggio and one bass note a bar. Nothing percussive and nothing that
moves quickly - it is meant to go on behind a problem you are already stuck on.
It loops without a seam, because the piece is rendered longer than the loop
and the overflowing tail is folded back onto the start.

AAC in an m4a container, mono, 22.05kHz, 34 seconds, about 200KB. The element
loops it, so it plays until the button is pressed again.

To change it, change the notes in the generator and re-encode:

    python3 tools-make-track.py
    afconvert -f m4af -d aac -b 64000 audio/track.wav audio/track.m4a

The wav it writes is the master and is gitignored - it is 1.5MB and the m4a is
the thing the page loads.

`sent.wav` and `reply.wav` are the two chimes the contact thread plays: one
rising as your message leaves, one falling as hers arrives. Both are
synthesised by `tools-make-chimes.py` rather than sampled, for the same reason
as everything else here. Mono, 22.05kHz, under a quarter of a second, 17KB for
the pair. Change the notes in the script rather than editing the binaries.

A browser refuses to play audio before the page has been interacted with, so
the first reply in the thread arrives silently and every one after it does
not. That is correct behaviour, not a bug to chase.

`site.js` only reveals the record's play button once the track reports that it
has loaded, so if that file is ever missing or in a format the browser will not
take, the button never appears and the page carries no dead control.

The elements point at these filenames. Replacing anything here means either
matching the name or changing the `src` in the page that uses it.
