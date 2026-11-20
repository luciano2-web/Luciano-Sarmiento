# Conexión real ESP32 ↔ app

Esta implementación usa BLE Nordic UART Service (NUS), no HC-05/SPP.
El firmware MicroPython debe incluir `bluetooth`. Copiar `main.py`,
`bluetooth_bridge.py`, `device_session.py`, `display.py`, `touch_sensor.py`
y `src/core/device_protocol.py` a la raíz de la placa, junto al controlador OLED.
Conservar los módulos adicionales que requiera el sensor.

En escritorio instalar `bleak==3.0.1` además de las dependencias de la app.
En Android, el spec incluye Bleak/Pyjnius y permisos BLE. Se solicita permiso
al tocar Conectar placa. Escribir la dirección BLE exacta de la placa,
no la dirección de un HC-05. El botón Desconectar permite reconectar después.
El estado Conectado requiere suscripción a notificaciones y respuesta hello_ack.
No hay reconexión automática ni transmisión de audio. Los botones de caricias
existentes siguen siendo simulación local; los eventos reales llegan del sensor.

La raíz main.py inicia la app modular; source.dir en el spec incluye src/core.
Las opciones Android se colocan bajo [app], como requiere Buildozer.
La compilación APK NO se ha verificado: las dependencias de IA existentes
(torch, bitsandbytes, etc.) todavía pueden requerir recetas o un backend móvil
compatible. No se declara una APK instalable por haber pasado pruebas Python.

## Validación

`python -m unittest discover -s tests -p test_device_link.py -v`

Las pruebas usan una radio falsa para recorrer handshake, evento, respuesta
y pantalla. También verifican fragmentación de 20 bytes, mensajes inválidos,
desbordamientos y rechazo de emociones sin un evento pendiente.

Prueba física pendiente: encender ESP32, conceder permisos Android, conectar,
tocar electrodo y verificar cambio en ambas pantallas; desconectar, volver
a conectar y repetir. Probar también permiso denegado, radio apagada y placa
fuera de alcance. No se ha realizado esta prueba ni medido estabilidad de radio.

Fuentes de compatibilidad:
- https://bleak.readthedocs.io/en/stable/backends/android.html
- https://python-for-android.readthedocs.io/en/latest/apis.html
