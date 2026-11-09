# -*- coding: utf-8 -*-
"""Sensor capacitivo de tacto para Félix (ESP32 clásico / MicroPython).

Un toque corto genera el evento "pet". Mantener el contacto genera
"press_to_talk_start" y soltar genera "press_to_talk_end".
Este módulo detecta contacto, no mide la fuerza de presión.
"""

import time

try:
    from src.core.constants import ESP32_TOUCH_PIN
except ImportError:
    ESP32_TOUCH_PIN = 32


def _ticks_ms():
    if hasattr(time, "ticks_ms"):
        return time.ticks_ms()
    return int(time.time() * 1000)


def _ticks_diff(newer, older):
    if hasattr(time, "ticks_diff"):
        return time.ticks_diff(newer, older)
    return newer - older


class TouchSensor:
    """Lee un TouchPad del ESP32 y convierte el contacto en eventos."""

    def __init__(
        self,
        touchpad,
        threshold,
        long_press_ms=900,
        debounce_ms=60,
        double_tap_ms=450,
        clock_ms=None,
    ):
        if touchpad is None:
            raise ValueError("Se necesita un objeto TouchPad válido")
        if long_press_ms <= 0 or debounce_ms < 0:
            raise ValueError("Los tiempos deben ser positivos")
        self.touchpad = touchpad
        self.threshold = threshold
        self.long_press_ms = long_press_ms
        self.debounce_ms = debounce_ms
        self.double_tap_ms = double_tap_ms
        self._last_short_release = None
        self.clock_ms = clock_ms or _ticks_ms
        self._stable_touched = False
        self._candidate_touched = False
        self._candidate_since = None
        self._pressed_at = None
        self._long_press_sent = False

    @classmethod
    def from_esp32(cls, pin=ESP32_TOUCH_PIN, samples=24, sample_delay_ms=20,
                   threshold_ratio=0.80, long_press_ms=900,
                   debounce_ms=60):
        """Crea el TouchPad y calibra sin tocar el electrodo.

        GPIO32 admite TouchPad en ESP32 clásico. Mantén libre ese pin
        y realiza la calibración con el sensor sin contacto.
        """
        from machine import Pin, TouchPad

        if not 0 < threshold_ratio < 1:
            raise ValueError("threshold_ratio debe estar entre 0 y 1")
        if samples <= 0:
            raise ValueError("samples debe ser mayor que cero")
        pad = TouchPad(Pin(pin))
        values = []
        for _ in range(samples):
            values.append(pad.read())
            if hasattr(time, "sleep_ms"):
                time.sleep_ms(sample_delay_ms)
            else:
                time.sleep(sample_delay_ms / 1000)
        baseline = sum(values) / len(values)
        if baseline <= 0:
            raise ValueError("No se pudo calibrar el sensor: lectura base inválida")
        threshold = int(baseline * threshold_ratio)
        print("[Touch] Calibración: base={}, umbral={}".format(
            int(baseline), threshold
        ))
        return cls(
            pad,
            threshold,
            long_press_ms=long_press_ms,
            debounce_ms=debounce_ms,
        )

    def read_raw(self):
        """Devuelve la lectura capacitiva sin procesar."""
        return self.touchpad.read()

    def poll(self, now_ms=None):
        """Devuelve un evento o None; llamar repetidamente desde el bucle principal.

        En ESP32 clásico, una lectura menor que el umbral indica contacto.
        """
        now = self.clock_ms() if now_ms is None else now_ms
        raw = self.read_raw()
        touched = raw < self.threshold

        if touched != self._candidate_touched:
            self._candidate_touched = touched
            self._candidate_since = now
            return None

        if touched != self._stable_touched:
            if self._candidate_since is None:
                self._candidate_since = now
                return None
            if _ticks_diff(now, self._candidate_since) < self.debounce_ms:
                return None

            self._stable_touched = touched
            if touched:
                self._pressed_at = now
                self._long_press_sent = False
                return {"type": "touch_start", "raw": raw}

            was_long_press = self._long_press_sent
            self._pressed_at = None
            self._long_press_sent = False
            if was_long_press:
                self._last_short_release = None
                event_type = "press_to_talk_end"
            elif (self._last_short_release is not None and
                  _ticks_diff(now, self._last_short_release) <= self.double_tap_ms):
                self._last_short_release = None
                event_type = "annoyed"
            else:
                self._last_short_release = now
                event_type = "pet"
            return {"type": event_type, "raw": raw}

        if touched and not self._long_press_sent:
            if self._pressed_at is not None:
                elapsed = _ticks_diff(now, self._pressed_at)
                if elapsed >= self.long_press_ms:
                    self._long_press_sent = True
                    return {"type": "press_to_talk_start", "raw": raw}

        return None
