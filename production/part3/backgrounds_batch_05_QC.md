# Part 3 Background Batch 05 — QC Record

**Scope:** 10 initial candidates: two pavilion/war-council interiors (clips 09–10) and six empty-pen environments (clip 11). Each image was opened individually from a filename-bannered review copy; embedded filename, dimensions, top-centre RGB median and SHA-256 prefix were verified against the source. All 10 were 1376×768. No people/faces/bodies, text/letters/numbers/inscriptions, logos/watermarks or modern objects were visible.

**Result:** 7 accepted; 3 pending targeted rerolls. Failures were composition/content: a central display intruded into the lower-third floor, one image rendered the council tent as an exterior camp, and one pen detail put fence rails/trough into the foreground. Rejected originals are out of the production directory; each pending plate has two rerolls remaining. Batch 05 is not complete, and no later batch has been generated.

## Accepted

| Plate | SHA-256 prefix | QC |
|---|---|---|
| `p3_clip_09_bg_05.jpg` | `0d40e24bf0bc` | Empty command pavilion with inanimate bronze armor/shield display in the midground and usable open foreground. |
| `p3_clip_10_bg_01.jpg` | `a0dcfe783ea0` | Clear war-council tent interior; empty bench and armor set aside, lower floor open. |
| `p3_clip_11_bg_01.jpg` | `8a80911e0abc` | Cold-dawn pen, trough set back near the fence, open foreground; no animals or remains. |
| `p3_clip_11_bg_02.jpg` | `2b1445b5b46d` | Ground-level pen detail with fence/trough behind the clear lower-third floor. |
| `p3_clip_11_bg_03.jpg` | `6ff75459b636` | Reverse wide empty pen with open foreground and no animals or remains. |
| `p3_clip_11_bg_04.jpg` | `2dae8757f5ee` | Raised view; trough/fence remain in the midground, lower third open. |
| `p3_clip_11_bg_06.jpg` | `92643f38d5a3` | Distant reverse pen view with trough set back and broad open foreground. |

## Pending targeted rerolls

| Plate | Candidate SHA-256 prefix | Finding / correction |
|---|---|---|
| `p3_clip_09_bg_06.jpg` | `4b4712c52893` | Armor/shield display and broad stand occupy central lower staging. Move the inanimate display off-centre into the midground; keep the full lower third bare floor and avoid mannequin-like forms. |
| `p3_clip_10_bg_02.jpg` | `ab16720530c1` | Rendered an exterior camp rather than the planned war-council tent interior. Show the canvas roof/walls from inside, bench/armor to one side and clear lower-third floor. |
| `p3_clip_11_bg_05.jpg` | `afb3e235657e` | Foreground rails and tipped trough intrude into lower staging. Keep the fence/trough behind the open foreground and leave the whole lower third clear. |

The pending prompts now encode these targeted corrections. Candidate hashes, visual notes and per-plate reroll counters are in `production/part3/background_manifest.json`.
