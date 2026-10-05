"""Build a labelled Part 2 background review sheet without implying acceptance."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SCENES_PATH = ROOT / "production/scenes.json"
MANIFEST_PATH = ROOT / "production/part2/background_manifest.json"


def build_contact(clip_numbers, batch_number, allow_pending=False):
    scenes = json.loads(SCENES_PATH.read_text())
    manifest = json.loads(MANIFEST_PATH.read_text())
    clips = {clip["clip_id"]: clip for clip in scenes["part2_clips"]}
    plates = {(plate["clip_id"], plate["shot_index"]): plate for plate in manifest["plates"]}
    accepted = sum(plate.get("qc_status") == "accepted" for plate in manifest["plates"])
    selected = []
    for number in clip_numbers:
        clip_id = f"p2_clip_{number:02d}"
        if clip_id not in clips:
            raise ValueError(f"Unknown Part 2 clip: {clip_id}")
        selected.append((number, clips[clip_id]))
    max_shots = max(len(clip["shots"]) for _, clip in selected)

    width, height, gap, row_height = 720, 405, 24, 465
    header = 120
    sheet = Image.new(
        "RGB",
        (gap + len(selected) * (width + gap), header + gap + max_shots * row_height),
        (21, 19, 17),
    )
    draw = ImageDraw.Draw(sheet)
    title = ImageFont.truetype(str(ROOT / "production/fonts/DisplaySerif-Bold.ttf"), 30)
    label = ImageFont.truetype(str(ROOT / "production/fonts/DisplaySans-Bold.ttf"), 18)
    draw.text((24, 22), "THE TROJAN WAR  /  PART 2", font=title, fill="#f8f0e1")
    draw.text(
        (24, 66),
        f"BACKGROUND BATCH {batch_number:02d}  |  {accepted} / {manifest['total_planned']} ACCEPTED",
        font=label,
        fill="#d98b52",
    )
    for col, (number, clip) in enumerate(selected):
        clip_id = clip["clip_id"]
        for row in range(max_shots):
            x, y = 12 + col * (width + gap), header + 10 + row * row_height
            if row >= len(clip["shots"]):
                draw.rectangle((x, y, x + width, y + height), fill="#28231e", outline="#655b50", width=2)
                draw.text((x + 45, y + 155), "NO PLANNED SHOT", font=title, fill="#b9afa3")
                draw.text((x + 8, y + height + 10), f"CLIP {number:02d}  /  ROW {row+1:02d}   |   NOT APPLICABLE", font=label, fill="#b9afa3")
                continue
            shot_index = row + 1
            plate = plates.get((clip_id, shot_index))
            if plate is None or plate.get("qc_status") != "accepted" or not (ROOT / plate["path"]).is_file():
                if not allow_pending:
                    raise ValueError(f"{clip_id} shot {shot_index:02d} is not accepted; use --allow-pending for a labelled placeholder")
                draw.rectangle((x, y, x + width, y + height), fill="#28231e", outline="#9b3a12", width=2)
                draw.text((x + 45, y + 150), "NOT ACCEPTED — PENDING", font=title, fill="#d98b52")
                draw.text((x + 45, y + 205), "Not counted as an accepted image", font=label, fill="#f8f0e1")
                draw.text((x + 8, y + height + 10), f"CLIP {number:02d}  /  SHOT {shot_index:02d}   |   PENDING", font=label, fill="#f8f0e1")
                continue
            with Image.open(ROOT / plate["path"]) as source:
                tile = ImageOps.fit(source.convert("RGB"), (width, height), method=Image.Resampling.LANCZOS)
            sheet.paste(tile, (x, y))
            draw.rectangle((x, y, x + width, y + height), outline="#9b3a12", width=2)
            location = plate.get("setting_label", plate["location"].removeprefix("loc_").upper())
            draw.text((x + 8, y + height + 10), f"CLIP {number:02d}  /  SHOT {shot_index:02d}   |   {location}", font=label, fill="#f8f0e1")

    output = ROOT / f"production/part2/backgrounds_batch_{batch_number:02d}_contact.jpg"
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=90)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clips", nargs="+", type=int, required=True, help="Part 2 clip numbers (1–24)")
    parser.add_argument("--batch", type=int, required=True)
    parser.add_argument("--allow-pending", action="store_true", help="Label pending slots; never count them as accepted")
    args = parser.parse_args()
    if not 1 <= len(args.clips) <= 4 or any(clip < 1 or clip > 24 for clip in args.clips):
        parser.error("Supply one to four Part 2 clip numbers between 1 and 24")
    print(build_contact(args.clips, args.batch, args.allow_pending))
