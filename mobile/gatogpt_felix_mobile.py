"""
🐱 GatoGPT Félix - Versión Mobile Mejorada
Optimizado para Android con TinyLlama + Google Drive
"""

import os
import re
import gc
import json
from datetime import datetime
from pathlib import Path

# Configuración
DEVICE = "cpu"
DTYPE = torch.float32

# Modelo ultra-ligero para móvil
CHAT_MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Directorios
APP_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = APP_DIR / "felix_outputs"
MODEL_CACHE_DIR = APP_DIR / "felix_models"
CHAT_SAVE_DIR = APP_DIR / "saved_chats"

OUTPUT_DIR.mkdir(exist_ok=True)
MODEL_CACHE_DIR.mkdir(exist_ok=True)
CHAT_SAVE_DIR.mkdir(exist_ok=True)

os.environ['HF_HOME'] = str(MODEL_CACHE_DIR)

# Google Drive integration
def save_chat_to_drive(history: list, filename: str = None):
    """Guarda el historial de chat en Google Drive."""
    if filename is None:
        filename = f"felix_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    filepath = CHAT_SAVE_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    # Subir a Google Drive si está configurado
    try:
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive
        
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        
        file_drive = drive.CreateFile({
            'title': filename,
            'parents': [{'id': 'root'}]
        })
        file_drive.SetContentFile(str(filepath))
        file_drive.Upload()
        
        print(f"✅ Chat subido a Google Drive: {filename}")
        return file_drive['id']
    except Exception as e:
        print(f"⚠️ No se pudo subir a Google Drive: {e}")
        return None

def load_chat_from_drive(filename: str):
    """Carga un historial de chat desde Google Drive o local."""
    filepath = CHAT_SAVE_DIR / filename
    
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Personalidad (importada del core)
from core.personality import FELIX_SYSTEM_PROMPT, FELIX_FALLBACK

# Motor de chat
class FelixChatEngine:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.history = []
        self.load_model()
    
    def load_model(self):
        """Carga el modelo de chat."""
        if self.model is not None:
            return
        
        print("🐱 Cargando TinyLlama para móvil...")
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        self.tokenizer = AutoTokenizer.from_pretrained(CHAT_MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(
            CHAT_MODEL_ID,
            torch_dtype=DTYPE,
            low_cpu_mem_usage=True,
        )
        print("✅ Modelo cargado")
    
    def chat(self, user_message: str) -> str:
        """Genera respuesta del chat."""
        messages = [
            {"role": "system", "content": FELIX_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]
        
        if self.history:
            for user_text, assistant_text in self.history[-5:]:
                messages.insert(-1, {"role": "user", "content": user_text})
                messages.insert(-1, {"role": "assistant", "content": assistant_text})
        
        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer([text], return_tensors="pt")
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        
        response = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True
        ).strip()
        
        if not response:
            response = FELIX_FALLBACK
        
        self.history.append((user_message, response))
        
        # Auto-guardar cada 10 mensajes
        if len(self.history) % 10 == 0:
            save_chat_to_drive(self.history)
        
        return response
    
    def unload(self):
        """Libera memoria del modelo."""
        self.model = None
        self.tokenizer = None
        gc.collect()

# Interfaz Kivy
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.core.window import Window
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False

class FelixMobileApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = FelixChatEngine()
    
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text='🐱 GatoGPT Félix',
            font_size='24sp',
            size_hint_y=0.1
        )
        layout.add_widget(title)
        
        # Chat display
        self.chat_display = Label(
            text="¡Miau! Soy Félix. Escribe algo para comenzar...",
            font_size='14sp',
            text_size=(Window.width - 40, None),
            valign='top',
            halign='left',
            size_hint_y=0.7
        )
        scroll = ScrollView()
        scroll.add_widget(self.chat_display)
        layout.add_widget(scroll)
        
        # Input
        self.text_input = TextInput(
            hint_text='Escribe a Félix...',
            font_size='14sp',
            size_hint_y=0.1,
            multiline=False
        )
        layout.add_widget(self.text_input)
        
        # Botón enviar
        send_btn = Button(
            text='Enviar 🐾',
            font_size='16sp',
            size_hint_y=0.1
        )
        send_btn.bind(on_press=self.send_message)
        layout.add_widget(send_btn)
        
        return layout
    
    def send_message(self, instance):
        user_msg = self.text_input.text.strip()
        if not user_msg:
            return
        
        response = self.engine.chat(user_msg)
        self.chat_display.text += f"\n\nTú: {user_msg}\n🐱 Félix: {response}"
        self.text_input.text = ''

if __name__ == '__main__':
    if KIVY_AVAILABLE:
        FelixMobileApp().run()
    else:
        print("⚠️ Kivy no instalado. Ejecutar: pip install kivy")
        print("🐱 Modo texto activado:")
        engine = FelixChatEngine()
        while True:
            msg = input("Tú: ")
            if msg.lower() in ['salir', 'exit']:
                break
            print(f"🐱 Félix: {engine.chat(msg)}")
