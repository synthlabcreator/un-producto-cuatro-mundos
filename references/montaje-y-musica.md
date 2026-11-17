# Montaje y música

Todo se hace en local con `scripts/reel.py` (ffmpeg + Python). Requisitos: `pip install -r requirements.txt` y ffmpeg en el PATH.

## 1 · Medir
```bash
python scripts/reel.py measure escena1.mp4
```
Devuelve en JSON:
- las ventanas de voz, medidas sobre la pista de voz separada con Demucs;
- los planos detectados, con una velocidad máxima sugerida.

Después hay que repasarlo a mano:
- **Mira una hoja de fotogramas y corrige el modo de cada plano**:
  - `c`: rápido en el centro (por defecto);
  - `k`: lento en el momento clave (saltos, trucos, impactos);
  - `n`: a velocidad real; es el que llevan **los planos de gente andando**.
- Comprueba las ventanas de voz de oído: a veces se cuela un efecto de sonido.

## 2 · Rampas sin música
Rellena `scenes` en `project.json` (mira `examples/nike/project.json`). Después ejecuta:
```bash
python scripts/reel.py ramps project.json
```
La voz va siempre a 1×, con una transición suave de 0,35 s, y el resto acelera hasta 3,2× con desenfoque de movimiento. **Enseña este montaje sin música antes de seguir.** En Nike, el usuario pidió que los planos andando volvieran a 1×.

## 3 · Canción con letra
El prompt se escribe a partir del montaje nuevo:
- **Tempo:** se elige para que 4 compases ocupen más o menos una escena; en Nike fueron unos 150 BPM.
- **Una frase de la letra por mundo, y el estribillo en el golpe de la ráfaga.**
- Los compases donde entra la voz van vaciados.

Plantilla (Flow Music, Suno, Dreamina…):
```
[GENRE that fits the brand], [BPM] BPM, [LANGUAGE] lyrics, male/female rap or vocal.
Structure: short intro hook ("Yeah"), four short verse lines, one per world:
1. "[line about world 1]"  2. "[line about world 2]"  3. "[line about world 3]"  4. "[line about world 4]"
then a big drop into the chorus: "[CHORUS with the product + 'four worlds']".
Leave space after each verse line (2 bars with no vocals) for a voice-over.
Punchy 808, crisp hats, mix ready for social media. Total about [DURATION] seconds.
```
La letra de Nike:
- Versos: «Court to the sky, I was drawn in the sun» / «Rain on the ramp, I don't fall, I just flip» / «Walk with the weight, one step, here I come».
- Estribillo: «One pair, four worlds, own the lane / never the same».

**Estas IA no respetan la duración ni los huecos.** En Nike salieron 67 s rapeando sin parar. No hace falta regenerar: los huecos se arreglan en el paso 4.

## 4 · Recolocar la letra y ajustar los cortes
```bash
python scripts/reel.py song cancion.wav --lyrics
```
Da el tempo, el pulso, los candidatos a golpe y cada frase de la letra con su segundo. Para medirla, separa la voz cantada con Demucs y la transcribe con Whisper. Después, en `music` de `project.json`, rellena:
- `song_drop`: el segundo del golpe en la canción;
- `beat`: la duración del pulso;
- `lines`: cada frase que quieras usar, con `start`, `end` y `shift_beats`. **Se mueve un número entero de pulsos para que siga a tiempo.**

Pon `target_frames` en cada escena para que cada corte caiga en un pulso. El corte cae en el golpe menos k pulsos. Luego ejecuta:
```bash
python scripts/reel.py ramps project.json
python scripts/reel.py music project.json      # avisa «CLASHES WITH VOICE» si una frase pisa una voz
python scripts/reel.py assemble project.json reel.mp4
```

## 5 · Mezcla
- La música baja **14 dB** bajo cada voz: empieza a bajar 0,25 s antes y vuelve en 0,3 s. Con 6 dB, en el móvil no se entiende.
- Los efectos de sonido de cada escena siguen el mismo mapa de tiempo que la imagen. Cuando el plano acelera, llevan un filtro de paso bajo para no sonar a «ardilla».
- La mezcla final va a −14 LUFS y lleva limitador, porque al pasar a AAC el pico sube.
- Para comprobarlo, pasa Whisper por la mezcla final: cada frase de la voz debe salir limpia.

## `tail`: lo que va después de las escenas
Se configura en `tail` del `project.json`. Lleva, en orden:
1. la ráfaga del producto a 1×, con su sonido bajado (`volume`);
2. el último plano a media velocidad y con acercamiento (`slow`, `push_in`);
3. la secuencia PNG del cartón (`images`).
