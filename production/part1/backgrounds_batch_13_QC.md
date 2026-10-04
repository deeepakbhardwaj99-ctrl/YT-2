# Part 1 — Background Batch 13 QC

**Date:** 2026-10-04 UTC  
**Generation result:** 2/2 accepted; the clip 24 shot 04 image is the successful reroll after batch 12’s pseudo-text rejection.  
**Reference:** `production/assets/locations/loc_aulis_ref.png`.

| Clip / shot | File | Visual and QC note |
|---|---|---|
| 24 / 04 | `p1_clip_24_bg_04.jpg` | Corrective image: empty Aulis landing, distant camp and ships; clear foreground; no text or pseudo-marks. |
| 25 / 05 | `p1_clip_25_bg_05.jpg` | Ship stern and gentle wake toward open inlet; no crew, symbols or text. |

Both sources were individually viewed and confirmed as 1376×768, within the accepted 16:9 tolerance. They match the approved harbor palette and have no people, animals, injuries, writing, modern props, logos or watermarks. The final two-plate contact sheet is saved as `backgrounds_batch_13_contact.jpg`.

`.venv/bin/python tools/validate_part1.py` confirms 125 unique planned paths, 125 accepted, 0 pending, locked script verbatim, and VO unchanged. Part 1 backgrounds are complete; full assembly now requires `ffmpeg` and `ffprobe`.
