# -*- coding: utf-8 -*-
"""
Audio Handler para Félix / GatoGPT

Módulo para manejar la grabación y reproducción de audio en el ESP32.
Soporta:
- Grabación de audio usando el micrófono INMP441 (I2S)
- Reproducción de audio usando un parlante (PWM)

Dependencias:
    - MicroPython (ESP32)
    - Módulo machine para I2S y PWM

Uso:
    from src.firmware.audio_handler import AudioHandler
    
    audio = AudioHandler()
    audio.initialize()
    
    # Grabar audio
    audio_data = audio.record(duration=3)  # Grabar 3 segundos
    
    # Reproducir audio
    audio.play(audio_data)
"""

import time
from machine import I2S, Pin, PWM

# Importar constantes
try:
    from src.core.constants import (
        ESP32_I2S_BCK_PIN,
        ESP32_I2S_WS_PIN,
        ESP32_I2S_SD_PIN,
        ESP32_I2S_PORT,
        ESP32_SPEAKER_PIN,
    )
except ImportError:
    # Fallback si no se encuentra el módulo de constantes
    ESP32_I2S_BCK_PIN = 24  # GPIO 24
    ESP32_I2S_WS_PIN = 23   # GPIO 23
    ESP32_I2S_SD_PIN = 25   # GPIO 25
    ESP32_I2S_PORT = 0     # Puerto I2S 0
    ESP32_SPEAKER_PIN = 26 # GPIO 26


class AudioHandler:
    """
    Clase para manejar la grabación y reproducción de audio.
    
    Atributos:
        i2s (I2S): Objeto I2S para grabación.
        pwm (PWM): Objeto PWM para reproducción.
        is_initialized (bool): Indica si el audio está inicializado.
    """
    
    def __init__(self):
        """Inicializa el manejador de audio."""
        self.i2s = None
        self.pwm = None
        self.is_initialized = False
    
    def initialize(self, sample_rate: int = 16000, bits_per_sample: int = 16) -> bool:
        """
        Inicializa el hardware de audio (I2S para micrófono, PWM para parlante).
        
        Args:
            sample_rate: Frecuencia de muestreo en Hz (default: 16000).
            bits_per_sample: Bits por muestra (default: 16).
        
        Returns:
            bool: True si la inicialización fue exitosa, False en caso contrario.
        """
        try:
            # Inicializar I2S para el micrófono INMP441
            self._initialize_i2s(sample_rate, bits_per_sample)
            
            # Inicializar PWM para el parlante
            self._initialize_pwm()
            
            self.is_initialized = True
            print(f"[Audio] Inicializado: I2S @ {sample_rate}Hz, {bits_per_sample} bits")
            return True
            
        except Exception as e:
            print(f"[Audio] Error al inicializar: {e}")
            self.is_initialized = False
            return False
    
    def _initialize_i2s(self, sample_rate: int, bits_per_sample: int):
        """
        Inicializa el periférico I2S para el micrófono INMP441.
        
        Args:
            sample_rate: Frecuencia de muestreo en Hz.
            bits_per_sample: Bits por muestra.
        """
        try:
            # Configurar pines
            bck_pin = Pin(ESP32_I2S_BCK_PIN)
            ws_pin = Pin(ESP32_I2S_WS_PIN)
            sd_pin = Pin(ESP32_I2S_SD_PIN)
            
            # Configurar I2S
            self.i2s = I2S(
                ESP32_I2S_PORT,
                sck=bck_pin,
                ws=ws_pin,
                sd=sd_pin,
                mode=I2S.RX,  # Modo recepción (grabación)
                bits=bits_per_sample,
                format=I2S.MONO,  # Mono (el INMP441 es mono)
                rate=sample_rate,
                ibuf=2048,  # Tamaño del buffer de entrada
            )
            print(f"[Audio] I2S inicializado para grabación")
            
        except Exception as e:
            print(f"[Audio] Error al inicializar I2S: {e}")
            self.i2s = None
    
    def _initialize_pwm(self):
        """Inicializa el PWM para el parlante."""
        try:
            # Configurar PWM para el parlante
            self.pwm = PWM(Pin(ESP32_SPEAKER_PIN))
            self.pwm.freq(44100)  # Frecuencia de 44.1 kHz (calidad CD)
            self.pwm.duty(0)  # Inicialmente apagado
            print(f"[Audio] PWM inicializado para parlante en GPIO {ESP32_SPEAKER_PIN}")
            
        except Exception as e:
            print(f"[Audio] Error al inicializar PWM: {e}")
            self.pwm = None
    
    def record(self, duration: float = 1.0) -> bytes:
        """
        Graba audio desde el micrófono INMP441.
        
        Args:
            duration: Duración de la grabación en segundos (default: 1.0).
        
        Returns:
            bytes: Datos de audio grabados. Si hay error, devuelve b''.
        """
        if not self.is_initialized or self.i2s is None:
            print("[Audio] Audio no inicializado")
            return b''
        
        try:
            # Calcular número de muestras a grabar
            samples = int(duration * self.i2s.rate())
            
            # Leer datos del I2S
            audio_data = bytearray()
            
            # Leer en bloques para evitar desbordamiento de buffer
            block_size = 1024
            blocks_to_read = (samples * 2) // block_size  # 2 bytes por muestra (16 bits)
            
            for _ in range(blocks_to_read):
                block = self.i2s.read(block_size)
                if block:
                    audio_data.extend(block)
            
            print(f"[Audio] Grabados {len(audio_data)} bytes ({duration}s)")
            return bytes(audio_data)
            
        except Exception as e:
            print(f"[Audio] Error al grabar: {e}")
            return b''
    
    def play(self, audio_data: bytes, sample_rate: int = 16000) -> bool:
        """
        Reproduce audio a través del parlante usando PWM.
        
        Args:
            audio_data: Datos de audio a reproducir (formato raw PCM).
            sample_rate: Frecuencia de muestreo en Hz (default: 16000).
        
        Returns:
            bool: True si la reproducción fue exitosa, False en caso contrario.
        
        Nota:
            Este método implementa una reproducción básica usando PWM.
            Para mejor calidad, considera usar un DAC externo o el I2S en modo TX.
        """
        if not self.is_initializado or self.pwm is None:
            print("[Audio] Audio no inicializado")
            return False
        
        if not audio_data:
            print("[Audio] Datos de audio vacíos")
            return False
        
        try:
            # Configurar frecuencia del PWM según la frecuencia de muestreo
            self.pwm.freq(sample_rate)
            
            # Reproducir cada muestra
            # Nota: Esto es una implementación simplificada.
            # Para audio de calidad, se necesita un DAC o I2S en modo TX.
            for i in range(0, len(audio_data), 2):
                # Leer muestra de 16 bits (little-endian)
                if i + 1 < len(audio_data):
                    sample = audio_data[i] | (audio_data[i + 1] << 8)
                    # Convertir a valor de duty (0-1023 para PWM de 10 bits)
                    duty = int((sample + 32768) / 65535 * 1023)
                    self.pwm.duty(duty)
                    # Pequeña pausa para mantener la frecuencia de muestreo
                    time.sleep_us(1000000 // sample_rate)
            
            # Apagar el PWM al terminar
            self.pwm.duty(0)
            print(f"[Audio] Reproducidos {len(audio_data)} bytes")
            return True
            
        except Exception as e:
            print(f"[Audio] Error al reproducir: {e}")
            self.pwm.duty(0)
            return False
    
    def play_tone(self, frequency: int, duration: float = 0.5) -> bool:
        """
        Reproduce un tono simple (para pruebas o notificaciones).
        
        Args:
            frequency: Frecuencia del tono en Hz.
            duration: Duración en segundos (default: 0.5).
        
        Returns:
            bool: True si fue exitoso, False en caso contrario.
        """
        if not self.is_initialized or self.pwm is None:
            print("[Audio] Audio no inicializado")
            return False
        
        try:
            self.pwm.freq(frequency)
            self.pwm.duty(512)  # 50% duty cycle
            time.sleep(duration)
            self.pwm.duty(0)
            return True
            
        except Exception as e:
            print(f"[Audio] Error al reproducir tono: {e}")
            self.pwm.duty(0)
            return False
    
    def stop(self):
        """Detiene la reproducción de audio."""
        if self.pwm is not None:
            self.pwm.duty(0)
        print("[Audio] Reproducción detenida")
    
    def deinitialize(self):
        """Desinicializa el hardware de audio."""
        self.stop()
        if self.i2s is not None:
            self.i2s.deinit()
            self.i2s = None
        if self.pwm is not None:
            self.pwm.deinit()
            self.pwm = None
        self.is_initialized = False
        print("[Audio] Audio desinicializado")


# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def normalize_audio(audio_data: bytes, target_volume: int = 50) -> bytes:
    """
    Normaliza el volumen de los datos de audio.
    
    Args:
        audio_data: Datos de audio en formato raw PCM (16 bits).
        target_volume: Volumen objetivo en porcentaje (0-100).
    
    Returns:
        bytes: Datos de audio normalizados.
    """
    # Implementación simplificada
    # En una implementación real, se calcularía el máximo y se escalaría
    return audio_data


def convert_to_mono(audio_data: bytes) -> bytes:
    """
    Convierte audio estéreo a mono (si es necesario).
    
    Args:
        audio_data: Datos de audio.
    
    Returns:
        bytes: Datos de audio en mono.
    """
    # El INMP441 ya graba en mono, así que esto es solo por compatibilidad
    return audio_data
