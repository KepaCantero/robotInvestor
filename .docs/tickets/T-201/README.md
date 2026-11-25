# T-201 · Bloque A: bajar la cuota de mypy sin cambiar ningún comportamiento

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (25-11-2026, QA r02 APTO sin hallazgos abiertos) |
| Pieza | bloque_a (ejecutor): los envoltorios `bloque_a/herramientas/ht02.py`, `ht03.py`, `ht07.py` y `ht09.py`, `seguimiento.py`, `configuracion.py`, `backtest.py`, `motor/servicio.py`, `motor/operaciones.py` y `motor/evaluacion.py` |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | Pedido por el operador el 24-11-2026 (cuotas de calidad). Objetivo cambiado el mismo día por el coordinador, por delegación del operador: opción (a), ver «Objetivo» |
| Deuda técnica | T-201 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Bajar `mypy_bloque_a` de `tools/cuotas.txt` (102) corrigiendo los errores de mypy del Bloque A que están en ficheros que no son del corpus ni copias suyas, y que no tocan la PR 3 de Astra ni T-196. No cambia ningún comportamiento: toda salida del ejecutor queda idéntica a la de `develop`.

**Cambio de objetivo (24-11-2026).** El encargo inicial era corregir los 53 errores de `bloque_a/herramientas/referencia/` (HT-09 26, HT-02 14, HT-03 13, contados con `mypy bloque_a`, sin `--ignore-missing-imports`). Esos ficheros son copias literales de `bloque_a/10_Herramientas/*.py`, que está en el corpus congelado (`tools/corpus_manifest.txt`), y `tests/test_unitarias.py::test_herramientas_de_referencia_sin_divergencia` compara sus huellas. Además, hay una decisión del operador del 16-11-2026: el HT-09 de referencia del corpus no se toca (`sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`, §1, fila G3-MET-13). El coordinador eligió la opción (a), por delegación del operador: las copias no se tocan y T-201 pasa a los demás errores.

**Deuda del corpus que no se puede bajar.** Lo que `herramientas/referencia/` aporta a la cuota se queda. Con la medida del gate (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a`, desde la raíz) son 61 líneas: 50 errores (HT-09 24, HT-02 13, HT-03 13) y 11 notas. Con la otra medida (`mypy bloque_a`, desde `bloque_a/11_Ejecutor`) salen 53 errores (HT-09 26, HT-02 14, HT-03 13): los 3 de más son los `import-not-found` de los imports entre copias, que el gate no cuenta. Son deuda del corpus congelado: así lo decidió el operador el 16-11-2026 (decisión citada arriba). Si algún día llega una entrega del corpus que los corrija, se bajarán entonces.

## Alcance

- **Entra:**
  - Los envoltorios de HT-02, HT-03, HT-07 y HT-09 (no son corpus). Importan la copia por `sys.path` con su nombre de primer nivel, y mypy no la encuentra: da `import-not-found` en el envoltorio y `attr-defined` en cada uso (`ht09.validar`, `ht03.evaluar_opcion`…). Con `if TYPE_CHECKING:`, mypy lee la copia por su ruta de paquete (`from .referencia.<modulo> import *`). En ejecución, la rama `else` importa exactamente lo mismo que antes.
  - Los errores de tipos de `seguimiento.py` (5 líneas), `motor/servicio.py` (3), `motor/operaciones.py` (3), `motor/evaluacion.py` (2), `backtest.py` (2) y `configuracion.py` (1).
- **No entra:**
  - `herramientas/referencia/` (corpus; ver arriba): 50 errores y 11 notas en la medida del gate y, en la de `mypy bloque_a`, además sus 3 `import-not-found` (`ht09_validador_g3.py:56-57` y `ht02_verificador_enlaces.py:74`), que el gate no cuenta. Están dentro de las copias, que se importan entre sí por `sys.path`. Solo se quitarían tocando las copias o la configuración de mypy, y las dos cosas están prohibidas.
  - Los ficheros de la PR 3 de Astra y de T-196: `orquestacion.py` (6 líneas), `cli.py`, `sintesis.py`, `redaccion.py`, `referencias.py`, `config/por_defecto.yaml` y `tests/mapa_plan_pruebas.json`, entre otros. Aun así, el arreglo de los envoltorios les quita los `attr-defined` sin tocarlos.
  - Los `[import-untyped]`, que lleva T-202 (stubs).
  - El `import-not-found` de `yfinance` (`herramientas/ht01_datos.py:400`). Es una dependencia opcional (extra `yahoo`) que el entorno fijado no instala. El gate no lo cuenta, porque corre con `--ignore-missing-imports`.
  - El caso del plan de pruebas: no lo hay.

## Diseño

- **Contratos y esquemas:** ninguno cambia. **Estado persistido:** no cambia. **Números:** ninguno.
- **Cambios mecánicos (solo anotaciones):** el retorno `-> (str, str)` pasa a `-> tuple[str, str]`; se anotan `ent`, `mapa`, `out` y `metricas`; `posicion_historica` admite un `np.ndarray`; se renombran la variable local `o` de `acierto_direccional` (ahora `arr`) y la `e` de un CACHE_HIT (ahora `hit`, porque ya era el nombre de una excepción en el mismo método).
- **Cambios no mecánicos (cada uno con su prueba, ver `pruebas.md`):**
  1. Envoltorios con `TYPE_CHECKING`. En ejecución, el mismo módulo (`sys.modules["ht0X_…"]`) y los mismos nombres. Si se importara por la ruta de paquete, el módulo se cargaría dos veces y `ht03.ErrorEntrada` dejaría de ser la clase que lanza HT-09.
  2. `seguimiento._cambio`: `.get(seg_id) if seg_id is not None else None`. F11 no tiene la clave None, así que da lo mismo.
  3. `seguimiento.b_agente(clase: str | None)`: con None devuelve «AG-03», que es lo que ya hacía `AGENTE_CLASE.get(None, "AG-03")`.
  4. `seguimiento._estado_hito`: sale de la comprensión de `_revision` sin cambiar nada. Lee el resultado binario siempre, también con el hito abierto, como antes.
  5. `motor/servicio.py`: `ALTERNATIVAS.get(ficha) if ficha is not None else None` (además, una ficha None se rechaza antes por la forma).
  6. `motor/operaciones.diferencial_rentabilidades`: el diferencial escalado se guarda en una variable y es el mismo objeto que antes se leía de `out["diferencial"]`.
  7. `configuracion.ruta` sin la clave o con la clave a null: el mismo `TypeError` que daba `Path(None)`, pero con el mensaje «rutas.<clave> no está en la configuración o es null» (r02, H-03). **Es el único cambio observable**, y solo en el mensaje de un error.
- **Cómo falla cerrado:** igual que antes; ningún camino de error cambia de tipo.
- **Decisiones `[PROPUESTO]`:** INC-T201-01 (en `docs/incidencias.md`): la rama `TYPE_CHECKING` en los envoltorios y la observación sobre `b_agente`, que se conserva tal cual.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Importar la copia por dos nombres en ejecución | Clases duplicadas; un `except ht03.ErrorEntrada` deja de casar | En ejecución se importa como antes (rama `else`); las pruebas comprueban la identidad del módulo y de la clase de error |
| Tocar ficheros de otras ramas abiertas | Conflictos al integrar | Ningún fichero tocado está en `git diff --name-only origin/develop...origin/astra/encargos-bloque-a-c38-c47` ni en wip/t196 |
| Un cambio de tipos que cambie una salida | Comportamiento distinto | Prueba de equivalencia de salidas (`equivalencia.sh`) frente a `origin/develop` |
| Otro ticket de cuotas (T-202, T-203) baja también las cuotas | Conflicto en `tools/cuotas.txt` | Se resuelve al integrar (regla común de los tickets de cuotas) |

## Criterios de aceptación (binarios)

1. CA-1: la cuota de mypy de A, medida como la mide el gate, baja de 102 a 67 y `tools/cuotas.txt` la recoge (`mypy_bloque_a=67`). Lo que queda son las 61 líneas de `herramientas/referencia/` (corpus: 50 errores y 11 notas) y las 6 de `orquestacion.py` (PR 3 de Astra y T-196).
2. CA-2: ningún fichero de `herramientas/referencia/`, del corpus, de la PR 3 de Astra ni de T-196 cambia. Tampoco cambia la configuración de ruff ni la de mypy, y no hay ningún `# type: ignore`, `# noqa` nuevo sin motivo, `cast` ni `Any` nuevo.
3. CA-3: en ejecución, los envoltorios importan el mismo módulo y reexportan los mismos objetos que antes; `ht03.ErrorEntrada` es la clase que usa HT-09.
4. CA-4: cada cambio no mecánico conserva el comportamiento de antes, incluidos los casos raros: None, la clave ausente y una resolución que no es un diccionario. Para `ruta`, el mismo tipo de error con un mensaje que nombra la clave cuando falta o está a null; con `""`, la raíz del paquete, y con `0`, el error de `Path`, como antes.
5. CA-5: el backtest del README, un ciclo mock, una petición, una consulta, un alta y un ciclo C6 de seguimiento, una evaluación y el estado dan las mismas salidas que `origin/develop`, byte a byte salvo rutas temporales, las dos latencias (`latencia_s` y `tiempo_respuesta_s`, por su nombre exacto, y la columna `latencia_s` de `consumo.csv`) y los resúmenes encadenados. Ningún instante se enmascara. El testigo de sensibilidad (`sensibilidad.py`, que lanza `equivalencia.sh`) da «puntos ciegos: ninguno».
6. CA-6: `./tools/check_all.sh` en verde (12/12); ruff no sube (baja de 2806 a 2797 y la cuota lo recoge); la suite de A no baja de 607.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `mypy --ignore-missing-imports --no-error-summary` sobre el paquete (la orden del gate) | regresión | CA-1 |
| `git diff --name-only` frente a las listas prohibidas; búsqueda de `type: ignore`, `noqa`, `cast` y `Any` en el diff | regresión | CA-2 |
| `tests/test_t201_cuotas.py`: identidad del módulo, la rama de mypy apunta al mismo fichero, reexportación, clase de error | regresión | CA-3 |
| `tests/test_t201_cuotas.py`: `ruta`, `_cambio`, `b_agente`, `_estado_hito` (comparado con la expresión de antes), `_revision` con hitos, `acierto_direccional`, `diferencial_rentabilidades`, el Motor sin ficha y el CACHE_HIT | nominal, límite, fallo cerrado | CA-4 |
| `.docs/tickets/T-201/equivalencia.sh` (prueba de equivalencia, en lugar de mutantes) y su testigo `.docs/tickets/T-201/sensibilidad.py` | integración | CA-5 |
| `./tools/check_all.sh` completo | regresión | CA-6 |

## Scripts

`.docs/tickets/T-201/equivalencia.sh`, `.docs/tickets/T-201/comparar.py` y `.docs/tickets/T-201/sensibilidad.py` (nuevos; el último desde la r02). Ejecutan la secuencia con el código de `origin/develop` y con el de la copia, en una carpeta temporal fuera del repositorio, y comparan las salidas.

## Registro

- 2026-11-24 · ABIERTO · claude · encargo del operador: los 53 errores de `herramientas/referencia/`
- 2026-11-24 · BLOQUEADO · claude · las copias son corpus congelado; decisión del operador del 16-11-2026
- 2026-11-24 · PLANIFICADO · claude · el coordinador, por delegación del operador, elige la opción (a): el objetivo pasa a los errores de fuera del corpus
- 2026-11-24 · EN CURSO · claude · envoltorios con `TYPE_CHECKING` y errores de tipos de seis ficheros
- 2026-11-24 · EN QA (r01) · claude · mypy de A 102 → 67, ruff 2806 → 2797; 35 pruebas nuevas; equivalencia de salidas EQUIVALENTE; commit local
- 2026-11-25 · EN QA (r02: QA r01 NO APTO) · claude · H-01: `comparar.py` enmascara solo las dos latencias por su nombre y ningún instante, y `equivalencia.sh` lanza el testigo de sensibilidad; H-02: caso de flotantes de `acierto_direccional`; H-03: mensaje de `ruta` «… o es null» y tres límites; H-04: cifras de `referencia/` con las dos medidas. 38 pruebas; M01 y M16 muertos
- 2026-11-25 · QA r02 · APTO sin hallazgos abiertos (`qa.md`).
- 2026-11-25 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
