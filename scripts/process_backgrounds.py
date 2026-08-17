import os
from PIL import Image, ImageFilter

SRC = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "originals")
DST = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

CANVAS_W, CANVAS_H = 1600, 900

# name -> (group, mode)
IMAGES = {
    "wright-flyer": ("sepia", "crop"),
    "curtiss-jenny": ("sepia", "crop"),
    "p51-mustang": ("blue", "crop"),
    "f86-sabre": ("blue", "crop"),
    "f100-super-sabre": ("blue", "crop"),
    "apollo-capsule": ("gray", "contain"),
    "gemini-capsule": ("gray", "crop"),
    "moon-landing": ("gray", "contain"),
}

DUOTONE = {
    "sepia": ((140, 110, 80), (250, 244, 230)),
    "blue": ((120, 140, 165), (246, 250, 253)),
    "gray": ((150, 150, 148), (248, 248, 246)),
}


def build_lut(shadow, highlight):
    luts = []
    for c in range(3):
        lut = [round(shadow[c] + (highlight[c] - shadow[c]) * (i / 255)) for i in range(256)]
        luts.append(lut)
    return luts


def apply_duotone(img, group):
    shadow, highlight = DUOTONE[group]
    luts = build_lut(shadow, highlight)
    gray = img.convert("L")
    r = gray.point(luts[0])
    g = gray.point(luts[1])
    b = gray.point(luts[2])
    return Image.merge("RGB", (r, g, b))


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
    for name, (group, mode) in IMAGES.items():
        src_path = os.path.join(SRC, f"{name}.jpg")
        img = Image.open(src_path).convert("RGB")

        if mode == "crop":
            framed = center_crop_to_canvas(img)
        else:
            framed = contain_with_edge_fill(img)

        toned = apply_duotone(framed, group)

        dst_path = os.path.join(DST, f"{name}.jpg")
        toned.save(dst_path, "JPEG", quality=87, optimize=True)
        print(f"{name}: {mode}/{group} -> {dst_path}")


if __name__ == "__main__":
    main()
