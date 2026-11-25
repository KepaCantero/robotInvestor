# T-204 · Análisis técnico

## Causa

Orden del operador del 25-11-2026: «olvídate del bloque A forex. Elimínalo». Después la amplió: «Elimina el bloque A Forex definitivamente» y «Haz esas tres cosas. Te doy mi consentimiento».

El Bloque A Forex era una prueba antigua (D-20 de la Constitución; aclaración del 13-11-2026). Seguía en el repositorio con su gate propio: mypy, pytest, 180 archivos del corpus y 1204 líneas de ruff. Ninguna otra pieza lo usaba.

## Archivos cambiados y por qué

| Archivo | Cambio |
| --- | --- |
| `bloque_a_forex/` | `git rm -r`: 317 archivos |
| `tools/check_all.sh` | `EJECUTORES` y `PAQUETES` con A y B. El YAML solo de A y B. El bucle de mypy recorre `"${!PAQUETES[@]}"` (antes, índices fijos `0 1 2`). Sin pytest del Forex; el de B usa `EJECUTORES[1]`. La cabecera dice 10 comprobaciones y que A y B son los bloques desde T-204. Ya no menciona el Forex: lo vigila la prueba nueva |
| `tools/cuotas.txt` | Fuera `mypy_bloque_a_forex` y `pytest_bloque_a_forex`. `ruff` pasa de 2806 a 1604, la medida del gate con A y B |
| `tools/corpus_manifest.txt` | `./tools/check_all.sh --update-corpus`: 705 → 525 huellas. El diff solo quita las 180 líneas de `bloque_a_forex/`. Antes de re-congelar, `corpus_integridad.py` daba exactamente esas 180 como «ELIMINADO» y ninguna otra diferencia |
| `tools/corpus_integridad.py` | El alcance y el `es_corpus` solo de `bloque_a` y `bloque_b` |
| `tools/refs_vivas.py` | Fuera de `RAICES_VALIDAS` y de `BLOQUES`. `RETIRADOS` y `REGISTROS`, y `bloque_retirado()` (INC-T204-02) |
| `tools/requisitos_entorno.txt` | Solo el comentario de arch. Las versiones son las mismas: el Forex tenía las mismas dependencias que A |
| `.docs/scripts/preparar_entorno.sh`, `.docs/scripts/qa_rama.sh` | Instalan y prueban A y B |
| `.docs/scripts/pruebas_gate_bloques.py` | Nueva (33 pruebas). Ver «Diseño» del README |
| `.docs/scripts/prueba_refs_vivas.py` | 18 casos del bloque retirado (25 → 43) |
| `.docs/scripts/linea_base_pruebas.txt` | 399 → 432 |
| `.secrets.baseline` | Fuera las entradas de dos ficheros borrados del Forex. Se mantiene el formato de detect-secrets (`indent=2`) |
| `CLAUDE.md` | Título, tabla de bloques con una nota de T-204, flujo, línea base, «10/10» (dos veces), trampa de pyprojects (solo INC-001), «cargas actuales», plan de fases (orden A → B, Fase 3 de bloque_a, Fase 4 sin el Forex), gate (525 archivos, 2 YAML, mypy ×2, pytest ×2) y comandos |
| `prompts/…`, `dashboard/prompts/01_DASHBOARD_V1.md`, `.agents/skills/ri-probar/SKILL.md` | Dos bloques, 10/10 y ninguna tarea sobre el Forex |
| `docs/AVANCE.md` | Fila del 03-11 marcada con T-204. Fuera «El Forex queda en T-115». Fila nueva de T-204 |
| `docs/incidencias.md` | Fuera INC-002 (solo del Forex) y su mención en INC-001. Nuevas INC-T204-01 a 04 |
| `sistema_global/README.md`, `Briefing_de_arranque.md`, `Decisiones_del_operador_Bloque_A.md`, `documentos_0/V0.75_…` | El A Forex fuera de las listas de bloques. La fila de su decisión pasa a la del 25-11-2026 |
| `Deuda_tecnica_y_pendientes_del_operador.md` | Fuera T-115 (solo del Forex). Reescritas T-54 (el paso de la carpeta lo hizo T-204), T-96, T-103, T-105 (queda B), T-120 y T-199. Fila T-204 nueva |
| `.docs/README.md`, `.docs/knowledge/01_que-es-el-robot-investor.md` | Una nota y la fila marcadas con T-204. El script nuevo, en la tabla |
| `.docs/memoria/compartida/2026-11-25_bloque-a-forex-eliminado.md` (+ `INDICE.md`) | Entrada nueva con `memoria.sh` |

## Lo que no se pudo hacer: bloqueado por el sistema de permisos

- **Constitución global.** La ampliación pedía la enmienda con su registro. Al escribir `Constitucion_Global.md`, el sistema de permisos de la sesión lo denegó por «acción destructiva o no deseada». Claude no lo ha sorteado: la orden llegó por otro agente, y eso no es el consentimiento del usuario de la sesión.
  - **Qué queda preparado:** el cambio completo, en `enmienda4_constitucion.patch` (`git apply --check` en verde sobre esta rama). Es la V0.7 con la enmienda 4, el cambio 43, D-48, D-20 reducida a B Forex, §2 y §14, y la línea del §15.
  - **Comprobado:** la batería del marco que lee la Constitución (`pruebas_parametros_doc_t83.py`) pasa con el parche aplicado.
  - **Dónde está:** INC-T204-01, `[PROPUESTO]`.
- **Limpieza de `.docs/`.** `limpiar_docs.py --aplicar` se denegó igual.
  - **Qué propondría:** sin opciones, el script lo dice (`limpiar_docs_propuesta.txt`): 18 líneas borradas y unas 280 reescritas, en 147 ficheros.
  - **Lo que no hay:** ningún ticket cuya pieza sea solo el Forex, ninguna nota de memoria solo del Forex y ninguna entrada del diario solo del Forex.
  - **Regla de la evidencia literal:** las órdenes entre `…` o en bloques de código, y los scripts y logs de `revisores/`, se conservan. Cambiarlas daría por ejecutado algo que no se ejecutó, como un ruff de 2902 «sobre A y B».
  - **Dónde está:** INC-T204-03.

## Decisiones y desviaciones

- **refs-vivas con un bloque retirado en lugar de la allowlist (INC-T204-02).** Las tres citas de tickets a `bloque_a_forex/11_Ejecutor` (T-176, T-177 y T-199) son registros y se quedan. En los documentos vivos, la cita se corrige o se marca con T-204: `CLAUDE.md`, `prompts/FASE0_VERIFICADOR_IDS.md`, `docs/AVANCE.md` y `.docs/knowledge/01_…`.
- **La prueba nueva está en `.docs/scripts/` y no en el gate.** Así el gate queda en 10 comprobaciones. La ejecutan `pruebas_scripts.sh` y, con él, `commit.sh` y `commit_limpio.sh`.
- **Bucle de mypy por la lista.** Antes eran índices fijos; con dos paquetes, `0 1 2` habría medido un paquete vacío con una cuota vacía (M3 lo comprueba).
- **«12/12» histórico.** Se conserva donde cuenta lo que pasó. Son las tablas de los tickets, el relevo, `requisitos_entorno.txt` («pasó 12/12 el 11-11-2026») y `.docs/knowledge/05_historia-del-proyecto.md`.
- **`AGENTS.md` no cambia.** Remite a `CLAUDE.md` y no nombra bloques, líneas base ni «12/12».
- **Observación fuera del alcance.** La skill `ri-probar` dice «A ≥ 439», pero la línea base de A es 607 desde T-102. Solo se ha quitado el Forex de esa línea.

## Límites conocidos

- El `.venv` compartido sigue teniendo `bloque-a-forex` instalado en modo editable. No afecta al gate: `--exclude-editable` no lo cuenta y nadie lo importa. Se va al recrear el entorno.
- El detector de la prueba busca `forex`, `fx` y `_fx` como palabra. Un nombre nuevo inventado para el mismo bloque no lo vería. Las pruebas del gate real sí verían un ejecutor de más, porque fijan la lista a A y B.

## Comandos

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider .docs/scripts/pruebas_gate_bloques.py   # 33 passed
.venv/bin/python .docs/scripts/prueba_refs_vivas.py                                       # 43/43
.venv/bin/python .docs/tickets/T-204/mutantes.py                                          # 29 de 29 muertos
.docs/scripts/pruebas_scripts.sh                                                          # 432 passed
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_b/11_Ejecutor | wc -l   # 1604
./tools/check_all.sh                                                                      # 10/10
.venv/bin/python .docs/tickets/T-204/limpiar_docs.py                                      # propuesta para .docs/, sin aplicar
git apply --check .docs/tickets/T-204/enmienda4_constitucion.patch                        # enmienda 4, sin aplicar
```

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-01 (media) | `docs/AVANCE.md`: «la enmienda de la Constitución queda propuesta, sin aplicar (INC-T204-01)» | `test_h01_avance_no_da_por_aplicada_otra_version_de_la_constitucion`; `r01_05` en verde |
| H-02 (media) | La enmienda pasa a llamarse **enmienda 6**. La 4 (`.docs/diseno/enmienda_4/`) y la 5 (`.docs/diseno/enmienda_5/`) son propuestas pendientes. INC-T204-01 declara que la numeración provisional de la 5 (V0.7, cambios 43–79, D-48–D-84) se corre en uno si la 6 se ratifica antes, como prevé su propia regla. El cambio 17 y las líneas de §2 y §14 llevan «enmienda 6, D-48». La cabecera pasa a «Nov 25, 2026». El parche lo genera `generar_enmienda.py`; el nombre del fichero, `enmienda4_constitucion.patch`, se conserva porque lo cita el script del revisor | `test_h02_el_parche_guardado_es_el_de_la_enmienda_6` (se omite si la Constitución ya no está en la V0.6); `r01_04` da 0 casos; `git apply --check` en verde; `pruebas_parametros_doc_t83.py` en verde con el parche aplicado en una copia aparte |
| H-03 (media) | `limpiar_docs.py` no toca: las líneas con la marca T-204; las que dan resultados de gate o de suites (`RE_EVIDENCIA`: 12/12, «12 de 12», «N pasan», ×3, «passed», cuotas, mypy, pytest, ruff, «doce controles»); los encargos (`encargo_revision_astra*.md`, en `.docs/diseno/` y en los tickets); la viñeta del A Forex de la historia («tres entregas»); y una frase cuya reescritura recortaría una cita «…». Propuesta regenerada: 12 borradas y 95 reescritas, en 80 ficheros | `test_h03_limpiar_conserva_la_marca_la_evidencia_y_las_citas` (8 casos), `test_h03_limpiar_borra_lo_que_solo_habla_del_forex_y_recorta_lo_mixto`, `test_h03_limpiar_no_entra_en_los_encargos_ni_en_el_ticket`; mutantes M32 a M36; `r01_01` con la propuesta nueva: 0 casos |
| H-04 (baja) | La skill `ri-probar` dice «A ≥ 607, B ≥ 174» | `test_h04_las_lineas_base_citadas_son_las_de_cuotas` (skill y `CLAUDE.md`) |
| H-05 (baja) | En `CLAUDE.md`, «43 hallazgos» en `.secrets.baseline` (eran 48; se quitaron los 5 del Forex). En `.pre-commit-config.yaml`, «(10 gates)» | `test_h05_hallazgos_de_secrets_baseline_y_gates_del_pre_commit` |
| H-06 (baja) | `refs_vivas.py`: la marca se busca como palabra (`marcada()`: `(?<![\w-])T-204(?!\d)`), y «=» solo parte las palabras que empiezan por «-». Tres casos nuevos en `prueba_refs_vivas.py` (46 en total) | Esos tres casos; `r01_02` 11/11; Q1 (adaptado) y Q7 muertos por las pruebas; mutantes M30 y M31 |
| H-07 (baja) | Prueba que mide ruff como el gate y exige que la cuota sea igual a la medida | `test_h07_la_cuota_de_ruff_es_la_medida_como_el_gate`; Q4 muerto |
| H-08 (baja) | INC-T204-04 añade el README de los goldens de A (T-115, cuya fila quitó T-204) y el F9 de B (23 líneas «F9 Forex V1.0» y las temáticas TFX-04, 05 y 09), con la lista de los cuatro ficheros de A y B que nombran el Forex | `test_h08_inc_t204_04_cita_todo_lo_que_nombra_el_forex_en_a_y_b` |

**Mutantes del revisor.** Q1 se escribió sobre el texto viejo, «RETIRADOS[retirado] not in linea», que la corrección de H-06 sustituye por `marcada()`. `r02_mutantes_revisor.py` ejecuta el script del revisor sin cambiarlo, con Q1 aplicado al código nuevo con el mismo sentido («la marca vale como prefijo T-20»). Los diez quedan muertos por las pruebas.

## Ronda r03 (QA r02 NO APTO)

La r02b de la coordinación aplicó la enmienda 6 (V0.7) y la limpieza de `.docs/` por orden del operador («Todo»). La r03 corrige lo que quedaba.

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-09 (media) | Lo que decía «pendiente» pasa a decir lo aplicado, en pasado, en: el cuerpo de INC-T204-01 y 03, la fila T-204 de la deuda, la memoria `compartida/2026-11-25_bloque-a-forex-eliminado`, el alcance, el inventario y los riesgos del README del ticket, y `sistema_global/README.md` (V0.7 desde el 25-11-2026). La memoria es de hoy y del mismo ticket, sin integrar: se corrige en el sitio y no se sustituye, porque `r02_02` la lee por su nombre | `test_h09_los_documentos_vivos_dicen_el_estado_aplicado`; `r02_02` da 0 casos |
| H-10 (media) | Desde la V0.7, `test_h02_la_enmienda_6_de_la_constitucion` comprueba invariantes del contenido: el párrafo «Enmiendas» cita la enmienda 6, existe la fila D-48, D-20 y el cambio 17 van anotados, y el A Forex solo aparece en las líneas de la enmienda 6 y en el cambio 43. Ya no aplica el parche. El `git apply -R --check` queda como comprobación del ticket (`pruebas.md`). En la V0.6 se sigue comparando con `generar_enmienda.py` | `r02_03`, tercer caso (cabecera en V0.8), en verde |
| H-11 (baja) | Vuelven a su texto de antes de la limpieza (`253f33fd`) cuatro líneas de evidencia. En el informe del revisor aparecían con el nombre del fichero siguiente del diff, y estos son los ficheros reales: `.docs/tickets/T-106/qa.md` (dos líneas, las 109 y 217), `.docs/tickets/T-187/pruebas.md:35` y `.docs/tickets/T-199/qa.md:26`. En `.docs/tickets/T-166/pruebas.md:39` se corrige la concordancia («la suite de B no se toca»). `RE_EVIDENCIA` de `limpiar_docs.py` reconoce además «N/N», «N de N en verde», «pasadas» y «tres suites, ejecutores o bloques». Sobre el árbol actual, `limpiar_docs.py` ya no propone nada (0 líneas) | Cinco casos nuevos en `test_h03_limpiar_conserva_la_marca_la_evidencia_y_las_citas`; mutante M37; `r02_01 253f33fd <commit de la r03a>`: 0 casos |
| H-12 (baja) | `bloque_retirado()` parte por «=» también las palabras de la forma `NOMBRE=` (`RE_ASIGNACION`), como `PYTHONPATH=bloque_a_forex/11_Ejecutor`. Un nombre de archivo con «=» (`bloque_a_forex/a=b.md`) no se parte | Dos casos nuevos en `prueba_refs_vivas.py` (48); `r02_03`, dos primeros casos; `r01_02` 11/11; mutante M38 |

**Otro cambio, fuera de los hallazgos.** La sección r02 de `qa.md` citaba `` `docs/x.md` `` entre comillas de código. Es el fichero de juguete de `r02_03`, que no existe en el repositorio, y esa cita hacía fallar `refs-vivas`. Se reescribe como texto, «(docs/x.md)», sin cambiar nada más del informe.

## Ronda de cierre de la QA r03

- **H-13 (baja).**
  - En INC-T204-03, «Lo que se corrigió después», los tickets corregidos ahora son los reales: dos líneas de T-106 `qa.md`, T-187 `pruebas.md` y T-199 `qa.md`, y la concordancia de T-166 `pruebas.md`.
  - La fila T-54 de la deuda conserva la cita de la D-20 antigua y añade «; desde la V0.7, enmienda 6, D-48, D-20 solo nombra B Forex». INC-T204-01 lo cuenta.
  - Prueba: `test_h09` comprueba también la fila T-54, y el mutante M39 la quita.
  - `r03_02` da 0 casos.
- **Observación del revisor.** `test_h02` busca la fila «| 17 |» solo en el §0, antes de «## 1.», porque la tabla de riesgos del §15 también numera sus filas.
- **Rebase sobre `origin/develop`** (`d11662ff`, que incluye T-196, T-201 y T-203). Hubo conflictos en `tools/cuotas.txt`, `docs/incidencias.md` y la deuda.
  - En `tools/cuotas.txt` salen las líneas del Forex y ruff queda en la medida del gate sobre A y B, 1533 (2735 de develop menos 1202 del Forex, línea a línea). mypy A queda en 67, el de develop, medido.
  - En las incidencias y la deuda se conservan los dos lados. De las entradas que T-204 reescribía en cada ronda (la fila T-204 e INC-T204-01) se queda solo su versión nueva.
  - El resultado se comprobó contra develop más los cambios de T-204. En la deuda están todas las filas nuevas de develop (T-196, T-201 y T-203) y todas las de T-204, y ninguna más. En las incidencias, el fichero de develop pierde INC-002 y gana el bloque INC-T204-01 a 04.
  - Las cifras vivas de ruff (AVANCE, fila T-204 y memoria) dicen 1533 tras el rebase.
  - Las líneas base de A (607) y B (174) son las de develop.

## Cierre 2 (H-14 de la ronda de cierre de la QA r03)

- **Rebase** sobre `origin/develop` `6c8910c1` (T-205). Las incidencias y la deuda conservan los dos lados: INC-T205-01 y la fila T-205 de develop, más lo de T-204. Se comprobó línea a línea contra develop más los cambios de T-204: no falta ni sobra nada y no hay duplicados. ruff sigue en 1533 (medida) y mypy A en 67.
- **`RE_EVIDENCIA`.** mypy, pytest y ruff, con cualquier mayúscula. Un recuento «A-Forex N, B N» o «FX N, B N» también es evidencia: cubre la línea de continuación de T-203 `qa.md`. Hay 5 casos nuevos en `test_h03`, y los mutantes M40 y M41 mueren.
- **Limpieza de los tickets del rebase.** La coordinación decidió aplicarla. El sistema de permisos de la sesión bloqueó `limpiar_docs.py --aplicar`, y no se sorteó.
  - Las 5 líneas que quedan están en `limpiar_docs_propuesta_cierre2.txt`: la fila «A-Forex, B» de T-196, T-201, T-203 y T-205 `pruebas.md`, y la enumeración de T-203 `qa.md`.
  - INC-T204-03 las declara como registro mientras no se apliquen.
  - `r04_02` da 0 casos.
