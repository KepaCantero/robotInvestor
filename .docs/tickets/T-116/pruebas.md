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
