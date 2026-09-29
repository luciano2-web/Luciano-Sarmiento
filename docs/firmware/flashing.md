# \ud83d\udcfd Gu\u00eda para Flashear el Firmware en el ESP32

**\ud83d\udc31 F\u00e9lix v2.0** | **\u00daltima actualizaci\u00f3n: 2024-09-28**

Esta gu\u00eda te explicar\u00e1 c\u00f3mo **cargar el firmware** en tu ESP32 para que F\u00e9lix funcione correctamente.

---

## \ud83c\udf0d Tabla de Contenidos
1. [Preparaci\u00f3n](#-preparaci\u00f3n)
2. [OPCI\u00d3N 1: Usando Arduino IDE](#1-opci\u00f3n-1-usando-arduino-ide)
3. [OPCI\u00d3N 2: Usando PlatformIO](#2-opci\u00f3n-2-usando-platformio)
4. [OPCI\u00d3N 3: Usando Thonny (MicroPython)](#3-opci\u00f3n-3-usando-thonny-micropython)
5. [OPCI\u00d3N 4: Usando esptool (L\u00ednea de Comandos)](#4-opci\u00f3n-4-usando-esptool-l\u00ednea-de-comandos)
6. [Verificaci\u00f3n del Firmware](#-verificaci\u00f3n-del-firmware)
7. [Soluci\u00f3n de Problemas](#-soluci\u00f3n-de-problemas)
8. [Actualizando el Firmware](#-actualizando-el-firmware)

---

## \ud83d\udc68 Preparaci\u00f3n

### \ud83d\udccd Requisitos
- **ESP32-WROOM-32** (o compatible).
- **Cable USB** (para conectar el ESP32 a la computadora).
- **Computadora** con:
  - **Sistema Operativo**: Windows 10/11, macOS 10.15+, o Linux (Ubuntu 20.04+).
  - **Python 3.7+** (para algunas opciones).
  - **Acceso a Internet** (para descargar herramientas).

### \ud83d\udc7c Herramientas Necesarias
| Herramienta | Descripci\u00f3n | Enlace | Plataforma |
|-------------|-------------|--------|------------|
| **Arduino IDE** | IDE oficial para Arduino/ESP32 | [arduino.cc](https://www.arduino.cc) | Windows/macOS/Linux |
| **PlatformIO** | IDE avanzado para desarrollo embebido | [platformio.org](https://platformio.org) | Windows/macOS/Linux |
| **Thonny** | IDE para MicroPython | [thonny.org](https://thonny.org) | Windows/macOS/Linux |
| **esptool** | Herramienta de l\u00ednea de comandos para ESP32 | [GitHub](https://github.com/espressif/esptool) | Windows/macOS/Linux |
| **Python** | Lenguaje de programaci\u00f3n | [python.org](https://python.org) | Windows/macOS/Linux |

### \ud83d\udcd1 Descarga el Firmware
El firmware de F\u00e9lix se encuentra en:
- `src/firmware/main.py` (MicroPython)
- `src/firmware/main.ino` (Arduino, si existe)

**\u26a0\ufe0f Aseg\u00farate de estar en la rama correcta de GitHub:**
```bash
git checkout main
git pull origin main
```

---

## \u2601\ufe0f OPCI\u00d3N 1: Usando Arduino IDE

### 1.1 Instalar Arduino IDE
1. Descarga **Arduino IDE** desde [arduino.cc](https://www.arduino.cc).
2. Inst\u00e1lalo siguiendo las instrucciones para tu sistema operativo.

### 1.2 Instalar Soporte para ESP32
1. Abre **Arduino IDE**.
2. Ve a **File > Preferences**.
3. En **Additional Boards Manager URLs**, agrega la siguiente URL:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
   - Si ya hay otras URLs, sep\u00e1ralas con comas (`,`).

4. Haz clic en **OK**.
5. Ve a **Tools > Board > Boards Manager**.
6. Busca **esp32** y instala la \u00faltima versi\u00f3n.

### 1.3 Configurar el ESP32
1. Conecta tu **ESP32** a la computadora usando un cable USB.
2. Ve a **Tools > Board** y selecciona **ESP32 Arduino > ESP32 Dev Module**.
3. Ve a **Tools > Port** y selecciona el puerto COM donde est\u00e1 conectado tu ESP32 (ej: `COM3` o `/dev/ttyUSB0`).

### 1.4 Cargar el Firmware
1. Abre el archivo de firmware (`src/firmware/main.ino`).
   - Si no existe, usa el c\u00f3digo de MicroPython y convi\u00e9rtelo a Arduino.
2. Haz clic en el bot\u00f3n **Verify** (\u2714) para compilar el c\u00f3digo.
3. Si no hay errores, haz clic en **Upload** (\u2190) para cargar el firmware.
4. Espera a que el proceso termine. Deber\u00edas ver:
   ```
   Done uploading.
   ```

### 1.5 Verificar la Carga
- El **LED azul** del ESP32 debe parpadear r\u00e1pidamente durante la carga.
- Una vez terminada, el ESP32 se reiniciar\u00e1 y el firmware de F\u00e9lix estar\u00e1 listo.

---

## \u2601\ufe0f OPCI\u00d3N 2: Usando PlatformIO

### 2.1 Instalar PlatformIO
1. Descarga **PlatformIO** desde [platformio.org](https://platformio.org).
   - Puedes instalarlo como **extensi\u00f3n de VS Code** o como **IDE independiente**.
2. Inst\u00e1lalo siguiendo las instrucciones.

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
3. Haz clic en el bot\u00f3n **Build** (\ud83d\udc7c) para compilar.
4. Haz clic en el bot\u00f3n **Upload** (\u2190) para cargar el firmware.

### 2.4 Verificar la Carga
- El **LED azul** del ESP32 debe parpadear durante la carga.
- En la consola de PlatformIO, deber\u00edas ver:
  ```
  *** [upload] successfully uploaded firmware ***
  ```

---

## \u2601\ufe0f OPCI\u00d3N 3: Usando Thonny (MicroPython)

### 3.1 Instalar Thonny
1. Descarga **Thonny** desde [thonny.org](https://thonny.org).
2. Inst\u00e1lalo siguiendo las instrucciones para tu sistema operativo.

### 3.2 Configurar Thonny para ESP32
1. Abre **Thonny**.
2. Ve a **Run > Select interpreter**.
3. Selecciona **MicroPython (ESP32)**.
4. Selecciona el **puerto COM** donde est\u00e1 conectado tu ESP32.

### 3.3 Instalar MicroPython en el ESP32
1. Descarga la \u00faltima versi\u00f3n de **MicroPython para ESP32** desde:
   [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/)
2. En Thonny, ve a **Run > Install MicroPython**.
3. Selecciona el archivo `.bin` descargado y el puerto COM.
4. Haz clic en **Install** y espera a que termine.

### 3.4 Cargar el Firmware
1. Abre el archivo `src/firmware/main.py` en Thonny.
2. Haz clic en el bot\u00f3n **Run** (\u25b6) para cargar y ejecutar el firmware.
3. El firmware se cargar\u00e1 y ejecutar\u00e1 autom\u00e1ticamente.

### 3.5 Verificar la Carga
- El **LED azul** del ESP32 debe parpadear.
- En la consola de Thonny, deber\u00edas ver el mensaje:
  ```
  F\u00e9lix firmware initialized!
  Bluetooth: Ready
  OLED: Ready
  ```

---

## \u2601\ufe0f OPCI\u00d3N 4: Usando esptool (L\u00ednea de Comandos)

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

### 4.3 Cargar el Firmware de F\u00e9lix
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
- Deber\u00edas ver:
  ```
  F\u00e9lix firmware initialized!
  Bluetooth: Ready
  OLED: Ready
  ```

---

## \u2705 Verificaci\u00f3n del Firmware

### 1. Verificar con LED
- El **LED azul** del ESP32 debe parpadear **r\u00e1pidamente** durante la carga y luego **permanecer encendido** o parpadear lentamente.

### 2. Verificar con Monitor Serial
1. Abre el **Monitor Serial** en Arduino IDE o usa un cliente serial.
2. Configura:
   - **Baud Rate**: 115200
   - **Puerto COM**: El puerto de tu ESP32.
3. Deber\u00edas ver mensajes como:
   ```
   [INFO] Inicializando F\u00e9lix...
   [INFO] Bluetooth listo
   [INFO] OLED lista
   [INFO] Micr\u00f3fono INMP441 listo
   [INFO] Esperando conexi\u00f3n...
   ```

### 3. Verificar con Bluetooth
1. Usa tu **tel\u00e9fono** para buscar dispositivos Bluetooth.
2. Deber\u00edas ver un dispositivo llamado **"F\u00e9lix"** o **"ESP32"**.
3. Con\u00e9ctate a \u00e9l usando la **app m\u00f3vil de F\u00e9lix**.

---

## \u26a0\ufe0f Soluci\u00f3n de Problemas

### \ud83d\udca5 El ESP32 no es detectado por la computadora
| Problema | Causa | Soluci\u00f3n |
|----------|-------|----------|
| No aparece el puerto COM | Driver faltante | Instala el driver [CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) |
| Puerto COM no funciona | Cable USB defectuoso | Prueba con otro cable |
| ESP32 no se enciende | Sin alimentaci\u00f3n | Verifica el Power Bank o el cable USB |

### \ud83d\udca5 Error al cargar el firmware
| Problema | Causa | Soluci\u00f3n |
|----------|-------|----------|
| `Failed to connect` | Puerto COM incorrecto | Verifica el puerto COM |
| `No module named esp32` | MicroPython no instalado | Instala MicroPython primero |
| `Out of memory` | Firmware demasiado grande | Usa una versi\u00f3n m\u00e1s ligera del firmware |
| `Invalid head of packet` | Velocidad de baudios incorrecta | Usa 115200 o 460800 |

### \ud83d\udca5 El firmware no funciona correctamente
| Problema | Causa | Soluci\u00f3n |
|----------|-------|----------|
| OLED no muestra nada | Conexi\u00f3n I2C incorrecta | Verifica SCL (GPIO 21) y SDA (GPIO 22) |
| Bluetooth no funciona | Firmware no cargado | Recarga el firmware |
| Micr\u00f3fono no graba | Conexi\u00f3n I2S incorrecta | Verifica WS, SCK, SD |
| Parlante no suena | Conexi\u00f3n PWM incorrecta | Verifica GPIO 26 |

---

## \ud83d\udc04 Actualizando el Firmware

### Pasos para Actualizar
1. **Descarga la \u00faltima versi\u00f3n del firmware** desde GitHub:
   ```bash
   git pull origin main
   ```

2. **Carga el nuevo firmware** usando uno de los m\u00e9todos anteriores.

3. **Reinicia el ESP32** para aplicar los cambios.

### \u26a0\ufe0f Notas Importantes
- **Haz backup** de tu firmware actual antes de actualizar.
- **Verifica los cambios** en el archivo `CHANGELOG.md` (si existe) para saber qu\u00e9 hay de nuevo.
- Si la actualizaci\u00f3n falla, **vuelve a cargar el firmware anterior**.

---

## \ud83d\udc81 Consejos Adicionales

1. **Usa un Power Bank de calidad**: Algunos Power Banks **apagan la salida** despu\u00e9s de unos minutos si no detectan suficiente consumo. Si el ESP32 se reinicia solo, prueba con otro Power Bank.

2. **Verifica las conexiones**: Si algo no funciona, **revisa las conexiones** antes de asumir que el firmware est\u00e1 mal.

3. **Usa el Monitor Serial**: El **Monitor Serial** es tu mejor amigo para depurar problemas.

4. **Consulta la documentaci\u00f3n**: Si tienes dudas, revisa:
   - [Diagrama de Hardware](../hardware/components.md)
   - [Gu\u00eda de Ensamblaje](../hardware/assembly.md)
   - [Arquitectura del Sistema](../ARCHITECTURE.md)

---

## \ud83d\udc31 \u00a1F\u00e9lix est\u00e1 listo para usar!

Una vez que el firmware est\u00e9 cargado correctamente, **F\u00e9lix est\u00e1 listo para chatear contigo**. 

**\u26a1 Pr\u00f3ximo paso:** [Configurar la App M\u00f3vil \u2192](../mobile/setup.md)

---

**\ud83d\udc31 F\u00e9lix te espera... Ronronea... \ud83d\udc3e**

[\u2190 Volver a Firmware](firmware) | [\ud83d\udc82 Ver Debugging Guide \u2192](debugging.md)
