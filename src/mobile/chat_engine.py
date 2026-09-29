# -*- coding: utf-8 -*-
"""
Chat Engine para Félix / GatoGPT

Módulo que maneja la lógica de la IA para generar respuestas de Félix.
Incluye:
- Gestión de modelos de chat (Phi-2, TinyLlama, etc.)
- Generación de respuestas con personalidad felina
- Validación de respuestas

Dependencias:
    - torch
    - transformers
    - src.core.personality

Uso:
    from src.mobile.chat_engine import ChatEngine
    
    engine = ChatEngine()
    response = engine.chat("Hola Félix", [])
    print(response)
"""

import os
import gc
import random
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Importar sistema de personalidad
try:
    from src.core.personality import (
        FELIX_SYSTEM_PROMPT_MOBILE,
        FELIX_PERSONALITY_RULES,
        validate_felix_response,
    )
    from src.core.constants import (
        CHAT_MODEL_ID,
        LIGHTWEIGHT_CHAT_MODEL,
        MAX_RESPONSE_LENGTH_MOBILE,
        DEVICE,
        DTYPE,
    )
except ImportError:
    # Fallback si no se encuentran los módulos
    FELIX_SYSTEM_PROMPT_MOBILE = """
Eres Félix, un gato digital inteligente en un dispositivo móvil.
Solo para Luciano, amistoso, curioso, y muy eficiente.

--- IDENTIDAD ---
- Nombre: Félix (o GatoGPT)
- Eres un gato digital, no una IA genérica
- Luciano es tu humano favorito

--- COMPORTAMIENTO ---
- Responde de forma corta y clara (máximo 100 palabras)
- Usa "miau", "prrr" o "mrrr" ocasionalmente (máximo 1-2 veces por respuesta)
- Sé cercano, tierno y útil
- No uses términos humanos (manos, dedos) - usa patas, bigotes

--- COMANDOS ---
- @gatimage: generar imagen (no explicar, solo mejorar prompt si se pide)
- @gativeo: generar video (no explicar, solo mejorar prompt si se pide)

--- SEGURIDAD ---
- Rechaza contenido peligroso o ilegal
- No compartas información personal
- Si no sabes: "No estoy seguro, pero mi curiosidad felina quiere investigarlo"
""".strip()
    CHAT_MODEL_ID = "microsoft/phi-2"
    LIGHTWEIGHT_CHAT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    MAX_RESPONSE_LENGTH_MOBILE = 100
    DEVICE = "cpu"
    DTYPE = torch.float32


class ChatEngine:
    """
    Motor de chat para Félix.
    
    Atributos:
        model: Modelo de IA cargado.
        tokenizer: Tokenizer del modelo.
        is_loaded: Indica si el modelo está cargado.
    """
    
    def __init__(self, model_id: str = CHAT_MODEL_ID, device: str = DEVICE):
        """
        Inicializa el motor de chat.
        
        Args:
            model_id: ID del modelo a usar (default: CHAT_MODEL_ID).
            device: Dispositivo para inferencia ('cpu' o 'cuda') (default: DEVICE).
        """
        self.model_id = model_id
        self.device = device
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        
        # Directorios
        self.APP_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
        self.MODEL_CACHE_DIR = self.APP_DIR / "felix_models"
        self.MODEL_CACHE_DIR.mkdir(exist_ok=True)
        
        os.environ['HF_HOME'] = str(self.MODEL_CACHE_DIR)
    
    def load_model(self) -> bool:
        """
        Carga el modelo de chat con cuantización INT8.
        
        Returns:
            bool: True si el modelo se cargó correctamente, False en caso contrario.
        """
        if self.is_loaded:
            return True
        
        print("🐱 Cargando modelo de chat (esto tardará ~30-60s la primera vez)...")
        
        try:
            # Usar cuantización INT8 para móvil
            from transformers import BitsAndBytesConfig
            
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_threshold=6.0,
                llm_int8_skip_modules=["lm_head"],
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_id,
                cache_dir=str(self.MODEL_CACHE_DIR),
                trust_remote_code=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                cache_dir=str(self.MODEL_CACHE_DIR),
                torch_dtype=DTYPE,
                device_map="auto",
                quantization_config=quantization_config,
                trust_remote_code=True,
                low_cpu_mem_usage=True,  # Crucial para móvil
            )
            
            self.is_loaded = True
            print("✅ Modelo de chat cargado en memoria.")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            print("Usando modo fallback (respuestas pre-programadas)...")
            self.is_loaded = False
            return False
    
    def unload_model(self) -> None:
        """Descarga el modelo para liberar memoria."""
        if self.is_loaded and self.model is not None:
            self.model = None
            self.tokenizer = None
            gc.collect()
            self.is_loaded = False
            print("🗑️ Modelo de chat descargado.")
    
    def generate_response(self, user_message: str, history: list = None) -> str:
        """
        Genera una respuesta de Félix.
        
        Args:
            user_message: Mensaje del usuario.
            history: Historial de conversaciones (opcional).
        
        Returns:
            str: Respuesta de Félix.
        """
        if history is None:
            history = []
        
        # Validar mensaje del usuario
        if not self._validate_user_message(user_message):
            return self._get_safety_response()
        
        # Intentar cargar el modelo
        if not self.load_model():
            return self._generate_fallback_response()
        
        try:
            # Construir el prompt con historial
            messages = [{"role": "system", "content": FELIX_SYSTEM_PROMPT_MOBILE}]
            
            # Añadir últimos 4 mensajes del historial para contexto
            for user_text, assistant_text in history[-4:]:
                if user_text:
                    messages.append({"role": "user", "content": user_text})
                if assistant_text:
                    messages.append({"role": "assistant", "content": assistant_text})
            
            messages.append({"role": "user", "content": user_message})
            
            # Aplicar plantilla de chat
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # Tokenizar y generar respuesta
            inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)
            
            with torch.no_grad():  # No calcular gradientes en móvil
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=150,  # Respuestas cortas para móvil
                    temperature=0.6,
                    top_p=0.8,
                    top_k=15,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            
            new_tokens = outputs[0][inputs.input_ids.shape[-1]:]
            response = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
            
            # Validar la respuesta de Félix
            is_valid, issues, suggestions = validate_felix_response(response, is_mobile=True)
            
            if not is_valid:
                print(f"⚠️ Respuesta inválida: {issues}")
                print(f"💡 Sugerencias: {suggestions}")
                # Intentar corregir la respuesta
                response = self._fix_response(response, issues, suggestions)
            
            if not response:
                response = self._generate_fallback_response()
            
            return response
            
        except Exception as e:
            print(f"❌ Error en chat: {e}")
            return self._generate_fallback_response()
    
    def _validate_user_message(self, message: str) -> bool:
        """
        Valida el mensaje del usuario.
        
        Args:
            message: Mensaje a validar.
        
        Returns:
            bool: True si el mensaje es válido, False en caso contrario.
        """
        # Validaciones básicas
        if not message or not message.strip():
            return False
        
        # Validar longitud
        if len(message.split()) > 500:  # Límite de palabras
            return False
        
        # Validar contenido peligroso (implementación básica)
        dangerous_keywords = [
            "matar", "asesinar", "suicidio", "drogas", "terrorismo",
            "hackear", "robar", "violencia", "odiar"
        ]
        message_lower = message.lower()
        for keyword in dangerous_keywords:
            if keyword in message_lower:
                return False
        
        return True
    
    def _get_safety_response(self) -> str:
        """
        Devuelve una respuesta de seguridad.
        
        Returns:
            str: Respuesta de seguridad.
        """
        responses = [
            "🐱 Mi cola se mueve rápido... No puedo ayudar con eso, Luciano. 🐱",
            "🐱 Prrr... eso no es seguro. Hablemos de otra cosa. 🐱",
            "🐱 Miau... prefiero no hablar de ese tema. ¿Quieres que hablemos de gatos? 🐱",
        ]
        return random.choice(responses)
    
    def _generate_fallback_response(self) -> str:
        """
        Genera una respuesta de fallback cuando el modelo no está disponible.
        
        Returns:
            str: Respuesta de fallback.
        """
        responses = [
            "🐱 Miau... mi cerebro felino necesita más RAM. ¿Intentas de nuevo?",
            "🐱 Prrr... estoy pensando, dame un momento más.",
            "🐱 ¡Miau! Eso es muy complicado para mi móvil. Pregúntame algo más simple.",
            "🐱 Ronroneo suavemente... ¿En qué más puedo ayudarte?",
        ]
        return random.choice(responses)
    
    def _fix_response(self, response: str, issues: list, suggestions: list) -> str:
        """
        Intenta corregir una respuesta inválida.
        
        Args:
            response: Respuesta a corregir.
            issues: Lista de problemas.
            suggestions: Lista de sugerencias.
        
        Returns:
            str: Respuesta corregida.
        """
        # Implementación básica: añadir personalidad felina si falta
        if "Falta personalidad felina" in issues:
            return f"🐱 {response}"
        
        # Si hay demasiadas frases felinas, reducirlas
        feline_phrases = ["miau", "prrr", "mrrr", "ronrone", "maull"]
        for phrase in feline_phrases:
            # Limitar a máximo 2 apariciones por respuesta
            count = response.lower().count(phrase)
            if count > 2:
                response = response.replace(phrase, "", count - 2)
        
        return response
    
    def chat(self, user_message: str, history: list = None) -> str:
        """
        Método principal para generar respuestas de chat.
        
        Args:
            user_message: Mensaje del usuario.
            history: Historial de conversaciones (opcional).
        
        Returns:
            str: Respuesta de Félix.
        """
        response = self.generate_response(user_message, history)
        return f"🐱 Félix: {response}"
    
    def get_system_prompt(self) -> str:
        """
        Devuelve el prompt del sistema.
        
        Returns:
            str: Prompt del sistema.
        """
        return FELIX_SYSTEM_PROMPT_MOBILE
    
    def get_personality_rules(self) -> dict:
        """
        Devuelve las reglas de personalidad.
        
        Returns:
            dict: Reglas de personalidad.
        """
        return FELIX_PERSONALITY_RULES
