# T-112 · Informe de pruebas

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `verificar_casos_control` con las 57 fichas con casos (21 de T-106, 35 de T-112 y AUD-REX-001); `tests/test_t112_motor.py` | 57 de 57 superadas (140 casos en la Fase 2) |
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
