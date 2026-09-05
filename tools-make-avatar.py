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


def o(fill, sw=None):
    return ('fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" '
            'stroke-linecap="round"' % (fill, INK, SW if sw is None else sw))


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
    # width/height must follow the box, or a landscape scene gets letterboxed
    # into a portrait frame.
    w, h = box.split()[2:]
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" '
           'width="%s" height="%s">%s</svg>' % (box, w, h, "".join(body)))
    path = os.path.join(HERE, "images", name)
    with open(path, "w") as fh:
        fh.write(svg)
    print("wrote images/%s (%d bytes)" % (name, len(svg)))


# A wide desk scene for the Skills card: the reference's work illustration
# is landscape and sits along the top edge, so this is built to match -
# the desk and machine lead, and she is cut by the top of the frame.
# A wide desk scene for the Skills card. Drawn back to front - hair, head,
# face, then the desk and machine in front of her - because layering it the
# other way puts her hair over her face.
# The trick on the reference: the head lives on the About card and the body
# on the card below it, lined up in the same column, so the gap between the
# two cards reads as the cut across the neck. So this scene starts at the
# neck - no head - and the desk sits in front of her.
# The Skills card is a full square now, so she can be drawn whole: seated at
# a desk with her legs under it, rather than a head and shoulders behind a
# strip of desk.
WIDE = [
    '<defs><linearGradient id="wb" x1="0" y1="0" x2="0.4" y2="1">'
    '<stop offset="0" stop-color="#17130F"/>'
    '<stop offset="1" stop-color="#100C0A"/></linearGradient></defs>'
    '<rect width="440" height="300" fill="url(#wb)"/>',

    # chair, behind her
    '<rect x="268" y="74" width="86" height="120" rx="20" %s/>' % o("#3A2E26"),
    # head and hair
    '<ellipse cx="311" cy="66" rx="58" ry="62" %s/>' % o(HAIR),
    '<path d="M287 104h48v40c0 12-48 12-48 0z" %s/>' % o(SKIN),
    '<ellipse cx="311" cy="62" rx="45" ry="50" %s/>' % o(SKIN),
    '<path d="M266 56c2-33 20-52 45-52s43 19 45 52c-7-19-18-29-45-29'
    's-38 10-45 29z" %s/>' % o(HAIR),
    '<circle cx="294" cy="60" r="11" fill="#FFFFFF" stroke="%s" '
    'stroke-width="4"/>' % INK,
    '<circle cx="328" cy="60" r="11" fill="#FFFFFF" stroke="%s" '
    'stroke-width="4"/>' % INK,
    '<circle cx="296" cy="63" r="5.5" fill="%s"/>' % INK,
    '<circle cx="330" cy="63" r="5.5" fill="%s"/>' % INK,
    '<path d="M299 84c8 7 16 7 24 0" stroke="%s" stroke-width="5" '
    'fill="none" stroke-linecap="round"/>' % INK,
    '<circle cx="279" cy="76" r="7" fill="#E79A94" opacity="0.5"/>',
    '<circle cx="343" cy="76" r="7" fill="#E79A94" opacity="0.5"/>',
    '<rect x="251" y="40" width="23" height="40" rx="11" %s/>' % o(CUP),
    '<rect x="348" y="40" width="23" height="40" rx="11" %s/>' % o(CUP),
    '<path d="M267 50c0-29 20-48 44-48s44 19 44 48" fill="none" '
    'stroke="%s" stroke-width="9" stroke-linecap="round"/>' % CUP,
    # torso
    '<path d="M252 210c0-40 27-64 59-64s59 24 59 64z" %s/>' % o(NAVY),
    '<path d="M311 150l-12 60h24z" %s/>' % o(SHIRT),
    # legs, which is the point of the taller card
    '<rect x="284" y="200" width="22" height="72" rx="9" %s/>' % o(NAVY_SH),
    '<rect x="316" y="200" width="22" height="72" rx="9" %s/>' % o(NAVY_SH),
    '<rect x="276" y="262" width="34" height="18" rx="8" %s/>' % o("#2A2119"),
    '<rect x="312" y="262" width="34" height="18" rx="8" %s/>' % o("#2A2119"),
    # an arm reaching to the keyboard
    '<path d="M256 208c-8-30 4-52 28-62l12 22c-14 8-20 22-18 40z" %s/>' % o(NAVY),
    '<ellipse cx="258" cy="206" rx="17" ry="12" %s/>' % o(SKIN),

    # desk in front, with legs of its own
    '<rect x="14" y="186" width="18" height="94" rx="6" %s/>' % o("#5B3F2A"),
    '<rect x="404" y="186" width="18" height="94" rx="6" %s/>' % o("#5B3F2A"),
    '<path d="M-10 172h460v28H-10z" fill="#6B4A31"/>',
    '<path d="M-10 172h460v9H-10z" fill="#8C6444"/>',

    # and the machine on it
    '<path d="M70 84h150l24 88H46z" %s/>' % o("#EDE8DF"),
    '<path d="M84 96h122l18 64H66z" fill="#1B1E24"/>',
    '<path d="M96 110h56M92 126h76M88 142h44" stroke="#8FE3B0" '
    'stroke-width="5" stroke-linecap="round"/>',
    '<path d="M46 172h198l20 18H26z" %s/>' % o("#D7D1C6"),
    '<rect x="120" y="176" width="50" height="6" rx="3" fill="%s"/>' % INK,
]


# ONE 500x500 scene, used on both cards.
#
# This is how the reference does it: a single file (/finalincon.png - him at
# a desk, startled, laptop in front) placed twice and cropped two ways by the
# cards. The About card frames just the head; the work card frames the desk
# and machine with the head cut off above its top edge. Two drawings could
# never line up the way one drawing cropped twice does.
SCENE = [
    # her, behind the desk
    '<ellipse cx="332" cy="196" rx="86" ry="92" %s/>' % o(HAIR),
    '<path d="M232 372c0-62 45-100 100-100s100 38 100 100z" %s/>' % o(NAVY),
    '<path d="M332 278l-18 94h36z" %s/>' % o(SHIRT),
    '<ellipse cx="332" cy="188" rx="72" ry="80" %s/>' % o(SKIN),
    '<path d="M260 180c2-52 32-84 72-84s70 32 72 84c-12-30-32-46-72-46'
    's-60 16-72 46z" %s/>' % o(HAIR),
    # headphones
    '<rect x="236" y="164" width="34" height="58" rx="16" %s/>' % o(CUP),
    '<rect x="394" y="164" width="34" height="58" rx="16" %s/>' % o(CUP),
    '<path d="M254 176c0-46 35-80 78-80s78 34 78 80" fill="none" stroke="%s" '
    'stroke-width="15" stroke-linecap="round"/>' % INK,
    '<path d="M254 176c0-46 35-80 78-80s78 34 78 80" fill="none" stroke="%s" '
    'stroke-width="8" stroke-linecap="round"/>' % CUP,
    # startled, the way his is
    '<circle cx="300" cy="188" r="25" fill="#FFFFFF" stroke="%s" '
    'stroke-width="5"/>' % INK,
    '<circle cx="366" cy="188" r="25" fill="#FFFFFF" stroke="%s" '
    'stroke-width="5"/>' % INK,
    '<circle cx="304" cy="192" r="11" fill="%s"/>' % INK,
    '<circle cx="370" cy="192" r="11" fill="%s"/>' % INK,
    '<circle cx="308" cy="187" r="4" fill="#FFFFFF"/>',
    '<circle cx="374" cy="187" r="4" fill="#FFFFFF"/>',
    '<path d="M278 148c10-9 26-10 38-4" stroke="%s" stroke-width="7" '
    'fill="none" stroke-linecap="round"/>' % INK,
    '<path d="M350 144c12-6 28-4 38 5" stroke="%s" stroke-width="7" '
    'fill="none" stroke-linecap="round"/>' % INK,
    '<ellipse cx="332" cy="240" rx="19" ry="15" fill="#4A2A28" stroke="%s" '
    'stroke-width="5"/>' % INK,
    '<circle cx="272" cy="222" r="13" fill="#E79A94" opacity="0.55"/>',
    '<circle cx="392" cy="222" r="13" fill="#E79A94" opacity="0.55"/>',

    # the desk, in front of her
    '<path d="M0 386L500 370L500 500L0 500Z" fill="#6B4A31"/>',
    '<path d="M0 386L500 370L500 382L0 400Z" fill="#8C6444"/>',

    # The laptop sits well below her chin, so the work card can crop between
    # the two without clipping either. It is angled and shadowed so it reads
    # as standing on the desk rather than pasted onto it.
    '<ellipse cx="168" cy="424" rx="150" ry="17" fill="#3B2718" '
    'fill-opacity="0.55"/>',
    '<path d="M96 302h150l26 88H70z" %s/>' % o("#EDE8DF"),
    '<path d="M110 314h122l19 64H88z" fill="#1B1E24"/>',
    '<path d="M122 330h56M118 346h74M114 362h42" stroke="#8FE3B0" '
    'stroke-width="6" stroke-linecap="round"/>',
    # the deck, wider at the front than the hinge
    '<path d="M70 390h202l34 30H36z" %s/>' % o("#E4DFD6"),
    '<path d="M86 396h170l22 16H64z" fill="#CFC9BE"/>',
    '<rect x="140" y="414" width="62" height="6" rx="3" fill="%s" '
    'fill-opacity="0.7"/>' % INK,
]

write("kanishka-avatar.svg", HEAD[:1] + SHOULDERS + HEAD[1:])
write("kanishka-desk.svg", HEAD[:1] + DESK[:3] + HEAD[1:] + DESK[3:])
write("kanishka-desk-wide.svg", WIDE, box="0 0 440 300")
# head only, ending at the neck, for the card above
write("kanishka-head.svg", HEAD, box="44 56 232 250")
write("kanishka-scene.svg", SCENE, box="0 0 500 500")
