# Production tools

Run from the repository root. Restore accepted reusable assets from GitHub rather than regenerating them.

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements.txt
.venv/bin/python tools/generate_scenes_plan.py
.venv/bin/python tools/validate_part1.py
.venv/bin/python tools/validate_part1.py --require-complete
```

Python dependencies are pinned in `requirements.txt`. `render_part1.py` uses system FFmpeg when available, or the bundled executable from `imageio-ffmpeg`; final media QC also requires `ffprobe`.

- `clip_beats.json` supplies narration-specific editorial cards; never edit locked VO when changing overlays.
- `background_manifest.json` is the accepted-asset ledger. Add an image only after visually checking it; include reference, dimensions, SHA-256 and QC notes.
- `generate_scenes_plan.py` is deterministic and retains all measured VO segments. Pending production paths do not silently fall back to reference crops.
- `validate_part1.py --require-complete` intentionally fails until all 125 unique plates are accepted.
- `scene_01_preview.mp4` is the approved clip 01 + 05 preview; preserve it. Do not overwrite it with a full-part render.
- `render_part1.py` validates all 125 accepted plates and renders all 25 locked VO clips with a 2.5-second opening title and closing Part II tease to `production/part1/part1_full.mp4`; the motion report is written separately.
- `qc_part1.py` checks the locked script/VO gate, stream format, frame count, duration/sync, full media decode, audio levels, motion gate, preview preservation, and GitHub single-file size target. It writes text and JSON reports alongside the export.
- `process_part2_vo.py` reuses the eight saved raw Part 2 voice batches, applies only the approved Chapter 7 VO override, and writes 24 measured clip MP3s plus manifests/QC. Use `--dry-run` to inspect timing first; `--overwrite` is required to replace already-created clips.
- `generate_part2_scene_plan.py` appends a VO-timed Part 2 motion plan to `production/scenes.json` without changing Part 1, and creates the separate pending-plate ledger at `production/part2/background_manifest.json`. It preserves accepted Part 2 plates if rerun; it does not generate backgrounds. `p2_clip_16` uses eight plates due to its 23.678-second duration.
- `build_part2_character_contact.py` creates the labelled Step 3 contact grid from the existing approved character sheets and the five new Part 2 candidates. Check `production/part2/character_sheets/character_sheet_manifest.json`; do not use candidate sheets in scenes until approved.
- `production/part2/part2_scene_plan_notes.md` records the shot-density decision and the Step 3 character-sheet approval gate. Do not generate Part 2 backgrounds before the new character assets are approved.

```sh
.venv/bin/python tools/render_part1.py
.venv/bin/python tools/qc_part1.py
.venv/bin/python tools/process_part2_vo.py --dry-run
.venv/bin/python tools/process_part2_vo.py
.venv/bin/python tools/generate_part2_scene_plan.py
```
