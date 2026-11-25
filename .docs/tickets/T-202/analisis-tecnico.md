# T-202 · Análisis técnico

## Causa

El gate mide mypy con `--ignore-missing-imports` (`tools/check_all.sh`), que trata como `Any` todo lo que viene de una librería sin tipos y no cuenta el aviso. Sin la opción, mypy dice `Library stubs not installed for …` `[import-untyped]` en cada import: 49 en A (pandas 27, scipy 14, jsonschema 7, yaml 1), 23 en A-Forex y 7 en B (openpyxl 3, pandas 3, yaml 1). Con los stubs, mypy deja de ver `Any` y comprueba las llamadas a esas librerías: pueden salir errores nuevos.

## Medición

Con un `.venv` propio de la copia (creado con `python3.12 -m venv` por `preparar_entorno.sh`, nunca el común), instalando cada conjunto con `-c tools/requisitos_entorno.txt`, midiendo y desinstalando (script de trabajo fuera del repositorio; el `.venv` vuelve cada vez a su `pip freeze` de partida). «Gate» es lo que cuenta `check_all.sh`; «untyped», los `[import-untyped]` sin la opción.

| Stubs | Gate A | Gate A-Forex | Gate B | untyped A / A-Forex / B | Dependencias nuevas | ¿Se fija? |
| --- | --- | --- | --- | --- | --- | --- |
| ninguno (develop) | 102 | 174 | 159 | 49 / 23 / 7 | — | — |
| types-PyYAML 6.0.12.20261122 | 102 | 174 | 159 | 48 / 22 / 6 | ninguna | sí |
| types-jsonschema 4.26.0.20261006 | 102 | 174 | 159 | 42 / 21 / 7 | ninguna (`referencing` ya estaba) | sí |
| scipy-stubs 1.18.1.1 | **158** (+56) | 174 | 159 | 35 / 18 / 7 | optype 0.19.0, numpy-typing-compat 20260602.2.5 | sí, tras corregir 4 errores en A (abajo) |
| pandas-stubs 3.1.0.261029 | **128** (+26) | **196** (+22) | **172** (+13) | 22 / 8 / 4 | ninguna | **no**: sube A-Forex y B, que no se tocan |
| types-openpyxl 3.1.5.20261122 | 102 | 174 | **160** (+1) | 49 / 23 / 4 | ninguna | **no**: sube B (`ht10_anexo_datos.py`, `Workbook.remove` con un `Optional`) |
| yaml + jsonschema | 102 | 174 | 159 | 41 / 20 / 6 | — | — |
| los cinco | 184 | 196 | 173 | 0 / 0 / 0 | — | — |
| **elegido**: yaml + jsonschema + scipy, con las 4 correcciones | **102** | **174** | **159** | **27 / 15 / 6** | optype, numpy-typing-compat | — |

Con el conjunto elegido, los errores del gate son **los mismos** que en develop en los tres paquetes (comparados línea a línea quitando el número de línea). Ninguna instalación cambió una versión fijada: el `pip freeze` solo tiene altas.

Lo que queda: los 27 `[import-untyped]` de A son de pandas (y `pandas.tseries.holiday`); los de A-Forex, pandas; los de B, pandas y openpyxl. pandas-stubs suma 26 líneas en A (`operaciones.py` 10, `fichas_p2.py` 7, `fichas_reales.py` 5, `fichas_fon_der.py` 2, `fichas_mon_idx.py` 1, `herramientas/ht01_datos.py` 1), 22 en A-Forex (`motor/operaciones.py`, `herramientas/ht01_datos.py`, `evaluador.py`) y 13 en B (`herramientas/ht01_datos.py`, `motor.py`, `backtest.py`): para fijarlo hace falta un ticket de A-Forex y otro de B.

## Los cuatro errores de scipy-stubs en el Bloque A

Los 56 son 4 errores y 52 notas (las variantes de cada sobrecarga, que el gate también cuenta). Ninguno es un fallo de verdad: SciPy acepta lo que se le pasa; los stubs piden un tipo más estrecho o mypy no infiere el de una `lambda`.

| Fichero, línea | Error | Corrección (solo tipos, sin cambiar ningún valor) |
| --- | --- | --- |
| `motor/fichas_series.py`, ST-INF-001 (`stats.wilcoxon`, `stats.mannwhitneyu`) | `alternative=_SCIPY_ALT[alt]` es `str` y los stubs piden `Literal["two-sided", "less", "greater"]` (2 errores) | `_SCIPY_ALT: dict[str, Literal["two-sided", "greater", "less"]]`, con los mismos valores |
| `motor/fichas_series.py`, ST-INF-001, mann_whitney | Al tipar lo anterior, `res` es `WilcoxonResult` en una rama y `MannwhitneyuResult` en la otra | `res_u` en la rama de mann_whitney (mismo uso: `statistic` y `pvalue`) |
| `motor/fichas_reales.py`, `_glm_theta` (ALT-DESMOOTH-001, GLM) | `optimize.minimize(…, constraints=[{"type": "ineq", "fun": lambda t: 1 - np.sum(t)}])`: mypy no casa el diccionario con el `TypedDict` de la restricción con una `lambda` dentro | `def holgura(t: np.ndarray) -> np.float64: return 1 - np.sum(t)`, la misma expresión, y `"fun": holgura` |
| `motor/fichas_fon_der.py`, `f_der_skew` (DER-SKEW-001, SVI) | `optimize.least_squares(lambda x: _svi(x, k)[0] - w_obs, …)`: «Cannot infer type of lambda» | `def residuo(x: np.ndarray) -> np.ndarray: return _svi(x, k)[0] - w_obs`, la misma expresión |

Ningún `cast`, `Any` ni `# type: ignore`; la configuración de mypy no cambia. Los tres ficheros no están en la lista de ficheros de las ramas abiertas (pull request 3 de Astra y T-196).

## Archivos cambiados

| Archivo | Cambio |
| --- | --- |
| `tools/requisitos_entorno.txt` | Cinco líneas fijadas (types-PyYAML, types-jsonschema, scipy-stubs, optype, numpy-typing-compat) en su sitio alfabético, sin mover las demás, y un comentario con lo que no se fija y por qué |
| `.docs/scripts/preparar_entorno.sh` | La orden de instalación añade `types-PyYAML types-jsonschema scipy-stubs` (las dependencias llegan solas, con su versión fijada por `-c`) |
| `.docs/scripts/pruebas_preparar_entorno.py` | `test_t202_el_script_instala_cada_stub_de_tipos_fijado`: con el fichero real, todo stub fijado está en la orden de instalación y `--comprobar` da conforme |
| `.docs/scripts/linea_base_pruebas.txt` | 399 → 400 |
| `bloque_a/11_Ejecutor/bloque_a/motor/fichas_series.py`, `fichas_reales.py`, `fichas_fon_der.py` | Las cuatro correcciones de tipos de la tabla |
| `bloque_a/11_Ejecutor/tests/test_t202_alternativas_rangos.py` | Nueva (8 casos): ST-INF-001 pasa a SciPy la alternativa declarada en wilcoxon (una muestra y pareada) y mann_whitney, contra SciPy como oráculo, y el sentido de «mayor» y «menor» |
| `.docs/tickets/T-202/` | Ticket, `equivalencia.py` y `mutantes.py` |
| `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | Fila T-202 |

## Decisiones y desviaciones

- **Las cuotas no bajan.** El gate no cuenta los `[import-untyped]`; los stubs solo pueden dejar la cuenta igual o subirla. Se dejan como estaban (`tools/cuotas.txt` sin cambios).
- **scipy-stubs se acepta con cuatro correcciones en A.** El encargo prohíbe instalar un stub que suba una cuota y arreglar errores nuevos en ficheros que no se pueden tocar; estos cuatro están en ficheros que sí. Decisión 2 de INC-T202-01.
- **INC-T202-01 va en el README del ticket**, no en `docs/incidencias.md`, porque ese fichero lo cambian el pull request 3 y T-196 (regla de cuotas). Al integrar, se copia allí.
- **Prueba nueva.** El mutante M01 (cambiar «mayor» por «menor» en `_SCIPY_ALT`) quedaba vivo con la suite de antes: ninguna prueba usaba una alternativa unilateral en los contrastes de rangos. Es un hueco anterior a T-202 (el mismo mutante sobre develop también vive); la prueba pasa en develop y en la rama.
- **No se regeneran las evidencias ni el mapa** (los cambian T-196 y el pull request 3; no hay caso del plan afectado).

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba de regresión | Mutante |
| --- | --- | --- | --- |
| H-03 (media): el gate no exigía los stubs; un `.venv` sin ellos daba verde lo que con ellos es rojo | `tools/check_all.sh`, solo en el bloque de mypy: antes del bucle, `preparar_entorno.sh --comprobar`; si falla, muestra su salida y cada gate de mypy sale ✗ con su motivo (`TOTAL` y `FAILED`), sin ejecutar mypy. Decisión 4 de INC-T202-01 `[PROPUESTO]` | `.docs/scripts/pruebas_gate_entorno.py` (5 casos): `check_all.sh` real en una raíz temporal con un `.venv` falso y el fichero de versiones real. Sin scipy-stubs, types-PyYAML o types-jsonschema, o con un paquete sin fijar, los gates de mypy salen ✗, mypy no se llama, fallan tantos como paquetes y el total es el mismo que con el entorno conforme; conforme, ✓. Los paquetes se leen de `PAQUETES=(…)` del propio script. Con el `check_all.sh` de la r01, 4 de 5 fallan | M12 (la comprobación siempre da bien): muerto |
| H-01 (baja): el residuo SVI con pesos (RQ05) vivía | `tests/test_t202_svi.py`, la prueba de `revisores/r03_…`: con una sonrisa que no es SVI, el RMSE publicado es el de los parámetros publicados sin pesos | pasa en la rama; falla con el mutante | M09 (= RQ05): muerto; con `--solo-suite-anterior`, vivo |
| H-02 (baja): la prueba del script filtraba los stubs antes de normalizar el nombre (`types_openpyxl`, `Types-openpyxl` pasaban) | El cambio de `revisores/r04_correccion_propuesta_H02.diff`: filtro sobre el nombre normalizado | `pruebas_preparar_entorno.py`, 10 de 10 | M10 y M11 (= RQ11 y RQ12): muertos |

Para facilitar la fusión con T-204, que quita A-Forex y cambia `for i in 0 1 2` por `for i in "${!PAQUETES[@]}"`, el cambio de `check_all.sh` no toca esa línea ni las contiguas. Va en dos sitios del bloque de mypy: antes del `if command -v .venv/bin/mypy` y después de `paq=…`. `git merge-file` con el `check_all.sh` de la copia de T-204 no da conflictos. La línea de la tabla del gate en `CLAUDE.md` no se toca, porque T-204 también la cambia.

## Límites conocidos

- Los entornos que ya existen (el `.venv` común y los de otras copias) no tienen los stubs: `--comprobar` dará «falta …» hasta que se ejecute `preparar_entorno.sh`, que los añade. En la r01 esto decía que «no se rompe ningún gate en marcha»: solo valía para el código de hoy (QA r01, H-03). Desde la r02, con un `.venv` así los tres gates de mypy salen ✗ y piden ejecutar el script (decisión 4 de INC-T202-01): el gate falla cerrado en vez de contar menos.
- Las versiones de los stubs dependen de la de su librería: al subir PyYAML, jsonschema o scipy hay que subir su stub y volver a medir.

## Comandos

```bash
# en la copia, con su .venv propio (nunca el común)
.docs/scripts/preparar_entorno.sh && .docs/scripts/preparar_entorno.sh --comprobar
for q in bloque_a bloque_a_forex bloque_b; do .venv/bin/mypy --ignore-missing-imports --no-error-summary $q/11_Ejecutor/$q | wc -l; done
for q in bloque_a bloque_a_forex bloque_b; do .venv/bin/mypy --no-error-summary $q/11_Ejecutor/$q | grep -c import-untyped; done
.venv/bin/python -m pytest -q .docs/scripts/pruebas_preparar_entorno.py
python3 .docs/tickets/T-202/equivalencia.py --base <copia de develop> --base-python <python de develop> \
  --nuevo . --nuevo-python .venv/bin/python --trabajo <carpeta fuera del repositorio>
cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-202/mutantes.py .
```
