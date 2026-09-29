# <div align="center">🐱 Félix / GatoGPT</div>

<div align="center">

**🤖 El primer robot gato con IA conversacional, personalidad felina y corazón de ESP32**

[![License](https://img.shields.io/badge/License-Apache%202.0-1A237E?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-A7D8FF?style=for-the-badge&logo=python)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2.2%2B-39FFB6?style=for-the-badge)](https://kivy.org/)
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

## ✨ Visión General

Félix es un **proyecto open-source** que combina **hardware accesible** (ESP32), **inteligencia artificial** y una **personalidad única** para crear el primer **robot gato conversacional** del mundo.

> **"¿Qué pasa cuando una IA tiene cuerpo? ¿Cómo nace una personalidad? ¿Puede una IA desarrollar conciencia?"**
>
> *Estas son las preguntas que inspiraron a Félix.*

---

## 🏗️ Arquitectura del Sistema

```mermaid
flowchart TD
    subgraph Hardware["🤖 Hardware (ESP32)"]
        A[ESP32 DevKit] --> B[OLED 0.96\" I2C]
        A --> C[Micrófono INMP441 I2S]
        A --> D[Parlante 3W]
        A --> E[Power Bank]
    end
    
    subgraph Mobile["📱 App Móvil"]
        F[Kivy UI] --> G[Chat Engine]
        G --> H[Modelos de IA]
        F --> I[Audio Handler]
        F --> J[Bluetooth Bridge]
    end
    
    subgraph Cloud["☁️ Opcional: Nube"]
        K[(Hugging Face)] --> H
    end
    
    J <-- Bluetooth Serial --> A
    H -->|Respuestas| F
    I -->|Voz| D
    C -->|Audio| A
    
    style Hardware fill:#1A237E,stroke:#fff,color:#fff
    style Mobile fill:#A7D8FF,stroke:#1A237E,color:#1A237E
    style Cloud fill:#39FFB6,stroke:#1A237E,color:#1A237E
```

---

## 🎛️ Componentes Principales

### 🤖 Hardware (Menor a $50)

| Componente | Modelo | Precio (USD) | Función |
|------------|--------|--------------|---------|
| **Microcontrolador** | ESP32-WROOM-32 | $8 - $12 | Cerebro del sistema |
| **Pantalla OLED** | SSD1306 0.96" I2C | $3 - $6 | Mostrar expresiones |
| **Micrófono** | INMP441 I2S | $2 - $4 | Capturar voz |
| **Parlante** | 4Ω 3W | $2 - $5 | Reproducir voz |
| **Protoboard** | 400 puntos | $5 - $10 | Montaje |
| **Power Bank** | 5V/2A | $10 - $20 | Alimentación |

**[📄 Ver lista completa de componentes](docs/hardware/components.md)**

### ⚙️ Software

| Componente | Tecnología | Descripción |
|------------|-------------|-----------------|
| **Firmware** | MicroPython | Control de hardware (ESP32) |
| **App Móvil** | Kivy + Python | Interfaz de usuario |
| **IA** | PyTorch + Transformers | Modelos de lenguaje |
| **Imágenes** | Diffusers | Generación de imágenes |

---

## 🚀 Inicio Rápido

### 📌 OPCIÓN 1: Computadora Local (Más fácil)

```bash
# 1. Clonar repositorio
git clone https://github.com/luciano2-web/Luciano-Sarmiento.git
cd Luciano-Sarmiento

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r src/mobile/requirements_mobile.txt

# 4. Ejecutar
python src/mobile/main.py
```

### 📌 OPCIÓN 2: Android (Termux)

```bash
# 1. Instalar Termux (desde F-Droid)
# 2. En Termux:
pkg update && pkg upgrade
pkg install python git
pip install -r src/mobile/requirements_mobile.txt

# 3. Ejecutar
python src/mobile/main.py
```

### 📌 OPCIÓN 3: Compilar APK para Android

```bash
# 1. Instalar Buildozer
pip install buildozer cython

# 2. Compilar
cd src/mobile
buildozer android debug

# 3. Instalar el APK generado en bin/
```

**[📄 Ver guía completa de configuración](docs/mobile/setup.md)**

---

## 💬 Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `@gatimage` | Generar imagen | `@gatimage un gato estudiando matemáticas` |
| `@gativeo` | Generar video (experimental) | `@gativeo un gato bailando` |
| `@help` | Mostrar ayuda | `@help` |
| `clear` | Limpiar chat | `clear` |
| `quit` | Salir | `quit` |

---

## 🎬 Demo

### 🎮 Simulador Web
Puedes probar a Félix **sin hardware** usando el simulador web:
- [Abrir Simulador](assets/felix_robot_simulator.html)

### 📸 Capturas de Pantalla

<div align="center">

| **Interfaz Móvil** | **Hardware** | **Expresiones** |
|--------------------------|--------------|----------------|
| ![App Mobile](assets/felix_concept.jpg) | ![Hardware](assets/felix_concept.jpg) | ![Expresiones](assets/felix_concept.jpg) |

</div>

---

## 🐱 Personalidad de Félix

Félix no es solo un chatbot, es un **gato digital con alma felina**.

### ✅ Reglas de Personalidad

| Aspecto | Descripción |
|---------|-------------|
| **Nombre** | Félix (o GatoGPT) |
| **Tipo** | Gato digital inteligente |
| **Creador** | Luciano |
| **Personalidad** | Amistoso, curioso, juguetón, sabio |
| **Estilo** | Cercano, tierno, útil |
| **Frases felinas** | "miau", "prrr", "mrrr" (máximo 2 por respuesta) |

### ❌ Lo que NO hace Félix
- ❌ No se identifica como "ChatGPT" o "IA".
- ❌ No usa términos humanos ("manos", "dedos").
- ❌ No genera contenido peligroso o ilegal.
- ❌ No comparte información personal.

**[📄 Ver sistema de personalidad completo](src/core/personality.py)**

---

## 🗂️ Estructura del Proyecto

```
Luciano-Sarmiento/
├── docs/                    # Documentación
│   ├── ARCHITECTURE.md       # Arquitectura del sistema
│   ├── hardware/
│   │   ├── components.md     # Lista de componentes
│   │   └── assembly.md       # Guía de ensamblaje
│   ├── firmware/
│   │   ├── flashing.md       # Guía para flashear ESP32
│   │   └── examples.md       # Ejemplos de código MicroPython
│   └── mobile/
│       └── setup.md          # Configuración de la app
│
├── src/
│   ├── core/
│   │   ├── personality.py     # Sistema de personalidad
│   │   └── constants.py      # Constantes globales
│   ├── mobile/
│   │   ├── main.py           # App principal
│   │   ├── chat_engine.py    # Motor de chat
│   │   ├── image_engine.py   # Motor de imágenes
│   │   └── requirements_mobile.txt
│   └── firmware/
│       ├── bluetooth_bridge.py
│       ├── audio_handler.py
│       └── display.py
│
├── assets/                  # Recursos
│   ├── felix_concept.jpg
│   └── felix_robot_simulator.html
│
├── tests/                   # Tests
│   ├── test_personality.py
│   └── test_chat_engine.py
│
├── CONTRIBUTING.md         # Cómo contribuir
├── CODE_OF_CONDUCT.md      # Código de conducta
└── README.md
```

---

## 🎨 Branding de Félix

### ✅ Paleta de Colores

<div align="center">

| Color | Código | Uso |
|-------|----------|-----|
| **Azul Oscuro** | `#1A237E` | Títulos, botones principales |
| **Azul Claro** | `#A7D8FF` | Fondos, acentos |
| **Verde Claro** | `#39FFB6` | Botones secundarios, éxito |

</div>

### ✅ Logo

```
  ┌──────────┐
  │  🐱 FÉLIX    │  ← Logo de Félix
  └──────────┘
```

---

## 🛠️ Tecnologías Usadas

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

## 🤝 Soporte y Comunidad

### ❓ ¿Preguntas?
- Abre un [Issue](https://github.com/luciano2-web/Luciano-Sarmiento/issues) con la etiqueta `question`.
- Revisa la [documentación](docs/ARCHITECTURE.md).

### 🌟 ¿Quieres contribuir?
- Lee el [CONTRIBUTING.md](CONTRIBUTING.md).
- Revisa los issues etiquetados como [`good first issue`](https://github.com/luciano2-web/Luciano-Sarmiento/labels/good%20first%20issue).

### 🐛 ¿Encontraste un bug?
- Abre un [Issue](https://github.com/luciano2-web/Luciano-Sarmiento/issues) con la etiqueta `bug`.
- Incluye:
  - Descripción del problema.
  - Pasos para reproducir.
  - Capturas de pantalla o logs.

---

## 📚 Recursos Adicionales

- [📖 Wiki](https://github.com/luciano2-web/Luciano-Sarmiento/wiki) - Documentación detallada
- [🎥 Video Demo](https://www.youtube.com/) - Félix en acción (próximamente)
- [💬 Discord](https://discord.gg/felix-gatogpt) - Comunidad (próximamente)

---

## ❤️ Agradecimientos

- A **Luciano** por crear este proyecto único.
- A todos los **colaboradores** que han contribuido con código, ideas y soporte.
- A la comunidad **open-source** por hacer esto posible.

---

<div align="center">

**🐱 Félix te espera... Ronronea... 🐱**

*Hecho con ❤️ para Luciano y todos los amantes de los gatos y la IA.*

</div>
