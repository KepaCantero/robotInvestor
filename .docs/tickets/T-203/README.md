# T-203 · Bloque A: bajar la cuota de ruff con correcciones mecánicas (UP006, UP045, UP035, I001, F401 y RUF100)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (25-11-2026, QA r01 APTO y ronda de cierre verificada, sin hallazgos abiertos) |
| Pieza | bloque_a (ejecutor), solo calidad: `bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py`, `bloque_a/mock_respuestas.py` y diez ficheros de `tests/` (lista en `analisis-tecnico.md`), más `tests/test_t203_cuotas.py`. Comparte `operaciones.py` con T-201, ya integrado (358576c3): T-203 va rebasado encima |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-24: cuotas de calidad, pedido por el operador (tickets T-201, T-202 y T-203, con reglas comunes); orden de integración del coordinador: primero T-201 y después T-203 rebasado |
| Deuda técnica | T-203 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Bajar la cuota de ruff (`tools/cuotas.txt`, cuenta los tres ejecutores) sin cambiar ningún comportamiento: solo reglas mecánicas y seguras, solo en `bloque_a/11_Ejecutor/` y sin tocar los ficheros vedados (PR 3 de Astra y T-196).

## Fuentes

- Encargo del operador del 24-11-2026 (reglas comunes de los tickets de cuotas T-201, T-202 y T-203).
- `tools/check_all.sh` (gate `ruff (hallazgos)`: `ruff check --output-format=concise` de los tres ejecutores desde la raíz, contando líneas; gate `mypy` por paquete) y `tools/cuotas.txt`.
- CLAUDE.md, regla 9 y sección «Calidad»: las cuotas solo bajan; prohibido relajar la configuración.
- QA r01 (`qa.md`): APTO pendiente de ronda de cierre por H-01 y H-02, y orden de integración con T-201.

## Alcance

- **Entra:** las reglas UP006, UP045, UP035, I001, F401, RUF100 y FURB167 en los ficheros de `bloque_a/11_Ejecutor/` que quedan fuera de la lista de exclusión (abajo), medidas con la configuración del gate (la de ruff por defecto, sin `--select`). Sobre develop con T-201 (`ruff` 2797) son 62 hallazgos, en UP006, UP045, UP035, I001 y F401 (FURB167 solo sale en ficheros excluidos).
- **No entra:**
  - ISC004, RUF059, RUF046, BLE001 y TRY004 (cambian el comportamiento o piden juicio).
  - Los ficheros vedados por las reglas de cuotas: el PR 3 de Astra (`git diff --name-only origin/develop...origin/astra/encargos-bloque-a-c38-c47`: `agentes.py`, `altas_referencias.py`, `cli.py`, `consumo.py`, `contratos.py`, `evaluador.py`, `herramientas/ht08_monitor.py`, `interfaz_broker.py`, `mantenimiento_fuentes.py`, `orquestacion.py`, `redaccion.py`, `referencias.py`, `sintesis.py`, `sombra.py`, `config/por_defecto.yaml` y sus ficheros de `tests/`) y T-196 (`cli.py`, `cola_peticiones.py`, `orquestacion.py`, `respuesta_final.py`, `config/por_defecto.yaml`, `tests/mapa_plan_pruebas.json`, `tests/test_t196.py`; integrado en develop en be35f28e).
  - Las copias de `herramientas/referencia/` (`ht02_verificador_enlaces.py`, `ht03_puntuaciones.py`, `ht07_legibilidad.py` y `ht09_validador_g3.py`): son copias literales de `bloque_a/10_Herramientas/` (corpus congelado) y `tests/test_unitarias.py::test_herramientas_de_referencia_sin_divergencia` exige que sean idénticas byte a byte.
  - Los envoltorios `herramientas/ht02.py`, `ht03.py` y `ht07.py`: la r01 los cambiaba (I001 y RUF100), pero T-201 los reescribió (rama `TYPE_CHECKING`, ya sin hallazgos de ruff) y, por el orden de integración, en el rebase manda su versión. T-203 ya no los toca.
  - Los hallazgos de RUF100 que solo aparecen al pasar `--select` (los `# noqa: BLE001` de `guias.py`, `motor/servicio.py`, `llm.py` y varias pruebas): con la configuración del gate BLE001 está activa y esos `noqa` sí se usan; no se tocan.
- **Solape con T-201 (H-01 de la QA r01):** la r01 decía que T-203 quedaba fuera de los ficheros de T-201 y que T-201 eran tres ficheros de `referencia/`. Era la lista del primer objetivo de T-201, que cambió el mismo día: T-201 tocó `ht02.py`, `ht03.py`, `ht07.py` y `motor/operaciones.py`, y las dos ramas no se fusionaban solas (seis ficheros: esos cuatro, `tools/cuotas.txt` y la deuda técnica). Resolución en el rebase sobre T-201: envoltorios de T-201; en `operaciones.py`, `def posicion_historica(valor: float, historia: Sequence[float] | np.ndarray) -> dict:` (el tipo de T-201 y el `dict` de T-203); en `tools/cuotas.txt`, `mypy_bloque_a=67` de T-201 y la cuota de ruff que da el gate; las dos líneas de la deuda. Tras el rebase, T-203 comparte con T-201 solo `operaciones.py`, `tools/cuotas.txt` y la deuda técnica, ya resueltos.

## Diseño

- **Contratos y esquemas:** ninguno cambia. **Estado persistido:** no cambia. **Números:** ninguno.
- **Cambios mecánicos** (los aplica `ruff check --fix --select …` desde la raíz del repositorio): `Dict`/`List` → `dict`/`list`, `Optional[X]` → `X | None`, `typing.Sequence` → `collections.abc.Sequence` (solo en anotaciones de dos módulos con `from __future__ import annotations`: no se evalúan al definir y nadie las evalúa: ni pydantic, ni dataclasses, ni `get_type_hints`, ni esquemas generados de tipos; comprobado con grep), imports sin usar en pruebas (ninguno se reexporta ni lo usa otro módulo; `nuevo_bloque` de `conftest` es una función, no una fixture) y orden de imports en pruebas.
- **Cambio no mecánico:** ninguno tras el rebase (el de los envoltorios era de la r01 y desaparece). `tests/test_t203_cuotas.py` se queda como guarda: la reexportación de HT-02/03/07 (ahora con `TYPE_CHECKING` entre los nombres) y las anotaciones de los dos módulos.
- **Cómo falla cerrado:** no aplica (no cambia comportamiento). La equivalencia la comprueba `.docs/tickets/T-203/equivalencia.py`.
- **Decisiones `[PROPUESTO]`:** ninguna; el encargo fija el alcance y nada del spec queda por decidir, así que no hay incidencia nueva.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Una anotación se evalúa en tiempo de ejecución | `dict[...]`/`X | None` podría romper algo que lea tipos | Grep de `get_type_hints`, `__annotations__`, pydantic, dataclass y `inspect.signature` en el paquete y las pruebas; `test_anotaciones_sin_evaluar_y_resolubles` |
| Quitar un import que otro usa | `ImportError` o `AttributeError` en otro módulo o en las pruebas | Grep de reexportaciones (`from … import Dict`, `import *`); suite completa |
| Choque con otras ramas | Conflictos de fusión | CA-2 con `.docs/tickets/T-203/ca2_solapes.sh` contra cada rama; rebasado sobre T-201; T-204 (retira el Bloque A Forex) comparte `tools/cuotas.txt` y la deuda técnica |
| La clasificación de I001 depende de dónde se ejecuta ruff (no hay `[tool.ruff]`) | Ejecutado desde otra carpeta, ruff podría pedir otro orden | Se aplica y se mide desde la raíz, como el gate |

## Criterios de aceptación (binarios)

1. CA-1: el gate `ruff (hallazgos)` baja de 2797 (develop con T-201) a 2735 (−62) y `tools/cuotas.txt` queda en `ruff=2735`; en los ficheros permitidos no queda ningún hallazgo de UP006, UP045, UP035, I001, F401, RUF100 ni FURB167. (En la r01, sobre develop sin T-201: 2806 → 2735, −71.)
2. CA-2: ningún fichero de T-203 está en el PR 3 de Astra, en T-196 ni en el corpus congelado salvo la deuda técnica (una fila nueva); con T-201 solo `operaciones.py`, `tools/cuotas.txt` y la deuda técnica, resueltos en el rebase (`ca2_solapes.sh`).
3. CA-3: mypy no sube en ningún bloque: A 67 (los mismos 67 avisos que develop), A-Forex 174 y B 159.
4. CA-4: las salidas del ejecutor son idénticas a las de develop (ciclo mock, backtest del README, una petición y una consulta), salvo latencias: `equivalencia.py` da IGUALES.
5. CA-5: las anotaciones y la reexportación de HT-02/03/07 tienen su prueba (`tests/test_t203_cuotas.py`), y la suite de A pasa entera (8551 recogidas, develop 8546).
6. CA-6: `./tools/check_all.sh` completo en verde (12/12); ningún `# noqa` ni `# type: ignore` nuevo, ningún `cast` ni `Any`, sin tocar la configuración de ruff o mypy ni el corpus.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Gate `ruff (hallazgos)` y recuento por regla frente a develop | regresión | CA-1 |
| `.docs/tickets/T-203/ca2_solapes.sh` (ficheros de T-203 frente a PR 3, T-196, T-201, T-204 y el corpus) | regresión | CA-2 |
| mypy de los tres paquetes, y diff de los avisos de A frente a develop | regresión | CA-3 |
| `.docs/tickets/T-203/equivalencia.py <develop> <ticket> <trabajo>` | equivalencia, integración | CA-4 |
| `tests/test_t203_cuotas.py` (5 casos) y la suite completa de A | regresión | CA-5 |
| `.docs/tickets/T-203/cierre_r01_04.sh` (r01_04 de la QA adaptado a T-201 integrado) | integración | CA-1, CA-3, CA-5 |
| `./tools/check_all.sh` | gate | CA-6 |

## Scripts

- `.docs/tickets/T-203/equivalencia.py`: compara las salidas de dos copias del repositorio.
- `.docs/tickets/T-203/ca2_solapes.sh` (cierre): ficheros de T-203 frente a los de las otras ramas.
- `.docs/tickets/T-203/cierre_r01_04.sh` (cierre): `revisores/r01_04_fusion_t201.sh` adaptado a T-201 ya en develop.
- `tools/check_all.sh` (gate completo).

## Registro

- 2026-11-24 · PLANIFICADO · claude · alcance y lista de exclusión comprobados con `git diff`.
- 2026-11-24 · EN CURSO · claude · 71 hallazgos corregidos; equivalencia IGUALES.
- 2026-11-24 · EN QA (r01) · claude · gate completo en verde; commit local en `wip/t203`.
- 2026-11-24 · QA r01 · revisor · APTO pendiente de ronda de cierre (H-01 y H-02, bajos; orden con T-201).
- 2026-11-25 · EN QA (ronda de cierre) · claude · rebasado sobre develop con T-201 (358576c3); envoltorios de T-201 (H-02 se cierra solo); `TYPE_CHECKING` en la prueba; H-01 corregido en los seis sitios; ruff 2797 → 2735; commit «T-203 cierre: …».
- 2026-11-25 · ronda de cierre verificada · APTO sin nada abierto (`qa.md`).
- 2026-11-25 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
