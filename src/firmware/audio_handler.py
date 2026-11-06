# -*- coding: utf-8 -*-
"""Grabación y reproducción básica de audio para MicroPython en ESP32."""

import time
from machine import I2S, Pin, PWM

try:
    from src.core.constants import (
        ESP32_I2S_BCK_PIN,
        ESP32_I2S_WS_PIN,
        ESP32_I2S_SD_PIN,
        ESP32_I2S_PORT,
        ESP32_SPEAKER_PIN,
    )
except ImportError:
    ESP32_I2S_BCK_PIN = 27
    ESP32_I2S_WS_PIN = 23
    ESP32_I2S_SD_PIN = 25
    ESP32_I2S_PORT = 0
    ESP32_SPEAKER_PIN = 26


class AudioHandler:
    """Gestiona captura I2S y salida PWM experimental."""

    def __init__(self):
        self.i2s = None
        self.pwm = None
        self.is_initialized = False
        self.sample_rate = 16000
        self.bits_per_sample = 16

    def initialize(self, sample_rate=16000, bits_per_sample=16):
        """Inicializa el micrófono I2S y la salida PWM; devuelve éxito o fallo."""
        self.sample_rate = sample_rate
        self.bits_per_sample = bits_per_sample
        try:
            self.i2s = I2S(
                ESP32_I2S_PORT,
                sck=Pin(ESP32_I2S_BCK_PIN),
                ws=Pin(ESP32_I2S_WS_PIN),
                sd=Pin(ESP32_I2S_SD_PIN),
                mode=I2S.RX,
                bits=bits_per_sample,
                format=I2S.MONO,
                rate=sample_rate,
                ibuf=4096,
            )
            self.pwm = PWM(Pin(ESP32_SPEAKER_PIN))
            self._set_duty(0)
            self.is_initialized = True
            return True
        except Exception as exc:
            print(f"[Audio] Error al inicializar: {exc}")
            self.deinitialize()
            return False

    def _set_duty(self, value):
        """Ajusta PWM en MicroPython antiguo (10 bits) o actual (16 bits)."""
        if self.pwm is None:
            return
        if hasattr(self.pwm, "duty_u16"):
            self.pwm.duty_u16(max(0, min(65535, value * 65535 // 1023)))
        else:
            self.pwm.duty(max(0, min(1023, value)))

    def record(self, duration=1.0):
        """Graba PCM mono usando readinto, API estándar de I2S en MicroPython."""
        if not self.is_initialized or self.i2s is None or duration <= 0:
            return b""
        target_bytes = int(duration * self.sample_rate * self.bits_per_sample // 8)
        audio_data = bytearray()
        block = bytearray(min(1024, target_bytes))
        deadline = time.ticks_add(time.ticks_ms(), int(duration * 1000))
        try:
            while len(audio_data) < target_bytes and time.ticks_diff(deadline, time.ticks_ms()) > 0:
                count = self.i2s.readinto(block)
                if count:
                    remaining = target_bytes - len(audio_data)
                    audio_data.extend(memoryview(block)[:min(count, remaining)])
            return bytes(audio_data)
        except Exception as exc:
            print(f"[Audio] Error al grabar: {exc}")
            return b""

    def play(self, audio_data, sample_rate=16000):
        """Reproduce PCM firmado de 16 bits mediante PWM (calidad limitada)."""
        if not self.is_initialized or self.pwm is None or not audio_data or sample_rate <= 0:
            return False
        try:
            period_us = max(1, 1000000 // sample_rate)
            for index in range(0, len(audio_data) - 1, 2):
                sample = audio_data[index] | (audio_data[index + 1] << 8)
                if sample >= 32768:
                    sample -= 65536
                self._set_duty((sample + 32768) * 1023 // 65535)
                time.sleep_us(period_us)
            self._set_duty(0)
            return True
        except Exception as exc:
            print(f"[Audio] Error al reproducir: {exc}")
            self._set_duty(0)
            return False

    def play_tone(self, frequency, duration=0.5):
        """Reproduce un tono de prueba."""
        if not self.is_initialized or self.pwm is None or frequency <= 0 or duration < 0:
            return False
        try:
            self.pwm.freq(frequency)
            self._set_duty(512)
            time.sleep(duration)
            self._set_duty(0)
            return True
        except Exception as exc:
            print(f"[Audio] Error al reproducir tono: {exc}")
            self._set_duty(0)
            return False

    def stop(self):
        """Silencia la salida PWM."""
        self._set_duty(0)

    def deinitialize(self):
        """Libera los periféricos de audio, incluso tras un fallo parcial."""
        self.stop()
        for peripheral in (self.i2s, self.pwm):
            if peripheral is not None:
                try:
                    peripheral.deinit()
                except Exception:
                    pass
        self.i2s = None
        self.pwm = None
        self.is_initialized = False


def normalize_audio(audio_data, target_volume=50):
    """Devuelve el audio sin cambios; normalización aún no implementada."""
    return audio_data


def convert_to_mono(audio_data):
    """El INMP441 ya entrega captura mono; conserva los bytes recibidos."""
    return audio_data
