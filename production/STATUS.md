# Production Status — THE TROJAN WAR: THE FULL STORY (Hybrid v3)

**Repo:** `deeepakbhardwaj99-ctrl/YT-2` · **Branch:** `arena/01a1032c-yt-2`
**Format:** 16:9 (1920×1080) · **Target Pace:** ~130 wpm · **Parts:** 4 parts (~4.7–7.2 min each, ~24.9 min total)
**Style Mode:** `HYBRID` (2D cartoon rigged characters + AI-generated painterly-realistic Bronze Age environments, no people/text in backgrounds)
**Motion:** `FULL ANIMATION` · **Preset:** `A — LIVELY EXPLAINER` (speech bubbles, callout cards, word pops, hops/pose swaps, 2s max static gate)
**Accent Color:** Burnt Orange `#9B3A12` · **Display Font:** Cinzel Decorative / Caesar Dressing (open-licensed, to be committed in Step 6B)

---

## Step 2 — Proposed Part Structure Table (Computed at 130 wpm)

| Part | Chapters / Sections | Spoken Words | Est. Runtime (@130 wpm) | Est. 15s Clips | Closing Line (Cliffhanger + Tease) |
|---|---|---:|---:|---:|---|
| **Part 1: The Apple & The Fleet** | `[COLD OPEN]`, `[CH 1: THE UNINVITED GUEST]`, `[CH 2: THE OATH]`, `[CH 3: THE FLEET AT AULIS]` | 938 | ~7.22 min | 29 | *"Next in Part Two: the Greeks hit the beach, only to watch their greatest warrior turn against his own army."* |
| **Part 2: The Wrath of Achilles** | `[CH 4: NINE YEARS OF NOTHING]`, `[CH 5: THE ARGUMENT]`, `[CH 6: A DUEL AND A GOODBYE]`, `[CH 7: ARMOR]` | 849 | ~6.53 min | 27 | *"Next in Part Three: a midnight ransom, the death of Achilles, and a giant wooden horse left on the sand."* |
| **Part 3: The Fall of Heroes & The Wooden Horse** | `[CH 8: THE KING IN THE TENT]`, `[CH 9: THE DEATH OF ACHILLES]`, `[CH 10: THE HORSE]` | 840 | ~6.46 min | 26 | *"Next in Part Four: the night Troy burned, the curse that hunted the victors home, and what archaeologists actually found buried under the hill."* |
| **Part 4: Ashes, Homecoming & History** | `[CH 11: THE NIGHT TROY BURNED]`, `[CH 12: THE ROAD HOME]`, `[CH 13: SO WHAT ACTUALLY HAPPENED?]` | 613 | ~4.72 min | 19 | *"In the Greek version, it all began with a guest list. A party, and one goddess nobody thought to invite."* |
| **TOTAL (Proposed Script)** | **14 sections** | **3,240** | **~24.92 min** | **101** | *(Original unedited script: 3,045 spoken words / ~23.42 min)* |

---

## Step 6B.6 — Cost & Turn Budget Estimate

- **Character Sheets & Location Sheets (Step 3 🔒):** 5 rigged character sheets + secondary static cut-out pack + 5 Hybrid location sheets (1 ref + 2×2 grid each) ≈ 2–3 turns.
- **Rig Packs & Face Calibration (Step 6B.1 🔒):** 5 rigged characters (Mascot + Achilles, Odysseus, Agamemnon, Hector) × 4 assets (`_a`, `_b`, `_c`, `_faces`) = 20 rig images + calibration frames ≈ 2–3 turns (built once, reused across all 4 parts).
- **Voiceover (Step 5 🔒):** 1 audition turn (Narrator + Mascot + 3 character voice archetypes) + ~3–4 VO generation turns per part (10 clips/turn platform cap).
- **Scene Backgrounds (Step 7):** ~5 unique HYBRID background images per 15s clip (or reused/angled from location sheets with continuous camera moves), delivered part-by-part across ~25–35 working turns total.
- **Encoding & Motion QC:** Python (PIL) frame generator piped directly into `ffmpeg` (~3–3.5× faster than realtime), verified with per-part `motion_report.txt` (0 stretches > 2s static).

---

## Pipeline Gate Checklist

- [x] **STEP 0 — Workspace Audit:** Completed. `production/` did not exist previously; initialized fresh from `MASTER_PROMPT_v3 Hybrid Trojan War.md` and `trojan_war_script_20min_with_dialogue.txt`.
- [ ] **STEP 1 — Script & Retention Pass 🔒 (WAITING FOR USER APPROVAL):**
  - Original script analyzed: 14 sections (`[COLD OPEN]` + `[CHAPTER 1]`–`[CHAPTER 13]`), 3,045 spoken words (~23.42 min at 130 wpm).
  - Proposed 10 targeted retention edits in `production/retention_proposals.md` and full proposed script in `production/script_proposed.txt` (3,240 spoken words, ~24.92 min at 130 wpm).
- [ ] **STEP 2 — Part Structure Table:** Drafted above; will lock upon Step 1 approval.
- [ ] **STEP 3 — Character & Location Sheets 🔒**
- [ ] **STEP 5 — Voiceover Auditions 🔒**
- [ ] **STEP 6 — Procedural Music Bed & Stems**
- [ ] **STEP 6B — Rig Packs + Face Calibration Frames 🔒 & First 20s Animated Scene 🔒**
- [ ] **STEP 7 & 8 — Part-by-Part Production & QC (Parts 1 → 4 + Master MP4)**
