# 🤝 Cómo contribuir a Félix / GatoGPT

¡Gracias por interesarte en Félix! Puedes colaborar en programación, robótica, diseño, pruebas o documentación. No necesitas conocer todo el proyecto para empezar.

## 1. Elige una tarea

- Revisa los [issues abiertos](https://github.com/luciano2-web/Luciano-Sarmiento/issues).
- Busca tareas pequeñas o marcadas como **good first issue**.
- Lee el objetivo y los criterios de aceptación.
- Comenta en el issue qué parte quieres realizar y espera confirmación si hay dudas o varias personas interesadas.

## 2. Antes de programar

1. Lee el [README](README.md) y el [Código de Conducta](CODE_OF_CONDUCT.md).
2. Comprueba qué está implementado y qué está planificado.
3. No inventes pines, modelos de componentes, voltajes, protocolos ni resultados de pruebas.
4. Si falta información, pregunta en el issue antes de asumirla.
5. Mantén los cambios relacionados con el objetivo del issue.

## 3. Flujo recomendado

1. Lee el [README](README.md) y el [Código de Conducta](CODE_OF_CONDUCT.md).
2. Comprueba qué está implementado y qué está planificado.
3. No inventes pines, modelos de componentes, voltajes, protocolos ni resultados de pruebas.
4. Si falta información, pregunta en el issue antes de asumirla.
5. Mantén los cambios relacionados con el objetivo del issue.

```bash
git clone https://github.com/luciano2-web/Luciano-Sarmiento.git
cd Luciano-Sarmiento
git checkout -b tipo/descripcion-corta
```

## 4. Qué debe incluir un Pull Request

- Qué problema resuelve y por qué.
- Qué archivos cambió.
- Cómo se probó y cuál fue el resultado.
- Capturas o registros cuando ayuden a revisar.
- Issue relacionado (por ejemplo, `Fixes #37` si realmente lo resuelve).

## 5. Hardware y prototipos

- Antes de proponer conexiones o alimentación, confirma los modelos exactos de los componentes.
- Distingue entre simulación, documentación y pruebas con hardware real.
- No se deben comprar materiales ni fabricar el prototipo físico de Félix hasta que el equipo confirme que están disponibles y que el diseño fue revisado.
- La construcción física está prevista para 2027; el diseño CAD y la documentación sí pueden avanzar antes.

## 6. Comunicación y reconocimiento

- Sé respetuoso y explica tus dudas con claridad.
- Si no puedes continuar una tarea, avisa en el issue para que otra persona pueda retomarla.
- Cada contribución válida se revisará y reconocerá según el trabajo realizado.
- No compartas datos personales en issues o Pull Requests.

## 7. Issues activos para colaborar

- [#36 — Diseño del Félix físico con forma de gato](https://github.com/luciano2-web/Luciano-Sarmiento/issues/36)
- [#37 — Integración de la app móvil, ESP32 y funcionamiento local](https://github.com/luciano2-web/Luciano-Sarmiento/issues/37)
- [#38 — Sección de proveedores en la app móvil](https://github.com/luciano2-web/Luciano-Sarmiento/issues/38)

## 8. Primer artículo de documentación

- Añade o actualiza un artículo bajo `docs/` que explique un caso de uso concreto del proyecto (por ejemplo, cómo conectar la app móvil, cómo configurar el firmware ESP32 o cómo usar el simulador web).
- Incluye: objetivo, requisitos, pasos, resultado esperado y lo que ya está probado.
- Distingue claramente entre código listo, simulación y prueba real en hardware.
- Si el artículo menciona un proceso, un archivo, un teclado, un botón o un modo, evita afirmar que está terminado hasta comprobarlo.
- Incluye capturas de pantalla o registros solo si son reales del estado del proyecto.

¡Gracias por ayudar a construir Félix! 🐾

## 9. Equipos de trabajo

El proyecto organiza las tareas en cinco equipos. No hace falta unirse formalmente a un equipo: puedes tomar una tarea concreta y colaborar de forma puntual.

1. **Firmware y electrónica ESP32** — [Issue #42](https://github.com/luciano2-web/Luciano-Sarmiento/issues/42). Dificultad intermedia–alta.
2. **App móvil y comunicación local** — [Issue #37](https://github.com/luciano2-web/Luciano-Sarmiento/issues/37) y [Issue #38](https://github.com/luciano2-web/Luciano-Sarmiento/issues/38). Dificultad inicial–alta según la tarea.
3. **Diseño mecánico y CAD** — [Issue #36](https://github.com/luciano2-web/Luciano-Sarmiento/issues/36). Dificultad intermedia–alta; el montaje físico está previsto para 2027.
4. **Sensores y visión** — [Issue #39](https://github.com/luciano2-web/Luciano-Sarmiento/issues/39) y [PR #40](https://github.com/luciano2-web/Luciano-Sarmiento/pull/40). Dificultad alta.
5. **Calidad, pruebas y documentación** — [Issue #43](https://github.com/luciano2-web/Luciano-Sarmiento/issues/43). Dificultad intermedia.

## 10. Comunidades técnicas

Consulta la [guía de comunidades y difusión respetuosa](docs/COMMUNITY_OUTREACH.md). Antes de publicar, lee las reglas de cada espacio, participa de forma auténtica y no envíes invitaciones masivas. No afirmes que una comunidad o persona respalda el proyecto sin su autorización.

## 11. Revisión y agradecimiento

- Se acusará recibo de las propuestas cuando sea posible, sin prometer tiempos de respuesta que no podamos cumplir.
- Las revisiones deben ser específicas, amables y centradas en el cambio, no en la persona.
- Si un PR necesita cambios, explica qué falta y cómo comprobarlo.
- Agradece el tiempo de cada persona, incluso si su propuesta no se puede integrar.
- No se fusiona código solo por cortesía: primero se comprueban alcance, pruebas, seguridad y documentación.
