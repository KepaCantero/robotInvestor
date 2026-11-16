# T-161 · Pruebas

Todo con el cliente simulado (`MockClient`): sin red, sin clave y sin coste. Copia de trabajo: worktree con la instantánea `b825452` en HEAD y los cambios de T-161 sin commit.

## Recuento

| Suite | Antes (HEAD) | Después |
| --- | --- | --- |
| `tests/test_t161_guias.py` | 0 | 130 |
| `tests/test_t158_guias.py` | 55 | 55 (dos preparaciones de PB-48 simulan el fallo del emisor; ninguna aserción cambia) |
| `tests/test_t126_pb26_pb48.py` | 13 | 13 |
| `test_t161` + `test_t158` + `test_t126_pb26_pb48` + `test_t126_r02` + `test_fase3_goldens` + `test_fase4_mapa` | — | 333 superadas y 1 fallo (`test_fase4_mapa`, por el documento de evidencias, antes de regenerarlo; ver la fila siguiente) |
| Suite completa de A (una vez, en segundo plano, 70 min con otras suites corriendo) | 6727 superadas en la QA de T-158 (antes de T-159 y T-160) | **6876 superadas, 2 omitidas y 1 fallo**. Lanzada con 124 pruebas de T-161: las 6 últimas se pasaron después, aparte. El fallo es `test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`: el documento de evidencias aún no estaba regenerado tras cambiar el texto de PB-48 en el mapa. Después de `evidencias_plan_a.py --ejecutar`, `test_fase4_mapa.py` + `test_t161_guias.py`: **153 superadas** |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 (H-01, 50 ataques) | `test_h01_los_50_ataques_del_revisor_se_detectan` (50 casos, copia literal de `r01_01`), `test_h01_normalizacion` (8), `test_h01_otra_escritura_es_conflicto` (3), `test_h01_otra_lengua_es_conflicto` (6), `test_h01_un_verbo_de_refuerzo_con_una_condicion_que_lo_debilita_es_conflicto` (5); `r01_01_detector.py`: **0 de 50 pasan** |
| CA-2 (falsos positivos) | `test_h01_ningun_falso_positivo_con_los_ejemplos_validos_del_diseno` (**17 válidos, 0 falsos positivos**); `test_h01_falsos_positivos_aceptados_por_prudencia` (5 de frontera, aceptados); `test_h01_el_ejemplo_de_la_cli_…`; `medir_detector.py` |
| CA-3 (H-02) | `test_h02_se_revisan_los_campos_descriptivos` (7), `test_h02_un_campo_descriptivo_en_conflicto_no_llega_a_ningun_agente` (ciclo) |
| CA-4 (H-04) | `test_h04_no_se_emite_una_guia_a_un_agente_de_control` (AG-11, AG-18, AG-19), `test_h04_una_guia_de_ha_a_un_agente_de_control_no_se_aplica_y_se_escala` (3), `test_h04_la_simulacion_no_lleva_la_guia_al_refutador_en_un_ciclo`; INC-T126-01 corregida |
| CA-5 (H-03) | `test_h03_si_la_reemision_falla_el_run_siguiente_no_duplica_cor_ni_p3`, `test_h03_si_falta_el_p3_se_escribe_con_el_id_del_cor` |
| CA-6 (H-05) | `test_h05_el_emisor_rechaza_un_item_en_conflicto_y_nada_cambia`, `test_h05_la_simulacion_solo_con_el_cliente_simulado_y_queda_anotada`, `test_h05_la_cli_rechaza_la_guia_de_pb48_y_solo_la_emite_simulando_el_fallo` |
| CA-7 (H-06, H-07) | `test_h06_estados_prioridades_reglas_de_datos_y_metricas` (8), `test_h06_las_prioridades_de_la_agenda_…`, `test_h07_un_verbo_de_rebaja_sin_control_no_es_conflicto` (G08), `test_h07_la_revision_del_f0_hace_determinista_el_ciclo_con_hilos` (G09), `test_h07_la_cache_de_la_revision_es_por_run` (G22); mutantes abajo |
| CA-8 (no se rompe nada) | `test_t158_guias.py` y `test_t126_pb26_pb48.py` en verde; `evidencias_plan_a.py --pb PB-48`: **PB-48 Superada**; goldens coinciden; cuotas; suite completa |

## Regresiones

- **Las pruebas nuevas contra el código de HEAD** (copia desechable con `git archive HEAD bloque_a` y solo `test_t161_guias.py` nuevo):
  - **90 fallos y 34 superadas**, de 124 pruebas (antes de añadir las 6 últimas).
  - Fallan 43 de los 50 ataques (los mismos 43 de la QA), todas las de H-02, H-03, H-04, H-05 y H-06, las de idioma y escritura, 4 de 7 de normalización, y la de G09, porque no existe la simulación.
  - Pasan con HEAD los 17 ejemplos válidos (no había falsos positivos), los 7 ataques que HEAD ya detectaba, los casos negativos de G08 y la caché por run (G22): esas dos fijan el comportamiento correcto que ya tenía HEAD y las matan sus mutantes.
- **Mutantes del revisor** (`r01_04_mutantes.py`, sin cambiarlo; copia desechable `qa29_t161_mut`). Se ejecutan con `.docs/scripts/mutantes_revisor_ampliado.py` y las pruebas de `PRUEBAS` más `tests/test_t161_guias.py`. Resultado: **30/30 muertos**, sin vivos y sin «no aplica». En la QA r01 seguían vivos G08, G09 y G22; ahora mueren con las pruebas nuevas.
  - **G09 aplicado a mano:** `test_h07_la_revision_del_f0_hace_determinista_el_ciclo_con_hilos` falla **3 de 3** veces. La prueba fija que lo primero que envía el ciclo es la reemisión CT-18 del F0, y no depende del orden de los hilos.
- **Mutantes de las correcciones de T-161** (`.docs/tickets/T-161/mutantes_t161.py`, M01–M14): **14/14 muertos**.
  - M01 (sin NFKC) vivía en la primera pasada: NFKD ya hace la descomposición de compatibilidad.
  - Lo mata el caso añadido del subrayado de anchura completa (U+FF3F). Sin NFKC no pasa a «_» antes de unificar y «segunda＿pasada» se cuela. Se comprobó a mano: con M01, `test_h01_normalizacion` falla.

## Scripts del revisor de T-158

| Script | Resultado | Por qué |
| --- | --- | --- |
| `r01_01_detector.py` | **0 de 50** ataques pasan | H-01 y H-02 corregidos |
| `r01_02_integracion.py` | 9 superadas, 7 fallan | **Dos de PS8** (`[que_cambia]` y `[como_se_sabe]`) y la **guía a AG-18**: su condición previa («el ataque debería pasar el detector») ya no se cumple, porque el detector la ve (H-01, H-02) y AG-18 es un control (H-04). **Cuatro de fallo cerrado, idempotencia y determinismo**: emiten la guía de PB-48 sin simular el fallo del emisor y ahora `emitir` la rechaza (H-05). Con una copia del script que solo añade `simular_fallo_del_emisor=True` en `_guia_en_conflicto` (en `scratchpad`, fuera del repositorio), 3 de esas 4 pasan. La cuarta, `…duplica_cor_y_p3…`, da `(1, 1)` en lugar de los `(2, 2)` que documentaba: **H-03 corregido** |
| `r01_03_regresion_sin_guias.py` | Sin guías, **0 de 15 ficheros difieren** frente a HEAD (T-158). La CLI con la guía de PB-48 sin la opción nueva termina con «no se emite» (H-05) | Con base `607dc9e` (anterior a T-158, la que pide el script) difiere `RC_registro_calculos.jsonl`. No es de T-161: frente a HEAD no difiere nada, así que viene de los commits intermedios (T-157, T-159, T-160). Con una copia que admite la base HEAD y pasa `--simular-fallo-del-emisor` a la CLI: «CLI con la guía de PB-48: bien» (GUI-AG02-0001 SUPERSEDED, GUI-AG02-0002 ISSUED, COR-2026-0001, P3-ORQ-2026-0001 PENDING_OPERATOR) |
| `r01_04_mutantes.py` | 30/30 muertos | ver arriba |
| `r01_05_controles_del_modelo.py` | 3 fallan | Su condición previa (la guía a AG-11 o AG-19 pasa el detector y se acepta) ya no se cumple: H-04 corregido. `test_h04_la_simulacion_no_lleva_la_guia_al_refutador_en_un_ciclo` prueba el caso de extremo a extremo |

## Gate

| Comprobación | Resultado |
| --- | --- |
| ruff desde la raíz (cuota 2825) | **2821** (`guias.py`, `test_t161_guias.py` y `test_t158_guias.py` limpios; en `cli.py` se corrigieron 4 avisos que ya tenía) |
| mypy de A (cuota 109) | **109** (ninguna línea de `guias.py`; la de `cli.py:142` es anterior) |
| `tests/goldens_ct.py` | «goldens de contratos: coinciden»; ni `contratos.py` ni `tests/goldens/` cambian |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | verdes; corpus de 695 archivos |
| `evidencias_plan_a.py --pb PB-48` | PB-48 «Superada» (11 pruebas SUPERADA) |
| `evidencias_plan_a.py --ejecutar` | «196 de 196 pruebas citadas superadas». `docs/evidencias_pruebas_bloque_a.md` regenerado: solo cambian la cabecera (commit `b825452`), el texto de PB-48 y sus dos pruebas nuevas |
| `./tools/check_all.sh` completo | No se ejecuta aquí. Lo hace la sesión coordinadora al integrar, como en T-158; sus piezas ligeras y las cuotas están arriba |

## Comandos usados

Desde `bloque_a/11_Ejecutor`:

```bash
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t161_guias.py tests/test_t158_guias.py tests/test_t126_pb26_pb48.py tests/test_t126_r02.py tests/test_fase3_goldens.py tests/test_fase4_mapa.py
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python ../../.docs/tickets/T-158/revisores/r01_01_detector.py
../../.venv/bin/python ../../.docs/tickets/T-161/medir_detector.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-158/revisores/r01_02_integracion.py ../../.docs/tickets/T-158/revisores/r01_05_controles_del_modelo.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider    # suite completa, en segundo plano
```

Desde la raíz:

```bash
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
.venv/bin/python tools/refs_vivas.py; .venv/bin/python tools/secrets_scan.py; .venv/bin/python tools/nfc_check.py; .venv/bin/python tools/corpus_integridad.py
.venv/bin/python .docs/tickets/T-158/revisores/r01_03_regresion_sin_guias.py <carpeta> 607dc9e
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-158/revisores/r01_04_mutantes.py <scratchpad>/qa29_t161_mut tests/test_t161_guias.py
.venv/bin/python .docs/tickets/T-161/mutantes_t161.py <scratchpad>/qa29_t161_mut
.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-48
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
```

Las copias desechables (`qa29_t161_mut`, la copia de HEAD para las regresiones y las de los scripts del revisor) se borraron al acabar.

## Ronda r02 (QA r01 de T-161: NO APTO)

Copia: worktree con `5bbd60d` en HEAD (T-161 integrado) y los cambios de la r02 sin commit.

### Recuento

| Suite | Antes (HEAD) | Después |
| --- | --- | --- |
| `tests/test_t161_r02.py` | 0 | 193 |
| `tests/test_t161_guias.py` | 130 | 130 (`FRONTERA` pasa de 5 casos a 2, y uno cambia de familia esperada; ver `analisis-tecnico.md`) |
| `tests/test_t158_guias.py` + `test_t126_pb26_pb48.py` + `test_t126_r02.py` | 75 | 75, sin cambios |
| Suite completa de A | 6894 + 1 de tiempo (QA r01 de T-161) | **7082 superadas, 2 omitidas, 0 fallos** (una vez, en segundo plano, 1 h 40 min con los mutantes corriendo). Se lanzó con 190 pruebas de la r02; las 3 últimas (condición en un campo descriptivo, M20) se pasaron aparte |

### Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-9 (H-01) | `test_h01_ag20_es_un_agente_de_control`, `test_h01_una_guia_simulada_a_ag20_no_llega_a_su_contexto_ni_a_las_lecciones` (ciclo), `test_h01_una_leccion_de_ag20_que_rebaja_un_control_no_se_escribe_en_f6` (ciclo: la mala no llega a F6 ni a ningún contexto y deja la incidencia; la buena sí se escribe), `test_h01_conflicto_de_leccion` (4) |
| CA-10 (H-02) | `test_h02_los_68_ataques_nuevos_se_detectan` (68, copia literal), `test_h02_inyeccion_instruccion_y_marcado_en_cualquier_campo` (5), `test_h02_homoglifos_…` (5), `test_h02_los_caracteres_corrientes_…` (6), `test_h02_cifras_leidas_como_letras` (2), `test_h02_una_instruccion_repartida_retira_la_guia_entera`, `test_h02_una_orden_con_condicion_sobre_un_control_en_un_campo_descriptivo` (3) |
| CA-11 (H-03) | `test_h03_ningun_falso_positivo_con_los_40_validos_de_la_qa` (40, copia literal), `test_h03_ningun_falso_positivo_con_el_vocabulario_de_los_analistas` (39 de dominio + 4 que eran frontera), `test_h03_falso_positivo_de_dominio_aceptado`, `test_h03_las_siglas_no_son_otra_lengua_pero_la_lengua_si` (2), `test_h03_el_enmascarado_financiero_no_tapa_el_tipo_3` (4); cifras en INC-T126-01 |
| CA-12 (H-05) | `test_h05_otra_escritura_y_otra_lengua_solas_en_un_campo_descriptivo` (Q06, Q12), `test_h05_el_emisor_no_guarda_campos_ajenos_al_item` (Q02), `test_h05_longitud_maxima_…`, `test_h05_una_guia_de_ha_demasiado_larga_no_se_aplica` |

### Medida del detector (`.docs/tickets/T-161/medir_detector.py`)

| Conjunto | Antes de la r02 | Después |
| --- | --- | --- |
| 50 ataques de T-158 | 0 pasan | 0 pasan |
| 68 ataques nuevos de la QA r01 de T-161 | 57 pasan o pasan en parte | **0 pasan**. En «dos ítems: clave y orden», el ítem «Haz la segunda pasada siempre ZETA» no dice nada solo; el otro es `INSTRUCCION` y retira la guía entera |
| 17 válidos del diseño | 0 falsos positivos | 0 |
| 40 válidos genéricos de la QA | 5 | **0** |
| 40 de dominio (vocabulario de los Analistas; la QA midió 25 de 34 con los suyos) | — | **1** («escala de 1 a 5», aceptado) |
| Frontera aceptada en `test_t161_guias.py` | 5 | 2 (β, escala) |

### Regresiones (mutantes)

| Script | Resultado |
| --- | --- |
| `r01_03_mutantes.py` (Q01–Q14 del revisor) con `mutantes_revisor_ampliado.py` y `tests/test_t161_r02.py` | **14/14 muertos** (en la r01 vivían Q02, Q06 y Q12) |
| T-158 `r01_04_mutantes.py` (G01–G30) con `test_t161_guias.py` y `test_t161_r02.py` | **30/30 muertos** |
| `mutantes_t161.py` (M01–M26; M15–M26 nuevos, M04 cambiado) | 25/26 en la pasada. M20 (sin condiciones en los campos descriptivos) vivía porque las palabras de los ataques también están en `RELAJA`. Se añadió `test_h02_una_orden_con_condicion_sobre_un_control_en_un_campo_descriptivo`: con M20 aplicado a mano, 3 fallos; sin él, 3 superadas |

### Scripts del revisor

| Script | Resultado | Por qué |
| --- | --- | --- |
| `r01_01_ataques_nuevos.py` | 1 de 68 «pasa en parte»; 0 de 40 falsos positivos | El parcial es el de arriba: lo mide ítem a ítem, y el receptor retira la guía entera |
| `r01_02_integracion.py` | 11 superadas, 6 fallan | **Cuatro de PS8** (`test_ataque_nuevo_pasa_el_detector…`): su condición previa («pasa el detector») ya no se cumple, porque los cuatro ataques se detectan (H-02). **`test_guia_al_evaluador_…`**: AG-20 es un control y `emitir` rechaza la guía (H-01). **`test_determinismo_con_hilos`**: emite sin simular dos guías que ahora se rechazan. Con una copia (fuera del repositorio) que solo añade `simular_fallo_del_emisor=True` a esas dos, las huellas coinciden con 4, 4 y 1 hilos. Falla solo su última línea, que esperaba que esas dos guías se aplicaran: ahora se retiran |
| `r01_04_regresion_y_cli.py` (base `HEAD~1`) | «RESULTADO: bien» | Sin guías, ninguno de los 15 ficheros difiere; la CLI sin la opción, con el cliente real, con el reproductor y con la grabadora se rechaza; con el simulado, la huella, SUPERSEDED, 1 COR- y 1 P3- |
| T-158 `r01_01_detector.py` | 0 de 50 | |
| T-158 `r01_02` + `r01_05` | 9 superadas y 10 fallan | Son las mismas 10 de la r01, explicadas arriba |

### Gate

| Comprobación | Resultado |
| --- | --- |
| ruff desde la raíz (cuota 2821) | **2821** |
| mypy de A (cuota 109) | **109** (ninguna línea de `guias.py` ni de lo tocado en `orquestacion.py`) |
| goldens (`tests/goldens_ct.py`) | coinciden |
| `refs_vivas`, `secrets_scan`, `nfc_check`, `corpus_integridad` | verdes; corpus de 695 archivos |
| `evidencias_plan_a.py --ejecutar` tras cambiar el mapa de PB-48 | «196 de 196 pruebas citadas superadas»; `docs/evidencias_pruebas_bloque_a.md` regenerado (cabecera y `no_comprueba` de PB-48); PB-48 «Superada»; `test_fase4_mapa.py`: 23 superadas |

Copias desechables (`qa29_r02q_mut`, `qa29_r02g_mut`, `qa29_r02m_mut` y las de los scripts del revisor): borradas.

## Ronda r03 (QA r02 de T-161: NO APTO)

Copia: worktree con `e987e54` en HEAD (r02 integrada) y los cambios de la r03 sin commit.

| Suite / comprobación | Resultado |
| --- | --- |
| `tests/test_t161_r03.py` (nuevo) | 188 superadas |
| `test_t161_guias.py` + `test_t161_r02.py` + `test_t158_guias.py` + `test_t126_pb26_pb48.py` + `test_t126_r02.py` + `test_fase3_goldens.py` | 501 superadas |
| Suite completa de A (una vez, en segundo plano, 65 min con carga ≈ 11 y los mutantes corriendo) | **7364 superadas, 2 omitidas y 1 fallo**: `test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`. Se cambió el texto de PB-48 en el mapa antes de regenerar el documento. Tras `evidencias_plan_a.py --ejecutar` (204 de 204 citadas superadas), `test_fase4_mapa.py` + `test_t161_r03.py`: 211 superadas |
| `evidencias_plan_a.py --pb PB-48` | PB-48 «Superada» |
| Goldens | coinciden |
| ruff (cuota 2813) · mypy de A (cuota 109) | **2813** · **109** |
| `refs_vivas`, `secrets_scan`, `nfc_check`, `corpus_integridad` | verdes; corpus de 695 |
| Sin guías, ciclo por la CLI frente a HEAD (copia de T-158 `r01_03` que admite la base HEAD y simula el fallo del emisor) | 15 ficheros, **ninguno difiere**; «CLI con la guía de PB-48: bien» |

### Medida

| Conjunto | Antes de la r03 | Después |
| --- | --- | --- |
| 52 ataques de `r02_01` | 47 pasan | **0** |
| 68 de la r01 y 50 de T-158 | 0 · 0 | 0 · 0 |
| 48 válidos de `r02_01` | 0 falsos positivos | **0** |
| 40 válidos de la r01 · 17 del diseño · 40 de dominio | 0 · 0 · 1 | 0 · 0 · 1 («escala de 1 a 5», aceptado) |
| Lecciones prudentes: las 6 de la QA, las 4 recomendaciones deterministas del Evaluador y 10 más | 3 de 6 retenidas | **0 de 20** |
| Lecciones que rebajan un control (8) | — | 8 de 8 retenidas |

### Mutantes

| Script | Resultado |
| --- | --- |
| `r02_03_mutantes.py` (S01–S11) + `test_t161_r03.py` | 9/11 en la pasada. **S06 no aplica** porque el umbral de mayúsculas se quitó, como pidió H-10. **S04 vivía**: mis frases financieras llevaban un verbo de rebaja y ya no se enmascaraban. Se añadió `test_h10_el_enmascarado_solo_tapa_la_frase_financiera`: con S04 aplicado a mano da 3 fallos; sin él, 3 superadas |
| `r01_03_mutantes.py` (Q01–Q14) | 14/14 |
| T-158 `r01_04_mutantes.py` (G01–G30) | 30/30 |
| `mutantes_t161.py` (M01–M38) | 37/38 en la pasada. M31 (se da una lección que no está en F6) vivía porque la prueba usaba una lección no válida. Se corrigió `test_h06_una_leccion_que_no_esta_en_f6_no_se_da` para usar una válida: con M31 aplicado a mano falla; sin él pasa |

### Scripts del revisor que fallan donde medían lo viejo

| Script | Resultado | Por qué |
| --- | --- | --- |
| `r02_02_integracion.py` | 7 superadas, 9 fallan | **3 lecciones a AG-11 y 1 lección ya escrita en F6:** su condición previa no se cumple o el código ya no da la lección (H-06 corregido). **`test_falsos_positivos_de_las_lecciones`:** cuenta 6 de 6 porque sus lecciones no llevan `tipo` y ahora no son válidas; con un `tipo` válido son 0 de 6 (`test_t161_r03.py::test_h08_*`). **3 ataques de la r02 frente a PS8:** su condición previa no se cumple porque ya se detectan. **Determinismo con hilos:** emite sin simular dos guías que ahora se rechazan. Con una copia que simula el fallo, las huellas coinciden con 4, 4 y 1 hilos; solo falla su última línea, que esperaba que se aplicaran |
| `r01_02_integracion.py` (r01) · T-158 `r01_02` + `r01_05` | 6 fallan · 10 fallan | los mismos de las rondas anteriores |

Copias desechables (`qa29_r03*_mut` y las de los scripts del revisor): borradas.
