# T-156 · Pruebas

Desde `bloque_a/11_Ejecutor`, sin red ni coste:

| Orden | Resultado |
| --- | --- |
| `pytest -q tests/test_t154.py -k t156` | 14 passed |
| `pytest -q tests/test_t154.py tests/test_t151_reintentos.py` | 104 passed |
| `pytest -q tests/test_t154.py tests/test_t151_reintentos.py tests/test_t146_presupuesto.py tests/test_t148.py tests/test_t129_modo_sombra.py tests/test_fase3_goldens.py` | 283 passed (al principio, 1 failed: `test_t154_h01_la_clasificacion_de_los_5xx_sale_de_la_configuracion` usaba 600 para mostrar que la configuración manda; ahora usa 400, con un 450 que pasa a cobrarse) |
| ruff, desde la raíz | 2831 (cuota 2831) |
| mypy de A | 109 (cuota 109) |

**Ronda de cierre (QA r01 APTO, H-01 y H-02 bajos).**
- **H-01.** El mutante P09 de `.docs/tickets/T-154/mutantes_t154.py` apunta ahora a la línea nueva que valida el rango.
- **H-02.** Esta tabla queda completa.

Los mutantes R01 a R03 del revisor de T-154 mueren todos (11/11 en `r01_03_mutantes_qa.py`, medido por la QA de T-156). La suite completa de A de la QA da 6638 passed y 2 skipped.
