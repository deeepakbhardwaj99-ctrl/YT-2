import json
import math
import os
import subprocess
import time
from collections import OrderedDict
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw, ImageFont

from rig import render_character_face_state

W, H = 1920, 1080
FPS = 24
SR = 24000
FONT_SERIF = "production/fonts/DisplaySerif-Bold.ttf"
FONT_SANS = "production/fonts/DisplaySans-Bold.ttf"
SPEAKER_TO_CHAR = {
    "MASCOT": "mascot", "ACHILLES": "achilles", "ODYSSEUS": "odysseus",
    "AGAMEMNON": "agamemnon", "HECTOR": "hector", "PARIS": "paris",
    "HELEN": "helen", "MENELAUS": "menelaus", "PRIAM": "priam",
    "TYNDAREUS": "priam", "ZEUS": "agamemnon", "PALAMEDES": "odysseus",
    "CALCHAS": "priam", "ERIS": "helen", "HERA": "helen",
    "ATHENA": "helen", "APHRODITE": "helen", "THETIS": "helen", "IPHIGENIA": "helen"
}

ACCENT_RGB = (155, 58, 18)       # #9B3A12 Burnt Orange
CREAM_RGB = (248, 240, 225)
DARK_RGB = (24, 20, 18)

def get_font(path, size):
    return ImageFont.truetype(path, size)

FONTS = {
    "title": get_font(FONT_SERIF, 54),
    "kicker": get_font(FONT_SANS, 20),
    "card_h": get_font(FONT_SERIF, 32),
    "chip": get_font(FONT_SANS, 19),
    "bubble": get_font(FONT_SANS, 25),
    "label": get_font(FONT_SERIF, 28),
    "sub": get_font(FONT_SANS, 25),
}

def ease_out_cubic(x):
    x = max(0.0, min(1.0, x))
    return 1.0 - (1.0 - x) ** 3

def ease_in_cubic(x):
    x = max(0.0, min(1.0, x))
    return x ** 3

def ease_out_back(x):
    x = max(0.0, min(1.0, x))
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * ((x - 1.0) ** 3) + c1 * ((x - 1.0) ** 2)

class AssetCache:
    def __init__(self):
        with open("production/assets/rigs/char_anchors.json") as f:
            self.anchors = json.load(f)
        self.bg_cache = OrderedDict()
        self.bg_cache_limit = 12
        self.base_pose_cache = {}
        self.sprite_cache = {}
        self.shadow_cache = {}
        # Prebuild deterministic film grain patterns (4 frames cycled)
        self.grains = []
        yy, xx = np.ogrid[:H:4, :W:4]
        for g_i in range(4):
            g_small = (((xx * 13 + yy * 29 + g_i * 17) % 5) - 2).astype(np.int16)
            self.grains.append(np.repeat(np.repeat(g_small, 4, axis=0), 4, axis=1)[:H, :W, None])

    def get_bg(self, path, dimmed=False):
        key = (path, dimmed)
        if key in self.bg_cache:
            self.bg_cache.move_to_end(key)
            return self.bg_cache[key]
        im = Image.open(path).convert("RGB").resize((2304, 1296), Image.Resampling.BILINEAR)
        if dimmed:
            arr = (np.asarray(im, dtype=np.uint16) * 56 // 100).astype(np.uint8)
            im = Image.fromarray(arr, "RGB")
        self.bg_cache[key] = im
        while len(self.bg_cache) > self.bg_cache_limit:
            self.bg_cache.popitem(last=False)
        return im

    def _get_base_pose(self, char_name, pose="a"):
        key = (char_name, pose)
        if key not in self.base_pose_cache:
            rig_path = f"production/assets/rigs/char_{char_name}_{pose}.png"
            cut_path = f"production/assets/rigs/cutout_{char_name}.png"
            path = rig_path if os.path.exists(rig_path) else cut_path
            im = Image.open(path).convert("RGBA")
            arr = np.asarray(im, dtype=np.float32)
            arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.02 + 3.0, 0, 255)
            arr[:, :, 1] = np.clip(arr[:, :, 1] * 0.99 + 1.0, 0, 255)
            arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.94, 0, 255)
            self.base_pose_cache[key] = Image.fromarray(arr.astype(np.uint8), "RGBA")
        return self.base_pose_cache[key]

    def get_char_sprite(self, char_name, pose, expr, mouth_bucket, blink, dimmed=False):
        """
        Returns pre-cropped, pre-scaled RGBA sprite for (char_name, pose, expr, mouth_bucket, blink, dimmed).
        Cached so each state is rendered at most once across the entire video!
        """
        key = (char_name, pose, expr, mouth_bucket, blink, dimmed)
        if key not in self.sprite_cache:
            info = self.anchors.get(char_name, self.anchors["achilles"])
            base_im = self._get_base_pose(char_name, pose)
            mouth_open = 0.0 if mouth_bucket == 0 else (0.45 if mouth_bucket == 1 else 0.85)
            framed = render_character_face_state(base_im, info, expression=expr, mouth_open=mouth_open, blink=blink)
            bx0, by0, bx1, by1 = info["bbox"]
            crop = framed.crop((max(0, bx0 - 16), max(0, by0 - 16), min(framed.width, bx1 + 16), min(framed.height, by1 + 16)))
            target_h = 500 if char_name == "mascot" else 575
            scale_f = target_h / float(max(1, crop.height))
            rw = max(1, int(crop.width * scale_f))
            rh = max(1, int(crop.height * scale_f))
            sprite = crop.resize((rw, rh), Image.Resampling.BILINEAR)
            if dimmed:
                arr = np.asarray(sprite, dtype=np.uint16)
                arr[:, :, :3] = (arr[:, :, :3] * 65) // 100
                sprite = Image.fromarray(arr.astype(np.uint8), "RGBA")
            self.sprite_cache[key] = sprite
        return self.sprite_cache[key]

    def get_shadow(self, width_px, height_px=34):
        key = (width_px, height_px)
        if key not in self.shadow_cache:
            sh = Image.new("RGBA", (width_px, height_px), (0, 0, 0, 0))
            d = ImageDraw.Draw(sh)
            d.ellipse([4, 4, width_px - 4, height_px - 4], fill=(12, 8, 5, 135))
            self.shadow_cache[key] = sh
        return self.shadow_cache[key]

def sample_camera_bg(bg_im, cam_type, progress):
    sw, sh = bg_im.size
    p = max(0.0, min(1.0, progress))
    if cam_type == "dolly-in":
        scale = 1.0 - 0.14 * p
        cw, ch = int(sw * scale), int(sh * scale)
        x0 = (sw - cw) // 2
        y0 = int((sh - ch) * (0.45 + 0.10 * p))
    elif cam_type == "pull-back":
        scale = 0.86 + 0.14 * p
        cw, ch = int(sw * scale), int(sh * scale)
        x0 = (sw - cw) // 2
        y0 = (sh - ch) // 2
    elif cam_type == "pan-right":
        cw, ch = int(sw * 0.84), int(sh * 0.84)
        x0 = int((sw - cw) * p)
        y0 = (sh - ch) // 2
    else:
        cw, ch = int(sw * 0.84), int(sh * 0.84)
        x0 = int((sw - cw) * (1.0 - p))
        y0 = (sh - ch) // 2
    return bg_im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.Resampling.NEAREST)

def draw_hand_drawn_arrow(draw, start_xy, end_xy, progress):
    if progress <= 0.0:
        return
    p = min(1.0, progress / 0.30)
    sx, sy = start_xy
    ex, ey = end_xy
    cx = (sx + ex) * 0.5
    cy = min(sy, ey) - 55
    pts = []
    n_steps = max(2, int(20 * p))
    for i in range(n_steps + 1):
        u = (i / 20.0)
        x = (1 - u) ** 2 * sx + 2 * (1 - u) * u * cx + u ** 2 * ex
        y = (1 - u) ** 2 * sy + 2 * (1 - u) * u * cy + u ** 2 * ey
        pts.append((x, y))
    if len(pts) >= 2:
        draw.line(pts, fill=(255, 248, 235), width=11, joint="curve")
        draw.line(pts, fill=ACCENT_RGB, width=6, joint="curve")
    if p >= 0.92:
        ang = math.atan2(ey - cy, ex - cx)
        ah = 22
        p1 = (ex, ey)
        p2 = (ex - ah * math.cos(ang - 0.45), ey - ah * math.sin(ang - 0.45))
        p3 = (ex - ah * math.cos(ang + 0.45), ey - ah * math.sin(ang + 0.45))
        draw.polygon([p1, p2, p3], fill=ACCENT_RGB, outline=(255, 248, 235))

def draw_callout_card(draw, card, pos_side, t_in_clip, clip_dur):
    if t_in_clip < 0.5 or t_in_clip > clip_dur - 0.4:
        return None
    enter_p = ease_out_back(min(1.0, (t_in_clip - 0.5) / 0.45))
    exit_p = ease_in_cubic(max(0.0, min(1.0, (t_in_clip - (clip_dur - 0.9)) / 0.45))) if t_in_clip > clip_dur - 0.9 else 0.0

    card_w, card_h = 620, 195
    target_x = 56 if pos_side == "top-left" else (W - card_w - 56)
    off_x = -card_w - 40 if pos_side == "top-left" else (W + 40)
    cur_x = int(off_x + (target_x - off_x) * (enter_p * (1.0 - exit_p)))
    cur_y = 52

    draw.rounded_rectangle([cur_x + 6, cur_y + 8, cur_x + card_w + 6, cur_y + card_h + 8], radius=18, fill=(10, 8, 6))
    draw.rounded_rectangle([cur_x, cur_y, cur_x + card_w, cur_y + card_h], radius=18, fill=(250, 244, 232), outline=ACCENT_RGB, width=4)

    draw.rounded_rectangle([cur_x + 22, cur_y + 16, cur_x + 210, cur_y + 44], radius=8, fill=ACCENT_RGB)
    draw.text((cur_x + 34, cur_y + 19), "KEY BEAT", fill=(255, 245, 230), font=FONTS["kicker"])

    words = card["headline"].split()
    emp = card["emphasis"].upper()
    wx = cur_x + 24
    wy = cur_y + 56
    for w_str in words:
        clean_w = w_str.strip(",.:;!?").upper()
        col = ACCENT_RGB if (emp in clean_w or clean_w in emp) else DARK_RGB
        draw.text((wx, wy), w_str + " ", fill=col, font=FONTS["card_h"])
        bbox = draw.textbbox((wx, wy), w_str + " ", font=FONTS["card_h"])
        wx = bbox[2]

    wipe_p = max(0.0, min(1.0, (t_in_clip - 0.75) / 0.40))
    uw = int((card_w - 48) * wipe_p)
    if uw > 4:
        draw.rectangle([cur_x + 24, cur_y + 104, cur_x + 24 + uw, cur_y + 110], fill=ACCENT_RGB)

    chip_x = cur_x + 24
    chip_y = cur_y + 126
    for c_i, chip_txt in enumerate(card.get("chips", [])[:3]):
        c_start = 0.90 + c_i * 0.15
        if t_in_clip >= c_start:
            cp = ease_out_cubic(min(1.0, (t_in_clip - c_start) / 0.25))
            cy_off = int((1.0 - cp) * 18)
            tb = draw.textbbox((0, 0), chip_txt, font=FONTS["chip"])
            tw = (tb[2] - tb[0]) + 28
            draw.rounded_rectangle([chip_x, chip_y + cy_off, chip_x + tw, chip_y + 42 + cy_off], radius=16, fill=(34, 28, 24), outline=ACCENT_RGB, width=2)
            draw.text((chip_x + 14, chip_y + 9 + cy_off), chip_txt, fill=CREAM_RGB, font=FONTS["chip"])
            chip_x += tw + 12

    return (cur_x + card_w // 2, cur_y + card_h)

def draw_speech_bubble(draw, bubble_text, speaker_name, mouth_xy):
    mx, my = mouth_xy
    bw, bh = 460, 108
    bx = max(40, min(W - bw - 40, int(mx - bw // 2 + (140 if mx < W // 2 else -140))))
    by = max(45, int(my - 210))

    tx = max(bx + 40, min(bx + bw - 40, int(mx)))
    tail = [(tx - 18, by + bh - 4), (tx + 18, by + bh - 4), (int(mx), int(my - 45))]
    draw.polygon(tail, fill=(252, 248, 240), outline=ACCENT_RGB)
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=(252, 248, 240), outline=ACCENT_RGB, width=4)

    draw.rounded_rectangle([bx + 16, by + 10, bx + 200, by + 36], radius=8, fill=ACCENT_RGB)
    draw.text((bx + 26, by + 13), speaker_name, fill=(255, 248, 235), font=FONTS["kicker"])

    words = bubble_text.split()
    wx = bx + 20
    wy = by + 48
    for idx, w_str in enumerate(words):
        col = ACCENT_RGB if idx == 0 else DARK_RGB
        draw.text((wx, wy), w_str + " ", fill=col, font=FONTS["bubble"])
        bbox = draw.textbbox((wx, wy), w_str + " ", font=FONTS["bubble"])
        wx = bbox[2]

def draw_establishing_label(draw, place_label, t_in_shot):
    p = ease_out_cubic(min(1.0, t_in_shot / 0.45))
    lx = int(-520 + 576 * p)
    ly = H - 185
    draw.rounded_rectangle([lx, ly, lx + 560, ly + 74], radius=12, fill=(20, 16, 14), outline=ACCENT_RGB, width=3)
    draw.rectangle([lx, ly, lx + 14, ly + 74], fill=ACCENT_RGB)
    draw.text((lx + 30, ly + 20), place_label, fill=CREAM_RGB, font=FONTS["label"])

def draw_subtitle_bar(draw, text, seg_progress=0.0):
    if not text:
        return
    words = text.split()
    if len(words) > 14:
        chunk_size = 12
        n_chunks = max(1, (len(words) + chunk_size - 1) // chunk_size)
        c_idx = min(n_chunks - 1, int(seg_progress * n_chunks))
        words = words[c_idx * chunk_size : (c_idx + 1) * chunk_size]
    lines, cur = [], []
    for w in words:
        if sum(len(x) + 1 for x in cur) + len(w) > 52 and len(lines) < 1:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    sub_txt = "\n".join(lines[:2])
    tb = draw.multiline_textbbox((0, 0), sub_txt, font=FONTS["sub"], align="center", spacing=6)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    bx0 = (W - tw) // 2 - 24
    by0 = H - th - 36
    draw.rounded_rectangle([bx0, by0 - 10, bx0 + tw + 48, by0 + th + 14], radius=10, fill=(14, 12, 10), outline=ACCENT_RGB, width=2)
    draw.multiline_text(((W - tw) // 2, by0), sub_txt, fill=(252, 246, 235), font=FONTS["sub"], align="center", spacing=6)

def render_part_card_frames(cache, card_spec, duration_s, global_t_offset=0.0):
    """Yield animated, standalone title or next-part card frames."""
    n_frames = max(1, int(round(duration_s * FPS)))
    bg_source = cache.get_bg(card_spec["bg_path"], dimmed=True)
    title_font = get_font(FONT_SERIF, 62)
    eyebrow_font = get_font(FONT_SANS, 25)
    subtitle_font = get_font(FONT_SANS, 23)
    dark = Image.new("RGB", (W, H), DARK_RGB)

    for f_idx in range(n_frames):
        progress = f_idx / max(1, n_frames - 1)
        bg = sample_camera_bg(bg_source, card_spec.get("camera", "dolly-in"), progress)
        fade_in = ease_out_cubic(progress / 0.12)
        fade_out = ease_in_cubic((progress - 0.88) / 0.12)
        opacity = max(0.0, min(1.0, fade_in * (1.0 - fade_out)))

        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        border_alpha = int(235 * opacity)
        panel_alpha = int(205 * opacity)
        draw.rounded_rectangle(
            [238, 305, 1682, 775], radius=18,
            fill=(18, 15, 13, panel_alpha),
            outline=(*ACCENT_RGB, border_alpha), width=4
        )
        center_x = W // 2
        draw.text(
            (center_x, 407), card_spec.get("eyebrow", "THE TROJAN WAR"),
            anchor="mm", font=eyebrow_font, fill=(*ACCENT_RGB, int(255 * opacity))
        )
        draw.text(
            (center_x, 525), card_spec["title"], anchor="mm", font=title_font,
            fill=(*CREAM_RGB, int(255 * opacity))
        )
        line_half = int(115 * ease_out_cubic(progress))
        draw.line(
            (center_x - line_half, 588, center_x + line_half, 588),
            fill=(*ACCENT_RGB, int(255 * opacity)), width=3
        )
        subtitle = card_spec.get("subtitle", "")
        if subtitle:
            draw.text(
                (center_x, 664), subtitle, anchor="mm", font=subtitle_font,
                fill=(*CREAM_RGB, int(230 * opacity))
            )

        frame = Image.alpha_composite(bg.convert("RGBA"), layer).convert("RGB")
        if fade_out > 0.0:
            frame = Image.blend(frame, dark, fade_out)
        yield np.asarray(frame, dtype=np.uint8), global_t_offset + f_idx / float(FPS)

def render_clip_frames(clip_plan, cache, global_t_offset=0.0):
    dur = clip_plan["duration_s"]
    n_frames = max(1, int(round(dur * FPS)))
    shots = clip_plan["shots"]
    segs = clip_plan["vo_segments"]
    active_chars = clip_plan["active_characters"]
    is_new_loc = clip_plan["is_new_location"]
    card = clip_plan["overlay_card"]

    slots = [540, 1340] if len(active_chars) > 1 else [1320 if (int(clip_plan["clip_id"][-2:]) % 2 == 1) else 580]

    for f_idx in range(n_frames):
        t = f_idx / float(FPS)
        t_global = global_t_offset + t

        cur_shot = shots[-1]
        prev_shot = None
        for s_i, sh in enumerate(shots):
            if sh["t_start"] <= t <= sh["t_end"] or (s_i == len(shots) - 1 and t >= sh["t_start"]):
                cur_shot = sh
                if s_i > 0:
                    prev_shot = shots[s_i - 1]
                break

        sh_dur = max(0.1, cur_shot["t_end"] - cur_shot["t_start"])
        sh_prog = (t - cur_shot["t_start"]) / sh_dur
        dim_bg = cur_shot["dim_background"] and not (cur_shot["shot_index"] == 1 and is_new_loc)
        bg_im = sample_camera_bg(cache.get_bg(cur_shot["bg_path"], dimmed=dim_bg), cur_shot["camera"], sh_prog)

        if prev_shot is not None and (t - cur_shot["t_start"]) < 0.36:
            alpha_xf = (t - cur_shot["t_start"]) / 0.36
            prev_dim = prev_shot["dim_background"] and not (prev_shot["shot_index"] == 1 and is_new_loc)
            prev_im = sample_camera_bg(cache.get_bg(prev_shot["bg_path"], dimmed=prev_dim), prev_shot["camera"], 1.0)
            bg_im = Image.blend(prev_im, bg_im, alpha_xf)

        active_seg = None
        for seg in segs:
            if seg["t_start"] <= t <= seg["t_end"]:
                active_seg = seg
                break

        draw = ImageDraw.Draw(bg_im)
        char_enter_t = shots[0]["t_end"] if is_new_loc else 0.0

        if is_new_loc and t < char_enter_t:
            draw_establishing_label(draw, clip_plan["place_label"], t)
        else:
            t_char = t - char_enter_t
            char_dur = max(0.5, dur - char_enter_t)
            for c_i, ch_name in enumerate(active_chars[:2]):
                beat_idx = int(t / 2.6) + c_i
                pose_key = ["a", "b", "c", "b"][beat_idx % 4]

                is_speaking = False
                if active_seg and active_seg["speaker"] != "NARRATOR":
                    sp_char = SPEAKER_TO_CHAR.get(active_seg["speaker"], active_chars[-1])
                    if ch_name == sp_char:
                        is_speaking = True

                if is_speaking:
                    m_val = 0.5 + 0.5 * math.sin(2.0 * math.pi * 4.2 * t)
                    m_bucket = 2 if m_val > 0.65 else (1 if m_val > 0.25 else 0)
                else:
                    m_bucket = 0

                blink = ((t + c_i * 1.1) % 3.3) < 0.13
                expr = "happy" if pose_key == "b" else ("surprised" if m_bucket == 2 else "neutral")
                dim_char = bool(active_seg and active_seg["speaker"] != "NARRATOR" and not is_speaking)

                sprite = cache.get_char_sprite(ch_name, pose_key, expr, m_bucket, blink, dimmed=dim_char)
                rw, rh = sprite.size

                target_x = slots[c_i % len(slots)]
                start_x = -320 if target_x < W // 2 else W + 320
                if t_char < 0.55:
                    ep = ease_out_back(t_char / 0.55)
                    cx = start_x + (target_x - start_x) * ep
                elif (dur - t) < 0.45:
                    xp = ease_in_cubic((0.45 - (dur - t)) / 0.45)
                    cx = target_x + (start_x - target_x) * xp
                else:
                    cx = target_x + (38 if c_i == 0 else -38) * ease_out_cubic(max(0.0, min(1.0, (t_char - 4.0) / 0.55)))

                hop_arc = -42.0 * math.sin(max(0.0, min(1.0, (t_char - 4.0) / 0.55)) * math.pi) if 4.0 <= t_char <= 4.55 else 0.0
                idle_bob = 6.5 * math.sin(2.0 * math.pi * 0.65 * t + c_i)

                ground_y = 955 + int(idle_bob + hop_arc)
                sh_w = int(rw * 0.62)
                sh_im = cache.get_shadow(sh_w, 34)
                bg_im.paste(sh_im, (int(cx - sh_w // 2), 958 - 17), sh_im)

                paste_x = int(cx - rw // 2)
                paste_y = int(ground_y - rh)
                bg_im.paste(sprite, (paste_x, paste_y), sprite)

                if is_speaking:
                    words = active_seg["text"].split()
                    excerpt = " ".join(words[:4]) + ("..." if len(words) > 4 else "")
                    mouth_screen_xy = (cx, paste_y + int(rh * 0.22))
                    draw_speech_bubble(draw, excerpt, active_seg["speaker"], mouth_screen_xy)

            if not (active_seg and active_seg["speaker"] != "NARRATOR"):
                pos_side = "top-left" if slots[0] > W // 2 else "top-right"
                card_anchor = draw_callout_card(draw, card, pos_side, t_char, char_dur)
                if card_anchor and 1.2 <= t_char <= 4.8:
                    target_char_xy = (slots[0] + (-145 if slots[0] > W // 2 else 145), 650)
                    draw_hand_drawn_arrow(draw, card_anchor, target_char_xy, t_char - 1.2)

        if active_seg:
            sub_prefix = f"{active_seg['speaker']}: " if active_seg["speaker"] != "NARRATOR" else ""
            seg_p = (t - active_seg["t_start"]) / max(0.1, active_seg["duration_s"])
            draw_subtitle_bar(draw, sub_prefix + active_seg["text"], seg_p)

        rgb_out = np.asarray(bg_im, dtype=np.uint8)
        yield rgb_out, t_global

def mix_audio_for_clips(clip_plans, stem_mp3, out_wav, pad_start_s=0.0,
                        pad_end_s=0.0, music_fade_out_s=0.0):
    vo_pieces = []
    clip_sample_counts = []
    for cp in clip_plans:
        tmp = cp["file_path"] + ".tmp.wav"
        subprocess.run(["ffmpeg", "-y", "-i", cp["file_path"], "-ac", "1", "-ar", str(SR), tmp],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _, data = wavfile.read(tmp)
        os.remove(tmp)
        target_samples = max(1, int(round(cp["duration_s"] * SR)))
        data = data.astype(np.float32) / 32768.0
        if len(data) > target_samples:
            data = data[:target_samples]
        elif len(data) < target_samples:
            data = np.pad(data, (0, target_samples - len(data)))
        vo_pieces.append(data)
        clip_sample_counts.append(target_samples)

    vo_full = np.concatenate(vo_pieces)
    pad_start_samples = max(0, int(round(pad_start_s * SR)))
    pad_end_samples = max(0, int(round(pad_end_s * SR)))
    vo_full = np.pad(vo_full, (pad_start_samples, pad_end_samples))
    total_samples = len(vo_full)

    tmp_m = stem_mp3 + ".tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-i", stem_mp3, "-ac", "1", "-ar", str(SR), tmp_m],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _, m_data = wavfile.read(tmp_m)
    os.remove(tmp_m)
    m_flt = m_data.astype(np.float32) / 32768.0
    if len(m_flt) == 0:
        raise ValueError(f"Music stem contains no decoded samples: {stem_mp3}")
    if len(m_flt) < total_samples:
        reps = (total_samples // len(m_flt)) + 2
        m_flt = np.tile(m_flt, reps)
    m_flt = m_flt[:total_samples]
    fade_samples = min(total_samples, max(0, int(round(music_fade_out_s * SR))))
    if fade_samples > 1:
        m_flt[-fade_samples:] *= np.linspace(1.0, 0.0, fade_samples, dtype=np.float32)

    # Linear-time moving averages avoid the quadratic cost of np.convolve on a full-length feature.
    from scipy.ndimage import uniform_filter1d
    vo_env = uniform_filter1d(np.abs(vo_full), size=int(0.05 * SR), mode="nearest")
    duck_gain = np.where(vo_env > 0.015, 0.12, 0.24).astype(np.float32)
    duck_smooth = uniform_filter1d(duck_gain, size=int(0.15 * SR), mode="nearest")

    sfx_track = np.zeros(total_samples, dtype=np.float32)
    sfx_map = {}
    for sname in ["pop", "whoosh", "arrow"]:
        _, s_d = wavfile.read(f"production/sfx/{sname}.wav")
        sfx_map[sname] = s_d.astype(np.float32) / 32768.0

    clip_cursor = pad_start_samples
    for cp, clip_samples in zip(clip_plans, clip_sample_counts):
        w_s = clip_cursor + int(0.55 * SR)
        w_a = sfx_map["whoosh"]
        if w_s + len(w_a) <= total_samples:
            sfx_track[w_s:w_s + len(w_a)] += w_a * 0.35
        a_s = clip_cursor + int(1.25 * SR)
        a_a = sfx_map["arrow"]
        if a_s + len(a_a) <= total_samples:
            sfx_track[a_s:a_s + len(a_a)] += a_a * 0.30
        for seg in cp["vo_segments"]:
            if seg["speaker"] != "NARRATOR":
                p_s = clip_cursor + int(round(seg["t_start"] * SR))
                p_a = sfx_map["pop"]
                if p_s + len(p_a) <= total_samples:
                    sfx_track[p_s:p_s + len(p_a)] += p_a * 0.45
        clip_cursor += clip_samples

    mix = vo_full + m_flt * duck_smooth + sfx_track
    peak = np.max(np.abs(mix)) + 1e-9
    mix = mix * min(1.0, 0.707 / peak)
    wavfile.write(out_wav, SR, (mix * 32767).astype(np.int16))

def render_sequence_to_mp4(clip_plans, stem_mp3, out_mp4, report_path,
                           title_card=None, end_card=None,
                           title_duration_s=2.5, end_duration_s=2.5):
    missing = [sh["bg_path"] for cp in clip_plans for sh in cp["shots"]
               if sh.get("asset_status") != "accepted" or not os.path.isfile(sh["bg_path"])]
    for card in (title_card, end_card):
        if card and not os.path.isfile(card["bg_path"]):
            missing.append(card["bg_path"])
    if missing:
        raise ValueError(f"Render blocked: {len(missing)} unaccepted/missing production backgrounds. "
                         "Generate and QC the plates; do not substitute reference crops.")
    if not clip_plans:
        raise ValueError("Render blocked: the clip sequence is empty.")

    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)
    t0 = time.time()
    cache = AssetCache()
    tmp_wav = out_mp4 + ".audio.wav"
    with open("production/part1/part1_vo_manifest.json") as f:
        vo_man = {c["clip_id"]: c for c in json.load(f)["clips"]}

    for cp in clip_plans:
        cp["file_path"] = vo_man[cp["clip_id"]]["file_path"]

    title_frames = int(round(title_duration_s * FPS)) if title_card else 0
    end_frames = int(round(end_duration_s * FPS)) if end_card else 0
    title_duration = title_frames / float(FPS)
    end_duration = end_frames / float(FPS)
    samples_per_frame = SR // FPS
    voice_samples = sum(max(1, int(round(cp["duration_s"] * SR))) for cp in clip_plans)
    clip_video_frames = sum(max(1, int(round(cp["duration_s"] * FPS))) for cp in clip_plans)
    clip_video_samples = clip_video_frames * samples_per_frame
    frame_rounding_tail_samples = max(0, clip_video_samples - voice_samples)
    end_audio_samples = end_frames * samples_per_frame + frame_rounding_tail_samples
    mix_audio_for_clips(
        clip_plans, stem_mp3, tmp_wav,
        pad_start_s=title_duration,
        pad_end_s=end_audio_samples / float(SR),
        music_fade_out_s=min(1.25, end_duration) if end_card else 0.0
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-i", tmp_wav,
        "-c:v", "libx264", "-preset", "medium", "-crf", "25", "-maxrate", "1400k", "-bufsize", "2800k", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", out_mp4
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    prev_small = None
    frame_diffs = []

    def emit_frame(frame, t_global):
        nonlocal prev_small
        proc.stdin.write(frame.tobytes())
        # Downsampled 8x grid for quick frame-to-frame motion-diff measurement.
        cur_small = frame[::8, ::8, :].astype(np.int16)
        if prev_small is not None:
            diff = float(np.mean(np.abs(cur_small - prev_small)))
            frame_diffs.append((round(t_global, 3), round(diff, 3)))
        prev_small = cur_small

    video_frames = 0
    if title_card:
        print(f"Rendering opening title card ({title_duration:.2f}s)...", flush=True)
        for frame, t_global in render_part_card_frames(cache, title_card, title_duration, 0.0):
            emit_frame(frame, t_global)
            video_frames += 1

    for clip_index, cp in enumerate(clip_plans, start=1):
        print(f"Rendering clip {clip_index:02d}/{len(clip_plans):02d}: {cp['clip_id']}...", flush=True)
        t_offset = video_frames / float(FPS)
        for frame, t_global in render_clip_frames(cp, cache, t_offset):
            emit_frame(frame, t_global)
            video_frames += 1

    if end_card:
        print(f"Rendering Part II tease card ({end_duration:.2f}s)...", flush=True)
        t_offset = video_frames / float(FPS)
        for frame, t_global in render_part_card_frames(cache, end_card, end_duration, t_offset):
            emit_frame(frame, t_global)
            video_frames += 1

    proc.stdin.close()
    returncode = proc.wait()
    if returncode:
        raise RuntimeError(f"ffmpeg failed with exit code {returncode}; output not accepted")
    os.remove(tmp_wav)

    total_duration = video_frames / float(FPS)
    frozen_run = 0
    max_frozen_run = 0
    for _, d in frame_diffs:
        if d < 0.25:
            frozen_run += 1
            max_frozen_run = max(max_frozen_run, frozen_run)
        else:
            frozen_run = 0
    max_frozen_s = max_frozen_run / float(FPS)
    mean_diff = float(np.mean([d for _, d in frame_diffs])) if frame_diffs else 0.0
    min_diff = float(np.min([d for _, d in frame_diffs])) if frame_diffs else 0.0
    max_diff = float(np.max([d for _, d in frame_diffs])) if frame_diffs else 0.0
    elapsed = time.time() - t0

    with open(report_path, "w") as f:
        f.write(f"MOTION QC REPORT — {os.path.basename(out_mp4)}\n")
        f.write(f"Title card: {title_duration:.2f}s | Main sequence: {clip_video_frames / float(FPS):.2f}s | Tease card: {end_duration:.2f}s\n")
        f.write(f"VO audio: {voice_samples / float(SR):.3f}s; frame-rounding tail pad: {frame_rounding_tail_samples / float(SR):.3f}s\n")
        f.write(f"Total Frames: {video_frames} ({total_duration:.2f}s @ {FPS} fps) | Render Time: {elapsed:.1f}s ({total_duration/max(0.1,elapsed):.1f}x realtime)\n")
        f.write(f"Mean Frame-to-Frame Diff: {mean_diff:.3f} RGB levels/channel (Min: {min_diff:.3f}, Max: {max_diff:.3f})\n")
        f.write(f"Max Near-Zero Motion Stretch (<0.25 diff): {max_frozen_s:.2f}s (Hard Gate: <= 2.00s) -> {'PASS' if max_frozen_s <= 2.0 else 'FAIL'}\n\n")
        f.write("Sampled 1-Second Frame-Diff Curve:\n")
        for idx in range(0, len(frame_diffs), FPS):
            t_s, d_v = frame_diffs[idx]
            bar = "#" * min(40, int(d_v * 6))
            f.write(f"  t={t_s:6.2f}s | diff={d_v:6.3f} | {bar}\n")

    print(f"Rendered {out_mp4} ({total_duration:.2f}s in {elapsed:.1f}s = {total_duration/max(0.1,elapsed):.1f}x realtime) | Mean diff={mean_diff:.3f} | Max frozen={max_frozen_s:.2f}s ({'PASS' if max_frozen_s <= 2.0 else 'FAIL'})")

if __name__ == "__main__":
    raise SystemExit(
        "assemble.py is the renderer module, not a standalone preview command. "
        "Use tools/render_part1.py for the complete Part 1 export; the approved preview is preserved."
    )
