# \ud83d\udcf1 Gu\u00eda de Configuraci\u00f3n - App M\u00f3vil de F\u00e9lix

**\ud83d\udc31 F\u00e9lix v2.0** | **\u00daltima actualizaci\u00f3n: 2024-09-28**

Esta gu\u00eda te llevar\u00e1 paso a paso a trav\u00e9s de la **configuraci\u00f3n de la app m\u00f3vil** de F\u00e9lix en tu dispositivo Android, iOS o computadora.

---

## \ud83c\udf0d Tabla de Contenidos
1. [Requisitos del Sistema](#-requisitos-del-sistema)
2. [Instalaci\u00f3n en Computadora Local](#1-instalaci\u00f3n-en-computadora-local)
   - [Windows](#windows)
   - [macOS](#macos)
   - [Linux](#linux)
3. [Instalaci\u00f3n en Android](#2-instalaci\u00f3n-en-android)
   - [OPCI\u00d3N A: Usando Termux](#opci\u00f3n-a-usando-termux)
   - [OPCI\u00d3N B: Compilando con Buildozer](#opci\u00f3n-b-compilando-con-buildozer)
4. [Instalaci\u00f3n en iOS](#3-instalaci\u00f3n-en-ios-experimental)
5. [Configuraci\u00f3n Inicial](#4-configuraci\u00f3n-inicial)
6. [Personalizaci\u00f3n](#5-personalizaci\u00f3n)
7. [Soluci\u00f3n de Problemas](#-soluci\u00f3n-de-problemas)

---

## \ud83d\udc68 Requisitos del Sistema

### \u2705 Dispositivos Soportados
| Dispositivo | Sistema Operativo | Requisitos M\u00ednimos | Estado |
|-------------|-------------------|-------------------------|--------|
| **Computadora** | Windows 10/11 | Python 3.9+, 8GB RAM | \u2705 Estable |
| **Computadora** | macOS 10.15+ | Python 3.9+, 8GB RAM | \u2705 Estable |
| **Computadora** | Linux (Ubuntu 20.04+) | Python 3.9+, 8GB RAM | \u2705 Estable |
| **Android** | Android 10+ | Snapdragon 8 Gen2 o equivalente | \u2705 Estable |
| **Android** | Android 12+ | Cualquier dispositivo | \u2705 Estable |
| **iOS** | iOS 15+ | iPhone/iPad con chip A12+ | \ud83d\udc61 Experimental |

### \u2705 Requisitos de Hardware (para Android)
- **Procesador**: Snapdragon 8 Gen2 (recomendado) o equivalente.
- **RAM**: M\u00ednimo **4GB** (para modelos de IA ligeros).
- **Almacenamiento**: M\u00ednimo **8GB libres** (para descargar modelos).
- **Bluetooth**: Bluetooth 4.0+ (para conectar con el ESP32).

### \u2705 Dependencias de Software
| Paquete | Versi\u00f3n M\u00ednima | Descripci\u00f3n |
|---------|-------------------|-------------|
| Python | 3.9+ | Lenguaje de programaci\u00f3n |
| Kivy | 2.2+ | Framework para UI |
| Transformers | 4.30+ | Librer\u00eda de Hugging Face |
| Torch | 2.0+ | PyTorch para IA |
| Pillow (PIL) | 9.0+ | Manejo de im\u00e1genes |
| ONNX Runtime | 1.14+ | Aceleraci\u00f3n de inferencia |

---

## \u2601\ufe0f 1. Instalaci\u00f3n en Computadora Local

### Windows

#### Paso 1: Instalar Python
1. Descarga **Python 3.9 o superior** desde [python.org](https://www.python.org/downloads/).
2. Durante la instalaci\u00f3n, **marca la opci\u00f3n** "Add Python to PATH".
3. Verifica la instalaci\u00f3n abriendo **CMD** y ejecutando:
   ```bash
   python --version
   pip --version
   ```

#### Paso 2: Crear un Entorno Virtual
1. Abre **CMD** o **PowerShell**.
2. Navega al directorio del proyecto:
   ```bash
   cd Luciano-Sarmiento
   ```
3. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```
4. Act\u00edvalo:
   ```bash
   venv\Scripts\activate
   ```

#### Paso 3: Instalar Dependencias
1. Instala las dependencias usando el archivo `requirements_mobile.txt`:
   ```bash
   pip install -r src/mobile/requirements_mobile.txt
   ```

2. **Opcional**: Si quieres soporte para GPU (NVIDIA), instala PyTorch con CUDA:
   ```bash
   pip uninstall torch
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

#### Paso 4: Ejecutar la App
1. Navega al directorio de la app m\u00f3vil:
   ```bash
   cd src/mobile
   ```
2. Ejecuta la app:
   ```bash
   python gatogpt_felix_mobile.py
   ```

---

### macOS

#### Paso 1: Instalar Python
1. Usa **Homebrew** para instalar Python:
   ```bash
   brew install python
   ```
2. Verifica la instalaci\u00f3n:
   ```bash
   python3 --version
   pip3 --version
   ```

#### Paso 2: Crear un Entorno Virtual
1. Abre **Terminal**.
2. Navega al directorio del proyecto:
   ```bash
   cd Luciano-Sarmiento
   ```
3. Crea un entorno virtual:
   ```bash
   python3 -m venv venv
   ```
4. Act\u00edvalo:
   ```bash
   source venv/bin/activate
   ```

#### Paso 3: Instalar Dependencias
1. Instala las dependencias:
   ```bash
   pip install -r src/mobile/requirements_mobile.txt
   ```

2. **Opcional**: Para soporte de GPU (Mac con chip M1/M2), instala PyTorch con Metal:
   ```bash
   pip uninstall torch
   pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
   ```

#### Paso 4: Ejecutar la App
```bash
cd src/mobile
python gatogpt_felix_mobile.py
```

---

### Linux

#### Paso 1: Instalar Python
1. En Ubuntu/Debian:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```
2. Verifica la instalaci\u00f3n:
   ```bash
   python3 --version
   pip3 --version
   ```

#### Paso 2: Crear un Entorno Virtual
1. Abre **Terminal**.
2. Navega al directorio del proyecto:
   ```bash
   cd Luciano-Sarmiento
   ```
3. Crea un entorno virtual:
   ```bash
   python3 -m venv venv
   ```
4. Act\u00edvalo:
   ```bash
   source venv/bin/activate
   ```

#### Paso 3: Instalar Dependencias
1. Instala las dependencias:
   ```bash
   pip install -r src/mobile/requirements_mobile.txt
   ```

2. **Opcional**: Para soporte de GPU (NVIDIA), instala PyTorch con CUDA:
   ```bash
   pip uninstall torch
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

#### Paso 4: Ejecutar la App
```bash
cd src/mobile
python gatogpt_felix_mobile.py
```

---

## \u2601\ufe0f 2. Instalaci\u00f3n en Android

### OPCI\u00d3N A: Usando Termux

**Termux** es una terminal para Android que permite ejecutar Python y otros programas.

#### Paso 1: Instalar Termux
1. Descarga **Termux** desde:
   - [F-Droid](https://f-droid.org/en/packages/com.termux/) (recomendado)
   - Google Play Store (puede estar desactualizado)

#### Paso 2: Configurar Termux
1. Abre **Termux**.
2. Actualiza los paquetes:
   ```bash
   pkg update && pkg upgrade
   ```
3. Instala Python:
   ```bash
   pkg install python
   ```
4. Instala git:
   ```bash
   pkg install git
   ```

#### Paso 3: Clonar el Repositorio
1. Clona el repositorio de F\u00e9lix:
   ```bash
   git clone https://github.com/luciano2-web/Luciano-Sarmiento.git
   cd Luciano-Sarmiento
   ```

#### Paso 4: Instalar Dependencias
1. Instala pip:
   ```bash
   pkg install python-pip
   ```
2. Instala las dependencias:
   ```bash
   pip install -r src/mobile/requirements_mobile.txt
   ```

**\u26a0\ufe0f Nota:** Algunas dependencias (como `torch`) pueden ser dif\u00edciles de instalar en Termux debido a limitaciones del entorno.

#### Paso 5: Ejecutar la App
```bash
cd src/mobile
python gatogpt_felix_mobile.py
```

---

### OPCI\u00d3N B: Compilando con Buildozer

**Buildozer** es una herramienta para compilar apps Python en APK para Android.

#### Paso 1: Instalar Buildozer
1. En tu computadora (Windows/macOS/Linux), instala Buildozer:
   ```bash
   pip install buildozer cython
   ```

#### Paso 2: Configurar Buildozer
1. Navega al directorio de la app m\u00f3vil:
   ```bash
   cd Luciano-Sarmiento/src/mobile
   ```

2. Edita el archivo `buildozer.spec` para configurar tu app:
   ```ini
   [app]
   title = Félix / GatoGPT
   package.name = felix
   package.domain = org.luciano2web
   source.dir = .
   source.include_exts = py,png,jpg,kv,atlas,ttf
   version = 2.0.0
   requirements = python3,kivy,transformers,torch,pillow
   android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION
   android.api = 30
   android.ndk = 23b
   android.sdk = 33
   android.ndk_path = /path/to/android-ndk  # Opcional: ruta al NDK
   ```

#### Paso 3: Compilar la App
1. Ejecuta Buildozer:
   ```bash
   buildozer android debug
   ```

2. **Espera** (puede tardar **15-30 minutos** la primera vez).

3. Una vez terminada la compilaci\u00f3n, encontrar\u00e1s el APK en:
   ```
   bin/felix-2.0.0-debug.apk
   ```

#### Paso 4: Instalar el APK
1. Copia el APK a tu dispositivo Android.
2. Inst\u00e1lalo usando un gestor de archivos.
3. **Habilita la instalaci\u00f3n de fuentes desconocidas** en la configuraci\u00f3n de Android.

---

## \u2601\ufe0f 3. Instalaci\u00f3n en iOS (Experimental)

**\u26a0\ufe0f Advertencia:** La instalaci\u00f3n en iOS es **experimental** y puede no funcionar correctamente.

### OPCI\u00d3N 1: Usando Pythonista

**Pythonista** es una app para iOS que permite ejecutar scripts Python.

#### Paso 1: Instalar Pythonista
1. Descarga **Pythonista 3** desde la App Store.

#### Paso 2: Clonar el Repositorio
1. Abre **Pythonista**.
2. Usa el gestor de archivos para descargar el repositorio:
   - Toca el bot\u00f3n **"+"** en la esquina superior derecha.
   - Selecciona **"Download from URL"**.
   - Ingresa: `https://github.com/luciano2-web/Luciano-Sarmiento/archive/refs/heads/main.zip`

#### Paso 3: Instalar Dependencias
1. Abre una nueva pesta\u00f1a en Pythonista.
2. Ejecuta:
   ```python
   import pip
   pip.main(['install', '-r', 'Luciano-Sarmiento/src/mobile/requirements_mobile.txt'])
   ```

**\u26a0\ufe0f Nota:** Algunas dependencias pueden no estar disponibles en Pythonista.

#### Paso 4: Ejecutar la App
1. Navega a `Luciano-Sarmiento/src/mobile`.
2. Abre `gatogpt_felix_mobile.py`.
3. Ejec\u00fatalo.

---

### OPCI\u00d3N 2: Usando a-Shell

**a-Shell** es otra terminal para iOS con soporte para Python.

#### Paso 1: Instalar a-Shell
1. Descarga **a-Shell** desde la App Store.

#### Paso 2: Clonar el Repositorio
1. Abre **a-Shell**.
2. Ejecuta:
   ```bash
   git clone https://github.com/luciano2-web/Luciano-Sarmiento.git
   cd Luciano-Sarmiento
   ```

#### Paso 3: Instalar Dependencias
1. Instala las dependencias:
   ```bash
   pip install -r src/mobile/requirements_mobile.txt
   ```

#### Paso 4: Ejecutar la App
```bash
cd src/mobile
python gatogpt_felix_mobile.py
```

---

## \u2601\ufe0f 4. Configuraci\u00f3n Inicial

### Primer Inicio
1. **Descarga de Modelos**: La primera vez que ejecutes la app, se descargar\u00e1n los modelos de IA. Esto puede tardar **varios minutos** dependiendo de tu conexi\u00f3n a internet.
   - **Modelo de chat**: ~1.5GB (Phi-2 cuantizado)
   - **Modelo de im\u00e1genes**: ~1GB (SSD-1B)

2. **Permisos**: En Android, la app puede solicitar permisos para:
   - **Almacenamiento**: Para guardar im\u00e1genes generadas.
   - **Bluetooth**: Para conectar con el ESP32.
   - **Ubicaci\u00f3n**: Para escanear dispositivos Bluetooth cercanos.

### Configuraci\u00f3n del Archivo YAML
La app usa un archivo de configuraci\u00f3n (`felix_mobile_config.yaml`) para personalizar el comportamiento. Puedes editarlo para:
- Cambiar el modelo de IA.
- Ajustar la resoluci\u00f3n de las im\u00e1genes.
- Configurar el n\u00famero de pasos para la generaci\u00f3n de im\u00e1genes.

**Ejemplo de configuraci\u00f3n:**
```yaml
models:
  chat:
    model_id: "microsoft/phi-2"  # Modelo de chat
    max_length: 100  # M\u00e1ximo de palabras por respuesta
  image:
    model_id: "segmind/SSD-1B"  # Modelo de im\u00e1genes
    resolution: [256, 256]  # Resoluci\u00f3n de las im\u00e1genes
    steps: 20  # N\u00famero de pasos para la generaci\u00f3n

# Configuraci\u00f3n de hardware
bluetooth:
  device_name: "F\u00e9lix"  # Nombre del dispositivo ESP32
  timeout: 10  # Timeout de conexi\u00f3n en segundos

# Configuraci\u00f3n de la UI
ui:
  theme: "dark"  # Tema de la interfaz (dark/light)
  font_size: 14  # Tama\u00f1o de la fuente
```

---

## \u2601\ufe0f 5. Personalizaci\u00f3n

### Personalizar el Prompt de F\u00e9lix
El prompt del sistema define la personalidad de F\u00e9lix. Puedes modificarlo en:
- `src/core/personality.py` (para todas las versiones)
- O sobrescribirlo en el archivo de configuraci\u00f3n.

**Ejemplo de personalizaci\u00f3n del prompt:**
```python
FELIX_SYSTEM_PROMPT_MOBILE = """
Eres F\u00e9lix, un gato digital muy sabio y juguet\u00f3n.

--- IDENTIDAD ---
- Nombre: F\u00e9lix
- Eres un gato robot con superpoderes
- Tu mejor amigo es Luciano

--- COMPORTAMIENTO ---
- Responde de forma creativa y divertida
- Usa muchos emojis de gato: \ud83d\udc31, \ud83d\udc3e, \ud83e\udde0
- Sé muy expresivo
"""
```

### Personalizar los Modelos de IA
Puedes cambiar los modelos de IA editando `src/mobile/gatogpt_felix_mobile.py`:
```python
# Modelos disponibles
CHAT_MODEL_ID = "microsoft/phi-2"  # Recomendado
# CHAT_MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # M\u00e1s ligero
# CHAT_MODEL_ID = "lmsys/fastchat-t5-3b"  # Alternativa

IMAGE_MODEL_ID = "segmind/SSD-1B"  # Recomendado
# IMAGE_MODEL_ID = "dpmcdemo/LCM_Dreamshaper_v7"  # Alternativa
```

### Personalizar la Interfaz de Usuario
La interfaz de usuario est\u00e1 definida en el c\u00f3digo de Kivy. Puedes modificar:
- Colores: En `src/mobile/ui/styles.py` (si existe).
- Tama\u00f1os: En el archivo `.kv` (si existe).
- Dise\u00f1o: En `src/mobile/ui/app.py` (si existe).

---

## \u26a0\ufe0f Soluci\u00f3n de Problemas

### \ud83d\udca5 Error: "Out of Memory" (Sin memoria)
**Causa:** El dispositivo no tiene suficiente RAM para cargar los modelos.

**Soluciones:**
1. **Usar un modelo m\u00e1s ligero**:
   ```python
   CHAT_MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Solo 1.1B
   ```
2. **Reducir la resoluci\u00f3n de las im\u00e1genes**:
   ```yaml
   image:
     resolution: [224, 224]  # En lugar de 256x256
   ```
3. **Cerrar otras apps** antes de ejecutar F\u00e9lix.
4. **Usar cuantizaci\u00f3n INT8** (ya est\u00e1 habilitada por defecto).

---

### \ud83d\udca5 Error: "Model not found" (Modelo no encontrado)
**Causa:** El modelo de IA no est\u00e1 descargado o la conexi\u00f3n a internet fall\u00f3.

**Soluciones:**
1. **Verifica tu conexi\u00f3n a internet**.
2. **Reinicia la app** para que intente descargar el modelo de nuevo.
3. **Borra la cache de modelos** y vuelve a intentarlo:
   ```bash
   rm -rf felix_models/
   ```
4. **Usa un modelo diferente** que ya est\u00e9 descargado.

---

### \ud83d\udca5 Error: "Bluetooth connection failed" (Fallo en la conexi\u00f3n Bluetooth)
**Causa:** Problemas con la conexi\u00f3n Bluetooth entre la app y el ESP32.

**Soluciones:**
1. **Verifica que el ESP32 est\u00e9 encendido** y con el firmware cargado.
2. **Ac\u00e9rcate al ESP32** (el Bluetooth tiene un alcance limitado).
3. **Reinicia el Bluetooth** en tu dispositivo:
   - En Android: Ve a **Configuraci\u00f3n > Conexiones > Bluetooth** y desact\u00edvalo/act\u00edvalo.
   - En el ESP32: Reinicia el dispositivo.
4. **Verifica el nombre del dispositivo**: Aseg\u00farate de que el nombre en la app coincida con el del ESP32.

---

### \ud83d\udca5 Error: "No module named 'kivy'" (Kivy no instalado)
**Causa:** Kivy no est\u00e1 instalado en el entorno.

**Soluciones:**
1. **Instala Kivy manualmente**:
   ```bash
   pip install kivy
   ```
2. **Verifica que est\u00e1s en el entorno virtual correcto**:
   ```bash
   which python
   ```
3. **Reinstala las dependencias**:
   ```bash
   pip install -r src/mobile/requirements_mobile.txt
   ```

---

### \ud83d\udca5 Error: "Torch not compiled with CUDA" (Torch sin CUDA)
**Causa:** PyTorch no est\u00e1 compilado con soporte para GPU.

**Soluciones:**
1. **Usa CPU** (la app ya est\u00e1 configurada para usar CPU por defecto).
2. **Instala PyTorch con CUDA** (solo para computadoras con GPU NVIDIA):
   ```bash
   pip uninstall torch
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

---

### \ud83d\udca5 La App no Responde
**Causa:** La app puede congelarse si hay un error en la ejecuci\u00f3n.

**Soluciones:**
1. **Reinicia la app**.
2. **Verifica los logs** en la consola para identificar el error.
3. **Prueba con un modelo m\u00e1s ligero**.
4. **Reduce la longitud m\u00e1xima de las respuestas**:
   ```python
   MAX_RESPONSE_LENGTH_MOBILE = 50  # En lugar de 100
   ```

---

## \ud83d\udc81 Consejos para Mejorar el Rendimiento

1. **Usa modelos cuantizados**: Los modelos en INT8 ocupan menos memoria y son m\u00e1s r\u00e1pidos.
2. **Reduce la resoluci\u00f3n de las im\u00e1genes**: 256x256 es suficiente para la mayor\u00eda de casos.
3. **Limita la longitud de las respuestas**: Usa `max_length: 100` para respuestas cortas.
4. **Cierra la app cuando no la uses**: Los modelos de IA consumen mucha RAM.
5. **Usa un dispositivo con buena refrigeraci\u00f3n**: Los modelos de IA pueden calentar el dispositivo.

---

## \ud83d\udc31 \u00a1F\u00e9lix est\u00e1 listo para usar!

Una vez que la app est\u00e9 configurada, podr\u00e1s:
- \u2705 Chatear con F\u00e9lix usando texto o voz.
- \u2705 Generar im\u00e1genes con `@gatimage`.
- \u2705 Conectar con el ESP32 para controlar el hardware.

**\u26a1 Pr\u00f3ximo paso:** [Ver la Gu\u00eda de Uso \u2192](usage.md)

---

**\ud83d\udc31 F\u00e9lix te espera... Ronronea... \ud83d\udc3e**

[\u2190 Volver a Mobile](mobile) | [\ud83d\udc82 Ver Gu\u00eda de Uso \u2192](usage.md)
