# T-126 · Análisis técnico

Solo pruebas: `bloque_a/11_Ejecutor/tests/test_t126_pb26_pb48.py`. No cambia código de producción ni el corpus. Medido el 14-11-2026: F7 560 referencias en 23 temáticas, F8 464 en 18, F9 389 en 19; ninguna sin temática válida, ninguna inversión de orden, todos los niveles coherentes con Q.

Límites: PB-26 comprueba el estado de los archivos, no el alta de referencias nuevas (Documentadores, modelo real); PB-48 comprueba que una guía que relaja un control no llega a la elegibilidad, pero el ejecutor no tiene el circuito de guías del Orquestador (CT-18) que registraría el conflicto (INC-T126-01).

Comandos: desde `bloque_a/11_Ejecutor`, `python -m pytest -q tests/test_t126_pb26_pb48.py`.

## Ronda r02 (hallazgos de la QA r01, APTO con hallazgos medios)

Solo pruebas, como la r01: `bloque_a/11_Ejecutor/tests/test_t126_r02.py` (11 casos). No cambia código de producción ni el corpus; `test_t126_pb26_pb48.py` no se toca.

| Hallazgo | Qué se hace |
| --- | --- |
| H-01 (media, J5) | Un ciclo de RV con la lección que relaja el control vigente y el Analista simulado haciendo la segunda pasada de todas sus dimensiones (lo que pide 9.1 frente a la guía): las opciones en banda marginal llegan a HT-03 con su segunda pasada, todas sus entradas de banda marginal quedan resueltas (`total_segunda_pasada`), ninguna cae por PS8 y la segunda pasada queda en F3. Contraprueba: las mismas entradas sin segunda pasada caen por PS8 |
| H-02 (media, J4) | `fichas_con_seccion` lee cada archivo con la sección `## TX-nn` en la que está físicamente cada ficha; se afirma que coincide con su campo «Temática», sin inversiones de Q por sección, y el desempate por fecha: a igualdad de Q, la de año de publicación más reciente primero. `[PROPUESTO]` (INC-T126-01): el año es el del campo «Año» si empieza por un año; un «Documento vivo» no tiene año y no se desempata. El caso dudoso (ANA-DOC-0522, 2016, antes que ANA-DOC-0089, Q 90 las dos) cae ahí: ANA-DOC-0089 es un «Documento vivo»; el lector del ejecutor (`referencias._anio`) le da 2026 porque mira también «Versión» («consultada el 2026-10-26»), lo que solo cuenta para la conocibilidad en backtest. Las fuentes de F9 no tienen año |
| H-03 (baja) | Las cinco comprobaciones de PB-26 son funciones (`fuera_de_su_seccion`, `inversiones_de_q`, `desempates_al_reves`, `niveles_incoherentes`, `tematicas_invalidas`) y se ejecutan sobre los archivos y sobre fichas estropeadas como J1–J4 y un desempate al revés |
| H-04 (baja) | El CT-06 del Analista de RV lleva `LEC-2026-0901` en `lecciones`, y ninguna entrada de HT-03 la lleva |

Límites: el revisor fija en `PRUEBAS` solo `test_t126_pb26_pb48.py`, así que J4 y J5 siguen vivos con su script tal cual; con las pruebas nuevas mueren (`.docs/scripts/mutantes_revisor_ampliado.py`). Que el ejecutor pida la segunda pasada cuando el Analista no la da no existe: la opción queda no elegible (PS8).

Comandos: desde `bloque_a/11_Ejecutor`, `python -m pytest -q tests/test_t126_pb26_pb48.py tests/test_t126_r02.py`; desde la raíz, `python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-126/revisores/r01_01_mutantes_y_ataques.py <copia con «_mut»>/bloque_a tests/test_t126_r02.py`.
