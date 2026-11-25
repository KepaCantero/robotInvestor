# T-167 · QA independiente

- **Revisor:** claude, subagente revisor nuevo (no implementó; solo plan, código y pruebas) · **Ronda:** r01 · 17-11-2026

## Reproducción desde limpio

Copia propia: `git worktree add --detach <scratchpad>/qa167 HEAD` (HEAD = `e35d284`), con los siete cambios sin commit de
T-167 copiados desde el árbol principal (`pyproject.toml`, `bloque_a/__init__.py`, `tests/test_t167_version.py`,
`docs/incidencias.md`, `CLAUDE.md`, la fila T-167 de la deuda y el ticket). Venv `/home/user/robotinvestor/.venv`. Por
indicación del coordinador (otros agentes trabajan a la vez) no se pasaron la suite completa de A ni `./tools/check_all.sh`.
El `conftest.py` de A pone la raíz de la copia al principio de `sys.path`: la prueba importa el paquete de la copia y no el
editable instalado del árbol principal (lo confirma la sonda de `r01_01`).

| Orden (en la copia) | Resultado |
| --- | --- |
| `pytest -q tests/test_t167_version.py tests/test_t113_deuda.py tests/test_v51.py` (versión, `requires-python` del pyproject, subcomandos V1.2) | 121 passed |
| `.docs/scripts/pruebas_scripts.sh` | 231 passed (línea base respetada) |
| `tools/corpus_integridad.py` · `nfc_check.py` · `secrets_scan.py` · `refs_vivas.py` · los 3 YAML | 696 archivos íntegros · NFC · sin secretos · refs vivas · YAML ok |
| ruff de los tres ejecutores · mypy `bloque_a` | 2813 (cuota 2813) · 109 (cuota 109): iguales |
| `ruff check` de `test_t167_version.py` y `__init__.py` | sin avisos |
| `.docs/scripts/preparar_entorno.sh --comprobar` (árbol principal) | conforme (49 paquetes): compara con `pip freeze --exclude-editable`, la versión del propio paquete no entra |

Script del revisor (`revisores/`, ronda r01):

- `r01_01_mutantes_version.py` (desde `bloque_a/11_Ejecutor` de una copia; restaura siempre los originales): original y sonda
  de origen del paquete pasan; **10/10 mutantes caen**: M01 pyproject a 1.1.0, M02 `__init__` a 1.1.0, M03 los dos a 1.1.0
  (coinciden entre sí, no con el README), M04 README «(V1.1)», M05 README «(V1.3)», M06 título sin versión, M07 pyproject
  1.2.1, M08 `__version__ = "1.2"`, M09 con espacio final, M10 los dos a 2.0.0. El control M11 (los tres a 1.3, coherente)
  pasa, como debe.

## Dependencias de la cadena «1.1.0»

`grep -rn '1\.1\.0'` en todo el repo (sin `.git`, `.venv` ni `99_Historico*`): fuera del propio ticket, la deuda y el registro
de decisiones solo aparece en `dashboard/consola_n/package-lock.json` (paquetes npm de Radix) y en
`sistema_global/marco_comun_c/pruebas/pruebas_motor_t26.py` (versión de un modelo de prueba): ninguno es el Bloque A. Ningún
código, prueba, golden ni script de `.docs/scripts` lee `bloque_a.__version__` ni `importlib.metadata` del paquete (el
registro de experimentos no lo usa; `preparar_entorno.sh` excluye los editables al comparar). El CLI no tiene `--version`.
Los ficheros tocados no están en `tools/corpus_manifest.txt`. El entorno compartido sigue con metadatos 1.1.0
(`__editable___bloque_a_1_1_0_finder.py`) hasta reinstalar, como dice la nota de INC-001; nada depende de eso.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · `pyproject.toml` y `__version__` dicen 1.2.0 | sí | diff; `python -c "import bloque_a"` en la copia: 1.2.0 |
| CA-2 · la prueba pasa y falla si uno vuelve a 1.1.0 o deja de coincidir con el README | sí | 2 passed; `r01_01`: 10/10 mutantes caen, el control coherente pasa |
| CA-3 · INC-001 resuelta con su motivo; INC-002 abierta | sí | nota en `docs/incidencias.md` (motivo: delegación, `Decisiones_del_operador_Bloque_A.md` §1, fila de INC-001); INC-002 sin cambios |
| CA-4 · gate en verde, cuotas iguales | sí, en lo pasado | gates ligeros en verde; ruff 2813 y mypy A 109 iguales a la cuota (gate completo no pasado, por indicación) |

Texto: la nota de INC-001 es exacta (las «tres» son README, pyproject y `__version__`; los metadatos instalados siguen en
1.1.0 hasta reinstalar, comprobado con `importlib.metadata`; `preparar_entorno.sh` reinstala con `pip install -e`). La trampa
de `CLAUDE.md` es exacta (A 1.2.0 desde T-167; A-Forex 1.0.0 con README «V1.0, actualizado V1.1»).

Invariantes: no hay F/G, LLM, controles ni estado en juego; ningún número del Anexo A; la decisión está delegada y registrada
(`Decisiones_del_operador_Bloque_A.md` §1); sin secretos; deuda al día (T-167 EN QA).

Observaciones sin acción: el comentario de cabecera de `config/por_defecto.yaml` («(V1.1)») y la cabecera de
`tests/MAPA_PLAN_DE_PRUEBAS.md` son rótulos históricos de la entrega, no declaran la versión del paquete; el texto original de
INC-001 cita `bloque-a --version`, que no existe (es de 03-11 y la nota nueva no lo repite).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `head -1 bloque_a/11_Ejecutor/bloque_a/__init__.py` | El fichero que ahora dice `__version__ = "1.2.0"` conserva en su docstring «· V1.1 ·»: el mismo fichero se contradice | En `bloque_a/11_Ejecutor/bloque_a/__init__.py`, línea 1, «Ejecutor programático del Bloque A (Robot Investor) · V1.1 · Versión óptima V5.0» → «Ejecutor programático del Bloque A (Robot Investor) · V1.2 · Versión óptima V5.0» (el resto igual) | corregido (ronda de cierre) |
| H-02 | baja | `sed -n 24p sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` | La decisión dice que solo `pyproject.toml` pasa a 1.2.0 «sin otro cambio», y en «Dónde» no figura `__init__.py`; T-167 también cambia `bloque_a.__version__` | En esa fila, «`bloque_a/11_Ejecutor/pyproject.toml` pasa de 1.1.0 a 1.2.0, la que dice su README, sin otro cambio (T-167)» → «`bloque_a/11_Ejecutor/pyproject.toml` y `bloque_a.__version__` pasan de 1.1.0 a 1.2.0, la que dice su README, sin otro cambio (T-167)»; y en la última columna añadir «; `bloque_a/11_Ejecutor/bloque_a/__init__.py`» tras «`bloque_a/11_Ejecutor/pyproject.toml`» | corregido (ronda de cierre) |
| H-03 | baja | Leer `pruebas.md` | CA-2 solo tiene «comprobado a mano antes del cambio» (no cubre `__version__` ni el desacuerdo con el README) y CA-4 no tiene evidencia | Añadir a la tabla de `pruebas.md` dos filas: «Mutantes de la QA r01 (`revisores/r01_01_mutantes_version.py`): 10/10 caen (pyproject o `__init__` a 1.1.0, los dos a 1.1.0, README V1.1/V1.3/sin versión, 1.2.1, "1.2", espacio final, 2.0.0); el control coherente (los tres a 1.3) pasa (CA-2)» y «Gates ligeros (corpus 696, NFC, secretos, refs vivas, YAML), ruff 2813 y mypy A 109, iguales a la cuota (CA-4; QA r01)» | corregido (ronda de cierre) |

## Veredicto

**APTO** · CA-1 a CA-4 se cumplen; la prueba ata pyproject, `__version__` y README y mata los diez mutantes; nada del repo
depende de «1.1.0» del Bloque A; textos de INC-001 y `CLAUDE.md` exactos. Ningún hallazgo crítico, alto ni
medio. Por la regla del operador, H-01, H-02 y H-03 (bajos) se subsanan en este ticket con una ronda de cierre (las
correcciones de arriba) antes de pasar T-167 a CERRADO; tras H-01, repetir `ruff check` y mypy de `bloque_a` (cuotas iguales).

## Ronda de cierre

Revisada en el árbol principal el 17-11-2026 por el mismo revisor, solo sobre los arreglos de H-01 a H-03.

| ID | Comprobación | Estado |
| --- | --- | --- |
| H-01 | `head -1 bloque_a/11_Ejecutor/bloque_a/__init__.py`: «· V1.2 · Versión óptima V5.0», el resto igual. `ruff check` del fichero sin avisos; mypy `bloque_a` 109 (cuota 109) | corregido |
| H-02 | Fila 24 de `Decisiones_del_operador_Bloque_A.md`: «`pyproject.toml` y `bloque_a.__version__` pasan de 1.1.0 a 1.2.0…» y `bloque_a/11_Ejecutor/bloque_a/__init__.py` en «Dónde»; el diff del fichero es solo esa línea | corregido |
| H-03 | `pruebas.md` con las dos filas (mutantes de r01 para CA-2; gates ligeros y cuotas para CA-4) | corregido |

Repetidos: `tests/test_t167_version.py` 2 passed; `revisores/r01_01_mutantes_version.py` en una copia nueva de HEAD con los
tres ficheros del paquete del árbol principal: 11/11 como se esperaba (10 mutantes caen, el control pasa); `refs_vivas.py` en
verde.

**Veredicto final: APTO.** T-167 pasa a CERRADO (README del ticket y fila de la deuda).
