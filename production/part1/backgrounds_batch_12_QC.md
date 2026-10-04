# Part 1 — Background Batch 12 QC (partial)

**Date:** 2026-10-04 UTC  
**Style lock:** HYBRID painterly-realistic Bronze Age environments; 2D characters are composited later.  
**Reference:** `production/assets/locations/loc_aulis_ref.png`.  
**Generation calls:** 10. **Accepted:** 9. **Rejected:** 1; not rerolled yet because the turn reached the image-call cap.  
**Progress:** 123 / 125 unique Part 1 plates accepted; 2 pending. Clips 01–23 are complete; clips 24 and 25 are each 4 / 5.

## Accepted image review

The nine accepted source files were opened individually and reviewed, then cross-checked in the labelled contact sheet. Each is 1376×768 and within the project’s accepted 16:9 tolerance. The Aulis palette and harbor continuity match the approved reference. The accepted set shows no people, animals, injury, text, logos, watermarks, or modern props; foreground staging remains clear.

| Clip / shot | File | Visual and QC note |
|---|---|---|
| 23 / 05 | `p1_clip_23_bg_05.jpg` | Still Aulis fleet and broad empty shore; sails appear slack. |
| 24 / 01 | `p1_clip_24_bg_01.jpg` | Plain linen peplos and olive wreath on an unmarked chest; no people/text. |
| 24 / 02 | `p1_clip_24_bg_02.jpg` | Empty camp and tents beside open beach and anchored ships. |
| 24 / 03 | `p1_clip_24_bg_03.jpg` | Aulis establishing harbor with camp, empty landing and clear ground. |
| 24 / 05 | `p1_clip_24_bg_05.jpg` | Reed canopy and plain garment at the edge; empty staging area. |
| 25 / 01 | `p1_clip_25_bg_01.jpg` | Diverging shore paths symbolise alternatives; no injury or figures. |
| 25 / 02 | `p1_clip_25_bg_02.jpg` | First breeze begins lifting sails at the empty harbor. |
| 25 / 03 | `p1_clip_25_bg_03.jpg` | Fleet starts leaving Aulis under a gentle breeze. |
| 25 / 04 | `p1_clip_25_bg_04.jpg` | Empty ship catches the breeze; clear shoreline foreground. |

## Rejected output and remaining work

- **Clip 24 / shot 04:** generated output showed pseudo-lettering / numeral-like marks on a wooden chest. Rejected under the no-text lock; the file is excluded from the manifest and removed. A reroll prompt that avoids marked props is saved in `next_background.json`.
- **Clip 25 / shot 05:** not generated in this batch.
- Contact sheet marks clip 24 / shot 04 as **REJECTED — PSEUDO-TEXT**; it is not represented as an accepted image.
- `.venv/bin/python tools/validate_part1.py` confirms the approved script remains verbatim, VO is unchanged, all 125 paths are unique, 123 plates are accepted, and 2 remain pending. Full-part render remains blocked.
- Next exact task: reroll `production/part1/backgrounds/p1_clip_24_bg_04.jpg`, then generate `production/part1/backgrounds/p1_clip_25_bg_05.jpg`.
