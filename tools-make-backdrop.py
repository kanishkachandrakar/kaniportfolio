# -*- coding: utf-8 -*-
"""Paint the scene the glass card floats on: dusk over a mountain lake.

Generated rather than photographed, so the site carries no stock imagery.
The palette is deliberately warm and dark - amber at the horizon, deep
indigo overhead - so it sits under the card's own amber accent without
fighting the text.

Run: python3 tools-make-backdrop.py  ->  images/scene.webp
"""
import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "images", "scene.webp")
W, H = 1920, 1200
HORIZON = int(H * 0.615)
random.seed(11)


def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_colour(t):
    """t: 0 at the top of the sky, 1 at the horizon."""
    stops = [(0.00, (11, 16, 42)), (0.34, (39, 30, 63)), (0.62, (96, 54, 66)),
             (0.84, (176, 96, 62)), (1.00, (226, 152, 78))]
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0))
    return stops[-1][1]


img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
for y in range(HORIZON):
    d.line([(0, y), (W, y)], fill=sky_colour(y / float(HORIZON)))

# --- stars, only where the sky is still dark ------------------------------
for _ in range(260):
    x = random.uniform(0, W)
    y = random.uniform(0, HORIZON * 0.62)
    fade = 1.0 - (y / (HORIZON * 0.62))
    if random.random() > fade * 0.9:
        continue
    v = int(random.uniform(120, 235) * fade)
    r = random.choice([0.6, 0.6, 0.9, 1.3])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, int(v * 0.94)))

# --- the sun, low and hazy ------------------------------------------------
SUNX, SUNY = W * 0.655, HORIZON - H * 0.235
sun = Image.new("L", (W, H), 0)
sd = ImageDraw.Draw(sun)
for r, v in ((360, 44), (210, 82), (110, 148), (42, 255)):
    sd.ellipse([SUNX - r, SUNY - r * 0.92, SUNX + r, SUNY + r * 0.92], fill=v)
sun = sun.filter(ImageFilter.GaussianBlur(48))
img = Image.composite(Image.new("RGB", (W, H), (255, 214, 150)), img, sun)

# --- clouds: long, thin, catching the light from below --------------------
clouds = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(clouds)
for _ in range(26):
    cy = random.uniform(HORIZON * 0.26, HORIZON * 0.95)
    t = cy / float(HORIZON)
    cw = random.uniform(W * 0.10, W * 0.42)
    ch = random.uniform(6, 20) * (0.5 + t)
    cx = random.uniform(-W * 0.1, W * 1.1)
    lit = abs(cx - SUNX) < W * 0.34 and t > 0.55
    col = (238, 176, 116, 150) if lit else lerp((60, 48, 78), (150, 92, 78), t) + (110,)
    cd.ellipse([cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2], fill=col)
clouds = clouds.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img.convert("RGBA"), clouds).convert("RGB")


def ridge(base_y, rough, seed):
    """A mountain profile by midpoint displacement."""
    rnd = random.Random(seed)
    pts = [base_y, base_y - rough * 0.35, base_y]
    while len(pts) < 129:
        nxt = [pts[0]]
        for i in range(len(pts) - 1):
            mid = (pts[i] + pts[i + 1]) / 2 + rnd.uniform(-rough, rough)
            nxt += [mid, pts[i + 1]]
            rough *= 0.999
        pts = nxt
        rough *= 0.52
    return pts


# --- mountain ranges, hazier the further back -----------------------------
RANGES = [(HORIZON - H * 0.205, 160, (74, 60, 92), 4),
          (HORIZON - H * 0.145, 130, (49, 39, 64), 9),
          (HORIZON - H * 0.088, 100, (30, 24, 41), 17),
          (HORIZON - H * 0.038, 62, (17, 14, 24), 23)]
for base_y, rough, colour, seed in RANGES:
    ys = ridge(base_y, rough, seed)
    step = W / float(len(ys) - 1)
    poly = [(i * step, y) for i, y in enumerate(ys)]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.polygon(poly + [(W, HORIZON + 4), (0, HORIZON + 4)], fill=colour + (255,))
    # a rim of light on the slopes facing the sun
    ld.line(poly, fill=(228, 158, 104, 120), width=3)
    layer = layer.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

# haze settling between the ranges
haze = Image.new("L", (W, H), 0)
ImageDraw.Draw(haze).rectangle([0, HORIZON - H * 0.20, W, HORIZON], fill=90)
haze = haze.filter(ImageFilter.GaussianBlur(70))
img = Image.composite(Image.new("RGB", (W, H), (150, 96, 92)), img, haze)

# --- the lake: the sky again, upside down and disturbed -------------------
water = img.crop((0, int(HORIZON - (H - HORIZON)), W, HORIZON)).transpose(
    Image.FLIP_TOP_BOTTOM).resize((W, H - HORIZON))
water = water.point(lambda v: int(v * 0.62))
water = water.filter(ImageFilter.GaussianBlur(3.0))
img.paste(water, (0, HORIZON))

ripple = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(ripple)
y = HORIZON + 2
gap = 3.0
while y < H:
    a = int(52 + 70 * ((y - HORIZON) / float(H - HORIZON)))
    rd.line([(0, y), (W, y)], fill=(6, 8, 18, a), width=1)
    y += gap
    gap *= 1.035
ripple = ripple.filter(ImageFilter.GaussianBlur(1.8))
img = Image.alpha_composite(img.convert("RGBA"), ripple).convert("RGB")

# the sun's path on the water: one soft wedge, broken by the ripples
path = Image.new("L", (W, H), 0)
ImageDraw.Draw(path).polygon([(SUNX - 26, HORIZON), (SUNX + 26, HORIZON),
                              (SUNX + 210, H), (SUNX - 210, H)], fill=190)
path = path.filter(ImageFilter.GaussianBlur(46))
# a few broken glints riding on the wedge, not a ladder of them
glint = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glint)
yy = HORIZON + 8
while yy < H:
    half = 18 + 200 * ((yy - HORIZON) / float(H - HORIZON)) ** 1.5
    for _ in range(random.randint(1, 3)):
        cx = SUNX + random.uniform(-half, half)
        seg = random.uniform(half * 0.10, half * 0.34)
        gd.line([(cx - seg, yy), (cx + seg, yy)],
                fill=random.randint(70, 160), width=2)
    yy += random.uniform(9, 20)
glint = glint.filter(ImageFilter.GaussianBlur(4.0))
path = ImageChops.lighter(path.point(lambda v: int(v * 0.55)),
                          ImageChops.multiply(glint, path.point(
                              lambda v: 255 if v > 30 else 0)))
path = path.point(lambda v: int(v * 0.8))
img = Image.composite(Image.new("RGB", (W, H), (255, 206, 146)), img, path)

# a band of mist where the water meets the land
mist = Image.new("L", (W, H), 0)
ImageDraw.Draw(mist).rectangle([0, HORIZON - 26, W, HORIZON + 16], fill=120)
mist = mist.filter(ImageFilter.GaussianBlur(30))
img = Image.composite(Image.new("RGB", (W, H), (208, 150, 116)), img, mist)

# --- settle -----------------------------------------------------------------
img = img.filter(ImageFilter.GaussianBlur(0.8))
img = img.point(lambda v: int(v * 0.92))

vig = Image.new("L", (W, H), 0)
ImageDraw.Draw(vig).ellipse([-W * 0.16, -H * 0.20, W * 1.16, H * 1.20], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(250))
img = Image.composite(img, Image.new("RGB", (W, H), (5, 5, 9)), vig)

img.save(DST, quality=84, method=6)
print("wrote %s %s (%dKB)" % (os.path.relpath(DST, HERE), img.size,
                              os.path.getsize(DST) // 1024))
