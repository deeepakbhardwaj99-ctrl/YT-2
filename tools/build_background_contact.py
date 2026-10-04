"""Build a labelled contact sheet from accepted plates; no generation or acceptance implied."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def build_contact(clip_numbers, batch_number, allow_pending=False):
    manifest = json.loads((ROOT / 'production/part1/background_manifest.json').read_text())
    plates = {(p['clip_id'], p['shot_index']): p for p in manifest['plates'] if p['qc_status'] == 'accepted'}
    width, height, gap, row_height = 720, 405, 24, 465
    sheet = Image.new('RGB', (len(clip_numbers) * (width + gap), 2455), (21, 19, 17))
    draw = ImageDraw.Draw(sheet)
    title = ImageFont.truetype(str(ROOT / 'production/fonts/DisplaySerif-Bold.ttf'), 30)
    label = ImageFont.truetype(str(ROOT / 'production/fonts/DisplaySans-Bold.ttf'), 18)
    draw.text((24, 22), 'THE TROJAN WAR  /  PART 1', font=title, fill='#f8f0e1')
    draw.text((24, 66), f'BACKGROUND BATCH {batch_number:02d}  |  {len(plates)} / {manifest["required_unique_plates"]} ACCEPTED', font=label, fill='#d98b52')
    for col, clip_num in enumerate(clip_numbers):
        for row in range(5):
            plate = plates.get((f'p1_clip_{clip_num:02d}', row + 1))
            x, y = 12 + col * (width + gap), 115 + row * row_height
            if plate is None:
                if not allow_pending:
                    raise ValueError(f'Clip {clip_num:02d} shot {row+1:02d} not accepted; use --allow-pending for an explicitly labelled placeholder')
                draw.rectangle((x, y, x + width, y + height), fill='#28231e', outline='#9b3a12', width=2)
                draw.text((x + 45, y + 150), 'NOT GENERATED — PENDING', font=title, fill='#d98b52')
                draw.text((x + 45, y + 205), 'Not counted as an accepted image', font=label, fill='#f8f0e1')
                draw.text((x + 8, y + height + 10), f'CLIP {clip_num:02d}  /  SHOT {row+1:02d}   |   PENDING', font=label, fill='#f8f0e1')
                continue
            with Image.open(ROOT / plate['path']) as source:
                tile = ImageOps.fit(source.convert('RGB'), (width, height), method=Image.Resampling.LANCZOS)
            sheet.paste(tile, (x, y))
            draw.rectangle((x, y, x + width, y + height), outline='#9b3a12', width=2)
            location = plate.get('setting_label', plate['location'].removeprefix('loc_').upper())
            draw.text((x + 8, y + height + 10), f'CLIP {clip_num:02d}  /  SHOT {row+1:02d}   |   {location}', font=label, fill='#f8f0e1')
    output = ROOT / f'production/part1/backgrounds_batch_{batch_number:02d}_contact.jpg'
    sheet.save(output, quality=90)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clips', nargs='+', type=int, required=True)
    parser.add_argument('--batch', type=int, required=True)
    parser.add_argument('--allow-pending', action='store_true', help='Label missing slots explicitly; never count them as images')
    args = parser.parse_args()
    if not 1 <= len(args.clips) <= 4 or any(c < 1 or c > 25 for c in args.clips):
        parser.error('Supply one to four Part 1 clip numbers between 1 and 25')
    print(build_contact(args.clips, args.batch, args.allow_pending))
