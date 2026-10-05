# Part 2 Motion Plan — The Wrath of Achilles

**Source of truth:** measured clip timing and verbatim segment text in `part2_vo_manifest.json`; the approved Chapter 7 VO-only override is documented separately and does not modify `production/script_approved.txt`.

## Planned coverage

- 24 VO-matched clips; 123 unique background slots in `production/scenes.json` and `background_manifest.json`.
- Twenty-three standard clips use five distinct plates each. `p2_clip_16` is 23.678 seconds / 50 words, so it receives eight plates (about 2.96 seconds per shot) to stay within the lively-explainer turnover target. No VO timing or text is altered.
- Shot entries include measured start/end times, setting and approved location-sheet reference, camera movement, empty-ground composition, protected props, speaker events, dialogue-bubble excerpts, overlay treatment, mascot direction, and image prompts that prohibit people/text in generated HYBRID backgrounds.
- Troy, the Greek camp, and Olympus reuse approved references. Lemnos is a one-clip island variation using the approved Greek-camp palette/reference; it does not trigger a new recurring-location sheet.
- Existing approved rigs remain the only rigs. New one-off/static art is needed for Protesilaus, Philoctetes, Chryses and Patroclus; Andromache's approved sheet/cutout should include infant Astyanax in her arms (no separate infant asset or voice).

## Approval / production gate

The user approved all five new static character-sheet designs with “continue” on 2026-10-05; the approval record and labelled 14-character review grid are under `production/part2/character_sheets/`. Step 3 is cleared. Five border-matted transparent cutouts and dialogue face anchors are QC-passed; their sources, hashes and calibration preview are recorded in the character-sheet manifest. Background batch 01 (clips 01–02) is complete: 10/123 plates accepted, 113 pending. Review contact sheet and checklist are `production/part2/backgrounds_batch_01_contact.jpg` and `production/part2/backgrounds_batch_01_QC.md`. Each subsequent generated plate still requires individual visual review before it is recorded as accepted.
