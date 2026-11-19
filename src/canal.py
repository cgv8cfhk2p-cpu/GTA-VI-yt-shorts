# -*- coding: utf-8 -*-
"""Genera el avatar (800x800) y el banner (2560x1440) del canal con el mismo estilo de los vídeos."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw
import render as R

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
th = R.THEMES["vice"]
bg = R.draw_bg("vice", 0.3)

# Avatar: recorte cuadrado del atardecer + texto
av = bg.crop((0, 560, 1080, 1640)).resize((800, 800), Image.LANCZOS)
t1 = R.text_img("GTA", 300, "dblacki", th["acc"], th["acc"], 760, 12, R.BLACK, True, 1)
t2 = R.text_img("CURIOSIDADES", 92, "dblack", R.WHITE, th["acc"], 760, 7, R.BLACK, True, 1)
av.paste(t1, (400 - t1.width // 2, 330 - t1.height // 2), t1)
av.paste(t2, (400 - t2.width // 2, 560 - t2.height // 2), t2)
av.save(os.path.join(ROOT, "canal", "avatar.png"))

# Banner: zona segura central 1546x423
bn = bg.crop((0, 700, 1080, 1308)).resize((2560, 1440), Image.LANCZOS)
t1 = R.text_img("CURIOSIDADES *GTA*", 190, "dblacki", R.WHITE, th["acc"], 1500, 10, R.BLACK, True, 1)
t2 = R.text_img("Datos, comparaciones y secretos de GTA · Nuevo Short cada día", 54, "black", th["acc2"], th["acc"], 1500, 5, R.BLACK, True, 1)
bn.paste(t1, (1280 - t1.width // 2, 680 - t1.height // 2), t1)
bn.paste(t2, (1280 - t2.width // 2, 820 - t2.height // 2), t2)
bn.save(os.path.join(ROOT, "canal", "banner.png"))
print("ok")
