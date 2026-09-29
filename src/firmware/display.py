# -*- coding: utf-8 -*-
"""
Display Controller para Félix / GatoGPT

Módulo para controlar la pantalla OLED SSD1306 en el ESP32.
Muestra expresiones faciales, texto y animaciones de Félix.

Dependencias:
    - MicroPython (ESP32)
    - Módulo machine para I2C
    - Librería ssd1306 (incluida en MicroPython para ESP32)

Uso:
    from src.firmware.display import DisplayController
    
    display = DisplayController()
    display.initialize()
    
    # Mostrar texto
    display.show_text("¡Miau!")
    
    # Mostrar emoción
    display.show_emotion("happy")
    
    # Mostrar animación
    display.show_animation("blink")
    
    # Limpiar pantalla
    display.clear()
"""

import time
from machine import I2C, Pin

# Importar librería SSD1306
try:
    from ssd1306 import SSD1306_I2C
except ImportError:
    # Si no está disponible, intentar importar desde otra ubicación
    try:
        from lib.ssd1306 import SSD1306_I2C
    except ImportError:
        print("[Display] Librería SSD1306 no encontrada. Instálala con: mip install ssd1306")
        SSD1306_I2C = None

# Importar constantes
try:
    from src.core.constants import (
        ESP32_OLED_SCL_PIN,
        ESP32_OLED_SDA_PIN,
        ESP32_I2C_FREQ,
        FELIX_NAME,
        FELIX_EMOTIONS,
    )
except ImportError:
    # Fallback si no se encuentra el módulo de constantes
    ESP32_OLED_SCL_PIN = 21
    ESP32_OLED_SDA_PIN = 22
    ESP32_I2C_FREQ = 400000
    FELIX_NAME = "Félix"
    FELIX_EMOTIONS = {
        "happy": {"action": "cola relajada", "sound": "ronroneo suave", "phrase": "prrr"},
        "curious": {"action": "orejas hacia adelante", "phrase": "observar antes de hablar"},
        "focused": {"action": "pausa breve", "phrase": "mirar algo moverse"},
    }


class DisplayController:
    """
    Clase para controlar la pantalla OLED SSD1306.
    
    Atributos:
        i2c (I2C): Objeto I2C para comunicación.
        oled (SSD1306_I2C): Objeto de la pantalla OLED.
        width (int): Ancho de la pantalla en píxeles.
        height (int): Alto de la pantalla en píxeles.
        is_initialized (bool): Indica si la pantalla está inicializada.
    """
    
    def __init__(self, width: int = 128, height: int = 64):
        """
        Inicializa el controlador de pantalla.
        
        Args:
            width: Ancho de la pantalla en píxeles (default: 128).
            height: Alto de la pantalla en píxeles (default: 64).
        """
        self.i2c = None
        self.oled = None
        self.width = width
        self.height = height
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """
        Inicializa la pantalla OLED.
        
        Returns:
            bool: True si la inicialización fue exitosa, False en caso contrario.
        """
        if SSD1306_I2C is None:
            print("[Display] Librería SSD1306 no disponible")
            return False
        
        try:
            # Configurar pines I2C
            scl_pin = Pin(ESP32_OLED_SCL_PIN)
            sda_pin = Pin(ESP32_OLED_SDA_PIN)
            
            # Inicializar I2C
            self.i2c = I2C(
                scl=scl_pin,
                sda=sda_pin,
                freq=ESP32_I2C_FREQ,
            )
            
            # Inicializar OLED
            self.oled = SSD1306_I2C(self.width, self.height, self.i2c)
            
            # Limpiar pantalla
            self.clear()
            
            self.is_initialized = True
            print(f"[Display] OLED {self.width}x{self.height} inicializada")
            return True
            
        except Exception as e:
            print(f"[Display] Error al inicializar: {e}")
            self.is_initialized = False
            return False
    
    def clear(self):
        """Limpia la pantalla."""
        if self.is_initialized and self.oled is not None:
            self.oled.fill(0)
            self.oled.show()
            print("[Display] Pantalla limpiada")
    
    def show_text(self, text: str, x: int = 0, y: int = 0, clear_first: bool = True) -> bool:
        """
        Muestra texto en la pantalla.
        
        Args:
            text: Texto a mostrar.
            x: Posición X en píxeles (default: 0).
            y: Posición Y en píxeles (default: 0).
            clear_first: Si True, limpia la pantalla antes de mostrar el texto (default: True).
        
        Returns:
            bool: True si fue exitoso, False en caso contrario.
        """
        if not self.is_initialized or self.oled is None:
            print("[Display] Pantalla no inicializada")
            return False
        
        try:
            if clear_first:
                self.clear()
            
            # Dividir texto en líneas si es muy largo
            lines = self._split_text(text)
            
            for i, line in enumerate(lines):
                self.oled.text(line, x, y + (i * 10))
            
            self.oled.show()
            print(f"[Display] Texto mostrado: {text}")
            return True
            
        except Exception as e:
            print(f"[Display] Error al mostrar texto: {e}")
            return False
    
    def _split_text(self, text: str, max_chars: int = 21) -> list:
        """
        Divide el texto en líneas que caben en la pantalla.
        
        Args:
            text: Texto a dividir.
            max_chars: Máximo número de caracteres por línea (default: 21).
        
        Returns:
            list: Lista de líneas de texto.
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines
    
    def show_emotion(self, emotion: str, duration: float = None) -> bool:
        """
        Muestra una emoción de Félix en la pantalla.
        
        Args:
            emotion: Emoción a mostrar (ej: "happy", "curious", "focused").
            duration: Duración en segundos para mostrar la emoción (default: None = hasta que se cambie).
        
        Returns:
            bool: True si fue exitoso, False en caso contrario.
        """
        if not self.is_initialized or self.oled is None:
            print("[Display] Pantalla no inicializada")
            return False
        
        try:
            # Obtener información de la emoción
            emotion_info = FELIX_EMOTIONS.get(emotion, {})
            action = emotion_info.get("action", emotion)
            phrase = emotion_info.get("phrase", "")
            
            # Mostrar emoción
            self.clear()
            self.oled.text(f"{FELIX_NAME}:", 0, 0)
            self.oled.text(action, 0, 10)
            if phrase:
                self.oled.text(phrase, 0, 20)
            self.oled.show()
            
            print(f"[Display] Emoción mostrada: {emotion}")
            
            # Si se especifica duración, esperar y limpiar
            if duration is not None:
                time.sleep(duration)
                self.clear()
            
            return True
            
        except Exception as e:
            print(f"[Display] Error al mostrar emoción: {e}")
            return False
    
    def show_animation(self, animation: str, duration: float = 2.0) -> bool:
        """
        Muestra una animación simple.
        
        Args:
            animation: Tipo de animación (ej: "blink", "wave", "pulse").
            duration: Duración de la animación en segundos (default: 2.0).
        
        Returns:
            bool: True si fue exitoso, False en caso contrario.
        """
        if not self.is_initialized or self.oled is None:
            print("[Display] Pantalla no inicializada")
            return False
        
        try:
            if animation == "blink":
                self._animate_blink(duration)
            elif animation == "wave":
                self._animate_wave(duration)
            elif animation == "pulse":
                self._animate_pulse(duration)
            else:
                print(f"[Display] Animación '{animation}' no reconocida")
                return False
            
            return True
            
        except Exception as e:
            print(f"[Display] Error en animación: {e}")
            return False
    
    def _animate_blink(self, duration: float):
        """
        Animación de parpadeo (encender/apagar la pantalla).
        
        Args:
            duration: Duración de la animación en segundos.
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            self.clear()
            self.oled.show()
            time.sleep(0.3)
            self.oled.fill(1)
            self.oled.show()
            time.sleep(0.3)
        self.clear()
    
    def _animate_wave(self, duration: float):
        """
        Animación de onda (línea que se mueve).
        
        Args:
            duration: Duración de la animación en segundos.
        """
        start_time = time.time()
        position = 0
        direction = 1
        
        while time.time() - start_time < duration:
            self.clear()
            self.oled.hline(0, position, self.width, 1)
            self.oled.show()
            position += direction
            if position <= 0 or position >= self.height:
                direction *= -1
            time.sleep(0.1)
        self.clear()
    
    def _animate_pulse(self, duration: float):
        """
        Animación de pulso (pantalla que parpadea con intensidad variable).
        
        Args:
            duration: Duración de la animación en segundos.
        """
        start_time = time.time()
        intensity = 0
        direction = 1
        
        while time.time() - start_time < duration:
            self.clear()
            # Dibujar un círculo con intensidad variable
            self.oled.fill(0)
            center_x = self.width // 2
            center_y = self.height // 2
            radius = min(self.width, self.height) // 4
            
            # Dibujar círculo (simplificado)
            for angle in range(0, 360, 10):
                rad = angle * 3.14159 / 180
                x = center_x + int(radius * 0.8 * (1 + intensity * 0.2) * (1 if angle % 2 == 0 else -1))
                y = center_y + int(radius * 0.8 * (1 + intensity * 0.2) * (1 if angle % 2 == 1 else -1))
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.oled.pixel(x, y, 1)
            
            self.oled.show()
            intensity += 0.1 * direction
            if intensity <= 0 or intensity >= 1:
                direction *= -1
            time.sleep(0.1)
        self.clear()
    
    def show_felix_face(self, emotion: str = "neutral") -> bool:
        """
        Muestra una cara de Félix en la pantalla.
        
        Args:
            emotion: Emoción para la cara (ej: "happy", "sad", "surprised").
        
        Returns:
            bool: True si fue exitoso, False en caso contrario.
        """
        if not self.is_initialized or self.oled is None:
            print("[Display] Pantalla no inicializada")
            return False
        
        try:
            self.clear()
            
            # Dibujar cara de gato (simplificada)
            center_x = self.width // 2
            center_y = self.height // 2
            
            # Orejas
            self.oled.line(center_x - 20, center_y - 10, center_x - 30, center_y - 20, 1)
            self.oled.line(center_x + 20, center_y - 10, center_x + 30, center_y - 20, 1)
            self.oled.line(center_x - 30, center_y - 20, center_x - 20, center_y - 10, 1)
            self.oled.line(center_x + 30, center_y - 20, center_x + 20, center_y - 10, 1)
            
            # Cabeza
            self.oled.circle(center_x, center_y - 5, 20, 1)
            
            # Ojos
            if emotion == "happy":
                # Ojos felices (cerrados parcialmente)
                self.oled.line(center_x - 10, center_y - 5, center_x - 5, center_y - 5, 1)
                self.oled.line(center_x + 5, center_y - 5, center_x + 10, center_y - 5, 1)
            elif emotion == "surprised":
                # Ojos grandes
                self.oled.circle(center_x - 8, center_y - 5, 3, 1)
                self.oled.circle(center_x + 8, center_y - 5, 3, 1)
            else:
                # Ojos normales
                self.oled.circle(center_x - 8, center_y - 5, 2, 1)
                self.oled.circle(center_x + 8, center_y - 5, 2, 1)
            
            # Nariz
            self.oled.fill_triangle(
                [center_x, center_y + 5],
                [center_x - 3, center_y + 8],
                [center_x + 3, center_y + 8],
                1
            )
            
            # Boca
            if emotion == "happy":
                # Sonrisa
                self.oled.line(center_x - 5, center_y + 12, center_x + 5, center_y + 12, 1)
                self.oled.line(center_x - 5, center_y + 12, center_x - 8, center_y + 15, 1)
                self.oled.line(center_x + 5, center_y + 12, center_x + 8, center_y + 15, 1)
            elif emotion == "sad":
                # Boca triste
                self.oled.line(center_x - 5, center_y + 12, center_x + 5, center_y + 12, 1)
                self.oled.line(center_x - 5, center_y + 12, center_x - 8, center_y + 10, 1)
                self.oled.line(center_x + 5, center_y + 12, center_x + 8, center_y + 10, 1)
            else:
                # Boca neutral
                self.oled.line(center_x - 5, center_y + 10, center_x + 5, center_y + 10, 1)
            
            # Bigotes
            self.oled.line(center_x - 20, center_y, center_x - 30, center_y, 1)
            self.oled.line(center_x + 20, center_y, center_x + 30, center_y, 1)
            self.oled.line(center_x - 20, center_y + 5, center_x - 30, center_y + 5, 1)
            self.oled.line(center_x + 20, center_y + 5, center_x + 30, center_y + 5, 1)
            
            self.oled.show()
            print(f"[Display] Cara de Félix mostrada (emoción: {emotion})")
            return True
            
        except Exception as e:
            print(f"[Display] Error al mostrar cara: {e}")
            return False
    
    def show_progress(self, progress: int, total: int = 100, label: str = "") -> bool:
        """
        Muestra una barra de progreso.
        
        Args:
            progress: Progreso actual.
            total: Total (default: 100).
            label: Etiqueta para mostrar (default: "").
        
        Returns:
            bool: True si fue exitoso, False en caso contrario.
        """
        if not self.is_initialized or self.oled is None:
            print("[Display] Pantalla no inicializada")
            return False
        
        try:
            self.clear()
            
            # Mostrar etiqueta
            if label:
                self.oled.text(label, 0, 0)
            
            # Calcular ancho de la barra
            bar_width = int((progress / total) * self.width)
            
            # Dibujar barra de progreso
            self.oled.hline(0, 20, self.width, 1)  # Línea base
            self.oled.hline(0, 20, bar_width, 1)  # Línea de progreso (invertida)
            for x in range(bar_width):
                self.oled.pixel(x, 21, 1)
            
            # Mostrar porcentaje
            percentage = int((progress / total) * 100)
            self.oled.text(f"{percentage}%", 0, 30)
            
            self.oled.show()
            return True
            
        except Exception as e:
            print(f"[Display] Error al mostrar progreso: {e}")
            return False
    
    def deinitialize(self):
        """Desinicializa la pantalla."""
        if self.oled is not None:
            self.clear()
            self.oled = None
        if self.i2c is not None:
            self.i2c.deinit()
            self.i2c = None
        self.is_initialized = False
        print("[Display] Pantalla desinicializada")


# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def create_felix_emoji(emotion: str = "happy") -> bytes:
    """
    Crea un emoji de Félix en formato de bitmap.
    
    Args:
        emotion: Emoción para el emoji (default: "happy").
    
    Returns:
        bytes: Bitmap del emoji (simplificado).
    """
    # Implementación para futuras versiones
    return b""
