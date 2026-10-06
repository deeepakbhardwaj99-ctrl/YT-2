# Part 3 Background Batch 02 — QC Record

**Scope:** 10 initial candidates: five for clip 03 (the shared-meal tent interior) and five for clip 04 (first-light beach camp). Each image was opened individually from a filename-bannered review copy. The embedded filename, dimensions, top-centre RGB median and SHA-256 prefix were checked against its source. All 10 were 1376×768. No image contained people/faces/bodies, text/letters/numbers/inscriptions, logos/watermarks or modern objects.

**Result:** 5 accepted; 5 pending targeted rerolls. Three clip-03 interiors otherwise looked suitable but showed daylight through the entrance, breaking continuity with Priam's approach and plea on the same twelfth night. Two clip-04 plates placed the firepit in the lower-third staging area. Rejected originals are out of the production background directory; each pending plate has two rerolls remaining. Batch 02 is not complete, and no later batch has been generated.

## Accepted

| Plate | SHA-256 prefix | QC |
|---|---|---|
| `p3_clip_03_bg_02.jpg` | `9efee0103818` | Ground-level tent detail, restrained tableware/linen and clear lower staging; no visible daylight or prohibited content. |
| `p3_clip_03_bg_05.jpg` | `f832ab4cb3b6` | Warm lamp-lit tent detail with linen and bowl; lower third open and no visible daylight or prohibited content. |
| `p3_clip_04_bg_02.jpg` | `128ca7aadd04` | Wide first-light reverse beach-camp view, period tents/shoreline and broad open sand. |
| `p3_clip_04_bg_03.jpg` | `be57202ab99b` | Raised dawn view with the firepit set back from the open foreground. |
| `p3_clip_04_bg_05.jpg` | `b34abe0a731d` | Distant reverse dawn view, sparse tents and firepit in the midground, clear sandy foreground. |

## Pending targeted rerolls

| Plate | Candidate SHA-256 prefix | Finding / correction |
|---|---|---|
| `p3_clip_03_bg_01.jpg` | `94aaf1e6921b` | Bright daylight is visible through the tent entrance during the continuous twelfth-night meal scene. Reroll with a warm bronze-lamp interior and only deep blue-black night beyond the entrance. |
| `p3_clip_03_bg_03.jpg` | `dec6dce1ebfd` | Wide tent interior opens onto bright daylight, breaking continuity with the same-night sequence. Reroll with a dark night entrance and warm lamp; no dawn/daylight. |
| `p3_clip_03_bg_04.jpg` | `4f8b456e8f70` | Daylight is visible through the entrance. Reroll with the same explicit night-continuity constraints. |
| `p3_clip_04_bg_01.jpg` | `5a30a8418a1c` | Firepit and two vessels intrude into lower-right staging. Set the firepit off-centre in the midground and keep the full lower third clear; no foreground vessels. |
| `p3_clip_04_bg_04.jpg` | `d9f32754f33e` | Large firepit is centered in the lower foreground. Keep the low side angle but move the pit back to the off-centre midground, leaving the lower third clear sand. |

The pending prompts now explicitly enforce the continuous night for clip 03 and clear lower-third staging for clip 04. Ledger hashes, visual notes and per-plate reroll counters are in `production/part3/background_manifest.json`.
