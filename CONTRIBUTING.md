# \ud83e\udd1d C\u00f3mo contribuir a F\u00e9lix / GatoGPT

**\ud83d\udc31 \u00a1Gracias por tu inter\u00e9s en ayudar a que F\u00e9lix sea mejor!**

Este proyecto es **open source** y crece gracias a colaboradores como t\u00fa. A continuaci\u00f3n te explicamos c\u00f3mo puedes contribuir de manera efectiva.

---

## \ud83d\udcc1 \u00c9ndice
1. [Reglas Generales](#-reglas-generales)
2. [\u00c1reas de Contribuci\u00f3n](#-\u00e1reas-de-contribuci\u00f3n)
3. [Primeros Pasos](#-primeros-pasos)
4. [Est\u00e1ndares de C\u00f3digo](#-est\u00e1ndares-de-c\u00f3digo)
5. [Enviando Cambios](#-enviando-cambios)
6. [Reportando Problemas](#-reportando-problemas)
7. [Solicitando Funciones](#-solicitando-funciones)
8. [C\u00f3digo de Conducta](#-c\u00f3digo-de-conducta)
9. [Reconocimiento](#-reconocimiento)

---

## \ud83d\udcd3 Reglas Generales

### \u2705 Qu\u00e9 se espera de ti:
- **S\u00e9 amable y respetuoso** con todos los miembros de la comunidad.
- **Sigue el [C\u00f3digo de Conducta](CODE_OF_CONDUCT.md)**.
- **Documenta tus cambios**: A\u00f1ade comentarios en el c\u00f3digo y actualiza la documentaci\u00f3n si es necesario.
- **Prueba tus cambios**: Aseg\u00farate de que el c\u00f3digo funcione antes de enviar un Pull Request.
- **Usa ramas descriptivas**: Ej: `feat/tts-voice`, `fix/bluetooth-bug`, `docs/hardware-guide`.

### \u274c Qu\u00e9 NO hacer:
- **No env\u00edes c\u00f3digo sin probar**.
- **No ignores los tests existentes** (si los hay).
- **No modifiques el sistema de personalidad de F\u00e9lix** (`personality.py`) sin consultar primero. Este es el **coraz\u00f3n** del proyecto y debe mantenerse consistente en todas las versiones.
- **No incluidas informaci\u00f3n personal o sensible** en el repositorio.
- **No uses el nombre del proyecto para fines comerciales** sin permiso.

---

## \ud83d\udc1f \u00c1reas de Contribuci\u00f3n

F\u00e9lix es un proyecto **multidisciplinario**. Puedes ayudar en varias \u00e1reas:

| \u00c1rea | Descripci\u00f3n | Dificultad | Habilidades Requeridas | Etiqueta en Issues |
|----------|-------------|------------|----------------------|-------------------|
| **Hardware** | Mejorar esquem\u00e1ticos, a\u00f1adir sensores, optimizar conexiones | Media/Alta | Electr\u00f3nica, ESP32, Fritzing | `hardware` |
| **Firmware** | Optimizar c\u00f3digo MicroPython, a\u00f1adir funcionalidades al ESP32 | Alta | MicroPython, C/C++, ESP-IDF | `firmware` |
| **App M\u00f3vil** | Mejorar UI/UX, a\u00f1adir funciones, optimizar rendimiento | Media | Kivy, Python, Android | `mobile` |
| **IA / Modelos** | Fine-tunear el modelo de F\u00e9lix, mejorar prompts, optimizar inferencia | Alta | PyTorch, Transformers, ONNX | `ai` |
| **Voz (TTS/STT)** | Integrar motores de voz, mejorar reconocimiento | Media | Python, librer\u00edas de audio | `voice` |
| **Documentaci\u00f3n** | Traducir, mejorar gu\u00edas, crear tutoriales | Baja | Markdown, GitHub | `documentation` |
| **Testing** | A\u00f1adir tests unitarios/integracion, reportar bugs | Media | pytest, unittest | `testing` |
| **Comunidad** | Moderar Discord, ayudar en issues, crear contenido | Baja | Comunicaci\u00f3n, paciencia | `community` |
| **Dise\u00f1o 3D** | Crear casos imprimibles en 3D para el hardware | Media | Blender, Tinkercad, Fusion 360 | `3d-design` |

---

## \ud83d\ude80 Primeros Pasos

### 1\ufe0f\u20e3 Fork y Clone
```bash
# 1. Haz fork del repositorio en GitHub
#    (Bot\u00f3n "Fork" en la parte superior derecha de la p\u00e1gina del repo)

# 2. Clona tu fork localmente
git clone https://github.com/tu-usuario/Luciano-Sarmiento.git
cd Luciano-Sarmiento

# 3. A\u00f1ade el upstream (repositorio original)
git remote add upstream https://github.com/luciano2-web/Luciano-Sarmiento.git
```

### 2\ufe0f\u20e3 Configura el entorno
#### Para desarrollo en **App M\u00f3vil** (Android/iOS/PC):
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

### 3\ufe0f\u20e3 Crea una rama
```bash
# Actualiza tu fork
git fetch upstream
git merge upstream/main

# Crea una nueva rama para tu contribuci\u00f3n
git checkout -b tipo/descripcion  # Ej: feat/tts-voice, fix/bluetooth-bug
```

---

## \ud83d\udca1 Est\u00e1ndares de C\u00f3digo

### \ud83d\udc80 Python
- **Sigue PEP 8**: Usa 4 espacios para indentaci\u00f3n, l\u00edneas de m\u00e1ximo 88 caracteres.
- **Nombres descriptivos**: Usa `snake_case` para variables/funciones y `PascalCase` para clases.
- **Tipado**: Usa type hints cuando sea posible.
- **Documentaci\u00f3n**: A\u00f1ade docstrings a funciones y clases.

**Ejemplo:**
```python
from typing import Optional

def generate_felix_response(prompt: str, max_length: int = 100) -> Optional[str]:
    """
    Genera una respuesta de F\u00e9lix usando el modelo de IA.
    
    Args:
        prompt: El texto de entrada del usuario.
        max_length: Longitud m\u00e1xima de la respuesta.
    
    Returns:
        La respuesta generada o None si hay un error.
    """
    # ... implementaci\u00f3n ...
    pass
```

### \ud83d\udc81 MicroPython (ESP32)
- **Evita librer\u00edas pesadas**: El ESP32 tiene memoria limitada.
- **Manejo de errores**: Usa `try-except` para operaciones cr\u00edticas (Bluetooth, I2C).
- **Optimiza el uso de memoria**: Libera recursos cuando no se usen.

**Ejemplo:**
```python
from machine import I2C, Pin
import time

def read_inmp441(i2c: I2C, address: int = 0x34) -> bytes:
    """Lee datos del micr\u00f3fono INMP441."""
    try:
        # ... implementaci\u00f3n ...
        pass
    except OSError as e:
        print(f"Error al leer INMP441: {e}")
        return b''
```

### \ud83d\udcd4 Kivy (App M\u00f3vil)
- **Sigue el patron MVVM**: Separa la l\u00f3gica de negocio de la interfaz.
- **Usa .kv files**: Para dise\u00f1os complejos, usa archivos `.kv` en lugar de Python puro.
- **Optimiza el rendimiento**: Evita actualizaciones innecesarias de la UI.

---

## \ud83d\udce5 Enviando Cambios

### 1\ufe0f\u20e3 Haz commit de tus cambios
```bash
# A\u00f1ade solo los archivos relevantes
git add src/mobile/chat_engine.py

# Escribe un mensaje de commit claro
git commit -m "feat: a\u00f1adir motor de voz TTS para F\u00e9lix"
```

**Reglas para mensajes de commit:**
- Usa el prefijo `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, etc. (seg\u00fan [Conventional Commits](https://www.conventionalcommits.org/)).
- Mant\u00en el mensaje en **m\u00e1ximo 50 caracteres** (primera l\u00ednea).
- Si es necesario, a\u00f1ade una descripci\u00f3n extendida.

**Ejemplos:**
```bash
git commit -m "feat: a\u00f1adir comando @help para listar comandos"
git commit -m "fix: corregir bug en comunicaci\u00f3n Bluetooth"
git commit -m "docs: actualizar gu\u00eda de hardware"
git commit -m "refactor: modularizar chat_engine.py"
```

### 2\ufe0f\u20e3 Sincroniza con el upstream
```bash
# Aseg\u00farate de que tu rama est\u00e1 actualizada
git fetch upstream
git rebase upstream/main
```

### 3\ufe0f\u20e3 Env\u00eda tu Pull Request (PR)
```bash
# Sube tu rama a tu fork
git push origin tipo/descripcion
```

Luego:
1. Ve a [https://github.com/luciano2-web/Luciano-Sarmiento](https://github.com/luciano2-web/Luciano-Sarmiento).
2. Haz clic en **"Pull Requests"** > **"New Pull Request"**.
3. Selecciona tu rama y describe:
   - **T\u00edtulo**: Clear y descriptivo (ej: "feat: a\u00f1adir TTS para voz de F\u00e9lix").
   - **Descripci\u00f3n**: Explica **qu\u00e9** hiciste y **por qu\u00e9**. Incluye capturas de pantalla si es relevante.
   - **Issues relacionadas**: Usa `Closes #123` o `Fixes #456` para cerrar issues autom\u00e1ticamente.

---

## \ud83d\udce2 Reportando Problemas

Si encuentras un **bug**, abre un **Issue** en GitHub:

1. Ve a [Issues](https://github.com/luciano2-web/Luciano-Sarmiento/issues).
2. Haz clic en **"New Issue"**.
3. Usa la plantilla **"Bug Report"** y completa:
   - **T\u00edtulo**: Descripci\u00f3n corta del problema.
   - **Descripci\u00f3n**: Explica el problema en detalle.
   - **Pasos para reproducir**: C\u00f3mo podemos replicar el error.
   - **Comportamiento esperado**: Qu\u00e9 deber\u00eda pasar.
   - **Comportamiento actual**: Qu\u00e9 pasa realmente.
   - **Entorno**: Versi\u00f3n de Python, SO, hardware, etc.
   - **Capturas de pantalla/Logs**: Si aplica.

**Ejemplo de un buen reporte de bug:**
```
T\u00edtulo: Error al conectar ESP32 con app m\u00f3vil via Bluetooth

Descripci\u00f3n:
La app m\u00f3vil se congela al intentar conectarse al ESP32 despu\u00e9s de 3 intentos fallidos.

Pasos para reproducir:
1. Encender el ESP32 con el firmware de F\u00e9lix.
2. Abrir la app m\u00f3vil.
3. Intentar conectar via Bluetooth.
4. Despu\u00e9s de 3 intentos fallidos, la app se congela.

Comportamiento esperado:
La app deber\u00eda mostrar un mensaje de error y permitir reintentar.

Comportamiento actual:
La app se congela y no responde.

Entorno:
- Android 13
- ESP32-WROOM-32
- App vers\u00f3n: 1.0.0
- Logs: [adjuntar logs]
```

---

## \ud83d\udc8b Solicitando Funciones

Si tienes una **idea para mejorar F\u00e9lix**, abre un **Issue** con la plantilla **"Feature Request"**:

1. Ve a [Issues](https://github.com/luciano2-web/Luciano-Sarmiento/issues).
2. Haz clic en **"New Issue"**.
3. Usa la plantilla **"Feature Request"** y completa:
   - **T\u00edtulo**: Nombre de la funcionalidad.
   - **Descripci\u00f3n**: Explica qu\u00e9 hace la funcionalidad y por qu\u00e9 es \u00fatil.
   - **Problema que resuelve**: Qu\u00e9 problema actual soluciona.
   - **Posible implementaci\u00f3n**: Ideas t\u00e9cnicas (opcional).

**Ejemplo de una buena solicitud de funcionalidad:**
```
T\u00edtulo: A\u00f1adir comando @gatmusic para generar m\u00fasica

Descripci\u00f3n:
Ser\u00eda genial si F\u00e9lix pudiera generar m\u00fasica de fondo usando IA, similar a @gatimage.

Problema que resuelve:
Actualmente, F\u00e9lix solo puede generar im\u00e1genes. A\u00f1adir m\u00fasica expandir\u00eda sus capacidades creativas.

Posible implementaci\u00f3n:
- Usar un modelo ligero como Riffusion o Stable Audio.
- Integrar con el sistema de comandos existente.
- Guardar los archivos generados en felix_outputs/music/.
```

---

## \ud83d\udc4c C\u00f3digo de Conducta

Este proyecto sigue el **[C\u00f3digo de Conducta del Contribuidor](CODE_OF_CONDUCT.md)**, basado en el [Contributor Covenant](https://www.contributor-covenant.org/).

**Reglas clave:**
- **S\u00e9 inclusivo**: No toleramos discriminaci\u00f3n por g\u00e9nero, raza, religi\u00f3n, orientaci\u00f3n sexual, etc.
- **S\u00e9 respetuoso**: Critica las ideas, no a las personas.
- **S\u00e9 responsable**: No compartas informaci\u00f3n personal sin consentimiento.
- **S\u00e9 colaborativo**: Ayuda a otros y acepta ayuda.

**\u26a0\ufe0f Si ves un comportamiento inapropiado, rep\u00f3rtalo a [luciano2-web](https://github.com/luciano2-web).**

---

## \ud83c\udf96 Reconocimiento

Todos los colaboradores ser\u00e1n reconocidos en:
- El archivo **[CONTRIBUTORS.md](CONTRIBUTORS.md)**.
- La secci\u00f3n de **\ud83c\udf96 Top Contribuidores** en el README.md.
- **Badges** en sus perfiles de GitHub (ej: *F\u00e9lix Contributor*).

**Niveles de reconocimiento:**
| Nivel | Requisitos | Badge |
|-------|------------|-------|
| **Bronce** | 1-5 contribuciones | \ud83e\uddf6 |
| **Plata** | 6-15 contribuciones | \ud83e\uddf8 |
| **Oro** | 16+ contribuciones | \ud83e\uddf7 |
| **Leyenda** | Contribuciones excepcionales | \ud83d\udc51 |

---

## \ud83d\udc87 Issues para Principiantes

Si eres nuevo en el proyecto, te recomendamos empezar con issues etiquetados como:
- [`good first issue`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/good%20first%20issue): Problemas simples y bien definidos.
- [`documentation`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/documentation): Mejorar gu\u00edas o traducciones.
- [`enhancement`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/enhancement): Mejoras menores.

**Ejemplos de "good first issues":**
- A\u00f1adir m\u00e1s emojis de gato a las respuestas de F\u00e9lix.
- Traducir la documentaci\u00f3n al ingl\u00e9s.
- Crear un diagrama de flujo para el hardware.
- A\u00f1adir un comando `@joke` para que F\u00e9lix cuente chistes.

---

## \ud83d\udc00 \u00bfNecesitas ayuda?

- **\u00bfPreguntas sobre el c\u00f3digo?** Abre un [Issue](https://github.com/luciano2-web/Luciano-Sarmiento/issues) con la etiqueta `question`.
- **\u00bfQuieres chatear?** \u00a1\u00d1nete a nuestro [Discord](https://discord.gg/felix-gatogpt) (pr\u00f3ximamente)!
- **\u00bfEncontraste un bug?** Sigue las instrucciones en [Reportando Problemas](#-reportando-problemas).
- **\u00bfTienes una idea?** Sigue las instrucciones en [Solicitando Funciones](#-solicitando-funciones).

---

**\ud83d\udc31 \u00a1Gracias por ser parte de la comunidad de F\u00e9lix!**

*F\u00e9lix te espera... Ronronea... \ud83d\udc3e*
