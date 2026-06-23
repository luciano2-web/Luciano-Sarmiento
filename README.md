# 🐱 GatoGPT Félix para Colab

Proyecto de chat local estilo ChatGPT para Google Colab, con personalidad felina de **Félix / GatoGPT** y comandos especiales para crear imagen y video sin API externa.

## Qué incluye

- Chat local con `Qwen/Qwen3-0.6B` usando `transformers`.
- Personalidad de Félix basada en las notas del usuario: gato curioso, amistoso, ronroneante, protector y educativo.
- Interfaz web estilo ChatGPT con Gradio.
- Comando `@gatimage` para generar una imagen local con `stabilityai/sd-turbo`.
- Comando `@gativeo` para generar un video local simple uniendo imágenes generadas en Colab.
- Carga diferida del modelo de imagen: solo se descarga cuando usas `@gatimage` o `@gativeo`.

> Nota: aunque no usa API, Colab necesita internet para descargar librerías y modelos desde Hugging Face. En cuenta gratuita puede tardar o fallar si no hay GPU/RAM suficiente.

## Cómo usarlo en Google Colab

1. Abre un notebook nuevo en Colab.
2. Si puedes, activa GPU gratuita: `Entorno de ejecución → Cambiar tipo de entorno de ejecución → T4 GPU`.
3. Copia el contenido de [`gatogpt_felix_colab.py`](gatogpt_felix_colab.py) en una celda.
4. Ejecuta primero la línea de instalación que está comentada al inicio del archivo:

```python
!pip install -q -U transformers accelerate torch diffusers safetensors gradio pillow imageio imageio-ffmpeg
```

5. Ejecuta el resto del código.
6. Abre el enlace público de Gradio que imprime Colab.

## Comandos dentro del chat

### Chat normal

```text
Explícame fracciones como si estuviera en sexto grado.
```

### Imagen local

```text
@gatimage Félix estudiando matemáticas en una biblioteca mágica
```

### Video local simple

```text
@gativeo Félix caminando por una biblioteca futurista con libros brillantes
```

## Modelos usados

- Texto: `Qwen/Qwen3-0.6B`.
- Imagen/video simple: `stabilityai/sd-turbo`.

El video se genera localmente como una secuencia de imágenes porque los modelos reales de texto-a-video suelen ser demasiado pesados para Colab gratuito.
