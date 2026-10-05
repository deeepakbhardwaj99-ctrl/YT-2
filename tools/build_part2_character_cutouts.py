"""Extract approved Part 2 character sheets as transparent static cutouts and face anchors.

The sheets have a plain, nearly uniform warm-cream background. This tool removes only
background-colored pixels connected to the canvas border, so cream robes and swaddling
inside the character silhouettes remain opaque (unlike a global color-distance matte).
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
SHEETS = ROOT / "production/part2/character_sheets"
RIG_DIR = ROOT / "production/assets/rigs"
ANCHORS_PATH = RIG_DIR / "char_anchors.json"
CALIBRATION_PATH = SHEETS / "part2_cutout_calibration.jpg"

CHARACTERS = {
    "protesilaus": {"sheet": "protesilaus_sheet.png", "face_roi": (575, 140, 700, 180)},
    "philoctetes": {"sheet": "philoctetes_sheet.png", "face_roi": (600, 108, 675, 132)},
    "chryses": {"sheet": "chryses_sheet.png", "face_roi": (620, 100, 700, 126)},
    "patroclus": {"sheet": "patroclus_sheet.png", "face_roi": (602, 104, 680, 130)},
    "andromache_astyanax": {"sheet": "andromache_astyanax_sheet.png", "face_roi": (672, 88, 738, 114)},
}


def border_pixels(rgb, thickness=18):
    return np.concatenate((
        rgb[:thickness, :, :].reshape(-1, 3),
        rgb[-thickness:, :, :].reshape(-1, 3),
        rgb[:, :thickness, :].reshape(-1, 3),
        rgb[:, -thickness:, :].reshape(-1, 3),
    ), axis=0)


def extract_border_connected_cutout(sheet_path: Path) -> Image.Image:
    source = Image.open(sheet_path).convert("RGB")
    rgb = np.asarray(source, dtype=np.float32)
    h, w = rgb.shape[:2]
    bg = np.median(border_pixels(rgb), axis=0)
    distance = np.sqrt(np.sum((rgb - bg) ** 2, axis=2))

    # Flat background varies by only a few RGB levels; allow generous tolerance for
    # subtle backdrop shading while using border connectivity to protect pale clothing.
    background_candidates = distance <= 48.0
    seeds = np.zeros((h, w), dtype=bool)
    seeds[0, :] = background_candidates[0, :]
    seeds[-1, :] = background_candidates[-1, :]
    seeds[:, 0] = background_candidates[:, 0]
    seeds[:, -1] = background_candidates[:, -1]
    background = ndimage.binary_propagation(
        input=seeds,
        structure=np.ones((3, 3), dtype=bool),
        mask=background_candidates,
    )

    # Reject isolated background texture/noise that is not part of the figure.
    foreground = ~background
    labeled, count = ndimage.label(foreground, structure=np.ones((3, 3), dtype=bool))
    sizes = np.bincount(labeled.ravel())
    keep = sizes >= 80
    keep[0] = False
    foreground = keep[labeled]
    background = ~foreground

    # A one-pixel inner transition keeps the edge antialiased without color-keying
    # the interior of light robes or the infant's swaddling.
    inside_distance = ndimage.distance_transform_edt(foreground)
    alpha = np.where(foreground, 255.0, 0.0)
    edge_band = foreground & (inside_distance < 1.5)
    alpha[edge_band] = np.clip(inside_distance[edge_band] / 1.5, 0.0, 1.0) * 255.0

    rgba = np.dstack((rgb, alpha)).clip(0, 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def detect_eyes_and_mouth(cutout: Image.Image, roi: tuple[int, int, int, int]) -> tuple[list, list, int, list]:
    arr = np.asarray(cutout)
    x0, y0, x1, y1 = roi
    if x1 > cutout.width or y1 > cutout.height:
        raise ValueError(f"Face ROI {roi} exceeds image size {cutout.size}.")
    rgb = arr[y0:y1, x0:x1, :3]
    alpha = arr[y0:y1, x0:x1, 3]
    lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    dark = (lum < 58) & (alpha > 128)
    labeled, count = ndimage.label(dark)

    components = []
    for label in range(1, count + 1):
        ys, xs = np.where(labeled == label)
        area = len(xs)
        bw = int(xs.max() - xs.min() + 1)
        bh = int(ys.max() - ys.min() + 1)
        aspect = max(bw, bh) / max(1, min(bw, bh))
        if 12 <= area <= 180 and aspect <= 3.5:
            components.append({
                "x": x0 + int(round(float(xs.mean()))),
                "y": y0 + int(round(float(ys.mean()))),
                "area": area,
                "radius": max(3, int(round(max(bw, bh) / 2))),
            })
    pairs = []
    expected_y = (y0 + y1) / 2.0
    for i, a in enumerate(components):
        for b in components[i + 1:]:
            left, right = sorted((a, b), key=lambda item: item["x"])
            dx = right["x"] - left["x"]
            dy = abs(right["y"] - left["y"])
            if 18 <= dx <= 65 and dy <= 7:
                score = (dy * 8.0 + abs(left["area"] - right["area"]) * 0.08
                         + abs((left["y"] + right["y"]) / 2.0 - expected_y) * 0.30
                         + abs(dx - 40) * 0.18)
                pairs.append((score, left, right))
    if not pairs:
        raise ValueError(f"Could not identify an eye pair in ROI {roi}.")
    _, left, right = min(pairs, key=lambda pair: pair[0])
    eye_left, eye_right = [left["x"], left["y"]], [right["x"], right["y"]]
    eye_radius = int(np.clip(round((left["radius"] + right["radius"]) / 2), 4, 10))
    midpoint_x = int(round((left["x"] + right["x"]) / 2))
    midpoint_y = int(round((left["y"] + right["y"]) / 2))
    mouth_y = midpoint_y + int(round((right["x"] - left["x"]) * 0.9))
    return eye_left, eye_right, eye_radius, [midpoint_x, mouth_y]


def face_and_body_anchors(cutout: Image.Image, face_roi: tuple[int, int, int, int]) -> dict:
    rgba = np.asarray(cutout)
    alpha = rgba[:, :, 3]
    ys, xs = np.where(alpha > 64)
    if len(xs) == 0:
        raise ValueError("Cutout has an empty foreground matte.")
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    bottom_band = y1 - max(4, int((y1 - y0) * 0.05))
    bottom_xs = xs[ys >= bottom_band]
    foot_x = int(np.median(bottom_xs)) if len(bottom_xs) else (x0 + x1) // 2
    center_x0, center_x1 = max(0, foot_x - 120), min(cutout.width, foot_x + 120)
    core_y, _ = np.where(alpha[:, center_x0:center_x1] > 64)
    if len(core_y) == 0:
        head_top = y0
        foot_bottom = y1 - 1
    else:
        head_top = int(core_y.min())
        foot_bottom = int(core_y.max())

    eyes_left, eyes_right, eye_radius, mouth = detect_eyes_and_mouth(cutout, face_roi)
    return {
        "bbox": [x0, y0, x1, y1],
        "foot_anchor": [foot_x, foot_bottom],
        "head_top_y": head_top,
        "eye_left": eyes_left,
        "eye_right": eyes_right,
        "eye_radius": eye_radius,
        "mouth_center": mouth,
        "mouth_radius": [10, 5],
    }


def make_calibration_grid(entries: list[tuple[str, Image.Image, dict]]) -> None:
    width, height, gap, header, columns = 500, 535, 24, 105, 3
    rows = (len(entries) + columns - 1) // columns
    sheet = Image.new("RGB", (gap + columns * (width + gap), header + gap + rows * (height + gap)), "#f3eee4")
    draw = ImageDraw.Draw(sheet)
    serif_path = ROOT / "production/fonts/DisplaySerif-Bold.ttf"
    sans_path = ROOT / "production/fonts/DisplaySans-Bold.ttf"
    title_font = ImageFont.truetype(str(serif_path), 34)
    label_font = ImageFont.truetype(str(sans_path), 20)
    draw.text((gap, 18), "PART 2 STATIC CUTOUTS — MATTE & FACE-ANCHOR QC", font=title_font, fill="#1e2932")
    draw.text((gap, 60), "Blue = crop bounds · cyan = eye anchors · green = mouth · red = foot anchor", font=label_font, fill="#48545a")

    for i, (name, cutout, anchor) in enumerate(entries):
        col, row = i % columns, i // columns
        x, y = gap + col * (width + gap), header + gap + row * (height + gap)
        draw.rounded_rectangle((x, y, x + width, y + height), radius=12, fill="#fffdf8", outline="#9b3a12", width=3)
        bx0, by0, bx1, by1 = anchor["bbox"]
        crop_box = (max(0, bx0 - 18), max(0, by0 - 18), min(cutout.width, bx1 + 18), min(cutout.height, by1 + 18))
        crop = cutout.crop(crop_box)
        max_size = (width - 30, height - 90)
        scale = min(max_size[0] / crop.width, max_size[1] / crop.height)
        new_size = (int(round(crop.width * scale)), int(round(crop.height * scale)))
        crop = crop.resize(new_size, Image.Resampling.LANCZOS)
        px, py = x + (width - crop.width) // 2, y + 10 + (height - 90 - crop.height) // 2
        checker = Image.new("RGBA", crop.size, (235, 229, 218, 255))
        checker.alpha_composite(crop)
        sheet.paste(checker.convert("RGB"), (px, py))
        factor = scale
        def point(pt):
            return (px + (pt[0] - crop_box[0]) * factor, py + (pt[1] - crop_box[1]) * factor)
        left, right = point(anchor["eye_left"]), point(anchor["eye_right"])
        mouth = point(anchor["mouth_center"])
        foot = point(anchor["foot_anchor"])
        radius = max(4, int(anchor["eye_radius"] * factor))
        for ex, ey in (left, right):
            draw.ellipse((ex-radius, ey-radius, ex+radius, ey+radius), outline="#00b8d9", width=3)
        mw, mh = anchor["mouth_radius"]
        draw.rectangle((mouth[0]-mw*factor, mouth[1]-mh*factor, mouth[0]+mw*factor, mouth[1]+mh*factor), outline="#29a34a", width=3)
        draw.ellipse((foot[0]-6, foot[1]-6, foot[0]+6, foot[1]+6), fill="#d62323")
        b0, b1 = point((bx0, by0)), point((bx1, by1))
        draw.rectangle((b0[0], b0[1], b1[0], b1[1]), outline="#2379dd", width=2)
        display_name = "ANDROMACHE + ASTYANAX" if name == "andromache_astyanax" else name.upper()
        draw.text((x + 14, y + height - 65), display_name, font=label_font, fill="#1e2932")
        draw.text((x + 14, y + height - 37), f"eyes {anchor['eye_left']} / {anchor['eye_right']} · mouth {anchor['mouth_center']}", font=ImageFont.truetype(str(ROOT / "production/fonts/DisplaySans-Bold.ttf"), 13), fill="#48545a")
    sheet.save(CALIBRATION_PATH, quality=93, optimize=True)


def main():
    RIG_DIR.mkdir(parents=True, exist_ok=True)
    SHEETS.mkdir(parents=True, exist_ok=True)
    anchors = json.loads(ANCHORS_PATH.read_text())
    entries = []
    for name, spec in CHARACTERS.items():
        sheet_path = SHEETS / spec["sheet"]
        if not sheet_path.is_file():
            raise FileNotFoundError(sheet_path)
        cutout = extract_border_connected_cutout(sheet_path)
        info = face_and_body_anchors(cutout, spec["face_roi"])
        out_path = RIG_DIR / f"cutout_{name}.png"
        cutout.save(out_path, optimize=True)
        anchors[name] = info
        entries.append((name, cutout, info))
        print(f"{name}: bbox={info['bbox']} eyes={info['eye_left']},{info['eye_right']} mouth={info['mouth_center']} feet={info['foot_anchor']}")

    ANCHORS_PATH.write_text(json.dumps(anchors, indent=2, ensure_ascii=False) + "\n")
    make_calibration_grid(entries)
    print(f"Saved {len(entries)} RGBA cutouts; updated {ANCHORS_PATH.relative_to(ROOT)}")
    print(f"Face/matte QC preview: {CALIBRATION_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
