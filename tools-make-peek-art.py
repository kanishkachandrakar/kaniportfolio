# -*- coding: utf-8 -*-
"""Draw the rail icons and the cartoon scene each one raises.

Icons and scenes are generated together so a section's sticker and its
picture always share a colour and a subject.
Run: python3 tools-make-peek-art.py
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

INK = "#2B211A"          # cartoon outline
SKIN = "#F3C9A2"
HAIR = "#3A2A21"
SPARK = "#FFE0A0"


# ------------------------------------------------------------- helpers
def sparkle(x, y, r, c=SPARK):
    k = r * 0.30
    pts = [(x, y - r), (x + k, y - k), (x + r, y), (x + k, y + k),
           (x, y + r), (x - k, y + k), (x - r, y), (x - k, y - k)]
    d = "M%s %s" % pts[0] + "".join("L%s %s" % p for p in pts[1:]) + "Z"
    return '<path d="%s" fill="%s"/>' % (d, c)


def star(x, y, r, c=SPARK):
    pts = []
    for i in range(10):
        ang = math.pi / 5 * i - math.pi / 2
        rad = r if i % 2 == 0 else r * 0.44
        pts.append((round(x + rad * math.cos(ang), 1),
                    round(y + rad * math.sin(ang), 1)))
    d = "M%s %s" % pts[0] + "".join("L%s %s" % p for p in pts[1:]) + "Z"
    return '<path d="%s" fill="%s"/>' % (d, c)


def blob(d, fill, sw=5):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" ' \
           'stroke-linejoin="round" stroke-linecap="round"/>' % (d, fill, INK, sw)


def rrect(x, y, w, h, r, fill, sw=5, extra=""):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, r, fill, INK, sw, extra))


def circ(cx, cy, r, fill, sw=5):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"/>' % (cx, cy, r, fill, INK, sw))


def face(cx, cy, s=1.0, happy=True):
    """Dot eyes and a smile, sized by s."""
    e = 3.4 * s
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="%s"/>'
            '<path d="M%s %sq%s %s %s 0" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-linecap="round"/>'
            % (cx - 11 * s, cy, e, INK, cx + 11 * s, cy, e, INK,
               cx - 10 * s, cy + 10 * s, 10 * s, 9 * s, 20 * s, INK, 3.6 * s))


# --------------------------------------------------------------- scenes
def scene_about(hue):
    return (
        blob("M186 300c0-46 30-78 74-78s74 32 74 78z", hue)          # body
        + circ(260, 176, 54, SKIN)                                    # head
        + blob("M206 168c2-40 26-62 54-62s52 22 54 62c-14-16-30-24-54-24"
               "s-40 8-54 24z", HAIR, 4)                              # hair
        + face(260, 176, 1.0)
        # arm, drawn ink-first so the outline sits behind the fill
        + '<path d="M302 262q44-18 46-58" stroke="%s" stroke-width="32" '
          'fill="none" stroke-linecap="round"/>' % INK
        + '<path d="M302 262q44-18 46-58" stroke="%s" stroke-width="22" '
          'fill="none" stroke-linecap="round"/>' % hue
        + circ(346, 196, 20, SKIN)                                    # waving hand
        + '<path d="M372 172c8-4 16-6 24-4M374 190c9 0 17 2 24 6" '
          'stroke="%s" stroke-width="5" stroke-linecap="round" fill="none"/>' % INK
        + rrect(88, 116, 108, 66, 20, "#FFFFFF")                      # speech bubble
        + blob("M126 178l-6 26 30-20z", "#FFFFFF")
        + ''.join('<circle cx="%s" cy="149" r="6" fill="%s"/>' % (x, INK)
                  for x in (118, 142, 166))
        + sparkle(408, 122, 15) + sparkle(432, 252, 11) + star(72, 262, 13))


def scene_education(hue):
    books = (rrect(150, 236, 168, 30, 8, "#F2A0A8")
             + rrect(140, 264, 188, 30, 8, "#9FD0F0")
             + rrect(158, 292, 152, 30, 8, "#FBD489"))
    cap = ('<g transform="rotate(-12 246 150)">'
           + blob("M246 96 358 138 246 180 134 138z", hue)
           + blob("M182 158v34c0 18 28 30 64 30s64-12 64-30v-34", "#FFFFFF", 5)
           + '<path d="M350 142v54" stroke="%s" stroke-width="5" '
             'stroke-linecap="round" fill="none"/>' % INK
           + circ(350, 204, 11, SPARK) + '</g>')
    scroll = ('<g transform="rotate(14 404 262)">'
              + rrect(374, 226, 62, 74, 10, "#FFF6E4")
              + '<path d="M386 248h38M386 264h38M386 280h24" stroke="%s" '
                'stroke-width="4" stroke-linecap="round"/>' % INK
              + rrect(366, 254, 78, 16, 8, hue) + '</g>')
    return books + cap + scroll + sparkle(96, 178, 15) + star(438, 132, 13) \
        + sparkle(78, 300, 11)


def scene_skills(hue):
    def cube(x, y, c1, c2, c3):
        return (blob("M%s %sl46-26 46 26-46 26z" % (x, y), c1)
                + blob("M%s %sv52l46 26v-52z" % (x, y), c2)
                + blob("M%s %sv52l-46 26v-52z" % (x + 92, y), c3))
    return (cube(150, 214, "#B7E7CB", "#8ED2AC", "#5FAE86")
            + cube(258, 214, "#CFE3FA", "#A6C8F0", "#7BA5D8")
            + cube(204, 150, "#FFD9A6", hue, "#D89A5E")
            + blob("M330 96l-46 66h30l-14 56 52-74h-32z", "#FFD452")   # bolt
            + sparkle(112, 138, 16) + sparkle(420, 210, 12)
            + star(140, 306, 12) + star(392, 118, 11))


def scene_projects(hue):
    laptop = (rrect(126, 122, 218, 146, 16, "#FFFFFF")
              + rrect(144, 140, 182, 110, 10, hue, 0)
              + face(235, 186, 1.15)
              + blob("M104 268h262l20 34H84z", "#E7ECF3")
              + '<rect x="212" y="280" width="46" height="7" rx="3.5" fill="%s"/>' % INK)
    phone = ('<g transform="rotate(11 396 226)">'
             + rrect(360, 156, 82, 148, 18, "#FFFFFF")
             + rrect(370, 168, 62, 112, 10, "#9FD0F0", 0)
             + '<rect x="388" y="288" width="26" height="6" rx="3" fill="%s"/>' % INK
             + '</g>')
    return laptop + phone + sparkle(88, 128, 15) + star(452, 122, 12) \
        + sparkle(96, 300, 11)


def scene_work(hue):
    rocket = ('<g transform="rotate(-18 250 190)">'
              + blob("M250 74c34 30 52 74 52 120l-16 40h-72l-16-40c0-46 18-90 52-120z", "#FFFFFF")
              + circ(250, 158, 22, "#9FD0F0")
              + blob("M198 186l-38 34v42l38-24z", hue)
              + blob("M302 186l38 34v42l-38-24z", hue)
              + blob("M222 234h56l-28 58z", "#FFB459")
              + blob("M236 248h28l-14 30z", "#FFE07A", 0)
              + '</g>')
    clouds = (blob("M78 268c0-14 12-24 26-24 4-16 20-26 36-22 8-12 26-14 36-2"
                   "c16-2 28 10 26 24-2 14-14 24-28 24H104c-14 0-26-10-26-24z",
                   "#FFFFFF", 4)
              + blob("M340 300c0-10 9-18 20-18 3-12 15-19 27-16 6-9 20-11 27-2"
                     "c12-1 21 8 19 18-1 11-10 18-21 18h-52c-11 0-20-8-20-18z",
                     "#FFFFFF", 4))
    return (clouds + rocket
            + '<path d="M92 150c22-6 44-6 66 0M84 178c18-5 36-5 54 0" '
              'stroke="#FFFFFF" stroke-opacity="0.7" stroke-width="6" '
              'stroke-linecap="round" fill="none"/>'
            + star(420, 108, 14) + sparkle(452, 196, 12) + sparkle(104, 96, 13))


def scene_contact(hue):
    env = (rrect(112, 176, 214, 148, 16, "#FFFFFF")
           + blob("M112 190l107 74 107-74", "none", 5).replace('fill="none"', 'fill="none"')
           + blob("M112 192l107 76 107-76v-6c0-8-6-14-14-14H126c-8 0-14 6-14 14z", hue))
    plane = ('<g transform="rotate(-16 368 156)">'
             + blob("M436 92 296 156l60 22 22 60z", "#FFFFFF")
             + blob("M356 178 436 92l-58 146-22-60z", "#DCE6F5", 4)
             + '</g>')
    trail = ('<path d="M96 130q40-30 84-14" stroke="#FFFFFF" stroke-opacity="0.6" '
             'stroke-width="6" stroke-linecap="round" stroke-dasharray="2 20" '
             'fill="none"/>')
    return env + plane + trail + sparkle(84, 246, 15) + star(448, 268, 13) \
        + sparkle(150, 92, 11)


SCENES = {
    "about": scene_about, "education": scene_education, "skills": scene_skills,
    "projects": scene_projects, "work": scene_work, "contact": scene_contact,
}


# ---------------------------------------------------------------- icons
def icon_motif(sid, hue):
    if sid == "about":
        return (circ(24, 25, 14, SPARK, 2.6)
                + '<circle cx="19.4" cy="22.6" r="2.1" fill="%s"/>'
                  '<circle cx="28.6" cy="22.6" r="2.1" fill="%s"/>' % (INK, INK)
                + '<path d="M18.6 28.6q5.4 5 10.8 0" stroke="%s" stroke-width="2.4" '
                  'fill="none" stroke-linecap="round"/>' % INK
                + '<circle cx="16.4" cy="27.8" r="2.2" fill="#F09A9A" opacity="0.75"/>'
                  '<circle cx="31.6" cy="27.8" r="2.2" fill="#F09A9A" opacity="0.75"/>')
    if sid == "education":
        return (blob("M24 12 40 20 24 28 8 20z", "#FFFFFF", 2.6)
                + blob("M14 23v7c0 3.4 4.5 5.8 10 5.8s10-2.4 10-5.8v-7l-10 5z",
                       "#DCE6F5", 2.6)
                + '<path d="M38.4 21v9" stroke="%s" stroke-width="2.4" '
                  'stroke-linecap="round" fill="none"/>' % INK
                + circ(38.4, 32, 2.6, SPARK, 2.2))
    if sid == "skills":
        return (blob("M24 10l14 8-14 8-14-8z", "#FFE1B0", 2.6)
                + blob("M10 18v16l14 8V26z", "#F0B979", 2.6)
                + blob("M38 18v16l-14 8V26z", "#D89A5E", 2.6))
    if sid == "projects":
        return (rrect(10, 13, 28, 20, 4, "#FFFFFF", 2.6)
                + rrect(13.4, 16.4, 21.2, 13.2, 2.4, hue, 0)
                + '<circle cx="20.4" cy="21.6" r="1.5" fill="%s"/>'
                  '<circle cx="27.6" cy="21.6" r="1.5" fill="%s"/>' % (INK, INK)
                + '<path d="M20 25.4q4 3.4 8 0" stroke="%s" stroke-width="1.9" '
                  'fill="none" stroke-linecap="round"/>' % INK
                + blob("M7 33h34l3 5H4z", "#E7ECF3", 2.4))
    if sid == "work":
        return (blob("M24 7c6 5.4 9.2 13.2 9.2 21.4l-3 7.2H17.8l-3-7.2"
                     "C14.8 20.2 18 12.4 24 7z", "#FFFFFF", 2.6)
                + circ(24, 22, 4.2, "#9FD0F0", 2.4)
                + blob("M15 29.6l-5 4.6v6l5-3.2z", hue, 2.4)
                + blob("M33 29.6l5 4.6v6l-5-3.2z", hue, 2.4)
                + blob("M20.6 36.6h6.8L24 44z", "#FFB459", 2.4))
    return (blob("M41 8 8 22l11.6 4.2L23.4 39z", "#FFFFFF", 2.6)
            + blob("M19.6 26.2 41 8 28.6 36.6l-5.2-9.6z", "#DCE6F5", 2.4))


SECTIONS = [
    ("about",     "#E8B87C", "#96602A"),
    ("education", "#8FB8EA", "#3F5F8E"),
    ("skills",    "#93D3AC", "#3F7A5B"),
    ("projects",  "#C2A2EA", "#63479A"),
    ("work",      "#EBA277", "#96522C"),
    ("contact",   "#E895AC", "#93475E"),
]

for sid, hue, deep in SECTIONS:
    icon = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" '
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
        '%s'
        '<rect x="0.7" y="0.7" width="46.6" height="46.6" rx="12.9" fill="none" '
        'stroke="#FFFFFF" stroke-opacity="0.30"/></svg>'
        % (hue, deep, icon_motif(sid, hue)))

    scene = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 360" '
        'width="520" height="360">'
        '<defs><radialGradient id="g" cx="50%%" cy="48%%" r="66%%">'
        '<stop offset="0" stop-color="%s" stop-opacity="0.30"/>'
        '<stop offset="0.55" stop-color="%s" stop-opacity="0.12"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
        '</radialGradient></defs>'
        '<ellipse cx="260" cy="184" rx="258" ry="176" fill="url(#g)"/>'
        '%s</svg>' % (hue, deep, deep, SCENES[sid](hue)))

    for name, data in (("icon-%s.svg" % sid, icon), ("peek-%s.svg" % sid, scene)):
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(data)
        print("wrote %s (%d bytes)" % (name, len(data)))
