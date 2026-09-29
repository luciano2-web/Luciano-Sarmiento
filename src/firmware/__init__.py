# -*- coding: utf-8 -*-
"""
Firmware Module for Félix / GatoGPT

Este módulo contiene el firmware para el ESP32:
- main.py: Punto de entrada principal
- bluetooth_bridge.py: Comunicación Bluetooth con la app móvil
- audio_handler.py: Manejo de audio (micrófono y parlante)
- display.py: Control de la pantalla OLED
- config.py: Configuración del hardware

Uso:
    from src.firmware.bluetooth_bridge import BluetoothBridge
    from src.firmware.audio_handler import AudioHandler
    from src.firmware.display import DisplayController
"""

__version__ = "2.0.0"
__author__ = "Luciano Sarmiento"
__description__ = "Firmware para ESP32 de Félix / GatoGPT"
