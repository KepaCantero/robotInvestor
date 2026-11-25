# T-202 · QA independiente

- **Revisor:** claude (revisor nuevo; no implementó T-202 ni leyó su conversación) · **Ronda:** r01 · 25-11-2026
- **Código revisado:** `wip/t202` (c045382c) sobre 7f92064a, y su fusión con el develop actual (d23afe04).

## Reproducción desde limpio

- Worktree propio desde `wip/t202`. **`.venv` propio, nunca el común**: primero con el `preparar_entorno.sh` y el fichero de versiones de develop (desde cero, 49 paquetes conformes), después con los de la rama encima, sobre el mismo `.venv`. Así queda probado el caso de un `.venv` que ya existe:
  - `--comprobar` antes de reinstalar sale con 1 y lista 5 «falta …» (numpy-typing-compat, optype, scipy-stubs, types-jsonschema, types-pyyaml);
  - la reinstalación tarda 12 s y termina con «entorno conforme: 54 paquetes»;
  - `pip freeze` antes y después: solo esas 5 altas, ninguna versión cambia;
  - `pip check`: sin dependencias rotas.
- **Desde cero con el script de la rama**, en una copia de la fusión con d23afe04: 54 conformes, con el mismo `pip freeze` byte a byte. El primer intento falló con `No space left on device`: el disco de la máquina estaba lleno, no es un fallo del script, que falló cerrado con «pip no pudo instalar». Se liberó espacio y se repitió.
- **Gate del implementador** (`scratchpad/gate_t202.log`): 12/12, rc=0 (ruff 2806; mypy 102, 174 y 159; pytest A 8445, A-Forex 68, B 176).
- **Pruebas:**
  - `test_t202_alternativas_rangos.py` junto con sus vecinas (`test_fase2_series.py`, `test_fase2_reales.py`, `test_fase1_fon_der.py`): 1171 pasan.
  - La prueba nueva pasa también sobre develop. Es lo esperado: es de cobertura, porque el comportamiento no cambia.
  - `.docs/scripts/pruebas_scripts.sh` en la fusión: 400 pasan, igual a la línea base.
- **`equivalencia.py`** (develop con el `.venv` común, sin stubs, frente a la rama con mi `.venv`): 107 ficheros iguales y 0 diferencias.
- **`mutantes.py`:** 8 de 8 muertos. Con `--solo-suite-anterior`, M01 queda VIVO y M02 muere, como dice `pruebas.md`.

## Mediciones propias (`scratchpad/qa202_mypy.sh`, mismas opciones que el gate)

| Código · entorno | Gate A | Gate A-Forex | Gate B | `[import-untyped]` A / A-Forex / B |
| --- | --- | --- | --- | --- |
| develop · sin stubs | 102 | 174 | 159 | 49 / 23 / 7 |
| develop · con stubs | **158** | 174 | 159 | 27 / 15 / 6 |
| rama · sin stubs | 102 | 174 | 159 | 49 / 23 / 7 |
| rama · con stubs | 102 | 174 | 159 | 27 / 15 / 6 |
| rama + d23afe04 · con stubs | 102 | 174 | 159 | 27 / 15 / 6 |
| rama + T-201 · con stubs | 67 (la cuota de T-201) | 174 | 159 | 27 / 15 / 6 |
| rama + T-203 · con stubs | 102 | 174 | 159 | 27 / 15 / 6 |
| rama · con stubs + pandas-stubs + types-openpyxl | 128 | 196 | 173 | — |

- Con los stubs, el gate da los mismos errores que develop en los tres paquetes; se compararon línea a línea, sin el número de línea.
- ruff: 2806 en la rama y en develop, 2735 con T-203 y 2797 con T-201, lo mismo que cada rama sola.
- Los números de pandas-stubs y types-openpyxl que da el análisis técnico se reproducen: A +26, A-Forex +22, B +14 (13 + 1).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | Tabla de arriba: 102, 174 y 159, con los mismos errores que develop |
| CA-2 | sí | 49 → 27, 23 → 15 y 7 → 6. pandas-stubs y types-openpyxl, sin fijar y con sus números (reproducidos) |
| CA-3 | sí | El `pip freeze` solo tiene altas y `pip check` está limpio. Las dependencias encajan con lo ya fijado: optype pide numpy <2.8 y typing-extensions ≥4.10; numpy-typing-compat pide numpy ≥2.5rc1 y <2.6, y numpy está en 2.5.4; types-jsonschema pide referencing 0.37.0, que ya estaba |
| CA-4 | sí, con H-02 | Probado desde cero y sobre un `.venv` existente. La prueba nueva deja pasar dos grafías del nombre (H-02) |
| CA-5 | sí | `equivalencia.py`: 107 iguales. `r02_entradas_raras.py`: 660 casos con entradas raras, 0 diferencias |
| CA-6 | sí, con H-01 | 8 de 8 mutantes muertos y ruff 2806, pero mi RQ05 vive (H-01). Gate 12/12 |

## Juicio de lo pedido

1. **¿Ganan algo de verdad las comprobaciones de mypy? Sí.**
   - `--ignore-missing-imports` no oculta una librería que tiene stubs: solo calla el error de importación de las que no los tienen.
   - Con las opciones exactas del gate, `r05_sonda_stubs.py` mete seis usos erróneos de scipy, yaml y jsonschema. Con stubs, mypy los ve los seis (8 errores). Sin stubs, ninguno. Entre ellos están un valor en español pasado tal cual a `alternative`, `alternativ=`, `sort_key=` y `validate` sin esquema.
   - Sobre el código de develop, los stubs ven 4 errores de tipos en A (de 102 a 158 líneas). Ninguno es un fallo real.
   - Lo que el gate sigue sin ver: pandas (27 en A, 15 en A-Forex, 3 en B), openpyxl (3 en B) y los `import-not-found`, que no son de stubs (8, 8 y 11).
   - **Coste:**
     - 5 paquetes, 7 MB.
     - El mypy del gate con la caché vacía tarda unos 25 s más en A, en una máquina cargada (de 60 a 85 s). Con la caché llena, 1 s.
     - numpy-typing-compat ata numpy a 2.5.x y scipy-stubs va con scipy 1.18.x: subir numpy o scipy obliga a subirlos. pip lo detiene con `-c`, así que falla cerrado.
     - Cada `.venv` tiene que volver a ejecutar `preparar_entorno.sh` (12 s, solo altas).
   - **El punto débil es H-03:** el gate no exige los stubs. Un `.venv` sin ellos sigue en verde mientras otro, con ellos, se pone en rojo con el mismo código.
   - **Recomendación: integrar, con H-01, H-02 y H-03 corregidos.** H-03 es lo que convierte la ganancia en una garantía para los dos agentes y no solo para quien haya reinstalado.
2. **Los cambios de `fichas_*.py` no cambian nada, tampoco con entradas raras.**
   - `r02_entradas_raras.py` compara develop y la rama con 660 casos, con el tipo y el texto de cada rechazo y el `repr` de cada número. Da 0 diferencias. Los casos:
     - en ST-INF-001, NaN, ±inf, None, textos, booleanos, vacíos, empates, extremos, 5000 observaciones y alternativas fuera del dominio;
     - en GLM, k de −1 a 6, 2.5, «2», True y None, con series constantes, NaN, inf y escaladas a 1e±150;
     - en SVI, superficies planas, con NaN, inf o vol 0, desalineadas, desordenadas, con forward 0 o NaN, y métodos fuera del dominio;
     - todos los casos de control.
   - Además, por lectura:
     - `res` no se usa después de las ramas, así que el cambio de nombre a `res_u` no tiene efecto;
     - las funciones `holgura` y `residuo` cierran sobre las mismas variables y en el mismo sitio que las `lambda`;
     - el `Literal` no hace nada en ejecución.
3. **Las versiones son compatibles (CA-3).** Las cinco son la última de la serie de su librería en el índice. La instalación sobre un `.venv` existente no cambia nada más.
4. **Ramas abiertas y fusión:**
   - El único fichero de T-202 que está en la lista prohibida es la fila de la deuda técnica, que pide el encargo. Está en la línea 187; el pull request 3, T-196, T-201 y T-203 la cambian en las líneas 218 y siguientes.
   - `git merge-tree` con el pull request 3 y con T-196 da exactamente los mismos ficheros en conflicto que develop solo, y la fila T-202 no cae en ningún bloque de conflicto. Con T-201 y con T-203, ningún conflicto.
   - La fusión con d23afe04 (el develop actual) no tiene conflictos y mypy sigue igual (102, 174 y 159; tabla de arriba).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Prueba de regresión | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| H-01 | baja | `revisores/r01_mutantes.py RQ05`: el residuo SVI de DER-SKEW-001 multiplicado por unos pesos de 1 a 2 | Se esperaba que lo matara alguna prueba. Queda VIVO: el único caso de SVI es una superficie exactamente SVI, con residuo nulo en el óptimo, y cualquier residuo con el mismo cero da el mismo ajuste. Es un hueco anterior a T-202, pero en la línea que cambia T-202 (de `lambda` a `residuo`) | Añadir a `tests/` (por ejemplo, a `test_t202_alternativas_rangos.py` o a un `test_t202_svi.py` nuevo) la prueba de `revisores/r03_prueba_propuesta_svi.py`: con una sonrisa con un rizo determinista, que no es SVI, el `rmse_varianza_total` publicado es el de los parámetros publicados sobre la varianza observada, sin pesos (`rel_tol` 1e-9), y es mayor que 1e-6 | Pasa en la rama y en develop; falla con RQ05 (comprobado). Añadir RQ05 a `mutantes.py` como M09 | abierto |
| H-02 | baja | `revisores/r01_mutantes.py RQ11 RQ12`: fijar `types_openpyxl==…` o `Types-openpyxl==…` sin instalarlo | pip y `--comprobar` aceptan las dos grafías. La prueba promete fallar «si se fija un stub que el script no instala», y las dos quedan VIVAS: filtra con `re.match(r"types-\|[^=]+-stubs==", x)` sobre el texto antes de normalizarlo | Filtrar sobre el nombre normalizado: `nombres = {norma(x.split("==")[0].strip()) for x in pins}` y `stubs = {n for n in nombres if n.startswith("types-") or n.endswith("-stubs")}` (`revisores/r04_correccion_propuesta_H02.diff`) | Con el cambio, RQ06 a RQ12 mueren y `pruebas_preparar_entorno.py` pasa (10 de 10). Añadir RQ11 y RQ12 a `mutantes.py` | abierto |
| H-03 | media | `revisores/r05_gate_segun_entorno.sh <develop> <.venv con stubs> <.venv común>`: el mismo código de develop da 158 en el mypy de A con stubs (rojo) y 102 sin ellos (verde); la sonda da 8 errores frente a 0 | Se esperaba que el gate midiera lo mismo en todos los entornos o fallara cerrado. Pero `check_all.sh` no comprueba el entorno, y con un `.venv` sin los stubs (el común, el de Astra o cualquier copia sin reinstalar) pasa en verde código que hace fallar el gate de quien sí los tiene. Antes de T-202, un entorno distinto (arch 9.0.0) subía la cuenta, que es un fallo ruidoso. Con T-202, el entorno viejo cuenta menos, que es un fallo silencioso. `analisis-tecnico.md` («no se rompe ningún gate en marcha») solo vale para el código de hoy | En `tools/check_all.sh`, dentro del bloque de mypy y antes del bucle, ejecutar `.docs/scripts/preparar_entorno.sh --comprobar`. Si falla, mostrar su salida y marcar ✗ los tres gates de mypy con «el .venv no coincide con tools/requisitos_entorno.txt (stubs incluidos): ejecuta .docs/scripts/preparar_entorno.sh» (`TOTAL` y `FAILED`), sin ejecutar mypy. El gate sigue en 12. Es una regla nueva del gate: decisión 4 de INC-T202-01 `[PROPUESTO]`. Variante más estrecha, si el operador la prefiere: comprobar solo los `types-*` y `*-stubs` fijados. Actualizar `analisis-tecnico.md` (límites) y la línea de la tabla del gate en `CLAUDE.md` si se toca | Una prueba en `.docs/scripts/` que ejecute `tools/check_all.sh` en una copia con un `.venv` falso (como el de `pruebas_preparar_entorno.py`), cuyo `pip freeze` no tenga scipy-stubs y con mypy, ruff y pytest falsos: los tres gates de mypy salen ✗ con el mensaje. Con el `freeze` completo, salen ✓. Un mutante que quite la comprobación tiene que morir. Sube la línea base de `.docs/scripts` | abierto |

### Condición al integrar (no es un hallazgo; se verifica en la ronda de cierre)

- INC-T202-01 `[PROPUESTO]`, con la decisión 4 de H-03, se copia a `docs/incidencias.md` en el commit de integración. Hoy está en el README del ticket porque ese fichero lo cambian el pull request 3 y T-196, y la regla de los tickets de cuotas impide tocarlo.
- Se ejecuta `preparar_entorno.sh` sobre el `.venv` común y se avisa a Astra para que lo ejecute en el suyo. Con H-03 corregido, si no lo hace, su gate lo dirá.

## Scripts del revisor (`revisores/`)

- `r01_mutantes.py`: 12 mutantes propios. Mueren 10 y viven RQ05 (H-01) y RQ11 y RQ12 (H-02).
- `r02_entradas_raras.py`: comparación de develop y la rama con 660 entradas raras en las tres fichas tocadas.
- `r03_prueba_propuesta_svi.py`: la prueba de regresión de H-01.
- `r04_correccion_propuesta_H02.diff`: la corrección de H-02.
- `r05_gate_segun_entorno.sh` y `r05_sonda_stubs.py`: la reproducción de H-03.

## Veredicto

**NO APTO**: H-03 es de gravedad media. H-01 y H-02 son bajos y, por la regla del operador, también se corrigen. El resto se cumple: equivalencia byte a byte, cuotas y errores iguales, versiones compatibles, solo altas en el entorno, sin conflictos nuevos con las ramas abiertas y la fusión con d23afe04 limpia. En la ronda r02 vuelvo a ejecutar `r01_mutantes.py` (los 12 tienen que morir), `r05_gate_segun_entorno.sh` contra el `check_all.sh` corregido, la prueba nueva de H-03 con su mutante y `mutantes.py`.

---

# Ronda r02 · 25-11-2026

- **Revisor:** claude, el mismo de la r01.
- **Código revisado:** 64a0ad63, encima de c045382c. Lo comprobé en mi worktree, con mi `.venv` propio, que sigue vivo tras el reinicio del contenedor: Python 3.12.3 y `--comprobar` conforme con 54 paquetes.

## Reproducción

- **Gate del implementador** (`scratchpad/gate_t202_r02.log`): 12/12, rc=0. pytest: A 8446, A-Forex 68, B 176.
- **Pruebas en mi copia:**
  - `.docs/scripts/pruebas_scripts.sh`: 405 pasan, igual a la línea base.
  - `test_t202_svi.py` y `test_t202_alternativas_rangos.py`: 9 pasan.
  - `test_t202_svi.py` también pasa sobre develop. Es lo esperado: es de cobertura.
- **`mutantes.py`:** 12 de 12 muertos. Con `--solo-suite-anterior`, M01 y M09 quedan VIVOS y M02 muere, como dice el implementador.
- **Mis scripts de la r01, repetidos:**
  - `revisores/r01_mutantes.py`: 12 de 12 muertos. Para que RQ05 ejecute la prueba nueva, `T_FD` incluye ahora `tests/test_t202_svi.py`; es el único cambio en el script.
  - `r05`: en lugar de repetirlo, comprobé el `check_all.sh` real (abajo).
- **Por qué no repito la equivalencia:** la r02 no cambia código del ejecutor (en `bloque_a/` solo añade una prueba), así que siguen valiendo la equivalencia de la r01 (107 iguales) y `r02_entradas_raras.py`.

## H-03: el gate real, con un entorno sin stubs y con uno conforme

Usé copias de 64a0ad63 con solo la sección de lint y tipos del `check_all.sh` real:

| `.venv` | ruff | mypy A / A-Forex / B | Salida |
| --- | --- | --- | --- |
| el común, sin stubs (49 paquetes) | ✓ 2806 | ✗ ✗ ✗ | Lista los 5 «falta …» y cada gate dice «el .venv no coincide con tools/requisitos_entorno.txt (stubs incluidos): ejecuta .docs/scripts/preparar_entorno.sh»; mypy no se ejecuta |
| el mío, conforme (54 paquetes) | ✓ 2806 | ✓ 102 / ✓ 174 / ✓ 159 | Sin cambios respecto a la r01 |

- **Mutantes propios del bloque nuevo** (`revisores/r06_mutantes_gate.py`), contra `pruebas_gate_entorno.py`: mueren 5 de 7.
  - Mueren: RG01 (sin `continue`), RG02 (sin `FAILED`), RG03 (sin `TOTAL`), RG04 (sin mostrar la salida de `--comprobar`) y RG06 (la comprobación solo avisa).
  - Viven dos, los dos equivalentes:
    - RG05 quita el `2>&1`. Lo que dice `--comprobar` sale igual por stderr y el gate falla con el texto de reserva.
    - RG07 quita el texto de reserva. `preparar_entorno.sh` no tiene ningún camino que falle sin decir nada: cada salida con 1 pasa por `fallo`, por `sys.exit(...)` o por un `ERROR:` impreso.
- **¿Es razonable exigir el fichero de versiones entero? Sí.**
  - Las cuotas dependen de más que los stubs: arch 9.0.0 subía mypy (T-96).
  - T-137 ya trata como error un paquete sin fijar.
  - `--exclude-editable` deja fuera los ejecutores, así que quitar el Forex con T-204 no rompe la comprobación.
  - Cuesta 0,7 s.
  - El precio es que un paquete ajeno instalado a mano en el `.venv` (por ejemplo, ipython) pone mypy en rojo. Pero la salida dice exactamente cuál es, y arreglarlo cuesta 12 s.
  - Al integrar, el `.venv` común y el de Astra saldrán en rojo en mypy hasta ejecutar `preparar_entorno.sh`. Es lo que se busca.
- **Observación sin hallazgo, fuera del alcance:** en un entorno que no coincide, los gates de pytest siguen ejecutándose. Si algún día se quiere coherencia total, se puede aplicar la misma comprobación. No es de T-202.

## Fusión con T-204 (`wip/t204`, 123118ea)

- **`git merge-file` de `tools/check_all.sh`: sin conflictos.**
  - El bucle queda `for i in "${!PAQUETES[@]}"`, el de T-204, con las dos inserciones de T-202 dentro.
  - `cuotas.txt` tampoco da conflicto.
- **`git merge-tree` del repositorio entero: 3 conflictos, todos triviales.**
  - `.docs/scripts/linea_base_pruebas.txt`: 405 frente a 432, porque cada uno añade sus pruebas a la de 399.
  - Comentarios de `preparar_entorno.sh`: «tres ejecutores» frente a «dos».
  - La cabecera de `tools/requisitos_entorno.txt`.
- Resolví la fusión en `scratchpad/qa202r02_con_t204`: textos de T-204 con los añadidos de T-202, y línea base 399 + 6 + 33 = 438.
- **La prueba de T-202 sigue valiendo.**
  - `pruebas_gate_entorno.py` pasa con dos bloques: lee `PAQUETES`.
  - M10, M11 y M12 mueren en la copia fusionada.
- **Pero la fusión tal cual rompe 4 pruebas de T-204 (H-04):**
  - `pruebas_gate_bloques.py::test_el_gate_y_sus_scripts_no_nombran_el_forex[requisitos_entorno.txt]`: el comentario de T-202 dice «A-Forex +22».
  - `test_el_gate_completo_son_diez_comprobaciones_sobre_a_y_b` y los dos casos de `test_cada_bloque_se_mide_con_su_propia_linea_base`: la raíz falsa de T-204 no tiene `preparar_entorno.sh` ni el fichero de versiones. Con el cambio de H-03, los gates de mypy salen ✗ y aparece «Fallaron: 3» donde se esperaba 0 o 1.
- **Con la resolución de `revisores/r07_resolucion_fusion_t204.diff`**:
  - `pruebas_gate_entorno.py`, `pruebas_preparar_entorno.py` y `pruebas_gate_bloques.py` pasan (48 de 48).
  - `pruebas_scripts.sh` en la copia fusionada da 436 pasan y 2 fallan. Los dos que fallan (`test_integracion_bloque_a` y `test_h25_el_sello_no_se_sube`) necesitan un repositorio git y esa copia es un `git archive`; en mi worktree, que sí es un repositorio, pasan. 436 + 2 = 438, la línea base fusionada.
  - Lo que cambia la resolución:
    - en `_raiz_falsa` de `pruebas_gate_bloques.py`, la raíz falsa copia `preparar_entorno.sh`, `common.sh` y el fichero de versiones real, y su `python` falso responde a `pip --version` y a `pip freeze` con los paquetes fijados;
    - el comentario de `requisitos_entorno.txt` deja de nombrar el Forex: «pandas-stubs (A +26, B +13)».

## Hallazgos r02

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Prueba de regresión | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| H-01 | baja | `r01_mutantes.py RQ05` y `mutantes.py M09` | Muertos por `tests/test_t202_svi.py` | — | Pasa en la rama y en develop | **corregido** |
| H-02 | baja | `r01_mutantes.py RQ11 RQ12` y `mutantes.py M10 M11` | Muertos | — | `pruebas_preparar_entorno.py` | **corregido** |
| H-03 | media | El `check_all.sh` real con el `.venv` común | ✗ en los tres gates de mypy, con el motivo y sin ejecutar mypy; con un `.venv` conforme, ✓ | — | `pruebas_gate_entorno.py` (5 casos), M12 muerto y 5 de 7 mutantes del revisor muertos (los 2 vivos son equivalentes) | **corregido** |
| H-04 | baja | `git merge-tree wip/t202 wip/t204`, con los conflictos resueltos, y `pytest .docs/scripts/pruebas_gate_bloques.py` | Se esperaba lo que dice el traspaso: que la fusión con T-204 sale limpia. Fallan 4 pruebas de T-204: la raíz falsa no tiene `preparar_entorno.sh` y el comentario nombra el Forex. Hay además dos conflictos de comentarios que el traspaso no anuncia. Es una incompatibilidad que solo aparece al fusionar las dos ramas; falla cerrado, porque `commit.sh` ejecuta `pruebas_scripts.sh` y no deja hacer commit, pero el traspaso la oculta | En `handoff.md` y en el README de T-202 (sección «Riesgos» o «Al integrar»): la rama que se integre en segundo lugar aplica `revisores/r07_resolucion_fusion_t204.diff` (raíz falsa de `pruebas_gate_bloques.py` y comentario de `requisitos_entorno.txt`), resuelve los comentarios de `preparar_entorno.sh` y pone la línea base en la suma (399 + 6 + 33 = 438 con las ramas de hoy). Corregir también la frase «sale limpio» del traspaso: limpio solo para `check_all.sh` | En la copia fusionada: 48 de 48 en las tres pruebas del gate y del entorno, 436 + 2 que necesitan git en `pruebas_scripts.sh`, y M10, M11 y M12 muertos. La ronda de cierre vuelve a ejecutarlo sobre la integración real | abierto |

Observación sin hallazgo: ruff (fuera del gate, que solo mira los ejecutores) sugiere `re.MULTILINE` en lugar de `re.M` en `pruebas_gate_entorno.py:40` (FURB167).

## Veredicto r02

**APTO, pendiente de una ronda de cierre que haré yo.**

- H-01, H-02 y H-03 quedan corregidos y probados.
- Solo queda abierto H-04, que es bajo: documentar en el traspaso la resolución exacta de la fusión con T-204 (`r07_resolucion_fusion_t204.diff`).
- En la ronda de cierre compruebo:
  - el traspaso y el README corregidos;
  - en el commit de integración, el diff r07 aplicado si T-204 ya está en develop, `pruebas_scripts.sh` en verde con la línea base sumada, INC-T202-01 (con la decisión 4) copiado a `docs/incidencias.md` y `preparar_entorno.sh` ejecutado en el `.venv` común.

---

# Ronda de cierre · 25-11-2026

- **Revisor:** claude, el mismo de la r01 y la r02.
- **Código revisado:** `wip/t202` rebasada sobre eda55e1b (develop con T-204 y T-201), con tres commits; la punta es 0b2c9237.
- **Entorno:** mi `.venv` propio sigue conforme con 54 paquetes fijados.

## H-04 y la fusión con T-204

- **Resolución de la fusión: está toda aplicada.**
  - `pruebas_gate_bloques.py` tiene la raíz falsa de `revisores/r07_…`, con `preparar_entorno.sh`, `common.sh`, el fichero de versiones real y un `freeze` que coincide con él.
  - El comentario de `requisitos_entorno.txt` ya no nombra el Forex («pandas-stubs (A +26, B +13)»). Ninguno de los tres ficheros del gate (`requisitos_entorno.txt`, `preparar_entorno.sh` y `check_all.sh`) lo nombra.
  - Los comentarios de `preparar_entorno.sh` dicen «los dos ejecutores», con los añadidos de T-202.
  - El bucle de mypy queda `for i in "${!PAQUETES[@]}"`, con las dos inserciones de T-202.
  - La línea base de `.docs/scripts` es 460 + 6 = 466.
- **Documentación corregida.** El traspaso ya no dice «sale limpio» sin matiz y el README tiene la sección «Al integrar».
- **INC-T202-01** está en `docs/incidencias.md`, con las cuatro decisiones y los números de A y B después de T-201 y T-204.
- **Pruebas:**
  - Del gate y del entorno: 76 de 76 (`pruebas_gate_entorno.py`, `pruebas_preparar_entorno.py` y `pruebas_gate_bloques.py`, con las guardas de T-204 contra el Forex).
  - `pruebas_scripts.sh`: 466 pasan, igual a la línea base.
  - `test_t202_svi.py` y `test_t202_alternativas_rangos.py`: 9 pasan.
- **El `check_all.sh` real**, sección de lint y tipos, sobre una copia de 0b2c9237:
  - con el `.venv` común, sin stubs: mypy A y mypy B salen ✗ con los 5 «falta …» y sin ejecutar mypy; 2 fallos de 8;
  - con mi `.venv`, conforme: ✓, con mypy A 67 de 67, B 159 de 159 y ruff 1533 de 1533.
- **mypy frente a develop:** con stubs, los errores de A y B son los mismos que en eda55e1b sin stubs (67 y 159 líneas, 0 diferencias sin contar el número de línea).
- **`equivalencia.py`** (eda55e1b con el `.venv` común frente a 0b2c9237 con el mío): 107 ficheros iguales y 0 diferencias.
- **Mutantes:**
  - `mutantes.py`: 12 de 12 muertos.
  - `revisores/r01_mutantes.py`, de RQ05 a RQ12: 8 de 8 muertos.
  - `revisores/r06_mutantes_gate.py`: 5 de 7 muertos. RG05 y RG07 viven y son equivalentes, como en la r02.
- **Gate del implementador** (`scratchpad/gate_t202_cierre.log`): 10/10 con rc=0 (pytest A 8586 y B 176).

## Hallazgos

| ID | Gravedad | Estado |
| --- | --- | --- |
| H-01 | baja | corregido (r02) |
| H-02 | baja | corregido (r02) |
| H-03 | media | corregido (r02); verificado otra vez sobre develop con T-204 |
| H-04 | baja | **corregido** (cierre): fusión resuelta, documentada y probada |

Una nota que no es hallazgo: los criterios de aceptación del README conservan los números del plan (A ≤ 102, A-Forex ≤ 174), que eran los vigentes al planificar. Los actuales (A 67, B 159) están en INC-T202-01 y en el registro.

## Fuera del commit (lo hace el coordinador al integrar)

- Ejecutar `.docs/scripts/preparar_entorno.sh` en el `.venv` común. Hoy da conforme con 49 paquetes frente al fichero de develop. En cuanto entre T-202, sus gates de mypy saldrán ✗ hasta que se ejecute el script, como manda la decisión 4.
- Avisar a Astra para que haga lo mismo en su `.venv`.

## Veredicto final

**APTO. No queda ningún hallazgo abierto.**
