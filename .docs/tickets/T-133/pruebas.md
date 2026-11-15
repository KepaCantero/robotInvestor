> **Número renumerado (15-11-2026).** Este ticket del Bloque A se abrió como T-133, pero otra sesión usó T-133 para los hallazgos del banco de medida (T-94) y lo subió antes. El ticket del Bloque A sigue en **`.docs/tickets/T-136/`**; lo de esta carpeta es la copia antigua y no se actualiza (de `.docs/` no se borra nada: lo viejo se marca).

# T-133 · Pruebas

| Suite o script | Resultado |
| --- | --- |
| `tests/test_t133_r8.py` | 12 passed |
| `tests/test_t133_coste.py` | 5 passed |
| R8 vecinas (`test_t130_r8.py`, `test_t123_*`, `test_t120_*`, `test_t122_*`) y `test_t129_modo_sombra.py` | en verde; una expectativa de `test_t129_modo_sombra.py` cambia por la cota nueva |
| T-130 `r01_01_registro_y_formatos.py` | 17 ok, 1 fallo: H-04, declarado |
| T-130 `r01_02_comparacion_r02.py` | RO, LV, CY e IT con letras detectados; filas de 8 números: 0 de 5 000 |
| T-123 `r02_01_falsos_r02.py` · `r01_02_caminos_r8.py` | 12/12 · 30/30 |
| T-123 `r01_01_banco_iban_tarjetas.py` | 9/11: los 11 IBAN sintéticos con BBAN solo de cifras en países que piden letras (ver el análisis) y el límite declarado de cuatro grupos de cuatro cifras |
| T-129 `r01_02_sensibilidad_cota.py` (12 tipos) | el mayor escenario, 20,78 USD; la cota nueva, 22,60 USD |
| `tests/goldens_ct.py` | coinciden |

La suite completa y el gate, en el commit con `commit_limpio.sh`.
