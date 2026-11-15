# T-130 · Pruebas

| Suite o script | Resultado |
| --- | --- |
| `tests/test_t130_r8.py` | nuevo, en verde |
| `test_t123_r02.py`, `test_t123_r8_iban_y_tarjetas.py`, `test_t120_r8_y_lecciones.py`, `test_t122_hallazgos.py` | en verde (177 con la nueva); dos expectativas cambian por la decisión de H-05: `4111111111111111.5` y `VISA + ",5"` se marcan |
| `r02_01_falsos_r02.py` (revisor de T-123 r02) | 12/12 (antes 6/12) |
| `r01_02_caminos_r8.py` | 30/30 |
| `r01_01_banco_iban_tarjetas.py` | 10/11: el que falla es el límite declarado; con dos espacios ya no se detecta (decisión de H-07) |
| `tests/goldens_ct.py` y `test_fase3_goldens.py` | coinciden; 102 passed |

La suite completa y el gate, en el commit con `commit_limpio.sh`.
