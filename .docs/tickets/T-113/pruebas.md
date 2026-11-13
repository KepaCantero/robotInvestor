# T-113 · Informe de pruebas

| Suite | Resultado |
| --- | --- |
| `tests/test_t113_deuda.py` | 57 en verde |
| `tests/test_t102_filtro.py`, `tests/test_t101_v6.py` | En verde. Dos pruebas de T-102 se adaptaron al cambio buscado: el singular de H-49 y el esquema de una a tres frases de H-50 |
| `tests/test_t106_r03.py`, `tests/test_fase1_mon_idx.py`, `tests/test_t106_motor.py` | En verde. La prueba de la incertidumbre usa ahora `incertidumbre_probabilidad_acumulada`, sin tolerancia absoluta (N05) |
| `tests/test_t88_consumo.py`, `tests/test_t65*.py`, `tests/test_t92_revision.py` | En verde |
| Oráculo de la QA r03 de T-106 (`r03_03_mon_exp_oraculo.py`) | 4/4. Ninguna curva con la precisión declarada se rechaza ya por «no se puede reproducir» (H-27). La probabilidad de cada reunión queda dentro de su cota (máximo 0,70 de la cota, H-23) |
| Suite completa y gate | En el commit (`commit_limpio.sh`) |

Cuotas: ruff 2902 (antes 2907); mypy de A 109.
