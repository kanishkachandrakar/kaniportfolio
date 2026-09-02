# -*- coding: utf-8 -*-
"""Generate the rail artwork: one SVG per section, sharing its colour and
glyph with the rail icon so the two read as the same object."""
import os

OUT = "/Users/kanishkachandrakar/Desktop/kaniportfolio/kaniportfolio-master/images"

# Glyphs are plain primitives (no icon-font paths), reused verbatim in the
# rail tile and as a watermark in the artwork.
GLYPHS = {
    "about": '<circle cx="12" cy="8.4" r="3.9"/>'
             '<path d="M4.6 20.2c0-4 3.3-6.4 7.4-6.4s7.4 2.4 7.4 6.4z"/>',
    "education": '<polygon points="12,3.6 22,8.6 12,13.6 2,8.6"/>'
                 '<path d="M6.2 11v4.9c0 1.8 2.6 3.2 5.8 3.2s5.8-1.4 5.8-3.2V11l-5.8 2.9z"/>',
    "skills": '<polygon points="12,3 21,7.4 12,11.8 3,7.4"/>'
              '<polygon points="12,13.4 19.2,9.9 21,10.8 12,15.2 3,10.8 4.8,9.9"/>'
              '<polygon points="12,16.8 19.2,13.3 21,14.2 12,18.6 3,14.2 4.8,13.3"/>',
    "projects": '<rect x="3" y="3" width="8" height="8" rx="2.4"/>'
                '<rect x="13" y="3" width="8" height="8" rx="2.4"/>'
                '<rect x="3" y="13" width="8" height="8" rx="2.4"/>'
                '<rect x="13" y="13" width="8" height="8" rx="2.4"/>',
    "work": '<rect x="2.6" y="7" width="18.8" height="12.6" rx="2.4"/>'
            '<path d="M9 6.2V5.4c0-.8.6-1.4 1.4-1.4h3.2c.8 0 1.4.6 1.4 1.4v.8h-1.9v-.4h-2.2v.4z"/>',
    "contact": '<polygon points="21.6,3 2.4,11.3 9.2,13.8 11.2,20.6 14.3,16.2 19.2,19.8"/>',
}

SECTIONS = [
    ("about",     "#E8B87C", "#B07C3E"),
    ("education", "#8FB8EA", "#4B6F9E"),
    ("skills",    "#93D3AC", "#4C8A67"),
    ("projects",  "#C2A2EA", "#7355A0"),
    ("work",      "#EBA277", "#A55F36"),
    ("contact",   "#E895AC", "#A0546B"),
]


def card(x, y, w, h, rot, cx, cy, inner=""):
    return (
        '<g transform="rotate(%s %s %s)">'
        '<rect x="%s" y="%s" width="%s" height="%s" rx="18" '
        'fill="#FFFFFF" fill-opacity="0.12" stroke="#FFFFFF" '
        'stroke-opacity="0.28"/>%s</g>' % (rot, cx, cy, x, y, w, h, inner))


def bar(x, y, w, h=9, o=0.34, fill="#FFFFFF"):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'fill-opacity="%s"/>' % (x, y, w, h, h / 2.0, fill, o))


def body(sid, hue):
    """Wireframe content per section, in the section's own colour."""
    if sid == "about":
        return (
            card(196, 96, 250, 228, -5, 321, 210,
                 '<circle cx="321" cy="164" r="34" fill="%s" fill-opacity="0.55"/>'
                 % hue
                 + bar(256, 218, 130) + bar(276, 240, 90, o=0.18)
                 + bar(244, 274, 68, 22, 0.20, hue)
                 + bar(322, 274, 78, 22, 0.14))
            + card(112, 150, 96, 132, -13, 160, 216, bar(130, 178, 60) + bar(130, 198, 44, o=0.16)))
    if sid == "education":
        return (
            card(96, 118, 210, 184, -7, 201, 210,
                 bar(124, 210, 120) + bar(124, 232, 84, o=0.16)
                 + bar(124, 262, 62, 22, 0.22, hue))
            + card(334, 118, 210, 184, 7, 439, 210,
                   bar(362, 210, 120) + bar(362, 232, 84, o=0.16)
                   + bar(362, 262, 62, 22, 0.22, hue)))
    if sid == "skills":
        chips = ""
        rows = [(128, [96, 74, 118]), (176, [86, 132, 68]),
                (224, [110, 92, 100]), (272, [78, 124])]
        for y, widths in rows:
            x = 320 - (sum(widths) + 14 * (len(widths) - 1)) / 2.0
            for i, w in enumerate(widths):
                o = 0.30 if (y + i) % 3 == 0 else 0.14
                f = hue if (y + i) % 3 == 0 else "#FFFFFF"
                chips += bar(x, y, w, 32, o, f)
                x += w + 14
        return card(84, 96, 472, 232, 0, 320, 212, chips)
    if sid == "projects":
        def win(x, rot, cx):
            return card(x, 108, 168, 204, rot, cx, 210,
                        bar(x + 20, 128, 52, 8, 0.30, hue)
                        + '<rect x="%s" y="%s" width="128" height="96" rx="10" '
                          'fill="#FFFFFF" fill-opacity="0.10"/>' % (x + 20, 148)
                        + bar(x + 20, 258, 100) + bar(x + 20, 278, 70, o=0.16))
        return win(66, -9, 150) + win(236, 0, 320) + win(406, 9, 490)
    if sid == "work":
        rows = ""
        for i, y in enumerate((142, 202, 262)):
            rows += ('<circle cx="188" cy="%s" r="9" fill="%s" fill-opacity="%s"/>'
                     % (y + 6, hue, 0.85 if i == 0 else 0.35))
            rows += bar(214, y, 168 - i * 26) + bar(214, y + 22, 118 - i * 20, o=0.15)
        return (card(148, 100, 344, 220, 0, 320, 210,
                     '<rect x="187" y="140" width="2" height="140" fill="#FFFFFF" '
                     'fill-opacity="0.18"/>' + rows))
    # contact
    return (
        card(150, 92, 250, 146, -6, 275, 165,
             bar(178, 128, 150) + bar(178, 150, 108, o=0.16)
             + bar(178, 186, 84, 26, 0.24, hue))
        + card(268, 210, 224, 118, 6, 380, 269,
               bar(296, 240, 130) + bar(296, 262, 92, o=0.16)
               + '<circle cx="452" cy="296" r="14" fill="%s" fill-opacity="0.6"/>' % hue))


for sid, hue, deep in SECTIONS:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 420" '
        'width="640" height="420">'
        '<defs><radialGradient id="g" cx="50%%" cy="46%%" r="70%%">'
        '<stop offset="0" stop-color="%s" stop-opacity="0.26"/>'
        '<stop offset="0.55" stop-color="%s" stop-opacity="0.10"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
        '</radialGradient></defs>'
        '<ellipse cx="320" cy="204" rx="318" ry="208" fill="url(#g)"/>'
        # The same glyph as the rail icon, sitting behind the cards.
        '<g transform="translate(320 208) scale(11.6) translate(-12 -12)" '
        'fill="%s" fill-opacity="0.15">%s</g>'
        '%s</svg>'
        % (hue, deep, deep, hue, GLYPHS[sid], body(sid, hue)))
    path = os.path.join(OUT, "peek-%s.svg" % sid)
    with open(path, "w") as fh:
        fh.write(svg)
    print("wrote %s (%d bytes)" % (os.path.basename(path), len(svg)))
