"""Build a labelled review grid for the original and new Part 2 character sheets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "production/assets/characters"
PART2 = ROOT / "production/part2/character_sheets"
OUTPUT = PART2 / "part2_character_contact_grid.jpg"

ITEMS = [
    ("ACHILLES", APPROVED / "achilles_sheet.png", False),
    ("PROTESILAUS", PART2 / "protesilaus_sheet.png", True),
    ("PHILOCTETES", PART2 / "philoctetes_sheet.png", True),
    ("ODYSSEUS", APPROVED / "odysseus_sheet.png", False),
    ("AGAMEMNON", APPROVED / "agamemnon_sheet.png", False),
    ("CHRYSES", PART2 / "chryses_sheet.png", True),
    ("HECTOR", APPROVED / "hector_sheet.png", False),
    ("PATROCLUS", PART2 / "patroclus_sheet.png", True),
    ("ANDROMACHE + ASTYANAX", PART2 / "andromache_astyanax_sheet.png", True),
    ("HELEN", APPROVED / "helen_sheet.png", False),
    ("PARIS", APPROVED / "paris_sheet.png", False),
    ("MENELAUS", APPROVED / "menelaus_sheet.png", False),
    ("PRIAM", APPROVED / "priam_sheet.png", False),
    ("MASCOT NARRATOR", APPROVED / "mascot_sheet.png", False),
]


def main():
    missing = [str(path.relative_to(ROOT)) for _, path, _ in ITEMS if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing character sheets: " + ", ".join(missing))

    width, height, gap, header, columns = 500, 365, 24, 130, 3
    rows = (len(ITEMS) + columns - 1) // columns
    canvas = Image.new("RGB", (gap + columns * (width + gap), header + gap + rows * (height + gap)), "#f4efe4")
    draw = ImageDraw.Draw(canvas)
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 36)
    subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
    label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 21)
    status_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    draw.text((gap, 22), "PART 2 CHARACTER SHEETS — REVIEW", font=title, fill="#1e2932")
    draw.text((gap, 76), "Gold border: five new static-art candidates awaiting approval  |  Grey border: approved existing designs",
              font=subtitle, fill="#48545a")

    for index, (label, path, is_new) in enumerate(ITEMS):
        col, row = index % columns, index // columns
        x, y = gap + col * (width + gap), header + gap + row * (height + gap)
        border = "#c17b22" if is_new else "#a5aaa8"
        draw.rounded_rectangle((x, y, x + width, y + height), radius=14, fill="#fffdf8", outline=border,
                               width=5 if is_new else 3)
        with Image.open(path) as source:
            image = ImageOps.contain(source.convert("RGB"), (width - 28, height - 95),
                                     method=Image.Resampling.LANCZOS)
        px, py = x + (width - image.width) // 2, y + 10 + (height - 95 - image.height) // 2
        canvas.paste(image, (px, py))
        text_y = y + height - 73
        draw.text((x + 15, text_y), label, font=label_font, fill="#1e2932")
        status = "NEW · APPROVAL NEEDED" if is_new else "APPROVED · REUSE"
        color = "#a86712" if is_new else "#577266"
        draw.text((x + 15, text_y + 30), status, font=status_font, fill=color)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, quality=93, optimize=True)
    print(f"Saved {OUTPUT.relative_to(ROOT)} ({canvas.width}x{canvas.height})")


if __name__ == "__main__":
    main()
