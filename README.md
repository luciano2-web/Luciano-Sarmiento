# <div align="center">🐱 Félix / GatoGPT</div>

<div align="center">

**🤖 Proyecto open-source de robot gato: IA conversacional, personalidad programada y hardware basado en ESP32**

[![License](https://img.shields.io/badge/License-Apache%202.0-1A237E?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-A7D8FF?style=for-the-badge&logo=python)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2.2%2B-39FFB6?style=for-the-badge&logo=kivy)](https://kivy.org/)
[![ESP32](https://img.shields.io/badge/ESP32-WROOM--32-1A237E?style=for-the-badge)](https://www.espressif.com/)

[![Stars](https://img.shields.io/github/stars/luciano2-web/Luciano-Sarmiento?style=social)](https://github.com/luciano2-web/Luciano-Sarmiento/stargazers)
[![Forks](https://img.shields.io/github/forks/luciano2-web/Luciano-Sarmiento?style=social)](https://github.com/luciano2-web/Luciano-Sarmiento/network/members)
[![Issues](https://img.shields.io/github/issues/luciano2-web/Luciano-Sarmiento)](https://github.com/luciano2-web/Luciano-Sarmiento/issues)

</div>

---

<div align="center">
  <img src="assets/felix_concept.jpg" alt="Félix / GatoGPT - Robot gato con IA" width="600" style="border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
</div>

---

## ✨ Visión general

Félix / GatoGPT es un proyecto open-source en desarrollo que explora la integración de inteligencia artificial, software móvil y hardware basado en ESP32 en un robot con forma de gato. El objetivo es construir un prototipo físico capaz de interactuar mediante conversación y respuestas programadas.

Este proyecto busca explorar una idea simple pero fascinante:

La personalidad de Félix es una capa de comportamiento diseñada mediante software. Las expresiones y reacciones del proyecto son respuestas programadas; no implican conciencia, emociones ni experiencias subjetivas.

---

## 🧠 Características principales

- Motor de conversación con IA en desarrollo; la experiencia completa de extremo a extremo aún está pendiente de integración y validación.
- Personalidad felina y estilo propio
- Interfaz móvil con Kivy
- Módulos de audio/voz en desarrollo; conversación de extremo a extremo pendiente
- Módulos de firmware ESP32 en desarrollo; integración física completa pendiente
- Simulador web para probar sin hardware
- Arquitectura abierta y extensible
- Diseño pensado para proyectos maker e investigación creativa

---

## 🔎 Estado técnico transparente

Esta tabla distingue el código que ya existe de las funciones que todavía no están completas. **Que un módulo esté en el repositorio no significa que esté validado en el robot físico.**

| Área | Estado | Qué se puede afirmar hoy |
|---|---|---|
| App móvil Kivy | <strong>Implementado parcialmente</strong> | Hay estructura y módulos de aplicación; falta demostrar el flujo completo con el robot. |
| Firmware de pantalla/audio/comunicación | <strong>Implementado parcialmente</strong> | Hay módulos separados; falta integrarlos y probarlos juntos en una placa concreta. |
| Simulador web | <strong>Disponible</strong> | Permite explorar una representación de Félix; no equivale a hardware real. |
| Sensor táctil | <strong>Prototipo de software</strong> | El módulo y sus pruebas de lógica están incorporados tras el PR #40; aún falta integración con el flujo principal y validación física. |
| Servos y movimiento | <strong>Planeado</strong> | Los modelos, alimentación, conexiones y control todavía deben definirse. |
| Cámara y visión | <strong>Planeado</strong> | Primero se debe seleccionar una placa y cámara compatibles; no hay captura integrada. |
| Comunicación móvil ↔ ESP32 sin nube | <strong>En desarrollo de diseño</strong> | El protocolo, la reconexión y el modo local siguen pendientes. |
| Proveedores en la app | <strong>Planeado</strong> | El directorio y sus filtros todavía deben construirse. |
| Prototipo físico | <strong>Planeado para 2027</strong> | La construcción espera a disponer de materiales y revisar el diseño. |

**Regla de publicación:** cada PR debe indicar si lo mostrado es código, simulación o una prueba realizada en hardware real. No se anunciará una función como terminada hasta que sus criterios de aceptación se hayan comprobado.

---

## 🏗️ Arquitectura del sistema

```mermaid
flowchart TD
    subgraph Hardware["💻 Hardware (ESP32)"]
        A[ESP32 DevKit] --> B[OLED 0.96" I2C]
        A --> C[Micrófono INMP441 I2S]
        A --> D[Parlante 3W]
        A --> E[Power Bank]
    end
    
    subgraph Mobile["📱 App móvil"]
        F[Kivy UI] --> G[Chat Engine]
        G --> H[Modelos de IA]
        F --> I[Audio Handler]
        F --> J[Bluetooth Bridge]
    end
    
    subgraph Cloud["☁️ Opcional: Nube"]
        K[(Hugging Face)] --> H
    end
    
    J <-->|UART: integración pendiente; Bluetooth no validado| A
    H -->|Respuestas| F
    I -->|Voz| D
    C -->|Audio| A
    
    style Hardware fill:#1A237E,stroke:#fff,color:#fff
    style Mobile fill:#A7D8FF,stroke:#1A237E,color:#1A237E
    style Cloud fill:#39FFB6,stroke:#1A237E,color:#39FFB6
```

---

## 🧩 Componentes principales

### 💻 Componentes base (estimación, no presupuesto total)

| Componente | Modelo | Precio (USD) | Función |
|------------|--------|--------------|---------|
| **Microcontrolador** | ESP32-WROOM-32 | $8 - $12 | Cerebro del sistema |
| **Pantalla OLED** | SSD1306 0.96" I2C | $3 - $6 | Mostrar expresiones |
| **Micrófono** | INMP441 I2S | $2 - $4 | Capturar voz |
| **Parlante** | 4Ω 3W | $2 - $5 | Reproducir voz |
| **Protoboard** | 400 puntos | $5 - $10 | Montaje |
| **Power Bank** | 5V/2A | $10 - $20 | Alimentación |
| **Servos** | Modelo y alimentación por definir | Por definir | Movimiento de cabeza y cola (servo_head / servo_tail) |
| **Sensor táctil** | TouchPad capacitivo GPIO 32 (ESP32 clásico) | Incluido en el chip + electrodo | Detectar gestos táctiles (requiere validar placa y montaje) |
| **Cámara** | Placa ESP32-S3 con PSRAM + cámara compatible (por seleccionar) | Por definir | Capturar imágenes para visión; pendiente de integración |

**Nota sobre el tacto:** el módulo `src/firmware/touch_sensor.py`, incorporado mediante el PR #40, implementa la lógica para traducir un toque corto en `pet`, dos toques rápidos en `annoyed` y una pulsación larga en eventos de inicio/fin de pulsar-para-hablar. Sus pruebas de software no sustituyen una prueba en placa: todavía falta integrarlo al flujo principal y al audio de la app.

**Nota sobre la cámara:** no está lista para conectar al ESP32-WROOM-32 actual. La placa y el sensor deben seleccionarse antes de escribir el controlador. Consulta el [Issue #39](https://github.com/luciano2-web/Luciano-Sarmiento/issues/39).

**Nota sobre el presupuesto:** los precios son orientativos y pueden variar según proveedor y país. La suma no es un presupuesto cerrado ni garantiza un costo inferior a USD 50. No incluye servos (modelo, cantidad y alimentación pendientes), cámara, herramientas, envío ni posibles componentes adicionales.

**Nota sobre servos:** la convención documental del proyecto es `servo_head` para la cabeza y `servo_tail` para la cola. El firmware todavía no incluye un módulo de control de servos. Consulta la [lista de componentes](docs/hardware/components.md) antes de definir conexiones o pines.

→ [Ver lista completa de componentes](docs/hardware/components.md)

### ⚙️ Software

| Componente | Tecnología | Descripción |
|------------|-------------|-------------|
| **Firmware** | MicroPython | Control del hardware ESP32 |
| **App móvil** | Kivy + Python | Interfaz de usuario |
| **IA** | PyTorch + Transformers | Modelos de lenguaje |
| **Imágenes** | Diffusers | Generación visual |

---

## 🚀 Inicio rápido

### 1) Computadora local

```bash
# Clonar repositorio
git clone https://github.com/luciano2-web/Luciano-Sarmiento.git
cd Luciano-Sarmiento

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r src/mobile/requirements_mobile.txt

# Ejecutar la app
python src/mobile/main.py
```

### 2) Android (Termux)

```bash
# 1. Instalar Termux desde F-Droid
# 2. Dentro de Termux:
pkg update && pkg upgrade
pkg install python git
pip install -r src/mobile/requirements_mobile.txt

# Ejecutar
python src/mobile/main.py
```

### 3) Compilar APK para Android

```bash
# Instalar Buildozer
pip install buildozer cython

# Compilar
cd src/mobile
buildozer android debug

# Instalar el APK generado en la carpeta bin/
```

→ [Ver guía completa de configuración](docs/mobile/setup.md)

---

## 🧪 Comandos disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `@gatimage` | Generar imagen | `@gatimage un gato estudiando matemáticas` |
| `@gativeo` | Generar video (experimental) | `@gativeo un gato bailando` |
| `@help` | Mostrar ayuda | `@help` |
| `clear` | Limpiar el chat | `clear` |
| `quit` | Salir de la aplicación | `quit` |

---

## 🎨 Demo

### 🖼️ Imagen conceptual

![Concepto visual de Félix](assets/felix_concept.jpg)

> Esta imagen es una referencia conceptual, no una fotografía de un prototipo físico terminado.

### 🎥 Video de demostración física

El video real se añadirá cuando exista un prototipo físico construido y probado. No presentamos una simulación o un montaje como si fuera una demostración del robot real.

- [Issue #36: colaborar en el diseño y construcción del Félix físico](https://github.com/luciano2-web/Luciano-Sarmiento/issues/36)
- Las personas colaboradoras podrán aportar fotografías del proceso, una imagen final y un video corto mostrando sus funciones verificadas.

### 🧪 Simulador web

Puedes explorar la idea de Félix sin hardware usando el simulador:

- [Abrir simulador](assets/felix_robot_simulator.html)

### 📷 Capturas de la aplicación

Las capturas reales de la app se recopilan en el [Issue #29](https://github.com/luciano2-web/Luciano-Sarmiento/issues/29). Se publicarán aquí cuando estén disponibles.

---

## 🐾 Personalidad de Félix

Félix utiliza una personalidad conversacional inspirada en el comportamiento de un gato, con un estilo amistoso, curioso y juguetón.

### ✨ Reglas de personalidad

| Aspecto | Descripción |
|---------|-------------|
| **Nombre** | Félix (o GatoGPT) |
| **Tipo** | Asistente de IA con personalidad felina simulada |
| **Creador** | Luciano |
| **Personalidad** | Amistoso, curioso, juguetón, sabio |
| **Estilo** | Cercano, tierno, útil |
| **Frases felinas** | “miau”, “prrr”, “mrrr” (máximo 2 por respuesta) |

### ❌ Lo que Félix no hace
- ❌ No oculta que es un sistema de IA cuando se le pregunta
- ❌ No usa términos humanos como “manos” o “dedos”
- ❌ No genera contenido peligroso o ilegal
- ❌ No comparte información personal

→ [Ver sistema completo de personalidad](src/core/personality.py)

---

## 🏆 Niveles y colaboradores

Consulta [CONTRIBUTOR_LEVELS.md](CONTRIBUTOR_LEVELS.md) para conocer el sistema de reconocimiento simbólico de contribuciones. Los niveles no conceden permisos técnicos ni sustituyen los permisos configurados en GitHub.

<!-- BADGES-START -->
| Usuario | Contribuciones | Nivel |
|---|---|---|
| 🐱 **Luciano Sarmiento (Kiten)** | Owner — creador del proyecto | 🐱 Kiten |
<!-- BADGES-END -->

 > Esta tabla identifica el reconocimiento actual del proyecto; cualquier actualización debe reflejar contribuciones verificadas.

---

## 📁 Estructura del proyecto

```text
Luciano-Sarmiento/
├── docs/                          # Documentación
│   ├── ARCHITECTURE.md           # Arquitectura general
│   ├── PLAN_CUMPLIMIENTO_PROMESAS.md
│   ├── hardware/
│   │   ├── components.md         # Lista de componentes
│   │   └── assembly.md           # Guía de montaje
│   ├── firmware/
│   │   ├── flashing.md           # Guía para flashear ESP32
│   │   └── examples.md           # Ejemplos de MicroPython
│   └── mobile/
│       └── setup.md              # Configuración de la app
│
├── scripts/
│   └── update_levels.py          # Detección automática de niveles
│
├── src/
│   ├── core/
│   │   ├── personality.py        # Sistema de personalidad
│   │   └── constants.py          # Constantes globales
│   ├── mobile/
│   │   ├── main.py               # App principal
│   │   ├── chat_engine.py        # Motor de chat
│   │   ├── image_engine.py       # Motor de imágenes
│   │   └── requirements_mobile.txt
│   └── firmware/
│       ├── bluetooth_bridge.py
│       ├── audio_handler.py
│       └── display.py
│
├── .github/workflows/
│   ├── levels.yml                # Niveles automáticos
│   └── welcome.yml               # Bienvenida automática
│
├── assets/                       # Recursos visuales
│   ├── felix_concept.jpg
│   └── felix_robot_simulator.html
│
├── tests/                        # Pruebas
│   ├── test_personality.py
│   └── test_chat_engine.py
│
├── CONTRIBUTORS.json             # Fuente de verdad de contribuciones
├── CONTRIBUTORS.md               # Tabla humana de colaboradores
├── CONTRIBUTING.md               # Cómo contribuir
├── CODE_OF_CONDUCT.md            # Código de conducta
├── LICENSE                       # Licencia Apache 2.0
├── README.md                     # Documentación principal
└── .gitignore
```

---

## 🎯 Roadmap

- [ ] Documentar y validar un sistema de reconocimiento de contribuciones
- [x] Bienvenida automática en issues y PRs
- [ ] Mejorar la integración de voz
- [ ] Añadir más expresiones faciales físicas
- [ ] Mejorar la personalidad con memoria contextual
- [ ] Soporte para más modelos de IA
- [ ] Optimizar la app móvil para Android
- [ ] Publicar guías más detalladas de montaje y firmware
- [ ] Demo reproducible con capturas reales

---

## 🧑‍💻 Contribuir

Las contribuciones son bienvenidas. No hace falta trabajar en todas las áreas ni tener experiencia avanzada: puedes elegir una tarea pequeña y pedir orientación.

### Tareas abiertas para nuevos colaboradores

- [Equipo 1 — Firmware ESP32 (#42)](https://github.com/luciano2-web/Luciano-Sarmiento/issues/42) — punto de entrada y coordinación de periféricos.
- [Equipo 2 — App móvil y comunicación local (#37)](https://github.com/luciano2-web/Luciano-Sarmiento/issues/37) y [directorio de proveedores (#38)](https://github.com/luciano2-web/Luciano-Sarmiento/issues/38).
- [Equipo 3 — Diseño mecánico y CAD (#36)](https://github.com/luciano2-web/Luciano-Sarmiento/issues/36) — diseño felino; construcción física aplazada hasta 2027.
- [Equipo 4 — Sensores y visión (#39)](https://github.com/luciano2-web/Luciano-Sarmiento/issues/39) — cámara y privacidad; el tacto está propuesto en el [PR #40](https://github.com/luciano2-web/Luciano-Sarmiento/pull/40).
- [Equipo 5 — Calidad, pruebas y documentación (#43)](https://github.com/luciano2-web/Luciano-Sarmiento/issues/43).
- [Ver otras tareas abiertas](https://github.com/luciano2-web/Luciano-Sarmiento/issues).

Si quieres ayudar, elige un issue, comenta qué parte te interesa y espera confirmación antes de empezar cambios grandes. Las tareas deben indicar qué archivos tocar, qué resultado se espera y cómo comprobarlo.

Consulta la guía de contribución aquí:

- [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🤝 Comunidad

### ❓ ¿Dudas?
- Abre un [Issue](https://github.com/luciano2-web/Luciano-Sarmiento/issues) con la etiqueta `question`
- Revisa la [documentación](docs/ARCHITECTURE.md)
- Consulta la [guía de comunidades técnicas y difusión respetuosa](docs/COMMUNITY_OUTREACH.md)

### 🐛 ¿Encontraste un bug?
- Abre un [Issue](https://github.com/luciano2-web/Luciano-Sarmiento/issues) con la etiqueta `bug`
- Incluye:
  - Descripción del problema
  - Pasos para reproducirlo
  - Capturas o logs

---

## 📚 Tecnologías usadas

<div align="center">

| Tecnología | Versión | Uso |
|------------|----------|-----|
| [Python](https://www.python.org/) | 3.9+ | Lenguaje principal |
| [Kivy](https://kivy.org/) | 2.2+ | Interfaz gráfica |
| [PyTorch](https://pytorch.org/) | 2.0+ | Inferencia de IA |
| [Transformers](https://huggingface.co/docs/transformers/) | 4.30+ | Modelos de lenguaje |
| [Diffusers](https://huggingface.co/docs/diffusers/) | - | Generación de imágenes |
| [MicroPython](https://micropython.org/) | - | Firmware ESP32 |
| [ESP-IDF](https://www.espressif.com/en/products/sdks/esp-idf) | - | Alternativa para ESP32 |

</div>

---

## 📖 Recursos adicionales

- [Wiki](https://github.com/luciano2-web/Luciano-Sarmiento/wiki) - Documentación detallada
- [Issues abiertos](https://github.com/luciano2-web/Luciano-Sarmiento/issues) — espacio principal para coordinar contribuciones y preguntas.
- No hay todavía un servidor de Discord ni un video físico publicado; se anunciarán aquí cuando existan.

---

## ❤️ Agradecimientos

- A **Luciano** por crear este proyecto único
- A todos los colaboradores que aportan ideas, mejoras y energía
- A la comunidad open-source por hacer posible proyectos como este

---

<div align="center">

**🐱 Félix te espera… Ronronea… 🐾**

*Hecho con ❤️ para Luciano y todos los amantes de los gatos y la IA.*

</div>
