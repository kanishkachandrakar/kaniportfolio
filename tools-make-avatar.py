# -*- coding: utf-8 -*-
"""Draw the cartoons of Kanishka used on the bento cards.

Two of them, from the same character: a bust for About, and the same
person behind a laptop for Skills & Experience - both cropped by the card
edge the way the reference crops its own.

Flat shapes with a dark outline. The headphones are the point: her bio
says she debugs to Bollywood and Punjabi songs, so the character says
something true about her rather than being a generic head.

Run: python3 tools-make-avatar.py
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


HEAD = [
    # hair, behind everything
    '<path d="M60 196c0-72 40-118 100-118s100 46 100 118c0 40-6 74-14 104'
    'c-4 14-22 16-26 2-6-20-10-44-10-70-14 12-32 18-50 18s-36-6-50-18'
    'c0 26-4 50-10 70-4 14-22 12-26-2-8-30-14-64-14-104z" %s/>' % o(HAIR),

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

SHOULDERS = [
    '<path d="M40 420c0-64 44-102 120-102s120 38 120 102z" %s/>' % o(NAVY),
    '<path d="M160 330l-26 90h52z" %s/>' % o(SHIRT),
    '<path d="M118 322l42 26-14 26-30-38z" fill="%s"/>' % NAVY_SH,
    '<path d="M202 322l-42 26 14 26 30-38z" fill="%s"/>' % NAVY_SH,
]

# Behind a laptop: the same person, arms out to the keyboard.
DESK = [
    '<path d="M18 430c0-72 52-114 142-114s142 42 142 114z" %s/>' % o(NAVY),
    '<path d="M160 330l-22 62h44z" %s/>' % o(SHIRT),
    # arms reaching in
    '<path d="M44 430c-4-44 14-74 44-84l16 30c-18 8-28 28-26 54z" %s/>' % o(NAVY),
    '<path d="M276 430c4-44-14-74-44-84l-16 30c18 8 28 28 26 54z" %s/>' % o(NAVY),
    '<ellipse cx="72" cy="404" rx="20" ry="16" %s/>' % o(SKIN),
    '<ellipse cx="248" cy="404" rx="20" ry="16" %s/>' % o(SKIN),
    # the machine
    '<path d="M74 356h172l14 46H60z" %s/>' % o("#EDE8DF"),
    '<path d="M60 402h200l10 20H50z" %s/>' % o("#D7D1C6"),
    '<rect x="132" y="408" width="56" height="7" rx="3.5" fill="%s"/>' % INK,
    '<path d="M96 366h128l8 28H88z" fill="#1B1E24"/>',
    '<path d="M108 374h44M108 382h62M108 390h34" stroke="#8FE3B0" '
    'stroke-width="4" stroke-linecap="round"/>',
]


def write(name, body, box="0 0 320 430"):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" '
           'width="320" height="430">%s</svg>' % (box, "".join(body)))
    path = os.path.join(HERE, "images", name)
    with open(path, "w") as fh:
        fh.write(svg)
    print("wrote images/%s (%d bytes)" % (name, len(svg)))


write("kanishka-avatar.svg", HEAD[:1] + SHOULDERS + HEAD[1:])
write("kanishka-desk.svg", HEAD[:1] + DESK[:3] + HEAD[1:] + DESK[3:])
