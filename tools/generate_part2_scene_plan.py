"""Build the Part 2 shot/motion plan and pending-background ledger from measured VO."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO_MANIFEST = ROOT / "production/part2/part2_vo_manifest.json"
OVERRIDE = ROOT / "production/part2/chapter7_vo_override.json"
SCENES_PATH = ROOT / "production/scenes.json"
BACKGROUND_MANIFEST = ROOT / "production/part2/background_manifest.json"

# All new named one-off characters remain static cutouts; approved rigs are reused.
SPEAKER_TO_CHAR = {
    "PROTESILAUS": "protesilaus",
    "PHILOCTETES": "philoctetes",
    "ODYSSEUS": "odysseus",
    "ACHILLES": "achilles",
    "AGAMEMNON": "agamemnon",
    "CHRYSES": "chryses",
    "HELEN": "helen",
    "PARIS": "paris",
    "MENELAUS": "menelaus",
    "ANDROMACHE": "andromache_astyanax",
    "HECTOR": "hector",
    "PATROCLUS": "patroclus",
}

# Existing location sheets supply approved palette/architecture references.
CLIP_DESIGNS = [
    {"location": "loc_troy", "label": "TROY SHORE — AEGEAN COAST", "theme": "Bronze Age Greek fleet approaching the long beach below Troy; empty shore, distant city walls and oared ships", "headline": "THE FIRST ASHORE", "emphasis": "FIRST", "chips": ["PROTESILAUS", "TROY SHORE", "A FATAL TRADITION"], "defaults": ["protesilaus"], "protected": ["distant fleet", "open shoreline"]},
    {"location": "loc_lemnos", "reference": "loc_camp", "label": "LEMNOS — ISLAND OF EXILE", "theme": "Quiet rocky Aegean island shore used as the remote setting of Lemnos; low cliffs, sparse scrub and a sheltered cove", "headline": "ABANDONED ON LEMNOS", "emphasis": "LEMNOS", "chips": ["PHILOCTETES", "HIS BOW", "LEFT BEHIND"], "defaults": ["philoctetes"], "protected": ["bow", "open beach foreground"]},
    {"location": "loc_troy", "label": "TROY — THE LONG WAR", "theme": "Ancient Trojan plain and monumental city walls, years of siege suggested by weathered stone and distant empty encampments", "headline": "HERACLES'S BOW", "emphasis": "BOW", "chips": ["PHILOCTETES", "LEMNOS", "A FUTURE WEAPON"], "defaults": ["odysseus", "mascot"], "protected": ["bow", "Troy's walls"]},
    {"location": "loc_troy", "label": "TROY — THE CITY WALLS", "theme": "Great stone walls of Troy, bronze-age towers above a broad empty plain, distant Greek camp and traces of repeated raids", "headline": "POSEIDON & APOLLO", "emphasis": "GODS", "chips": ["TROY'S WALLS", "UNPAID DEBT", "YEARS OF RAIDS"], "defaults": ["hector", "mascot"], "protected": ["city wall silhouette", "open foreground"]},
    {"location": "loc_camp", "label": "GREEK CAMP — TROY", "theme": "Greek camp on the windy Aegean beach, orderly tents, beached ships and a long view toward distant Troy", "headline": "NINE YEARS OF NOTHING", "emphasis": "NINE YEARS", "chips": ["TROY STILL STANDS", "THE TENTH YEAR", "AN ARGUMENT AHEAD"], "defaults": ["achilles", "mascot"], "protected": ["Greek ships", "camp tent line"]},
    {"location": "loc_camp", "label": "GREEK CAMP — THE PLAGUE", "theme": "Greek camp under ominous skies, empty tents and extinguished braziers suggesting a plague; no people or bodies", "headline": "PLAGUE AT THE CAMP", "emphasis": "PLAGUE", "chips": ["CHRYSEIS", "APOLLO", "NINE DAYS"], "defaults": ["chryses"], "supporting_characters": ["agamemnon"], "protected": ["camp tents", "unmarked altar"]},
    {"location": "loc_camp", "label": "GREEK CAMP — AGAMEMNON'S TENT", "theme": "Bronze Age command tent in the Greek camp, simple war standards, bronze weapons kept low and unobtrusive, tense torchlight", "headline": "BRISEIS IS TAKEN", "emphasis": "TAKEN", "chips": ["AGAMEMNON", "ACHILLES", "A BROKEN ALLIANCE"], "defaults": ["agamemnon", "achilles"], "protected": ["empty command tent", "bronze helmet"]},
    {"location": "loc_camp", "label": "GREEK CAMP — THE QUARREL", "theme": "Interior of a large Greek command tent opening onto the Aegean camp, dramatic shafts of amber light, no figures", "headline": "THE ARGUMENT", "emphasis": "ARGUMENT", "chips": ["KING VS WARRIOR", "A SWORD HELD BACK"], "defaults": ["achilles", "agamemnon"], "protected": ["sheathed sword", "tent entrance"]},
    {"location": "loc_camp", "label": "GREEK CAMP — ACHILLES'S TENT", "theme": "Secluded tent at the edge of the Greek camp, tide-worn shore and quiet ships beyond, reflective dusk", "headline": "ACHILLES WALKS AWAY", "emphasis": "WALKS AWAY", "chips": ["HIS MOTHER", "ZEUS", "A TERRIBLE REQUEST"], "defaults": ["achilles", "mascot"], "protected": ["tent opening", "distant fleet"]},
    {"location": "loc_olympus", "label": "OLYMPUS — THE GODS TURN THE TIDE", "theme": "Mythic Mount Olympus above cloud and sea, restrained gold light over ancient marble terraces, no figures", "headline": "ZEUS TURNS THE TIDE", "emphasis": "TIDE", "chips": ["A PRAYER ANSWERED", "THE WAR SHIFTS"], "defaults": ["achilles", "mascot"], "protected": ["marble terrace", "storm-lit horizon"]},
    {"location": "loc_troy", "label": "TROY — THE DUEL", "theme": "Open ground before Troy's walls prepared for a single combat, broad empty space between two distant standards", "headline": "PARIS VS MENELAUS", "emphasis": "DUEL", "chips": ["SINGLE COMBAT", "HELEN AT STAKE"], "defaults": ["paris", "menelaus"], "protected": ["open duel ground", "distant city gate"]},
    {"location": "loc_troy", "label": "TROY — THE WALLS", "theme": "High Trojan ramparts seen from a shaded parapet, pale Aegean mist over the distant plain", "headline": "APHRODITE INTERVENES", "emphasis": "MIST", "chips": ["PARIS SAVED", "THE DUEL INTERRUPTED"], "defaults": ["paris", "menelaus"], "protected": ["parapet", "misty horizon"]},
    {"location": "loc_troy", "label": "TROY — HELEN'S CHAMBER", "theme": "Quiet upper chamber in ancient Troy overlooking the walls, woven cloth, bronze lamp and empty window opening", "headline": "HELEN'S ANGER", "emphasis": "ALIVE", "chips": ["HELEN", "PARIS", "TRUCE BROKEN"], "defaults": ["helen"], "supporting_characters": ["paris"], "protected": ["window opening", "bronze lamp"]},
    {"location": "loc_troy", "label": "TROY — HECTOR COMES HOME", "theme": "A sheltered inner courtyard near the Trojan gate, warm stone, olive branches and a quiet path from the walls", "headline": "HECTOR COMES HOME", "emphasis": "HOME", "chips": ["WIFE AND SON", "TROY", "FAREWELL"], "defaults": ["hector", "andromache_astyanax"], "protected": ["courtyard path", "open lower ground"]},
    {"location": "loc_troy", "label": "TROY — THE FAREWELL", "theme": "Private Trojan courtyard with a low stone bench, warm lamp and the city gate visible beyond", "headline": "A GOODBYE", "emphasis": "GOODBYE", "chips": ["ANDROMACHE", "HECTOR", "ASTYANAX"], "defaults": ["andromache_astyanax", "hector"], "protected": ["stone bench", "lamp"]},
    {"location": "loc_troy", "label": "TROY — A FATHER'S HELMET", "theme": "Sunlit Trojan doorway and courtyard, a small bronze helmet resting safely on the stone floor, calm family interior", "headline": "A FATHER'S HELMET", "emphasis": "HELMET", "chips": ["A CHILD'S FEAR", "A QUIET MOMENT"], "defaults": ["hector", "andromache_astyanax"], "supporting_characters": ["andromache_astyanax"], "protected": ["small helmet", "clear floor"]},
    {"location": "loc_troy", "label": "TROY — BEFORE THE FALL", "theme": "Distant Trojan walls at late afternoon, empty parapet and a long shadow reaching across the plain", "headline": "WITHOUT ACHILLES", "emphasis": "WITHOUT", "chips": ["GREEKS STRUGGLE", "ENVOYS SENT", "HOMEWARD?"], "defaults": ["achilles", "odysseus", "mascot"], "protected": ["Troy wall", "empty plain"]},
    {"location": "loc_camp", "label": "GREEK CAMP — THE BEACH", "theme": "Greek beach camp at first light, one empty ship with a small controlled fire in the distance, no people", "headline": "THE BEACH BURNS", "emphasis": "BURNS", "chips": ["A GREEK SHIP", "PATROCLUS", "THE TROJANS ADVANCE"], "defaults": ["patroclus", "hector"], "protected": ["ship silhouette", "clear beach"]},
    {"location": "loc_camp", "label": "GREEK CAMP — THE ARMOR", "theme": "Inside Achilles's tent: a neat bronze armor stand, shield, spear and open doorway to the beach, no people", "headline": "THE ARMOR", "emphasis": "ARMOR", "chips": ["ACHILLES", "PATROCLUS", "ONE RULE"], "defaults": ["achilles", "patroclus"], "protected": ["armor stand", "shield"]},
    {"location": "loc_troy", "label": "THE PLAIN BEFORE TROY", "theme": "Battle-scarred but empty plain between the Greek ships and Troy's walls, dropped unmarked shield and distant river, no bodies", "headline": "PATROCLUS FALLS", "emphasis": "PATROCLUS", "chips": ["APOLLO", "HECTOR", "A TRAGIC TURN"], "defaults": ["patroclus", "hector"], "protected": ["empty path to walls", "unmarked helmet"]},
    {"location": "loc_camp", "label": "GREEK CAMP — NEW ARMOR", "theme": "Quiet Greek camp after battle, new bronze armor and an ornate round shield resting under warm lamplight", "headline": "HEPHAESTUS'S SHIELD", "emphasis": "SHIELD", "chips": ["NEW ARMOR", "ACHILLES RETURNS"], "defaults": ["achilles", "mascot"], "protected": ["round shield", "armor stand"]},
    {"location": "loc_troy", "label": "SCAMANDER — OUTSIDE TROY", "theme": "Ancient river Scamander beside the Trojan plain, high water and foaming currents, firelit cloud reflections, no bodies or figures", "headline": "SCAMANDER RISES", "emphasis": "RIVER", "chips": ["A GOD'S ANGER", "THE TROJANS FLEE"], "defaults": ["achilles", "mascot"], "protected": ["river channel", "stone bank"]},
    {"location": "loc_troy", "label": "TROY — THE CHASE", "theme": "Broad circuit outside Troy's high gates with a dusty path curving along the walls, stormy dusk and no figures", "headline": "THE CHASE", "emphasis": "CHASE", "chips": ["HECTOR", "ATHENA", "ONE LAST DUEL"], "defaults": ["hector", "achilles"], "supporting_characters": ["achilles"], "protected": ["curving path", "city gate"]},
    {"location": "loc_camp", "label": "GREEK CAMP — PATROCLUS'S TOMB", "theme": "A quiet memorial mound near the Greek camp at dawn, an unmarked chariot track circling the tomb, no person or body", "headline": "TWELVE DAYS", "emphasis": "TWELVE DAYS", "chips": ["ACHILLES", "PATROCLUS'S TOMB", "HECTOR"], "defaults": ["achilles", "mascot"], "protected": ["memorial mound", "chariot track"]},
]

SHOT_CYCLE = [
    ("establishing", "dolly-in", "panoramic coastline or landscape, low horizon and clear empty foreground"),
    ("wide", "pan-right", "oblique wide view from a different axis, layered terrain and distant architecture"),
    ("medium", "pull-back", "medium environment detail with a single symbolic prop or architectural feature"),
    ("detail", "pan-left", "close environmental detail at ground level, no figures, visually distinct composition"),
    ("wide", "dolly-in", "reverse wide angle at a different time of day, atmospheric depth and open staging space"),
    ("medium", "pan-up", "raised three-quarter view that reveals a new spatial layer and an unobstructed foreground"),
    ("detail", "pull-back", "low side-angle environmental insert with distinct leading lines and a restrained focal object"),
    ("wide", "pan-left", "distant reverse view with atmospheric haze, changed light, and generous negative space"),
]

CHARACTER_ASSET_REQUIREMENTS = {
    "protesilaus": {"kind": "static cutout", "status": "new character sheet approval required", "voice": "PROTESILAUS"},
    "philoctetes": {"kind": "static cutout", "status": "new character sheet approval required", "voice": "PHILOCTETES"},
    "chryses": {"kind": "static cutout", "status": "new character sheet approval required", "voice": "CHRYSES"},
    "patroclus": {"kind": "static cutout", "status": "new character sheet approval required", "voice": "PATROCLUS"},
    "andromache_astyanax": {"kind": "combined static cutout", "status": "new character sheet approval required", "voice": "ANDROMACHE", "note": "Andromache holding swaddled infant Astyanax; infant has no dialogue."},
}


def build_prompt(design: dict, shot_index: int, shot_type: str, view: str) -> str:
    unique_detail = [
        "keep the shoreline clear and place only the setting's distant landmarks along the horizon",
        "frame dominant architecture or landforms from an offset axis with open negative space",
        "focus on surface texture and a small unmarked material detail belonging to this setting",
        "use close ground-level geology or architecture for depth without cluttering the lower third",
        "shift to softer evening light and a reverse composition without adding new props",
        "reveal a raised oblique spatial layer distinct from prior frames; keep open staging ground",
        "use a restrained environmental insert; do not invent objects that contradict the location",
        "finish on a distant reverse view with atmospheric depth, changed light, and location continuity",
    ][(shot_index - 1) % len(SHOT_CYCLE)]
    return (
        f"One standalone 16:9 cinematic painterly-realistic HYBRID background for {design['theme']}. "
        f"{shot_type.capitalize()} composition: {view}; {unique_detail}. Match the approved "
        f"{design.get('reference', design['location'])} location-sheet palette and Bronze Age materials. "
        "Warm ochre, weathered stone, bronze and deep sea blues; soft atmospheric depth; level open ground "
        "in the lower third for later 2D character cutouts. No people, faces, silhouettes, bodies, text, "
        "letters, numbers, inscriptions, logos, watermarks, modern objects, or layout guides."
    )


def main():
    manifest = json.loads(VO_MANIFEST.read_text())
    override = json.loads(OVERRIDE.read_text())
    if manifest["clip_count"] != len(CLIP_DESIGNS):
        raise ValueError(f"Expected {len(CLIP_DESIGNS)} Part 2 clip designs; VO manifest has {manifest['clip_count']}.")
    if override.get("source_script_modified") is not False:
        raise ValueError("The approved source script must remain unchanged.")

    global_scenes = json.loads(SCENES_PATH.read_text())
    background_manifest = json.loads(BACKGROUND_MANIFEST.read_text()) if BACKGROUND_MANIFEST.exists() else {"part": 2, "plates": []}
    existing_plates = {(p["clip_id"], p["shot_index"]): p for p in background_manifest.get("plates", [])}
    accepted_statuses = {"accepted"}
    seen_locations = set()
    previous_location = None
    part2_clips = []
    planned_plates = []

    for clip_index, (clip, design) in enumerate(zip(manifest["clips"], CLIP_DESIGNS)):
        clip_id = clip["clip_id"]
        if clip_id != f"p2_clip_{clip_index + 1:02d}":
            raise ValueError(f"Nonsequential Part 2 clip id: {clip_id}")
        location_id = design["location"]
        is_new_location = location_id != previous_location
        previous_location = location_id
        seen_locations.add(location_id)

        dialogue_bubbles = []
        active_characters = []
        for segment in clip["segments"]:
            if segment["speaker"] != "NARRATOR":
                char = SPEAKER_TO_CHAR.get(segment["speaker"])
                if not char:
                    raise ValueError(f"Missing speaker-to-character mapping: {segment['speaker']}")
                if char not in active_characters:
                    active_characters.append(char)
                words = segment["text"].split()
                excerpt = " ".join(words[:4]) + ("..." if len(words) > 4 else "")
                dialogue_bubbles.append({
                    "speaker": segment["speaker"], "char": char, "bubble_text": excerpt,
                    "t_start": segment["t_start"], "t_end": segment["t_end"],
                    "source_line_index": segment["line_index"],
                })
        if not active_characters:
            active_characters = list(design["defaults"])
        for character in design.get("supporting_characters", []):
            if character not in active_characters:
                active_characters.append(character)

        duration = clip["duration_s"]
        # Keep Preset A's lively ~2–4 s visual turnover on unusually long VO clips.
        # The 23.678 s clip receives eight plates (~2.96 s each) instead of stretching five to 4.74 s.
        shot_count = 8 if duration > 20.0 else 5
        shot_duration = duration / shot_count
        shots = []
        for shot_index in range(1, shot_count + 1):
            shot_type, camera, view = SHOT_CYCLE[(clip_index + shot_index - 1) % len(SHOT_CYCLE)]
            if shot_index == 1 and is_new_location:
                shot_type, camera, view = "establishing", "dolly-in", SHOT_CYCLE[0][2]
            t_start = round((shot_index - 1) * shot_duration, 3)
            t_end = round(shot_index * shot_duration, 3) if shot_index < 5 else duration
            bg_path = f"production/part2/backgrounds/{clip_id}_bg_{shot_index:02d}.jpg"
            reference_key = design.get("reference", location_id)
            reference_path = f"production/assets/locations/{reference_key}_ref.png"
            if not (ROOT / reference_path).is_file():
                raise FileNotFoundError(f"Missing approved location reference: {reference_path}")
            plate_record = existing_plates.get((clip_id, shot_index))
            if plate_record and plate_record.get("path") != bg_path:
                raise ValueError(f"Background manifest path conflict for {clip_id} shot {shot_index}.")
            if plate_record and plate_record.get("qc_status") in accepted_statuses:
                asset_status = "accepted"
                shot_location = plate_record.get("location", location_id)
                prompt = plate_record.get("image_prompt", build_prompt(design, shot_index, shot_type, view))
            else:
                asset_status = "pending_generation"
                shot_location = location_id
                prompt = build_prompt(design, shot_index, shot_type, view)

            overlapping = [segment for segment in clip["segments"]
                           if segment["t_start"] < t_end and segment["t_end"] > t_start]
            shot = {
                "shot_index": shot_index,
                "t_start": t_start,
                "t_end": t_end,
                "location": shot_location,
                "shot_type": shot_type,
                "bg_path": bg_path,
                "image_prompt": prompt,
                "reference_path": reference_path,
                "setting_label": design["label"],
                "composition": {"view": view, "open_lower_third": True},
                "protected_objects": design["protected"],
                "asset_status": asset_status,
                "speaker_events": [
                    {"speaker": segment["speaker"], "t_start": segment["t_start"], "t_end": segment["t_end"],
                     "line_index": segment["line_index"]}
                    for segment in overlapping
                ],
                "camera": camera,
                "characters": [] if shot_index == 1 and is_new_location else active_characters,
                "speaker": ("narrator" if overlapping[0]["speaker"] == "NARRATOR" else overlapping[0]["speaker"]) if overlapping else "narrator",
                "bubble_text": next((bubble["bubble_text"] for bubble in dialogue_bubbles
                                      if bubble["t_start"] < t_end and bubble["t_end"] > t_start), ""),
                "overlay_text": design["label"] if shot_index == 1 and is_new_location else design["headline"],
                "emphasis_word": design["emphasis"],
                "chips": design["chips"],
                "text_style": "label" if shot_index == 1 and is_new_location else ("bubble" if overlapping and any(s["speaker"] != "NARRATOR" for s in overlapping) else "card"),
                "text_position": "bottom-left" if shot_index == 1 and is_new_location else ("top-left" if clip_index % 2 == 0 else "top-right"),
                "mascot": {"pose": "pose_b" if clip_index % 2 == 0 else "pose_c", "side": "left" if clip_index % 2 == 0 else "right"} if "mascot" in active_characters else "none",
                "arrow_target": design["protected"][0] if design["protected"] else "center",
                "dim_background": shot_index == 3 or bool(dialogue_bubbles),
                "sfx": "pop" if any(s["speaker"] != "NARRATOR" for s in overlapping) else ("whoosh" if shot_index == 2 else "arrow" if shot_index == 4 else "none"),
            }
            shots.append(shot)
            if not plate_record or plate_record.get("qc_status") not in accepted_statuses:
                planned_plates.append({
                    "clip_id": clip_id,
                    "shot_index": shot_index,
                    "path": bg_path,
                    "location": location_id,
                    "shot_type": shot_type,
                    "reference": reference_path,
                    "image_prompt": prompt,
                    "dimensions": None,
                    "sha256": None,
                    "qc_status": "pending_generation",
                    "qc_note": "Awaiting image generation and individual visual review; backgrounds must contain no people or text.",
                    "composition": {"view": view, "open_lower_third": True},
                    "protected_objects": design["protected"],
                })

        card = {
            "headline": design["headline"],
            "emphasis": design["emphasis"],
            "chips": design["chips"],
            "style": "card",
        }
        part2_clips.append({
            "clip_id": clip_id,
            "chapter": clip["chapter"],
            "duration_s": clip["duration_s"],
            "is_new_location": is_new_location,
            "place_label": design["label"],
            "location": location_id,
            "active_characters": active_characters,
            "dialogue_bubbles": dialogue_bubbles,
            "overlay_card": card,
            "shots": shots,
            "vo_segments": clip["segments"],
            "character_asset_requirements": sorted({
                character for character in active_characters if character in CHARACTER_ASSET_REQUIREMENTS
            }),
        })

    global_scenes["part2_clips"] = part2_clips
    global_scenes["part2_character_asset_requirements"] = CHARACTER_ASSET_REQUIREMENTS
    SCENES_PATH.write_text(json.dumps(global_scenes, indent=2, ensure_ascii=False) + "\n")

    # Refresh pending prompt metadata when the plan changes, but never reset or overwrite an accepted plate.
    by_key = {(p["clip_id"], p["shot_index"]): p for p in background_manifest.get("plates", [])}
    for record in planned_plates:
        key = (record["clip_id"], record["shot_index"])
        if by_key.get(key, {}).get("qc_status") == "accepted":
            continue
        by_key[key] = record
    background_manifest.update({
        "part": 2,
        "schema_version": 1,
        "total_planned": sum(len(clip["shots"]) for clip in part2_clips),
        "accepted": sum(1 for p in by_key.values() if p.get("qc_status") == "accepted"),
        "pending": sum(1 for p in by_key.values() if p.get("qc_status") != "accepted"),
        "plates": sorted(by_key.values(), key=lambda p: (int(p["clip_id"][-2:]), p["shot_index"])),
        "note": "Part 2 background plates are planned from measured VO; accept only after individual visual review.",
    })
    BACKGROUND_MANIFEST.write_text(json.dumps(background_manifest, indent=2, ensure_ascii=False) + "\n")

    print(f"Saved {len(part2_clips)} Part 2 clips and {sum(len(clip['shots']) for clip in part2_clips)} shot entries to {SCENES_PATH.relative_to(ROOT)}")
    print(f"Part 2 plate ledger: {background_manifest['accepted']} accepted / {background_manifest['pending']} pending")
    print(f"New static character cutouts needing approval: {', '.join(CHARACTER_ASSET_REQUIREMENTS)}")


if __name__ == "__main__":
    main()
