import json
import os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

os.makedirs("production/assets/locations", exist_ok=True)
os.makedirs("production/assets/rigs", exist_ok=True)

FONT_PATH = "production/fonts/DisplaySerif-Bold.ttf"

def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

# ---------------------------------------------------------
# 1. Build 2x2 Angle/Lighting Grids for the 5 Hybrid Locations
#    + Master Locations Contact Grid
# ---------------------------------------------------------
locations = [
    ("loc_troy", "WALLS & GATES OF TROY", "production/assets/locations/loc_troy_ref.png"),
    ("loc_camp", "GREEK CAMP & BEACH", "production/assets/locations/loc_camp_ref.png"),
    ("loc_palace", "BRONZE AGE PALACE HALL", "production/assets/locations/loc_palace_ref.png"),
    ("loc_olympus", "MOUNT OLYMPUS & IDA", "production/assets/locations/loc_olympus_ref.png"),
    ("loc_aulis", "HARBOR OF AULIS", "production/assets/locations/loc_aulis_ref.png"),
]

def make_location_variants(ref_img, loc_id):
    w, h = ref_img.size
    # 1. Wide Establishing (full frame, golden hour grade)
    v_wide = ref_img.copy()
    # 2. Medium framing (1.28x push-in toward mid-ground)
    cw, ch = int(w * 0.76), int(h * 0.76)
    x0, y0 = int(w * 0.12), int(h * 0.14)
    v_med = ref_img.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.Resampling.LANCZOS)
    # 3. Architectural / Foreground Detail (1.55x crop on focal structure)
    dw, dh = int(w * 0.62), int(h * 0.62)
    dx0, dy0 = int(w * 0.24), int(h * 0.10)
    v_det = ref_img.crop((dx0, dy0, dx0 + dw, dy0 + dh)).resize((w, h), Image.Resampling.LANCZOS)
    # 4. Dusk / Night Torchlight Time-of-Day Grade
    arr = np.asarray(ref_img, dtype=np.float32)
    # Cool deep twilight shadows + warm torch highlights
    lum = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255.0
    hi_mask = np.clip((lum - 0.55) * 2.2, 0.0, 1.0)[:, :, None]
    dusk = np.zeros_like(arr)
    dusk[:, :, 0] = arr[:, :, 0] * 0.42 + hi_mask[:, :, 0] * 110.0
    dusk[:, :, 1] = arr[:, :, 1] * 0.46 + hi_mask[:, :, 0] * 65.0
    dusk[:, :, 2] = arr[:, :, 2] * 0.68 + 18.0
    v_dusk = Image.fromarray(np.clip(dusk, 0, 255).astype(np.uint8))

    # Save standalone angle variants so scene assembler can use all 4 per location (20 unique background plates!)
    v_wide.save(f"production/assets/locations/{loc_id}_wide.jpg", quality=92)
    v_med.save(f"production/assets/locations/{loc_id}_med.jpg", quality=92)
    v_det.save(f"production/assets/locations/{loc_id}_detail.jpg", quality=92)
    v_dusk.save(f"production/assets/locations/{loc_id}_night.jpg", quality=92)

    # Compose 2x2 angle grid
    gw, gh = 960, 540
    grid = Image.new("RGB", (gw * 2, gh * 2), (20, 18, 16))
    draw = ImageDraw.Draw(grid)
    font = load_font(24)
    angles = [
        ("1. WIDE ESTABLISHING", v_wide),
        ("2. MEDIUM FRAMING", v_med),
        ("3. ARCHITECTURAL DETAIL", v_det),
        ("4. DUSK / NIGHT GRADE", v_dusk),
    ]
    for idx, (label, im) in enumerate(angles):
        r, c = divmod(idx, 2)
        cell = im.resize((gw, gh), Image.Resampling.LANCZOS)
        grid.paste(cell, (c * gw, r * gh))
        bx, by = c * gw, r * gh
        draw.rectangle([bx, by, bx + gw - 1, by + gh - 1], outline=(155, 58, 18), width=4)
        draw.rectangle([bx + 14, by + gh - 48, bx + 420, by + gh - 12], fill=(20, 18, 16))
        draw.text((bx + 24, by + gh - 42), label, fill=(245, 215, 160), font=font)
    grid_path = f"production/assets/locations/{loc_id}_grid.jpg"
    grid.save(grid_path, quality=90)
    return grid_path

for loc_id, title, ref_path in locations:
    ref_im = Image.open(ref_path).convert("RGB")
    make_location_variants(ref_im, loc_id)

# Master contact sheet showing all 5 Hybrid Locations + their 2x2 grids
master_loc = Image.new("RGB", (1920, 1080), (24, 21, 19))
mdraw = ImageDraw.Draw(master_loc)
mfont = load_font(22)
tfont = load_font(30)
mdraw.text((40, 18), "STEP 3 — HYBRID LOCATION SHEETS (PRIMARY REFS + 2x2 ANGLE GRIDS)", fill=(245, 215, 160), font=tfont)

for idx, (loc_id, title, ref_path) in enumerate(locations):
    col = idx % 3
    row = idx // 3
    cw, ch = 610, 480
    x0 = 30 + col * 630
    y0 = 75 + row * 495
    ref_im = Image.open(ref_path).convert("RGB").resize((cw, 235), Image.Resampling.LANCZOS)
    grid_im = Image.open(f"production/assets/locations/{loc_id}_grid.jpg").convert("RGB").resize((cw, 235), Image.Resampling.LANCZOS)
    master_loc.paste(ref_im, (x0, y0))
    master_loc.paste(grid_im, (x0, y0 + 240))
    mdraw.rectangle([x0, y0, x0 + cw, y0 + 475], outline=(155, 58, 18), width=3)
    mdraw.rectangle([x0 + 8, y0 + 8, x0 + 380, y0 + 40], fill=(20, 18, 16))
    mdraw.text((x0 + 16, y0 + 12), title, fill=(245, 215, 160), font=mfont)

master_loc.save("production/assets/locations/locations_contact_grid.jpg", quality=92)
print("Saved all 5 location 2x2 angle grids and locations_contact_grid.jpg")
