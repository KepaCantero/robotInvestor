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
