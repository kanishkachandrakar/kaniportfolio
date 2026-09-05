"""Lift the painted irises out of the About crop.

She wanted the two moving eyes to match, and they could not while the drawn
ones sat under them: the crop has one iris 43px tall and the other 35px, each
filling its socket nearly edge to edge, so a cover big enough to hide both had
to be lopsided and had nowhere left to travel. This paints both sockets back
to sclera and site.css puts a matched pair on top.

Nothing here is filled on colour alone, because none of it separates cleanly:
her pupil is as dark as her lash line, and the lit underside of her iris is
the same warm brown as the shadow on her lid. So the fill goes by distance
from skin as well - the lash hugs her lid, the pupil sits deep inside - and
leaves an unpainted gap next to skin no matter what, which is what keeps the
white from ever bleeding onto a lid or a cheek.

    python3 tools-blank-eyes.py                    # rewrites the crop
    python3 tools-blank-eyes.py --preview out.png  # before/after strip instead

The crop itself can be remade from images/kani-edit.png if this needs redoing.
"""

import sys
from PIL import Image, ImageDraw, ImageFilter

SRC = "images/kani-about.webp"

# Where to look for each socket: centre and radii as fractions of the crop,
# hugging the eye she drew. Only the colour tests below decide what is actually
# painted, but this keeps the search off her lid shadow, which is the one thing
# that reads the same as the lit underside of an iris.
EYES = [(0.68830, 0.76120, 0.02150, 0.03870),   # her right
        (0.77410, 0.82990, 0.02250, 0.03330)]   # her left

# Her left iris, which she drew almost fully open - centre and radius in crop
# pixels. Cut out and reused for both eyes, so the pair matches by construction
# and the moving part is her own artwork rather than anything drawn here.
IRIS = (810.5, 527.5, 16.5)
IRIS_OUT = "images/kani-iris.webp"

SCLERA_LIT = (252, 252, 249)
SCLERA_SHADE = (216, 215, 217)      # under the upper lid
LASH_REACH = 8                      # how thick her lash line runs, in px
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


def socket(px, cx, cy, rx, ry, W, H):
    """The inside of one eye, as a set of pixels.

    Sclera goes by colour. The iris cannot, because it darkens to black at the
    pupil and meets a lash line that is black as well - so those two are told
    apart by where they sit: the lash hugs her lid and is never more than a few
    pixels from skin, while the pupil sits deep in the socket. Along her lower
    lid there is no lash at all, only iris meeting cheek, so warmth decides
    there instead; her lash stays neutral even at its darkest.
    """
    pad = 14
    x0, x1 = int((cx - rx) * W) - pad, int((cx + rx) * W) + pad
    y0, y1 = int((cy - ry) * H) - pad, int((cy + ry) * H) + pad

    dist, stack, head = {}, [], 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if is_skin(px[x, y]):
                dist[(x, y)] = 0
                stack.append((x, y))
    while head < len(stack):
        a, b = stack[head]
        head += 1
        if dist[(a, b)] > LASH_REACH:
            continue
        for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (a + da, b + db)
            if x0 <= n[0] < x1 and y0 <= n[1] < y1 and n not in dist:
                dist[n] = dist[(a, b)] + 1
                stack.append(n)

    fill, inside = set(), set()
    for y in range(y0, y1):
        for x in range(x0, x1):
            nx = (x - cx * W) / (rx * W)
            ny = (y - cy * H) / (ry * H)
            if nx * nx + ny * ny > 1.0:
                continue
            p = px[x, y]
            if is_skin(p):
                continue
            inside.add((x, y))
            d = dist.get((x, y), 99)
            if d <= SKIN_GAP:
                continue        # her lid's own edge, whatever colour it is
            near = d <= LASH_REACH
            if is_sclera(p) or not near or p[0] - p[2] >= 26:
                fill.add((x, y))

    # What that spared is either lash, which runs off the edge of the search
    # area, or a last scrap of pupil ringed by sclera. Walk in from the rim:
    # what the walk reaches is lash and stays, the rest is eye.
    rest = inside - fill
    stack = [q for q in rest
             if any((q[0] + a, q[1] + b) not in inside
                    for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    lash = set(stack)
    while stack:
        a, b = stack.pop()
        for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (a + da, b + db)
            if n in rest and n not in lash:
                lash.add(n)
                stack.append(n)
    return fill | (rest - lash)


def inscribed(mask, W, H):
    """The largest ellipse that fits in a socket, as a CSS box.

    site.css puts the moving iris inside this, so it has to be clear of her
    lashes at every angle - hence a fit rather than a bounding box.
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
    for ox in (cx - 2, cx - 1, cx, cx + 1, cx + 2):
        for oy in (cy - 2, cy - 1, cy, cy + 1, cy + 2):
            for ry in range(6, 40):
                rx = 4
                while rx < 40 and fits(ox, oy, rx + 1, ry):
                    rx += 1
                if not fits(ox, oy, rx, ry):
                    continue
                if rx * ry > best[0]:
                    best = (rx * ry, ox, oy, rx, ry)
    _, ox, oy, rx, ry = best
    return ((ox - rx) / W * 100, (oy - ry) / H * 100,
            rx * 2 / W * 100, ry * 2 / H * 100, rx * 2, ry * 2)


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
    for cx, cy, rx, ry in EYES:
        m = socket(px, cx, cy, rx, ry, W, H)
        xs = [p[0] for p in m]
        ys = [p[1] for p in m]
        top, bot = min(ys), max(ys)
        for x, y in m:
            # the top of a socket sits in the lid's shadow, the rest is lit
            t = min(1.0, (y - top) / max(1.0, (bot - top) * 0.45))
            px[x, y] = tuple(
                int(SCLERA_SHADE[i] + (SCLERA_LIT[i] - SCLERA_SHADE[i]) * t)
                for i in range(3))
        print("  socket x %.2f%%..%.2f%%  y %.2f%%..%.2f%%  %dx%d px  (%d filled)"
              % (min(xs) / W * 100, max(xs) / W * 100, top / H * 100, bot / H * 100,
                 max(xs) - min(xs) + 1, bot - top + 1, len(m)))
        print("         css: left %.2f%% top %.2f%% width %.2f%% height %.2f%%"
              " (%dx%d px)" % inscribed(m, W, H))
        holes |= m

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
