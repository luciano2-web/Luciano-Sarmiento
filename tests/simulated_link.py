"""Simulación local del enlace app <-> Félix, sin radio Bluetooth real.

Sirve para probar el formato y el intercambio de mensajes antes de conectar
una placa. No emula alcance, interferencias, emparejamiento ni BLE/GATT.
"""
from collections import deque

from src.core.device_protocol import encode_message, decode_message


class SimulatedLink:
    def __init__(self):
        self.app_to_robot = deque()
        self.robot_to_app = deque()
        self.connected = True

    def app_send(self, message_type, payload=None, request_id=None):
        if not self.connected:
            raise ConnectionError("Enlace simulado desconectado")
        self.app_to_robot.append(
            encode_message(message_type, payload, request_id)
        )

    def robot_receive(self):
        if not self.app_to_robot:
            return None
        return decode_message(self.app_to_robot.popleft())

    def robot_send(self, message_type, payload=None, request_id=None):
        if not self.connected:
            raise ConnectionError("Enlace simulado desconectado")
        self.robot_to_app.append(
            encode_message(message_type, payload, request_id)
        )

    def app_receive(self):
        if not self.robot_to_app:
            return None
        return decode_message(self.robot_to_app.popleft())

    def disconnect(self):
        self.connected = False
