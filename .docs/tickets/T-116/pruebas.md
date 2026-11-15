# T-116 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `bloque_a/11_Ejecutor` (recogidas) | 3744 (con T-114) | 3768: 16 en `tests/test_fase4_mapa.py` y 8 en `tests/test_fase4_huecos.py` |
| Pruebas citadas por el mapa | — | 94 (del ejecutor y de `10_Herramientas`), las 94 superadas |
| ruff (cuenta del gate) | 2902 | 2902 |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_ca1_el_mapa_tiene_las_67_pruebas_del_plan` |
| CA-2 | `test_ca2_el_mapa_no_tiene_problemas_y_cada_prueba_citada_existe`; `.venv/bin/python .docs/scripts/evidencias_plan_a.py` → «67 pruebas del plan, 94 pruebas automáticas citadas y todas existen», código 0 |
| CA-3 | `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` → «escrito docs/evidencias_pruebas_bloque_a.md · 94 de 94 pruebas citadas superadas», código 0 (2 min 31 s) |
| CA-4 | Orden de PB-22 copiada del documento y ejecutada desde la raíz: `3 passed` |
| CA-5 | `test_ca5_una_fila_sin_pruebas_nunca_resulta_superada`, `test_el_documento_tiene_una_fila_por_prueba_del_plan` |
| CA-6 | `test_ca6_un_mapa_estropeado_se_detecta` (11 casos) |
| CA-7 | Sección «Huecos» del `README.md` y fila T-116 de la deuda |
| CA-8 | Gate: ver abajo |

## Resultado del plan (13-11-2026, cliente simulado)

| Resultado | Pruebas del plan |
| --- | --- |
| Superada | 27 |
| Superada en parte | 28 |
| Pendiente API | 7 |
| Sin prueba | 3 |
| Requiere usuarios | 1 |
| Revisión documental | 1 |

## Regresiones

Las ocho pruebas de `test_fase4_huecos.py` no corrigen fallos: afirman cláusulas del plan que nadie comprobaba. Dos de ellas dejan constancia de que el ejecutor no hace lo que el plan pide (INC-T116-01 y INC-T116-02), sin cambiarlo.

## Gate

El gate completo 12/12 lo pasa `commit_limpio.sh` al hacer el commit; su resultado se anota en el registro del ticket.

## Ronda r04 (14-11-2026)

| Qué | Orden (desde la raíz de la copia, con el `.venv`) | Resultado |
| --- | --- | --- |
| Pruebas de la fase | `cd bloque_a/11_Ejecutor && python -m pytest -q tests/test_fase4_huecos.py tests/test_fase4_mapa.py` | 25 pruebas nuevas en `test_fase4_huecos.py` (29 casos) y dos ampliadas (PB-16 y PB-22); un caso de `test_fase4_mapa.py` corregido (dependía de cuántas pruebas cita PB-01). Las dos en verde |
| Goldens de contratos | `cd bloque_a/11_Ejecutor && python tests/goldens_ct.py` | «goldens de contratos: coinciden» (tras cada corrección del ejecutor) |
| Evidencias | `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` | «escrito docs/evidencias_pruebas_bloque_a.md · 132 de 132 pruebas citadas superadas», código 0 (8 min con la máquina compartida) |
| Suite del Bloque A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **5527 passed** en 1546 s (máquina compartida), el árbol queda limpio |
| ruff (tres `11_Ejecutor`, `--output-format=concise \| wc -l`) y mypy de A | — | 2902 (cuota 2902) y 109 (cuota 109) |
| Corpus, refs, secretos, NFC | `tools/corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | los cuatro con código 0 |
| Mutantes de la QA r03 | `python .docs/tickets/T-116/revisores/r03_01_pb32_y_muestra.py <copia desechable con «qa2_mut»>` | P32a a P32h, S06, S14, S33, S56, S60a y S60b: todos MUERTOS; a mano, los tres entregables declaran la degradación |
| Mutantes propios | `python .docs/tickets/T-116/r04_mutantes_implementador.py <copia desechable con «_mut»>` | 20 de 20 MUERTOS |

Regresiones: `test_pb60_…` falla sin la corrección de los entregables (comprobado en la copia desechable con `orquestacion.py` y `redaccion.py` del commit anterior: falla en «limitación visible en el paquete»). M06 (escalado), M09 (servicio pendiente), M10 y M11 (nota del visual y servicio ya provisto) son los mutantes que deshacen las otras dos correcciones, y mueren.

Resultado del plan tras la r04: 22 superadas, 33 en parte, 7 pendientes de la API, 3 sin prueba, 1 con usuarios y 1 documental.

No se ha pasado el gate completo (`tools/check_all.sh`) por indicación del encargo (máquina compartida); lo pasa quien coordina al integrar.
