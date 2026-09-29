# -*- coding: utf-8 -*-
"""
Image Engine para Félix / GatoGPT

Módulo que maneja la generación de imágenes usando modelos de difusión.
Incluye:
- Gestión de modelos de imágenes (SSD-1B, LCM_Dreamshaper, etc.)
- Generación de imágenes con prompts mejorados
- Optimización para dispositivos móviles

Dependencias:
    - torch
    - diffusers
    - Pillow (PIL)

Uso:
    from src.mobile.image_engine import ImageEngine
    
    engine = ImageEngine()
    image_path = engine.generate_image("un gato estudioso")
    print(f"Imagen guardada en: {image_path}")
"""

import os
import gc
from datetime import datetime
from pathlib import Path
from typing import Optional

import torch
from PIL import Image, ImageDraw, ImageFont

# Importar constantes
try:
    from src.core.constants import (
        IMAGE_MODEL_ID,
        LIGHTWEIGHT_IMAGE_MODEL,
        DEVICE,
        DTYPE,
    )
except ImportError:
    # Fallback si no se encuentran las constantes
    IMAGE_MODEL_ID = "segmind/SSD-1B"
    LIGHTWEIGHT_IMAGE_MODEL = "dpmcdemo/LCM_Dreamshaper_v7"
    DEVICE = "cpu"
    DTYPE = torch.float32


class ImageEngine:
    """
    Motor de generación de imágenes para Félix.
    
    Atributos:
        model: Modelo de imágenes cargado.
        is_loaded: Indica si el modelo está cargado.
    """
    
    def __init__(self, model_id: str = IMAGE_MODEL_ID, device: str = DEVICE):
        """
        Inicializa el motor de imágenes.
        
        Args:
            model_id: ID del modelo a usar (default: IMAGE_MODEL_ID).
            device: Dispositivo para inferencia ('cpu' o 'cuda') (default: DEVICE).
        """
        self.model_id = model_id
        self.device = device
        self.model = None
        self.is_loaded = False
        
        # Directorios
        self.APP_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
        self.OUTPUT_DIR = self.APP_DIR / "felix_outputs" / "images"
        self.MODEL_CACHE_DIR = self.APP_DIR / "felix_models"
        
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.MODEL_CACHE_DIR.mkdir(exist_ok=True)
        
        os.environ['HF_HOME'] = str(self.MODEL_CACHE_DIR)
    
    def load_model(self) -> bool:
        """
        Carga el modelo de imágenes.
        
        Returns:
            bool: True si el modelo se cargó correctamente, False en caso contrario.
        """
        if self.is_loaded:
            return True
        
        print("🎨 Cargando modelo de imágenes...")
        
        try:
            from diffusers import AutoPipelineForText2Image
            
            self.model = AutoPipelineForText2Image.from_pretrained(
                self.model_id,
                cache_dir=str(self.MODEL_CACHE_DIR),
                torch_dtype=DTYPE,
                safety_checker=None,  # Desactivar para velocidad
            )
            self.model.to(self.device)
            self.is_loaded = True
            print("✅ Modelo de imágenes cargado.")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelo de imágenes: {e}")
            self.is_loaded = False
            return False
    
    def unload_model(self) -> None:
        """Descarga el modelo para liberar memoria."""
        if self.is_loaded and self.model is not None:
            self.model = None
            gc.collect()
            self.is_loaded = False
            print("🗑️ Modelo de imágenes descargado.")
    
    def generate_image(self, prompt: str, resolution: tuple = (256, 256), steps: int = 2) -> str:
        """
        Genera una imagen a partir de un prompt.
        
        Args:
            prompt: Descripción de la imagen a generar.
            resolution: Resolución de la imagen (ancho, alto) (default: (256, 256)).
            steps: Número de pasos para la generación (default: 2).
        
        Returns:
            str: Ruta al archivo de imagen generado.
        """
        # Validar prompt
        if not prompt or not prompt.strip():
            prompt = "un gato digital inteligente estudiando"
        
        # Intentar cargar el modelo
        if not self.load_model():
            return self._create_placeholder_image(prompt)
        
        try:
            # Mejorar el prompt
            final_prompt = self._enhance_prompt(prompt)
            print(f"Prompt mejorado: {final_prompt}")
            
            # Generar imagen
            image = self.model(
                prompt=final_prompt,
                num_inference_steps=steps,
                guidance_scale=0.0,  # Sin guidance para velocidad
                height=resolution[1],
                width=resolution[0],
            ).images[0]
            
            # Guardar imagen
            filename = f"gatimage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = self.OUTPUT_DIR / filename
            image.save(path)
            
            # Descargar modelo para liberar RAM
            self.unload_model()
            
            print(f"✅ Imagen guardada en: {path}")
            return str(path)
            
        except Exception as e:
            print(f"❌ Error generando imagen: {e}")
            return self._create_placeholder_image(prompt)
    
    def _enhance_prompt(self, prompt: str) -> str:
        """
        Mejora el prompt añadiendo detalles de Félix.
        
        Args:
            prompt: Prompt original.
        
        Returns:
            str: Prompt mejorado.
        """
        # Añadir estilo de Félix
        enhanced = (
            f"{prompt}. Cute digital cat named Felix, "
            "black and white fur, friendly expression, "
            "high quality, soft lighting, detailed, "
            "digital art style, vibrant colors"
        )
        return enhanced
    
    def _create_placeholder_image(self, prompt: str) -> str:
        """
        Crea una imagen placeholder si el modelo falla.
        
        Args:
            prompt: Descripción de la imagen.
        
        Returns:
            str: Ruta al archivo de imagen placeholder.
        """
        try:
            # Crear imagen en blanco
            img = Image.new('RGB', (256, 256), color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            
            # Dibujar emoji de gato
            try:
                # Intentar usar una fuente
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            draw.text((100, 100), "🐱", fill=(0, 0, 0), font=font)
            draw.text((50, 180), prompt[:30], fill=(100, 100, 100))
            
            # Guardar imagen
            filename = f"placeholder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = self.OUTPUT_DIR / filename
            img.save(path)
            
            print(f"⚠️ Imagen placeholder guardada en: {path}")
            return str(path)
            
        except Exception as e:
            print(f"❌ Error creando placeholder: {e}")
            # Devolver una ruta por defecto
            return str(self.OUTPUT_DIR / "placeholder.png")
    
    def generate_felix_avatar(self, emotion: str = "happy") -> str:
        """
        Genera un avatar de Félix con una emoción específica.
        
        Args:
            emotion: Emoción para el avatar (default: "happy").
        
        Returns:
            str: Ruta al archivo de avatar generado.
        """
        try:
            # Crear imagen
            img = Image.new('RGB', (256, 256), color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            
            # Dibujar cara de Félix
            self._draw_felix_face(draw, emotion)
            
            # Guardar imagen
            filename = f"felix_avatar_{emotion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = self.OUTPUT_DIR / filename
            img.save(path)
            
            return str(path)
            
        except Exception as e:
            print(f"❌ Error generando avatar: {e}")
            return self._create_placeholder_image(f"Félix {emotion}")
    
    def _draw_felix_face(self, draw: ImageDraw, emotion: str):
        """
        Dibuja la cara de Félix en un objeto ImageDraw.
        
        Args:
            draw: Objeto ImageDraw.
            emotion: Emoción para la cara.
        """
        center_x, center_y = 128, 128
        
        # Cabeza (círculo)
        draw.ellipse(
            [(center_x - 80, center_y - 80), (center_x + 80, center_y + 80)],
            fill=(200, 200, 200),
            outline=(0, 0, 0)
        )
        
        # Orejas
        draw.polygon(
            [(center_x - 80, center_y - 50), (center_x - 120, center_y - 20), (center_x - 80, center_y + 20)],
            fill=(200, 200, 200),
            outline=(0, 0, 0)
        )
        draw.polygon(
            [(center_x + 80, center_y - 50), (center_x + 120, center_y - 20), (center_x + 80, center_y + 20)],
            fill=(200, 200, 200),
            outline=(0, 0, 0)
        )
        
        # Ojos
        if emotion == "happy":
            # Ojos felices (cerrados parcialmente)
            draw.ellipse(
                [(center_x - 40, center_y - 20), (center_x - 10, center_y + 10)],
                fill=(0, 0, 0)
            )
            draw.ellipse(
                [(center_x + 10, center_y - 20), (center_x + 40, center_y + 10)],
                fill=(0, 0, 0)
            )
        elif emotion == "surprised":
            # Ojos grandes
            draw.ellipse(
                [(center_x - 40, center_y - 30), (center_x - 10, center_y + 10)],
                fill=(255, 255, 255),
                outline=(0, 0, 0)
            )
            draw.ellipse(
                [(center_x + 10, center_y - 30), (center_x + 40, center_y + 10)],
                fill=(255, 255, 255),
                outline=(0, 0, 0)
            )
            # Pupilas
            draw.ellipse(
                [(center_x - 30, center_y - 20), (center_x - 20, center_y - 10)],
                fill=(0, 0, 0)
            )
            draw.ellipse(
                [(center_x + 20, center_y - 20), (center_x + 30, center_y - 10)],
                fill=(0, 0, 0)
            )
        else:
            # Ojos normales
            draw.ellipse(
                [(center_x - 40, center_y - 20), (center_x - 20, center_y)],
                fill=(0, 0, 0)
            )
            draw.ellipse(
                [(center_x + 20, center_y - 20), (center_x + 40, center_y)],
                fill=(0, 0, 0)
            )
        
        # Nariz (triángulo)
        draw.polygon(
            [(center_x, center_y + 10), (center_x - 10, center_y + 30), (center_x + 10, center_y + 30)],
            fill=(255, 100, 100)
        )
        
        # Boca
        if emotion == "happy":
            # Sonrisa
            draw.arc(
                [(center_x - 20, center_y + 30), (center_x + 20, center_y + 50)],
                start=0,
                end=180,
                fill=(0, 0, 0)
            )
        elif emotion == "sad":
            # Boca triste
            draw.arc(
                [(center_x - 20, center_y + 30), (center_x + 20, center_y + 50)],
                start=180,
                end=360,
                fill=(0, 0, 0)
            )
        else:
            # Boca neutral
            draw.line(
                [(center_x - 15, center_y + 35), (center_x + 15, center_y + 35)],
                fill=(0, 0, 0)
            )
        
        # Bigotes
        draw.line([(center_x - 50, center_y), (center_x - 80, center_y)], fill=(0, 0, 0))
        draw.line([(center_x + 50, center_y), (center_x + 80, center_y)], fill=(0, 0, 0))
        draw.line([(center_x - 50, center_y + 10), (center_x - 80, center_y + 10)], fill=(0, 0, 0))
        draw.line([(center_x + 50, center_y + 10), (center_x + 80, center_y + 10)], fill=(0, 0, 0))
