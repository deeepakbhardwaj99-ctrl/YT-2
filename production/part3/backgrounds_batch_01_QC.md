# Part 3 Background Batch 01 — QC Record

**Scope:** 10 initial candidates (4 for clip 01, 6 for clip 02) and 8 targeted reroll candidates. All 18 images were opened individually from filename-bannered review copies; the embedded filename, dimensions, top-centre RGB median and SHA-256 prefix were checked against each source. Every candidate was 1376×768. No candidate contained people/faces/bodies, text/letters/numbers/inscriptions, logos/watermarks or modern objects.

**Result: Batch 01 complete.** All 10 planned plates passed individual visual review. Eight reroll attempts were used across the seven initially rejected plates; `p3_clip_02_bg_03` required its second and final allowed reroll. No later batch has been generated. The ledger records all 10 accepted plates and their hashes; rejected attempts are not renderable.

## Accepted plates

| Plate | SHA-256 prefix | QC |
|---|---|---|
| `p3_clip_01_bg_01.jpg` | `ee142812cef6` | Original candidate passed: moonlit establishing view, period camp/coast, clear sandy lower staging, no prohibited content. |
| `p3_clip_01_bg_02.jpg` | `bb816d8afafd` | Original candidate passed: distinct oblique moonlit camp and open central path; no prohibited content. |
| `p3_clip_01_bg_03.jpg` | `fc8cb9444e8b` | Reroll passed: empty moonlit beach camp, open sandy lower third, no cart/chariot/wheeled vehicle or prohibited content. |
| `p3_clip_01_bg_04.jpg` | `8edc5ba60095` | Original candidate passed: reverse camp/coast view with open lower-center sand; no prohibited content. |
| `p3_clip_02_bg_01.jpg` | `984771f5e561` | Reroll passed: clearly night-lit tent interior, open floor, moonlit sea at entrance. |
| `p3_clip_02_bg_02.jpg` | `25e8503c9922` | Reroll passed: quiet night interior with period stool/linen/lamp and clear lower staging. |
| `p3_clip_02_bg_03.jpg` | `a08ca821e68f` | Final reroll passed: enclosed canvas command-tent interior, small dark doorway, bronze lamp and broad open lower-third floor. |
| `p3_clip_02_bg_04.jpg` | `764c19a9c7f8` | Reroll passed: reverse wide tent-interior view, dark moonlit exterior, open floor. |
| `p3_clip_02_bg_05.jpg` | `a2527cf49bdc` | Reroll passed: lamp-lit night interior, period furnishings, unobstructed lower-third floor. |
| `p3_clip_02_bg_06.jpg` | `47849e10c361` | Reroll passed: tent interior receding to a dark moonlit entrance, open lower staging. |

## Rejected attempts (all replaced by accepted candidates)

| Plate | Attempt | Candidate SHA-256 prefix | Finding |
|---|---:|---|---|
| `p3_clip_01_bg_03.jpg` | 0 (initial) | `1ca6a849997b` | A large unprompted wheeled cart/chariot and clustered props intruded into lower-third staging; reroll 1 passed. |
| `p3_clip_02_bg_01.jpg` | 0 (initial) | `046bcbd1a22d` | Bright daytime exterior broke the established moonlit-night continuity; reroll 1 passed. |
| `p3_clip_02_bg_02.jpg` | 0 (initial) | `04c901c52b9a` | Bright daytime lighting broke night continuity; reroll 1 passed. |
| `p3_clip_02_bg_03.jpg` | 0 (initial) | `062ff4ca1552` | Bright daytime lighting broke night continuity. |
| `p3_clip_02_bg_03.jpg` | 1 (reroll) | `1e449c69107c` | Night-lit but showed an exterior beach/camp vista rather than the command-tent interior; final reroll 2 passed. |
| `p3_clip_02_bg_04.jpg` | 0 (initial) | `c4afb8f8bb87` | Bright daytime exterior broke night continuity; reroll 1 passed. |
| `p3_clip_02_bg_05.jpg` | 0 (initial) | `2689880a247f` | Pink dusk/daylight broke night continuity; reroll 1 passed. |
| `p3_clip_02_bg_06.jpg` | 0 (initial) | `1d0c58755691` | Bright daytime lighting broke night continuity; reroll 1 passed. |

Per-plate candidate hashes, dimensions, QC notes and reroll counters are in `production/part3/background_manifest.json`. Batch 02 remains unstarted pending the next explicit continue instruction.
