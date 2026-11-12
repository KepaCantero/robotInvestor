# T-91 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t91_resolucion.py` | — | 10 |
| Suites de resolución y evaluación (las que usan `resolver`, el Evaluador, `pronosticos.csv` o `_sesiones_entre`) | 434 | 434 |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_h26_h1_cuenta_las_sesiones_sin_los_festivos_de_ps2` (Navidad y Pascua), `test_h26_sin_festivos_el_cierre_cuenta_como_sesion`, `test_h26_la_cesta_descarta_con_los_mismos_festivos` |
| CA-2 | `test_h27_proxy_y_referencia_se_miden_hasta_la_fecha_mas_antigua`, `test_h27_la_cesta_mide_todos_sus_miembros_hasta_la_misma_fecha` |
| CA-3 | `test_h28_el_criterio_congelado_dice_la_regla`, `test_h28_pronosticos_csv_lleva_la_fecha_de_cada_serie` |
| CA-4 | (a) `test_h29_a_ps2_con_la_referencia_sin_datos_no_pasa`; (b) `fecha_dato` en `test_h27_proxy…` y `test_h29_b…`; (c) la fecha de la CESTA en `test_h27_la_cesta…` |
| CA-5 | Gate de `commit_limpio.sh`; ruff 2986 → 2938 en el total (correcciones seguras de los archivos tocados, también de T-88 y T-103), mypy de A 109 |

## Gate

`./tools/check_all.sh` completo con `commit_limpio.sh`, en el mismo commit que T-88 y la ronda r02 de T-103 (comparten `orquestacion.py` y el diario).
