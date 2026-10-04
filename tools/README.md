# Production tools

Run from the repository root. Restore accepted reusable assets from GitHub rather than regenerating them.

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements.txt
.venv/bin/python tools/generate_scenes_plan.py
.venv/bin/python tools/validate_part1.py
.venv/bin/python tools/validate_part1.py --require-complete
```

Python dependencies are pinned in `requirements.txt`. Encoding/audio tools additionally require system `ffmpeg` and `ffprobe` (not present in the restored sandbox at the time of background batch 01; install before rendering).

- `clip_beats.json` supplies narration-specific editorial cards; never edit locked VO when changing overlays.
- `background_manifest.json` is the accepted-asset ledger. Add an image only after visually checking it; include reference, dimensions, SHA-256 and QC notes.
- `generate_scenes_plan.py` is deterministic and retains all measured VO segments. Pending production paths do not silently fall back to reference crops.
- `validate_part1.py --require-complete` intentionally fails until all 125 unique plates are accepted.
- `assemble.py` currently defaults to the former clip 01 + 05 preview selection. It now refuses missing/unaccepted plates. The approved preview is retained in Git; do not overwrite it as a substitute for a full Part 1 delivery.
- Full-part assembly still needs title/tease cards and final visual/audio/timing QC. The media-size estimate is documented in the batch QC report.
