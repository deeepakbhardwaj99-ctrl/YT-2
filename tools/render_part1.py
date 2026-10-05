"""Render the locked, complete Part 1 cut without touching the approved preview."""
from pathlib import Path
import json
import os
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "tools"))


def ensure_ffmpeg():
    if shutil.which("ffmpeg"):
        return
    try:
        import imageio_ffmpeg
    except ImportError as exc:
        raise RuntimeError(
            "FFmpeg is required. Install tools/requirements.txt or add ffmpeg to PATH."
        ) from exc
    venv_bin = ROOT / ".venv" / "bin"
    venv_bin.mkdir(parents=True, exist_ok=True)
    ffmpeg_link = venv_bin / "ffmpeg"
    if not ffmpeg_link.exists():
        ffmpeg_link.symlink_to(imageio_ffmpeg.get_ffmpeg_exe())
    os.environ["PATH"] = str(venv_bin) + os.pathsep + os.environ.get("PATH", "")


ensure_ffmpeg()
from assemble import render_sequence_to_mp4  # noqa: E402
from validate_part1 import validate  # noqa: E402


OUTPUT = ROOT / "production/part1/part1_full.mp4"
REPORT = ROOT / "production/part1/part1_motion_report.txt"
PREVIEW = ROOT / "production/part1/scene_01_preview.mp4"


def main():
    readiness = validate(require_complete=True)
    if not readiness["full_render_ready"] or readiness["accepted_plates"] != 125:
        raise RuntimeError(f"Part 1 asset gate failed: {readiness}")
    if OUTPUT.resolve() == PREVIEW.resolve():
        raise RuntimeError("Refusing to overwrite the approved scene_01_preview.mp4")

    with (ROOT / "production/scenes.json").open() as f:
        scenes = json.load(f)

    title_card = {
        "bg_path": "production/part1/backgrounds/p1_clip_01_bg_01.jpg",
        "camera": "dolly-in",
        "eyebrow": "THE TROJAN WAR  •  PART I",
        "title": "THE APPLE & THE FLEET",
        "subtitle": "GODS, OATHS & A FLEET BOUND FOR TROY",
    }
    end_card = {
        "bg_path": "production/part1/backgrounds/p1_clip_25_bg_05.jpg",
        "camera": "pull-back",
        "eyebrow": "COMING NEXT  •  PART II",
        "title": "THE WRATH OF ACHILLES",
        "subtitle": "NINE YEARS OF NOTHING",
    }

    render_sequence_to_mp4(
        scenes["part1_clips"],
        "production/music/part1_stem.mp3",
        str(OUTPUT.relative_to(ROOT)),
        str(REPORT.relative_to(ROOT)),
        title_card=title_card,
        end_card=end_card,
        title_duration_s=2.5,
        end_duration_s=2.5,
    )


if __name__ == "__main__":
    main()
