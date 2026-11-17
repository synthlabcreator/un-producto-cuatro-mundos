# Ejemplo rellenado · Nike «Un producto, cuatro mundos» (noviembre de 2026)

Spec ad de portafolio, sin encargo ni afiliación con Nike.

## Brief
- **Producto:** zapatilla Nike plateada de estilo P-6000, en cuero metalizado con malla negra.
- **Acento común:** verde lima #CEFF00.
- **Voz:** castellano de España; una frase por personaje, dicha a cámara en el primer plano final.
- **Canción:** rap en inglés generado en Flow Music, unos 150 BPM, 5 créditos.
- **Herramientas:** imágenes y vídeos de las escenas con ChatGPT; montaje, rampas, música y cartón con Claude Code en local (ffmpeg, Python y Remotion para el cartón).
- **Llamada:** «¿Quieres saber cómo se hace? Te dejo la skill en GitHub. Enlace en el comentario. ¡Guárdalo!».

## Resultado
| Reel (s) | Imagen | Voz en off | Letra |
|---|---|---|---|
| 0–6,71 | Mecha · guerrero mecánico | «Un producto» · «Cuatro mundos» | «Yeah» |
| 6,71–13,54 | Anime · baloncesto bajo el paso elevado | «Un estilo para cada historia» | «Court to the sky, I was drawn in the sun» |
| 13,54–19,92 | Cartoon 3D · skater bajo la lluvia | «Tu producto en cualquier mundo» | «Rain on the ramp, I don't fall, I just flip» |
| 19,92–28,33 | Calle real · andando a 1× | «Más contenido, menos producción» | «Walk with the weight, one step, here I come» |
| **28,33** | Golpe: ráfaga de la zapatilla | — | «One pair, four worlds, own the lane / never the same» |
| 30,83–36,29 | Cartón: swoosh oficial, JUST DO IT y llamada | — | Estribillo |

- **Duración:** de 48 s en bruto a 36,3 s.
- **Mezcla:** −14,6 LUFS y pico de −1,2 dBFS.
- **Voces:** las cinco frases salen limpias en Whisper.

## Qué se corrigió por el camino
1. La v1, a 48 s y con una canción que no estaba hecha para el clip, era lenta. Se arregló con rampas y con una canción compuesta para este montaje.
2. Los planos del chico andando se veían rotos acelerados, así que se dejaron a 1×.
3. La canción salió de 67 s, rapeando seguido. Se separó la voz y cada frase se movió pulsos enteros a los huecos.
4. Bajar la música 6 dB no bastaba; con 14 dB, sí.
5. Al pasar a AAC el pico superaba 0 dBFS, así que se añadió un limitador.

`project.json` es el proyecto de montaje de este caso. Las rutas son relativas a la carpeta del reel.
