# -*- coding: utf-8 -*-
"""Estilo 2: fondo de vídeo real (tráilers) a pantalla completa + HUD tipo videojuego.

Título con número verde y etiqueta blanca inclinada arriba, paneles oscuros con borde neón
en la parte media-baja y subtítulos en cursiva con la palabra activa en verde.
"""
import functools
import json
import math
import os
import random
import subprocess

from PIL import Image, ImageDraw, ImageFilter

import render as R
from render import (W, H, WHITE, BLACK, RED, clamp, ease_out_back, ease_out_cubic, lerp,
                    text_img, put, font, fmt_num, icon, _steps)
from planos import TAGS, XPOS, PLAN, ROTATE

GREEN = (72, 232, 84)
NAVY = (12, 16, 30)
FPS = 30
HEADER_Y = 330
HUD_Y = 1170
CAP_Y = 1450
CLIPS_DIR = os.environ.get("CLIPS_DIR", "clips")


# ----------------------------------------------------------------- planos de fondo
@functools.lru_cache(maxsize=1)
def shots():
    with open(os.path.join(CLIPS_DIR, "shots.json")) as f:
        return {s["id"]: s for s in json.load(f)}


def plan_pieces(vid, starts, durs, seed):
    """Reparte planos reales en cada escena: cortes cada ~1-1.6 s, sin repetir seguidos."""
    rng = random.Random(seed)
    lib = shots()
    used = {}
    pieces = []  # (frame_inicio, n_frames, shot_id, src_start)
    prev = None
    for i, (s, d) in enumerate(zip(starts, durs)):
        f0 = round(s * FPS)
        f1 = round((s + d) * FPS)
        pool = []
        for tag in PLAN[vid][i]:
            pool += [x for x in TAGS[tag] if x in lib]
        pool = list(dict.fromkeys(pool))
        f = f0
        while f < f1:
            cands = [x for x in pool if x != prev] or pool
            m = min(used.get(x, 0) for x in cands)
            pick = rng.choice([x for x in cands if used.get(x, 0) == m])
            used[pick] = used.get(pick, 0) + 1
            sh = lib[pick]
            slen = sh["b"] - sh["a"]
            want = rng.uniform(1.0, 1.6)
            dur = min(slen, want)
            n = max(10, int(dur * FPS))
            if f1 - (f + n) < 12:  # no dejar un trocito final minúsculo
                n = f1 - f
            n = min(n, f1 - f)
            off = rng.uniform(0, max(0, slen - n / FPS))
            pieces.append((f, n, pick, sh["a"] + off))
            prev = pick
            f += n
    return pieces


class PieceReader:
    """Decodifica un plano ya recortado a 9:16 y escalado a 1080x1920."""

    def __init__(self, shot_id, src, n):
        sh = shots()[shot_id]
        clip = sh["clip"]
        x = XPOS.get(shot_id, 0.5)
        vf = []
        if clip in ROTATE:
            vf.append(ROTATE[clip])
        vf += [f"crop=trunc(ih*9/16/2)*2:ih:(iw-ow)*{x}:0",
               "scale=1080:1920:flags=bicubic",
               "eq=contrast=1.07:saturation=1.2:brightness=-0.015",
               "unsharp=5:5:0.6", "fps=30", "tpad=stop_mode=clone:stop_duration=3"]
        cmd = ["ffmpeg", "-v", "error", "-ss", f"{src:.3f}", "-i", os.path.join(CLIPS_DIR, clip + ".mp4"),
               "-an", "-vf", ",".join(vf), "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self.last = None

    def frame(self):
        buf = self.p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            self.last = Image.frombuffer("RGB", (W, H), buf)
        return self.last.copy() if self.last else Image.new("RGB", (W, H))

    def close(self):
        self.p.stdout.close()
        self.p.wait()


@functools.lru_cache(maxsize=1)
def shade():
    """Degradados oscuros arriba y abajo para que se lean los textos."""
    g = Image.new("L", (1, H))
    for y in range(H):
        top = clamp(1 - y / 620) ** 1.6 * 150
        bot = clamp((y - 1150) / 770) ** 1.4 * 190
        g.putpixel((0, y), int(max(top, bot)))
    return g.resize((W, H))


def background(raw, k, n, is_scene_start):
    """Zoom de empuje continuo + golpe de zoom en cada corte."""
    p = k / max(1, n - 1)
    z = 1.0 + 0.07 * p
    z += 0.10 * (1 - ease_out_cubic(k / 6)) if k < 6 else 0
    if is_scene_start and k < 8:
        z += 0.06 * (1 - k / 8)
    cw, ch = W / z, H / z
    x0, y0 = (W - cw) / 2, (H - ch) / 2
    img = raw.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)
    img.paste((0, 0, 0), (0, 0, W, H), shade())
    return img


# ----------------------------------------------------------------- piezas del HUD
@functools.lru_cache(maxsize=128)
def hud_panel(w, h, border=GREEN):
    pad = 30
    img = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle((pad, pad, pad + w, pad + h), radius=28,
                                           outline=border + (255,), width=10)
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((pad, pad, pad + w, pad + h), radius=28, fill=NAVY + (225,),
                        outline=border + (255,), width=5)
    # brillo superior
    d.rounded_rectangle((pad + 14, pad + 10, pad + w - 14, pad + 16), radius=3, fill=(255, 255, 255, 28))
    return img


@functools.lru_cache(maxsize=128)
def header_img(label, num):
    lab = text_img(label.upper(), 66, "dblacki", BLACK, (40, 120, 40), 800, 0, BLACK, False, 1)
    plate = Image.new("RGBA", (lab.width + 30, lab.height + 6), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle((0, 0, plate.width - 1, plate.height - 1), radius=14,
                                            fill=(250, 250, 250, 255))
    plate.paste(lab, (15, 3), lab)
    parts = []
    if num:
        sq = Image.new("RGBA", (plate.height, plate.height), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sq)
        sd.rounded_rectangle((0, 0, sq.width - 1, sq.height - 1), radius=14, fill=GREEN + (255,),
                             outline=(20, 60, 20, 255), width=4)
        sd.text((sq.width / 2, sq.height / 2 + 4), str(num), font=font("dblacki", int(sq.height * 0.66)),
                fill=BLACK, anchor="mm")
        parts.append(sq)
    parts.append(plate)
    gap = 16
    w = sum(p.width for p in parts) + gap * (len(parts) - 1)
    h = max(p.height for p in parts)
    img = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    x = 10
    for p in parts:
        img.paste(p, (x, 10 + (h - p.height) // 2), p)
        x += p.width + gap
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(8)).point(lambda v: v * 0.6))
    out = Image.new("RGBA", (img.width + 12, img.height + 12), (0, 0, 0, 0))
    out.paste(sh, (8, 10), sh)
    out.paste(img, (0, 0), img)
    return out


def header(c, t, label, num=None, y=HEADER_Y):
    img = header_img(label, num)
    p = ease_out_back(t / 0.35, 1.6)
    x = lerp(-img.width, W / 2, p)
    put(c, img, x, y, rot=-2.5, scale=lerp(0.8, 1.0, clamp(t / 0.25)))


def hud_in(t, delay=0.15):
    a = ease_out_cubic((t - delay) / 0.25)
    s = lerp(0.85, 1.0, ease_out_back((t - delay) / 0.35, 2.2))
    return a, s


def compose(panel, items):
    """Pega imágenes (img, x, y centrados) sobre una copia del panel."""
    out = panel.copy()
    for img, x, y in items:
        out.paste(img, (int(x - img.width / 2), int(y - img.height / 2)), img)
    return out


# ----------------------------------------------------------------- escenas
def s_title(c, t, d, v):
    lines = v["lines"]
    for i, ln in enumerate(lines):
        s = ease_out_back((t - i * 0.12) / 0.35, 2.2)
        col = WHITE if i % 2 == 0 else GREEN
        img = text_img(ln, 128, "dblacki", col, GREEN, 1000, 10, BLACK, True, 1)
        put(c, img, W / 2, 380 + i * 150, scale=s * (1 + 0.015 * math.sin(t * 4)), rot=-2.5)
    if v.get("sub"):
        a, s = hud_in(t, 0.45)
        put(c, header_img(v["sub"], None), W / 2, 380 + len(lines) * 150 + 30, alpha=a, scale=s, rot=-2.5)


def s_year(c, t, d, v):
    header(c, t, v.get("tag") or v["year"])
    yr = text_img(v["year"], 190, "dblacki", GREEN, GREEN, 800, 8, BLACK, False, 1)
    items, hgt = [(yr, 0, 0)], yr.height
    if v.get("head"):
        hd = text_img(v["head"], 66, "dblacki", WHITE, GREEN, 780, 4, BLACK, False, 2)
        items.append((hd, 0, hgt))
        hgt += hd.height
    if v.get("label"):
        lb = text_img(v["label"], 44, "black", (190, 255, 195), GREEN, 780, 0, BLACK, False, 2)
        items.append((lb, 0, hgt + 6))
        hgt += lb.height + 6
    pw, ph = 880, hgt + 40
    panel = hud_panel(pw, ph)
    img = compose(panel, [(im, panel.width / 2, 30 + 20 + y + im.height / 2) for im, _, y in items])
    a, s = hud_in(t)
    put(c, img, W / 2, HUD_Y, alpha=a, scale=s)


def s_counter(c, t, d, v):
    header(c, t, v.get("tag", ""))
    val = v["value"]
    dur = min(1.6, d * 0.5)
    p = ease_out_cubic((t - 0.15) / dur)
    pre = v.get("prefix", "")
    final = pre + fmt_num(val)
    size = 150
    while font("dblacki", size).getlength(final) > 820 and size > 50:
        size -= 6
    num = text_img(pre + fmt_num(val * p), size, "dblacki", WHITE, GREEN, 900, 6, BLACK, False, 1)
    lb = text_img(v.get("label", ""), 46, "black", GREEN, GREEN, 800, 0, BLACK, False, 2)
    pw, ph = 900, 60 + int(size * 1.25) + lb.height
    panel = hud_panel(pw, ph)
    img = compose(panel, [(num, panel.width / 2, 30 + 30 + size * 0.62),
                          (lb, panel.width / 2, 30 + ph - 20 - lb.height / 2)])
    a, s = hud_in(t)
    pulse = 1 + (0.06 * math.exp(-(t - 0.15 - dur) * 8) if t > 0.15 + dur else 0)
    put(c, img, W / 2, HUD_Y, alpha=a, scale=s * pulse)


@functools.lru_cache(maxsize=64)
def vs_card(head, body, border):
    hd = text_img(head, 120, "dblacki", GREEN if border == GREEN else (255, 214, 0), GREEN, 380, 6, BLACK, False, 1)
    bd = text_img(body, 48, "black", WHITE, GREEN, 380, 0, BLACK, False, 3)
    panel = hud_panel(420, 330, border)
    return compose(panel, [(hd, panel.width / 2, 30 + 105), (bd, panel.width / 2, 30 + 245)])


def s_versus(c, t, d, v):
    header(c, t, v.get("title", ""))
    L, Rr = v["left"], v["right"]
    lp = vs_card(L["head"], L["body"], (120, 160, 255))
    rp = vs_card(Rr["head"], Rr["body"], GREEN)
    pl = ease_out_back((t - 0.1) / 0.4, 1.4)
    pr = ease_out_back((t - 0.25) / 0.4, 1.4)
    put(c, lp, lerp(-300, 290, pl), HUD_Y)
    put(c, rp, lerp(W + 300, 790, pr), HUD_Y)
    s = ease_out_back((t - 0.5) / 0.3, 3)
    put(c, R.vs_badge(), W / 2, HUD_Y, scale=s * 0.8, rot=8 * math.sin(t * 5) * math.exp(-max(0, t - 0.5) * 2))


def s_pairs(c, t, d, v):
    header(c, t, v["title"])
    rows = v["rows"]
    times = _steps(len(rows), d, 0.25)
    rh = 105
    pw, ph = 940, rh * len(rows) + 30
    panel = hud_panel(pw, ph).copy()
    for i, (a_, b_) in enumerate(rows):
        if t < times[i]:
            continue
        al = text_img(a_, 52, "dblacki", GREEN, GREEN, 400, 0, BLACK, False, 1, "right")
        ar = text_img("→", 52, "black", WHITE, WHITE, 80, 0, BLACK, False, 1)
        bl = text_img(b_, 52, "dblacki", WHITE, GREEN, 400, 0, BLACK, False, 1, "left")
        k = ease_out_cubic((t - times[i]) / 0.25)
        y = 30 + 15 + i * rh + rh / 2
        dx = int(60 * (1 - k))
        panel.paste(al, (int(30 + 430 - al.width + dx), int(y - al.height / 2)), al)
        panel.paste(ar, (int(30 + pw / 2 - ar.width / 2 + dx), int(y - ar.height / 2)), ar)
        panel.paste(bl, (int(30 + 530 + dx), int(y - bl.height / 2)), bl)
    a, s = hud_in(t)
    put(c, panel, W / 2, HUD_Y, alpha=a, scale=s)


def s_bars(c, t, d, v):
    header(c, t, v["title"])
    rows = v["rows"]
    n = len(rows)
    vmax = max(r[1] for r in rows)
    times = _steps(n, d, 0.25, 0.7)
    rh = 82 if n > 3 else 110
    pw, ph = 940, rh * n + 40
    panel = hud_panel(pw, ph).copy()
    dd = ImageDraw.Draw(panel)
    x0, maxw = 30 + 270, 520
    for i, (label, val, disp) in enumerate(rows):
        y = 30 + 20 + i * rh + rh / 2
        lb = text_img(label, 40, "dblacki", WHITE, GREEN, 240, 0, BLACK, False, 1, "right")
        panel.paste(lb, (int(x0 - 20 - lb.width), int(y - lb.height / 2)), lb)
        dd.rounded_rectangle((x0, y - 20, x0 + maxw, y + 20), radius=20, fill=(40, 48, 66, 255))
        g = ease_out_cubic((t - times[i]) / 0.7)
        if g > 0:
            last = i == n - 1
            bw = max(40, int(maxw * val / vmax * g))
            col = RED if last else GREEN
            dd.rounded_rectangle((x0, y - 20, x0 + bw, y + 20), radius=20, fill=col + (255,))
            dd.rounded_rectangle((x0 + 10, y - 14, x0 + bw - 10, y - 8), radius=3, fill=(255, 255, 255, 90))
            vi = text_img(disp, 44, "dblacki", WHITE, GREEN, 140, 0, BLACK, False, 1)
            panel.paste(vi, (int(min(x0 + bw + 12, x0 + maxw + 12)), int(y - vi.height / 2)), vi)
    a, s = hud_in(t)
    put(c, panel, W / 2, HUD_Y, alpha=a, scale=s)


def s_strike(c, t, d, v):
    header(c, t, v["title"])
    items = v["items"]
    times = _steps(len(items), d, 0.25, 0.75)
    rh = 110
    pw, ph = 900, rh * len(items) + 30
    panel = hud_panel(pw, ph).copy()
    dd = ImageDraw.Draw(panel)
    for i, (txt, struck) in enumerate(items):
        if t < times[i]:
            continue
        y = 30 + 15 + i * rh + rh / 2
        col = (200, 200, 210) if struck else GREEN
        ti = text_img(txt + ("" if struck else "  ✓"), 70, "dblacki", col, GREEN, 820, 0, BLACK, False, 1)
        panel.paste(ti, (int(30 + pw / 2 - ti.width / 2), int(y - ti.height / 2)), ti)
        if struck:
            sp = ease_out_cubic((t - times[i] - 0.35) / 0.3)
            if sp > 0:
                x1 = 30 + pw / 2 - ti.width / 2 + 10
                dd.rounded_rectangle((x1, y - 7, x1 + (ti.width - 20) * sp, y + 7), radius=7, fill=RED + (255,))
    a, s = hud_in(t)
    put(c, panel, W / 2, HUD_Y, alpha=a, scale=s)


def s_facts(c, t, d, v):
    header(c, t, v["head"], v.get("num"))
    ic = icon(v.get("icon", "star"), (255, 214, 0), GREEN).resize((190, 190), Image.LANCZOS)
    body = text_img(v["body"], 50, "black", WHITE, GREEN, 600, 0, BLACK, False, 3, "left")
    pw = 920
    ph = max(200, body.height + 60)
    panel = hud_panel(pw, ph)
    bob = int(6 * math.sin(t * 3))
    img = compose(panel, [(ic, 30 + 120, 30 + ph / 2 + bob)])
    img.paste(body, (30 + 235, int(30 + ph / 2 - body.height / 2)), body)
    a, s = hud_in(t, 0.2)
    put(c, img, W / 2, HUD_Y, alpha=a, scale=s)


def s_outro(c, t, d, v):
    q = text_img(v["q"].replace("*", ""), 92, "dblacki", WHITE, GREEN, 960, 9, BLACK, True, 3)
    put(c, q, W / 2, 420, scale=ease_out_back(t / 0.4, 2) * (1 + 0.015 * math.sin(t * 4)), rot=-2.5)
    clicked = t > 1.5
    s = ease_out_back((t - 0.35) / 0.35)
    col = (70, 70, 80) if clicked else RED
    label = "SUSCRITO ✓" if clicked else "SUSCRÍBETE"
    btn = R.panel_img(640, 150, col + (255,), 75).copy()
    li = text_img(label, 74, "dblacki", WHITE, WHITE, 600, 0, BLACK, False, 1)
    btn.paste(li, ((btn.width - li.width) // 2, (btn.height - li.height) // 2), li)
    press = 0.92 if 1.35 < t < 1.5 else 1.0
    put(c, btn, W / 2, HUD_Y, scale=s * press * (1 + (0.04 * math.sin(t * 7) if not clicked else 0)))
    if 0.9 < t < 2.0:
        ct = ease_out_cubic((t - 0.9) / 0.45)
        cx, cy = lerp(W + 100, W / 2 + 150, ct), lerp(1450, 1200, ct)
        hand = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
        ImageDraw.Draw(hand).ellipse((5, 5, 85, 85), fill=(255, 255, 255, 230), outline=BLACK, width=5)
        put(c, hand, cx, cy)
        if t > 1.4:
            rp = clamp((t - 1.4) / 0.4)
            ring = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
            ImageDraw.Draw(ring).ellipse((10, 10, 290, 290), outline=(255, 255, 255, 255), width=10)
            put(c, ring, cx, cy, scale=0.3 + rp, alpha=1 - rp)


SCENES = dict(title=s_title, year=s_year, counter=s_counter, versus=s_versus, pairs=s_pairs,
              bars=s_bars, strike=s_strike, facts=s_facts, outro=s_outro)


def caption(c, t, words, times, chunks, scene_end):
    for ci, ch in enumerate(chunks):
        start = times[ch[0]]
        end = times[chunks[ci + 1][0]] if ci + 1 < len(chunks) else scene_end
        if start <= t < end:
            cur = ch[0]
            for j in ch:
                if times[j] <= t:
                    cur = j
            parts = ["*" + words[j].upper() + "*" if j == cur else words[j].upper() for j in ch]
            img = text_img(" ".join(parts), 78, "dblacki", WHITE, GREEN, 900, 8, BLACK, True, 2)
            pop = 1 + 0.14 * (1 - ease_out_cubic((t - start) / 0.12))
            put(c, img, W / 2, CAP_Y, scale=pop)
            return
