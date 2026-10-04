# Part 1 — Background Batch 08 QC

**Date:** 2026-10-04 UTC  
**Style lock:** HYBRID, painterly-realistic Bronze Age environments; 2D characters are composited later.  
**Reference:** `production/assets/locations/loc_palace_ref.png` passed to every generation.  
**Generation result:** 10 new images accepted, 0 rerolls.  
**Progress after batch:** 84 / 125 unique Part 1 plates accepted; 41 pending. Clips 01–16 complete; clip 17 is 4 / 5.

## Individual image review

All ten files were opened and viewed individually after generation. Each is a clean palace-environment plate consistent with the approved red-ochre, timber, bronze and warm-stone palette. No people, faces, readable writing, logos, watermarks or modern objects were visible. The lower staging areas remain suitable for later 2D rigs.

| Clip / shot | File | Visual and QC note |
|---|---|---|
| 15 / 05 | `backgrounds/p1_clip_15_bg_05.jpg` | Empty guest room with open storage chest, folded linen and bronze lamp; no people/text. **1365×768**, within 16:9 tolerance. |
| 16 / 01 | `backgrounds/p1_clip_16_bg_01.jpg` | Empty hall with two open routes, preserving ambiguity around Helen’s departure. |
| 16 / 02 | `backgrounds/p1_clip_16_bg_02.jpg` | Empty private chamber, half-open courtyard door and folded cloth; no sign of force. |
| 16 / 03 | `backgrounds/p1_clip_16_bg_03.jpg` | Dressing alcove with mirror turned away; no reflected person. |
| 16 / 04 | `backgrounds/p1_clip_16_bg_04.jpg` | Detail of a quiet threshold and untouched bronze cup; no human-shaped shadows. |
| 16 / 05 | `backgrounds/p1_clip_16_bg_05.jpg` | Balcony and courtyard with two open passages; neutral, unresolved mood. |
| 17 / 01 | `backgrounds/p1_clip_17_bg_01.jpg` | Empty council hall, stools and unmarked bronze helmets; lower staging area clear. |
| 17 / 02 | `backgrounds/p1_clip_17_bg_02.jpg` | Table-height view with a small wooden ship model and bronze bowl; no map or writing. |
| 17 / 03 | `backgrounds/p1_clip_17_bg_03.jpg` | Vacant council seat and folded red cloak with a plain bronze object; no lettering or insignia. |
| 17 / 04 | `backgrounds/p1_clip_17_bg_04.jpg` | Empty colonnaded passage toward a sunlit gate, with vacant benches; no harbor or ships. |

## Checks

- Full generation prompts are stored in `production/scenes.json` and `production/part1/background_manifest.json`.
- SHA-256, exact dimensions, reference, shot type and QC notes are recorded per accepted image.
- Contact sheet: `backgrounds_batch_08_contact.jpg`; clip 17 shot 05 is explicitly marked **NOT GENERATED — PENDING** and is not counted.
- `.venv/bin/python tools/validate_part1.py` confirms the script remains verbatim, VO segments are unchanged, all 125 planned paths are unique, 84 plates are accepted, and 41 remain pending. Full-part assembly is still blocked.
- Next exact asset: `production/part1/backgrounds/p1_clip_17_bg_05.jpg` (see `next_background.json`).
