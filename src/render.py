# -*- coding: utf-8 -*-
"""Motor de render de Shorts: fondo animado synthwave + motion graphics + subtítulos."""
import functools
import math
import random
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
HORIZON = 1180
FONT_DIR = "/usr/share/fonts/opentype/inter/"
FONTS = {
    "black": FONT_DIR + "Inter-Black.otf",
    "xbold": FONT_DIR + "Inter-ExtraBold.otf",
    "bold": FONT_DIR + "Inter-Bold.otf",
    "dblack": FONT_DIR + "InterDisplay-Black.otf",
    "dblacki": FONT_DIR + "InterDisplay-BlackItalic.otf",
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 35, 60)
GREEN = (60, 230, 120)
BRAND = "CURIOSIDADES GTA"

THEMES = {
    "vice": dict(sky=[(18, 4, 44), (110, 18, 110), (255, 92, 140)], sun=[(255, 225, 90), (255, 50, 150)],
                 grid=(255, 60, 200), acc=(255, 214, 0), acc2=(0, 230, 255), mount=(40, 8, 70)),
    "sunset": dict(sky=[(24, 6, 30), (140, 28, 60), (255, 140, 60)], sun=[(255, 240, 130), (255, 70, 50)],
                   grid=(255, 120, 60), acc=(255, 214, 0), acc2=(255, 110, 160), mount=(50, 10, 40)),
    "night": dict(sky=[(4, 4, 22), (26, 20, 86), (96, 50, 190)], sun=[(150, 235, 255), (130, 80, 255)],
                  grid=(90, 150, 255), acc=(0, 230, 255), acc2=(255, 80, 200), mount=(14, 10, 50)),
    "leonida": dict(sky=[(3, 26, 38), (8, 100, 115), (250, 170, 90)], sun=[(255, 236, 140), (255, 110, 90)],
                    grid=(0, 255, 200), acc=(255, 214, 0), acc2=(0, 255, 190), mount=(4, 40, 50)),
    "gold": dict(sky=[(20, 10, 4), (105, 55, 10), (255, 175, 60)], sun=[(255, 250, 190), (255, 140, 30)],
                 grid=(255, 190, 60), acc=(255, 220, 40), acc2=(120, 255, 200), mount=(40, 20, 6)),
}


# ----------------------------------------------------------------- utilidades
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease_out_cubic(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_out_back(t, s=1.9):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def ease_in_out(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


@functools.lru_cache(maxsize=256)
def font(name, size):
    return ImageFont.truetype(FONTS[name], size)


def parse_rich(text, base, acc):
    toks = []
    hl = False
    for part in re.split(r"(\*)", text):
        if part == "*":
            hl = not hl
            continue
        for i, seg in enumerate(part.split("\n")):
            if i > 0:
                toks.append(("\n", None))
            for w in seg.split(" "):
                if w:
                    toks.append((w, acc if hl else base))
    return toks


def layout(toks, f, max_w):
    space = f.getlength(" ")
    lines, cur, cw = [], [], 0.0
    for w, c in toks:
        if w == "\n":
            lines.append(cur)
            cur, cw = [], 0.0
            continue
        ww = f.getlength(w)
        if cur and cw + space + ww > max_w:
            lines.append(cur)
            cur, cw = [], 0.0
        cur.append((w, c, ww))
        cw += (space if len(cur) > 1 else 0) + ww
    if cur:
        lines.append(cur)
    widths = [sum(x[2] for x in ln) + space * (len(ln) - 1) for ln in lines]
    return lines, widths, space


@functools.lru_cache(maxsize=2048)
def text_img(text, size, fname="black", color=WHITE, acc=(255, 214, 0), max_w=960, stroke=0,
             stroke_color=BLACK, shadow=True, max_lines=4, align="center", lh=1.12):
    toks = parse_rich(text, color, acc)
    while True:
        f = font(fname, size)
        lines, widths, space = layout(toks, f, max_w)
        if (max(widths or [0]) <= max_w and len(lines) <= max_lines) or size <= 24:
            break
        size = int(size * 0.92)
    asc, desc = f.getmetrics()
    line_h = int(size * lh)
    pad = stroke + int(size * 0.18) + 6
    iw = int(max(widths or [1])) + 2 * pad
    ih = line_h * len(lines) + (asc + desc - line_h if asc + desc > line_h else 0) + 2 * pad
    img = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))

    def draw_all(d, override=None, off=(0, 0), sw=stroke):
        for li, ln in enumerate(lines):
            lw = widths[li]
            x = pad + (0 if align == "left" else (iw - 2 * pad - lw) / 2 if align == "center" else iw - 2 * pad - lw)
            y = pad + li * line_h
            for w, c, ww in ln:
                d.text((x + off[0], y + off[1]), w, font=f, fill=override or c,
                       stroke_width=sw, stroke_fill=override or stroke_color)
                x += ww + space

    if shadow:
        sh = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
        draw_all(ImageDraw.Draw(sh), override=(0, 0, 0, 170), off=(0, int(size * 0.07)), sw=stroke + 2)
        sh = sh.filter(ImageFilter.GaussianBlur(max(2, size * 0.05)))
        img = Image.alpha_composite(img, sh)
    draw_all(ImageDraw.Draw(img))
    return img


@functools.lru_cache(maxsize=256)
def panel_img(w, h, fill=(0, 0, 0, 160), radius=36, outline=None, width=6):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=fill,
                        outline=outline, width=width if outline else 0)
    return img


class Ctx:
    """Estado de cámara (temblor) compartido por los elementos de un frame."""
    ox = 0
    oy = 0


def put(canvas, img, cx, cy, scale=1.0, alpha=1.0, rot=0.0, anchor="center"):
    if alpha <= 0.01 or scale <= 0.01:
        return
    if rot:
        img = img.rotate(rot, resample=Image.BICUBIC, expand=True)
    if abs(scale - 1) > 0.004:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BILINEAR)
    if alpha < 0.995:
        a = img.getchannel("A").point(lambda v: int(v * alpha))
        img = img.copy()
        img.putalpha(a)
    if anchor == "center":
        x, y = cx - img.width / 2, cy - img.height / 2
    elif anchor == "left":
        x, y = cx, cy - img.height / 2
    else:  # right
        x, y = cx - img.width, cy - img.height / 2
    canvas.paste(img, (int(x + Ctx.ox), int(y + Ctx.oy)), img)


# ----------------------------------------------------------------- iconos
def _ss(draw_fn, size=380, glow=None):
    S = size * 2
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(img), S, img)
    img = img.resize((size, size), Image.LANCZOS)
    if glow:
        g = Image.new("RGBA", img.size, glow + (0,))
        g.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(18)))
        base = Image.new("RGBA", (size + 80, size + 80), (0, 0, 0, 0))
        base.paste(g, (40, 40), g)
        base.paste(g, (40, 40), g)
        base.paste(img, (40, 40), img)
        return base
    return img


@functools.lru_cache(maxsize=64)
def icon(name, acc, acc2):
    O = (10, 10, 20, 255)

    def warning(d, S, im):
        d.polygon([(S / 2, S * .08), (S * .95, S * .88), (S * .05, S * .88)], fill=acc + (255,), outline=O, width=int(S * .03))
        d.rounded_rectangle((S * .46, S * .33, S * .54, S * .66), radius=S * .03, fill=O)
        d.ellipse((S * .455, S * .71, S * .545, S * .80), fill=O)

    def star(d, S, im):
        pts = []
        for i in range(10):
            r = S * (.46 if i % 2 == 0 else .2)
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((S / 2 + r * math.cos(a), S * .53 + r * math.sin(a)))
        d.polygon(pts, fill=acc + (255,), outline=O, width=int(S * .025))

    def heart(d, S, im):
        r = S * .23
        d.ellipse((S * .07, S * .15, S * .07 + 2 * r, S * .15 + 2 * r), fill=RED + (255,))
        d.ellipse((S * .93 - 2 * r, S * .15, S * .93, S * .15 + 2 * r), fill=RED + (255,))
        d.polygon([(S * .09, S * .47), (S * .91, S * .47), (S / 2, S * .92)], fill=RED + (255,))
        d.ellipse((S * .2, S * .25, S * .33, S * .36), fill=(255, 150, 160, 255))
        # cadenas
        for k in range(6):
            x = S * .05 + k * S * .17
            d.ellipse((x, S * .55, x + S * .16, S * .64), outline=(200, 200, 210, 255), width=int(S * .02))

    def dollar(d, S, im):
        d.ellipse((S * .06, S * .06, S * .94, S * .94), fill=(40, 190, 90, 255), outline=O, width=int(S * .03))
        d.ellipse((S * .14, S * .14, S * .86, S * .86), outline=(170, 255, 190, 255), width=int(S * .02))
        f = font("black", int(S * .6))
        d.text((S / 2, S / 2 + S * .02), "$", font=f, fill=WHITE, anchor="mm")

    def trophy(d, S, im):
        g = acc + (255,)
        d.ellipse((S * .08, S * .14, S * .34, S * .44), outline=g, width=int(S * .05))
        d.ellipse((S * .66, S * .14, S * .92, S * .44), outline=g, width=int(S * .05))
        d.polygon([(S * .22, S * .1), (S * .78, S * .1), (S * .7, S * .5), (S * .3, S * .5)], fill=g)
        d.chord((S * .22, S * .2, S * .78, S * .66), 0, 180, fill=g)
        d.rectangle((S * .45, S * .6, S * .55, S * .76), fill=g)
        d.rounded_rectangle((S * .28, S * .76, S * .72, S * .9), radius=S * .03, fill=g)
        d.text((S / 2, S * .33), "1", font=font("black", int(S * .22)), fill=O, anchor="mm")

    def crown(d, S, im):
        g = acc + (255,)
        d.polygon([(S * .08, S * .78), (S * .08, S * .3), (S * .3, S * .52), (S * .5, S * .2),
                   (S * .7, S * .52), (S * .92, S * .3), (S * .92, S * .78)], fill=g, outline=O, width=int(S * .02))
        for x, y in [(.08, .27), (.5, .17), (.92, .27)]:
            d.ellipse((S * x - S * .05, S * y - S * .05, S * x + S * .05, S * y + S * .05), fill=RED + (255,))
        d.rectangle((S * .08, S * .7, S * .92, S * .8), fill=mix(acc, BLACK, .3) + (255,))

    def mountain(d, S, im):
        d.polygon([(S * .02, S * .88), (S * .4, S * .18), (S * .78, S * .88)], fill=(90, 100, 130, 255))
        d.polygon([(S * .35, S * .88), (S * .68, S * .38), (S * .98, S * .88)], fill=(60, 70, 100, 255))
        d.polygon([(S * .4, S * .18), (S * .3, S * .36), (S * .37, S * .33), (S * .43, S * .38), (S * .5, S * .36)], fill=WHITE)
        d.line([(S * .02, S * .88), (S * .4, S * .18), (S * .78, S * .88)], fill=acc2 + (255,), width=int(S * .02))

    def ufo(d, S, im):
        d.polygon([(S * .35, S * .55), (S * .65, S * .55), (S * .9, S * .98), (S * .1, S * .98)], fill=acc2 + (90,))
        d.ellipse((S * .3, S * .18, S * .7, S * .5), fill=(170, 240, 255, 220), outline=O, width=int(S * .02))
        d.ellipse((S * .04, S * .36, S * .96, S * .62), fill=(150, 160, 180, 255), outline=O, width=int(S * .025))
        for k in range(5):
            x = S * (.18 + k * .16)
            d.ellipse((x - S * .035, S * .46, x + S * .035, S * .53), fill=acc + (255,))

    def pin(d, S, im):
        d.ellipse((S * .18, S * .05, S * .82, S * .69), fill=RED + (255,), outline=O, width=int(S * .025))
        d.polygon([(S * .25, S * .5), (S * .75, S * .5), (S * .5, S * .97)], fill=RED + (255,))
        d.ellipse((S * .36, S * .23, S * .64, S * .51), fill=WHITE)

    def gamepad(d, S, im):
        d.rounded_rectangle((S * .04, S * .25, S * .96, S * .75), radius=S * .2, fill=(40, 40, 55, 255), outline=acc2 + (255,), width=int(S * .025))
        d.rectangle((S * .17, S * .45, S * .37, S * .55), fill=WHITE)
        d.rectangle((S * .22, S * .4, S * .32, S * .6), fill=WHITE)
        for (x, y, c) in [(.7, .4, acc), (.8, .5, RED), (.6, .5, acc2), (.7, .6, GREEN)]:
            d.ellipse((S * x - S * .045, S * y - S * .045, S * x + S * .045, S * y + S * .045), fill=c + (255,))

    def clock(d, S, im):
        d.ellipse((S * .06, S * .06, S * .94, S * .94), fill=WHITE, outline=acc2 + (255,), width=int(S * .05))
        for k in range(12):
            a = k * math.pi / 6
            d.line([(S / 2 + S * .36 * math.cos(a), S / 2 + S * .36 * math.sin(a)),
                    (S / 2 + S * .41 * math.cos(a), S / 2 + S * .41 * math.sin(a))], fill=O, width=int(S * .02))
        d.line([(S / 2, S / 2), (S / 2, S * .2)], fill=O, width=int(S * .035))
        d.line([(S / 2, S / 2), (S * .72, S * .6)], fill=RED + (255,), width=int(S * .03))
        d.ellipse((S * .46, S * .46, S * .54, S * .54), fill=O)

    def skull(d, S, im):
        d.ellipse((S * .14, S * .06, S * .86, S * .7), fill=(235, 235, 240, 255))
        d.rounded_rectangle((S * .3, S * .55, S * .7, S * .9), radius=S * .06, fill=(235, 235, 240, 255))
        d.ellipse((S * .26, S * .32, S * .44, S * .52), fill=O)
        d.ellipse((S * .56, S * .32, S * .74, S * .52), fill=O)
        d.polygon([(S * .5, S * .56), (S * .45, S * .66), (S * .55, S * .66)], fill=O)
        for k in range(4):
            x = S * (.36 + k * .09)
            d.line([(x, S * .76), (x, S * .9)], fill=O, width=int(S * .02))

    def play(d, S, im):
        d.rounded_rectangle((S * .06, S * .18, S * .94, S * .76), radius=S * .06, fill=(30, 30, 40, 255), outline=acc2 + (255,), width=int(S * .03))
        d.polygon([(S * .42, S * .32), (S * .42, S * .62), (S * .66, S * .47)], fill=acc + (255,))
        d.rectangle((S * .36, S * .76, S * .64, S * .84), fill=(80, 80, 90, 255))
        d.line([(S * .3, S * .18), (S * .2, S * .04)], fill=WHITE, width=int(S * .02))
        d.line([(S * .7, S * .18), (S * .8, S * .04)], fill=WHITE, width=int(S * .02))

    fns = dict(warning=warning, star=star, heart=heart, dollar=dollar, trophy=trophy, crown=crown,
               mountain=mountain, ufo=ufo, pin=pin, gamepad=gamepad, clock=clock, skull=skull, play=play)
    return _ss(fns[name], 360, glow=acc2)


# ----------------------------------------------------------------- fondo
def _palm(d, x, base_y, h, lean, color):
    pts_l, pts_r = [], []
    for i in range(21):
        t = i / 20
        cx = x + lean * t * t * h
        cy = base_y - t * h
        wdt = lerp(26, 12, t)
        pts_l.append((cx - wdt, cy))
        pts_r.append((cx + wdt, cy))
    d.polygon(pts_l + pts_r[::-1], fill=color)
    tx, ty = x + lean * h, base_y - h
    for k in range(9):
        a = -math.pi + k * (math.pi / 8) + 0.1 * math.sin(k * 3)
        L = h * 0.45
        pts = []
        for j in range(16):
            s = j / 15
            px = tx + math.cos(a) * L * s
            py = ty + math.sin(a) * L * s + (s * s) * L * 0.55
            pts.append((px, py))
        upper = [(px, py - 16 * math.sin(math.pi * j / 15)) for j, (px, py) in enumerate(pts)]
        lower = [(px, py + 16 * math.sin(math.pi * j / 15)) for j, (px, py) in enumerate(pts)]
        d.polygon(upper + lower[::-1], fill=color)


@functools.lru_cache(maxsize=8)
def background(theme_name):
    th = THEMES[theme_name]
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    s0, s1, s2 = th["sky"]
    for y in range(HORIZON):
        t = y / HORIZON
        c = mix(s0, s1, t / 0.6) if t < 0.6 else mix(s1, s2, (t - 0.6) / 0.4)
        d.line([(0, y), (W, y)], fill=c)
    rnd = random.Random(7)
    for _ in range(140):
        x, y = rnd.randrange(W), rnd.randrange(int(HORIZON * 0.55))
        r = rnd.choice([1, 1, 2, 2, 3])
        b = rnd.randrange(120, 255)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(b, b, b))
    # sol con franjas
    R, cx, cy = 330, W // 2, HORIZON - 150
    sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    for y in range(cy - R, cy + R):
        t = (y - (cy - R)) / (2 * R)
        dx = math.sqrt(max(0, R * R - (y - cy) ** 2))
        sd.line([(cx - dx, y), (cx + dx, y)], fill=mix(th["sun"][0], th["sun"][1], t) + (255,))
    for k in range(9):
        yy = cy - 20 + k * 30
        hh = 4 + k * 2.2
        sd.rectangle((0, yy, W, yy + hh), fill=(0, 0, 0, 0))
    glow = sun.filter(ImageFilter.GaussianBlur(60))
    img.paste(glow, (0, 0), glow)
    img.paste(sun, (0, 0), sun)
    # montañas
    m = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(m)
    pts = [(0, HORIZON)]
    rnd = random.Random(3)
    x = 0
    while x < W:
        x += rnd.randrange(60, 140)
        pts.append((x, HORIZON - rnd.randrange(40, 230) * (0.4 if 300 < x < 780 else 1)))
    pts.append((W, HORIZON))
    md.polygon(pts, fill=th["mount"] + (255,))
    md.line(pts, fill=th["grid"] + (255,), width=3)
    img.paste(m, (0, 0), m)
    # suelo
    d.rectangle((0, HORIZON, W, H), fill=mix(th["mount"], BLACK, 0.6))
    d.line([(0, HORIZON), (W, HORIZON)], fill=th["grid"], width=4)
    # oscurecer + viñeta para legibilidad
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.blend(img, dark, 0.35)
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    for i in range(60):
        a = int(150 * (1 - i / 60) ** 2)
        vd.rectangle((i * 6, i * 9, W - i * 6, H - i * 9), outline=a, width=9)
    img.paste(dark, (0, 0), vig.filter(ImageFilter.GaussianBlur(30)))
    return img


@functools.lru_cache(maxsize=8)
def palms(theme_name):
    th = THEMES[theme_name]
    col = mix(th["mount"], BLACK, 0.75) + (255,)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    _palm(d, 70, H + 20, 820, 0.25, col)
    _palm(d, 190, H + 60, 600, 0.35, col)
    _palm(d, W - 80, H + 20, 760, -0.28, col)
    _palm(d, W - 230, H + 80, 520, -0.2, col)
    return img


def draw_bg(theme_name, t):
    th = THEMES[theme_name]
    img = background(theme_name).copy()
    d = ImageDraw.Draw(img)
    gcol = mix(th["grid"], BLACK, 0.35)
    # líneas horizontales en perspectiva que avanzan
    phase = (t * 0.9) % 1.0
    N = 14
    for k in range(N + 1):
        p = (k + phase) / N
        y = HORIZON + (H - HORIZON) * p ** 2.3
        d.line([(0, y), (W, y)], fill=gcol, width=max(1, int(1 + 4 * p)))
    for j in range(-12, 13):
        d.line([(W / 2 + j * 22, HORIZON), (W / 2 + j * 260, H)], fill=gcol, width=2)
    # partículas
    rnd = random.Random(11)
    for i in range(45):
        x0 = rnd.randrange(W)
        sp = rnd.uniform(20, 70)
        y = (rnd.randrange(H) - t * sp) % H
        x = x0 + 12 * math.sin(t * 0.8 + i)
        r = rnd.choice([2, 3, 4])
        c = mix(th["acc2"], BLACK, rnd.uniform(0.3, 0.7))
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    p = palms(theme_name)
    img.paste(p, (0, 0), p)
    return img


# ----------------------------------------------------------------- escenas
def tag_pill(text, th, size=44):
    ti = text_img(text, size, "black", BLACK, BLACK, 940, 0, BLACK, False, 1)
    pw, ph = ti.width + 40, ti.height + 10
    pill = panel_img(pw, ph, th["acc"] + (255,), ph // 2)
    out = pill.copy()
    out.paste(ti, ((pw - ti.width) // 2, (ph - ti.height) // 2), ti)
    return out


def sc_title(c, t, d, v, th):
    lines = v["lines"]
    n = len(lines)
    gap = 175
    y0 = 800 - (n - 1) * gap / 2
    band_h = n * gap + 120
    band = panel_img(1300, band_h, (0, 0, 0, 170), 0, th["acc2"] + (255,), 8)
    bx = lerp(-1300, W / 2, ease_out_cubic(t / 0.25))
    put(c, band, bx, 800, rot=-4)
    breathe = 1 + 0.018 * math.sin(t * 2 * math.pi * 0.7)
    for i, ln in enumerate(lines):
        s = ease_out_back((t - i * 0.1) / 0.35)
        img = text_img(ln, 150, "dblack", WHITE, th["acc"], 1000, 8, BLACK, True, 1)
        put(c, img, W / 2, y0 + i * gap, scale=s * breathe, rot=-4)
    if v.get("sub"):
        a = ease_out_cubic((t - 0.4) / 0.3)
        img = text_img(v["sub"], 64, "black", th["acc2"], th["acc"], 900, 6)
        put(c, img, W / 2, y0 + n * gap + 60 + 30 * (1 - a), alpha=a)


def sc_year(c, t, d, v, th):
    if v.get("tag"):
        put(c, tag_pill(v["tag"], th), W / 2, 500, scale=ease_out_back(t / 0.3))
    p = ease_out_cubic(t / 0.4)
    img = text_img(v["year"], 300, "dblacki", th["acc"], th["acc"], 1000, 10, BLACK, True, 1)
    put(c, img, lerp(W / 2 + 500, W / 2, p), 730, alpha=p, scale=1 + 0.01 * math.sin(t * 3))
    y = 960
    if v.get("head"):
        s = ease_out_back((t - 0.2) / 0.35)
        img = text_img(v["head"], 104, "dblack", WHITE, th["acc"], 980, 7, BLACK, True, 2)
        put(c, img, W / 2, y, scale=s)
        y += img.height / 2 + 70
    if v.get("label"):
        a = ease_out_cubic((t - 0.4) / 0.35)
        img = text_img(v["label"], 58, "xbold", th["acc2"], th["acc"], 940, 5, BLACK, True, 2)
        put(c, img, W / 2, y + 30 * (1 - a), alpha=a)


def fmt_num(n):
    return f"{int(n):,}".replace(",", ".")


def sc_counter(c, t, d, v, th):
    if v.get("tag"):
        put(c, tag_pill(v["tag"], th), W / 2, 560, scale=ease_out_back(t / 0.3))
    val = v["value"]
    dur = min(1.6, d * 0.5)
    p = ease_out_cubic(t / dur)
    pre = v.get("prefix", "")
    final = pre + fmt_num(val)
    # tamaño fijo calculado con el número final
    size = 200
    while font("dblack", size).getlength(final) > 1000 and size > 60:
        size -= 6
    txt = pre + fmt_num(val * p)
    img = text_img(txt, size, "dblack", WHITE, th["acc"], 1040, 9, BLACK, True, 1)
    pulse = 1 + 0.08 * math.exp(-max(0, t - dur) * 8) * (1 if t > dur else 0)
    put(c, img, W / 2, 780, scale=pulse)
    if v.get("label"):
        a = ease_out_cubic((t - 0.3) / 0.35)
        img = text_img(v["label"], 60, "xbold", th["acc2"], th["acc"], 940, 5, BLACK, True, 2)
        put(c, img, W / 2, 960 + 30 * (1 - a), alpha=a)


@functools.lru_cache(maxsize=64)
def vs_panel(head, body, color, th_name):
    th = THEMES[th_name]
    pw, ph = 480, 640
    base = panel_img(pw, ph, mix(color, BLACK, 0.75) + (220,), 40, color + (255,), 8).copy()
    hi = text_img(head, 170, "dblack", WHITE, th["acc"], 430, 8, BLACK, True, 1)
    bi = text_img(body, 66, "black", color, th["acc"], 430, 5, BLACK, True, 3)
    base.paste(hi, ((pw - hi.width) // 2, int(ph * 0.33 - hi.height / 2)), hi)
    base.paste(bi, ((pw - bi.width) // 2, int(ph * 0.72 - bi.height / 2)), bi)
    return base


@functools.lru_cache(maxsize=4)
def vs_badge():
    S = 200
    img = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((8, 8, 2 * S - 8, 2 * S - 8), fill=RED + (255,), outline=WHITE, width=14)
    d.text((S, S + 6), "VS", font=font("dblacki", 150), fill=WHITE, anchor="mm", stroke_width=6, stroke_fill=BLACK)
    return img.resize((S, S), Image.LANCZOS)


def sc_versus(c, t, d, v, th, th_name):
    if v.get("title"):
        img = text_img(v["title"], 96, "dblack", WHITE, th["acc"], 1000, 7)
        put(c, img, W / 2, 430, scale=ease_out_back(t / 0.3))
    L, R = v["left"], v["right"]
    lp = vs_panel(L["head"], L["body"], th["acc2"], th_name)
    rp = vs_panel(R["head"], R["body"], th["acc"], th_name)
    pl = ease_out_back(t / 0.4, 1.2)
    pr = ease_out_back((t - 0.15) / 0.4, 1.2)
    put(c, lp, lerp(-400, 290, pl), 900, rot=2 * (1 - pl))
    put(c, rp, lerp(W + 400, 790, pr), 900, rot=-2 * (1 - pr))
    s = ease_out_back((t - 0.45) / 0.3, 3)
    put(c, vs_badge(), W / 2, 900, scale=s, rot=8 * math.sin(t * 5) * math.exp(-max(0, t - 0.45) * 2))


def _steps(n, d, start=0.15, frac=0.78):
    span = max(0.35, (d * frac - start) / max(1, n))
    return [start + i * span for i in range(n)]


@functools.lru_cache(maxsize=128)
def pair_row(a, b, th_name):
    th = THEMES[th_name]
    pw, ph = 1000, 160
    base = panel_img(pw, ph, (0, 0, 0, 175), 30, th["acc2"] + (255,), 5).copy()
    ai = text_img(a, 64, "black", th["acc"], th["acc"], 400, 5, BLACK, True, 1, "right")
    bi = text_img(b, 64, "black", WHITE, th["acc"], 400, 5, BLACK, True, 1, "left")
    ar = text_img("→", 70, "black", th["acc2"], th["acc2"], 100, 4, BLACK, False, 1)
    base.paste(ai, (int(450 - ai.width), (ph - ai.height) // 2), ai)
    base.paste(ar, (int(pw / 2 - ar.width / 2), (ph - ar.height) // 2), ar)
    base.paste(bi, (550, (ph - bi.height) // 2), bi)
    return base


def sc_pairs(c, t, d, v, th, th_name):
    img = text_img(v["title"], 96, "dblack", WHITE, th["acc"], 1000, 7)
    put(c, img, W / 2, 430, scale=ease_out_back(t / 0.3))
    rows = v["rows"]
    times = _steps(len(rows), d)
    y0 = 620 if len(rows) >= 3 else 720
    for i, (a, b) in enumerate(rows):
        p = ease_out_back((t - times[i]) / 0.4, 1.3)
        if t < times[i]:
            continue
        put(c, pair_row(a, b, th_name), lerp(W + 600, W / 2, p), y0 + i * 200)


def sc_bars(c, t, d, v, th):
    img = text_img(v["title"], 90, "dblack", WHITE, th["acc"], 1000, 7)
    put(c, img, W / 2, 430, scale=ease_out_back(t / 0.3))
    rows = v["rows"]
    n = len(rows)
    vmax = max(r[1] for r in rows)
    times = _steps(n, d, 0.2, 0.7)
    rh = 150 if n > 3 else 200
    y0 = 580 if n > 3 else 700
    x0, maxw = 360, 560
    for i, (label, val, disp) in enumerate(rows):
        y = y0 + i * rh
        a = ease_out_cubic((t - times[i]) / 0.25)
        if a <= 0:
            continue
        li = text_img(label, 54, "black", WHITE, th["acc"], 290, 5, BLACK, True, 1, "right")
        put(c, li, x0 - 25, y, alpha=a, anchor="right")
        g = ease_out_cubic((t - times[i]) / 0.7)
        bw = max(8, int(maxw * val / vmax * g))
        last = i == n - 1
        col = RED if last else th["acc2"]
        bar = panel_img(bw, 96, col + (255,), 20, WHITE + (255,), 4)
        put(c, bar, x0, y, anchor="left")
        vi = text_img(disp, 64 if not last else 76, "dblack", th["acc"] if last else WHITE, th["acc"], 300, 6)
        put(c, vi, x0 + bw + 20, y, alpha=a, anchor="left",
            scale=1 + (0.15 * math.sin(t * 6) if last and g >= 1 else 0))


def sc_strike(c, t, d, v, th):
    img = text_img(v["title"], 96, "dblack", WHITE, th["acc"], 1000, 7)
    put(c, img, W / 2, 430, scale=ease_out_back(t / 0.3))
    items = v["items"]
    times = _steps(len(items), d, 0.2, 0.75)
    for i, (txt, struck) in enumerate(items):
        if t < times[i]:
            continue
        y = 640 + i * 210
        p = ease_out_back((t - times[i]) / 0.35)
        sp = ease_out_cubic((t - times[i] - 0.45) / 0.3) if struck else 0
        col = WHITE if struck else GREEN
        ti = text_img(txt, 110, "dblack", col, th["acc"], 960, 8, BLACK, True, 1)
        sc_ = p * (1 + (0.06 * math.sin(t * 7) if not struck and t - times[i] > 0.4 else 0))
        put(c, ti, W / 2, y, scale=sc_, alpha=1 - 0.45 * sp)
        if struck and sp > 0:
            lw = int((ti.width - 40) * sp)
            line = panel_img(max(4, lw), 18, RED + (255,), 9)
            put(c, line, W / 2 - (ti.width - 40) / 2, y + 4, anchor="left", rot=0)
        if not struck and t - times[i] > 0.4:
            badge = tag_pill("¡CONFIRMADO!", th, 42)
            put(c, badge, W / 2, y + 120, scale=ease_out_back((t - times[i] - 0.4) / 0.3))


def sc_facts(c, t, d, v, th):
    ic = icon(v.get("icon", "star"), th["acc"], th["acc2"])
    s = ease_out_back(t / 0.4)
    put(c, ic, W / 2, 560 + 14 * math.sin(t * 2.5), scale=s * 0.92, rot=6 * math.sin(t * 1.7))
    if v.get("num"):
        b = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        bd = ImageDraw.Draw(b)
        bd.ellipse((10, 10, 290, 290), fill=RED + (255,), outline=WHITE, width=16)
        bd.text((150, 158), "#" + v["num"], font=font("dblack", 140), fill=WHITE, anchor="mm")
        b = b.resize((170, 170), Image.LANCZOS)
        put(c, b, 300, 420, scale=ease_out_back((t - 0.1) / 0.3, 3), rot=-10)
    a = ease_out_cubic((t - 0.1) / 0.25)
    head = text_img(v["head"], 104, "dblack", th["acc"], th["acc"], 960, 8, BLACK, True, 2)
    body = text_img(v["body"], 62, "black", WHITE, th["acc"], 900, 4, BLACK, True, 3)
    top = 810
    ph = head.height + body.height + 30
    put(c, panel_img(1010, ph, (0, 0, 0, 170), 36, th["acc2"] + (255,), 5), W / 2, top + ph / 2, alpha=a)
    put(c, head, W / 2, top + 10 + head.height / 2, scale=ease_out_back((t - 0.15) / 0.35))
    ba = ease_out_cubic((t - 0.35) / 0.3)
    put(c, body, W / 2, top + head.height + body.height / 2 + 25 * (1 - ba), alpha=ba)


def sc_outro(c, t, d, v, th):
    q = text_img(v["q"], 100, "dblack", WHITE, th["acc"], 960, 8, BLACK, True, 4)
    put(c, q, W / 2, 640, scale=ease_out_back(t / 0.4) * (1 + 0.015 * math.sin(t * 4)))
    clicked = t > 1.5
    s = ease_out_back((t - 0.35) / 0.35)
    if not clicked:
        btn = panel_img(660, 160, RED + (255,), 80)
        label = "SUSCRÍBETE"
    else:
        btn = panel_img(660, 160, (70, 70, 80, 255), 80)
        label = "SUSCRITO ✓"
    li = text_img(label, 78, "dblack", WHITE, WHITE, 600, 0, BLACK, False, 1)
    b = btn.copy()
    b.paste(li, ((b.width - li.width) // 2, (b.height - li.height) // 2), li)
    press = 0.92 if 1.35 < t < 1.5 else 1.0
    pulse = 1 + (0.04 * math.sin(t * 7) if not clicked else 0)
    put(c, b, W / 2, 1010, scale=s * press * pulse)
    # cursor/toque
    if 0.9 < t < 2.0:
        ct = clamp((t - 0.9) / 0.45)
        cx, cy = lerp(W + 100, W / 2 + 150, ease_out_cubic(ct)), lerp(1300, 1040, ease_out_cubic(ct))
        hand = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hand)
        hd.ellipse((5, 5, 85, 85), fill=(255, 255, 255, 230), outline=BLACK, width=5)
        put(c, hand, cx, cy)
        if t > 1.4:
            rp = clamp((t - 1.4) / 0.4)
            ring = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
            ImageDraw.Draw(ring).ellipse((10, 10, 290, 290), outline=(255, 255, 255, 255), width=10)
            put(c, ring, cx, cy, scale=0.3 + rp, alpha=1 - rp)
    a = ease_out_cubic((t - 0.6) / 0.3)
    sub = text_img("Curiosidades de GTA cada día", 54, "black", th["acc2"], th["acc"], 940, 5)
    put(c, sub, W / 2, 1160, alpha=a)


def render_scene(c, t, d, v, th, th_name):
    typ = v["type"]
    if typ == "title":
        sc_title(c, t, d, v, th)
    elif typ == "year":
        sc_year(c, t, d, v, th)
    elif typ == "counter":
        sc_counter(c, t, d, v, th)
    elif typ == "versus":
        sc_versus(c, t, d, v, th, th_name)
    elif typ == "pairs":
        sc_pairs(c, t, d, v, th, th_name)
    elif typ == "bars":
        sc_bars(c, t, d, v, th)
    elif typ == "strike":
        sc_strike(c, t, d, v, th)
    elif typ == "facts":
        sc_facts(c, t, d, v, th)
    elif typ == "outro":
        sc_outro(c, t, d, v, th)
    else:
        raise ValueError(typ)


# ----------------------------------------------------------------- subtítulos
def caption_chunks(say, t0, t1):
    """Reparte las palabras de la locución en el tiempo y las agrupa en bloques cortos."""
    words = say.replace("*", "").split()
    weights = []
    for w in words:
        k = len(w) + 2
        if w[-1] in ",;:":
            k += 4
        if w[-1] in ".?!":
            k += 7
        weights.append(k)
    tot = sum(weights)
    times, acc = [], t0
    for k in weights:
        times.append(acc)
        acc += (t1 - t0) * k / tot
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        txt = " ".join(words[j] for j in cur)
        if len(cur) >= 3 or len(txt) >= 16 or w[-1] in ".,?!:;":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return words, times, chunks


def draw_caption(c, t, words, times, chunks, scene_end, th):
    for ci, ch in enumerate(chunks):
        start = times[ch[0]]
        end = times[chunks[ci + 1][0]] if ci + 1 < len(chunks) else scene_end
        if start <= t < end:
            cur = ch[0]
            for j in ch:
                if times[j] <= t:
                    cur = j
            parts = []
            for j in ch:
                w = words[j].upper()
                parts.append("*" + w + "*" if j == cur else w)
            img = text_img(" ".join(parts), 84, "dblack", WHITE, th["acc"], 880, 10, BLACK, True, 2)
            pop = 1 + 0.12 * (1 - ease_out_cubic((t - start) / 0.12))
            ox, oy = Ctx.ox, Ctx.oy
            Ctx.ox = Ctx.oy = 0
            put(c, img, W / 2, 1430, scale=pop)
            Ctx.ox, Ctx.oy = ox, oy
            return


def overlays(c, t, total, th):
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 12), fill=(0, 0, 0))
    d.rectangle((0, 0, int(W * t / total), 12), fill=th["acc"])
    pill = text_img(BRAND, 38, "black", WHITE, th["acc"], 900, 0, BLACK, False, 1)
    pw = pill.width + 36
    put(c, panel_img(pw, pill.height + 12, (0, 0, 0, 150), (pill.height + 12) // 2, th["acc"] + (255,), 3), W / 2, 210)
    put(c, pill, W / 2, 210)
