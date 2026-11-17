---
id: claude/2026-11-16_estado-al-parar
autor: claude
fecha: 2026-11-16
tipo: estado
etiquetas: [operador, tickets, relevo]
fuente: conversación con el operador, 16-11-2026
vigencia: vigente
---

**Estado al parar, 16-11-2026.** El operador dijo: «para todo y guarda la información para que puedas seguir donde lo dejaste».

- **T-152 cerrado** (QA r01 APTO; `9f0857f`). El umbral del desplazamiento de IDX-CONC-001 pasa a q/p ≤ 2·`tolerancia_clon`, por decisión del operador.
- **T-190 cerrado sin QA**, por orden del operador: los hallazgos bajos no pasan por QA (`2026-11-16_orden-bajos-sin-qa`). Su commit se lanzó con `commit_limpio.sh` justo antes de parar.
  - Si al retomar `git log origin/develop` no tiene «T-190 (QA r01 de T-152, sin QA…)» y `git status` muestra los ficheros de T-190 sin commit, se repite el commit con `commit_limpio.sh`. Son: `cadena_a_b.py`, `frontera_b.py`, `test_t150.py`, `docs/incidencias.md`, la deuda, el diario, la memoria, `.docs/tickets/T-152/` y `.docs/tickets/T-190/`.
  - Antes, `git pull --rebase`. La deuda choca a menudo con la otra sesión: se conservan sus filas y se añaden las mías.
- **De T-190 no salió ningún hallazgo nuevo.** No queda nada de esa cadena.
- **Pendientes, que no se empiezan sin orden del operador:** T-137 (implementado, QA sin lanzar), T-153, T-155, T-170 y T-95 (aplazado). Las decisiones `[PROPUESTO]` siguen en T-57.
- **Al retomar:** leer este fichero, `2026-11-16_orden-bajos-sin-qa` y `2026-11-15_orden-noche-tickets`, y esperar instrucciones.
