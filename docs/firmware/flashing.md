# Instalar el firmware MicroPython de Félix

Esta guía corresponde a `src/firmware/main.py`. La integración se prueba con dobles de software; la validación en ESP32 físico sigue pendiente. No hay un firmware Arduino `.ino` en este repositorio.

## Placa y conexiones

La configuración actual apunta a ESP32 clásico WROOM-32 con MicroPython y BLE, OLED SSD1306 I2C de 128×64 (dirección 0x3C) y electrodo táctil GPIO32. No asumir compatibilidad con cualquier variante ESP32.

Con la placa desconectada, conecta una OLED compatible con 3,3 V: GND a GND, VCC a 3V3, SCL a GPIO21 y SDA a GPIO22. Confirma estos pines con `display.py` y tu placa antes de alimentar el montaje.

## Copiar todos los módulos

1. Instala [MicroPython para ESP32 clásico](https://micropython.org/download/ESP32_GENERIC/) siguiendo las instrucciones de esa placa. Conserva una copia de cualquier programa previo.
2. Cierra otras consolas serie y ejecuta desde la raíz del repositorio:

```sh
python -m pip install mpremote
mpremote connect auto mip install ssd1306
mpremote connect auto fs cp src/firmware/display.py :display.py
mpremote connect auto fs cp src/firmware/touch_sensor.py :touch_sensor.py
mpremote connect auto fs cp src/firmware/bluetooth_bridge.py :bluetooth_bridge.py
mpremote connect auto fs cp src/firmware/device_session.py :device_session.py
mpremote connect auto fs cp src/core/device_protocol.py :device_protocol.py
mpremote connect auto fs cp src/firmware/main.py :main.py
mpremote connect auto reset
```

Este es un despliegue plano: los seis archivos deben quedar juntos en la raíz de la placa, además del controlador SSD1306. El puente usa el protocolo local cuando no existe el paquete `src`.

## Primera comprobación

Deja libre el electrodo durante la calibración. Inspecciona la salida con `mpremote connect auto repl`; Ctrl-D reinicia y Ctrl-C interrumpe el programa.

El código imprime `[Felix] Listo. Toca y suelta el electrodo.` después de inicializar pantalla, BLE y sensor. Un toque muestra una cara feliz; un doble toque, sorpresa. Es el comportamiento esperado por el código, aún pendiente de comprobar en placa.

La comunicación usa BLE Nordic UART Service, no HC-05/SPP. Sigue la [guía BLE](../BLE_CONNECTION.md) para la app. La interfaz solo anuncia conexión después de recibir la confirmación del protocolo. Voz, micrófono, altavoz y servos no se validan mediante esta prueba.

## Diagnóstico

| Problema | Comprobación |
|---|---|
| Import ausente | Verifica que copiaste los seis archivos y que SSD1306 está instalado |
| No aparece OLED | Revisa alimentación, dirección I2C y pines del controlador |
| No arranca BLE | Comprueba soporte BLE del firmware MicroPython y de la placa |
| Gestos incorrectos | Reinicia con el electrodo libre; revisa calibración y montaje |
| La app no conecta | Revisa servicio BLE, dirección y permisos; conserva el error completo |

No hay una señal de LED ni un mensaje de micrófono listo garantizados por este firmware. No se presenta una ejecución en consola o con mocks como una prueba física.

[Volver al README](../../README.md)
