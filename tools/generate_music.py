import os
import subprocess
import numpy as np
from scipy.io import wavfile

SR = 24000

def karplus_strong_pluck(freq, dur_s, sr=SR, decay=0.994):
    n_samples = int(dur_s * sr)
    N = max(2, int(sr / freq))
    buf = np.random.uniform(-1.0, 1.0, N).astype(np.float32)
    # Warm lowpass on initial excitation
    buf = np.convolve(buf, np.ones(4)/4.0, mode="same")
    out = np.zeros(n_samples, dtype=np.float32)
    for i in range(n_samples):
        out[i] = buf[i % N]
        avg = 0.5 * (buf[i % N] + buf[(i + 1) % N]) * decay
        buf[i % N] = avg
    # Gentle attack/release envelope
    env = np.ones(n_samples, dtype=np.float32)
    att = min(int(0.015 * sr), n_samples // 4)
    rel = min(int(0.15 * sr), n_samples // 3)
    env[:att] = np.linspace(0.0, 1.0, att)
    env[-rel:] = np.linspace(1.0, 0.0, rel)
    return out * env

def generate_part_stem(part_num, duration_s, root_hz, scale_ratios, tempo_bpm, out_mp3):
    n_samples = int((duration_s + 2.0) * SR)
    t = np.arange(n_samples, dtype=np.float32) / SR

    # 1. Warm atmospheric Bronze Age drone pad (root + fifth + octave with slow LFO)
    lfo1 = 0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t)
    lfo2 = 0.5 + 0.5 * np.cos(2 * np.pi * 0.05 * t)
    drone = (
        0.35 * np.sin(2 * np.pi * (root_hz * 0.5) * t) +
        0.25 * lfo1 * np.sin(2 * np.pi * (root_hz * 0.75) * t) +
        0.18 * lfo2 * np.sin(2 * np.pi * root_hz * t) +
        0.08 * np.sin(2 * np.pi * (root_hz * 1.5) * t)
    ).astype(np.float32)

    # 2. Plucked Greek Lyre / Kithara arpeggios in Dorian/Phrygian mode
    beat_s = 60.0 / tempo_bpm
    lyre_track = np.zeros(n_samples, dtype=np.float32)
    rng = np.random.default_rng(100 + part_num)
    pattern = [0, 2, 4, 3, 5, 4, 2, 1]
    step_s = beat_s * 0.5
    n_steps = int(duration_s / step_s)
    for idx in range(n_steps):
        if rng.random() < 0.18:
            continue
        deg = pattern[idx % len(pattern)]
        octave = 2.0 if (idx % 8 == 0 or rng.random() < 0.35) else 1.0
        freq = root_hz * scale_ratios[deg % len(scale_ratios)] * octave
        pluck = karplus_strong_pluck(freq, step_s * 2.2, SR, decay=0.995)
        start = int(idx * step_s * SR)
        end = min(n_samples, start + len(pluck))
        lyre_track[start:end] += 0.32 * pluck[:end - start]

    # 3. Deep frame drum (tymponon) heartbeat pulse on downbeats
    drum_track = np.zeros(n_samples, dtype=np.float32)
    measure_s = beat_s * 4.0
    n_measures = int(duration_s / measure_s)
    hit_len = int(0.45 * SR)
    ht = np.arange(hit_len, dtype=np.float32) / SR
    f_env = root_hz * 0.5 * (1.0 + 0.6 * np.exp(-ht * 28.0))
    amp_env = np.exp(-ht * 9.5)
    drum_hit = (np.sin(2 * np.pi * f_env * ht) * amp_env).astype(np.float32)

    for m in range(n_measures):
        for offset_beats, gain in [(0.0, 0.38), (2.5, 0.22)]:
            start = int((m * measure_s + offset_beats * beat_s) * SR)
            end = min(n_samples, start + hit_len)
            if end > start:
                drum_track[start:end] += gain * drum_hit[:end - start]

    mix = (0.45 * drone + 0.40 * lyre_track + 0.30 * drum_track)[:int(duration_s * SR)]
    # Fade in 1.5s, fade out 2.0s
    fi = int(1.5 * SR)
    fo = int(2.0 * SR)
    mix[:fi] *= np.linspace(0.0, 1.0, fi)
    mix[-fo:] *= np.linspace(1.0, 0.0, fo)

    # Normalize to -14 dBFS RMS so it sits cleanly before ducking
    rms = np.sqrt(np.mean(mix * mix) + 1e-12)
    mix = np.clip(mix * (0.18 / rms), -0.90, 0.90)

    tmp_wav = out_mp3 + ".tmp.wav"
    wavfile.write(tmp_wav, SR, (mix * 32767).astype(np.int16))
    subprocess.run([
        "ffmpeg", "-y", "-i", tmp_wav, "-c:a", "libmp3lame", "-b:a", "192k", out_mp3
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp_wav)
    print(f"Generated {out_mp3} ({duration_s:.1f}s)")

# Generate Preset A subtle SFX
def generate_sfx():
    # 1. Soft bubble pop
    n = int(0.12 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    freq = 320.0 + 480.0 * (t / 0.12)
    pop = np.sin(2 * np.pi * freq * t) * np.exp(-t * 32.0) * 0.35
    wavfile.write("production/sfx/pop.wav", SR, (pop * 32767).astype(np.int16))

    # 2. Soft card whoosh
    n = int(0.22 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    noise = np.random.normal(0, 1, n).astype(np.float32)
    noise = np.convolve(noise, np.ones(18)/18.0, mode="same")
    env = np.sin(np.pi * (t / 0.22)) ** 1.5
    whoosh = noise * env * 0.25
    wavfile.write("production/sfx/whoosh.wav", SR, (whoosh * 32767).astype(np.int16))

    # 3. Hand-drawn arrow sketch swish
    n = int(0.28 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    noise = np.random.normal(0, 1, n).astype(np.float32)
    noise = np.convolve(noise, np.ones(8)/8.0, mode="same")
    env = np.sin(np.pi * (t / 0.28))
    arrow = noise * env * 0.20
    wavfile.write("production/sfx/arrow.wav", SR, (arrow * 32767).astype(np.int16))
    print("Generated Preset A SFX: pop.wav, whoosh.wav, arrow.wav")

if __name__ == "__main__":
    generate_sfx()
    # D Dorian / E Phrygian / A Aeolian / D Dorian scales
    dorian = [1.0, 9/8, 6/5, 4/3, 3/2, 5/3, 9/5]
    phrygian = [1.0, 16/15, 6/5, 4/3, 3/2, 8/5, 9/5]
    aeolian = [1.0, 9/8, 6/5, 4/3, 3/2, 8/5, 9/5]

    generate_part_stem(1, 415.0, 146.83, dorian, 68.0, "production/music/part1_stem.mp3")
    generate_part_stem(2, 370.0, 164.81, phrygian, 74.0, "production/music/part2_stem.mp3")
    generate_part_stem(3, 370.0, 130.81, aeolian, 66.0, "production/music/part3_stem.mp3")
    generate_part_stem(4, 290.0, 146.83, dorian, 64.0, "production/music/part4_stem.mp3")
