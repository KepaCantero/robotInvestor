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
