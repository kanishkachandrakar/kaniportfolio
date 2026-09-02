# -*- coding: utf-8 -*-
"""Draw the rail icons.

Clean flat symbols on a coloured tile - one per section, in the same colour
as the photo that section raises. About uses a real photo instead of a
symbol, so it is not generated here.
Run: python3 tools-make-peek-art.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

MOTIFS = {
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
    ("education", "#8FB8EA", "#3F5F8E"),
    ("skills",    "#93D3AC", "#3F7A5B"),
    ("projects",  "#C2A2EA", "#63479A"),
    ("work",      "#EBA277", "#96522C"),
    ("contact",   "#E895AC", "#93475E"),
]

for sid, hue, deep in SECTIONS:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" '
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
        % (hue, deep, MOTIFS[sid]))
    name = "icon-%s.svg" % sid
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(svg)
    print("wrote %s (%d bytes)" % (name, len(svg)))
