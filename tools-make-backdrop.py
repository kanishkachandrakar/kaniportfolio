# -*- coding: utf-8 -*-
"""Paint the scene the glass card floats on: first light over a still lake.

Generated rather than photographed, so the site carries no stock imagery.
The palette is pastel throughout - lilac overhead, blush and peach at the
horizon, ranges receding through lilac into soft teal. Everything is kept
light and low in contrast on purpose: the card is white frosted glass, so
any real darkness behind it shows through and turns the panel grey.

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
    stops = [(0.00, (214, 206, 242)), (0.34, (232, 214, 242)),
             (0.62, (248, 220, 226)), (0.84, (253, 228, 210)),
             (1.00, (255, 242, 228))]
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

# the sun's warmth bleeding sideways along the horizon
spread = Image.new("L", (W, H), 0)
ImageDraw.Draw(spread).ellipse([-W * 0.35, HORIZON - H * 0.30,
                                W * 1.35, HORIZON + H * 0.06], fill=96)
spread = spread.filter(ImageFilter.GaussianBlur(150))
img = Image.composite(Image.new("RGB", (W, H), (255, 226, 204)), img, spread)

# --- the sun, low and hazy ------------------------------------------------
SUNX, SUNY = W * 0.655, HORIZON - H * 0.235
sun = Image.new("L", (W, H), 0)
sd = ImageDraw.Draw(sun)
for r, v in ((360, 44), (210, 82), (110, 148), (42, 255)):
    sd.ellipse([SUNX - r, SUNY - r * 0.92, SUNX + r, SUNY + r * 0.92], fill=v)
sun = sun.filter(ImageFilter.GaussianBlur(48))
img = Image.composite(Image.new("RGB", (W, H), (255, 250, 240)), img, sun)

# --- rays fanning out of the sun ------------------------------------------
rays = Image.new("L", (W, H), 0)
ryd = ImageDraw.Draw(rays)
for k in range(11):
    ang = math.radians(-118 + k * 13 + random.uniform(-3, 3))
    spread_a = math.radians(random.uniform(1.1, 3.0))
    far = H * 1.5
    ryd.polygon([(SUNX, SUNY),
                 (SUNX + far * math.cos(ang - spread_a),
                  SUNY + far * math.sin(ang - spread_a)),
                 (SUNX + far * math.cos(ang + spread_a),
                  SUNY + far * math.sin(ang + spread_a))],
                fill=random.randint(12, 26))
rays = rays.filter(ImageFilter.GaussianBlur(34))
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).rectangle([0, 0, W, HORIZON], fill=255)
rays = ImageChops.multiply(rays, mask.filter(ImageFilter.GaussianBlur(20)))
img = Image.composite(Image.new("RGB", (W, H), (255, 246, 234)), img, rays)

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
    col = ((255, 238, 228, 132) if lit
           else lerp((208, 200, 234), (248, 218, 218), t) + (96,))
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
RANGES = [(HORIZON - H * 0.205, 160, (206, 198, 234), 4),
          (HORIZON - H * 0.145, 130, (184, 190, 226), 9),
          (HORIZON - H * 0.088, 100, (158, 192, 210), 17),
          (HORIZON - H * 0.038, 62, (136, 186, 194), 23)]
for base_y, rough, colour, seed in RANGES:
    ys = ridge(base_y, rough, seed)
    step = W / float(len(ys) - 1)
    poly = [(i * step, y) for i, y in enumerate(ys)]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.polygon(poly + [(W, HORIZON + 4), (0, HORIZON + 4)], fill=colour + (255,))
    # a rim of light on the slopes facing the sun
    ld.line(poly, fill=(255, 248, 240, 140), width=3)
    layer = layer.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

# haze settling between the ranges
haze = Image.new("L", (W, H), 0)
ImageDraw.Draw(haze).rectangle([0, HORIZON - H * 0.20, W, HORIZON], fill=90)
haze = haze.filter(ImageFilter.GaussianBlur(70))
img = Image.composite(Image.new("RGB", (W, H), (252, 234, 230)), img, haze)

# --- the lake: the sky again, upside down and disturbed -------------------
water = img.crop((0, int(HORIZON - (H - HORIZON)), W, HORIZON)).transpose(
    Image.FLIP_TOP_BOTTOM).resize((W, H - HORIZON))
water = water.point(lambda v: int(212 + (v - 212) * 0.72))
water = water.filter(ImageFilter.GaussianBlur(3.0))
img.paste(water, (0, HORIZON))

ripple = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(ripple)
y = HORIZON + 2
gap = 3.0
while y < H:
    a = int(12 + 22 * ((y - HORIZON) / float(H - HORIZON)))
    rd.line([(0, y), (W, y)], fill=(150, 146, 186, a), width=1)
    y += gap
    gap *= 1.035
# a heavier blur than the dark version needed: at this contrast the lines
# read as stripes rather than as water
ripple = ripple.filter(ImageFilter.GaussianBlur(3.2))
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
img = Image.composite(Image.new("RGB", (W, H), (255, 252, 244)), img, path)

# a band of mist where the water meets the land
mist = Image.new("L", (W, H), 0)
ImageDraw.Draw(mist).rectangle([0, HORIZON - 26, W, HORIZON + 16], fill=120)
mist = mist.filter(ImageFilter.GaussianBlur(30))
img = Image.composite(Image.new("RGB", (W, H), (255, 246, 240)), img, mist)

# --- headlands framing the lower corners ----------------------------------
shore = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shd = ImageDraw.Draw(shore)
for side in (0, 1):
    rnd = random.Random(41 + side)
    pts = []
    for i in range(13):
        t = i / 12.0
        x = (-W * 0.06 + t * W * 0.46) if side == 0 else (W * 1.06 - t * W * 0.46)
        y = H * (0.86 + 0.16 * t) - rnd.uniform(0, H * 0.10) * (1 - t)
        pts.append((x, y))
    shd.polygon(pts + [(pts[-1][0], H + 40), (pts[0][0], H + 40)],
                fill=(126, 168, 176, 255))
    shd.line(pts, fill=(255, 250, 244, 120), width=3)
shore = shore.filter(ImageFilter.GaussianBlur(1.6))
img = Image.alpha_composite(img.convert("RGBA"), shore).convert("RGB")

# --- birds, for scale ------------------------------------------------------
bd2 = ImageDraw.Draw(img)
for bx, by, sc in ((W * 0.20, H * 0.19, 1.0), (W * 0.245, H * 0.155, 0.8),
                   (W * 0.285, H * 0.205, 0.7), (W * 0.83, H * 0.14, 0.85),
                   (W * 0.875, H * 0.175, 0.65)):
    w2, h2 = 13 * sc, 5 * sc
    bd2.line([(bx - w2, by), (bx - w2 * 0.35, by - h2), (bx, by - h2 * 0.25)],
             fill=(150, 142, 178), width=max(1, int(2 * sc)))
    bd2.line([(bx, by - h2 * 0.25), (bx + w2 * 0.35, by - h2), (bx + w2, by)],
             fill=(150, 142, 178), width=max(1, int(2 * sc)))

# --- settle -----------------------------------------------------------------
img = img.filter(ImageFilter.GaussianBlur(0.8))
# Dither the long sky gradient so it does not band on a wide screen.
# effect_noise centres on 128, so subtract that back off rather than
# adding a flat +128 to every channel.
grain = Image.effect_noise((W, H), 3).convert("L")
img = ImageChops.add(img, Image.merge("RGB", (grain, grain, grain)),
                     scale=1, offset=-128)
img = img.point(lambda v: min(255, int(v * 1.02)))

vig = Image.new("L", (W, H), 0)
ImageDraw.Draw(vig).ellipse([-W * 0.16, -H * 0.20, W * 1.16, H * 1.20], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(250))
img = Image.composite(img, Image.new("RGB", (W, H), (250, 244, 250)), vig)

img.save(DST, quality=88, method=6)
print("wrote %s %s (%dKB)" % (os.path.relpath(DST, HERE), img.size,
                              os.path.getsize(DST) // 1024))
