# T-65 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `bloque_a/11_Ejecutor` (pytest) | 201 pasan (165 s) | **265 pasan** (176 s): +40 en `tests/test_t65_hallazgos.py` y +24 en `tests/test_t65_resto_t53.py`; dos pruebas de T-53 adaptadas (abajo) |
| `.docs/scripts/prueba_refs_vivas.py` | no existía (con el `tools/refs_vivas.py` anterior, 4/6) | 6/6 |
| `.docs/tickets/T-65/mutaciones.py` | — | 39/39 mutaciones detectadas |
| ruff (tres ejecutores) | 3102 (cuota 3109) | 3083 |
| mypy `bloque_a` | 123 (cuota 123) | 123 |
| `bloque_a_forex`, `bloque_b` | 68 y 174 | sin tocar (en el gate) |

### Tras la QA r03

| Suite | 8d74622 (r03) | Ahora (r04) |
| --- | --- | --- |
| `bloque_a/11_Ejecutor` (pytest) | 300 pasan | **317 pasan** (+17 en `tests/test_t65_qa_r03.py`) |
| `tests/test_t65_qa_r03.py` con el código de 8d74622 | — | 12 fallan y 5 pasan: los 3 controles con datos sanos y las 2 de H-19, que cubren partes que ya estaban y se comprueban con su mutación |
| `.docs/scripts/prueba_refs_vivas.py` | 15/15 | **25/25** (con el script de 8d74622, 19/25) |
| `.docs/tickets/T-65/mutaciones.py` | 57/57 | **67/67** (10 nuevas, «r03»; se rehicieron las de «H-15 fechas duplicadas», «r01 H-01 valor_en» y «r02 H-14» porque el código que mutaban se movió) |
| Sondas de la QA | r03_01 a r03_04 con hallazgos | Con 0 hallazgos: r03_01 (0 INFO), r03_02 (5 INFO, todos los que la QA ya daba por correctos), r03_03 (0 INFO), r02_02, r02_03, r01_02, r01_04 y r01_06. r03_04: detecta las 2 mutaciones que aplica; la tercera ya no casa con el código, y la cubre la mutación «r03 H-19 sin las referencias de las vigentes». **Cambios esperados por H-21:** r01_01 marca 2 «hallazgos» (parte C, «dup»: la línea duplicada es la última del archivo, 2026-10-30, posterior a la fecha as_of) y r02_01 marca 1 («B/desordenado_y_duplicado»: la fecha repetida es de 2023-01-05, fuera de todas las ventanas). Las dos sondas se escribieron cuando HT-01 validaba el archivo entero y esperan que se rechace. Con H-21, que pedía la r03, un dato malo que no se usa ya no excluye el símbolo |
| ruff (tres ejecutores) · mypy `bloque_a` | 3083 · 123 | 3083 · 123 |

### Tras la QA r02

| Suite | 052e79a (r02) | Ahora (r03) |
| --- | --- | --- |
| `bloque_a/11_Ejecutor` (pytest) | 285 pasan | **300 pasan** (+15 en `tests/test_t65_qa_r02.py`) |
| `tests/test_t65_qa_r02.py` con el código de 052e79a | — | Fallan las 11 pruebas que había al probar contra ese commit. Pasa solo el control con datos sanos (`test_r02_h12_referencia_sana_no_cambia_nada`). Las 4 de motivo explícito (`test_r02_h13_motivo_explicito_de_cada_forma_rara`) se añadieron después y se comprueban con mutaciones |
| `.docs/scripts/prueba_refs_vivas.py` | 8/8 | **15/15** (con el script de 052e79a, 11/15) |
| `.docs/tickets/T-65/mutaciones.py` | 50/50 | **57/57** (7 nuevas, «r02») |
| Sondas de la QA r02_03 · r02_02 | H-12 y H-13: caía el ciclo · 2 INFO | r02_03: HALLAZGOS: 0 · r02_02: HALLAZGOS: 0 · INFO: 0 (también r02_01: 0 hallazgos y 43 OK; r01_01, r01_04 y r01_06: 0) |
| ruff (tres ejecutores) · mypy `bloque_a` | 3083 · 123 | 3083 · 123 |

Sobre las mutaciones:

- **Mutantes equivalentes.** Con el envoltorio de H-13, tres mutaciones anteriores pasaban la suite: «H-15 fechas duplicadas», «H-15 CSV con fechas ilegibles» y la nueva «r02 H-13 columnas duplicadas aceptadas». Quitar el control explícito ya no tumba el ciclo, porque el envoltorio convierte el error en `DatosInvalidos`, pero sí cambia el motivo declarado.
- **Prueba nueva.** `test_r02_h13_motivo_explicito_de_cada_forma_rara` exige el motivo propio de cada forma (no «datos no normalizables»). Las tres mutaciones apuntan ahora a ella y fallan.

### Tras la QA r01

| Suite | b699d4f (r01) | Ahora (r02) |
| --- | --- | --- |
| `bloque_a/11_Ejecutor` (pytest) | 265 pasan | **285 pasan** (+20 en `tests/test_t65_qa_r01.py`) |
| `tests/test_t65_qa_r01.py` con el código de b699d4f | — | 15 fallan y 5 pasan: los 5 son los casos de H-04 que ya se rechazaban y las pruebas de efecto de H-08, que se comprueban con mutaciones |
| `.docs/scripts/prueba_refs_vivas.py` | 6/6 | 8/8 (con el script de b699d4f, 7/8: falla «argumento roto de una orden falla») |
| `.docs/tickets/T-65/mutaciones.py` | 39/39 | **50/50** (11 nuevas, con prefijo «r01») |
| Sondas de la QA `r01_04_cierre_malo_antiguo.py` y `r01_01_datos_raros.py` | con hallazgos: H-01; H-02 y la parte D (H-07) | «HALLAZGOS: 0» en r01_04, y «HALLAZGOS: 0 · INFO: 0» en r01_01: parte D sin rechazo y parte E PARCIAL, sin caer |
| ruff (tres ejecutores) | 3083 | 3083 |
| mypy `bloque_a` | 123 | 123 |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 · cada corrección con una prueba que falla sin ella | Las 39 mutaciones de `mutaciones.py` (tabla de abajo) y `prueba_refs_vivas.py` contra el script anterior (falla en 2 de 6 casos) |
| CA-2 · los puntos ya hechos citan su prueba y pasa | H-06: `test_t66_propuestas.py::test_h06_todo_pausado_no_redacta_ni_falla_en_el_esquema`. H-12: `test_t53_seleccion_y_entrega.py::test_h12_dos_bloques_con_la_misma_configuracion_no_comparten_la_tabla_de_horizontes`. Las dos pasan en la suite de 265 |
| CA-3 · lo no hecho, con motivo y destino | Tabla del `README.md` (CS-10 P-07 → T-57; CS-11, 44 parámetros en F10 → T-83 y T-57; CS-18, ρ del prompt → revisión del corpus; CS-08, promoción → revisión del corpus) y límites de `analisis-tecnico.md` |
| CA-4 · ningún número nuevo en el código; los del operador `[PROPUESTO]` | `test_cs10_todas_las_claves_leidas_existen_en_por_defecto` (las 64 rutas leídas con `parametro()` existen en el YAML), `test_h08_*`, `test_h09_*` (7 incidencias marcadas junto a su clave) |
| CA-5 · suite en verde y por encima de 201; gate 12/12 | 265 pasan; gate abajo |
| CA-6 · sin tocar lo prohibido ni el corpus | `git status`: solo `bloque_a/11_Ejecutor/`, `.docs/tickets/T-65/`, `.docs/scripts/prueba_refs_vivas.py` y `tools/refs_vivas.py` (ver la nota de H-11). Gate `corpus-integridad` en verde |

## Regresiones

### Ronda r04 (hallazgos de la QA r03)

Las pruebas fallan con el código de 8d74622 (copia `git worktree add --detach` de 8d74622 más el archivo de pruebas nuevo, ya retirada) o con su mutación, de prefijo «r03»:

| Hallazgo | Prueba | Con 8d74622 | Mutación |
| --- | --- | --- | --- |
| H-16 | `test_r03_h16_referencia_parada_deja_fuera_los_tipos_que_la_usan`, `…_la_frescura_de_la_referencia_sale_de_la_configuracion`, `…_no_se_resuelve_con_una_serie_parada` (ACWI y SPY), `…_un_miembro_parado_de_la_cesta_no_cuenta` y el control `…_con_las_dos_series_al_dia_se_resuelve` | Fallan las 5 primeras; el control pasa | Sin frescura · `max` en la resolución · tolerancia fija · miembro parado: fallan |
| H-17 | `test_r03_h17_subyacente_sin_archivo_se_declara_y_no_se_cambia_por_la_cesta` y el control `…_columna_vacia_sigue_siendo_la_cesta` | Falla la primera | Subyacente ausente → CESTA: falla |
| H-18 | `test_r03_h18_vigente_con_subyacente_malo_excluye_solo_su_indicador` | Falla | Vigente SUBYACENTE como referencia del tipo: falla |
| H-19 | `test_r03_h19_la_referencia_guardada_en_una_vigente_se_valida`, `…_una_fuga_de_informacion_en_la_referencia_corta` | Pasan (ya estaba) | Sin las referencias de las vigentes · fuga absorbida: fallan |
| H-20 | `test_r03_h20_cabecera_repetida_es_dato_invalido` (3 cabeceras) | Fallan las 3 | Cabecera repetida aceptada: falla |
| H-21 | `test_r03_h21_un_dato_malo_posterior_a_as_of_no_excluye_el_simbolo`, `…_un_dato_malo_fuera_de_la_ventana_no_importa` y el control `…_una_fecha_repetida_en_el_rango_sigue_siendo_invalida` | Fallan las 2 primeras | Validación del archivo entero: falla |
| H-22 | `prueba_refs_vivas.py`: `python3 -I`, `-X utf8`, comillas con espacios, `python3.12`, `pytest`, corchetes literales | Fallan esos 6 casos | — |
| H-23 | lectura de `docs/incidencias.md` (INC-T65-01) y del README del ejecutor | — | — |

### Ronda r03 (hallazgos de la QA r02)

Las pruebas fallan con el código de 052e79a (copia `git worktree add --detach` de 052e79a más el archivo de pruebas nuevo, ya retirada) o con su mutación, de prefijo «r02»:

| Hallazgo | Prueba | Con 052e79a | Mutación |
| --- | --- | --- | --- |
| H-12 | `test_r02_h12_referencia_mala_degrada_solo_los_tipos_que_la_usan` (ACWI con cierre 0, binaria y ausente; ciclo de RV, IDX y DIV) y `test_r02_h12_subyacente_malo_excluye_solo_su_indicador` | Fallan las 4: el ciclo caía y el subyacente no se miraba | Referencia sin validar · sin incidencia · subyacente sin validar: fallan |
| H-13 | `test_r02_h13_csv_raro_es_dato_invalido_del_simbolo` (Close y Adj Close, fechas con zona, `fecha_publicacion` con zona), `test_r02_h13_cualquier_error_de_la_normalizacion_es_dato_invalido` y `test_r02_h13_motivo_explicito_de_cada_forma_rara` | Fallan las 4 primeras | Columnas duplicadas aceptadas · zona aceptada · normalización sin envolver: fallan |
| H-14 | `test_r02_h14_cierre_booleano_se_rechaza` (True y False) | Fallan las 2 | Booleanos aceptados: falla |
| H-15 | `prueba_refs_vivas.py`: comodín que casa, archivo de salida, script roto detrás de un intérprete y argumento roto entre comillas | Fallan esos 4 casos | — |

### Ronda r02 (hallazgos de la QA r01)

Cada prueba falla con el código de b699d4f, en una copia (`git worktree add --detach` en b699d4f más el archivo de pruebas nuevo), o con su mutación en `mutaciones.py` (prefijo «r01»):

| Hallazgo | Prueba | Con b699d4f | Mutación |
| --- | --- | --- | --- |
| H-01 | `test_r01_h01_cierre_malo_fuera_de_la_ventana_no_vacia_el_tipo` (0 y −1), `test_r01_h01_valor_en_valida_solo_el_cierre_que_devuelve`, `test_r01_h01_un_precio_invalido_excluye_y_declara_el_simbolo` | fallan las 4 | `valor_en` valida toda la historia · precio inválido en silencio: fallan |
| H-02 | `test_r01_h02_csv_ilegible_falla_cerrado_por_simbolo` (vacío, binario, UTF-16) | fallan las 3 | lectura sin capturar: falla |
| H-03 | gate `refs-vivas` en una copia limpia | 11/12 | — |
| H-04 | `test_r01_h04_festivo_fijo_con_formato_no_estricto_se_rechaza` | fallan `" 1-25"` y `"١٢-٢٥"` (los otros 3 ya se rechazaban) | «MM-DD» laxo: falla |
| H-05 | `test_r01_h05_frecuencias_y_presupuestos_sin_respaldo_en_el_codigo`, `test_r01_h05_textos_con_los_dias_de_la_configuracion` | fallan | respaldo 7 · «10 días» fijo: fallan |
| H-06 | `prueba_refs_vivas.py`, «argumento roto de una orden falla» | falla | — |
| H-07 | `test_r01_h07_dos_proxies_sin_solape_no_tumban_los_clusteres` | falla | sin mirar el solape: falla |
| H-08 | `test_r01_h08_pregunta_repetida_…`, `test_r01_h08_recalibracion_de_rk_…`, `test_r01_h08_ps1_…` | pasan las dos primeras (b699d4f ya leía la configuración); PS1 falla (no había `_ps1`) | 3 fijo · paso 0,05 fijo · 2 raíces fijas: fallan las tres (con b699d4f, las dos primeras pasaban la suite entera) |
| H-11 | `test_r01_h11_limitacion_de_la_tasa_base_con_coma_decimal` | falla | punto decimal: falla |

Las comprueba `python3 .docs/tickets/T-65/mutaciones.py`. El script quita cada corrección (sustituye el texto en el archivo), ejecuta su prueba y restaura el archivo comprobando su huella. Resultado: **39/39 FALLA** (todas detectadas).

| Punto | Mutación (se quita la corrección) | Prueba que falla |
| --- | --- | --- |
| H-07 | El Evaluador usa la tabla del módulo · la síntesis usa la función del módulo | `test_h07_dos_evaluadores_con_tablas_distintas_no_se_pisan`, `test_h07_la_sintesis_usa_la_tabla_de_su_bloque` |
| H-08 | Literal 65 en el siguiente paso · una clave nula se acepta | `test_h08_umbrales_de_presentacion_sin_respaldo_en_el_codigo`, `test_h08_un_parametro_que_falta_en_todas_partes_falla_cerrado` |
| H-09 | Sin `[PROPUESTO]` en INC-T53-03 | `test_h09_incidencias_marcadas_propuesto_junto_a_su_clave` |
| H-10 | `estado_g3` en memoria · carpeta antigua del C6 · `DatosInvalidos` como «sin datos» | `test_h10a_…`, `test_h10b_…`, `test_h10c_…` |
| H-13 | `efecto_desde` = as_of + 1 | `test_h13_la_degradacion_registra_el_efecto_desde_el_mismo_ciclo` |
| H-14 | El rechazo de la ficha no se anota | `test_h14_una_ficha_rechazada_por_el_motor_se_declara` |
| H-15 | Cierres ≤ 0 aceptados · duplicadas como `ValueError` · sin el `except` genérico · fechas ilegibles sin capturar | `test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara`, `test_h15_cualquier_error_del_proveedor_para_un_simbolo_se_declara`, `test_h15_csv_con_fechas_ilegibles_se_excluye_y_se_declara` |
| H-16 | Todos los proxies a ML-CLUS-001 | `test_h16_un_finalista_con_poca_historia_no_desactiva_los_clusteres` |
| H-17 | Sin validación · sin lunes de Pascua | `test_h17_ps2_festivos_mal_formado_impide_crear_el_bloque`, `test_h17_lunes_de_pascua_configurable_y_propuesto_desactivado` |
| H-20 | Un contenedor que no es lista es «sin objeciones» | `test_h20_contenedor_mal_formado_cuenta_como_fuerte_abierta` |
| H-21 | Se sanea el texto propio · una incidencia por cita · sin `run_id` | `test_h21_texto_propio_del_analista_llega_intacto`, `test_h21_lo_externo_se_sanea_con_run_id_y_una_incidencia_por_fuente` |
| CA-14 | 21 sesiones por mes fijas · tasa base 0,5 · zona ±5 % · umbral C6 del 5 % | `test_ca14_*` (4) |
| CA-15 | Un solo contador de `msg_id` · `participantes` sin ordenar | `test_ca15_*` (2) |
| CS-08 | Sin fichas «Documentado» · alternativa no servible | `test_cs08_*` (2) |
| CS-10 | 200 réplicas · 2 celdas · falta `ps1` en el YAML | `test_cs10_*` (3) |
| CS-11 | Clave oculta `_parametros_ht03` · YAML distinto del corpus · regímenes incompletos · P-30 «4.0» | `test_cs11_*` (4) |
| CS-18 | Ventana de «2 años + 14 días» | `test_cs18_la_ventana_de_clusteres_sale_de_la_configuracion` |
| CS-19 | Sin la fila de PB-56 en el mapa | `test_cs19_mapa_cubre_las_67_pruebas_del_plan` |
| CS-23 | Cita de `test_herramientas.py` | `test_cs23_herramientas_cita_una_prueba_que_existe` |
| H-11 | `tools/refs_vivas.py` anterior (`git show HEAD:tools/refs_vivas.py`) | `prueba_refs_vivas.py`: fallan «revisores/ con una ruta rota falla» y «orden con argumentos viva» |

**Pruebas existentes adaptadas** (comprobaban el comportamiento que se corrige):

- `test_t53_evaluacion_y_almacen.py::test_bandas_desde_configuracion_y_validadas`. Esperaba que crear un `Evaluador` cambiara la tabla del módulo, que es justo el defecto H-07. Ahora comprueba la tabla de la instancia, que la del módulo no cambia y que una tabla inválida falla al validar y al crear el Evaluador.
- `test_t53_seleccion_y_entrega.py::test_h01_historia_corta_tambien_queda_declarada`. Esperaba «clústeres de exposición no calculados» para todos. Con H-16 se declara solo el proxy corto («sin medir para USDNEW=X»), y el run sigue PARCIAL.

## Gate

Comando: `.docs/scripts/gate.sh` con `--completo` (llama a `./tools/check_all.sh`).

**Ronda r01 (commit b699d4f).** En el árbol de trabajo dio 12/12, pero la QA lo repitió desde una copia limpia y dio 11/12: `refs-vivas` fallaba porque este `pruebas.md` citaba con forma de ruta un log local, que no se sube (H-03). La cita se ha quitado: los logs se nombran solo por su archivo, sin ruta.

**Ronda r04: 12/12 en verde desde una copia limpia** (2026-11-10, log gate_20261110_163540.log, que no se sube). La copia es un `git worktree add --detach` de HEAD (b7dc4d1, que contiene 8d74622) en el scratchpad, con los archivos de T-65 sin commit y un enlace a `.venv`; después se quitó con `git worktree remove`.

| Gate | Resultado |
| --- | --- |
| corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas | ✓ |
| ruff (hallazgos) | ✓ (3083 ≤ 3109) |
| mypy bloque_a · bloque_a_forex · bloque_b | ✓ (123 · 174 · 159) |
| pytest bloque_a · bloque_a_forex · bloque_b | ✓ 317 · 68 · 174 passed |

**Ronda r03: 12/12 en verde desde una copia limpia** (2026-11-10, log gate_20261110_152104.log, que no se sube). La copia es un `git worktree add --detach` de HEAD (bc1ee45, que contiene 052e79a) en el scratchpad, con los archivos de T-65 sin commit y un enlace a `.venv`; después se quitó con `git worktree remove`. `tools/refs_vivas.py` se repitió en la copia con los documentos finales, y pasa.

| Gate | Resultado |
| --- | --- |
| corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas | ✓ |
| ruff (hallazgos) | ✓ (3083 ≤ 3109) |
| mypy bloque_a · bloque_a_forex · bloque_b | ✓ (123 · 174 · 159) |
| pytest bloque_a · bloque_a_forex · bloque_b | ✓ 300 · 68 · 174 passed |

**Ronda r02: 12/12 en verde desde una copia limpia** (2026-11-10, log gate_20261110_143201.log, que no se sube). La copia es un `git worktree add --detach` de HEAD (c482bf1, que contiene b699d4f) en el scratchpad, con los archivos de T-65 sin commit y un enlace a `.venv`. Se repitió `tools/refs_vivas.py` en la copia con los documentos finales del ticket, y pasa.

| Gate | Resultado |
| --- | --- |
| corpus-integridad, nombres-nfc, yaml-configs, secrets | ✓ |
| refs-vivas | ✓ |
| ruff (hallazgos) | ✓ (3083 ≤ 3109) |
| mypy bloque_a · bloque_a_forex · bloque_b | ✓ (123 · 174 · 159) |
| pytest bloque_a | ✓ 285 passed |
| pytest bloque_a_forex | ✓ 68 passed |
| pytest bloque_b | ✓ 174 passed |

Además: `python3 tools/refs_vivas.py` pasa, y ya no excluye las carpetas `revisores/`. Con el script anterior, el gate `refs-vivas` fallaba por una cita de otro ticket en curso (`.docs/scripts/gate.sh --completo` en `.docs/tickets/T-80/analisis-tecnico.md`); con el arreglo de H-11, esa cita cuenta como viva.

## Comandos usados

Ronda r02 (además de los de abajo):

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider                         # 285
../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r01_04_cierre_malo_antiguo.py                       # HALLAZGOS: 0
../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r01_01_datos_raros.py                              # HALLAZGOS: 0 · INFO: 0
cd ../.. && python3 .docs/tickets/T-65/mutaciones.py                                                          # 50/50
python3 .docs/scripts/prueba_refs_vivas.py                                                                    # 8/8
# copia limpia para el gate: worktree de HEAD + los archivos de T-65 + enlace a .venv; dentro, gate.sh con --completo
```

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider      # 201 antes · 265 después
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t65_hallazgos.py tests/test_t65_resto_t53.py
cd ../.. && python3 .docs/tickets/T-65/mutaciones.py                                     # 39/39
python3 .docs/scripts/prueba_refs_vivas.py                                               # 6/6
git show HEAD:tools/refs_vivas.py > /tmp/viejo.py && python3 .docs/scripts/prueba_refs_vivas.py /tmp/viejo.py   # 4/6
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
.docs/scripts/gate.sh --completo
```
