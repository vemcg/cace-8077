"""Crop/letterbox assets/images/originals/*.jpg into assets/images/*.jpg at
1600x900, in natural color -- no recoloring. Legibility over these photos is
handled entirely by the white overlay in assets/css/style.css
(.reveal .slides section::before), not by anything baked into the image.

Usage:
    python scripts/process_backgrounds.py                 # all images
    python scripts/process_backgrounds.py wright-flyer     # just one
"""

import os
import sys
from PIL import Image, ImageFilter

SRC = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "originals")
DST = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

CANVAS_W, CANVAS_H = 1600, 900

# name -> crop mode ("crop" center-crops to fill the frame; "contain" scales
# to fit height and fills the sides with a blurred edge-extension, for the
# tall/square shots where cropping would cut off the subject).
IMAGES = {
    "wright-flyer": "crop",
    "spirit-of-st-louis": "crop",
    "curtiss-jenny": "crop",
    "p51-mustang": "crop",
    "f86-sabre": "crop",
    "f100-super-sabre": "crop",
    "apollo-capsule": "contain",
    "gemini-capsule": "crop",
    "moon-landing": "contain",
}


def center_crop_to_canvas(img):
    w, h = img.size
    target_ratio = CANVAS_W / CANVAS_H
    ratio = w / h
    if ratio > target_ratio:
        new_w = round(h * target_ratio)
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:
        new_h = round(w / target_ratio)
        top = (h - new_h) // 2
        box = (0, top, w, top + new_h)
    cropped = img.crop(box)
    return cropped.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)


def contain_with_edge_fill(img):
    w, h = img.size
    scale = CANVAS_H / h
    new_w = round(w * scale)
    resized = img.resize((new_w, CANVAS_H), Image.LANCZOS)

    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H))
    x_offset = (CANVAS_W - new_w) // 2

    if x_offset > 0:
        sample_w = max(40, round(new_w * 0.08))
        blur_radius = 60

        left_source = resized.crop((0, 0, sample_w, CANVAS_H))
        left_source = left_source.filter(ImageFilter.GaussianBlur(blur_radius))
        left_strip = left_source.resize((x_offset, CANVAS_H), Image.LANCZOS)

        right_source = resized.crop((new_w - sample_w, 0, new_w, CANVAS_H))
        right_source = right_source.filter(ImageFilter.GaussianBlur(blur_radius))
        right_strip = right_source.resize((CANVAS_W - new_w - x_offset, CANVAS_H), Image.LANCZOS)

        canvas.paste(left_strip, (0, 0))
        canvas.paste(right_strip, (x_offset + new_w, 0))

    canvas.paste(resized, (x_offset, 0))
    return canvas


def main():
    if len(sys.argv) > 1:
        requested = sys.argv[1:]
        unknown = [n for n in requested if n not in IMAGES]
        if unknown:
            print(f"Unknown image name(s): {unknown}. Valid: {sorted(IMAGES)}")
            sys.exit(1)
        targets = requested
    else:
        targets = list(IMAGES)

    for name in targets:
        mode = IMAGES[name]
        src_path = os.path.join(SRC, f"{name}.jpg")
        img = Image.open(src_path).convert("RGB")

        if mode == "crop":
            framed = center_crop_to_canvas(img)
        else:
            framed = contain_with_edge_fill(img)

        dst_path = os.path.join(DST, f"{name}.jpg")
        framed.save(dst_path, "JPEG", quality=90, optimize=True)
        print(f"{name}: {mode} -> {dst_path}")


if __name__ == "__main__":
    main()
