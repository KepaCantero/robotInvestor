# T-93 · Pruebas

Ejecutadas el 12-11-2026 por Claude, con el `.venv` de T-96.

| Suite | Antes | Después |
| --- | --- | --- |
| `r04_01_r8_regla_texto.py` | 11 fallos | 0 |
| `r04_02_almacen_corte.py` | 2 fallos | 0 |
| `r04_03_plazos_iso.py` | 4 fallos | 0 |
| `pytest bloque_a/11_Ejecutor` | 439 | 476 (37 nuevas) |
| ruff (los tres ejecutores) | 3072 | 3019 |
| mypy de A | 115 | 114 |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | Los tres scripts `r04_0x` | 0, 0 y 0 fallos |
| CA-2 | `r04_01` caso 1 y `test_h33_el_recall_de_las_claves_reales_no_baja` | Igual que la r04: todos los formatos al 100 % salvo los residuos de H-36 (3910/4000, 3986/4000 y 0/4000, las mismas cifras) |
| CA-3 | `tests/test_t93_hallazgos.py` | 37 pasan |
| CA-4 | Suite de A y gate | 476 pasan; gate en la copia limpia de `commit_limpio.sh` |
| CA-5 | `git status` | Solo `bloque_a/11_Ejecutor`, `tools/cuotas.txt`, `CLAUDE.md`, la deuda técnica y `.docs/` |

## Regresiones

Las 37 pruebas nuevas, copiadas a una copia limpia de HEAD (`5d03192`, sin el cambio): **34 fallan y 3 pasan**. Las 3 que pasan son vigilancia de lo que ya funcionaba: el recall de las claves reales, que una fecha de 8 cifras que no existe sigue siendo clave y el plazo en un día sin medianoche (H-39 c, que la r04 ya resolvía sin prueba).

Ajuste propio durante la implementación: la primera versión de la prueba de H-35 recortaba un registro **ya sellado**, y el almacén falla cerrado, que es lo correcto; la prueba se rehízo con una línea nueva cortada antes de su sello, que es el caso de H-35.

## Gate

Pasa en la copia limpia de `.docs/scripts/commit_limpio.sh`.
