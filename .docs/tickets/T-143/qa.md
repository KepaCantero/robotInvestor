# T-143 · QA independiente

- **Revisor:** Claude, subagente revisor nuevo sin el contexto de la implementación (no implementó T-143) · **Ronda:** r01 · 15-11-2026
- **Copia revisada:** worktree limpio en `3e63e2a` («wip local: T-143», sobre `1ccffd5`), con el `.venv` del proyecto enlazado. Sin red ni gasto: cliente simulado y Motor local.

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6580 pasadas, 2 omitidas (26 min); ≥ 607 |
| `tests/test_fase3_goldens.py` | 125 pasadas |
| `tests/goldens_ct.py` | «coinciden», código 0 |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | en verde; corpus íntegro con 696 archivos |
| `.docs/scripts/pruebas_scripts.sh` | 203 pasadas (línea base respetada) |
| `.docs/scripts/prueba_refs_vivas.py` | 25/25 |
| `.docs/scripts/borrador_anexo_b.py --comprobar` | 0 |
| ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2831 (cuota 2831) |
| mypy de A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 (cuota 109) |
| `./tools/check_all.sh --core` | 8/8 gates en verde (corpus 696, NFC, YAML, secretos, refs vivas, pytest A 6580, A-Forex 68, B 176) |
| `git diff --diff-filter=D 1ccffd5 HEAD -- .docs` | vacío: no se borró nada |

### Scripts del revisor (orden de ejecución, desde la raíz, con el Python del `.venv`)

1. `.venv/bin/python .docs/tickets/T-143/revisores/r01_02_bateria_y_corpus.py 1ccffd5` → 0 fallos. Batería: los mismos 370 casos en el mismo orden; los 86 cuyo ejemplo cambió llevan dentro el ejemplo de `1ccffd5` con su contrato y tipo de mensaje y nada más cambia (salvo `que` de los tres «sueltos»); los 284 restantes, intactos y con un ejemplo que no cambió; `aceptaciones_rechazos.json` idéntico byte a byte. Manifiesto: 695 → 696, quitadas las dos rutas V5.1 de `01_Gobernanza`, puestas la V5.2 y las dos del histórico con el mismo hash, cambiado solo el README índice; los 696 hashes coinciden con el disco. Documento 0 fuera del Anexo B: 4 líneas quitadas y 5 puestas (cabecera y fila del Anexo F); en el Anexo B, los mismos títulos, bloques de código cerrados (los 9 bloques JSON se parsean), y los esquemas `informe_seguimiento_opcion` y `paquete_oportunidades` sin cambios.
2. `.venv/bin/python .docs/tickets/T-143/revisores/r01_01_anexo_b_contra_codigo.py` → 8 hallazgos (H-01 a H-04). Contrasta afirmaciones del Anexo B V5.2 con el ejecutor de verdad (Bloque con `MockClient`, Motor local), fuera de los goldens.
3. `.venv/bin/python .docs/tickets/T-143/revisores/r01_03_mutantes.py <carpeta fuera del repositorio> [IDs]` → 20 mutantes (10 en el código, 10 en el Anexo B V5.2). Cada uno se aplica a una copia, se re-congela con `goldens_ct.py --update --motivo` (el caso peor: quien re-congela sin mirar) y se pasa `test_fase3_goldens.py`. Los 12 que las pruebas de T-143 dicen cubrir mueren todos; sobreviven 8 que nadie dice cubrir (H-05). Sin re-congelar, todos fallan ya por las huellas o la comparación byte a byte.

Los mutantes del implementador están dentro de `test_fase3_goldens.py` (parametrizados en `test_t143_*`, `test_ca4_*` y `test_ca7_*`); pasan con la suite. No hay script aparte.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r01_02` (4 quitadas, 5 puestas fuera del Anexo B) y `test_t143_la_v52_es_la_v51_con_el_anexo_b_corregido` |
| CA-2 | sí | `r01_02` y `sha256sum`: `26691b68…` (.docx) y `7e708a03…` (.md) en `99_Historico_V5.1/01_Gobernanza/`; un solo Documento 0 en `01_Gobernanza` |
| CA-3 | sí | `divergencias_anexo_b.json` solo con CT-18, CT-20 y CT-21 sin campos; `test_t143_las_divergencias_que_quedan` |
| CA-4 | sí | las pruebas que fijaban divergencias fijan la coincidencia; mutantes C01, C03–C06, C08, C09, D01, D02, D07 y D08 mueren tras re-congelar (`r01_03`). Con huecos: H-05 |
| CA-5 | sí | `aceptaciones_rechazos.json` idéntico a `1ccffd5`; `goldens_ct.py` → 0; dos líneas T-143 en `REGISTRO.md` |
| CA-6 | **no** | `refs_vivas.py` en verde, pero `bloque_a/11_Ejecutor/config/por_defecto.yaml` (línea 2) sigue diciendo «subordinado al Documento 0 óptima V5.1», la misma frase que se corrigió en `11_Ejecutor/README.md` y en `tests/MAPA_PLAN_DE_PRUEBAS.md` (H-06) |
| CA-7 | sí | `r01_02`: el diff del manifiesto toca exactamente las seis rutas declaradas; el motivo propuesto para el commit (análisis, «Corpus») describe bien el cambio |
| CA-8 | sí | el borrador dice «aplicado en el Documento 0 V5.2», conserva el borrador aplicado (solo baja los títulos y cita el estado anterior); `--comprobar` → 0 |
| CA-9 | sí | INC-T114-01 con la ronda T-143, INC-T143-01 (sin `.docx`), la decisión del operador «Aplicada en la V5.2», fila nueva en `.docs/README.md`, README índice con su fila de registro y la de `99_Historico_V5.1` |
| CA-10 | sí | suite de A 6580 pasadas; ruff 2831; mypy A 109; gates ligeros en verde |

Movimiento de la V5.1 y lo que no se tocó: con razón. Los system prompts y demás corpus congelado citan «Documento 0 óptima V5.1» como dato congelado (regla 1 de CLAUDE.md); los tickets cerrados y la memoria son registro histórico; `herramientas/referencia/ht09_validador_g3.py` es copia del corpus. Ninguna referencia viva apunta a una ruta que ya no existe.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_01` (función `ct04_sin_los_cuatro_bloques`); ya lo fija `tests/test_t66_propuestas.py::test_pa10_ct04_aprueba_un_certificado_propuesto_y_rechaza_uno_desconocido` | El Anexo B V5.2 (frase nueva de esta tarea) dice: «Los cuatro bloques (`decisiones`, `valoracion_informe`, `configuracion` y `resultado_comunicado`) son opcionales…; un CT-04 sin ninguno se rechaza». `Bloque.decision` admite un quinto bloque, `aprobar_certificados` (PA-10, T-66), y un CT-04 que solo lo lleva no se rechaza (estado REGISTRADA o APLICADA). El Anexo B no nombra `aprobar_certificados`, que es la única vía por la que un certificado de horizonte (que relaja un control, R13) entra en vigor | Nombrar `aprobar_certificados` (lista de CERT-, opcional) entre los bloques de CT-04 y decir «un CT-04 sin ninguno de los cinco se rechaza»; ajustar `anexo_b_esquemas.json`/`anexo_b_ejemplos.json` y re-congelar | abierto |
| H-02 | media | `r01_01` (`ct15_respuesta`); `orquestacion.py`, `_redactar` | El Anexo B dice de CT-15 «respuesta: rutas de los tres entregables + métricas de legibilidad». El Redactor (AG-17) responde con el esquema `REDACCION` (`frases_30s`, `tarjetas`, `motivos_llanos`, `glosario`, `frase_historial`) y el Sintetizador V6 con `SINTESIS`; las rutas las escribe el ejecutor y la legibilidad la mide HT-07/HT-09. «Cómo se lee este anexo» enumera los retornos internos con esquema de respuesta (CT-06 a CT-08 y CT-11 a CT-14) y se deja CT-15, que también lo tiene. Texto heredado de la V5.1, no medido por ningún golden (CT-15.RETORNO no tiene esquema derivado) | Describir el retorno de CT-15 con la frase fija («con `REDACCION`, que exige …; admite además …», y `SINTESIS` en V6), decir que los entregables y su legibilidad los produce el ejecutor, y añadir CT-15 a `ESQUEMAS_DE_RESPUESTA` de la prueba. El §6.1 («devolución de los tres entregables») queda fuera del Anexo B; si se quiere tocar, es otra decisión del operador | abierto |
| H-03 | media | `r01_01` (`ct03_escalado_sin_ejecutar`, `ct06_prosa_de_los_anidados`) | Por la regla que el propio Anexo B V5.2 fija («Un campo marcado «opcional» o «si aplica» puede faltar; los demás campos nombrados los lleva el mensaje»), estas frases dicen que se lleva algo que el código no siempre da: (a) CT-03, el `escalado` «es un objeto con `run_id`, `plazo_estimado`, `nivel`, `clases`, `estado_run` y `respuesta_provisional`»; con `bloque-a consulta --sin-escalado` (`ejecutar_escalado=False`) no lleva `estado_run` y `run_id` es nulo; (b) CT-06, cada elemento de `cribado` lleva «la señal»: `INFORME_CLASE` exige `candidata`, `paso_gc1` y `motivo`, ningún campo de señal; (c) `finalistas` lleva «puntuaciones provisionales, pre-mortem, cálculos y evidencias»: `FINALISTA` no tiene puntuaciones (tiene `dimensiones`) ni cálculos; (d) cada elemento de `respuestas` lleva «la evidencia citada»: `evidencia_citada` es opcional en `RESPUESTA_OBJECIONES`. (b) y (c) vienen de la V5.1; ninguna lo mide una prueba | (a) «`estado_run` si el análisis se ejecutó; `run_id` nulo si no»; (b)–(d) nombrar los campos del esquema (`candidata`, `paso_gc1`, `motivo`; `dimensiones`, `premortem`, `afirmaciones`…) y marcar `evidencia_citada` «si aplica» | abierto |
| H-04 | baja | `r01_01` (`ct09_fecha_corte`) | La V5.2 cambia «`fecha_corte` (obligatoria en evaluaciones y backtesting)» por «obligatoria siempre» y el análisis lo justifica con «el ejecutor es más estricto». Solo lo es la mensajería (`CAMPOS_MINIMOS`), por la que no pasa ningún CT-09 del ejecutor; `Motor.servir` sirve una petición sin `fecha_corte` (toma la del proveedor, o ninguna: SERVED_WITH_LIMITATIONS con un proveedor sin fecha). Los llamadores del ejecutor siempre la envían, así que hoy no hay fuga | Decir en el Anexo B quién la exige («la exige la mensajería; el Motor, si falta, usa la fecha del proveedor») o hacer que el Motor la exija (cambio de código, fuera de esta tarea) | abierto |
| H-05 | baja | `r01_03` con C02, C07, D03, D04, D05, D06, D09 y D10 | Tras un re-congelado, las pruebas no detectan: valores de las listas de los retornos internos y del Motor en la prosa frente a `ESQUEMAS` (C02: un `veredicto_global` nuevo; D09: APTO en el dictamen; D10: un valor de `clase_cifra` inventado en la prosa), cuándo emite el ciclo cada fase de CT-06 (C07, D05) ni que la prosa vuelva a exigir un campo que el esquema derivado deja opcional (D03, D04) o añada uno anidado (D06). La correspondencia prosa → esquema derivado es a mano (diseño de T-114) y la huella del Documento 0 obliga a un re-congelado deliberado, así que no es una regresión; pero la frase fija de T-143 solo compara nombres de primer nivel | Extender `_esquemas_de_respuesta_que_difieren` a los valores (`enum`) que la prosa nombra; comparar las listas «son opcionales …» de cada párrafo con `required` del derivado; una prueba de qué fase de CT-06 emite cada nivel | abierto |
| H-06 | baja | `grep -n "subordinado al Documento 0" bloque_a/11_Ejecutor/config/por_defecto.yaml` | CA-6: una referencia viva no cita la V5.1 como vigente. La línea 2 de `config/por_defecto.yaml` dice «subordinado al Documento 0 óptima V5.1», la misma frase que la tarea corrigió en `11_Ejecutor/README.md` y en `tests/MAPA_PLAN_DE_PRUEBAS.md`; el análisis la cuenta entre las que «fechan en qué versión entró algo», pero no lo hace. Además, CLAUDE.md dice «695 archivos» del corpus (ya señalado por el implementador para la sesión coordinadora) | Cambiar la cabecera a «subordinado al Documento 0 óptima V5.2» (no es corpus) y, en la sesión coordinadora, 695 → 696 en CLAUDE.md | abierto |

Comprobado sin hallazgo (contrato a contrato, contra `contratos.py`, `orquestacion.py`, `diseno_v6.py`, `seguimiento.py`, `interfaz_broker.py` y `motor/servicio.py`): CT-01 (lo que exige la mensajería); CT-03 (query_id asignado por el bloque, `contexto` y `urgencia` opcionales); CT-06 (las siete fases, CRIBADO_E_INVESTIGACION en N2/N3 y REVISION_VIGENTES en los demás, RESPUESTA_OBJECIONES, SEGUIMIENTO sin informe del Analista y revisión calculada por `seguimiento.py`; frases fijas de los tres esquemas); CT-07/CT-08 (`BUSQUEDA`; las piezas de CT-11 las forma el ejecutor); CT-09 y CT-10 (claves de `Motor.servir`, caché, rechazo y `reejecutar`, también la re-ejecución fallida; ACLARACION_REQUERIDA en el `detalle` con motivo DATOS_INSUFICIENTES, aunque hoy solo la emite una ficha); CT-11 a CT-13 (lotes con los campos que se envían en V5 y V6, `clase`/`nivel` por elemento solo en V6, contrarréplica con `peticiones` vacía; sin `fechas`, `unidad_divisa`, tesis ni razonamiento); CT-14 (`DICTAMEN_G3`, sin dictamen del Orquestador si HT-09 da apto); CT-16, CT-17 y CT-19 (lo que se emite); CT-22 (`tipo` y `tipo_aviso`, únicos sitios que emiten cada valor); CT-23 a CT-25 (estado propio, normalización de `estado`, opcionales, recordatorio sin `herramienta` ni `urgencia`); las afirmaciones sobre qué listas cerradas comprueba la mensajería y qué exige en un retorno rechazado.

No comprobado: el retorno de CT-05 (no lo emite ningún flujo); la calidad del `.docx` que falta (INC-T143-01, no hay); el gate completo 12/12 (no lo pedía la tarea; ruff y mypy de A se midieron aparte con los mismos comandos).

Los scripts de ataque van en `revisores/` dentro de este ticket, numerados por ronda y sin sobrescribir.

## Veredicto

**NO APTO** · El movimiento de la V5.1, el re-congelado del corpus (solo las seis rutas), los goldens, la batería (mide lo mismo, byte a byte), el borrador y las incidencias están bien, y las pruebas que fijaban divergencias fallan si el código o el Anexo B vuelven a diferir en lo que dicen cubrir. Pero CA-6 no se cumple del todo (H-06) y el Anexo B V5.2, cuyo objetivo es describir lo que hace el ejecutor, contiene tres afirmaciones que el código contradice (H-01, frase nueva de esta tarea; H-02 y H-03, en parte heredadas). Son correcciones de texto pequeñas, y el momento de hacerlas es antes del commit: una vez congelada, la V5.2 solo se corrige con otra entrega autorizada del Documento 0. Siguiente paso: `ri-implementar` para H-01, H-02, H-03 y H-06 (H-04 y H-05 pueden ir a la deuda), re-congelar y QA r02 con estos mismos scripts.

## Ronda r02

- **Revisor:** Claude, subagente revisor sin el contexto de la implementación (no implementó T-143) · **Ronda:** r02 · 16-11-2026
- **Copia revisada:** worktree en `9f8bd53` («wip local: T-143 r02», sobre `3e63e2a` = r01 y `1ccffd5` = base), con el `.venv` del proyecto enlazado. Sin red ni gasto: cliente simulado y Motor local. Sin commit ni push.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6605 pasadas, 2 omitidas (46 min, con otras suites en paralelo); ≥ 607 |
| `tests/test_fase3_goldens.py` | 150 recogidas, 25 de ellas `test_t143_r02_*` (H-05) |
| `tests/goldens_ct.py` | «coinciden», código 0 |
| Goldens r01 → r02 | generados: solo `huellas.json` y `mensajes_ejemplo.json`; a mano: `anexo_b_esquemas.json`, `anexo_b_ejemplos.json`, README; una línea nueva «T-143 r02» en `REGISTRO.md` con su motivo |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | en verde; corpus íntegro con **696** archivos |
| Manifiesto | frente a `3e63e2a`, solo la línea de la V5.2 (`0695971f…` → `ca5ab7dd…`, igual al `sha256sum` del fichero); frente a `1ccffd5`, las mismas 6 rutas (r01_02) |
| `.docs/scripts/pruebas_scripts.sh` | 203 pasadas (línea base respetada) |
| `.docs/scripts/prueba_refs_vivas.py` | 25/25 |
| `.docs/scripts/borrador_anexo_b.py --comprobar` | 0 |
| ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2831 (cuota 2831) |
| mypy de A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 (cuota 109) |
| `./tools/check_all.sh --core` | 8/8 gates en verde (corpus 696, NFC, YAML, secretos, refs vivas, pytest A 6605, A-Forex 68, B 176) |
| `git diff --diff-filter=D 1ccffd5 HEAD -- .docs` | vacío: no se borró nada |
| `CLAUDE.md` | sin cambios frente a `1ccffd5` (el 695 → 696 lo hará la sesión coordinadora; no es hallazgo) |
| `config/por_defecto.yaml`, línea 2 | «subordinado al Documento 0 óptima V5.2 (15/11/2026)» (H-06 corregido) |
| `docs/incidencias.md` | INC-T114-01 con la ronda r02 de T-143; INC-T143-01 sigue |

### Scripts del revisor (orden de ejecución, desde la raíz, con el Python del `.venv`)

1. `.venv/bin/python .docs/tickets/T-143/revisores/r01_02_bateria_y_corpus.py 1ccffd5` → **0 fallos**: batería igual y `aceptaciones_rechazos.json` idéntico; manifiesto 695 → 696 con las seis rutas (dos V5.1 quitadas de `01_Gobernanza`, dos en el histórico con el mismo hash, la V5.2, el README índice cambiado) y los 696 hashes iguales al disco; el Documento 0 fuera del Anexo B solo cambia la cabecera y la fila del Anexo F (4 quitadas, 5 puestas); en la r02 ningún cambio fuera del Anexo B (`git diff 3e63e2a HEAD` del Documento 0: solo líneas 858–946).
2. `.venv/bin/python .docs/tickets/T-143/revisores/r02_01_anexo_b_contra_codigo.py` → **8 «HALLAZGO»** (código 1). Sustituye a `r01_01` (anclado al texto r01). Analizador propio de la prosa; lee del código qué esquema valida cada `_invocar` y lo confirma con dos ciclos simulados (V5 con auditoría y seguimiento C6, y V6), y compara contrato a contrato: frase fija de cada esquema, anidados (también dentro de FINALISTA), valores de las listas cerradas, `memoria` de cada tipo de CT-05, CT-03 con y sin escalado ejecutado, CT-04 con cinco bloques y con uno ajeno, CT-09 sin `fecha_corte` con y sin fecha del proveedor, CT-01 sin `alcance.clases`, lo que se lee de cada referencia de `BUSQUEDA`, los opcionales de CT-24.
3. `.venv/bin/python .docs/tickets/T-143/revisores/r01_03_mutantes.py <carpeta fuera del repo>` → C01–C09, D01, D02, D04, D05, D07, D08 y D10 **mueren**; C10 sobrevive; D03, D06 y D09 **no aplican** (su anclaje cambió).
4. `.venv/bin/python .docs/tickets/T-143/revisores/r02_02_mutantes.py <carpeta fuera del repo> [IDs]` → 25 mutantes con el procedimiento de `r01_03` (importado; `-x` en pytest). D03b, D06b y D09b (D03, D06 y D09 sobre el texto r02) **mueren**. En el código: C11 (INTEGRACION), C14 (REDACCION), C15 (CT-04), C16 (`estado_run`), C17 (Motor exige `fecha_corte`), C20 (BUSQUEDA), C24 (PROSPECTIVA) mueren; C21 (N2 emite REVISION_VIGENTES) muere al re-congelar por un `IndexError` de la captura, no por una prueba de T-143 (la regla la cubre C07, que muere). En el Anexo B: D11–D16 y D18 mueren. Sobreviven, como esperaba («?»): C12 (AUDITORIA), C13 (`tipo_opcion` nuevo), C18 y C19 (`memoria` de CT-05), D20 (CT-15 vuelve a decir «rutas y legibilidad»), D21 (CT-14 admite APTO en prosa), D23 (`memoria` de CT-05 en prosa). Se lanzó en dos mitades: `… D03b D06b D09b C11 C14 C15 C16 C17 C20 C21 C24 C12` y `… C13 C18 C19 D11 D12 D13 D14 D15 D16 D18 D20 D21 D23`; las dos terminan en 0.
5. `.venv/bin/python .docs/tickets/T-143/revisores/r02_03_prosa_en_memoria.py` → 8 cambios de prosa aplicados en memoria a las tres comprobaciones r02 (`_esquemas_de_respuesta_que_difieren`, `_listas_de_la_prosa_que_difieren`, `_opcionales_sin_marca`), que leen el párrafo y los derivados a mano (equivale a cambiar el Documento 0 y re-congelar). **Ninguno se detecta**, tampoco P01, P02, P03 y P07, que contradicen el código (H-08, H-11).

**C10 es equivalente.** Añade un campo al encargo de CT-06; el Anexo B («el esquema del operador puede añadir campos (6.2.3)») y los derivados lo admiten, así que no hay afirmación que contradiga. Sin re-congelar, `formas_flujos_mock.json` lo detecta por comparación byte a byte: la deriva no es silenciosa.

### Hallazgos de la r01

| ID | Estado en la r02 | Evidencia |
| --- | --- | --- |
| H-01 | corregido | CT-04 nombra los cinco bloques y «sin ninguno de los cinco se rechaza»; `Bloque.decision` mira esos cinco y rechaza uno ajeno (`r02_01`); C15 y D13 mueren |
| H-02 | corregido | CT-15 con `REDACCION` y `SINTESIS` y sus anidados, iguales a `ESQUEMAS`; V5 responde con REDACCION y V6 con SINTESIS en los flujos (`r02_01`); C14, D12 mueren. La última frase (quién escribe rutas y legibilidad) no la mide nada (D20, H-11) |
| H-03 | corregido | `cribado`, `finalistas` (22 obligatorios de FINALISTA), `evidencia_citada` «admite además», `estado_run` «solo si se ejecutó»; CT-05 INTEGRACION, `alcance` de CT-01 y `BUSQUEDA` con `ref_id`: todos coinciden con `ESQUEMAS` y el ejecutor (`r02_01`). Quedan H-07, H-08 y H-10, nuevos |
| H-04 | corregido | Motor sin `fecha_corte`: con proveedor sin fecha sirve (SERVED_WITH_LIMITATIONS); con fecha, usa la del proveedor (queda en RC); la mensajería la exige (`r02_01`); C17 y D15 mueren |
| H-05 | corregido | 25 `test_t143_r02_*`; C02, C07, D04, D05, D10 y D03b/D06b/D09b mueren; huecos nuevos en H-11 |
| H-06 | corregido | línea 2 de `por_defecto.yaml` cita la V5.2; CLAUDE.md, para la sesión coordinadora |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-07 | media | `r02_01` (`comprueba_ct05`); mutantes C18, C19 y D23 sobreviven | CT-05 da `memoria` como «(OPP- vigentes, TND- activas, LEC- aplicables, certificados de horizonte)» para toda orden, y la r02 añade INTEGRACION diciendo que solo cambia `insumos_integracion`. Solo la orden del ciclo lleva eso (`opp_vigentes`, `tnd_activas`, `lec_aplicables`, `certificados`). La orden SEGUIMIENTO (`seguimiento.py`) lleva `memoria` = `{senales_interes}` y `delta_gc0` vacío; la orden INTEGRACION (`_integrar`, nueva en el texto de la r02) lleva `{run_anterior, top3_anterior}` y `delta_gc0` con solo los motivos. Además, en el diseño V6 no hay orden INTEGRACION ni retorno con `INTEGRACION` (`diseno_v6.integracion_determinista`), y el párrafo no lo dice (el de CT-15 sí distingue V6). Ninguna prueba mide `memoria` | Decir qué lleva `memoria` en cada tipo: la del ciclo, las señales de interés en SEGUIMIENTO, el run anterior y su top-3 en INTEGRACION. Añadir «en el diseño V6 la integración es determinista y no hay orden INTEGRACION». Una prueba que compare las claves de `memoria` por tipo con los flujos | abierto |
| H-08 | media | `r02_01` («Regla de lectura» y «Campos anidados»); `r02_03` P03; C13 sobrevive | La introducción (texto de la r02) dice «En esas frases, un campo con lista cerrada lleva sus valores entre paréntesis» y que los anidados se describen con «En `ESQUEMA`, cada elemento de …». En la frase de `finalistas` (y por remisión, en `exploratorias`), `tipo_opcion` (lista cerrada `TIPOS_OPCION`, 8 valores), `horizontes_aplicables` (H1–H5) y `regiones` (10 códigos) van sin valores. Por la regla del anexo, un lector los toma por texto libre, y el código rechaza la ficha si no son de la lista. Los anidados de la ficha (`ambito`, `indicador_seguimiento`, `invertibilidad`, `catalizadores`, `afirmaciones`, `dimensiones`, `invalidacion_cuantitativa`, `tendencia`) tampoco tienen frase. La prueba lo salta a propósito (`_con_anidados` no recorre FINALISTA, y la rama «los opcionales de `FINALISTA`» hace `continue` antes de mirar los valores). El borrador lo reconoce («dentro de la ficha `FINALISTA` solo se comparan sus campos obligatorios»), pero el Anexo B no lo dice | Dar los valores de esos tres campos en la frase de `finalistas` (y que la prueba los mire), o acotar la regla en la introducción («salvo dentro de la ficha `FINALISTA`, cuyas listas y campos anidados están en `FINALISTA` de `contratos.py`») | abierto |
| H-09 | baja | `r02_01` (CT-17); C12 sobrevive | El Auditor responde por CT-17 con `AUDITORIA` (exige `hallazgos` y `resumen`, y cada hallazgo `regla`, `descripcion` y `severidad` (Crítica \| Material \| Operativa \| Menor)), que `_auditar` valida y lee. El Anexo B remite la respuesta a los prompts y la deja fuera de la lista de retornos internos con esquema («CT-05 a CT-08 y CT-11 a CT-15»), la misma omisión que H-02 tenía con CT-15. No dice nada falso | Describir el retorno de CT-17 con la frase fija y añadir CT-17 a la lista de la introducción y a `ESQUEMAS_DE_RESPUESTA` | abierto |
| H-10 | baja | `r02_01` (CT-07/CT-08) | «En `BUSQUEDA`, cada elemento de `referencias` lleva `ref_id` (una REF-)», sin «admite además». `_peticion_conocimiento` lee además `afirmacion`, `direccion`, `extracto` (o `motivo`) y `pronostico_fuente`, con valores por defecto, y con ellos forma las piezas de CT-11 que la frase siguiente menciona. Que `ref_id` sea una REF- ofrecida solo se exige en backtest | «admite además `afirmacion`, `direccion`, `extracto`, `motivo` y `pronostico_fuente`, que el ejecutor pasa a la pieza de CT-11» y «(una REF-; en backtest, una de las ofrecidas)» | abierto |
| H-11 | baja | `r02_03` (P01, P02 y P07); `r02_02` (D20, D21; C21) | Las pruebas r02 tienen huecos. (a) `_opcionales_sin_marca` acepta un campo si su frase contiene en cualquier sitio «solo », «salvo»…: «son obligatorios … y no solo `accion`» (CT-24), «los lleva toda respuesta, salvo error» (CT-25) y «`insumos_integracion` en todas las órdenes» (CT-05, en la frase de «van solo con SEGUIMIENTO») pasan. (b) No se mide la prosa que no es una lista de campos: tras re-congelar, CT-15 puede volver a decir que el Redactor devuelve rutas y legibilidad (D20, lo que corrigió H-02), y CT-14 puede decir que hay dictamen APTO (D21). (c) C21 muere por un `IndexError` de `goldens_ct.py --update`, no por una prueba | (a) Exigir que la marca acompañe al campo (por ejemplo, el campo dentro de la lista que sigue a «son opcionales», o «`campo` … si aplica»). (b) Fijar con una prueba de texto las frases que corrigió H-02 (y la de «No hay dictamen APTO»). (c) Nada que corregir en T-143 | abierto |

Comprobado sin hallazgo (contrato a contrato, contra `contratos.py`, `orquestacion.py`, `diseno_v6.py`, `seguimiento.py` y `motor/servicio.py`, y con los flujos simulados V5 y V6):
- CT-01: `alcance` opcional por dentro; sin `clases`, los tipos activos.
- CT-03: `escalado` con y sin análisis ejecutado.
- CT-04: los cinco bloques, y uno ajeno se rechaza.
- CT-05: `INTEGRACION` exige y admite lo que dice el anexo; el retorno parcial no lo lee ningún código; INTEGRACION no pasa por la mensajería.
- CT-06: los tres esquemas y sus anidados de primer nivel, con los valores de `recomendacion`; las fases por nivel.
- CT-07/CT-08: el primer nivel de `BUSQUEDA`.
- CT-09: lo que dice el anexo de la mensajería y del Motor.
- CT-11 a CT-14: `CURACION`, `PROSPECTIVA` (con `pronosticos` y sus tres listas), `REFUTACION`, `CONTRARREPLICA` y `DICTAMEN_G3`, todos con sus valores.
- CT-15: `REDACCION` y `SINTESIS` con `tarjetas` y `glosario`; V5 responde con uno y V6 con otro.
- CT-24: la lista de opcionales es la del bloque JSON menos `accion`.

El motivo del commit de «Ronda r02» del análisis es correcto: describe las seis rutas frente a `1ccffd5`, los dos re-congelados, los cambios de la r02 y INC-T143-01. Lleva el prefijo `docs:`, el más usado en el historial.

### Veredicto r02

**NO APTO** · Los seis hallazgos de la r01 están corregidos de verdad. El corpus solo cambia en las seis rutas declaradas (la V5.2 en `ca5ab7dd…`, 696 archivos). Fuera del Anexo B solo cambian la cabecera y la fila del Anexo F. Los goldens y su registro están bien, las 25 pruebas nuevas matan los mutantes de la r01 que siguen aplicando y los adaptados, la suite y las cuotas están en verde y no se borró nada de `.docs/`. Pero el texto nuevo de la r02 deja dos afirmaciones que el código contradice: `memoria` de CT-05, ahora también para INTEGRACION (H-07), y la regla de lectura frente a las listas cerradas de la ficha FINALISTA (H-08). Son de la misma clase que H-01 a H-03 de la r01, que dieron NO APTO. Son medias, pero son texto del corpus que se va a congelar: si pasan a la deuda, solo se corrigen con otra entrega (V5.3). Las dos se corrigen con pocas palabras y sin cambiar código. Siguiente paso: `ri-implementar` para H-07 y H-08 (y, si se quiere, H-09 y H-10, que son una frase cada uno), re-congelar y hacer la QA r03 con `r02_01`, `r02_02` y `r02_03`. H-11 puede ir a la deuda.

## Ronda r03

- **Revisor:** Claude, subagente revisor sin el contexto de la implementación (no implementó T-143) · **Ronda:** r03 · 16-11-2026
- **Copia revisada:** worktree en `0bcab3d` («wip local: T-143 r03», sobre la r02 `9f8bd53` y la base `1ccffd5`), con el `.venv` del proyecto enlazado. Sin red ni gasto. Sin commit ni push.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6627 pasadas, 2 omitidas y 1 fallo (89 min, con la máquina a carga 11–14) |
| El fallo | `tests/test_t102_filtro.py::test_r05_h37_sufijo_en_tiempo_lineal`: mide tiempo (< 2,0 s) y dio 3,9 s. Repetida a solas: falla una vez con 2,1 s y pasa la siguiente; ya en reposo, pasa (3,4 s en total) y pasa en el segundo `check_all`. T-143 no toca ni esa prueba ni `diseno_v6.py` (de `bloque_a/` solo cambia el docstring de `contratos.py`): es la carga de la máquina, no un hallazgo |
| `tests/test_fase3_goldens.py` | 173 (de 150) |
| `tests/goldens_ct.py` | «coinciden», código 0 |
| Goldens r02 → r03 | generados: solo `huellas.json` y `mensajes_ejemplo.json`; a mano: `anexo_b_esquemas.json`, `anexo_b_ejemplos.json` (CT-17.RETORNO), README; una línea «T-143 r03» en `REGISTRO.md` con su motivo; `goldens_ct.py` (captura): los flujos de decisión y seguimiento quedan vacíos si no hay opciones (H-11 c) |
| Corpus | `corpus_integridad.py`: 696 archivos. Frente a la r02, solo la línea de la V5.2 (`ca5ab7dd…` → `21d01585…`, igual al `sha256sum` del fichero); frente a `1ccffd5`, las mismas seis rutas (`r01_02`) |
| `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | en verde |
| `.docs/scripts/pruebas_scripts.sh` | 203 pasadas |
| `.docs/scripts/prueba_refs_vivas.py` | 25/25 |
| `.docs/scripts/borrador_anexo_b.py --comprobar` | 0 |
| ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2831 (cuota 2831) |
| mypy de A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 (cuota 109) |
| `./tools/check_all.sh --core` | primera vez, a carga 11–14: 7/8 (pytest A, 1 fallo: la misma prueba de tiempo); repetida con la máquina en reposo: **8/8** (corpus 696, NFC, YAML, secretos, refs vivas, pytest A 6628, A-Forex 68, B 176). Así, la suite completa de A pasa entera: 6628 pasadas |
| `git diff --diff-filter=D 1ccffd5 HEAD -- .docs` | vacío |
| `CLAUDE.md` | sin cambios frente a `1ccffd5` |
| `docs/incidencias.md` | INC-T114-01 con la ronda r03; INC-T143-01 sigue |
| Motivo del commit («Ronda r03» del análisis) | correcto: seis rutas frente a `1ccffd5`, los dos re-congelados, el contenido de las rondas r02 y r03, INC-T143-01. Si se corrige H-12, no hay que tocarlo («sin INTEGRACION en V6» sigue siendo cierto) |

### Scripts del revisor (desde la raíz, con el Python del `.venv`)

1. `.venv/bin/python .docs/tickets/T-143/revisores/r01_02_bateria_y_corpus.py 1ccffd5` → **0 fallos**. Batería igual y `aceptaciones_rechazos.json` idéntico. Manifiesto 695 → 696 con las seis rutas. Fuera del Anexo B, solo la cabecera y la fila del Anexo F; la r03 solo toca el Anexo B (líneas 858–918).
2. `.venv/bin/python .docs/tickets/T-143/revisores/r03_01_anexo_b_contra_codigo.py` → **5 «HALLAZGO»** (código 1). Sustituye a `r02_01`, que se cae porque busca «`memoria` (…)». Lee la notación «En `FINALISTA`, …» que fija la introducción, y con ella **la ficha queda bien descrita**: sus 8 anidados, los 13 opcionales y todos los valores, incluidos los de los opcionales nombrados. La notación basta y no es hallazgo. Además:
   - mide `memoria` y la forma de `delta_gc0` de cada tipo de CT-05 con espías en flujos V5, V6 y V6 con `v6.sintetizador: false`;
   - mide lo que el ejecutor lee de cada referencia de `BUSQUEDA` y de cada hallazgo de `AUDITORIA`;
   - mide qué retornos internos con esquema deja de pedir el V6 por defecto;
   - repite CT-01, CT-03, CT-04, CT-09 y CT-24 como en la r02.

   Sus cinco líneas: H-12 (V6 sin sintetizador), H-13 (CT-11), H-14 (`objeto` de AUDITORIA y las 3 primeras referencias). La quinta, CT-17 en el V6, es falso positivo: el Auditor del V6 se muestrea por run (`auditoria_fraccion`), no deja de existir.
3. `.venv/bin/python .docs/tickets/T-143/revisores/r02_03_prosa_en_memoria.py` → sin mutar no ve nada. **P01, P02, P05, P06, P07 y P08 DETECTADOS**; P03 y P04 no aplican (su anclaje cambió). P03 adaptado a mano sobre el texto nuevo («`tipo_opcion` (MERCADO | PAIS)») se detecta.
4. `.venv/bin/python .docs/tickets/T-143/revisores/r03_02_mutantes.py <carpeta fuera del repo>` → 14 mutantes sobre lo reescrito en la r03, con el procedimiento de `r01_03`:
   - mueren D23b (D23 adaptado), D24 (`delta_gc0` de SEGUIMIENTO), D25–D27 (FINALISTA: `region`, ESTRUCTURAL, opcionales del indicador), D28 (severidades), D29 (sin la nota del V6), C25 (`delta_gc0` no vacío), C26 (severidad nueva) y C27 (opcional nuevo en FINALISTA);
   - sobreviven, como esperaba («?»): D30 y C28 (el valor por defecto de `direccion` en la prosa o en el código), D31 (sin la regla de backtest) y C29 (otra clave leída de cada hallazgo), que son H-14 y H-15.
5. `r01_03_mutantes.py` y `r02_02_mutantes.py`, en paralelo en dos carpetas: el trabajo en segundo plano se paró al llegar al límite de 2 h, con la máquina a carga 14. Antes del corte:
   - en `r01_03`, C01–C09 mueren;
   - en `r02_02`, mueren D03b, D06b, D09b, C11, C14, C15, C16, C17, C20, C24 y **C21, ahora por una prueba** (159 s, sin `IndexError`).

   Lo que faltaba lo pasé una sola vez, por tandas, cuando la máquina ya estaba en reposo (todo terminado):
   - `r02_02_mutantes.py <carpeta> C12 C13 C18 C19 D20 D21`: **mueren los seis** que sobrevivían en la r02;
   - `r01_03_mutantes.py <carpeta> C10 D01 D02 D03 D04 D05 D06 D07 D08 D09 D10`: mueren D01, D02, D04, D05, D07, D08 y D10; C10 sobrevive (equivalente, como en la r02); D03, D06 y D09 no aplican (su anclaje cambió en la r02; sus versiones D03b, D06b y D09b mueren);
   - `r02_02_mutantes.py <carpeta> D11 D12 D13 D14 D15 D16 D18 D23`: mueren D11–D16 y D18; D23 no aplica (su anclaje cambió en la r03; D23b de `r03_02` muere).

   Con eso, **todos los mutantes de `r01_03`, `r02_02` y `r03_02` que debían morir mueren**, y no sobrevive ninguno inesperado. Los scripts terminan con 1 solo por los que no aplican. Los mutantes del implementador están dentro de `test_fase3_goldens.py` y pasan con la suite.

### Hallazgos de la r02

| ID | Estado en la r03 | Evidencia |
| --- | --- | --- |
| H-07 | corregido, salvo la nota del V6 (H-12) | `memoria` y `delta_gc0` de la orden del ciclo, de SEGUIMIENTO y de INTEGRACION coinciden con los flujos (`r03_01`); C18, C19, C25, D23b y D24 mueren |
| H-08 | corregido | valores de `tipo_opcion`, `horizontes_aplicables`, `regiones` y de los opcionales; 8 frases «En `FINALISTA`, …» iguales al código (`r03_01`); C13, C27, D25–D27 mueren |
| H-09 | corregido | CT-17 con `AUDITORIA`, en la lista de la introducción; C12, C26, D28 mueren. Queda `objeto` (H-14) |
| H-10 | corregido | lo que se lee de cada referencia y sus valores por defecto coinciden con `_peticion_conocimiento` (`r03_01`); sin prueba (H-15) |
| H-11 | corregido | (a) P01, P02, P07 y P08 detectados; (b) D20, D21, P05 y P06 detectados; (c) C21 muere por una prueba |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-12 | media | Texto nuevo de la r03 en CT-05: «En el diseño V6 no hay orden INTEGRACION ni su retorno: la integración la calcula el código». Contrastar con `diseno_v6.integracion_determinista` (su docstring: «La lectura del conjunto y los factores los escribe el Sintetizador»), `INSTR_SINTESIS` («escribe la integración (régimen macro común, el factor que domina cada clúster, la lectura del conjunto, preguntas sugeridas para el Broker y limitaciones)») y `_aplicar_integracion`; `r03_01` («V6 con `v6.sintetizador: false`») | En el V6 el código calcula antes de G3 una integración provisional: régimen de cada tipo unido y cambios frente al run anterior, con factores, preguntas y limitaciones vacíos y una lectura de relleno. Después, el Sintetizador (AG-26, CT-15, `SINTESIS`) escribe en el paquete `regimen_macro`, los factores dominantes, las preguntas, la lectura del conjunto y las limitaciones. Es decir, la integración del V6 la escribe un modelo, y la frase dice lo contrario. La frase solo vale además con `v6.sintetizador: true` (el valor por defecto): con `false`, el V6 emite la orden INTEGRACION a AG-02 (y CT-15 con `REDACCION`). Es una afirmación de la r03 que el código contradice, en texto que se congela | Cambiar la frase por «En el diseño V6 (con `v6.sintetizador`, el valor por defecto) no hay orden INTEGRACION ni su retorno: el código calcula antes de G3 el régimen de cada tipo y los cambios frente al run anterior, y el Sintetizador escribe después la integración con `SINTESIS` (CT-15)». Ajustar la frase fija de la prueba. Opcional: en CT-15, «los campos de integración de `SINTESIS` son la integración del V6» | abierto |
| H-13 | baja | `r03_01` (CT-11); `config/por_defecto.yaml` (`v6.curacion_llm: false`, `v6.dictamen_g3_llm: false`); `orquestacion.py` (curación solo en N2/N3; `_validar_g3`) | Desde la r03 el Anexo B dice qué cambia en el V6 en CT-05 y CT-15, pero no en dos sitios iguales. CT-11: con el valor por defecto el V6 no pide al Curador (ningún `CURACION`); en el V5 solo se pide en N2 y N3. CT-14: el V6 dictamina por regla, sin AG-18 ni `DICTAMEN_G3`. Nada de lo que dice es falso: está incompleto | En CT-11, «el ejecutor lo pide en N2 y N3; en el diseño V6, solo con `v6.curacion_llm`». En CT-14, «en el diseño V6, el dictamen lo da la regla salvo con `v6.dictamen_g3_llm`» | abierto |
| H-14 | baja | `r03_01` (CT-17 y CT-07/CT-08); C29 sobrevive | Como en H-10, el ejecutor lee campos que el esquema no pide. `_auditar` toma de cada hallazgo `objeto` (por defecto, el run), y la frase de `AUDITORIA` no lo nombra. `_peticion_conocimiento` solo usa las tres primeras referencias de la respuesta (`[:3]`, como el `max_fuentes` del encargo), y el Anexo B no lo dice | «De cada hallazgo toma además, si lo trae, `objeto` (si no, el run)» y «solo cuentan las tres primeras referencias» | abierto |
| H-15 | baja | `r03_02`: D30, D31 y C28 sobreviven tras re-congelar | Ninguna prueba fija lo que H-10 añadió: los valores por defecto de `afirmacion` y `direccion` y la regla de backtest pueden cambiar en la prosa o en el código sin que falle nada (`pruebas.md` lo da por «revisión del texto») | Una prueba de texto de esas frases frente a `_peticion_conocimiento`, o una medida con el cliente simulado | abierto |

Comprobado sin hallazgo con `r03_01` (contrato a contrato, contra `contratos.py`, `orquestacion.py`, `diseno_v6.py`, `seguimiento.py` y `motor/servicio.py`, con flujos V5 y V6):
- CT-01, CT-03, CT-04, CT-09 y CT-24, como en la r02.
- CT-05: `memoria` y `delta_gc0` de los tres tipos; `INTEGRACION`; ninguna orden INTEGRACION en el V6 por defecto.
- CT-06: los tres esquemas y la ficha completa (22 obligatorios, 13 opcionales con sus valores, 8 anidados).
- CT-07/CT-08: el primer nivel de `BUSQUEDA` y lo que se lee de cada referencia.
- CT-11 a CT-15, con sus valores.
- CT-17: `AUDITORIA` y sus severidades.
- La regla de lectura se cumple en todas las frases, también en los opcionales nombrados.

### Veredicto r03

**NO APTO** · H-07 a H-11 están corregidos. El corpus solo cambia en las seis rutas (la V5.2 en `21d01585…`, 696 archivos). Fuera del Anexo B solo cambian la cabecera y la fila del Anexo F. Los goldens y su registro están bien, las 173 pruebas matan todos los mutantes que debían morir (y los seis que sobrevivían en la r02), y las cuotas, los gates, `check_all --core` (8/8) y la suite (6628 pasadas) están en verde.

Queda **un hallazgo medio de texto, H-12**. La frase que la r03 añadió sobre el V6 en CT-05 («la integración la calcula el código») la contradice el código: en el V6 la integración la escribe el Sintetizador con `SINTESIS`, y la frase solo vale con `v6.sintetizador` activado. Es una frase, pero una vez congelada solo se corrige con otra entrega.

Los bajos H-13 a H-15 no bloquean. H-15 es de pruebas y cabe en la deuda. H-13 y H-14 son texto del Anexo B, incompleto pero no falso. Cabrían en la deuda como pendientes de la próxima entrega del Documento 0, pero son una frase cada uno, y lo razonable es corregirlos con H-12 antes de congelar.

Siguiente paso: `ri-implementar` para H-12 (y, si se quiere, H-13 y H-14), re-congelar y hacer la QA r04 con `r03_01` y `r03_02`.

## Ronda r04

- **Revisor:** Claude, subagente revisor nuevo sin el contexto de la implementación (no implementó T-143) · **Ronda:** r04 · 17-11-2026. La QA r04 anterior se cortó al empezar; esta empieza desde cero.
- **Copia revisada:** worktree en `0b09071` (rama local `wip/t143`: la r04 `238ef4d` más la instantánea de la pausa, sobre `1ccffd5`), con el `.venv` del proyecto. Sin red ni gasto. Sin push. Por orden de la sesión coordinadora no paso la suite completa de A ni `check_all.sh` (hay otros agentes); sí `test_fase3_goldens.py`, `goldens_ct.py`, los gates ligeros y los scripts de revisor.
- **Aviso de método.** La carpeta de trabajo (scratchpad) es compartida con sesiones anteriores: ya había `mut_r03/` y `mut_r04/` de la QA cortada, con un Documento 0 mutado a medias (D23b aplicado), y `r01_03_mutantes.py` reutiliza `DESTINO/arbol` si existe. Mi primera pasada de `r03_02` dio por eso D23b y D24 «NO APLICA»; la descarté y repetí todo en carpetas nuevas (`r04b_*`). Cualquier revisor que repita: usar un `DESTINO` que no exista.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| `tests/test_fase3_goldens.py` | **180 pasadas** (173 + 7 `test_t143_r04_*`), 120 s |
| `tests/goldens_ct.py` | «coinciden», código 0 |
| Goldens r03 → r04 | solo `huellas.json` (la huella de la V5.2, `21d01585…` → `d8f9e3d0…`) y una línea «T-143 r04» en `REGISTRO.md` con su motivo; esquemas y ejemplos derivados sin cambios |
| `tools/corpus_integridad.py` | 696 archivos íntegros. Frente a la r03, solo la línea de la V5.2 (`d8f9e3d0…`, igual al `sha256sum` del fichero). Frente a `1ccffd5`: las dos V5.1 de `01_Gobernanza` quitadas, las dos del histórico con los mismos hashes (`26691b68…` `.docx`, `7e708a03…` `.md`, comprobado con `sha256sum`), la V5.2 nueva y el README índice (`70f6b0de…` → `e25d7eb7…`); nada más. `develop` no ha cambiado el manifiesto desde `1ccffd5` |
| `01_Gobernanza` | un solo Documento 0 (la V5.2) |
| Fuera del alcance (`git diff 1ccffd5 HEAD`) | sin cambios en `CLAUDE.md`, `bloque_a_forex/`, `bloque_b/`, `sistema_global/marco_comun_c/` ni la Constitución. En `sistema_global/seguimiento/`: la fila de la decisión del operador (en el alcance) y **la deuda técnica (fuera del alcance, H-18)**; además, un `.venv` versionado (H-18) |
| `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | en verde |
| `.docs/scripts/borrador_anexo_b.py --comprobar` | 0 |
| Integración con `develop` (`c728c91`), en otra copia: `git merge --no-commit 238ef4d` | sin conflictos; corpus 696 íntegro, `goldens_ct.py` coincide, `refs_vivas` en verde, `test_fase3_goldens.py` 180 pasadas, `r04_01` 0 hallazgos y `r03_01` las mismas 3 líneas. Lo que `develop` añadió desde `1ccffd5` (T-152 a T-190: guías CT-18, CT-10 con conglomerados, HT-09 MET13…) no contradice el Anexo B V5.2 en lo que miden las pruebas y los scripts |

### Afirmaciones nuevas del Anexo B, contra el código

| Contrato | Frase de la r04 | Código | Resultado |
| --- | --- | --- | --- |
| CT-05 | V6 con `v6.sintetizador` (por defecto `true`, `config/por_defecto.yaml`): sin orden INTEGRACION; el código calcula antes de G3 el régimen de cada tipo y los cambios; el Sintetizador escribe la integración con `SINTESIS`. Sin `v6.sintetizador`, INTEGRACION como el V5 | `Bloque.ciclo` (orquestacion.py:682): `integracion_determinista` (régimen y `cambios_vs_anterior`) o `_integrar` (CT-05 INTEGRACION a AG-02); `_redactar`: `v6.sintetizar` (AG-26, `SINTESIS`, `_aplicar_integracion`) o AG-17 con `REDACCION` | cierta |
| CT-15 | el Sintetizador responde con `v6.sintetizador`; si no, el Redactor con `REDACCION`; «los campos de integración de `SINTESIS` son la integración del V6» | `_redactar` y `_aplicar_integracion` (`regimen_macro`, `factor_dominante` de cada clúster, preguntas, lectura, limitaciones) | cierta |
| CT-11 | curación solo en N2 y N3; en el V6 solo con `v6.curacion_llm` (por defecto `false`): sin CT-11, curación determinista | `_registrar_evidencia_clase` (orquestacion.py:1305) | cierta; `r04_01` lo mide en N0–N3 × {V5, V6, V6 con `curacion_llm`} |
| CT-14 | V6 salvo `v6.dictamen_g3_llm` (por defecto `false`): el CT-14 se emite, sin dictamen de AG-18; regla: apto con advertencias sin bloqueos, bloqueado con ellos | `_validar_g3` (orquestacion.py:1757–1772) | cierta; `r04_01` lo mide con HT-09 en ADVERTENCIA y en BLOQUEO × {V5, V6, V6 con `dictamen_g3_llm`} |
| CT-17 | de cada hallazgo, `objeto` si lo trae; si no, el run | `_auditar`: `h.get("objeto", run_id)` | cierta (con `objeto: null` explícito queda `None`: es del código, no del texto; observación) |
| CT-07/CT-08 | solo las tres primeras referencias | `_peticion_conocimiento`: `[:3]` antes del filtro de backtest | cierta; `r04_01`: con cinco ofrecidas cuentan tres, y una no ofrecida entre las tres primeras no la sustituye la cuarta |

Ninguna afirmación nueva es falsa. **H-12, H-13 y H-14 están corregidos.**

### Scripts del revisor (desde la raíz, con el Python del `.venv`)

1. `r01_02_bateria_y_corpus.py 1ccffd5` → **0 fallos** (batería y `aceptaciones_rechazos.json` iguales, seis rutas en el manifiesto, fuera del Anexo B solo la cabecera y la fila del Anexo F).
2. `r03_01_anexo_b_contra_codigo.py` → 3 «HALLAZGO», los tres falsos positivos, como dice el implementador: los dos de CT-05 buscan literalmente la frase de la r03 («En el diseño V6 no hay orden INTEGRACION ni su retorno», línea 291 del script) y miden justo lo que dice el texto nuevo (0 órdenes con el V6 por defecto; 1 con `sintetizador: false`, que el texto nuevo cuenta); el de CT-17 es el muestreo del Auditor en el V6 (`auditoria_fraccion`), ya señalado en la r03.
3. `r02_03_prosa_en_memoria.py` → sin mutar no ve nada; P01, P02, P05–P08 detectados; P03 y P04 no aplican (como en la r03).
4. **Nuevo** `r04_01_interruptores_v6.py` → **0 hallazgos** (22 comprobaciones: tabla de arriba).
5. `r03_02_mutantes.py <carpeta nueva>` → **mueren 13 de 14**, entre ellos C28, C29, D30 y D31, que sobrevivían en la r03 (CA-16). D29 no aplica: su anclaje es la frase de la r03 que H-12 cambió; su versión adaptada, D29b de `r04_03`, muere. Lo que dice el implementador es cierto.
6. **Nuevo** `r04_02_mutantes.py <carpeta nueva>` (8 mutantes sobre lo de la r04): mueren E04 (cuatro referencias), E05 (V6 con INTEGRACION) y F03 (otra regla del dictamen en la prosa); **sobreviven E01** (el V6 pide el dictamen a AG-18 sin `dictamen_g3_llm`), **E02** (el V6 no cura ni con `curacion_llm`), **E03** (curación también en N1), **F01** (sin «Los campos de integración de `SINTESIS` son la integración del V6») y **F02** (sin la condición del Sintetizador en CT-15). Son «?» (nadie decía cubrirlos): H-16.
7. **Nuevo** `r04_03_mutantes_adaptados.py <carpeta nueva>`: D12 de `r02_02` (SINTESIS sin `limitaciones`) tampoco aplica desde la r04, porque la frase nueva de CT-15 cambia su anclaje (el implementador solo nombra D29); D12b y D29b son los dos adaptados → **mueren D12b y D29b**.
8. `r02_02_mutantes.py <carpeta nueva> D09b D11 D20 D21 C12 C18 C19` y `r01_03_mutantes.py <carpeta nueva> D01 D07 D08 C01` (los que tocan los párrafos que cambió la r04) → **mueren los once** (D09b, D11, D20, D21, C12, C18, C19; D01, D07, D08, C01).

### Hallazgos de la r03

| ID | Estado en la r04 | Evidencia |
| --- | --- | --- |
| H-12 | corregido | frase de CT-05 y de CT-15 iguales al código (tabla); frase prohibida de la r03; E05 muere |
| H-13 | corregido (texto) | CT-11 y CT-14 iguales al código (`r04_01`); las pruebas no los fijan del todo (H-16) |
| H-14 | corregido | CT-17 y CT-07/CT-08 iguales al código; C29 y E04 mueren |
| H-15 | corregido | C28, C29, D30 y D31 mueren (CA-16) |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-16 | baja | `r04_02_mutantes.py <carpeta nueva> E01 E02 E03 F01 F02` | Lo que la r04 añadió del V6 en CT-14 y CT-11 y las dos frases nuevas de CT-15 pueden cambiar en el código o en la prosa sin que falle nada. La aserción `("CT-14", "DICTAMEN_G3") not in v6` de `test_t143_r04_lo_que_cambia_en_el_v6_…` es vacía: con el cliente simulado HT-09 sale APTO y el ciclo no llega a CT-14 (el análisis lo reconoce: «la otra mitad queda en la frase fija»); el ciclo corto va en N2 y no ve N0/N1 ni el V6 con `curacion_llm`; `FRASES_FIJAS["CT-15"]` no lleva las dos frases nuevas | En `tests/test_fase3_goldens.py`: (a) `test_t143_r04b_dictamen_g3_del_v6`, parametrizada en V5, V6 y V6 con `v6: {dictamen_g3_llm: true}` × HT-09 en ADVERTENCIA y en BLOQUEO, que sustituye `orquestacion.sint.ht09_validar` (con `monkeypatch`) por una comprobación `C05` con ese resultado, cuenta los `mensajeria.crear("CT-14", …)` y las invocaciones `("AG-18", "CT-14", "DICTAMEN_G3")` de `_validar_g3({"clases": {}, "limitaciones": []}, {}, …)` y exige: CT-14 emitido en los seis casos; DICTAMEN_G3 pedido en V5 y en V6 con `dictamen_g3_llm`, no en V6; dictamen APTO_CON_ADVERTENCIAS o BLOQUEADO (lo de la sección 1 de `r04_01`); (b) `test_t143_r04b_curacion_por_nivel_y_diseno`, en N1 y N2 × V5, V6 y V6 con `v6: {curacion_llm: true}`, que llama a `_registrar_evidencia_clase` con una finalista con una pieza (`_filtrar_evidencia` sustituido) y exige CT-11 solo en N2 del V5 y del V6 con `curacion_llm` (sección 2 de `r04_01`); (c) añadir a `FRASES_FIJAS["CT-15"]` «En el diseño V6 (con \`v6.sintetizador\`, el valor por defecto; si no, responde el Redactor con \`REDACCION\`), el Sintetizador responde con \`SINTESIS\`» y «Los campos de integración de \`SINTESIS\` son la integración del V6.». Después, E01, E02, E03, F01 y F02 de `r04_02` deben morir | abierto |
| H-17 | baja | `r02_02_mutantes.py … D12` → «NO APLICA»; `pruebas.md` («Ronda r04») | `pruebas.md` dice que, de los mutantes anteriores, solo D29 deja de aplicar; D12 de la r02 también, por la frase nueva de CT-15. No es un hueco de pruebas (D12b muere: muere), pero el informe está incompleto | En `pruebas.md`, «Ronda r04», tras el párrafo de D29: «D12 de `r02_02` tampoco aplica (la frase nueva de CT-15 cambia su anclaje); su versión adaptada, D12b de `r04_03_mutantes_adaptados.py`, muere, como D29b.» | abierto |
| H-18 | baja | `git show --stat 0b09071`; `git show develop:sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | La instantánea de la pausa (`0b09071`), que forma parte de la rama a integrar, versiona `.venv` (un enlace simbólico a la ruta absoluta del venv del árbol principal: `.gitignore` tiene `.venv/`, que no casa con un enlace) y cambia filas de la deuda técnica fuera del alcance (T-151, T-152 y una T-153 nueva), contra lo que dice el README («la fila no se toca en esta tarea: la actualiza la sesión coordinadora»). Esas filas ya no son las de `develop` (allí T-151 manda sus hallazgos a T-154 y T-153 es otro ticket): integrarlas reescribiría la deuda con texto rancio | No integrar el contenido de `0b09071`: el commit final de T-143 se hace sobre `develop` con el árbol de `238ef4d` más la ronda de cierre (en la copia de integración, `git merge --no-commit 238ef4d` no da conflictos); si se parte de `wip/t143`, antes `git rm --cached .venv` y `git checkout develop -- sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`. Y comprobar `git diff --name-status develop` antes de commit: ni `.venv` ni la deuda | abierto |

Observaciones (sin hallazgo): con `objeto: null` explícito, `_auditar` escribe `objeto: None` en el HAL (código, fuera del alcance de T-143); el V6 cambia también quién atiende CT-07/CT-08 (`v6.lector_evidencia`, AG-28) y CT-03 N0 (`v6.respondedor`) y muestrea el Auditor (`auditoria_fraccion`), y el Anexo B no lo dice; no es falso (no nombra al agente de CT-07/CT-08 ni promete auditar cada run), y el borrador no lo pedía.

### Criterios

CA-1 a CA-9: se mantienen (`r01_02`, corpus, goldens, `refs_vivas`, borrador). CA-10: no repetido por orden de la coordinación (la r04 solo cambia el Anexo B, `huellas.json`, `REGISTRO.md` y pruebas; el implementador dio 6635 pasadas y cuotas 2831/109); quien integre pasa `check_all.sh` sobre `develop`. CA-15: H-12 a H-14 corregidos. CA-16: C28, C29, D30 y D31 mueren.

### Veredicto r04

**APTO** · H-12 a H-15 están corregidos y ninguna afirmación nueva del Anexo B es falsa: las seis frases de la r04 coinciden con `orquestacion.py` y `diseno_v6.py`, medidas con el ejecutor (`r04_01`) y no solo con la prosa. La entrega del corpus está limpia: el manifiesto solo cambia en las seis rutas (696 archivos), el histórico tiene los mismos hashes y no se toca nada de otros bloques, de `marco_comun_c`, de la Constitución ni de `CLAUDE.md`. Los goldens coinciden (solo `huellas.json` en la r04), pasan las 180 pruebas de `test_fase3_goldens.py`, y la rama se integra sobre `develop` sin conflictos, con las mismas comprobaciones en verde.

No hay hallazgos críticos, altos ni medios. Quedan **tres bajos (H-16 a H-18)**. Por la regla del operador (16-11-2026) no van a la deuda: se subsanan en una **ronda de cierre** de T-143 con la corrección exacta de la tabla, y el ticket no se cierra antes. Para cerrar hace falta:

- que E01, E02, E03, F01 y F02 de `r04_02` mueran;
- `pruebas.md` corregido (H-17);
- el commit sobre `develop` sin `.venv` ni la deuda (H-18), con `check_all.sh` en verde sobre `develop`.

La revisión de esa ronda puede limitarse a volver a pasar `r04_02` y `git diff --name-status develop`.

## Ronda de cierre

- **Revisor:** el mismo de la r04 (Claude, subagente revisor; no implementó T-143) · 17-11-2026.
- **Copia revisada:** `t143cierre`, desacoplada sobre `origin/develop` (`c728c91`): `57bbdc0` (el merge de `238ef4d` con `qa.md` y `revisores/` de la QA r04, iguales byte a byte a `6336cdc`) y `449fc8e` (la ronda de cierre). Para ejecutar, un enlace `.venv` temporal sin versionar, quitado antes del commit. Sin suite completa ni `check_all.sh` (orden de la coordinación: se pasan al integrar).

| Comprobación | Resultado |
| --- | --- |
| `git diff --name-status origin/develop HEAD` | ni `.venv` ni `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`; de `sistema_global/` solo la fila de la decisión del operador; las rutas son las de la r04 (Documento 0 V5.2, V5.1 al histórico, goldens, pruebas, ticket, README índice, manifiesto, incidencias, prompts, borrador) |
| `git diff 238ef4d HEAD -- bloque_a tools` | lo que trae `develop` y, de T-143, solo `tests/test_fase3_goldens.py` |
| `tests/test_fase3_goldens.py` | **192 pasadas** (180 + 6 + 6) |
| `goldens_ct.py` / `corpus_integridad.py` | coinciden / 696 íntegros, sin re-congelar |
| ruff (los tres ejecutores) | 2813, la cuota de `develop` (`tools/cuotas.txt`); `test_fase3_goldens.py` sin hallazgos |
| `refs_vivas`, `secrets_scan`, `nfc_check` | en verde |
| `r04_02_mutantes.py <DESTINO nuevo>` | **mueren los 8**, código 0: E01 lo mata `test_t143_r04b_dictamen_g3_del_v6[V6-…]`; E02 y E03, `test_t143_r04b_curacion_por_nivel_y_diseno` (`[V6 con curacion_llm-N2]` y `[V5-N1]`); F01 y F02, las frases fijas nuevas de CT-15; E04, E05 y F03, como en la r04 |

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-16 | corregido | (a) `test_t143_r04b_dictamen_g3_del_v6` (6 casos: CT-14 emitido siempre, DICTAMEN_G3 salvo en el V6, dictamen APTO_CON_ADVERTENCIAS o BLOQUEADO), y fuera la aserción vacía; (b) `test_t143_r04b_curacion_por_nivel_y_diseno` (6 casos); (c) las dos frases en `FRASES_FIJAS["CT-15"]`. E01, E02, E03, F01 y F02 mueren |
| H-17 | corregido | el párrafo de D12 / D12b en «Ronda r04» de `pruebas.md`, con el texto propuesto |
| H-18 | corregido | la rama parte de `develop` sin `0b09071`; el diff no trae `.venv` ni la deuda |

### Veredicto final

**APTO.** Todos los criterios se cumplen y no queda ningún hallazgo abierto: H-01 a H-15 se corrigieron en las rondas r02 a r04, y H-16 a H-18 en esta ronda de cierre. T-143 queda CERRADO. Al integrar en `develop`, falta pasar `check_all.sh` (12/12) y hacer el commit con el motivo de «Ronda r04» del análisis técnico, sin `[pendiente QA]`. La fila de T-143 en la deuda técnica la actualiza la sesión coordinadora.
