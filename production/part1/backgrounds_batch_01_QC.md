# Part 1 — Background batch 01 QC

**Date:** 2026-10-04 · **Scope:** clips 01–02, 10 distinct production backgrounds.

- [x] Each of the ten source images opened individually with `read_file` before acceptance.
- [x] No visible people, dialogue lettering, labels or watermarks in the generated plates.
- [x] Semi-realistic warm environments; approved Troy/Olympus location reference supplied for every generation.
- [x] New compositions, not crops or color grades counted as extra images. SHA-256 and dimensions recorded in `background_manifest.json`.
- [x] Usable foreground for compositing; final character grounding/overlay clearance still needs assembled-frame QC.
- [x] Script byte-for-byte unchanged; all 25 VO segment lists and measured timings unchanged.
- [x] Ten accepted paths connected to `scenes.json`; 115 ungenerated paths explicitly marked pending.
- [x] Replaced cyclic callout selection with 25 narration-specific cards in `clip_beats.json`.
- [x] Validator rejects a full render while any production background is pending.
- [ ] Full-part visual/audio/motion QC — not run; no new full-part MP4 delivered in this batch.

These are artistic environments. Olympus is mythic architecture; Troy is an imagined reconstruction, not verified archaeological site imagery. The original approved style-preview MP4 remains unchanged.

## Remaining assembly checks
- Complete clips 03–25: 115 background plates.
- Check exact card/subtitle timing against speech; proportional subtitle timing is not word-level alignment.
- Verify character identity substitutions, multi-speaker clips, speech-bubble tails, new-location establishing frames and title/tease cards in full-part assembly.
- Run full motion curve, spot-frame review and audio peak/ducking checks before delivery.

## Encoding correction
The earlier estimate of 45–60 MB at a 2.2 Mbps video cap was too low. For 406.63 s, 2.2 Mbps video plus 192 kbps audio is about **122 MB** before overhead at the rate cap. The renderer now uses a **1.4 Mbps video cap**, 192 kbps audio and medium H.264 preset: approximately **81 MB** before overhead at the cap. Actual size and picture quality must be measured after rendering; this is an estimate, not a QC result.
