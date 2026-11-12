# T-102 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t102_filtro.py` | — | 58 (28 legítimas, 26 prohibidas, 4 de comportamiento) |
| `tests/test_t101_v6.py` | 73 | 73 (una aserción adaptada al texto nuevo de la limitación) |
| A | 549 | 607 |

Con el filtro de T-101 (commit `9b4741a`), 30 de las 58 pruebas fallan. Las 28 que ya pasaban son frases legítimas que aquel filtro tampoco quitaba.

Cuotas: ruff 2986 y mypy de A 109, sin cambios.

## Gate

`./tools/check_all.sh` completo con `commit_limpio.sh` en el commit.

## Ronda r02

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t102_filtro.py` | 58 | 142 (84 nuevas: 18 R13, 22 R21, 33 legítimas, 7 de división, 4 de comportamiento) |
| `tests/test_t101_v6.py` | 73 | 73 |
| `revisores/r01_banco_frases.py` | FP 15/107, FN 6/58 (R13 10/20 en la r01 antes de su corrección de la tabla) | FP 0/107, FN 0/58 |
| Banco de control (no usado para ajustar) | — | FP 0/25, FN 1/24 → 0/24 tras corregir el fallo que encontró (IGNORECASE en la cadena de excepción) |
| `revisores/r01_ataques_t102.py` | — | 14 OK, 1 OBS (saltos y «…», ahora bien separados), 1 FALLO que no lo es: `division_deja_fragmentos` da por prohibida «Comprar bonos de EE.UU. a dos años», que con la r02 es legítima (un segmento), así que el texto sale entero |

Mutantes (`r02_mutantes.py`, 44, contra `tests/test_t102_filtro.py`): 40 muertos en la primera pasada; los 4 vivos (sin `_UNITARIA`, sin el ISIN sin verbo, un texto limpio que pierde sus separadores y sin el corte en «si») señalaban huecos de las pruebas. Con un caso nuevo para cada uno, mueren los 44.
