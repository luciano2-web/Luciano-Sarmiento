# Instalación y primera prueba de Félix

Esta guía corresponde a la app modular de `src/mobile`. El proyecto sigue en desarrollo: abrir la interfaz o pasar pruebas de software no demuestra que la IA, una APK o el robot físico funcionen de extremo a extremo.

## Elige qué quieres probar

| Objetivo | Ruta | Qué comprueba |
|---|---|---|
| Explorar desde una tablet o teléfono | [Simulador web](https://felix-gatogpt-simulador.lucian15.chatgpt.site) | Circuito virtual, gestos y conversación con el modelo elegido |
| Probar sin descargar modelos | Consola con Python, pasos 1–3 | Arranque, ayuda e historial |
| Abrir la interfaz de escritorio | Paso 4 | Interfaz Kivy, sujeta al entorno gráfico |
| Experimentar con IA local | Paso 5 | Requiere dependencias y recursos compatibles |
| Conectar una placa | [Guía BLE](../BLE_CONNECTION.md) | Integración experimental; prueba física pendiente |
| Crear una APK | Apartado Android | Compilación todavía no verificada |

## 1. Obtener el código

En [el repositorio](https://github.com/luciano2-web/Luciano-Sarmiento), selecciona **Code → Download ZIP**, descomprime el archivo y abre una terminal en la carpeta extraída.

La **raíz del proyecto** es la carpeta que contiene `README.md`, `src` y `tests`. Si descargaste el ZIP, normalmente se llama `Luciano-Sarmiento-main`. Todos los comandos siguientes parten de esa carpeta, salvo donde se indique otra cosa.

Usa Python 3.11 como referencia: es la versión configurada en las pruebas de GitHub Actions. No se garantiza compatibilidad de todas las dependencias con versiones posteriores.

## 2. Instalación en computadora: elige tu sistema

Los tres sistemas tienen instrucciones propias. Sigue solo la sección de tu computadora y después continúa con el paso 3. No instales todavía las dependencias de IA.

### Windows

1. Necesitas Python 3.11 instalado. Abre **PowerShell** en la carpeta extraída del proyecto (la que contiene `README.md` y `src`).
2. Comprueba Python y crea el entorno:

```powershell
py -3.11 --version
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

3. Desde esa misma carpeta, inicia la prueba de consola:

```powershell
python -m src.mobile.main
```

Si PowerShell bloquea la activación, no necesitas cambiar su política. Ejecuta directamente:

```powershell
.\.venv\Scripts\python.exe -m src.mobile.main
```

En ese caso, sustituye también `python` por `.\.venv\Scripts\python.exe` en los pasos posteriores. Si `py` no existe, comprueba tu instalación de Python; puedes usar `python -m venv .venv` cuando `python --version` muestre 3.11.

**Alternativa con CMD:** activa el entorno con `.venv\Scripts\activate.bat` en lugar del comando de PowerShell.

### Linux

1. Necesitas Python 3.11 y su componente `venv`. Abre una **terminal** dentro de la carpeta extraída del proyecto.
2. Comprueba Python y crea el entorno:

```bash
python3.11 --version
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

3. Desde esa misma carpeta, inicia la prueba de consola:

```bash
python -m src.mobile.main
```

Si no existe `python3.11`, comprueba `python3 --version`: puedes sustituir el comando por `python3` si corresponde a Python 3.11. En caso contrario, prepara esa versión para tu distribución antes de continuar.

Si la creación del entorno falla por falta de `venv` o `ensurepip`, instala el componente de entornos virtuales correspondiente a tu versión de Python mediante el gestor de paquetes de tu distribución. No hay un único comando de instalación del sistema que sirva para todas las distribuciones Linux.

### macOS (computadoras Mac)

1. Necesitas Python 3.11 instalado. Abre la aplicación **Terminal** y entra en la carpeta extraída del proyecto.
2. Comprueba Python y crea el entorno:

```bash
python3.11 --version
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

3. Desde esa misma carpeta, inicia la prueba de consola:

```bash
python -m src.mobile.main
```

Si no existe `python3.11`, comprueba `python3 --version`: puedes sustituir el comando por `python3` si corresponde a Python 3.11. Si no, instala esa versión antes de continuar. No uses comandos de PowerShell ni rutas `Scripts\` en Terminal.

Estas instrucciones describen la preparación del entorno en Mac; no certifican compatibilidad de las dependencias de IA con todos los Mac Intel o Apple Silicon.

**Para los tres sistemas:** mantén la terminal en la raíz del proyecto. Si la cierras, vuelve a esa carpeta y activa otra vez el entorno antes de usar los comandos de los pasos siguientes.

## 3. Primera prueba sin modelos

Desde la raíz, con el entorno nuevo y sin paquetes externos:

```bash
python -m src.mobile.main
```

Al no haber Kivy, el programa informa de su ausencia y abre la consola. Prueba, en este orden:

```text
@help
Hola Félix
clear
quit
```

Resultados esperados:

- `@help` muestra los comandos.
- `Hola Félix` usa una respuesta preprogramada al no disponer del motor de IA. El mensaje de error al cargar el modelo es esperable en esta prueba: **no es una conversación generada por un modelo**.
- `clear` borra el historial guardado de esta interfaz.
- `quit` termina la consola.

No uses `@gatimage` en esta prueba mínima: requiere dependencias adicionales.

Para comprobar arranque, persistencia y comunicación simulada, sin descargar modelos:

```bash
python -m unittest tests.test_mobile_startup tests.test_chat_history tests.test_device_link -v
```

Es el comando del workflow `mobile-device-tests.yml`. Usa dobles de prueba; no valida una ventana real, una radio Bluetooth ni inferencia de IA.

## 4. Interfaz gráfica de escritorio

Con el mismo entorno activo:

```bash
python -m pip install "Kivy==2.2.1"
python -m src.mobile.main
```

Se necesita una sesión gráfica compatible. No ejecutes el módulo después de entrar en `src/mobile`: sus importaciones parten de la raíz.

Prueba primero el botón de ayuda y los botones de caricias. Estos últimos simulan gestos localmente; no demuestran una conexión al robot. Instalar Kivy por sí solo no instala los modelos de IA.

## 5. IA local: ruta experimental

El conjunto de dependencias existente se instala con:

```bash
python -m pip install -r src/mobile/requirements_mobile.txt
python -m pip check
python -m src.mobile.main
```

Este archivo fija versiones de Torch, Transformers, BitsAndBytes y Diffusers, entre otras. No es una instalación completa validada en todos los sistemas; puede fallar por disponibilidad de paquetes o incompatibilidad entre dependencias. `pip check` comprueba requisitos declarados, no que el modelo pueda cargarse.

El modelo de chat se intenta cargar al enviar el primer mensaje normal. El motor de imágenes se crea al usar `@gatimage`. La primera carga puede necesitar Internet y espacio para los modelos; no hay un tiempo de descarga ni una cantidad de RAM garantizados.

La fuente de configuración efectiva es [src/core/constants.py](../../src/core/constants.py):

- Chat: `CHAT_MODEL_ID = LIGHTWEIGHT_CHAT_MODEL`, actualmente TinyLlama.
- Imágenes: `IMAGE_MODEL_ID = DEFAULT_IMAGE_MODEL`, actualmente SSD-1B.
- El motor de chat intenta cuantización INT8 con BitsAndBytes; que exista un valor `DEVICE = "cpu"` no garantiza que esa ruta sea compatible con el equipo.
- `felix_mobile_config.yaml` existe, pero la entrada modular y estos motores no lo cargan. Editarlo no cambia por sí solo su comportamiento.

Si la carga falla, el chat devuelve respuestas preprogramadas. El motor de imágenes puede intentar crear una imagen de sustitución. Ninguno de esos resultados demuestra que la inferencia esté funcionando.

## Archivos que guarda la app

| Datos | Ubicación usada por la implementación |
|---|---|
| Caché de modelos | `src/mobile/felix_models/` |
| Imágenes | `src/mobile/felix_outputs/images/` |
| Historial de consola | `~/.local/share/felix/chat_history.json`, o `$XDG_DATA_HOME/felix/chat_history.json` si se define esa variable |
| Historial de Kivy | `chat_history.json` dentro de `App.user_data_dir` |

Consola y Kivy pueden usar historiales distintos. Cada uno conserva hasta 200 turnos; el motor usa los últimos cuatro como contexto. El comando `clear` elimina el historial de la interfaz actual, no la caché de modelos.

## Android e iOS

### Hablar con Félix en el simulador

Abre el [simulador web de Félix](https://felix-gatogpt-simulador.lucian15.chatgpt.site) y elige un modelo de conversación.

- **Qwen en Android.** En [MNN Chat](https://github.com/alibaba/MNN/tree/master/apps/Android/MnnLlmChat), descarga y selecciona [Qwen3‑1.7B‑MNN](https://huggingface.co/taobao-mnn/Qwen3-1.7B-MNN). Activa el servicio API de la app. En el simulador, selecciona Qwen y comprueba que el puerto de `127.0.0.1` coincide con el que indica MNN Chat. Pulsa **Usar modelo** y envía un mensaje desde la misma tableta. La conexión requiere que el navegador y el servicio permitan la solicitud local. La prueba en una Redmi Pad SE física sigue pendiente.
- **API personalizada.** Introduce la dirección base, el identificador del modelo y la clave si el proveedor la exige. Al enviar, el navegador comparte los turnos recientes con esa dirección. El servicio debe admitir Chat Completions y permitir solicitudes desde el sitio. Introduce la clave solo en el campo del simulador.
- **TinyLlama en el navegador.** Selecciona TinyLlama y pulsa **Cargar TinyLlama**. La primera descarga ocupa unos 910 MB.

Para probar la conversación, pregunta «Félix, ¿qué pasa si toco dos veces tu sensor?» y compara su respuesta con lo que ves en la OLED virtual.

**Termux:** no hay una instalación completa validada del conjunto Kivy/Torch/BitsAndBytes del proyecto. No se ofrece `pip install -r ...` como una receta garantizada para Android.

**APK con Buildozer:** existe [buildozer.spec](../../src/mobile/buildozer.spec), pero la compilación y la ejecución en dispositivo están pendientes de validación. Para colaboradores que ya tengan un entorno Buildozer configurado, el punto de entrada es:

```bash
cd src/mobile
buildozer android debug
```

Si la compilación termina correctamente, revisa la salida de Buildozer y el directorio `bin/`. Las dependencias de IA pueden requerir recetas o un backend móvil distinto. No se promete un APK funcional, un plazo de compilación ni soporte en cualquier teléfono.

**iOS:** no hay un procedimiento de instalación validado en este repositorio. Pythonista y a-Shell no se presentan como sustitutos de una compilación de la app.

## Bluetooth opcional

Para el cliente BLE de escritorio, la [guía de conexión](../BLE_CONNECTION.md) indica:

```bash
python -m pip install "bleak==3.0.1"
```

La app usa BLE Nordic UART Service, no un HC-05/SPP. Consulta esa guía para firmware, dirección de la placa, permisos y limitaciones. Las pruebas automáticas usan una radio simulada; la validación física sigue pendiente.

## Problemas frecuentes

| Síntoma | Qué revisar |
|---|---|
| `No module named src` | Vuelve a la carpeta que contiene `src` y ejecuta `python -m src.mobile.main` |
| `No module named kivy` | Para la interfaz instala Kivy dentro del entorno activo; la prueba mínima usa consola |
| `No matching distribution` | Copia el nombre del paquete, versión de Python y sistema; no asumas que la lista de escritorio es compatible con Android |
| Error de BitsAndBytes, CUDA o memoria | La ruta de IA no está validada en ese equipo; distingue el fallback de una respuesta generada |
| La ventana no abre | Revisa la salida de Kivy y la disponibilidad del entorno gráfico; la consola no prueba que la GUI funcione |
| Aviso al guardar historial | Revisa la ruta y permisos; conserva una copia antes de modificar el archivo |
| No conecta la placa | Comprueba BLE/NUS, dirección, permisos y firmware siguiendo la guía BLE |

Para reportar un fallo, incluye sistema operativo, `python --version`, comando exacto, carpeta desde la que lo ejecutaste y error completo. Indica si probaste consola, interfaz, modelo o hardware.

## Alcance de esta guía

Los comandos y rutas se contrastaron con el código y los workflows del repositorio. Esta revisión documental no certifica una instalación nueva en Windows, macOS, Linux, Android o iOS, ni una compilación APK o prueba física.

[Volver al README](../../README.md)
