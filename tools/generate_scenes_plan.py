import json
import os

with open("production/part1/part1_vo_manifest.json") as f:
    p1_vo = json.load(f)

# Map chapters to primary location & character ensembles
chapter_meta = {
    "[COLD OPEN]": {
        "location": "loc_troy",
        "place_label": "TROY (HISARLIK) — 1180 BC",
        "default_chars": ["mascot", "achilles", "hector"],
        "overlay_cards": [
            {"headline": "3,200 YEARS AGO", "emphasis": "3,200", "chips": ["WINDY HILL", "BURNED RUINS", "MYTH VS FACT"], "style": "card"},
            {"headline": "ONE GOLDEN APPLE", "emphasis": "GOLDEN", "chips": ["POETRY", "SHOVEL WORK", "1200 SHIPS"], "style": "keyword"},
        ]
    },
    "[CHAPTER 1: THE UNINVITED GUEST]": {
        "location": "loc_olympus",
        "place_label": "MOUNT OLYMPUS & MOUNT IDA",
        "default_chars": ["mascot", "paris", "helen"],
        "overlay_cards": [
            {"headline": "WEDDING OF PELEUS & THETIS", "emphasis": "PROPHECY", "chips": ["GREATER SON", "MORTAL GROOM"], "style": "card"},
            {"headline": "ERIS: UNINVITED GUEST", "emphasis": "UNINVITED", "chips": ["GODDESS OF STRIFE", "GOLDEN APPLE"], "style": "keyword"},
            {"headline": "FOR THE MOST BEAUTIFUL", "emphasis": "BEAUTIFUL", "chips": ["HERA", "ATHENA", "APHRODITE"], "style": "card"},
            {"headline": "JUDGMENT OF PARIS", "emphasis": "PARIS", "chips": ["MOUNT IDA", "SECRET PRINCE", "HELEN"], "style": "card"},
        ]
    },
    "[CHAPTER 2: THE OATH]": {
        "location": "loc_palace",
        "place_label": "ROYAL PALACE OF SPARTA",
        "default_chars": ["odysseus", "menelaus", "agamemnon", "helen", "paris"],
        "overlay_cards": [
            {"headline": "THE OATH OF TYNDAREUS", "emphasis": "OATH", "chips": ["SUITORS OF HELEN", "ODYSSEUS'S PLAN"], "style": "card"},
            {"headline": "SWORN ON A SACRIFICED HORSE", "emphasis": "HORSE", "chips": ["DEFEND THE MARRIAGE", "MENELAUS CHOSEN"], "style": "keyword"},
            {"headline": "HELEN TAKEN FROM SPARTA", "emphasis": "SPARTA", "chips": ["PARIS THE GUEST", "OATH CALLED IN"], "style": "card"},
        ]
    },
    "[CHAPTER 3: THE FLEET AT AULIS]": {
        "location": "loc_aulis",
        "place_label": "HARBOR OF AULIS — GREECE",
        "default_chars": ["odysseus", "achilles", "agamemnon"],
        "overlay_cards": [
            {"headline": "ODYSSEUS PLOWS SALT", "emphasis": "SALT", "chips": ["FEIGNING MADNESS", "PALAMEDES'S TEST"], "style": "card"},
            {"headline": "ACHILLES ON SKYROS", "emphasis": "ACHILLES", "chips": ["SHORT GLORIOUS LIFE", "FATED TO DIE"], "style": "keyword"},
            {"headline": "1,200 SHIPS — NO WIND", "emphasis": "AULIS", "chips": ["ARTEMIS ANGRY", "IPHIGENIA"], "style": "card"},
            {"headline": "THE FLEET SAILS FOR TROY", "emphasis": "SAILS", "chips": ["WIND RISES", "CLYTEMNESTRA WAITS"], "style": "keyword"},
        ]
    }
}

shot_cycle = [
    ("establishing", "wide", "dolly-in"),
    ("wide", "med", "pan-right"),
    ("medium", "detail", "pull-back"),
    ("detail", "wide", "pan-left"),
    ("wide", "night", "dolly-in"),
]

speaker_to_char = {
    "MASCOT": "mascot",
    "ACHILLES": "achilles",
    "ODYSSEUS": "odysseus",
    "AGAMEMNON": "agamemnon",
    "HECTOR": "hector",
    "PARIS": "paris",
    "HELEN": "helen",
    "MENELAUS": "menelaus",
    "PRIAM": "priam",
    "TYNDAREUS": "priam",
    "ZEUS": "agamemnon",
    "PALAMEDES": "odysseus",
    "CALCHAS": "priam",
    "ERIS": "helen",
    "HERA": "helen",
    "ATHENA": "helen",
    "APHRODITE": "helen",
    "THETIS": "helen",
    "IPHIGENIA": "helen",
}

scenes_plan = {
    "project": "THE TROJAN WAR: THE FULL STORY (Hybrid v3)",
    "style_mode": "HYBRID",
    "preset": "A — LIVELY EXPLAINER",
    "accent_color": "#9B3A12",
    "font": "production/fonts/DisplaySerif-Bold.ttf",
    "part1_clips": []
}

seen_locations = set()

for c_idx, clip in enumerate(p1_vo["clips"]):
    chap = clip["chapter"]
    meta = chapter_meta[chap]
    loc = meta["location"]
    is_new_loc = loc not in seen_locations
    if is_new_loc:
        seen_locations.add(loc)

    dur = clip["duration_s"]
    # 5 background shots per clip (~3-4s each, Preset A schedule)
    n_shots = 5
    shot_dur = round(dur / n_shots, 3)

    # Identify active speakers in this clip
    segs = clip["segments"]
    active_chars = []
    for s in segs:
        sp = s["speaker"]
        if sp != "NARRATOR":
            ch = speaker_to_char.get(sp, "mascot")
            if ch not in active_chars:
                active_chars.append(ch)
    if not active_chars:
        # Pick 1-2 recurring characters from chapter default
        dchars = meta["default_chars"]
        active_chars = [dchars[c_idx % len(dchars)]]
        if c_idx % 2 == 1 and len(dchars) > 1:
            active_chars.append(dchars[(c_idx + 1) % len(dchars)])

    card_list = meta["overlay_cards"]
    card = card_list[c_idx % len(card_list)]

    # Check if any segment is dialogue to extract 2-5 word bubble_text
    dialogue_bubbles = []
    for s in segs:
        if s["speaker"] != "NARRATOR":
            words = s["text"].split()
            excerpt = " ".join(words[:4]) + ("..." if len(words) > 4 else "")
            dialogue_bubbles.append({
                "speaker": s["speaker"],
                "char": speaker_to_char.get(s["speaker"], "mascot"),
                "bubble_text": excerpt,
                "t_start": s["t_start"],
                "t_end": s["t_end"]
            })

    shots = []
    for s_i in range(n_shots):
        stype, angle_suffix, cam = shot_cycle[(c_idx + s_i) % len(shot_cycle)]
        if s_i == 0 and is_new_loc:
            stype = "establishing"
            angle_suffix = "wide"
            cam = "dolly-in"
        bg_file = f"production/assets/locations/{loc}_{angle_suffix}.jpg"
        shots.append({
            "shot_index": s_i + 1,
            "t_start": round(s_i * shot_dur, 3),
            "t_end": round((s_i + 1) * shot_dur if s_i < n_shots - 1 else dur, 3),
            "location": loc,
            "shot_type": stype,
            "bg_path": bg_file,
            "image_prompt": f"{meta['place_label']}, {stype} shot, Bronze Age architecture, warm golden-hour color grade, open foreground ground, no people, no text, 16:9",
            "camera": cam,
            "characters": [] if (s_i == 0 and is_new_loc) else active_chars,
            "speaker": dialogue_bubbles[0]["speaker"] if dialogue_bubbles else "narrator",
            "bubble_text": dialogue_bubbles[0]["bubble_text"] if dialogue_bubbles else "",
            "overlay_text": meta["place_label"] if (s_i == 0 and is_new_loc) else card["headline"],
            "emphasis_word": card["emphasis"],
            "chips": card["chips"],
            "text_style": "label" if (s_i == 0 and is_new_loc) else ("bubble" if dialogue_bubbles else card["style"]),
            "text_position": "bottom-left" if (s_i == 0 and is_new_loc) else ("top-left" if c_idx % 2 == 0 else "top-right"),
            "mascot": {"pose": "pose_b" if c_idx % 2 == 0 else "pose_c", "side": "left" if c_idx % 2 == 0 else "right"} if ("mascot" in active_chars or c_idx % 3 == 0) else "none",
            "arrow_target": active_chars[0] if active_chars else "center",
            "dim_background": True if (s_i == 2 or dialogue_bubbles) else False,
            "sfx": "pop" if dialogue_bubbles else ("whoosh" if s_i == 1 else "arrow" if s_i == 3 else "none")
        })

    scenes_plan["part1_clips"].append({
        "clip_id": clip["clip_id"],
        "chapter": chap,
        "duration_s": dur,
        "is_new_location": is_new_loc,
        "place_label": meta["place_label"],
        "active_characters": active_chars,
        "dialogue_bubbles": dialogue_bubbles,
        "overlay_card": card,
        "shots": shots,
        "vo_segments": segs
    })

with open("production/scenes.json", "w") as f:
    json.dump(scenes_plan, f, indent=2)

print(f"Saved production/scenes.json with {len(scenes_plan['part1_clips'])} clips ({len(scenes_plan['part1_clips'])*5} background shot entries)")
