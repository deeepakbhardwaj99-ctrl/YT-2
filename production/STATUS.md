# Production Status — THE TROJAN WAR: THE FULL STORY (Hybrid v3)

**Repo:** `deeepakbhardwaj99-ctrl/YT-2` · **Branch:** `arena/01a1032c-yt-2`
**Format:** 16:9 (1920×1080) · **Target Pace:** ~130 wpm · **Parts:** 4 parts (~23.40 min total, 92 clips)
**Style Mode:** `HYBRID` (2D cartoon rigged characters + AI-generated painterly-realistic Bronze Age environments, no people/text in backgrounds)
**Motion:** `FULL ANIMATION` · **Preset:** `A — LIVELY EXPLAINER` (speech bubbles, callout cards, word pops, hops/pose swaps, 2s max static gate)
**Accent Color:** Burnt Orange `#9B3A12` · **Committed Display Font:** `production/fonts/DisplaySerif-Bold.ttf` (`DejaVuSerif-Bold`, open-licensed)

---

## Step 2 — Locked Part Structure Table (Original Unedited Script — 3,045 Spoken Words)

| Part | Sections | Spoken Words | Measured / Est. Runtime | Clips | Closing Line |
|---|---|---:|---:|---:|---|
| **Part 1: The Apple & The Fleet** | `[COLD OPEN]`, `[CH 1: THE UNINVITED GUEST]`, `[CH 2: THE OATH]`, `[CH 3: THE FLEET AT AULIS]` | 885 | **6.78 min (406.63s measured VO @ 130.6 wpm)** | **25** | *"The wind rose. The fleet sailed. And Clytemnestra, back in Mycenae, began to wait."* |
| **Part 2: The Wrath of Achilles** | `[CH 4: NINE YEARS OF NOTHING]`, `[CH 5: THE ARGUMENT]`, `[CH 6: A DUEL AND A GOODBYE]`, `[CH 7: ARMOR]` | 780 | ~6.00 min (360.0s est.) | 24 | *"The spear went through his neck. Achilles tied the body behind his chariot and dragged it around Patroclus's tomb every morning, for twelve days."* |
| **Part 3: The Fall of Heroes & The Wooden Horse** | `[CH 8: THE KING IN THE TENT]`, `[CH 9: THE DEATH OF ACHILLES]`, `[CH 10: THE HORSE]` | 780 | ~6.00 min (360.0s est.) | 24 | *"He held it there until she went away. The Trojans pulled the horse inside. They celebrated all night, and then they slept."* |
| **Part 4: Ashes, Homecoming & History** | `[CH 11: THE NIGHT TROY BURNED]`, `[CH 12: THE ROAD HOME]`, `[CH 13: SO WHAT ACTUALLY HAPPENED?]` | 600 | ~4.62 min (276.9s est.) | 19 | *"In the Greek version, it all began with a guest list. A party, and one goddess nobody thought to invite."* |
| **TOTAL** | **14 sections** | **3,045** | **~23.40 min** | **92** | |

---

## Pipeline Gate Checklist & Asset Progress

- [x] **STEP 0 — Workspace Audit:** Completed.
- [x] **STEP 1 — Script Lock 🔒:** Approved by user. Locked verbatim in `production/script_approved.txt`.
- [x] **STEP 2 — Part Structure:** Computed and saved in `production/parts_breakdown.json`.
- [x] **STEP 3 — Character & Hybrid Location Sheets 🔒 (APPROVED — user “continue”, 2026-10-04):**
  - **Character Sheets (9/9 complete & QC'd):** `production/assets/characters/character_contact_grid.png`
  - **Hybrid Location Sheets (5/5 primary refs + 2×2 angle grids complete & QC'd):**
    - `production/assets/locations/locations_contact_grid.jpg` (Master Contact Grid)
    - `loc_troy_ref.png` + `loc_troy_grid.jpg` (`_wide`, `_med`, `_detail`, `_night`)
    - `loc_camp_ref.png` + `loc_camp_grid.jpg` (`_wide`, `_med`, `_detail`, `_night`)
    - `loc_palace_ref.png` + `loc_palace_grid.jpg` (`_wide`, `_med`, `_detail`, `_night`)
    - `loc_olympus_ref.png` + `loc_olympus_grid.jpg` (`_wide`, `_med`, `_detail`, `_night`)
    - `loc_aulis_ref.png` + `loc_aulis_grid.jpg` (`_wide`, `_med`, `_detail`, `_night`)
- [x] **STEP 5 — Voiceover Auditions 🔒 & VO Progress:**
  - All 5 voices selected and mapped in `production/voices.json`.
  - **Part 1 VO:** 25/25 clips complete & QC'd (`406.63s` / `6.78 min` @ `130.6 wpm`).
  - **Part 2 VO:** 7/8 raw voice batches generated (`p2_narr_c4`, `p2_narr_c5`, `p2_narr_c6`, `p2_v02_a`, `p2_v02_b`, `p2_v03`, `p2_v04`); Ch 7 narrator remaining next turn.
  - **Part 3 VO:** 1/5 raw voice batches generated (`p3_narr_c8`).
- [x] **STEP 6 — Procedural Music Bed & Stems:**
  - `part1_stem.mp3`–`part4_stem.mp3` + `pop.wav`, `whoosh.wav`, `arrow.wav` complete.
- [x] **STEP 6B — Rig Packs + Face Calibration Sheet 🔒 & First Animated Scene Preview 🔒 (APPROVED — user “continue”, 2026-10-04):**
  - **Rig Packs & Alignment IoU (`production/assets/rigs/rig_calibration_sheet.jpg`):**
    - `mascot`: IoU = **0.89** (`PASS >= 0.80`)
    - `achilles`: IoU = **0.84** (`PASS >= 0.80`)
    - `odysseus`: IoU = **0.85** (`PASS >= 0.80`)
    - `agamemnon`: IoU = **0.91** (`PASS >= 0.80`)
    - `hector`: IoU = **0.87** (`PASS >= 0.80`)
  - **Per-Scene Plan (`production/scenes.json`):** 25 clips / 125 shot entries for Part 1.
  - **First Assembled Animated Scene Preview (`production/part1/scene_01_preview.mp4`):**
    - Duration: `38.13s` @ 24 fps · Mean frame diff: `5.395` · Max frozen stretch: `0.00s` (`PASS <= 2.00s`).
    - Motion report: `production/part1/scene_01_motion_report.txt` · Spot frames: `production/part1/scene_01_spot_frames.jpg`.
- [ ] **STEP 7 & 8 — Part-by-Part Production & QC (Parts 1 → 4 + Master MP4)**


## Current batch — 2026-10-04
- User approved Step 3 locations/characters and Step 6B rigs/motion with “continue”.
- Restored accepted assets from GitHub commit `99259ae`; original script remains unchanged.
- Part 1 production backgrounds: **30/125 unique scene plates accepted**, 95 remaining. Reference angle crops are NOT counted as unique production plates.
- Clips 01–06: 5/5 plates each individually viewed; no visible people/text; palette and empty foreground checked. These are imagined reconstructions, not exact archaeological reconstructions.
- Density: five distinct generated backgrounds per clip. Full Part 1 assembly is blocked until all 125 plates are accepted. No additional Part 2/3 generation before Part 1 delivery.
- Next: clip 07 (five plates), then clips 08–25. Replaced recycled card selection with 25 narration-specific cards; script and VO timings verified unchanged.

- Batch review: `production/part1/backgrounds_batch_01_contact.jpg`; checklist: `backgrounds_batch_01_QC.md`; machine validation: `background_validation.json`.
- Validation passed: 25 clips, 125 unique planned paths, 30 accepted plates, 95 pending; deliberate full-render readiness check correctly fails while images are missing.
- Approved style preview is preserved, not a final Part 1 deliverable. Final title/tease cards, detailed text/speaker timing, ground placement and audio/motion QC remain open.
- Encoding cap corrected to 1.4 Mbps video + 192 kbps audio (~81 MB cap estimate for 406.63s, not a measured file size). See batch QC for correction to prior estimate.
- Python environment restored from `tools/requirements.txt`; system ffmpeg/ffprobe must be installed before rendering in this restored sandbox.

## Background batch 02 — complete (2026-10-04)
- Clip 03: 5/5 newly generated plates individually viewed and accepted; approved Olympus reference used throughout.
- Clip 04: 5/5 newly generated plates individually viewed and accepted. Original script, VO and approved rig assets unchanged.

- Batch 02: 10/10 accepted, no image re-rolls; prophecy plate 03/05 intentionally cooler, with gold/marble continuity retained.
- Production total: 20/125 (16%); no full-part render attempted with the remaining 105 backgrounds missing.
- Batch 02 review: `production/part1/backgrounds_batch_02_contact.jpg`; QC: `production/part1/backgrounds_batch_02_QC.md`. Both the ten individual source images and final contact sheet were viewed.
- Validation reconfirmed script/VO unchanged, all 20 accepted hashes/dimensions valid, deterministic plan regeneration, and full-render readiness correctly blocked by 105 pending plates.
- Reusable contact-sheet tool: `.venv/bin/python tools/build_background_contact.py --clips 3 4 --batch 2` (use new clip/batch numbers on subsequent batches).

## Background batch 03 — complete
- Clip 05: 5/5 accepted. Clip 06: 5/5 accepted. One clip 05 image corrected to remove modern-looking string lights before acceptance.
- Golden apple introduced without generated lettering. Inscription, rolling motion, and protected-object clearance remain assembly work.

- Resumed interrupted turn from saved commit `56a15c1`; remaining clip 06 plates completed. One detail plate re-rolled for a genuinely different camera angle. Apple safety boxes and no-character insert intent saved in manifest; renderer integration still pending.
