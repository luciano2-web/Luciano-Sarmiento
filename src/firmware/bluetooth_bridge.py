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


_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
_TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
_FLAG_WRITE = (bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE) if bluetooth else 0
_FLAG_NOTIFY = bluetooth.FLAG_NOTIFY if bluetooth else 0


def _advertising_payload(name):
    name_bytes = name.encode("utf-8")
    return bytes((2, 0x01, 0x06, len(name_bytes) + 1, 0x09)) + name_bytes


class BluetoothBridge:
    """Servidor BLE UART; no simula una conexión cuando no hay central."""

    def __init__(self, device_name=BLUETOOTH_DEVICE_NAME):
        self.device_name = device_name
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
                (_UART_UUID, (
                    (_TX_UUID, _FLAG_NOTIFY),
                    (_RX_UUID, _FLAG_WRITE),
                )),
            ))
            self.ble.gap_advertise(100000, adv_data=_advertising_payload(self.device_name))
            print("[BLE] Anunciando '{}'; esperando conexión BLE real".format(
                self.device_name
            ))
            return True
        except Exception as exc:
            self.connected = False
            print("[BLE] No se pudo iniciar BLE: {}".format(exc))
            return False

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
            print("[BLE] Central desconectado: {}".format(conn_handle))
            if self.ble is not None:
                self.ble.gap_advertise(100000, adv_data=_advertising_payload(self.device_name))
        elif event == 3:  # _IRQ_GATTS_WRITE
            conn_handle, value_handle = data
            if value_handle == self._rx_handle:
                self._rx_buffer += self.ble.gatts_read(self._rx_handle)
                while b"\n" in self._rx_buffer:
                    line, self._rx_buffer = self._rx_buffer.split(b"\n", 1)
                    if line:
                        self._messages.append(line)

    def send(self, message):
        if not self.connected or self.ble is None or self._tx_handle is None:
            return False
        try:
            import json
            data = json.dumps(message).encode("utf-8") + b"\n"
            if len(data) > 180:
                raise ValueError("Mensaje supera el límite conservador de 180 bytes")
            for conn_handle in tuple(self._connections):
                self.ble.gatts_notify(conn_handle, self._tx_handle, data)
            return True
        except Exception as exc:
            print("[BLE] Error al notificar: {}".format(exc))
            return False

    def receive(self):
        if not self._messages:
            return None
        import json
        try:
            return json.loads(self._messages.pop(0).decode("utf-8"))
        except (ValueError, UnicodeError) as exc:
            print("[BLE] Mensaje inválido: {}".format(exc))
            return None

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
        self.ble = None
