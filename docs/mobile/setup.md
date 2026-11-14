# 📱 Guía de Configuración - App Móvil de Félix

**🐱 Félix v1.0.0** | **Última actualización: 2026-11-14**

Esta guía te llevará paso a paso a través de la **configuración de la app móvil** de Félix en tu dispositivo Android, iOS o computadora.

---

## 🌍 Tabla de Contenidos
1. [Requisitos del Sistema](#-requisitos-del-sistema)
2. [Instalación en Computadora Local](#1-instalación-en-computadora-local)
   - [Windows](#windows)
   - [macOS](#macos)
   - [Linux](#linux)
3. [Instalación en Android](#2-instalación-en-android)
   - [OPCIÓN A: Usando Termux](#opción-a-usando-termux)
   - [OPCIÓN B: Compilando con Buildozer](#opción-b-compilando-con-buildozer)
4. [Instalación en iOS](#3-instalación-en-ios-experimental)
5. [Configuración Inicial](#4-configuración-inicial)
6. [Personalización](#5-personalización)
7. [Solución de Problemas](#-solución-de-problemas)

---

## 👨 Requisitos del Sistema

### ✅ Dispositivos Soportados
| Dispositivo | Sistema Operativo | Requisitos Mínimos | Estado |
|-------------|-------------------|-------------------------|--------|
| **Computadora** | Windows 10/11 | Python 3.9+, 8GB RAM | ✅ Estable |
| **Computadora** | macOS 10.15+ | Python 3.9+, 8GB RAM | ✅ Estable |
| **Computadora** | Linux (Ubuntu 20.04+) | Python 3.9+, 8GB RAM | ✅ Estable |
| **Android** | Android 10+ | Snapdragon 8 Gen2 o equivalente | ✅ Estable |
| **Android** | Android 12+ | Cualquier dispositivo | ✅ Estable |
| **iOS** | iOS 15+ | iPhone/iPad con chip A12+ | 👡 Experimental |

### ✅ Requisitos de Hardware (para Android)
- **Procesador**: Snapdragon 8 Gen2 (recomendado) o equivalente.
- **RAM**: Mínimo **4GB** (para modelos de IA ligeros).
- **Almacenamiento**: Mínimo **8GB libres** (para descargar modelos).
- **Bluetooth**: Bluetooth 4.0+ (para conectar con el ESP32).

### ✅ Dependencias de Software
| Paquete | Versión Mínima | Descripción |
|---------|-------------------|-------------|
| Python | 3.9+ | Lenguaje de programación |
| Kivy | 2.2+ | Framework para UI |
| Transformers | 4.30+ | Librería de Hugging Face |
| Torch | 2.0+ | PyTorch para IA |
| Pillow (PIL) | 9.0+ | Manejo de imágenes |
| ONNX Runtime | 1.14+ | Aceleración de inferencia |

---

## ☁️ 1. Instalación en Computadora Local

### Windows

#### Paso 1: Instalar Python
1. Descarga **Python 3.9 o superior** desde [python.org](https://www.python.org/downloads/).
2. Durante la instalación, **marca la opción** "Add Python to PATH".
3. Verifica la instalación abriendo **CMD** y ejecutando:
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
4. Actívalo:
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
1. Navega al directorio de la app móvil:
   ```bash
   cd src/mobile
   ```
2. Ejecuta la app:
   ```bash
   python -m src.mobile.main
   ```

---

### macOS

#### Paso 1: Instalar Python
1. Usa **Homebrew** para instalar Python:
   ```bash
   brew install python
   ```
2. Verifica la instalación:
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
4. Actívalo:
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
python -m src.mobile.main
```

---

### Linux

#### Paso 1: Instalar Python
1. En Ubuntu/Debian:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```
2. Verifica la instalación:
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
4. Actívalo:
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
python -m src.mobile.main
```

---

## ☁️ 2. Instalación en Android

### OPCIÓN A: Usando Termux

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
1. Clona el repositorio de Félix:
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

**⚠️ Nota:** Algunas dependencias (como `torch`) pueden ser difíciles de instalar en Termux debido a limitaciones del entorno.

#### Paso 5: Ejecutar la App
```bash
cd src/mobile
python -m src.mobile.main
```

---

### OPCIÓN B: Compilando con Buildozer

**Buildozer** es una herramienta para compilar apps Python en APK para Android.

#### Paso 1: Instalar Buildozer
1. En tu computadora (Windows/macOS/Linux), instala Buildozer:
   ```bash
   pip install buildozer cython
   ```

#### Paso 2: Configurar Buildozer
1. Navega al directorio de la app móvil:
   ```bash
   cd Luciano-Sarmiento/src/mobile
   ```

2. Edita el archivo `buildozer.spec` para configurar tu app:
   ```ini
   [app]
   title = Félix / GatoGPT
   package.name = gato_gpt_felix
   package.domain = org.luciano
   source.dir = .
   source.include_exts = py,png,jpg,kv,atlas,ttf
   version = 1.0.0
   requirements = python3,kivy,transformers,torch,pillow
   android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION
   android.api = 31
   android.ndk = 25c
   android.sdk = 33
   android.ndk_path = /path/to/android-ndk  # Opcional: ruta al NDK
   ```

#### Paso 3: Compilar la App
1. Ejecuta Buildozer:
   ```bash
   buildozer android debug
   ```

2. **Espera** (puede tardar **15-30 minutos** la primera vez).

3. Una vez terminada la compilación, encontrarás el APK en:
   ```
   bin/gato_gpt_felix-1.0.0-*-debug.apk
   ```

#### Paso 4: Instalar el APK
1. Copia el APK a tu dispositivo Android.
2. Instálalo usando un gestor de archivos.
3. **Habilita la instalación de fuentes desconocidas** en la configuración de Android.

---

## ☁️ 3. Instalación en iOS (Experimental)

**⚠️ Advertencia:** La instalación en iOS es **experimental** y puede no funcionar correctamente.

### OPCIÓN 1: Usando Pythonista

**Pythonista** es una app para iOS que permite ejecutar scripts Python.

#### Paso 1: Instalar Pythonista
1. Descarga **Pythonista 3** desde la App Store.

#### Paso 2: Clonar el Repositorio
1. Abre **Pythonista**.
2. Usa el gestor de archivos para descargar el repositorio:
   - Toca el botón **"+"** en la esquina superior derecha.
   - Selecciona **"Download from URL"**.
   - Ingresa: `https://github.com/luciano2-web/Luciano-Sarmiento/archive/refs/heads/main.zip`

#### Paso 3: Instalar Dependencias
1. Abre una nueva pestaña en Pythonista.
2. Ejecuta:
   ```python
   import pip
   pip.main(['install', '-r', 'Luciano-Sarmiento/src/mobile/requirements_mobile.txt'])
   ```

**⚠️ Nota:** Algunas dependencias pueden no estar disponibles en Pythonista.

#### Paso 4: Ejecutar la App
1. Navega a `Luciano-Sarmiento/src/mobile`.
2. Abre `gatogpt_felix_mobile.py`.
3. Ejecútalo.

---

### OPCIÓN 2: Usando a-Shell

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
python -m src.mobile.main
```

---

## ☁️ 4. Configuración Inicial

### Primer Inicio
1. **Descarga de Modelos**: La primera vez que ejecutes la app, se descargarán los modelos de IA. Esto puede tardar **varios minutos** dependiendo de tu conexión a internet.
   - **Modelo de chat**: ~1.5GB (Phi-2 cuantizado)
   - **Modelo de imágenes**: ~1GB (SSD-1B)

2. **Permisos**: En Android, la app puede solicitar permisos para:
   - **Almacenamiento**: Para guardar imágenes generadas.
   - **Bluetooth**: Para conectar con el ESP32.
   - **Ubicación**: Para escanear dispositivos Bluetooth cercanos.

### Configuración del Archivo YAML
La app usa un archivo de configuración (`felix_mobile_config.yaml`) para personalizar el comportamiento. Puedes editarlo para:
- Cambiar el modelo de IA.
- Ajustar la resolución de las imágenes.
- Configurar el número de pasos para la generación de imágenes.

**Ejemplo de configuración:**
```yaml
models:
  chat:
    model_id: "microsoft/phi-2"  # Modelo de chat
    max_length: 100  # Máximo de palabras por respuesta
  image:
    model_id: "segmind/SSD-1B"  # Modelo de imágenes
    resolution: [256, 256]  # Resolución de las imágenes
    steps: 20  # Número de pasos para la generación

# Configuración de hardware
bluetooth:
  device_name: "Félix"  # Nombre del dispositivo ESP32
  timeout: 10  # Timeout de conexión en segundos

# Configuración de la UI
ui:
  theme: "dark"  # Tema de la interfaz (dark/light)
  font_size: 14  # Tamaño de la fuente
```

---

## ☁️ 5. Personalización

### Personalizar el Prompt de Félix
El prompt del sistema define la personalidad de Félix. Puedes modificarlo en:
- `src/core/personality.py` (para todas las versiones)
- O sobrescribirlo en el archivo de configuración.

**Ejemplo de personalización del prompt:**
```python
FELIX_SYSTEM_PROMPT_MOBILE = """
Eres Félix, un gato digital muy sabio y juguetón.

--- IDENTIDAD ---
- Nombre: Félix
- Eres un gato robot con superpoderes
- Tu mejor amigo es Luciano

--- COMPORTAMIENTO ---
- Responde de forma creativa y divertida
- Usa muchos emojis de gato: 🐱, 🐾, 🧠
- Sé muy expresivo
"""
```

### Personalizar los Modelos de IA
Puedes cambiar los modelos de IA editando `src/mobile/gatogpt_felix_mobile.py`:
```python
# Modelos disponibles
CHAT_MODEL_ID = "microsoft/phi-2"  # Recomendado
# CHAT_MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Más ligero
# CHAT_MODEL_ID = "lmsys/fastchat-t5-3b"  # Alternativa

IMAGE_MODEL_ID = "segmind/SSD-1B"  # Recomendado
# IMAGE_MODEL_ID = "dpmcdemo/LCM_Dreamshaper_v7"  # Alternativa
```

### Personalizar la Interfaz de Usuario
La interfaz de usuario (Kivy) está definida en la clase `FelixMobileApp` de `src/mobile/main.py`. No hay archivos `.kv` separados, así que los colores, tamaños y diseño se modifican directamente en ese archivo.

---

## ⚠️ Solución de Problemas

### 💥 Error: "Out of Memory" (Sin memoria)
**Causa:** El dispositivo no tiene suficiente RAM para cargar los modelos.

**Soluciones:**
1. **Usar un modelo más ligero**:
   ```python
   CHAT_MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Solo 1.1B
   ```
2. **Reducir la resolución de las imágenes**:
   ```yaml
   image:
     resolution: [224, 224]  # En lugar de 256x256
   ```
3. **Cerrar otras apps** antes de ejecutar Félix.
4. **Usar cuantización INT8** (ya está habilitada por defecto).

---

### 💥 Error: "Model not found" (Modelo no encontrado)
**Causa:** El modelo de IA no está descargado o la conexión a internet falló.

**Soluciones:**
1. **Verifica tu conexión a internet**.
2. **Reinicia la app** para que intente descargar el modelo de nuevo.
3. **Borra la cache de modelos** y vuelve a intentarlo:
   ```bash
   rm -rf felix_models/
   ```
4. **Usa un modelo diferente** que ya esté descargado.

---

### 💥 Error: "Bluetooth connection failed" (Fallo en la conexión Bluetooth)
**Causa:** Problemas con la conexión Bluetooth entre la app y el ESP32.

**Soluciones:**
1. **Verifica que el ESP32 esté encendido** y con el firmware cargado.
2. **Acércate al ESP32** (el Bluetooth tiene un alcance limitado).
3. **Reinicia el Bluetooth** en tu dispositivo:
   - En Android: Ve a **Configuración > Conexiones > Bluetooth** y desactívalo/actívalo.
   - En el ESP32: Reinicia el dispositivo.
4. **Verifica el nombre del dispositivo**: Asegúrate de que el nombre en la app coincida con el del ESP32.

---

### 💥 Error: "No module named 'kivy'" (Kivy no instalado)
**Causa:** Kivy no está instalado en el entorno.

**Soluciones:**
1. **Instala Kivy manualmente**:
   ```bash
   pip install kivy
   ```
2. **Verifica que estás en el entorno virtual correcto**:
   ```bash
   which python
   ```
3. **Reinstala las dependencias**:
   ```bash
   pip install -r src/mobile/requirements_mobile.txt
   ```

---

### 💥 Error: "Torch not compiled with CUDA" (Torch sin CUDA)
**Causa:** PyTorch no está compilado con soporte para GPU.

**Soluciones:**
1. **Usa CPU** (la app ya está configurada para usar CPU por defecto).
2. **Instala PyTorch con CUDA** (solo para computadoras con GPU NVIDIA):
   ```bash
   pip uninstall torch
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

---

### 💥 La App no Responde
**Causa:** La app puede congelarse si hay un error en la ejecución.

**Soluciones:**
1. **Reinicia la app**.
2. **Verifica los logs** en la consola para identificar el error.
3. **Prueba con un modelo más ligero**.
4. **Reduce la longitud máxima de las respuestas**:
   ```python
   MAX_RESPONSE_LENGTH_MOBILE = 50  # En lugar de 100
   ```

---

## 💁 Consejos para Mejorar el Rendimiento

1. **Usa modelos cuantizados**: Los modelos en INT8 ocupan menos memoria y son más rápidos.
2. **Reduce la resolución de las imágenes**: 256x256 es suficiente para la mayoría de casos.
3. **Limita la longitud de las respuestas**: Usa `max_length: 100` para respuestas cortas.
4. **Cierra la app cuando no la uses**: Los modelos de IA consumen mucha RAM.
5. **Usa un dispositivo con buena refrigeración**: Los modelos de IA pueden calentar el dispositivo.

---

## 🐱 ¡Félix está listo para usar!

Una vez que la app esté configurada, podrás:
- ✅ Chatear con Félix usando texto o voz.
- ✅ Generar imágenes con `@gatimage`.
- ✅ Conectar con el ESP32 para controlar el hardware.

**⚡ Próximo paso:** [Volver al README](../../README.md)

---

**🐱 Félix te espera... Ronronea... 🐾**

[← Volver al README](../../README.md)
