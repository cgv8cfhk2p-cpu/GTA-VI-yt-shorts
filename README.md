# GTA-VI-yt-shorts
Contenido sobre GTA VI para TikTok y YouTube Shorts: curiosidades, secretos, teorías, novedades y comparaciones con GTA V. Vídeos cortos y entretenidos para los fans de GTA.

## Qué hay aquí
- `videos/`: los 16 Shorts terminados (MP4 1080×1920) con su portada.
- `PUBLICACION.md`: títulos, descripciones, etiquetas y calendario para subirlos.
- `guiones/`: el guion de cada vídeo (locución y texto en pantalla).
- `canal/`: avatar y banner del canal.
- `src/`: el pipeline que los genera (guion → voz → música → animación → montaje).

## Regenerar o crear vídeos nuevos
Hay dos estilos:
- **Estilo 1** (`src/build.py`, vídeos 02, 04, 06, 07 y 09): fondo synthwave animado y gráficos generados por código.
- **Estilo 2** (`src/build2.py`, vídeos 01, 03, 05, 08, 10, 11, 12, 13, 14, 15 y 16): planos reales de los tráilers oficiales de GTA VI
  a pantalla completa, con título numerado, paneles tipo HUD y subtítulos en cursiva. Los clips no están en el repositorio:
  se ponen en `CLIPS_DIR` (c2.mp4 … c6.mp4 + shots.json) y en `src/planos.py` se elige qué planos van con cada escena.
  Se usa solo la imagen: el audio del tráiler se descarta.

La voz y la música son las mismas en los dos estilos (música generada por código, sin copyright).

```bash
pip install -r requirements.txt
# modelo de voz Kokoro (GitHub releases de kokoro-onnx)
mkdir -p models && cd models
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd ..
# 1) edita src/guiones.py  2) genera voces  3) renderiza  4) guía de publicación
python src/build.py tts
python src/build.py render            # o: render 01_13_anos_de_espera
python src/publicacion.py
CLIPS_DIR=/ruta/clips python src/build2.py render   # estilo 2
```
Requiere `ffmpeg` y la fuente Inter.

**Voz:** por defecto es Piper `es_ES-davefx-medium` (masculina, España), ejecutada con onnxruntime (`src/piper_tts.py`).
Descárgala en `models/`:
```bash
cd models && curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-es_ES-davefx-medium.tar.bz2 && tar xjf vits-piper-es_ES-davefx-medium.tar.bz2
```
`PIPER_LENGTH` controla la velocidad (0.9 por defecto; menos = más rápido). `VOICE=em_alex` vuelve a la voz Kokoro anterior.
