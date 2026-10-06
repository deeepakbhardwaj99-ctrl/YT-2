# Part 3 Scene Plan — The Fall of Heroes & The Wooden Horse

**Source of truth:** `production/part3/part3_vo_manifest.json` (24 measured clips; verbatim VO text/timing) and the approved script. The two Chapter 9 substitutions are audio-only and recorded in `chapter9_vo_override.json`; the locked script remains unchanged.

## Plan summary

- 24 VO-timed clips; **121 unique background plates** in `production/scenes.json` and `background_manifest.json`.
- Plate count is chosen to target roughly three seconds per image, clamped to 2–8 shots per clip. All planned shot holds are 2–4 seconds. The first generation batch covers clips 01–02 (4 + 6 = 10 plates), exactly matching the required 10-image cadence.
- Approved location references only: `loc_camp` for Greek camp/beach scenes, `loc_troy` for the Trojan plain/gates/outskirts, and `loc_palace` for interiors. No new location sheet is introduced.
- Prompts require painterly-realistic HYBRID style, 16:9 framing, open lower-third staging, and environment-only plates with no people/faces/bodies, writing, marks, logos, watermarks, modern objects, or guides. The empty wooden horse is allowed only as an inanimate timber prop when called for by the scene.
- Part 1 and Part 2 scene-plan sections are preserved. The plan is validated by `tools/validate_part3.py`; backgrounds remain pending until generated and individually reviewed.

## VO coverage by clip

| Clip | Story beat | Reference setting | VO (s) | Plates |
|---|---|---|---:|---:|
| 01 | Priam's night approach to the Greek camp | Greek camp | 13.493 | 4 |
| 02 | Priam pleads with Achilles in the tent | Greek camp | 16.855 | 6 |
| 03 | Achilles and Priam share grief and a meal | Greek camp | 14.594 | 5 |
| 04 | Hector's funeral truce; the Iliad's ending | Greek camp | 16.223 | 5 |
| 05 | Lost poems introduce Troy's last allies | Trojan plain | 7.473 | 2 |
| 06 | Penthesilea and Memnon arrive | Trojan plain | 15.314 | 5 |
| 07 | Paris's arrow kills Achilles | Troy's gate | 14.399 | 5 |
| 08 | The heel detail is a later poetic addition | Palace writing room | 11.036 | 4 |
| 09 | Ajax claims Achilles's armor | Greek camp | 17.415 | 6 |
| 10 | Odysseus contests Ajax's claim | Greek camp | 5.311 | 2 |
| 11 | Ajax's grief after the judgment | Greek camp | 19.404 | 6 |
| 12 | Helenus names the three things needed to take Troy | Greek camp | 16.365 | 5 |
| 13 | Philoctetes returns and Paris is struck | Trojan plain | 17.285 | 6 |
| 14 | Oenone refuses Paris, then regrets it | Mount Ida grove | 12.799 | 4 |
| 15 | Odysseus and Diomedes steal Athena's statue | Trojan temple | 10.327 | 3 |
| 16 | Odysseus proposes the wooden horse | Greek camp | 16.996 | 6 |
| 17 | Epeius begins building it | Greek camp | 14.359 | 5 |
| 18 | The uncertain number of men inside | Greek camp | 14.405 | 5 |
| 19 | The Trojans discover and debate the horse | Troy's gate | 20.632 | 7 |
| 20 | Laocoön's warning and the hollow horse | Troy's gate | 20.576 | 7 |
| 21 | Sinon persuades the Trojans | Troy's gate | 11.863 | 4 |
| 22 | Cassandra is ignored | Trojan palace courtyard | 18.033 | 6 |
| 23 | Helen calls to the men inside the horse | Troy's gate at night | 19.150 | 6 |
| 24 | The Greeks stay silent; Troy brings in the horse | Troy's gate at night | 20.239 | 7 |

## Existing character visual proxies

No character art is regenerated or added in this scene-planning pass. Existing approved assets are reused. Exact existing cutouts/rigs are used for Priam, Achilles, Odysseus, Helen, Philoctetes and Paris. One-off Chapter 9–10 dialogue roles use documented approved archetype proxies (e.g. Trojan elders use Priam; Trojan women use Helen; Greek male one-offs use Agamemnon; generic Trojans use Hector/Priam). Dialogue bubbles and subtitles retain each exact speaker name. The mapping is recorded in `production/scenes.json` under `part3_speaker_visual_mapping` and in `tools/generate_part3_scene_plan.py`.
