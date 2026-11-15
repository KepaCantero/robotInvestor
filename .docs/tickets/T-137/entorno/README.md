# T-137 · Entorno reproducible: hallazgos abiertos de la QA r01 de T-96

> La carpeta `.docs/tickets/T-137/` guarda la copia antigua de un ticket del Bloque A que se renumeró (ver su README). Este ticket, el T-137 de la deuda («Entorno reproducible (T-96): hallazgos abiertos de la QA r01»), vive en esta subcarpeta.

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `.docs/scripts/preparar_entorno.sh`, `prompts/00_ENTORNO.md`, `CLAUDE.md` (pre-commit) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-15: «Después del T-97 quiero que sigas terminando los tickets que se han generado de los hallazgos de estos tickets» |
| Deuda técnica | T-137 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Qué se corrige

| Hallazgo | Corrección |
| --- | --- |
| H-01 (media) | `valida_venv`, antes de tocar nada, comprueba que el Python del `.venv` arranca, que es 3.12 y que pip funciona. Si no, para y dice cómo salir (`rm -rf .venv`). Si la creación del `.venv` falla, el script borra el que acaba de crear. |
| H-02 (media) | Esa misma validación va antes de `pip install`: un `.venv` de otro Python se rechaza sin instalar nada. |
| H-03 (media) | Un paquete instalado que no está fijado es un **error**, no un aviso, como dice el «Diseño» de T-96. |
| H-04 (media) | `prompts/00_ENTORNO.md` manda usar el script y nunca `pip install` sin versión. El pre-commit es opcional y va fuera del entorno fijado (`pipx`), y `CLAUDE.md` lo dice igual. |
| H-05 (baja) | El fichero se lee como pip: comentarios al final de la línea, solo `paquete==versión` y error si un paquete está repetido. |
| H-06 (baja) | Un argumento de más es un error, y `PYTHON_ENTORNO` admite un nombre del PATH. |
| H-07 (baja) | CA-2 de T-96 remite a `tools/cuotas.txt`. |
| H-08 (baja) | Límite declarado (abajo): pip, el `setuptools` de los editables y los hashes no se fijan. |

## Límites declarados (H-08)

El entorno no es reproducible al bit:
- pip sale del `ensurepip` del Python del sistema;
- el `setuptools` con el que se construyen los editables se baja sin versión fija;
- no hay hashes (`--require-hashes`), y hace falta la red hasta PyPI.

Las cuotas no dependen de ninguno de los tres (la QA de T-96 lo comprobó). Fijarlos queda como mejora.

## Criterios de aceptación (binarios)

1. CA-1: `.docs/scripts/pruebas_preparar_entorno.py` en verde, con una prueba por hallazgo de código (H-01, H-02, H-03, H-05 y H-06), y `pruebas_scripts.sh` por encima de su línea base.
2. CA-2: `preparar_entorno.sh --comprobar` da 0 con el `.venv` del proyecto.
3. CA-3: en un clon limpio, el script crea un `.venv` desde cero y el gate da 12/12 con él.
4. CA-4: no cambia ningún bloque, el marco común, la Constitución ni `tools/check_all.sh`.

## Registro

- 2026-11-15 · EN QA · H-01 a H-08 corregidos o declarados
