# 📋 Plan de cumplimiento de promesas — Félix / GatoGPT

> Este documento traduce lo prometido en `CONTRIBUTOR_LEVELS.md` y `COLABORACION_STRATEGY.md`
> en tareas concretas, ordenadas por prioridad, para cumplirlo sin romper el principio central:
> **invitar, no engañar.**

## Estado: qué está prometido y qué falta

| Promesa | Estado | Tarea para cumplir |
|---|---|---|
| Niveles 1-7 con privilegios definidos | ✅ Documentado | Aún sin aplicarse a nadie (no hay colaboradores aún) |
| Detección automática de nivel (GitHub Actions + bot) | 🚧 Planificado | F1: workflow `.github/workflows/levels.yml` |
| Badge por nivel en README | ❌ Pendiente | F2: tabla de badges + script de actualización |
| Mención en `CONTRIBUTORS.md` | ✅ Documentado | F3: actualizar el archivo tras cada PR merged |
| Rol/canal de Discord desde 🐧 | 🚧 Planificado (Discord no existe) | F4: crear servidor o marcar como "en revisión" |
| Mensaje de bienvenida automático (onboarding) | ❌ Pendiente | F5: workflow de bienvenida en issues/PRs |
| Mentoría | 🚧 Planificado | F6: definir mentores cuando haya 3+ colaboradores activos |
| Invitación a syncs desde 🐧 | ❌ Pendiente | F7: agendar sync mensual cuando haya colaboradores |
| Issues pequeños con criterios de aceptación | 🚧 Parcial | F8: crear 3-5 issues "good first issue" reales |
| Demo/capturas verificables | ❌ Pendiente | F9: demo reproducible o capturas reales |
| Instalación verificada y enlaces correctos | ❌ Pendiente | F10: auditoría del README |

## Fases

### Fase 0 — Honestidad inmediata (esta semana, sin código)
1. **F10: Auditoría del README.** Verificar comandos, enlaces y funciones descritas; marcar lo "Planificado" como tal.
2. Etiquetar en `CONTRIBUTOR_LEVELS.md` lo que aún no existe (Discord, detección automática) como "Planificado", tal como ya se hace.
3. No prometer nada nuevo hasta completar la Fase 1.

### Fase 1 — Base técnica de niveles (2-3 semanas)
4. **F1: Workflow de niveles** (`.github/workflows/levels.yml`):
   - Se dispara en `pull_request_target: closed` y `issues: closed`.
   - Lee `CONTRIBUTORS.json` (nuevo) con el historial de contribuciones.
   - Aplica las reglas de subida (PRs merged, triage, reviews) y baja (>90 días inactivo).
   - Abre un PR automático actualizando `CONTRIBUTORS.md` y los badges del README.
5. **F2: Badges en README**: sección "Colaboradores" con badge de emoji por nivel, generada desde `CONTRIBUTORS.json`.
6. **F3: `CONTRIBUTORS.json`** como fuente única de verdad (usuario, PRs, nivel, fecha última contribución).

### Fase 2 — Experiencia del colaborador (mes 2)
7. **F5: Bienvenida automática**: comentario inicial en cada issue/PR nuevo con guía a `CONTRIBUTING.md`.
8. **F8: 3-5 issues "good first issue"** con plantilla: objetivo, archivos a tocar, cómo probar, criterios de aceptación.
9. **F9: Demo reproducible**: notebook o capturas reales de Gatogpt funcionando, señalando lo experimental.

### Fase 3 — Comunidad (cuando haya 3+ colaboradores activos)
10. **F4: Discord** (o eliminar la promesa si no se crea) + roles automáticos por nivel.
11. **F6: Mentoría**: emparejar 🐧+ con 👾 según área (IA, móvil, firmware, docs).
12. **F7: Sync mensual** grabado, con agenda publicada.
13. Elevar a 🦉 (maintainer) al primer colaborador que cumpla nivel 7.

## Métricas de cumplimiento (revisión mensual)
- % de promesas de la tabla marcadas ✅.
- Tiempo medio de respuesta a PRs/issues.
- Issues "good first issue" completados.
- Colaboradores que subieron de nivel.

## Reglas de oro
- **No prometer lo que no se puede cumplir hoy.** Si algo queda "Planificado", se dice claramente.
- Los privilegios de nivel solo se otorgan con el mecanismo real ya implementado.
- Félix supervisa el roadmap; Kiten (Luciano) tiene la decisión final. 🐱
