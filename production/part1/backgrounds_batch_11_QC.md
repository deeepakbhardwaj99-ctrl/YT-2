# Part 1 — Background Batch 11 QC

**Date:** 2026-10-04 UTC  
**Style lock:** HYBRID, painterly-realistic Bronze Age environments; 2D characters are composited later.  
**Reference:** `production/assets/locations/loc_aulis_ref.png` for all ten images.  
**Generation result:** 10 new images accepted, 0 rerolls.  
**Progress after batch:** 114 / 125 unique Part 1 plates accepted; 11 pending. Clips 01–22 complete; clip 23 is 4 / 5.

## Individual image review

All ten source files were opened individually and reviewed, then cross-checked in the labelled contact sheet. Each image is 1376×768 and within the project’s accepted 16:9 tolerance. Aulis palette and harbor continuity match the approved location reference. The clip 23 plates communicate windless waiting ships. No generated people, crews, animals, text, logos, watermarks, or modern props appear; staging foreground remains available.

| Clip / shot | File | Visual and QC note |
|---|---|---|
| 21 / 05 | `p1_clip_21_bg_05.jpg` | Curving Aulis beach, calm ships and a low rocky island horizon; open foreground. |
| 22 / 01 | `p1_clip_22_bg_01.jpg` | Contemplative cove, still ships and open pebbled shore. |
| 22 / 02 | `p1_clip_22_bg_02.jpg` | Unmarked spear, shield and folded mantle at the edge of the landing. |
| 22 / 03 | `p1_clip_22_bg_03.jpg` | Slack mooring rope and weathered ring on pale quay; no marks. |
| 22 / 04 | `p1_clip_22_bg_04.jpg` | Low oblique empty beach toward motionless ships under limestone hills. |
| 22 / 05 | `p1_clip_22_bg_05.jpg` | Establishing view from rocky point toward anchored fleet and distant island. |
| 23 / 01 | `p1_clip_23_bg_01.jpg` | Empty ship with limp sail beside still water and clear landing. |
| 23 / 02 | `p1_clip_23_bg_02.jpg` | Motionless sailcloth and slack rigging; no crew or symbols. |
| 23 / 03 | `p1_clip_23_bg_03.jpg` | Wide anchored fleet with every sail slack and an empty beach. |
| 23 / 04 | `p1_clip_23_bg_04.jpg` | Natural elevated panorama of crowded fleet, glassy inlet and open foreground. |

## Checks

- Full generation prompts, location references, exact dimensions, and SHA-256 hashes are recorded in `production/scenes.json` and `production/part1/background_manifest.json`.
- `backgrounds_batch_11_contact.jpg` is the labelled review sheet; missing clip 23 shot 05 is not included or counted.
- `.venv/bin/python tools/validate_part1.py` confirms the approved script is verbatim, VO segments are unchanged, all 125 planned paths are unique, 114 plates are accepted, and 11 remain pending. Full-part assembly remains blocked.
- Next exact asset: `production/part1/backgrounds/p1_clip_23_bg_05.jpg` (see `next_background.json`).
