# -*- coding: utf-8 -*-
"""Draw the cartoon of Kanishka used on the About card.

Flat shapes with a dark outline, in the manner of the reference site's own
character. The headphones are the point: her bio says she debugs to
Bollywood and Punjabi songs, so the avatar says something true about her
rather than being a generic head.

Run: python3 tools-make-avatar.py  ->  images/kanishka-avatar.svg
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "images", "kanishka-avatar.svg")

INK = "#241C16"
SKIN = "#EEC49E"
SKIN_SH = "#DCAE85"
HAIR = "#3B2A20"
HAIR_HI = "#5A4130"
NAVY = "#2C3B59"
NAVY_SH = "#233049"
SHIRT = "#F6F2EA"
CUP = "#E8B87C"
CUP_SH = "#C89355"

SW = 6          # outline weight


def o(fill):
    return ('fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" '
            'stroke-linecap="round"' % (fill, INK, SW))


parts = [
    # hair, behind everything
    '<path d="M60 196c0-72 40-118 100-118s100 46 100 118c0 40-6 74-14 104'
    'c-4 14-22 16-26 2-6-20-10-44-10-70-14 12-32 18-50 18s-36-6-50-18'
    'c0 26-4 50-10 70-4 14-22 12-26-2-8-30-14-64-14-104z" %s/>' % o(HAIR),

    # shoulders
    '<path d="M40 420c0-64 44-102 120-102s120 38 120 102z" %s/>' % o(NAVY),
    '<path d="M160 330l-26 90h52z" %s/>' % o(SHIRT),
    '<path d="M118 322l42 26-14 26-30-38z" fill="%s"/>' % NAVY_SH,
    '<path d="M202 322l-42 26 14 26 30-38z" fill="%s"/>' % NAVY_SH,

    # neck
    '<path d="M136 268h48v56c0 14-48 14-48 0z" %s/>' % o(SKIN),
    '<path d="M136 284c14 10 34 12 48 6v-22h-48z" fill="%s"/>' % SKIN_SH,

    # head
    '<ellipse cx="160" cy="186" rx="76" ry="86" %s/>' % o(SKIN),

    # fringe, parted in the middle
    '<path d="M84 178c2-58 34-92 76-92s74 34 76 92c-10-34-30-52-54-58'
    'c-6 14-16 22-30 26-24 6-48 12-68 32z" %s/>' % o(HAIR),
    '<path d="M108 128c14-16 32-24 52-24" stroke="%s" stroke-width="5" '
    'fill="none" stroke-linecap="round"/>' % HAIR_HI,

    # ears
    '<circle cx="84" cy="196" r="14" %s/>' % o(SKIN),
    '<circle cx="236" cy="196" r="14" %s/>' % o(SKIN),

    # headphones
    '<path d="M74 192c0-52 38-90 86-90s86 38 86 90" fill="none" stroke="%s" '
    'stroke-width="16" stroke-linecap="round"/>' % INK,
    '<path d="M74 192c0-52 38-90 86-90s86 38 86 90" fill="none" stroke="%s" '
    'stroke-width="8" stroke-linecap="round"/>' % CUP,
    '<rect x="56" y="176" width="38" height="56" rx="16" %s/>' % o(CUP),
    '<rect x="226" y="176" width="38" height="56" rx="16" %s/>' % o(CUP),
    '<rect x="64" y="188" width="22" height="32" rx="11" fill="%s"/>' % CUP_SH,
    '<rect x="234" y="188" width="22" height="32" rx="11" fill="%s"/>' % CUP_SH,

    # eyes, big and bright
    '<ellipse cx="130" cy="186" rx="17" ry="19" fill="#FFFFFF" stroke="%s" '
    'stroke-width="4.5"/>' % INK,
    '<ellipse cx="190" cy="186" rx="17" ry="19" fill="#FFFFFF" stroke="%s" '
    'stroke-width="4.5"/>' % INK,
    '<circle cx="133" cy="189" r="8.5" fill="%s"/>' % INK,
    '<circle cx="193" cy="189" r="8.5" fill="%s"/>' % INK,
    '<circle cx="136.5" cy="185" r="3" fill="#FFFFFF"/>',
    '<circle cx="196.5" cy="185" r="3" fill="#FFFFFF"/>',

    # brows
    '<path d="M114 158c8-7 22-8 32-3" stroke="%s" stroke-width="6" '
    'fill="none" stroke-linecap="round"/>' % INK,
    '<path d="M174 155c10-5 24-4 32 3" stroke="%s" stroke-width="6" '
    'fill="none" stroke-linecap="round"/>' % INK,

    # nose and smile
    '<path d="M160 196v14c0 4-4 7-8 7" stroke="%s" stroke-width="5" '
    'fill="none" stroke-linecap="round"/>' % INK,
    '<path d="M138 228c12 12 32 12 44 0" stroke="%s" stroke-width="6" '
    'fill="none" stroke-linecap="round"/>' % INK,

    # cheeks
    '<circle cx="110" cy="214" r="11" fill="#E79A94" opacity="0.55"/>',
    '<circle cx="210" cy="214" r="11" fill="#E79A94" opacity="0.55"/>',
]

svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 430" '
       'width="320" height="430">'
       '<g transform="translate(0 0)">%s</g></svg>' % "".join(parts))

with open(DST, "w") as fh:
    fh.write(svg)
print("wrote %s (%d bytes)" % (os.path.relpath(DST, HERE), len(svg)))
