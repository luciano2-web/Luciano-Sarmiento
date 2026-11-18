"""Arranque local de Félix: copiar como /main.py a un ESP32 clásico."""
import time

from display import DisplayController
from touch_sensor import TouchSensor


def main():
    display = DisplayController()
    if not display.initialize():
        print("[Felix] Revisa OLED, controlador y conexiones I2C.")
        return
    try:
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
                    expression = "happy" if gesture == "pet" else "surprised"
                    if not display.show_felix_face(expression):
                        return
                    print("[Felix]", gesture, "->", expression)
            time.sleep_ms(20)
    finally:
        display.deinitialize()


if __name__ == "__main__":
    main()
