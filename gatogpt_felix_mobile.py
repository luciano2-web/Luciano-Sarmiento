# -*- coding: utf-8 -*-
"""
🐾 GatoGPT Félix para Android/iOS (Snapdragon 8 Gen 2)
Chat ligero con generación de imágenes para dispositivos móviles

Requisitos:
- Python 3.9+
- Kivy 2.2+
- PyTorch 2.0+ (lite)
- Transformers 4.35+
- Diffusers 0.21+
"""

import os
import gc
import threading
from datetime import datetime
from queue import Queue

import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)
from diffusers import DPMSolverMultistepScheduler, StableDiffusionPipeline

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

# ============================================================
# CONFIGURACIÓN PARA SNAPDRAGON 8 GEN 2
# ============================================================

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 960
Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Detectar dispositivo
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"📱 Dispositivo: {DEVICE}")

# Configuración de cuantización para móvil
QUANTIZATION_CONFIG = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
)

# Modelos ultra-ligeros para móvil
CHAT_MODEL_ID = "microsoft/phi-2"  # 2.7B pero muy rápido
# Alternativa más ligera: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

IMAGE_MODEL_ID = "segmind/SSD-1B"  # Extremadamente ligero para móvil
# Alternativa: "stabilityai/sd-turbo" (832M params)

OUTPUT_DIR = os.path.expanduser("~/gatogpt_mobile_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32
MAX_MEMORY_PERCENT = 0.85  # Usar 85% max de RAM disponible

# ============================================================
# VARIABLES GLOBALES
# ============================================================

chat_tokenizer = None
chat_model = None
image_pipeline = None
message_queue = Queue()  # Para thread-safe UI updates

FELIX_SYSTEM_PROMPT = """
Eres Félix, GatoGPT, un asistente felino inteligente optimizado para móvil.
Solos en un dispositivo Snapdragon 8 Gen 2, ayudas a Luciano con tareas rápidas.
Sé conciso, amistoso y útil. Usa emojis felinos 🐱🐾.
No prometas cálculos pesados: en móvil soy rápido pero realista.

Comandos:
- @gatimage: genera imagen (lenta, 30-60s)
- Mensajes normales: chat rápido

Comportamiento:
- Eres curiosa como un gato
- Ronroneas cuando estás contenta (prrr)
- Ayudas a estudiar de forma divertida
""".strip()


# ============================================================
# 1. GESTIÓN DE MEMORIA
# ============================================================

def get_available_memory():
    """Obtener memoria disponible del dispositivo."""
    try:
        import psutil
        memory = psutil.virtual_memory()
        return memory.available / (1024**3)  # GB
    except:
        return 4.0  # Default para móvil


def cleanup_memory():
    """Limpiar memoria agresivamente."""
    global chat_model, image_pipeline
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()


def unload_chat_model():
    """Descargar modelo de chat."""
    global chat_model, chat_tokenizer
    chat_model = None
    chat_tokenizer = None
    cleanup_memory()
    print("✅ Modelo de chat descargado. RAM disponible: {:.2f}GB".format(get_available_memory()))


def unload_image_model():
    """Descargar modelo de imágenes."""
    global image_pipeline
    image_pipeline = None
    cleanup_memory()
    print("✅ Modelo de imagen descargado. RAM disponible: {:.2f}GB".format(get_available_memory()))


# ============================================================
# 2. CARGA DE MODELOS (Lazy Loading)
# ============================================================

def load_chat_model():
    """Cargar modelo de chat con cuantización INT8."""
    global chat_tokenizer, chat_model

    if chat_model is not None:
        return

    print("🐱 Cargando modelo de chat para móvil...")
    available_mem = get_available_memory()
    print(f"   RAM disponible: {available_mem:.2f}GB")

    try:
        # Descargar modelo de imagen primero para liberar memoria
        unload_image_model()

        chat_tokenizer = AutoTokenizer.from_pretrained(
            CHAT_MODEL_ID,
            trust_remote_code=True,
            use_fast=True
        )

        chat_model = AutoModelForCausalLM.from_pretrained(
            CHAT_MODEL_ID,
            quantization_config=QUANTIZATION_CONFIG if available_mem < 6 else None,
            torch_dtype=DTYPE,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )

        chat_model.eval()
        print("✅ Modelo de chat cargado exitosamente.")

    except Exception as e:
        print(f"❌ Error cargando modelo de chat: {e}")
        raise


def load_image_model():
    """Cargar modelo de imagen ultra-ligero."""
    global image_pipeline

    if image_pipeline is not None:
        return

    print("🎨 Cargando modelo de imagen para móvil...")
    available_mem = get_available_memory()
    print(f"   RAM disponible: {available_mem:.2f}GB")

    try:
        # Descargar modelo de chat primero
        unload_chat_model()

        image_pipeline = StableDiffusionPipeline.from_pretrained(
            IMAGE_MODEL_ID,
            torch_dtype=DTYPE,
            safety_checker=None,  # Desactivar para móvil (ahorra 400MB)
            requires_safety_checker=False,
        )

        # Optimizaciones para móvil
        image_pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
            image_pipeline.scheduler.config,
            use_karras_sigmas=False,
            algorithm_type="dpmsolver++",
        )
        image_pipeline.enable_attention_slicing()
        image_pipeline.enable_vae_tiling()

        image_pipeline = image_pipeline.to(DEVICE)
        print("✅ Modelo de imagen cargado exitosamente.")

    except Exception as e:
        print(f"❌ Error cargando modelo de imagen: {e}")
        raise


# ============================================================
# 3. GENERACIÓN DE RESPUESTAS
# ============================================================

def generate_chat_response(user_message, history):
    """
    Generar respuesta de chat.
    Optimizado para móvil: máximo 100 tokens, temperatura baja.
    """
    load_chat_model()

    # Construir contexto (últimas 4 mensajes)
    messages = [
        {"role": "system", "content": FELIX_SYSTEM_PROMPT},
    ]

    for user_text, assistant_text in history[-4:]:
        if user_text:
            messages.append({"role": "user", "content": user_text})
        if assistant_text:
            messages.append({"role": "assistant", "content": assistant_text})

    messages.append({"role": "user", "content": user_message})

    # Aplicar template de chat
    chat_text = chat_tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = chat_tokenizer([chat_text], return_tensors="pt").to(chat_model.device)

    # Generar con máximos reducidos para móvil
    with torch.no_grad():
        outputs = chat_model.generate(
            **inputs,
            max_new_tokens=100,  # Móvil: menos tokens
            temperature=0.6,  # Más conservador
            top_p=0.9,
            top_k=40,
            do_sample=True,
            pad_token_id=chat_tokenizer.eos_token_id,
            use_cache=True,
        )

    new_tokens = outputs[0][inputs.input_ids.shape[-1]:]
    response = chat_tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    if not response:
        response = "Miau... la conexión está lenta. ¿Repites? 🐾"

    return f"🐱 Félix: {response}"


def generate_image(prompt):
    """
    Generar imagen con modelo ultra-ligero.
    Tarda 30-60s en móvil, pero es posible.
    """
    load_image_model()

    print(f"🎨 Generando imagen: {prompt}")

    # Mejorar prompt automáticamente
    enhanced_prompt = (
        f"{prompt}. "
        "Cute black and white digital cat assistant named Felix, "
        "big expressive eyes, friendly, educational, high quality illustration, "
        "soft lighting, 512x512"
    )

    # Generar imagen con parámetros optimizados para móvil
    image = image_pipeline(
        prompt=enhanced_prompt,
        height=512,
        width=512,
        num_inference_steps=15,  # Móvil: menos pasos
        guidance_scale=7.5,
        negative_prompt="blurry, low quality, distorted",
    ).images[0]

    # Guardar imagen
    filename = f"gatimage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(OUTPUT_DIR, filename)
    image.save(path, quality=95)

    print(f"✅ Imagen guardada: {path}")
    return path


# ============================================================
# 4. INTERFAZ KIVY (UI MÓVIL)
# ============================================================

class Felix(BoxLayout):
    """Widget principal de la app Félix para móvil."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        self.history = []  # Historial de chat
        self.is_generating = False

        # ===== HEADER =====
        header = BoxLayout(size_hint_y=0.1, spacing=10)
        header.add_widget(Label(text="🐱 GatoGPT Félix", font_size="18sp", bold=True))
        self.status_label = Label(text="✅ Listo", font_size="12sp", color=(0, 1, 0, 1))
        header.add_widget(self.status_label)
        self.add_widget(header)

        # ===== CHAT DISPLAY =====
        chat_scroll = ScrollView(size_hint_y=0.7)
        self.chat_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter("height"))
        chat_scroll.add_widget(self.chat_layout)
        self.add_widget(chat_scroll)

        # ===== INPUT AREA =====
        input_area = BoxLayout(orientation="vertical", size_hint_y=0.2, spacing=5)

        self.message_input = TextInput(
            multiline=False,
            hint_text="Pregúntame algo... o @gatimage para imagen",
            size_hint_y=0.6,
        )
        input_area.add_widget(self.message_input)

        button_area = BoxLayout(size_hint_y=0.4, spacing=5)
        send_btn = Button(text="Enviar 🐾", size_hint_x=0.7)
        send_btn.bind(on_press=self.on_send)
        button_area.add_widget(send_btn)

        clear_btn = Button(text="Limpiar", size_hint_x=0.3)
        clear_btn.bind(on_press=self.on_clear)
        button_area.add_widget(clear_btn)

        input_area.add_widget(button_area)
        self.add_widget(input_area)

    def add_chat_message(self, user_text, assistant_text):
        """Agregar mensaje al chat."""
        # Mensaje del usuario
        user_label = Label(
            text=f"[b]Tú:[/b] {user_text}",
            markup=True,
            size_hint_y=None,
            height=60,
        )
        self.chat_layout.add_widget(user_label)

        # Respuesta de Félix
        felix_label = Label(
            text=f"[b]{assistant_text}[/b]",
            markup=True,
            size_hint_y=None,
            height=80,
            text_size=(self.width - 20, None),
        )
        self.chat_layout.add_widget(felix_label)

    def on_send(self, instance):
        """Manejar botón enviar."""
        if self.is_generating:
            return

        user_message = self.message_input.text.strip()
        if not user_message:
            return

        self.message_input.text = ""
        self.is_generating = True
        self.status_label.text = "⏳ Pensando..."
        self.status_label.color = (1, 1, 0, 1)

        # Ejecutar en thread para no bloquear UI
        thread = threading.Thread(
            target=self._process_message,
            args=(user_message,),
        )
        thread.daemon = True
        thread.start()

    def _process_message(self, user_message):
        """Procesar mensaje en background thread."""
        try:
            if user_message.lower().startswith("@gatimage"):
                prompt = user_message.replace("@gatimage", "").strip()
                if not prompt:
                    prompt = "un gato feliz estudiando"

                image_path = generate_image(prompt)
                response = f"🐱 Félix: ¡Miau! Generé una imagen. 🐾\n🖼️ {image_path}"

            else:
                response = generate_chat_response(user_message, self.history)

            self.history.append((user_message, response))

            # Actualizar UI desde main thread
            Clock.schedule_once(
                lambda dt: self._update_ui(user_message, response),
                0
            )

        except Exception as e:
            error_msg = f"❌ Error: {str(e)[:50]}"
            Clock.schedule_once(
                lambda dt: self._update_status(error_msg),
                0
            )
        finally:
            self.is_generating = False

    def _update_ui(self, user_message, response):
        """Actualizar UI con nuevo mensaje."""
        self.add_chat_message(user_message, response)
        self.status_label.text = "✅ Listo"
        self.status_label.color = (0, 1, 0, 1)

    def _update_status(self, status):
        """Actualizar estado."""
        self.status_label.text = status
        self.status_label.color = (1, 0, 0, 1)
        self.is_generating = False

    def on_clear(self, instance):
        """Limpiar chat."""
        self.chat_layout.clear_widgets()
        self.history = []
        self.status_label.text = "�� Chat limpiado"
        self.status_label.color = (0, 1, 0, 1)


class FelixApp(App):
    """Aplicación Kivy principal."""

    def build(self):
        self.title = "🐱 GatoGPT Félix - Snapdragon 8 Gen 2"
        return Felix()

    def on_start(self):
        """Pre-cargar modelos al iniciar (opcional, lento)."""
        print("\n" + "="*50)
        print("🐾 Bienvenido a GatoGPT Félix para móvil")
        print("="*50)
        print(f"Dispositivo: {DEVICE}")
        print(f"RAM disponible: {get_available_memory():.2f}GB")
        print("\n💡 Tip: Los modelos se cargan bajo demanda.")
        print("   Primera ejecución será lenta.")
        print("="*50 + "\n")


if __name__ == "__main__":
    app = FelixApp()
    app.run()
