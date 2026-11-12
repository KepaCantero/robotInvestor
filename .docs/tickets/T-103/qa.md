# T-103 · QA independiente

## Ronda r01

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; regla del operador del 12-11-2026) · **Ronda:** r01 · **Fecha:** 2026-11-12
- **Objeto:** commit `33385c9` de `develop` (correcciones de H-40 a H-46 de la QA r01 de T-93). Opinión formada con el README del ticket, el diff y el código antes de leer `analisis-tecnico.md`.

### Reproducción desde limpio

Worktrees desechables (fuera del árbol de trabajo, que tiene cambios sin confirmar de T-102), con el `.venv/` de la raíz enlazado: `33385c9` (T-103), `33385c9^` = `c688d72` (antes de T-103) y `8604f00` (antes de T-93). Todo con `.venv/bin/python -I`.

```bash
git worktree add --detach <tmp>/wt_nuevo 33385c9 && git worktree add --detach <tmp>/wt_viejo 33385c9^
ln -s "$PWD/.venv" <tmp>/wt_nuevo/.venv && (cd <tmp>/wt_nuevo && ./tools/check_all.sh)          # 12/12
W=<tmp>/wt_nuevo/bloque_a/11_Ejecutor; V=<tmp>/wt_viejo/bloque_a/11_Ejecutor
for f in r01_01_r8_escapes r01_02_almacen_legado r01_03_plazos_tipos; do .venv/bin/python -I .docs/tickets/T-93/revisores/$f.py $W; done   # 0, 0, 0 fallos
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_01_r8_regla_texto.py $W                                                         # 0 fallos
.venv/bin/python -I .docs/tickets/T-103/revisores/r01_01_r8_escapes_y_falsos.py $W $V   # 0 fallos; INFO: formas no cubiertas y falsos positivos nuevos
.venv/bin/python -I .docs/tickets/T-103/revisores/r01_02_r8_rendimiento.py $W $V        # 3 fallos (H-47); tarda unos 15 min
.venv/bin/python -I .docs/tickets/T-103/revisores/r01_03_almacen_cortes.py $W           # 3 fallos, todos del caso 7 (H-48)
git worktree add --detach <tmp>/wt_mut 33385c9
.venv/bin/python -I .docs/tickets/T-103/revisores/r01_04_mutantes.py <tmp>/wt_mut/bloque_a/11_Ejecutor   # 1 fallo (H-49)
```

Resultados:

- **Gate** `./tools/check_all.sh` en `33385c9` limpio: **12/12**, exit 0. Bloque A 630 (607 + 23), A-Forex 68, B 176. Cuotas iguales: ruff 2986, mypy A 109, FX 174, B 159.
- `test_t103_r8_y_bajos.py`, `test_t93_hallazgos.py`, `test_t92_revision.py` y `test_v51.py`: 143 en verde.
- La batería nueva sobre el código anterior (`c688d72`): **18 fallan y 5 pasan**, como dice `pruebas.md`.
- Scripts de T-93 (`r01_01`, `r01_02`, `r01_03`) y `r04_01` de T-92: **0 fallos**.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `T-93/revisores/r01_01_r8_escapes.py` da 0 fallos. Los casos 1 y 1b, los cuatro enumerados del 2 y el 3 se detectan. `r01_01_r8_escapes_y_falsos.py` 1b: también con tres y cuatro capas de JSON, una URL codificada tres veces, un `repr` de `repr` y `\U0001F511` en mayúsculas |
| CA-2 | sí | `r01_02_almacen_legado.py`: casos 1 (341 cortes) y 2 OK. `r01_03_plazos_tipos.py` 3b OK. 0 fallos en los dos. Ampliado en `r01_03_almacen_cortes.py`, casos 1 a 6: 281, 281 y 280 cortes por escenario, con la cadena entera. Ver H-48 para el caso 7 |
| CA-3 | sí | `r04_01_r8_regla_texto.py`: 0 fallos. Los formatos de proveedor dan las mismas cifras que en la r04, y 0 de los 12 textos de H-33 se marcan |
| CA-4 | **no (parcial)** | Sin el commit fallan 18 de 23, como dice `pruebas.md`. Pero, corrección a corrección, el mutante «H-44 sin frozenset» sobrevive a la batería nueva y también a la heredada (H-49): `test_h44` pasa sin la corrección de H-44. Los otros 15 mutantes no equivalentes de H-40 a H-43 mueren (2 de ellos solo con la batería heredada de T-92 y T-93) |
| CA-5 | sí | Gate 12/12. A tiene 630 (≥ 607 + 23) y las cuotas no suben |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-47 | media | `r01_02_r8_rendimiento.py <T-103> <c688d72>`. Por ejemplo, `contenido_sensible("\\" * 99_999 + "z")` | **Esperado:** R8 lineal, como antes. El peor tiempo de `r04_01` con entradas adversarias era 0,92 s. **Obtenido:** **regresión de rendimiento de T-103, con coste cuadrático.** La alternativa `\\+(?:…)` vuelve a empezar en cada barra de un tramo que no acaba en un escape y lo recorre entero. Con 10 000 barras y una «z», 1,25 s en `contenido_sensible` y 7,3 s en `contiene_credenciales`. Con 20 000, 5,8 s y 25,6 s. Con 99 999, **129 s y 592 s**. Con 100 000 barras solas, `contiene_credenciales` tarda 114 s. Con 100 tramos de 999 barras, 6 s. Antes de T-103, 0,03 s y 0,07 s. R8 corre sobre cada respuesta del modelo (`respuesta_segura`), sobre el mensaje y el contexto antes de cada llamada (`agentes.py:109`), en cada `Mensajeria.crear` (`contratos.py:340`) y en las consultas del Broker. `json.dumps` duplica las barras, así que el coste se multiplica. Un texto externo hostil cuelga el ciclo: no falla cerrado, se queda parado | Anclar el tramo a su primera barra y hacerlo posesivo: `(?<!\\)\\++(?:u[0-9a-fA-F]{4}\|U[0-9a-fA-F]{8}\|x[0-9a-fA-F]{2}\|[0-7]{1,3}\|[ntrbf/"])`, y dejar igual la parte `%`. Da la misma sustitución en 300 000 cadenas aleatorias, y 1 000 000 de barras se procesan en 0,02 s. También vale quitar el `+` (`\\(?:…)`): delante de «sk-» queda igual un espacio, y las 23 pruebas pasan (`r01_04`, mutante equivalente). Añadir una regresión con 100 000 barras y un límite de tiempo | abierto |
| H-48 | **alta** | `r01_03_almacen_cortes.py`, caso 7: `Almacen(d).escribir("F5", "AG-01", {"id": "uno", "nota": "a\u2028b"})` y después `Almacen(d)`. De extremo a extremo: `b.consultas.entrante("Nota copiada de una web:\u2028el plazo cambia")` y después abrir otro `Bloque` sobre el mismo estado | **Esperado:** un registro confirmado se vuelve a leer. Los separadores de registro del JSONL son «\n», que es lo que escribe `escribir` y en lo que se apoyan H-34 y H-42. **Obtenido:** el almacén **no vuelve a abrir** (`JSONDecodeError: Unterminated string`, ni siquiera «Fallo de integridad»). Pasa si un valor lleva U+2028, U+2029 o U+0085. La causa: `_actualizar` parte con `texto.splitlines()`, que también corta en esos caracteres, y `json.dumps(ensure_ascii=False)` no los escapa. Ningún ciclo posterior arranca, y no hay reparación a mano posible: editar el fichero rompe la cadena de hashes. Los datos están enteros. Se llega por interfaces normales: CT-23 entrante, textos del modelo y evidencia citada de webs o PDF. U+0085 es además lo que da la elipsis de cp1252 leída como latin-1. **Anterior a T-103** (está igual en `c688d72` y en `8604f00`, desde la entrega), pero es la misma lectura de líneas que corrige H-42. `ReplayClient` (`llm.py:231`, la cinta) tiene el mismo patrón | En `_actualizar`, partir solo por «\n» (`datos.split(b"\n")` o `texto.split("\n")`, ignorando las líneas vacías; `json.loads` admite el «\r» final de un CRLF). Lo mismo en `ReplayClient`. Es compatible con todo lo escrito, porque `json.dumps` nunca emite «\n» sin escapar. Regresión con U+2028, U+2029 y U+0085 en un valor, en un almacén sellado y en uno anterior a los sellos. Si el operador prefiere sacarlo de T-103, abrir un ticket propio antes del modo sombra | abierto |
| H-49 | baja | `r01_04_mutantes.py`: el mutante «H-44 sin frozenset» sobrevive a `test_t103_r8_y_bajos.py` y a `test_t93` + `test_t92` | **Esperado:** `test_h44` falla sin `frozenset` en `_textos` (CA-4). **Obtenido:** pasa. Desde H-40, el volcado ya ve la clave que va detrás de `\\n` en el `str()` del `frozenset`, así que la prueba no depende de lo que corrige. Hay un caso que sí depende de ello: `contiene_credenciales({"x": frozenset({'"password": "xxxxxxxxxxxx"'})})` da `[]` en `c688d72` y lo detecta en T-103, porque en el volcado las comillas salen escapadas y `RE_SECRETO` no casa | Cambiar `test_h44` por ese caso, con el par armado en tiempo de ejecución, o probar `list(_textos(frozenset({...})))` directamente | abierto |
| H-50 | baja | `r01_01_r8_escapes_y_falsos.py`, caso 3 | **Esperado:** README, H-41: «lo que sigue sin verse se declara». **Obtenido:** las colas de **3 grupos de 5 a 7 cifras** (de 20 a 26 caracteres) y las de 3 fechas AAAAMMDD válidas dan 0/500 en T-103. Antes de T-93 (`8604f00`) se veían 200/200: el tramo `[0-9]{5,7}` es de T-93, y la regla de «4 o más tramos» no las recoge. «Límites» solo declara las de 3×10 y 4×6 mayúsculas | Declararlo en «Límites», con las cifras. O bajar la regla a 3 o más tramos de solo cifras: el mutante «desde 3 tramos» pasa las 23 pruebas, y los 12 textos de H-33 tienen siempre un tramo de letras. Comprobarlo con `r04_01` | abierto |
| H-51 | baja | `r01_01_r8_escapes_y_falsos.py`, caso 2: 9 de 20 textos que no son clave se marcan ahora, y antes de T-103 no | **Esperado:** si la corrección amplía los falsos positivos, se declara (como H-45). **Obtenido:** hay dos fuentes nuevas, no declaradas. (a) La regla de H-41 marca referencias y marcas de tiempo de solo cifras con 4 o más grupos y 20 o más caracteres: `sk-2024-11-12-10-30-00-123`, `SK-421-02-5930-1234-5678`, `sk-0001-0002-0003-0004-0005` y `…/sk-2024-07-25-2024-07-26`. (b) La expresión ancha expone, detrás de un escape doble, las colas de H-45: titulares en JSON anidado (`\\nsk-hynix-16gb-…`, `300mm`, `2tn`) y rutas de Windows dentro de JSON (`C:\\docs\\nsk-6205-2rs-…`). Falla cerrado: sale PARCIAL con una incidencia, y no se pierde ninguna clave | Declarar (a) y (b) en «Límites», junto a H-45. Es el precio esperado de detectar de más |
| H-52 | baja | `r01_01_r8_escapes_y_falsos.py`, caso 1 (INFO) | **Esperado:** «Límites conocidos» enumera lo que sigue sin verse. **Obtenido:** declara solo las entidades HTML y `\N{…}`, que además sí se detectan (el «;» y la «}» no son letra). Siguen sin verse, y tampoco se veían antes (no es una regresión): la barra codificada seguida de «n» (`%5Cn`, `%5C%5Cn`, `\u005cn`, `\x5cn`), quoted-printable (`=3D`, `=0A`), `\a`, `\v` y `\e` de C o bash, `%U2014` en mayúscula, la clave en base64, la clave con U+200B o U+00AD dentro, la clave con un `\u0041` dentro (JSON con `ensure_ascii`) y la clave partida en líneas dentro de un JSON | Declararlo en «Límites conocidos». Si se quiere cerrar la clase entera, decodificar (des-escapar por capas hasta que no cambie) en lugar de sustituir por un espacio | abierto |

Los scripts de esta ronda están en `revisores/` (`r01_01` a `r01_04`). Arman las claves en tiempo de ejecución y no usan red.

### Invariantes del sistema

- **Ningún camino a una orden sin F y G; no hay LLM en la ruta determinista ni en los controles:** el cambio no toca esas rutas. R8 sigue siendo determinista.
- **Los controles no se relajan solos:** en tiempo de ejecución, se cumple. La detección recupera lo que T-93 había perdido, salvo H-50.
- **Todo falla cerrado:** se cumple en H-42 y H-43. `r01_03` casos 1 a 6: los cortes en cada byte, con y sin sellos, y una excepción a mitad de escritura dejan el fichero byte a byte como estaba. El «\n» antepuesto no entra en el hash y no rompe la cadena (`verificar_integridad` en verde). **Excepciones:** H-47, que cuelga en lugar de fallar cerrado, y H-48, que falla cerrado pero sin salida.
- **Ningún número a mano:** «4 o más tramos» es una regla de forma, como las de `RE_TRAMO_TEXTO`. Está declarada en el diseño.
- **Ninguna decisión del operador en silencio:** las reglas de H-38 y H-43 ya están en el README del ejecutor (H-46 c).
- **Secretos y datos personales:** no hay claves literales ni en las pruebas ni en los scripts, y el gate `secrets` está en verde.
- **Documentación:** H-46 a, b y c están hechos (`T-93/analisis-tecnico.md` y la línea de CT-23 del README del ejecutor), y la deuda tiene T-103. Faltan las declaraciones de H-50, H-51 y H-52.

### Veredicto

**NO APTO.**

- **H-48 (alta) está abierto.** No lo introduce T-103, pero está en la misma lectura de líneas del almacén que corrige H-42, y deja el Bloque A sin arrancar por un carácter corriente en texto externo.
- **CA-4 no se cumple entero:** `test_h44` no vigila H-44 (H-49).
- **H-47 (media) es una regresión de rendimiento de la propia corrección de H-40.** Se arregla en una línea y se recomienda corregirlo antes del modo sombra con API, junto con H-48.
- **H-50 a H-52 son bajos**, de declaración o de refuerzo. Si no se corrigen, pasan a la deuda con su ID.

Según el encargo, el revisor no cambia el estado del ticket, no hace commit y no escribe fuera de este `qa.md` y de `revisores/r01_*`. La vuelta a `ri-implementar` queda para quien coordina. Después, este revisor vuelve a ejecutar `r01_01` a `r01_04` en una ronda r02.

## Ronda r02

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; regla del operador del 12-11-2026) · **Ronda:** r02 · **Fecha:** 2026-11-12
- **Objeto:** commit `7feb697` de `develop`, solo la parte de T-103: `RE_ESCAPES` con lookbehind y posesivo y la regla de tres tramos de cifras en `contratos.py`; los JSONL partidos por «\n» en `almacen.py`, `llm.py` (`ReplayClient`) y `herramientas/ht06_indice.py`; y las 8 pruebas de la «ronda r02» de `tests/test_t103_r8_y_bajos.py`. T-88 y T-91, que van en el mismo commit, quedan fuera. Opinión formada con el README, el diff y el código antes de leer la sección «Ronda r02» de `analisis-tecnico.md`.

### Reproducción desde limpio

Worktrees desechables en el scratchpad: `7feb697` (r02), `7feb697^` = `9297df9` (T-103 r01 más T-102 r02, que no toca R8 ni el almacén) y otro `7feb697` para los mutantes. El `.venv/` de la raíz va enlazado y todo corre con `.venv/bin/python -I`. Los worktrees se borraron al acabar.

```bash
git worktree add --detach <tmp>/wt_nuevo 7feb697 && git worktree add --detach <tmp>/wt_viejo 7feb697^ && git worktree add --detach <tmp>/wt_mut 7feb697
ln -s "$PWD/.venv" <tmp>/wt_nuevo/.venv && (cd <tmp>/wt_nuevo && ./tools/check_all.sh)            # 12/12
W=<tmp>/wt_nuevo/bloque_a/11_Ejecutor; V=<tmp>/wt_viejo/bloque_a/11_Ejecutor; R=.docs/tickets/T-103/revisores
.venv/bin/python -I $R/r01_01_r8_escapes_y_falsos.py $W $V        # 0 fallos
.venv/bin/python -I $R/r01_02_r8_rendimiento.py $W                # 0 fallos (sin la 2.ª ruta: la r01 tarda unos 15 min)
.venv/bin/python -I $R/r01_03_almacen_cortes.py $W                # 0 fallos (el caso 7 pasa)
.venv/bin/python -I $R/r01_04_mutantes.py <tmp>/wt_mut/bloque_a/11_Ejecutor   # 11 «FALLO» de texto: ver abajo
for f in r01_01_r8_escapes r01_02_almacen_legado r01_03_plazos_tipos; do .venv/bin/python -I .docs/tickets/T-93/revisores/$f.py $W; done  # 0, 0, 0
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_01_r8_regla_texto.py $W   # 0 fallos
.venv/bin/python -I $R/r02_01_jsonl_lectores.py $W $V --repo "$PWD"           # 0 fallos; INFO del caso 6 = H-53
.venv/bin/python -I $R/r02_02_r8_rendimiento_adversario.py $W $V              # 0 fallos; INFO del caso 3 = H-56
.venv/bin/python -I $R/r02_03_tres_tramos_falsos_positivos.py $W $V           # 0 fallos; INFO del caso 2
.venv/bin/python -I $R/r02_04_mutantes.py <tmp>/wt_mut/bloque_a/11_Ejecutor   # 0 fallos (unos 6 min)
.venv/bin/python -I $R/r02_05_python_310.py "$(uv python find 3.10)" $W $V    # INFO = H-55
.venv/bin/python -I $R/r02_06_cache_cortada.py $W                             # INFO = H-54
```

Resultados:

- **Gate** `./tools/check_all.sh` en `7feb697` limpio: **12/12**, exit 0. Bloque A 737 (≥ 607; incluye las 31 de `test_t103_r8_y_bajos.py` y las de T-102, T-88 y T-91), A-Forex 68, B 176. Cuotas sin subir: ruff 2938, mypy A 109, FX 174 y B 159.
- **Scripts de la r01**, otra vez:
  - `r01_01`: 0 fallos. Las colas de 3 grupos de 6 y 7 cifras y las de 3 fechas pasan de 0 a 500 de 500. Se marcan 0 de 20 falsos positivos nuevos frente a la r01.
  - `r01_02`: 0 fallos. Con 99 999 barras y una «z», 0,012 s y 0,036 s (en la r01, 129 s y 592 s). La variante sin cambios da 0 diferencias en 300 000 cadenas.
  - `r01_03`: 0 fallos. Las 4 variantes del caso 7 (U+2028, U+2029, U+0085 y U+001C) reabren.
  - `r01_04`: cuenta 11 «FALLO», todos porque no encuentra el texto original: busca la `RE_ESCAPES` y la regla `>= 4` de `33385c9`, que la r02 cambió. Los 9 mutantes que todavía encuentra mueren, y entre ellos «H-44 sin frozenset», que en la r01 sobrevivía (H-49). El método se porta a `r02_04` sobre el código de la r02.
- **Scripts de T-93 y T-92:** `r01_01`, `r01_02` y `r01_03` de T-93 y `r04_01` de T-92 dan 0 fallos. 0 de los 12 textos de H-33 se marcan, y el peor tiempo es 1,18 s con la máquina cargada.

### Ataques de esta ronda (`revisores/r02_*`)

- **`r02_01`, lectores de JSONL:**
  - El almacén reabre y vuelve a escribir con U+2028, U+2029 y U+0085 en un valor, en una clave del registro, en un dict anidado y en una lista. Lo hace sellado y anterior a los sellos (se migra al abrir). En el código anterior, los 6 escenarios dan `JSONDecodeError`.
  - Una escritura cortada a mitad de los 3 bytes de U+2028 se aparta como las demás.
  - **CRLF:** un almacén convertido entero a «\r\n» abre, escribe y reabre, sellado y legado, y la cinta y la caché también. El hash se calcula sobre el objeto leído, no sobre la línea, así que el «\r» final no rompe la cadena.
  - La cinta graba y reproduce, y la caché guarda y reabre, con los tres separadores.
  - **«\r» solo (INFO, igual que antes de la r02):** el almacén sellado falla cerrado. En el legado, el fichero entero se toma por una línea cortada, se aparta a `*.no_confirmado.jsonl` y se anota una incidencia. No es un formato que escriba nadie.
- **Otros lectores con `splitlines()` sobre datos persistidos:**
  - En el paquete del Bloque A no queda ninguno. `referencias.py:76` lee F7, F8 y F9, que son corpus congelado sin esos caracteres (se buscaron en todo `bloque_a/`: 0). `ht02_verificador_enlaces.py:701` usa `readlines()` en modo texto, que solo corta en «\n».
  - Fuera del bloque quedan los de H-53.
- **`r02_02`, rendimiento:**
  - La sustitución de la r02 es idéntica a la de la r01 en 400 000 cadenas de un alfabeto hostil y en 8 casos dirigidos.
  - 19 entradas adversarias nuevas: barras con escape casi completo, barras con «%», «%25» sin fin, «%u» casi, «sk-» repetido, cola de guiones, «"password"» sin cierre, «Bearer» y espacios, «-----BEGIN» sin fin, cifras de DNI. Ninguna pasa de 0,12 s con 100 000 caracteres, y de 100 000 a 1 000 000 de caracteres el tiempo crece entre 7 y 14 veces, que es lineal.
  - Ver H-56 para los diccionarios anidados.
- **`r02_03`, regla de tres tramos:**
  - Recall de 300 de 300 en 6-6-6 (justo 20 caracteres), 5-6-7, 7-7-7, 8-8-8, fechas, «_», separadores repetidos y «SK-» en mayúsculas.
  - 5-5-5 y 5-6-6 no son candidatas (menos de 20 caracteres, declarado).
  - Hay 6 falsos positivos nuevos de 8 textos corrientes: marcas de tiempo `sk-20241112-103000-123456`, periodo con código de cotización, lotes y nombres de fichero con fecha y hora, y rangos de nominales. Todos caben en lo declarado en «Límites conocidos» («referencias y marcas de tiempo de solo cifras con tres o más grupos y 20 caracteres o más») y fallan cerrado.
  - Los titulares con un tramo de letras siguen sin marcarse (0 de 5).
- **`r02_04`, mutantes sobre `7feb697`:** 0 fallos. Mueren:
  - «sin lookbehind» (con solo el posesivo vuelve a ser cuadrático: la prueba de H-47 falla en 5,7 s);
  - «vuelve la r01» (258 s);
  - los tres lectores de vuelta a `splitlines()`, cada uno por su prueba;
  - «parte por «\r\n»»;
  - la regla de vuelta a 4 tramos, «sin la regla» y «any»;
  - «sin frozenset»;
  - los de H-40 a H-43.

  Igual que en la r01, «sin \xNN» y «sin \b ni \f» solo los mata la batería heredada de T-92 y T-93. Hay tres equivalentes que sobreviven, como se esperaba:
  - «sin posesivo»: con el lookbehind solo ya es lineal, porque cada tramo se intenta una vez;
  - «una sola barra»;
  - «desde 2 tramos»: dos tramos de 8 cifras o menos no llegan a 20 caracteres.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `T-93/revisores/r01_01_r8_escapes.py`: 0 fallos. `r01_01_r8_escapes_y_falsos.py` casos 1 y 1b: OK (tres y cuatro capas de JSON, URL codificada tres veces, `repr` de `repr`) |
| CA-2 | sí | `T-93/revisores/r01_02_almacen_legado.py` y `r01_03_plazos_tipos.py`: 0 fallos |
| CA-3 | sí | `T-92/revisores/r04_01_r8_regla_texto.py`: 0 fallos, con 0 de 12 textos de H-33. `r02_03` caso 3: 0 de 5 titulares con letras |
| CA-4 | sí | `r02_04`: cada mutante no equivalente de las correcciones de la r01 y de la r02 muere (2, solo con la batería heredada, como en la r01). El de H-49 ya muere con la batería nueva |
| CA-5 | sí | Gate 12/12. A tiene 737 (≥ 607 + 31) y las cuotas no suben (ruff 2938, mypy 109/174/159) |
| CA-6 | sí | `test_r02_h47` pasa. `r01_02`: 0 fallos, 0,012 s + 0,036 s con 99 999 barras. `r02_02`: 0 fallos con 19 entradas adversarias nuevas, lineal hasta 1 000 000 de caracteres |
| CA-7 | sí | `r01_03` caso 7: 0 fallos. `r02_01` casos 1, 2, 3 y 5: almacén sellado y legado, cinta y caché con los tres separadores, también con «\r\n» |
| CA-8 | sí | `test_r02_h49` muere sin `frozenset` (`r01_04` y `r02_04`). Tres tramos de cifras de 20 caracteres o más: 300 de 300 en 8 formas (`r02_03` caso 1) |
| CA-9 | sí | «Límites conocidos (se declaran: H-50 a H-52)» de `analisis-tecnico.md`, y la fila T-103 de la deuda: colas de menos de 20, falsos positivos de cifras y de H-45 detrás de un escape doble, y las formas codificadas que no se ven. Los falsos positivos que mide `r02_03` caso 2 caben en lo declarado |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-53 | media | `r02_01_jsonl_lectores.py <W> --repo <raíz>`, caso 6: `Almacen(d).escribir(...)` con «a b» en A-Forex y en B, y después `Almacen(d)`. Además, `.docs/scripts/registro_experimentos.py` con U+2028 en una anotación | **Esperado:** la causa de H-48 (alta en la r01) se corrige o se declara donde también está. **Obtenido:** el mismo `splitlines()` sobre JSONL escrito con `ensure_ascii=False` sigue en `bloque_a_forex` (`almacen.py:96` y `:212`, `llm.py:177`, `herramientas/ht06_indice.py:42`) y en `bloque_b` (`almacen.py:104` y `:213`, `llm.py:177`). Los dos almacenes no vuelven a abrir (`JSONDecodeError`), y `registro_experimentos.py:64` da «el registro está dañado». No está en `analisis-tecnico.md`, ni en la fila T-103 de la deuda, ni en `docs/incidencias.md`. La regla 8 impide arreglarlo dentro de T-103, pero hay que declararlo: para A-Forex y B el defecto es tan grave como H-48, y los dos van al modo sombra | Abrir una fila de deuda o un ticket por bloque (A-Forex y B, `split("\n")` en los mismos sitios y la regresión de `test_r02_h48`) antes de su modo sombra. `registro_experimentos.py` es del espacio de trabajo y se corrige en una línea | abierto |
| H-54 | media | `r02_06_cache_cortada.py <W>`: `cache_resultados.jsonl` con el último registro a medias (el proceso murió durante `CacheResultados.guardar`), y después `nuevo_bloque(...)` sobre el mismo estado | **Esperado:** como en el almacén (H-10, H-29, H-35), una escritura cortada no impide el siguiente arranque, o falla cerrado diciendo qué fichero y qué hacer. **Obtenido:** ningún `Bloque` arranca. Sale un `JSONDecodeError: Unterminated string…`, o un `UnicodeDecodeError` si el corte cae a mitad de un carácter, sin nombre de fichero. `guardar` no hace `fsync`, y con valores de más de 8 KB el `write` en modo texto puede ir en varias llamadas. La cinta (`ReplayClient`) se comporta igual, pero ahí fallar cerrado es razonable. **Anterior a T-103**: es el mismo lector que toca la r02. Se arregla borrando la caché, pero el mensaje no lo dice | En `CacheResultados.__init__`, ignorar con una incidencia, o apartar, una última línea sin «\n» que no sea JSON (es una caché: perderla es seguro). Si no, envolver el error con la ruta y «borre la caché». Regresión con un corte en cada byte del último registro. Si no entra en T-103, a la deuda con su ID | abierto |
| H-55 | baja | `r02_05_python_310.py "$(uv python find 3.10)" <W> <V>` | **Esperado:** el paquete carga con el Python mínimo que declara (`pyproject.toml`: `requires-python = ">=3.10"`; README del ejecutor: «Python ≥ 3.10»). **Obtenido:** con 3.10.20, `import bloque_a.contratos` da `re.error: multiple repeat at position 10`, porque los cuantificadores posesivos existen desde 3.11. Antes de la r02, `contratos` sí importaba. No es lo primero que rompe 3.10: `redaccion.py:186` ya usaba una f-string de 3.12 (PEP 701), y el entorno del proyecto exige 3.12 (`preparar_entorno.sh`). La declaración ya era falsa, y ahora además cae el núcleo de R8 | Registrar una incidencia para subir `requires-python` y el README a 3.12, sin corregirlo en silencio (como INC-001 y INC-002). O quitar el posesivo: el lookbehind solo ya es lineal (mutante equivalente en `r02_04`, 31 pasan en 0,86 s), compila en 3.10 y da la misma sustitución | abierto |
| H-56 | baja | `r02_02_r8_rendimiento_adversario.py <W>`, caso 3: `contenido_sensible` sobre un dict anidado de 400 niveles con una hoja de 100 000 caracteres | **Esperado:** R8 lineal en el tamaño de la entrada (CA-6, menos de 2 s). **Obtenido:** `contenido_sensible(dict)` vuelca el JSON entero en cada nivel y luego baja (`llm.py:58-60`), así que el coste es la profundidad por el tamaño: 100 niveles, 1,4 s; 400 niveles, 7,2 s; 400 niveles con 1 MB, 60 s. `contiene_credenciales` vuelca una sola vez (0,05 s). Se llega por `agentes.py:109` (contexto) y `agentes.py:119` (respuesta del modelo leída de la caché), con la respuesta acotada por `max_tokens`. Anterior a T-103; no es una regresión de la r02 | Volcar una sola vez, arriba, y luego recorrer solo las hojas de texto, como `contiene_credenciales`. O declararlo en «Límites». A la deuda con su ID | abierto |

Los scripts de esta ronda están en `revisores/` (`r02_01` a `r02_06`). Arman las claves en tiempo de ejecución, no usan red y no escriben fuera de carpetas temporales. `r02_04` solo muta una copia desechable.

### Invariantes del sistema

- **Ningún camino a una orden sin F y G, y nada de LLM en la ruta determinista ni en los controles:** la r02 no toca esas rutas. R8 sigue siendo una expresión regular determinista.
- **Los controles no se relajan solos:** la sustitución es idéntica a la de la r01 (400 000 cadenas). La regla de tres tramos solo añade detección (falsos positivos declarados que fallan cerrado).
- **Todo falla cerrado y valida antes de mutar:** el almacén reabre con los tres separadores y con «\r\n», y los cortes siguen apartándose (`r01_03` y `r02_01` caso 2). R8 ya no se cuelga con muchas barras. Excepciones anteriores a T-103: H-54 (la caché cortada bloquea el arranque sin decir por qué) y H-56.
- **Ningún número a mano:** «tres tramos» y «20 caracteres» son reglas de forma de R8, declaradas en el diseño. El límite de 2 s está solo en la prueba.
- **Ninguna decisión del operador en silencio:** no se toma ninguna. La versión de Python declarada (H-55) se deja al operador, por incidencia.
- **Secretos y datos personales:** no hay claves literales en las pruebas ni en los scripts, y el gate `secrets` está en verde. Las pruebas llevan U+2028 y U+2029 como caracteres literales (`test_t103_r8_y_bajos.py:126` y `:139`); `nombres-nfc` está en verde.
- **Documentación:** «Límites conocidos», la fila T-103 de la deuda y el diario están al día con la r02. Falta declarar H-53 a H-56.

### Veredicto

**APTO.**

- Los nueve criterios se cumplen, con evidencia propia: la r01 vuelta a ejecutar y los ataques nuevos, con 0 fallos.
- H-47, H-48, H-49 y H-50 están corregidos, y cada corrección tiene una prueba que la mata si se quita (`r02_04`). H-51 y H-52 están declarados.
- No queda abierto ningún hallazgo crítico ni alto de T-103. H-53 y H-54 son medios, y H-55 y H-56, bajos. H-54 y H-56 son anteriores a T-103, y H-53 está fuera de su alcance por la regla 8. Pasan a la deuda técnica con su ID: H-53, con una fila o ticket por bloque (A-Forex y B) antes del modo sombra de esos bloques; H-54, con un ticket antes del modo sombra con API del Bloque A.

Según el encargo, el revisor no cambia el estado del ticket, no hace commit y no escribe fuera de esta sección y de `revisores/r02_*`. El cierre de la skill `ri-qa` (estado `CERRADO`, deuda con H-53 a H-56, diario, memoria y commit) queda para quien coordina.
