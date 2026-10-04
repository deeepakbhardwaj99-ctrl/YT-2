# Part 1 — Background Batch 09 QC

**Date:** 2026-10-04 UTC  
**Style lock:** HYBRID, painterly-realistic Bronze Age environments; 2D characters are composited later.  
**References:** `loc_palace_ref.png` for clip 17 shot 05; `loc_aulis_ref.png` for all clip 18–19 backgrounds.  
**Generation result:** 10 new images accepted, 0 rerolls.  
**Progress after batch:** 94 / 125 unique Part 1 plates accepted; 31 pending. Clips 01–18 complete; clip 19 is 4 / 5.

## Individual image review

All ten source files were opened individually and reviewed, then checked in the labelled contact sheet. Every image is 1376×768 and within the project's accepted 16:9 tolerance. Location palette and composition match the approved references. No generated people, faces, text, logos, watermarks, modern props, infant, or injury appear; all lower foregrounds are suitable for later 2D character staging.

| Clip / shot | File | Visual and QC note |
|---|---|---|
| 17 / 05 | `backgrounds/p1_clip_17_bg_05.jpg` | Quiet Sparta palace gate hall opens to a sunny courtyard; clear foreground; no people/text. |
| 18 / 01 | `backgrounds/p1_clip_18_bg_01.jpg` | Aulis establishing view: sheltered inlet, Bronze Age ships, limestone hills and empty beach. |
| 18 / 02 | `backgrounds/p1_clip_18_bg_02.jpg` | Salt-and-plow detail with hoofprints; no people or animals. |
| 18 / 03 | `backgrounds/p1_clip_18_bg_03.jpg` | Wide beach, shallow salt furrows and unattended plow; no people/animals. |
| 18 / 04 | `backgrounds/p1_clip_18_bg_04.jpg` | Oblique harbor view from a low dock; distinct angle, empty staging beach. |
| 18 / 05 | `backgrounds/p1_clip_18_bg_05.jpg` | Curving beach, faint salt lines and plow; clear lower foreground. |
| 19 / 01 | `backgrounds/p1_clip_19_bg_01.jpg` | Close plow/hoofprint detail; no people, infant, animals or injury. |
| 19 / 02 | `backgrounds/p1_clip_19_bg_02.jpg` | Wide empty shore with separate furrow and hoofprint trails. |
| 19 / 03 | `backgrounds/p1_clip_19_bg_03.jpg` | Inland-facing scrub and stony ground with tracks and furrows. |
| 19 / 04 | `backgrounds/p1_clip_19_bg_04.jpg` | Salt furrow curves beside separate hoofprints; non-violent and text-free. |

## Checks

- Full generation prompts are stored in `production/scenes.json` and `production/part1/background_manifest.json`.
- SHA-256, exact dimensions, location references, shot types and QC notes are saved for every accepted plate.
- Contact sheet: `backgrounds_batch_09_contact.jpg`. Clip 19 shot 05 is labelled **NOT GENERATED — PENDING** and is not counted.
- `.venv/bin/python tools/validate_part1.py` confirms the script remains verbatim, VO segments are unchanged, all 125 planned paths are unique, 94 plates are accepted, and 31 remain pending. Full-part assembly remains blocked.
- Next exact asset: `production/part1/backgrounds/p1_clip_19_bg_05.jpg` (see `next_background.json`).
