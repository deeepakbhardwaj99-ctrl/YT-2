"""Run delivery QC on the full Part 2 export and write machine/text reports."""
from fractions import Fraction
from pathlib import Path
import json
import math
import os
import re
import shutil
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
LOCAL_BIN = ROOT / ".venv" / "bin"
if LOCAL_BIN.is_dir():
    os.environ["PATH"] = str(LOCAL_BIN) + os.pathsep + os.environ.get("PATH", "")
sys.path.insert(0, str(ROOT / "tools"))
from validate_part2 import validate  # noqa: E402

VIDEO = ROOT / "production/part2/part2_full.mp4"
MOTION_REPORT = ROOT / "production/part2/part2_motion_report.txt"
TEXT_REPORT = ROOT / "production/part2/part2_qc_report.txt"
JSON_REPORT = ROOT / "production/part2/part2_qc_report.json"
FPS = 24
SR = 24000
TOLERANCE_S = 0.12


def run(command):
    return subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def rms_dbfs(samples):
    if len(samples) == 0:
        return float("-inf")
    x = samples.astype(np.float64) / 32768.0
    rms = float(np.sqrt(np.mean(x * x)))
    return 20.0 * math.log10(max(rms, 1e-12))


def main():
    if not VIDEO.is_file():
        raise FileNotFoundError(f"Full Part 2 render not found: {VIDEO}")
    ffprobe = shutil.which("ffprobe")
    ffmpeg = shutil.which("ffmpeg")
    if not ffprobe or not ffmpeg:
        raise RuntimeError("QC requires both ffprobe and ffmpeg on PATH.")

    scenes = json.loads((ROOT / "production/scenes.json").read_text())["part2_clips"]
    vo_manifest = json.loads((ROOT / "production/part2/part2_vo_manifest.json").read_text())
    title_frames = round(2.5 * FPS)
    end_frames = round(2.5 * FPS)
    clip_frames = sum(max(1, round(c["duration_s"] * FPS)) for c in scenes)
    expected_frames = title_frames + clip_frames + end_frames
    expected_duration = expected_frames / FPS
    expected_vo_samples = sum(max(1, round(c["duration_s"] * SR)) for c in scenes)
    video_rounding_pad_s = max(0, clip_frames * (SR // FPS) - expected_vo_samples) / SR

    asset_gate = validate(require_complete=True)
    probe = json.loads(run([
        ffprobe, "-v", "error", "-show_entries",
        "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,channels,sample_rate,duration,nb_frames",
        "-of", "json", str(VIDEO)
    ]).stdout)
    streams = probe.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
    video_duration = float(video_stream.get("duration", probe.get("format", {}).get("duration", 0.0)))
    audio_duration = float(audio_stream.get("duration", 0.0))
    try:
        actual_frames = int(video_stream.get("nb_frames", -1))
    except (TypeError, ValueError):
        actual_frames = -1
    if actual_frames < 0:
        frame_probe = json.loads(run([
            ffprobe, "-v", "error", "-select_streams", "v:0", "-count_frames",
            "-show_entries", "stream=nb_read_frames", "-of", "json", str(VIDEO)
        ]).stdout)
        actual_frames = int(frame_probe["streams"][0].get("nb_read_frames", -1))

    # Decode both tracks fully, so truncated/corrupt packets cannot pass metadata-only QC.
    decode = run([ffmpeg, "-v", "error", "-i", str(VIDEO), "-f", "null", "-"])
    audio_decode = run([
        ffmpeg, "-v", "error", "-i", str(VIDEO), "-map", "0:a:0", "-ac", "1", "-ar", str(SR),
        "-f", "s16le", "pipe:1"
    ])
    audio_pcm = np.frombuffer(audio_decode.stdout, dtype="<i2")
    audio_duration_pcm = len(audio_pcm) / float(SR)
    peak = float(np.max(np.abs(audio_pcm.astype(np.int32)))) / 32768.0 if len(audio_pcm) else 0.0
    head_rms = rms_dbfs(audio_pcm[: SR // 2])
    tail_rms = rms_dbfs(audio_pcm[-SR // 2:])
    overall_rms = rms_dbfs(audio_pcm)

    motion_text = MOTION_REPORT.read_text() if MOTION_REPORT.is_file() else ""
    motion_gate = re.search(r"Max Near-Zero Motion Stretch.*->\s*(PASS|FAIL)", motion_text)
    motion_pass = bool(motion_gate and motion_gate.group(1) == "PASS")
    fps_raw = video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate") or "0/1"
    actual_fps = float(Fraction(fps_raw))
    part1_unchanged = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", "production/part1"], cwd=ROOT
    ).returncode == 0
    file_size = VIDEO.stat().st_size
    format_duration = float(probe.get("format", {}).get("duration", 0.0))

    checks = {
        "locked_script_and_vo_unchanged": asset_gate["script_verbatim"] and asset_gate["vo_segments_unchanged"],
        "all_123_backgrounds_accepted": asset_gate["accepted_plates"] == 123 and asset_gate["pending_plates"] == 0,
        "24_clips_in_export": len(scenes) == 24,
        "vo_manifest_qc_passed": all(vo_manifest.get("qc_checks", {}).values()),
        "chapter7_override_recorded": bool(vo_manifest.get("override_path")),
        "h264_1080p_video": video_stream.get("codec_name") == "h264" and
                             video_stream.get("width") == 1920 and video_stream.get("height") == 1080,
        "24_fps": abs(actual_fps - FPS) < 0.01,
        "expected_video_frame_count": actual_frames == expected_frames,
        "video_duration_within_tolerance": abs(video_duration - expected_duration) <= TOLERANCE_S,
        "audio_present_aac_mono_24khz": audio_stream.get("codec_name") == "aac" and
                                        audio_stream.get("channels") == 1 and
                                        int(audio_stream.get("sample_rate", 0)) == SR,
        "audio_duration_within_tolerance": abs(audio_duration_pcm - expected_duration) <= TOLERANCE_S,
        "audio_not_silent": overall_rms > -35.0 and head_rms > -50.0 and tail_rms > -50.0,
        "audio_not_clipped": peak < 0.999,
        "full_audio_video_decode": decode.returncode == 0 and audio_decode.returncode == 0,
        "motion_gate_passed": motion_pass,
        "part1_export_unchanged": part1_unchanged,
        "under_99mb_single_file_push_target": file_size < 99_000_000,
    }
    passed = all(checks.values())
    report = {
        "passed": passed,
        "checks": checks,
        "asset_gate": asset_gate,
        "expected": {
            "clip_count": len(scenes),
            "video_frames": expected_frames,
            "frame_rate": FPS,
            "duration_seconds": round(expected_duration, 6),
            "vo_sample_count_before_cards": expected_vo_samples,
            "video_frame_rounding_audio_pad_seconds": round(video_rounding_pad_s, 6),
        },
        "measured": {
            "format_duration_seconds": round(format_duration, 6),
            "video_duration_seconds": round(video_duration, 6),
            "audio_stream_duration_seconds": round(audio_duration, 6),
            "decoded_audio_duration_seconds": round(audio_duration_pcm, 6),
            "video_frames": actual_frames,
            "frame_rate": actual_fps,
            "video_codec": video_stream.get("codec_name"),
            "resolution": f"{video_stream.get('width')}x{video_stream.get('height')}",
            "audio_codec": audio_stream.get("codec_name"),
            "audio_sample_rate": audio_stream.get("sample_rate"),
            "audio_channels": audio_stream.get("channels"),
            "audio_peak_dbfs": round(20 * math.log10(max(peak, 1e-12)), 3),
            "audio_rms_dbfs": round(overall_rms, 3),
            "first_half_second_rms_dbfs": round(head_rms, 3),
            "last_half_second_rms_dbfs": round(tail_rms, 3),
            "file_size_bytes": file_size,
            "file_size_mib": round(file_size / (1024 * 1024), 2),
        },
    }
    JSON_REPORT.write_text(json.dumps(report, indent=2) + "\n")
    lines = [
        f"PART 2 DELIVERY QC — {'PASS' if passed else 'FAIL'}",
        f"Video: {VIDEO.relative_to(ROOT)} ({report['measured']['file_size_mib']} MiB)",
        f"Duration: video {video_duration:.3f}s | decoded audio {audio_duration_pcm:.3f}s | expected {expected_duration:.3f}s",
        f"Picture: {video_stream.get('codec_name')} {video_stream.get('width')}x{video_stream.get('height')} @ {actual_fps:.3f} fps, {actual_frames} frames",
        f"Sound: {audio_stream.get('codec_name')} {audio_stream.get('sample_rate')} Hz, {audio_stream.get('channels')} channel(s), peak {report['measured']['audio_peak_dbfs']:.2f} dBFS, RMS {overall_rms:.2f} dBFS",
        "",
        "Checks:",
    ]
    lines.extend(f"  {'PASS' if ok else 'FAIL'}  {name.replace('_', ' ')}" for name, ok in checks.items())
    lines.append("")
    TEXT_REPORT.write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"Detailed JSON: {JSON_REPORT.relative_to(ROOT)}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
