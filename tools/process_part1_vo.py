import json
import os
import subprocess
import shutil
import numpy as np
from scipy.io import wavfile

SR = 24000
TARGET_WPM = 130.0

def mp3_to_wav_array(mp3_path, atempo=0.85):
    tmp_wav = mp3_path + ".tmp.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_path,
        "-filter:a", f"atempo={atempo}",
        "-ac", "1", "-ar", str(SR), "-f", "wav", tmp_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sr, data = wavfile.read(tmp_wav)
    os.remove(tmp_wav)
    if data.dtype == np.int16:
        flt = data.astype(np.float32) / 32768.0
    else:
        flt = data.astype(np.float32)
    return flt

def split_audio_by_segments(audio, texts):
    n = len(texts)
    if n == 1:
        nz = np.where(np.abs(audio) > 0.008)[0]
        if len(nz) > 0:
            s0 = max(0, int(nz[0]) - int(0.05 * SR))
            s1 = min(len(audio), int(nz[-1]) + int(0.08 * SR))
            return [audio[s0:s1]]
        return [audio]

    hop = int(0.01 * SR)
    win = int(0.02 * SR)
    num_frames = max(1, (len(audio) - win) // hop)
    rms = np.zeros(num_frames, dtype=np.float32)
    for i in range(num_frames):
        seg = audio[i * hop : i * hop + win]
        rms[i] = np.sqrt(np.mean(seg * seg) + 1e-12)

    kernel = np.ones(5, dtype=np.float32) / 5.0
    rms_smooth = np.convolve(rms, kernel, mode="same")

    thresh = max(np.percentile(rms_smooth, 25), 0.008)
    is_silent = rms_smooth < thresh

    pauses = []
    in_pause = False
    start_f = 0
    for i, s in enumerate(is_silent):
        if s and not in_pause:
            in_pause = True
            start_f = i
        elif not s and in_pause:
            in_pause = False
            dur_f = i - start_f
            if start_f > 20 and i < num_frames - 20 and dur_f >= 10:
                mid_f = (start_f + i) // 2
                min_rms = float(np.min(rms_smooth[start_f:i]))
                pauses.append((mid_f * hop, dur_f * 0.01, min_rms))

    weights = [max(len(t.split()), 2) + 1.5 for t in texts]
    total_w = sum(weights)
    cum_fracs = []
    acc = 0
    for w in weights[:-1]:
        acc += w
        cum_fracs.append(acc / total_w)

    total_samples = len(audio)
    split_points = [0]
    used_pauses = set()

    for frac in cum_fracs:
        target_sample = int(frac * total_samples)
        prev_split = split_points[-1]
        window = int(0.16 * total_samples)
        best_p = None
        best_score = 1e18
        for idx, (p_sample, p_dur, p_rms) in enumerate(pauses):
            if idx in used_pauses:
                continue
            if p_sample <= prev_split + int(0.3 * SR):
                continue
            dist = abs(p_sample - target_sample)
            if dist <= window:
                score = (dist / SR) - (p_dur * 1.8)
                if score < best_score:
                    best_score = score
                    best_p = (idx, p_sample)
        if best_p is not None:
            used_pauses.add(best_p[0])
            split_points.append(best_p[1])
        else:
            lo_f = max((prev_split // hop) + 25, int((target_sample - 0.08 * total_samples) // hop))
            hi_f = min(num_frames - 25, int((target_sample + 0.08 * total_samples) // hop))
            if hi_f > lo_f:
                best_f = lo_f + int(np.argmin(rms_smooth[lo_f:hi_f]))
                split_points.append(best_f * hop)
            else:
                split_points.append(target_sample)

    split_points.append(total_samples)
    segments = []
    for i in range(n):
        seg = audio[split_points[i]:split_points[i+1]]
        nz = np.where(np.abs(seg) > 0.008)[0]
        if len(nz) > 0:
            s0 = max(0, int(nz[0]) - int(0.05 * SR))
            s1 = min(len(seg), int(nz[-1]) + int(0.08 * SR))
            seg = seg[s0:s1]
        segments.append(seg)
    return segments

def conform_segment_pace(seg, word_count, target_wpm=132.0):
    """Ensure segment duration is within +-12% of word_count / target_wpm using pitch-preserving atempo."""
    cur_dur = len(seg) / SR
    target_speech_dur = max(0.8, (word_count / target_wpm) * 60.0 - 0.32)
    ratio = cur_dur / target_speech_dur
    if 0.88 <= ratio <= 1.12:
        return seg
    # Apply gentle pitch-preserving atempo clamped to [0.75, 1.25]
    atempo = max(0.75, min(1.25, ratio))
    in_wav = "/tmp/seg_in.wav"
    out_wav = "/tmp/seg_out.wav"
    wavfile.write(in_wav, SR, (np.clip(seg, -1.0, 1.0) * 32767).astype(np.int16))
    subprocess.run([
        "ffmpeg", "-y", "-i", in_wav,
        "-filter:a", f"atempo={atempo:.4f}",
        "-ac", "1", "-ar", str(SR), "-f", "wav", out_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _, data = wavfile.read(out_wav)
    return data.astype(np.float32) / 32768.0

with open("production/parts_breakdown.json") as f:
    parts = json.load(f)

p1_lines = parts["1"]["lines"]

groups = {
    "production/part1/vo_raw/p1_narr_c0.mp3": [i for i, l in enumerate(p1_lines) if l["speaker"] == "NARRATOR" and l["chapter"] == "[COLD OPEN]"],
    "production/part1/vo_raw/p1_narr_c1.mp3": [i for i, l in enumerate(p1_lines) if l["speaker"] == "NARRATOR" and l["chapter"] == "[CHAPTER 1: THE UNINVITED GUEST]"],
    "production/part1/vo_raw/p1_narr_c2.mp3": [i for i, l in enumerate(p1_lines) if l["speaker"] == "NARRATOR" and l["chapter"] == "[CHAPTER 2: THE OATH]"],
    "production/part1/vo_raw/p1_narr_c3.mp3": [i for i, l in enumerate(p1_lines) if l["speaker"] == "NARRATOR" and l["chapter"] == "[CHAPTER 3: THE FLEET AT AULIS]"],
    "production/part1/vo_raw/p1_v01_1.mp3": [i for i, l in enumerate(p1_lines) if l["voice_id"] == "voice-01"][:1],
    "production/part1/vo_raw/p1_v01_2.mp3": [i for i, l in enumerate(p1_lines) if l["voice_id"] == "voice-01"][1:],
    "production/part1/vo_raw/p1_v02_all.mp3": [i for i, l in enumerate(p1_lines) if l["voice_id"] == "voice-02"],
    "production/part1/vo_raw/p1_v03_a.mp3": [i for i, l in enumerate(p1_lines) if l["voice_id"] == "voice-03"][:4],
    "production/part1/vo_raw/p1_v03_b.mp3": [i for i, l in enumerate(p1_lines) if l["voice_id"] == "voice-03"][4:],
    "production/part1/vo_raw/p1_v04_all.mp3": [i for i, l in enumerate(p1_lines) if l["voice_id"] == "voice-04"],
}

line_audios = {}
for mp3_path, idxs in groups.items():
    atempo = 0.85 if "v04" not in mp3_path else 0.92
    audio = mp3_to_wav_array(mp3_path, atempo=atempo)
    texts = [p1_lines[i]["clean_speech"] for i in idxs]
    segs = split_audio_by_segments(audio, texts)
    for idx, seg in zip(idxs, segs):
        seg = conform_segment_pace(seg, p1_lines[idx]["words"], target_wpm=132.0)
        line_audios[idx] = seg
        p1_lines[idx]["duration_s"] = round(len(seg) / SR, 3)

expanded_items = []
for idx, l in enumerate(p1_lines):
    seg = line_audios[idx]
    dur = len(seg) / SR
    txt = l["clean_speech"]
    if l["speaker"] == "NARRATOR" and l["words"] >= 45 and ". " in txt:
        sents = [s.strip() + ("." if not s.strip().endswith((".", "?")) else "") for s in txt.split(". ") if s.strip()]
        mid = len(sents) // 2
        t1 = " ".join(sents[:mid])
        t2 = " ".join(sents[mid:])
        sub_segs = split_audio_by_segments(seg, [t1, t2])
        for stxt, sseg in zip([t1, t2], sub_segs):
            w = len(stxt.split())
            sseg = conform_segment_pace(sseg, w, target_wpm=132.0)
            item = dict(l)
            item["clean_speech"] = stxt
            item["words"] = w
            item["duration_s"] = round(len(sseg) / SR, 3)
            item["audio"] = sseg
            expanded_items.append(item)
    else:
        item = dict(l)
        item["audio"] = seg
        expanded_items.append(item)

# Group into ~30-35 word (~14-16s) clips within each chapter
shutil.rmtree("production/part1/vo", ignore_errors=True)
os.makedirs("production/part1/vo", exist_ok=True)

clips = []
cur_lines = []
cur_words = 0
for item in expanded_items:
    w = item["words"]
    chap_changed = (cur_lines and cur_lines[-1]["chapter"] != item["chapter"])
    if cur_lines and (cur_words + w > 42 or chap_changed):
        if chap_changed and cur_words < 18 and len(clips) > 0 and clips[-1][0]["chapter"] == cur_lines[0]["chapter"]:
            clips[-1].extend(cur_lines)
        else:
            clips.append(cur_lines)
        cur_lines = []
        cur_words = 0
    cur_lines.append(item)
    cur_words += w
if cur_lines:
    if cur_words < 18 and len(clips) > 0 and clips[-1][0]["chapter"] == cur_lines[0]["chapter"]:
        clips[-1].extend(cur_lines)
    else:
        clips.append(cur_lines)

manifest = {"part": 1, "total_clips": len(clips), "clips": []}
total_vo_sec = 0.0
total_words = 0

for c_idx, c_lines in enumerate(clips, 1):
    clip_id = f"p1_clip_{c_idx:02d}"
    clip_words = sum(l["words"] for l in c_lines)
    target_clip_dur = (clip_words / TARGET_WPM) * 60.0
    speech_dur = sum(len(l["audio"]) / SR for l in c_lines)
    num_gaps = len(c_lines) + 1
    gap_dur = max(0.20, min(0.55, (target_clip_dur - speech_dur) / num_gaps))

    pieces = []
    timeline = []
    t_cursor = round(gap_dur * 0.6, 3)
    pieces.append(np.zeros(int(t_cursor * SR), dtype=np.float32))
    for l in c_lines:
        seg = l["audio"]
        rms = np.sqrt(np.mean(seg * seg) + 1e-12)
        gain = min(3.0, 0.12 / rms)
        seg_norm = np.clip(seg * gain, -0.89, 0.89)
        dur = len(seg_norm) / SR
        timeline.append({
            "line_index": l["line_index"],
            "speaker": l["speaker"],
            "voice_id": l["voice_id"],
            "text": l["clean_speech"],
            "words": l["words"],
            "t_start": round(t_cursor, 3),
            "t_end": round(t_cursor + dur, 3),
            "duration_s": round(dur, 3)
        })
        pieces.append(seg_norm)
        t_cursor += dur
        pieces.append(np.zeros(int(gap_dur * SR), dtype=np.float32))
        t_cursor += gap_dur

    full_clip_audio = np.concatenate(pieces)
    clip_dur = round(len(full_clip_audio) / SR, 3)
    wpm = round((clip_words / clip_dur) * 60.0, 1) if clip_dur > 0 else 0.0
    wav_path = f"production/part1/vo/{clip_id}.wav"
    mp3_path = f"production/part1/vo/{clip_id}.mp3"
    wavfile.write(wav_path, SR, (full_clip_audio * 32767).astype(np.int16))
    subprocess.run([
        "ffmpeg", "-y", "-i", wav_path, "-c:a", "libmp3lame", "-b:a", "192k", mp3_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(wav_path)
    total_vo_sec += clip_dur
    total_words += clip_words
    manifest["clips"].append({
        "clip_id": clip_id,
        "chapter": c_lines[0]["chapter"],
        "file_path": mp3_path,
        "duration_s": clip_dur,
        "words": clip_words,
        "wpm": wpm,
        "segments": timeline
    })

manifest["total_duration_s"] = round(total_vo_sec, 2)
manifest["total_minutes"] = round(total_vo_sec / 60.0, 2)
manifest["total_words"] = total_words
manifest["average_wpm"] = round((total_words / total_vo_sec) * 60.0, 1)

with open("production/part1/part1_vo_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Assembled {len(clips)} Part 1 VO clips | Total: {manifest['total_duration_s']}s ({manifest['total_minutes']} min) | {total_words} words | Avg WPM: {manifest['average_wpm']}")
for c in manifest["clips"]:
    print(f"  {c['clip_id']} ({c['chapter']}): {c['duration_s']}s | {c['words']}w | {c['wpm']} wpm | {len(c['segments'])} segs")
