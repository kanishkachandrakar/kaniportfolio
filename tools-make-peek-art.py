# -*- coding: utf-8 -*-
"""Draw everything the rail needs: one app-icon tile and one product mockup
per section. All generated - no photographs.
Run: python3 tools-make-peek-art.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

GLASS = "#211D1A"
W = "#FFFFFF"


def bar(x, y, w, h=6, o=0.30, fill=W):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'fill-opacity="%s"/>' % (x, y, w, h, h / 2.0, fill, o))


def box(x, y, w, h, r, fill, o=1.0):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'fill-opacity="%s"/>' % (x, y, w, h, r, fill, o))


def dot(cx, cy, r, fill, o=1.0):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s"/>'
            % (cx, cy, r, fill, o))


def screen(x, y, w, h, rot, inner):
    """A device-ish window: frame, title bar with dots, then its content."""
    cx, cy = x + w / 2.0, y + h / 2.0
    return ('<g transform="rotate(%s %s %s)" filter="url(#d)">'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="16" fill="%s" '
            'stroke="%s" stroke-opacity="0.18"/>'
            '%s%s%s'
            '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
            'stroke-opacity="0.12"/>'
            '%s</g>'
            % (rot, cx, cy, x, y, w, h, GLASS, W,
               dot(x + 15, y + 15, 3, W, 0.30),
               dot(x + 25, y + 15, 3, W, 0.18),
               dot(x + 35, y + 15, 3, W, 0.18),
               x, y + 30, x + w, y + 30, W,
               inner))


def tag(x, y, w, hue, label_w):
    """A small floating chip, like the file tags on the reference site."""
    return ('<g transform="rotate(9 %s %s)" filter="url(#d)">'
            '<rect x="%s" y="%s" width="%s" height="34" rx="10" fill="#F7F3EC"/>'
            '%s%s</g>'
            % (x + w / 2.0, y + 17, x, y, w,
               box(x + 10, y + 10, 14, 14, 4, hue, 0.9),
               bar(x + 30, y + 14, w - 42, 6, 0.55, "#2A2521")))


# --------------------------------------------------------------- content
# Each content function takes its screen's origin so the content follows
# the frame it belongs to rather than sitting at fixed coordinates.
def c_about(x, y, w, hue):
    return (dot(x + 40, y + 62, 17, hue, 0.9)
            + bar(x + 64, y + 54, w - 92, 7, 0.38)
            + bar(x + 64, y + 68, w - 118, 5, 0.16)
            + box(x + 16, y + 92, w - 32, 30, 8, W, 0.07)
            + bar(x + 28, y + 103, w - 76, 6, 0.22)
            + box(x + 16, y + 132, (w - 40) / 2.0, 22, 7, hue, 0.34)
            + box(x + 24 + (w - 40) / 2.0, y + 132, (w - 40) / 2.0, 22, 7, W, 0.10))


def c_rows(x, y, w, hue):
    out = ""
    for i in range(4):
        yy = y + 46 + i * 27
        out += dot(x + 22, yy + 7, 6, hue if i == 0 else W, 1 if i == 0 else 0.20)
        out += bar(x + 36, yy + 1, w - 60 - i * 8, 6, 0.30)
        out += bar(x + 36, yy + 12, w - 96, 5, 0.14)
    return out


def c_chips(x, y, w, hue):
    out = bar(x + 16, y + 46, 52, 7, 0.34)
    rows = [(0, 42), (48, 34), (88, 46), (0, 36), (42, 52), (100, 34),
            (0, 48), (54, 38), (98, 40)]
    for i, (dx, cw) in enumerate(rows):
        r = i // 3
        out += box(x + 16 + dx, y + 66 + r * 26, cw, 19, 6,
                   hue if i % 3 == 0 else W, 0.34 if i % 3 == 0 else 0.11)
    return out


def c_chart(x, y, w, hue):
    out = bar(x + 16, y + 46, 46, 7, 0.34)
    for i, h in enumerate((22, 40, 30, 52, 44, 62)):
        out += box(x + 18 + i * 19, y + 132 - h, 12, h, 4, hue,
                   0.85 if i in (3, 5) else 0.34)
    return out + bar(x + 16, y + 142, w - 40, 5, 0.12)


def c_app(x, y, w, hue, accent):
    return (box(x + 14, y + 42, w - 28, 58, 12, accent, 0.55)
            + bar(x + 14, y + 110, w - 46, 7, 0.30)
            + bar(x + 14, y + 124, w - 72, 6, 0.14)
            + box(x + 14, y + 144, w - 28, 22, 8, accent, 0.34))


def c_compose(x, y, w, hue):
    return (bar(x + 16, y + 46, 62, 7, 0.34)
            + box(x + 16, y + 62, w - 32, 26, 8, W, 0.07)
            + box(x + 16, y + 96, w - 32, 26, 8, W, 0.07)
            + box(x + 16, y + 132, 62, 24, 9, hue, 0.6)
            + bar(x + 28, y + 141, 38, 6, 0.55, "#2A2521"))


def c_badge(x, y, w, hue):
    cx = x + w / 2.0
    return ('<polygon points="%s,%s %s,%s %s,%s %s,%s" fill="%s" '
            'fill-opacity="0.85"/>'
            % (cx, y + 50, cx + 46, y + 71, cx, y + 92, cx - 46, y + 71, hue)
            + bar(x + 18, y + 110, w - 36, 7, 0.30)
            + bar(x + 30, y + 126, w - 60, 6, 0.14)
            + box(x + 18, y + 146, w - 36, 22, 7, W, 0.10))


# Screens are spaced apart rather than stacked, so each reads on its own.
def art_about(hue):
    return (screen(14, 54, 160, 178, -7, c_about(14, 54, 160, hue))
            + screen(210, 34, 176, 196, 6, c_rows(210, 34, 176, hue))
            + tag(238, 4, 116, hue, 0))


def art_education(hue):
    return (screen(14, 44, 150, 190, -8, c_badge(14, 44, 150, hue))
            + screen(200, 38, 186, 196, 5, c_rows(200, 38, 186, hue))
            + tag(230, 6, 112, hue, 0))


def art_craft(hue):
    return (screen(10, 48, 158, 180, -8, c_chart(10, 48, 158, hue))
            + screen(202, 30, 182, 206, 6, c_chips(202, 30, 182, hue))
            + tag(232, 2, 118, hue, 0))


def art_projects(hue):
    return (screen(6, 56, 122, 182, -10, c_app(6, 56, 122, hue, "#7EC4F0"))
            + screen(148, 34, 126, 206, 0, c_app(148, 34, 126, hue, hue))
            + screen(292, 54, 118, 180, 9, c_app(292, 54, 118, hue, "#F0A9C0"))
            + tag(282, 2, 104, hue, 0))


def art_contact(hue):
    return (screen(12, 52, 152, 180, -7, c_rows(12, 52, 152, hue))
            + screen(198, 36, 180, 198, 6, c_compose(198, 36, 180, hue))
            + tag(228, 4, 112, hue, 0))


ART = {"about": art_about, "education": art_education, "craft": art_craft,
       "projects": art_projects, "contact": art_contact}

ICONS = {
    "about":
        '<circle cx="24" cy="19" r="7.6" fill="#FFFFFF"/>'
        '<path d="M9.6 39.4c0-7.8 6.4-12.4 14.4-12.4s14.4 4.6 14.4 12.4z" '
        'fill="#FFFFFF" fill-opacity="0.88"/>',
    "education":
        '<polygon points="24,9 42,18 24,27 6,18" fill="#FFFFFF"/>'
        '<path d="M13.5 22.5v9.6c0 3.5 4.7 6.1 10.5 6.1s10.5-2.6 10.5-6.1v-9.6'
        'L24 27.6z" fill="#FFFFFF" fill-opacity="0.72"/>'
        '<path d="M40.4 19.2v10.6" stroke="#FFFFFF" stroke-width="2.4" '
        'stroke-linecap="round" fill="none"/>'
        '<circle cx="40.4" cy="31.8" r="2.7" fill="#FFFFFF"/>',
    "craft":
        '<polygon points="24,7 41,15.8 24,24.6 7,15.8" fill="#FFFFFF"/>'
        '<polygon points="24,27.6 38.4,20.4 41,21.8 24,30.6 7,21.8 9.6,20.4" '
        'fill="#FFFFFF" fill-opacity="0.72"/>'
        '<polygon points="24,34.4 38.4,27.2 41,28.6 24,37.4 7,28.6 9.6,27.2" '
        'fill="#FFFFFF" fill-opacity="0.48"/>',
    "projects":
        '<rect x="7" y="7" width="15.6" height="15.6" rx="4.6" fill="#FFFFFF"/>'
        '<rect x="25.4" y="7" width="15.6" height="15.6" rx="4.6" fill="#FFFFFF" '
        'fill-opacity="0.62"/>'
        '<rect x="7" y="25.4" width="15.6" height="15.6" rx="4.6" fill="#FFFFFF" '
        'fill-opacity="0.62"/>'
        '<rect x="25.4" y="25.4" width="15.6" height="15.6" rx="4.6" fill="#FFFFFF"/>',
    "contact":
        '<path d="M42 7 6 22.4l13.4 4.8 4.4 13.8z" fill="#FFFFFF"/>'
        '<path d="M19.4 27.2 42 7l-18 33.6-4.6-13.8z" fill="#FFFFFF" '
        'fill-opacity="0.7"/>',
}

SECTIONS = [
    ("about",     "#E8B87C", "#96602A"),
    ("education", "#8FB8EA", "#3F5F8E"),
    ("craft",     "#93D3AC", "#3F7A5B"),
    ("projects",  "#C2A2EA", "#63479A"),
    ("contact",   "#E895AC", "#93475E"),
]

SHADOW = ('<filter id="d" x="-30%" y="-30%" width="170%" height="170%">'
          '<feDropShadow dx="0" dy="10" stdDeviation="13" flood-color="#000000" '
          'flood-opacity="0.6"/></filter>')

for sid, hue, deep in SECTIONS:
    art = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 430 250" '
           'width="430" height="250"><defs>%s'
           '<radialGradient id="g" cx="50%%" cy="50%%" r="62%%">'
           '<stop offset="0" stop-color="%s" stop-opacity="0.24"/>'
           '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
           '</radialGradient></defs>'
           '<ellipse cx="215" cy="130" rx="214" ry="124" fill="url(#g)"/>'
           '%s</svg>' % (SHADOW, hue, deep, ART[sid](hue)))
    icon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" '
            'width="48" height="48">'
            '<defs><linearGradient id="b" x1="0.1" y1="0" x2="0.75" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
            '</linearGradient>'
            '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.40"/>'
            '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>'
            '</linearGradient></defs>'
            '<rect width="48" height="48" rx="13.5" fill="url(#b)"/>'
            '<path d="M0 13.5A13.5 13.5 0 0 1 13.5 0h21A13.5 13.5 0 0 1 48 13.5V22'
            'C36 28 12 28 0 22z" fill="url(#s)"/>'
            '<g transform="translate(24 24) scale(0.8) translate(-24 -24)">%s</g>'
            '<rect x="0.7" y="0.7" width="46.6" height="46.6" rx="12.9" fill="none" '
            'stroke="#FFFFFF" stroke-opacity="0.32"/></svg>'
            % (hue, deep, ICONS[sid]))
    for name, data in (("peek-%s.svg" % sid, art), ("icon-%s.svg" % sid, icon)):
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(data)
        print("wrote %s (%d bytes)" % (name, len(data)))
