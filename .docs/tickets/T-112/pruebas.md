# T-112 · Informe de pruebas

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `verificar_casos_control` con las 57 fichas con casos (21 de T-106, 35 de T-112 y AUD-REX-001); `tests/test_t112_motor.py` | 57 de 57 superadas (~~140 casos en la Fase 2~~ corrección de T-118, H-15 de la QA r02: **136** casos en la Fase 2 —S 36, R 36, V 38, P 26— y 6 de AUD-REX-001, contados al ejecutar `verificar_casos_control`) |
| CA-2 | `tests/test_t106_motor.py::test_el_motor_sirve_exactamente_lo_que_el_catalogo_da_por_implementado` (con AUD-REX-001 por CT-10) | Sí: 70 manejadores, los 70 servibles, y AUD-REX-001 por CT-10 |
| CA-3 | `tests/test_fase2_*.py` (rechazos, dominio, umbrales fijos y determinismo); `test_t112_motor.py` (no finitos, semilla y BIB-MET) | Sí |
| CA-4 | Oráculos de cada `test_fase2_*.py`; mutantes en `revisores/impl_*_mutantes.py` | Mutantes vivos: S 0 de 55 (uno equivalente, declarado), R 0 de 43, V 0 de 34, P 0 de 65 |
| CA-5 | `.docs/scripts/promover_fichas_catalogo.py --aplicar --etiqueta "ejecutor, casos de control registrados (T-112)"` | 36 promovidas; §1.3 con 71 IMPLEMENTADO y 10 DOCUMENTADO; corpus re-congelado (695 archivos) en el mismo commit |
| CA-6 | Gate del commit (`commit_limpio.sh`) | Ver «Gate» |

## Suites

| Suite | Pruebas |
| --- | --- |
| `test_fase2_series.py` | 320 |
| `test_fase2_riesgo.py` | 415 |
| `test_fase2_valoracion.py` | 547 |
| `test_fase2_reales.py` | 505 |
| `test_t112_motor.py` | 51 |
| Suite completa de A (`pytest -q tests`) | **3319** en verde (antes, 1481), 14 min |

## Regresiones adaptadas

Siete pruebas anteriores daban por hecho cosas que T-112 cambia:
- `test_t106_motor.py` contaba exactamente 21 fichas con casos de control. Ahora toma las de la Fase 1 de `servicio.FASE1` y comprueba los casos de las 57.
- `test_t106_r03.py` (S06), `test_t65_resto_t53.py` (CS-08) y `test_t92_revision.py` comprobaban que ACC-ERP-001, FX-MOM-001 y REI-CAP-001 no se sirven. Ahora comprueban que se sirven con los módulos nuevos, y la regla de `DOCUMENTADAS_CON_CODIGO` con el conjunto puesto a mano.
- La alternativa de CS-08 y la de `test_unitarias.py` usaban fichas que ahora se sirven (ACC-VAL-001, REI-NAV-001, RISK-VAR-001 y REG-HMM-001). Ahora usan CHR-ONCHAIN-001, que es P2 y sigue DOCUMENTADO.

## Gate

Lo pasa `.docs/scripts/commit_limpio.sh` en una copia limpia. Cuotas: ruff baja de 2908 a 2907 (`tools/cuotas.txt`); mypy de A, 109, sin cambios.

## Ronda r02

| Suite | r01 | r02 |
| --- | --- | --- |
| `test_fase2_series.py` | 320 | 380 |
| `test_fase2_riesgo.py` | 415 | 507 |
| `test_fase2_valoracion.py` | 547 | 620 |
| `test_fase2_reales.py` | 505 | 585 |
| `test_t112_motor.py` | 51 | 67 |

- **Casos de control:** las 57 fichas los superan (`verificar_casos_control`).
- **Mutantes de los grupos** (`impl_*_mutantes.py` y la parte de cada grupo en `r01_10_mutantes.py`): ninguno vivo. En `impl_R_mutantes.py` hubo que cambiar el texto de M15, porque cambió la línea; el mutante es el mismo.
- **`r01_06_hostiles.py`, por grupo:** sin fallos, con y sin `ulimit -v`. El script del revisor se corta en el bloque 5, porque espera que se sirva una petición con dos semillas distintas, y ahora se rechaza (H-05). Hay que adaptarlo en la QA r02.
- **Otros scripts del revisor:** `r01_11_config.py`, 6/6; `r01_03_oraculos_R.py`, 54/54; `r01_04_oraculos_V.py`, 114/114; `r01_05_oraculos_P.py`, 30/30.
- **Cuotas:** ruff 2907 y mypy de A 109; el corpus, íntegro.
- **Suite completa y gate:** en el commit (`commit_limpio.sh`).

