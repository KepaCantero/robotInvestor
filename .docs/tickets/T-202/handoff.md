# T-202 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-25 · de claude (implementador, cierre) a QA (ronda de cierre)

- **Fase en la que se entrega:** ronda de cierre, tras el APTO de la QA r02 con H-04 abierto.
- **Hecho:**
  - Rebase de `wip/t202` sobre `origin/develop` (`eda55e1b`, con T-204 integrado). Hubo tres conflictos, resueltos según el README del ticket, sección «Al integrar»:
    - la línea base de `.docs/scripts`;
    - los comentarios de `preparar_entorno.sh`;
    - la cabecera de `requisitos_entorno.txt`.
  - `revisores/r07_resolucion_fusion_t204.diff` aplicado: la raíz falsa de `pruebas_gate_bloques.py`. La parte del comentario de `requisitos_entorno.txt` ya estaba en la resolución del conflicto.
  - Línea base de `.docs/scripts`: 466 (460 de develop + 6 de T-202).
  - INC-T202-01 copiada a `docs/incidencias.md`, con las cifras de la integración: A 67 y B 159; `[import-untyped]` de 50 a 28 en A y de 7 a 6 en B.
  - H-04 corregido en este traspaso (la frase «sale limpio» de la r02) y en el README («Al integrar»).
  - `.venv` propio rehecho desde cero con el script fusionado: 54 paquetes conformes; editables, solo A y B.
- **Falta:** la ronda de cierre de la QA. Commit local «T-202 cierre: …», sin push.
- **Cuidado con:** al integrar, el coordinador ejecuta `preparar_entorno.sh` en el `.venv` común. Hasta entonces, los gates de mypy de ese entorno salen ✗ (decisión 4).

## 2026-11-25 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02), después del NO APTO de la r01.
- **Hecho:**
  - **H-03:** `tools/check_all.sh` ejecuta `preparar_entorno.sh --comprobar` antes de mypy. Si falla, los gates de mypy salen ✗ con su motivo, sin ejecutar mypy, y el total sigue en 12. Es la decisión 4 de INC-T202-01. La prueba nueva es `.docs/scripts/pruebas_gate_entorno.py` (5 casos) y su mutante es M12.
  - **H-01:** prueba nueva `tests/test_t202_svi.py`, la de `revisores/r03_…`; su mutante es M09 (= RQ05).
  - **H-02:** el filtro de stubs de `pruebas_preparar_entorno.py` trabaja con el nombre normalizado, como propone `revisores/r04_…`; sus mutantes son M10 y M11 (= RQ11 y RQ12).
  - `mutantes.py`: 12 de 12 muertos. `revisores/r01_mutantes.py` y el gate: ver `pruebas.md`, «Ronda r02».
  - Línea base de `.docs/scripts`: de 400 a 405.
- **Falta:** la QA r02. Commit local «T-202 r02: …» en `wip/t202`, sin push.
- **Cuidado con:**
  - La fusión con T-204 (quita A-Forex del gate):
    - `check_all.sh` solo cambia dentro del bloque de mypy y no toca `for i in 0 1 2` ni las líneas contiguas. `git merge-file` con el `check_all.sh` de la copia de T-204 sale limpio. **Corregido en el cierre (QA r02, H-04):** limpio solo para `check_all.sh`. La fusión del repositorio entero da otros dos conflictos de comentarios (`preparar_entorno.sh` y la cabecera de `requisitos_entorno.txt`) y rompe 4 pruebas de T-204 en `pruebas_gate_bloques.py`: su raíz falsa no tiene `preparar_entorno.sh` y el comentario de T-202 nombraba el Forex. La resolución es `revisores/r07_resolucion_fusion_t204.diff` (sección del cierre, arriba).
    - La prueba nueva lee los paquetes de `PAQUETES=(…)`, así que sirve con dos bloques o con tres.
    - `linea_base_pruebas.txt` choca seguro, porque es una línea: al integrar, la base es la suma de lo que añade cada uno.
  - `CLAUDE.md` no se toca: su tabla del gate también la cambia T-204. Al integrar se puede añadir en la fila de mypy que exige el entorno fijado.
  - Con este cambio, el gate del `.venv` común y del de Astra sale en rojo en mypy hasta que se ejecute `preparar_entorno.sh` en cada uno. Es lo que se busca.
  - El contenedor se reinició durante `revisores/r01_mutantes.py` y dejó RQ02 aplicado en `fichas_series.py`. Lo restauré con `git checkout` y volví a ejecutar el script entero.

## 2026-11-24 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - Stubs fijados en `tools/requisitos_entorno.txt` e instalados por `preparar_entorno.sh`: types-PyYAML, types-jsonschema y scipy-stubs, con sus dependencias optype y numpy-typing-compat (54 paquetes fijados).
  - Los `[import-untyped]` bajan: de 49 a 27 en A, de 23 a 15 en A-Forex y de 7 a 6 en B. Las tres cuotas del gate siguen en 102, 174 y 159, con los mismos errores que develop.
  - Cuatro anotaciones de tipos en el Motor de A, que pide scipy-stubs y que no cambian ningún valor.
  - Una prueba nueva del script y una de ST-INF-001 (`tests/test_t202_alternativas_rangos.py`).
  - Equivalencia con develop sin diferencias y 8 mutantes muertos.
- **Falta:** la QA. Commit local en `wip/t202`, sin push.
- **Cuidado con:**
  - La QA tiene que usar un `.venv` con los stubs. El común no los tiene. Crea uno propio en la copia, con `python3.12 -m venv` mediante `preparar_entorno.sh`. No instales en el común.
  - Al integrar, ejecuta `.docs/scripts/preparar_entorno.sh` sobre cada `.venv` que ya exista: añade los cinco paquetes sin tocar el resto. Hasta entonces, `--comprobar` dirá «falta …».
  - INC-T202-01 `[PROPUESTO]` está en el README del ticket y no en `docs/incidencias.md`, porque ese fichero lo cambian el pull request 3 y T-196. Al integrar, se copia allí.
  - pandas-stubs y types-openpyxl no se fijan porque suben A-Forex y B. Sus números están en `analisis-tecnico.md`.
  - La fila T-202 de la deuda técnica va justo después de la de T-137, lejos de las filas que añaden las otras ramas.
- **Scripts útiles:** `.docs/tickets/T-202/equivalencia.py` (develop con su Python frente a la rama con el suyo, en una carpeta fuera del repositorio) y `.docs/tickets/T-202/mutantes.py` (`--solo-suite-anterior` para ver que M01 vivía sin la prueba nueva).
