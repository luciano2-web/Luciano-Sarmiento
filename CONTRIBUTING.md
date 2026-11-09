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

```bash
git clone https://github.com/luciano2-web/Luciano-Sarmiento.git
cd Luciano-Sarmiento
git checkout -b tipo/descripcion-corta
```

Haz cambios pequeños, describe lo que modificaste y ejecuta las pruebas pertinentes cuando sea posible. Después:

```bash
git add .
git commit -m "tipo: resumen breve del cambio"
git push -u origin tipo/descripcion-corta
```

Abre un Pull Request hacia `main` y enlaza el issue relacionado. Si no puedes ejecutar una prueba, indícalo con claridad; no marques como comprobado algo que no ejecutaste.

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

¡Gracias por ayudar a construir Félix! 🐾
