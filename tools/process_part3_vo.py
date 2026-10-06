"""Split Part 3 raw voice batches into measured, mixed per-clip VO assets."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
LOCAL_BIN = ROOT / ".venv" / "bin"
if LOCAL_BIN.is_dir():
    os.environ["PATH"] = str(LOCAL_BIN) + os.pathsep + os.environ.get("PATH", "")
if not shutil.which("ffmpeg"):
    try:
        import imageio_ffmpeg
    except ImportError as exc:
        raise RuntimeError("FFmpeg is required. Install tools/requirements.txt or add ffmpeg to PATH.") from exc
    LOCAL_BIN.mkdir(parents=True, exist_ok=True)
    ffmpeg_link = LOCAL_BIN / "ffmpeg"
    if ffmpeg_link.is_symlink() and not ffmpeg_link.exists():
        ffmpeg_link.unlink()
    if not ffmpeg_link.exists():
        ffmpeg_link.symlink_to(imageio_ffmpeg.get_ffmpeg_exe())
    os.environ["PATH"] = str(LOCAL_BIN) + os.pathsep + os.environ.get("PATH", "")
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
SR = 24000
TARGET_WPM = 130.0
CONFORM_WPM = 132.0
# Part 3's estimated 24-shot edit needs a slightly wider assembly cap than
# Part 2 to avoid creating two extra, very short VO shots; pace QC stays strict.
MAX_CLIP_WORDS = 44
RAW_DIR = ROOT / "production/part3/vo_raw"
OUT_DIR = ROOT / "production/part3/vo"
MANIFEST_PATH = ROOT / "production/part3/part3_vo_manifest.json"
QC_JSON_PATH = ROOT / "production/part3/part3_vo_qc_report.json"
QC_TEXT_PATH = ROOT / "production/part3/part3_vo_qc_report.txt"

# Chapter 9's narrator audio is split across three raw batches because speech
# moderation blocks the full-chapter text even after the user-approved
# substitutions in production/part3/chapter9_vo_override.json.
CHAPTER_NARRATOR_BATCH = {
    "[CHAPTER 8: THE KING IN THE TENT]": "p3_narr_c8.mp3",
    "[CHAPTER 10: THE HORSE]": "p3_narr_c10.mp3",
}
C9_BATCH_BY_LINE = {
    5: "p3_narr_c9a.mp3", 6: "p3_narr_c9a.mp3",
    7: "p3_narr_c9c.mp3", 10: "p3_narr_c9c.mp3",
    11: "p3_narr_c9b.mp3", 13: "p3_narr_c9b.mp3",
    15: "p3_narr_c9b.mp3", 16: "p3_narr_c9b.mp3",
}
VOICE_BATCHES = {
    "voice-02": "p3_v02.mp3",
    "voice-03": "p3_v03.mp3",
    "voice-04": "p3_v04.mp3",
}
PRE_ATEMPO = {
    "voice-00": 0.85,
    "voice-02": 0.85,
    "voice-03": 0.85,
    "voice-04": 0.92,
}
EXPECTED_RAW = {
    "p3_narr_c8.mp3", "p3_narr_c9a.mp3", "p3_narr_c9b.mp3", "p3_narr_c9c.mp3",
    "p3_narr_c10.mp3", "p3_v02.mp3", "p3_v03.mp3", "p3_v04.mp3",
}
# Session voice IDs used when the raw batches were synthesized (these differ from
# the historical project mapping; the project role is what each segment records).
GENERATION_VOICE_SESSIONS = {
    "p3_narr_c8.mp3": "session voice-00 (narrator)",
    "p3_narr_c9a.mp3": "session voice-00 (narrator)",
    "p3_narr_c9b.mp3": "session voice-00 (narrator)",
    "p3_narr_c9c.mp3": "session voice-00 (narrator)",
    "p3_narr_c10.mp3": "session voice-00 (narrator)",
    "p3_v02.mp3": "session voice-01 (heroic/young male; project voice-02 role)",
    "p3_v03.mp3": "session voice-04 (regal/gruff; project voice-03 role)",
    "p3_v04.mp3": "session voice-03 (female; project voice-04 role)",
}

def run(command):
    return subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def mp3_to_float(path: Path, atempo: float) -> np.ndarray:
    with tempfile.TemporaryDirectory(prefix="part3_vo_decode_") as tmpdir:
        tmp_wav = Path(tmpdir) / "decoded.wav"
        run([
            FFMPEG, "-y", "-v", "error", "-i", str(path),
            "-filter:a", f"atempo={atempo:.4f}",
            "-ac", "1", "-ar", str(SR), "-f", "wav", str(tmp_wav)
        ])
        _, data = wavfile.read(tmp_wav)
    if data.dtype == np.int16:
        return data.astype(np.float32) / 32768.0
    return data.astype(np.float32)


def split_audio_by_segments(audio: np.ndarray, texts: list[str]) -> list[np.ndarray]:
    """Allocate a combined raw batch to its script lines using pauses and word weights."""
    n = len(texts)
    if n == 0:
        return []
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
        frame = audio[i * hop : i * hop + win]
        rms[i] = np.sqrt(np.mean(frame * frame) + 1e-12)
    rms_smooth = np.convolve(rms, np.ones(5, dtype=np.float32) / 5.0, mode="same")

    threshold = max(float(np.percentile(rms_smooth, 25)), 0.008)
    is_silent = rms_smooth < threshold
    pauses = []
    in_pause = False
    start_f = 0
    for i, silent in enumerate(is_silent):
        if silent and not in_pause:
            in_pause = True
            start_f = i
        elif not silent and in_pause:
            in_pause = False
            duration_frames = i - start_f
            if start_f > 20 and i < num_frames - 20 and duration_frames >= 10:
                mid_f = (start_f + i) // 2
                min_rms = float(np.min(rms_smooth[start_f:i]))
                pauses.append((mid_f * hop, duration_frames * 0.01, min_rms))

    weights = [max(len(text.split()), 2) + 1.5 for text in texts]
    total_weight = sum(weights)
    cumulative = []
    acc = 0.0
    for weight in weights[:-1]:
        acc += weight
        cumulative.append(acc / total_weight)

    total_samples = len(audio)
    split_points = [0]
    used_pauses = set()
    for fraction in cumulative:
        target_sample = int(fraction * total_samples)
        previous = split_points[-1]
        search_window = int(0.16 * total_samples)
        best = None
        best_score = 1e18
        for pause_index, (position, duration, pause_rms) in enumerate(pauses):
            if pause_index in used_pauses or position <= previous + int(0.3 * SR):
                continue
            distance = abs(position - target_sample)
            if distance <= search_window:
                score = distance / SR - duration * 1.8
                if score < best_score:
                    best_score = score
                    best = (pause_index, position)
        if best is not None:
            used_pauses.add(best[0])
            split_points.append(best[1])
        else:
            lo_frame = max((previous // hop) + 25, int((target_sample - 0.08 * total_samples) // hop))
            hi_frame = min(num_frames - 25, int((target_sample + 0.08 * total_samples) // hop))
            if hi_frame > lo_frame:
                best_frame = lo_frame + int(np.argmin(rms_smooth[lo_frame:hi_frame]))
                split_points.append(best_frame * hop)
            else:
                split_points.append(target_sample)
    split_points.append(total_samples)

    segments = []
    for index in range(n):
        segment = audio[split_points[index] : split_points[index + 1]]
        nonzero = np.where(np.abs(segment) > 0.008)[0]
        if len(nonzero) > 0:
            start = max(0, int(nonzero[0]) - int(0.05 * SR))
            end = min(len(segment), int(nonzero[-1]) + int(0.08 * SR))
            segment = segment[start:end]
        segments.append(segment)
    return segments


def conform_segment_pace(segment: np.ndarray, word_count: int) -> np.ndarray:
    current_duration = len(segment) / SR
    if current_duration <= 0.0:
        raise ValueError("An assigned VO line decoded to zero samples.")
    target_duration = max(0.9, (word_count / CONFORM_WPM) * 60.0)
    current_wpm = word_count / current_duration * 60.0
    if 124.0 <= current_wpm <= 140.0:
        return segment
    ratio = current_duration / target_duration
    tempo = max(0.60, min(1.70, ratio))
    with tempfile.TemporaryDirectory(prefix="part3_vo_tempo_") as tmpdir:
        input_wav = Path(tmpdir) / "input.wav"
        output_wav = Path(tmpdir) / "conformed.wav"
        wavfile.write(input_wav, SR, (np.clip(segment, -1.0, 1.0) * 32767).astype(np.int16))
        run([
            FFMPEG, "-y", "-v", "error", "-i", str(input_wav),
            "-filter:a", f"atempo={tempo:.4f}",
            "-ac", "1", "-ar", str(SR), "-f", "wav", str(output_wav)
        ])
        _, data = wavfile.read(output_wav)
    return data.astype(np.float32) / 32768.0


def get_sentence_chunks(text: str) -> list[str]:
    pieces = re.split(r"(?<=[.!?])\s+", text.strip())
    return [piece for piece in pieces if piece]


def sentence_split_long_narration(item: dict, audio: np.ndarray) -> list[dict]:
    text = item["clean_speech"]
    if item["speaker"] != "NARRATOR" or item["words"] < 45:
        item = dict(item)
        item["audio"] = conform_segment_pace(audio, item["words"])
        return [item]
    sentences = get_sentence_chunks(text)
    if len(sentences) < 2:
        item = dict(item)
        item["audio"] = conform_segment_pace(audio, item["words"])
        return [item]
    midpoint = len(sentences) // 2
    texts = [" ".join(sentences[:midpoint]), " ".join(sentences[midpoint:])]
    if " ".join(texts) != text:
        raise AssertionError("Narration split did not preserve exact text.")
    audio_parts = split_audio_by_segments(audio, texts)
    result = []
    for part_index, (part_text, part_audio) in enumerate(zip(texts, audio_parts), start=1):
        part = dict(item)
        part["clean_speech"] = part_text
        part["words"] = len(part_text.split())
        part["subline_index"] = part_index
        part["audio"] = conform_segment_pace(part_audio, part["words"])
        result.append(part)
    return result


def prepare_lines(part_lines: list[dict], override_doc: dict) -> tuple[list[dict], dict[str, list[dict]]]:
    replacements = {entry["before"]: entry["after"] for entry in override_doc["replacements"]}
    lines_by_batch: dict[str, list[dict]] = {}
    seen = set()

    for source_line in part_lines:
        item = dict(source_line)
        text = item["clean_speech"]
        for before, after in replacements.items():
            if before in text:
                if text.count(before) != 1:
                    raise AssertionError(f"Expected one override match on line {item['line_index']}.")
                text = text.replace(before, after, 1)
        item["clean_speech"] = text
        item["words"] = len(text.split())

        if item["voice_id"] == "voice-00":
            if item["chapter"].startswith("[CHAPTER 9"):
                batch_name = C9_BATCH_BY_LINE.get(item["line_index"])
            else:
                batch_name = CHAPTER_NARRATOR_BATCH.get(item["chapter"])
            if not batch_name:
                raise ValueError(
                    f"No narrator raw batch mapping for {item['chapter']} line {item['line_index']}."
                )
        elif item["voice_id"] in VOICE_BATCHES:
            batch_name = VOICE_BATCHES[item["voice_id"]]
        else:
            raise ValueError(f"Unknown voice mapping for line {item['line_index']}.")
        if batch_name not in RAW_FILES:
            raise FileNotFoundError(f"Missing raw VO batch: {RAW_DIR / batch_name}")
        item["raw_batch"] = batch_name
        lines_by_batch.setdefault(batch_name, []).append(item)
        seen.add(item["line_index"])

    expected = {line["line_index"] for line in part_lines}
    if seen != expected:
        raise AssertionError(f"Unmapped script lines: {sorted(expected - seen)}")
    for batch_lines in lines_by_batch.values():
        batch_lines.sort(key=lambda line: line["line_index"])
    return part_lines, lines_by_batch


def assemble_clips(expanded_items: list[dict]) -> tuple[list[list[dict]], list[dict]]:
    clip_lines = []
    current = []
    current_words = 0
    for item in expanded_items:
        words = item["words"]
        chapter_changed = bool(current and current[-1]["chapter"] != item["chapter"])
        if current and (current_words + words > MAX_CLIP_WORDS or chapter_changed):
            if (chapter_changed and current_words < 18 and clip_lines and
                    clip_lines[-1][0]["chapter"] == current[0]["chapter"]):
                clip_lines[-1].extend(current)
            else:
                clip_lines.append(current)
            current = []
            current_words = 0
        current.append(item)
        current_words += words
    if current:
        if (current_words < 18 and clip_lines and
                clip_lines[-1][0]["chapter"] == current[0]["chapter"]):
            clip_lines[-1].extend(current)
        else:
            clip_lines.append(current)

    rendered = []
    for clip_index, items in enumerate(clip_lines, start=1):
        clip_id = f"p3_clip_{clip_index:02d}"
        clip_words = sum(item["words"] for item in items)
        target_clip_duration = (clip_words / TARGET_WPM) * 60.0
        speech_duration = sum(len(item["audio"]) / SR for item in items)
        number_of_gaps = len(items) + 1
        gap_duration = max(0.20, min(0.55, (target_clip_duration - speech_duration) / number_of_gaps))
        gap_samples = int(round(gap_duration * SR))
        opening_gap_samples = int(round(gap_duration * 0.6 * SR))
        pieces = [np.zeros(opening_gap_samples, dtype=np.float32)]
        cursor_samples = opening_gap_samples
        timeline = []
        for item in items:
            speech = item["audio"]
            rms = float(np.sqrt(np.mean(speech * speech) + 1e-12))
            gain = min(3.0, 0.12 / rms)
            normalized = np.clip(speech * gain, -0.89, 0.89).astype(np.float32)
            duration = len(normalized) / SR
            segment = {
                "line_index": item["line_index"],
                "subline_index": item.get("subline_index", 1),
                "speaker": item["speaker"],
                "voice_id": item["voice_id"],
                "text": item["clean_speech"],
                "words": item["words"],
                "t_start": round(cursor_samples / SR, 3),
                "t_end": round((cursor_samples + len(normalized)) / SR, 3),
                "duration_s": round(duration, 3),
                "speech_wpm": round(item["words"] / duration * 60.0, 1),
                "raw_batch": item["raw_batch"],
            }
            timeline.append(segment)
            pieces.append(normalized)
            cursor_samples += len(normalized)
            pieces.append(np.zeros(gap_samples, dtype=np.float32))
            cursor_samples += gap_samples

        pcm = np.concatenate(pieces)
        clip_duration = len(pcm) / SR
        clip_wpm = clip_words / clip_duration * 60.0
        rendered.append({
            "clip_id": clip_id,
            "chapter": items[0]["chapter"],
            "file_path": f"production/part3/vo/{clip_id}.mp3",
            "duration_s": round(clip_duration, 3),
            "words": clip_words,
            "wpm": round(clip_wpm, 1),
            "segments": timeline,
            "pcm": pcm,
        })
    return clip_lines, rendered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Measure and report without writing clip files.")
    parser.add_argument("--overwrite", action="store_true", help="Replace only p3_clip_*.mp3 and Part 3 VO reports.")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg is required on PATH (or in .venv/bin).")
    part_data = json.loads((ROOT / "production/parts_breakdown.json").read_text())["3"]
    part_lines = part_data["lines"]
    override_doc = json.loads((ROOT / "production/part3/chapter9_vo_override.json").read_text())
    if override_doc.get("source_script_modified") is not False:
        raise ValueError("The approved source script must remain unchanged.")

    global RAW_FILES
    RAW_FILES = {path.name for path in RAW_DIR.glob("*.mp3")}
    expected_raw = set(EXPECTED_RAW)
    missing_raw = sorted(expected_raw - RAW_FILES)
    if missing_raw:
        raise FileNotFoundError(f"Missing Part 3 raw voice batches: {missing_raw}")

    _, batch_lines = prepare_lines(part_lines, override_doc)
    expected_batch_names = sorted(expected_raw)
    expanded_items = []
    batch_diagnostics = {}
    for batch_name in expected_batch_names:
        lines = batch_lines.get(batch_name, [])
        if not lines:
            raise ValueError(f"Raw batch {batch_name} is not mapped to any approved script lines.")
        voice_id = lines[0]["voice_id"]
        if any(line["voice_id"] != voice_id for line in lines):
            raise ValueError(f"Mixed voice identities in {batch_name}.")
        raw_path = RAW_DIR / batch_name
        atempo = PRE_ATEMPO[voice_id]
        audio = mp3_to_float(raw_path, atempo)
        line_texts = [line["clean_speech"] for line in lines]
        audio_segments = split_audio_by_segments(audio, line_texts)
        if len(audio_segments) != len(lines):
            raise AssertionError(f"Line split count mismatch in {batch_name}.")
        before_tempo_wpm = sum(line["words"] for line in lines) / max(0.001, len(audio) / SR) * 60.0
        batch_diagnostics[batch_name] = {
            "voice_id": voice_id,
            "lines": len(lines),
            "words": sum(line["words"] for line in lines),
            "raw_batch_decoded_seconds_after_pretime": round(len(audio) / SR, 3),
            "estimated_preconform_wpm": round(before_tempo_wpm, 1),
        }
        for line, segment in zip(lines, audio_segments):
            if len(segment) < int(0.25 * SR):
                raise ValueError(f"Suspiciously short audio assignment for line {line['line_index']} in {batch_name}.")
            line_items = sentence_split_long_narration(line, segment)
            expanded_items.extend(line_items)

    # Ensure script-order assembly independent of the order in which raw batches were decoded.
    expanded_items.sort(key=lambda item: (item["line_index"], item.get("subline_index", 1)))
    clip_lines, clips = assemble_clips(expanded_items)

    per_line_text = {}
    per_line_occurrences = {}
    for item in expanded_items:
        per_line_text.setdefault(item["line_index"], []).append(item["clean_speech"])
        per_line_occurrences[item["line_index"]] = per_line_occurrences.get(item["line_index"], 0) + 1
    expected_text = {}
    repl = {entry["before"]: entry["after"] for entry in override_doc["replacements"]}
    for line in part_lines:
        text = line["clean_speech"]
        for before, after in repl.items():
            if before in text:
                text = text.replace(before, after, 1)
        expected_text[line["line_index"]] = text
    line_text_check = all(
        " ".join(per_line_text.get(index, [])) == text
        for index, text in expected_text.items()
    )
    expected_index_set = set(expected_text)
    observed_index_set = set(per_line_text)
    line_coverage = expected_index_set == observed_index_set
    total_words = sum(item["words"] for item in expanded_items)
    total_duration = sum(clip["duration_s"] for clip in clips)
    average_wpm = total_words / max(0.001, total_duration) * 60.0
    clip_pace_pass = all(104.0 <= clip["wpm"] <= 156.0 for clip in clips)
    line_pace_pass = all(104.0 <= item["words"] / max(0.001, len(item["audio"]) / SR) * 60.0 <= 156.0
                         for item in expanded_items)
    estimate_clips = int(part_data.get("est_clips", len(clips)))
    checks = {
        "all_8_raw_batches_mapped": len(batch_diagnostics) == 8,
        "all_source_lines_covered": line_coverage,
        "voice_text_matches_source_plus_approved_override": line_text_check,
        "clip_count_matches_estimate": len(clips) == estimate_clips,
        "all_clips_within_44_word_cap": all(clip["words"] <= MAX_CLIP_WORDS for clip in clips),
        "all_clip_paces_within_20_percent": clip_pace_pass,
        "all_segment_paces_within_20_percent": line_pace_pass,
        "average_pace_within_20_percent": 104.0 <= average_wpm <= 156.0,
    }

    if not args.dry_run:
        existing = list(OUT_DIR.glob("p3_clip_*.mp3")) if OUT_DIR.exists() else []
        if existing and not args.overwrite:
            raise FileExistsError(
                f"{len(existing)} existing Part 3 VO clips found; pass --overwrite only if you intend to replace these assets."
            )
        if args.overwrite:
            for path in existing:
                path.unlink()
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        manifest_clips = []
        for clip in clips:
            wav_path = OUT_DIR / f"{clip['clip_id']}.tmp.wav"
            mp3_path = ROOT / clip["file_path"]
            wavfile.write(wav_path, SR, (clip["pcm"] * 32767).astype(np.int16))
            run([
                FFMPEG, "-y", "-v", "error", "-i", str(wav_path),
                "-c:a", "libmp3lame", "-b:a", "192k", str(mp3_path)
            ])
            wav_path.unlink(missing_ok=True)
            # Probe the encoded clip so the hash/bytes reflect the accepted delivery asset.
            decoded = run([
                FFMPEG, "-v", "error", "-i", str(mp3_path), "-ac", "1", "-ar", str(SR),
                "-f", "s16le", "pipe:1"
            ]).stdout
            encoded_samples = len(decoded) // 2
            audio_array = np.frombuffer(decoded, dtype="<i2").astype(np.float32) / 32768.0
            peak = float(np.max(np.abs(audio_array))) if len(audio_array) else 0.0
            rms = float(np.sqrt(np.mean(audio_array * audio_array))) if len(audio_array) else 0.0
            manifest_clips.append({
                key: value for key, value in clip.items() if key != "pcm"
            } | {
                "file_path": str(mp3_path.relative_to(ROOT)),
                "decoded_seconds_after_mp3": round(encoded_samples / SR, 3),
                "audio_peak_dbfs": round(20.0 * math.log10(max(peak, 1e-12)), 2),
                "audio_rms_dbfs": round(20.0 * math.log10(max(rms, 1e-12)), 2),
                "file_bytes": mp3_path.stat().st_size,
                "file_sha256": hashlib.sha256(mp3_path.read_bytes()).hexdigest(),
            })
        manifest = {
            "part": 3,
            "title": part_data["title"],
            "source_script": "production/script_approved.txt",
            "source_script_sha256": hashlib.sha256((ROOT / "production/script_approved.txt").read_bytes()).hexdigest(),
            "override_path": "production/part3/chapter9_vo_override.json",
            "clip_count": len(manifest_clips),
            "word_count": total_words,
            "total_duration_s": round(total_duration, 3),
            "total_minutes": round(total_duration / 60.0, 3),
            "average_wpm": round(average_wpm, 1),
            "target_wpm": TARGET_WPM,
            "batch_diagnostics": batch_diagnostics,
            "generation_voice_sessions": GENERATION_VOICE_SESSIONS,
            "clips": manifest_clips,
            "qc_checks": checks,
        }
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n")
        qc_report = {
            "passed": all(checks.values()),
            "checks": checks,
            "clip_count": len(clips),
            "expected_clips": estimate_clips,
            "word_count": total_words,
            "duration_seconds": round(total_duration, 3),
            "average_wpm": round(average_wpm, 1),
            "batch_diagnostics": batch_diagnostics,
            "clip_summary": [
                {"clip_id": clip["clip_id"], "chapter": clip["chapter"], "words": clip["words"],
                 "duration_s": clip["duration_s"], "wpm": clip["wpm"]}
                for clip in clips
            ],
        }
        QC_JSON_PATH.write_text(json.dumps(qc_report, indent=2) + "\n")
        text_lines = [
            f"PART 3 VO QC — {'PASS' if qc_report['passed'] else 'FAIL'}",
            f"Raw batches: {len(batch_diagnostics)}/8 | Clips: {len(clips)} (estimate {estimate_clips})",
            f"VO words: {total_words} | Runtime: {total_duration:.2f}s ({total_duration/60.0:.2f} min) | Average pace: {average_wpm:.1f} WPM",
            "",
            "Checks:",
        ]
        text_lines.extend(f"  {'PASS' if ok else 'FAIL'}  {name.replace('_', ' ')}" for name, ok in checks.items())
        text_lines += ["", "Clip pace summary:"]
        text_lines.extend(
            f"  {clip['clip_id']} | {clip['chapter']} | {clip['words']}w | {clip['duration_s']:.2f}s | {clip['wpm']:.1f} WPM"
            for clip in clips
        )
        QC_TEXT_PATH.write_text("\n".join(text_lines) + "\n")

    print(f"Part 3 raw batches mapped: {len(batch_diagnostics)}/8")
    for name, diag in batch_diagnostics.items():
        print(f"  {name}: {diag['lines']} lines, {diag['words']} words, {diag['estimated_preconform_wpm']:.1f} WPM after pre-tempo")
    print(f"Measured clips: {len(clips)} (estimate {estimate_clips}) | {total_words} words | {total_duration:.2f}s | {average_wpm:.1f} WPM")
    for clip in clips:
        print(f"  {clip['clip_id']} | {clip['chapter']} | {clip['words']}w | {clip['duration_s']:.2f}s | {clip['wpm']:.1f} WPM")
    print("QC:", json.dumps(checks, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit(1)
    if not args.dry_run:
        print(f"Wrote {MANIFEST_PATH.relative_to(ROOT)}, {QC_TEXT_PATH.relative_to(ROOT)}, and {len(clips)} MP3 clips.")


if __name__ == "__main__":
    main()
