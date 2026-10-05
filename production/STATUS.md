# Production Status — THE TROJAN WAR: THE FULL STORY (Hybrid v3)

**Repo:** `deeepakbhardwaj99-ctrl/YT-2` · **Branch:** `arena/01a1063f-yt-2`
**Recovered checkpoint:** `origin/arena/01a1032c-yt-2` at `774100f` (2026-10-04); accepted assets and recorded approvals are reused, not regenerated.
**Locked script source:** `production/script_approved.txt` remains byte-identical to the supplied script; the separate retention draft is not the VO source. By explicit user approval, three non-graphic wording substitutions are permitted for Part 2 Chapter 7 narrator audio only; they are documented in `production/part2/chapter7_vo_override.json` and do not alter the locked source file.
**Part 1 status:** Complete — 125/125 accepted plates, all 25 clips assembled, rendered, and QC-passed. The full export and QC reports are saved under `production/part1/`; the approved preview is unchanged.
**Part 2 status:** VO and motion plan complete (24 measured clips / 123 unique plate slots). The five new character sheets were approved by the user with “continue” on 2026-10-05; all five static cutouts and face anchors pass visual QC. Background batches 01–05 are complete: 50/123 plates accepted, 73 pending (batch 05 included one corrective reroll).
## Current session — 2026-10-05
- Added a separate complete-Part-1 renderer at `tools/render_part1.py` (all 25 clips, animated 2.5-second opening title and Part II tease). It writes `production/part1/part1_full.mp4` and does not overwrite the approved clip 01 + 05 preview.
- Added exact per-clip VO sample trimming/padding against the locked timeline, frame-rounding audio tail compensation, a bounded background cache, and a music fade on the teaser card. Approved script text and VO segment records remain untouched.
- Added full-export QC tooling at `tools/qc_part1.py` and refreshed setup/assembly notes. FFmpeg 7.0.2 and FFprobe 4.0.2 are available locally in the ignored `.venv`.
- Full Part 1 export: `production/part1/part1_full.mp4` (25 clips + opening title/Part II tease, 1920×1080, 24 fps H.264/AAC, 411.71s, 73.21 MiB). Motion report: `production/part1/part1_motion_report.txt` (mean frame diff 4.560; max near-zero-motion stretch 0.00s — PASS).
- Delivery QC: `production/part1/part1_qc_report.txt` and `.json` — PASS. Full audio/video decode succeeded; 9,881 frames; decoded audio 411.733s vs 411.708s expected; peak −3.02 dBFS; audio RMS −20.99 dBFS; preview unchanged; output remains below GitHub's single-file size limit.
- Locked script, VO segments, accepted assets and approved preview were preserved. Part 1 is delivered; Step 7–8 remains open for Parts 2–4 and the master MP4.
- Part 2 narrator batch: after exact-text synthesis was blocked, the user approved three non-graphic Chapter 7 narrator-only substitutions; the locked source script remains unchanged. The missing raw narration was generated with selected voice `voice-00`: 222 words, 88.23s decoded, 151 WPM. Raw-audio QC/hash metadata: `production/part2/p2_narr_c7_manifest.json`; override: `production/part2/chapter7_vo_override.json`.
- Part 2 per-clip VO is complete: 24 clips, 776 words, 364.60s (6.08 min), 127.7 WPM average. All 8 raw batches map to the source lines, the approved VO override is applied, pace gates pass, and audio QC manifests are in `production/part2/part2_vo_manifest.json` and `part2_vo_qc_report.txt`/`.json`.
- Part 2 motion plan is complete and appended to `production/scenes.json` without changing the approved Part 1 plan. `production/part2/background_manifest.json` records 123 unique plates: 50 accepted and 73 pending. Twenty-three clips use five shots; `p2_clip_16` (23.678s / 50 words) uses eight (~2.96s per shot) for Preset A density. New dialogue/supporting character assignments, timed events, labels/callouts, camera moves, and text-free HYBRID prompts are included. See `production/part2/part2_scene_plan_notes.md`.
- Step 3 character-sheet gate cleared: the user approved all five new static designs (“continue”, 2026-10-05): Protesilaus, Philoctetes, Chryses, Patroclus, and Andromache holding Astyanax. Transparent cutouts are saved as `production/assets/rigs/cutout_{protesilaus,philoctetes,chryses,patroclus,andromache_astyanax}.png`; face anchors were appended to `char_anchors.json`, and speaker mappings were added to `tools/assemble.py`. Matte/anchor review: `production/part2/character_sheets/part2_cutout_calibration.jpg`; processor and hashes are recorded in the character-sheet manifest.
- Background batch 01: 10/10 plates for clips 01–02 individually viewed and accepted (0 rerolls); see `production/part2/backgrounds_batch_01_contact.jpg` and `backgrounds_batch_01_QC.md`.
- Background batch 02: 10/10 plates for clips 03–04 individually viewed and accepted (0 rerolls); see `production/part2/backgrounds_batch_02_contact.jpg` and `backgrounds_batch_02_QC.md`.
- Background batch 03: 10/10 plates for clips 05–06 individually viewed and accepted (0 rerolls). At that checkpoint, the total was 30/123 accepted, 93 pending. Contact sheet and QC: `production/part2/backgrounds_batch_03_contact.jpg` and `backgrounds_batch_03_QC.md`.
- Background batch 04: clips 07–08 complete; 10/10 plates individually viewed and accepted, with no rerolls. At that checkpoint: 40/123 accepted, 83 pending. Contact sheet and QC: `production/part2/backgrounds_batch_04_contact.jpg` and `backgrounds_batch_04_QC.md`.
- Background batch 05: clips 09–10 complete; all 10 plates individually reviewed and accepted after one corrective reroll. The first Olympus detail candidate (`p2_clip_10` shot 03) was rejected for a modern-looking grate and text-like ornament; its corrected, grate-free prompt produced the accepted replacement. Current total: 50/123 accepted, 73 pending. Contact sheet and QC: `production/part2/backgrounds_batch_05_contact.jpg` and `backgrounds_batch_05_QC.md`. Next: batch 06, clips 11–12.

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
  - **Original Character Sheets (9/9 complete & QC'd):** `production/assets/characters/character_contact_grid.png`
  - **Part 2 character-sheet extension (5/5 approved by user “continue”, 2026-10-05):** Protesilaus, Philoctetes, Chryses, Patroclus, and combined Andromache/Astyanax. Approval record and contact grid are under `production/part2/character_sheets/`; their five transparent static cutouts and face anchors are now QC-passed.
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
  - **Part 2 VO:** 8/8 raw batches processed into **24/24 per-clip MP3s** (`production/part2/vo/p2_clip_01.mp3`–`p2_clip_24.mp3`). Total: 776 voice words after the approved Chapter 7 VO-only override, 364.60s / 6.08 min, average 127.7 WPM; all clip/segment pace and line-coverage QC passed. Manifest and reports: `part2_vo_manifest.json`, `part2_vo_qc_report.txt`/`.json`.
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
  - **Per-Scene Plan (`production/scenes.json`):** Part 1 remains 25 clips / 125 accepted shot entries; Part 2 has 24 clips / 123 planned plates (30 accepted, 93 pending; `p2_clip_16` uses eight for its longer 23.678s VO clip). Step 3 is cleared and all new static cutouts/face anchors are QC-passed.
  - **First Assembled Animated Scene Preview (`production/part1/scene_01_preview.mp4`):**
    - Duration: `38.13s` @ 24 fps · Mean frame diff: `5.395` · Max frozen stretch: `0.00s` (`PASS <= 2.00s`).
    - Motion report: `production/part1/scene_01_motion_report.txt` · Spot frames: `production/part1/scene_01_spot_frames.jpg`.
- [ ] **STEP 7 & 8 — Part-by-Part Production & QC (Parts 1 → 4 + Master MP4)**


## Prior checkpoint — through batch 06 (2026-10-04)
- User approved Step 3 locations/characters and Step 6B rigs/motion with “continue”.
- Restored accepted assets from GitHub commit `99259ae`; original script remains unchanged.
- Part 1 production backgrounds: **64/125 unique scene plates accepted**, 61 remaining. Reference angle crops are NOT counted as unique production plates.
- Clips 01–12: 5/5 plates each individually viewed; no visible people/text; palette and empty foreground checked. These are imagined reconstructions, not exact archaeological reconstructions.
- Density: five distinct generated backgrounds per clip. Full Part 1 assembly is blocked until all 125 plates are accepted. No additional Part 2/3 generation before Part 1 delivery.
- Next: clip 13 shot 05, then clips 14–25. Replaced recycled card selection with 25 narration-specific cards; script and VO timings verified unchanged.

- Batch review: `production/part1/backgrounds_batch_01_contact.jpg`; checklist: `backgrounds_batch_01_QC.md`; machine validation: `background_validation.json`.
- Validation passed: 25 clips, 125 unique planned paths, 64 accepted plates, 61 pending; deliberate full-render readiness check correctly fails while images are missing.
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

## Background batch 04 — complete (2026-10-04)
- Resumed from authoritative GitHub commit `2641a66`; clips 05–06 already complete, not regenerated.
- Clip 07: 5/5 accepted after individual viewing. Clip 08: 5/5 accepted after individual viewing. Apple inserts remain text-free with composition notes recorded for assembly.

- Batch 04: 10/10 new plates, no re-rolls; Part 1 total 40/125 (32%), 85 remaining.
- Mount Ida is staged as a pastoral extension of the approved Troy regional palette, not Olympus or verified geographical reconstruction. Per-shot setting labels, Paris staging intent and apple safety regions are saved in scenes.json; renderer integration remains pending.
- Batch 04 review: `production/part1/backgrounds_batch_04_contact.jpg`; QC: `production/part1/backgrounds_batch_04_QC.md`. All ten sources and the final contact sheet were viewed.
- Automated checks passed: 40 accepted hashes/dimensions, script and VO unchanged, deterministic plan regeneration, protected-object/composition metadata preserved. Full-render readiness correctly blocked by 85 pending plates.

## Background batch 05 — in progress
- Clip 09: 5/5 individually viewed and accepted, using approved Troy reference and accepted Mount Ida continuity plates. Clip 10: 5/5 accepted after individual viewing; one ground-guide artifact corrected. Clip 11 next.
- Dream-of-fire plate is symbolic: DREAM label required in assembly; no literal infant or injury shown.

- Resumed latest authoritative checkpoint `9439af9` (clip 09 already complete); no duplicate regeneration. Next pending clip: 11.


## Previous handoff — clips 10–11 (2026-10-04)
- Starting checkpoint: `9439af9`, 45 accepted plates. Added **9 new accepted plates**: clip 10 all five, clip 11 shots 01/03/04/05.
- Clip 10 shot 04 used one corrective generation to remove unwanted circular ground guides; corrected image viewed before acceptance.
- Generation quota reached: 10 successful generation calls = nine new plates plus one correction. Clip 11 shot 02 was not generated; exact next prompt and references saved in `production/part1/next_background.json`.
- Total: **54/125** accepted; **71 remaining**. Clips 01–10 complete; clip 11 **4/5**. Script and VO unchanged.
- Next pending asset is the apple insert, not any of the saved clip 11 palace plates. No full-part MP4 rendered in this batch.
- Review: `production/part1/backgrounds_batch_05_contact.jpg` (clips 10–11; missing insert explicitly labelled pending). QC: `production/part1/backgrounds_batch_05_QC.md`.
- Validation passed: 54 accepted hashes/dimensions, script/VO unchanged, deterministic scene regeneration. Full-render readiness correctly rejects 71 missing plates. Contact sheets reject missing slots unless `--allow-pending` is explicitly requested.

## Current batch 06 — complete (2026-10-04)
- Resumed authoritative GitHub checkpoint `1ee30b1` (54 accepted); clips 09–10 and four clip 11 plates already saved, not regenerated.
- Completed missing clip 11 apple insert and all five clip 12 palace backgrounds. Individually viewed and accepted: **60/125**, 65 remaining; clips 01–12 complete.
- Clip 13 next. No script, VO or approved rig changes; assembly and full-part QC remain pending.

- Added four clip 13 oath-proposal backgrounds, individually viewed and accepted. **64/125 total, 61 remaining**; clips 01–12 complete, clip 13 shots 01–04 accepted.
- Ten generation calls this batch produced ten accepted new images, no re-rolls. Next exact asset is clip 13 shot 05 (Penelope bargain), saved in `production/part1/next_background.json`; then clips 14–25.

- Batch 06 review: `production/part1/backgrounds_batch_06_contact.jpg` (clips 11–13, pending slot explicitly labelled); QC: `production/part1/backgrounds_batch_06_QC.md`.
- Final checks passed: 64 accepted hashes/dimensions, script and all VO timings unchanged, deterministic plan generation. Full render correctly blocked by 61 pending backgrounds; no new full-part MP4 delivered.

## Session resume checkpoint — 2026-10-04
- Starting workspace was a clean checkout containing only the two supplied source files. GitHub had prior production work on `arena/01a1032c-yt-2`; its latest checkpoint (`774100f`) was fast-forward recovered onto this required session branch without regenerating accepted media.
- Recovered assets include the approved character/location sheets, rigs, Part 1 VO/music, animation preview, production tools, and 64 individually QC'd Part 1 backgrounds. Recorded approvals and the original locked script are retained.
- Resume point was `production/part1/backgrounds/p1_clip_13_bg_05.jpg`; it and the next nine plates were accepted in batch 07. Continue with the remaining unique Part 1 plates only; do not start another part before Part 1 is delivered.
- This restored sandbox has Python dependencies installed in the ignored `.venv`. `ffmpeg`/`ffprobe` are not installed; install them before video assembly.


## Background batch 07 — complete (2026-10-04)
- Generated and individually viewed **10/10** new HYBRID backgrounds with no re-rolls: clip 13 shot 05; all five shots for clip 14; clip 15 shots 01–04.
- **74/125 accepted, 51 remaining.** Clips 01–14 are complete; clip 15 is 4/5. No previously accepted art was regenerated.
- All ten files are 1376×768 (16:9); hashes and prompts are saved in `production/part1/background_manifest.json` and `production/scenes.json`. No visible people, writing, logos, modern props, or watermarks; all match the approved Sparta palace reference and retain clear staging ground.
- Review contact sheet: `production/part1/backgrounds_batch_07_contact.jpg`; per-image checklist: `production/part1/backgrounds_batch_07_QC.md`. Machine validation: `production/part1/background_validation.json` (74 accepted / 51 pending; full render correctly blocked).
- Exact next image: `production/part1/backgrounds/p1_clip_15_bg_05.jpg`, recorded in `production/part1/next_background.json`. Full Part 1 assembly remains blocked until all 125 unique plates are accepted; `ffmpeg`/`ffprobe` also need installing before render.


## Background batch 08 — complete (2026-10-04)
- Generated and individually viewed **10/10** new HYBRID backgrounds with no re-rolls: clip 15 shot 05; all five shots for clip 16; clip 17 shots 01–04.
- **84/125 accepted, 41 remaining.** Clips 01–16 are complete; clip 17 is 4/5.
- All backgrounds match the approved Sparta palace reference, preserve the empty lower staging area, and show no people, readable text, logos, modern objects or watermarks. Nine are 1376×768; `p1_clip_15_bg_05.jpg` is 1365×768, still within the approved 16:9 tolerance. Exact dimensions and hashes are recorded in the manifest.
- Contact sheet: `production/part1/backgrounds_batch_08_contact.jpg`; per-image QC: `production/part1/backgrounds_batch_08_QC.md`. Validation: 125 unique planned paths, 84 accepted, 41 pending, script and VO unchanged.
- Next exact asset: `production/part1/backgrounds/p1_clip_17_bg_05.jpg`, saved in `production/part1/next_background.json`. Full Part 1 render remains blocked until the remaining 41 backgrounds are accepted.


## Background batch 09 — complete (2026-10-04)
- Generated and individually reviewed **10/10** new backgrounds with no re-rolls: clip 17 shot 05; all five shots for clip 18; clip 19 shots 01–04.
- **94/125 accepted, 31 remaining.** Clips 01–18 are complete; clip 19 is 4/5.
- Used the approved Sparta palace reference for clip 17 shot 05 and the Aulis harbor reference for all new-location plates. The establishing image introduces Aulis; no generated people, text, infant, or injury appear. Palette, Bronze Age ships, shoreline, and open character-staging ground pass visual review.
- All ten images are 1376×768 and within the project’s accepted 16:9 tolerance. Prompts, SHA-256 hashes, references, and QC notes are recorded in `production/scenes.json` and `production/part1/background_manifest.json`.
- Contact sheet: `production/part1/backgrounds_batch_09_contact.jpg`; per-image checklist: `production/part1/backgrounds_batch_09_QC.md`. Validation confirms 125 unique planned paths, 94 accepted, 31 pending, script verbatim, and VO unchanged.
- Exact next image: `production/part1/backgrounds/p1_clip_19_bg_05.jpg`, recorded in `production/part1/next_background.json`. Full Part 1 render remains blocked while 31 backgrounds are pending.


## Background batch 10 — complete (2026-10-04)
- Generated and individually reviewed **10/10** new backgrounds: clip 19 shot 05; all five shots for clip 20; clip 21 shots 01–04. No rerolls.
- **104/125 accepted, 21 remaining.** Clips 01–20 are complete; clip 21 is 4/5.
- Continued the approved Aulis harbor look throughout, using its location reference. All ten images are 1376×768; no generated people, animals, infant, injury, text, logos, watermarks, or modern props. Clear character staging areas and Bronze Age coast continuity pass visual review.
- Prompts, references, dimensions, SHA-256 hashes, and QC notes are saved in `production/scenes.json` and `production/part1/background_manifest.json`.
- Labelled contact sheet: `production/part1/backgrounds_batch_10_contact.jpg`; per-image review: `production/part1/backgrounds_batch_10_QC.md`. Validation confirms 125 unique paths, 104 accepted, 21 pending, locked script verbatim, and VO unchanged. Full Part 1 render remains blocked while 21 backgrounds are pending.
- Exact next image: `production/part1/backgrounds/p1_clip_21_bg_05.jpg`, recorded in `production/part1/next_background.json`.


## Background batch 11 — complete (2026-10-04)
- Generated and individually reviewed **10/10** new backgrounds: clip 21 shot 05; all five shots for clip 22; clip 23 shots 01–04. No rerolls.
- **114/125 accepted, 11 remaining.** Clips 01–22 are complete; clip 23 is 4/5.
- Retained the approved Aulis harbor reference per the current scene plan. All ten images are 1376×768; no generated people, crews, animals, text, logos, watermarks, or modern props. The clip 23 plates emphasize the windless fleet; open character staging and coast continuity pass visual review.
- Prompts, references, dimensions, SHA-256 hashes, and QC notes are saved in `production/scenes.json` and `production/part1/background_manifest.json`.
- Labelled contact sheet: `production/part1/backgrounds_batch_11_contact.jpg`; per-image review: `production/part1/backgrounds_batch_11_QC.md`. Validation confirms 125 unique paths, 114 accepted, 11 pending, locked script verbatim, and VO unchanged. Full Part 1 render remains blocked while 11 backgrounds are pending.
- Exact next image: `production/part1/backgrounds/p1_clip_23_bg_05.jpg`, recorded in `production/part1/next_background.json`.


## Background batch 12 — in progress (2026-10-04)
- Reached the 10-call generation cap. Of the ten new outputs, **9 passed review**: clip 23 shot 05; clip 24 shots 01–03 and 05; clip 25 shots 01–04.
- Clip 24 shot 04 was rejected: the chest in the generated image carried pseudo-lettering/numeral-like marks, violating the no-text lock. It is excluded from the manifest and will be rerolled next batch. Clip 25 shot 05 has not yet been generated.
- **123/125 accepted, 2 remain.** Clips 01–23 complete; clips 24 and 25 are each 4/5. No script or VO changes.
- The nine accepted plates are 1376×768, use the approved Aulis reference, and contain no visible people, animals, injury, or text. Accepted prompts, hashes and QC are saved in the manifest and scenes plan.
- Partial labelled contact sheet and QC: `production/part1/backgrounds_batch_12_contact.jpg` and `production/part1/backgrounds_batch_12_QC.md`. Validation reports 123 accepted / 2 pending; full render remains blocked.
- Exact next task: reroll `production/part1/backgrounds/p1_clip_24_bg_04.jpg`; after it passes review, generate `p1_clip_25_bg_05.jpg`.


## Background batch 13 — complete (2026-10-04)
- Accepted the final two Part 1 plates after individual visual review: clip 24 shot 04 (successful reroll after a rejected pseudo-text output) and clip 25 shot 05.
- **125/125 accepted; 0 pending.** All 25 Part 1 clips now have five unique backgrounds each.
- Both images are 1376×768 and match the approved Aulis reference; neither contains people, animals, injury, text, logos, watermarks, or modern props.
- Prompts, references, hashes, dimensions, and QC notes are recorded in the scene plan and background manifest. Batch contact sheet: `production/part1/backgrounds_batch_13_contact.jpg`; review: `production/part1/backgrounds_batch_13_QC.md`.
- Validation confirms 125 unique plates, 125 accepted, 0 pending, locked script verbatim, VO unchanged, and `full_render_ready: true`. Next: install `ffmpeg` and `ffprobe`, then assemble and QC Part 1.
