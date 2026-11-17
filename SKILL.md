---
name: un-producto-cuatro-mundos
description: Crea el reel vertical «Un producto, cuatro mundos»: el mismo producto real viaja por cuatro mundos con estilos distintos (mecha 3D, anime, cartoon 3D, foto real…), cada uno con su avatar que dice una frase en voz en off, y termina en una ráfaga del producto y un cartón con llamada a la acción. Da la idea que vende, el guion, los prompts de personajes y escenas para cualquier generador (ChatGPT/Sora, Veo/Flow, Kling, Seedance, Dreamina), el montaje con rampas de velocidad a pulso, la canción con letra que no pisa la voz, el cartón y el copy de Instagram. Úsala cuando pidan un anuncio o reel de producto con personajes o avatares de IA, «el producto en varios estilos o mundos», un spec ad para una marca hecho con IA, o rehacer el reel «un producto, cuatro mundos» con otro producto.
---

# Un producto, cuatro mundos

## La idea que vende
A una marca no le vendes un vídeo: le vendes **un sistema**. El mismo producto, idéntico, aparece en cuatro mundos que no tienen nada que ver (un guerrero mecánico, un anime, un cartoon 3D y la calle real), y cada mundo tiene su propio protagonista. El mensaje cabe en cinco frases:

> «Un producto. Cuatro mundos. Un estilo para cada historia. Tu producto en cualquier mundo. Más contenido, menos producción.»

Funciona por tres motivos:
1. **El producto es el hilo.** Todo cambia (estilo, personaje, luz) menos el producto, así que el ojo lo sigue de un mundo a otro.
2. **Va de la fantasía a la realidad.** El último mundo es foto real, y justo después llega la ráfaga del producto: la fantasía engancha y la realidad vende.
3. **Habla al cliente, no al público.** «Tu producto en cualquier mundo» y «más contenido, menos producción» se dirigen a quien paga anuncios. Es una pieza de portafolio que se explica sola.

## Qué sale al final
- Reel 9:16, 1080×1920, de 30 a 40 s, con −14 LUFS y el pico por debajo de −1 dBFS.
- 4 escenas de mundos (de 10 s en bruto; entre 6 y 8,5 s después de las rampas) → ráfaga del producto en el golpe de la canción → cartón con logo y llamada a la acción.
- Canción con letra en el idioma que se pida, cuyas frases nunca pisan la voz en off.
- Copy de Instagram: descripción, comentario fijado y hashtags.

## Proceso (cada paso termina con el visto bueno del usuario)
1. **Brief.** Pide estos datos:
   - el producto, con fotos reales u oficiales y la vista que mejor lo identifica;
   - la marca y su logo oficial (en archivo, nunca generado);
   - el idioma de la voz y el de la canción;
   - el generador de imagen y el de vídeo que tiene el usuario;
   - la llamada final («Comenta X», «Enlace en el comentario», «Guárdalo»…).
2. **Cuatro mundos.** Elígelos en `references/mundos.md`. Reglas:
   - de más fantasía a más real; el cuarto, siempre foto real;
   - un **color de acento común** en los cuatro (en Nike, verde lima #CEFF00), que aparece en luces, ropa o detalles;
   - cada mundo con una **acción propia del producto** (con zapatillas: saltar, patinar, andar).
3. **Guion.** Sigue `references/guion.md`: 5 frases de voz y 5 planos por escena. Las frases se adaptan al producto y al idioma; la estructura no se toca.
4. **Hojas de personaje.** Usa las plantillas de `references/prompts.md`. Primero una imagen por mundo, con el personaje llevando o usando el producto. Se aprueban **antes** de generar vídeo, porque cada imagen es el fotograma de partida de su escena.
5. **Escenas de vídeo.** Usa la plantilla de escena de `references/prompts.md`. Antes de cada generación de pago di el prompt y el coste, y espera el visto bueno. Revisa cada toma con la lista de rechazo; con el producto deformado, la toma no vale.
6. **Montaje y música.** Sigue `references/montaje-y-musica.md` con `scripts/reel.py`:
   1. Mide dónde está la voz y aplica las rampas sin la canción, y enseña ese montaje.
   2. Genera la canción con letra.
   3. Recoloca la letra en los huecos de la voz.
   4. Ajusta los cortes al pulso y baja la música 14 dB bajo la voz.
7. **Cierre y copy.** Sigue `references/cierre-y-copy.md`: cartón a pulso (plantilla Remotion en `plantillas/cierre/`), descripción del post, comentario fijado y hashtags.
8. **Revisión final**:
   - hoja de fotogramas;
   - Whisper sobre la mezcla, donde todas las frases de voz deben salir limpias;
   - −14 LUFS;
   - abrir el render en el reproductor del usuario.

## Reglas que no se rompen
- **El producto es el real.** Se parte de sus fotos. Si una toma cambia la forma, los colores, el logo o el número de piezas, se repite o se corta.
- **Logos y eslóganes de marca, solo de archivos oficiales.** No se redibujan ni se generan. Si un plano generado trae un logo mal escrito o texto inventado, se corta.
- **Personajes de diseño propio.** No se imitan personajes, actores ni artistas existentes, ni el estilo exacto de una serie concreta.
- **La voz en off va siempre a 1×.** Las rampas solo aceleran lo que no tiene voz. A los planos de alguien andando no se les aplica rampa.
- **La música manda en los cortes y la letra nunca pisa la voz.**
- **Créditos:** se pregunta antes de cada generación de pago, con el prompt y el coste.
- **Si es un spec ad sin encargo**, el copy lo dice: «Proyecto personal de portafolio. Sin afiliación con [marca]».

## Archivos
| Archivo | Para qué |
|---|---|
| `references/guion.md` | Línea de tiempo, las 5 frases, los 5 planos por escena y variantes por idioma o producto |
| `references/mundos.md` | Los 4 mundos del caso Nike, catálogo de mundos y acción por tipo de producto |
| `references/prompts.md` | Plantillas de hoja de personaje, escena de 10 s y ráfaga de producto, y lista de rechazo |
| `references/montaje-y-musica.md` | Rampas, canción y mezcla con `scripts/reel.py` |
| `references/cierre-y-copy.md` | Cartón final, llamadas a la acción y copy de Instagram |
| `scripts/reel.py` | `measure`, `song`, `ramps`, `music`, `assemble` (ffmpeg + Python, todo en local) |
| `plantillas/cierre/Cierre.tsx` | Cartón final en Remotion, con palabras que suben a pulso |
| `examples/nike/` | El caso completo de Nike, rellenado (`brief.md`, `project.json`) |
