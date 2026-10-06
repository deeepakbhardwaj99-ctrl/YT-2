# Part 3 Background Batch 06 — QC Record

**Scope:** 10 initial candidates: five prophecy-tent interiors (clip 12) and five Trojan-field/gate plates (clip 13). Each image was opened individually from a filename-bannered review copy; the embedded filename, dimensions, top-centre RGB median and SHA-256 prefix were checked against the source. All 10 were 1376×768. No image contained people/faces/bodies, text/letters/numbers/inscriptions, logos/watermarks or modern objects.

**Result:** 9 accepted; 1 pending targeted reroll. The rejected image's bow extends into lower-centre character staging. Its original is out of the production background directory, and the plate has two rerolls remaining. Batch 06 is not complete; no later batch has been generated.

## Accepted

| Plate | SHA-256 prefix | QC |
|---|---|---|
| `p3_clip_12_bg_01.jpg` | `c89deb00570e` | Empty prophecy tent, blank niche and bow/table detail; clear lower floor. |
| `p3_clip_12_bg_02.jpg` | `7e0a3e6a4d47` | Wide canvas-tent interior with open entrance, bow/table aside and generous staging floor. |
| `p3_clip_12_bg_04.jpg` | `6a88e8b6462c` | Tent corridor/detail, clear floor, blank niche and bow/table in the midground. |
| `p3_clip_12_bg_05.jpg` | `593542026a5e` | Reverse tent view, warm lamplight and bow/table to one side; open floor. |
| `p3_clip_13_bg_01.jpg` | `7348a8539854` | Broad dawn field and distant Troy; bow/arrow and ledge at far edge, central staging open. |
| `p3_clip_13_bg_02.jpg` | `a062e8104a59` | Raised empty field and weathered gate, bow/arrow off-centre, lower ground open. |
| `p3_clip_13_bg_03.jpg` | `3e058ba19246` | Side-angle gate detail with bow at the edge and clear central foreground. |
| `p3_clip_13_bg_04.jpg` | `23fe179c9950` | Distant reverse gate view, broad empty ground and bow/arrow at far-side ledge. |
| `p3_clip_13_bg_05.jpg` | `2fce8b46308d` | Wide dawn view, bow/arrow set to one side and open staging foreground. |

## Pending targeted reroll

| Plate | Candidate SHA-256 prefix | Finding / correction |
|---|---|---|
| `p3_clip_12_bg_03.jpg` | `26b0aa453e42` | The bow leans down from the table into lower-centre staging. Reroll with the bow laid flat on the off-centre tabletop in the midground and the full lower third clear of props. |

The pending prompt now encodes that correction. Candidate hashes, QC notes and the reroll counter are in `production/part3/background_manifest.json`.
