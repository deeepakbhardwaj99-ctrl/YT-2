# Part 1 — Background Batch 10 QC

**Date:** 2026-10-04 UTC  
**Style lock:** HYBRID, painterly-realistic Bronze Age environments; 2D characters are composited later.  
**Reference:** `production/assets/locations/loc_aulis_ref.png` for all ten images.  
**Generation result:** 10 new images accepted, 0 rerolls.  
**Progress after batch:** 104 / 125 unique Part 1 plates accepted; 21 pending. Clips 01–20 complete; clip 21 is 4 / 5.

## Individual image review

All ten source files were opened individually and reviewed, then cross-checked in the labelled contact sheet. Each image is 1376×768 and within the project’s accepted 16:9 tolerance. Aulis palette, shoreline continuity, and clear staging areas match the approved location reference. No generated people, animals, infant, injury, text, logos, watermarks, or modern props appear.

| Clip / shot | File | Visual and QC note |
|---|---|---|
| 19 / 05 | `p1_clip_19_bg_05.jpg` | Plow handle, salt furrow and separate hoofprints; no people, animals, infant, injury or text. |
| 20 / 01 | `p1_clip_20_bg_01.jpg` | Aulis beach and anchored fleet; slack sails, broad open foreground. |
| 20 / 02 | `p1_clip_20_bg_02.jpg` | Elevated panoramic inlet and rocky headlands; empty foreground. |
| 20 / 03 | `p1_clip_20_bg_03.jpg` | Shore-level harbor view with still reflections and clear sand. |
| 20 / 04 | `p1_clip_20_bg_04.jpg` | Plain helmet and shield on stone ledge; no marks or lettering. |
| 20 / 05 | `p1_clip_20_bg_05.jpg` | Spear and shield edge with mooring rope; no symbols or text. |
| 21 / 01 | `p1_clip_21_bg_01.jpg` | Open inlet, distant rocky headland and anchored ships. |
| 21 / 02 | `p1_clip_21_bg_02.jpg` | Diagonal cove view toward an empty rocky shore and ships. |
| 21 / 03 | `p1_clip_21_bg_03.jpg` | Single empty moored ship and stone point against a hazy ridge. |
| 21 / 04 | `p1_clip_21_bg_04.jpg` | Furled sail and empty hull beside a clear stone landing. |

## Checks

- Full generation prompts, location references, exact dimensions, and SHA-256 hashes are recorded in `production/scenes.json` and `production/part1/background_manifest.json`.
- `backgrounds_batch_10_contact.jpg` is the labelled review sheet; missing clip 21 shot 05 is not included or counted.
- `.venv/bin/python tools/validate_part1.py` confirms the approved script is verbatim, VO segments are unchanged, all 125 planned paths are unique, 104 plates are accepted, and 21 remain pending. Full-part assembly remains blocked.
- Next exact asset: `production/part1/backgrounds/p1_clip_21_bg_05.jpg` (see `next_background.json`).
