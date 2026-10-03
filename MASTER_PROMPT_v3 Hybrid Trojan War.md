# MASTER PROMPT TEMPLATE v3 — Long-Form ANIMATED Cartoon Video Production Agent

> **v3 = v2 (motion & animation layer, unchanged) + the cartoon explainer style lock, a rigged mascot narrator, a per-scene overlay plan, dialogue/voice handling, and a tone preset switch (A lively / B calm).** All v2 tooling (`tools/rig.py`, `tools/assemble.py`) and gates stay as they are; v3 only adds style, text and dialogue rules on top.

> **v2 adds the MOTION & ANIMATION LAYER (Step 6B).** v1 produced narrated sequences of stills with
> camera moves; v2 produces *animated cartoons* — rigged characters that enter, hop, gesture, talk,
> and react, plus text that pops in on the VO. Everything in this file is implemented and proven in
> `samples/time-explainer/` (`tools/rig.py` = rig + motion toolkit, `tools/assemble.py` = assembler).

This is your reusable skeleton. Fill in the bracketed `[...]` sections with each new project's specifics, paste your finalized script at the end (or let the agent rewrite it per Step 1), and send the whole thing to Arena AI in a GitHub-connected session.

---

## HOW TO USE THIS TEMPLATE EACH TIME
1. Fill in the **Project Setup** block below (title, topic, tone, visual style, length, character list).
2. Paste your draft script at the very end, under **THE SCRIPT**.
3. Make sure you're in a GitHub-connected Arena session (see your earlier "Workspace setup" step) — update the repo name in the block below.
4. Fill in the **Motion Block** (Step 6B): motion level, which characters get rigs, and where text pops.
5. Attach this master prompt file AND your script file (separate .txt) together in your first message.

---

# PRODUCTION BRIEF — "[VIDEO TITLE]"
**Format:** [16:9 / 9:16 / etc.] · [total length, e.g. 20–30 minutes] total (flexible — target the script's natural length at [125–135] wpm) · produced in **[N] parts** of ~[X] min each
**Tone:** [e.g. soothing bedtime-story narration / high-energy hype / calm educational]
**Motion:** `[FULL ANIMATION / LIGHT MOTION / SLIDESHOW]` — this is an **animated** production, not a slideshow: every recurring character is rigged and moves with eased motion, text pops in on the VO, and the camera never fully stops.
**Motion energy:** `[e.g. warm and bouncy / tense and slow / crisp and snappy]`
**Style mode:** `[CARTOON / HYBRID]`
- **CARTOON:** characters AND backgrounds are 2D illustrated cartoon (see CARTOON STYLE LOCK, Step 4).
- **HYBRID:** characters are 2D cartoon rigs; **backgrounds are AI-generated realistic or semi-realistic environments** (landscapes, buildings, interiors, ruins, skies). See HYBRID STYLE LOCK, Step 4. In HYBRID mode, the "no photorealism" rule applies to **characters only**, never to environments.
**Preset:** `[A — LIVELY EXPLAINER / B — CALM STORY]`
- **A — Lively:** backgrounds change every ~2–4 s, bubbles/cards/word-pops as in Step 6B, hops and pose swaps on most sentence boundaries, tiny sound effects (pop, whoosh) used sparingly.
- **B — Calm:** backgrounds change every ~6–10 s, slow camera only, gentle fades (0.8–1.5 s), idle breathing only, rare titles and keywords, no speech bubbles, no sound effects. The 2-second frozen-stretch gate becomes 5 seconds.
**You are** the production agent. Work step by step. Check in with me at the approval gates marked 🔒. Keep a live `production/STATUS.md` (done vs remaining per asset) and update it after every batch. **Follow the efficiency rules in Step 10 at all times — they are not optional.**

**Workspace setup:** This session is connected to a GitHub repo (`[owner/repo-name]`). Commit code, scripts, `STATUS.md`, and scene/VO metadata (JSON/CSV, not binaries) to the repo as you go — this is your durable memory across the session, not the local workspace. Do not let generated media pile up unpushed and undeleted in the session workspace.

**Media handling — push everything to the repo immediately:** As soon as ANY file is generated and accepted — an image, a VO clip, a music stem, an assembled part MP4, metadata, scripts — commit and push it to the GitHub repo right away, in the same turn if possible. Don't batch pushes for later and don't leave finished assets sitting only in the local session workspace. The repo is the single source of truth: when you need to reuse or reference an earlier asset (a character sheet, a VO file, a prior part), fetch it from the repo rather than assuming it's still in the local workspace.

**One real constraint to watch:** GitHub rejects any single file over 100 MB pushed normally. Your assembled part MP4s may approach or exceed this. If a push fails for that reason: tell me immediately rather than silently dropping the file, and default to enabling Git LFS for that file type (`git lfs track "*.mp4"`) so future large files push cleanly — note this in `STATUS.md` once set up so you don't re-hit the same failure.

---

## STEP 0 — Workspace audit (do this first)
List `production/` recursively. Reuse any existing script, scene breakdown, character sheets, VO, or music tooling found there. Never regenerate character sheets if approved ones already exist. If empty, build everything from this brief and the script below.

## STEP 1 — Read the full script + retention pass 🔒
Read the complete script (end of this document). You MAY propose retention-boosting edits — and only these kinds:
1. Sharpen the first 30 seconds (stronger hook).
2. Add open loops / curiosity gaps, especially at the END of every part (each part ends on a cliffhanger + one-line tease of the next part).
3. Occasional pattern interrupts so attention never flattens.
4. Part-opening 5-second recap-hook lines.

Present every proposed change as a before → after list. **Do not generate any VO until I approve the final script.** After approval, the VO text is VERBATIM — never paraphrase at generation time.

**Important:** the final approved script is the ONLY source of truth for word count and timing — recompute everything in Step 2 from the actual approved text, not from any earlier draft.

## STEP 2 — Part structure (compute from the approved script — do not hardcode)
Voice pace: ~[125–135] wpm. Measure actual generated VO and re-cut clip boundaries to measured durations.

After Step 1 is approved:
1. Count the final approved script's total words.
2. Divide it into **[N] parts** of roughly equal length, snapping each part boundary to the nearest natural chapter/topic break.
3. Present the resulting part table to me (scenes per part, word count, estimated runtime, closing line of each part) before proceeding.
4. Total target: [X–Y min]. If over, trim pacing rather than cutting content. If under, extend closing holds on the final part rather than padding VO.

**Retention rule:** no part may end flat — cliffhanger + tease card burned in at the end of every part; each part opens with a 5s hook.

### Clip unit (the production atom)
- Every **[15]-second video clip** is covered by **[Preset A: 5–8 / Preset B: 2–3]** unique background images (slow zoom-pan each), [0.3–0.5]s crossfade between images. Rigged characters and overlays are layered on top and may persist across background changes or exit and re-enter.
- Each script scene becomes ⌈scene_VO_duration / [15]⌉ clips, split at natural sentence boundaries.
- If the platform's per-turn image budget forces lower density: minimum **[5]** images per clip, and tell me the density you're running.

## STEP 3 — Character/asset sheets FIRST (before ANY scene images) 🔒
Generate (or reuse from workspace) all identity sheets for recurring characters/subjects, present a contact grid, wait for my approval. Every scene image featuring a character MUST pass the relevant sheet(s) as reference image(s).

**Characters/recurring subjects:**
1. `[name — description, defining visual traits, any locked details like a specific prop material]`
2. `[name — ...]`
3. `[add as many as needed]`

Sheet composition: full body, neutral standing pose, front three-quarter view, **plain light neutral backdrop**, character-concept-sheet layout.

**Mascot narrator (v3):** one recurring mascot `[name — description, e.g. a cartoon skeleton in a Spartan-style helmet with red crest, gold chest armor and red cape; simple black dot eyes]`. The mascot is a **fully rigged character** (rig pack per Step 6B) with a talking mouth and a thick white sticker outline, used to introduce ideas, react, and deliver key points. Vary poses and screen side; never repeat the same pose twice in a row.

**Rig budget rule (v3):** rig the mascot plus at most **[3–4] main story characters**. Every other character is a single static cut-out image that slides or pops in and out. Never rig a character that appears in fewer than 3 scenes.

**Character face language:** simple round heads, small dot eyes, minimal mouths, expressive details such as tears or sweat drops.

**Location sheets (HYBRID mode, 🔒 approve with the character sheets):** for every recurring place (e.g. `[the walled city, the Greek camp, the palace hall, Mount Olympus, the harbor]`), generate 1 reference image plus a 2×2 contact grid of angles (wide establishing, medium, interior or detail, different time of day) so the place looks consistent every time it returns. Every later background of that place must pass its location sheet as reference. Backgrounds contain **no people** (at most tiny distant silhouettes) and **no text**.

## STEP 4 — Visual style lock (bake into EVERY image prompt)
`[Describe the visual style: art movement/medium, color palette, lighting style, line/brush quality, aspect ratio.]`

**Pacing/motion must match the tone:** `[e.g. "even in tense scenes, keep motion slow and held" OR "fast cuts and dynamic framing throughout" — state the intended energy explicitly.]`
This is an **animated** production: characters enter and exit with eased motion, hop between beats, breathe
while idle, and move their mouths on their own dialogue; text pops in; the camera never stops. Static
source art is the starting point, never the finished shot.

**Never:** `[list of style violations to avoid, e.g. generic photorealism, anime, glossy 3D, slideshow look, static poses.]`
**QC locks:** `[list any hard visual rules — content restrictions, prop consistency, no-gore, no-text, no-watermark, etc.]`

**CARTOON STYLE LOCK (v3 — bake into every image prompt):**
`[Illustrated 2D cartoon, NOT realistic. Clean confident outlines, flat-to-soft shading, warm storybook feel. Characters: simplified, dot eyes, minimal mouths. Backgrounds: richer cartoon environments with depth, always less detailed than a photograph. Palette: [e.g. gold, deep red, brown, black, cream, night-sky blue]. Aspect ratio: [16:9].]`
- **Never:** photorealism, photo textures, 3D renders, glossy/plastic look, anime, style drift between scenes.
- **No text, letters, numbers, logos or watermarks inside any generated image.** All words are added in the overlay layer (Step 6B) with a real font, because image generators misspell. Exception only if I approve in-image text, and then each image gets a spelling check.
- **Background prompt template (CARTOON):** `[scene description], 2D illustrated cartoon style, clean outlines, simple dot-eye characters, [palette], storybook backdrop, no text, no letters, no watermark, [16:9]`

**HYBRID STYLE LOCK (v3 — use instead of the cartoon background template when Style mode = HYBRID):**
- **Environments:** `[AI-generated realistic or painterly-realistic environment: cinematic landscape / ancient architecture / interior / ruins / sky, consistent era and materials, [palette-matched color grade], eye-level camera, a clear open ground area in the lower third for characters to stand, 16:9]`.
- **Background prompt template (HYBRID):** `[location and view], [time of day], [era/architecture details], cinematic wide shot, realistic textures, soft atmospheric depth, open flat ground in the foreground, no people, no text, no letters, no watermark, [16:9]`
- **Never in backgrounds:** people or faces, text/signs/inscriptions, logos, modern objects, watermarks, extreme fisheye distortion.
- **Characters stay 2D cartoon** (dot eyes, outlines, sticker outline on the mascot). Realistic human faces are never generated.
- **Style bridge (so cartoons do not look pasted on):** apply the same color grade to the background and a mild palette-matched tint to the characters; add a soft contact shadow under every character, matched to the scene's light direction; add subtle atmospheric haze or depth blur to the far background; apply a very light shared film grain over the final frame; keep character scale consistent with the scene's perspective (feet on the ground area, size matching the camera distance).
- **Establishing shots:** every time the story enters a new location, open with a slow wide establishing shot of that place (about 3–5 s, no characters or only a distant one) with a lower-third place name in the overlay font, then cut or push in to the characters. Re-establish briefly (1–2 s) when returning to a place after a long absence.
- **Palette note:** HYBRID palette = the grade applied to environments plus the accent color used for text and arrows; keep both consistent across the whole video.

## STEP 5 — Voiceover 🔒
`[Describe the voice: tone, pace, gender/style if relevant.]` Audition **two NEW voices** speaking a representative line from the script; I pick one.

**Dialogue handling (v3):** the script may contain `SPEAKER: "line"` dialogue and `MASCOT: "line"` interjections between narration. Text in (parentheses) is a delivery note and is NOT spoken; speaker tags are never read aloud. Audition the narrator plus **up to 3 extra character voices** (e.g. deep male, female, older/gruff) and a lighter distinct mascot voice; assign each speaker to the closest voice and keep it consistent across the whole video. Every line is spoken verbatim. Dialogue clips stay short and punchy with a brief pause before and after, and the talking-mouth animation (Step 6B) plays only on the speaker's own lines.

Then generate **one VO file per [15]-second clip** (exact timing + per-clip edits). Target ~[125–135] wpm. Measure every file; flag clips >20% off target; text must be verbatim from the approved script.

## STEP 6 — Music / sound design
`[Describe the intended music bed: genre, energy, instrumentation, what to avoid.]` Synthesize procedurally, adapting any reusable tooling from the workspace. Deliver: full-length bed + per-part stems. Ducking: music −18 to −24 dB under VO, up to −12 dB in VO gaps.

## STEP 6B — MOTION & ANIMATION LAYER 🔒

**This is a fully animated production, NOT a slideshow of stills.** Still images may be the *source art*,
but every scene must move: camera, characters, or on-screen text — ideally all three.

**Motion level:** `[FULL ANIMATION / LIGHT MOTION / SLIDESHOW]` · **Motion energy:** `[e.g. warm and bouncy / tense and slow / crisp and snappy]`

### 1. Rig every recurring character BEFORE the scene-image phase
For each named character, generate a **rig pack** (this is separate from the character sheet and costs
image budget, so plan for it):
1. `char_<name>_a` — full body, front view, neutral standing pose, on a **plain flat single-colour background**, nothing else in frame.
2. `char_<name>_b`, `_c` — the same character, same framing, with **only the limbs/expression changed** (arm raised / arm extended / walking). Ask for "change ONLY the arm, keep everything else pixel-identical."
3. `char_<name>_faces` — 3–4 head close-ups (neutral, happy, surprised, sad) for expression swaps.
4. `char_<name>_anchors` — the agent finds and records the mouth / eye coordinates, then **shows me a calibration frame** marking them before the rig is locked. 🔒

**Rig alignment is a hard QC gate:** pose variants must land on the same canvas at the same scale,
aligned at the feet/lower body, so the character never jumps or changes size when poses swap.
Report the alignment IoU per character (target ≥ 0.80).

### 2. Motion vocabulary — the agent must use all of these across a part
| Move | Where to use it |
|---|---|
| **Entrance** — character slides in from off-screen with ease-out, lands with a soft squash & stretch | first appearance in a scene |
| **Hop / travel** — arc move across frame with stretch on take-off, squash on landing | character moving between two topics |
| **Idle life** — slow breathing bob, occasional blink, tiny head/body sway | every second the character is on screen |
| **Talking mouth** — visible mouth movement while that character's VO line plays | all dialogue |
| **Pose swap** — arm gesture changes to match the beat (waving, presenting, pointing, thumbs-up) | on sentence boundaries |
| **Expression swap** — face swaps for reaction beats (surprised, sad, delighted) | on emotional turns |
| **Exit** — staged exit on cue (slide out, sink, walk off); never just vanish | scene end |
| **Camera** — slow push-in / pull-back / pan per scene, **never fully stopping** | continuous |
| **Transition family** — pick 2–3 per part (wipe, iris, slide, dip-to-cream) and use them consistently | between scenes |

### 3. On-screen text (the "pop-up" layer)
- **Dialogue → speech bubbles.** Every spoken line that is *dialogue* gets a bubble with an outlined
  tail anchored to the speaker's mouth; it pops in with a slight overshoot, holds for the line's length,
  then fades. Never more than one bubble on screen at a time.
- **Facts/definitions → callout cards.** A white rounded card with kicker + headline, a coral underline
  wipe, and 2–4 chips that slide in **staggered** (0.12–0.18 s apart). Cards slide in from off-screen and out again.
- **Key terms → chips/tags.** Pill-shaped labels for word lists (e.g. "new route", "weird hobby").
- **Emphasis → word-by-word headline.** Big headline words pop in one at a time on their own beats.
- **Lower-thirds** for names/dates/places when the subject changes.
- **Rule:** text pops in *with* the VO — the word appears within ±0.2 s of being spoken when it illustrates that exact word.
- **Rule:** never more than ~7 words on screen at once; every card readable for ≥ 1.5 s.

**Text style rules (v3):**
- One bold, slightly rough hand-carved or rune-style display font appropriate to the topic, from an open-licensed source (state the font and commit it to the repo). Use it for ALL overlay text.
- **Two-color rule:** the key word in an accent color `[e.g. burnt orange #9B3A12]`, supporting words in black or white, whichever contrasts. Thin outline or soft shadow behind text so it stays legible on any background.
- **Bubbles:** a speaking character's bubble shows a 2–5 word excerpt of the spoken line (the full line is still spoken in the VO).
- **Dimming rule:** when a callout, headline or mascot is the focus, darken the background and non-speaking characters to ~40–60% brightness for the duration, then restore.
- **Arrow rule:** a hand-drawn arrow in the accent color with a white outline, drawn on in ~0.3 s, points at the important object.
- **Placement rule:** callouts, bubbles and chips must NEVER cover a speaking character's face or the object being discussed; place them in empty background space.
- Subtitles: **[ON / OFF]** (default OFF for Preset A if bubbles and cards already carry the words; ON if I ask for accessibility captions). When ON: bottom safe area, max 2 lines, bubbles/cards are additional, not a replacement.

### 3B. Per-scene plan file (v3)
Save `production/scenes.json` and reference it in `STATUS.md`. For every background image record: `location` (from the location sheets, HYBRID mode), `shot_type` (establishing / wide / medium / detail), `image_prompt` (no text, no people in HYBRID), `camera` (dolly-in / pan / pull-back / hold), `characters` (who is on screen, entering / idle / exiting), `speaker` (character name or `narrator`), `bubble_text` (2–5 words or empty), `overlay_text` and `emphasis_word` (1–4 words, accent word), `text_style` (`keyword` / `bubble` / `card` / `label`), `text_position`, `mascot` (pose, side, or none), `arrow_target`, `dim_background` (true/false), `sfx` (Preset A only). Backgrounds change on the preset's schedule; characters may persist across changes.

### 4. Expression / lip-sync quality bar
Mouth movement must be drawn **over** the character's existing mouth (cover the drawn smile first,
clone-stamping the surrounding colour so there is no smudge or double-mouth), pulsing at ~4 Hz
while the character's own VO plays, and released to the resting expression during silence.

### 5. Technical rules
- Render frame-by-frame in Python (PIL) and pipe straight into ffmpeg — no intermediate PNG sequences.
- Everything on a shared timeline: `(event, t_start, t_end, easing)` tracks, all timing derived from measured VO.
- Supersample stills ≥ 2× before camera moves so zoom-pan never jitters.
- **Motion QC (hard gate, per part):** compute a frame-to-frame difference curve and report it.
  Any stretch longer than **2 seconds (Preset B: 5 seconds) with near-zero motion is a failure** — add life or a camera move and re-render.
- Audio: VO RMS-normalised, music ducked ~9–10 dB under speech, delivery ceiling −3 dBFS
  (AAC adds ~1.5 dB of inter-sample overshoot, so do not master to −1).

### 6. Cost & budget (state this in your plan before starting)
- Rig packs cost ~3–4 images per character **once**, and are reused across every part.
- Encoding runs ~3–3.5× faster than realtime (a 20 s scene ≈ 60–70 s of render).
- For a 25-minute film: ~230–280 scene images across ~25 image turnovers + 3–4 VO batches +
  1 rig batch per character — budget **25–35 working turns total**, delivered part by part.

### 7. Gates 🔒
- After the rig packs + face calibration frames: **I approve the rigs before any scene is animated.**
- After the first assembled *animated* scene (~20 s): **I approve the motion style before it is applied to the whole part.**

## STEP 7 — Assembly + ANIMATION (per part)
Build each scene on a single shared timeline of tracks: background camera (dolly-in / pan / pull-back /
pan-up, alternating, never stopping), character tracks (enter → idle → talk → gesture → exit), bubble and
card tracks (pop-in → hold → fade), and the text layer. Composite the rig layers in Python (PIL) and pipe
frames straight into ffmpeg — no intermediate PNG sequences. Crossfades between images, dip between scenes,
staggered entrance of card content (0.12–0.18 s), word-by-word headlines for emphasis beats. Part title card
at start; tease card at end. Burned-in subtitles (max 2 lines, bottom safe area, synced to VO) remain the
accessibility track — bubbles/cards are additional, not a replacement. **Run the motion QC curve and fix any
frozen stretch > 2 s before delivering.** Output: 1920×1080 H.264 MP4, AAC 192k, within each part's target window.

## STEP 8 — QC protocol (run on EVERY asset, report a checklist per part)
- **Images:** VIEW each generated image before accepting. Fail + re-roll (max 2 re-rolls, then flag to me) for any violation of Step 4's style lock or QC locks.
- **VO:** duration within ±20% of word-count/pace; consistent voice across clips; verbatim text (spot-check 3 random clips); no glitches at clip edges.
- **Part video:** extract spot-frames and VIEW them; verify VO/visual sync; transitions smooth; subs legible; music under VO; duration within target.
- **Motion:** report the frame-to-frame difference curve; zero frozen stretches > 2 s; every entrance/exit eased; characters never vanish mid-shot.
- **Rig:** pose alignment IoU ≥ 0.80 per character; pose swaps cause no jump in position or scale; face anchors verified on a calibration frame.
- **Text timing:** bubbles/cards readable ≥ 1.5 s, pop within ±0.2 s of the spoken word, never covering the speaker's face.
- **Style (v3):** no realistic or photo look; no text/letters in any generated image (re-roll if found); overlay spelling correct and in the committed font; accent color on the right word; mascot design consistent across all poses; palette consistent across the video.
- **Hybrid integration (HYBRID mode):** every character has a contact shadow and stands on the ground area (no floating); character scale matches the shot; light direction and color grade are consistent between character and background; no people or text appear in any generated background (re-roll if found); recurring locations match their location sheets; each new location opens with an establishing shot.
- **Dialogue (v3):** each speaker has one consistent voice; talking mouth plays only on that speaker's lines; delivery notes and speaker tags are not spoken.
- Deliverable per part: the part MP4 + a one-page QC checklist.

## STEP 9 — Budget protocol + part sequencing
The platform may cap generation per turn. If a batch hits the cap:
1. Never crash or retry spam — finish what fits, update `production/STATUS.md` with exact remaining counts.
2. Report: "Part N: X/Y clips VO done · A/B images done — say 'continue' to keep going."
3. On my "continue", resume exactly where STATUS.md says.

**Per-part work order (strict — complete each part fully before starting the next):**
(a) part script final (🔒 if edits) → (b) clip list → (c) ALL VO for the part → (c2) per-scene motion plan (who moves where, which bubbles/cards, which camera move) → (c3) build or reuse rig packs → (d) ALL images for the part → (e) part music stem → (f) assemble + animate + render part → (g) motion QC curve + QC checklist + deliver part MP4.
Rig packs are built **once per character** and reused across every part — never regenerate a rig mid-project.

Part 1 must be fully complete and delivered before Part 2 begins, and so on. After all parts: verify combined runtime is within target, concatenate into one final video with consistent audio levels across join points, deliver a final part-by-part report.

**Workspace cleanup (after every part, before starting the next):** Once a part's assets (images, VO, music stem, part MP4) have all been pushed to the GitHub repo and QC'd, delete the local copies from the session workspace — the repo now holds the authoritative copy, so nothing is lost. This keeps the session workspace light without losing anything, since everything reusable now lives in the repo.

## STEP 10 — Efficiency & communication rules (apply at all times)
- Do not re-print the full script, character sheet list, or this brief back to me in status updates — reference `STATUS.md` instead.
- Status updates should be short: what's done, what's next, what you need from me.
- Batch tool calls where possible instead of one-at-a-time narration.
- Only stop for the 🔒 gates explicitly marked in this brief.
- If something is ambiguous, make the most reasonable production decision yourself and note the assumption in one line, rather than asking and waiting — unless it affects the locked visual style, the verbatim VO text, or content in a way I'd need to approve.
- Render motion with a frame generator piped into ffmpeg; never write thousands of intermediate PNG frames to disk.
- Keep a `motion_report.txt` per part (frame-diff curve + any frozen-stretch list) and reference it instead of re-explaining motion in status updates.
- Reuse one rig pack per character across all parts; treat rig alignment (IoU) as a locked QC number, not a vibe.

---

## THE SCENE LIST
`[Optional: list scene/chapter names here for clip-splitting reference, like "S01 Cold open · S02 ... " — or tell the agent to derive scenes itself from the attached script.]`

---

## THE SCRIPT
The draft script is attached as a separate `.txt` file alongside this brief — read it from there. Treat its contents as the verbatim source of truth for Step 1's retention pass, exactly as if it were pasted inline here.

---
**Start now with STEP 0.** Show me the workspace audit result, then proceed to STEP 1 (retention proposals) using the attached script. 🔒 Wait for my approval before any VO.

**Motion gates (v2):** 🔒 rig packs + face calibration frames are approved before any scene is animated,
and the first assembled animated scene (~20 s) is approved before the motion style is applied to a whole part.
