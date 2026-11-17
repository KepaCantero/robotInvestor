# T-166 · QA independiente

- **Revisor:** claude (subagente nuevo, sin contexto de la implementación; solo el plan, el código y el corpus) · **Ronda:** r01 · 2026-11-17
- **Base:** `wip/t166` = `1d457ce` (sobre develop `a9210c0`), en un worktree propio.

## Reproducción desde limpio

Worktree nuevo (`git worktree add --detach … wip/t166`), venv del proyecto. Por regla de la tarea, sin la suite completa ni el gate.

| Comando | Resultado |
| --- | --- |
| `pytest -q tests/test_t166_entrega_corpus.py tests/test_fase3_goldens.py` | 247 passed (55 de T-166 + 192) |
| `python tests/goldens_ct.py` | «goldens de contratos: coinciden», rc 0 |
| `python tools/corpus_integridad.py` | 705 archivos coinciden, rc 0 |
| `python tools/refs_vivas.py` · `tools/nfc_check.py` | en verde |
| `python -m bloque_a.herramientas.verificador_ids --json <copia> --auditoria <copia del .md>` | 0 errores, 1 aviso (RF-1); la salida es **idéntica byte a byte** a `docs/auditoria_ids_bloque_a.json` y `.md` |
| `.docs/scripts/borrador_anexo_b.py --comprobar` | rc 0 |
| `revisores/r01_01_final_contra_anexo_b.py` (pytest, ejecutor mock) | 14 passed (incluye las tres pruebas `hallazgo_*`, que fijan lo que el Anexo B dice mal) |
| `revisores/r01_02_mutantes_prosa.py` | 6 de 10 mutantes de prosa propios **viven** (H-04) |
| `revisores/r01_03_mutantes_codigo.py --resto` | M1, M2, M5 muertos por T-166; M3 y M6 viven en T-166 y los matan T-162/T-169; **M4 vive en todas** (H-05) |
| `revisores/r01_04_prompts_y_huellas.py` | 28 agentes: ninguno carga del histórico; AG-20 trae RF-0046, sin RF-0123; su huella cambia frente al texto de la V5.2 y es estable |
| `revisores/r01_05_manifiesto.py` | base 696 → 705; quitadas 9, puestas 18, cambiadas 9; todo dentro del alcance; el histórico tiene los hashes de la base; los hashes del manifiesto son los del disco |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_ca1_*`; mi grep de `Cat[aá]logo… V4[.,]0` y de `catalog_version "4…` sobre `bloque_a/` vivo (sin `11_Ejecutor` ni `99_Historico*`): nada. Los únicos «4.0» restantes son tickets cerrados, la memoria, INC-T157-02/03 (historia) y el patrón del verificador |
| CA-2 | sí | Verificador: 0 errores, solo el aviso RF-1; FC-EVAL-001 v1.0 VIGENTE, MC-10, IMPLEMENTADO, H1–H4 (encaja con un cálculo de tasa base del MC-10 en H3); RF-0046 existe en F9, «Estado: Aprobada», TF-05, fuera del Registro de bajas; encaja con `fiabilidad_fuentes` (fuente de opinión con previsiones), y el ejemplo es coherente (10 + 10·0,06 → 11 puntos) |
| CA-3 | sí | `diff` V5.2 (histórico) → V5.3: solo cabecera (4 líneas), «Cómo se lee este anexo (V5.2 y V5.3)», el párrafo «Respuesta final (V5.3)» tras CT-03 y una fila del Anexo F. SHA-256 de la V5.2 del histórico = `d8f9e3d0…` de la base |
| CA-4 | sí | `git diff -U0` de los 8 `.md`: solo las 6 líneas «Catálogo V4.0→V5.0» de los MC (1 en prosa en MC-01 y 5 en JSON), MOTOR-F05, la línea de `operacion` del Registro de cálculos y la de `fiabilidad_fuentes` del Evaluador; `.md` y `.docx` anteriores en el histórico con los hashes de la base (`r01_05`) |
| CA-5 | **no del todo** | Campos, los cinco resultados, el estado común, el estado en F5, los prefijos, las reglas de referencias y la confianza **coinciden con el código** (medido con el ejecutor en `r01_01`). Pero tres frases del mismo párrafo no describen lo que hace el código (H-01 a H-03) y la prueba no ve 6 mutantes de prosa ni uno de código (H-04, H-05) |
| CA-6 | sí | `test_ca6_*`; `goldens_ct.py` coincide; `REGISTRO.md` con la línea del re-congelado; solo cambian dos huellas en `huellas.json` |
| CA-7 | sí | `test_ca7_*` y `r01_04` |
| CA-8 | sí | `r01_05`: ni otros bloques, ni `marco_comun_c`, ni la Constitución; `corpus_integridad.py` y `refs_vivas.py` en verde |
| CA-9 | no reproducido | Por regla de la tarea no se pasó la suite completa ni el gate. `ruff check` de `test_t166_entrega_corpus.py`: limpio (los 20 ISC004 de `.docs/scripts/borrador_anexo_b.py` ya estaban en la base y quedan fuera del gate) |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_01::test_hallazgo_errores_que_no_son_de_integridad_ni_del_almacen_tambien_paran` (FugaDeInformacion, ReplayFaltante, CanalNoPrevisto); `respuesta_final.ERRORES_DE_CONTROL` y `para_la_consulta` | El Anexo B dice «Un fallo de integridad o de control del almacén durante el análisis para la consulta: no hay provisional ni final», y de lo demás, FALLIDO. El código para también con los controles de la **mensajería** (`CanalNoPrevisto`, `DatosSensibles`, `MensajeInvalido`), con una **fuga de información** de HT-01 y con un **`ReplayFaltante`**: sin QRY en F5 y sin ningún CT-03, no con una final FALLIDO. Lo mismo en «si no se puede enviar, se aparta una vez…»: una pendiente con fallo de integridad o de control no se aparta, para la consulta o el ciclo (`enviar_pendientes`) | Sustituir la última frase del párrafo por: «Un fallo de integridad del almacén o un error de control durante el análisis (los controles del almacén y de la mensajería, un mensaje que no cumple su contrato, una fuga de información de HT-01 o una respuesta sin grabar en el modo de reproducción: `respuesta_final.ERRORES_DE_CONTROL`) para la consulta: no hay provisional ni final; cualquier otro error da la final FALLIDO.» Y en la frase de las pendientes: «…si no se puede enviar, se aparta una vez con una incidencia escalada al operador, salvo un fallo de integridad o un error de control, que para la consulta o el ciclo.» Actualizar las dos `FRASES_FIJAS_FINAL` y añadir un mutante de código que quite `FugaDeInformacion` de `ERRORES_DE_CONTROL` comparado con la frase | abierto |
| H-02 | media | `r01_01::test_hallazgo_sobre_sin_run_id_no_es_nulo_es_ausente`; `contratos.Mensajeria.crear` (`if run_id: msg["run_id"] = run_id`) | El Anexo B: «En el sobre, … `run_id` el del RUN- solo si consta en F5 y lo lanzó esta consulta (si no, nulo)». En el sobre del CT-03 la clave **no está**; nulo solo en la copia que queda en F5 (`respuesta_final.run_id`) y en lo que devuelve `consulta` | «…`run_id` el del RUN- solo si consta en F5 y lo lanzó esta consulta (si no, el sobre no lleva `run_id`, y la copia de la final en F5 lo deja nulo).» Actualizar la `FRASE_FIJA` y el mutante de prosa correspondiente | abierto |
| H-03 | media | `r01_01::test_hallazgo_un_rechazo_r8_de_la_final_escribe_en_ha` | El Anexo B: «La final se valida con su esquema … y por la mensajería **antes de escribir nada**». Un rechazo R8 (o de canal) de la mensajería escribe su incidencia en HA (SEGURIDAD o CANAL_NO_PREVISTO), y `nuevo_id` ya avanzó el contador MSG-. Lo que no se escribe es la final en F5 | «…y por la mensajería antes de escribir la final en F5 (un rechazo de la mensajería deja su incidencia en HA, como con cualquier mensaje), sale una sola vez…». Actualizar la `FRASE_FIJA` | abierto |
| H-04 | baja | `r01_02_mutantes_prosa.py` | Viven 6 mutantes que cambian el sentido: «la más **alta** de las suyas en F3», «registrado en **F3**», «`escalado` (**distinto** del de la provisional)», «ruta **N0**», «(**solo si entrega**)» y «`provisional_msg_id` (el **`query_id` de la consulta**…)». CA-5 promete que un cambio de prosa se nota | Añadir a `FRASES_FIJAS_FINAL`, literalmente: (a) la primera frase entera, `"Respuesta final (V5.3). Cuando termina el análisis escalado de una consulta de ruta ANALITICA (o falla, no entrega o no se lanzó), el Coordinador envía otro CT-03 RETORNO al Broker, la respuesta final; la provisional no cambia."` (en lugar de la actual que empieza por «el Coordinador»); (b) `` "`escalado` (el mismo que la provisional)" ``; (c) `` "`provisional_msg_id` (el `msg_id` de la provisional, MSG-, que queda registrado en F5)" ``; (d) `"La confianza es, con opciones, la más baja de las suyas en F3 ("`. Pasar los 6 mutantes de `r01_02` a `MUTANTES_PROSA`; `r01_02` debe dar «vivos: 0» | abierto |
| H-05 | baja | `r01_03_mutantes_codigo.py --resto`, M4 | La regla «sin opciones o sin resultado, la más baja entre la de la provisional y especulativo» no la ejercita ninguna prueba: quitar el tope `"especulativo"` en `construir` no lo nota ni T-166, ni T-162, ni T-169 (con el mock la provisional ya es «especulativo») | Copiar a `test_t166_entrega_corpus.py` (CA-5) la prueba `test_sin_resultado_la_confianza_es_la_mas_baja_entre_la_provisional_y_especulativo` de `r01_01` (parametrizada: establecido→especulativo, probable→especulativo, especulativo→especulativo, en disputa→en disputa; necesita `nuevo_bloque` de `conftest`) | abierto |
| H-06 | baja | `grep -n "V5.2" bloque_a/11_Ejecutor/tests/goldens/README.md`; `sed -n 367p docs/auditoria_ids_bloque_a.md` | Dos frases vivas quedan desfasadas. `goldens/README.md`, l. 14: `anexo_b_esquemas.json` «derivado solo del Anexo B del Documento 0 V5.2 (hasta T-143, de la V5.1)», pero los 38 esquemas llevan ya la marca V5.3. `docs/auditoria_ids_bloque_a.md` (fuera de las marcas del informe): «La Fase 0 no aplica ninguna; D-1 la aplicó después T-160.», cuando D-2 a D-4 ya están aplicadas | `goldens/README.md`, l. 14: «…derivado solo del Anexo B del Documento 0 V5.3 (hasta T-166, de la V5.2; hasta T-143, de la V5.1)». `docs/auditoria_ids_bloque_a.md`: «La Fase 0 no aplica ninguna; D-1 la aplicó después T-160, y D-2 a D-4, T-166.» | abierto |

Las correcciones de H-01 a H-03 cambian el Documento 0 V5.3 todavía no publicado en develop. Hay que repetir el re-congelado del manifiesto y de `huellas.json` (con su línea en `REGISTRO.md`) y regenerar la auditoría de IDs si su informe cita la huella.

## Comprobado sin hallazgo

- **Respuesta final contra el código, con el ejecutor** (`r01_01`, flujo PB-07 real con mock y casos de fallo). El cuerpo lleva exactamente los 8 campos, y `respuesta_final` no va en la provisional. El `escalado` es idéntico al de la provisional. Emisor y receptor son AG-01 y BROKER (AG-01 es el Coordinador). Estado común y estado en F5 según `RESULTADOS` y `ESTADO_F5`. `provisional_msg_id` es el `msg_id` de la provisional y queda en F5. Las referencias empiezan por el RUN-, siguen el orden del top-3 (OPP, TND, CLM, PRG de su RUN-), no se repiten y solo usan los cinco prefijos. NO_EJECUTADO va sin referencias, y FALLIDO lleva como mucho el RUN-. FALLIDO da FINAL_SIN_RESULTADO. Sin resultado, el texto dice «no se confirma ni se amplía». La final sale una sola vez (`repetido`). Una final pendiente se construye con la fecha de su consulta. La confianza con opciones es la más baja de las citadas (en el nominal, «probable»).
- **El orden de `_resultado`** (FALLIDO antes que NO_EJECUTADO) y **la regla de «lo lanzó esta consulta»**: el Anexo B los dice bien. La prueba de T-166 no los ve (M3 y M6), pero sí T-162 y T-169.
- **V5.3 = V5.2 + lo declarado**, y los 8 ficheros cambian solo en lo declarado (CA-3 y CA-4).
- **Manifiesto** (`r01_05`): el histórico tiene los hashes de la base, y no se toca nada fuera del Bloque A ni de las rutas de la entrega.
- **Rutas en documentos cerrados.** En T-143 (README y análisis técnico) y en la ronda T-143 de INC-T114-01, la ruta pasa al histórico con la nota «(en `01_Gobernanza` hasta T-166…)», así que conservan la historia y la ruta existe. El paréntesis anidado de INC-T114-01 queda feo, pero es correcto. Los scripts `revisores/r01_02` y `r01_03` de T-143 siguen apuntando a la ruta antigua: se dejan así con razón, porque son evidencia de una QA cerrada (no son referencias vivas y `refs_vivas.py` no los mira).
- **Las dos frases propuestas para `CLAUDE.md`** son correctas: el manifiesto tiene 705 líneas y la trampa de «Catálogo V4.0» ya no es cierta. Al aplicar la segunda hay que sustituir también el «(81 fichas)» que sigue a «el catálogo entregado es V5.0», porque la frase nueva ya lo lleva. Si no, sale dos veces. `AGENTS.md` no cita ni 696 ni «Catálogo V4.0».
- **Invariantes.** No se cambia código de producción: solo dos docstrings y un comentario de `por_defecto.yaml`. No hay números nuevos ni LLM en la ruta de la final. Las decisiones `[PROPUESTO]` están en INC-T166-01 y en el registro de decisiones (D-2 a D-4 aplicadas). No hay secretos: el correo de `r01_01` es ficticio, en el dominio `ejemplo.com`, como en las pruebas de T-169.

No comprobado: la suite completa de A, las cuotas de ruff y mypy y el gate 12/12 (no lo pedía la tarea), y la calidad de los `.docx` que faltan (INC-T166-01).

## Veredicto

**NO APTO.** El párrafo nuevo del Anexo B, que es la razón de esta entrega, tiene tres frases que no describen lo que hace el código. H-01 dice qué errores paran la consulta. H-02 dice que el `run_id` del sobre es nulo cuando en realidad falta. H-03 dice «antes de escribir nada». Son hallazgos medios y CA-5 no se cumple del todo. Corregirlos ahora cuesta una edición de texto y un re-congelado. Dejarlos en la deuda obligaría a otra entrega del corpus congelado. H-04 a H-06 son bajos y se subsanan en el mismo ticket con la corrección exacta indicada. En la r02, el revisor vuelve a ejecutar `r01_01` a `r01_05`. Las pruebas `hallazgo_*` de `r01_01` fijan el comportamiento del código y siguen valiendo; la r02 comprueba que el texto corregido dice eso mismo. `r01_02` tiene que dar 0 vivos.

## Ronda r02

- **Revisor:** claude (el mismo de la r01) · 2026-11-17 · **Base:** `wip/t166` = `3c162a8`, en un worktree nuevo. `qa.md` y `revisores/r01_*` del commit son idénticos a los de mi r01 (`git diff 3498eba 3c162a8` vacío en esas rutas).

### Reproducción

| Comando | Resultado |
| --- | --- |
| `pytest revisores/r01_01_final_contra_anexo_b.py tests/test_t166_entrega_corpus.py` | 87 passed (14 + 73) |
| `revisores/r01_02_mutantes_prosa.py` | vivos: 0 |
| `revisores/r01_03_mutantes_codigo.py --resto` | M1, M2, **M4** y M5 muertos por T-166; M3 y M6 los matan T-162/T-169; el código queda restaurado |
| `revisores/r01_04_prompts_y_huellas.py` · `r01_05_manifiesto.py` | rc 0 · rc 0 (696 → 705, todo en alcance, histórico con los hashes de la base) |
| `git diff 1d457ce 3c162a8 -- bloque_a/99_Historico_V5.2` · `-- tools/corpus_manifest.txt` | vacío · una sola línea (la V5.3) |
| `goldens_ct.py` · `corpus_integridad.py` · `refs_vivas.py` · `nfc_check.py` · `borrador_anexo_b.py --comprobar` | coinciden · 705 · verde · verde · 0 |
| Verificador `--json`/`--auditoria` sobre copias | 0 errores, 1 aviso (RF-1); idéntico byte a byte a `docs/auditoria_ids_bloque_a.*` |
| `revisores/r02_01_pendientes_y_errores_de_control.py` (nuevo) | 6 passed (fija el comportamiento de H-07) |

### Los hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 | corregido en el análisis; **la frase de las pendientes, no** (H-07) | La última frase enumera exactamente `ERRORES_DE_CONTROL` (`PermissionError` = controles del almacén y de la mensajería; `MensajeInvalido`; `FugaDeInformacion`; `ReplayFaltante`) y «cualquier otro error da la final FALLIDO»: `r01_01` (KeyError → FALLIDO; Fuga, Replay, Canal → sin provisional ni final) y `test_ca5_los_errores_de_control_…`; mutantes de código y de prosa nuevos, muertos |
| H-02 | corregido | `r01_01::test_hallazgo_sobre_sin_run_id…` (el sobre no lleva `run_id`) y `test_no_ejecutado…` (la copia lo deja nulo) |
| H-03 | corregido | `r01_01::test_hallazgo_un_rechazo_r8…`: la incidencia SEGURIDAD queda en HA y la final no se escribe en F5. Matiz sin hallazgo: un `MensajeInvalido` de la mensajería no escribe incidencia (`r02_01::test_mensaje_invalido_no_deja_incidencia…`), pero para la final no se alcanza, porque su cuerpo pasa antes `ESQUEMA` y no admite campos reservados |
| H-04 | corregido | `r01_02`: 0 vivos; las cuatro frases fijas y los seis mutantes están en la suite |
| H-05 | corregido | prueba ×4 en CA-5; M4 muere |
| H-06 | corregido | `goldens/README.md` l. 14 y `docs/auditoria_ids_bloque_a.md` con el texto propuesto |

Frases nuevas contrastadas con el código y sin hallazgo: la del sobre (H-02), la de la validación (H-03) y la última (H-01). También se comprobó que el resto del párrafo y del Documento 0 no cambia (diff palabra a palabra: solo esas cuatro frases).

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-07 | media | `revisores/r02_01_pendientes_y_errores_de_control.py`; `respuesta_final.enviar_pendientes` (`except (RespuestaFinalInvalida, *RECHAZOS_SIN_EFECTO)`) | La frase corregida de las pendientes dice «se aparta una vez con una incidencia escalada al operador, **salvo un fallo de integridad o un error de control, que para la consulta o el ciclo**». Pero dos de los errores de control que la frase siguiente enumera, `DatosSensibles` (R8) y `MensajeInvalido` (`RECHAZOS_SIN_EFECTO`), **no paran** con el almacén íntegro: la pendiente se aparta (`final_no_enviable`, incidencia con `escalado_operador`) y la consulta sigue. Solo paran los demás (`CanalNoPrevisto`, `FugaDeInformacion`… lo mide `r02_01`). El texto salió de mi corrección de H-01 en la r01: el error es del revisor y se subsana aquí | En el Documento 0 V5.3, sustituir «si no se puede enviar, se aparta una vez con una incidencia escalada al operador, salvo un fallo de integridad o un error de control, que para la consulta o el ciclo.» por «si no se puede enviar, se aparta una vez con una incidencia escalada al operador, también si la rechazan su esquema o la mensajería (R8 o un mensaje que no cumple su contrato), salvo un fallo de integridad o cualquier otro error de control, que para la consulta o el ciclo.» En `test_t166_entrega_corpus.py`: (1) la misma sustitución en `FRASES_FIJAS_FINAL`, y en `MUTANTES_PROSA` el viejo del mutante de esa frase pasa a `", salvo un fallo de integridad o cualquier otro error de control, que para la consulta o el ciclo."`; (2) en `_codigo`, `"rechazos": [e.__name__ for e in respuesta_final.RECHAZOS_SIN_EFECTO]`; en `_final_que_difiere`, `if set(c["rechazos"]) != {"DatosSensibles", "MensajeInvalido"} or "(R8 o un mensaje que no cumple su contrato)" not in p: difieren.append(...)`; (3) un mutante de código `"un rechazo más se aparta": lambda c: c["rechazos"].append("CanalNoPrevisto")` y uno de prosa `("también si la rechazan su esquema o la mensajería (R8 o un mensaje que no cumple su contrato), ", "")`; (4) copiar `test_hallazgo_rechazos_de_la_mensajeria_…` de `r02_01` a CA-5 (dos casos). Re-congelar el manifiesto y `huellas.json` (línea en `REGISTRO.md`) y regenerar la auditoría de IDs, que cita la huella | abierto |

### Veredicto r02

**NO APTO.** H-02 a H-06 están corregidos y verificados con el ejecutor. H-01 está corregido en la frase del análisis, pero la frase nueva de las pendientes afirma algo falso (H-07, media): los rechazos R8 y de campos de una final pendiente se apartan, no paran. Es la misma regla de la r01 (una afirmación falsa del Documento 0 cuenta como media) y la corrección es una frase más un re-congelado. En la r03 el revisor vuelve a pasar `r01_01` a `r01_05` y `r02_01`, y `r01_02` tiene que seguir en 0 vivos.

## Ronda r03

- **Revisor:** claude (el mismo de la r01 y la r02) · 2026-11-17 · **Base:** `wip/t166` = `afa6db0`, en un worktree nuevo. `qa.md` y `revisores/` del commit son los de mi r02.

### Reproducción

| Comando | Resultado |
| --- | --- |
| `pytest revisores/r03_01_… revisores/r02_01_… revisores/r01_01_… tests/test_t166_entrega_corpus.py` | 99 passed (2 + 6 + 14 + 77) |
| `revisores/r01_02_mutantes_prosa.py` | vivos: 0 |
| `revisores/r01_03_mutantes_codigo.py --resto` | M1, M2, M4 y M5 los mata T-166; M3 y M6, T-162/T-169; código restaurado |
| `revisores/r01_04_…` · `r01_05_…` | rc 0 · rc 0 (705, todo en alcance, histórico con los hashes de la base) |
| `git diff 3c162a8 afa6db0 -- bloque_a/99_Historico_V5.2` · `-- tools/corpus_manifest.txt` | vacío · una línea (la V5.3) |
| `goldens_ct.py` · `corpus_integridad.py` · `refs_vivas.py` · `nfc_check.py` · `borrador_anexo_b.py --comprobar` | coinciden · 705 · verde · verde · 0 |
| Verificador `--json`/`--auditoria` sobre copias | 0 errores, 1 aviso (RF-1); idéntico byte a byte a `docs/auditoria_ids_bloque_a.*` |
| `ruff check` del ejecutor desde la raíz (como el gate) | 2813 = cuota; `test_t166_entrega_corpus.py` limpio. Desde `bloque_a/11_Ejecutor` sale un I001 en ese archivo: lo da el directorio de trabajo (otra detección de módulos propios), no el gate. Sin hallazgo |

### H-07

**Corregido.** La V5.3 solo cambia en la frase de las pendientes (diff palabra a palabra: el inciso «también si la rechazan su esquema o la mensajería (R8 o un mensaje que no cumple su contrato),» y «un» → «cualquier otro»). Contrastada con el ejecutor:

- R8 (`DatosSensibles`) y `MensajeInvalido` se apartan y la consulta sigue (`r02_01` y la copia en CA-5).
- Un rechazo del esquema (`RespuestaFinalInvalida`) se aparta (`r03_01`, nuevo).
- Con el almacén no íntegro, un rechazo R8 para y no se aparta: «salvo un fallo de integridad» (`r03_01`, nuevo).
- `CanalNoPrevisto` y `FugaDeInformacion` paran (`r02_01`), y otro error (KeyError) se aparta.

El mutante de código «un rechazo más se aparta» y el de prosa que quita el inciso están en la suite y mueren.

Se releyó el párrafo frase a frase contra `respuesta_final.py` y `orquestacion.consulta`. Ninguna afirmación nueva es falsa. Las frases que ya se habían contrastado en la r01 y la r02 no han cambiado.

### Hallazgos

| ID | Gravedad | Estado |
| --- | --- | --- |
| H-01 a H-06 | — | corregidos (r02) |
| H-07 | media | corregido (r03) |

No hay hallazgos abiertos.

### Veredicto r03

**APTO.** Se cumplen los criterios de aceptación CA-1 a CA-8. CA-9 se reproduce en lo que cubre esta QA, que es ruff desde la raíz; la suite completa de A la pasó el implementador y esta QA no la repitió, por regla de la tarea. No queda ningún hallazgo abierto. Cierre en esta copia: el Estado del README pasa a «CERRADO (17-11-2026, QA r03 APTO)» y la fila T-166 de la deuda técnica, a cerrada. Quedan para la sesión coordinadora el diario, la memoria, las dos frases de `CLAUDE.md` (r01: 696 → 705 y la trampa del «Catálogo V4.0», que debe sustituir también el «(81 fichas)» que la sigue), y el commit en develop y el push.
