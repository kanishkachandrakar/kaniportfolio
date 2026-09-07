# -*- coding: utf-8 -*-
"""Paint the scene the glass card floats on: a lake under a mountain range.

Generated rather than photographed, so the site carries no stock imagery.
One composition, painted twice, because the site has two themes and a
backdrop has to belong to the one it sits under. Dusk is the original -
amber at the horizon, indigo overhead. Overcast is its muted counterpart
in oat, stone and sage, kept well below full brightness: the light card is
translucent, so anything bright behind it burns through the blur, and
anything dark turns the panel grey.

Everything that differs between them is a colour, so the palettes are data
and the painting below is shared.

Run: python3 tools-make-backdrop.py
  -> images/scene.webp (dark theme), images/scene-light.webp (light)
"""
import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1200
HORIZON = int(H * 0.615)
random.seed(11)


def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_colour(t, P):
    """t: 0 at the top of the sky, 1 at the horizon."""
    stops = P["sky"]
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0))
    return stops[-1][1]



DUSK = dict(
    stars=True,
    sky=[(0.00, (11, 16, 42)), (0.34, (39, 30, 63)), (0.62, (96, 54, 66)),
         (0.84, (176, 96, 62)), (1.00, (226, 152, 78))],
    spread=(198, 112, 66), spread_a=120,
    sun=(255, 214, 150), ray=(255, 208, 152), ray_a=(26, 54),
    cloud_lit=(238, 176, 116, 150),
    cloud_lo=(60, 48, 78), cloud_hi=(150, 92, 78), cloud_a=110,
    ranges=[(74, 60, 92), (49, 39, 64), (30, 24, 41), (17, 14, 24)],
    rim=(228, 158, 104, 120), haze=(150, 96, 92),
    water=lambda v: int(v * 0.62),
    ripple=(6, 8, 18), ripple_a=(52, 70), ripple_blur=1.8,
    path=(255, 206, 146), mist=(208, 150, 116),
    shore=(6, 6, 11), shore_rim=(150, 104, 84, 90),
    bird=(24, 22, 34), gain=0.92, vig=(5, 5, 9),
)

# No stars - the sky never gets dark enough for one. The ripples also need
# their alpha cut and their blur raised: at dusk contrast those lines read as
# water, at this contrast the same lines read as stripes.
OVERCAST = dict(
    stars=False,
    sky=[(0.00, (188, 194, 200)), (0.34, (206, 208, 204)),
         (0.62, (222, 218, 206)), (0.84, (232, 226, 210)),
         (1.00, (240, 235, 220))],
    spread=(236, 226, 204), spread_a=80,
    sun=(250, 246, 236), ray=(245, 242, 232), ray_a=(10, 20),
    cloud_lit=(240, 236, 224, 110),
    cloud_lo=(186, 190, 190), cloud_hi=(214, 210, 198), cloud_a=88,
    ranges=[(196, 200, 198), (176, 184, 182), (156, 168, 162), (136, 152, 146)],
    rim=(246, 244, 234, 120), haze=(232, 228, 214),
    water=lambda v: int(200 + (v - 200) * 0.78),
    ripple=(120, 124, 118), ripple_a=(10, 20), ripple_blur=3.2,
    path=(250, 248, 238), mist=(240, 236, 224),
    shore=(120, 134, 126), shore_rim=(240, 238, 228, 110),
    bird=(128, 132, 126), gain=1.0, vig=(238, 236, 226),
)

SCENES = [("scene.webp", DUSK), ("scene-light.webp", OVERCAST)]


def paint(P):
    """One scene, in the palette given."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(HORIZON):
        d.line([(0, y), (W, y)], fill=sky_colour(y / float(HORIZON), P))

    # the sun's warmth bleeding sideways along the horizon
    spread = Image.new("L", (W, H), 0)
    ImageDraw.Draw(spread).ellipse([-W * 0.35, HORIZON - H * 0.30,
                                    W * 1.35, HORIZON + H * 0.06], fill=P["spread_a"])
    spread = spread.filter(ImageFilter.GaussianBlur(150))
    img = Image.composite(Image.new("RGB", (W, H), P["spread"]), img, spread)

    # --- stars, only where the sky is still dark ------------------------------
    for _ in range(260 if P["stars"] else 0):
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
    img = Image.composite(Image.new("RGB", (W, H), P["sun"]), img, sun)

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
                    fill=random.randint(*P["ray_a"]))
    rays = rays.filter(ImageFilter.GaussianBlur(34))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle([0, 0, W, HORIZON], fill=255)
    rays = ImageChops.multiply(rays, mask.filter(ImageFilter.GaussianBlur(20)))
    img = Image.composite(Image.new("RGB", (W, H), P["ray"]), img, rays)

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
        col = (P["cloud_lit"] if lit
               else lerp(P["cloud_lo"], P["cloud_hi"], t) + (P["cloud_a"],))
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
    RANGES = [(HORIZON - H * 0.205, 160, P["ranges"][0], 4),
              (HORIZON - H * 0.145, 130, P["ranges"][1], 9),
              (HORIZON - H * 0.088, 100, P["ranges"][2], 17),
              (HORIZON - H * 0.038, 62, P["ranges"][3], 23)]
    for base_y, rough, colour, seed in RANGES:
        ys = ridge(base_y, rough, seed)
        step = W / float(len(ys) - 1)
        poly = [(i * step, y) for i, y in enumerate(ys)]
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.polygon(poly + [(W, HORIZON + 4), (0, HORIZON + 4)], fill=colour + (255,))
        # a rim of light on the slopes facing the sun
        ld.line(poly, fill=P["rim"], width=3)
        layer = layer.filter(ImageFilter.GaussianBlur(1.2))
        img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

    # haze settling between the ranges
    haze = Image.new("L", (W, H), 0)
    ImageDraw.Draw(haze).rectangle([0, HORIZON - H * 0.20, W, HORIZON], fill=90)
    haze = haze.filter(ImageFilter.GaussianBlur(70))
    img = Image.composite(Image.new("RGB", (W, H), P["haze"]), img, haze)

    # --- the lake: the sky again, upside down and disturbed -------------------
    water = img.crop((0, int(HORIZON - (H - HORIZON)), W, HORIZON)).transpose(
        Image.FLIP_TOP_BOTTOM).resize((W, H - HORIZON))
    water = water.point(P["water"])
    water = water.filter(ImageFilter.GaussianBlur(3.0))
    img.paste(water, (0, HORIZON))

    ripple = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ripple)
    y = HORIZON + 2
    gap = 3.0
    while y < H:
        a = int(P["ripple_a"][0] + P["ripple_a"][1]
                * ((y - HORIZON) / float(H - HORIZON)))
        rd.line([(0, y), (W, y)], fill=P["ripple"] + (a,), width=1)
        y += gap
        gap *= 1.035
    ripple = ripple.filter(ImageFilter.GaussianBlur(P["ripple_blur"]))
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
    img = Image.composite(Image.new("RGB", (W, H), P["path"]), img, path)

    # a band of mist where the water meets the land
    mist = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mist).rectangle([0, HORIZON - 26, W, HORIZON + 16], fill=120)
    mist = mist.filter(ImageFilter.GaussianBlur(30))
    img = Image.composite(Image.new("RGB", (W, H), P["mist"]), img, mist)

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
                    fill=P["shore"] + (255,))
        shd.line(pts, fill=P["shore_rim"], width=3)
    shore = shore.filter(ImageFilter.GaussianBlur(1.6))
    img = Image.alpha_composite(img.convert("RGBA"), shore).convert("RGB")

    # --- birds, for scale ------------------------------------------------------
    bd2 = ImageDraw.Draw(img)
    for bx, by, sc in ((W * 0.20, H * 0.19, 1.0), (W * 0.245, H * 0.155, 0.8),
                       (W * 0.285, H * 0.205, 0.7), (W * 0.83, H * 0.14, 0.85),
                       (W * 0.875, H * 0.175, 0.65)):
        w2, h2 = 13 * sc, 5 * sc
        bd2.line([(bx - w2, by), (bx - w2 * 0.35, by - h2), (bx, by - h2 * 0.25)],
                 fill=P["bird"], width=max(1, int(2 * sc)))
        bd2.line([(bx, by - h2 * 0.25), (bx + w2 * 0.35, by - h2), (bx + w2, by)],
                 fill=P["bird"], width=max(1, int(2 * sc)))

    # --- settle -----------------------------------------------------------------
    img = img.filter(ImageFilter.GaussianBlur(0.8))
    # Dither the long sky gradient so it does not band on a wide screen.
    # effect_noise centres on 128, so subtract that back off rather than
    # adding a flat +128 to every channel.
    grain = Image.effect_noise((W, H), 3).convert("L")
    img = ImageChops.add(img, Image.merge("RGB", (grain, grain, grain)),
                         scale=1, offset=-128)
    img = img.point(lambda v: min(255, int(v * P["gain"])))

    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-W * 0.16, -H * 0.20, W * 1.16, H * 1.20], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(250))
    img = Image.composite(img, Image.new("RGB", (W, H), P["vig"]), vig)
    return img


for _name, _P in SCENES:
    random.seed(11)          # same mountains and clouds in both
    _dst = os.path.join(HERE, "images", _name)
    _img = paint(_P)
    _img.save(_dst, quality=88, method=6)
    print("wrote %s %s (%dKB)" % (os.path.relpath(_dst, HERE), _img.size,
                                  os.path.getsize(_dst) // 1024))
