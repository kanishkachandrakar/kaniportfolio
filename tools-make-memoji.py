"""Turn her pasted Memoji into the avatar the top bar wears.

The file she saved is a screenshot, so the Memoji sits on a flat dark card
rather than on transparency, and it is off-centre in a rectangle. Dropped into
a 46px circle as-is it would show a dark disc and crop the thumbs-up.

Two things happen here. The card is keyed out - it is exactly (30, 30, 30)
across 50k pixels, and her hair, though nearly as dark, is textured and never
lands on that value over a run reaching the border, so a flood fill from the
edge takes the background and leaves her alone. Then the result is cropped
square around what remains, which is what lets object-fit leave the figure
whole instead of cutting the thumb off.

    python3 tools-make-memoji.py

Reads images/kani-memoji.png, writes images/kani-memoji.webp.
"""

from PIL import Image, ImageFilter

SRC = "images/kani-memoji.png"
OUT = "images/kani-memoji.webp"
TOL = 3        # how far off the card colour still counts as card
PAD = 1        # breathing room around the figure, in source pixels
DROP = 18      # extra headroom above her, so the circle clears her hair


def main():
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    px = im.load()
    card = px[2, 2]

    def is_card(p):
        return max(abs(p[i] - card[i]) for i in range(3)) <= TOL

    # Flood in from the border. Reaching the border is the test - an interior
    # pixel that happens to match the card colour is part of her, and stays.
    seen = set()
    stack = [(x, y) for x in range(W) for y in (0, H - 1) if is_card(px[x, y])]
    stack += [(x, y) for y in range(H) for x in (0, W - 1) if is_card(px[x, y])]
    seen.update(stack)
    while stack:
        a, b = stack.pop()
        for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (a + da, b + db)
            if (0 <= n[0] < W and 0 <= n[1] < H and n not in seen
                    and is_card(px[n])):
                seen.add(n)
                stack.append(n)

    alpha = Image.new("L", (W, H), 255)
    ap = alpha.load()
    for p in seen:
        ap[p] = 0
    # soften the cut so the edge does not stair-step at small sizes
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))

    out = im.convert("RGBA")
    out.putalpha(alpha)

    x0, y0, x1, y1 = out.getbbox()
    cx = (x0 + x1) / 2.0

    # Square, so a circular crop keeps the whole figure rather than a slice.
    # The extra room all goes above her: centred, the circle cut across the top
    # of her hair, because a circle inscribed in a square only reaches the edge
    # at the four midpoints and takes the corners off everything else.
    side = max(x1 - x0, y1 - y0) + 2 * PAD + DROP
    top = y0 - PAD - DROP
    left = cx - side / 2.0
    # crop() pads with transparency where it runs past the source
    sq = out.crop((int(left), int(top), int(left + side), int(top + side)))
    sq = sq.resize((256, 256), Image.LANCZOS)
    sq.save(OUT, "WEBP", quality=92, method=6)
    print("kept %d px of card out of %d" % (len(seen), W * H))
    print("figure x %d..%d y %d..%d -> %s (%dx%d)"
          % (x0, x1, y0, y1, OUT, sq.width, sq.height))


if __name__ == "__main__":
    main()
