# Sensor táctil de Félix

## Estado comprobado

El repositorio ya incluye `src/firmware/touch_sensor.py` y pruebas en
`tests/test_touch_sensor.py`. Para la placa objetivo ESP32-WROOM-32 se reserva
GPIO 32 como entrada capacitiva (TouchPad). Se usa el TouchPad integrado del
ESP32 clásico: no hace falta comprar un módulo táctil adicional si se construye
un electrodo adecuado.

El sensor detecta contacto capacitivo; **no mide fuerza ni presión**.

## Gestos que reconoce

| Gesto | Evento | Uso previsto en Félix |
|---|---|---|
| Toque corto | `pet` | Reacción de cariño: expresión y movimiento suave |
| Dos toques cortos dentro de la ventana configurada | `annoyed` | Expresión de sorpresa o molestia juguetona |
| Mantener pulsado (900 ms por defecto) | `press_to_talk_start` | Solicitar inicio de captura de voz |
| Soltar después de mantener | `press_to_talk_end` | Solicitar fin de captura y envío de audio |

También puede aparecer `touch_start` cuando el contacto se estabiliza. La app
debe consumir los eventos sin bloquear el bucle principal.

## Inicialización en ESP32

Ejemplo para MicroPython, ejecutado en la placa y no en Android:

```python
from src.firmware.touch_sensor import TouchSensor

touch = TouchSensor.from_esp32(
    pin=32,
    samples=24,
    sample_delay_ms=20,
    threshold_ratio=0.80,
    long_press_ms=900,
    debounce_ms=60,
)

while True:
    event = touch.poll()
    if event is not None:
        print(event)
```

**Calibración:** al iniciar, no toques el electrodo durante el muestreo. El
umbral se calcula como una fracción de la lectura base. Si el entorno, el cable
o el electrodo cambian, vuelve a calibrar y valida el umbral con pruebas reales.

## Integración pendiente

El detector ya produce eventos y tiene pruebas unitarias, pero eso no significa
que el circuito completo esté terminado. Falta conectar cada evento con el
controlador de expresiones, los servos y el flujo de audio de Félix. En
particular, `press_to_talk_start/end` son señales de control: todavía hace falta
implementar y probar el recorrido completo de captura, transmisión a la app y
respuesta de voz.

La app Android/desktop deberá recibir estados/eventos del firmware mediante el
transporte Bluetooth real que se implemente. No debe asumir que una lectura
UART equivale a una conexión Bluetooth; el transporte y su emparejamiento deben
validarse por separado.

## Seguridad eléctrica y montaje

- Confirma que la placa sea ESP32-WROOM-32 clásico y que GPIO 32 esté disponible.
- Mantén el electrodo y el cableado táctil alejados de cables de servos y motores.
- Comparte GND cuando corresponda, pero no conectes el electrodo a una fuente de
  alimentación.
- No conectes motores ni servos al pin táctil.
- Prueba primero el sensor sin servos ni audio para separar problemas eléctricos.

## Pruebas

Ejecuta desde la raíz del repositorio:

```bash
python -m unittest tests.test_touch_sensor -v
```

Las pruebas cubren toque corto, doble toque y pulsación larga con liberación.
La validación en hardware real sigue pendiente hasta probar la placa y el
electrodo físicos.
