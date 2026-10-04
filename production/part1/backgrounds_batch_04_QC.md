# Part 1 — Background batch 04 QC

**Date:** 2026-10-04 · **Scope:** clips 07–08 · **New plates:** 10/10 accepted · **Total:** 40/125.

## Checkpoint recovery
GitHub's latest saved commit was `2641a66`, with all 30 backgrounds for clips 01–06 already accepted. Those files were restored and reused, not generated again. This batch contains only the ten new images for clips 07–08.

## Image checks
- [x] Every new source image opened individually before acceptance.
- [x] No visible people, generated lettering, watermarks or modern electrical decorations.
- [x] Olympus plates use the approved Olympus reference; apple shots additionally use the accepted clip 06 apple plate.
- [x] Three Mount Ida/Troas countryside plates use the approved Troy reference for regional light, palette and stone materials, rather than importing Olympus architecture into the earthly setting.
- [x] Five different compositions per clip, not duplicate crops counted as extra images. No re-rolls this batch.
- [x] SHA-256, dimensions, reference provenance and composition notes recorded in `background_manifest.json`.
- [x] Batch contact sheet generated and viewed after the individual source checks.

## Story and assembly notes
- Clip 07: Aphrodite's claim, golden-apple insert, then the council and Zeus's reluctance.
- Clip 08: Zeus's refusal, the route toward the mortal world, Mount Ida establishing landscape, shepherd's hut, then a symbolic distant Troy connection.
- Mount Ida is an artistic pastoral extension of the approved Troy regional palette. No claim is made about exact historical architecture, vegetation or a real sightline from Mount Ida to Troy.
- The apple insert in clip 07 shot 02 is **not** a full-body character stage. Keep the apple free of captions and camera cropping; use voiceover/bubble treatment appropriate to an insert.
- Clip 08 shot 03 is a new-setting establishing view; subsequent pasture shots should show Paris, not the Zeus stand-in. Per-shot staging intent is retained in `scenes.json`, but renderer support remains pending.
- Characters, shadows, dialogue bubbles, inscriptions and motion have not been composited or QC'd in this background batch.

## Automated checks
- [x] Locked script byte-for-byte unchanged; all 25 VO segment lists and measured timings unchanged.
- [x] 125 unique planned paths; 40 accepted image hashes and dimensions validated; 85 paths still pending.
- [x] Scene generation deterministic; reference paths, protected-object regions and composition metadata survive regeneration.
- [x] Full-render readiness intentionally fails while 85 production backgrounds are missing.
- [ ] Full-part visual, audio, subtitle timing and motion QC — not run in this batch.

**Next:** clips 09–10, Paris's backstory and the three offers. No full Part 1 MP4 delivered in this batch.
