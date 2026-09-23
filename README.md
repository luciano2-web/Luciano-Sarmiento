# Luciano Sarmiento

Proyectos de robótica e IA desarrollados en Termux (Android), sin PC.

<div align="center">
  <img src="assets/felix_concept.jpg" alt="Félix / GatoGPT" width="360">
</div>

## Félix / GatoGPT

Gato robot con asistente de IA integrado. También conocido como GatoGPT.

- **Plataforma**: ESP32 DevKit + app Android (Termux)
- **Hardware**: 2x OLED 0.96" I2C, micrófono INMP441 I2S, parlante 4Ω 3W, protoboard, power bank
- **Objetivo**: asistente conversacional con personalidad felina, voz y expresiones en pantalla
- **Estado**: diseño completado, componentes pendientes de compra

Documentación de componentes: [Wiki — Félix Gato Robot](https://github.com/luciano2-web/Luciano-Sarmiento/wiki)

## ESP32-Android Bridge

Conexión Bluetooth entre microcontroladores ESP32 y apps Android.

- Firmware: MicroPython
- App: Python/Kivy
- Comunicación: Bluetooth Serial

## Mobile Use Skill

Automatización de interfaz gráfica de tablets Android desde Termux.

- Herramientas: ADB + Termux:API
- Funciones: capturas de pantalla, simulación de toques, navegación entre apps

## Cómo contribuir

1. Haz fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit: `git commit -m "Descripción clara"`
4. Envía un pull request

Las issues etiquetadas `good first issue` son un buen punto de partida. Guía completa en [CONTRIBUTING.md](CONTRIBUTING.md).

## Contacto

¿Interesado en colaborar? Abre un issue en cualquiera de los repositorios del proyecto.
