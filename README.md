# kaniportfolio

Personal portfolio for **Kanishka Chandrakar** — MS Computer Science (AI/ML) at
NYU Courant.

Live: <https://kanishkachandrakar.github.io/kaniportfolio/>

## What's here

Seven static pages sharing one shell: a full-bleed backdrop, a floating glass
card, and a rail of icons that show artwork on hover. No framework, no build
step to install — the HTML is committed and served as-is.

## Themes

Two of them, dark and light, swapped by pulling the lamp cord hanging into the
top of the page.

Everything either theme changes is a custom property in one of two blocks at
the top of `site.css`; no rule below them names a colour. Adding a third would
be another block, not another pass through the file.

The choice is remembered in `localStorage`. Until one is made the system
setting decides, and keeps deciding — pulling the cord ends that, because an
explicit choice should outrank it. A small script in `<head>` applies the
theme before the stylesheet loads, so the page is never painted in one theme
and repainted in the other.

Two things are deliberately not themed. The bento illustrations were drawn on
a dark card and carry that background in their pixels, so those tiles stay
dark under both and read as image tiles; cutting the figures out does not
work, because the card is darker than parts of her hair. And the rail hues are
one set, chosen to hold up on either ground.

| | |
| --- | --- |
| `index.html` | Hero, plus the Explore grid |
| `about.html` · `education.html` | Background and studies |
| `skills.html` · `work.html` | What she uses, and where |
| `projects.html` | Twelve builds, with a modal per project |
| `connect.html` | Contact |
| `site.css` · `site.js` | The whole design system and behaviour |

Asset links carry `?v=<hash of the file>`, so a stale cached copy can never
pair with fresh markup.

## Music

The hero portrait is a record. A play button sits on its lower right, and the
photograph turns while a track plays.

`audio/track.wav` is a placeholder synthesised by `tools-make-track.py` —
generated rather than borrowed, like the rest of the artwork. Replace it with
something real; an mp3, since it downloads on the home page.

Two things worth keeping if this is edited:

- **The button is hidden until the file reports that it loaded.** A missing or
  unplayable track leaves no dead control on the page.
- **The spin follows the audio element, not the button.** Playback stops for
  reasons that never reach a click handler — the track ending, another tab
  taking the audio, the media keys — and the photograph should stop with it.

The rotation is paused rather than removed when the music stops, so the
picture holds its angle instead of snapping upright, and it is dropped
entirely under `prefers-reduced-motion` — the music still plays.

## Tools

Small scripts that generate committed artwork. Each is standalone and only
needs Pillow.

| Script | Makes |
| --- | --- |
| `tools-make-backdrop.py` | Both backdrops — one composition, two palettes |
| `tools-make-peek-art.py` | Rail icons and the hover artwork |
| `tools-rasterize-peeks.py` | Those SVGs, as WebP |
| `tools-make-cutout.py` | The headshot, with its background removed |
| `tools-blank-eyes.py` | Clears the sockets in the About avatar and cuts out an iris, so `site.js` can make the eyes follow the pointer |
| `tools-make-memoji.py` | Keys the card out from behind her Memoji for the top-bar avatar |
| `tools-make-portrait.py` | Cuts the square hero portrait out of the full-frame photograph |
| `tools-make-track.py` | The placeholder music loop |

Two of these have an order to them. `tools-blank-eyes.py` reads the untouched
crop, so restore `images/kani-about.webp` from `images/kani-edit.png` before
re-running it. And `tools-rasterize-peeks.py` runs after
`tools-make-peek-art.py`, never before.

Each tool reads only from `images/`. That is worth keeping: the peek generator
once read its photographs from a scratch directory outside the repo, and when
that directory went away the tool could not be run at all.

## Not in use

`knowmemore.html` and `navbar.html` are from the site that came before this
one. Nothing links to them and they are not in the sitemap; they are kept only
so the content is not lost.
