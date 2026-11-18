# -*- coding: utf-8 -*-
"""Servidor BLE GATT para ESP32 con MicroPython.

Expone un servicio tipo Nordic UART Service (NUS). Esto es BLE, no Bluetooth
Classic SPP. El estado conectado solo cambia tras eventos reales de la radio.
La app cliente todavía debe descubrir el servicio y sus características.
"""
try:
    import bluetooth
except ImportError:
    bluetooth = None

try:
    from src.core.constants import BLUETOOTH_DEVICE_NAME
except ImportError:
    BLUETOOTH_DEVICE_NAME = "Felix"

try:
    from src.core.device_protocol import (
        MAX_MESSAGE_BYTES, ProtocolError, decode_message, encode_message,
    )
except ImportError:
    # Permite copiar este módulo al ESP32 sin instalar el paquete completo.
    MAX_MESSAGE_BYTES = 4096

    class ProtocolError(ValueError):
        pass

    def decode_message(raw):
        import json
        if isinstance(raw, str):
            raw = raw.encode("utf-8")
        if not raw or len(raw) > MAX_MESSAGE_BYTES:
            raise ProtocolError("Tamaño de mensaje inválido")
        try:
            message = json.loads(raw.decode("utf-8").strip())
        except (ValueError, UnicodeError) as exc:
            raise ProtocolError("JSON inválido") from exc
        allowed = (
            "hello", "hello_ack", "ping", "pong", "touch_event",
            "audio_start", "audio_end", "transcript", "assistant_text",
            "tts_start", "tts_end", "emotion", "display_text", "diagnostic", "error",
        )
        if not isinstance(message, dict) or message.get("version") != 1:
            raise ProtocolError("Mensaje o versión inválidos")
        if message.get("type") not in allowed:
            raise ProtocolError("Tipo de mensaje desconocido")
        if not isinstance(message.get("payload", {}), dict):
            raise ProtocolError("payload debe ser un objeto")
        return message

    def encode_message(message_type, payload=None, request_id=None):
        import json
        allowed = (
            "hello", "hello_ack", "ping", "pong", "touch_event",
            "audio_start", "audio_end", "transcript", "assistant_text",
            "tts_start", "tts_end", "emotion", "display_text", "diagnostic", "error",
        )
        if message_type not in allowed:
            raise ProtocolError("Tipo de mensaje no permitido")
        message = {"version": 1, "type": message_type, "payload": payload or {}}
        if request_id is not None:
            message["request_id"] = str(request_id)
        raw = json.dumps(message, separators=(",", ":")).encode("utf-8")
        if len(raw) > MAX_MESSAGE_BYTES:
            raise ProtocolError("Mensaje demasiado grande")
        return raw + b"\\n"


_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
_TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
_FLAG_WRITE = (bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE) if bluetooth else 0
_FLAG_NOTIFY = bluetooth.FLAG_NOTIFY if bluetooth else 0


def _advertising_payload(name):
    name_bytes = name.encode("utf-8")
    if len(name_bytes) > 26:
        raise ValueError("Nombre BLE demasiado largo para el paquete de anuncio")
    return bytes((2, 0x01, 0x06, len(name_bytes) + 1, 0x09)) + name_bytes


class BluetoothBridge:
    """Servidor BLE UART con framing JSONL y validación compartida."""

    def __init__(self, device_name=BLUETOOTH_DEVICE_NAME, max_queue=16):
        self.device_name = device_name
        self.max_queue = max(1, int(max_queue))
        self.ble = None
        self.connected = False
        self._connections = set()
        self._rx_buffer = b""
        self._messages = []
        self._tx_handle = None
        self._rx_handle = None

    def start_server(self):
        if bluetooth is None:
            print("[BLE] Este firmware no incluye el módulo bluetooth")
            return False
        try:
            self.ble = bluetooth.BLE()
            self.ble.active(True)
            self.ble.irq(self._irq)
            ((self._tx_handle, self._rx_handle),) = self.ble.gatts_register_services((
                (_UART_UUID, ((_TX_UUID, _FLAG_NOTIFY), (_RX_UUID, _FLAG_WRITE))),
            ))
            self.ble.gap_advertise(100000, adv_data=_advertising_payload(self.device_name))
            print("[BLE] Anunciando '{}'; esperando conexión BLE real".format(self.device_name))
            return True
        except Exception as exc:
            self.connected = False
            print("[BLE] No se pudo iniciar BLE: {}".format(exc))
            return False

    def _queue_line(self, line):
        if not line:
            return
        if len(line) > MAX_MESSAGE_BYTES:
            print("[BLE] Mensaje descartado: supera el límite")
            return
        try:
            message = decode_message(line)
        except (ProtocolError, ValueError) as exc:
            print("[BLE] Mensaje inválido: {}".format(exc))
            return
        if len(self._messages) >= self.max_queue:
            self._messages.pop(0)
            print("[BLE] Cola llena; se descartó el mensaje más antiguo")
        self._messages.append(message)

    def _irq(self, event, data):
        if event == 1:  # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self.connected = True
            print("[BLE] Central conectado: {}".format(conn_handle))
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            conn_handle, _, _ = data
            self._connections.discard(conn_handle)
            self.connected = bool(self._connections)
            if not self._connections:
                self._rx_buffer = b""
            print("[BLE] Central desconectado: {}".format(conn_handle))
            if self.ble is not None:
                self.ble.gap_advertise(100000, adv_data=_advertising_payload(self.device_name))
        elif event == 3:  # _IRQ_GATTS_WRITE
            _, value_handle = data
            if value_handle != self._rx_handle:
                return
            chunk = self.ble.gatts_read(self._rx_handle)
            for byte in chunk:
                if byte == 10:
                    self._queue_line(self._rx_buffer)
                    self._rx_buffer = b""
                elif len(self._rx_buffer) < MAX_MESSAGE_BYTES:
                    self._rx_buffer += bytes((byte,))
                else:
                    self._rx_buffer = b""
                    print("[BLE] Trama descartada: supera el límite")

    def send(self, message):
        if not self.connected or self.ble is None or self._tx_handle is None:
            return False
        try:
            data = encode_message(message.get("type"), message.get("payload", {}), message.get("request_id"))
            if len(data) > 180:
                raise ProtocolError("Mensaje supera el límite conservador de 180 bytes")
            for conn_handle in tuple(self._connections):
                self.ble.gatts_notify(conn_handle, self._tx_handle, data)
            return True
        except (AttributeError, ProtocolError, ValueError) as exc:
            print("[BLE] Mensaje de salida inválido: {}".format(exc))
            return False
        except Exception as exc:
            print("[BLE] Error al notificar: {}".format(exc))
            return False

    def receive(self):
        if not self._messages:
            return None
        return self._messages.pop(0)

    def is_connected(self):
        return self.connected and bool(self._connections)

    def close(self):
        if self.ble is not None:
            try:
                self.ble.active(False)
            except Exception:
                pass
        self._connections = set()
        self.connected = False
        self._rx_buffer = b""
        self._messages = []
        self.ble = None
