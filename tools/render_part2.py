"""Render the locked, complete Part 2 cut to production/part2/part2_full.mp4."""
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
from validate_part2 import validate  # noqa: E402


OUTPUT = ROOT / "production/part2/part2_full.mp4"
REPORT = ROOT / "production/part2/part2_motion_report.txt"
VO_MANIFEST = "production/part2/part2_vo_manifest.json"


def main():
    readiness = validate(require_complete=True)
    if not readiness["full_render_ready"] or readiness["accepted_plates"] != 123:
        raise RuntimeError(f"Part 2 asset gate failed: {readiness}")

    with (ROOT / "production/scenes.json").open() as f:
        scenes = json.load(f)

    title_card = {
        "bg_path": "production/part2/backgrounds/p2_clip_01_bg_01.jpg",
        "camera": "dolly-in",
        "eyebrow": "THE TROJAN WAR  •  PART II",
        "title": "THE WRATH OF ACHILLES",
        "subtitle": "NINE YEARS OF NOTHING",
    }
    end_card = {
        "bg_path": "production/part2/backgrounds/p2_clip_23_bg_02.jpg",
        "camera": "pull-back",
        "eyebrow": "COMING NEXT  •  PART III",
        "title": "THE FALL OF HEROES",
        "subtitle": "& THE WOODEN HORSE",
    }

    render_sequence_to_mp4(
        scenes["part2_clips"],
        "production/music/part2_stem.mp3",
        str(OUTPUT.relative_to(ROOT)),
        str(REPORT.relative_to(ROOT)),
        title_card=title_card,
        end_card=end_card,
        title_duration_s=2.5,
        end_duration_s=2.5,
        vo_manifest_path=VO_MANIFEST,
    )


if __name__ == "__main__":
    main()
