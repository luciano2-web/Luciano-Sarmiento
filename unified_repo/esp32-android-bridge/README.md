# ESP32-Android Bridge

## 🌉 Conexión inteligente entre microcontrolador ESP32 y dispositivos Android

### Descripción
Este proyecto implementa un puente bidireccional entre ESP32 y Android, permitiendo:

- **Comunicación Bluetooth serial (HC-05/HC-06)** con ESP32
- **Control de sensores vía Android** (temperatura, humedad, distancia)
- **Toma de decisiones autónomas** en ESP32 basada en datos del móvil
- **Sincronización de estados** entre dispositivos

### Arquitectura

```
┌─────────────┐       Bluetooth       ┌─────────────┐
│   Android   │ ◄═════════════════════► │    ESP32    │
│     App     │                       │   Firmware  │
└─────────────┘                       └─────────────┘
      │                                     │
      └── Python/Kivy                   └── MicroPython/C
```

### Características
- Interfaz de usuario en Android con Kivy
- Firmware ESP32 en MicroPython
- Protocolo de comunicación estructurado (JSON sobre serial)
- Soporte para múltiples sensores

### Instalación rápida
```bash
# Clonar repositorio
git clone https://github.com/luciano2-web/esp32-android-bridge.git
cd esp32-android-bridge

# Instalar dependencias Android
pip install -r mobile/requirements.txt

# Flash de firmware ESP32
# (ver docs/firmware-setup.md)
```

### Contribuir
¡Las contribuciones son bienvenidas! Lee nuestras [Guías para Contribuidores](docs/CONTRIBUTING.md) y revisa las [Issues](https://github.com/luciano2-web/esp32-android-bridge/issues).

### Licencia
MIT License - por Luciano Sarmiento

---
*Con ❤️ desde Termux en una tablet Android 15* 🐱