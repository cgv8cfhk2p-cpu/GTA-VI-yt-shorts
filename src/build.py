# -*- coding: utf-8 -*-
"""Pipeline completo: guion -> voz (Kokoro TTS) -> música -> animación -> montaje MP4.

Uso:
  python src/build.py tts                 # genera las voces de todos los vídeos
  python src/build.py render [ids...]     # renderiza (por defecto todos, en paralelo)
  python src/build.py preview <id> <seg>  # exporta un frame PNG para revisar
"""
import json
import math
import os
import random
import subprocess
import sys
import wave
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from guiones import VIDEOS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.environ.get("SHORTS_WORK", os.path.join(ROOT, "work"))
OUT = os.path.join(ROOT, "videos")
MODELS = os.environ.get("KOKORO_DIR", os.path.join(ROOT, "models"))
VOICE = os.environ.get("VOICE", "em_alex")
SPEED = float(os.environ.get("SPEED", "1.12"))
SR = 44100
GAP = 0.28        # silencio entre escenas
LEAD = 0.05

# Pronunciación: el TTS lee mejor estas palabras escritas "a la española"
PHON = [
    ("GTA Online", "ge te a onláin"), ("GTA", "ge te a"), ("Rockstar North", "Rocstar Nors"), ("Rockstar", "Rocstar"),
    ("Vice City", "Váis Síti"), ("Liberty City", "Líberti Síti"), ("Race and Chase", "Réis an Chéis"),
    ("DMA Design", "de eme a disáin"), ("Tommy Vercetti", "Tómi Verchéti"), ("Ray Liotta", "Réi Lióta"),
    ("Niko Bellic", "Níko Bélic"), ("Michael", "Máikel"), ("Franklin", "Fránklin"), ("Trevor", "Trévor"),
    ("Jason", "Yéison"), ("Bonnie y Clyde", "Bóni y Cláid"), ("PlayStation", "Pléisteishon"),
    ("Xbox Series", "Équis box Síries"), ("Minecraft", "Máincraft"), ("Bigfoot", "Bigfút"),
    ("Grassrivers", "Grasríbers"), ("Everglades", "Éverglèids"), ("Amazon Fire Stick", "Ámazon Fáier Stic"),
    ("Red Dead Redemption", "Red Ded Ridémpshon"), ("jetpack", "yétpac"), ("hacker", "jáker"),
    ("Easter eggs", "íster egs"), ("Chiliad", "Chíliad"), ("Leonida", "Leonída"),
    ("2D", "dos de"), ("Liberty", "Líberti"), ("Las Venturas", "Las Bentúras"),
]


def phon(text):
    s = text.replace("*", "")
    for a, b in PHON:
        s = s.replace(a, b)
    return s


def wpath(vid, i):
    return os.path.join(WORK, vid, f"s{i:02d}.wav")


def write_wav(path, data, sr):
    data = np.clip(data, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((data * 32767).astype(np.int16).tobytes())


def read_wav(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32767
    return x, sr


def do_tts(only=None):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(MODELS, "kokoro-v1.0.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))
    for v in VIDEOS:
        if only and v["id"] not in only:
            continue
        os.makedirs(os.path.join(WORK, v["id"]), exist_ok=True)
        for i, sc in enumerate(v["scenes"]):
            p = wpath(v["id"], i)
            if os.path.exists(p):
                continue
            samples, sr = k.create(phon(sc["say"]), voice=VOICE, speed=SPEED, lang="es")
            samples = np.asarray(samples, dtype=np.float32)
            # recorta silencios de los bordes
            idx = np.where(np.abs(samples) > 0.01)[0]
            if len(idx):
                samples = samples[max(0, idx[0] - 600): idx[-1] + 1200]
            write_wav(p, samples, sr)
            print(v["id"], i, f"{len(samples) / sr:.2f}s", flush=True)


def timeline(v):
    from scipy.signal import resample_poly
    voices, starts, durs = [], [], []
    t = 0.0
    n = len(v["scenes"])
    for i in range(n):
        x, sr = read_wav(wpath(v["id"], i))
        if sr != SR:
            g = math.gcd(SR, sr)
            x = resample_poly(x, SR // g, sr // g).astype(np.float32)
        vl = len(x) / SR
        d = LEAD + vl + GAP + (1.6 if i == n - 1 else 0)
        voices.append(x)
        starts.append(t)
        durs.append(d)
        t += d
    return voices, starts, durs, t


def movavg(x, k):
    c = np.cumsum(np.concatenate([np.zeros(k // 2 + 1), x, np.zeros(k)]))
    return ((c[k:k + len(x)] - c[:len(x)]) / k).astype(np.float32)


def build_audio(v, voices, starts, durs, total, path):
    from music import synthwave, whoosh, impact, pop
    seed = sum(map(ord, v["id"]))
    rng = random.Random(seed)
    n = int((total + 0.5) * SR)
    voice = np.zeros(n, np.float32)
    for x, s in zip(voices, starts):
        a = int((s + LEAD) * SR)
        voice[a:a + len(x)] += x[: n - a]
    voice /= (np.max(np.abs(voice)) + 1e-9)
    voice *= 0.95
    sfx = np.zeros(n, np.float32)

    def add(sig, t, g=1.0):
        a = max(0, int(t * SR))
        e = min(n, a + len(sig))
        sfx[a:e] += sig[: e - a] * g

    add(impact(seed), 0.0, 0.55)
    for i, s in enumerate(starts[1:], 1):
        add(whoosh(seed + i), s - 0.2, 0.35)
    for i, sc in enumerate(v["scenes"]):
        if sc["vis"]["type"] == "outro":
            add(pop(), starts[i] + 1.42, 0.8)
    music = synthwave(n / SR, bpm=rng.choice([96, 100, 104, 108]), root=rng.choice([52, 55, 57, 50]),
                      seed=seed, style=rng.randrange(3))
    music = np.pad(music, (0, max(0, n - len(music))))[:n]
    # ducking: baja la música cuando habla la voz
    env = np.abs(voice)
    k = int(0.08 * SR)
    env = movavg(movavg(env, k), k * 3)
    duck = 0.30 - 0.17 * np.clip(env / 0.05, 0, 1)
    mixd = voice + music * duck + sfx * 0.6
    mixd /= (np.max(np.abs(mixd)) + 1e-9)
    write_wav(path, mixd * 0.95, SR)


def frame_at(v, t, starts, durs, caps, total):
    from render import Ctx, THEMES, draw_bg, render_scene, draw_caption, overlays, ease_out_cubic
    from PIL import Image
    th_name = v["theme"]
    th = THEMES[th_name]
    i = max(j for j in range(len(starts)) if starts[j] <= t + 1e-9)
    lt = t - starts[i]
    c = draw_bg(th_name, t)
    # temblor de cámara al empezar cada escena
    sh = math.exp(-lt * 14) * (16 if i == 0 else 9)
    Ctx.ox = int(sh * math.sin(lt * 90))
    Ctx.oy = int(sh * math.cos(lt * 77))
    render_scene(c, lt, durs[i], v["scenes"][i]["vis"], th, th_name)
    Ctx.ox = Ctx.oy = 0
    words, times, chunks = caps[i]
    draw_caption(c, t, words, times, chunks, starts[i] + durs[i], th)
    overlays(c, t, total, th)
    if i > 0 and lt < 0.12:
        c = Image.blend(c, Image.new("RGB", c.size, (255, 255, 255)), 0.45 * (1 - lt / 0.12))
    return c


def prepare(v):
    from render import caption_chunks
    voices, starts, durs, total = timeline(v)
    caps = []
    for i, sc in enumerate(v["scenes"]):
        t0 = starts[i] + LEAD
        caps.append(caption_chunks(sc["say"], t0, t0 + len(voices[i]) / SR))
    return voices, starts, durs, total, caps


def render_video(vid):
    v = next(x for x in VIDEOS if x["id"] == vid)
    os.makedirs(OUT, exist_ok=True)
    wd = os.path.join(WORK, vid)
    voices, starts, durs, total, caps = prepare(v)
    apath = os.path.join(wd, "mix.wav")
    build_audio(v, voices, starts, durs, total, apath)
    out = os.path.join(OUT, f"{vid}.mp4")
    nframes = int(total * 30)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920",
           "-r", "30", "-i", "-", "-i", apath, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
           "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(nframes):
        t = f / 30
        img = frame_at(v, t, starts, durs, caps, total)
        p.stdin.write(img.tobytes())
        if f == int(0.7 * 30):
            img.save(os.path.join(OUT, f"{vid}_portada.jpg"), quality=92)
    p.stdin.close()
    p.wait()
    meta = {"id": vid, "duracion_s": round(total, 2), "escenas": [round(s, 2) for s in starts]}
    with open(os.path.join(wd, "meta.json"), "w") as fh:
        json.dump(meta, fh)
    return vid, total


def preview(vid, t):
    v = next(x for x in VIDEOS if x["id"] == vid)
    voices, starts, durs, total, caps = prepare(v)
    img = frame_at(v, float(t), starts, durs, caps, total)
    os.makedirs(os.path.join(WORK, "preview"), exist_ok=True)
    p = os.path.join(WORK, "preview", f"{vid}_{t}.png")
    img.save(p)
    print(p, f"total={total:.1f}s", "starts=", [round(s, 1) for s in starts])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "tts":
        do_tts(sys.argv[2:] or None)
    elif cmd == "render":
        ids = sys.argv[2:] or [v["id"] for v in VIDEOS]
        with ProcessPoolExecutor(max_workers=int(os.environ.get("JOBS", "4"))) as ex:
            for vid, total in ex.map(render_video, ids):
                print(f"OK {vid} {total:.1f}s", flush=True)
    elif cmd == "preview":
        for t in sys.argv[3:]:
            preview(sys.argv[2], t)
