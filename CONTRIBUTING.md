# 🤝 Cómo contribuir a Félix / GatoGPT

**🐱 ¡Gracias por tu interés en ayudar a que Félix sea mejor!**

Este proyecto es **open source** y crece gracias a colaboradores como tú. A continuación te explicamos cómo puedes contribuir de manera efectiva.

---

## 📁 Índice
1. [Reglas Generales](#-reglas-generales)
2. [Áreas de Contribución](#-áreas-de-contribución)
3. [Primeros Pasos](#-primeros-pasos)
4. [Estándares de Código](#-estándares-de-código)
5. [Enviando Cambios](#-enviando-cambios)
6. [Reportando Problemas](#-reportando-problemas)
7. [Solicitando Funciones](#-solicitando-funciones)
8. [Código de Conducta](#-código-de-conducta)
9. [Reconocimiento](#-reconocimiento)

---

## 📓 Reglas Generales

### ✅ Qué se espera de ti:
- **Sé amable y respetuoso** con todos los miembros de la comunidad.
- **Sigue el [Código de Conducta](CODE_OF_CONDUCT.md)**.
- **Documenta tus cambios**: Añade comentarios en el código y actualiza la documentación si es necesario.
- **Prueba tus cambios**: Asegúrate de que el código funcione antes de enviar un Pull Request.
- **Usa ramas descriptivas**: Ej: `feat/tts-voice`, `fix/bluetooth-bug`, `docs/hardware-guide`.

### ❌ Qué NO hacer:
- **No envíes código sin probar**.
- **No ignores los tests existentes** (si los hay).
- **No modifiques el sistema de personalidad de Félix** (`personality.py`) sin consultar primero. Este es el **corazón** del proyecto y debe mantenerse consistente en todas las versiones.
- **No incluyas información personal o sensible** en el repositorio.
- **No uses el nombre del proyecto para fines comerciales** sin permiso.

---

## 🐟 Áreas de Contribución

Félix es un proyecto **multidisciplinario**. Puedes ayudar en varias áreas:

| Área | Descripción | Dificultad | Habilidades Requeridas | Etiqueta en Issues |
|------|-------------|------------|------------------------|-------------------|
| **Hardware** | Mejorar esquemáticos, añadir sensores, optimizar conexiones | Media/Alta | Electrónica, ESP32, Fritzing | `hardware` |
| **Firmware** | Optimizar código MicroPython, añadir funcionalidades al ESP32 | Alta | MicroPython, C/C++, ESP-IDF | `firmware` |
| **App Móvil** | Mejorar UI/UX, añadir funciones, optimizar rendimiento | Media | Kivy, Python, Android | `mobile` |
| **IA / Modelos** | Fine-tunear el modelo de Félix, mejorar prompts, optimizar inferencia | Alta | PyTorch, Transformers, ONNX | `ai` |
| **Voz (TTS/STT)** | Integrar motores de voz, mejorar reconocimiento | Media | Python, librerías de audio | `voice` |
| **Documentación** | Traducir, mejorar guías, crear tutoriales | Baja | Markdown, GitHub | `documentation` |
| **Testing** | Añadir tests unitarios/integración, reportar bugs | Media | pytest, unittest | `testing` |
| **Comunidad** | Moderar Discord, ayudar en issues, crear contenido | Baja | Comunicación, paciencia | `community` |
| **Diseño 3D** | Crear casos imprimibles en 3D para el hardware | Media | Blender, Tinkercad, Fusion 360 | `3d-design` |

---

## 🚀 Primeros Pasos

### 1️⃣ Fork y Clone
```bash
# 1. Haz fork del repositorio en GitHub
#    (Botón "Fork" en la parte superior derecha de la página del repo)

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

## 💡 Estándares de Código

### 🐍 Python
- **Sigue PEP 8**: Usa 4 espacios para indentación, líneas de máximo 88 caracteres.
- **Nombres descriptivos**: Usa `snake_case` para variables/funciones y `PascalCase` para clases.
- **Tipado**: Usa type hints cuando sea posible.
- **Documentación**: Añade docstrings a funciones y clases.

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
- **Evita librerías pesadas**: El ESP32 tiene memoria limitada.
- **Manejo de errores**: Usa `try-except` para operaciones críticas (Bluetooth, I2C).
- **Optimiza el uso de memoria**: Libera recursos cuando no se usen.

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

### 📖 Kivy (App Móvil)
- **Sigue el patrón MVVM**: Separa la lógica de negocio de la interfaz.
- **Usa .kv files**: Para diseños complejos, usa archivos `.kv` en lugar de Python puro.
- **Optimiza el rendimiento**: Evita actualizaciones innecesarias de la UI.

---

## 📥 Enviando Cambios

### 1️⃣ Haz commit de tus cambios
```bash
# Añade solo los archivos relevantes
git add src/mobile/chat_engine.py

# Escribe un mensaje de commit claro
git commit -m "feat: añadir motor de voz TTS para Félix"
```

**Reglas para mensajes de commit:**
- Usa el prefijo `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, etc. (según [Conventional Commits](https://www.conventionalcommits.org/)).
- Mantén el mensaje en **máximo 50 caracteres** (primera línea).
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
   - **Título**: Claro y descriptivo (ej: "feat: añadir TTS para voz de Félix").
   - **Descripción**: Explica **qué** hiciste y **por qué**. Incluye capturas de pantalla si es relevante.
   - **Issues relacionadas**: Usa `Closes #123` o `Fixes #456` para cerrar issues automáticamente.

---

## 📢 Reportando Problemas

Si encuentras un **bug**, abre un **Issue** en GitHub:

1. Ve a [Issues](https://github.com/luciano2-web/Luciano-Sarmiento/issues).
2. Haz clic en **"New Issue"**.
3. Usa la plantilla **"Bug Report"** y completa:
   - **Título**: Descripción corta del problema.
   - **Descripción**: Explica el problema en detalle.
   - **Pasos para reproducir**: Cómo podemos replicar el error.
   - **Comportamiento esperado**: Qué debería pasar.
   - **Comportamiento actual**: Qué pasa realmente.
   - **Entorno**: Versión de Python, SO, hardware, etc.
   - **Capturas de pantalla/Logs**: Si aplica.

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

## 💋 Solicitando Funciones

Si tienes una **idea para mejorar Félix**, abre un **Issue** con la plantilla **"Feature Request"**:

1. Ve a [Issues](https://github.com/luciano2-web/Luciano-Sarmiento/issues).
2. Haz clic en **"New Issue"**.
3. Usa la plantilla **"Feature Request"** y completa:
   - **Título**: Nombre de la funcionalidad.
   - **Descripción**: Explica qué hace la funcionalidad y por qué es útil.
   - **Problema que resuelve**: Qué problema actual soluciona.
   - **Posible implementación**: Ideas técnicas (opcional).

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

## 👌 Código de Conducta

Este proyecto sigue el **[Código de Conducta del Contribuidor](CODE_OF_CONDUCT.md)**, basado en el [Contributor Covenant](https://www.contributor-covenant.org/).

**Reglas clave:**
- **Sé inclusivo**: No toleramos discriminación por género, raza, religión, orientación sexual, etc.
- **Sé respetuoso**: Critica las ideas, no a las personas.
- **Sé responsable**: No compartas información personal sin consentimiento.
- **Sé colaborativo**: Ayuda a otros y acepta ayuda.

**⚠️ Si ves un comportamiento inapropiado, repórtalo a [luciano2-web](https://github.com/luciano2-web).**

---

## 🏖 Reconocimiento

Todos los colaboradores serán reconocidos en:
- El archivo **[CONTRIBUTORS.md](CONTRIBUTORS.md)**.
- La sección de **🏖 Top Contribuidores** en el README.md.
- **Badges** en sus perfiles de GitHub (ej: *Félix Contributor*).

**Niveles de reconocimiento:**
| Nivel | Requisitos | Badge |
|-------|------------|-------|
| **Bronce** | 1-5 contribuciones | 🧶 |
| **Plata** | 6-15 contribuciones | 🧸 |
| **Oro** | 16+ contribuciones | 🏆 |
| **Leyenda** | Contribuciones excepcionales | 👑 |

---

## 🐧 Issues para Principiantes

Si eres nuevo en el proyecto, te recomendamos empezar con issues etiquetados como:
- [`good first issue`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/good%20first%20issue): Problemas simples y bien definidos.
- [`documentation`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/documentation): Mejorar guías o traducciones.
- [`enhancement`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/enhancement): Mejoras menores.

**Ejemplos de "good first issues":**
- Añadir más emojis de gato a las respuestas de Félix.
- Traducir la documentación al inglés.
- Crear un diagrama de flujo para el hardware.
- Añadir un comando `@joke` para que Félix cuente chistes.

---

## 🐈 ¿Necesitas ayuda?

- **¿Preguntas sobre el código?** Abre un [Issue](https://github.com/luciano2-web/Luciano-Sarmiento/issues) con la etiqueta `question`.
- **¿Quieres chatear?** ¡Únete a nuestro [Discord](https://discord.gg/felix-gatogpt) (próximamente)!
- **¿Encontraste un bug?** Sigue las instrucciones en [Reportando Problemas](#-reportando-problemas).
- **¿Tienes una idea?** Sigue las instrucciones en [Solicitando Funciones](#-solicitando-funciones).

---

**🐱 ¡Gracias por ser parte de la comunidad de Félix!**

*Félix te espera... Ronronea... 🐾*
