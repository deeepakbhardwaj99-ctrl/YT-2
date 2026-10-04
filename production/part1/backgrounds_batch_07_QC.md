# Part 1 — Background Batch 07 QC

**Date:** 2026-10-04 UTC  
**Style lock:** HYBRID, cinematic painterly-realistic Bronze Age environments; 2D characters are composited later.  
**Reference:** `production/assets/locations/loc_palace_ref.png` passed to every generation.  
**Generation result:** 10 new images accepted, 0 rerolls.  
**Progress after batch:** 74 / 125 unique Part 1 plates accepted; 51 pending. Clips 01–14 complete; clip 15 is 4 / 5.

## Individual image review

All files below were opened and viewed individually after generation. Each is 1376×768 (16:9), visually distinct, and consistent with the approved Royal Palace of Sparta palette and architectural motifs. No people, faces, text, watermarks, or modern objects were visible. The foreground and staging space remain clear for the later 2D rigs.

| Clip / shot | File | Visual and QC note |
|---|---|---|
| 13 / 05 | `backgrounds/p1_clip_13_bg_05.jpg` | Side doorway into a quiet courtyard, chairs and folded ivory cloth; open foreground and wall; no people/text. |
| 14 / 01 | `backgrounds/p1_clip_14_bg_01.jpg` | Uninscribed bronze horse figurine, bowl, and linen in an empty ceremonial room; no sacrifice, blood, people, or text. |
| 14 / 02 | `backgrounds/p1_clip_14_bg_02.jpg` | Empty oath hall, benches and modest platform; broad clear lower foreground. |
| 14 / 03 | `backgrounds/p1_clip_14_bg_03.jpg` | New corner view of the courtyard, steps and distant tether posts; no people/text. |
| 14 / 04 | `backgrounds/p1_clip_14_bg_04.jpg` | Colonnade framing an empty courtyard and a small offering setup; clear ground. |
| 14 / 05 | `backgrounds/p1_clip_14_bg_05.jpg` | Side-chamber angle through a painted doorway into the oath hall; no people/text. |
| 15 / 01 | `backgrounds/p1_clip_15_bg_01.jpg` | Empty guest dining hall with couches, low table and bronze cups; no people/text. |
| 15 / 02 | `backgrounds/p1_clip_15_bg_02.jpg` | Palace gate opening to olive trees and low hills; clear lower foreground. |
| 15 / 03 | `backgrounds/p1_clip_15_bg_03.jpg` | Quiet banquet room with empty couches and corridor; warm material continuity. |
| 15 / 04 | `backgrounds/p1_clip_15_bg_04.jpg` | Empty guest room with bench, linen and bronze lamp; no people/text. |

## Checks

- Full prompts are recorded per shot in `production/scenes.json` and copied into `production/part1/background_manifest.json`.
- SHA-256, dimensions, reference, shot type, and QC notes are recorded in the accepted-asset manifest.
- Contact sheet: `backgrounds_batch_07_contact.jpg`. Clip 15 shot 05 is labelled **NOT GENERATED — PENDING** and is not counted as accepted.
- `.venv/bin/python tools/validate_part1.py` confirms verbatim script, unchanged VO segment timing, 125 unique planned paths, 74 accepted images, and 51 pending images. Full-part assembly remains blocked until all 125 plates are accepted.
- Next exact asset: `production/part1/backgrounds/p1_clip_15_bg_05.jpg` (see `next_background.json`).
