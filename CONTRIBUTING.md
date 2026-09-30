# 🤝 Cómo contribuir a Félix / GatoGPT

**🐱 ¡Gracias por tu interés en ayudar a que Félix sea mejor!**

Este proyecto es **open source** y crece gracias a colaboradores como tú. A continuación te explicamos cómo puedes contribuir de manera efectiva, clara y respetuosa.

---

## 📁 Índice
1. [Reglas generales](#-reglas-generales)
2. [Áreas de contribución](#-áreas-de-contribución)
3. [Primeros pasos](#-primeros-pasos)
4. [Estándares de código](#-estándares-de-código)
5. [Enviando cambios](#-enviando-cambios)
6. [Reportando problemas](#-reportando-problemas)
7. [Solicitando funciones](#-solicitando-funciones)
8. [Código de conducta](#-código-de-conducta)
9. [Reconocimiento](#-reconocimiento)

---

## 📓 Reglas generales

### ✅ Qué se espera de ti
- **Sé amable y respetuoso** con todos los miembros de la comunidad.
- **Sigue el [Código de Conducta](CODE_OF_CONDUCT.md)**.
- **Documenta tus cambios**: añade comentarios en el código y actualiza la documentación si es necesario.
- **Prueba tus cambios**: asegúrate de que el código funcione antes de enviar un pull request.
- **Usa ramas descriptivas**: por ejemplo, `feat/tts-voice`, `fix/bluetooth-bug`, `docs/hardware-guide`.

### ❌ Qué NO hacer
- **No envíes código sin probarlo**.
- **No ignores las pruebas existentes** (si las hay).
- **No modifiques el sistema de personalidad de Félix** (`personality.py`) sin consultar antes. Este es el **corazón** del proyecto y debe mantenerse consistente en todas las versiones.
- **No incluyas información personal o sensible** en el repositorio.
- **No uses el nombre del proyecto para fines comerciales** sin permiso.

---

## 🐟 Áreas de contribución

Félix es un proyecto **multidisciplinario**. Puedes ayudar en varias áreas:

| Área | Descripción | Dificultad | Habilidades requeridas | Etiqueta en issues |
|------|-------------|------------|------------------------|-------------------|
| **Hardware** | Mejorar esquemáticos, añadir sensores y optimizar conexiones | Media/Alta | Electrónica, ESP32, Fritzing | `hardware` |
| **Firmware** | Optimizar código MicroPython y añadir funcionalidades al ESP32 | Alta | MicroPython, C/C++, ESP-IDF | `firmware` |
| **App móvil** | Mejorar UI/UX, añadir funciones y optimizar rendimiento | Media | Kivy, Python, Android | `mobile` |
| **IA / Modelos** | Fine-tunear modelos, mejorar prompts y optimizar inferencia | Alta | PyTorch, Transformers, ONNX | `ai` |
| **Voz (TTS/STT)** | Integrar motores de voz y mejorar reconocimiento | Media | Python, librerías de audio | `voice` |
| **Documentación** | Traducir, mejorar guías y crear tutoriales | Baja | Markdown, GitHub | `documentation` |
| **Testing** | Añadir tests unitarios/integración y reportar bugs | Media | pytest, unittest | `testing` |
| **Comunidad** | Moderar Discord, ayudar en issues y crear contenido | Baja | Comunicación, paciencia | `community` |
| **Diseño 3D** | Crear carcasas e impresiones 3D para el hardware | Media | Blender, Tinkercad, Fusion 360 | `3d-design` |

---

## 🚀 Primeros pasos

### 1️⃣ Fork y clone
```bash
# 1. Haz fork del repositorio en GitHub
#    (botón "Fork" en la parte superior derecha de la página del repo)

# 2. Clona tu fork localmente
git clone https://github.com/tu-usuario/Luciano-Sarmiento.git
cd Luciano-Sarmiento

# 3. Añade el upstream (repositorio original)
git remote add upstream https://github.com/luciano2-web/Luciano-Sarmiento.git
```

### 2️⃣ Configura el entorno
#### Para desarrollo en **App Móvil** (Android/iOS/PC):
```bash
# Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instala dependencias
pip install -r src/mobile/requirements_mobile.txt
```

#### Para desarrollo en **Firmware (ESP32)**:
```bash
# Instala MicroPython y herramientas para ESP32
pip install esptool adafruit-ampy

# Descarga el firmware de MicroPython para ESP32
wget https://micropython.org/resources/firmware/esp32-YYYYMMDD-vX.X.X.bin
```

### 3️⃣ Crea una rama
```bash
# Actualiza tu fork
git fetch upstream
git merge upstream/main

# Crea una nueva rama para tu contribución
git checkout -b tipo/descripcion  # Ej: feat/tts-voice, fix/bluetooth-bug
```

---

## 💡 Estándares de código

### 🐍 Python
- **Sigue PEP 8**: usa 4 espacios para indentación y líneas de máximo 88 caracteres.
- **Nombres descriptivos**: usa `snake_case` para variables y funciones, y `PascalCase` para clases.
- **Tipado**: usa type hints cuando sea posible.
- **Documentación**: añade docstrings a funciones y clases.

**Ejemplo:**
```python
from typing import Optional


def generate_felix_response(prompt: str, max_length: int = 100) -> Optional[str]:
    """
    Genera una respuesta de Félix usando el modelo de IA.

    Args:
        prompt: El texto de entrada del usuario.
        max_length: Longitud máxima de la respuesta.

    Returns:
        La respuesta generada o None si hay un error.
    """
    # ... implementación ...
    pass
```

### 🧑‍💻 MicroPython (ESP32)
- **Evita librerías pesadas**: el ESP32 tiene memoria limitada.
- **Manejo de errores**: usa `try-except` para operaciones críticas (Bluetooth, I2C).
- **Optimiza el uso de memoria**: libera recursos cuando no se usen.

**Ejemplo:**
```python
from machine import I2C, Pin
import time


def read_inmp441(i2c: I2C, address: int = 0x34) -> bytes:
    """Lee datos del micrófono INMP441."""
    try:
        # ... implementación ...
        pass
    except OSError as e:
        print(f"Error al leer INMP441: {e}")
        return b''
```

### 📖 Kivy (App móvil)
- **Sigue el patrón MVVM**: separa la lógica de negocio de la interfaz.
- **Usa archivos `.kv`**: para diseños complejos, usa archivos `.kv` en lugar de Python puro.
- **Optimiza el rendimiento**: evita actualizaciones innecesarias de la UI.

---

## 📥 Enviando cambios

### 1️⃣ Haz commit de tus cambios
```bash
# Añade solo los archivos relevantes
git add src/mobile/chat_engine.py

# Escribe un mensaje de commit claro
git commit -m "feat: añadir motor de voz TTS para Félix"
```

**Reglas para mensajes de commit:**
- Usa el prefijo `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, etc. (según [Conventional Commits](https://www.conventionalcommits.org/)).
- Mantén el mensaje en **máximo 50 caracteres** en la primera línea.
- Si es necesario, añade una descripción extendida.

**Ejemplos:**
```bash
git commit -m "feat: añadir comando @help para listar comandos"
git commit -m "fix: corregir bug en comunicación Bluetooth"
git commit -m "docs: actualizar guía de hardware"
git commit -m "refactor: modularizar chat_engine.py"
```

### 2️⃣ Sincroniza con el upstream
```bash
# Asegúrate de que tu rama esté actualizada
git fetch upstream
git rebase upstream/main
```

### 3️⃣ Envía tu Pull Request (PR)
```bash
# Sube tu rama a tu fork
git push origin tipo/descripcion
```

Luego:
1. Ve a [https://github.com/luciano2-web/Luciano-Sarmiento](https://github.com/luciano2-web/Luciano-Sarmiento).
2. Haz clic en **"Pull Requests"** > **"New Pull Request"**.
3. Selecciona tu rama y describe:
   - **Título**: claro y descriptivo (ej.: "feat: añadir TTS para voz de Félix").
   - **Descripción**: explica **qué** hiciste y **por qué**. Incluye capturas de pantalla si es relevante.
   - **Issues relacionadas**: usa `Closes #123` o `Fixes #456` para cerrar issues automáticamente.

---

## 📢 Reportando problemas

Si encuentras un **bug**, abre un **Issue** en GitHub:

1. Ve a [Issues](https://github.com/luciano2-web/Luciano-Sarmiento/issues).
2. Haz clic en **"New Issue"**.
3. Usa la plantilla **"Bug Report"** y completa:
   - **Título**: descripción corta del problema.
   - **Descripción**: explica el problema en detalle.
   - **Pasos para reproducir**: cómo podemos replicar el error.
   - **Comportamiento esperado**: qué debería pasar.
   - **Comportamiento actual**: qué pasa realmente.
   - **Entorno**: versión de Python, SO, hardware, etc.
   - **Capturas de pantalla / logs**: si aplica.

**Ejemplo de un buen reporte de bug:**
```
Título: Error al conectar ESP32 con app móvil vía Bluetooth

Descripción:
La app móvil se congela al intentar conectarse al ESP32 después de 3 intentos fallidos.

Pasos para reproducir:
1. Encender el ESP32 con el firmware de Félix.
2. Abrir la app móvil.
3. Intentar conectar vía Bluetooth.
4. Después de 3 intentos fallidos, la app se congela.

Comportamiento esperado:
La app debería mostrar un mensaje de error y permitir reintentar.

Comportamiento actual:
La app se congela y no responde.

Entorno:
- Android 13
- ESP32-WROOM-32
- App versión: 1.0.0
- Logs: [adjuntar logs]
```

---

## 💋 Solicitando funciones

Si tienes una **idea para mejorar Félix**, abre un **Issue** con la plantilla **"Feature Request"**:

1. Ve a [Issues](https://github.com/luciano2-web/Luciano-Sarmiento/issues).
2. Haz clic en **"New Issue"**.
3. Usa la plantilla **"Feature Request"** y completa:
   - **Título**: nombre de la funcionalidad.
   - **Descripción**: explica qué hace la funcionalidad y por qué es útil.
   - **Problema que resuelve**: qué problema actual soluciona.
   - **Posible implementación**: ideas técnicas (opcional).

**Ejemplo de una buena solicitud de funcionalidad:**
```
Título: Añadir comando @gatmusic para generar música

Descripción:
Sería genial si Félix pudiera generar música de fondo usando IA, similar a @gatimage.

Problema que resuelve:
Actualmente, Félix solo puede generar imágenes. Añadir música expandiría sus capacidades creativas.

Posible implementación:
- Usar un modelo ligero como Riffusion o Stable Audio.
- Integrar con el sistema de comandos existente.
- Guardar los archivos generados en felix_outputs/music/.
```

---

## 👌 Código de conducta

Este proyecto sigue el **[Código de Conducta del Contribuidor](CODE_OF_CONDUCT.md)**, basado en el [Contributor Covenant](https://www.contributor-covenant.org/).

**Reglas clave:**
- **Sé inclusivo**: no toleramos discriminación por género, raza, religión, orientación sexual, etc.
- **Sé respetuoso**: critica las ideas, no a las personas.
- **Sé responsable**: no compartas información personal sin consentimiento.
- **Sé colaborativo**: ayuda a otros y acepta ayuda.

**⚠️ Si ves un comportamiento inapropiado, repórtalo a [luciano2-web](https://github.com/luciano2-web).**

---

## 🏖 Reconocimiento

Todos los colaboradores serán reconocidos en:
- El archivo **[CONTRIBUTORS.md](CONTRIBUTORS.md)**.
- La sección de **🏖 Top Contribuidores** en el README.md.
- **Badges** en sus perfiles de GitHub (por ejemplo, *Félix Contributor*).

**Niveles de reconocimiento:**
| Nivel | Requisitos | Badge |
|-------|------------|-------|
| **Bronce** | 1-5 contribuciones | 🧶 |
| **Plata** | 6-15 contribuciones | 🧸 |
| **Oro** | 16+ contribuciones | 🏆 |
| **Leyenda** | Contribuciones excepcionales | 👑 |

---

## 🐧 Issues para principiantes

Si eres nuevo en el proyecto, te recomendamos empezar con issues etiquetados como:
- [`good first issue`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/good%20first%20issue): problemas simples y bien definidos.
- [`documentation`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/documentation): mejorar guías o traducciones.
- [`enhancement`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/enhancement): mejoras menores.

**Ejemplos de "good first issues":**
- Añadir más emojis de gato a las respuestas de Félix.
- Traducir la documentación al inglés.
- Crear un diagrama de flujo para el hardware.
- Añadir un comando `@joke` para que Félix cuente chistes.

---

## 🐈 ¿Necesitas ayuda?

- **¿Preguntas sobre el código?** Abre un [Issue](https://github.com/luciano2-web/Luciano-Sarmiento/issues) con la etiqueta `question`.
- **¿Quieres chatear?** ¡Únete a nuestro [Discord](https://discord.gg/felix-gatogpt) (próximamente)!
- **¿Encontraste un bug?** Sigue las instrucciones en [Reportando problemas](#-reportando-problemas).
- **¿Tienes una idea?** Sigue las instrucciones en [Solicitando funciones](#-solicitando-funciones).

---

**🐱 ¡Gracias por ser parte de la comunidad de Félix!**

*Félix te espera... Ronronea... 🐾*
