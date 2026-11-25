# T-203 · Análisis técnico

## Motivo

La cuota de ruff (`tools/cuotas.txt`) era 2806 hallazgos en los tres ejecutores. El operador pidió el 24-11-2026 bajarla con las reglas mecánicas y seguras (UP006, UP045, UP035, I001, F401, RUF100 y FURB167), solo en `bloque_a/11_Ejecutor/` y sin tocar los ficheros de otras ramas abiertas.

## Evidencia

- Antes: `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l` (la orden del gate, desde la raíz) → 2806. En `bloque_a/11_Ejecutor`, 321 hallazgos de las siete reglas; 250 están en ficheros excluidos y 71 en ficheros permitidos.
- Después (r01): 2735 (−71). En los ficheros permitidos ya no queda ninguno de esas reglas.
- Tras el rebase sobre T-201 (develop 358576c3, ruff 2797): 2735 (−62: UP006 30, I001 11, UP045 8, F401 7 y UP035 6; los 9 de los envoltorios ya los quitó T-201) y ningún hallazgo nuevo.
- Una trampa de medida: con `--select` las reglas que no se seleccionan pasan por inactivas, y RUF100 da por «sin uso» los `# noqa: BLE001` (en `guias.py`, `motor/servicio.py`, `llm.py`, `evaluador.py`, `orquestacion.py` y varias pruebas). Con la configuración del gate (la de ruff por defecto, sin `[tool.ruff]` en el repositorio) BLE001 está activa y esos `noqa` se usan. Por eso el recuento se hace con la orden del gate, filtrando por código, y esos `noqa` no se tocan.

## Lista de exclusión (comprobada con `git diff --name-only`)

- PR 3 de Astra, `origin/develop...origin/astra/encargos-bloque-a-c38-c47`: 14 módulos del paquete (`agentes.py`, `altas_referencias.py`, `cli.py`, `consumo.py`, `contratos.py`, `evaluador.py`, `herramientas/ht08_monitor.py`, `interfaz_broker.py`, `mantenimiento_fuentes.py`, `orquestacion.py`, `redaccion.py`, `referencias.py`, `sintesis.py`, `sombra.py`), `config/por_defecto.yaml`, los goldens, `tests/mapa_plan_pruebas.json` y 13 ficheros de pruebas.
- T-196, `origin/develop...wip/t196`: `cli.py`, `cola_peticiones.py`, `orquestacion.py`, `respuesta_final.py`, `config/por_defecto.yaml`, `tests/mapa_plan_pruebas.json`, `tests/test_t196.py`, el README del ejecutor y dos documentos de `docs/`.
- T-201 (H-01 de la QA r01): la r01 ponía aquí tres ficheros de `referencia/` (`ht09_validador_g3.py`, `ht02_verificador_enlaces.py`, `ht03_puntuaciones.py`), la lista del primer objetivo de T-201. T-201 cambió de objetivo el mismo día y tocó `herramientas/ht02.py`, `ht03.py`, `ht07.py` y `motor/operaciones.py`, que T-203 también cambiaba: las dos ramas no se fusionaban solas (esos cuatro, `tools/cuotas.txt` y la deuda técnica). T-201 está en develop (358576c3) y T-203 va rebasado encima: los envoltorios quedan como los deja T-201 y en `operaciones.py` y `tools/cuotas.txt` se juntan los dos cambios (ver «Ronda de cierre»).
- `herramientas/referencia/` entera (las cuatro copias, `ht07_legibilidad.py` con 33 hallazgos incluida): son copias literales de `bloque_a/10_Herramientas/` (corpus congelado) y `tests/test_unitarias.py::test_herramientas_de_referencia_sin_divergencia` exige que sean iguales byte a byte.

## Implementación

- **Archivos cambiados y por qué** (todo en `bloque_a/11_Ejecutor/`):

  | Fichero | Reglas | Hallazgos | Cambio |
  | --- | --- | --- | --- |
  | `bloque_a/motor/operaciones.py` | UP006, UP045, UP035, F401 (+1 I001 que sale del UP035) | 32 | `Dict` → `dict`, `Optional[X]` → `X \| None` en firmas; `from typing import Dict, List, Optional, Sequence, Tuple` → `from collections.abc import Sequence`, en su sitio por orden alfabético |
  | `bloque_a/mock_respuestas.py` | UP006, UP035 | 14 | `Dict`/`List` → `dict`/`list` en firmas; `from typing import Any` |
  | `bloque_a/herramientas/ht02.py`, `ht03.py`, `ht07.py` | I001, RUF100 | 9 en la r01; 0 tras el rebase | solo en la r01 (el cambio no mecánico de abajo); tras el rebase quedan como los deja T-201 |
  | `tests/test_autocritica.py`, `test_fase1_fon_der.py`, `test_fase1_mon_idx.py`, `test_fase1_tcv.py`, `test_integracion.py`, `test_t174_pb61_revision_c2.py`, `test_t66_propuestas.py`, `test_unitarias.py`, `test_v5.py`, `test_v51.py` | I001, F401 | 16 | orden de imports; fuera `Evaluador` (`test_integracion.py`), `Path` y `nuevo_bloque` (`test_unitarias.py`), `pandas` y `AS_OF` (`test_v5.py`) |
  | `tests/test_t203_cuotas.py` (nuevo) | — | — | 5 casos: anotaciones de los dos módulos y reexportación de HT-02/03/07 (en el cierre, con `TYPE_CHECKING` entre los nombres) |
  | `tools/cuotas.txt` | — | — | r01: `ruff=2806` → `ruff=2735`; tras el rebase: `ruff=2797` (T-201) → `ruff=2735`, con `mypy_bloque_a=67` de T-201 |

- **Por qué UP006, UP045 y UP035 son seguros aquí.** Los dos módulos empiezan con `from __future__ import annotations`, así que las anotaciones son cadenas que no se evalúan al definir la función. Nadie las evalúa después: en el paquete y en las pruebas no hay pydantic, ni `typing.get_type_hints`, ni lectura de `__annotations__`, ni esquemas generados de tipos; las `dataclass` del paquete están en otros módulos (`consumo.py`, `agentes.py`, `llm.py`, `verificador_ids.py`) que no se tocan; el único `inspect.signature` (`evaluador.py`) lee valores por defecto, no tipos. `Dict`, `List`, `Optional` y `Tuple` solo aparecían en firmas, y ningún módulo los importa de `operaciones` ni de `mock_respuestas` (grep de `from … import Dict` y de `import *`). Y aunque alguien las evaluara, `dict[...]` y `X | None` valen en Python 3.12 (`requires-python >= 3.12`); lo comprueba `test_anotaciones_sin_evaluar_y_resolubles`.
- **Por qué F401 es seguro aquí.** Los cinco imports quitados están en módulos de prueba, que nadie importa (grep de `from test_…` y de `sys.modules["test_…`); `nuevo_bloque` es una función de `conftest.py`, no una fixture, y ninguna prueba de esos ficheros la usa. No se ha tocado ningún `__init__.py`.
- **I001 en las pruebas.** Solo cambia el orden: ahora algún `from bloque_a…` va antes de `from conftest import …`. `conftest.py` mete la raíz del ejecutor en `sys.path`, pero pytest lo carga antes de importar cualquier módulo de prueba, así que el orden dentro del módulo no importa. La suite completa pasa.
- **Cambio no mecánico de la r01 (desaparece en el rebase): HT-02, HT-03 y HT-07.** Antes:

  ```python
  from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)
  import ht02_verificador_enlaces as _ref  # noqa: E402
  from ht02_verificador_enlaces import *  # noqa: F401,F403,E402
  ```

  I001 pone primero los dos imports de la referencia (terceros) y después el relativo; RUF100 quita los `noqa` sin uso (E402 y F403 no están activos y F401 no salta en esas líneas; el `noqa: F401` de `DIR_REFERENCIA` sí se usa y se queda). Es equivalente porque `from . import DIR_REFERENCIA` nunca fue lo que preparaba `sys.path`: para importar `bloque_a.herramientas.ht02` Python ejecuta antes `bloque_a/herramientas/__init__.py`, que es quien mete `referencia/` en `sys.path`. Se reescribe el comentario para que diga eso. Las referencias no tienen `__all__` ni definen `DIR_REFERENCIA`, `_ref` o `modulo`, así que el orden de las asignaciones no cambia ningún nombre. `test_reexportacion_de_referencia_sin_cambios` lo comprueba en un intérprete nuevo sin la carpeta de referencia en `sys.path`: el módulo carga, `modulo` y `_ref` son la referencia, reexporta exactamente sus nombres públicos (los mismos objetos) más `DIR_REFERENCIA`, `_ref` y `modulo`. Esta prueba también pasa en develop: es de equivalencia.
- **Decisiones y desviaciones:** ninguna desviación del encargo. No hay ningún `# noqa` ni `# type: ignore` nuevo, ningún `cast` ni `Any` nuevo, y la configuración de ruff y de mypy no cambia (no hay `[tool.ruff]` ni `[tool.mypy]` en el repositorio; el gate usa los valores por defecto de ruff 0.17.4). El corpus no se toca.
- **mypy:** r01: A en 102 avisos, los mismos; tras el rebase, A en 67, los mismos que develop con T-201 (diff de los mensajes sin número de línea: vacío). A-Forex 174 y B 159, sin tocar.

## Ronda de cierre (2026-11-25, tras la QA r01)

- **Rebase sobre develop con T-201 (358576c3)**, en el orden que fijó el coordinador. Conflictos en `herramientas/ht02.py`, `ht03.py`, `ht07.py`, `motor/operaciones.py` y `tools/cuotas.txt` (la deuda técnica se fusionó sola). Resolución:
  - envoltorios HT-02/03/07: los de T-201, sin cambios (`git diff origin/develop` de los tres, vacío). Con eso **H-02 se cierra solo**: el `noqa: F401` y su motivo son los de T-201, que no se tocan;
  - `operaciones.py`: `def posicion_historica(valor: float, historia: Sequence[float] | np.ndarray) -> dict:`; el resto de T-203 en ese fichero entró sin conflicto;
  - `tools/cuotas.txt`: `mypy_bloque_a=67` de T-201 y `ruff=2735`, lo que mide el gate tras el rebase.
- **Prueba:** `test_reexportacion_de_referencia_sin_cambios` espera también `TYPE_CHECKING` entre los nombres del envoltorio (lo añade T-201); sin eso fallaban sus 3 casos. El docstring de `test_t203_cuotas.py` dice ahora que la prueba es guarda de equivalencia de los envoltorios de T-201.
- **H-01:** corregido en los seis sitios que cita la QA (README: «Pieza», «No entra» y CA-2; este análisis: la lista de exclusión y el aviso para T-201; `handoff.md`; `pruebas.md`, CA-2; la fila T-203 de la deuda técnica; y el mensaje del commit, reescrito en el rebase). CA-2 se rehace con `ca2_solapes.sh` contra las ramas de hoy.
- **T-204** (retira el Bloque A Forex, `wip/t204`) aún no está en develop: comparte con T-203 `tools/cuotas.txt` y la deuda técnica. Si entra antes, la cuota de ruff hay que recalcularla con el gate en la integración (quitará los hallazgos del ejecutor del Forex).

## Límites conocidos

- Sin `[tool.ruff]` en el repositorio, ruff clasifica los imports (propios o de terceros) según desde dónde se ejecuta. El orden de I001 es el que pide ruff ejecutado desde la raíz, como el gate; ejecutado desde `bloque_a/11_Ejecutor/` ruff podría pedir otro. Por eso algunos bloques de imports de las pruebas quedan con una agrupación rara (`from bloque_a.motor import …` con los de terceros). No se añade configuración (las reglas de cuotas prohíben tocarla).
- Quedan en `bloque_a/11_Ejecutor/` 250 hallazgos de estas siete reglas (igual tras el rebase), todos en ficheros excluidos: `referencia/ht02_verificador_enlaces.py` 79, `ht03_puntuaciones.py` 63, `ht09_validador_g3.py` 55, `ht07_legibilidad.py` 33 (copias del corpus), `referencias.py` 12 y `redaccion.py` 8 (PR 3).

## Aviso para T-201 (r01; ya no aplica)

`tests/test_unitarias.py::test_herramientas_de_referencia_sin_divergencia` compara byte a byte las cuatro copias de `bloque_a/11_Ejecutor/bloque_a/herramientas/referencia/` (`ht02_verificador_enlaces.py`, `ht03_puntuaciones.py`, `ht07_legibilidad.py` y `ht09_validador_g3.py`) con sus originales de `bloque_a/10_Herramientas/` (corpus congelado). Cualquier cambio de T-201 en esos tres ficheros hace fallar esa prueba, salvo que se cambie también el original (y se re-congele el corpus, que las reglas de cuotas prohíben). T-201 no tocó al final esas copias (cambió los envoltorios), así que el aviso queda sin efecto.

## Comandos exactos para probarlo

Desde la raíz de la copia:

- `.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l` → 2735 (develop con T-201: 2797).
- `.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l` → 67 (como develop con T-201).
- `.venv/bin/pytest -q bloque_a/11_Ejecutor/tests/test_t203_cuotas.py` → 5 superadas.
- `.venv/bin/python -I .docs/tickets/T-203/equivalencia.py <copia de develop> <esta copia> <carpeta de trabajo>` → IGUALES.
- `./tools/check_all.sh` → 12/12.
- `.docs/tickets/T-203/ca2_solapes.sh <esta copia>` (CA-2) y `.docs/tickets/T-203/cierre_r01_04.sh <esta copia>` (r01_04 adaptado) → TODO BIEN.
