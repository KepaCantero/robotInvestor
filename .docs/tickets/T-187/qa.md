# T-187 · QA independiente

- **Revisor:** claude (sesión de QA sin el contexto de la implementación; solo plan, código y datos del ticket) · **Ronda:** r01 · 18-11-2026
- **Base revisada:** `86f0385` («wip local: T-187 paso 3», sobre `2a34b7a` y `c9daa4e`), en una copia nueva (`git worktree add <scratchpad>/qa187 86f0385`) con el `.venv` del proyecto enlazado.

## Reproducción desde limpio

| Orden | Resultado |
| --- | --- |
| .venv/bin/python -m pytest -q .docs/tickets/T-187/test_revision_prompts.py (ruta de la r01; desde la r02, `.docs/scripts/pruebas_revision_prompts_pb51.py`) | 87 pasadas |
| .venv/bin/python .docs/tickets/T-187/revision_prompts_pb51.py --comprobar (ruta de la r01; desde la r02, `.docs/scripts/revision_prompts_pb51.py`) | «igual», 0 |
| .venv/bin/python .docs/tickets/T-187/mutantes_pb51.py (ruta de la r01; desde la r02, `.docs/scripts/mutantes_revision_prompts_pb51.py`) | 63 de 63 muertos |
| `(cd bloque_a/11_Ejecutor && pytest -q tests/test_t187_pb51.py)` | 5 pasadas |
| `.venv/bin/python .docs/scripts/evidencias_plan_a.py` | mapa coherente (67 pruebas del plan, 301 citadas, todas existen) |
| `./tools/check_all.sh` (completo) | ver «Gates» abajo |
| `python3 -I revisores/r01_01_recuento.py .` (recuento propio, sin el script del ticket) | lote 1: 66/2/22; lote 2: 58/5/27; lote 3: 74/2/14; lote 4: 62/0/18; total 260/9/81; 96,65 % sobre 269 y 74,29 % sobre 350. Coinciden con el informe |

Ni el corpus (`bloque_a/02_System_prompts`), ni los otros bloques, ni `sistema_global/marco_comun_c/` cambian en el diff. Sin secretos, datos personales ni identificadores de modelo en lo añadido (búsqueda sobre el diff).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 a CA-8 | sí | Pruebas del ticket (87), mutantes (63), `--comprobar`, INC-T187-01 |
| CA-9 | no | Recuentos y fallo cerrado de los casos previstos, sí; pero «PB-51 sale "Superada"» no es honesto con el plan (H-01), el paso 3 no tiene 10 afirmaciones técnicas en 28 prompts (H-02), el comentario atribuye a los revisores lo que sus notas no dicen (H-03), la fuente de los veredictos no se declara (H-04) y hay entradas malas que dan traza o pasan (H-05) |

## Los cinco puntos del encargo

1. **«Superada» o «Superada en parte».** El plan dice, para PB-51: *Resultado esperado*: «12 secciones en todos; sección 10 organizada por áreas con fórmulas y referencias (autor, año, título) sin DOI inventados; **ninguna afirmación técnica errónea en la muestra**»; *Criterio de aprobación*: «100 % de prompts con estructura completa; ≥ 95 % de afirmaciones muestreadas correctas; **tamaños dentro de las orientaciones**». Las propias evidencias definen «Superada» como «comprueban **todo** el criterio de aprobación del plan, salvo lo que solo existe con tiempo real o con el modelo real» y «Superada en parte» como «queda alguna cláusula del criterio que el ejecutor podría comprobar y ninguna prueba comprueba». Aquí quedan dos cláusulas sin comprobar que no dependen ni del tiempo real ni del modelo: los tamaños de 21 de los 35 papeles (no hay orientación) y el resultado esperado, que se incumple (9 ERRONEA), además de un denominador `[PROPUESTO]`. **Decisión: «Superada en parte»** (H-01, corrección exacta abajo).
2. **Fidelidad de `comentario.json`.** Las 9 erratas son fieles a las notas (error y corrección salen de ellas, sin añadir datos). Cuatro de los cinco casos dudosos también. Pero hay dos atribuciones que no están en ninguna nota: «Los revisores de los lotes 1 y 2 consideran discutibles» AF-AG-22-03 y AF-AG-24-05 (las dos son del lote 1, y ninguna nota dice «discutible»), y para AF-AG-21-07 «la búsqueda web no confirmó el año», cuando la nota dice justo lo contrario (la confirma con el capítulo de Springer de 2021, «Búsqueda web»). Además, la elección de los cinco dudosos no tiene un criterio escrito: AF-AG-21-07 no tiene matiz en la nota y AF-MC-02-04 («ojo: no garantiza batir al ingenuo…») sí lo tiene y queda fuera. → H-03.
3. **Prueba del ejecutor que depende de `.docs/tickets/`.** Que una prueba del ejecutor cargue un script de `.docs/` tiene precedente (`test_t142_cadena_b.py`, `test_t136_coste.py`, `test_t140.py`…), pero siempre de `.docs/scripts/`; ninguna carga un script de un ticket. El script es repetible (PB-51 se repite en la batería de regresión ante cada versión nueva de un prompt, §6 del plan), y la regla 4 de `.docs/README.md` lo manda a `.docs/scripts/` con su fila en la tabla. Además, sus 87 pruebas y sus 63 mutantes no los ejecuta ningún gate (`pruebas_scripts.sh` solo recoge `.docs/scripts/pruebas_*.py`): si alguien cambia el script, solo lo verían las 5 pruebas del ejecutor. Ampliar `evidencias_plan_a.py` no hace falta: mezclaría el generador genérico de evidencias con una revisión concreta. → H-06 (baja).
4. **Denominador de INC-T187-02.** Muestreé 15 NO_VERIFICABLE (`revisores/r01_02_muestreo.py . NO_VERIFICABLE 15`): las 15 son reglas, umbrales, listas o convenciones internas del sistema (R25, niveles A–D de Q, vetos de §6, mapa TM- de F8, partición por hash…), sin literatura con la que contrastarlas. Sacarlas del denominador es razonable, **pero** entonces no son «afirmaciones técnicas» y la muestra del paso 3 («10 afirmaciones técnicas por prompt») queda corta: 43 de las 52 frases de la §6 son NO_VERIFICABLE, y 28 de los 35 prompts tienen menos de 10 verificables (Coordinador 2, Orquestador 3, Auditor y Redactor 5) → H-02. Contrasté 10 CORRECTA al azar (`r01_02_muestreo.py . CORRECTA 10`: retardos de Friedman, XIV en 2018, ISM, EUDR, «¿quién está al otro lado?», Gwillim Law 2011, Fama-French/Barras-Scaillet-Wermers/Kosowski et al., Crameri et al. 2020, Coval-Stafford 2007 y Lou 2012, ETF de bitcoin y ether): de acuerdo con las 10. De las 9 ERRONEA confirmo 8 (GSW 2010 no es un modelo afín; la matriz frente al cubo de swaptions; N = exp(entropía) de Meucci; la PBO de 2017; Tetlock 2005; el 26 % y el 58 % de McLean-Pontiff; el factor 2 del tamaño por grupo; ACT/360 frente a ACT/365 al 3 % da unos 4 pb). AF-AG-22-03 (costes de ESMA) no la puedo confirmar ni refutar con una búsqueda: las cifras cambian según el año del informe y según se trate de costes corrientes o totales. Queda como ERRONEA y la sensibilidad ya muestra que no cambia el veredicto. Lo que sí pesa: según sus notas, 251 de las 260 CORRECTA son «conocimiento propio» del revisor y solo 5 se contrastaron con búsqueda; de las 9 ERRONEA, 5 se hallaron buscando. El plan pide afirmaciones «contrastadas con su referencia», y eso no se declara en ningún sitio → H-04.
5. **Gates.** `./tools/check_all.sh` completo desde mi copia limpia: ver «Gates». Cuotas sin cambio: ruff 2807, mypy 102/174/159.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Prueba de regresión | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| H-01 | alta | `python3 -I .docs/tickets/T-187/revisores/r01_04_comprobaciones_cierre.py` (línea H-01); `grep PB-51 docs/evidencias_pruebas_bloque_a.md` | Esperado: «Superada en parte», porque los tamaños de 21 papeles quedan sin comprobar y el resultado esperado «ninguna afirmación técnica errónea» se incumple (9). Obtenido: «Superada» (cobertura `AUTOMATICA`) | En `mapa_plan_pruebas.json`, PB-51: `"cobertura": "PARCIAL"` y, al principio de `no_comprueba`: «El resultado esperado del plan, "ninguna afirmación técnica errónea en la muestra", no se cumple: 9 ERRONEA (INC-T187-03), pendientes de la próxima entrega del corpus. "Tamaños dentro de las orientaciones" solo se comprueba en los 14 papeles con tope; los otros 21 no tienen orientación (INC-T187-01, T-57).», y después el texto actual. En `comprueba`, quitar «(10 por prompt)» (H-02). Regenerar las evidencias (`evidencias_plan_a.py --ejecutar`: 39 Superada y 20 Superada en parte). Ajustar en coherencia el CA-9 y los «Resultados» del README, la viñeta «"Resultado esperado" frente al criterio» de INC-T187-02 («PB-51 queda "Superada en parte"»), el handoff, `pruebas.md` y la fila T-187 de la deuda | En `tests/test_t187_pb51.py`, `test_pb51_fila_del_mapa_superada_en_parte`: lee el mapa y exige `cobertura == "PARCIAL"` y que `no_comprueba` cite «ninguna afirmación técnica errónea», «INC-T187-03» y «21 papeles»; y `r01_04` (H-01) en verde | abierto |
| H-02 | media | `r01_04` (línea H-02); `r01_01_recuento.py` | Esperado (paso 3 del plan): 10 afirmaciones técnicas por prompt, o la falta declarada. Obtenido: 81 de las 350 no son técnicas (43 de 52 en la §6); 28 de 35 prompts con menos de 10 verificables (mínimo 2, Coordinador); no se declara en ningún sitio, y el mapa dice «(10 por prompt)» | (a) En `informe_contraste`, añadir a la tabla por prompt la columna «Verificables» y una línea con los prompts por debajo de 10 (28; Coordinador 2, Orquestador 3, Auditor 5, Redactor 5…). (b) En INC-T187-02, viñeta nueva: «La muestra tiene 269 afirmaciones técnicas y no 350: 28 de 35 prompts quedan por debajo de 10 (mínimo 2, Coordinador); 43 de las 52 frases de la §6 son reglas internas». (c) En `no_comprueba` de PB-51: «El paso 3 pide 10 afirmaciones técnicas por prompt: 28 de 35 tienen menos de 10 verificables». Recomendado, si el operador lo quiere completo: muestra de reposición con la semilla «T-187 · PB-51 · reposición\|archivo», solo de la §10, entre las candidatas no muestreadas, hasta 10 verificables por prompt, juzgada por revisores independientes | En `test_revision_prompts.py`, `test_contraste_cuenta_verificables_por_prompt_y_lista_los_cortos` (lotes sintéticos con un prompt de 3 verificables: sale en la lista y en la columna); `r01_04` (H-02) en verde | abierto |
| H-03 | media | `r01_04` (línea H-03); comparar `comentario.json` con `lote_1.json` y `lote_2.json` (`r01_01_recuento.py . --volcar`) | Esperado: lo que el comentario atribuye a los revisores está en sus notas. Obtenido: «los revisores de los lotes 1 y 2 consideran discutibles» AF-AG-22-03 y AF-AG-24-05 (las dos son del lote 1 y ninguna nota lo dice); AF-AG-21-07, «la búsqueda web no confirmó el año», contradice la nota. Se repite en el informe y en INC-T187-02 e INC-T187-03 («discutible para el revisor») | (a) En `comentario.json`, cada errata, dudosa y discutible lleva `"cita_nota"`, un fragmento literal de la nota del revisor que la sostiene, y `contraste()` termina con 2 si `cita_nota` no es una subcadena de la nota de ese id. (b) Quitar `discutibles` y la sección de sensibilidad, o dejarla con la atribución verdadera («a juicio de quien escribe el comentario, no de los revisores»), y corregirlo en INC-T187-02 e INC-T187-03. (c) Quitar AF-AG-21-07 de las dudosas (su nota la confirma sin matiz), o reescribir el matiz con lo que dice la nota. (d) Escribir el criterio de las dudosas: CORRECTA cuya nota trae un matiz explícito («Matiz», «exagera», «difieren», «ojo»), y aplicarlo (entra AF-MC-02-04) | En `test_revision_prompts.py`, `test_contraste_falla_cerrado_si_la_cita_no_esta_en_la_nota` (una `cita_nota` inventada da 2); `r01_04` (H-03) en verde | abierto |
| H-04 | media | `r01_01_recuento.py` y el recuento por fuente de este informe (las notas dicen «Conocimiento propio», «Búsqueda web» o «Cálculo propio») | Esperado (paso 3 del plan): afirmaciones «contrastadas con su referencia», o la diferencia declarada. Obtenido: 251 de las 260 CORRECTA se juzgaron de memoria y solo 5 con búsqueda (5 de las 9 ERRONEA salieron buscando); ni el informe, ni las incidencias, ni el mapa lo dicen | (a) En `contraste()`, clasificar cada nota por su fuente («búsqueda web» sin «sin búsqueda web» → web; «conocimiento propio» o «cálculo propio» → propio; el resto, sin fuente) y en el informe, tabla veredicto × fuente. (b) En INC-T187-02 y en `no_comprueba`: «De las 260 CORRECTA, 251 las juzgó el revisor de memoria, sin consultar la referencia; la QA r01 contrastó 10 al azar y coincidió en las 10» | En `test_revision_prompts.py`, `test_contraste_cuenta_veredictos_por_fuente` (tres notas sintéticas, una de cada fuente, incluida «sin búsqueda web» como propia) | abierto |
| H-05 | baja | `.venv/bin/python .docs/tickets/T-187/revisores/r01_03_ataques_contraste.py`: 3 de 10 casos fallan cerrado | Esperado (README, «Cómo falla cerrado»): salida 2 sin traza. Obtenido: traza con `discutibles` no hashable (`TypeError`), un lote o el comentario en UTF-8 inválido (`UnicodeDecodeError`) o un `lote_9.json` que es una carpeta (`IsADirectoryError`). Pasan la validación un `revisor` en blanco, una dudosa con matiz vacío y una nota que es solo «—». Ninguno escribe nada, pero una traza sale con 1, igual que «difiere» de `--comprobar` | En `leer_lotes` y `leer_contraste`, capturar `UnicodeDecodeError` y `OSError` junto a `JSONDecodeError` y convertirlos en `ContrasteInvalido`. En `leer_lotes`, exigir `d["revisor"].strip()`. En `contraste()`, exigir que `discutibles` sea una lista de `str`, que cada valor de `dudosas` sea un `str` no vacío y que la nota tenga al menos una letra o cifra (`re.search(r"\w", nota)`) | En `test_revision_prompts.py`, un `pytest.mark.parametrize` con los 7 casos de `r01_03` que hoy no salen con 2; y `r01_03` en verde (10 de 10) | abierto |
| H-06 | baja | `grep -rn tickets bloque_a/11_Ejecutor/tests/test_t187_pb51.py`; `cat .docs/scripts/pruebas_scripts.sh` | Esperado: un script repetible (PB-51 entra en la batería de regresión de cada prompt nuevo) vive en `.docs/scripts/`, con sus pruebas en un gate. Obtenido: está en el ticket, y sus 87 pruebas y 63 mutantes no los ejecuta ningún gate | Mover con `git mv` a la carpeta `.docs/scripts/`: `revision_prompts_pb51.py` con el mismo nombre, `test_revision_prompts.py` con el nombre `pruebas_revision_prompts_pb51.py` (para que lo recoja `pruebas_scripts.sh`) y `mutantes_pb51.py` con el nombre `mutantes_revision_prompts_pb51.py`, con `--salida` por defecto en `.docs/tickets/T-187` (los datos se quedan en el ticket); fila nueva en la tabla de `.docs/README.md`; subir `.docs/scripts/linea_base_pruebas.txt` de 231 a 231 + 87 + las pruebas nuevas; `TICKET` → `SCRIPTS` en `test_t187_pb51.py`; una línea en `analisis-tecnico.md` que diga adónde se movió | `pruebas_scripts.sh` con la nueva línea base en verde; `test_t187_pb51.py` carga el script de `.docs/scripts/` | abierto |
| H-07 | baja | `grep -n "sin juzgar" .docs/tickets/T-187/informe_pb51.md` | Esperado: el informe dice el estado actual. Obtenido: «## Paso 3 · Muestra (preparada, sin juzgar)», cuando ya está juzgada | En `revision_prompts_pb51.py`, línea 847: «## Paso 3 · Muestra» (el texto de debajo ya dice cómo se sacó); regenerar el informe | `test_corpus_real_lo_generado_coincide_con_lo_guardado` y `--comprobar` tras regenerar; en `test_revision_prompts.py`, que el informe con contraste no contenga «sin juzgar» | abierto |

Fuera de los hallazgos (no hay que corregir nada): el denominador de las verificables es razonable para lo que de verdad no es técnico; de los invariantes del sistema, ninguno se toca (no hay ruta a órdenes, LLM ni controles en el diff; ningún número de configuración nuevo; los criterios `[PROPUESTO]` están en INC-T187-01 y 02 y en la deuda). AF-AG-22-03 la deja como ERRONEA una sola búsqueda sin resultado concluyente, y la sensibilidad ya cubre el caso.

## Scripts de esta ronda (`revisores/`)

- `r01_01_recuento.py`: recuento independiente desde los lotes y volcado de cada ERRONEA y dudosa con su nota y su comentario (`--volcar`).
- `r01_02_muestreo.py`: muestra reproducible (semilla de texto) de un veredicto dado, para contrastar a mano.
- `r01_03_ataques_contraste.py`: 10 entradas malas del paso 3; hoy 3 de 10 fallan cerrado (H-05).
- `r01_04_comprobaciones_cierre.py`: las comprobaciones de H-01, H-02 y H-03; hoy fallan las tres. En la ronda de cierre deben dar 0, como `r01_03` (10 de 10).

## Gates

`./tools/check_all.sh` completo, desde la copia limpia (`86f0385`): los 9 primeros gates en verde (corpus-integridad con 705 archivos, nombres-nfc, yaml-configs, secrets, refs-vivas, ruff 2807 = cuota, mypy A 102, FX 174 y B 159 = cuotas). La ejecución se cortó al llegar a los 30 minutos que tiene una tarea en segundo plano en esta sesión, mientras corría la suite de A (el equipo lo compartían otras dos suites de A de otras sesiones). Las tres suites, ejecutadas aparte en la misma copia: **A 8272 pasadas y 2 omitidas** (≥ 607, 53 min 53 s), **A-Forex 68** (≥ 68) y **B 176** (≥ 174). Equivale a 12/12, en dos tandas. La suite dirigida: `test_t187_pb51.py` 5, las pruebas del ticket 87, mutantes 63 de 63 y `ruff check` de `revisores/` sin hallazgos. Cuotas sin cambio.

## Veredicto

**NO APTO.** Hay un hallazgo alto (H-01: PB-51 sale «Superada» con dos cláusulas del plan sin cumplir o sin comprobar) y tres medios (H-02 a H-04). Por regla del operador, ninguno queda abierto ni va a la deuda, tampoco los bajos (H-05 a H-07). Vuelve a `ri-implementar`. En la ronda r02, esta QA vuelve a ejecutar `revisores/r01_01` a `r01_04` además de las pruebas del implementador.

---

# Ronda r02

- **Revisor:** claude (la misma sesión de QA que la r01, sin el contexto de la implementación) · **Ronda:** r02 · 18-11-2026
- **Base revisada:** `da24d06` («wip local: T-187 r02», sobre `86f0385`), en una copia nueva (`git worktree add <scratchpad>/qa187r2 da24d06`) con el `.venv` del proyecto enlazado. Ni el corpus, ni los otros bloques, ni `sistema_global/marco_comun_c/`, ni el paquete `bloque_a` cambian. No hay secretos, datos personales ni identificadores de modelo en lo añadido. Los lotes y la muestra no cambian.
- **Mis cambios en esta ronda:** `revisores/r01_03_ataques_contraste.py` carga el script de su ruta nueva (`.docs/scripts/`, por encargo del coordinador; los casos no cambian). `revisores/r02_01_ataques_r02.py` es nuevo. En la tabla de reproducción de la r01, las tres rutas viejas del ticket quedan como texto marcado «ruta de la r01», con la nueva al lado, sin borrar nada.

## Reproducción desde limpio

| Orden | Resultado |
| --- | --- |
| `.venv/bin/python -m pytest -q -p no:cacheprovider .docs/scripts/pruebas_revision_prompts_pb51.py` | 105 pasadas |
| `.venv/bin/python .docs/scripts/revision_prompts_pb51.py --comprobar` | «igual», 0 |
| `.venv/bin/python .docs/scripts/mutantes_revision_prompts_pb51.py` | 78 de 78 muertos |
| `.docs/scripts/pruebas_scripts.sh` | 336 pasadas (línea base 336) |
| `(cd bloque_a/11_Ejecutor && pytest -q tests/test_t187_pb51.py)` | 6 pasadas |
| `.venv/bin/python .docs/scripts/evidencias_plan_a.py` | 67 pruebas del plan y 302 citadas, todas existen; AUTOMATICA 39 y PARCIAL 20 |
| `python3 -I .docs/tickets/T-187/revisores/r01_01_recuento.py .docs/tickets/T-187` | 260/9/81; 96,65 % y 74,29 %, como en la r01 |
| `python3 -I .docs/tickets/T-187/revisores/r01_04_comprobaciones_cierre.py` | «las tres comprobaciones pasan» (en la r01 fallaban las tres) |
| `.venv/bin/python .docs/tickets/T-187/revisores/r01_03_ataques_contraste.py` | 10 de 10 fallan cerrado (en la r01, 3 de 10) |
| `.venv/bin/python .docs/tickets/T-187/revisores/r02_01_ataques_r02.py` | 14 de 16 como se espera (H-09) |

## Hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 | corregido | Mapa en `PARCIAL`. «No comprueba» empieza por el resultado esperado incumplido (9 ERRONEA, INC-T187-03) y sigue con los 21 papeles sin orientación. Evidencias con 39 Superada y 20 Superada en parte. `test_pb51_fila_del_mapa_superada_en_parte` y `r01_04` en verde. El README, INC-T187-02 y la deuda dicen «Superada en parte» |
| H-02 | corregido | Columna «Verificables» y la lista de los 28 prompts por debajo de 10 en el informe. Lo mismo en INC-T187-02 y en «No comprueba», sin muestra de reposición: declararlo es la corrección mínima que yo daba, y la reposición queda como opción del operador, escrita en INC-T187-02 |
| H-03 | corregido (con H-09 abierto) | Comprobé `comentario.json` contra las notas, uno a uno: las 9 `cita_nota` y las 5 citas de los dudosos son literales y sostienen el error o el matiz. El criterio de los dudosos está escrito, y el conjunto es exactamente el de las CORRECTA que lo cumplen: entra AF-MC-02-04 y sale AF-AG-21-07. Ya no se atribuyen «discutibles» a los revisores: `discutibles` está vacío, y la `sensibilidad` la firma quien escribe el comentario, con su motivo. INC-T187-02 e INC-T187-03, corregidas. Desviación aceptada: la cita de cada dudoso va en `dudosas_cita_nota` y no dentro de `dudosas`, con la misma comprobación |
| H-04 | corregido | Tabla veredicto × fuente en el informe, y la cifra en INC-T187-02 y en «No comprueba». Desviación aceptada: el script da 249 CORRECTA de memoria, 3 con búsqueda web y 8 con cálculo a mano, frente a mis 251 y 5. Mis cifras estaban mal: mi clasificación de la r01 tomaba «web» y «búsqueda» en cualquier lugar de la nota, y por eso contaba como búsqueda AF-AG-12-03 («casi duplicados web») y AF-MC-02-02 («búsqueda escalonada»), que son de memoria. Las cifras buenas son las del script |
| H-05 | corregido | `r01_03` 10 de 10, con el script en su ruta nueva |
| H-06 | corregido | `git mv` a `.docs/scripts/` (los nombres de las pruebas y los mutantes son los que yo propuse), fila en la tabla de `.docs/README.md`, línea base de 231 a 336 (`pruebas_scripts.sh`, 336 pasadas) y `test_t187_pb51.py` cargando de `.docs/scripts/`. Los datos se quedan en el ticket |
| H-07 | corregido | «## Paso 3 · Muestra», y el mutante M78 muere |

## Lo que pide el coordinador

- **(a) Las tres rutas viejas en `tools/refs_allowlist.txt`: no es aceptable.** La lista es, según su cabecera y `tools/refs_vivas.py` («Entregables FUTUROS citados en prompts de fases… se quitan de la lista al aterrizar»), para archivos que todavía no existen y se citan a propósito. Meter ahí rutas que ya no existen, con la marca «No se QUITAN», hace que el gate no vea nunca más esas tres rutas: cualquier documento nuevo que mande al script viejo pasaría sin aviso. La única excepción permanente que hay (`.docs/scripts/.logs`) es un directorio que sí existe al ejecutar. Lo correcto es actualizar las cuatro citas, marcando lo viejo sin borrarlo (regla 1 de `.docs/README.md`). Yo ya marqué las tres de mi `qa.md` (arriba). Queda la del diario, y quitar la allowlist → H-08.
- **(b)** Hecho: `r01_03` carga el script de `.docs/scripts/` y da 10 de 10.

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Prueba de regresión | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| H-08 | baja | `git diff 86f0385..da24d06 -- tools/refs_allowlist.txt` | Esperado: la allowlist solo con entregables futuros, y las citas de rutas movidas, actualizadas. Obtenido: tres rutas que ya no existen, en la lista para siempre | (1) Quitar de `tools/refs_allowlist.txt` las cinco líneas añadidas (los dos comentarios «T-187 r02…» y las tres rutas). (2) En `.docs/diario/2026-11.md`, en la entrada del 18-11 «T-187 en curso», cambiar el inicio de «**Resultado.**» por: «**Resultado.** revision_prompts_pb51.py, entonces en la carpeta del ticket (desde la r02, `.docs/scripts/revision_prompts_pb51.py`), (sin red, determinista) revisa…». Lo viejo queda como texto marcado, sin las comillas de código. (3) En `analisis-tecnico.md`, la viñeta «**Rutas viejas.**» de la r02: que diga que se marcaron en el diario y en la QA y que la allowlist no cambia | `.venv/bin/python tools/refs_vivas.py` en verde sin esas líneas en la allowlist, y `grep -c "T-187" tools/refs_allowlist.txt` = 0 | abierto |
| H-09 | baja | `.venv/bin/python .docs/tickets/T-187/revisores/r02_01_ataques_r02.py`: los casos `cita_de_una_letra` y `cita_de_una_palabra_vacia` salen con 0 | Esperado (H-03 de la r01: «un fragmento literal de la nota que la sostiene»): una cita que no sostiene nada no pasa. Obtenido: `cita_nota` = «a» o « de », subcadenas de cualquier nota, pasan. Además la cita no sale en el informe, así que `--comprobar` no ve que cambie (por eso esos casos dan 0 y no 1) | (1) En `revision_prompts_pb51.py`, `MIN_PALABRAS_CITA = 3`, declarado como `[PROPUESTO]` junto a `MAX_PALABRAS_NOTA` y en el análisis («la cita más corta de hoy tiene 4 palabras»). En `contraste()`, la cita, además de ser literal, debe tener al menos `MIN_PALABRAS_CITA` palabras con letra o cifra; si no, `ContrasteInvalido`. (2) En `informe_contraste`, columna «Cita de la nota» en las tablas de ERRONEA y de dudosos. Regenerar el informe | En `pruebas_revision_prompts_pb51.py`, `test_contraste_falla_cerrado_con_una_cita_de_menos_de_tres_palabras` (con 2 palabras da 2 y con 3 vale) y un mutante que quite la comprobación. `r02_01` 16 de 16 | abierto |

## Gates

`./tools/check_all.sh` completo, de una vez, desde la copia limpia de `da24d06`: **12/12 en verde**. Corpus íntegro, NFC, YAML, secretos, refs-vivas, ruff 2807 y mypy 102/174/159, iguales a sus cuotas; pytest A 8273 (≥ 607), A-Forex 68 y B 176. En el worktree `t187`, con mi `qa.md` de la r02 y las rutas viejas marcadas, `tools/refs_vivas.py`, `tools/secrets_scan.py` y `tools/nfc_check.py` también pasan. `ruff check` de `revisores/` sin hallazgos.

## Veredicto (r02)

**APTO, pendiente de una ronda de cierre.** Los siete hallazgos de la r01 están corregidos y comprobados con mis propios scripts. Quedan dos bajos nuevos, H-08 y H-09, que por regla del operador no pueden quedar abiertos ni ir a la deuda. No cierro el ticket: el README y la deuda no cambian. En la ronda de cierre vuelvo a ejecutar `r01_01` a `r01_04` y `r02_01` (16 de 16), además de `tools/refs_vivas.py`, sin las rutas viejas en la allowlist, y el gate.

---

# Ronda de cierre de la QA r02 (H-08 y H-09)

- **Revisor:** claude (la misma sesión de QA) · 18-11-2026 · **Base revisada:** `1483871` («wip local: T-187 cierre r02», sobre `da24d06`), en una copia nueva (`git worktree add <scratchpad>/qa187r3 1483871`) con el `.venv` del proyecto enlazado. Mis scripts de las rondas anteriores llegan al commit sin cambios.

## Verificación

| Orden | Resultado |
| --- | --- |
| `python3 -I .docs/tickets/T-187/revisores/r01_01_recuento.py .docs/tickets/T-187` | 260/9/81; 96,65 % y 74,29 % |
| `python3 -I .docs/tickets/T-187/revisores/r01_04_comprobaciones_cierre.py` | las tres comprobaciones pasan |
| `.venv/bin/python .docs/tickets/T-187/revisores/r01_03_ataques_contraste.py` | 10 de 10 fallan cerrado |
| `.venv/bin/python .docs/tickets/T-187/revisores/r02_01_ataques_r02.py` | 16 de 16 (en la r02, 14 de 16) |
| `.venv/bin/python .docs/tickets/T-187/revisores/r03_01_ataques_cierre.py` (nuevo) | 9 de 9 |
| `.venv/bin/python -m pytest -q -p no:cacheprovider .docs/scripts/pruebas_revision_prompts_pb51.py` | 106 pasadas |
| `.venv/bin/python .docs/scripts/mutantes_revision_prompts_pb51.py` | 81 de 81 muertos (M79 a M81 nuevos) |
| `.docs/scripts/pruebas_scripts.sh` | 337 pasadas (línea base 337) |
| `.venv/bin/python .docs/scripts/revision_prompts_pb51.py --comprobar` | «igual», 0 |
| `.venv/bin/python .docs/scripts/evidencias_plan_a.py` | 302 citadas y todas existen; AUTOMATICA 39 y PARCIAL 20 |
| `.venv/bin/python tools/refs_vivas.py` y `grep -c T-187 tools/refs_allowlist.txt` | en verde, y 0 |
| `./tools/check_all.sh` completo | **12/12**: ruff 2807 y mypy 102/174/159, iguales a sus cuotas; pytest A 8273, A-Forex 68 y B 176 |

## Ataques a las dos correcciones (`r03_01_ataques_cierre.py`)

- **H-09.** Una cita de 2 palabras (en una errata o en un dudoso), tres signos y una palabra, o una cita de 3 palabras que no es literal: los cuatro casos salen con 2. Una cita literal de 3 palabras, distinta de la guardada, pasa la validación, y `--comprobar` da 1 porque la cita ya sale en el informe (columna «Cita de la nota» en ERRONEA y en dudosos). La cita original da 0. El límite que queda está declarado: la cita prueba que el texto está en la nota, no que la paráfrasis sea fiel. Por eso el informe pone cita y nota juntas para quien lo lea. `MIN_PALABRAS_CITA = 3` es un parámetro del script, `[PROPUESTO]` y declarado en el script y en el análisis, como `MAX_PALABRAS_NOTA`. No es un número de configuración del ejecutor.
- **H-08.** La allowlist ya no tiene ninguna línea de T-187 y `refs_vivas` pasa. La cita del diario queda marcada sin borrar nada («revision_prompts_pb51.py, entonces en la carpeta del ticket (desde la r02, `.docs/scripts/revision_prompts_pb51.py`)»), y la viñeta «Rutas viejas» del análisis lo cuenta.

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-08 | corregido | `r03_01` (allowlist sin T-187, `refs_vivas` 0) |
| H-09 | corregido | `r02_01` 16 de 16 y `r03_01` 7 de 7 casos de cita; M80 y M81 mueren |

Ningún hallazgo nuevo. No queda nada abierto de la r01 (H-01 a H-07) ni de la r02 (H-08 y H-09), y nada va a la deuda.

## Veredicto final

**APTO.** T-187 queda CERRADO, y PB-51 «Superada en parte» por las 9 erratas, pendientes de la próxima entrega del corpus (INC-T187-03), y los 21 papeles sin orientación de tamaño (T-57). Sin commit ni push, por encargo del coordinador.
