# audio

Drop the track the hero portrait spins to in here as `track.mp3`.

`site.js` only reveals the play button once the file reports that it has
loaded, so until one is here the button never appears — the page has no dead
control on it, and nothing else changes.

`track.wav` here now is a placeholder, synthesised by
`tools-make-track.py` — a slow four-chord loop, generated rather than
borrowed so the repo carries nothing it does not own. Replace it.

Anything a browser can play works. The element points at this filename,
so either match it or change the `src` in the build's `HOME` block. Keep
it small: it downloads on the home page, and a real track should be an
mp3 rather than a wav for that reason.
