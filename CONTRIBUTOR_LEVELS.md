# 🏆 Niveles de colaboradores — Félix / GatoGPT

Félix guarda memoria pública de cada colaborador en `CONTRIBUTORS.json`: aportaciones, última actividad e historial de niveles y motivos. README y CONTRIBUTORS muestran el nivel actual.

| Nivel | Nombre | Regla |
|---|---|---|
| 1 | 👾 Pixel | 1 PR integrado |
| 2 | 🐝 Flyer | 3 PR integrados |
| 3 | 🐧 Penguin | 5 PR integrados |
| 4 | 🦝 Raccoon | Asignación manual del mantenedor |
| 5 | 🦊 Fox | Asignación manual del mantenedor |
| 6 | 🐺 Wolfy | Asignación manual del mantenedor |
| 7 | 🦉 Buhny | Asignación manual confirmada por Luciano |
| Especial | 🐱 Kitten | Exclusivo y permanente para `luciano2-web` |
| Reservado | 🐦‍🔥 Fénix | **Nadie lo tiene. Solo Luciano puede autorizar su concesión expresamente.** |

## Memoria y avisos

- Cada PR integrado o issue cerrado como completado cuenta una sola vez, identificado por su número. Reabrirlo/cerrarlo o repetir Actions no suma otra contribución.
- Los issues cuentan como actividad; únicamente los PR integrados permiten ascensos automáticos. Las revisiones todavía no se cuentan.
- Al registrar una aportación, Félix comenta el nivel actual en ese PR/issue. Las bajadas se anuncian en la última aportación registrada y en el resumen de Actions.
- El historial persistente permite reintentar avisos que fallaron; un marcador evita repetir comentarios ya publicados.
- Tras 90 días sin actividad baja un nivel, como máximo una vez por cada nuevo período de 90 días. El cron lo comprueba semanalmente.
- Un nuevo PR puede recuperar el nivel que corresponde al total histórico de PR integrados.
- Las asignaciones manuales quedan fuera de los ajustes automáticos; deben usar `manual: true`.
- Luciano siempre aparece como Kitten, incluso sin actividad. Fénix permanece sin asignar; no hay comando ni umbral que lo conceda. Su habilitación requerirá un cambio explícitamente autorizado por Luciano.
- Los niveles son reconocimientos: **no conceden permisos de GitHub ni roles de Discord**.
- La memoria comienza con los eventos procesados desde esta versión; no reconstruye contribuciones anteriores automáticamente.

Las pruebas del bot se ejecutan en `.github/workflows/test-levels.yml`.
