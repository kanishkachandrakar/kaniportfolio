# kaniportfolio

Personal portfolio for **Kanishka Chandrakar** — MS Computer Science (AI/ML) at
NYU Courant.

Live: <https://kanishkachandrakar.github.io/kaniportfolio/>

## What's here

Seven static pages sharing one shell: a full-bleed backdrop, a floating glass
card, and a rail of icons that show artwork on hover. No framework, no build
step to install — the HTML is committed and served as-is.

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

## Tools

Small scripts that generate committed artwork. Each is standalone and only
needs Pillow.

| Script | Makes |
| --- | --- |
| `tools-make-backdrop.py` | The scenic backdrop behind the card |
| `tools-make-peek-art.py` | Rail icons and the hover artwork |
| `tools-rasterize-peeks.py` | Those SVGs, as WebP |
| `tools-make-cutout.py` | The headshot, with its background removed |
| `tools-blank-eyes.py` | Clears the sockets in the About avatar and cuts out an iris, so `site.js` can make the eyes follow the pointer |

`tools-blank-eyes.py` reads the untouched crop, so restore
`images/kani-about.webp` from `images/kani-edit.png` before re-running it.

## Not in use

`knowmemore.html` and `navbar.html` are from the site that came before this
one. Nothing links to them and they are not in the sitemap; they are kept only
so the content is not lost.
