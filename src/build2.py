# -*- coding: utf-8 -*-
"""Render del estilo 2 (fondo de vídeo real + HUD). Reutiliza voz, tiempos y audio de build.py.

Uso:
  CLIPS_DIR=/ruta/clips python src/build2.py render [ids...]
  CLIPS_DIR=/ruta/clips python src/build2.py preview <id> <segundo> [...]
"""
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import build as B  # noqa: E402
import render2 as R2  # noqa: E402
from guiones import VIDEOS  # noqa: E402
from planos import PLAN  # noqa: E402

FPS = 30


def overlay(c, v, i, lt, durs, t, caps, starts):
    R2.SCENES[v["scenes"][i]["vis"]["type"]](c, lt, durs[i], v["scenes"][i]["vis"])
    words, times, chunks = caps[i]
    R2.caption(c, t, words, times, chunks, starts[i] + durs[i])
    if i > 0 and lt < 0.1:
        c = Image.blend(c, Image.new("RGB", c.size, (255, 255, 255)), 0.5 * (1 - lt / 0.1))
    return c


def scene_at(starts, t):
    return max(j for j in range(len(starts)) if starts[j] <= t + 1e-9)


def render_video(vid, preview_times=None):
    v = next(x for x in VIDEOS if x["id"] == vid)
    voices, starts, durs, total, caps = B.prepare(v)
    seed = sum(map(ord, vid)) + 7
    pieces = R2.plan_pieces(vid, starts, durs, seed)
    nframes = pieces[-1][0] + pieces[-1][1]
    scene_start_frames = {round(s * FPS) for s in starts}

    if preview_times is not None:
        outs = []
        for tt in preview_times:
            fr = int(float(tt) * FPS)
            pc = next(p for p in pieces if p[0] <= fr < p[0] + p[1])
            k = fr - pc[0]
            rd = R2.PieceReader(pc[2], pc[3] + k / FPS, 1)
            raw = rd.frame()
            rd.close()
            c = R2.background(raw, k, pc[1], pc[0] in scene_start_frames)
            i = scene_at(starts, fr / FPS)
            c = overlay(c, v, i, fr / FPS - starts[i], durs, fr / FPS, caps, starts)
            p = os.path.join(B.WORK, "preview", f"v2_{vid}_{tt}.png")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            c.save(p)
            outs.append(p)
        return outs

    wd = os.path.join(B.WORK, vid)
    apath = os.path.join(wd, "mix.wav")
    B.build_audio(v, voices, starts, durs, total, apath)
    os.makedirs(B.OUT, exist_ok=True)
    out = os.path.join(B.OUT, f"{vid}.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920",
           "-r", "30", "-i", "-", "-i", apath, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
           "-shortest", "-movflags", "+faststart", out]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for (f0, n, sid, src) in pieces:
        rd = R2.PieceReader(sid, src, n)
        for k in range(n):
            fr = f0 + k
            t = fr / FPS
            raw = rd.frame()
            c = R2.background(raw, k, n, f0 in scene_start_frames)
            i = scene_at(starts, t)
            c = overlay(c, v, i, t - starts[i], durs, t, caps, starts)
            enc.stdin.write(c.tobytes())
            if fr == int(0.8 * FPS):
                c.save(os.path.join(B.OUT, f"{vid}_portada.jpg"), quality=92)
        rd.close()
    enc.stdin.close()
    enc.wait()
    return vid, total, len(pieces)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "render":
        ids = sys.argv[2:] or list(PLAN)
        with ProcessPoolExecutor(max_workers=int(os.environ.get("JOBS", "4"))) as ex:
            for vid, total, np_ in ex.map(render_video, ids):
                print(f"OK {vid} {total:.1f}s {np_} planos", flush=True)
    elif cmd == "preview":
        for p in render_video(sys.argv[2], sys.argv[3:]):
            print(p)
