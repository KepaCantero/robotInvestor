# T-204 · QA

## QA r01 · 2026-11-25 · revisor independiente (claude, sin el contexto de la implementación)

**Veredicto: NO APTO.** Tres hallazgos medios (H-01 a H-03) y cinco bajos (H-04 a H-08). El borrado del Forex y el gate están bien: A y B no cambian, el corpus solo pierde las huellas del Forex y la cuota de ruff es exacta. Los defectos están en los documentos y en las dos piezas sin aplicar (el parche de la Constitución y la limpieza de `.docs/`).

Base `d23afe0` (develop). Rama `wip/t204`, commit `123118ea`. Worktree propio en `<scratchpad>/qa_t204`, con `.venv` enlazado. Una segunda extracción de `d23afe0` sirvió de comparación y una tercera, desechable, para aplicar el parche. No se tocó la copia del implementador.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| Gate del implementador (`gate_t204_r2.log`, terminado a las 02:07, antes del commit de las 02:07:59; el árbol de `t204` está limpio en `123118ea`) | **10/10**, «TODOS LOS GATES PASARON»: corpus 525, ruff 1604/1604, mypy 102 · 159, pytest A 8443 y B 176 |
| corpus-integridad, nombres-nfc, secrets y refs-vivas en el worktree de QA | en verde, 525 archivos |
| `.docs/scripts/pruebas_scripts.sh` | 432 passed (línea base 432). Las 399 pruebas de develop siguen todas, con el mismo ID |
| `pruebas_gate_bloques.py` sobre los scripts de develop | 12 failed y 21 passed, como dice `pruebas.md` |
| `prueba_refs_vivas.py` (43 casos) con el `refs_vivas.py` de develop | 35/43: fallan los 8 casos del bloque retirado |
| `mutantes.py` del ticket | 29 de 29 muertos |
| Colección de pytest de A y de B, ticket frente a develop | **idéntica**: 8445 ID en A (8443 pasan y 2 se omiten) y 176 en B |
| Pruebas de A que leen ficheros cambiados por el ticket (`docs/incidencias.md`, `refs_vivas`, CLAUDE.md, prompts…): `test_fase3_goldens`, `test_t129`, `test_t148`, `test_t157`, `test_t166`, `test_t187_pb51` y `test_t65_qa_r01` a `r03` | 419 passed |
| Suite de B completa | 176 passed |
| ruff y mypy de los ficheros tocados | sin hallazgos nuevos: los 3 de ruff (`EXE001` ×2, `PLW1510`) ya estaban en develop. mypy da 0 en `refs_vivas.py` y en `pruebas_gate_bloques.py` |

### Lo que se pidió mirar

1. **A y B no cambian.** Ningún fichero de `bloque_a/` ni de `bloque_b/` está en el diff. Los 317 borrados son de `bloque_a_forex/`: 180 del corpus y 137 de su `11_Ejecutor`. En los ejecutores de A y B, ninguna prueba, configuración ni código nombra el Forex. La única excepción es el texto de `tests/goldens/README.md` (ver H-08). Las pruebas de A que tocan `.docs/scripts/` usan otros scripts, no los que cambian aquí.
2. **Corpus.** El manifiesto de develop tiene 705 líneas y el nuevo 525. Comparados ordenados, salen 180 líneas quitadas, todas de `bloque_a_forex/`, y ninguna añadida ni cambiada.
3. **ruff 1604.** Medido como el gate, da 2806 en develop con los tres ejecutores y 1604 con A y B, tanto en develop como en la rama, con **la misma lista de hallazgos línea a línea**. La bajada es solo por los ficheros borrados. Falta una prueba que fije la cifra (H-07).
4. **refs-vivas.** No se cuela ninguna ruta muerta que no sea del Forex. Con la marca en la línea o en un registro, las demás rutas de la cita se siguen comprobando. `r01_02` lo prueba en 5 casos (A, B, `tools/`, `.docs/` y un registro). Por el lado del Forex hay tres huecos pequeños (H-06).
5. **CLAUDE.md.** La tabla, las líneas base (607 y 174), el 10/10 (dos veces), el gate (525, 2 YAML, mypy ×2, pytest ×2) y los comandos están bien. Queda la cifra de `.secrets.baseline`, 48, cuando ahora son 43 (H-05).
6. **INC-T204-04.** Las menciones de B (README y F8) están justificadas, igual que las «Divisas (Forex)» y las FX- de A y B Forex: B no tiene ningún enumerado ni código del Forex, y su `origen.tipo` es `BLOQUE_A` o `LIBRE`. El inventario está incompleto (H-08).
7. **«A ≥ 439» en `ri-probar`.** Es un defecto. La línea dice «(las de `tools/cuotas.txt`)» y allí pone 607 desde T-102. Este ticket reescribió justo esa línea, y la skill se carga en cada fase de pruebas. Conviene corregirlo aquí (H-04).

**Parche de la Constitución.** `git apply --check` está en verde. Aplicado en una extracción aparte, `pruebas_parametros_doc_t83.py` da 109 comprobaciones en verde, y corpus, refs-vivas, secretos y NFC siguen en verde. No rompe nada, pero choca con la numeración de las propuestas pendientes (H-02).

**Limpieza de `.docs/`.** No borra nada de A ni de B. Ninguna cita «…» cambia salvo dentro de frases que solo hablan del Forex, y ninguna orden entre `…` cambia. Pero borra la huella de T-204 y reescribe evidencia medida (H-03).

### Hallazgos

**H-01 · media · `docs/AVANCE.md` da por aplicada la enmienda de la Constitución.**
- **Reproducir:** la fila del 2026-11-25 dice «la Constitución pasa a la V0.7 (enmienda 4)». La cabecera de `Constitucion_Global.md` sigue en V0.6 y el parche no está aplicado. La fila T-204 de la deuda y INC-T204-01 dicen lo contrario. `r01_05_coherencia_docs.py` lo detecta.
- **Esperado:** el registro de avance describe el estado real.
- **Corrección:** cambiar ese trozo por «la enmienda de la Constitución queda propuesta, sin aplicar (INC-T204-01)».
- **Regresión:** prueba en `pruebas_gate_bloques.py`: toda «Constitución pasa a la V0.N» de `docs/AVANCE.md` es la versión del H1 de la Constitución. `r01_05` en verde.

**H-02 · media · El parche de la Constitución reutiliza números ya tomados por propuestas pendientes.**
- **Reproducir:** `r01_04_parche_constitucion.py` da 4 casos.
  - «Enmienda 4» ya es el nombre de la propuesta de `.docs/diseno/enmienda_4/` (11-11-2026), que la enmienda 5 cita («el resto de la enmienda 4») y que `.docs/knowledge/05_historia-del-proyecto.md` también nombra.
  - V0.7, los cambios 43 en adelante y D-48 en adelante son la numeración provisional de la enmienda 5 (`propuesta_claude.md`: «D-48 a D-56 y cambios 43 a 51»; la parte 2 sigue con 52 a 79 y D-57 a D-84). La deuda viva ya cita esa numeración (T-99: «D-53 propuesta en la enmienda 5»).
  - INC-T204-01 no dice nada de esto. Aplicado tal cual, «enmienda 4» y «D-48» nombrarían dos cosas distintas en la fuente de verdad del sistema y en sus propuestas.
  - Además, el cambio 17, una fila ratificada de «De la V0.3 a la V0.4», se reescribe sin anotar quién la reduce (D-20 sí lo anota), y la línea de fecha («Nov 9, 2026») no cambia con la V0.7.
- **Corrección:**
  - Dar a la enmienda un nombre libre: «enmienda 6», porque la 4 y la 5 son propuestas pendientes. V0.7, el cambio 43 y D-48 pueden quedarse, porque son los siguientes del texto ratificado.
  - Declarar en INC-T204-01 que la numeración provisional de la enmienda 5 se corre en uno al ratificarse, como dice su propia regla («se renumera si algo se ratifica antes»).
  - Anotar el cambio 17 con «(texto reducido por la enmienda 6, D-48)».
  - Actualizar la fecha de la cabecera.
- **Regresión:** `r01_04` da 0 casos, `git apply --check` sigue en verde y `pruebas_parametros_doc_t83.py` sigue en verde con el parche.

**H-03 · media · `limpiar_docs.py` borraría la huella de T-204 y reescribiría evidencia medida, en contra de su propia regla.**
- **Reproducir:**
  - Ejecutado hoy, borra la fila de `.docs/knowledge/01_que-es-el-robot-investor.md` «`bloque_a_forex/` | Eliminado el 25-11-2026 por orden del operador (T-204)». Es una de las excepciones que INC-T204-03 dice conservar.
  - La propuesta guardada está desfasada: en su línea 68 aún sale el texto de antes («Prueba antigua; fuera del Robot Investor»).
  - Reescribe resultados medidos, y 93 de las líneas reescritas siguen diciendo 12/12, ×3 o «tres». Por ejemplo, T-200 `pruebas.md` acabaría en «A y B dentro de cuota (102, 174, 159…)» y T-198 en «12 de 12 en verde … mypy 102/159». T-65 diría «los tres mypy (123, 159)» y la historia, «tres entregas» con dos viñetas.
  - Eso da por ejecutado un gate que no se ejecutó, justo lo que su docstring prohíbe («la evidencia literal se conserva»).
  - También reescribe las instrucciones literales de los encargos a Astra (`.docs/diseno/*/encargo_revision_astra.md`).
  - No tiene ninguna prueba. `r01_01_propuesta_limpieza.py` lo detecta.
- **Esperado:** el script listo para `--aplicar` respeta sus propias reglas y las excepciones de INC-T204-03.
- **Corrección:**
  - No tocar ninguna línea que lleve «T-204».
  - Tratar como evidencia, sin reescribirlas, las líneas que dan resultados de gate o de suites (12/12, «12 de 12», ×3, «passed», cuotas o recuentos de mypy, pytest y ruff) y las instrucciones de los encargos.
  - Regenerar `limpiar_docs_propuesta.txt` y corregir sus cifras en INC-T204-03.
- **Regresión:** pruebas de `limpiar()`. Una línea con «T-204» queda igual, una de un gate de 12/12 con «A-Forex 68» queda igual y una frase solo del Forex se borra. `r01_01` en verde con la propuesta nueva.

**H-04 · baja · La skill `ri-probar` dice «A ≥ 439».**
- **Reproducir:** `.agents/skills/ri-probar/SKILL.md:27`. `tools/cuotas.txt` dice 607 desde T-102.
- **Corrección:** «A ≥ 607, B ≥ 174».
- **Regresión:** prueba en `pruebas_gate_bloques.py`: cada «A ≥ N» y «B ≥ N» de la skill y de `CLAUDE.md` coincide con `cuotas.txt`. `r01_05` en verde.

**H-05 · baja · Dos cifras del gate desfasadas fuera del inventario.**
- **Reproducir:**
  - `CLAUDE.md` dice «`.secrets.baseline` (48 hallazgos…)», y el fichero tiene 43 desde que se quitaron los 5 del Forex.
  - `.pre-commit-config.yaml:5` dice «`tools/check_all.sh` (12 gates)».
- **Corrección:**
  - «(48 hallazgos auditados como falsos el 03-11; 43 desde T-204, sin los 5 del Forex)», o 43 sin más.
  - «(10 gates)».
- **Regresión:** las dos comprobaciones de `r01_05`, pasadas a `pruebas_gate_bloques.py`.

**H-06 · baja · Tres huecos de `refs-vivas` con el bloque retirado.**
- **Reproducir:** `r01_02_ataques_refs_vivas.py` da 8 de 11.
  - La marca se busca como subcadena, así que «T-2040» y «T-2041» la satisfacen. El mutante Q1 («T-20») sigue vivo.
  - `.split("=")` se aplica a todas las palabras, así que `bloque_a_forex/a=b.md` no se ve.
  - El caso «marca antes de la cita en la misma línea», que se da de verdad en `docs/AVANCE.md`, no está entre los de `prueba_refs_vivas.py`. Su mutante Q7 solo lo mata el gate sobre el repositorio real.
- **Corrección:**
  - Buscar la marca con `re.search(rf"(?<![\w-]){re.escape(marca)}(?!\d)", linea)`.
  - Partir por «=» solo las palabras que empiezan por «-».
  - Añadir esos tres casos a `prueba_refs_vivas.py`.
- **Regresión:** `r01_02` 11/11 y Q1 y Q7 de `r01_03` muertos por las pruebas.

**H-07 · baja · La cifra de ruff de CA-2 no la fija ninguna prueba.**
- **Reproducir:** con el mutante Q4 (`ruff=2806` en `cuotas.txt`), `pruebas_gate_bloques.py` y el gate siguen en verde. La cláusula «ruff baja a lo que mide (1604)» solo se ha comprobado midiendo.
- **Corrección:** prueba en `pruebas_gate_bloques.py` que mide ruff como el gate (se omite si no hay `.venv/bin/ruff`) y exige que la cuota sea igual a la medida. Es el trinquete que pide `CLAUDE.md` («cada fase debe dejarlas más bajas si toca el paquete»).
- **Si el operador no quiere atar la cuota a la medida:** quitar la cifra de CA-2 y dejar la cláusula en `pruebas.md` como comprobada por medida en esta QA.
- **Regresión:** Q4 de `r01_03` muerto.

**H-08 · baja · INC-T204-04 no recoge todas las menciones que se quedan.**
- **Reproducir:**
  - `bloque_a/11_Ejecutor/tests/goldens/README.md:84` dice «El Bloque A Forex queda para T-115», y T-204 ha quitado la fila T-115 de la deuda, así que la referencia queda colgando sin que la incidencia lo diga.
  - El F9 de B (`Registro de Fuentes para el Analizador de Mercados - V2.0.md`) tiene 27 «Origen: … F9 Forex …». Las temáticas TFX- son del A Forex, y la incidencia no las cita.
- **Corrección:** añadir las dos a INC-T204-04. La primera, con la nota de que T-115 se eliminó con T-204. La segunda, como texto del corpus congelado sin enumerado ni código.
- **Regresión:** prueba en `pruebas_gate_bloques.py`: cada fichero de `bloque_a/` y `bloque_b/` que nombra «A Forex», «A-Forex» o «F9 Forex» (fuera de `99_Historico*`) está citado en INC-T204-04.

### Invariantes

- **Números:** ninguno nuevo. 1604 sale de la medida y 432 del recuento.
- **Corpus y esquemas:** solo cambian las 180 huellas del Forex.
- **Pruebas antiguas:** ninguna se ha debilitado. En `prueba_refs_vivas.py` solo cambia el docstring.
- **Ciclo mock y backtest:** no se tocó código de A ni de B, y sus colecciones de pruebas son idénticas.
- **Datos personales y secretos:** ninguno en lo nuevo. La línea «@Dani» de la Constitución ya estaba y el parche no la añade.
- **Decisiones del operador:** las cuatro INC-T204 están en `[PROPUESTO]`.
- **Ramas abiertas:** `wip/t202`, que mide el Forex, queda declarada como riesgo al integrar.

### Scripts del revisor (`revisores/`)

- `r01_01_propuesta_limpieza.py <salida de limpiar_docs.py>`: 299 cambios, 3 casos (H-03).
- `r01_02_ataques_refs_vivas.py`: 8/11 (H-06).
- `r01_03_mutantes.py`: 10 mutantes, 8 muertos. Quedan vivos Q1 (H-06) y Q4 (H-07), y Q7 solo lo mata el gate.
- `r01_04_parche_constitucion.py`: 4 casos (H-02).
- `r01_05_coherencia_docs.py`: 4 casos (H-01, H-04 y H-05).

En la ronda siguiente se vuelven a ejecutar todos, junto con `mutantes.py`, `pruebas_scripts.sh` y el log de un gate nuevo.

## QA r02 · 2026-11-25 · el mismo revisor

**Veredicto: NO APTO.** Los ocho hallazgos de la r01 están corregidos y verificados con mis scripts. La aplicación de la r02b (enmienda 6 y limpieza de `.docs/`) es correcta en lo esencial. Quedan dos hallazgos medios nuevos (H-09 y H-10) y dos bajos (H-11 y H-12).

Commits revisados:
- `253f33fd`: la r02 del implementador;
- `ba651950` y `129376f4`: la r02b, por orden del operador del 25-11-2026, «Todo».

El worktree es el mismo, ahora en `129376f4`, y hay una extracción aparte de `253f33fd` para lo que había antes de aplicar. El gate completo de la r02 (`gate_t204_r02.log`, anterior a la r02b) da 10/10, con A 8443, B 176, ruff 1604 y mypy 102 · 159. No he lanzado otro. La r02b no toca A, B, el corpus ni el gate. Lo que sí toca lo he ejecutado aparte: `pruebas_scripts.sh`, refs-vivas, corpus y la batería del marco.

### Correcciones de la r01: verificadas

| Hallazgo | Evidencia |
| --- | --- |
| H-01 | `r01_05` da 0 casos. AVANCE dice hoy «la Constitución pasa a la V0.7», y es verdad. `test_h01` |
| H-02 | `r01_04` da 0 casos sobre `253f33fd`: «enmienda 6», INC-T204-01 declara la renumeración de la 5, el cambio 17 va anotado y la fecha es la nueva |
| H-03 | `r01_01` da 0 casos sobre la propuesta regenerada (107 cambios, reproducible byte a byte). `test_h03` ×3 |
| H-04 y H-05 | `r01_05` da 0 casos. `test_h04` y `test_h05` |
| H-06 | `r01_02` da 11/11. Q1 y Q7 mueren por las pruebas (`r02_mutantes_revisor.py`, que solo adapta el texto de Q1 al código nuevo) |
| H-07 | Q4 muerto. `test_h07` compara la cuota con la medida: 1604 = 1604 |
| H-08 | `test_h08`: INC-T204-04 recoge el README de los goldens y el F9 de B |
| Mutantes | Los 36 de `mutantes.py` y los 10 del revisor, todos muertos |
| `pruebas_scripts.sh` | 449 passed (línea base 449) |

### Estado aplicado (r02b)

- **La Constitución es coherente.**
  - `git apply -R --check` del parche está en verde: lo aplicado es exactamente el parche.
  - La V0.7 tiene la enmienda 6, el cambio 43 y D-48. D-20, el cambio 17, el §2 y el §14 van anotados.
  - El §15 dice que las enmiendas 4 y 5 siguen propuestas, y la fecha es la nueva.
  - «A Forex» solo queda en las cuatro líneas que describen la enmienda 6.
- **La batería del marco pasa.** `.docs/scripts/pruebas_marco.sh` (las suites que lista el LEEME del marco) da 62 pasan y 0 fallan, entre ellas `pruebas_parametros_doc_t83.py`.
- **Corpus, refs-vivas, secretos y NFC** en verde, con 525 archivos.
- **La limpieza (`ba651950`) es exactamente la salida de `limpiar_docs.py --aplicar`.** La he reproducido sobre `253f33fd` y el diff es idéntico: 107 líneas en 80 ficheros.
  - Solo toca `.docs/`, además de la Constitución. Nada de A ni de B.
  - Ninguna línea con T-204, ningún encargo a Astra, ninguna cita «…», ninguna orden entre `…` y ningún bloque de código. Todo lo que quita nombra el Forex.
  - Lo comprueba `r02_01_limpieza_aplicada.py`, salvo los 5 casos de H-11.
- **Cuotas:** ruff 1604 (medido) y mypy 0 en los ficheros tocados. Los 7 avisos ISC004 de `generar_enmienda.py` son de un script del ticket, fuera del gate.

### Hallazgos nuevos

**H-09 · media · Los documentos vivos siguen diciendo que la enmienda y la limpieza están pendientes.**
- **Reproducir:** `r02_02_estado_aplicado.py` da 13 casos.
  - **Fila T-204 de la deuda:** «Pendiente del operador: … la enmienda 6 está propuesta … y la limpieza de `.docs/` preparada».
  - **Memoria vigente `compartida/2026-11-25_bloque-a-forex-eliminado`:** «la Constitución global … no se ha tocado» y «la limpieza … Sin opciones solo propone». La leen los agentes al empezar.
  - **INC-T204-01 y 03:** la cabecera dice RESUELTO, pero el cuerpo dice «Propuesta, lista para aplicar», «Si se aplica…», «La decisión es del operador» y «`.docs/` queda como estaba».
  - **README de T-204:** «Ampliación del operador que no se pudo aplicar» y «sin aplicar».
  - **`sistema_global/README.md`:** «la Constitución global (V0.6 desde el 9-11-2026…)».
- **Esperado:** el estado real (V0.7, limpieza aplicada) en todos los documentos vivos.
- **Corrección:** reescribir esas frases en pasado («se aplicó el 25-11-2026 por orden del operador, “Todo”») y poner la V0.7 en el índice de `sistema_global/`.
- **Regresión:** `r02_02` da 0 casos. En `pruebas_gate_bloques.py`, que la versión del índice de `sistema_global/README.md` sea la del H1 de la Constitución y que la fila T-204 y la memoria no digan «Pendiente del operador» mientras la Constitución esté en la V0.7 o después.

**H-10 · media · `test_h02` falla en cuanto la Constitución pase legítimamente de la V0.7.**
- **Reproducir:** `r02_03_ataques_r02.py` cambia la cabecera a V0.8 (la de la enmienda 5, cuando se ratifique) y `test_h02` da «la Constitución no está ni en la V0.6 ni en la V0.7». Aunque no cambiara la cabecera, el `git apply -R --check` del parche dejaría de cumplirse con cualquier enmienda que toque las líneas de contexto (el párrafo del §0, el de «Enmiendas» o la tabla de decisiones).
- **Consecuencia:** `pruebas_scripts.sh`, y con él `commit.sh` y `commit_limpio.sh`, fallarían con la próxima enmienda por una prueba de un ticket cerrado.
- **Corrección:** con la Constitución en la V0.7 o después, que la prueba compruebe invariantes del contenido y no el parche:
  - el párrafo «Enmiendas» cita la enmienda 6;
  - existe la fila D-48 de la enmienda 6;
  - D-20 y el cambio 17 van anotados;
  - «A Forex» solo aparece en líneas que nombran la enmienda 6.
  - El `git apply -R --check` puede quedarse solo como comprobación del ticket (en `revisores/` o en `pruebas.md`), no en `pruebas_scripts.sh`.
- **Regresión:** `r02_03`, segundo caso, en verde.

**H-11 · baja · La limpieza aplicada dejó cinco líneas incoherentes, una de ellas evidencia de un gate.** `r02_01` da 5 casos:
- `.docs/tickets/T-194/pruebas.md`: «`--core` en verde (8/8) … y las tres suites (A 8 272 pasadas, B 176…)». Es el resultado de un gate, al que se le quitó «A-Forex 68». El patrón de evidencia de `limpiar_docs.py` no reconoce «8/8» ni «pasadas».
- `.docs/tickets/T-106/qa.md` y `.docs/tickets/T-113/README.md`: «`PYTHONPATH` … a los tres ejecutores (comprobado que `bloque_a` y `bloque_b` se importan…)».
- `.docs/tickets/T-200/pruebas.md`: «en las tres suites | B: nada…».
- `.docs/tickets/T-167/README.md`: «la suite de B no se tocan» (concordancia).
- **Corrección:**
  - Devolver a su texto original las cuatro primeras: son evidencia de lo que se ejecutó.
  - En la de T-167, poner «no se toca».
  - Añadir a la regla de evidencia de `limpiar_docs.py` «N/N», «N de N en verde», «pasadas» y «tres suites/ejecutores/bloques», con esos casos en `test_h03`.
- **Regresión:** `r02_01` da 0 casos, y los casos nuevos de `test_h03` pasan.

**H-12 · baja · refs-vivas dejó de ver el bloque retirado en una asignación de entorno.**
- **Reproducir:** `r02_03`, primer caso. `PYTHONPATH=bloque_a_forex/11_Ejecutor pytest -q` (o con `env …`) en un documento vivo de juguete (docs/x.md) pasa el gate. En la r01 se veía, porque se partía por «=» toda palabra. La corrección de H-06 solo parte las que empiezan por «-». Es la forma en que este repositorio escribe sus órdenes (`PYTHONPATH` a los ejecutores).
- **Corrección:** en `bloque_retirado()`, partir también las palabras de la forma `^[A-Za-z_][A-Za-z0-9_]*=`, y añadir los dos casos a `prueba_refs_vivas.py`. `bloque_a_forex/a=b.md` debe seguir fallando.
- **Regresión:** `r02_03`, primer caso, en verde, y `r01_02` sigue en 11/11.

### Scripts nuevos del revisor (`revisores/`)

- `r02_01_limpieza_aplicada.py [antes] [después]`: el diff de la limpieza aplicada (por defecto `253f33fd..ba651950`). Da 5 casos (H-11).
- `r02_02_estado_aplicado.py`: da 13 casos (H-09).
- `r02_03_ataques_r02.py`: da 3 fallos (H-12 ×2 y H-10).

En la ronda siguiente se vuelven a ejecutar `r01_01` a `r01_05` y `r02_01` a `r02_03`, junto con `mutantes.py`, `r02_mutantes_revisor.py`, `pruebas_scripts.sh`, `pruebas_marco.sh` y refs-vivas.

## QA r03 · 2026-11-25 · el mismo revisor

**Veredicto: APTO pendiente de la ronda de cierre.** H-09 a H-12 están corregidos y verificados. No aparecen regresiones de código. Queda un hallazgo bajo (H-13), de documentación, que verificaré en la ronda de cierre.

Revisado: `f8df1129` (encima de `129376f4`, con `80d152ec` y `901a2c1d`). Gate completo de la r03 (`gate_t204_r03.log`, terminado antes de `f8df1129`, que solo añade su resultado a `pruebas.md`): **10/10**, con A 8443, B 176, ruff 1604, mypy 102 · 159 y corpus 525. No lancé otro.

### Correcciones de la r02: verificadas

| Hallazgo | Evidencia |
| --- | --- |
| H-09 | `r02_02_estado_aplicado.py` da 0 casos. La fila T-204, la memoria, el cuerpo de INC-T204-01 y 03, el README del ticket y el índice de `sistema_global/` (V0.7) dicen el estado aplicado. `test_h09` |
| H-10 | `r02_03`, caso V0.8: 1 passed. `test_h02` comprueba invariantes del contenido desde la V0.7 y ya no aplica el parche al revés |
| H-11 | Las cuatro líneas de evidencia (T-106 ×2, T-187, T-199) coinciden byte a byte con su texto de antes de la limpieza (`git diff 253f33fd f8df1129` vacío en esos ficheros). T-166 dice «la suite de B no se toca». `limpiar_docs.py` ya no cambia nada (0 líneas). M37 muerto |
| H-12 | `r02_03`, casos `PYTHONPATH=…` y `env PYTHONPATH=…`: salida 1. `bloque_a_forex/a=b.md` sigue fallando (`r01_02`, 11/11). M38 muerto |

Además:
- `pruebas_scripts.sh` da 455 passed (línea base 455).
- `mutantes.py` da 38 de 38 muertos y `r02_mutantes_revisor.py` 10 de 10.
- `pruebas_marco.sh` da 62 pasan y 0 fallan. La r03 cambia la deuda, que lee `pruebas_parametros_doc_t83.py`.
- `r01_05` da 0 casos.
- corpus, refs-vivas, secretos y NFC están en verde.

### Error mío en la r02, y lo que he comprobado

El implementador tiene razón: las etiquetas de fichero de H-11 estaban mal.
- **Causa:** `r02_01_limpieza_aplicada.py` cambiaba el nombre del fichero antes de revisar el último trozo del anterior, así que cada caso salía con el nombre del fichero siguiente.
- **Lo que ya se sabía:** el contenido de las cinco líneas era el correcto.
- **Arreglo:** `r03_01_limpieza_aplicada.py` es la copia corregida. Revisa el último trozo antes de cambiar de fichero; `r02_01` se queda como estaba, como registro.
- **Resultado:** sobre `253f33fd..ba651950` da los 5 casos con sus ficheros reales (T-106 ×2, T-166, T-187 y T-199). Sobre `253f33fd..f8df1129` (la limpieza más la r03) solo quedan los cambios de la memoria de T-204 (H-09), que son los esperados.

**La cita que cambió el implementador en mi `qa.md` me vale.** Yo había escrito entre comillas de código una ruta de juguete que no existe, y `refs-vivas` también la comprueba en los registros. Quitar las comillas no cambia el sentido.

### Hallazgo

**H-13 · baja · INC-T204-03 copia mis etiquetas erróneas de la r02, y la fila T-54 cita la D-20 antigua sin anotar.** `r03_02_etiquetas_h11_y_t54.py` da 2 casos:
1. **`docs/incidencias.md`, INC-T204-03, «Lo que se corrigió después (r03)»:** dice «T-194 `pruebas.md`, T-106 `qa.md`, T-113 `README.md` y T-200 `pruebas.md`» y «En T-167 `README.md`», pero `80d152ec` cambió T-106 (×2), T-187, T-199 y T-166. El commit y el mensaje de la coordinación dicen lo correcto; la incidencia, no.
   - **Corrección:** «Cuatro líneas de evidencia vuelven a su texto original: dos de T-106 `qa.md`, T-187 `pruebas.md` y T-199 `qa.md`», y «En T-166 `pruebas.md` se arregla la concordancia».
2. **Fila T-54 de la deuda.** La pregunta era si dejarla así es aceptable. Mi respuesta es que conviene anotarla.
   - La fila sigue abierta («Antes de conectar A y B en la Fase 1») y empieza «Consecuencias de D-20 (A Forex y B Forex fuera, ratificado en la V0.4)».
   - Como cita histórica es exacta, pero la deuda es un documento vivo y la propia enmienda 6 anota cada fila ratificada que reduce (D-20 y el cambio 17: «texto reducido por la enmienda 6, D-48»). Ese mismo criterio pedí en H-02.
   - **Corrección:** basta con un inciso, sin borrar la cita: «(A Forex y B Forex fuera, ratificado en la V0.4; desde la V0.7, enmienda 6, D-48, D-20 solo nombra B Forex)».
- **Regresión:** `r03_02` da 0 casos. Si se quiere en `pruebas_scripts.sh`, `test_h09` puede comprobar también que la fila T-54 nombra la enmienda 6 mientras cite la redacción antigua.

### Observación (no es hallazgo)

`test_h02` busca la fila del cambio 17 con `l.startswith("| 17 |")` en toda la Constitución, y la tabla de riesgos del §15 ya llega al 13. Si algún día llega al 17, la prueba fallaría sin motivo. Si se toca `test_h02` en el cierre, conviene buscar esa fila solo en la tabla del §0.

### Scripts nuevos del revisor (`revisores/`)

- `r03_01_limpieza_aplicada.py [antes] [después]`: la copia corregida de `r02_01`.
- `r03_02_etiquetas_h11_y_t54.py [commit]`: 2 casos (H-13).

En la ronda de cierre: `r03_02` debe dar 0 casos, y se vuelven a ejecutar `r01_02`, `r01_05`, `r02_02`, `r02_03`, `r03_01` (sobre `253f33fd` y la punta), `pruebas_scripts.sh` y refs-vivas.

## Ronda de cierre de la QA r03 · 2026-11-25 · el mismo revisor

**Veredicto: APTO, con un hallazgo bajo abierto (H-14).** H-13 y la observación están corregidos, y el rebase no ha perdido nada. Al rebasar entraron tres tickets de develop que la limpieza de `.docs/` no cubrió, y `limpiar_docs.py` reescribiría dos líneas de evidencia suyas. Queda pendiente de una ronda más, breve, que verificaré yo.

Revisado `16c18af5` (`wip/t204`), rebasado sobre develop `d11662ff` (T-201 y T-203). El gate de cierre (`gate_t204_cierre.log`) da **10/10**: ruff 1533 (cuota 1533), mypy 67 · 159, pytest A 8549 y B 176. No lancé otro.

### H-13 y la observación

| Punto | Evidencia |
| --- | --- |
| INC-T204-03, etiquetas | `r03_02_etiquetas_h11_y_t54.py fad84daf` (el antiguo `80d152ec`) da 0 casos. Las etiquetas son dos de T-106, T-187, T-199 y T-166 |
| Fila T-54 | Lleva el inciso «desde la V0.7, enmienda 6, D-48, D-20 solo nombra B Forex». Lo comprueba `test_h09` y el mutante M39 muere |
| Observación de `test_h02` | El cambio 17 se busca solo en el §0, hasta `## 1.` |

### El rebase no ha perdido nada

- **Ficheros.** De los 105 que cambia develop (`d23afe0..d11662ff`), los que T-204 no toca están byte a byte igual que en `d11662ff`. De los que solo toca T-204, ninguno difiere de la r03 (`f8df1129`) salvo los que cambia el cierre. Cuatro los tocan los dos.
- **`tools/cuotas.txt`.** ruff 1533, y la medida de A y B en la punta es idéntica línea a línea a la de develop: 2735 en develop con los tres ejecutores, menos las 1202 del Forex. Lo demás: mypy A 67, mypy B 159, A ≥ 607 y B ≥ 174. No queda ninguna línea del Forex.
- **Deuda.** Las 200 filas, comparadas una a una contra la base, develop y la r03:
  - T-196, T-201 y T-203 están idénticas a develop;
  - solo T-54 y T-204 difieren, y son los cambios esperados;
  - T-115 sigue fuera;
  - el texto que no está en filas es idéntico.
- **Incidencias.** INC-T196-01 e INC-T201-01 están idénticas a develop, y también la nota de PB-08 «Aplicada en T-196». Solo cambian INC-002 (fuera) e INC-T204-01 a 04.
- **Diario.** Las entradas de T-201 y T-203 siguen. Las líneas que quita el diff contra develop nombran todas el Forex.
- **Cifras en los documentos vivos.** La fila T-204, AVANCE y la memoria dicen «1604 sobre la base de T-200; 1533 tras el rebase». El README del ticket conserva el plan con 1604 y su registro dice 1533.
- **Suites de A y B.** Las colecciones de pytest son idénticas a las de develop: 8551 ID en A (8549 pasan) y 176 en B.
- **Corpus.** Sigue con 525 archivos. El manifiesto es el de la r03, porque develop no lo toca.

### Mis scripts sobre la punta

- `r01_02` da 11/11.
- `r01_05`, `r02_02` y `r03_02` dan 0 casos.
- `r02_03` da 3 OK.
- `r03_01`:
  - sobre `2980b8c6..0229f899` (la limpieza tal como se aplicó) da los 5 casos históricos;
  - sobre `2980b8c6..HEAD` da 7, todos de la memoria de T-204, que H-09 y el rebase reescribieron (cuotas 1533 y estado aplicado). Son esperados.
- `r04_01_mutantes_revisor_cierre.py`: 10 de 10 muertos. Adapta los textos de Q1 y de Q4, que pasa a `ruff=1533 → 2735`.
- `mutantes.py` da 39 de 39 y `pruebas_scripts.sh` 455 passed (línea base 455).
- `pruebas_marco.sh` da 62 pasan y 0 fallan.
- corpus, refs-vivas, secretos y NFC están en verde.

### Hallazgo

**H-14 · baja · La limpieza de `.docs/` no cubre lo que trajo el rebase, y `limpiar_docs.py` reescribiría evidencia de esos tickets.**
- **Reproducir:** `r04_02_limpieza_tras_rebase.py` da 3 casos.
  - `limpiar_docs.py`, sin opciones, propone 7 cambios en T-196, T-201 y T-203. Son tickets de develop, escritos antes de que T-204 quitara el Forex. INC-T204-03 da la limpieza por aplicada y no los menciona.
  - De esos 7, dos son evidencia medida y el script la reescribiría. Uno es «Pytest: A 8415 (antes 8400), FX 68, B 176» de T-196 `qa.md`, porque `RE_EVIDENCIA` solo reconoce `pytest` y `mypy` en minúscula. El otro es la continuación «T-201 sola), A-Forex 174, B 159…» de T-203 `qa.md`, porque la palabra «mypy» está en la línea anterior.
  - Esa misma línea de T-196 aparece dos veces (líneas 87 y 168).
- **Corrección:**
  1. En `RE_EVIDENCIA`, hacer insensibles a mayúsculas `mypy`, `pytest` y `ruff`, y reconocer como evidencia un recuento `(?:A-Forex|FX) \d+, B \d+`. Añadir las tres líneas a `test_h03_limpiar_conserva…`.
  2. Después, una de dos:
     - aplicar `limpiar_docs.py --aplicar` a lo que quede: las tres filas «| A-Forex, B | sin tocar | sin tocar |» de T-196, T-201 y T-203 `pruebas.md`, y la enumeración «(A, A-Forex, B, …)» de T-203 `qa.md`, línea 54;
     - o declarar en INC-T204-03 que T-196, T-201 y T-203 se quedan como registro.

     La primera es coherente con «definitivamente» y con lo que se hizo con los demás tickets.
- **Regresión:** `r04_02` da 0 casos, y `limpiar_docs.py` propone 0 cambios o solo los declarados.

### Scripts nuevos (`revisores/`)

- `r04_01_mutantes_revisor_cierre.py`: 10 de 10 muertos.
- `r04_02_limpieza_tras_rebase.py`: 3 casos (H-14).

## Segunda ronda de cierre · 2026-11-25 · el mismo revisor

**Veredicto final: APTO, sin ningún hallazgo abierto.** H-14 está corregido. La limpieza que aplicó la coordinación (`594f8541`) no toca evidencia, y el segundo rebase, sobre develop `6c8910c1` (T-205), no ha perdido nada.

He revisado `594f8541` (`wip/t204`). El gate de cierre (`gate_t204_cierre2.log`, sobre `ef3fd250`) da **10/10**, con pytest A 8577 y B 176. De `ef3fd250` a `594f8541` solo cambian `.docs/` y `docs/`: 7 ficheros. No lancé otro gate.

### H-14

- `r04_02_limpieza_tras_rebase.py` da 0 casos.
- `RE_EVIDENCIA` ya no distingue mayúsculas y reconoce el recuento «FX N, B N». `test_h03` tiene 5 casos más, y los mutantes M40 y M41 mueren.
- `limpiar_docs.py`, sin opciones, da 0 líneas.
- **La limpieza de `594f8541`** cambia 5 líneas: la fila «| A-Forex, B | sin tocar | sin tocar |» de T-196, T-201, T-203 y T-205 `pruebas.md`, y la enumeración de T-203 `qa.md`, en la línea 54. Además, INC-T204-03 pasa a decir que están aplicadas.
  - **Es exactamente lo que produce el script.** Ejecuté `limpiar_docs.py --aplicar` en una extracción de `f1b72f17` y el diff de `.docs/` es idéntico.
  - `r03_01_limpieza_aplicada.py f1b72f17 594f8541` da 0 casos: ninguna línea con T-204, encargo, evidencia medida, cita «…» ni orden entre `…`.
  - Las tres líneas de evidencia de H-14 están byte a byte igual que en develop: T-196 `qa.md`, líneas 87 y 168, y T-203 `qa.md`, línea 109.

### El segundo rebase no ha perdido nada

- **Ficheros.** El conjunto de ficheros cambiados frente a la base es el de la punta anterior más los 5 de la limpieza y los ficheros nuevos del ticket. No falta ninguno.
  - `bloque_a/`, `bloque_b/` y `docs/evidencias_pruebas_bloque_a.md` están idénticos a `6c8910c1`.
  - Los ficheros que solo toca T-204 están igual que en la punta anterior, salvo los del cierre 2.
  - En el diario, el diff contra develop solo quita líneas del Forex.
- **Cuotas.** ruff 1533: la medida de A y B en la punta es idéntica línea a línea a la de develop, que en `6c8910c1` sigue con la cuota en 2735. mypy A 67, mypy B 159, A ≥ 607 y B ≥ 174. La colección de pytest de A es idéntica a la de develop: 8579 pruebas, de las que pasan 8577.
- **Deuda.** 201 filas, la de T-205 incluida, idéntica a develop. Solo cambia la de T-204, como se esperaba.
- **Incidencias.** 69 bloques. Las de develop están idénticas, y solo cambia INC-T204-03, como se esperaba.
- **Batería del marco.** `pruebas_parametros_doc_t83.py` da 109 comprobaciones en verde. Lee la deuda.

### Mis scripts y las pruebas

- `r01_02` da 11/11.
- `r01_05`, `r02_02`, `r03_02` y `r04_02` dan 0 casos.
- `r02_03` da 3 OK.
- `r04_01` da 10 de 10 muertos.
- `mutantes.py` da 41 de 41 y `pruebas_scripts.sh` 460 passed (línea base 460).
- corpus (525), refs-vivas, secretos y NFC están en verde.

### Resumen de la QA

- **Rondas:** r01 (8 hallazgos), r02 (4), r03 (1), cierre (1) y segundo cierre (0).
- **Hallazgos:** H-01 a H-14, todos cerrados, cada uno con su prueba o su script de regresión. Ninguno va a la deuda.
- **Ticket:** puede pasar a CERRADO.
