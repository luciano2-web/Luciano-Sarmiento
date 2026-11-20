"""Arranque local de Félix: copiar como /main.py a un ESP32 clásico."""
import time

from display import DisplayController
from touch_sensor import TouchSensor
from bluetooth_bridge import BluetoothBridge
from device_session import DeviceSession


def main():
    display = DisplayController()
    if not display.initialize():
        print("[Felix] Revisa OLED, controlador y conexiones I2C.")
        return
    bridge = BluetoothBridge()
    try:
        bridge.start_server()
        session = DeviceSession(bridge, display)
        if not display.show_felix_face("neutral"):
            return
        print("[Felix] Calibrando. Mantén el electrodo libre.")
        sensor = TouchSensor.from_esp32()
        print("[Felix] Listo. Toca y suelta el electrodo.")
        while True:
            event = sensor.poll()
            if event:
                gesture = event["type"]
                if gesture in ("pet", "annoyed"):
                    session.touch(gesture)
            session.poll()
            time.sleep_ms(20)
    finally:
        bridge.close()
        display.deinitialize()


if __name__ == "__main__":
    main()
