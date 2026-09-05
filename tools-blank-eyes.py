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
    [(699, 476), (703, 471), (707, 468), (711, 466), (715, 464), (719, 463),
     (723, 463), (727, 464), (731, 466), (735, 469), (739, 474), (742, 480),
     (743, 486), (743, 492), (741, 499), (738, 504), (734, 506), (730, 505),
     (726, 503), (722, 501), (718, 498), (714, 494), (710, 489), (706, 484),
     (702, 479)],
    # her left
    [(772, 529), (775, 523), (779, 518), (784, 514), (789, 512), (794, 510),
     (799, 509), (804, 509), (809, 509), (814, 510), (819, 512), (824, 515),
     (829, 519), (833, 525), (837, 532), (838, 535), (835, 540), (831, 543),
     (826, 545), (821, 545), (816, 545), (811, 544), (806, 543), (801, 541),
     (796, 539), (791, 536), (786, 534), (781, 531), (776, 529)],
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
