# T-202 · Entorno: stubs de tipos para mypy (import-untyped del Bloque A)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (25-11-2026, QA r02 APTO y ronda de cierre verificada, sin hallazgos abiertos) |
| Pieza | entorno (`tools/requisitos_entorno.txt`, `.docs/scripts/preparar_entorno.sh`); en el Bloque A, solo anotaciones de tipos en tres módulos del Motor |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-24: tickets de cuotas de calidad (T-201, T-202, T-203), pedidos por el operador; sin decisión nueva |
| Deuda técnica | T-202 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

mypy sin `--ignore-missing-imports` da 49 errores `[import-untyped]` en el Bloque A (y 23 en A-Forex y 7 en B): librerías sin tipos (`yaml`, `jsonschema`, `pandas`, `scipy`, `openpyxl`). Se instalan sus paquetes de stubs con versión fijada en `tools/requisitos_entorno.txt` y `preparar_entorno.sh` los instala, eligiendo el conjunto que más los baja **sin que suba ninguna cuota de mypy** (A 102, A-Forex 174, B 159) ni cambie ningún comportamiento.

## Fuentes

- Encargo del operador del 24-11-2026 (T-202) y las reglas comunes de los tickets de cuotas (T-201 a T-203): sin cambios de comportamiento, salidas idénticas a develop, sin `# type: ignore`, `cast` ni `Any` para tapar errores, sin relajar la configuración de mypy, sin tocar los ficheros de las ramas abiertas (pull request 3 de Astra y T-196) ni el corpus.
- T-96 y T-137: el entorno reproducible (`tools/requisitos_entorno.txt`, `preparar_entorno.sh` y `--comprobar`, que exige que todo lo instalado esté fijado y todo lo fijado instalado).
- `tools/check_all.sh`: el gate cuenta las líneas de `mypy --ignore-missing-imports --no-error-summary` por paquete.

## Alcance

- **Entra:**
  - Medir, con el `.venv` propio de la copia, cada stub por separado y juntos: las tres cuotas como las mide el gate y los `[import-untyped]` sin la opción (tabla en `analisis-tecnico.md`).
  - Fijar los stubs elegidos y sus dependencias nuevas en `tools/requisitos_entorno.txt`, con versiones de la serie de cada librería fijada; `preparar_entorno.sh` los instala; una prueba de `pruebas_preparar_entorno.py` comprueba que todo stub fijado está en la orden de instalación.
  - Con scipy-stubs, mypy ve cuatro errores en ficheros del Bloque A que se pueden tocar (no están en ninguna rama abierta): se corrigen solo con tipos (un `Literal`, dos funciones con tipos en lugar de dos `lambda` y un nombre de variable), sin cambiar ningún valor.
  - La prueba de equivalencia (`equivalencia.py`) y los mutantes de cada cambio no mecánico (`mutantes.py`); una prueba nueva, `tests/test_t202_alternativas_rangos.py`, porque el mutante M01 quedaba vivo con la suite de antes.
- **No entra:**
  - pandas-stubs y types-openpyxl: suben cuotas por errores en A-Forex y B, que este ticket no puede tocar (anotados con su número).
  - types-requests: ningún bloque importa `requests`.
  - Los errores `[import-not-found]` (`yfinance` y los módulos de referencia `htNN_*`): no son de stubs.
  - El mapa del plan de pruebas, las evidencias y `docs/incidencias.md`: los cambian otras ramas abiertas (T-196, pull request 3) y no hay caso del plan afectado. La decisión `[PROPUESTO]` queda en este README (INC-T202-01, abajo) para pasarla a `docs/incidencias.md` al integrar.

## Diseño

- **Contratos y esquemas:** ninguno cambia. **Estado persistido:** no cambia.
- **Números:** ninguno nuevo. Las versiones de los stubs no son parámetros: salen de la serie de cada librería fijada (PyYAML 6.0.3 → types-PyYAML 6.0.12.x; jsonschema 4.26.0 → types-jsonschema 4.26.0.x; scipy 1.18.1 → scipy-stubs 1.18.1.x), la publicación más reciente de esa serie el 24-11-2026.
- **Cómo falla cerrado:** `preparar_entorno.sh --comprobar` falla si falta un stub fijado o si hay uno instalado sin fijar (ya lo hacía, T-137); la prueba nueva falla si se fija un stub que el script no instala. Un `.venv` sin los stubs (el de develop) da «falta …» hasta que se ejecuta el script, que los añade sin cambiar ninguna otra versión.
- **INC-T202-01 `[PROPUESTO]`**, copiada a `docs/incidencias.md` en el cierre, ya integrado T-204. En la r01 y la r02 solo estaba aquí, porque `docs/incidencias.md` lo cambiaban otras ramas abiertas:
  1. «El conjunto que más baje el total» se lee como el que más `[import-untyped]` quita sin que suba ninguna de las tres cuotas del gate. El gate no los cuenta (usa `--ignore-missing-imports`), así que **las cuotas no bajan**: se quedan en 102 / 174 / 159, con exactamente los mismos errores que develop.
  2. Un stub cuyos errores nuevos caen solo en ficheros del Bloque A que se pueden tocar se acepta si se corrigen sin cambiar el comportamiento (scipy-stubs: 4 errores, 56 líneas de mypy contando las notas). Uno que sube A-Forex o B no se acepta.
  3. Versiones: la más reciente de la serie de cada librería (arriba).
  4. (r02, QA r01 H-03) **El gate exige el entorno fijado para medir mypy.** `tools/check_all.sh` ejecuta
     `preparar_entorno.sh --comprobar` antes de mypy. Si falla (falta un stub o cualquier versión fijada, o hay un paquete sin
     fijar), muestra su salida y cada gate de mypy sale ✗ con «el .venv no coincide con tools/requisitos_entorno.txt (stubs
     incluidos): ejecuta .docs/scripts/preparar_entorno.sh», sin ejecutar mypy; el total de gates no cambia. Motivo: sin
     los stubs, mypy cuenta menos y el gate pasaba en verde código que, con ellos, lo pone en rojo (fallo silencioso).
     Se comprueba el fichero entero y no solo los stubs porque las cuotas dependen también de otras versiones (T-96:
     arch 9.0.0). Variante más estrecha, si el operador la prefiere: comprobar solo los `types-*` y `*-stubs`.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Un stub sube una cuota | Gate en rojo | Medido stub a stub y juntos; solo se fijan los que dejan las tres en su valor |
| `pip install` de un stub cambia una versión fijada | Entorno distinto del de los demás gates | `-c tools/requisitos_entorno.txt`; comparado el `pip freeze` antes y después: solo altas; `--comprobar` conforme con 54 |
| El `.venv` común y los de otras copias no tienen los stubs | `--comprobar` falla en ellos y su mypy no mide lo mismo | El script los añade sobre un `.venv` existente (probado); el operador lo ejecuta al integrar (`handoff.md`). Sin los stubs las cuotas siguen igual (mismo conjunto de errores) |
| Las anotaciones cambian un resultado | Comportamiento distinto | Prueba de equivalencia byte a byte contra develop y mutantes de cada línea tocada |
| Conflictos con las ramas abiertas | Fusión con conflictos | Ningún fichero de la lista prohibida, salvo la fila de la deuda técnica que pide el encargo (en la zona del entorno, T-137, lejos de las filas que añaden las otras ramas) |

## Al integrar (QA r02, H-04)

La rama que entre en segundo lugar resuelve la fusión con T-204, que quitó el Bloque A Forex. T-204 entró antes, en `eda55e1b`, y la resolución está aplicada en el commit de cierre:
- **`tools/check_all.sh`:** se fusiona sin conflictos. El bucle de mypy queda `for i in "${!PAQUETES[@]}"`, el de T-204, con las dos inserciones de T-202.
- **`revisores/r07_resolucion_fusion_t204.diff`:**
  - la raíz falsa de `.docs/scripts/pruebas_gate_bloques.py` lleva `preparar_entorno.sh`, `common.sh`, el fichero de versiones real y un `pip freeze` que coincide con él; sin eso, los gates de mypy salían ✗ y fallaban 3 pruebas de T-204;
  - el comentario de `tools/requisitos_entorno.txt` deja de nombrar el Forex: «pandas-stubs (A +26, B +13)».
- **Comentarios de `preparar_entorno.sh`:** se quedan los textos de T-204 («los dos ejecutores») con los añadidos de T-202.
- **Línea base de `.docs/scripts`:** la de develop más las 6 pruebas de T-202, 460 + 6 = 466.
- **`docs/incidencias.md`:** INC-T202-01, con las cuatro decisiones.
- **Fuera del commit (lo hace el coordinador):** ejecutar `.docs/scripts/preparar_entorno.sh` en el `.venv` común y avisar a Astra para que lo ejecute en el suyo. Hasta entonces, los gates de mypy de esos entornos salen ✗ (decisión 4).

## Criterios de aceptación (binarios)

1. CA-1: con los stubs fijados, las tres cuotas de mypy del gate no suben (A ≤ 102, A-Forex ≤ 174, B ≤ 159) y los errores son los mismos que en develop (salvo el número de línea).
2. CA-2: los `[import-untyped]` bajan: A de 49 a 27, A-Forex de 23 a 15 y B de 7 a 6. Los stubs que subirían una cuota no se fijan y quedan anotados con su número.
3. CA-3: `tools/requisitos_entorno.txt` fija cada stub y sus dependencias nuevas; `pip install` no cambia ninguna otra versión fijada.
4. CA-4: `preparar_entorno.sh` instala los stubs, desde cero y sobre un `.venv` sin ellos, y `--comprobar` da conforme; una prueba falla si se fija un stub que el script no instala, con cualquier grafía que pip acepte (r02, H-02).
5. CA-5: el comportamiento no cambia: ciclo mock, backtest del README, una petición, una consulta y las fichas tocadas dan lo mismo que develop, byte a byte salvo rutas y latencias.
6. CA-6: cada cambio no mecánico tiene sus mutantes muertos, también el residuo SVI con pesos (r02, H-01); ruff no sube (2806); `./tools/check_all.sh` completo en verde (12/12) con el `.venv` propio de la copia.
7. CA-7 (r02, H-03): con un `.venv` que no coincide con `tools/requisitos_entorno.txt`, los gates de mypy salen ✗ con su motivo, sin ejecutar mypy, y el total de gates no cambia; con el entorno conforme, salen ✓.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Medición stub a stub y juntos (`analisis-tecnico.md`) | medida | CA-1, CA-2 |
| `pip freeze` antes y después; `preparar_entorno.sh --comprobar` | entorno | CA-3 |
| `preparar_entorno.sh` desde cero y sobre un `.venv` de develop; `pruebas_preparar_entorno.py::test_t202_el_script_instala_cada_stub_de_tipos_fijado` | entorno, fallo cerrado | CA-4 |
| `equivalencia.py` (develop con su entorno frente a la rama con el suyo) | equivalencia, regresión | CA-5 |
| `mutantes.py` (8) y `tests/test_t202_alternativas_rangos.py` (8 casos) | robustez de las pruebas | CA-6 |
| r02: `tests/test_t202_svi.py` (H-01), filtro normalizado en `pruebas_preparar_entorno.py` (H-02), `.docs/scripts/pruebas_gate_entorno.py` (H-03, 5 casos); mutantes M09 a M12 | regresión, fallo cerrado | CA-4, CA-6, CA-7 |
| `./tools/check_all.sh` | gate | CA-1, CA-6 |

## Scripts

`.docs/tickets/T-202/equivalencia.py` (comparación de salidas) y `.docs/tickets/T-202/mutantes.py`; `.docs/scripts/preparar_entorno.sh [--comprobar]`; `.docs/scripts/pruebas_scripts.sh`.

## Registro

- 2026-11-24 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-24 · PLANIFICADO · claude · medición de los cinco stubs y plan
- 2026-11-24 · EN CURSO · claude · stubs fijados, script y cuatro anotaciones en el Motor del Bloque A
- 2026-11-24 · EN QA (r01) · claude · equivalencia sin diferencias, 8 mutantes muertos, gate completo; commit local
- 2026-11-25 · EN QA (r02: QA r01 NO APTO) · claude · H-01, H-02 y H-03 corregidos con sus pruebas (decisión 4 de INC-T202-01); 12 mutantes muertos; gate completo; commit local
- 2026-11-25 · EN QA (cierre: QA r02 APTO, pendiente de H-04) · claude · rebase sobre develop con T-204, resolución r07, comentarios sin Forex, línea base 466, INC-T202-01 en `docs/incidencias.md`, traspaso y README corregidos; gate completo; commit local
- 2026-11-25 · ronda de cierre verificada · APTO sin nada abierto (`qa.md`).
- 2026-11-25 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`; `preparar_entorno.sh` ejecutado en el `.venv` común.
