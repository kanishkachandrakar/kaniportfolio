# audio

`track.m4a` is what the hero portrait spins to. It is hers, recorded rather
than borrowed, so the repo carries nothing it does not own.

AAC in an m4a container, mono, 48kHz, about ten seconds. The element loops it,
so it plays until the button is pressed again. Small enough not to matter on
the home page at roughly 136KB, which is why it stays AAC rather than being
re-encoded to mp3 for size it does not need to save.

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
