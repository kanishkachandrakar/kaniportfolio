"""Cut the round hero portrait out of images/profile-option.JPG.

The circle is 1:1 and the photograph is 3:4 with her standing off to the
right, so object-fit alone could not do it: with cover, a portrait image
fills the box's width and is only cropped vertically, which would have left
her against the right edge of the circle rather than in it.

So the square is cut here. Her face centres at 73.5% across the frame, and
the frame ends at 92%, which is what sets the size: the widest square that
still has her in the middle of it reaches the right edge of the photograph
and is 508px. Her face sits at 40% of the way down it rather than halfway,
which leaves room for her shoulders underneath - centring the face vertically
puts the crop's bottom edge at her collar.

    python3 tools-make-portrait.py  ->  images/kani-portrait.webp
"""

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "images", "profile-option.JPG")
DST = os.path.join(HERE, "images", "kani-portrait.webp")

FACE_X = 0.735      # where her face sits in the frame
FACE_Y = 0.490
FACE_DOWN = 0.40    # and where it should sit in the crop


def main():
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    cx, cy = FACE_X * W, FACE_Y * H

    # the widest square that keeps her centred and stays inside the frame
    side = int(min(cx, W - cx) * 2)
    left = int(cx - side / 2)
    top = int(cy - side * FACE_DOWN)
    top = max(0, min(top, H - side))

    out = im.crop((left, top, left + side, top + side))
    out.save(DST, "WEBP", quality=88, method=6)
    print("cut %dx%d from (%d, %d) -> %s (%dKB)"
          % (side, side, left, top, os.path.relpath(DST, HERE),
             os.path.getsize(DST) // 1024))
    print("   her face lands at %.0f%% across, %.0f%% down the crop"
          % ((cx - left) / side * 100, (cy - top) / side * 100))


if __name__ == "__main__":
    main()
