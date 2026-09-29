# -*- coding: utf-8 -*-
"""
🐱 GatoGPT Félix - Versión Mobile para Snapdragon 8 Gen2
App principal que integra todos los módulos

Requisitos:
- Python 3.9+
- Kivy 2.2+
- Transformers 4.30+
- ONNX Runtime (para inferencia rápida)

Uso:
    python main.py
"""

import re
from datetime import datetime
from pathlib import Path

# Importar módulos
from src.mobile.chat_engine import ChatEngine
from src.mobile.image_engine import ImageEngine

# Importar constantes
try:
    from src.core.constants import (
        GATIMAGE_COMMAND,
        CLEAR_COMMAND,
        QUIT_COMMAND,
        HELP_COMMAND,
        FELIX_WELCOME_MESSAGE,
        FELIX_GOODBYE_MESSAGE,
        FELIX_UNKNOWN_COMMAND_MESSAGE,
    )
except ImportError:
    # Fallback si no se encuentran las constantes
    GATIMAGE_COMMAND = "@gatimage"
    CLEAR_COMMAND = "clear"
    QUIT_COMMAND = "quit"
    HELP_COMMAND = "@help"
    FELIX_WELCOME_MESSAGE = "¡Miauuu! 🐱 Hola humano, soy el Gato Félix, tu amigo felino."
    FELIX_GOODBYE_MESSAGE = "¡Hasta luego, Luciano! Ronronea... 🐱"
    FELIX_UNKNOWN_COMMAND_MESSAGE = "Miau... no conozco ese comando. Prueba con @gatimage o @help. 🐱"

# Configuración de directorios
APP_DIR = Path(__file__).parent
OUTPUT_DIR = APP_DIR / "felix_outputs"
MODEL_CACHE_DIR = APP_DIR / "felix_models"
OUTPUT_DIR.mkdir(exist_ok=True)
MODEL_CACHE_DIR.mkdir(exist_ok=True)


# =============================================================================
# INTERFAZ KIVY (MÓVIL)
# =============================================================================

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.image import Image as KivyImage
    from kivy.core.window import Window
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("⚠️ Kivy no instalado. Instalación: pip install kivy python-for-android")


# Paleta de colores de Félix
COLORS = {
    "primary": (0.06, 0.14, 0.49, 1),      # #1A237E (Azul oscuro)
    "secondary": (0.65, 0.85, 1.0, 1),      # #A7D8FF (Azul claro)
    "accent": (0.22, 1.0, 0.71, 1),        # #39FFB6 (Verde claro)
    "background": (0.95, 0.95, 0.98, 1),    # Fondo claro
    "text": (0.1, 0.1, 0.1, 1),            # Texto oscuro
    "user": (0.2, 0.8, 0.2, 1),            # Verde para usuario
    "felix": (0.2, 0.6, 1.0, 1),           # Azul para Félix
    "error": (1.0, 0.2, 0.2, 1),           # Rojo para errores
    "button": (0.2, 0.6, 1.0, 1),           # Azul para botones
    "button_pressed": (0.1, 0.5, 0.9, 1),   # Azul más oscuro al presionar
}


class FelixMobileApp(App):
    """Aplicación Kivy para GatoGPT Félix en móvil."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_engine = ChatEngine()
        self.image_engine = ImageEngine()
        self.chat_history = []

    def build(self):
        """Construye interfaz móvil."""
        if KIVY_AVAILABLE:
            Window.size = (400, 700)  # Tamaño típico móvil
            Window.clearcolor = COLORS["background"]
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Título
        title = Label(
            text="🐱 GatoGPT Félix Mobile",
            size_hint_y=0.1,
            font_size='18sp',
            bold=True,
            color=COLORS["primary"]
        )
        root.add_widget(title)
        
        # Área de chat (scroll)
        self.chat_scroll = ScrollView(size_hint_y=0.7, background_color=COLORS["background"])
        self.chat_box = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.chat_scroll.add_widget(self.chat_box)
        root.add_widget(self.chat_scroll)
        
        # Input de texto
        input_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        
        self.text_input = TextInput(
            hint_text="Escribe a Félix...",
            multiline=True,
            size_hint_x=0.8,
            background_color=COLORS["secondary"],
            foreground_color=COLORS["text"],
            font_size='14sp'
        )
        input_layout.add_widget(self.text_input)
        
        send_btn = Button(
            text="Enviar\n🐱",
            size_hint_x=0.2,
            background_color=COLORS["button"],
            background_normal='',
            color=COLORS["background"],
            font_size='14sp'
        )
        send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(send_btn)
        
        root.add_widget(input_layout)
        
        # Botones de comando
        cmd_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        
        img_btn = Button(
            text="@gatimage",
            background_color=COLORS["accent"],
            background_normal='',
            color=COLORS["background"],
            font_size='14sp'
        )
        img_btn.bind(on_press=self.on_image_cmd)
        cmd_layout.add_widget(img_btn)
        
        help_btn = Button(
            text="@help",
            background_color=COLORS["secondary"],
            background_normal='',
            color=COLORS["primary"],
            font_size='14sp'
        )
        help_btn.bind(on_press=self.on_help_cmd)
        cmd_layout.add_widget(help_btn)
        
        clear_btn = Button(
            text="Limpiar",
            background_color=COLORS["button"],
            background_normal='',
            color=COLORS["background"],
            font_size='14sp'
        )
        clear_btn.bind(on_press=self.clear_chat)
        cmd_layout.add_widget(clear_btn)
        
        root.add_widget(cmd_layout)
        
        # Mensaje de bienvenida
        self.add_chat_bubble(FELIX_WELCOME_MESSAGE, "felix")
        
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
        if message.lower().startswith(GATIMAGE_COMMAND):
            self.process_image_command(message)
        elif message.lower().startswith(HELP_COMMAND):
            self.process_help_command()
        elif message.lower() == CLEAR_COMMAND:
            self.clear_chat(None)
        elif message.lower() == QUIT_COMMAND:
            self.stop()
        else:
            # Chat normal
            response = self.chat_engine.chat(message, self.chat_history)
            self.chat_history.append((message, response))
            self.add_chat_bubble(response, "felix")

    def on_image_cmd(self, instance):
        """Botón para generar imagen."""
        cmd = f"{GATIMAGE_COMMAND} un gato estudioso"
        self.text_input.text = cmd

    def on_help_cmd(self, instance=None):
        """Botón para mostrar ayuda."""
        help_text = (
            "🐱 Comandos disponibles:\n\n"
            f"• {GATIMAGE_COMMAND} <texto> - Generar imagen\n"
            f"• {HELP_COMMAND} - Mostrar esta ayuda\n"
            f"• {CLEAR_COMMAND} - Limpiar el chat\n"
            f"• {QUIT_COMMAND} - Salir"
        )
        self.add_chat_bubble(help_text, "felix")

    def process_image_command(self, message: str):
        """Procesa comando @gatimage."""
        prompt = re.sub(rf"^{re.escape(GATIMAGE_COMMAND)}\s*", "", message, flags=re.IGNORECASE).strip()
        
        if not prompt:
            prompt = "un gato digital inteligente estudiando"
        
        self.add_chat_bubble("🐱 Félix: Generando imagen... esto puede tardar 30-60 segundos. Paciencia 🐱", "felix")
        
        try:
            image_path = self.image_engine.generate_image(prompt)
            self.add_chat_bubble(f"✅ Imagen guardada en: {image_path}", "felix")
            self.chat_history.append((message, f"Imagen generada: {image_path}"))
        except Exception as e:
            self.add_chat_bubble(f"❌ Error: {e}", "error")

    def process_help_command(self):
        """Procesa comando @help."""
        self.on_help_cmd()

    def add_chat_bubble(self, text: str, sender: str):
        """Añade un mensaje al chat."""
        # Determinar color según el remitente
        if sender == "user":
            color = COLORS["user"]
        elif sender == "felix":
            color = COLORS["felix"]
        elif sender == "error":
            color = COLORS["error"]
        else:
            color = COLORS["text"]
        
        bubble = Label(
            text=text,
            size_hint_y=None,
            height=max(50, len(text) * 8),
            text_size=(350, None),
            markup=True,
            color=color,
            font_size='14sp'
        )
        
        # Fondo del bubble (simulado con padding)
        bubble.padding = (10, 10)
        
        self.chat_box.add_widget(bubble)
        self.chat_scroll.scroll_y = 0  # Scroll al final

    def clear_chat(self, instance):
        """Limpia el historial de chat."""
        self.chat_box.clear_widgets()
        self.chat_history = []
        self.add_chat_bubble("🐱 Félix: Nuevo chat, ¡hola Luciano!", "felix")


# =============================================================================
# INTERFAZ CONSOLA (Fallback)
# =============================================================================

class FelixConsole:
    """Interfaz por consola para testing sin Kivy."""

    def __init__(self):
        self.chat_engine = ChatEngine()
        self.image_engine = ImageEngine()
        self.chat_history = []

    def run(self):
        """Loop principal de consola."""
        print("\n" + "="*50)
        print("🐱 GatoGPT Félix - Versión Mobile")
        print("Optimizado para Snapdragon 8 Gen2")
        print("="*50)
        print("\nComandos:")
        print(f"  {GATIMAGE_COMMAND} <prompt> - Generar imagen")
        print(f"  {HELP_COMMAND}              - Mostrar ayuda")
        print(f"  {CLEAR_COMMAND}              - Limpiar chat")
        print(f"  {QUIT_COMMAND}               - Salir")
        print("="*50 + "\n")
        
        # Mensaje de bienvenida
        print(f"🐱 {FELIX_WELCOME_MESSAGE}\n")

        while True:
            try:
                user_input = input("🐱 Tú: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == QUIT_COMMAND:
                    print(f"\n🐱 {FELIX_GOODBYE_MESSAGE}")
                    break
                
                if user_input.lower() == CLEAR_COMMAND:
                    self.chat_history = []
                    print("\n✨ Chat limpiado.\n")
                    continue
                
                if user_input.lower() == HELP_COMMAND:
                    self.on_help_cmd()
                    continue
                
                if user_input.lower().startswith(GATIMAGE_COMMAND):
                    self.process_image_command(user_input)
                    continue
                
                response = self.chat_engine.chat(user_input, self.chat_history)
                self.chat_history.append((user_input, response))
                print(f"\n{response}\n")
            
            except KeyboardInterrupt:
                print(f"\n\n🐱 {FELIX_GOODBYE_MESSAGE}")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def on_help_cmd(self):
        """Muestra la ayuda."""
        help_text = (
            "🐱 Comandos disponibles:\n\n"
            f"• {GATIMAGE_COMMAND} <texto> - Generar imagen\n"
            f"• {HELP_COMMAND} - Mostrar esta ayuda\n"
            f"• {CLEAR_COMMAND} - Limpiar el chat\n"
            f"• {QUIT_COMMAND} - Salir"
        )
        print(help_text)

    def process_image_command(self, message: str):
        """Procesa comando @gatimage."""
        prompt = re.sub(rf"^{re.escape(GATIMAGE_COMMAND)}\s*", "", message, flags=re.IGNORECASE).strip()
        
        if not prompt:
            prompt = "un gato digital inteligente estudiando"
        
        print(f"\n🎨 Generando imagen: '{prompt}'...")
        print("(esto puede tardar 30-60 segundos)")
        
        try:
            image_path = self.image_engine.generate_image(prompt)
            print(f"✅ Imagen guardada en: {image_path}")
        except Exception as e:
            print(f"❌ Error generando imagen: {e}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    if KIVY_AVAILABLE:
        # Intentar ejecutar la app de Kivy
        try:
            FelixMobileApp().run()
        except Exception as e:
            print(f"❌ Error al ejecutar Kivy: {e}")
            print("Falling back a modo consola...")
            FelixConsole().run()
    else:
        # Modo consola
        FelixConsole().run()
