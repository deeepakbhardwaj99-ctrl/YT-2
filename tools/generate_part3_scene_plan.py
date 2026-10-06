"""Build the Part 3 shot/motion plan and pending-background ledger from measured VO."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO_MANIFEST = ROOT / "production/part3/part3_vo_manifest.json"
OVERRIDE = ROOT / "production/part3/chapter9_vo_override.json"
SCENES_PATH = ROOT / "production/scenes.json"
BACKGROUND_MANIFEST = ROOT / "production/part3/background_manifest.json"

# One-off Chapter 9–10 speakers reuse already-approved visual archetypes/cutouts.
# Their exact speaker names remain in subtitles and dialogue bubbles; proxy use is
# recorded explicitly so no unapproved character art is introduced.
SPEAKER_TO_CHAR = {
    "PRIAM": "priam",
    "ACHILLES": "achilles",
    "AJAX": "agamemnon",
    "ODYSSEUS": "odysseus",
    "HELENUS": "priam",
    "OENONE": "helen",
    "EPEIUS": "agamemnon",
    "TROJAN": "hector",
    "ANOTHER TROJAN": "priam",
    "THIRD TROJAN": "hector",
    "LAOCOON": "priam",
    "SINON": "agamemnon",
    "CASSANDRA": "helen",
    "CROWD": "hector",
    "HELEN": "helen",
    "PHILOCTETES": "philoctetes",
    "PARIS": "paris",
}

SPEAKER_VISUAL_MAPPING = {
    "PRIAM": {"character": "priam", "mapping": "exact approved cutout"},
    "ACHILLES": {"character": "achilles", "mapping": "exact approved rig"},
    "ODYSSEUS": {"character": "odysseus", "mapping": "exact approved rig"},
    "HELEN": {"character": "helen", "mapping": "exact approved cutout"},
    "AJAX": {"character": "agamemnon", "mapping": "approved Greek-warrior proxy; not a literal portrait"},
    "HELENUS": {"character": "priam", "mapping": "approved Trojan-elder proxy; not a literal portrait"},
    "OENONE": {"character": "helen", "mapping": "approved Trojan-woman proxy; not a literal portrait"},
    "EPEIUS": {"character": "agamemnon", "mapping": "approved Greek-male proxy; not a literal portrait"},
    "TROJAN": {"character": "hector", "mapping": "approved generic-Trojan proxy"},
    "ANOTHER TROJAN": {"character": "priam", "mapping": "approved generic-Trojan proxy"},
    "THIRD TROJAN": {"character": "hector", "mapping": "approved generic-Trojan proxy"},
    "LAOCOON": {"character": "priam", "mapping": "approved Trojan-elder proxy; not a literal portrait"},
    "SINON": {"character": "agamemnon", "mapping": "approved Greek-male proxy; not a literal portrait"},
    "CASSANDRA": {"character": "helen", "mapping": "approved Trojan-woman proxy; not a literal portrait"},
    "CROWD": {"character": "hector", "mapping": "approved generic-Trojan group proxy"},
    "PHILOCTETES": {"character": "philoctetes", "mapping": "exact approved static cutout"},
    "PARIS": {"character": "paris", "mapping": "exact approved cutout"},
}

# Part 3's 24 measured clips are matched to the narrative beats in order.
# Background plates remain environment-only; character cutouts are composited later.
CLIP_DESIGNS = [
    {"location": "loc_camp", "label": "GREEK CAMP — THE NIGHT APPROACH", "night": True, "additional_prompt_constraints": "No carts, chariots, wagons, wheeled vehicles, or extra furniture; keep the lower third as open sand.", "theme": "A quiet Bronze Age Greek beach camp at night, a moonlit sandy path between low canvas command tents and dark braziers, the Aegean barely visible beyond; completely empty", "headline": "PRIAM CROSSES THE PLAIN", "emphasis": "PRIAM", "chips": ["AN OLD KING", "A RANSOM", "ONE LAST NIGHT"], "defaults": ["priam", "mascot"], "protected": ["moonlit path", "command tent entrance"]},
    {"location": "loc_camp", "label": "GREEK CAMP — ACHILLES'S TENT", "interior": True, "night": True, "additional_prompt_constraints": "Clearly show the scene from inside an enclosed command tent, with canvas roof and side walls framing the view; limit the outside to the dark doorway; no wide exterior beach or camp vista.", "theme": "A deep-night interior of a plain Bronze Age Greek command tent beside the sea, warm bronze oil-lamp glow, open tent entrance onto a dark moonlit Aegean, a low stool and folded undyed linen; no occupants or daylight", "headline": "A FATHER'S PLEA", "emphasis": "FATHER'S", "chips": ["PRIAM", "ACHILLES", "PITY FOR AN ENEMY"], "defaults": ["priam", "achilles"], "supporting_characters": ["achilles"], "protected": ["open tent entrance", "low stool"]},
    {"location": "loc_camp", "label": "GREEK CAMP — A SHARED MEAL", "interior": True, "night": True, "additional_prompt_constraints": "This scene continues the same night as Priam's arrival: if the entrance is visible, show only deep blue-black night beyond it, never daylight, dawn or a bright sky.", "theme": "An empty nighttime interior of a spare Bronze Age Greek tent, a low wooden table, two simple bowls, folded linen and one warm bronze oil lamp, quiet and unoccupied", "headline": "SHARED GRIEF", "emphasis": "GRIEF", "chips": ["TWO FATHERS", "A SHARED MEAL", "MOURNING"], "defaults": ["achilles", "priam"], "supporting_characters": ["priam"], "protected": ["low wooden table", "bronze lamp"]},
    {"location": "loc_camp", "label": "GREEK CAMP — HECTOR'S FUNERAL TRUCE", "additional_prompt_constraints": "For ground-level/detail angles, set the extinguished firepit back in the off-centre midground; preserve the entire lower third as clear, level sand. No firepit, pots, vessels or extra objects in the foreground.", "theme": "A quiet beach camp at first light, an extinguished ceremonial firepit beside open ground, canvas tents and a calm grey sea beyond; no people, remains or bodies", "headline": "THE ILIAD'S END", "emphasis": "ILIAD'S", "chips": ["HECTOR BURIED", "A TRUCE", "THE WAR CONTINUES"], "defaults": ["achilles", "mascot"], "protected": ["empty firepit", "open beach"]},
    {"location": "loc_troy", "label": "TROJAN PLAIN — NEW ALLIES", "theme": "The broad empty plain below Troy's ancient walls, dry grasses, distant ridges and a muted dawn sky suggesting new forces arriving from far away; no figures", "headline": "LOST POEMS, LAST ALLIES", "emphasis": "ALLIES", "chips": ["PENTHESILEA", "MEMNON", "THE STORY CONTINUES"], "defaults": ["mascot"], "protected": ["open plain", "distant city walls"]},
    {"location": "loc_troy", "label": "TROJAN PLAIN — PENTHESILEA AND MEMNON", "theme": "A windswept Bronze Age plain outside Troy, two distant empty standards and a long track through ochre grass, atmospheric eastern dawn light; no people or silhouettes", "headline": "PENTHESILEA & MEMNON", "emphasis": "MEMNON", "chips": ["AMAZON QUEEN", "KING FROM THE EAST", "TWO LAST ALLIES"], "defaults": ["mascot"], "protected": ["empty standards", "open track"]},
    {"location": "loc_troy", "label": "TROY'S GATES — ACHILLES'S LAST BATTLE", "theme": "The wide approach to Troy's monumental Bronze Age gate, empty dusty ground, one unmarked bow and arrow lying in the foreground and storm-soft light on the walls; no people", "headline": "THE FALL OF ACHILLES", "emphasis": "ACHILLES", "chips": ["PARIS", "APOLLO", "AN ARROW"], "defaults": ["paris", "achilles"], "supporting_characters": ["achilles"], "protected": ["unmarked bow", "distant city gate"]},
    {"location": "loc_palace", "label": "A LATER STORYTELLER'S ROOM", "interior": True, "theme": "A quiet ancient palace writing room with a blank, unmarked clay tablet, a bronze stylus and a simple bronze greave on a low table; no writing, inscriptions or people", "headline": "THE FAMOUS HEEL CAME LATER", "emphasis": "HEEL", "chips": ["NOT IN THE ILIAD", "A LATER ADDITION", "A ROMAN POET"], "defaults": ["mascot"], "protected": ["blank tablet", "bronze greave"]},
    {"location": "loc_camp", "label": "GREEK CAMP — THE ARMOR DISPUTE", "interior": True, "additional_prompt_constraints": "Place the plain armor and shield on an empty low display stand off-centre in the midground; no armor/display stand in the lower third. Leave the full lower third as clear floor; no mannequin or human-shaped forms.", "theme": "An empty Greek command pavilion after battle, ornate bronze armor and a large round shield displayed on a low stand between two vacant places, no people", "headline": "WHO GETS ACHILLES'S ARMOR?", "emphasis": "ARMOR", "chips": ["AJAX", "ODYSSEUS", "THE JUDGES"], "defaults": ["agamemnon", "achilles"], "supporting_characters": ["achilles"], "protected": ["bronze armor", "round shield"]},
    {"location": "loc_camp", "label": "GREEK CAMP — THE JUDGMENT", "interior": True, "additional_prompt_constraints": "Show the scene unmistakably from inside a war-council tent, with canvas roof and side walls visible; no exterior-wide camp view. Set the empty judging bench and plain armor to one side in the midground and preserve the whole lower third as clear floor; no mannequins or human forms.", "theme": "A bare Greek war-council tent with an empty judging bench and bronze armor resting in warm lamplight, open canvas sides reveal the silent camp; no figures", "headline": "LET THE JUDGES DECIDE", "emphasis": "JUDGES", "chips": ["A CLAIM", "A VERDICT", "A WARRIOR'S PRIDE"], "defaults": ["odysseus", "agamemnon"], "protected": ["empty judging bench", "bronze armor"]},
    {"location": "loc_camp", "label": "GREEK CAMP — AFTER THE AWARD", "additional_prompt_constraints": "Keep fence rails and the tipped trough in the midground/background; no foreground fence crossing the lower third. Preserve the entire lower third as clear level ground.", "theme": "A deserted animal pen at cold dawn, a tipped wooden trough, scattered straw and an empty fenced corner near the tents, quiet and non-graphic; no animals or people", "headline": "AJAX'S GRIEF", "emphasis": "GRIEF", "chips": ["THE ARMOR IS GONE", "A TRAGIC MISTAKE", "MORNING AFTER"], "defaults": ["mascot"], "protected": ["tipped trough", "empty pen"]},
    {"location": "loc_camp", "label": "GREEK CAMP — THE SEER'S WARNING", "interior": True, "theme": "An empty command tent used for a prophecy, a plain bow on a low table and an empty wall niche with lamplight falling across the canvas; no writing or people", "headline": "THREE THINGS THE GREEKS NEED", "emphasis": "THREE", "chips": ["ACHILLES'S SON", "ATHENA'S STATUE", "HERACLES'S BOW"], "defaults": ["priam", "odysseus"], "supporting_characters": ["odysseus"], "protected": ["plain bow", "empty niche"]},
    {"location": "loc_troy", "label": "TROJAN PLAIN — PHILOCTETES RETURNS", "theme": "A broad empty field before Troy's weathered walls, an unmarked bow and a single arrow on a low stone ledge, clear ochre earth and distant gates; no people", "headline": "PHILOCTETES RETURNS", "emphasis": "RETURNS", "chips": ["HERACLES'S BOW", "PARIS", "A FINAL REQUEST"], "defaults": ["philoctetes", "paris"], "supporting_characters": ["paris"], "protected": ["unmarked bow", "open field"]},
    {"location": "loc_troy", "label": "MOUNT IDA — OENONE'S GROVE", "theme": "A secluded grove on the slopes near Troy at dusk, olive branches, a small stone hearth with a low funeral flame and an empty path through the trees; no people, remains or bodies", "headline": "OENONE'S REFUSAL", "emphasis": "REFUSAL", "chips": ["A PAST BETRAYAL", "A PLEA", "TOO LATE"], "defaults": ["helen", "paris"], "supporting_characters": ["paris"], "protected": ["stone hearth", "empty grove path"]},
    {"location": "loc_palace", "label": "TROY — THE TEMPLE OF ATHENA", "interior": True, "theme": "A quiet Bronze Age Trojan temple chamber at night, an empty stone plinth and open alcove beneath woven fabric, soft moonlight and no statue, people, writing or inscriptions", "headline": "THE ATHENA STATUE", "emphasis": "STATUE", "chips": ["ODYSSEUS", "DIOMEDES", "THE FINAL PROPHECY"], "defaults": ["odysseus", "mascot"], "protected": ["empty stone plinth", "open alcove"]},
    {"location": "loc_camp", "label": "GREEK CAMP — THE WOODEN HORSE PLAN", "theme": "An empty stretch of the Bronze Age Greek beach camp with a colossal horse-shaped timber framework under construction, neat ropes and cut beams, distant ships and open sand; no people", "headline": "A PLAN TO OPEN THE GATES", "emphasis": "GATES", "chips": ["THE WOODEN HORSE", "A GIFT TO ATHENA", "A WAY INSIDE"], "defaults": ["odysseus", "mascot"], "supporting_characters": ["mascot"], "protected": ["timber horse frame", "open beach"]},
    {"location": "loc_camp", "label": "GREEK CAMP — EPEIUS'S WORKSHOP", "theme": "A temporary Bronze Age carpentry yard beside the Greek camp, pine beams, wooden pegs and an unfinished hollow timber horse frame on clear ground; no people, writing or markings", "headline": "EPEIUS BUILDS A HORSE", "emphasis": "EPEIUS", "chips": ["PINE FROM IDA", "THREE DAYS", "A HOLLOW FRAME"], "defaults": ["agamemnon", "mascot"], "protected": ["pine beams", "horse frame"]},
    {"location": "loc_camp", "label": "GREEK CAMP — INSIDE THE HORSE", "interior": True, "theme": "A close environmental view through the open ribs of a huge hollow wooden horse, curved timbers, pegs and dark empty interior space, no people, letters or marks", "headline": "HOW MANY MEN FIT?", "emphasis": "MEN", "chips": ["TWENTY?", "FIFTY?", "NOBODY SAYS"], "defaults": ["mascot"], "protected": ["hollow timber ribs", "open interior"]},
    {"location": "loc_troy", "label": "TROY'S GATE — THE HORSE APPEARS", "theme": "At pale dawn outside Troy, the empty Greek beach camp has been struck and a huge wooden horse stands alone in the sand before the distant city gate; no people, figures or text", "headline": "THE TROJANS FIND THE HORSE", "emphasis": "HORSE", "chips": ["GREEK CAMP GONE", "A STRANGE GIFT", "DIVIDED OPINIONS"], "defaults": ["hector", "priam"], "protected": ["wooden horse", "distant city gate"]},
    {"location": "loc_troy", "label": "TROY'S GATE — LAOCOON'S WARNING", "theme": "The immense wooden horse outside Troy at night, one plain spear resting against its hollow timber side and moonlit water beyond the wall, no people or bodies", "headline": "LAOCOON'S WARNING", "emphasis": "WARNING", "chips": ["A HOLLOW SOUND", "SEA SERPENTS", "A FALSE SIGN"], "defaults": ["priam", "hector"], "supporting_characters": ["hector"], "protected": ["horse timber side", "plain spear"]},
    {"location": "loc_troy", "label": "TROY'S GATE — SINON'S STORY", "theme": "A shadowed gate courtyard with the wooden horse visible through the open entrance, an empty stone step and a dropped unmarked cloak in cool morning light; no people", "headline": "SINON'S STORY", "emphasis": "SINON", "chips": ["A CAPTURED GREEK", "A CAREFUL LIE", "KEEP THE HORSE"], "defaults": ["agamemnon", "hector"], "protected": ["open gate", "unmarked cloak"]},
    {"location": "loc_palace", "label": "TROY — CASSANDRA'S WARNING", "theme": "An empty Trojan palace courtyard facing the city gate, long evening shadows, plain stone columns and an open path toward the wooden horse beyond; no people or inscriptions", "headline": "CASSANDRA ISN'T BELIEVED", "emphasis": "CASSANDRA", "chips": ["SHE KNOWS THE TRUTH", "APOLLO'S CURSE", "NO ONE LISTENS"], "defaults": ["helen", "hector"], "supporting_characters": ["hector"], "protected": ["open courtyard", "gate passage"]},
    {"location": "loc_troy", "label": "TROY'S GATE — HELEN IN THE DARK", "theme": "A moonlit Trojan gate at night, the towering wooden horse casting a long shadow over empty paving stones and dark walls, eerie stillness; no people, faces or text", "headline": "HELEN CALLS TO THE HORSE", "emphasis": "HELEN", "chips": ["IN THE DARK", "THEIR WIVES' VOICES", "MEN INSIDE"], "defaults": ["helen"], "protected": ["wooden horse", "empty paving"]},
    {"location": "loc_troy", "label": "TROY'S GATE — THE HORSE ENTERS", "theme": "A silent Trojan city gate at late night, the giant wooden horse has just been drawn through the open stone arch, empty torch niches and quiet streets beyond; no people, bodies or text", "headline": "TROY OPENS ITS GATES", "emphasis": "GATES", "chips": ["NOT A SOUND", "A CITY CELEBRATES", "THEN SLEEPS"], "defaults": ["odysseus", "mascot"], "supporting_characters": ["mascot"], "protected": ["open stone arch", "wooden horse"]},
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


def build_prompt(design: dict, shot_index: int, shot_type: str, view: str) -> str:
    if design.get("interior"):
        view = {
            "establishing": "wide view from the open doorway, showing the empty room and clear lower-third floor",
            "wide": "oblique view from a different interior corner, with the entrance and open floor visible",
            "medium": "medium interior view of a restrained period prop with clear foreground floor",
            "detail": "ground-level environmental detail with architecture receding into an empty room",
        }[shot_type]
        unique_detail = [
            "keep the doorway and clear floor visible; add no occupants or extra furniture",
            "use foreground-to-background depth through canvas, stone or timber without clutter",
            "emphasize period materials already appropriate to the reference; invent no props",
            "use natural leading lines across the bare floor toward the empty entrance",
            "shift to warm lamp or dawn light while preserving the approved room palette",
            "show one restrained architectural layer and an unobstructed lower third",
            "place the focal prop to one side and leave clear ground for later character cutouts",
            "preserve the room's layout and avoid marks, writing or decorative emblems",
        ][(shot_index - 1) % len(SHOT_CYCLE)]
        focus = {
            "establishing": "show the room's broad layout and a clear open lower-third floor",
            "wide": "keep the interior architecture readable with generous negative space",
            "medium": "layer the room around one restrained focal area",
            "detail": "frame a period surface or architectural detail without clutter",
        }[shot_type]
    else:
        unique_detail = [
            "keep the horizon clear and place only landmarks from the named setting in the distance",
            "use strong foreground-to-background separation and generous open staging ground",
            "emphasize weathering and materials already appropriate to this environment; invent no props",
            "use natural leading lines to guide the eye through a clear, subject-free environment",
            "shift to softer evening or dawn light and a reverse-axis composition",
            "add a raised spatial layer without introducing structures absent from the location reference",
            "place the setting's main environmental feature in a distinct part of the composition",
            "use atmospheric depth and late light while preserving location continuity",
        ][(shot_index - 1) % len(SHOT_CYCLE)]
        focus = {
            "establishing": "show a broad, readable vista and a clear open lower-third foreground",
            "wide": "keep the major geography visible with generous negative space",
            "medium": "layer the environment around one restrained focal area",
            "detail": "frame an environmental surface or architectural detail without clutter",
        }[shot_type]
    if design.get("night") and "dawn" in unique_detail:
        unique_detail = "combine warm oil-lamp glow with cool moonlight; show no dawn or daylight"
    night_guidance = (
        " Night lighting only: cool moonlight and warm bronze oil-lamp glow; deep blue-black outside; absolutely no sun, dawn, daylight or bright daytime sky."
        if design.get("night") else ""
    )
    extra_constraints = design.get("additional_prompt_constraints", "")
    extra_constraints = f" Additional composition constraints: {extra_constraints}" if extra_constraints else ""
    return (
        f"One standalone 16:9 landscape background plate, approximately 1376x768, cinematic painterly-realistic HYBRID style, for {design['theme']}. "
        f"{shot_type.capitalize()} composition: {view}; {focus}; {unique_detail}. Match the approved "
        f"{design.get('reference', design['location'])} location-sheet palette, architecture and Bronze Age materials. "
        "Warm ochre, weathered stone, bronze and deep Aegean blues; soft atmospheric depth; an unobstructed, level lower third for later 2D character cutouts. "
        "Environment only: absolutely no people, faces, human silhouettes, bodies, statues or reliefs; no live animals; no text, letters, numbers, inscriptions, emblems, logos, watermarks, modern objects, or layout guides. If the theme specifically calls for the wooden horse, it is the sole permitted animal-shaped object and must be an empty, inanimate timber prop without riders."
        f"{night_guidance}{extra_constraints}"
    )


def shot_count_for(duration_s: float) -> int:
    """Target ~3 s per plate while keeping every shot in the 2–4 s explainer range."""
    return max(2, min(8, int(duration_s / 3.0 + 0.5)))


def main():
    manifest = json.loads(VO_MANIFEST.read_text())
    override = json.loads(OVERRIDE.read_text())
    if manifest.get("part") != 3 or manifest.get("clip_count") != len(CLIP_DESIGNS):
        raise ValueError(f"Expected 24 Part 3 VO clips; manifest says {manifest.get('clip_count')}.")
    if override.get("source_script_modified") is not False:
        raise ValueError("The approved source script must remain unchanged.")
    source_hash = hashlib.sha256((ROOT / "production/script_approved.txt").read_bytes()).hexdigest()
    if manifest.get("source_script_sha256") != source_hash:
        raise ValueError("Part 3 VO manifest does not match the locked source-script checksum.")

    global_scenes = json.loads(SCENES_PATH.read_text())
    preserve_sections = {
        key: copy.deepcopy(global_scenes[key])
        for key in ("part1_clips", "part2_clips") if key in global_scenes
    }
    background_manifest = (
        json.loads(BACKGROUND_MANIFEST.read_text())
        if BACKGROUND_MANIFEST.exists() else {"part": 3, "plates": []}
    )
    existing_plates = {(p["clip_id"], p["shot_index"]): p for p in background_manifest.get("plates", [])}
    if len(existing_plates) != len(background_manifest.get("plates", [])):
        raise ValueError("Duplicate Part 3 plate record in background manifest.")

    part3_clips = []
    planned_plates = []
    expected_plate_keys = set()
    previous_location = None
    accepted_statuses = {"accepted"}

    for clip_index, (clip, design) in enumerate(zip(manifest["clips"], CLIP_DESIGNS)):
        clip_id = clip["clip_id"]
        if clip_id != f"p3_clip_{clip_index + 1:02d}":
            raise ValueError(f"Nonsequential Part 3 VO clip id: {clip_id}")
        if design["emphasis"] not in design["headline"]:
            raise ValueError(f"Emphasis must appear in the overlay headline for {clip_id}.")
        location_id = design["location"]
        is_new_location = location_id != previous_location
        previous_location = location_id

        dialogue_bubbles = []
        active_characters = []
        for segment in clip["segments"]:
            if segment["speaker"] == "NARRATOR":
                continue
            character = SPEAKER_TO_CHAR.get(segment["speaker"])
            if not character:
                raise ValueError(f"Missing Part 3 speaker mapping for {segment['speaker']}.")
            if character not in active_characters:
                active_characters.append(character)
            words = segment["text"].split()
            excerpt = " ".join(words[:4]) + ("..." if len(words) > 4 else "")
            dialogue_bubbles.append({
                "speaker": segment["speaker"], "char": character, "bubble_text": excerpt,
                "t_start": segment["t_start"], "t_end": segment["t_end"],
                "source_line_index": segment["line_index"],
                "visual_mapping": SPEAKER_VISUAL_MAPPING[segment["speaker"]]["mapping"],
            })
        if not active_characters:
            active_characters = list(design["defaults"])
        for character in design.get("supporting_characters", []):
            if character not in active_characters:
                active_characters.append(character)
        if len(active_characters) > 2:
            raise ValueError(f"Part 3 clip {clip_id} has more than two visible cutouts: {active_characters}")
        for character in active_characters:
            rig_path = ROOT / f"production/assets/rigs/char_{character}_a.png"
            cutout_path = ROOT / f"production/assets/rigs/cutout_{character}.png"
            if character == "mascot":
                rig_path = ROOT / "production/assets/rigs/char_mascot_a.png"
            if not rig_path.is_file() and not cutout_path.is_file():
                raise FileNotFoundError(f"No approved Part 3 character asset for {character}.")

        duration = float(clip["duration_s"])
        count = shot_count_for(duration)
        shot_duration = duration / count
        shots = []
        for shot_index in range(1, count + 1):
            shot_type, camera, view = SHOT_CYCLE[(clip_index + shot_index - 1) % len(SHOT_CYCLE)]
            if shot_index == 1 and is_new_location:
                shot_type, camera, view = "establishing", "dolly-in", SHOT_CYCLE[0][2]
            t_start = round((shot_index - 1) * shot_duration, 3)
            t_end = duration if shot_index == count else round(shot_index * shot_duration, 3)
            bg_path = f"production/part3/backgrounds/{clip_id}_bg_{shot_index:02d}.jpg"
            reference_path = f"production/assets/locations/{design['location']}_ref.png"
            if not (ROOT / reference_path).is_file():
                raise FileNotFoundError(f"Missing approved location reference: {reference_path}")
            plate_key = (clip_id, shot_index)
            expected_plate_keys.add(plate_key)
            plate_record = existing_plates.get(plate_key)
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
                "text_style": "label" if shot_index == 1 and is_new_location else (
                    "bubble" if overlapping and any(s["speaker"] != "NARRATOR" for s in overlapping) else "card"
                ),
                "text_position": "bottom-left" if shot_index == 1 and is_new_location else (
                    "top-left" if clip_index % 2 == 0 else "top-right"
                ),
                "mascot": {"pose": "pose_b" if clip_index % 2 == 0 else "pose_c",
                           "side": "left" if clip_index % 2 == 0 else "right"}
                          if "mascot" in active_characters else "none",
                "arrow_target": design["protected"][0] if design["protected"] else "center",
                "dim_background": shot_index == 3 or bool(dialogue_bubbles),
                "sfx": "pop" if any(s["speaker"] != "NARRATOR" for s in overlapping) else (
                    "whoosh" if shot_index == 2 else "arrow" if shot_index == 4 else "none"
                ),
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
                    "qc_note": "Awaiting image generation and individual visual review against the approved location sheet.",
                    "composition": {"view": view, "open_lower_third": True},
                    "protected_objects": design["protected"],
                })

        part3_clips.append({
            "clip_id": clip_id,
            "chapter": clip["chapter"],
            "duration_s": clip["duration_s"],
            "is_new_location": is_new_location,
            "place_label": design["label"],
            "location": location_id,
            "active_characters": active_characters,
            "dialogue_bubbles": dialogue_bubbles,
            "overlay_card": {
                "headline": design["headline"], "emphasis": design["emphasis"],
                "chips": design["chips"], "style": "card",
            },
            "shots": shots,
            "vo_segments": clip["segments"],
            "character_asset_requirements": [],
        })

    global_scenes["part3_clips"] = part3_clips
    global_scenes["part3_character_asset_requirements"] = []
    global_scenes["part3_speaker_visual_mapping"] = SPEAKER_VISUAL_MAPPING
    if any(global_scenes.get(key) != value for key, value in preserve_sections.items()):
        raise AssertionError("Part 3 planning must not modify the accepted Part 1/2 scene plans.")
    SCENES_PATH.write_text(json.dumps(global_scenes, indent=2, ensure_ascii=True) + "\n")

    by_key = {(p["clip_id"], p["shot_index"]): p for p in background_manifest.get("plates", [])}
    if set(by_key) - expected_plate_keys:
        raise ValueError("Part 3 background manifest contains plate keys absent from the current scene plan.")
    for record in planned_plates:
        key = (record["clip_id"], record["shot_index"])
        prior = by_key.get(key, {})
        if prior.get("qc_status") == "accepted":
            continue
        for audit_key in ("candidate_history", "rerolls_used", "rerolls_remaining", "qc_note"):
            if audit_key in prior:
                record[audit_key] = prior[audit_key]
        by_key[key] = record
    background_manifest.update({
        "part": 3,
        "schema_version": 1,
        "total_planned": sum(len(clip["shots"]) for clip in part3_clips),
        "accepted": sum(1 for p in by_key.values() if p.get("qc_status") == "accepted"),
        "pending": sum(1 for p in by_key.values() if p.get("qc_status") != "accepted"),
        "plates": sorted(by_key.values(), key=lambda p: (int(p["clip_id"][-2:]), p["shot_index"])),
        "note": "Part 3 background plates are generated in batches of 10 and accepted only after individual visual review; every plate must have open lower-third staging and contain no people, faces, bodies, text or modern objects.",
        "shot_cadence_seconds_target": 3.0,
        "character_proxy_note": "Only existing approved cutouts/rigs are used; one-off Chapter 9-10 speakers retain their exact names in dialogue and subtitles, while the proxy map is recorded in scenes.json and part3_scene_plan_notes.md.",
    })
    BACKGROUND_MANIFEST.write_text(json.dumps(background_manifest, indent=2, ensure_ascii=True) + "\n")

    print(f"Saved {len(part3_clips)} Part 3 clips and {background_manifest['total_planned']} shot entries.")
    print(f"Part 3 plate ledger: {background_manifest['accepted']} accepted / {background_manifest['pending']} pending.")
    print("Chapter 9-10 one-off dialogue roles use documented existing character proxies; no new character sheets are introduced.")


if __name__ == "__main__":
    main()
