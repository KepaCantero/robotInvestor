# T-143 · Pruebas

| Suite | Antes (`1ccffd5`) | Después |
| --- | --- | --- |
| `bloque_a/11_Ejecutor/tests/test_fase3_goldens.py` | 102 | 125 (todas en verde) |
| Suite completa del Bloque A | ≥ 607 (línea base del gate) | 6580 pasadas, 2 omitidas (32 min) |
| `.docs/scripts/pruebas_*.py` (`pruebas_scripts.sh`) | 203 | 203 |
| `.docs/scripts/prueba_refs_vivas.py` | 25/25 | 25/25 |
| `goldens_ct.py` (comprobación) | coinciden | coinciden (tras el re-congelado deliberado) |
| `.docs/scripts/borrador_anexo_b.py --comprobar` | 0 | 0 |

No hay pruebas del verificador de IDs: `bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py` no existe (está en `tools/refs_allowlist.txt` como entregable futuro de la Fase 0); de `prompts/FASE0_VERIFICADOR_IDS.md` solo cambia la ruta del Documento 0.

## Pruebas de `test_fase3_goldens.py`

Actualizadas a propósito (fijaban divergencias que la V5.2 corrige; ahora fijan la coincidencia y siguen fallando si vuelve la diferencia):

- `CON_CAMPOS` / `SIN_CAMPOS`: CT-16, CT-17 y CT-19 pasan a tener campos; sin campos, CT-18, CT-20 y CT-21.
- `test_ca4_ct22_lleva_tipo_o_tipo_aviso_y_ct18_ct20_ct21_ningun_campo` (antes `…_de_ct16_a_ct22_el_anexo_b_solo_nombra_el_tipo_de_ct22`): el párrafo nombra exactamente `tipo` y `tipo_aviso` con sus valores; el esquema derivado, con `oneOf`; uno, sí; ninguno o los dos, no.
- `test_ca4_un_ejemplo_sin_un_campo_obligatorio_o_fuera_de_lista_no_cumple`: `> 150` → `== 99` (hay menos campos obligatorios; el número exacto detecta uno que deja de serlo).
- `test_ca4_los_retornos_declaran…`: 16 retornos (más CT-19) y la frase del Anexo B sobre los retornos rechazados.
- `test_ca4_un_campo_de_otro_contrato_se_detecta`: el campo mutado de CT-13.RETORNO cuelga ahora de `resultados`.
- `test_ca7_el_tipo_de_ct22_coincide_con_el_anexo_b_y_vuelve_a_diferir_si_cambia` (antes `…_esta_congelado`): sin diferencia hoy; con los cuatro valores en `tipo` (lo que decía la V5.1) vuelve la diferencia de campo; con los dos campos o ninguno, falla el `oneOf`.
- `test_los_mensajes_de_ejemplo…`: ningún ejemplo rechazado (antes, CT-11 a CT-13).
- `test_las_huellas…`: la huella es la de la V5.2.
- `test_h01_los_flujos_cubren…`: valores de `tipo` y `tipo_aviso` en CT-22 y de `estado_consulta` en CT-23.

Nuevas (`test_t143_*`, 23 casos):

| Prueba | Qué fija |
| --- | --- |
| `test_t143_los_retornos_internos_son_los_esquemas_de_respuesta_del_codigo` | De cada retorno interno, el Anexo B nombra exactamente lo que exige y admite cada esquema de `ESQUEMAS`, y el derivado no exige nada |
| `test_t143_un_cambio_en_los_esquemas_de_respuesta_se_nota` (5 mutantes) | Un campo exigido nuevo o que deja de serlo, uno admitido quitado o nuevo, y otro esquema de CT-06: la comparación lo detecta |
| `test_t143_el_estado_propio_de_ct23_a_ct25_es_el_del_codigo` | Campo y valores de `CAMPO_ESTADO` y `ESTADOS_ESPECIFICOS`, en el JSON del Anexo B y en el derivado |
| `test_t143_las_claves_de_los_retornos_del_motor_son_las_del_anexo_b` | Con el Motor de verdad: servido, caché, rechazo y re-ejecución dan exactamente las claves del Anexo B; `clase_cifra` y `coincide` en su lista |
| `test_t143_lo_que_el_anexo_b_ya_describe_vuelve_a_diferir_si_el_ejecutor_cambia` (8 mutantes) | Sobre los mensajes capturados: pieza sin `indice`, encargo sin `tipo_pronostico`, petición sin `evidencias`, fase nueva, `escalado` sin plazo, estado propio en `estado` (CT-23 y CT-24), `paquete_auditoria` sin `entregables`: cada uno da una diferencia |
| `test_t143_un_campo_que_el_anexo_b_vuelve_a_exigir_y_el_ejecutor_no_da_una_diferencia` (5) | Si el Anexo B volviera a exigir un campo que el ejecutor no exige (`opp_id` de CT-24, `urgencia` de CT-25, `fecha_objetivo` de CT-01, `respuestas` de CT-23, `escalado` de CT-03), la diferencia vuelve |
| `test_t143_las_divergencias_que_quedan` | El golden: solo CT-18, CT-20 y CT-21 sin campos |
| `test_t143_la_v52_es_la_v51_con_el_anexo_b_corregido` | Un solo Documento 0 en `01_Gobernanza`; la V5.1 `.md` y `.docx` en el histórico; fuera del Anexo B solo cambian las cuatro líneas de cabecera y una fila del Anexo F; `version_contrato` «5.1» |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_t143_la_v52_es_la_v51_con_el_anexo_b_corregido`; `diff` V5.1 → V5.2 (solo líneas 3, 6–8, el Anexo B y una del Anexo F) |
| CA-2 | `test_t143_la_v52_es_la_v51_con_el_anexo_b_corregido`; `sha256sum` de la V5.1 movida = hashes del manifiesto anterior (`26691b68…`, `7e708a03…`) |
| CA-3 | `test_t143_las_divergencias_que_quedan`, `test_ca1_cada_golden_coincide_byte_a_byte` |
| CA-4 | pruebas actualizadas y `test_t143_*` (mutantes) |
| CA-5 | `cmp aceptaciones_rechazos.json` con la copia previa (igual); `goldens_ct.py` → «coinciden»; línea nueva en `REGISTRO.md`; `test_h01_la_bateria_cubre…` |
| CA-6 | `tools/refs_vivas.py` (en verde; antes de corregir los prompts fallaba con las dos rutas V5.1) |
| CA-7 | `tools/corpus_integridad.py` (696 archivos); `git diff -U0 tools/corpus_manifest.txt` (6 rutas, ver análisis) |
| CA-8 | `borrador_anexo_b.py --comprobar` → 0; el diff del borrador solo cambia niveles de título y la línea de estado (citada) |
| CA-9 | revisión de `docs/incidencias.md` (INC-T114-01 ronda T-143, INC-T143-01) y de `Decisiones_del_operador_Bloque_A.md`; `test_ca7_el_tipo_de_ct22…` lee INC-T114-01 |
| CA-10 | suite completa de A, cuotas, gates |

## Regresiones

- Las pruebas que fijaban divergencias se comprobaron contra lo que había: con los esquemas derivados V5.1 el golden tenía 23 + 14 + 4 diferencias (copia en `.docs/diseno/bloque_a/divergencias_anexo_b_v51.json`); con los V5.2, ninguna. Los mutantes de `test_t143_*` reintroducen cada tipo de diferencia (campo exigido, campo emitido, estado en otro campo, `oneOf`, esquema de respuesta, claves del Motor) y la prueba la detecta.
- Primera ejecución del módulo tras escribir las pruebas: 124 en verde y 1 fallo propio (`test_t143_las_claves…` usaba una ficha sin casos de control); corregido eligiendo una ficha servible con casos.

## Gate y cuotas

- La suite completa se pasó antes de la corrección de redacción del Anexo B (solo cambia una frase del Documento 0 y su huella); después se repitieron `test_fase3_goldens.py`, `test_t142_cadena_b.py` y `test_t126_pb26_pb48.py` (las que leen el Documento 0): 168 pasadas, y `check_all.sh --core` vuelve a pasar la suite de A.

- `tools/refs_vivas.py`, `tools/secrets_scan.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py`: en verde.
- ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l`): 2831 (cuota 2831; las líneas de `test_fase3_goldens.py` y `contratos.py` no cambian: 1 antes y 1 después).
- mypy de A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l`): 109 (cuota 109).
- `./tools/check_all.sh --core`: TODOS LOS GATES PASARON (8/8: corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas, pytest A 6580, A-Forex 68, B 176); con el Documento 0 ya corregido. El gate completo (12/12, con ruff y mypy) no se ejecutó entero: ruff (2831) y mypy de A (109) se midieron aparte con los mismos comandos que usa.

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_fase3_goldens.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider
cd ../..
.venv/bin/python .docs/scripts/borrador_anexo_b.py --comprobar
.docs/scripts/pruebas_scripts.sh
.venv/bin/python .docs/scripts/prueba_refs_vivas.py
for s in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$s.py; done
./tools/check_all.sh --core
```

## Ronda r02 (QA r01 NO APTO)

| Suite | r01 | r02 |
| --- | --- | --- |
| `tests/test_fase3_goldens.py` | 125 | 150 (25 nuevas `test_t143_r02_*`), todas en verde |
| Suite completa del Bloque A | 6580 pasadas, 2 omitidas | 6605 pasadas, 2 omitidas (37 min) |
| `goldens_ct.py` | coinciden | coinciden, tras el re-congelado r02 (`huellas.json`, `mensajes_ejemplo.json`) |
| `.docs/scripts/pruebas_scripts.sh` | 203 | 203 |
| `prueba_refs_vivas.py` | 25/25 | 25/25 |
| `borrador_anexo_b.py --comprobar` | 0 | 0 |
| Gates ligeros (`refs_vivas`, `secrets_scan`, `nfc_check`, `corpus_integridad`) | en verde | en verde (corpus 696) |
| ruff / mypy de A | 2831 / 109 | 2831 / 109 (cuotas 2831 / 109) |
| `./tools/check_all.sh --core` | 8/8 | 8/8 (corpus 696, NFC, YAML, secretos, refs vivas, pytest A 6605, A-Forex 68, B 176) |

### Scripts del revisor, con lo que dan en la r02

- `r01_02_bateria_y_corpus.py 1ccffd5`: **0 fallos** (batería igual, `aceptaciones_rechazos.json` idéntico, manifiesto con las seis rutas, Documento 0 fuera del Anexo B solo con la cabecera y la fila del Anexo F).
- `r01_01_anexo_b_contra_codigo.py`: **5 «HALLAZGO» y luego termina con `IndexError`**. El script compara frases del texto de la r01 y mide el código, que no cambia:
  - «el Anexo B dice que un CT-04 sin los cuatro bloques se rechaza» sale como hallazgo porque esa frase ya no está;
  - «CT-04 con solo `aprobar_certificados` … lo admite» mide el código, que lo admite como dice ahora el Anexo B (lo fija `test_t143_r02_ct04_con_solo_aprobar_certificados_no_se_rechaza`); la línea siguiente da OK («el Anexo B nombra `aprobar_certificados`»);
  - «CT-03 con `consulta --sin-escalado` … le falta `estado_run`» mide el código; el Anexo B dice ahora «`estado_run` solo si se ejecutó el análisis» (`test_t143_r02_ct03_sin_ejecutar_el_analisis_no_lleva_estado_run`);
  - las dos de CT-09 (la frase «obligatoria siempre» y el Motor que sirve sin `fecha_corte`): la frase ya no está y el Anexo B dice lo que hace el Motor (`test_t143_r02_ct09_sin_fecha_corte_el_motor_sirve_y_el_anexo_b_lo_dice`);
  - `ct06_prosa_de_los_anidados` falla con `IndexError` porque busca «`cribado`, por candidata,», que se sustituyó por la frase fija de los anidados. Lo que medía (señal, cálculos y puntuaciones, `evidencia_citada`) lo comparan ahora con `ESQUEMAS` `test_t143_los_retornos_internos_…` y `test_t143_r02_un_cambio_en_los_valores_o_en_los_anidados_se_nota`.

  El script necesita una versión r02 anclada al texto nuevo; no la escribo (es del revisor).
- `r01_03_mutantes.py <carpeta fuera del repo>` (20 mutantes, re-congelando cada uno):

| Mutante | r01 | r02 |
| --- | --- | --- |
| C01, C03 a C06, C08, D01, D02, D07 y D08 | mueren | mueren |
| C09 | muere | muere |
| C02 (veredicto nuevo en el código) | sobrevive | **muere** (`test_t143_los_retornos_internos_…`) |
| C07 (PROFUNDIZACION en N0/N1) | sobrevive | **muere** (`test_t143_r02_cada_fase_de_ct06_…`) |
| D04 (CT-25 exige `urgencia`) | sobrevive | **muere** (`test_t143_r02_lo_que_el_derivado_no_exige_…`) |
| D05 (sin REVISION_VIGENTES) | sobrevive | **muere** (`test_t143_r02_las_listas_de_la_prosa_…`) |
| D10 (`clase_cifra` MIXTA) | sobrevive | **muere** (`test_t143_r02_las_listas_de_la_prosa_…`) |
| D03, D06 y D09 | sobreviven | **no aplican**: su texto de anclaje cambió en la r02; sus equivalentes sobre el texto nuevo están en `test_fase3_goldens.py` y mueren («D03 CT-01» en `test_t143_r02_quitar_una_marca_de_opcional_se_nota`; «D06 la prosa vuelve a poner evidencia» y «D09 la prosa admite APTO» en `test_t143_r02_un_cambio_en_los_valores_o_en_los_anidados_se_nota`) |
| C10 (un campo de más en el encargo de CT-06) | sobrevive | sobrevive, como esperaba el revisor («?»): el 6.2.3 admite campos de más, no es una diferencia |

  El script termina con 1 porque cuenta como fallo los tres que no aplican.

### Criterio → prueba (r02)

| Criterio | Prueba |
| --- | --- |
| H-01 | `test_t143_r02_ct04_con_solo_aprobar_certificados_no_se_rechaza`; mutante «CT-04» de `test_t143_r02_quitar_una_marca_de_opcional_se_nota` |
| H-02 | `test_t143_los_retornos_internos_…` (CT-15 con `REDACCION` y `SINTESIS`); mutantes «REDACCION con rutas» y «CT-15 sin REDACCION» |
| H-03 | `test_t143_los_retornos_internos_…` (anidados); `test_t143_r02_ct03_…`; mutantes «cribado con señal», «evidencia_citada exigida», «la ficha sin premortem» |
| H-04 | `test_t143_r02_ct09_sin_fecha_corte_…` |
| H-05 | las `test_t143_r02_*` y los mutantes de arriba |
| H-06 | `grep -n "subordinado al Documento 0" bloque_a/11_Ejecutor/config/por_defecto.yaml` → V5.2; CLAUDE.md, sin tocar (ver el análisis) |

## Ronda r03 (QA r02 NO APTO)

| Suite | r02 | r03 |
| --- | --- | --- |
| `tests/test_fase3_goldens.py` | 150 | 173 (23 casos nuevos: 12 mutantes de valores y anidados, 4 de marcas de opcional, la prueba de `memoria` y sus 5 mutantes, y el mutante «CT-04» renombrado), todas en verde tras el re-congelado |
| Suite completa del Bloque A | 6605 pasadas, 2 omitidas | 6628 pasadas, 2 omitidas (68 min, con los mutantes en paralelo) |
| `goldens_ct.py` | coinciden | coinciden, tras el re-congelado r03 (`huellas.json`, `mensajes_ejemplo.json`) |
| `.docs/scripts/pruebas_scripts.sh` | 203 | 203 |
| `prueba_refs_vivas.py` | 25/25 | 25/25 |
| `borrador_anexo_b.py --comprobar` | 0 | 0 |
| Gates ligeros | en verde | en verde (corpus 696) |
| ruff / mypy de A | 2831 / 109 | 2831 / 109 (un primer intento dio 2832 por un caso duplicado en un `parametrize`, PT014; corregido) |
| `./tools/check_all.sh --core` | 8/8 | 8/8 (corpus 696, NFC, YAML, secretos, refs vivas, pytest A, A-Forex 68, B 176) |

### Scripts del revisor (r02_*), con lo que dan en la r03

- `r02_03_prosa_en_memoria.py`: sin mutar, ninguna comprobación ve diferencias. **P01, P02, P05, P06, P07 y P08 DETECTADOS** (P01, P02 y P07 por la marca de opcional que ahora acompaña al campo; P05 y P06 por las frases fijas; P08 por `query_id`, que ya no se excluye). P03 y P04 **no aplican**: su texto de anclaje cambió (`tipo_opcion` lleva ahora sus valores; `memoria` ya no lleva la lista entre paréntesis). Sus equivalentes sobre el texto nuevo están en `test_fase3_goldens.py` y se detectan: «P03 tipo_opcion con otros valores» y «D23 la prosa cambia la memoria del ciclo».
- `r02_02_mutantes.py` (25 mutantes, en dos mitades): **mueren 24**. Entre ellos, los que en la r02 sobrevivían: C12 (AUDITORIA), C13 (`tipo_opcion` nuevo), C18 y C19 (`memoria` de CT-05), D20 (CT-15 rutas y legibilidad) y D21 (CT-14 APTO). C21 muere tras re-congelar por una prueba (`test_ca7_el_tipo_de_ct22…`, con `-x` la primera que falla, porque el flujo de decisión queda vacío; también fallan `test_t143_r02_cada_fase_de_ct06_…` y `test_h01_los_flujos_cubren_…`), no por un `IndexError`. **D23 no aplica** (su anclaje «`memoria` (OPP- vigentes, …)» ya no está); el script termina con 1 por ese.
- `r02_01_anexo_b_contra_codigo.py`: **1 «HALLAZGO» y después `AttributeError`**:
  - el hallazgo pide frases para los anidados de la ficha con su notación (`INFORME_CLASE.finalistas[].ambito`, y lo mismo bajo `REVISION_VIGENTES.exploratorias[]`), y el Anexo B los describe con «En `FINALISTA`, `ambito` lleva …», como dice su introducción («La ficha de cada finalista de CT-06 es la de `FINALISTA` … y sus campos anidados se describen igual, con «En `FINALISTA`, …»»);
  - el `AttributeError` sale en `comprueba_ct05`: busca «`memoria` (…)», que la r03 sustituyó por una frase por tipo. Lo que medía lo mide ahora `test_t143_r03_la_memoria_de_cada_orden_ct05_es_la_del_anexo_b` con las órdenes reales (las de los flujos y la de INTEGRACION por un espía de `_invocar`).

  No escribo una versión r03 del script: es del revisor.

### Criterio → prueba (r03)

| Criterio | Prueba |
| --- | --- |
| H-07 | `test_t143_r03_la_memoria_de_cada_orden_ct05_es_la_del_anexo_b`, `test_t143_r03_un_cambio_en_la_memoria_se_nota` (C18, C19, D23), frase fija de V6 en CT-05 |
| H-08 | `test_t143_los_retornos_internos_…` (la ficha por dentro, con clave `FINALISTA`) y los mutantes «C13 tipo_opcion nuevo», «una región menos», «ambito exige un campo más», «P03 …», «horizontes_aplicables sin valores», «la ficha sin tendencia» |
| H-09 | `test_t143_los_retornos_internos_…` (CT-17 con `AUDITORIA`); mutantes «C12 …», «una severidad nueva», «CT-17 sin AUDITORIA» |
| H-10 | revisión del texto frente a `_peticion_conocimiento`; C20 de `r02_02` muere (BUSQUEDA exige `afirmacion`) |
| H-11 a | `test_t143_r02_quitar_una_marca_de_opcional_se_nota` con P01, P02, P07 y P08 |
| H-11 b | frases fijas y prohibidas; mutantes «D20 …», «D21 …», «P06 …» |
| H-11 c | `capturar_flujos` sin `IndexError`; C21 muere por prueba |

## Ronda r04 (QA r03 NO APTO)

| Suite | r03 | r04 |
| --- | --- | --- |
| `tests/test_fase3_goldens.py` | 173 | 180 (7 casos nuevos `test_t143_r04_*`; el espía corre ahora tres ciclos cortos), todas en verde tras el re-congelado |
| Suite completa del Bloque A | 6628 pasadas, 2 omitidas | 6635 pasadas, 2 omitidas (51 min, con los mutantes en paralelo); `test_t102_filtro::test_r05_h37_sufijo_en_tiempo_lineal` pasó |
| `goldens_ct.py` | coinciden | coinciden, tras el re-congelado r04 (solo `huellas.json`) |
| `borrador_anexo_b.py --comprobar` | 0 | 0 |
| Gates ligeros | en verde | en verde (corpus 696) |
| ruff / mypy de A | 2831 / 109 | 2831 / 109 (un primer recuento dio 2834 por tres ISC004 en `FRASES_FIJAS`; corregidos con paréntesis) |
| `./tools/check_all.sh --core` | 8/8 | 8/8 (corpus 696, NFC, YAML, secretos, refs vivas, pytest A 6635, A-Forex 68, B 176; relanzado una vez tras el reinicio del contenedor) |

### Scripts del revisor (r03_*), con lo que dan en la r04

- `r03_02_mutantes.py <carpeta fuera del repo>` (14 mutantes): **mueren 13**, entre ellos los cuatro que en la r03 sobrevivían: C28 y C29 (por `test_t143_r04_lo_que_el_ejecutor_lee_…` y `test_t143_r04_de_cada_hallazgo_…`), D30 y D31 (por las frases fijas de CT-07). **D29 no aplica**: su anclaje es la frase de la r03 que H-12 corrige. Su equivalente es la frase prohibida «la integración la calcula el código» y la frase fija nueva de CT-05, y quitar la nota del V6 lo detecta `_esquemas_de_respuesta_que_difieren`. El script termina con 1 por ese.
- D12 de `r02_02` tampoco aplica (la frase nueva de CT-15 cambia su anclaje); su versión adaptada, D12b de `r04_03_mutantes_adaptados.py`, muere, como D29b.
- `r03_01_anexo_b_contra_codigo.py`: **3 «HALLAZGO»**. Ya no marca CT-11, `objeto` de `AUDITORIA` ni las tres primeras referencias (H-13 y H-14). Las tres líneas que quedan:
  - las dos de CT-05 salen de su anclaje a la frase de la r03, «En el diseño V6 no hay orden INTEGRACION»: la primera da por hallazgo que el V6 por defecto no tenga orden INTEGRACION, que es lo que dice el Anexo B; la segunda dice que el Anexo B lo afirma «sin condición», y el texto nuevo lo condiciona a `v6.sintetizador` y cuenta el caso con `false`;
  - la de CT-17 en el V6 es el falso positivo que la propia QA r03 señaló: el Auditor del V6 se muestrea por run.

  Lo que miden lo fijan ahora `test_t143_r04_lo_que_cambia_en_el_v6_…` (con los tres ciclos) y las frases fijas.

### Criterio → prueba (r04)

| Criterio | Prueba |
| --- | --- |
| H-12 | `test_t143_r04_lo_que_cambia_en_el_v6_es_lo_que_dice_el_anexo_b` (V6 sin INTEGRACION y con `SINTESIS`; V6 sin Sintetizador con INTEGRACION y `REDACCION`), frases fijas y prohibidas de CT-05, `test_t143_r03_la_memoria_…` |
| H-13 | la misma prueba (V5 con CURACION; V6 sin CURACION ni DICTAMEN_G3) y las frases fijas de CT-11 y CT-14 |
| H-14 | `test_t143_r04_de_cada_hallazgo_el_ejecutor_toma_objeto` (C29), `test_t143_r04_lo_que_el_ejecutor_lee_de_cada_referencia_…` (la cuarta referencia no cuenta) |
| H-15 | `test_t143_r04_lo_que_el_ejecutor_lee_de_cada_referencia_…` (C28, D31) y `test_t143_r04_un_cambio_en_esas_frases_se_nota` (D30, D31) |

## Ronda de cierre (QA r04 APTO con H-16 a H-18)

Copia nueva sobre `origin/develop` (`c728c91`) con `git merge --no-ff --no-commit 238ef4d` (sin conflictos) y `qa.md` y `revisores/` de `6336cdc`; sin la instantánea `0b09071` (H-18). Por orden de la coordinación no se pasan la suite completa de A ni `check_all.sh`: se hará al integrar.

| Comprobación | Resultado |
| --- | --- |
| `tests/test_fase3_goldens.py` | **192 pasadas** (180 + 6 `test_t143_r04b_dictamen_g3_del_v6` + 6 `test_t143_r04b_curacion_por_nivel_y_diseno`), 125 s |
| `goldens_ct.py` | coinciden (sin re-congelado: esta ronda no cambia goldens) |
| `tools/corpus_integridad.py` | 696 archivos íntegros (sin re-congelado) |
| Gates ligeros (`refs_vivas`, `secrets_scan`, `nfc_check`, YAML) y `borrador_anexo_b.py --comprobar` | en verde, 0 |
| ruff / mypy de A | 2813 / 109, las cuotas de `develop` (los tres `.py` del diff, con 0 hallazgos de ruff, como en `develop`; un primer recuento dio 2814 por un I001 en los imports de la prueba nueva, corregido) |

### Mutantes de `r04_02` (H-16), en una carpeta nueva

`r04_02_mutantes.py <carpeta nueva>` → **mueren los 8**; termina con 0:

| Mutante | Lo mata |
| --- | --- |
| E01 (el V6 pide el dictamen sin `dictamen_g3_llm`) | `test_t143_r04b_dictamen_g3_del_v6[V6-…]` |
| E02 (el V6 no cura ni con `curacion_llm`) | `test_t143_r04b_curacion_por_nivel_y_diseno[V6 con curacion_llm-N2]` |
| E03 (curación también en N1) | `test_t143_r04b_curacion_por_nivel_y_diseno[V5-N1]` |
| E04, E05, F03 | como en la r04 |
| F01 (sin la frase de la integración del V6), F02 (sin la condición del Sintetizador) | las frases fijas nuevas de CT-15 (`test_t143_los_retornos_internos_…`) |

### Criterio → prueba (cierre)

| Criterio | Prueba |
| --- | --- |
| H-16 a | `test_t143_r04b_dictamen_g3_del_v6`; fuera la aserción vacía `("CT-14", "DICTAMEN_G3") not in v6` |
| H-16 b | `test_t143_r04b_curacion_por_nivel_y_diseno` |
| H-16 c | `FRASES_FIJAS["CT-15"]` con las dos frases; las comprueban `test_t143_r04_lo_que_cambia_en_el_v6_…` y `test_t143_los_retornos_internos_…` |
| H-17 | el párrafo de D12 en «Ronda r04» |
| H-18 | `git diff --name-status origin/develop` sin `.venv` ni la deuda técnica |
