"""Validate Part 3 VO-linked scene plans and accepted/pending background plates."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCENES_PATH = ROOT / "production/scenes.json"
VO_PATH = ROOT / "production/part3/part3_vo_manifest.json"
BG_PATH = ROOT / "production/part3/background_manifest.json"
OVERRIDE_PATH = ROOT / "production/part3/chapter9_vo_override.json"


def shot_count_for(duration_s: float) -> int:
    return max(2, min(8, int(duration_s / 3.0 + 0.5)))


def validate(require_complete: bool = False) -> dict:
    scenes = json.loads(SCENES_PATH.read_text())
    part3 = scenes["part3_clips"]
    vo_manifest = json.loads(VO_PATH.read_text())
    background_manifest = json.loads(BG_PATH.read_text())
    override = json.loads(OVERRIDE_PATH.read_text())

    assert vo_manifest.get("part") == 3
    assert vo_manifest.get("clip_count") == 24
    assert len(part3) == len(vo_manifest["clips"]) == 24
    assert background_manifest.get("part") == 3
    assert override.get("source_script_modified") is False
    approved_script = ROOT / "production/script_approved.txt"
    source_script = ROOT / "trojan_war_script_20min_with_dialogue.txt"
    assert approved_script.read_bytes() == source_script.read_bytes(), "Locked source script changed"
    script_hash = hashlib.sha256(approved_script.read_bytes()).hexdigest()
    assert vo_manifest["source_script_sha256"] == script_hash

    visual_map = scenes["part3_speaker_visual_mapping"]
    vo_by_id = {clip["clip_id"]: clip for clip in vo_manifest["clips"]}
    plate_by_key = {(p["clip_id"], p["shot_index"]): p for p in background_manifest["plates"]}
    assert len(plate_by_key) == len(background_manifest["plates"]), "Duplicate background-manifest key"

    planned_paths = set()
    accepted_digests = set()
    pending_paths = []
    accepted_count = 0
    total_shots = 0
    dialogue_speakers = {
        segment["speaker"]
        for clip in vo_manifest["clips"]
        for segment in clip["segments"]
        if segment["speaker"] != "NARRATOR"
    }
    assert dialogue_speakers <= set(visual_map), f"Missing visual mappings: {sorted(dialogue_speakers - set(visual_map))}"

    for index, (clip, source) in enumerate(zip(part3, vo_manifest["clips"]), start=1):
        expected_id = f"p3_clip_{index:02d}"
        assert clip["clip_id"] == source["clip_id"] == expected_id
        assert clip["duration_s"] == source["duration_s"]
        assert clip["vo_segments"] == source["segments"], f"VO text/timing changed in {expected_id}"
        assert clip["overlay_card"]["emphasis"] in clip["overlay_card"]["headline"]
        assert 1 <= len(clip["active_characters"]) <= 2
        for character in clip["active_characters"]:
            rig = ROOT / f"production/assets/rigs/char_{character}_a.png"
            cutout = ROOT / f"production/assets/rigs/cutout_{character}.png"
            if character == "mascot":
                rig = ROOT / "production/assets/rigs/char_mascot_a.png"
            assert rig.is_file() or cutout.is_file(), f"Missing approved character asset: {character}"

        bubbles = {(b["speaker"], b["source_line_index"]): b for b in clip["dialogue_bubbles"]}
        for segment in source["segments"]:
            if segment["speaker"] == "NARRATOR":
                continue
            key = (segment["speaker"], segment["line_index"])
            assert key in bubbles, f"Missing dialogue bubble {key} in {expected_id}"
            bubble = bubbles[key]
            assert bubble["char"] == visual_map[segment["speaker"]]["character"]
            assert bubble["char"] in clip["active_characters"]

        expected_count = shot_count_for(float(source["duration_s"]))
        assert len(clip["shots"]) == expected_count
        total_shots += expected_count
        previous_end = 0.0
        for shot_index, shot in enumerate(clip["shots"], start=1):
            assert shot["shot_index"] == shot_index
            assert abs(float(shot["t_start"]) - previous_end) < 0.002, f"Gap/overlap in {expected_id}"
            assert shot["t_end"] > shot["t_start"]
            shot_duration = shot["t_end"] - shot["t_start"]
            assert 2.0 <= shot_duration <= 4.0, f"Shot outside 2–4 s cadence: {expected_id}/{shot_index}"
            previous_end = float(shot["t_end"])
            assert shot["composition"].get("open_lower_third") is True
            assert shot["asset_status"] in {"pending_generation", "accepted"}
            assert shot["bg_path"].startswith("production/part3/backgrounds/")
            assert shot["bg_path"].endswith(".jpg")
            assert shot["reference_path"].startswith("production/assets/locations/")
            assert (ROOT / shot["reference_path"]).is_file()
            assert "no people" in shot["image_prompt"].lower()
            assert "lower third" in shot["image_prompt"].lower()
            assert shot["image_prompt"] == plate_by_key[(expected_id, shot_index)]["image_prompt"]
            assert shot["bg_path"] not in planned_paths, f"Reused background path: {shot['bg_path']}"
            planned_paths.add(shot["bg_path"])

            plate = plate_by_key[(expected_id, shot_index)]
            assert plate["path"] == shot["bg_path"]
            assert plate["reference"] == shot["reference_path"]
            assert plate["composition"].get("open_lower_third") is True
            if plate["qc_status"] == "accepted":
                accepted_count += 1
                image_path = ROOT / plate["path"]
                data = image_path.read_bytes()
                digest = hashlib.sha256(data).hexdigest()
                assert digest == plate["sha256"] and digest not in accepted_digests
                accepted_digests.add(digest)
                with Image.open(image_path) as im:
                    assert list(im.size) == plate["dimensions"]
                    assert abs(im.width / im.height - 16 / 9) < 0.03
                    im.verify()
            else:
                assert plate["qc_status"] == "pending_generation"
                assert shot["asset_status"] == "pending_generation"
                pending_paths.append(plate["path"])

        assert abs(previous_end - float(source["duration_s"])) < 0.002
        assert (ROOT / source["file_path"]).is_file(), f"Missing VO asset: {source['file_path']}"

    assert len(plate_by_key) == len(planned_paths) == total_shots == background_manifest["total_planned"]
    assert background_manifest["accepted"] == accepted_count
    assert background_manifest["pending"] == len(pending_paths)
    result = {
        "script_verbatim": True,
        "vo_segments_unchanged": True,
        "clip_count": len(part3),
        "planned_unique_plates": total_shots,
        "accepted_plates": accepted_count,
        "pending_plates": len(pending_paths),
        "dialogue_speakers_mapped": len(dialogue_speakers),
        "full_render_ready": not pending_paths,
    }
    if require_complete and pending_paths:
        raise ValueError(f"Part 3 render blocked: {len(pending_paths)} backgrounds pending visual QC")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(args.require_complete), indent=2))
