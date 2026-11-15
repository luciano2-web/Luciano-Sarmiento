# 🏗️ Plan de desarrollo de Félix — Perspectiva actual

> Actualizado: 2026-11-10. Refleja el estado real del repositorio `main`
> (2026-11-09) y los gaps que aún tienen que cerrar.

## Resumen ejecutivo

Félix tiene:

- Un núcleo de chat con validación de personalidad y módulos de imagen local.
- Module de firmware MicroPython (pantalla OLED, micrófono I2S, Bluetooth UART,
  sensor táctil).
- Una app móvil (Kivy) con motor de chat e imagen.
- Simulador web.
- Tests de Python (chat engine, personalidad, sensor táctil).
- CI: pytest, lint, validación de scripts Felix y actualización de niveles.

Lo que **no** tiene integrado en el estado actual:

- App ↔ ESP32 como integración funcional.
- Puente Bluetooth completo.
- Audio / reconocimiento y síntesis de voz de extremo a extremo.
- Cámara / visión.
- Servos (head/tail) con pines y alimentación definidos.
- Prototipo físico.

## Tabla de estrategia

| Área | Estado real | Lo que se afirma hoy | Lo que falta |
|---|---|---|---|
| App móvil (Kivy) | Implementado parcialmente | Estructura, módulos, motor de chat | Demo completa, bridge con ESP32 |
| Firmware ESP32 | Módulos separados | display, audio I2S, bluetooth UART, touch | Main que integre los módulos, control de servos |
| Simulador web | Disponible | Representación de Félix | — |
| Sensor táctil | Experimental (PR #40) | Propuesta y pruebas de lógica | Integración en main |
| Servos y movimiento | Planeado | Nomenclatura propuesta | Selección de placas, pines, alimentación |
| Cámara y visión | Planeado | No hay captura integrada | Seleccionar placa + cámara |
| Comunicación local app↔ESP32 | En desarrollo de diseño | Protocolo de discusión | Implementación y tests reales |
| Proveedores en la app | Planeado | Directorio y filtros pendientes | Construcción |
| Prototipo físico | Planeado para 2027 | — | Materiales y diseño revisado |

## Regla de publicación

Cada PR debe indicar si lo que muestra es:

- **Código** listo.
- **Simulación**.
- **Prueba realizada en hardware**.

No se anunciará una función como terminada hasta que hayan comprobado sus
criterios de aceptación.

## Documentación que se recomienda

- `docs/ARCHITECTURE.md` — versión actual con estado real.
- `docs/COMMUNITY_OUTREACH.md` — guía de difusión.
- `docs/PLAN_CUMPLIMIENTO_PROMESAS.md` — trazabilidad de promesas.
- `CONTRIBUTING.md` — cómo contribuir.
- `CONTRIBUTOR_LEVELS.md` — sistema de niveles.
- `docs/mobile/setup.md` — cómo preparar la app móvil.

## Pendientes claros

1. Integrar los módulos de firmware en un punto de entrada.
2. Definir pines, alimentación y control de servos.
3. Implementar el puente Bluetooth y probarlo.
4. Añadir audio completo (captura + síntesis) si es necesario.
5. Elegir placa y cámara para la visión.
6. Publicar pruebas reales en hardware en la documentación.
