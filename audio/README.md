# audio

Drop the track the hero portrait spins to in here as `track.mp3`.

`site.js` only reveals the play button once the file reports that it has
loaded, so until one is here the button never appears — the page has no dead
control on it, and nothing else changes.

Anything a browser can play works; the element points at `track.mp3`, so
either name the file that or change the `src` in the build's `HOME` block.
Keep it small — it downloads on the home page.
