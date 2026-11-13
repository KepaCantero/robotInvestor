# T-93 · QA independiente

## Ronda r01

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación (subagente de QA) · **Ronda:** r01 · 12-11-2026
- **Código revisado:** `c688d72` (develop). El cambio de T-93 es `bb2d692`; después solo T-101 (`16aa49e`) toca dos de sus ficheros (`contratos.py`: canales V6 y esquema `SINTESIS`; `llm.py`: caché simulada por prefijo), sin tocar R8, el almacén ni CT-23. Comparaciones con `8604f00` (`bb2d692^`, el código anterior a T-93).

### Reproducción desde limpio

```bash
git worktree add --detach /tmp/claude-0/t93qa HEAD              # c688d72
git worktree add --detach /tmp/claude-0/t93qa_antes bb2d692^    # 8604f00, sin T-93
git worktree add --detach /tmp/claude-0/t93qa_mut HEAD          # copia desechable para los mutantes
ln -s /home/user/robotinvestor/.venv /tmp/claude-0/t93qa/.venv
W=/tmp/claude-0/t93qa/bloque_a/11_Ejecutor
cd /tmp/claude-0/t93qa && PYTHONPATH=$W .venv/bin/python -m pytest -q bloque_a/11_Ejecutor/tests   # 607 passed in 585 s
cd /tmp/claude-0/t93qa && ./tools/check_all.sh                                                     # ver «Gate»
# sondas de la QA r04 de T-92 (python -I; comprueban que bloque_a se importa de la copia)
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_01_r8_regla_texto.py $W   # 0 fallos (62 OK)
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_02_almacen_corte.py $W    # 0 fallos (10 OK)
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_03_plazos_iso.py $W       # 0 fallos (34 OK)
# sondas anteriores de T-92 sobre HEAD: r02_01, r02_02, r03_01 y r03_02 dan 0; r03_03 da 1 (2a, H-30, ya explicado)
# la batería de T-93 sobre el código anterior
cp $W/tests/test_t93_hallazgos.py /tmp/claude-0/t93qa_antes/bloque_a/11_Ejecutor/tests/
pytest -q tests/test_t93_hallazgos.py        # en t93qa_antes: 34 failed, 3 passed
# sondas de esta ronda (en revisores/)
.venv/bin/python -I .docs/tickets/T-93/revisores/r01_01_r8_escapes.py $W /tmp/claude-0/t93qa_antes/bloque_a/11_Ejecutor  # 13 fallos
.venv/bin/python -I .docs/tickets/T-93/revisores/r01_02_almacen_legado.py $W     # 2 fallos (1 y 2: H-42)
.venv/bin/python -I .docs/tickets/T-93/revisores/r01_03_plazos_tipos.py $W       # 1 fallo (3b: H-43)
.venv/bin/python -I .docs/tickets/T-93/revisores/r01_04_mutantes.py /tmp/claude-0/t93qa_mut/bloque_a/11_Ejecutor  # 0 fallos
```

Los tres worktrees se quitan al terminar. Las tres pruebas que pasan con el código anterior son las que `pruebas.md` dice (la fecha de 8 cifras inexistente, el recall y la medianoche inexistente).

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1: los tres scripts `r04_0x` dan 0 fallos | sí | `r04_01`: 0 fallos (antes de T-93, 11). `r04_02`: 0 (antes, 2); el caso 1 abre en los 321 cortes. `r04_03`: 0 (antes, 4) |
| CA-2: la detección de claves reales no baja (formatos de `r04_01` caso 1 iguales que en la r04) | sí, en su medida, con reservas | Todos los formatos de proveedor al 100 % (4000/4000), igual que develop y la r04; los residuos de H-36, con las mismas cifras: 3910/4000, 3986/4000 y 0/4000. **Reservas:** fuera de esa medida, la detección sí baja. Una clave con forma real detrás de un escape doble (`\\n`, `\\t`, `\\r`) se veía antes de T-93 y ahora no (H-40). La ampliación de `RE_TRAMO_TEXTO` deja sin ver formas que la r04 veía al 100 % (H-41) |
| CA-3: las 37 pruebas nuevas pasan y la mayoría fallan con el código anterior | sí | 37 pasan en HEAD. Sobre `8604f00`, 34 fallan y 3 pasan, como dice `pruebas.md`. Mutantes (`r01_04`): mueren los 21 no equivalentes, uno por cada parte de la corrección. Sobreviven los dos equivalentes: quitar `\"` y `\\` de `RE_ESCAPES`, porque ni «"» ni «\» son letra o cifra, y quitar el `bool` explícito, porque `bool` es `int` |
| CA-4: la suite de A pasa entera y el gate da 12/12, con ruff y mypy de A por debajo de su cuota | sí | Suite de A: 607 pasan (la línea base ha subido por T-101). Gate en la copia limpia: ver «Gate». En `bb2d692`, ruff bajó de 3072 a 3019 y mypy de A de 115 a 114 (`tools/cuotas.txt` de ese commit) |
| CA-5: nada fuera de `bloque_a/11_Ejecutor` salvo documentación, cuotas y cola | sí, con una observación | Lo de T-93 en `bb2d692` está en `bloque_a/11_Ejecutor`, `tools/cuotas.txt`, `CLAUDE.md`, la deuda técnica y `.docs/`. El mismo commit lleva también T-99 (`.docs/scripts/registro_experimentos.py`, `banco_medida.py` y sus pruebas) y los borradores de CT-G-08 y CT-G-24 (`.docs/diseno/contratos/`), declarados en el mensaje. Son otras tareas, no cambios de T-93, pero `pruebas.md` resume CA-5 como «`.docs/`» sin separarlas |

### Estado de H-32 a H-39

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-32 | **corregido en los casos citados; incompleto y con una regresión (H-40)** | `r04_01` casos 2b, 2c y 2d: los diez escapes de la r04 se ven (`«`, `“`, ` `, `—`, emoji en pares sustitutos, `\b`, `\f`, `%3D`, `%20` y `\xa0`). La grabadora no escribe la clave en la cinta. `contenido_sensible` recorre `set` y `frozenset`. Siguen sin verse `\U0001f511` (`ascii()`), el octal `\253`, `%u2014` y los escapes dobles. Los dobles `\\n`, `\\t` y `\\r` se veían antes de T-93 (H-40). `contiene_credenciales` no recorre `frozenset` (H-44) |
| H-33 | **corregido para los 12 textos; quedan falsos positivos con cifra y unidad (H-45)** | `r04_01` caso 3b: 0 de 12. La fecha de 8 cifras que no existe sigue siendo clave (prueba y mutantes). `r01_01` caso 4: siguen marcando 6 de 10 titulares reales con cifra y unidad («2nm», «16gb», «300mm», «1bn», «2tn», «lpddr5x») |
| H-34 | **corregido para la línea a medias; queda el registro entero sin «\n» final (H-42)** | `r04_02` caso 5 y `r01_02` caso 1: en un almacén anterior a los sellos, con el cuarto registro cortado en cada uno de sus 341 bytes, abre, escribe y reabre bien en 340 (antes de T-93, en 1). En el corte justo antes del salto de línea, la siguiente escritura lo corrompe |
| H-35 | **corregido** | `r04_02` caso 1: los 321 cortes abren (r04: 312). `r01_02` caso 5: un corte entre los dos bytes de «ñ» se aparta. Caso 6: una línea intermedia con UTF-8 roto falla cerrado sin tocar nada. Observación: lo apartado se guarda decodificado con `errors="replace"`, así que la copia en `.no_confirmado.jsonl` no conserva los bytes originales del corte. Eso no afecta a la cadena |
| H-36 | **declarado; la frase «T-93 no lo empeora» no es exacta (H-41)** | «Límites (H-36)» de `analisis-tecnico.md` da las cifras de la r04, que se repiten. Pero la ampliación de H-33 añade formas nuevas que no se detectan (H-41) |
| H-37 | **corregido** | `r04_03` caso 3 y `r01_03` caso 1: `int`, `float` (también NaN e inf), `bool`, `np.int64`, `np.float64` y `np.bool_` dan ValueError. `Decimal`, `Fraction` y `complex` dan TypeError: se rechazan igual. Ninguno se lee como 1970. Un `date` vence al terminar el día, como su texto, también el 29-3 y el 25-10 en Madrid (`r01_03` caso 4). `False` o `0` ya no se toman por «sin plazo». Un `datetime`, un `Timestamp` o un `np.datetime64` a medianoche vencen a las 00:00: llevan hora y es coherente (INFO) |
| H-38 | **corregido para los plazos que no se leen; queda el campo ausente (H-43)** | `r01_03` caso 3, con nueve formas guardadas («2026-6-8», 20260608, 2026.5, True, None, un dict, una lista, «» y «nan»): vence con una sola incidencia DATOS. Un segundo `vencer()` no repite nada, y la clase deja de estar pausada. Si al CNS le falta `plazo_respuesta`, `vencer()` lanza KeyError (H-43) |
| H-39 | **corregido** | (a) El README de T-92 ya explicaba `r03_03` desde `3d3cbb6`. (b) `pruebas.md` de T-92 da el recuento de 16 de 20. (c) Existe `test_h39_plazo_en_un_dia_sin_medianoche`, que pasa |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-40 | media | `r01_01`, casos 1 y 1b, con la ruta del código anterior como segundo argumento. Por ejemplo, `contenido_sensible(json.dumps({"x": json.dumps({"nota": "a\n" + clave})}))`, con `clave` una `ant-api03` armada en tiempo de ejecución: JSON dentro de una cadena JSON, como un resultado de herramienta que el agente cita | **Esperado:** ningún escape delante de la clave la oculta (H-32), y T-93 no detecta menos que antes. **Obtenido:** **regresión**. Con `\\n`, `\\t` o `\\r` (escape doble) delante, la clave se veía antes de T-93 y ahora no. Tampoco se ve con «\\n» literal delante (una ruta o el `repr` de un `repr`), ni en una clave de dict que lleve esa forma. La causa es la alternativa `\\[…\\]` de `RE_ESCAPES`: consume la barra escapada y deja la «n» pegada a «sk-». Además, H-32 sigue abierto con escapes que no se enumeran: dobles (`\\u00ab`, `%253D`), `\U0001f511` de `ascii()`, el octal `\253` y `%u2014`. La grabadora escribiría la clave en la cinta, como en H-32 (los datos ya leídos sí se bloquean con `contiene_credenciales`). **Media, como H-32:** es el mismo mecanismo, en formas menos frecuentes | Sustituir los tramos de barras enteros: `\\+(?:u[0-9a-fA-F]{4}\|U[0-9a-fA-F]{8}\|x[0-9a-fA-F]{2}\|[0-7]{1,3}\|[ntrbf/"])` y `%(?:25)*(?:u[0-9A-Fa-f]{4}\|[0-9A-Fa-f]{2})`, o aplicar la sustitución hasta que no cambie. Probado en la copia desechable: con esa expresión, los 9 casos de `r01_01` (1 y 2) se detectan, y las 107 pruebas de `test_t92_revision.py` y `test_t93_hallazgos.py` pasan. Añadir esos casos como regresión. Se recomienda corregirlo antes del modo sombra con API, como H-32 | abierto |
| H-41 | baja | `r01_01`, caso 5 (INFO), frente al código anterior | **Esperado:** «T-93 no lo empeora» (`analisis-tecnico.md`, «Límites»). **Obtenido:** la ampliación de `RE_TRAMO_TEXTO` (H-33) deja de detectar formas que antes de T-93 se veían al 100 %. Son colas de 5 grupos de 5 cifras (0/2000, antes 2000/2000), de 4 grupos de 6 cifras (0/2000, antes 2000/2000) y de 3 grupos de 10 mayúsculas (0/2000, antes 2000/2000). Ningún proveedor conocido usa esas formas, y es el mismo precio aceptado que en H-36. Pero no está declarado, y el documento afirma lo contrario | Declararlo en «Límites», con las cifras. Si se quiere acotar, que una cola hecha solo de tramos de cifras cuente como clave (los 12 textos de H-33 tienen siempre un tramo de letras) |
| H-42 | baja | `r01_02`, casos 1 y 2. En un almacén anterior a los sellos, el último registro está entero pero sin el «\n» final (un corte justo antes del salto de línea, 1 de las 341 posiciones). O un almacén sellado cuyo último registro sellado no acaba en «\n», que es lo que deja la migración en ese mismo caso | **Esperado:** se aparta o se completa, como cualquier otro corte (H-34). **Obtenido:** abre y lo sella. La siguiente escritura se pega a esa línea, y al reabrir el almacén no abre (`JSONDecodeError: Extra data`): el registro confirmado queda fuera de la cadena hasta repararlo a mano. Ya pasaba antes de T-93 y en develop. Solo en la migración y con 1 byte de cada línea | Al abrir con `recuperar`, si el fichero no acaba en «\n» y la última línea es un registro válido, añadir el «\n» (o, en `escribir`, anteponerlo si el fichero no acaba en él). Regresión con los casos 1 y 2 |
| H-43 | baja | `r01_03`, caso 3b: un CNS `ENVIADA` y `SALIENTE` en F5 sin el campo `plazo_respuesta` (estado manipulado o de otra versión) | **Esperado:** como H-38, vence con una incidencia y el ciclo sigue. **Obtenido:** `vencer()` lanza `KeyError: 'plazo_respuesta'` (`c["plazo_respuesta"]`). F0 no lo captura (`orquestacion.py`, `self.consultas.vencer(instante)`), así que no corre ningún análisis hasta arreglar F5 a mano. Ninguna versión conocida escribe un CNS sin el campo | Leerlo con `c.get("plazo_respuesta")` (con `None` ya va por la rama de la incidencia). Regresión con el caso 3b |
| H-44 | baja | `r01_01`, caso 3: `contiene_credenciales({"x": frozenset({"\n" + clave})})` | **Esperado:** como `contenido_sensible`, que desde T-93 recorre `set` y `frozenset`. **Obtenido:** `False`. `_textos` solo recorre `list`, `tuple` y `set`, y en el volcado el `str()` del `frozenset` deja la clave detrás de `\\n` (H-40). Ningún JSON produce un `frozenset` | Añadir `frozenset` en `_textos`. Regresión con el caso 3 |
| H-45 | baja | `r01_01`, caso 4 (INFO) | **Esperado:** el nombre de una URL de prensa financiera no es clave (H-33). **Obtenido:** siguen marcando 6 de 10 titulares reales con cifra y unidad: «lpddr5x», «2nm», «1bn», «16gb», «300mm» y «2tn». Falla cerrado (PARCIAL con incidencia), y no está declarado | Admitir los tramos `[0-9]{1,4}[a-z]{1,3}` y las siglas de producto de 5 letras con cifra (`[a-z]{2,5}[0-9][a-z]?`), comprobando el recall con `r04_01` caso 1 y `r01_01` caso 5. O declararlo en «Límites» |
| H-46 | baja | Lectura de documentos | (a) «Límites (H-36)» dice que T-93 no empeora la detección (ver H-41). (b) `analisis-tecnico.md` habla de `RelojSistema.fecha`, pero la clase es `Reloj`. (c) El README del ejecutor (CT-23 y «Operación del Bloque A tras T-92») no recoge que los plazos se aceptan solo en ISO 8601 o como `date` (un número se rechaza). Tampoco que una consulta guardada con un plazo que no se lee vence con una incidencia DATOS, y así una BLOQUEANTE deja de pausar. Es un cambio de comportamiento visible para el operador; está en el diseño del ticket, pero no en el README | Corregir (a) y (b). Añadir a la línea de CT-23 del README las dos reglas de (c) |

**Lo que se intentó y no se rompió:**
- **R8, claves de proveedor:** la detección es del 100 % en todos los formatos de `r04_01` caso 1, con los diez escapes de H-32 y en `set`, `frozenset`, listas y tuplas anidadas (`contenido_sensible`). Las entidades HTML y `\N{…}` delante también se detectan.
- **Almacén:**
  - Una línea cortada en dos ficheros de un almacén legado falla cerrado sin cambiar ningún fichero (`r01_02` caso 3).
  - Abrir dos veces tras apartar no aparta nada más ni repite la incidencia (caso 4).
  - El UTF-8 roto en una línea intermedia falla cerrado (caso 6).
  - Las sondas de recuperación anteriores (`r02_02` y `r03_02`) siguen dando 0.
- **CT-23:**
  - Un instante numérico en `vencer()` o `enviar()` se rechaza (`r01_03` caso 5).
  - «» y `None` toman el plazo del modo, y «   » se rechaza.
  - `vencer()` es idempotente con plazos que no se leen.
- **Mutantes (`r01_04`):** cada parte de la corrección (cada escape, los conjuntos, cada tramo nuevo, la fecha de 8 cifras, el apartado legado, la lectura en bytes, el rechazo de números, el `date`, `False` como plazo, y la captura, el vencimiento y la incidencia de H-38) tiene una prueba que la mata.

### Invariantes

- **F y G antes de una orden:** sin cambios. El Bloque A no emite órdenes.
- **Sin LLM en la ruta determinista ni en los controles:** se cumple. Los cambios son expresiones regulares, lectura de ficheros y fechas.
- **Los controles no se relajan solos:** se cumple en tiempo de ejecución. Pero el cambio de diseño de R8 detecta menos que antes en dos casos: el escape doble (H-40), que es una regresión no buscada, y las formas de H-41, que no se declaran. Ninguno afecta a los formatos de proveedor en texto plano.
- **Falla cerrado y valida antes de mutar:**
  - un registro sellado truncado sigue siendo fallo de integridad;
  - dos líneas sin sello fallan cerrado sin tocar nada;
  - un plazo no válido se rechaza al enviar.
  - H-38 vence a propósito en lugar de parar, como pedía la QA r04 y declara el diseño del ticket. H-43 es la excepción: para el ciclo.
- **Ningún número escrito a mano:** se cumple. Las longitudes de los tramos (15 letras, 5 a 7 cifras, tope de 30) y `RE_FECHA_8` son reglas de forma del texto, como las de T-92, no parámetros de política.
- **Ninguna decisión del operador en silencio:** la regla de H-38 (vencer con una incidencia en lugar de pausar) está en el diseño del ticket y la proponía la QA. Falta en el README del ejecutor (H-46 c).
- **Sin secretos ni datos personales:** `tools/secrets_scan.py` no da hallazgos con las sondas `r01_*` y este `qa.md`. Las claves se arman en tiempo de ejecución.
- **Documentación:**
  - al día: la fila T-93 de la deuda («EN QA», QA sin asignar), `CLAUDE.md` y `tools/cuotas.txt` (que ya llevan la línea base de T-101), y el recuento de T-92 en `pruebas.md`;
  - pendiente: H-46.

### Gate

`./tools/check_all.sh` sobre la copia limpia de `c688d72`: **12 pasan, 0 fallan**. Pasan corpus, NFC, YAML, secretos, referencias, ruff, mypy ×3 y pytest ×3 (A 607, A-Forex 68 y B 176).

### Veredicto

**APTO.** Se cumplen CA-1 a CA-5, con las reservas anotadas en CA-2 y CA-5, y no queda ningún hallazgo crítico ni alto.
- **H-32 a H-39 están corregidos en lo que pedía la QA r04,** con su prueba. Fallan 34 de las 37 con el código anterior, y cada parte de la corrección tiene una prueba que mata su mutante.
- **H-40 es media y es una regresión de la propia corrección:** la clave detrás de un escape doble ya no se ve. Se recomienda corregirlo antes del modo sombra con API, como se pedía para H-32: es una línea, y la expresión sugerida ya se ha probado contra las 107 pruebas de T-92 y T-93.
- **H-41 a H-46 son bajos.** Al cerrar, H-40 a H-46 pasan a la deuda con su ID.

Esta QA no cierra el ticket: según el encargo, el revisor no cambia su estado, no hace commit y no escribe fuera de este `qa.md` y de `revisores/r01_*`. Los pasos de cierre de `ri-qa` (estado, deuda con H-40 a H-46, diario, memoria y commit) quedan para quien coordina.
