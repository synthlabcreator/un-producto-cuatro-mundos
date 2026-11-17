# Un producto, cuatro mundos

**Skill para Claude**: el reel en el que el mismo producto viaja por cuatro mundos (mecha 3D, anime, cartoon 3D y calle real), cada uno con su avatar y su frase, y acaba en una ráfaga del producto. Trae la idea, el guion, los prompts, el montaje, la música y el copy.

> «Un producto. Cuatro mundos. Un estilo para cada historia. Tu producto en cualquier mundo. Más contenido, menos producción.»

*English below.*

---

## Español

### Qué trae
| | |
|---|---|
| **La idea que vende** | Por qué funciona: el producto es el hilo, el viaje va de la fantasía a la realidad y el mensaje habla a la marca |
| **Guion** | Línea de tiempo, las 5 frases de la voz en off y los 5 planos de cada escena |
| **Mundos** | Los 4 del caso Nike, un catálogo de 10 mundos y la acción que mejor enseña cada tipo de producto |
| **Prompts** | Hoja de personaje, escena de 10 s con voz, ráfaga del producto y lista de rechazo. Valen para ChatGPT, Veo/Flow, Kling, Seedance o Dreamina |
| **Montaje** | `scripts/reel.py`: rampas de velocidad que nunca tocan la voz y cortes al pulso de la canción |
| **Música** | Prompt de la canción con letra. La letra se recoloca para que no pise la voz y la música baja 14 dB bajo cada frase |
| **Cierre y copy** | Cartón en Remotion a pulso, llamadas a la acción, descripción, comentario fijado y hashtags |
| **Ejemplo** | El caso Nike completo, rellenado |

### Instalación
- **Claude Code:** copia la carpeta en `~/.claude/skills/un-producto-cuatro-mundos/`.
- **App de Claude:** comprime la carpeta en un .zip y súbela en *Ajustes → Capacidades → Skills*.
- **Para el montaje:** Python 3.10+, [ffmpeg](https://ffmpeg.org) en el PATH y `pip install -r requirements.txt`.

### Uso
Pídeselo a Claude:
> «Haz el reel *un producto, cuatro mundos* con [mi producto]. Aquí tienes sus fotos.»

Claude te pide el brief, propone los cuatro mundos y el guion, y te da los prompts de imagen y de vídeo para tu generador. Después monta lo que generes, con rampas, la canción y el cartón. Antes de cada paso de pago te pide permiso.

### Reglas
- El producto es el real; los logos, solo de archivos oficiales.
- Los personajes son de diseño propio.
- Si es un spec ad, se dice en el copy.

---

## English

### What it is
A Claude skill for the *one product, four worlds* reel: the exact same real product travels through four worlds (3D mech, anime, 3D cartoon, real street). Each world has its own avatar, who says one voice-over line to camera, and the reel ends on a product burst and an end card. The skill includes:
- the idea and why it sells;
- the script (5 lines, 5 shots per scene);
- a library of worlds;
- image and video prompts for any generator;
- local editing with speed ramps that never touch the voice, cut to the beat;
- a song whose lyrics never cover the voice;
- a Remotion end card and the Instagram copy.

### Install
Copy the folder to `~/.claude/skills/`, or zip it and upload it in the Claude app (*Settings → Capabilities → Skills*). The editing script needs Python 3.10+, ffmpeg and `pip install -r requirements.txt`.

### Use
Ask Claude: *"Make the one product, four worlds reel with [my product]. Here are its photos."*

---

Made by **SynthlabCreator** · MIT License
