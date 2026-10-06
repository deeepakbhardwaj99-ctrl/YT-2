# Part 3 Background Batch 08 — QC Record

**Scope:** 10 initial candidates: four additional beach-camp wooden-horse views (clip 16), five carpentry-yard views (clip 17), and the first interior view from inside the hollow horse (clip 18). All 10 were opened individually from filename-bannered review copies; filename, dimensions, top-centre RGB median and SHA-256 were checked against each source. Eight files are 1376×768 and two are 1365×768; both sizes are near the requested 16:9 format and within the project validator's aspect-ratio tolerance. No image contains people/faces/bodies, text/letters/numbers/inscriptions, logos/watermarks or modern objects. Any horse-shaped image is only an empty, inanimate timber framework.

**Result:** 9 accepted; 1 pending targeted reroll. The rejected carpentry-yard plate has large beam stacks filling most of the lower-right foreground. No later batch has been generated.

## Accepted

| Plate | Dimensions | SHA-256 prefix | QC |
|---|---:|---|---|
| `p3_clip_16_bg_03.jpg` | 1365×768 | `4d9113c9754e` | Oblique beach-camp view; timber framework left, broad clear sand staging at right. |
| `p3_clip_16_bg_04.jpg` | 1376×768 | `2fe9348fb74b` | Medium hollow-framework view at right, open beach floor at left. |
| `p3_clip_16_bg_05.jpg` | 1376×768 | `dc3e48fbb02c` | Close joinery and rope detail to the right; clear sand lane to the left. |
| `p3_clip_16_bg_06.jpg` | 1376×768 | `bf848d9b7113` | Reverse dawn view; framework in midground and broad sand foreground. |
| `p3_clip_17_bg_01.jpg` | 1376×768 | `5b6a9810dbaf` | Panoramic carpentry yard; materials at far sides and central sandy staging. |
| `p3_clip_17_bg_03.jpg` | 1376×768 | `7db6b4c000ae` | Peg-joint detail at right; empty path remains at left for staging. |
| `p3_clip_17_bg_04.jpg` | 1376×768 | `6661cc60d36a` | Low-angle yard; lumber frames the edges while central sand remains open. |
| `p3_clip_17_bg_05.jpg` | 1376×768 | `3e9093cf1ec0` | Reverse dawn view with materials in midground and broad empty sand foreground. |
| `p3_clip_18_bg_01.jpg` | 1365×768 | `7be5ca527078` | Interior view through the hollow horse's ribs; empty plank floor and no occupants. |

## Pending targeted reroll

| Plate | Candidate dimensions | Initial SHA-256 prefix | Finding / correction |
|---|---:|---|---|
| `p3_clip_17_bg_02.jpg` | 1376×768 | `84fd54630dda` | Rejected: lumber stacks spill across most of the lower-right foreground, leaving too little broad staging. Reroll with all lumber and pegs confined to far edges or distant midground, preserving a wide uninterrupted bare-sand lower third. |

The pending prompt now encodes that correction. Candidate hashes, QC notes and reroll counters are in `production/part3/background_manifest.json`.
