# audio

`track.m4a` is what the hero portrait spins to. It is hers, recorded rather
than borrowed, so the repo carries nothing it does not own.

AAC in an m4a container, mono, 48kHz, about ten seconds. The element loops it,
so it plays until the button is pressed again. Small enough not to matter on
the home page at roughly 136KB, which is why it stays AAC rather than being
re-encoded to mp3 for size it does not need to save.

`site.js` only reveals the play button once the file reports that it has
loaded, so if this is ever missing or in a format the browser will not take,
the button never appears and the page carries no dead control.

The element points at this filename. Replacing the track means either matching
the name or changing the `src` in index.html.
