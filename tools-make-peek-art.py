# -*- coding: utf-8 -*-
"""Generate the rail icons and the artwork each one raises.

Both come from the same motif definitions, so an icon and the picture it
opens always share a shape and a colour. Run: python3 tools-make-peek-art.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# Each motif is drawn once, in a 24x24 box, with three colour slots. The
# icon fills them with a bright palette; the artwork fills all three with
# the section colour to use the same shape as a watermark.
MOTIFS = {
    "about":
        '<circle cx="12" cy="12" r="8.1" fill="{c1}"/>'
        '<circle cx="9.3" cy="10.5" r="1.35" fill="{c3}"/>'
        '<circle cx="14.7" cy="10.5" r="1.35" fill="{c3}"/>'
        '<path d="M8.3 13.9c.95 1.95 2.15 2.9 3.7 2.9s2.75-.95 3.7-2.9" '
        'stroke="{c3}" stroke-width="1.7" stroke-linecap="round" fill="none"/>',
    "education":
        '<polygon points="12,4.4 21.6,8.9 12,13.4 2.4,8.9" fill="{c1}"/>'
        '<path d="M6.6 10.9v4.6c0 1.75 2.4 3.05 5.4 3.05s5.4-1.3 5.4-3.05v-4.6'
        'L12 13.5z" fill="{c2}"/>'
        '<path d="M20.7 9.3v5.4" stroke="{c3}" stroke-width="1.35" '
        'stroke-linecap="round" fill="none"/>'
        '<circle cx="20.7" cy="15.8" r="1.6" fill="{c3}"/>',
    "skills":
        '<polygon points="12,3.2 20.4,8 12,12.8 3.6,8" fill="{c1}"/>'
        '<polygon points="3.6,8 12,12.8 12,21.4 3.6,16.6" fill="{c2}"/>'
        '<polygon points="20.4,8 12,12.8 12,21.4 20.4,16.6" fill="{c3}"/>',
    "projects":
        '<rect x="2.8" y="2.8" width="8.4" height="8.4" rx="2.7" fill="{c1}"/>'
        '<rect x="12.8" y="2.8" width="8.4" height="8.4" rx="2.7" fill="{c2}"/>'
        '<rect x="2.8" y="12.8" width="8.4" height="8.4" rx="2.7" fill="{c3}"/>'
        '<rect x="12.8" y="12.8" width="8.4" height="8.4" rx="2.7" fill="{c1}"/>',
    "work":
        '<path d="M12 2.4c3.1 2.3 4.8 5.8 4.8 9.6l-1.7 3.6H8.9l-1.7-3.6'
        'c0-3.8 1.7-7.3 4.8-9.6z" fill="{c1}"/>'
        '<circle cx="12" cy="10.1" r="2.3" fill="{c3}"/>'
        '<path d="M7.2 12.5 4.3 15.2v3.2l3.1-1.8zM16.8 12.5l2.9 2.7v3.2'
        'l-3.1-1.8z" fill="{c2}"/>'
        '<path d="M10.3 17.2h3.4L12 21.6z" fill="{c2}"/>',
    "contact":
        '<path d="M21.5 2.6 2.5 10.9l7.2 2.7 2.6 7.2z" fill="{c1}"/>'
        '<path d="M9.7 13.6 21.5 2.6l-6.4 16-2.7-5.2z" fill="{c2}"/>'
        '<circle cx="9.7" cy="13.6" r="1.25" fill="{c3}"/>',
}

# id, hue, deep hue, then the icon's own palette.
SECTIONS = [
    ("about",     "#E8B87C", "#96602A", "#FFEBCB", "#FFFFFF", "#6B441C"),
    ("education", "#8FB8EA", "#3F5F8E", "#FFFFFF", "#D9E7FA", "#2E4870"),
    ("skills",    "#93D3AC", "#3F7A5B", "#E9FBF1", "#86CCA5", "#2F6247"),
    ("projects",  "#C2A2EA", "#63479A", "#FFFFFF", "#EBD9FF", "#5B3E92"),
    ("work",      "#EBA277", "#96522C", "#FFFFFF", "#FFD2AE", "#7E3F1D"),
    ("contact",   "#E895AC", "#93475E", "#FFFFFF", "#FFD1DD", "#82374E"),
]


# ------------------------------------------------------------------ icons
def icon_svg(sid, hue, deep, c1, c2, c3):
    motif = MOTIFS[sid].format(c1=c1, c2=c2, c3=c3)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" '
        'width="48" height="48">'
        '<defs>'
        '<linearGradient id="b" x1="0.1" y1="0" x2="0.75" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        '</linearGradient>'
        '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.42"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>'
        '</linearGradient>'
        '</defs>'
        '<rect width="48" height="48" rx="13.5" fill="url(#b)"/>'
        '<path d="M0 13.5A13.5 13.5 0 0 1 13.5 0h21A13.5 13.5 0 0 1 48 13.5'
        'V22C36 28 12 28 0 22z" fill="url(#s)"/>'
        '<g transform="translate(24 25) scale(1.34) translate(-12 -12)">%s</g>'
        '<rect x="0.7" y="0.7" width="46.6" height="46.6" rx="12.9" '
        'fill="none" stroke="#FFFFFF" stroke-opacity="0.30"/>'
        '</svg>' % (hue, deep, motif))


# ---------------------------------------------------------------- artwork
def card(x, y, w, h, rot, cx, cy, inner=""):
    return ('<g transform="rotate(%s %s %s)">'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="18" '
            'fill="#FFFFFF" fill-opacity="0.12" stroke="#FFFFFF" '
            'stroke-opacity="0.28"/>%s</g>' % (rot, cx, cy, x, y, w, h, inner))


def bar(x, y, w, h=9, o=0.34, fill="#FFFFFF"):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'fill-opacity="%s"/>' % (x, y, w, h, h / 2.0, fill, o))


def body(sid, hue):
    if sid == "about":
        return (card(196, 96, 250, 228, -5, 321, 210,
                     '<circle cx="321" cy="164" r="34" fill="%s" '
                     'fill-opacity="0.55"/>' % hue
                     + bar(256, 218, 130) + bar(276, 240, 90, o=0.18)
                     + bar(244, 274, 68, 22, 0.20, hue)
                     + bar(322, 274, 78, 22, 0.14))
                + card(112, 150, 96, 132, -13, 160, 216,
                       bar(130, 178, 60) + bar(130, 198, 44, o=0.16)))
    if sid == "education":
        return (card(96, 118, 210, 184, -7, 201, 210,
                     bar(124, 210, 120) + bar(124, 232, 84, o=0.16)
                     + bar(124, 262, 62, 22, 0.22, hue))
                + card(334, 118, 210, 184, 7, 439, 210,
                       bar(362, 210, 120) + bar(362, 232, 84, o=0.16)
                       + bar(362, 262, 62, 22, 0.22, hue)))
    if sid == "skills":
        chips = ""
        for y, widths in ((128, [96, 74, 118]), (176, [86, 132, 68]),
                          (224, [110, 92, 100]), (272, [78, 124])):
            x = 320 - (sum(widths) + 14 * (len(widths) - 1)) / 2.0
            for i, w in enumerate(widths):
                hot = (y + i) % 3 == 0
                chips += bar(x, y, w, 32, 0.30 if hot else 0.14,
                             hue if hot else "#FFFFFF")
                x += w + 14
        return card(84, 96, 472, 232, 0, 320, 212, chips)
    if sid == "projects":
        def win(x, rot, cx):
            return card(x, 108, 168, 204, rot, cx, 210,
                        bar(x + 20, 128, 52, 8, 0.30, hue)
                        + '<rect x="%s" y="148" width="128" height="96" rx="10" '
                          'fill="#FFFFFF" fill-opacity="0.10"/>' % (x + 20)
                        + bar(x + 20, 258, 100) + bar(x + 20, 278, 70, o=0.16))
        return win(66, -9, 150) + win(236, 0, 320) + win(406, 9, 490)
    if sid == "work":
        rows = ""
        for i, y in enumerate((142, 202, 262)):
            rows += ('<circle cx="188" cy="%s" r="9" fill="%s" '
                     'fill-opacity="%s"/>' % (y + 6, hue, 0.85 if i == 0 else 0.35))
            rows += bar(214, y, 168 - i * 26) + bar(214, y + 22, 118 - i * 20, o=0.15)
        return card(148, 100, 344, 220, 0, 320, 210,
                    '<rect x="187" y="140" width="2" height="140" fill="#FFFFFF" '
                    'fill-opacity="0.18"/>' + rows)
    return (card(150, 92, 250, 146, -6, 275, 165,
                 bar(178, 128, 150) + bar(178, 150, 108, o=0.16)
                 + bar(178, 186, 84, 26, 0.24, hue))
            + card(268, 210, 224, 118, 6, 380, 269,
                   bar(296, 240, 130) + bar(296, 262, 92, o=0.16)
                   + '<circle cx="452" cy="296" r="14" fill="%s" '
                     'fill-opacity="0.6"/>' % hue))


def art_svg(sid, hue, deep):
    watermark = MOTIFS[sid].format(c1=hue, c2=hue, c3=hue)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 420" '
        'width="640" height="420">'
        '<defs><radialGradient id="g" cx="50%%" cy="46%%" r="70%%">'
        '<stop offset="0" stop-color="%s" stop-opacity="0.26"/>'
        '<stop offset="0.55" stop-color="%s" stop-opacity="0.10"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
        '</radialGradient></defs>'
        '<ellipse cx="320" cy="204" rx="318" ry="208" fill="url(#g)"/>'
        '<g transform="translate(320 208) scale(11.6) translate(-12 -12)" '
        'opacity="0.15">%s</g>%s</svg>'
        % (hue, deep, deep, watermark, body(sid, hue)))


for sid, hue, deep, c1, c2, c3 in SECTIONS:
    for name, svg in (("icon-%s.svg" % sid, icon_svg(sid, hue, deep, c1, c2, c3)),
                      ("peek-%s.svg" % sid, art_svg(sid, hue, deep))):
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(svg)
        print("wrote %s (%d bytes)" % (name, len(svg)))
