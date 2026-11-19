# -*- coding: utf-8 -*-
"""Guiones de los 10 Shorts.

Cada vídeo es una lista de escenas. Cada escena tiene:
  - say: texto que lee la voz (y que aparece como subtítulo)
  - vis: tipo de animación + parámetros (ver render.py)
Las palabras entre *asteriscos* se pintan con el color de acento.
"""

VIDEOS = [
    # ------------------------------------------------------------------ 01
    {
        "id": "01_13_anos_de_espera",
        "theme": "vice",
        "title": "13 AÑOS esperando GTA 6… así fue la espera 😱 #shorts",
        "description": (
            "De GTA V en 2013 al lanzamiento de GTA VI en noviembre de 2026: filtraciones, "
            "tráilers que rompieron récords y retrasos. ¿Cuántos años tenías cuando salió GTA V?\n\n"
            "#gta6 #gtavi #gta #rockstargames #vicecity #shorts"
        ),
        "tags": ["gta 6", "gta vi", "gta 6 lanzamiento", "gta 6 trailer", "rockstar games",
                 "vice city", "gta 5", "curiosidades gta", "historia gta 6"],
        "scenes": [
            {"say": "Trece años. Eso es lo que hemos esperado para tener GTA 6 en nuestras manos.",
             "vis": {"type": "title", "lines": ["*13 AÑOS*", "DE ESPERA"], "sub": "GTA V → GTA VI"}},
            {"say": "Todo empezó en septiembre de 2013, cuando salió GTA 5.",
             "vis": {"type": "year", "year": "2013", "tag": "GTA V", "label": "Sale a la venta en septiembre"}},
            {"say": "En 2022, un hacker filtró más de 90 vídeos del desarrollo. Rockstar confirmó que eran reales.",
             "vis": {"type": "facts", "icon": "warning", "head": "LA GRAN FILTRACIÓN", "body": "Más de 90 vídeos del desarrollo filtrados en 2022"}},
            {"say": "En diciembre de 2023 llegó el primer tráiler: más de 90 millones de visitas en 24 horas. Récord mundial.",
             "vis": {"type": "counter", "value": 90421491, "tag": "TRÁILER 1 · 24 HORAS", "label": "visitas en YouTube · Récord Guinness"}},
            {"say": "El segundo tráiler fue todavía más lejos: 475 millones de visualizaciones en un solo día, sumando todas las plataformas.",
             "vis": {"type": "counter", "value": 475000000, "tag": "TRÁILER 2 · 24 HORAS", "label": "visualizaciones en todas las plataformas"}},
            {"say": "Luego llegaron los retrasos. Primero 2025, después mayo de 2026, y al final, el 19 de noviembre.",
             "vis": {"type": "strike", "title": "FECHA DE SALIDA", "items": [["OTOÑO 2025", True], ["26 MAYO 2026", True], ["19 NOV 2026", False]]}},
            {"say": "Y por fin, Vice City ha vuelto. ¿Cuántos años tenías cuando salió GTA 5? Te leo en comentarios.",
             "vis": {"type": "outro", "q": "¿Cuántos años tenías cuando salió *GTA V?*"}},
        ],
    },
    # ------------------------------------------------------------------ 02
    {
        "id": "02_gta_nacio_de_un_bug",
        "theme": "sunset",
        "title": "GTA existe gracias a un ERROR de programación 🐛 #shorts",
        "description": (
            "Antes de llamarse Grand Theft Auto era un juego de carreras llamado Race'n'Chase. "
            "Un bug en la policía lo cambió todo.\n\n#gta #gta6 #curiosidades #videojuegos #rockstar #shorts"
        ),
        "tags": ["gta", "origen de gta", "race n chase", "dma design", "rockstar north",
                 "curiosidades gta", "historia de gta", "gta 1", "gta 6"],
        "scenes": [
            {"say": "GTA existe gracias a un error de programación.",
             "vis": {"type": "title", "lines": ["GTA NACIÓ", "DE UN *BUG*"]}},
            {"say": "A mediados de los noventa, un pequeño estudio escocés, DMA Design, trabajaba en un juego de carreras llamado Race and Chase.",
             "vis": {"type": "year", "year": "1995", "tag": "DMA DESIGN · ESCOCIA", "head": "Race'n'Chase", "label": "Un simple juego de persecuciones"}},
            {"say": "Pero un fallo hizo que los coches de policía se volvieran locos: en vez de seguir su ruta, intentaban embestir al jugador sin parar.",
             "vis": {"type": "facts", "icon": "warning", "head": "EL BUG", "body": "La policía se volvía agresiva y te embestía sin parar"}},
            {"say": "Al equipo le pareció tan divertido que decidieron que ese caos fuera el centro del juego.",
             "vis": {"type": "facts", "icon": "star", "head": "¿UN ERROR?", "body": "No: ¡la mejor idea del juego!"}},
            {"say": "Así, en 1997, nació Grand Theft Auto: vista desde arriba, gráficos en 2D y muchísima polémica.",
             "vis": {"type": "year", "year": "1997", "tag": "NACE LA SAGA", "head": "Grand Theft Auto", "label": "Vista cenital · 2D · polémica"}},
            {"say": "Ese estudio acabaría convirtiéndose en Rockstar North, los creadores de toda la saga.",
             "vis": {"type": "versus", "title": "EL MISMO ESTUDIO", "left": {"head": "DMA", "body": "Design\nDundee"}, "right": {"head": "RN", "body": "Rockstar\nNorth"}}},
            {"say": "Hoy la saga suma casi 475 millones de copias vendidas. Todo por un bug.",
             "vis": {"type": "counter", "value": 475000000, "tag": "COPIAS DE LA SAGA", "label": "y todo empezó con un bug"}},
            {"say": "Sígueme para más curiosidades de GTA.",
             "vis": {"type": "outro", "q": "¿Sabías que GTA nació de un *error?*"}},
        ],
    },
    # ------------------------------------------------------------------ 03
    {
        "id": "03_vice_city_2002_vs_2026",
        "theme": "vice",
        "title": "Vice City 2002 vs Vice City 2026 🌴 La diferencia es BRUTAL #shorts",
        "description": (
            "Comparamos GTA Vice City (2002) con el Vice City de GTA 6: época, protagonistas, mapa y consolas. "
            "¿Con cuál te quedas?\n\n#gta6 #vicecity #gtavicecity #antesyahora #gta #shorts"
        ),
        "tags": ["vice city", "gta vice city", "gta 6", "vice city vs gta 6", "antes y ahora",
                 "comparacion gta", "tommy vercetti", "lucia gta 6", "leonida"],
        "scenes": [
            {"say": "Vice City en 2002 contra Vice City en 2026. La diferencia es brutal.",
             "vis": {"type": "title", "lines": ["VICE CITY", "*2002 vs 2026*"]}},
            {"say": "El original estaba ambientado en 1986: neón, camisas hawaianas y música ochentera. El nuevo transcurre en la actualidad, con redes sociales y vídeos virales.",
             "vis": {"type": "versus", "title": "LA ÉPOCA", "left": {"head": "1986", "body": "Neón y\nmúsica 80s"}, "right": {"head": "HOY", "body": "Redes sociales\ny virales"}}},
            {"say": "Antes controlabas a Tommy Vercetti, un mafioso recién salido de la cárcel. Ahora tienes dos protagonistas: Lucía y Jason, una pareja al estilo Bonnie y Clyde.",
             "vis": {"type": "versus", "title": "PROTAGONISTAS", "left": {"head": "1", "body": "Tommy\nVercetti"}, "right": {"head": "2", "body": "Lucía\ny Jason"}}},
            {"say": "En 2002 el mapa era solo la ciudad. En GTA 6, Vice City es solo una parte del estado de Leonida, la Florida de Rockstar.",
             "vis": {"type": "versus", "title": "EL MAPA", "left": {"head": "1", "body": "Una\nciudad"}, "right": {"head": "∞", "body": "Todo el estado\nde Leonida"}}},
            {"say": "Y el original salió primero en PlayStation 2. Ahora llega a PlayStation 5 y Xbox Series.",
             "vis": {"type": "versus", "title": "CONSOLAS", "left": {"head": "PS2", "body": "Octubre\n2002"}, "right": {"head": "PS5", "body": "y Xbox Series\n2026"}}},
            {"say": "¿Con cuál te quedas, el clásico o el nuevo? Te leo en comentarios.",
             "vis": {"type": "outro", "q": "*¿2002* o 2026?*"}},
        ],
    },
    # ------------------------------------------------------------------ 04
    {
        "id": "04_evolucion_protagonistas",
        "theme": "night",
        "title": "La EVOLUCIÓN de los protagonistas de GTA (2001-2026) #shorts",
        "description": (
            "De Claude, que nunca habla, a Lucía y Jason en GTA 6. Así han cambiado los protagonistas de GTA. "
            "¿Cuál es tu favorito?\n\n#gta #gta6 #gtasanandreas #gta5 #evolucion #shorts"
        ),
        "tags": ["protagonistas gta", "evolucion gta", "cj", "niko bellic", "tommy vercetti",
                 "trevor", "lucia gta 6", "jason gta 6", "gta 6"],
        "scenes": [
            {"say": "Así han evolucionado los protagonistas de GTA en 25 años.",
             "vis": {"type": "title", "lines": ["EVOLUCIÓN DE", "LOS *PROTAS*"], "sub": "2001 → 2026"}},
            {"say": "2001, GTA 3. Claude, el protagonista que no dice ni una sola palabra en todo el juego.",
             "vis": {"type": "year", "year": "2001", "tag": "GTA III", "head": "Claude", "label": "No dice ni una palabra"}},
            {"say": "2002, Vice City. Tommy Vercetti, con la voz del actor Ray Liotta.",
             "vis": {"type": "year", "year": "2002", "tag": "VICE CITY", "head": "Tommy Vercetti", "label": "Voz de Ray Liotta"}},
            {"say": "2004, San Andreas. CJ vuelve a Los Santos tras la muerte de su madre. Podía engordar, ganar músculo y hasta nadar.",
             "vis": {"type": "year", "year": "2004", "tag": "SAN ANDREAS", "head": "CJ", "label": "Engorda, gana músculo y nada"}},
            {"say": "2008, GTA 4. Niko Bellic, un veterano de guerra que llega a Liberty City buscando el sueño americano.",
             "vis": {"type": "year", "year": "2008", "tag": "GTA IV", "head": "Niko Bellic", "label": "Busca el sueño americano"}},
            {"say": "2013, GTA 5. Michael, Franklin y Trevor: tres protagonistas y puedes cambiar entre ellos cuando quieras.",
             "vis": {"type": "year", "year": "2013", "tag": "GTA V", "head": "Michael · Franklin · Trevor", "label": "Tres protagonistas a la vez"}},
            {"say": "Y 2026, GTA 6. Lucía y Jason. Lucía es la primera protagonista femenina de la saga moderna.",
             "vis": {"type": "year", "year": "2026", "tag": "GTA VI", "head": "Lucía y Jason", "label": "Primera protagonista de la era 3D"}},
            {"say": "¿Cuál es tu favorito? Te leo en comentarios.",
             "vis": {"type": "outro", "q": "¿Cuál es tu *protagonista* favorito?"}},
        ],
    },
    # ------------------------------------------------------------------ 05
    {
        "id": "05_ciudades_gta_vs_reales",
        "theme": "leonida",
        "title": "Todas las ciudades de GTA EXISTEN en la vida real 🗺️ #shorts",
        "description": (
            "Liberty City, Vice City, Los Santos, San Fierro, Las Venturas y Leonida: estas son las ciudades reales "
            "en las que se inspiran.\n\n#gta #gta6 #leonida #vicecity #lossantos #curiosidades #shorts"
        ),
        "tags": ["ciudades gta", "gta vida real", "leonida florida", "vice city miami", "los santos los angeles",
                 "liberty city nueva york", "gta 6 mapa", "curiosidades gta"],
        "scenes": [
            {"say": "Todas las ciudades de GTA existen en la vida real. Mira.",
             "vis": {"type": "title", "lines": ["CIUDADES GTA", "VS *REALES*"]}},
            {"say": "Liberty City es Nueva York. Vice City es Miami. Y Los Santos es Los Ángeles.",
             "vis": {"type": "pairs", "title": "GTA → REAL", "rows": [["Liberty City", "Nueva York"], ["Vice City", "Miami"], ["Los Santos", "Los Ángeles"]]}},
            {"say": "En San Andreas también estaban San Fierro, que es San Francisco, y Las Venturas, que es Las Vegas.",
             "vis": {"type": "pairs", "title": "SAN ANDREAS", "rows": [["San Fierro", "San Francisco"], ["Las Venturas", "Las Vegas"]]}},
            {"say": "Y en GTA 6 llega Leonida, que es Florida. Con Grassrivers, inspirado en los Everglades, y los Cayos de Leonida, como los Cayos de Florida.",
             "vis": {"type": "pairs", "title": "GTA VI", "rows": [["Leonida", "Florida"], ["Grassrivers", "Everglades"], ["Leonida Keys", "Florida Keys"]]}},
            {"say": "Rockstar ha recreado medio Estados Unidos en 25 años. ¿Qué ciudad te gustaría ver en el próximo GTA?",
             "vis": {"type": "outro", "q": "¿Qué ciudad quieres en el *próximo GTA?*"}},
        ],
    },
    # ------------------------------------------------------------------ 06
    {
        "id": "06_records_gta_v",
        "theme": "gold",
        "title": "Los RÉCORDS absurdos de GTA 5 💰 #shorts",
        "description": (
            "Mil millones de dólares en 3 días, más de 230 millones de copias y tres generaciones de consolas. "
            "Los récords de GTA V que GTA 6 tendrá que superar.\n\n#gta5 #gta6 #records #gta #rockstar #shorts"
        ),
        "tags": ["gta 5", "records gta 5", "gta 5 ventas", "juego mas vendido", "gta online",
                 "gta 6", "curiosidades gta", "guinness gta"],
        "scenes": [
            {"say": "Los récords de GTA 5 que parecen inventados.",
             "vis": {"type": "title", "lines": ["RÉCORDS", "*ABSURDOS*", "DE GTA V"]}},
            {"say": "Ganó mil millones de dólares en solo tres días. Ningún producto de entretenimiento lo había hecho tan rápido.",
             "vis": {"type": "counter", "value": 1000000000, "prefix": "$", "tag": "EN SOLO 3 DÍAS", "label": "récord Guinness en 2013"}},
            {"say": "Ha vendido más de 230 millones de copias.",
             "vis": {"type": "counter", "value": 230000000, "tag": "COPIAS VENDIDAS", "label": "y sigue sumando"}},
            {"say": "Es el segundo juego más vendido de la historia. Solo lo supera Minecraft.",
             "vis": {"type": "bars", "title": "MÁS VENDIDOS", "unit": "M", "rows": [["Minecraft", 350, "+300M"], ["GTA V", 230, "+230M"]]}},
            {"say": "Ha salido en tres generaciones de consolas: PlayStation 3, 4 y 5.",
             "vis": {"type": "facts", "icon": "gamepad", "head": "3 GENERACIONES", "body": "PS3 · PS4 · PS5\nXbox 360 · One · Series"}},
            {"say": "Y GTA Online sigue recibiendo actualizaciones más de diez años después de su lanzamiento.",
             "vis": {"type": "facts", "icon": "clock", "head": "+10 AÑOS", "body": "GTA Online sigue vivo desde 2013"}},
            {"say": "¿Crees que GTA 6 superará estos récords?",
             "vis": {"type": "outro", "q": "¿GTA VI superará a *GTA V?*"}},
        ],
    },
    # ------------------------------------------------------------------ 07
    {
        "id": "07_curiosidades_san_andreas",
        "theme": "sunset",
        "title": "5 curiosidades de GTA San Andreas que NO sabías 🌄 #shorts",
        "description": (
            "Bigfoot, el gimnasio, el mapa con tres ciudades y el récord de PS2. "
            "Curiosidades del GTA más querido.\n\n#gtasanandreas #gta #cj #curiosidades #ps2 #shorts"
        ),
        "tags": ["gta san andreas", "curiosidades san andreas", "cj", "bigfoot gta",
                 "san andreas secretos", "ps2", "gta", "grove street"],
        "scenes": [
            {"say": "Cinco curiosidades de GTA San Andreas que quizá no sabías.",
             "vis": {"type": "title", "lines": ["SAN ANDREAS", "*5 SECRETOS*"]}},
            {"say": "Uno. El mapa tenía tres ciudades completas: Los Santos, San Fierro y Las Venturas, además de campo, desierto y montañas.",
             "vis": {"type": "facts", "num": "1", "icon": "pin", "head": "3 CIUDADES", "body": "Los Santos · San Fierro · Las Venturas"}},
            {"say": "Dos. CJ podía engordar, ponerse musculoso, nadar y pilotar aviones. Algo nunca visto en 2004.",
             "vis": {"type": "facts", "num": "2", "icon": "trophy", "head": "CJ EVOLUCIONA", "body": "Engorda, gana músculo, nada y vuela"}},
            {"say": "Tres. Es el juego más vendido de toda la historia de PlayStation 2.",
             "vis": {"type": "facts", "num": "3", "icon": "crown", "head": "REY DE LA PS2", "body": "El juego más vendido de la consola"}},
            {"say": "Cuatro. Durante años, miles de jugadores buscaron a Bigfoot en los bosques del juego. Nunca existió.",
             "vis": {"type": "facts", "num": "4", "icon": "mountain", "head": "BIGFOOT", "body": "Años de búsqueda… y nunca existió"}},
            {"say": "Cinco. Un minijuego oculto en el código provocó tal polémica en 2005 que el juego tuvo que retirarse y relanzarse.",
             "vis": {"type": "facts", "num": "5", "icon": "warning", "head": "LA POLÉMICA", "body": "Código oculto que obligó a relanzar el juego"}},
            {"say": "¿Cuál no sabías? Sígueme para más.",
             "vis": {"type": "outro", "q": "¿Cuál *no sabías?*"}},
        ],
    },
    # ------------------------------------------------------------------ 08
    {
        "id": "08_la_mayor_filtracion",
        "theme": "night",
        "title": "La MAYOR filtración de la historia de los videojuegos 🕵️ #shorts",
        "description": (
            "En 2022 un adolescente filtró más de 90 vídeos de GTA 6. Así lo hizo y así terminó todo.\n\n"
            "#gta6 #leak #filtracion #gta #rockstar #shorts"
        ),
        "tags": ["gta 6 leak", "filtracion gta 6", "hacker gta 6", "gta 6", "rockstar games",
                 "gta 6 trailer filtrado", "curiosidades gta"],
        "scenes": [
            {"say": "La mayor filtración de la historia de los videojuegos.",
             "vis": {"type": "title", "lines": ["LA MAYOR", "*FILTRACIÓN*", "DE LA HISTORIA"]}},
            {"say": "Septiembre de 2022. Un hacker publica más de 90 vídeos del desarrollo de GTA 6.",
             "vis": {"type": "counter", "value": 90, "prefix": "+", "tag": "SEPTIEMBRE 2022", "label": "vídeos filtrados de GTA VI"}},
            {"say": "Rockstar confirmó que eran reales y dijo estar extremadamente decepcionada.",
             "vis": {"type": "facts", "icon": "warning", "head": "CONFIRMADO", "body": "Rockstar: «extremadamente decepcionados»"}},
            {"say": "El responsable era un adolescente británico que ya había atacado a otras grandes empresas tecnológicas.",
             "vis": {"type": "facts", "icon": "skull", "head": "EL HACKER", "body": "Un adolescente británico"}},
            {"say": "Lo más loco: lo hizo desde la habitación de un hotel, con un Amazon Fire Stick y un móvil, mientras estaba en libertad bajo fianza.",
             "vis": {"type": "facts", "icon": "play", "head": "¿CON QUÉ?", "body": "Un Fire Stick, un móvil y una tele de hotel"}},
            {"say": "Y un año después, el primer tráiler también se filtró, y Rockstar tuvo que publicarlo antes de tiempo.",
             "vis": {"type": "year", "year": "2023", "tag": "OTRA VEZ", "head": "Tráiler filtrado", "label": "Rockstar lo publicó antes de tiempo"}},
            {"say": "¿Tú viste los vídeos filtrados? Cuéntamelo en comentarios.",
             "vis": {"type": "outro", "q": "¿Viste los vídeos *filtrados?*"}},
        ],
    },
    # ------------------------------------------------------------------ 09
    {
        "id": "09_easter_eggs_legendarios",
        "theme": "leonida",
        "title": "Easter eggs de GTA que te van a volar la cabeza 🤯 #shorts",
        "description": (
            "El corazón de la Estatua de la Felicidad, el misterio del Monte Chiliad, el OVNI hundido "
            "y el mensaje secreto de GTA III.\n\n#gta #eastereggs #gta5 #gta4 #secretos #shorts"
        ),
        "tags": ["easter eggs gta", "secretos gta", "monte chiliad", "estatua de la felicidad",
                 "ovni gta 5", "gta 3 secreto", "misterios gta", "gta 6"],
        "scenes": [
            {"say": "Easter eggs de GTA que te van a volar la cabeza.",
             "vis": {"type": "title", "lines": ["EASTER EGGS", "*LEGENDARIOS*"]}},
            {"say": "En GTA 4, dentro de la Estatua de la Felicidad, hay un corazón gigante encadenado. Y late.",
             "vis": {"type": "facts", "icon": "heart", "head": "GTA IV", "body": "Un corazón gigante que late dentro de la estatua"}},
            {"say": "En GTA 5, el mural del Monte Chiliad está lleno de símbolos: un ovni, un huevo y un jetpack. Los jugadores llevan años intentando descifrarlo.",
             "vis": {"type": "facts", "icon": "mountain", "head": "MONTE CHILIAD", "body": "OVNI · huevo · jetpack… ¿qué significa?"}},
            {"say": "Y también en GTA 5, en el fondo del mar, hay restos de un ovni hundido.",
             "vis": {"type": "facts", "icon": "ufo", "head": "BAJO EL MAR", "body": "Un OVNI hundido frente a la costa"}},
            {"say": "En GTA 3, si llegas a un lugar imposible, aparece un mensaje: no deberías poder llegar aquí, ¿sabes?",
             "vis": {"type": "facts", "icon": "star", "head": "GTA III", "body": "«No deberías poder llegar aquí, ¿sabes?»"}},
            {"say": "¿Qué secretos crees que esconde GTA 6? Sígueme para descubrirlos.",
             "vis": {"type": "outro", "q": "¿Qué secretos esconde *GTA VI?*"}},
        ],
    },
    # ------------------------------------------------------------------ 10
    {
        "id": "10_por_que_tardo_tanto",
        "theme": "gold",
        "title": "¿Por qué GTA 6 tardó TANTO? ⏳ #shorts",
        "description": (
            "Mira cuántos años pasaron entre cada GTA y por qué GTA 6 tardó más de 13 años en llegar.\n\n"
            "#gta6 #gta #gta5 #rockstar #reddead #shorts"
        ),
        "tags": ["gta 6", "por que gta 6 tardo", "gta 6 retraso", "gta online", "red dead redemption 2",
                 "rockstar games", "historia gta", "gta 5"],
        "scenes": [
            {"say": "¿Por qué GTA 6 tardó tanto? Mira cuánto tiempo pasó entre cada GTA.",
             "vis": {"type": "title", "lines": ["¿POR QUÉ", "TARDÓ *TANTO?*"]}},
            {"say": "De GTA 3 a Vice City, un año. A San Andreas, dos. A GTA 4, cuatro. A GTA 5, cinco. Y a GTA 6, trece.",
             "vis": {"type": "bars", "title": "AÑOS ENTRE JUEGOS", "unit": "", "rows": [["III → VC", 1, "1"], ["VC → SA", 2, "2"], ["SA → IV", 4, "4"], ["IV → V", 5, "5"], ["V → VI", 13, "13"]]}},
            {"say": "Es más tiempo que entre GTA 3 y GTA 5 juntos.",
             "vis": {"type": "versus", "title": "MÁS QUE…", "left": {"head": "12", "body": "años de\nGTA III a V"}, "right": {"head": "13", "body": "años de\nGTA V a VI"}}},
            {"say": "La razón principal: GTA Online. Siguió generando miles de millones durante más de una década.",
             "vis": {"type": "facts", "icon": "dollar", "head": "GTA ONLINE", "body": "Miles de millones durante una década"}},
            {"say": "Además, Rockstar dedicó años a Red Dead Redemption 2, que salió en 2018.",
             "vis": {"type": "year", "year": "2018", "tag": "MIENTRAS TANTO", "head": "Red Dead Redemption 2", "label": "Años de desarrollo en otro juego"}},
            {"say": "Y GTA 6 es el proyecto más ambicioso de su historia. ¿Valió la pena la espera?",
             "vis": {"type": "outro", "q": "¿Valió la pena *la espera?*"}},
        ],
    },
]
