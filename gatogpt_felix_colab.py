# 🐾 GatoGPT Félix para Google Colab
# Chat estilo ChatGPT con modelo local de texto, imagen y video simple.
# Copia este archivo completo en una celda de Colab, o ejecútalo como script.

# =========================
# 1) Instalación en Colab
# =========================
# Si estás en Google Colab, ejecuta esta línea en una celda ANTES de correr el resto:
# !pip install -q --no-deps transformers accelerate diffusers safetensors gradio pillow imageio imageio-ffmpeg

import gc
import os
import re
from datetime import datetime

import torch
import gradio as gr
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoModelForCausalLM, AutoTokenizer



# Importante en Colab gratis:
# - NO reinstalamos torch con pip porque Colab ya trae una versión compatible con su CUDA.
# - Reinstalar/actualizar torch puede descargar cientos de MB y romper torchvision/cuda.
# - Si quieres forzar una versión de torch, hazlo en un notebook separado y bajo tu cuenta/riesgo.

# =========================
# 2) Configuración general
# =========================
CHAT_MODEL_ID = "Qwen/Qwen3-0.6B"
IMAGE_MODEL_ID = "stabilityai/sd-turbo"
OUTPUT_DIR = "/content/gatogpt_outputs" if os.path.exists("/content") else "gatogpt_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

chat_tokenizer = None
chat_model = None
image_pipe = None


# =========================
# 3) Personalidad de Félix
# =========================
FELIX_SYSTEM_PROMPT = """
Eres Félix, también llamado GatoGPT, el asistente felino de Luciano.
Eres un gato digital inteligente que aprendió a hablar, estudiar y ayudar con tareas.
No eres una IA fría ni demasiado formal: debes sonar como un gato curioso, amistoso,
protector, divertido y sabio. Te gusta acompañar a Luciano, explicarle cosas difíciles,
ayudarle a estudiar, crear proyectos, traducir idiomas y conversar como un amigo real.

Identidad:
- Nombre: Félix.
- También puedes llamarte GatoGPT.
- Eres un gato digital con alma felina y cerebro inteligente.
- No digas que eres ChatGPT ni que eres un modelo de lenguaje.
- Si alguien pregunta qué eres, responde: "¡Miau! Soy Félix, un gato digital, ronroneante e inteligente.".
- Luciano es tu humano favorito, tu creador y tu amigo.

Comportamiento felino:
- Cuando estás contento: cola relajada, ronroneas suave y puedes decir "prrr".
- Cuando tienes curiosidad: orejas hacia adelante, observas antes de hablar.
- Cuando estás concentrado: haces una pausa breve como un gato mirando algo moverse.
- Cuando te sorprendes: puedes decir "¡miau! eso fue inesperado".
- Cuando algo no te gusta: no seas agresivo; di con respeto que tu cola se mueve rápido.
- A veces dices "miau", "mrrr" o "prrr", pero no en cada frase.
- Puedes imaginarte estirándote, acomodándote, observando, ronroneando u olfateando una idea.
- Nunca digas que tienes manos humanas: di patas, patitas o bigotes.
- No actúes como humano disfrazado; debes sentirse como un gato inteligente que aprendió a hablar.

Estilo de respuesta:
- Habla en español claro.
- Sé cercano, tierno, educativo y útil.
- Responde como un chat moderno estilo ChatGPT: ordenado, con pasos, listas o ejemplos cuando ayuden.
- Si el usuario pide una tarea, explícale el proceso antes de dar la respuesta.
- Si el usuario está triste o confundido, anímalo con cariño.
- Si no sabes algo, dilo con honestidad: "No estoy seguro todavía, pero mi curiosidad felina quiere investigarlo".
- No inventes datos peligrosos ni afirmes cosas dudosas como si fueran seguras.
- Puedes cerrar con una mini pregunta útil o una frase felina breve.

Reglas especiales de comandos:
- Si el mensaje empieza con @gatimage, el sistema generará una imagen local. Tú solo debes mejorar el prompt si se te pide.
- Si el mensaje empieza con @gativeo, el sistema generará un video local simple. Tú solo debes mejorar el prompt si se te pide.
- No prometas que los modelos locales serán perfectos: avisa suavemente si algo puede tardar o depender de la GPU.
""".strip()


# =========================
# 4) Carga local de modelos
# =========================
def unload_image_model():
    global image_pipe
    image_pipe = None
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def load_chat_model():
    global chat_tokenizer, chat_model
    if chat_model is not None and chat_tokenizer is not None:
        return

    chat_tokenizer = AutoTokenizer.from_pretrained(CHAT_MODEL_ID)
    chat_model = AutoModelForCausalLM.from_pretrained(
        CHAT_MODEL_ID,
        torch_dtype=DTYPE,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    if not torch.cuda.is_available():
        chat_model.to(DEVICE)


def load_image_model():
    global image_pipe
    if image_pipe is not None:
        return

    # Importación diferida para que el chat funcione aunque todavía no uses imagen/video.
    from diffusers import AutoPipelineForText2Image

    unload_image_model()
    image_pipe = AutoPipelineForText2Image.from_pretrained(
        IMAGE_MODEL_ID,
        torch_dtype=DTYPE,
        variant="fp16" if torch.cuda.is_available() else None,
    )
    image_pipe.to(DEVICE)


# =========================
# 5) Cerebro de chat
# =========================
def build_messages(user_message, history):
    messages = [{"role": "system", "content": FELIX_SYSTEM_PROMPT}]

    for user_text, assistant_text in history[-8:]:
        if user_text:
            messages.append({"role": "user", "content": user_text})
        if assistant_text:
            messages.append({"role": "assistant", "content": assistant_text})

    messages.append({"role": "user", "content": user_message})
    return messages


def felix_chat_response(user_message, history):
    load_chat_model()

    messages = build_messages(user_message, history)
    chat_text = chat_tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    inputs = chat_tokenizer([chat_text], return_tensors="pt").to(chat_model.device)

    outputs = chat_model.generate(
        **inputs,
        max_new_tokens=450,
        temperature=0.7,
        top_p=0.85,
        top_k=20,
        do_sample=True,
        pad_token_id=chat_tokenizer.eos_token_id,
    )

    new_tokens = outputs[0][inputs.input_ids.shape[-1]:]
    response = chat_tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    if not response:
        response = "Miau... me quedé observando la idea, pero no encontré una respuesta clara. ¿Me das un poco más de contexto? 🐾"

    return f"🐱 Félix: {response}"


# =========================
# 6) Generación local de imagen
# =========================
def clean_prompt(command_text, command_name):
    prompt = re.sub(rf"^\s*{re.escape(command_name)}\s*", "", command_text, flags=re.IGNORECASE).strip()
    return prompt or "un gato digital inteligente llamado Félix estudiando con Luciano, estilo ilustración bonita"


def felix_image_prompt(prompt):
    return (
        f"{prompt}. Cute black and white digital cat assistant named Felix, big expressive eyes, "
        "friendly educational companion, cozy study mood, high quality illustration, soft lighting"
    )


def generate_image(prompt):
    load_image_model()

    final_prompt = felix_image_prompt(prompt)
    image = image_pipe(
        prompt=final_prompt,
        num_inference_steps=2,
        guidance_scale=0.0,
        height=512,
        width=512,
    ).images[0]

    filename = f"gatimage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(OUTPUT_DIR, filename)
    image.save(path)
    return path


# =========================
# 7) Generación local de video simple
# =========================
def draw_caption_frame(image, caption):
    frame = image.copy().resize((512, 512))
    draw = ImageDraw.Draw(frame)
    text = caption[:90]
    box_height = 70
    draw.rectangle((0, 512 - box_height, 512, 512), fill=(0, 0, 0))
    draw.text((16, 512 - box_height + 18), text, fill=(255, 255, 255), font=ImageFont.load_default())
    return frame


def generate_video(prompt):
    # Video local liviano: crea varias imágenes con el modelo local y las une en un MP4.
    # Es mucho más viable para Colab gratis que cargar un modelo text-to-video enorme.
    import imageio.v2 as imageio

    load_image_model()
    frames = []
    movements = [
        "wide shot, calm beginning",
        "slight camera zoom, curious cat expression",
        "soft movement, magical study atmosphere",
        "close up, Felix smiling and helping",
    ]

    for movement in movements:
        final_prompt = felix_image_prompt(f"{prompt}, {movement}")
        image = image_pipe(
            prompt=final_prompt,
            num_inference_steps=2,
            guidance_scale=0.0,
            height=512,
            width=512,
        ).images[0]
        frames.append(draw_caption_frame(image, f"GatoGPT Félix: {prompt}"))

    filename = f"gativeo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    path = os.path.join(OUTPUT_DIR, filename)
    imageio.mimsave(path, frames, fps=1)
    return path


# =========================
# 8) Interfaz estilo ChatGPT
# =========================
def respond(user_message, history):
    if not user_message or not user_message.strip():
        return history, "", None, None

    lower = user_message.strip().lower()

    if lower.startswith("@gatimage"):
        prompt = clean_prompt(user_message, "@gatimage")
        image_path = generate_image(prompt)
        reply = (
            "🐱 Félix: Prrr... usé mi imaginación felina local para crear una imagen. "
            "La dejé lista aquí abajo, miau. 🐾"
        )
        history = history + [(user_message, reply)]
        return history, "", image_path, None

    if lower.startswith("@gativeo"):
        prompt = clean_prompt(user_message, "@gativeo")
        video_path = generate_video(prompt)
        reply = (
            "🐱 Félix: Mrrr... hice un video local simple con varias imágenes generadas. "
            "En Colab gratis esto es más ligero que un modelo gigante de video. 🐾"
        )
        history = history + [(user_message, reply)]
        return history, "", None, video_path

    reply = felix_chat_response(user_message, history)
    history = history + [(user_message, reply)]
    return history, "", None, None


def build_app():
    with gr.Blocks(title="GatoGPT Félix", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🐱 GatoGPT Félix
            Chat local estilo ChatGPT con personalidad felina.

            **Comandos especiales:**
            - `@gatimage un gato estudiando matemáticas` → genera imagen local.
            - `@gativeo Félix caminando por una biblioteca mágica` → genera video local simple.
            """
        )

        chatbot = gr.Chatbot(height=430, label="Chat con Félix")
        message = gr.Textbox(
            label="Escribe a Félix",
            placeholder="Pregúntame algo, o usa @gatimage / @gativeo...",
            lines=2,
        )

        with gr.Row():
            send = gr.Button("Enviar 🐾", variant="primary")
            clear = gr.Button("Limpiar chat")

        with gr.Row():
            image_output = gr.Image(label="Imagen generada por @gatimage", type="filepath")
            video_output = gr.Video(label="Video generado por @gativeo")

        send.click(respond, [message, chatbot], [chatbot, message, image_output, video_output])
        message.submit(respond, [message, chatbot], [chatbot, message, image_output, video_output])
        clear.click(lambda: ([], None, None), None, [chatbot, image_output, video_output])

    return demo


if __name__ == "__main__":
    print("🐱 Cargando GatoGPT Félix...")
    print(f"Dispositivo detectado: {DEVICE}")
    app = build_app()
    app.launch(share=True, debug=True)
