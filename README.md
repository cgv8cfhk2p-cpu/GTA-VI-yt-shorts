# GTA-VI-yt-shorts
Contenido sobre GTA VI para TikTok y YouTube Shorts: curiosidades, secretos, teorías, novedades y comparaciones con GTA V. Vídeos cortos y entretenidos para los fans de GTA.

## Qué hay aquí
- `videos/`: los 14 Shorts terminados (MP4 1080×1920) con su portada.
- `PUBLICACION.md`: títulos, descripciones, etiquetas y calendario para subirlos.
- `guiones/`: el guion de cada vídeo (locución y texto en pantalla).
- `canal/`: avatar y banner del canal.
- `src/`: el pipeline que los genera (guion → voz → música → animación → montaje).

## Regenerar o crear vídeos nuevos
Todo el material visual y la música son originales y se generan por código. No se usan imágenes, logos ni música de Rockstar.

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
```
Requiere `ffmpeg` y la fuente Inter. La voz se elige con `VOICE=em_alex|em_santa|ef_dora`.
