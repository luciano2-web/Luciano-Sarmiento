# 🌟 Luciano Sarmiento — Portfolio Tecnológico

## 🚀 Proyectos Activos

### 🐱 GatoGPT Félix
Asistente IA con personalidad felina en Termux/Android

- Modelo: *TinyLlama-1.1B* cuantizado (Q4_K_M)
- Stack: Python + llama.cpp + Kivy
- Características:
  - Chat con **personalidad felina** (ronroneos, bigotes, orejas expresivas)
  - Generación de imágenes locales (`@gatimage [prompt]`)
  - Animaciones simples (`@gativeo [descripción]`)
  - Guardado automático de conversaciones

---

**Ejemplo de interacción:**

```
Usuario: Hola Félix
Félix: ¡Miau! 🐾 ¿En qué puedo ayudarte hoy?
Usuario: ¿Cuál es el sentido de la vida?
Félix: *estira las patas* Bueno... yo creo que es disfrutar de cada momento, 
       mover la cola con curiosidad y ¡ronronear cuando algo nos emociona! 
       ¿Tú qué opinas? 🐱✨
```

---

### 🔗 ESP32-Android Bridge
Conexión **Bluetooth Serial** entre microcontroladores ESP32 y apps Android.

- Firmware: MicroPython en ESP32
- App: Python/Kivy en Android
- Comunicación: Serial vía HC-05/HC-06

**Arquitectura:**
```
┌─────────────┐   HC-05/HC-06   ┌─────────────┐
│   Android   │ ◄═════Serial════► │    ESP32    │
│   App       │                 │   Firmware  │
└─────────────┘                 └─────────────┘
```

---

### 📱 Mobile Use Skill
Automatización GUI de tablets desde Termux.

- Herramientas: ADB + Termux:API
- Funciones:
  - Captura de pantalla (`screencap`)
  - Simulación de toques (`input tap`)
  - Navegación entre apps (`am start`)
  - Lectura de notificaciones (`termux-notification`)

---

## 📈 Estado del Proyecto

![GitHub stars](https://img.shields.io/github/stars/luciano2-web/Luciano-Sarmiento?style=social)
![GitHub issues](https://img.shields.io/github/issues/luciano2-web/Luciano-Sarmiento)
![GitHub contributors](https://img.shields.io/github/contributors/luciano2-web/Luciano-Sarmiento)

---

## 🤝 Cómo Contribuir

1. **Fork** del repositorio
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commitear cambios: `git commit -m "Descripción clara"`
4. Push y PR: `git push origin feature/nueva-funcionalidad`

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para detalles.  
Revisa también las [issues abiertas](https://github.com/luciano2-web/Luciano-Sarmiento/issues).

---

## 📚 Wiki Técnica

Documentación completa en:  
[https://github.com/luciano2-web/Luciano-Sarmiento/wiki](https://github.com/luciano2-web/Luciano-Sarmiento/wiki)

---

## 📞 Contacto

¿Interesado en colaborar? Abre un issue o contacta a los mantenedores.

---
*Desarrollado con ❤️ desde Termux — Tablet Xiaomi Redmi Pad 5 (Android 15)*
