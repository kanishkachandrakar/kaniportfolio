# -*- coding: utf-8 -*-
"""Draw the rail icons and the illustration each one opens.

Every asset is generated - flat cut-out illustrations with a white sticker
outline, plus badges carrying real phrases.
Run: python3 tools-make-peek-art.py
"""
import base64
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

SMALL = ("/private/tmp/claude-501/-Users-kanishkachandrakar-Desktop-"
         "kaniportfolio-kaniportfolio-master/"
         "1265d3b4-3f1f-4a0b-a512-4ded02a83abe/scratchpad/small")


def photo(name):
    """A real photo, inlined so the SVG stays self-contained."""
    with open(os.path.join(SMALL, name), "rb") as fh:
        return "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode()


CUT_FILTER = (
    '<filter id="cut" x="-30%" y="-30%" width="160%" height="160%">'
    '<feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000000" '
    'flood-opacity="0.55"/></filter>')


def photo_webp(name):
    with open(os.path.join(SMALL, name), "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()


def img(href, x, y, w, h, clip):
    return ('<image href="%s" x="%s" y="%s" width="%s" height="%s" '
            'preserveAspectRatio="xMidYMid slice" clip-path="url(#%s)"/>'
            % (href, x, y, w, h, clip))


FONT = "Helvetica Neue,Helvetica,Arial,sans-serif"
INK = "#2A2521"
SKIN = "#EFC49C"
HAIR = "#241A15"
NAVY = "#2B3A58"
CUT = "#FFFFFF"          # the sticker cut-out edge


def o(fill, sw=7):
    return ('fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" '
            'stroke-linecap="round"' % (fill, CUT, sw))


def path(d, fill, sw=7):
    return '<path d="%s" %s/>' % (d, o(fill, sw))


def rect(x, y, w, h, r, fill, sw=7):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" %s/>'
            % (x, y, w, h, r, o(fill, sw)))


def circ(cx, cy, r, fill, sw=7):
    return '<circle cx="%s" cy="%s" r="%s" %s/>' % (cx, cy, r, o(fill, sw))


def plain(shape):
    return shape


def sticker(x, y, text, fill, fg, rot, fs=13):
    glyphs = len(re.sub(r"&[a-zA-Z0-9#]+;", "x", text))
    w = glyphs * fs * 0.60 + 26
    h = fs + 17
    cx, cy = x + w / 2.0, y + h / 2.0
    return ('<g transform="rotate(%s %s %s)" filter="url(#d)">'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#FFFFFF"/>'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>'
            '<text x="%s" y="%s" text-anchor="middle" font-family="%s" '
            'font-size="%s" font-weight="700" fill="%s">%s</text></g>'
            % (rot, cx, cy, x - 3.5, y - 3.5, w + 7, h + 7, (h + 7) / 2.0,
               x, y, w, h, h / 2.0, fill,
               cx, y + h - (h - fs) / 2.0 - 1, FONT, fs, fg, text))


def smiley(cx, cy, r):
    return ('<g filter="url(#d)"><circle cx="%s" cy="%s" r="%s" fill="#FFFFFF"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="#FFD452"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="%s"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="%s"/>'
            '<path d="M%s %sq%s %s %s 0" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-linecap="round"/></g>'
            % (cx, cy, r + 3.5, cx, cy, r,
               cx - r * 0.34, cy - r * 0.16, r * 0.13, INK,
               cx + r * 0.34, cy - r * 0.16, r * 0.13, INK,
               cx - r * 0.42, cy + r * 0.24, r * 0.42, r * 0.42, r * 0.84,
               INK, r * 0.15))


# ------------------------------------------------------------ illustrations
def figure(x, y, s=1.0, rot=0):
    """The headshot with its background actually removed, given a white
    sticker edge by dilating its own alpha - so the outline follows her,
    not a generic silhouette."""
    body = ('<image href="%s" x="0" y="0" width="256" height="300" '
            'filter="url(#cut)"/>' % photo_webp("cut.webp"))
    return ('<g transform="translate(%s %s) scale(%s) rotate(%s 128 150)">'
            '%s</g>' % (x, y, s, rot, body))


def cap(x, y, s=1.0, rot=0, hue="#8FB8EA"):
    body = (path("M84 8 164 44 84 80 4 44z", hue)
            + path("M30 56v34c0 15 24 26 54 26s54-11 54-26V56L84 80z", "#F2F5FA")
            + '<path d="M152 50v42" stroke="%s" stroke-width="7" fill="none" '
              'stroke-linecap="round"/>' % CUT
            + '<path d="M152 50v42" stroke="%s" stroke-width="3.5" fill="none" '
              'stroke-linecap="round"/>' % INK
            + circ(152, 100, 10, "#FFD452", 5))
    return ('<g transform="translate(%s %s) scale(%s) rotate(%s 84 60)" '
            'filter="url(#d)">%s</g>' % (x, y, s, rot, body))


def books(x, y, s=1.0, rot=0):
    body = (rect(0, 56, 140, 26, 7, "#E5798A", 5)
            + rect(8, 30, 132, 26, 7, "#7FB6E8", 5)
            + rect(0, 4, 128, 26, 7, "#FBD489", 5))
    return ('<g transform="translate(%s %s) scale(%s) rotate(%s 70 44)" '
            'filter="url(#d)">%s</g>' % (x, y, s, rot, body))


def scroll(x, y, s=1.0, rot=0, hue="#8FB8EA"):
    body = (rect(0, 0, 68, 92, 8, "#F7F3EC", 5)
            + '<path d="M14 22h40M14 40h40M14 58h26" stroke="%s" '
              'stroke-width="4" stroke-linecap="round"/>' % INK
            + rect(-8, 34, 84, 18, 9, hue, 5))
    return ('<g transform="translate(%s %s) scale(%s) rotate(%s 34 46)" '
            'filter="url(#d)">%s</g>' % (x, y, s, rot, body))


def laptop(x, y, s=1.0, rot=0, hue="#93D3AC"):
    body = (rect(14, 12, 172, 116, 12, "#F7F3EC", 6)
            + '<clipPath id="lap"><rect x="26" y="24" width="148" height="92" '
              'rx="7"/></clipPath>'
            + '<rect x="26" y="24" width="148" height="92" rx="7" fill="#1C1A18"/>'
            + img(photo("lap.jpg"), 26, 24, 148, 92, "lap")
            + path("M0 128h200l16 26H-16z", "#DCE3E8", 6))
    return ('<g transform="translate(%s %s) scale(%s) rotate(%s 100 84)" '
            'filter="url(#d)">%s</g>' % (x, y, s, rot, body))


def phone(x, y, s, rot, screen):
    body = rect(0, 0, 104, 190, 20, "#F7F3EC", 6) + screen
    return ('<g transform="translate(%s %s) scale(%s) rotate(%s 52 95)" '
            'filter="url(#d)">%s</g>' % (x, y, s, rot, body))


def shot(name, cid):
    """A real screenshot filling a phone's screen."""
    return ('<clipPath id="%s"><rect x="10" y="34" width="84" height="140" '
            'rx="10"/></clipPath>' % cid
            + '<rect x="10" y="34" width="84" height="140" rx="10" '
              'fill="#1C1A18"/>'
            + img(photo(name), 10, 34, 84, 140, cid))


def bubble(x, y, w, h, fill, right=False, sw=6):
    tail = ("M%s %sq14 4 20 12-16 0-24-8z" % (x + w - 12, y + h - 18)
            if right else "M%s %sq-14 4-20 12 16 0 24-8z" % (x + 12, y + h - 18))
    return (rect(x, y, w, h, h / 2.0, fill, sw) + path(tail, fill, sw))


def imessage(x, y, s=1.0):
    body = (bubble(0, 0, 150, 46, "#E9E4DE")
            + bubble(58, 62, 158, 48, "#2C8BF0", True)
            + bubble(0, 126, 116, 44, "#E9E4DE")
            + ''.join('<circle cx="%s" cy="148" r="6.5" fill="#8A8078"/>' % cx
                      for cx in (36, 58, 80)))
    return ('<g transform="translate(%s %s) scale(%s)" filter="url(#d)">%s</g>'
            % (x, y, s, body))


# ------------------------------------------------------------------ scenes
def art_about(hue):
    return (figure(110, 26, 0.84, -3)
            + sticker(14, 34, "MS @ NYU &#8217;27", hue, INK, -9)
            + sticker(26, 132, "git push", "#FFFFFF", INK, 8, 12)
            + sticker(66, 214, "&lt;/&gt;", "#2F6BE0", "#FFFFFF", -7, 13)
            + sticker(296, 120, "Python", "#FFFFFF", INK, -8, 12)
            + sticker(256, 206, "Ships clean code", "#FFFFFF", INK, 7, 12)
            + smiley(322, 52, 18))


def art_education(hue):
    disc = ('<clipPath id="edu"><circle cx="238" cy="152" r="104"/></clipPath>'
            '<g filter="url(#d)"><circle cx="238" cy="152" r="104" fill="#1C1A18"/>'
            '<image href="%s" x="134" y="48" width="208" height="208" '
            'preserveAspectRatio="xMidYMid slice" clip-path="url(#edu)"/></g>'
            % photo_webp("grad.webp"))
    return (disc + books(6, 208, 0.72, -6)
            + cap(150, 8, 0.62, -10, hue)
            + sticker(8, 66, "Dean&#8217;s List", hue, INK, -10)
            + sticker(160, 250, "Penn State", "#FFFFFF", INK, 6, 12)
            + sticker(322, 62, "AI / ML", "#FFFFFF", INK, 9, 12)
            + sticker(2, 160, "O(n log n)", "#FFFFFF", INK, 7, 12)
            + sticker(318, 128, "CS &#8226; NYU", hue, INK, -8, 12))


def art_craft(hue):
    return (laptop(66, 54, 1.0, -5, hue)
            + sticker(24, 46, "PyTorch", hue, INK, -10)
            + sticker(232, 208, "30+ reviews / wk", "#FFFFFF", INK, 7, 12)
            + sticker(286, 46, "Python", "#FFFFFF", INK, 9, 12)
            + sticker(28, 148, "{ }", "#2F6BE0", "#FFFFFF", 8, 14)
            + sticker(288, 150, "npm run dev", "#FFFFFF", INK, -8, 11)
            + smiley(146, 246, 17))


def art_projects(hue):
    return (phone(10, 62, 0.86, -12, shot("p1.jpg", "s1"))
            + phone(276, 58, 0.86, 12, shot("p3.jpg", "s3"))
            + phone(140, 34, 0.96, 0, shot("p2.jpg", "s2"))
            + sticker(16, 36, "12 builds", hue, INK, -10)
            + sticker(222, 236, "SwiftUI", "#FFFFFF", INK, 7, 12)
            + sticker(296, 38, "Xcode", "#FFFFFF", INK, 9, 12)
            + sticker(18, 170, "git commit", "#FFFFFF", INK, 8, 11)
            + smiley(330, 130, 17))


def art_contact(hue):
    return (imessage(74, 46, 0.94)
            + sticker(22, 40, "Let&#8217;s talk", hue, INK, -9)
            + sticker(214, 220, "Open to interns", "#FFFFFF", INK, 7, 12)
            + sticker(26, 172, "@ inbox", "#FFFFFF", INK, 8, 12)
            + sticker(288, 136, "say hi", hue, INK, -8, 12)
            + smiley(316, 48, 18))


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
        '<rect x="8" y="11" width="32" height="22" rx="3.4" fill="#FFFFFF"/>'
        '<rect x="11.4" y="14.4" width="25.2" height="15.2" rx="2" '
        'fill="#FFFFFF" fill-opacity="0.35"/>'
        '<path d="M4 35h40l3 5H1z" fill="#FFFFFF" fill-opacity="0.8"/>',
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
          'flood-opacity="0.55"/></filter>')

for sid, hue, deep in SECTIONS:
    art = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 430 300" '
           'width="430" height="300"><defs>%s'
           '<radialGradient id="g" cx="50%%" cy="50%%" r="62%%">'
           '<stop offset="0" stop-color="%s" stop-opacity="0.24"/>'
           '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
           '</radialGradient>%s</defs>'
           '<ellipse cx="215" cy="150" rx="212" ry="146" fill="url(#g)"/>'
           '%s</svg>' % (SHADOW, hue, deep, CUT_FILTER, ART[sid](hue)))
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
            '</svg>'
            % (hue, deep, ICONS[sid]))
    for name, data in (("peek-%s.svg" % sid, art), ("icon-%s.svg" % sid, icon)):
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(data)
        print("wrote %s (%d bytes)" % (name, len(data)))
