# -*- coding: utf-8 -*-
"""Draw the rail icons and the mockup each one emerges into.

The artwork is frameless and transparent so it can sit underneath its icon
and read as one object, the way the reference site does it.
Run: python3 tools-make-peek-art.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

PANEL = "#211D1A"
LINE = "#FFFFFF"


def sh(o=0.18):
    return ('<filter id="d" x="-30%" y="-30%" width="170%" height="170%">'
            '<feDropShadow dx="0" dy="10" stdDeviation="14" '
            'flood-color="#000000" flood-opacity="0.55"/></filter>')


def panel(x, y, w, h, rot, cx, cy, inner="", fill=PANEL):
    return ('<g transform="rotate(%s %s %s)" filter="url(#d)">'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="15" fill="%s" '
            'stroke="%s" stroke-opacity="0.16"/>%s</g>'
            % (rot, cx, cy, x, y, w, h, fill, LINE, inner))


def bar(x, y, w, h=7, o=0.30, fill=LINE):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'fill-opacity="%s"/>' % (x, y, w, h, h / 2.0, fill, o))


def dot(cx, cy, r, fill, o=1):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s"/>'
            % (cx, cy, r, fill, o))


def chip(x, y, w, h, fill, o=0.9, r=6):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'fill-opacity="%s"/>' % (x, y, w, h, r, fill, o))


def sticker(x, y, w, h, rot, hue, inner=""):
    """A small floating tag, like the file chips on the reference site."""
    return ('<g transform="rotate(%s %s %s)" filter="url(#d)">'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="9" fill="#F6F2EA"/>'
            '<rect x="%s" y="%s" width="%s" height="4" rx="2" fill="%s"/>%s</g>'
            % (rot, x + w / 2, y + h / 2, x, y, w, h,
               x + 9, y + h - 11, w - 18, hue, inner))


def rows(x, y, n, w, step=22, hue=None, avatar=True):
    out = ""
    for i in range(n):
        yy = y + i * step
        if avatar:
            out += dot(x + 9, yy + 8, 8, hue if i == 0 else LINE,
                       1 if i == 0 else 0.22)
            out += bar(x + 24, yy + 2, w, 6, 0.34) + bar(x + 24, yy + 12, w * 0.6, 5, 0.16)
        else:
            out += bar(x, yy + 2, w, 6, 0.30) + bar(x, yy + 12, w * 0.62, 5, 0.15)
    return out


def art_about(hue):
    main = panel(150, 46, 208, 214, 6, 254, 153,
                 dot(254, 104, 30, hue, 0.85)
                 + bar(206, 148, 96, 9, 0.42) + bar(224, 166, 60, 7, 0.20)
                 + chip(188, 190, 62, 20, hue, 0.30) + chip(258, 190, 58, 20, LINE, 0.12)
                 + bar(186, 224, 136, 6, 0.18))
    side = panel(38, 96, 132, 152, -9, 104, 172,
                 rows(52, 118, 4, 74, 30, hue))
    tag = sticker(268, 20, 96, 34, 9, hue,
                  bar(277, 30, 62, 6, 0.55, "#2B2622"))
    return side + main + tag


def art_education(hue):
    main = panel(126, 40, 232, 206, -5, 242, 143,
                 bar(150, 64, 108, 9, 0.42) + bar(150, 82, 66, 6, 0.18)
                 + rows(150, 108, 4, 148, 30, hue, avatar=False)
                 + chip(150, 214, 74, 20, hue, 0.32))
    badge = panel(38, 130, 118, 118, 8, 97, 189,
                  '<polygon points="97,158 141,178 97,198 53,178" fill="%s" '
                  'fill-opacity="0.9"/>' % hue
                  + bar(70, 214, 54, 7, 0.30))
    tag = sticker(272, 18, 88, 34, -8, hue, bar(281, 28, 54, 6, 0.55, "#2B2622"))
    return badge + main + tag


def art_skills(hue):
    grid = ""
    ws = [(0, 46), (54, 62), (124, 40), (0, 58), (66, 44), (118, 46),
          (0, 40), (48, 66), (122, 42)]
    for i, (dx, w) in enumerate(ws):
        r = i // 3
        grid += chip(152 + dx, 92 + r * 30, w, 21,
                     hue if i % 4 == 0 else LINE, 0.34 if i % 4 == 0 else 0.13)
    main = panel(130, 44, 216, 196, 5, 238, 142,
                 bar(152, 64, 96, 9, 0.42) + grid)
    side = panel(30, 118, 122, 128, -10, 91, 182,
                 bar(46, 140, 62, 7, 0.34)
                 + chip(46, 158, 88, 18, hue, 0.30)
                 + chip(46, 182, 66, 18, LINE, 0.13)
                 + chip(46, 206, 78, 18, LINE, 0.13))
    tag = sticker(268, 20, 92, 34, 10, hue, bar(277, 30, 58, 6, 0.55, "#2B2622"))
    return side + main + tag


def art_projects(hue):
    def phone(x, y, rot, cx, cy, accent):
        return panel(x, y, 92, 176, rot, cx, cy,
                     bar(x + 14, y + 18, 44, 6, 0.34)
                     + chip(x + 14, y + 34, 64, 46, accent, 0.55, 10)
                     + bar(x + 14, y + 90, 64, 6, 0.22)
                     + bar(x + 14, y + 104, 48, 6, 0.14)
                     + chip(x + 14, y + 126, 64, 18, accent, 0.34))
    return (phone(40, 74, -10, 86, 162, "#7EC4F0")
            + phone(140, 50, -3, 186, 138, hue)
            + phone(242, 66, 7, 288, 154, "#F0A9C0")
            + sticker(286, 14, 90, 34, 12, hue,
                      bar(295, 24, 56, 6, 0.55, "#2B2622")))


def art_work(hue):
    tl = ""
    for i, yy in enumerate((104, 146, 188)):
        tl += dot(170, yy + 6, 7, hue, 1 if i == 0 else 0.35)
        tl += bar(188, yy, 118 - i * 18, 7, 0.34) + bar(188, yy + 14, 84 - i * 12, 6, 0.15)
    main = panel(146, 44, 210, 196, -4, 251, 142,
                 bar(170, 66, 92, 9, 0.42)
                 + '<rect x="169" y="100" width="2" height="98" fill="#FFFFFF" '
                   'fill-opacity="0.16"/>' + tl)
    side = panel(34, 112, 126, 134, 9, 97, 179,
                 dot(66, 144, 16, hue, 0.9)
                 + bar(50, 172, 74, 7, 0.32) + bar(50, 188, 52, 6, 0.16)
                 + chip(50, 208, 60, 18, hue, 0.28))
    tag = sticker(276, 16, 86, 34, -9, hue, bar(285, 26, 52, 6, 0.55, "#2B2622"))
    return side + main + tag


def art_contact(hue):
    main = panel(132, 52, 226, 172, 5, 245, 138,
                 bar(156, 76, 88, 9, 0.42)
                 + chip(156, 96, 178, 30, LINE, 0.09, 10)
                 + chip(156, 134, 178, 30, LINE, 0.09, 10)
                 + chip(156, 176, 82, 26, hue, 0.55, 13)
                 + bar(172, 187, 50, 5, 0.6, "#2B2622"))
    side = panel(32, 108, 118, 122, -10, 91, 169,
                 rows(46, 128, 3, 58, 30, hue))
    tag = sticker(274, 18, 92, 34, 10, hue, bar(283, 28, 58, 6, 0.55, "#2B2622"))
    return side + main + tag


ART = {"about": art_about, "education": art_education, "skills": art_skills,
       "projects": art_projects, "work": art_work, "contact": art_contact}

ICONS = {
    "about": None,   # uses the real headshot
    "education":
        '<polygon points="24,9 42,18 24,27 6,18" fill="#FFFFFF"/>'
        '<path d="M13.5 22.5v9.6c0 3.5 4.7 6.1 10.5 6.1s10.5-2.6 10.5-6.1v-9.6'
        'L24 27.6z" fill="#DCE7F8"/>'
        '<path d="M40.4 19.2v10.6" stroke="#FFFFFF" stroke-width="2.4" '
        'stroke-linecap="round" fill="none"/>'
        '<circle cx="40.4" cy="31.8" r="2.7" fill="#FFFFFF"/>',
    "skills":
        '<polygon points="24,8 41,16.8 24,25.6 7,16.8" fill="#FFFFFF"/>'
        '<polygon points="24,28.6 38.4,21.4 41,22.8 24,31.6 7,22.8 9.6,21.4" '
        'fill="#E4F7EC"/>'
        '<polygon points="24,35.4 38.4,28.2 41,29.6 24,38.4 7,29.6 9.6,28.2" '
        'fill="#BFE9D2"/>',
    "projects":
        '<rect x="7" y="7" width="15.6" height="15.6" rx="4.6" fill="#FFFFFF"/>'
        '<rect x="25.4" y="7" width="15.6" height="15.6" rx="4.6" fill="#EFE1FF"/>'
        '<rect x="7" y="25.4" width="15.6" height="15.6" rx="4.6" fill="#EFE1FF"/>'
        '<rect x="25.4" y="25.4" width="15.6" height="15.6" rx="4.6" fill="#FFFFFF"/>',
    "work":
        '<rect x="6.4" y="14.6" width="35.2" height="24" rx="4.6" fill="#FFFFFF"/>'
        '<path d="M17.6 13.2v-1.6a3.4 3.4 0 0 1 3.4-3.4h6a3.4 3.4 0 0 1 3.4 3.4'
        'v1.6h-4.2v-.8h-4.4v.8z" fill="#FFFFFF"/>'
        '<rect x="6.4" y="23.4" width="35.2" height="3.4" fill="#F6D4BC"/>'
        '<rect x="20.6" y="21.4" width="6.8" height="7.4" rx="2" fill="#F6D4BC"/>',
    "contact":
        '<path d="M42 7 6 22.4l13.4 4.8 4.4 13.8z" fill="#FFFFFF"/>'
        '<path d="M19.4 27.2 42 7l-18 33.6-4.6-13.8z" fill="#FBDCE4"/>',
}

SECTIONS = [
    ("about",     "#E8B87C", "#96602A"),
    ("education", "#8FB8EA", "#3F5F8E"),
    ("skills",    "#93D3AC", "#3F7A5B"),
    ("projects",  "#C2A2EA", "#63479A"),
    ("work",      "#EBA277", "#96522C"),
    ("contact",   "#E895AC", "#93475E"),
]

for sid, hue, deep in SECTIONS:
    scene = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 290" '
             'width="400" height="290"><defs>%s'
             '<radialGradient id="g" cx="52%%" cy="48%%" r="62%%">'
             '<stop offset="0" stop-color="%s" stop-opacity="0.22"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
             '</radialGradient></defs>'
             '<ellipse cx="205" cy="145" rx="198" ry="142" fill="url(#g)"/>'
             '%s</svg>' % (sh(), hue, deep, ART[sid](hue)))
    name = "peek-%s.svg" % sid
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(scene)
    print("wrote %s (%d bytes)" % (name, len(scene)))

    if ICONS[sid] is None:
        continue
    icon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" '
            'width="48" height="48">'
            '<defs><linearGradient id="b" x1="0.1" y1="0" x2="0.75" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
            '</linearGradient>'
            '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.38"/>'
            '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>'
            '</linearGradient></defs>'
            '<rect width="48" height="48" rx="13.5" fill="url(#b)"/>'
            '<path d="M0 13.5A13.5 13.5 0 0 1 13.5 0h21A13.5 13.5 0 0 1 48 13.5V22'
            'C36 28 12 28 0 22z" fill="url(#s)"/>'
            '<g transform="translate(24 24) scale(0.82) translate(-24 -24)">%s</g>'
            '<rect x="0.7" y="0.7" width="46.6" height="46.6" rx="12.9" fill="none" '
            'stroke="#FFFFFF" stroke-opacity="0.30"/></svg>'
            % (hue, deep, ICONS[sid]))
    name = "icon-%s.svg" % sid
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(icon)
    print("wrote %s (%d bytes)" % (name, len(icon)))
