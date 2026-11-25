# T-149 · Pruebas

Copia: git worktree `t149` con `.venv` enlazado, sin red ni coste. Comandos desde `bloque_a/11_Ejecutor` salvo que se diga otra cosa.

| Suite | Antes | Después |
| --- | --- | --- |
| Suite completa de A (`../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6338 passed (QA r01 de T-144 y T-147, HEAD `f197bc5`) | **6428 passed, 2 skipped** en 22 min 8 s, exit 0 (+90: 77 + 2 omitidas de `test_t149.py`, 2 de `test_t144.py`, 11 de `test_t147.py`). Se lanzó con la vía de cifras significativas a factor 1,9; con el 2,3 de ahora, `test_t149.py` vuelve a dar 77 passed, 2 skipped |
| `tests/test_t149.py` (nuevo) | — | 77 passed, 2 skipped (1/8 y 0,25 a 12: paso del 1 % del precio o más, límite declarado) |
| `tests/test_t144.py` | 33 | 35 |
| `tests/test_t147.py` | 96 | 107 |
| Vecinas: `test_t149`, `t144`, `t147`, `t142_cadena_b`, `t141_datos_bce`, `t135_motor`, `t127_hallazgos`, `t127_r02`, `t128_frontera`, `t128_r02`, `test_fase3_goldens` | — | 497 passed, 2 skipped (146 s) |
| `tests/goldens_ct.py` | coinciden | coinciden |

## Criterio de aceptación → prueba

| Criterio | Prueba y resultado |
| --- | --- |
| CA-1 | `test_t149.py::test_h01_la_misma_serie_en_otra_rejilla_es_una_copia` (14 vías: 0,05, 0,25, 0,02, 0,025, 1/8, 1/16, 1/32, 1/128, pasos de 5 y 50, un precio y tres precios sin redondear, 4 cifras significativas cruzando 100, 0,05 con una sesión ausente; amplitud `null` sin identificadores), `test_h01_paso_de_cada_rejilla`, `…un_precio_suelto…`, `…la_fraccion_en_rejilla…`, `…paso_por_decada…`, `…series_distintas_en_otras_rejillas_no_son_copias` (100 semillas × 0,05, 0,25, 1/8, 1/32 × niveles 100 y 12: 0), `…limites_declarados_no_se_agrupan`; `test_t144.py::test_h01_series_distintas_muy_correladas_no_son_copias` sigue en 0. Revisor: `.venv/bin/python -I .docs/tickets/T-144/revisores/r01_01_copias_otras_rejillas.py` → **0 hallazgos** (antes 5); `T-135/revisores/r01_01_copias_idx_conc.py` 39 ok, `r01_02_aviso_firmas.py` 24 ok. Medida de 300 semillas en `analisis-tecnico.md` (`.docs/tickets/T-149/medir_copias.py`) |
| CA-2 | `test_t144.py::test_t149_la_cota_de_niveles_es_el_redondeo_de_las_dos_mas_dos_tolerancias` y `…en_el_borde_exacto_de_la_cota_es_copia`. `r01_03_mutantes_qa.py <copia «t147_mut»> --ticket T-144`: **Q08, Q09, Q10 y Q11 muertos, 0 vivos** |
| CA-3 | `test_t149.py::test_h01_un_campo_enumerado_…` (5 campos × correo, clave e IBAN), `…tipos_secundarios_…`, `…la_configuracion_…` (nivel, prioridad, perfil, idioma × 3 datos × con y sin exigir correspondencia), `…el_simbolo_sin_correspondencia_…`, `…sin_datos_protegidos`, `…el_script_no_escribe_ni_imprime_…`, `…el_script_no_imprime_un_dato_de_la_correspondencia`. Revisor: `T-147/revisores/r01_01_r8_y_peticion.py` → **0 hallazgos** (C2 a C5 en verde; los 4 OBS son los límites de INC-T123-01) |
| CA-4 | `test_t149.py::test_h02_*` (fecha repetida sin ceros y con el mismo texto; una fecha sin ceros sola es válida; destino fichero y dentro de un fichero, sin descargar; un CSV de destino que es una carpeta; un `OSError` al escribir, sin carpeta temporal). Revisor: `T-147/revisores/r01_02_bce_y_clases.py <tmp>` → **0 hallazgos** (2 OBS que ya traía); `T-141/revisores/r03_respuestas_raras.py`: normal 0 y 6 CSV, raras 1 y 0 CSV |
| CA-5 | `test_t147.py::test_t149_*` (clave genérica 15/16 caracteres, dominio de una letra y de dos, fechas «11/12/2026» y «20261112», la sonda con un correo). `r01_03_mutantes_qa.py <copia> --ticket T-147`: **Q01 a Q07 muertos, 0 vivos** |
| CA-6 | `test_t149.py::test_g3_un_paquete_sin_entrega_no_se_encarga` (sin `estado_g3`, BLOQUEADO, SIN_RESULTADO, «apto»; con y sin exigir correspondencia), `…un_paquete_entregado_si` (APTO y APTO_CON_ADVERTENCIAS), `…los_estados_son_los_de_la_entrega_ct02` (los de `contratos.py` y del esquema), `…el_script_no_envia_nada_sin_entrega` (bloqueo en F6 sin entregables, en F7 con el borrador del paquete, SIN_RESULTADO: código 1, `sin_envio`, una sola llamada al Bloque A, ninguna petición ni CT-04). De punta a punta con los dos ejecutores simulados: `cadena_a_b.py --sonda-sin-correspondencia` → entrega ENTREGADA, G3 APTO, 1 entregada y válida, sonda ADMITIDA; `T-142/revisores/r02_cadena_doce_tipos.sh` → código 0, 30 enviables, 2 entregadas válidas con su RET (lo mismo que la QA de T-147) |
| CA-7 | `.venv/bin/python .docs/tickets/T-147/mutantes.py <copia «t147_mut»>` por grupos: T-147 16 de 16, T-144 8 de 8, T-148 8 de 8 muertos. `T-142/revisores/r01_ataques_peticion.py`: 36 OK · 4 OBS (como antes). Suite completa y gates, abajo |

## Regresiones

Copia desechable con el código de HEAD (`frontera_b.py`, `cadena_b.py`, `cadena_a_b.py`, `descargar_datos_bce.py`) y las pruebas nuevas: fallan 66 (todas las de rejillas, paso, fracción y década; todas las de los detalles sin el dato; las del BCE con fecha sin ceros, destino y fallo al escribir; todas las de G3; `test_t144.py::test_h01_paso_de_precio`). Pasan en HEAD, como deben, los controles (la fecha repetida con el mismo texto, una fecha sin ceros sola, APTO y APTO_CON_ADVERTENCIAS) y las pruebas que solo matan mutantes (Q02–Q07 y Q08–Q10 fijan lo que ya hacía el código). La vía de cifras significativas se eligió para que falle sin `_paso_por_decada` (la serie cruza 100; con el factor 1,9 no lo cruzaba y pasaba también sin la corrección).

## Gates y cuotas (desde la raíz)

| Gate | Resultado |
| --- | --- |
| `tools/refs_vivas.py` | todas las rutas citadas existen; `.docs/scripts/prueba_refs_vivas.py` 25/25 |
| `tools/secrets_scan.py` | sin hallazgos |
| `tools/nfc_check.py` | en forma canónica |
| `tools/corpus_integridad.py` | 695 archivos coinciden |
| ruff (`… bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2838 (cuota 2838; los ficheros tocados, sin avisos) |
| mypy de A (`… bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 (cuota 109) |

`./tools/check_all.sh` entero no se ejecutó: B no se toca y la suite de A se ejecutó una vez, aparte.
