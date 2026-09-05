"""Lift the painted irises out of the About crop.

She wanted the two moving eyes to match, and they could not while the drawn
ones sat under them: the crop has one iris 41px across and the other 35px,
each filling its socket nearly edge to edge, so a cover big enough to hide
both had to be lopsided and had nowhere left to travel. This paints both
sockets back to sclera and cuts one iris out to move on top of them.

Where a socket ends is a hand trace, and it has to be. Her lash line and her
iris are both near-black and they touch, so no colour test separates them, and
her sockets are pointed almonds, so no ellipse follows one without either
cutting into the lash or leaving a sliver of old iris behind in the white.
Every rule tried here - warmth, depth from skin, filling inwards from the lid,
filling outwards from the pupil - put one of those two faults on screen.

    python3 tools-blank-eyes.py                    # rewrites the crop
    python3 tools-blank-eyes.py --preview out.png  # before/after strip instead

Reads the untouched crop, so restore it from images/kani-edit.png before
re-running. Writes images/kani-about.webp and images/kani-iris.webp.
"""

import sys
from PIL import Image, ImageDraw, ImageFilter

SRC = "images/kani-about.webp"

# Each socket traced along the inside of her lash line, in crop pixels.
#
# This is a hand trace because nothing automatic could draw it. Her lash and
# her iris are both near-black and they touch, so no colour test separates
# them; and her sockets are pointed almonds, so no ellipse follows one without
# either cutting the lash or leaving a sliver of old iris behind in the white.
# Every version that tried left one fault or the other on screen.
EYES = [
    # her right
    [(699, 475), (703, 468), (708, 464), (713, 462), (718, 462), (723, 463),
     (728, 465), (733, 469), (738, 474), (742, 481), (744, 488), (744, 495),
     (741, 501), (737, 506), (733, 508), (729, 507), (725, 505), (721, 503),
     (717, 500), (713, 497), (709, 493), (705, 489), (702, 484), (699, 480)],
    # her left
    [(774, 529), (777, 523), (781, 518), (786, 514), (791, 512), (796, 511),
     (801, 510), (806, 510), (811, 510), (816, 511), (821, 513), (826, 516),
     (830, 520), (834, 526), (837, 532), (838, 536), (836, 541), (832, 544),
     (827, 546), (822, 547), (817, 547), (812, 546), (807, 545), (802, 544),
     (797, 542), (792, 540), (787, 537), (782, 534), (778, 531)],
]

# Her left iris, which she drew almost fully open - centre and radius in crop
# pixels. Cut out and reused for both eyes, so the pair matches by construction
# and the moving part is her own artwork rather than anything drawn here.
IRIS = (810.5, 527.5, 16.5)
IRIS_OUT = "images/kani-iris.webp"

SCLERA_LIT = (252, 252, 249)
SCLERA_SHADE = (216, 215, 217)      # under the upper lid
SKIN_GAP = 2                        # never paint this close to skin


def is_skin(p):
    """Her lid, cheek and inner corner: warm, and never this far from lit.

    The threshold sits above the lit underside of her iris, which is warm too
    but a good deal darker - painting that as skin is what used to leave a
    blob of the old eye behind.
    """
    r, g, b = p
    return r - b > 40 and r + g + b > 340


def is_sclera(p):
    r, g, b = p
    return r + g + b >= 500 and abs(r - b) < 30


def socket(px, poly, W, H):
    """One traced socket, as {pixel: how much of it to paint}.

    Drawn at 4x and shrunk so the outline antialiases; at this size a hard
    edge against her lash is plainly visible. Skin is still refused outright,
    as a backstop against a mistraced point.
    """
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    x0, y0 = min(xs) - 2, min(ys) - 2
    w, h = max(xs) - x0 + 3, max(ys) - y0 + 3

    Z = 4
    mask = Image.new("L", (w * Z, h * Z), 0)
    ImageDraw.Draw(mask).polygon(
        [((x - x0) * Z + Z // 2, (y - y0) * Z + Z // 2) for x, y in poly],
        fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    # Back off a pixel from the trace. What that leaves is the thin lid line
    # she drew under each eye - in her artwork most of the dark weight along
    # the bottom is the iris itself, so clearing right up to the trace takes
    # the lower lash with it and the eye ends up open to the skin.
    mask = mask.filter(ImageFilter.MinFilter(3))
    mp = mask.load()

    out = {}
    for y in range(h):
        for x in range(w):
            a = mp[x, y]
            if a and not is_skin(px[x0 + x, y0 + y]):
                out[(x0 + x, y0 + y)] = a / 255.0
    return out


def cut_iris(im):
    """Save one of her irises as a disc with a soft edge.

    Has to run before the sockets are painted, or there is nothing left to cut.
    The mask is drawn at 8x and shrunk so the rim antialiases instead of
    stair-stepping - at this size a hard edge is obvious against the sclera.
    """
    cx, cy, r = IRIS
    if sum(im.getpixel((int(cx), int(cy)))) > 300:
        raise SystemExit(
            "the sockets are already painted - this reads the original crop, "
            "so restore it from images/kani-edit.png before running again")
    # cropped tight to the disc, so the element site.css sizes is the iris
    # itself - any transparent margin would eat into how far it can travel
    x0, y0, n = int(cx - r), int(cy - r), int(r * 2)
    disc = im.crop((x0, y0, x0 + n, y0 + n)).convert("RGBA")

    Z = 8
    mask = Image.new("L", (n * Z, n * Z), 0)
    mx, my = (cx - x0) * Z, (cy - y0) * Z
    ImageDraw.Draw(mask).ellipse(
        [mx - r * Z, my - r * Z, mx + r * Z, my + r * Z], fill=255)
    disc.putalpha(mask.resize((n, n), Image.LANCZOS))
    disc.save(IRIS_OUT, "WEBP", quality=95, method=6, lossless=True)
    print("  iris   %s (%d x %d)" % (IRIS_OUT, n, n))


def inscribed(mask, W, H):
    """The largest upright ellipse that fits inside a cleared socket.

    site.css clips the moving iris to this. It has to sit wholly within the
    sclera, because anywhere the clip crosses open white it slices the iris and
    the cut edge reads as a dark arc lying in the eye - which is what a clip
    box left over from an older, differently shaped socket was doing.
    """
    xs = [p[0] for p in mask]
    ys = [p[1] for p in mask]
    cx = (min(xs) + max(xs)) / 2.0
    cy = (min(ys) + max(ys)) / 2.0

    def fits(ox, oy, rx, ry):
        for y in range(int(oy - ry), int(oy + ry) + 1):
            for x in range(int(ox - rx), int(ox + rx) + 1):
                nx, ny = (x - ox) / rx, (y - oy) / ry
                if nx * nx + ny * ny <= 1.0 and (x, y) not in mask:
                    return False
        return True

    best = (0, 0, 0, 0, 0)
    for ox in (cx - 3, cx - 1.5, cx, cx + 1.5, cx + 3):
        for oy in (cy - 3, cy - 1.5, cy, cy + 1.5, cy + 3):
            for ry in range(5, 34):
                rx = 4
                while rx < 40 and fits(ox, oy, rx + 1, ry):
                    rx += 1
                if rx * ry > best[0] and fits(ox, oy, rx, ry):
                    best = (rx * ry, ox, oy, rx, ry)
    _, ox, oy, rx, ry = best
    return ((ox - rx) / W * 100, (oy - ry) / H * 100,
            rx * 2 / W * 100, ry * 2 / H * 100, rx * 2, ry * 2)


def main():
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    px = im.load()

    cut_iris(im)

    holes = set()
    for poly in EYES:
        m = socket(px, poly, W, H)
        xs = [p[0] for p in m]
        ys = [p[1] for p in m]
        top, bot = min(ys), max(ys)
        for (x, y), a in m.items():
            # the top of a socket sits in the lid's shadow, the rest is lit
            t = min(1.0, (y - top) / max(1.0, (bot - top) * 0.45))
            lit = tuple(
                int(SCLERA_SHADE[i] + (SCLERA_LIT[i] - SCLERA_SHADE[i]) * t)
                for i in range(3))
            old = px[x, y]
            px[x, y] = tuple(int(old[i] + (lit[i] - old[i]) * a) for i in range(3))
            if a > 0.5:
                holes.add((x, y))
        print("  socket x %.2f%%..%.2f%%  y %.2f%%..%.2f%%  %dx%d px  (%d painted)"
              % (min(xs) / W * 100, max(xs) / W * 100, top / H * 100, bot / H * 100,
                 max(xs) - min(xs) + 1, bot - top + 1, len(m)))
        print("         css: left %.2f%%; top %.2f%%; width %.2f%%; height %.2f%%;"
              "   (%dx%d px)" % inscribed(set(m), W, H))

    # take the hard edge off the seam, inside the sockets only
    soft = im.filter(ImageFilter.GaussianBlur(0.7))
    sp = soft.load()
    for p in holes:
        px[p] = sp[p]

    if "--preview" in sys.argv:
        before = Image.open(SRC).convert("RGB")
        box = (int(W * 0.63), int(H * 0.68), int(W * 0.83), int(H * 0.90))
        t = [i.crop(box) for i in (before, im)]
        t = [i.resize((i.width * 4, i.height * 4), Image.LANCZOS) for i in t]
        out = Image.new("RGB", (t[0].width * 2 + 14, t[0].height), (25, 25, 25))
        out.paste(t[0], (0, 0))
        out.paste(t[1], (t[0].width + 14, 0))
        out.save(sys.argv[sys.argv.index("--preview") + 1])
        print("preview written")
        return

    im.save(SRC, "WEBP", quality=92, method=6)
    print("wrote %s (%d x %d)" % (SRC, W, H))


if __name__ == "__main__":
    main()
