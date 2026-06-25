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
>
> **Importante:** no instales ni actualices `torch` en Colab. Colab ya trae PyTorch compatible con su CUDA; actualizarlo puede descargar muchos GB y causar conflictos con `torchvision`, `cuda-toolkit`, `cudf` y otras librerías preinstaladas. Por eso la instalación recomendada usa `--no-deps`: instala las librerías principales sin dejar que `pip` cambie PyTorch/CUDA.

## Cómo usarlo en Google Colab

1. Abre un notebook nuevo en Colab.
2. Si puedes, activa GPU gratuita: `Entorno de ejecución → Cambiar tipo de entorno de ejecución → T4 GPU`.
3. Copia el contenido de [`gatogpt_felix_colab.py`](gatogpt_felix_colab.py) en una celda.
4. Ejecuta primero la línea de instalación que está comentada al inicio del archivo. Esta línea evita reinstalar `torch` para no romper el entorno gratuito de Colab:

```python
!pip install -q --no-deps transformers accelerate diffusers safetensors gradio pillow imageio imageio-ffmpeg
```

5. Ejecuta el resto del código.
6. Abre el enlace público de Gradio que imprime Colab.


### Si `pip` descargó muchos archivos de CUDA o cambió `torch`

Si ves errores como `torchvision ... requires torch==... but you have torch ...` o descargas de cientos de MB, tu sesión de Colab ya quedó mezclada. Haz esto:

1. Ve a `Entorno de ejecución → Reiniciar sesión` o, mejor, `Entorno de ejecución → Desconectar y eliminar entorno de ejecución`.
2. Vuelve a ejecutar la instalación segura:

```python
!pip install -q --no-deps transformers accelerate diffusers safetensors gradio pillow imageio imageio-ffmpeg
```

3. Luego ejecuta la celda del script.

No ejecutes `pip install torch`, `pip install -U torch` ni una instalación sin `--no-deps` si quieres conservar el entorno gratuito de Colab estable.

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

## Solución de errores comunes

### `IndentationError: unexpected indent` en `image_pipe = None`

Ese error suele pasar cuando se copia solo una parte del código y se pierde la línea anterior:

```python
def unload_image_model():
```

El bloque correcto debe quedar exactamente así, con `def` pegado al margen izquierdo y las líneas internas con 4 espacios:

```python
def unload_image_model():
    global image_pipe
    image_pipe = None
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
```

Si aparece ese error en Colab, borra la celda 2 completa y vuelve a copiar el archivo completo desde el inicio. No copies desde una captura ni desde texto con numeración de líneas.
