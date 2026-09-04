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
    body = (
        rect(10, 8, 216, 146, 14, "#F4F0E9", 6)                     # lid
        + '<rect x="22" y="20" width="192" height="122" rx="8" fill="#15161A"/>'
        + '<clipPath id="lap"><rect x="22" y="20" width="192" height="122" '
          'rx="8"/></clipPath>'
        + img(photo("lap.jpg"), 22, 20, 192, 122, "lap")
        + '<rect x="22" y="20" width="192" height="122" rx="8" fill="none" '
          'stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="2"/>'
        # a soft sheen across the glass
        + '<path d="M22 20h74l-46 122H30a8 8 0 0 1-8-8z" fill="#FFFFFF" '
          'fill-opacity="0.06"/>'
        + path("M-8 154h252l20 30H-28z", "#E4E9EE", 6)               # base
        + '<rect x="96" y="162" width="44" height="7" rx="3.5" '
          'fill="#B9C2CB"/>'                                        # notch
        + '<path d="M-20 184h268" stroke="#C2CAD2" stroke-width="5" '
          'stroke-linecap="round"/>')
    return ('<g transform="translate(%s %s) scale(%s) rotate(%s 110 96)" '
            'filter="url(#d)">%s</g>' % (x, y, s, rot, body))


def phone(x, y, s, rot, screen):
    """A handset: rounded shell, inset screen, island and a side button."""
    body = (rect(0, 0, 104, 212, 22, "#F4F0E9", 6)
            + screen
            + '<rect x="38" y="14" width="28" height="8" rx="4" fill="#15161A"/>'
            + '<rect x="104" y="56" width="4" height="30" rx="2" '
              'fill="#DCD6CD"/>')
    return ('<g transform="translate(%s %s) scale(%s) rotate(%s 52 106)" '
            'filter="url(#d)">%s</g>' % (x, y, s, rot, body))


def shot(name, cid):
    """A real app screen filling the handset's display."""
    return ('<clipPath id="%s"><rect x="9" y="10" width="86" height="192" '
            'rx="15"/></clipPath>' % cid
            + '<rect x="9" y="10" width="86" height="192" rx="15" '
              'fill="#15161A"/>'
            + '<image href="%s" x="9" y="10" width="86" height="192" '
              'preserveAspectRatio="xMidYMid slice" clip-path="url(#%s)"/>'
              % (photo_webp(name), cid)
            + '<rect x="9" y="10" width="86" height="192" rx="15" fill="none" '
              'stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.6"/>')


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
            + sticker(6, 74, "Dean&#8217;s List", hue, INK, -10)
            + sticker(158, 252, "Penn State", "#FFFFFF", INK, 6, 12)
            + sticker(318, 122, "AI / ML", "#FFFFFF", INK, -8, 12))


def art_craft(hue):
    return (laptop(94, 48, 1.02, -4, hue)
            + sticker(2, 62, "PyTorch", hue, INK, -10)
            + sticker(150, 250, "30+ reviews / wk", "#FFFFFF", INK, 6, 12)
            + sticker(316, 104, "Python", "#FFFFFF", INK, -8, 12)
            + sticker(6, 200, "Docker", "#FFFFFF", INK, 8, 12))


def art_projects(hue):
    return (phone(16, 54, 0.80, -12, shot("p1.webp", "s1"))
            + phone(276, 50, 0.80, 12, shot("p3.webp", "s3"))
            + phone(146, 28, 0.92, 0, shot("p2.webp", "s2"))
            + sticker(2, 40, "12 builds", hue, INK, -10)
            + sticker(150, 254, "SwiftUI", "#FFFFFF", INK, 6, 12)
            + sticker(330, 160, "Xcode", "#FFFFFF", INK, -8, 12)
            + sticker(30, 196, "Firebase", "#FFFFFF", INK, 8, 12))


def art_contact(hue):
    return (imessage(74, 46, 0.94)
            + sticker(22, 40, "Let&#8217;s talk", hue, INK, -9)
            + sticker(214, 220, "Open to interns", "#FFFFFF", INK, 7, 12)
            + sticker(26, 172, "@ inbox", "#FFFFFF", INK, 8, 12)
            + sticker(288, 136, "based in NYC", hue, INK, -8, 12))


ART = {"about": art_about, "education": art_education, "craft": art_craft,
       "projects": art_projects, "contact": art_contact}

# Each icon shows the same object its preview opens on, rather than a
# generic pictogram - an ID card, a cap on books, a terminal, a fan of app
# screens, a chat thread.
ICONS = {
    "about":
        '<rect x="8" y="11" width="32" height="26" rx="5" fill="#FFFFFF"/>'
        '<rect x="8" y="11" width="32" height="7.5" rx="5" fill="#FFFFFF"/>'
        '<rect x="8" y="15" width="32" height="3.5" fill="#E4D8C6"/>'
        '<circle cx="18" cy="27" r="5.4" fill="#C79A62"/>'
        '<path d="M11.4 35.6c0-3.7 2.9-6 6.6-6s6.6 2.3 6.6 6z" fill="#C79A62"/>'
        '<rect x="27" y="24" width="10.5" height="2.8" rx="1.4" fill="#CFC2AE"/>'
        '<rect x="27" y="29" width="7.5" height="2.8" rx="1.4" fill="#DFD5C6"/>',
    "education":
        '<rect x="9" y="30" width="30" height="5.4" rx="2.2" fill="#E58B9B"/>'
        '<rect x="11" y="24.6" width="26" height="5.4" rx="2.2" fill="#7FB6E8"/>'
        '<polygon points="24,8 42,16 24,24 6,16" fill="#FFFFFF"/>'
        '<path d="M15 19.6v3.8c0 2.2 4 3.8 9 3.8s9-1.6 9-3.8v-3.8L24 23.6z" '
        'fill="#DCE7F8"/>'
        '<path d="M40.4 17v7.4" stroke="#FFFFFF" stroke-width="1.9" '
        'stroke-linecap="round" fill="none"/>'
        '<circle cx="40.4" cy="26" r="2.2" fill="#FFD452"/>',
    "craft":
        '<rect x="7" y="10" width="34" height="28" rx="5" fill="#F2EFE8"/>'
        '<rect x="7" y="10" width="34" height="7.6" rx="5" fill="#D9D3C7"/>'
        '<rect x="7" y="14" width="34" height="3.6" fill="#D9D3C7"/>'
        '<circle cx="12.6" cy="13.8" r="1.5" fill="#E5796F"/>'
        '<circle cx="17.4" cy="13.8" r="1.5" fill="#EBBE63"/>'
        '<circle cx="22.2" cy="13.8" r="1.5" fill="#7FBF87"/>'
        '<rect x="7" y="17.6" width="34" height="20.4" rx="0" fill="#1B1E24"/>'
        '<path d="M12.5 23.5l4.5 4-4.5 4" stroke="#8FE3B0" stroke-width="2.4" '
        'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="20" y="29.4" width="11" height="2.6" rx="1.3" fill="#8FE3B0"/>',
    "projects":
        '<g transform="rotate(-13 17 25)">'
        '<rect x="7" y="13" width="15" height="24" rx="3.4" fill="#F2EFE8"/>'
        '<rect x="9" y="16" width="11" height="14" rx="2" fill="#7EC4F0"/></g>'
        '<g transform="rotate(13 31 25)">'
        '<rect x="26" y="13" width="15" height="24" rx="3.4" fill="#F2EFE8"/>'
        '<rect x="28" y="16" width="11" height="14" rx="2" fill="#F0A9C0"/></g>'
        '<rect x="16.5" y="9" width="15" height="30" rx="3.6" fill="#FFFFFF"/>'
        '<rect x="18.6" y="12.4" width="10.8" height="16" rx="2.2" fill="#C2A2EA"/>'
        '<rect x="18.6" y="30.4" width="10.8" height="2.4" rx="1.2" '
        'fill="#D8CFE6"/>',
    "contact":
        '<path d="M9 12.5h20a4 4 0 0 1 4 4v7a4 4 0 0 1-4 4H17l-6 4.6v-4.6h-2'
        'a4 4 0 0 1-4-4v-7a4 4 0 0 1 4-4z" fill="#FFFFFF"/>'
        '<circle cx="14.5" cy="20" r="1.9" fill="#B5556F"/>'
        '<circle cx="20" cy="20" r="1.9" fill="#B5556F"/>'
        '<circle cx="25.5" cy="20" r="1.9" fill="#B5556F"/>'
        '<path d="M43 21.5a3.4 3.4 0 0 0-3.4-3.4h-4.2v9.4a3.4 3.4 0 0 0 3.4 3.4'
        'h1.6l3.2 2.6v-2.6h-.6z" fill="#FBDCE4"/>',
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
