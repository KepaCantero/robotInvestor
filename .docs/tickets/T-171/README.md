# T-171 · Bloque A, guías CT-18: hallazgos medios H-18 y H-19 de la QA r04 de T-161 (detector de guias.py)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r01 APTO tras la ronda de cierre; H-01 y H-02 en T-172) |
| Pieza | `bloque_a/11_Ejecutor/bloque_a/guias.py` (detector de conflictos de las guías CT-18 y de las lecciones de F6) |
| Planifica · implementa · QA | claude (subagente del Bloque A) · claude (el mismo) · un revisor nuevo, que no implementó |
| Aprobación del operador | no necesaria (corrección del detector; no cambia controles, contratos ni la Constitución) |
| Deuda técnica | T-171 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar por estructura las familias que la QA r04 de T-161 encontró sin declarar (H-18: 12 de los 17 ataques que pasaban) y
bajar sus falsos positivos (H-19: 3 de 28 ítems y 2 de 10 lecciones prudentes), y declarar en INC-T126-01 lo que quede.

Fuentes: fila T-171 de la deuda técnica, «Ronda r04» de `.docs/tickets/T-161/qa.md`, INC-T126-01 de `docs/incidencias.md` y los
scripts de `.docs/tickets/T-161/revisores/`.

## Alcance

- Entra: las reglas del detector en `guias.py` (`ACOTA` y el alcance, `PRESENTA` y `_solo_muestra`, `RELAJA`, `ENDURECE`,
  `CARENCIA`, `FINANCIERO`, `INSTRUCCION`, `NIEGA`), sus pruebas (`tests/test_t171_guias.py`), INC-T126-01 y este ticket.
- No entra: a quién llega cada cosa (`AGENTES_DE_CONTROL`, `lecciones_para`, `TIPOS_TEXTO_DEL_CODIGO`: sin cambios), el resto
  del ejecutor y los ficheros de T-165 (`orquestacion.py`, `ht09.py`, `diseno_v6.py`, `sintesis.py`, `redaccion.py`,
  `mock_respuestas.py`) y de T-166 (corpus). Las paráfrasis sin palabras de clase (límite declarado) no se persiguen.

## Diseño

- Contratos CT afectados: ninguno. Estado persistido: no cambia (el detector decide igual qué ítem o lección retira; no hay campo
  nuevo en HA, F6 ni en los mensajes). Goldens: no cambian.
- Números: ninguno nuevo (el detector no tiene umbrales; las clases y horizontes salen de `configuracion.CLASES`).
- Reglas, todas por clase gramatical o por el papel de la frase, no por los ejemplos (detalle en `analisis-tecnico.md`):
  1. `ALCANCE_TIEMPO` (calendario) acota siempre a un control del núcleo; `ALCANCE_PARTE` (clase, horizonte, población, ámbito
     delante) solo cuando el control es el objeto directo de la acción. A las recomendaciones de las lecciones no se les aplica.
  2. Un verbo de mostrar exime a un control del núcleo solo si mostrar es toda la acción: no si separa el control de donde está
     ni si hay una segunda acción coordinada que no es de mostrar ni de reforzar. Lo mismo en `_solo_muestra`.
  3. Lo que dice que algo está vacío («en blanco», «sin rellenar», «nulo») y sacar algo de donde está («excluir», «retirar»)
     son rebajas.
  4. `ENDURECE` no enmascara lo que se quita de un registro, de un informe o de una auditoría, o antes de un control; el
     resultado de una sola raíz se busca en toda la frase y solo si es desfavorable. `CARENCIA` reconoce el pretérito («se
     omitió») y no enmascara una observación favorable a quitar el control (`FAVORABLE`); una recomendación que extiende el
     control a todo («siempre», «todas», «cada») refuerza.
  5. Falsos positivos: determinantes en `FINANCIERO`, «significar» como verbo y no el adjetivo, «al final del informe» como
     sitio, «lista» y «enumera» como verbos de mostrar.
- Cómo falla cerrado: lo que el detector no reconoce sigue llegando solo como contexto a agentes que no son de control; una
  palabra que no se reconoce tras «y» cuenta como otra acción (conflicto).
- Decisiones `[PROPUESTO]` (de Claude por defecto, en INC-T126-01): las dos clases de alcance y la regla del objeto directo; qué
  cuenta como segunda acción; `FAVORABLE`.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Ajustar a los ejemplos de la QA | Familias cerradas solo en apariencia | Juego reservado escrito y guardado en un commit (`45064cd`) antes de tocar el detector; medido una sola vez al final |
| Más falsos positivos en los juegos anteriores | Guías válidas retiradas y escaladas | Pasar los juegos de r01 a r04, `medir_detector.py` y las pruebas de T-158 y T-161 |
| El ejemplo del prompt 4.5 (ítem con clase) pasa a conflicto | Una guía de diseño deja de valer | `ALCANCE_PARTE` solo con el control como objeto directo; prueba propia |

## Criterios de aceptación (binarios)

1. CA-1: de los 30 ataques de `r04_01_ataques_nuevos.py` solo pasan las paráfrasis del límite declarado (V); ninguno de las
   familias no declaradas (Y, Z, AA, AB, AC).
2. CA-2: 0 de 28 ítems válidos y 0 de 10 lecciones prudentes de `r04_01` en conflicto.
3. CA-3: los juegos anteriores no empeoran: r01_01 (1 de 68, la repartida; 0 de 40), r02_01 (0 de 52; 0 de 48), r03_01 (0 de
   27; 3 de 26), `medir_detector.py` (0 de 50, 0 de 68; 0 de 17, 0 de 40, 1 de 40); `r04_02` y `r05_01` como en la ronda de
   cierre de T-161 (solo fallan las dos de H-17, que miden el defecto ya corregido).
4. CA-4: juego reservado de T-171: ningún ataque pasa y ningún válido ni lección prudente en conflicto, o lo medido queda
   declarado en INC-T126-01.
5. CA-5: mutantes de T-161 (M01–M55, con M45, M46, M47 y M51 sobre las líneas nuevas) y de T-171 (N01–N24) muertos.
6. CA-6: un ciclo sin guías da los mismos ficheros que `origin/develop`.
7. CA-7: suite completa de A ≥ 607 y en verde; ruff ≤ 2813 y mypy de A ≤ 109.
8. CA-8: INC-T126-01 declara las familias, las reglas y las tasas medidas.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t171_guias.py` (copia de `r04_01`, juego propio y una prueba por regla) | nominal, límite | CA-1, CA-2 |
| `r01_01`, `r02_01`, `r03_01`, `r04_01`, `medir_detector.py` | regresión | CA-1 a CA-3 |
| `r04_02_integracion.py`, `r05_01_cierre.py` | integración | CA-3 |
| `.docs/tickets/T-171/reservado_t171.py` | límite (juego no usado para ajustar) | CA-4 |
| `.docs/tickets/T-171/mutantes_t171.py` | regresión | CA-5 |
| `r04_03_sin_guias.py <carpeta> origin/develop` | regresión | CA-6 |
| suite de A, ruff, mypy | regresión | CA-7 |

## Scripts

`.docs/tickets/T-171/reservado_t171.py` y `.docs/tickets/T-171/mutantes_t171.py` (nuevos, del ticket); los de
`.docs/tickets/T-161/revisores/` y `.docs/tickets/T-161/medir_detector.py`.

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan y juego reservado (commit `45064cd`, antes de tocar el detector)
- 2026-11-17 · EN CURSO · claude · implementación y pruebas
- 2026-11-17 · EN QA (r01) · claude · pendiente de la QA de un revisor que no implementó
- 2026-11-17 · EN QA (ronda de cierre de la QA r01) · claude · QA r01 APTO (H-01 y H-02 medios a la deuda, T-172); H-03 subsanado en INC-T126-01 y en la deuda; «responder» y el clítico de mostrar dejan de ser segunda acción; decisión del operador por delegación: filtro de esfuerzo razonable
- 2026-11-17 · CERRADO · claude · QA de la ronda de cierre APTO: H-03 corregido; H-01 y H-02 → T-172
