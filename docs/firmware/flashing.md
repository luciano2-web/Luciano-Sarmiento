# 📽️ Guía para Flashear el Firmware en el ESP32

**🐱 Félix v2.0** | **Última actualización: 2024-09-28**

Esta guía te explicará cómo **cargar el firmware** en tu ESP32 para que Félix funcione correctamente.

---

## 🌍 Tabla de Contenidos
1. [Preparación](#-preparación)
2. [Opción 1: Usando Arduino IDE](#1-opción-1-usando-arduino-ide)
3. [Opción 2: Usando PlatformIO](#2-opción-2-usando-platformio)
4. [Opción 3: Usando Thonny (MicroPython)](#3-opción-3-usando-thonny-micropython)
5. [Opción 4: Usando esptool (Línea de Comandos)](#4-opción-4-usando-esptool-línea-de-comandos)
6. [Verificación del Firmware](#-verificación-del-firmware)
7. [Solución de Problemas](#-solución-de-problemas)
8. [Actualizando el Firmware](#-actualizando-el-firmware)

---

## 👨 Preparación

### 📍 Requisitos
- **ESP32-WROOM-32** (o compatible).
- **Cable USB** para conectar el ESP32 a la computadora.
- **Computadora** con:
  - **Sistema Operativo**: Windows 10/11, macOS 10.15+, o Linux (Ubuntu 20.04+).
  - **Python 3.7+** (para algunas opciones).
  - **Acceso a Internet** para descargar herramientas.

### 🐾 Herramientas Necesarias

| Herramienta | Descripción | Enlace | Plataforma |
|-------------|-------------|--------|------------|
| **Arduino IDE** | IDE oficial para Arduino/ESP32 | [arduino.cc](https://www.arduino.cc) | Windows/macOS/Linux |
| **PlatformIO** | IDE avanzado para desarrollo embebido | [platformio.org](https://platformio.org) | Windows/macOS/Linux |
| **Thonny** | IDE para MicroPython | [thonny.org](https://thonny.org) | Windows/macOS/Linux |
| **esptool** | Herramienta de línea de comandos para ESP32 | [GitHub](https://github.com/espressif/esptool) | Windows/macOS/Linux |
| **Python** | Lenguaje de programación | [python.org](https://python.org) | Windows/macOS/Linux |

### 📑 Descarga el Firmware
El firmware de Félix se encuentra en:
- `src/firmware/main.py` (MicroPython)
- `src/firmware/main.ino` (Arduino, si existe)

**⚠️ Asegúrate de estar en la rama correcta de GitHub:**
```bash
git checkout main
git pull origin main
```

---

## ☁️ Opción 1: Usando Arduino IDE

### 1.1 Instalar Arduino IDE
1. Descarga **Arduino IDE** desde [arduino.cc](https://www.arduino.cc).
2. Instálalo siguiendo las instrucciones para tu sistema operativo.

### 1.2 Instalar Soporte para ESP32
1. Abre **Arduino IDE**.
2. Ve a **File > Preferences**.
3. En **Additional Boards Manager URLs**, agrega la siguiente URL:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
   - Si ya hay otras URLs, sepáralas con comas (`,`).

4. Haz clic en **OK**.
5. Ve a **Tools > Board > Boards Manager**.
6. Busca **esp32** e instala la última versión.

### 1.3 Configurar el ESP32
1. Conecta tu **ESP32** a la computadora usando un cable USB.
2. Ve a **Tools > Board** y selecciona **ESP32 Arduino > ESP32 Dev Module**.
3. Ve a **Tools > Port** y selecciona el puerto COM donde está conectado tu ESP32 (ej: `COM3` o `/dev/ttyUSB0`).

### 1.4 Cargar el Firmware
1. Abre el archivo de firmware (`src/firmware/main.ino`).
   - Si no existe, usa el código de MicroPython y conviértelo a Arduino.
2. Haz clic en el botón **Verify** (✔) para compilar el código.
3. Si no hay errores, haz clic en **Upload** (→) para cargar el firmware.
4. Espera a que el proceso termine. Deberías ver:
   ```
   Done uploading.
   ```

### 1.5 Verificar la Carga
- El **LED azul** del ESP32 debe parpadear rápidamente durante la carga.
- Una vez terminada, el ESP32 se reiniciará y el firmware de Félix estará listo.

---

## ☁️ Opción 2: Usando PlatformIO

### 2.1 Instalar PlatformIO
1. Descarga **PlatformIO** desde [platformio.org](https://platformio.org).
   - Puedes instalarlo como **extensión de VS Code** o como **IDE independiente**.
2. Instálalo siguiendo las instrucciones.

### 2.2 Configurar el Proyecto
1. Abre **PlatformIO**.
2. Haz clic en **New Project**.
3. Configura el proyecto:
   - **Name**: `Felix-Firmware`
   - **Board**: `ESP32 Dev Module`
   - **Framework**: `Arduino` o `MicroPython`
   - **Location**: Selecciona la carpeta `src/firmware`

4. Haz clic en **Finish**.

### 2.3 Cargar el Firmware
1. Copia el archivo `main.py` o `main.ino` a la carpeta del proyecto.
2. Conecta tu **ESP32** a la computadora.
3. Haz clic en el botón **Build** (🔧) para compilar.
4. Haz clic en el botón **Upload** (→) para cargar el firmware.

### 2.4 Verificar la Carga
- El **LED azul** del ESP32 debe parpadear durante la carga.
- En la consola de PlatformIO, deberías ver:
  ```
  *** [upload] successfully uploaded firmware ***
  ```

---

## ☁️ Opción 3: Usando Thonny (MicroPython)

### 3.1 Instalar Thonny
1. Descarga **Thonny** desde [thonny.org](https://thonny.org).
2. Instálalo siguiendo las instrucciones para tu sistema operativo.

### 3.2 Configurar Thonny para ESP32
1. Abre **Thonny**.
2. Ve a **Run > Select interpreter**.
3. Selecciona **MicroPython (ESP32)**.
4. Selecciona el **puerto COM** donde está conectado tu ESP32.

### 3.3 Instalar MicroPython en el ESP32
1. Descarga la última versión de **MicroPython para ESP32** desde:
   [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/)
2. En Thonny, ve a **Run > Install MicroPython**.
3. Selecciona el archivo `.bin` descargado y el puerto COM.
4. Haz clic en **Install** y espera a que termine.

### 3.4 Cargar el Firmware
1. Abre el archivo `src/firmware/main.py` en Thonny.
2. Haz clic en el botón **Run** (▶) para cargar y ejecutar el firmware.
3. El firmware se cargará y ejecutará automáticamente.

### 3.5 Verificar la Carga
- El **LED azul** del ESP32 debe parpadear.
- En la consola de Thonny, deberías ver el mensaje:
  ```
  Félix firmware initialized!
  Bluetooth: Ready
  OLED: Ready
  ```

---

## ☁️ Opción 4: Usando esptool (Línea de Comandos)

### 4.1 Instalar esptool
1. Abre una **terminal** (Windows: CMD/PowerShell, macOS/Linux: Terminal).
2. Instala `esptool` usando pip:
   ```bash
   pip install esptool
   ```

### 4.2 Instalar MicroPython
1. Descarga el firmware de **MicroPython para ESP32** desde:
   [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/)
   - Ejemplo: `esp32-YYYYMMDD-vX.X.X.bin`

2. Conecta tu **ESP32** a la computadora y anota el **puerto COM** (ej: `COM3` o `/dev/ttyUSB0`).

3. Ejecuta el siguiente comando para **borrar la memoria flash** (opcional, pero recomendado):
   ```bash
   esptool.py --port COM3 erase_flash
   ```

4. Ejecuta el siguiente comando para **cargar MicroPython**:
   ```bash
   esptool.py --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 esp32-YYYYMMDD-vX.X.X.bin
   ```
   - Reemplaza `COM3` con tu puerto COM.
   - Reemplaza `esp32-YYYYMMDD-vX.X.X.bin` con el nombre del archivo descargado.

### 4.3 Cargar el Firmware de Félix
1. Copia el archivo `src/firmware/main.py` a tu computadora.
2. Usa **ampy** (herramienta para MicroPython) para cargar el archivo:
   ```bash
   pip install adafruit-ampy
   ampy --port COM3 put main.py
   ```

3. Reinicia el ESP32:
   ```bash
   esptool.py --port COM3 reset
   ```

### 4.4 Verificar la Carga
- Usa un **cliente serial** (ej: **PuTTY**, **Screen**, o **Arduino Serial Monitor**) para conectarte al ESP32.
- Configura:
  - **Baud Rate**: 115200
  - **Puerto COM**: El mismo que usaste para cargar el firmware.
- Deberías ver:
  ```
  Félix firmware initialized!
  Bluetooth: Ready
  OLED: Ready
  ```

---

## ✅ Verificación del Firmware

### 1. Verificar con LED
- El **LED azul** del ESP32 debe parpadear **rápidamente** durante la carga y luego **permanecer encendido** o parpadear lentamente.

### 2. Verificar con Monitor Serial
1. Abre el **Monitor Serial** en Arduino IDE o usa un cliente serial.
2. Configura:
   - **Baud Rate**: 115200
   - **Puerto COM**: El puerto de tu ESP32.
3. Deberías ver mensajes como:
   ```
   [INFO] Inicializando Félix...
   [INFO] Bluetooth listo
   [INFO] OLED lista
   [INFO] Micrófono INMP441 listo
   [INFO] Esperando conexión...
   ```

### 3. Verificar con Bluetooth
1. Usa tu **teléfono** para buscar dispositivos Bluetooth.
2. Deberías ver un dispositivo llamado **"Félix"** o **"ESP32"**.
3. Conéctate a él usando la **app móvil de Félix**.

---

## ⚠️ Solución de Problemas

### 💥 El ESP32 no es detectado por la computadora

| Problema | Causa | Solución |
|----------|-------|----------|
| No aparece el puerto COM | Driver faltante | Instala el driver [CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) |
| Puerto COM no funciona | Cable USB defectuoso | Prueba con otro cable |
| ESP32 no se enciende | Sin alimentación | Verifica el Power Bank o el cable USB |

### 💥 Error al cargar el firmware

| Problema | Causa | Solución |
|----------|-------|----------|
| `Failed to connect` | Puerto COM incorrecto | Verifica el puerto COM |
| `No module named esp32` | MicroPython no instalado | Instala MicroPython primero |
| `Out of memory` | Firmware demasiado grande | Usa una versión más ligera del firmware |
| `Invalid head of packet` | Velocidad de baudios incorrecta | Usa 115200 o 460800 |

### 💥 El firmware no funciona correctamente

| Problema | Causa | Solución |
|----------|-------|----------|
| OLED no muestra nada | Conexión I2C incorrecta | Verifica SCL (GPIO 21) y SDA (GPIO 22) |
| Bluetooth no funciona | Firmware no cargado | Recarga el firmware |
| Micrófono no graba | Conexión I2S incorrecta | Verifica WS, SCK, SD |
| Parlante no suena | Conexión PWM incorrecta | Verifica GPIO 26 |

---

## 🐾 Actualizando el Firmware

### Pasos para Actualizar
1. **Descarga la última versión del firmware** desde GitHub:
   ```bash
   git pull origin main
   ```

2. **Carga el nuevo firmware** usando uno de los métodos anteriores.

3. **Reinicia el ESP32** para aplicar los cambios.

### ⚠️ Notas Importantes
- **Haz backup** de tu firmware actual antes de actualizar.
- **Verifica los cambios** en el archivo `CHANGELOG.md` (si existe) para saber qué hay de nuevo.
- Si la actualización falla, **vuelve a cargar el firmware anterior**.

---

## 🐾 Consejos Adicionales

1. **Usa un Power Bank de calidad**: Algunos Power Banks **apagan la salida** después de unos minutos si no detectan suficiente consumo. Si el ESP32 se reinicia solo, prueba con otro Power Bank.
2. **Verifica las conexiones**: Si algo no funciona, **revisa las conexiones** antes de asumir que el firmware está mal.
3. **Usa el Monitor Serial**: El **Monitor Serial** es tu mejor amigo para depurar problemas.
4. **Consulta la documentación**: Si tienes dudas, revisa:
   - [Diagrama de Hardware](../hardware/components.md)
   - [Guía de Ensamblaje](../hardware/assembly.md)
   - [Arquitectura del Sistema](../ARCHITECTURE.md)

---

## 🐱 ¡Félix está listo para usar!

Una vez que el firmware esté cargado correctamente, **Félix está listo para chatear contigo**.

**⚡ Próximo paso:** [Configurar la App Móvil →](../mobile/setup.md)

---

**🐱 Félix te espera... Ronronea... 🐾**

[← Volver a Firmware](firmware) | [💂 Ver Debugging Guide →](debugging.md)
