# -*- coding: utf-8 -*-
"""Biblioteca de planos de los tráilers oficiales de GTA VI y qué planos van con cada escena.

Los clips no se suben al repositorio (son material de Rockstar). Se esperan en CLIPS_DIR como
c2.mp4 ... c6.mp4 junto a shots.json (inicio/fin de cada plano, generado con detección de cortes).
"""

# rotación necesaria por clip (c5 venía girado 90º)
ROTATE = {"c5": "transpose=2"}

# etiqueta -> planos
TAGS = {
    "lj": ["c4_02", "c4_04", "c4_06", "c6_01", "c6_09", "c4_16", "c3_03", "c6_06"],
    "lucia": ["c4_11", "c4_09", "c6_20", "c4_04", "c6_01"],
    "action": ["c4_03", "c4_07", "c6_17", "c4_08", "c4_09", "c6_20", "c2_21", "c6_04", "c4_15"],
    "police": ["c3_08", "c6_12", "c3_02", "c2_21"],
    "city_aerial": ["c2_02", "c2_04", "c3_07", "c3_09", "c3_11", "c5_02", "c2_08", "c2_16"],
    "city_sunset": ["c3_14", "c6_08", "c4_12"],
    "neon": ["c2_18", "c5_09", "c5_10", "c6_11", "c6_07", "c5_08", "c5_14", "c5_13"],
    "beach": ["c2_00", "c5_04", "c6_14", "c5_01", "c2_17"],
    "keys": ["c2_01", "c5_11", "c2_17"],
    "swamp": ["c2_03", "c3_10", "c5_03"],
    "boat": ["c2_06", "c3_13", "c5_05", "c2_07"],
    "dive": ["c3_12", "c5_01"],
    "store": ["c2_11", "c2_12", "c2_13", "c3_06", "c3_05"],
    "vault": ["c4_01", "c6_05"],
    "money": ["c4_01", "c6_05", "c3_05", "c2_11", "c3_02"],
    "gym": ["c6_15"],
    "phone": ["c2_14", "c2_15"],
    "chars": ["c2_09", "c2_20", "c2_15", "c2_19", "c3_01", "c3_04", "c6_16", "c2_05", "c5_16"],
    "cars": ["c2_10", "c4_05", "c5_17", "c6_08", "c5_07", "c2_18"],
    "gator": ["c5_16"],
}

# El clip 3 lleva la marca de agua de otro editor ("Xeamerr") y un contador superpuesto: no se usa.
EXCLUIR = ("c3_",)
TAGS["dive"] += ["c2_06"]
TAGS = {k: [x for x in v if not x.startswith(EXCLUIR)] for k, v in TAGS.items()}

# encuadre horizontal del recorte 9:16 (0 = izquierda, 0.5 = centro, 1 = derecha)
XPOS = {
    "c4_04": 0.3, "c6_01": 0.35, "c2_12": 0.3, "c2_13": 0.35, "c3_06": 0.35, "c4_16": 0.4,
    "c4_11": 0.55, "c6_15": 0.25, "c6_16": 0.6, "c6_12": 0.4, "c4_09": 0.75, "c6_20": 0.3,
    "c4_08": 0.55, "c3_05": 0.4, "c2_09": 0.55, "c2_14": 0.55, "c4_02": 0.45, "c6_09": 0.45,
    "c2_10": 0.45, "c3_12": 0.45,
}

# vídeo -> etiquetas de planos por escena
PLAN = {
    "01_13_anos_de_espera": [["lj", "lucia"], ["city_aerial"], ["phone", "chars"], ["lj", "lucia"],
                             ["action", "neon"], ["city_sunset", "cars"], ["lj", "beach"]],
    "03_vice_city_2002_vs_2026": [["neon", "city_aerial"], ["neon", "phone"], ["lj", "lucia"],
                                  ["keys", "swamp", "beach"], ["cars", "city_aerial"], ["city_sunset"]],
    "05_ciudades_gta_vs_reales": [["city_aerial"], ["city_aerial", "beach"], ["neon", "city_sunset"],
                                  ["swamp", "keys"], ["city_sunset", "beach"]],
    "08_la_mayor_filtracion": [["action"], ["chars", "phone"], ["chars"], ["chars", "neon"],
                               ["neon", "cars"], ["lj"], ["action"]],
    "10_por_que_tardo_tanto": [["city_sunset"], ["city_aerial", "beach"], ["lj"], ["money"],
                               ["swamp", "city_sunset"], ["city_aerial", "keys"]],
    "11_trucos_gta6": [["action"], ["lj"], ["action", "police"], ["gym"], ["phone", "cars"],
                       ["chars"], ["action"]],
    "12_ganar_dinero_rapido": [["money"], ["dive", "boat"], ["cars"], ["store"], ["lj"], ["vault"],
                               ["chars"], ["money"]],
    "13_no_pierdas_tu_dinero": [["police", "action"], ["action", "police"], ["chars"], ["phone"],
                                ["lj"], ["city_aerial"], ["vault"], ["store"]],
    "14_lo_que_gta6_no_te_explica": [["city_aerial"], ["chars", "gator"], ["boat"], ["cars", "police"],
                                     ["neon", "city_sunset"], ["city_aerial"], ["lj"], ["beach"]],
}
