# T-132 · QA independiente

# Ronda r01 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01
- **Copia revisada:** copia git desconectada en `fe5b7d0` (T-132 entra en ese commit: ocho ficheros del ejecutor y `tools/cuotas.txt`).
- **Orden de lectura:** `README.md` → `git diff 08b357e fe5b7d0` de los ocho ficheros y de `tools/cuotas.txt` → cómo cuenta el gate (`tools/check_all.sh`) → mis comprobaciones → al final `analisis-tecnico.md` y `pruebas.md`.

## Reproducción desde limpio

Desde la raíz de la copia, con las herramientas del repositorio (`ruff` 0.17.4, la de `tools/requisitos_entorno.txt`; `py` = `/home/user/robotinvestor/.venv/bin/python`).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| El diff es exactamente `ruff check --fix` seguro | En una copia desechable (`qa11_mut`, ya borrada): poner la versión de `08b357e` de los ocho ficheros (`git show 08b357e:bloque_a/11_Ejecutor/<f>`), `ruff check --no-cache --fix <los ocho>` desde `bloque_a/11_Ejecutor`, y `diff` con los de `fe5b7d0` | **Los ocho idénticos.** Antes 69 hallazgos en esos ficheros, «55 fixed, 5 remaining» (como dice el registro del ticket); quedan 2 arreglos inseguros sin aplicar |
| Qué cambia | lectura del diff | Solo: `Dict`/`List`/`Tuple`/`Optional` → `dict`/`list`/`tuple`/`X \| None` en anotaciones (con `from __future__ import annotations` en todos), importaciones sin usar de `typing` y de `CLASES` y `HORIZONTES` en `sintesis.py`, `Sequence` de `collections.abc`, y `dt.timezone.utc` → `dt.UTC` (el mismo objeto; `requires-python = ">=3.12"`) |
| ¿Algo dependía de lo quitado? | `grep` de `sintesis.CLASES`, `sintesis.HORIZONTES`, importaciones de nombres de `typing` desde los ocho módulos, `get_type_hints` y `__annotations__` en el paquete | Nada. Sin reexportaciones ni introspección de anotaciones |
| Cómo cuenta el gate | `tools/check_all.sh`, línea 148: `.venv/bin/ruff check --output-format=concise <tres ejecutores> \| wc -l` contra `ruff=` de `tools/cuotas.txt` | Cuenta **líneas**, que son los hallazgos más dos de resumen («Found N errors.» y la de «fixable») |
| ruff desde la raíz | `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2838** (2836 hallazgos + 2 líneas de resumen) = la cuota de `tools/cuotas.txt`. La bajada de 64 líneas es la de los ocho ficheros (69 → 5) |
| mypy de A como el gate | `cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l` | **109** = la cuota |

## Comunes a T-129, T-130, T-131 y T-132

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Suite completa de A, una vez | `cd bloque_a/11_Ejecutor && py -m pytest -q -p no:cacheprovider` | **5951 passed** en 24 min 46 s, código 0 (incluye `test_t129_modo_sombra.py`, `test_t130_r8.py`, `test_t131_preparativos.py` y `test_fase3_goldens.py`) |
| Goldens CT | `cd bloque_a/11_Ejecutor && py tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff y mypy | arriba | 2838 ≤ 2838; 109 ≤ 109 |
| Gates ligeros | `py tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | Secretos sin hallazgos (también con mis scripts de `revisores/`); refs vivas, NFC y corpus (695 archivos) en verde |
| No lanzado (por instrucción) | `./tools/check_all.sh`, suites de A-Forex y B | — |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | ruff 2838 desde la raíz, contado como el gate; `tools/cuotas.txt` dice 2838 |
| CA-2 | sí | mypy A 109; el diff es el de `ruff --fix` seguro, reproducido byte a byte, y solo toca anotaciones, importaciones y `dt.UTC` |
| CA-3 | sí, salvo el gate entero (no lanzado por instrucción) | suite completa de A (arriba), que incluye `test_unitarias.py`, `test_integracion.py` y `test_fase3_goldens.py` |

## Hallazgos

Ninguno.

## Invariantes

- Ningún cambio de comportamiento: anotaciones (cadenas, por `from __future__ import annotations`), importaciones sin usar y un alias idéntico. ✔
- Cuotas: solo bajan (ruff 2902 → 2838; mypy sin cambio). ✔
- El paquete entregado: no se tocan las herramientas de `herramientas/referencia/` (copias del corpus) ni el corpus (695 archivos íntegros). ✔
- Secretos: ninguno. ✔

## Veredicto

**APTO** · Los tres criterios se cumplen (CA-3 sin el gate entero, que no lancé por instrucción). El diff es exactamente lo que da `ruff check --fix` sin arreglos inseguros sobre los ocho ficheros de `08b357e`; no cambia el comportamiento, y la cuota de 2838 es lo que cuenta el gate (líneas de la salida, con las dos de resumen). Sin hallazgos.
