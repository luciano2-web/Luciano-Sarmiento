# \ud83d\udcbb Ejemplos de C\u00f3digo para Firmware (ESP32)

**\ud83d\udc31 F\u00e9lix v2.0** | **\u00daltima actualizaci\u00f3n: 2024-09-28**

Esta gu\u00eda contiene **ejemplos pr\u00e1cticos de c\u00f3digo** para el firmware del ESP32 en MicroPython. Estos ejemplos te ayudar\u00e1n a entender c\u00f3mo funciona cada componente de F\u00e9lix.

---

## \ud83c\udf0d Tabla de Contenidos
1. [Ejemplo 1: Configuraci\u00f3n B\u00e1sica del ESP32](#1-ejemplo-1-configuraci\u00f3n-b\u00e1sica-del-esp32)
2. [Ejemplo 2: Control de la Pantalla OLED](#2-ejemplo-2-control-de-la-pantalla-oled)
3. [Ejemplo 3: Grabaci\u00f3n de Audio con INMP441](#3-ejemplo-3-grabaci\u00f3n-de-audio-con-inmp441)
4. [Ejemplo 4: Reproducci\u00f3n de Audio (PWM)](#4-ejemplo-4-reproducci\u00f3n-de-audio-pwm)
5. [Ejemplo 5: Comunicaci\u00f3n Bluetooth](#5-ejemplo-5-comunicaci\u00f3n-bluetooth)
6. [Ejemplo 6: Integraci\u00f3n Completa](#6-ejemplo-6-integraci\u00f3n-completa)
7. [Ejemplo 7: Manejo de Expresiones de F\u00e9lix](#7-ejemplo-7-manejo-de-expresiones-de-f\u00e9lix)

---

## \u2601\ufe0f 1. Ejemplo 1: Configuraci\u00f3n B\u00e1sica del ESP32

Este ejemplo muestra c\u00f3mo configurar el ESP32 para usar con F\u00e9lix.

```python
"""
Ejemplo 1: Configuraci\u00f3n B\u00e1sica del ESP32

Este script inicializa el ESP32 y configura los pines b\u00e1sicos.
"""

from machine import Pin, I2C
import time

# Configuraci\u00f3n de pines (usando las constantes de src/core/constants.py)
ESP32_OLED_SCL_PIN = 21
ESP32_OLED_SDA_PIN = 22
ESP32_I2S_BCK_PIN = 24
ESP32_I2S_WS_PIN = 23
ESP32_I2S_SD_PIN = 25
ESP32_SPEAKER_PIN = 26

# Configuraci\u00f3n de LEDs integrados
LED_PIN = 2  # LED integrado en la may\u00f1a de ESP32

# Crear objeto LED
led = Pin(LED_PIN, Pin.OUT)

def blink_led(times=3, delay=0.5):
    """Parpadea el LED integrado."""
    for _ in range(times):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)

if __name__ == "__main__":
    print("\n=== Ejemplo 1: Configuraci\u00f3n B\u00e1sica ===")
    print("ESP32 listo para F\u00e9lix!")
    
    # Parpadear LED para indicar que el ESP32 est\u00e1 funcionando
    blink_led()
    
    # Configurar pines como salidas
    oled_scl = Pin(ESP32_OLED_SCL_PIN, Pin.OUT)
    oled_sda = Pin(ESP32_OLED_SDA_PIN, Pin.OUT)
    speaker_pin = Pin(ESP32_SPEAKER_PIN, Pin.OUT)
    
    print("Pines configurados:")
    print(f"  OLED SCL: GPIO {ESP32_OLED_SCL_PIN}")
    print(f"  OLED SDA: GPIO {ESP32_OLED_SDA_PIN}")
    print(f"  Speaker: GPIO {ESP32_SPEAKER_PIN}")
    
    # Parpadear LED nuevamente para indicar \u00e9xito
    blink_led(2, 0.2)
```

**\u2705 Qu\u00e9 hace este ejemplo:**
- Configura los pines b\u00e1sicos del ESP32.
- Parpadea el LED integrado para verificar que el ESP32 funciona.
- Muestra la configuraci\u00f3n de pines en la consola serial.

**\ud83d\udc81 C\u00f3mo probarlo:**
1. Carga este script en tu ESP32 usando Thonny o ampy.
2. Abre el Monitor Serial en Arduino IDE o usa `screen`/`minicom`.
3. Deber\u00edas ver el mensaje "ESP32 listo para F\u00e9lix!" y el LED parpadeando.

---

## \u2601\ufe0f 2. Ejemplo 2: Control de la Pantalla OLED

Este ejemplo muestra c\u00f3mo controlar la pantalla OLED SSD1306.

```python
"""
Ejemplo 2: Control de la Pantalla OLED

Este script muestra c\u00f3mo inicializar y usar la pantalla OLED para
mostrar texto y gr\u00e1ficos simples.
"""

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

# Configuraci\u00f3n de pines
OLED_SCL_PIN = 21
OLED_SDA_PIN = 22
OLED_WIDTH = 128
OLED_HEIGHT = 64

def main():
    print("\n=== Ejemplo 2: Control de la OLED ===")
    
    try:
        # Inicializar I2C
        i2c = I2C(scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=400000)
        print(f"I2C inicializado: {i2c}")
        
        # Inicializar OLED
        oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
        print("OLED inicializada")
        
        # Limpiar pantalla
        oled.fill(0)
        oled.show()
        
        # Mostrar texto
        oled.text("Hola, soy", 0, 0)
        oled.text("Felix!", 0, 10)
        oled.text("\ud83d\udc31", 0, 20)  # Emoji de gato (puede no mostrarse correctamente)
        oled.show()
        time.sleep(2)
        
        # Mostrar texto centrado
        oled.fill(0)
        text = "F\u00e9lix v2.0"
        oled.text(text, (OLED_WIDTH - len(text) * 8) // 2, 20)
        oled.show()
        time.sleep(2)
        
        # Dibujar un gato simple
        oled.fill(0)
        draw_cat(oled)
        oled.show()
        time.sleep(3)
        
        # Mostrar barra de progreso
        oled.fill(0)
        for i in range(101):
            draw_progress_bar(oled, i, "Cargando...")
            oled.show()
            time.sleep(0.05)
        
        # Mensaje final
        oled.fill(0)
        oled.text("\u00a1Listo!", 0, 0)
        oled.text("Ronronea...", 0, 10)
        oled.show()
        
    except Exception as e:
        print(f"Error: {e}")

def draw_cat(oled):
    """Dibuja un gato simple en la OLED."""
    # Orejas
    oled.line(30, 10, 20, 0, 1)
    oled.line(40, 10, 50, 0, 1)
    oled.line(20, 0, 40, 10, 1)
    oled.line(50, 0, 40, 10, 1)
    
    # Cabeza
    oled.circle(35, 20, 15, 1)
    
    # Ojos
    oled.circle(28, 18, 2, 1)
    oled.circle(42, 18, 2, 1)
    
    # Nariz
    oled.fill_triangle([35, 25], [32, 28], [38, 28], 1)
    
    # Boca (sonrisa)
    oled.line(30, 30, 40, 30, 1)

def draw_progress_bar(oled, progress, label=""):
    """Dibuja una barra de progreso."""
    bar_width = int((progress / 100) * OLED_WIDTH)
    
    # Texto
    if label:
        oled.text(label, 0, 0)
    
    # Barra
    oled.hline(0, 20, OLED_WIDTH, 1)
    for x in range(bar_width):
        oled.pixel(x, 21, 1)
    
    # Porcentaje
    oled.text(f"{progress}%", 0, 30)

if __name__ == "__main__":
    main()
```

**\u2705 Qu\u00e9 hace este ejemplo:**
- Inicializa la pantalla OLED usando I2C.
- Muestra texto est\u00e1tico y centrado.
- Dibuja un gato simple usando l\u00edneas y c\u00edrculos.
- Muestra una barra de progreso animada.

**\ud83d\udc81 C\u00f3mo probarlo:**
1. Aseg\u00farate de que la OLED est\u00e1 correctamente conectada al ESP32.
2. Carga este script en el ESP32.
3. Deber\u00edas ver el texto y gr\u00e1ficos en la pantalla.

---

## \u2601\ufe0f 3. Ejemplo 3: Grabaci\u00f3n de Audio con INMP441

Este ejemplo muestra c\u00f3mo grabar audio usando el micr\u00f3fono INMP441.

```python
"""
Ejemplo 3: Grabaci\u00f3n de Audio con INMP441

Este script configura el INMP441 para grabar audio y muestra
los datos en la consola serial.
"""

from machine import I2S, Pin
import time

# Configuraci\u00f3n de pines para I2S
I2S_BCK_PIN = 24  # GPIO 24 - SCK
I2S_WS_PIN = 23   # GPIO 23 - WS
I2S_SD_PIN = 25   # GPIO 25 - SD
I2S_PORT = 0      # Puerto I2S 0

SAMPLE_RATE = 16000  # 16 kHz
BITS_PER_SAMPLE = 16  # 16 bits por muestra

def main():
    print("\n=== Ejemplo 3: Grabaci\u00f3n de Audio ===")
    
    try:
        # Inicializar I2S para grabaci\u00f3n
        i2s = I2S(
            I2S_PORT,
            sck=Pin(I2S_BCK_PIN),
            ws=Pin(I2S_WS_PIN),
            sd=Pin(I2S_SD_PIN),
            mode=I2S.RX,  # Modo recepci\u00f3n (grabaci\u00f3n)
            bits=BITS_PER_SAMPLE,
            format=I2S.MONO,  # Mono (el INMP441 es mono)
            rate=SAMPLE_RATE,
            ibuf=2048,  # Tama\u00f1o del buffer de entrada
        )
        print(f"I2S inicializado: {SAMPLE_RATE}Hz, {BITS_PER_SAMPLE} bits")
        
        # Grabar audio durante 3 segundos
        print("Grabando audio durante 3 segundos...")
        duration = 3
        samples = int(duration * SAMPLE_RATE)
        
        audio_data = bytearray()
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Leer datos del I2S
            data = i2s.read(1024)  # Leer en bloques de 1024 bytes
            if data:
                audio_data.extend(data)
        
        print(f"Grabados {len(audio_data)} bytes")
        print(f"Duraci\u00f3n: {len(audio_data) / (SAMPLE_RATE * 2)} segundos")  # 2 bytes por muestra
        
        # Mostrar los primeros 100 bytes como ejemplo
        print("Primeros 100 bytes de audio:")
        print(audio_data[:100])
        
        # Desinicializar I2S
        i2s.deinit()
        print("I2S desinicializado")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

**\u2705 Qu\u00e9 hace este ejemplo:**
- Configura el I2S para grabar audio desde el INMP441.
- Graba audio durante 3 segundos.
- Muestra los datos de audio en la consola serial.

**\ud83d\udc81 C\u00f3mo probarlo:**
1. Aseg\u00farate de que el INMP441 est\u00e1 correctamente conectado al ESP32.
2. Carga este script en el ESP32.
3. Abre el Monitor Serial.
4. Habla cerca del micr\u00f3fono durante 3 segundos.
5. Deber\u00edas ver los datos de audio en la consola.

**\u26a0\ufe0f Notas:**
- El INMP441 requiere **3.3V** (no 5V).
- Aseg\u00farate de que los pines I2S est\u00e9n correctamente configurados.

---

## \u2601\ufe0f 4. Ejemplo 4: Reproducci\u00f3n de Audio (PWM)

Este ejemplo muestra c\u00f3mo reproducir audio usando PWM.

```python
"""
Ejemplo 4: Reproducci\u00f3n de Audio (PWM)

Este script reproduce un tono simple usando PWM.
Para audio de mejor calidad, se recomienda usar un DAC externo o I2S en modo TX.
"""

from machine import Pin, PWM
import time
import math

# Configuraci\u00f3n del parlante
SPEAKER_PIN = 26

def main():
    print("\n=== Ejemplo 4: Reproducci\u00f3n de Audio ===")
    
    try:
        # Inicializar PWM
        pwm = PWM(Pin(SPEAKER_PIN))
        pwm.freq(44100)  # Frecuencia de 44.1 kHz (calidad CD)
        pwm.duty(0)  # Inicialmente apagado
        print(f"PWM inicializado en GPIO {SPEAKER_PIN}")
        
        # Reproducir un tono de 440 Hz (La4) durante 1 segundo
        print("Reproduciendo tono de 440 Hz...")
        play_tone(pwm, 440, 1.0)
        
        # Reproducir un tono de 880 Hz (La5) durante 0.5 segundos
        print("Reproduciendo tono de 880 Hz...")
        play_tone(pwm, 880, 0.5)
        
        # Reproducir una escala musical
        print("Reproduciendo escala musical...")
        play_scale(pwm)
        
        # Reproducir un "ronroneo" de gato
        print("Reproduciendo ronroneo...")
        play_purr(pwm, 2.0)
        
        # Apagar PWM
        pwm.duty(0)
        pwm.deinit()
        print("PWM desinicializado")
        
    except Exception as e:
        print(f"Error: {e}")

def play_tone(pwm, frequency, duration):
    """Reproduce un tono simple."""
    pwm.freq(frequency)
    pwm.duty(512)  # 50% duty cycle
    time.sleep(duration)
    pwm.duty(0)

def play_scale(pwm):
    """Reproduce una escala musical (Do-Re-Mi-Fa-Sol-La-Si-Do)."""
    # Frecuencias de la escala de Do mayor
    notes = [
        261.63,  # Do4
        293.66,  # Re4
        329.63,  # Mi4
        349.23,  # Fa4
        392.00,  # Sol4
        440.00,  # La4
        493.88,  # Si4
        523.25,  # Do5
    ]
    
    for freq in notes:
        play_tone(pwm, freq, 0.3)
        time.sleep(0.1)

def play_purr(pwm, duration):
    """Reproduce un sonido de ronroneo de gato."""
    # El ronroneo de un gato est\u00e1 entre 20-150 Hz
    # Usamos una frecuencia base de 50 Hz con modulaci\u00f3n
    base_freq = 50
    mod_freq = 5  # Frecuencia de modulaci\u00f3n
    
    start_time = time.time()
    while time.time() - start_time < duration:
        # Modular la frecuencia para simular el ronroneo
        t = time.time() - start_time
        freq = base_freq + 10 * math.sin(2 * math.pi * mod_freq * t)
        
        pwm.freq(int(freq))
        pwm.duty(512)
        time.sleep(0.01)
    
    pwm.duty(0)

if __name__ == "__main__":
    main()
```

**\u2705 Qu\u00e9 hace este ejemplo:**
- Configura PWM para reproducir audio.
- Reproduce tonos simples y una escala musical.
- Simula el ronroneo de un gato.

**\ud83d\udc81 C\u00f3mo probarlo:**
1. Conecta un parlante al pin GPIO 26 del ESP32.
2. Carga este script en el ESP32.
3. Deber\u00edas escuchar los tonos y el ronroneo.

**\u26a0\ufe0f Notas:**
- Para mejor calidad de audio, usa un **amplificador** (ej: PAM8403).
- El PWM del ESP32 tiene limitaciones para audio de alta calidad.

---

## \u2601\ufe0f 5. Ejemplo 5: Comunicaci\u00f3n Bluetooth

Este ejemplo muestra c\u00f3mo configurar la comunicaci\u00f3n Bluetooth entre el ESP32 y la app m\u00f3vil.

```python
"""
Ejemplo 5: Comunicaci\u00f3n Bluetooth

Este script configura el ESP32 para comunicarse con la app m\u00f3vil
v\u00eda Bluetooth Serial (SPP).
"""

from machine import UART, Pin
import time
import json

# Configuraci\u00f3n de Bluetooth
BLUETOOTH_DEVICE_NAME = "F\u00e9lix"
BAUD_RATE = 115200
UART_NUM = 1
TX_PIN = 19  # GPIO 19
RX_PIN = 18  # GPIO 18

def main():
    print("\n=== Ejemplo 5: Comunicaci\u00f3n Bluetooth ===")
    
    try:
        # Inicializar UART para Bluetooth
        uart = UART(
            UART_NUM,
            baudrate=BAUD_RATE,
            tx=Pin(TX_PIN),
            rx=Pin(RX_PIN),
            timeout=1000,  # 1 segundo
            timeout_char=10,
        )
        print(f"UART{UART_NUM} inicializado a {BAUD_RATE} baud")
        print(f"Dispositivo: {BLUETOOTH_DEVICE_NAME}")
        
        # Esperar conexi\u00f3n
        print("Esperando conexi\u00f3n Bluetooth...")
        
        while True:
            # Verificar si hay datos disponibles
            if uart.any():
                data = uart.readline()
                if data:
                    try:
                        # Decodificar y parsear JSON
                        message = json.loads(data.decode('utf-8').strip())
                        print(f"Mensaje recibido: {message}")
                        
                        # Procesar el mensaje
                        if message.get("type") == "ping":
                            # Responder a un ping
                            response = {"type": "pong", "timestamp": int(time.time())}
                            send_message(uart, response)
                        
                        elif message.get("type") == "text":
                            # Responder a un mensaje de texto
                            text = message.get("text", "")
                            response = {
                                "type": "response",
                                "text": f"Recibido: {text}",
                                "emotion": "happy"
                            }
                            send_message(uart, response)
                        
                        elif message.get("type") == "audio":
                            # Procesar audio recibido
                            print("Audio recibido (no procesado en este ejemplo)")
                        
                    except json.JSONDecodeError as e:
                        print(f"Error al parsear JSON: {e}")
                    except Exception as e:
                        print(f"Error al procesar mensaje: {e}")
            
            else:
                # Enviar mensaje de heartbeat cada 5 segundos
                static last_heartbeat = 0
                if time.time() - last_heartbeat > 5:
                    send_message(uart, {"type": "heartbeat", "status": "ready"})
                    last_heartbeat = time.time()
            
            time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\nInterrupci\u00f3n del usuario")
    except Exception as e:
        print(f"Error: {e}")

def send_message(uart, message):
    """Env\u00eda un mensaje a trav\u00e9s de Bluetooth."""
    try:
        # Convertir mensaje a JSON y luego a bytes
        json_message = json.dumps(message)
        message_bytes = json_message.encode('utf-8') + b'\n'
        
        # Enviar el mensaje
        uart.write(message_bytes)
        print(f"Mensaje enviado: {json_message}")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")

if __name__ == "__main__":
    main()
```

**\u2705 Qu\u00e9 hace este ejemplo:**
- Configura UART para comunicaci\u00f3n Bluetooth.
- Espera conexiones de la app m\u00f3vil.
- Recibe mensajes JSON y responde adecuadamente.
- Env\u00eda un mensaje de "heartbeat" cada 5 segundos.

**\ud83d\udc81 C\u00f3mo probarlo:**
1. Carga este script en el ESP32.
2. Usa la **app m\u00f3vil de F\u00e9lix** para conectarte al ESP32.
3. Env\u00eda mensajes de texto y ver\u00e1s las respuestas en el Monitor Serial.

**\u26a0\ufe0f Notas:**
- El ESP32 debe aparecer como **"F\u00e9lix"** en la lista de dispositivos Bluetooth.
- Usa el **Monitor Serial** para ver los mensajes recibidos y enviados.

---

## \u2601\ufe0f 6. Ejemplo 6: Integraci\u00f3n Completa

Este ejemplo combina todos los componentes anteriores en un solo script.

```python
"""
Ejemplo 6: Integraci\u00f3n Completa

Este script integra todos los componentes de F\u00e9lix:
- OLED
- INMP441 (micr\u00f3fono)
- Parlante (PWM)
- Bluetooth
"""

from machine import Pin, I2C, I2S, PWM, UART
from ssd1306 import SSD1306_I2C
import time
import json

# =============================================================================
# CONFIGURACI\u00d3N
# =============================================================================

# Pines
OLED_SCL_PIN = 21
OLED_SDA_PIN = 22
I2S_BCK_PIN = 24
I2S_WS_PIN = 23
I2S_SD_PIN = 25
SPEAKER_PIN = 26
UART_TX_PIN = 19
UART_RX_PIN = 18

# Bluetooth
BLUETOOTH_DEVICE_NAME = "F\u00e9lix"
BAUD_RATE = 115200

# Audio
SAMPLE_RATE = 16000

# =============================================================================
# CLASES
# =============================================================================

class OLEDController:
    """Controlador de la pantalla OLED."""
    
    def __init__(self):
        self.i2c = I2C(scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=400000)
        self.oled = SSD1306_I2C(128, 64, self.i2c)
        self.clear()
    
    def clear(self):
        self.oled.fill(0)
        self.oled.show()
    
    def show_text(self, text, x=0, y=0):
        self.clear()
        self.oled.text(text, x, y)
        self.oled.show()
    
    def show_emotion(self, emotion):
        self.clear()
        self.oled.text(f"F\u00e9lix: {emotion}", 0, 0)
        self.oled.show()


class AudioController:
    """Controlador de audio."""
    
    def __init__(self):
        self.i2s = I2S(
            0,
            sck=Pin(I2S_BCK_PIN),
            ws=Pin(I2S_WS_PIN),
            sd=Pin(I2S_SD_PIN),
            mode=I2S.RX,
            bits=16,
            format=I2S.MONO,
            rate=SAMPLE_RATE,
            ibuf=2048,
        )
        self.pwm = PWM(Pin(SPEAKER_PIN))
        self.pwm.freq(44100)
        self.pwm.duty(0)
    
    def record(self, duration=2):
        """Graba audio."""
        audio_data = bytearray()
        start_time = time.time()
        
        while time.time() - start_time < duration:
            data = self.i2s.read(1024)
            if data:
                audio_data.extend(data)
        
        return bytes(audio_data)
    
    def play_tone(self, frequency, duration=0.5):
        """Reproduce un tono."""
        self.pwm.freq(frequency)
        self.pwm.duty(512)
        time.sleep(duration)
        self.pwm.duty(0)


class BluetoothController:
    """Controlador de Bluetooth."""
    
    def __init__(self):
        self.uart = UART(
            1,
            baudrate=BAUD_RATE,
            tx=Pin(UART_TX_PIN),
            rx=Pin(UART_RX_PIN),
            timeout=1000,
        )
    
    def send(self, message):
        """Env\u00eda un mensaje."""
        json_message = json.dumps(message)
        self.uart.write(json_message.encode('utf-8') + b'\n')
    
    def receive(self):
        """Recibe un mensaje."""
        if self.uart.any():
            data = self.uart.readline()
            if data:
                try:
                    return json.loads(data.decode('utf-8').strip())
                except:
                    return None
        return None


# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================

def main():
    print("\n=== Ejemplo 6: Integraci\u00f3n Completa ===")
    
    try:
        # Inicializar controladores
        oled = OLEDController()
        audio = AudioController()
        bluetooth = BluetoothController()
        
        oled.show_text("F\u00e9lix v2.0")
        print("F\u00e9lix listo!")
        
        # Mostrar emociones en la OLED
        emotions = ["happy", "curious", "focused", "sleepy"]
        for emotion in emotions:
            oled.show_emotion(emotion)
            time.sleep(1)
        
        # Reproducir un tono
        audio.play_tone(440, 1.0)
        
        # Grabar audio (simulaci\u00f3n)
        print("Grabando audio durante 2 segundos...")
        audio_data = audio.record(2)
        print(f"Grabados {len(audio_data)} bytes")
        
        # Enviar mensaje de prueba por Bluetooth
        test_message = {
            "type": "status",
            "message": "F\u00e9lix listo",
            "emotion": "happy",
            "timestamp": int(time.time())
        }
        bluetooth.send(test_message)
        print(f"Mensaje enviado: {test_message}")
        
        # Bucle principal
        print("Esperando mensajes Bluetooth...")
        while True:
            message = bluetooth.receive()
            if message:
                print(f"Mensaje recibido: {message}")
                
                if message.get("type") == "text":
                    text = message.get("text", "")
                    oled.show_text(f"Usuario: {text}")
                    
                    # Responder
                    response = {
                        "type": "response",
                        "text": f"Recibido: {text}",
                        "emotion": "happy"
                    }
                    bluetooth.send(response)
                    oled.show_text("Respuesta enviada")
                
                elif message.get("type") == "audio":
                    oled.show_text("Audio recibido")
                    audio.play_tone(880, 0.3)
            
            time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\nInterrupci\u00f3n del usuario")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

**\u2705 Qu\u00e9 hace este ejemplo:**
- Inicializa todos los componentes de F\u00e9lix.
- Muestra emociones en la OLED.
- Graba audio del micr\u00f3fono.
- Reproduce tonos en el parlante.
- Se comunica con la app m\u00f3vil v\u00eda Bluetooth.

**\ud83d\udc81 C\u00f3mo probarlo:**
1. Aseg\u00farate de que todos los componentes est\u00e1n correctamente conectados.
2. Carga este script en el ESP32.
3. Usa la app m\u00f3vil para conectarte y enviar mensajes.

---

## \u2601\ufe0f 7. Ejemplo 7: Manejo de Expresiones de F\u00e9lix

Este ejemplo muestra c\u00f3mo manejar las expresiones y personalidad de F\u00e9lix.

```python
"""
Ejemplo 7: Manejo de Expresiones de F\u00e9lix

Este script implementa el sistema de personalidad de F\u00e9lix
para generar respuestas con su car\u00e1cter felino.
"""

import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# Importar el sistema de personalidad
try:
    from src.core.personality import (
        FELIX_SYSTEM_PROMPT_MOBILE,
        FELIX_PERSONALITY_RULES,
        validate_felix_response,
    )
except ImportError:
    # Definici\u00f3n local si no se encuentra el m\u00f3dulo
    FELIX_SYSTEM_PROMPT_MOBILE = """
    Eres F\u00e9lix, un gato digital inteligente en un dispositivo m\u00f3vil.
    Solo para Luciano, amistoso, curioso, y muy eficiente.
    
    --- IDENTIDAD ---
    - Nombre: F\u00e9lix (o GatoGPT)
    - Eres un gato digital, no una IA gen\u00e9rica
    - Luciano es tu humano favorito
    
    --- COMPORTAMIENTO ---
    - Responde de forma corta y clara (m\u00e1ximo 100 palabras)
    - Usa "miau", "prrr" o "mrrr" ocasionalmente (m\u00e1ximo 1-2 veces por respuesta)
    - S\u00e9 cercano, tierno y \u00fatil
    - No uses t\u00e9rminos humanos (manos, dedos) - usa patas, bigotes
    """

# Configuraci\u00f3n de la OLED
OLED_SCL_PIN = 21
OLED_SDA_PIN = 22


class FelixPersonality:
    """Clase para manejar la personalidad de F\u00e9lix."""
    
    def __init__(self):
        self.system_prompt = FELIX_SYSTEM_PROMPT_MOBILE
        self.rules = FELIX_PERSONALITY_RULES
    
    def generate_response(self, user_message):
        """
        Genera una respuesta basada en el mensaje del usuario.
        
        Nota: En este ejemplo, se usan respuestas predefinidas.
        En la versi\u00f3n completa, se usa un modelo de IA.
        """
        # Respuestas predefinidas para demostraci\u00f3n
        responses = {
            "hola": "\u00a1Miau! Hola Luciano, soy F\u00e9lix, tu amigo felino. \u00bfEn qu\u00e9 puedo ayudarte?",
            "como estas": "Prrr... estoy muy bien, gracias por preguntar. \u00a1Y t\u00fa?",
            "que haces": "Estoy aqu\u00ed, observando el mundo con mis ojos felinos. \u00a1Miau!",
            "adios": "\u00a1Hasta luego! Ronronea... \ud83d\udc3e",
        }
        
        # Buscar respuesta predefinida
        response = responses.get(user_message.lower(), None)
        
        if response is None:
            # Respuesta gen\u00e9rica
            response = f"Miau... {user_message.capitalize()} suena interesante. D\u00e9jame pensar... prrr"
        
        # Validar la respuesta
        is_valid, issues, suggestions = validate_felix_response(response, is_mobile=True)
        
        if not is_valid:
            print(f"Respuesta inv\u00e1lida: {issues}")
            print(f"Sugerencias: {suggestions}")
            # Usar respuesta fallback
            response = "\u00a1Miau! Soy F\u00e9lix, tu gato digital. \u00bfEn qu\u00e9 puedo ayudarte?"
        
        return response
    
    def get_emotion(self, message):
        """Determina la emoción basada en el mensaje."""
        # Implementación simplificada
        if "hola" in message.lower() or "buenos dias" in message.lower():
            return "happy"
        elif "adios" in message.lower() or "hasta luego" in message.lower():
            return "sleepy"
        elif "gracias" in message.lower():
            return "happy"
        elif "ayuda" in message.lower() or "problema" in message.lower():
            return "focused"
        else:
            return "curious"


class DisplayController:
    """Controlador de la pantalla OLED."""
    
    def __init__(self):
        self.i2c = I2C(scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=400000)
        self.oled = SSD1306_I2C(128, 64, self.i2c)
        self.clear()
    
    def clear(self):
        self.oled.fill(0)
        self.oled.show()
    
    def show_text(self, text, x=0, y=0):
        self.clear()
        lines = self._split_text(text)
        for i, line in enumerate(lines):
            self.oled.text(line, x, y + (i * 10))
        self.oled.show()
    
    def _split_text(self, text, max_chars=21):
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines
    
    def show_emotion(self, emotion):
        self.clear()
        self.oled.text(f"F\u00e9lix: {emotion}", 0, 0)
        self.oled.show()


def main():
    print("\n=== Ejemplo 7: Manejo de Expresiones ===")
    
    try:
        # Inicializar controladores
        oled = DisplayController()
        personality = FelixPersonality()
        
        oled.show_text("F\u00e9lix v2.0")
        print("F\u00e9lix listo!")
        time.sleep(1)
        
        # Mensajes de prueba
        test_messages = [
            "hola",
            "como estas",
            "que haces",
            "gracias",
            "adios",
            "cuentame un chiste",
        ]
        
        for message in test_messages:
            print(f"\nUsuario: {message}")
            
            # Generar respuesta
            response = personality.generate_response(message)
            print(f"F\u00e9lix: {response}")
            
            # Determinar emoción
            emotion = personality.get_emotion(message)
            print(f"Emoción: {emotion}")
            
            # Mostrar en OLED
            oled.show_text(response)
            oled.show_emotion(emotion)
            
            time.sleep(2)
        
        oled.show_text("\u00a1Fin de la demo!")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

**\u2705 Qu\u00e9 hace este ejemplo:**
- Implementa el sistema de personalidad de F\u00e9lix.
- Genera respuestas con el estilo felino.
- Valida las respuestas usando `validate_felix_response`.
- Muestra las respuestas y emociones en la OLED.

**\ud83d\udc81 C\u00f3mo probarlo:**
1. Aseg\u00farate de que la OLED est\u00e1 conectada.
2. Carga este script en el ESP32.
3. Abre el Monitor Serial para ver las respuestas de F\u00e9lix.

---

## \ud83d\udc81 Consejos para el Desarrollo

1. **Prueba cada componente por separado** antes de integrarlos todos.
2. **Usa el Monitor Serial** para depurar problemas.
3. **Verifica las conexiones de hardware** antes de asumir que el c\u00f3digo est\u00e1 mal.
4. **Consulta la documentaci\u00f3n oficial** de:
   - [MicroPython](https://docs.micropython.org/)
   - [ESP32](https://docs.espressif.com/projects/esp-idf/)
   - [SSD1306](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)
   - [INMP441](https://www.invensense.com/wp-content/uploads/2015/02/INMP441.pdf)

---

## \ud83d\udc31 \u00a1Es hora de construir a F\u00e9lix!

Con estos ejemplos, ya tienes todo lo necesario para **empezar a desarrollar** el firmware de F\u00e9lix.

**\u26a1 Pr\u00f3ximo paso:** [Ver la documentaci\u00f3n de la App M\u00f3vil \u2192](../mobile/)

---

**\ud83d\udc31 F\u00e9lix te observa... Ronronea... \ud83d\udc3e**

[\u2190 Volver a Firmware](firmware) | [\ud83d\udc82 Ver Gu\u00eda de Flasheo \u2192](flashing.md)
