# -*- coding: utf-8 -*-
"""Genera PUBLICACION.md y la carpeta guiones/ a partir de guiones.py."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from guiones import VIDEOS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.environ.get("SHORTS_WORK", os.path.join(ROOT, "work"))

# Orden de publicación recomendado (lo más buscado primero: lanzamiento de GTA VI)
ORDEN = ["01_13_anos_de_espera", "12_ganar_dinero_rapido", "03_vice_city_2002_vs_2026",
         "14_lo_que_gta6_no_te_explica", "11_trucos_gta6", "08_la_mayor_filtracion",
         "13_no_pierdas_tu_dinero", "04_evolucion_protagonistas", "10_por_que_tardo_tanto",
         "05_ciudades_gta_vs_reales", "06_records_gta_v", "02_gta_nacio_de_un_bug",
         "09_easter_eggs_legendarios", "07_curiosidades_san_andreas"]
DIAS = ["Vie 20 nov · 15:00", "Vie 20 nov · 15:00", "Vie 20 nov · 15:00", "Sáb 21 nov · 15:00",
        "Dom 22 nov · 15:00", "Lun 23 nov · 15:00", "Mar 24 nov · 15:00", "Mié 25 nov · 15:00",
        "Jue 26 nov · 15:00", "Vie 27 nov · 15:00", "Sáb 28 nov · 15:00", "Dom 29 nov · 15:00",
        "Lun 30 nov · 15:00", "Mar 1 dic · 15:00"]


def dur(vid):
    try:
        with open(os.path.join(WORK, vid, "meta.json")) as f:
            return f"{json.load(f)['duracion_s']:.0f} s"
    except OSError:
        return "—"


def main():
    by = {v["id"]: v for v in VIDEOS}
    L = []
    L.append("# Publicación: 14 Shorts de GTA\n")
    L.append("Todos los vídeos están en `videos/` (MP4 vertical 1080×1920, 30 fps, H.264 + AAC, "
             "audio normalizado a −14 LUFS, menos de 60 s). Cada uno tiene su portada `_portada.jpg`.\n")
    L.append("## Calendario\n")
    L.append("**Opción A (lo que pediste):** programar los 14 para el **viernes 20 de noviembre a las 15:00**.\n")
    L.append("**Opción B (recomendada para crecer):** los 3 más fuertes el viernes a las 15:00 y luego uno al día "
             "a la misma hora. Un canal nuevo que sube muchos Shorts a la vez reparte las visualizaciones de prueba "
             "entre todos; publicar a diario le da al algoritmo una señal constante.\n")
    L.append("| # | Vídeo | Duración | Opción B |")
    L.append("|---|---|---|---|")
    for i, vid in enumerate(ORDEN):
        L.append(f"| {i + 1} | `videos/{vid}.mp4` | {dur(vid)} | {DIAS[i]} |")
    L.append("")
    L.append("> Los vídeos 11–14 (trucos, dinero y consejos de GTA VI) se basan en guías publicadas en la semana "
             "del lanzamiento. Solo incluyen datos en los que coinciden varias guías, pero conviene revisarlos si sale un parche.\n")
    L.append("## Cómo programarlos (YouTube Studio)\n")
    L.append("1. Crea el canal (nombre sugerido: **Curiosidades GTA**; el texto del logo de los vídeos "
             "se cambia en `BRAND`, dentro de `src/render.py`).")
    L.append("2. Sube el logo (`canal/avatar.png`) y el banner (`canal/banner.png`).")
    L.append("3. Studio → **Crear → Subir vídeos** → elige el MP4. Al ser vertical y durar menos de 3 minutos, "
             "YouTube lo publica como Short automáticamente.")
    L.append("4. Copia el título, la descripción y las etiquetas de abajo.")
    L.append("5. Audiencia: **No, no es contenido para niños**.")
    L.append("6. Visibilidad → **Programar** → fecha y hora (15:00, en tu zona horaria).")
    L.append("7. En el móvil puedes elegir el fotograma de portada del Short; usa el del título (segundo 0–1).\n")
    L.append("> Contenido alterado o sintético: la locución usa una voz sintética que no imita a ninguna persona "
             "real, y no hay imágenes realistas. Según las normas de YouTube no hace falta marcar la casilla, "
             "pero marcarla no penaliza.\n")
    L.append("## Títulos, descripciones y etiquetas\n")
    for i, vid in enumerate(ORDEN):
        v = by[vid]
        L.append(f"### {i + 1}. `{vid}.mp4`\n")
        L.append(f"**Título:**\n```\n{v['title']}\n```")
        L.append(f"**Descripción:**\n```\n{v['description']}\n```")
        L.append(f"**Etiquetas:**\n```\n{', '.join(v['tags'])}\n```\n")
    with open(os.path.join(ROOT, "PUBLICACION.md"), "w") as f:
        f.write("\n".join(L))

    os.makedirs(os.path.join(ROOT, "guiones"), exist_ok=True)
    for v in VIDEOS:
        G = [f"# {v['title']}\n", f"Archivo: `videos/{v['id']}.mp4`\n", "| Escena | Locución | En pantalla |", "|---|---|---|"]
        for j, sc in enumerate(v["scenes"]):
            vis = sc["vis"]
            parts = [str(vis.get(k)) for k in ("lines", "tag", "year", "head", "label", "title", "body", "q", "rows", "items", "left", "right") if vis.get(k)]
            onscreen = " · ".join(parts).replace("*", "").replace("|", "/").replace("\n", " ")
            G.append(f"| {j + 1} ({vis['type']}) | {sc['say'].replace('*', '')} | {onscreen} |")
        with open(os.path.join(ROOT, "guiones", f"{v['id']}.md"), "w") as f:
            f.write("\n".join(G) + "\n")


if __name__ == "__main__":
    main()
