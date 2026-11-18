# T-187 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `.docs/scripts/pruebas_revision_prompts_pb51.py` (antes `test_revision_prompts.py` en el ticket) | 70 (pasos 1 y 2) · 87 (r01) | 105 en verde (103 sintéticas y 2 de regresión sobre el corpus real) |
| `.docs/scripts/mutantes_revision_prompts_pb51.py` (antes `mutantes_pb51.py`) | 41 · 63 (r01) | 78 de 78 muertos, ninguno equivalente |
| `bloque_a/11_Ejecutor/tests/test_t187_pb51.py` | — · 5 (r01) | 6 en verde (PB-51 en el mapa del plan, «Superada en parte») |
| `.docs/scripts/pruebas_scripts.sh` | línea base 231 | 336 pasadas, línea base subida a 336 |
| Suites de los ejecutores | A 607 | A: una prueba nueva (`test_t187_pb51.py`); no se toca ningún `.py` de los paquetes |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_anexo_g_*`, `test_estructura_completa_y_titulos_coherentes`, `test_titulos_en_mayusculas_y_plurales_coinciden`, `test_titulo_sin_palabra_comun_es_variante_pero_no_rompe_la_estructura`, `test_falta_una_seccion`, `test_seccion_repetida_sobrante_o_desordenada`, `test_titulos_dentro_de_un_bloque_de_codigo_no_son_secciones`, `test_la_seccion_acaba_en_un_titulo_de_nivel_1` |
| CA-2 | `test_subareas_*`, `test_preambulo_antes_de_la_primera_subarea`, `test_elementos_*`, `test_definicion`, `test_formulas`, `test_umbrales`, `test_trampas_por_titulo_y_por_texto`, `test_recuento_por_subarea_con_inventario_excluido`, `test_recuento_sin_seccion_10` |
| CA-3 | `test_citas_*`, `test_entradas_de_la_lista_y_autores_heredados`, `test_entrada_de_tabla_por_celdas`, `test_entrada_con_iniciales_e_institucion`, `test_referencias_estricto_y_amplio`, `test_sin_lista_de_referencias`, `test_estructura_del_doi`, `test_identificadores_en_texto`, `test_isbn` |
| CA-4 | `test_tamano_con_tope_propio_con_tope_de_analista_y_sin_tope` |
| CA-5 | `test_frases_con_abreviaturas_codigo_e_iniciales`, `test_marcas`, `test_candidatas_*`, `test_muestra_determinista_de_tamano_fijo_y_ordenada`, `test_de_punta_a_punta_y_comprobar` |
| CA-6 | `test_de_punta_a_punta_y_comprobar`, `test_determinista_entre_ejecuciones`, `test_falla_cerrado_*`, `test_corpus_real_lo_generado_coincide_con_lo_guardado` |
| CA-7 | `mutantes_pb51.py` |
| CA-8 | INC-T187-01 en `docs/incidencias.md` (revisión documental) |
| CA-9 | `test_contraste_recuentos_por_lote_por_prompt_y_totales`, `test_contraste_umbral_en_el_limite_y_no_verificables_fuera_del_denominador`, `test_contraste_falla_cerrado_con_ids_o_veredictos_que_no_casan` (faltan, sobran, desconocido, duplicado), `test_contraste_falla_cerrado_con_un_id_repetido_entre_lotes`, `test_contraste_nota_de_40_palabras_vale_y_de_41_o_vacia_falla`, `test_contraste_falla_cerrado_si_el_comentario_no_casa`, `test_leer_lotes_falla_cerrado_sin_lotes_o_con_formato_malo`, `test_de_punta_a_punta_con_veredictos_y_fallo_cerrado`, `test_corpus_real_el_contraste_supera_el_criterio`; `bloque_a/11_Ejecutor/tests/test_t187_pb51.py`; INC-T187-02 e INC-T187-03 (revisión documental); PB-51 «Superada» en `docs/evidencias_pruebas_bloque_a.md` |

## Regresiones

Cada comprobación del script tiene su mutante en `mutantes_pb51.py` (M01 a M41: orden, repetidas, faltan, coherencia de títulos, código, Anexo G mal numerado, bis, inventario, rutas, «=» del texto, comparadores en palabras, paréntesis de la definición, trampas por texto, las tres formas de cita, partículas, falsos autores, criterio amplio, instrucciones en las listas, autores heredados, tablas, DOI, ISBN, ISSN, abreviaturas, código en frases, semilla por archivo, orden y tamaño de la muestra, secciones de la muestra, referencias fuera de la muestra, frases sin marca, tamaño del analista, comparación con el tope, los tres fallos cerrados, `--comprobar`, veredicto vacío y plantilla). Los 41 hacen fallar alguna prueba. Paso 3 (M42 a M63): ids que faltan y que sobran, veredicto desconocido, duplicado, nota en el límite de 40, sin límite y vacía, no verificables en el denominador, 95 % exacto, sin verificables, erratas frente a ERRONEA, errata sin corrección, dudosa no CORRECTA, discutible no ERRONEA, las dos sensibilidades, recuento por lote y por prompt, salida 2 con veredictos no válidos, sin lotes, orden de los lotes y escape de las barras en el informe. Los 63 hacen fallar alguna prueba (M37 se reescribió tras sacar la lectura de las entradas a `revisar`).

## Gate

Gate ligero en la copia de trabajo (18-11-2026), con el `.venv` del proyecto: `tools/corpus_integridad.py` (705 archivos coinciden), `tools/nfc_check.py`, `tools/secrets_scan.py` y `tools/refs_vivas.py` en verde; ruff de los ejecutores 2 807, igual a la cuota (no se toca ningún `.py` de los paquetes). Los tres archivos `.py` del ticket pasan `ruff check` y el script pasa `mypy`. Las suites de los ejecutores no se ejecutaron: no cambia su código.

### Gate del paso 3 (18-11-2026)

- `./tools/check_all.sh --core` en verde (8/8): corpus íntegro (705 archivos), nombres NFC, YAML, secretos, refs vivas y las tres suites (A 8 272 pasadas, A-Forex 68, B 176; ninguna por debajo de su línea base).
- `ruff check` de los tres `.py` del ticket y de `bloque_a/11_Ejecutor/tests/test_t187_pb51.py`: sin hallazgos; `mypy` del script: sin errores. Ningún `.py` de los paquetes cambia: cuotas de `tools/cuotas.txt` sin tocar (ruff 2 807, mypy A 102).
- `.docs/scripts/evidencias_plan_a.py --ejecutar`: 301 de 301 pruebas citadas superadas; PB-51 «Superada» (40 Superada, 19 Superada en parte, 7 Pendiente API, 1 Requiere usuarios).
- `mutantes_pb51.py`: 63 de 63 muertos.
- `./tools/check_all.sh` completo en verde (12/12): además ruff y mypy ×3 dentro de sus cuotas, sin subirlas.

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Prueba de regresión |
| --- | --- |
| H-01 | `test_t187_pb51.py::test_pb51_fila_del_mapa_superada_en_parte`; `revisores/r01_04` (H-01) en verde; evidencias: PB-51 «Superada en parte» |
| H-02 | `test_contraste_cuenta_verificables_por_prompt_y_lista_los_cortos`; `test_corpus_real_el_contraste_supera_el_criterio` (28 cortos, mínimo 2); `r01_04` (H-02) |
| H-03 | `test_contraste_falla_cerrado_si_la_cita_no_esta_en_la_nota`, `test_contraste_dudosas_exactamente_las_correctas_con_matiz` y los casos nuevos de `test_contraste_falla_cerrado_si_el_comentario_no_casa` (discutible sin apoyo en la nota, discutibles que no son ids, sensibilidad); `r01_04` (H-03) |
| H-04 | `test_contraste_cuenta_veredictos_por_fuente` («sin búsqueda web» como memoria, «Web:» como búsqueda) |
| H-05 | `test_entradas_que_no_se_pueden_leer_salen_con_2_sin_traza` (UTF-8 inválido en un lote y en el comentario, un lote o el comentario que son carpetas), `test_contraste_nota_de_40_palabras_vale_y_de_41_vacia_o_sin_letras_falla` («—», «  »), revisor en blanco o «—» en `test_leer_lotes_falla_cerrado_sin_lotes_o_con_formato_malo`, veredicto lista; `r01_03` 10 de 10 (copia con la ruta nueva, ver `analisis-tecnico.md`) |
| H-06 | `pruebas_scripts.sh` con la línea base 336 en verde; `test_t187_pb51.py` carga el script de `.docs/scripts/` |
| H-07 | `test_de_punta_a_punta_con_veredictos_y_fallo_cerrado` (título «## Paso 3 · Muestra», sin «sin juzgar»); `--comprobar` y la regresión del corpus real tras regenerar |
| (M01) | `test_desordenada_sin_faltar_sobrar_ni_repetir_no_es_completa` |

Mutantes M64 a M78: cita frente a la nota, criterio de los dudosos, discutible sin apoyo, discutibles que no son ids, sensibilidad que no es ERRONEA o sin motivo, texto sin letras, lectura con UTF-8 inválido o carpeta, revisor en blanco, lista de los cortos, verificables con las NO_VERIFICABLE, «sin búsqueda web» como búsqueda, «Web:», dudoso sin matiz y el título «sin juzgar». Todos muertos.

Scripts de la QA r01: `r01_01_recuento.py` (260/9/81, igual), `r01_02_muestreo.py` (sin errores), `r01_03_ataques_contraste.py` (10 de 10 con la copia de ruta nueva) y `r01_04_comprobaciones_cierre.py` («las tres comprobaciones pasan»).

Gate de la r02: `./tools/check_all.sh` completo en verde (12/12): corpus íntegro (705), NFC, YAML, secretos, refs vivas (con las tres rutas viejas en `tools/refs_allowlist.txt`), ruff 2807 y mypy 102/174/159 (iguales a sus cuotas), A 8 273, A-Forex 68 y B 176. `.docs/scripts/pruebas_scripts.sh`: 336 (línea base 336). `evidencias_plan_a.py --ejecutar`: 302 de 302 superadas; PB-51 «Superada en parte» (39 Superada, 20 Superada en parte).

## Ronda de cierre de la QA r02

| Hallazgo | Prueba de regresión |
| --- | --- |
| H-08 | `tools/refs_vivas.py` en verde sin las rutas viejas en la allowlist; `grep -c T-187 tools/refs_allowlist.txt` = 0 |
| H-09 | `test_contraste_falla_cerrado_con_una_cita_de_menos_de_tres_palabras` («a», « de », «es de» y «Año erróneo:» dan 2; con 3 palabras vale; también en los dudosos); la columna «Cita de la nota» en `test_contraste_recuentos_por_lote_por_prompt_y_totales`; mutantes M79 a M81; `revisores/r02_01` 16 de 16 |

`pruebas_revision_prompts_pb51.py`: 106 pasadas. `pruebas_scripts.sh`: línea base de 336 a 337. Scripts de la QA: `r01_01` (260/9/81), `r01_02`, `r01_03` (10 de 10), `r01_04` («las tres comprobaciones pasan») y `r02_01` (16 de 16).

Gate de la ronda de cierre: `./tools/check_all.sh` completo en verde (12/12), con refs vivas sin rutas de T-187 en la allowlist; ruff 2807 y mypy 102/174/159 iguales a sus cuotas; A 8 273, A-Forex 68 y B 176. Mutantes: 81 de 81 muertos. Evidencias: 302 de 302 superadas, PB-51 «Superada en parte».
