# T-203 · QA

## Ronda de cierre · 2026-11-25 · revisor: claude (el mismo de la r01)

**Veredicto final: APTO, sin nada abierto.** H-01 y H-02 están cerrados. No hay hallazgos nuevos.

Código revisado: `wip/t203` `7da2b8e2` (cierre) sobre `5c3f534a` (el ticket rebasado), y los dos encima de `develop` `358576c3`, que ya
incluye T-201 (y T-196 y T-200). Worktree propio `qa_t203` en `7da2b8e2`, uno de `develop` (`qa_t203_dev`) y uno desechable para los
mutantes. Los scripts de la r01 se han vuelto a ejecutar. Donde los envoltorios de T-201 cambian lo esperado, se han copiado como `rc_`
(`revisores/rc_01` a `rc_07`).

| Qué | Cómo | Resultado |
| --- | --- | --- |
| ¿El rebase pierde algo de T-201? | Para cada fichero del commit de T-201 (`358576c3^..358576c3`), `git diff 358576c3 7da2b8e2` | Solo cambian `motor/operaciones.py`, `tools/cuotas.txt` y la deuda técnica. Los envoltorios de HT-02/03/07/09, `seguimiento.py`, `configuracion.py`, `backtest.py`, `servicio.py`, `evaluacion.py`, `test_t201_cuotas.py` e `incidencias.md` quedan byte a byte como en develop |
| ¿Se conserva lo de T-201 en `operaciones.py`? | range-diff de las líneas `+`/`-`: diff de T-203 en la r01 (`7f92064a..f38f3b9d`) frente al rebasado (`358576c3..7da2b8e2`), sin los envoltorios | Solo difieren `posicion_historica` (ahora `Sequence[float] \| np.ndarray`, de T-201, con `-> dict`) y, en `test_t203_cuotas.py`, el docstring y `TYPE_CHECKING`. Los cambios de T-201 (`mapa: dict[int, int]`, `diferencial`, `out: dict[str, float \| str]`) no aparecen en el diff: siguen intactos |
| Cuotas, con las órdenes del gate | `r01_03_cuotas.sh` en develop y en el cierre (`rc_03_cuotas.txt`) | Develop: ruff 2797, mypy 67/174/159. Cierre: **ruff 2735**, mypy **67/174/159**. Es exactamente `tools/cuotas.txt` (`ruff=2735`, `mypy_bloque_a=67`) y lo que da el gate (`gate_t203_cierre.log`: «cuota 2735, actual 2735», «cuota 67, actual 67») |
| Qué baja ruff | Diff por regla frente a develop | −62: UP006 30, I001 11, UP045 8, F401 7 y UP035 6. Ningún hallazgo nuevo. La lista de hallazgos es idéntica a la de la fusión que resolví en la r01 (`r01_04`) |
| mypy | Diff de los avisos sin número de línea | A: los mismos 67 avisos de develop. A-Forex y B: idénticos |
| H-02 | `git diff 358576c3 7da2b8e2 -- herramientas/` | Vacío: los envoltorios y su `noqa` son los de T-201. **Cerrado** |
| H-01 | Lectura de README («Pieza», «No entra», «Solape con T-201», CA-2), `analisis-tecnico.md`, `handoff.md`, `pruebas.md` (CA-2), la fila de la deuda y el mensaje de `5c3f534a`; grep de «ningún fichero en común» y «fuera de … T-201» | Los seis sitios dicen ya que T-203 comparte con T-201 `operaciones.py`, `tools/cuotas.txt` y la deuda, y que va rebasado. La frase de la r01 solo aparece citada como error corregido. `ca2_solapes.sh` lo reproduce: PR 3 y T-196, solo la deuda; corpus, nada. **Cerrado** |
| Scripts de cierre del implementador | `cierre_r01_04.sh` y `ca2_solapes.sh` en mi copia | TODO BIEN (rebasada sobre `358576c3`, merge-tree limpio, envoltorios de T-201, cuotas = medidas, 43 pruebas de T-201 y T-203). El resultado de CA-2 es el de arriba |
| Envoltorios en un intérprete nuevo | `rc_01_import_aislado.py` (`python -I`, fuera del repo; espera también `TYPE_CHECKING`) | En develop y en el cierre: mismos objetos, extra `DIR_REFERENCIA`, `TYPE_CHECKING`, `_ref` y `modulo` |
| Reexportaciones | `rc_02_reexportaciones.py` con base `358576c3` | Se quitan los mismos nombres que en la r01, con 0 usos en todo el repo |
| Mutantes contra `test_t203_cuotas.py` | `rc_05_mutantes_prueba.sh` en una copia desechable de `7da2b8e2` | 9 de 9 muertos |
| Equivalencia | `equivalencia.py` (sin cambios desde la r01), develop `358576c3` contra el cierre (`rc_06_equivalencia_cierre.txt`) | **IGUALES**, 90 ficheros, los cuatro con código 0 |
| Pruebas | Las de T-201 y T-203 y los diez ficheros que toca T-203 (`rc_07_vecinas.txt`); ids recogidos | 719 de 719. Ids: develop 8546, cierre 8551, la diferencia son exactamente los 5 de `test_t203_cuotas.py` |
| Suite completa y gate | `gate_t203_cierre.log` | 12/12; A 8549 pasadas de 8551 recogidas (las 2 de `test_t149.py:126`, omisión fija de la r01), A-Forex 68, B 176 |
| Gates baratos | corpus, NFC, secretos y refs vivas en la copia del cierre | En verde (705 ficheros del corpus) |

**Nota de coordinación (no es hallazgo).** T-204 (`wip/t204` `129376f4`) comparte con T-203 `tools/cuotas.txt` y la deuda técnica. Esos
conflictos, y el de `docs/incidencias.md`, ya existen entre T-204 y develop: T-203 no añade ninguno. T-204 retira A-Forex
(`ruff=1604` medido sobre 2806), así que, al integrarlo, la cuota de ruff habrá que medirla otra vez sobre develop con T-201 y T-203.

## Ronda r01 · 2026-11-24 · revisor: claude (sesión independiente, no implementó)

**Veredicto: APTO pendiente de ronda de cierre** (ningún hallazgo alto ni medio; dos bajos, H-01 y H-02, que verificará el mismo revisor
en la ronda de cierre).

Código revisado: `wip/t203` (`f38f3b9d`) sobre `7f92064a` (`git merge-base wip/t203 origin/develop`; el ticket es un solo commit), en un
worktree propio (`qa_t203`), más uno de la base (`qa_t203_base`), uno desechable para mutantes (`qa203_mut`) y uno de la fusión con T-201
(`qa_t203_fusion`). Scripts y salidas en `revisores/` (r01_01 a r01_06). No se lanzó `./tools/check_all.sh` (máquina de 4 núcleos con otros gates); se
leyó el del implementador (`gate_t203.log` del scratchpad: 12/12) y se repitió aparte cada parte que cuenta.

### Lo comprobado

| Qué | Cómo | Resultado |
| --- | --- | --- |
| Gate del implementador | `gate_t203.log` | 12/12; ruff 2735 (cuota 2735), mypy 102/174/159, pytest A 8442, FX 68, B 176 |
| Cuotas con las órdenes del gate | `r01_03_cuotas.sh` (desde la raíz, como `check_all.sh`) en base y ticket | base: ruff 2806, mypy 102/174/159; ticket: **ruff 2735**, mypy **102/174/159**. `tools/cuotas.txt` dice `ruff=2735`: exacto |
| Qué baja ruff | diff de las dos salidas por regla y fichero | −71: UP006 30, I001 14, UP045 8, F401 7, UP035 6, RUF100 6; ningún hallazgo nuevo. Lo que queda de esas reglas en A está solo en `referencia/` (corpus) y en `redaccion.py` y `referencias.py` (PR 3). FURB167 solo en esos ficheros |
| mypy de A, aviso a aviso | diff de las dos salidas sin número de línea | idénticas (los mismos 102); A-Forex y B, byte a byte iguales |
| 1. Envoltorios HT-02/03/07 en un intérprete nuevo | `r01_01_import_aislado.py`: `python -I`, carpeta temporal fuera del repo, `bloque_a.herramientas.htXX` como primer import del paquete | en base y ticket: carga, reexporta los mismos objetos (58, 27 y 29 nombres públicos, `is`), `modulo is _ref`, y los únicos nombres extra son `DIR_REFERENCIA`, `_ref` y `modulo`. Python ejecuta `herramientas/__init__.py` antes que cualquier submódulo (garantía del lenguaje); la referencia no define `DIR_REFERENCIA` ni `modulo`, así que el orden del `import *` no cambia qué nombre gana |
| 2. Anotaciones evaluadas en ejecución | grep propio en los tres ejecutores, `tools/`, `sistema_global/` y `.docs/scripts/`: `get_type_hints`, `__annotations__`, `inspect.signature`, `get_args`/`get_origin`, pydantic, dataclasses, `singledispatch`, typeguard/beartype, `eval(` | solo `evaluador.py:57` (`inspect.signature(ev.evaluar_celda)`, de `evaluacion`, no de los módulos tocados, y solo lee `.default`). `operaciones.py` y `mock_respuestas.py` no tienen clases de datos y los dos llevan `from __future__ import annotations` |
| 3. Reexportaciones | `r01_02_reexportaciones.py`: con `ast`, los nombres de módulo que desaparecen en cada `.py` tocado y sus usos en todo el repo (A, A-Forex, B, `sistema_global`, `tools`, `.docs`): `from … import`, `import *`, `alias.nombre` y cadenas | desaparecen `Dict`, `List`, `Optional`, `Tuple` (`operaciones`, `mock_respuestas`) y, en pruebas, `Evaluador`, `Path`, `nuevo_bloque`, `AS_OF`, `pd`: **0 usos**. Grep además en `origin/astra/encargos-bloque-a-c38-c47`, `wip/t196`, `wip/t201`, `wip/t202`: nadie toma esos nombres de esos módulos |
| 4. mypy y ruff | ver arriba | mypy no sube en ningún bloque; cuota de ruff = la del gate |
| 5. Ficheros vedados | `git diff --name-only 7f92064a wip/t203` frente a `origin/develop...` de PR 3, `wip/t196` y `wip/t201`, `tools/corpus_manifest.txt` y `referencia/` | PR 3 y T-196: solo la deuda técnica (`merge-tree` con la base sola da los mismos conflictos: T-203 no añade ninguno). Corpus: ninguno. `referencia/`: ninguno. Configuración de ruff/mypy y `check_all.sh`: ninguno. **T-201: cuatro ficheros de código en común** (H-01 y «Coordinación») |
| `noqa`, `type: ignore`, `cast`, `Any` | líneas del diff | ninguno nuevo; se quitan `noqa` sin uso; `# noqa: BLE001`: 25 en base y 25 en el ticket, ninguno tocado. El comentario del `noqa: F401` que queda es H-02 |
| Pruebas antiguas | lectura del diff de los diez ficheros de `tests/`; ids recogidos en base y ticket | solo cambian líneas de import (y una línea en blanco en `test_integracion.py`); ids: 8439 → 8444, exactamente los 5 de `test_t203_cuotas.py`, ninguno perdido |
| Las pruebas nuevas fallan sin el cambio | `test_t203_cuotas.py` copiado a la base | `test_anotaciones_…` falla en las dos (`hasattr(modulo, "Dict")`); `test_reexportacion_…` pasa (es de equivalencia, declarado en `pruebas.md`) |
| Mutantes propios contra `test_t203_cuotas.py` | `r01_05_mutantes_prueba.sh` (9 mutantes: sin `__future__` en cada módulo, vuelve `Dict`, anotación irresoluble, sin `DIR_REFERENCIA`, nombre extra, objeto distinto, referencia por ruta de paquete, `__init__` sin `sys.path`) | 9 de 9 muertos |
| Equivalencia (CA-4) | `equivalencia.py` del implementador, base contra ticket, en carpeta propia | **IGUALES**, 90 ficheros, los cuatro con código 0 (`revisores/r01_06_equivalencia_ticket.txt`) |
| ¿Detecta la equivalencia un cambio en `mock_respuestas`? | mutante propio: `"cobertura_variables": 70 → 71` en `_ficha` | 76 DIFERENCIAS (F1–F4, entregables, salidas; `revisores/r01_06_equivalencia_mutante_mock.txt`): la comprobación es sensible a lo que T-203 toca |
| Gates baratos en la copia de QA | `corpus_integridad.py`, `nfc_check.py`, `secrets_scan.py`, `refs_vivas.py` | los cuatro en verde (705 ficheros del corpus) |
| Suite completa de A | `pytest -q -rs bloque_a/11_Ejecutor` en `qa_t203` (`revisores/r01_07_suite_a.txt`) | **8442 pasadas, 2 omitidas, 0 fallos** (1 h 04 min con carga). Las 2 omitidas son `test_t149.py:126` («paso del orden del 1 % del precio: límite declarado»), una omisión fija por parámetros en un fichero que T-203 no toca: 8442 + 2 = 8444 recogidas |
| Clasificación de I001 | `ruff --select I001` desde `bloque_a/11_Ejecutor` | pide otro orden en 4 ficheros (sin `[tool.ruff]`, `bloque_a` es de primera parte solo desde la raíz). No es hallazgo: el gate mide desde la raíz y está declarado en los riesgos del README |

### H-01 · baja · La documentación dice que T-203 queda fuera de los ficheros de T-201, y no es así

- **Reproducir:** `git diff --name-only origin/develop...wip/t201` contiene `herramientas/ht02.py`, `ht03.py`, `ht07.py` y
  `motor/operaciones.py`, que T-203 también cambia; `git merge-tree --write-tree --name-only wip/t201 wip/t203` da conflicto en seis
  ficheros (esos cuatro, `tools/cuotas.txt` y la deuda técnica). `r01_04_fusion_t201.sh` lo reproduce.
- **Esperado:** README («Pieza», «No entra», CA-2), `analisis-tecnico.md` (línea 17 y «Aviso para T-201»), `handoff.md`, `pruebas.md`
  (CA-2: «ningún fichero en común»), la línea T-203 de la deuda técnica y el mensaje del commit dicen «fuera de los ficheros … de T-201»,
  con T-201 = tres ficheros de `referencia/`.
- **Pasa:** esa lista es la del primer objetivo de T-201; T-201 lo cambió el mismo día (su README, «Cambio de objetivo») y ahora toca los
  envoltorios y `operaciones.py`. CA-2 se comprobó contra una lista desfasada. No viola la regla común (la lista vedada es la del PR 3 y
  T-196), pero el ticket afirma algo falso y el que integre se encuentra conflictos que el ticket niega.
- **Corrección:** en esos seis sitios, decir que T-203 comparte con T-201 (objetivo actual) `ht02.py`, `ht03.py`, `ht07.py` y
  `operaciones.py`, con el orden de integración que decida el coordinador y la resolución (la de «Coordinación», abajo); rehacer CA-2
  contra `git diff --name-only origin/develop...wip/t201` actual. Si se integra después de T-201, rebasar y dejar el ticket como quede
  (ver abajo: el cambio no mecánico de los envoltorios desaparece).
- **Prueba de regresión:** `r01_04_fusion_t201.sh` (fusión limpia, ruff y mypy de la combinación y las pruebas de los dos tickets) y la
  salida de la orden de CA-2 pegada en `pruebas.md`.

### H-02 · baja · El motivo escrito junto al `# noqa: F401` de HT-02/03/07 ya no justifica el `noqa`

- **Reproducir:** `head -5 bloque_a/11_Ejecutor/bloque_a/herramientas/ht02.py` (igual en `ht03.py` y `ht07.py`).
- **Esperado:** regla común: ningún `noqa` sin un motivo concreto al lado. El `noqa: F401` dice por qué se mantiene un import sin uso.
- **Pasa:** el comentario nuevo dice que la carpeta de referencia entra en `sys.path` en `herramientas/__init__.py`, que Python ejecuta
  antes: es decir, que la línea ya no hace falta para eso. No dice por qué se conserva. El único motivo es no cambiar los nombres del
  módulo (`ht0X.DIR_REFERENCIA`; nadie lo usa salvo `test_t203_cuotas.py`).
- **Corrección:** `from . import DIR_REFERENCIA  # noqa: F401  (se conserva para que el módulo siga exponiendo DIR_REFERENCIA como antes;
  sys.path lo prepara herramientas/__init__.py, que Python ejecuta antes que este módulo)`. Si T-201 se integra antes y su versión de los
  envoltorios gana (ver abajo), este hallazgo se cierra solo: basta con comprobarlo.
- **Prueba de regresión:** `test_reexportacion_de_referencia_sin_cambios` ya exige `DIR_REFERENCIA` entre los nombres (mutante M5 de
  `r01_05` muerto); en la ronda de cierre se relee la línea.

### Coordinación con T-201 (no es hallazgo de T-203)

Con `r01_04_fusion_t201.sh` (`wip/t201` `67a52fd0` + `wip/t203` `f38f3b9d`):

- **`git merge-tree`: no se fusionan solas.** Conflictos en `ht02.py`, `ht03.py`, `ht07.py` (los dos reescriben el bloque de imports),
  `motor/operaciones.py` (líneas vecinas: `posicion_historica` y la firma de `diferencial_rentabilidades`), `tools/cuotas.txt` y la
  deuda técnica.
- **Resolución mínima:** envoltorios de T-201 (con `TYPE_CHECKING`; ya no tienen hallazgos de ruff, así que los −9 de T-203 en ellos
  quedan cubiertos); en `operaciones.py`, `def posicion_historica(valor: float, historia: Sequence[float] | np.ndarray) -> dict:`; las dos
  líneas de la deuda; `ruff=2735` y `mypy_bloque_a=67`.
- **ruff y mypy de la combinación:** ruff **2735** (la misma lista de hallazgos que T-203 sola), mypy A **67** (los mismos avisos que
  T-201 sola), A-Forex 174, B 159. **Equivalencia** de la combinación contra la base: **IGUALES** (90 ficheros).
- **Pero la suite no pasa entera:** fallan las 3 de `test_t203_cuotas.py::test_reexportacion_de_referencia_sin_cambios`, porque el
  envoltorio de T-201 añade el nombre `TYPE_CHECKING` y la prueba de T-203 exige el conjunto exacto de nombres. Con
  `"TYPE_CHECKING"` en la lista esperada pasan las 40 de los dos tickets, y los diez ficheros de pruebas que toca T-203 pasan en la combinación (676 de 676).
- **Orden recomendado:** primero T-201 y después T-203 rebasado. Así el cambio no mecánico de T-203 en los envoltorios desaparece (los
  deja T-201, ya limpios), H-02 se cierra solo, T-203 queda en `operaciones.py`, `mock_respuestas.py` y pruebas (−62 sobre 2797 = 2735),
  y lo que hay que tocar es la prueba (`TYPE_CHECKING`) y la documentación (H-01). Al revés hay que resolver los mismos seis ficheros en
  T-201 y adaptar igual la prueba de T-203.

### Criterios de aceptación

| CA | Resultado |
| --- | --- |
| CA-1 | Cumple: 2806 → 2735 y `ruff=2735`; 0 hallazgos de esas reglas en los ficheros permitidos |
| CA-2 | Cumple contra PR 3 y T-196; contra T-201 la lista era la antigua (H-01) |
| CA-3 | Cumple: mismos 102 avisos en A; 174 y 159 |
| CA-4 | Cumple: IGUALES (repetido por el revisor) |
| CA-5 | Cumple: 5 pruebas, 9 mutantes propios muertos; suite 8442 + 2 omitidas = 8444 |
| CA-6 | Cumple (gate del implementador 12/12; sin `noqa`/`ignore`/`cast`/`Any` nuevos; configuración y corpus intactos) |
