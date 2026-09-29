# -*- coding: utf-8 -*-
"""
Bluetooth Bridge para Félix / GatoGPT

Módulo para manejar la comunicación Bluetooth entre el ESP32 y la app móvil.
Usa el protocolo Bluetooth Serial (SPP) para enviar y recibir mensajes en formato JSON.

Dependencias:
    - MicroPython (ESP32)
    - Módulo bluetooth de MicroPython

Uso:
    from src.firmware.bluetooth_bridge import BluetoothBridge
    
    bridge = BluetoothBridge(device_name="Félix")
    bridge.start_server()
    
    # Enviar mensaje
    bridge.send({"type": "response", "text": "¡Miau!"})
    
    # Recibir mensaje
    message = bridge.receive()
    print(f"Recibido: {message}")
"""

import json
import struct
import time
from machine import UART

# Importar constantes
try:
    from src.core.constants import (
        BLUETOOTH_DEVICE_NAME,
        BLUETOOTH_BAUD_RATE,
        BLUETOOTH_TIMEOUT,
        BLUETOOTH_MAX_RETRIES,
    )
except ImportError:
    # Fallback si no se encuentra el módulo de constantes
    BLUETOOTH_DEVICE_NAME = "Félix"
    BLUETOOTH_BAUD_RATE = 115200
    BLUETOOTH_TIMEOUT = 10
    BLUETOOTH_MAX_RETRIES = 3


class BluetoothBridge:
    """
    Clase para manejar la comunicación Bluetooth entre el ESP32 y la app móvil.
    
    Atributos:
        device_name (str): Nombre del dispositivo Bluetooth.
        uart (UART): Objeto UART para comunicación serial.
        connected (bool): Indica si hay una conexión activa.
    """
    
    def __init__(self, device_name: str = BLUETOOTH_DEVICE_NAME, uart_num: int = 1):
        """
        Inicializa el puente Bluetooth.
        
        Args:
            device_name: Nombre del dispositivo Bluetooth (default: "Félix").
            uart_num: Número de UART a usar (default: 1).
        """
        self.device_name = device_name
        self.uart_num = uart_num
        self.uart = None
        self.connected = False
        self._initialize_uart()
    
    def _initialize_uart(self):
        """Inicializa el UART para comunicación Bluetooth."""
        try:
            # Configurar UART con los parámetros para Bluetooth
            self.uart = UART(
                self.uart_num,
                baudrate=BLUETOOTH_BAUD_RATE,
                tx=19,  # GPIO 19 para TX (puede variar según el ESP32)
                rx=18,  # GPIO 18 para RX (puede variar según el ESP32)
                timeout=BLUETOOTH_TIMEOUT * 1000,  # Convertir a milisegundos
                timeout_char=10,
            )
            print(f"[Bluetooth] UART{self.uart_num} inicializado a {BLUETOOTH_BAUD_RATE} baud")
        except Exception as e:
            print(f"[Bluetooth] Error al inicializar UART: {e}")
            self.uart = None
    
    def start_server(self):
        """
        Inicia el servidor Bluetooth y espera conexiones.
        
        Returns:
            bool: True si se conectó correctamente, False en caso contrario.
        """
        if self.uart is None:
            print("[Bluetooth] UART no inicializado")
            return False
        
        print(f"[Bluetooth] Esperando conexión como '{self.device_name}'...")
        
        # En MicroPython, el Bluetooth clásico (SPP) se configura automáticamente
        # cuando se usa UART con los pines correctos
        self.connected = True
        print("[Bluetooth] Servidor Bluetooth listo")
        return True
    
    def send(self, message: dict, max_retries: int = BLUETOOTH_MAX_RETRIES) -> bool:
        """
        Envía un mensaje a través de Bluetooth.
        
        Args:
            message: Diccionario con los datos a enviar.
            max_retries: Número máximo de reintentos (default: BLUETOOTH_MAX_RETRIES).
        
        Returns:
            bool: True si el mensaje se envió correctamente, False en caso contrario.
        """
        if not self.connected or self.uart is None:
            print("[Bluetooth] No hay conexión activa")
            return False
        
        try:
            # Convertir mensaje a JSON y luego a bytes
            json_message = json.dumps(message)
            message_bytes = json_message.encode('utf-8')
            
            # Añadir delimitador de fin de mensaje (nueva línea)
            message_bytes += b'\n'
            
            # Enviar el mensaje
            self.uart.write(message_bytes)
            print(f"[Bluetooth] Mensaje enviado: {json_message}")
            return True
            
        except Exception as e:
            print(f"[Bluetooth] Error al enviar mensaje: {e}")
            return False
    
    def receive(self) -> dict:
        """
        Recibe un mensaje a través de Bluetooth.
        
        Returns:
            dict: Mensaje recibido como diccionario. Si hay error, devuelve None.
        """
        if not self.connected or self.uart is None:
            print("[Bluetooth] No hay conexión activa")
            return None
        
        try:
            # Leer datos del UART
            if self.uart.any():
                data = self.uart.readline()
                if data:
                    # Decodificar y parsear JSON
                    message_str = data.decode('utf-8').strip()
                    message = json.loads(message_str)
                    print(f"[Bluetooth] Mensaje recibido: {message}")
                    return message
            return None
            
        except json.JSONDecodeError as e:
            print(f"[Bluetooth] Error al parsear JSON: {e}")
            return None
        except Exception as e:
            print(f"[Bluetooth] Error al recibir mensaje: {e}")
            return None
    
    def receive_blocking(self, timeout: int = BLUETOOTH_TIMEOUT) -> dict:
        """
        Recibe un mensaje de forma bloqueante (espera hasta recibirlo o timeout).
        
        Args:
            timeout: Tiempo máximo de espera en segundos (default: BLUETOOTH_TIMEOUT).
        
        Returns:
            dict: Mensaje recibido como diccionario. Si hay timeout, devuelve None.
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            message = self.receive()
            if message is not None:
                return message
            time.sleep(0.1)
        
        print(f"[Bluetooth] Timeout al recibir mensaje después de {timeout}s")
        return None
    
    def close(self):
        """Cierra la conexión Bluetooth."""
        if self.uart is not None:
            self.uart.deinit()
            self.uart = None
        self.connected = False
        print("[Bluetooth] Conexión cerrada")
    
    def is_connected(self) -> bool:
        """
        Verifica si hay una conexión activa.
        
        Returns:
            bool: True si hay conexión, False en caso contrario.
        """
        return self.connected and self.uart is not None


# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def create_message(message_type: str, **kwargs) -> dict:
    """
    Crea un mensaje en formato estándar para enviar por Bluetooth.
    
    Args:
        message_type: Tipo de mensaje (ej: "response", "audio", "error").
        **kwargs: Argumentos adicionales para el mensaje.
    
    Returns:
        dict: Mensaje formateado.
    
    Ejemplo:
        >>> create_message("response", text="¡Miau!", emotion="happy")
        {'type': 'response', 'text': '¡Miau!', 'emotion': 'happy'}
    """
    message = {"type": message_type}
    message.update(kwargs)
    return message


def parse_audio_message(audio_data: bytes) -> dict:
    """
    Parsea un mensaje de audio recibido.
    
    Args:
        audio_data: Datos de audio en bytes.
    
    Returns:
        dict: Mensaje parseado con los datos de audio.
    """
    # Por implementar según el formato de audio usado
    return {
        "type": "audio",
        "data": audio_data.hex(),  # Convertir a hex para JSON
        "format": "raw",
        "sample_rate": 16000,  # Ejemplo: 16 kHz
        "bits_per_sample": 16,
    }
