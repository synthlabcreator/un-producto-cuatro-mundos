# Prompts

Los prompts van en inglés, porque los generadores lo entienden mejor. La frase de la voz va en el idioma del reel. Los parámetros de cada modelo (duración máxima, resolución, si admite voz o fotograma inicial) se miran en su documentación del momento; no se dan por supuestos.

## 1 · Hoja de personaje (imagen, una por mundo)
Adjunta como referencia la foto real del producto.
```
Vertical 9:16 image. [WORLD STYLE: e.g. "high-end collectible figure CGI render" / "2D anime cel-shaded frame" / "3D animated feature film still" / "cinematic photograph, 35mm"].
An original character: [CHARACTER: age, look, clothes, hair], wearing / holding the [PRODUCT] from the reference image.
The [PRODUCT] must match the reference exactly: same shape, same colours, same materials, same logo position. Do not redesign it, do not add text or extra logos.
Setting: [WORLD SET], [LIGHT]. Accent colour [ACCENT HEX] in [where: lights / clothing details].
Full body, product clearly visible, no text, no watermark.
```
Pide también un primer plano de la cara, con el mismo personaje y la misma ropa: es el último plano de su escena.

## 2 · Escena de 10 s (de imagen a vídeo)
Fotograma inicial: la hoja de personaje aprobada.
```
Vertical 9:16, 10 seconds, [WORLD STYLE], keep the exact character, outfit and [PRODUCT] from the start image in every shot.
Multi-shot sequence, hard cuts:
0-2s: [ESTABLISH: wide hero shot of the character in the world, or macro of a world detail], slow push-in.
2-4s: extreme close-up of the [PRODUCT] on the character, [material detail], camera glides along it.
4-6s: [ACTION of this world, e.g. "low angle from below, the character jumps for a dunk, soles toward camera"].
6-8s: close-up of the [PRODUCT] as it lands / settles, [environment reaction: splash, sparks, dust].
8-10s: close-up of the character's face looking into the lens, says in [LANGUAGE]: "[LINE]". Lips in sync, natural delivery.
Sound: only natural sound effects of this world, no music, no other voices.
No on-screen text, no added logos, no subtitles.
```
En la escena 1, el personaje dice las dos frases: «[LÍNEA 1]» hacia el segundo 5 y «[LÍNEA 2]» al final.

## 3 · Ráfaga del producto (de 4 a 6 s)
```
Vertical 9:16, fast montage of extreme close-ups of the [PRODUCT] from the reference: [material 1], [material 2], logo detail, sole/edge, in [WORLD 4 look: real, rainy street light].
Very short cuts, micro camera moves, shallow depth of field. Last shot: the product side with the logo, held still for 1 second on a neutral grey background.
No text, no people talking, no music.
```
El último plano quieto sirve de puente al cartón: el logo oficial del cartón aparece en el mismo sitio que el del producto (corte por forma).

## Escenas de Nike reconstruidas
Reconstruidas a partir de los fotogramas del resultado. Sirven de ejemplo rellenado.
- **Mecha:** `high-end collectible figure CGI. Armoured mech warrior, black plates with lime green trims, glowing green reactor core in the chest, spiky silver hair. Dark industrial lab, overhead ring light, robotic arms, lit pedestal. 0-2s macro of the chest core pulsing; 2-4s full hero shot on the pedestal; 4-6s the metal hand holds the silver sneaker to camera; 6-8s macro of the swoosh and the chrome cage; 8-10s hero holding the sneaker, says "Cuatro mundos."` (con «Un producto» hacia el segundo 5)
- **Anime:** `2D anime cel-shaded. Teen with black hair and green eyes, black tracksuit with a green stripe, silver sneakers. Basketball court under a highway overpass, late afternoon blue sky, wet ground. 0-2s wide shot of the game; 2-4s low close-up of the sneakers; 4-6s from below, he jumps for a dunk, soles to camera; 6-8s the sneakers land on the wet court; 8-10s face close-up, smiling, says "Un estilo para cada historia."`
- **Cartoon 3D:** `3D animated feature film look. Red curly hair skater girl with freckles, cap, lime jacket, ripped jeans. Skatepark at night in the rain, green neon lights, reflective ground. 0-2s her feet on the board; 2-4s macro of the sneaker on the deck; 4-6s ollie on the ramp; 6-8s landing close-up, splash; 8-10s face close-up, says "Tu producto en cualquier mundo."`
- **Calle real:** `cinematic handheld photograph look, 35mm. Young man with dreadlocks, chain, black and green track jacket, silver sneakers. Under an iron bridge, autumn, wet street, overcast light. 0-2s he walks toward camera; 2-4s low tracking shot of his steps; 4-6s steps up onto a curb; 6-8s close on the sneakers walking on; 8-10s face close-up, says "Más contenido, menos producción."`

## Lista de rechazo (se mira cada toma)
- El producto cambia de forma, de color, de logo o de número de piezas entre planos.
- Aparece texto en la imagen, sobre todo mal escrito: carteles, letreros o marcas inventadas.
- Hay dedos de más, pies fundidos con el suelo o la cara cambia entre planos.
- Los labios no van con la frase, o la frase está mal pronunciada.
- Hay música dentro de la escena: estorba a la canción.

Si una toma falla solo en un tramo, no hace falta repetirla: se corta ese tramo en el montaje. En Nike, la escena 4 traía un letrero mal escrito y la pierna de la 4.1 andaba mal; se cortaron los dos tramos.
