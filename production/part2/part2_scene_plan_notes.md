# Part 2 Motion Plan — The Wrath of Achilles

**Source of truth:** measured clip timing and verbatim segment text in `part2_vo_manifest.json`; the approved Chapter 7 VO-only override is documented separately and does not modify `production/script_approved.txt`.

## Planned coverage

- 24 VO-matched clips; 123 unique background slots in `production/scenes.json` and `background_manifest.json`.
- Twenty-three standard clips use five distinct plates each. `p2_clip_16` is 23.678 seconds / 50 words, so it receives eight plates (about 2.96 seconds per shot) to stay within the lively-explainer turnover target. No VO timing or text is altered.
- Shot entries include measured start/end times, setting and approved location-sheet reference, camera movement, empty-ground composition, protected props, speaker events, dialogue-bubble excerpts, overlay treatment, mascot direction, and image prompts that prohibit people/text in generated HYBRID backgrounds.
- Troy, the Greek camp, and Olympus reuse approved references. Lemnos is a one-clip island variation using the approved Greek-camp palette/reference; it does not trigger a new recurring-location sheet.
- Existing approved rigs remain the only rigs. New one-off/static art is needed for Protesilaus, Philoctetes, Chryses and Patroclus; Andromache's approved sheet/cutout should include infant Astyanax in her arms (no separate infant asset or voice).

## Approval / production gate

The user approved all five new static character-sheet designs with “continue” on 2026-10-05; the approval record and labelled 14-character review grid are under `production/part2/character_sheets/`. Step 3 is cleared. Five border-matted transparent cutouts and dialogue face anchors are QC-passed; their sources, hashes and calibration preview are recorded in the character-sheet manifest. Background batches 01–05 are complete: 50/123 plates accepted, 73 pending; batch 05 includes one accepted corrective reroll. Batch 01 covers clips 01–02; batch 02 covers clips 03–04; batch 03 covers clips 05–06; batch 04 covers clips 07–08; batch 05 covers clips 09–10. Their review contact sheets and checklists are `production/part2/backgrounds_batch_01_contact.jpg` / `backgrounds_batch_01_QC.md`, `production/part2/backgrounds_batch_02_contact.jpg` / `backgrounds_batch_02_QC.md`, `production/part2/backgrounds_batch_03_contact.jpg` / `backgrounds_batch_03_QC.md`, `production/part2/backgrounds_batch_04_contact.jpg` / `backgrounds_batch_04_QC.md`, and `production/part2/backgrounds_batch_05_contact.jpg` / `backgrounds_batch_05_QC.md`. The initial `p2_clip_10` shot 03 candidate was rejected and excluded; a corrected, grate-free prompt was used for the accepted reroll and is recorded in both `background_manifest.json` and `scenes.json`. Each generated plate still requires individual visual review before it is recorded as accepted.
