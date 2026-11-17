# T-190 · Pruebas

Se probó en el árbol de trabajo y en una copia desechable **completa** con «t147_mut» en la ruta (`git archive` de HEAD, los cambios encima y `.venv` enlazado). Antes de mutar, la copia pasa las 226 pruebas de `test_t150`, `t149` y `t144`. Sin red ni coste. Sin QA independiente, por orden del operador (`qa.md`).

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t150.py` | 103 | **112 passed**: 2 de `test_t190_h01_*` y 7 de `test_t190_h02_*` |
| `test_t150`, `t149`, `t147` y `t142_cadena_b` | — | 328 passed, 2 skipped |
| Suite completa de A | 7204 passed (gate de T-152) | En el gate de `commit_limpio.sh` |
| `.docs/scripts/pruebas_scripts.sh` | 231 | 231 |
| ruff, desde la raíz, sobre los ficheros tocados | — | sin avisos |

## Criterio de aceptación → prueba

| Criterio | Prueba y resultado |
| --- | --- |
| CA-1 (H-01) | `test_t190_h01_el_umbral_tambien_se_fija_por_arriba`, con 2 tramos × 6 semillas del revisor. `T-152/mutantes.py --grupo FB`: **U2 (4 %), U5 (2,1 %) y U6 (`<` estricto) muertos**, y también U1, U2b y U4; 0 vivos y ningún equivalente esperado. Con un umbral del 2,1 %, las dos pruebas nuevas fallan. Los textos de T-152 que daban U2 por equivalente (README, análisis y pruebas) llevan la nota de corrección. El docstring de la prueba del borde y el comentario de `frontera_b.py` están corregidos |
| CA-2 (H-02) | `T-152/revisores/r01_03_formas_qa.py`: **0 TRAZA**; antes, 4. Las pruebas `test_t190_h02_*` cubren el sustituto suelto al escribir y al imprimir, que un fallo no deja el fichero vacío ni el temporal, el `opp_id` de 300 cifras en el envío y en la sonda, y el JSON y el YAML anidados 100 000 niveles. Con el `cadena_a_b.py` de HEAD fallan las 5 primeras que se escribieron; las otras 2 se añadieron después para matar R7 y R9. Cadena real con los dos ejecutores simulados: código 0, ENTREGADA, G3 APTO, 3 enviables, 1 envío válido y la sonda ADMITIDA, sin temporales en `peticiones/` |
| CA-3 (H-03) | `grep -rn 4e39324 .docs/tickets/T-152/*.md`: solo en `qa.md`, que es el hallazgo citado por el revisor. 24 pruebas en el análisis y el diario de T-152; el comentario de T-150 dice 2·`tol` |
| CA-4 | `T-190/mutantes.py`: **9 de 9 muertos** (R1 a R9). `T-152/mutantes.py`: 0 vivos. `mutantes_heredados.py`: 22 de 22 en `T-150/mutantes.py`; en el revisor de T-150 solo vive X02, el casi equivalente conocido. `T-149/revisores/r01_02_mutantes_qa.py`: 0 vivos. `T-147/mutantes.py`: 0 vivos. `T-147/revisores/r01_03_mutantes_qa.py`, con `--ticket T-144` y con `--ticket T-147`: 0 vivos. Gate, en el commit |

## Lo que salió por el camino

- **Las líneas que mutan los scripts de otros tickets no se tocan.** La primera versión ponía un comentario en las dos líneas `except` de la lectura y añadía `RecursionError` a la tupla. Eso rompía K10 de `T-152/mutantes.py` y S8 de `T-150/mutantes.py`, que se paraban con su `assert`. Se rehízo: la recursión se convierte en el error que esas líneas ya capturan, dentro de `_leer_json` y de `_leer_yaml_extra`, y las líneas quedan tal cual.
- **R8 de `T-190/mutantes.py`** no era único, porque `_motivo_lectura` tiene el mismo `return`. Se alargó con la línea anterior.
- **Ningún hallazgo nuevo medio o alto.** No hay nada que pasar por QA.
