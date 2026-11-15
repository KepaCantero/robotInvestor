> **Número renumerado (15-11-2026).** Este ticket del Bloque A se abrió como T-137, pero otra sesión usó T-137 para los hallazgos del entorno reproducible (T-96) y lo subió antes. El ticket del Bloque A sigue en **`.docs/tickets/T-140/`**; lo de esta carpeta es la copia antigua y no se actualiza (de `.docs/` no se borra nada: lo viejo se marca).

# T-137 · Pruebas

| Suite o script | Resultado |
| --- | --- |
| `tests/test_t137.py` | 12 passed |
| `test_t13*`, `test_t12*`, `test_t125*` | 588 passed |
| `goldens_ct.py` | coinciden |
| T-136 `r01_02_cota_por_peticion.py` | la cota cubre A (25,19) y con las reparaciones da 56,79, igual que su B |
| T-136 `r01_01_iban_tarjetas_formas.py` | tarjetas junto a otro número: 50/50 en cada caso; fallan las formas declaradas (H-03), los identificadores alfanuméricos al azar (34 de 126 000, declarado) y la fila de dos tarjetas válidas |
| ruff · mypy A | 2838 · 109 |

La suite completa y el gate, en el commit con `commit_limpio.sh`.
