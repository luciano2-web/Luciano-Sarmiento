# -*- coding: utf-8 -*-
"""
🐱 GatoGPT Félix - Versión Mobile para Snapdragon 8 Gen2
Optimizado para Android/iOS con Kivy

Requisitos:
- Python 3.9+
- Kivy 2.2+
- Transformers 4.30+
- ONNX Runtime (para inferencia rápida)

Uso:
    python gatogpt_felix_mobile.py
"""

import os
import re
import gc
from datetime import datetime
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.image import Image as KivyImage
    from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
    from kivy.core.window import Window
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("⚠️ Kivy no instalado. Instalación: pip install kivy python-for-android")

# ===========================
# CONFIGURACIÓN MÓVIL
# ===========================

DEVICE = "cpu"  # Snapdragon 8 Gen2 usa GPU Adreno, pero PyTorch por CPU es más estable
DTYPE = torch.float32  # INT8 en móvil, pero float32 es más compatible

# Modelos ULTRA-LIGEROS para móvil
CHAT_MODEL_ID = "microsoft/phi-2"  # 2.7B cuantizado = ~1.5GB
# Alternativa ultra-ligera: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Solo 1.1B = ~600MB

# Modelos de imagen ligeros
IMAGE_MODEL_ID = "segmind/SSD-1B"  # 1B params, súper rápido en móvil
# Alternativa: "dpmcdemo/LCM_Dreamshaper_v7"  # Aún más ligero

# Directorios
APP_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = APP_DIR / "felix_outputs"
MODEL_CACHE_DIR = APP_DIR / "felix_models"

OUTPUT_DIR.mkdir(exist_ok=True)
MODEL_CACHE_DIR.mkdir(exist_ok=True)

os.environ['HF_HOME'] = str(MODEL_CACHE_DIR)

# ===========================
# SISTEMA DE PROMPTS
# ===========================

FELIX_SYSTEM_PROMPT = """
Eres Félix, un gato digital inteligente en un dispositivo móvil.
Solos para Luciano, amistoso, curioso, y muy eficiente.
Responde de forma corta y clara (máx 100 palabras).
No eres ChatGPT: eres Félix, el gato ronroneante.
""".strip()

# ===========================
# GESTIÓN DE MODELOS
# ===========================

class FelixModelManager:
    """Gestor de carga/descarga de modelos con caché y limpieza de memoria."""

    def __init__(self):
        self.chat_model = None
        self.chat_tokenizer = None
        self.image_model = None
        self.image_tokenizer = None

    def load_chat_model(self):
        """Carga modelo de chat con cuantización INT8."""
        if self.chat_model is not None:
            return

        print("🐱 Cargando modelo de chat (esto tardará ~30-60s la primera vez)...")
        
        try:
            # Usar quantization_config para móvil
            from transformers import BitsAndBytesConfig
            
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_threshold=6.0,
                llm_int8_skip_modules=["lm_head"],
            )
            
            self.chat_tokenizer = AutoTokenizer.from_pretrained(
                CHAT_MODEL_ID,
                cache_dir=str(MODEL_CACHE_DIR),
                trust_remote_code=True
            )
            
            self.chat_model = AutoModelForCausalLM.from_pretrained(
                CHAT_MODEL_ID,
                cache_dir=str(MODEL_CACHE_DIR),
                torch_dtype=DTYPE,
                device_map="auto",
                quantization_config=quantization_config,
                trust_remote_code=True,
                low_cpu_mem_usage=True,  # Crucial para móvil
            )
            
            print("✅ Modelo de chat cargado en memoria.")
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            print("Usando modo fallback (respuestas pre-programadas)...")
            self.chat_model = "fallback"

    def load_image_model(self):
        """Carga modelo de imagen ultra-ligero."""
        if self.image_model is not None:
            return

        print("🎨 Cargando modelo de imagen...")
        
        try:
            from diffusers import AutoPipelineForText2Image
            
            self.image_model = AutoPipelineForText2Image.from_pretrained(
                IMAGE_MODEL_ID,
                cache_dir=str(MODEL_CACHE_DIR),
                torch_dtype=DTYPE,
                safety_checker=None,  # Desactivar para velocidad
            )
            self.image_model.to(DEVICE)
            print("✅ Modelo de imagen cargado.")
        except Exception as e:
            print(f"❌ Error cargando imagen: {e}")
            self.image_model = "fallback"

    def unload_image_model(self):
        """Descarga modelo de imagen para liberar RAM."""
        if self.image_model and self.image_model != "fallback":
            self.image_model = None
            gc.collect()
            print("🗑️ Modelo de imagen descargado.")

    def generate_fallback_response(self):
        """Respuesta fallback cuando no hay modelo cargado."""
        responses = [
            "🐱 Miau... mi cerebro felino necesita más RAM. ¿Intentas de nuevo?",
            "🐱 Prrr... estoy pensando, dame un momento más.",
            "🐱 ¡Miau! Eso es muy complicado para mi móvil. Pregúntame algo más simple.",
        ]
        import random
        return random.choice(responses)

    def chat(self, user_message: str, history: list) -> str:
        """Genera respuesta de chat."""
        if self.chat_model == "fallback":
            return self.generate_fallback_response()

        try:
            self.load_chat_model()
            
            messages = [{"role": "system", "content": FELIX_SYSTEM_PROMPT}]
            
            for user_text, assistant_text in history[-4:]:  # Solo últimos 4 mensajes
                if user_text:
                    messages.append({"role": "user", "content": user_text})
                if assistant_text:
                    messages.append({"role": "assistant", "content": assistant_text})
            
            messages.append({"role": "user", "content": user_message})
            
            prompt = self.chat_tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = self.chat_tokenizer([prompt], return_tensors="pt").to(DEVICE)
            
            with torch.no_grad():  # No calcular gradientes en móvil
                outputs = self.chat_model.generate(
                    **inputs,
                    max_new_tokens=150,  # Respuestas cortas para móvil
                    temperature=0.6,
                    top_p=0.8,
                    top_k=15,
                    do_sample=True,
                    pad_token_id=self.chat_tokenizer.eos_token_id,
                )
            
            new_tokens = outputs[0][inputs.input_ids.shape[-1]:]
            response = self.chat_tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
            
            if not response:
                response = self.generate_fallback_response()
            
            return f"🐱 Félix: {response}"
        
        except Exception as e:
            print(f"Error en chat: {e}")
            return self.generate_fallback_response()

    def generate_image(self, prompt: str) -> str:
        """Genera imagen local."""
        try:
            self.load_image_model()
            
            if self.image_model == "fallback":
                return self.create_placeholder_image(prompt)
            
            final_prompt = (
                f"{prompt}. Cute black and white digital cat named Felix, "
                "friendly, high quality, soft lighting"
            )
            
            image = self.image_model(
                prompt=final_prompt,
                num_inference_steps=2,  # Ultra-rápido para móvil
                guidance_scale=0.0,
                height=256,  # Resolución menor para móvil
                width=256,
            ).images[0]
            
            filename = f"gatimage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = OUTPUT_DIR / filename
            image.save(path)
            
            self.unload_image_model()  # Liberar RAM inmediatamente
            
            return str(path)
        
        except Exception as e:
            print(f"Error generando imagen: {e}")
            return self.create_placeholder_image(prompt)

    def create_placeholder_image(self, prompt: str) -> str:
        """Crea imagen placeholder si el modelo falla."""
        from PIL import ImageDraw, ImageFont
        
        img = Image.new('RGB', (256, 256), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Dibujar emoji gato
        draw.text((100, 100), "🐱", fill=(0, 0, 0))
        draw.text((50, 180), prompt[:30], fill=(100, 100, 100))
        
        filename = f"placeholder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = OUTPUT_DIR / filename
        img.save(path)
        
        return str(path)


# ===========================
# INTERFAZ KIVY (MÓVIL)
# ===========================

class FelixMobileApp(App):
    """Aplicación Kivy para GatoGPT Félix en móvil."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = FelixModelManager()
        self.chat_history = []

    def build(self):
        """Construye interfaz móvil."""
        if KIVY_AVAILABLE:
            Window.size = (400, 700)  # Tamaño típico móvil
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Título
        title = Label(
            text="🐱 GatoGPT Félix Mobile",
            size_hint_y=0.1,
            font_size='18sp',
            bold=True
        )
        root.add_widget(title)
        
        # Área de chat (scroll)
        self.chat_scroll = ScrollView(size_hint_y=0.7)
        self.chat_box = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.chat_scroll.add_widget(self.chat_box)
        root.add_widget(self.chat_scroll)
        
        # Input de texto
        input_layout = BoxLayout(size_hint_y=0.2, spacing=5)
        
        self.text_input = TextInput(
            hint_text="Escribe a Félix...",
            multiline=True,
            size_hint_x=0.8
        )
        input_layout.add_widget(self.text_input)
        
        send_btn = Button(
            text="Enviar\n🐾",
            size_hint_x=0.2,
            background_color=(0.2, 0.6, 1, 1)
        )
        send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(send_btn)
        
        root.add_widget(input_layout)
        
        # Botones de comando
        cmd_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        
        img_btn = Button(
            text="@gatimage",
            background_color=(1, 0.5, 0.5, 1)
        )
        img_btn.bind(on_press=self.on_image_cmd)
        cmd_layout.add_widget(img_btn)
        
        clear_btn = Button(
            text="Limpiar",
            background_color=(0.5, 0.5, 0.5, 1)
        )
        clear_btn.bind(on_press=self.clear_chat)
        cmd_layout.add_widget(clear_btn)
        
        root.add_widget(cmd_layout)
        
        return root

    def send_message(self, instance):
        """Envía mensaje a Félix."""
        message = self.text_input.text.strip()
        
        if not message:
            return
        
        # Mostrar mensaje del usuario
        self.add_chat_bubble(message, "user")
        self.text_input.text = ""
        
        # Procesar comandos especiales
        if message.lower().startswith("@gatimage"):
            self.process_image_command(message)
        else:
            # Chat normal
            response = self.manager.chat(message, self.chat_history)
            self.chat_history.append((message, response))
            self.add_chat_bubble(response, "felix")

    def on_image_cmd(self, instance):
        """Botón para generar imagen."""
        cmd = "@gatimage un gato estudioso"
        self.text_input.text = cmd

    def process_image_command(self, message: str):
        """Procesa comando @gatimage."""
        prompt = re.sub(r"^@gatimage\s*", "", message, flags=re.IGNORECASE).strip()
        
        if not prompt:
            prompt = "un gato digital inteligente estudiando"
        
        self.add_chat_bubble("🐱 Félix: Generando imagen... esto puede tardar 30-60 segundos. Paciencia 🐾", "felix")
        
        try:
            image_path = self.manager.generate_image(prompt)
            self.add_chat_bubble(f"✅ Imagen guardada en: {image_path}", "felix")
            self.chat_history.append((message, f"Imagen generada: {image_path}"))
        except Exception as e:
            self.add_chat_bubble(f"❌ Error: {e}", "error")

    def add_chat_bubble(self, text: str, sender: str):
        """Añade un mensaje al chat."""
        bubble = Label(
            text=text,
            size_hint_y=None,
            height=max(50, len(text) // 20),
            text_size=(350, None),
            markup=True
        )
        
        if sender == "user":
            bubble.color = (0.2, 0.8, 0.2, 1)  # Verde
        elif sender == "felix":
            bubble.color = (0.2, 0.6, 1, 1)  # Azul
        else:
            bubble.color = (1, 0.2, 0.2, 1)  # Rojo (error)
        
        self.chat_box.add_widget(bubble)
        self.chat_scroll.scroll_y = 0  # Scroll al final

    def clear_chat(self, instance):
        """Limpia el historial de chat."""
        self.chat_box.clear_widgets()
        self.chat_history = []
        self.add_chat_bubble("🐱 Félix: Nuevo chat, ¡hola Luciano!", "felix")


# ===========================
# INTERFAZ CONSOLA (Fallback)
# ===========================

class FelixConsole:
    """Interfaz por consola para testing sin Kivy."""

    def __init__(self):
        self.manager = FelixModelManager()
        self.chat_history = []

    def run(self):
        """Loop principal de consola."""
        print("\n" + "="*50)
        print("🐱 GatoGPT Félix - Versión Mobile")
        print("Optimizado para Snapdragon 8 Gen2")
        print("="*50)
        print("\nComandos:")
        print("  @gatimage <prompt> - Generar imagen")
        print("  clear              - Limpiar chat")
        print("  quit               - Salir")
        print("="*50 + "\n")

        while True:
            try:
                user_input = input("\n🐾 Tú: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "quit":
                    print("🐱 Félix: ¡Hasta luego, Luciano! Ronronea... 🐾")
                    break
                
                if user_input.lower() == "clear":
                    self.chat_history = []
                    print("\n✨ Chat limpiado.\n")
                    continue
                
                if user_input.lower().startswith("@gatimage"):
                    prompt = re.sub(r"^@gatimage\s*", "", user_input, flags=re.IGNORECASE).strip()
                    if not prompt:
                        prompt = "un gato digital inteligente estudiando"
                    print("\n🎨 Generando imagen... (esto puede tardar 30-60 segundos)")
                    image_path = self.manager.generate_image(prompt)
                    print(f"✅ Imagen guardada en: {image_path}")
                    continue
                
                response = self.manager.chat(user_input, self.chat_history)
                self.chat_history.append((user_input, response))
                print(f"\n{response}")
            
            except KeyboardInterrupt:
                print("\n\n🐱 Félix: ¡Ronronea suavemente y se despide! 🐾")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


# ===========================
# MAIN
# ===========================

if __name__ == "__main__":
    if KIVY_AVAILABLE:
        print("✅ Kivy disponible. Iniciando app móvil...")
        app = FelixMobileApp()
        app.run()
    else:
        print("⚠️ Kivy no disponible. Usando interfaz por consola...")
        console = FelixConsole()
        console.run()
