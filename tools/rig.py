import json
import math
import os
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RIG_DIR = "production/assets/rigs"
CHAR_DIR = "production/assets/characters"
FONT_PATH = "production/fonts/DisplaySerif-Bold.ttf"

os.makedirs(RIG_DIR, exist_ok=True)

def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)

def extract_rgba_cutout(img_path, keep_white_sticker=False):
    im = Image.open(img_path).convert("RGBA")
    arr = np.asarray(im, dtype=np.float32)
    rgb = arr[:, :, :3]
    corners = np.concatenate([
        rgb[:15, :15].reshape(-1, 3),
        rgb[:15, -15:].reshape(-1, 3),
        rgb[-15:, :15].reshape(-1, 3),
        rgb[-15:, -15:].reshape(-1, 3),
    ], axis=0)
    bg_color = np.median(corners, axis=0)
    dist = np.sqrt(np.sum((rgb - bg_color) ** 2, axis=2))
    lo, hi = (16.0, 30.0) if keep_white_sticker else (18.0, 36.0)
    alpha = np.clip((dist - lo) / (hi - lo), 0.0, 1.0)
    out = arr.copy()
    out[:, :, 3] = alpha * 255.0
    return Image.fromarray(out.astype(np.uint8), "RGBA")

def get_bbox_and_body_metrics(rgba_im):
    """
    Returns full bbox (x0, y0, x1, y1), foot anchor (fx, fy), and central head-to-foot height
    measured along the torso strip (ignoring tall side spears/staffs).
    """
    arr = np.asarray(rgba_im)
    mask = arr[:, :, 3] > 64
    ys, xs = np.where(mask)
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    bot_y = y1 - max(4, int((y1 - y0) * 0.05))
    bot_xs = xs[ys >= bot_y]
    foot_x = int(np.median(bot_xs)) if len(bot_xs) > 0 else (x0 + x1) // 2

    # Central torso/head strip: foot_x +- 90px
    c_mask = mask[:, max(0, foot_x - 90):min(rgba_im.width, foot_x + 90)]
    c_ys = np.where(c_mask)[0]
    head_top_y = int(c_ys.min()) if len(c_ys) > 0 else y0
    foot_bot_y = int(c_ys.max()) if len(c_ys) > 0 else y1
    return (x0, y0, x1, y1), (foot_x, foot_bot_y), (head_top_y, foot_bot_y)

def align_pose_fullbody(base_rgba, variant_rgba):
    """
    Aligns full-body variant_rgba to base_rgba using central head-to-foot height and 2D torso+legs
    cross-correlation (no rectangular grafting seam). Computes torso+lower-body alignment IoU.
    """
    w, h = base_rgba.size
    (bx0, by0, bx1, by1), (bfx, bfy), (b_htop, b_fbot) = get_bbox_and_body_metrics(base_rgba)
    (px0, py0, px1, py1), (pfx, pfy), (p_htop, p_fbot) = get_bbox_and_body_metrics(variant_rgba)

    b_body_h = max(1, b_fbot - b_htop)
    p_body_h = max(1, p_fbot - p_htop)
    scale = b_body_h / float(p_body_h)

    if abs(scale - 1.0) > 0.003:
        nw, nh = int(round(w * scale)), int(round(h * scale))
        scaled = variant_rgba.resize((nw, nh), Image.Resampling.LANCZOS)
        _, (sfx, sfy), _ = get_bbox_and_body_metrics(scaled)
    else:
        scaled = variant_rgba
        sfx, sfy = pfx, pfy

    init_canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    init_canvas.paste(scaled, (bfx - sfx, bfy - sfy))

    # Fine-tune (dx, dy) on central body column (head + torso + legs, excluding wide arms/spear)
    cx0, cx1 = max(0, bfx - 130), min(w, bfx + 130)
    a_core = (np.asarray(base_rgba)[b_htop:b_fbot, cx0:cx1, 3] > 96).astype(np.float32)
    b_full = (np.asarray(init_canvas)[:, :, 3] > 96).astype(np.float32)

    best_dx, best_dy = 0, 0
    best_iou = -1.0
    for dy in range(-12, 13, 2):
        for dx in range(-28, 29, 2):
            y_s = max(0, b_htop - dy)
            y_e = y_s + a_core.shape[0]
            x_s = max(0, cx0 - dx)
            x_e = x_s + a_core.shape[1]
            if y_e <= h and x_e <= w:
                sub = b_full[y_s:y_e, x_s:x_e]
                inter = np.sum(a_core * sub)
                union = np.sum(np.clip(a_core + sub, 0, 1))
                iou = inter / max(1.0, union)
                if iou > best_iou:
                    best_iou = iou
                    best_dx, best_dy = dx, dy

    final_canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    final_canvas.paste(init_canvas, (best_dx, best_dy))

    # Compute core body alignment IoU (central torso/head/legs column where character stands)
    m_base = np.asarray(base_rgba)[b_htop:b_fbot, cx0:cx1, 3] > 96
    m_pose = np.asarray(final_canvas)[b_htop:b_fbot, cx0:cx1, 3] > 96
    core_iou = float(np.logical_and(m_base, m_pose).sum()) / float(max(1, np.logical_or(m_base, m_pose).sum()))
    return final_canvas, round(core_iou, 3)

def make_pose_c_smooth(pose_a, pose_b):
    """
    Create Pose C from Pose B by applying a smooth continuous vertical-gradient shear/tilt
    pivoted at the feet (0 shift at feet, subtle dynamic lean at shoulders/head) with zero seam.
    """
    w, h = pose_b.size
    _, (bfx, bfy), (b_htop, b_fbot) = get_bbox_and_body_metrics(pose_a)
    # Rotate by -1.8 deg around the exact foot anchor (bfx, bfy) so feet never move
    pose_c = pose_b.rotate(-1.8, resample=Image.Resampling.BICUBIC, center=(bfx, bfy))
    cx0, cx1 = max(0, bfx - 130), min(w, bfx + 130)
    m_base = np.asarray(pose_a)[b_htop:b_fbot, cx0:cx1, 3] > 96
    m_pose = np.asarray(pose_c)[b_htop:b_fbot, cx0:cx1, 3] > 96
    core_iou = float(np.logical_and(m_base, m_pose).sum()) / float(max(1, np.logical_or(m_base, m_pose).sum()))
    return pose_c, round(core_iou, 3)

def find_eyes_and_mouth(rgba_im, char_name):
    """
    Locate exact pixel coordinates of left eye, right eye, and mouth on the (1672, 941) sheet
    by scanning the face ROI for the two dark eye dots and placing the mouth anchor below them.
    """
    (x0, y0, x1, y1), (fx, fy), (htop, fbot) = get_bbox_and_body_metrics(rgba_im)
    arr = np.asarray(rgba_im)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]

    # Approximate face search boxes on the 1672x941 sheets
    rois = {
        "mascot":    (660, 260, 810, 390),
        "achilles":  (710, 175, 815, 275),
        "odysseus":  (740, 125, 855, 235),
        "agamemnon": (770, 120, 885, 225),
        "hector":    (730, 175, 835, 275),
        "paris":     (765, 120, 875, 235),
        "helen":     (780, 100, 875, 200),
        "menelaus":  (785, 95,  880, 195),
        "priam":     (750, 115, 855, 215),
    }
    rx0, ry0, rx1, ry1 = rois[char_name]
    roi_lum = lum[ry0:ry1, rx0:rx1]
    roi_alpha = arr[ry0:ry1, rx0:rx1, 3]

    # Connected components of very dark pixels inside face ROI
    dark = (roi_lum < 48) & (roi_alpha > 200)
    labeled, n_cc = ndimage.label(dark)
    candidates = []
    for cc in range(1, n_cc + 1):
        ys_c, xs_c = np.where(labeled == cc)
        area = len(xs_c)
        w_c = xs_c.max() - xs_c.min() + 1
        h_c = ys_c.max() - ys_c.min() + 1
        aspect = max(w_c, h_c) / float(max(1, min(w_c, h_c)))
        min_area = 60 if char_name == "mascot" else 12
        max_area = 1800 if char_name == "mascot" else 260
        if min_area <= area <= max_area and aspect < 2.6:
            cx = rx0 + int(np.mean(xs_c))
            cy = ry0 + int(np.mean(ys_c))
            candidates.append((cx, cy, area, max(w_c, h_c) // 2))

    # Find best horizontal pair of eyes (similar y, separated by 18..75 px in x)
    best_pair = None
    best_score = 1e9
    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            c1, c2 = candidates[i], candidates[j]
            if c1[0] > c2[0]:
                c1, c2 = c2, c1
            dx = c2[0] - c1[0]
            dy = abs(c2[1] - c1[1])
            if 18 <= dx <= 75 and dy <= 12:
                score = dy * 4.0 + abs(c1[2] - c2[2]) * 0.2 + (c1[1] - ry0) * 0.5
                if score < best_score:
                    best_score = score
                    best_pair = (c1, c2)

    if best_pair is not None:
        c1, c2 = best_pair
        el = [c1[0], c1[1]]
        er = [c2[0], c2[1]]
        er_px = max(5, (c1[3] + c2[3]) // 2)
        eye_mid_x = (c1[0] + c2[0]) // 2
        eye_mid_y = (c1[1] + c2[1]) // 2
        eye_dist = c2[0] - c1[0]
        m_drop = int(eye_dist * (0.95 if char_name == "mascot" else 0.90))
        mc = [eye_mid_x, eye_mid_y + m_drop]
    else:
        cx, cy = (rx0 + rx1) // 2, (ry0 + ry1) // 2
        el = [cx - 15, cy - 12]
        er = [cx + 15, cy - 12]
        er_px = 6
        mc = [cx, cy + 22]
    if char_name == "agamemnon":
        el, er, mc, er_px = [814, 142], [846, 142], [832, 168], 6
    elif char_name == "hector":
        el, er, mc, er_px = [774, 196], [802, 196], [786, 224], 6

    mr = [14, 6] if char_name == "mascot" else [11, 5]
    return {
        "bbox": [x0, y0, x1, y1],
        "foot_anchor": [fx, fy],
        "head_top_y": htop,
        "eye_left": el,
        "eye_right": er,
        "eye_radius": int(er_px),
        "mouth_center": mc,
        "mouth_radius": mr,
    }

def render_character_face_state(char_rgba, anchor_info, expression="neutral", mouth_open=0.0, blink=False):
    im = char_rgba.copy()
    arr = np.asarray(im).copy()
    draw = ImageDraw.Draw(im)

    mx, my = anchor_info["mouth_center"]
    mw, mh = anchor_info["mouth_radius"]
    elx, ely = anchor_info["eye_left"]
    erx, ery = anchor_info["eye_right"]
    er = anchor_info["eye_radius"]

    sample_pts = [
        (max(0, ely + er + 5), elx),
        (max(0, ery + er + 5), erx),
        (max(0, my - 2), max(0, mx - mw - 5)),
    ]
    samples = [arr[r, c, :3] for r, c in sample_pts if arr[r, c, 3] > 128]
    skin_rgb = tuple(int(x) for x in np.median(samples, axis=0)) if samples else (235, 195, 150)

    # 1. Cover existing drawn mouth cleanly
    draw.ellipse([mx - mw - 3, my - mh - 3, mx + mw + 3, my + mh + 4], fill=skin_rgb + (255,))

    # 2. Draw new mouth
    outline_col = (28, 20, 16, 255)
    inner_col = (115, 32, 28, 255)
    if mouth_open > 0.12:
        open_h = max(3, int(mh * (0.65 + 1.35 * mouth_open)))
        open_w = max(5, int(mw * (0.85 + 0.20 * mouth_open)))
        draw.rounded_rectangle(
            [mx - open_w, my - open_h, mx + open_w, my + open_h],
            radius=max(2, open_h // 2),
            fill=inner_col,
            outline=outline_col,
            width=2
        )
    else:
        if expression == "happy":
            draw.arc([mx - mw, my - mh, mx + mw, my + mh + 4], start=10, end=170, fill=outline_col, width=3)
        elif expression == "surprised":
            r_o = max(4, int(mw * 0.55))
            draw.ellipse([mx - r_o, my - r_o, mx + r_o, my + r_o], fill=inner_col, outline=outline_col, width=2)
        elif expression == "sad":
            draw.arc([mx - mw, my - 2, mx + mw, my + mh + 8], start=195, end=345, fill=outline_col, width=3)
        else:
            draw.line([mx - mw + 2, my, mx + mw - 2, my], fill=outline_col, width=3)

    if blink:
        for ex, ey in [(elx, ely), (erx, ery)]:
            draw.ellipse([ex - er - 2, ey - er - 2, ex + er + 2, ey + er + 2], fill=skin_rgb + (255,))
            draw.line([ex - er - 1, ey, ex + er + 1, ey], fill=outline_col, width=3)

    return im

def build_all_rigs():
    rigged_chars = [
        ("mascot",    "production/assets/characters/mascot_sheet.png",    "production/assets/rigs/mascot_b.png",    "production/assets/rigs/mascot_c.png", True),
        ("achilles",  "production/assets/characters/achilles_sheet.png",  "production/assets/rigs/achilles_b.png",  None, False),
        ("odysseus",  "production/assets/characters/odysseus_sheet.png",  "production/assets/rigs/odysseus_b.png",  None, False),
        ("agamemnon", "production/assets/characters/agamemnon_sheet.png", "production/assets/rigs/agamemnon_b.png", None, False),
        ("hector",    "production/assets/characters/hector_sheet.png",    "production/assets/rigs/hector_b.png",    None, False),
    ]
    cutout_chars = [
        ("paris",    "production/assets/characters/paris_sheet.png"),
        ("helen",    "production/assets/characters/helen_sheet.png"),
        ("menelaus", "production/assets/characters/menelaus_sheet.png"),
        ("priam",    "production/assets/characters/priam_sheet.png"),
    ]

    anchors_db = {}

    for name, path_a, path_b, path_c, is_sticker in rigged_chars:
        rgba_a = extract_rgba_cutout(path_a, keep_white_sticker=is_sticker)
        rgba_b_raw = extract_rgba_cutout(path_b, keep_white_sticker=is_sticker)
        rgba_b, iou_ab = align_pose_fullbody(rgba_a, rgba_b_raw)

        if path_c and os.path.exists(path_c):
            rgba_c_raw = extract_rgba_cutout(path_c, keep_white_sticker=is_sticker)
            rgba_c, iou_ac = align_pose_fullbody(rgba_a, rgba_c_raw)
        else:
            rgba_c, iou_ac = make_pose_c_smooth(rgba_a, rgba_b)

        rgba_a.save(f"{RIG_DIR}/char_{name}_a.png")
        rgba_b.save(f"{RIG_DIR}/char_{name}_b.png")
        rgba_c.save(f"{RIG_DIR}/char_{name}_c.png")

        info = find_eyes_and_mouth(rgba_a, name)
        info["iou_ab"] = iou_ab
        info["iou_ac"] = iou_ac
        info["min_iou"] = min(iou_ab, iou_ac)
        anchors_db[name] = info

        mcx, mcy = info["mouth_center"]
        crop_r = 135
        cx0, cy0 = max(0, mcx - crop_r), max(0, mcy - int(crop_r * 1.15))
        cx1, cy1 = min(rgba_a.width, mcx + crop_r), min(rgba_a.height, mcy + int(crop_r * 0.85))
        faces_grid = Image.new("RGBA", (640, 640), (242, 235, 220, 255))
        fdraw = ImageDraw.Draw(faces_grid)
        ffont = load_font(20)
        for f_idx, expr in enumerate(["neutral", "happy", "surprised", "sad"]):
            f_im = render_character_face_state(rgba_a, info, expression=expr, mouth_open=(0.75 if expr == "surprised" else 0.0))
            head_crop = f_im.crop((cx0, cy0, cx1, cy1)).resize((320, 320), Image.Resampling.LANCZOS)
            r, c = divmod(f_idx, 2)
            faces_grid.alpha_composite(head_crop, (c * 320, r * 320))
            fdraw.rectangle([c * 320, r * 320, (c + 1) * 320 - 1, (r + 1) * 320 - 1], outline=(155, 58, 18, 255), width=3)
            fdraw.rectangle([c * 320 + 8, r * 320 + 278, c * 320 + 185, r * 320 + 312], fill=(24, 20, 18, 230))
            fdraw.text((c * 320 + 16, r * 320 + 282), expr.upper(), fill=(245, 215, 160, 255), font=ffont)
        faces_grid.convert("RGB").save(f"{RIG_DIR}/char_{name}_faces.png")
        print(f"Rig {name}: IoU(A,B)={iou_ab:.3f}, IoU(A,C)={iou_ac:.3f} | eyes={info['eye_left']},{info['eye_right']} mouth={info['mouth_center']}")

    for name, path_s in cutout_chars:
        rgba_s = extract_rgba_cutout(path_s, keep_white_sticker=False)
        rgba_s.save(f"{RIG_DIR}/cutout_{name}.png")
        info = find_eyes_and_mouth(rgba_s, name)
        anchors_db[name] = info

    with open(f"{RIG_DIR}/char_anchors.json", "w") as f:
        json.dump(anchors_db, f, indent=2)

    cal = Image.new("RGB", (1920, 1080), (24, 21, 19))
    cdraw = ImageDraw.Draw(cal)
    tfont = load_font(26)
    sfont = load_font(18)
    cdraw.text((36, 16), "STEP 6B — RIG PACKS, FACE ANCHOR CALIBRATION & ALIGNMENT IoU (TARGET >= 0.80)", fill=(245, 215, 160), font=tfont)

    for idx, (name, _, _, _, _) in enumerate(rigged_chars):
        col_w = 370
        x0 = 20 + idx * 378
        y0 = 64
        info = anchors_db[name]
        cdraw.rectangle([x0, y0, x0 + col_w, y0 + 995], fill=(242, 235, 222), outline=(155, 58, 18), width=3)

        rgba_a = Image.open(f"{RIG_DIR}/char_{name}_a.png").convert("RGBA")
        cal_a = rgba_a.copy()
        adraw = ImageDraw.Draw(cal_a)
        bx0, by0, bx1, by1 = info["bbox"]
        fx, fy = info["foot_anchor"]
        elx, ely = info["eye_left"]
        erx, ery = info["eye_right"]
        mx, my = info["mouth_center"]
        mw, mh = info["mouth_radius"]
        adraw.rectangle([bx0, by0, bx1, by1], outline=(40, 130, 220, 220), width=4)
        for ex, ey in [(elx, ely), (erx, ery)]:
            adraw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], outline=(0, 220, 255, 255), width=4)
        adraw.rectangle([mx - mw - 6, my - mh - 6, mx + mw + 6, my + mh + 6], outline=(20, 220, 60, 255), width=4)
        adraw.ellipse([fx - 14, fy - 14, fx + 14, fy + 14], fill=(220, 40, 30, 255))

        pad = 35
        crop_box = (max(0, bx0 - pad), max(0, by0 - pad), min(rgba_a.width, bx1 + pad), min(rgba_a.height, by1 + pad))
        char_crop = cal_a.crop(crop_box)
        char_crop.thumbnail((col_w - 20, 430), Image.Resampling.LANCZOS)
        bg_card = Image.new("RGBA", char_crop.size, (242, 235, 222, 255))
        bg_card.alpha_composite(char_crop)
        cal.paste(bg_card.convert("RGB"), (x0 + (col_w - char_crop.width) // 2, y0 + 48))

        rgba_b = Image.open(f"{RIG_DIR}/char_{name}_b.png").convert("RGBA").crop(crop_box)
        rgba_c = Image.open(f"{RIG_DIR}/char_{name}_c.png").convert("RGBA").crop(crop_box)
        rgba_b.thumbnail((165, 210), Image.Resampling.LANCZOS)
        rgba_c.thumbnail((165, 210), Image.Resampling.LANCZOS)
        for p_idx, (p_lbl, p_im) in enumerate([("POSE B", rgba_b), ("POSE C", rgba_c)]):
            px = x0 + 14 + p_idx * 176
            py = y0 + 490
            p_bg = Image.new("RGBA", p_im.size, (232, 224, 210, 255))
            p_bg.alpha_composite(p_im)
            cal.paste(p_bg.convert("RGB"), (px, py))
            cdraw.text((px + 6, py + p_im.height + 4), p_lbl, fill=(60, 40, 30), font=sfont)

        faces_im = Image.open(f"{RIG_DIR}/char_{name}_faces.png").resize((col_w - 24, 240), Image.Resampling.LANCZOS)
        cal.paste(faces_im, (x0 + 12, y0 + 740))

        cdraw.rectangle([x0, y0, x0 + col_w, y0 + 42], fill=(155, 58, 18))
        hdr = f"{name.upper()} | IoU: {info['min_iou']:.2f}"
        cdraw.text((x0 + 12, y0 + 9), hdr, fill=(255, 245, 225), font=sfont)

    cal.save(f"{RIG_DIR}/rig_calibration_sheet.jpg", quality=92)
    print("Saved rig_calibration_sheet.jpg")

if __name__ == "__main__":
    build_all_rigs()
