# -*- coding: utf-8 -*-
"""Bake each peek-*.svg into a WebP bitmap.

The scenes carry drop-shadow filters over embedded photos. As SVG, the
browser re-rasterises all of that on every frame of the open animation,
which is what made the hover feel heavy. A bitmap animates for free.

Run after tools-make-peek-art.py:  python3 tools-rasterize-peeks.py
"""
import os
import subprocess
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "images")
CHROME = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
W, H = 688, 480            # 2x display size, for retina

for sid in ("about", "education", "craft", "projects", "contact"):
    svg = os.path.join(IMAGES, "peek-%s.svg" % sid)
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "p.html")
        with open(page, "w") as fh:
            fh.write('<!doctype html><style>html,body{margin:0;background:none}'
                     'img{display:block;width:%dpx;height:%dpx}</style>'
                     '<img src="file://%s">' % (W, H, svg))
        shot = os.path.join(tmp, "out.png")
        subprocess.run([CHROME, "--headless", "--disable-gpu",
                        "--hide-scrollbars", "--allow-file-access-from-files",
                        "--default-background-color=00000000",
                        "--virtual-time-budget=4000",
                        "--window-size=%d,%d" % (W, H),
                        "--screenshot=" + shot, "file://" + page],
                       check=True, capture_output=True)
        im = Image.open(shot).convert("RGBA")
    dst = os.path.join(IMAGES, "peek-%s.webp" % sid)
    im.save(dst, quality=80, method=6)
    print("wrote %s %s (%dKB, was %dKB as svg)"
          % (os.path.basename(dst), im.size, os.path.getsize(dst) // 1024,
             os.path.getsize(svg) // 1024))
