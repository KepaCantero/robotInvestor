# T-96 · Pruebas

Todas ejecutadas el 11-11-2026 por Claude, en el clon de la sesión (Linux, Python 3.12.3).

| Suite | Antes | Después |
| --- | --- | --- |
| Gate completo en un clon nuevo con versiones sin fijar | 10/12 (mypy A 117 > 115, mypy A-Forex 176 > 174) | 12/12 con el `.venv` creado por el script |
| pytest A · A-Forex · B | 439 · 68 · 176 | 439 · 68 · 176 |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `.venv` movido fuera del repositorio; `.docs/scripts/preparar_entorno.sh` sin argumentos | Crea el entorno con `/usr/bin/python3.12`, instala y dice «entorno conforme: 49 paquetes con la versión fijada»; código 0, 37 s |
| CA-2 | `./tools/check_all.sh` en ese entorno | 12/12; pytest 439, 68 y 176 |
| CA-3 | `pip install arch==9.0.0` y `preparar_entorno.sh --comprobar` | Código 1: «arch: instalado 9.0.0, fijado 8.0.0». Al volver a ejecutar el script sin argumentos, reinstala 8.0.0 y da conforme (código 0) |
| CA-3 | `--comprobar` sobre el entorno verificado | Código 0 |
| CA-4 | `PYTHON_ENTORNO=/no/existe/python3.12` sin `.venv` | Código 1: «no encuentro Python 3.12» |
| CA-4 | `PYTHON_ENTORNO=/usr/local/bin/python3` (3.13) sin `.venv` | Código 1: «es Python 3.13; el proyecto usa 3.12» |
| CA-4 | `--comprobar` sin `.venv` | Código 1: «no hay entorno» |
| CA-5 | `git status` | Cambian solo `tools/requisitos_entorno.txt` (nuevo), `.docs/scripts/preparar_entorno.sh` (nuevo), `CLAUDE.md`, `.docs/README.md`, el relevo, la deuda técnica, el diario y este ticket. Ningún bloque, ni el marco común, ni la Constitución, ni `tools/check_all.sh` |

## Regresiones

Sin el fichero de versiones (`pip install` sin restricciones, como decía `CLAUDE.md`), el clon nuevo instaló `arch` 9.0.0 y el gate dio 10/12. La comprobación lo detecta (CA-3).

## Gate

`./tools/check_all.sh` con el `.venv` creado desde cero por el script: 12 ejecutados, 12 pasaron, 0 omitidos. El commit pasa además el gate completo en una copia limpia (`.docs/scripts/commit_limpio.sh`).
