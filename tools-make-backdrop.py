# -*- coding: utf-8 -*-
"""Render the backdrop the glass card floats on.

The reference uses a photograph of a sunlit loft. This paints the same idea
procedurally - warm window light raking across a dark room, a plank floor
catching it, dust in the air - so the site carries no stock imagery.

Run: python3 tools-make-backdrop.py  ->  images/scene.webp
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "images", "scene.webp")
W, H = 1920, 1200
random.seed(7)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# --- the room: warm at the top where the light is, sinking to near black ---
base = Image.new("RGB", (W, H))
d = ImageDraw.Draw(base)
TOP, MID, BOT = (46, 33, 23), (28, 20, 15), (10, 8, 7)
for y in range(H):
    t = y / float(H)
    d.line([(0, y), (W, y)], fill=lerp(TOP, MID, t * 1.6) if t < 0.62
           else lerp(MID, BOT, (t - 0.62) / 0.38))

# --- the window: a broad warm pool of light from the upper right ----------
glow = Image.new("RGB", (W, H), (0, 0, 0))
g = ImageDraw.Draw(glow)
for r, c in ((760, (150, 104, 58)), (520, (196, 140, 80)), (300, (228, 176, 110))):
    g.ellipse([W * 0.72 - r, H * 0.10 - r, W * 0.72 + r, H * 0.10 + r], fill=c)
glow = glow.filter(ImageFilter.GaussianBlur(190))
base = Image.blend(base, Image.new("RGB", (W, H), (0, 0, 0)), 0.0)
base = Image.composite(Image.new("RGB", (W, H), (255, 236, 208)), base,
                       glow.convert("L").point(lambda v: int(v * 0.62)))

# --- the window the light comes through -----------------------------------
WX0, WX1 = W * 0.615, W * 0.945
WY0, WY1 = H * 0.045, H * 0.545
win = Image.new("RGBA", (W, H), (0, 0, 0, 0))
wd = ImageDraw.Draw(win)
wd.rounded_rectangle([WX0, WY0, WX1, WY1], radius=26, fill=(206, 180, 143, 232))
# frame: one mullion, two transoms
bar = (44, 31, 22, 255)
wd.rounded_rectangle([WX0 - 12, WY0 - 12, WX1 + 12, WY1 + 12], radius=30,
                     outline=bar, width=22)
mid = (WX0 + WX1) / 2
wd.rectangle([mid - 8, WY0, mid + 8, WY1], fill=bar)
for t in (0.34, 0.67):
    y = WY0 + (WY1 - WY0) * t
    wd.rectangle([WX0, y - 7, WX1, y + 7], fill=bar)
win = win.filter(ImageFilter.GaussianBlur(2.2))
base = Image.alpha_composite(base.convert("RGBA"), win).convert("RGB")

# bloom spilling off the glass
bloom = Image.new("L", (W, H), 0)
ImageDraw.Draw(bloom).rounded_rectangle([WX0 - 40, WY0 - 40, WX1 + 40, WY1 + 40],
                                        radius=60, fill=104)
bloom = bloom.filter(ImageFilter.GaussianBlur(120))
base = Image.composite(Image.new("RGB", (W, H), (206, 176, 138)), base, bloom)

# --- ceiling beams --------------------------------------------------------
beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beams)
bd.rectangle([0, 0, W, H * 0.055], fill=(26, 18, 13, 250))
for i in range(7):
    x = W * (i / 6.0)
    bd.polygon([(x - 34, 0), (x + 34, 0), (x + 78, H * 0.135), (x - 78, H * 0.135)],
               fill=(30, 21, 15, 205))
bd.rectangle([0, H * 0.128, W, H * 0.150], fill=(22, 15, 11, 190))
beams = beams.filter(ImageFilter.GaussianBlur(3.5))
base = Image.alpha_composite(base.convert("RGBA"), beams).convert("RGB")

# --- brick suggestion on the left wall ------------------------------------
brick = Image.new("RGBA", (W, H), (0, 0, 0, 0))
kd = ImageDraw.Draw(brick)
row = 0
y = H * 0.14
while y < H * 0.70:
    kd.line([(0, y), (W * 0.40, y)], fill=(70, 48, 34, 70), width=2)
    off = 0 if row % 2 else 46
    for x in range(-40, int(W * 0.40), 92):
        kd.line([(x + off, y), (x + off, y + 26)], fill=(70, 48, 34, 55), width=2)
    y += 26
    row += 1
brick = brick.filter(ImageFilter.GaussianBlur(1.4))
base = Image.alpha_composite(base.convert("RGBA"), brick).convert("RGB")

# --- light shafts raking down to the left ---------------------------------
shafts = Image.new("L", (W, H), 0)
s = ImageDraw.Draw(shafts)
for i, (x, wide, val) in enumerate(((0.64, 170, 132), (0.78, 110, 104),
                                    (0.90, 200, 78), (0.70, 80, 66))):
    x0 = W * x
    s.polygon([(x0, H * 0.10), (x0 + wide, H * 0.10),
               (x0 - W * 0.42 + wide, H * 1.05), (x0 - W * 0.42, H * 1.05)],
              fill=val)
shafts = shafts.filter(ImageFilter.GaussianBlur(86))
shafts = shafts.point(lambda v: int(v * 0.62))
base = Image.composite(Image.new("RGB", (W, H), (255, 240, 214)), base, shafts)

# --- plank floor, catching the light --------------------------------------
floor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
f = ImageDraw.Draw(floor)
HORIZON = int(H * 0.66)
f.rectangle([0, HORIZON, W, H], fill=(34, 23, 16, 235))
y = HORIZON
step = 3.0
while y < H:
    y += step
    step *= 1.14
    f.line([(0, y), (W, y)], fill=(12, 8, 6, 170), width=max(1, int(step * 0.16)))
for k in range(-8, 26):                      # boards converging to a vanishing point
    x_far = W * 0.62 + k * 26
    x_near = W * 0.62 + k * 250
    f.line([(x_far, HORIZON), (x_near, H)], fill=(14, 9, 7, 120), width=2)
floor = floor.filter(ImageFilter.GaussianBlur(1.6))
base = Image.alpha_composite(base.convert("RGBA"), floor).convert("RGB")

# a wash of the same window light spilling across the boards
spill = Image.new("L", (W, H), 0)
sp = ImageDraw.Draw(spill)
sp.polygon([(W * 0.52, HORIZON), (W * 0.98, HORIZON), (W * 1.15, H), (W * 0.10, H)],
           fill=96)
spill = spill.filter(ImageFilter.GaussianBlur(120))
base = Image.composite(Image.new("RGB", (W, H), (226, 176, 116)), base, spill)

# --- dust in the light ----------------------------------------------------
dust = Image.new("L", (W, H), 0)
du = ImageDraw.Draw(dust)
for _ in range(220):
    x = random.gauss(W * 0.66, W * 0.20)
    y = random.gauss(H * 0.40, H * 0.26)
    r = random.uniform(1.0, 3.4)
    du.ellipse([x - r, y - r, x + r, y + r], fill=random.randint(60, 150))
dust = dust.filter(ImageFilter.GaussianBlur(2.2))
base = Image.composite(Image.new("RGB", (W, H), (255, 244, 226)), base, dust)

# --- settle it: a touch of blur, then a vignette --------------------------
base = base.filter(ImageFilter.GaussianBlur(1.4))
base = base.point(lambda v: int(v * 0.72))          # a stop darker overall
vig = Image.new("L", (W, H), 0)
v = ImageDraw.Draw(vig)
v.ellipse([-W * 0.18, -H * 0.22, W * 1.18, H * 1.22], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(260))
base = Image.composite(base, Image.new("RGB", (W, H), (6, 5, 4)), vig)

base.save(DST, quality=82, method=6)
print("wrote %s %s (%dKB)" % (os.path.relpath(DST, HERE), base.size,
                              os.path.getsize(DST) // 1024))
