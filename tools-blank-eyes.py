"""Lift the painted irises out of the About crop.

She wanted the two moving eyes to match, and they could not while the drawn
ones sat under them: the crop has one iris 43px tall and the other 35px, each
filling its socket nearly edge to edge, so a cover big enough to hide both had
to be lopsided and had nowhere left to travel. This paints both sockets back
to sclera, leaving her lashes and lids as drawn, and site.css puts a matched
pair on top.

    python3 tools-blank-eyes.py                    # rewrites the crop
    python3 tools-blank-eyes.py --preview out.png  # before/after strip instead

The crop itself can be remade from images/kani-edit.png if this needs redoing.
"""

import sys
from PIL import Image, ImageFilter

SRC = "images/kani-about.webp"

# Each iris, measured off the artwork: centre and radii as fractions of the
# crop. Tight to the iris - drawn any larger and the fill eats her lash line,
# which curls over the top of both sockets.
EYES = [(0.68840, 0.76220, 0.01790, 0.03360),   # her right
        (0.77440, 0.83530, 0.01900, 0.02970)]   # her left

SCLERA_LIT = (252, 252, 249)
SCLERA_SHADE = (206, 204, 201)      # under the upper lid


def main():
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    px = im.load()

    holes = set()
    for cx, cy, rx, ry in EYES:
        x0, x1 = int((cx - rx) * W) - 1, int((cx + rx) * W) + 2
        y0, y1 = int((cy - ry) * H) - 1, int((cy + ry) * H) + 2
        for y in range(y0, y1):
            for x in range(x0, x1):
                nx = (x - cx * W) / (rx * W)
                ny = (y - cy * H) / (ry * H)
                d = nx * nx + ny * ny
                if d > 1.0:
                    continue
                # top of the socket sits in the lid's shadow, the rest is lit
                t = min(1.0, max(0.0, (ny + 1.0) / 0.9))
                col = tuple(int(SCLERA_SHADE[i] + (SCLERA_LIT[i] - SCLERA_SHADE[i]) * t)
                            for i in range(3))
                # feather the last of the ellipse so the seam is not a hard line
                a = min(1.0, (1.0 - d) / 0.14)
                old = px[x, y]
                px[x, y] = tuple(int(old[i] + (col[i] - old[i]) * a)
                                 for i in range(3))
                holes.add((x, y))
        print("  erased x %.2f%%..%.2f%%  y %.2f%%..%.2f%%  %dx%d px"
              % ((cx - rx) * 100, (cx + rx) * 100, (cy - ry) * 100, (cy + ry) * 100,
                 int(rx * 2 * W), int(ry * 2 * H)))

    soft = im.filter(ImageFilter.GaussianBlur(0.8))
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
