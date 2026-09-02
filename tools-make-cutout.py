# -*- coding: utf-8 -*-
"""Lift the subject out of images/user.jpg into a transparent cut-out.

Colour alone cannot do it: the studio backdrop (luminance 11-26) and her
hair (3-57) overlap almost entirely. Three tests together can -

  neutral   the backdrop is grey; the blazer is navy and skin is warm
  dark      the backdrop never exceeds ~26, so a cap keeps the white
            shirt out of the fill
  smooth    the backdrop is a smooth gradient (roughness 1-2) while hair
            is textured (4-27), which is what saves the hair

Run: python3 tools-make-cutout.py   ->  images/kanishka-cutout.webp
"""
import collections
import os

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "images", "user.jpg")
DST = os.path.join(HERE, "images", "kanishka-cutout.webp")

TOL = 11        # how far the fill may step in one move
MAX_LUM = 70    # brighter than this is never backdrop
MAX_ROUGH = 6   # rougher than this is never backdrop

im = Image.open(SRC).convert("RGB")
im.thumbnail((520, 520))
w, h = im.size
px = im.load()

gray = im.convert("L")
blur = gray.filter(ImageFilter.GaussianBlur(2.2))
g, b = gray.load(), blur.load()
fine = [[abs(g[x, y] - b[x, y]) for y in range(h)] for x in range(w)]
rough = [[max(fine[min(w - 1, max(0, x + dx))][min(h - 1, max(0, y + dy))]
              for dx in (-2, 0, 2) for dy in (-2, 0, 2)) for y in range(h)]
         for x in range(w)]


def backdrop(x, y):
    r, gg, bb = px[x, y]
    return (max(r, gg, bb) - min(r, gg, bb) <= 20 and abs(r - bb) <= 16
            and g[x, y] <= MAX_LUM and rough[x][y] <= MAX_ROUGH)


bg = bytearray(w * h)
q = collections.deque()
for x in range(w):
    for y in (0, h - 1):
        if backdrop(x, y) and not bg[y * w + x]:
            bg[y * w + x] = 1
            q.append((x, y))
for y in range(h):
    for x in (0, w - 1):
        if backdrop(x, y) and not bg[y * w + x]:
            bg[y * w + x] = 1
            q.append((x, y))

while q:
    x, y = q.popleft()
    r0, g0, b0 = px[x, y]
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx]:
            r, gg, bb = px[nx, ny]
            if abs(r - r0) + abs(gg - g0) + abs(bb - b0) < TOL and backdrop(nx, ny):
                bg[ny * w + nx] = 1
                q.append((nx, ny))

mask = Image.frombytes("L", (w, h), bytes(255 if not v else 0 for v in bg))
mask = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
mask = mask.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(0.9))

out = im.convert("RGBA")
out.putalpha(mask)
out = out.crop(mask.point(lambda v: 255 if v > 40 else 0).getbbox())
out.thumbnail((300, 300))
out.save(DST, quality=80, method=6)
print("wrote %s %s (%dKB)"
      % (os.path.relpath(DST, HERE), out.size, os.path.getsize(DST) // 1024))
