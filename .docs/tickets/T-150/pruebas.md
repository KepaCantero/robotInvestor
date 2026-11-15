# T-150 · Pruebas

Copia: git worktree `t150` (HEAD `0e08a7d`) con `.venv` enlazado, sin red ni coste. Comandos desde `bloque_a/11_Ejecutor` salvo que se diga otra cosa.

| Suite | Antes | Después |
| --- | --- | --- |
| Suite completa de A (`../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6444 passed, 2 skipped (QA r01 de T-149) | **6520 passed, 2 skipped** en 28 min 26 s, exit 0 (con los mutantes corriendo a la vez en otra copia). +76: 74 de `test_t150.py` tal como estaba al lanzarla y 2 de `test_t149.py`. Después se añadieron 5 casos a `test_h05_un_precio_con_paso_grande_…` (semillas concretas, para matar F4): `test_t150.py` da ahora 79 passed |
| `tests/test_t150.py` (nuevo) | — | 79 passed |
| `tests/test_t149.py` | 77 passed, 2 skipped | 79 passed, 2 skipped |
| `tests/test_t144.py` | 35 | 35 (cambia `_hueco_de_la_cota`, abajo) |
| Vecinas: `test_t150`, `t149`, `t147`, `t144`, `t142_cadena_b`, `t141_datos_bce`, `t135_motor` | — | 357 passed, 2 skipped (61 s; antes de los 5 casos de F4) |
| `.docs/scripts/pruebas_scripts.sh` | 194 | 194 (línea base 194) |

## Criterio de aceptación → prueba

| Criterio | Prueba y resultado |
| --- | --- |
| CA-1 (H-01) | `test_t150.py::test_h01_dos_datos_pegados_no_dejan_rastro` (20 pares × 4 plantillas), `…el_correo_pegado_a_la_clave_era_el_caso_de_la_qa`, `…tramos_que_se_solapan_o_se_tocan…`, `…un_texto_corriente_no_cambia…`, y el límite O-03 fijado en `…lo_que_el_detector_no_ve_pegado_tampoco_se_quita`. Revisor `r01_03_r8_y_g3_qa.py`: R1 **OK** (queda el OBS de O-03) |
| CA-2 (H-02) | `test_h02_el_stderr_se_limpia_antes_de_recortarlo` (5 datos, el corte en cada posición), `…la_salida_que_no_es_json…`. Revisor: R4 **OK** |
| CA-3 (H-03) | `test_t149.py::test_t150_el_mensaje_de_jsonschema_se_limpia_antes_de_recortarlo` (relleno 150–199), `…el_script_limpia_el_fallo_de_un_ejecutor_que_imprime`. `r01_02_mutantes_qa.py <copia «t147_mut»>`: **N21 y N27 muertos; 0 vivos** (exit 0; N25, N31 y N32 equivalentes, como dijo el revisor) |
| CA-4 (H-04) | `test_h04_un_opp_id_con_un_correo_no_llega_al_resumen_ni_a_la_salida`, `…el_resumen_entero_pasa_por_la_limpieza`. Revisor: R3 **OK** |
| CA-5 (H-05, O-01) | `test_h05_una_copia_truncada_es_una_copia` (8 vías, amplitud `null` sin identificadores), `…antes_no_se_agrupaba…`, `…un_precio_con_paso_grande_no_quita_la_hipotesis_al_resto` (6), `…series_distintas_truncadas_no_son_copias` (5 rejillas × 40 semillas × 3 pares: 0), `…un_paso_grande_frente_al_precio_no_se_desplaza`, `…pares_por_hipotesis`, `…limites_declarados_no_se_agrupan` (redondeo hacia arriba; tabla por tramos como MiFID II). Revisor `r01_01_rejillas_qa.py`: **0 hallazgos** (antes 2; los 4 OBS son límites declarados, entre ellos las dos tablas por tramo, nombradas ahora en INC-T127-01). `medir_truncado.py --semillas 300`: copias truncadas no agrupadas **0** en todo (antes 296–300 de 300 frente a la original), falsos positivos **0** (antes también 0). `T-149/medir_copias.py --semillas 300`: idéntico a antes salvo tres casillas del límite declarado de los fondos (1/8 a 12: 183 → 196 y 285 → 287; 1/32 a 2: 283 → 284) |
| CA-6 (H-06, O-05) | `test_h06_una_fila_sin_fecha…` (2), `…una_lectura_cortada…` (IncompleteRead, BadStatusLine, RemoteDisconnected), `test_o05_un_traslado_a_medias_dice_que_csv_quedaron`, `…el_primer_traslado_que_falla…`, `…un_destino_que_es_un_enlace_roto…` (2), `test_h06_una_respuesta_valida…`. Revisor `r01_04_bce_qa.py`: **0 hallazgos** (antes 1); el OBS del enlace roto desaparece; queda el de la falta de atomicidad entre ficheros (declarado), con un mensaje que ya nombra los CSV escritos |
| CA-7 (O-04, O-06) | `test_o04_un_paquete_que_no_se_lee…` (no existe, no es JSON, lista, texto con un correo), `test_o06_un_config_a_que_no_se_lee…` (6), `…el_yaml_roto_da_la_posicion_y_no_la_linea`. Revisor: el OBS de G2 (paquete inexistente con traza) desaparece; R5 OK |
| CA-8 | `.docs/tickets/T-150/mutantes.py <copia>`: **22 de 22 muertos**. `T-147/mutantes.py <copia>`: **37 de 37**. `T-147/revisores/r01_03_mutantes_qa.py --ticket T-144`: Q08–Q11 muertos; `--ticket T-147`: Q01–Q07 muertos. Otros revisores: `T-144/r01_01_copias_otras_rejillas.py` 0 hallazgos, `T-135/r01_01` 39 ok y `r01_02` 24 ok, `T-147/r01_01` y `r01_02` 0 hallazgos. Cadena real con los dos ejecutores simulados (`cadena_a_b.py --sonda-sin-correspondencia`): código 0, ENTREGADA, G3 APTO, 3 enviables, 1 entregada y válida, 1 vuelta, sonda ADMITIDA. Suite completa y gates, arriba y abajo |

## Regresiones

En una copia desechable («t147_mut»), con cada fichero corregido vuelto a su versión de HEAD por separado y las pruebas nuevas: `frontera_b.py` → fallan 9 (todas las copias truncadas salvo la de 2 decimales frente a 0,05, el paso grande por precio y `_pares_por_hipotesis`); `cadena_b.py` → 8 (seis pares pegados, el caso de la QA y los tramos); `cadena_a_b.py` → 21 (todas las de H-02, H-04, O-04 y O-06); `descargar_datos_bce.py` → 7 (sin fecha, lecturas cortadas salvo `RemoteDisconnected`, que ya era `OSError`, traslado a medias y enlace roto). Pasan en HEAD, como deben, los controles (falsos positivos, monetario, límites declarados, respuesta válida, primer traslado que falla, O-03) y las dos de H-03 (fijan lo que el código ya hacía; matan N21 y N27). `test_t144.py::test_t149_la_cota_de_niveles_…` fallaba con el código nuevo y la ayuda de T-149: con la hipótesis truncada el hueco mínimo es un 0,6 % menor; se calcula ahora el menor de los cuatro (`analisis-tecnico.md`) y sigue matando Q08 y Q09.

## Gates y cuotas (desde la raíz)

| Gate | Resultado |
| --- | --- |
| `tools/refs_vivas.py` | todas las rutas citadas existen |
| `tools/secrets_scan.py` | sin hallazgos |
| `tools/nfc_check.py` | en forma canónica |
| `tools/corpus_integridad.py` | 695 archivos coinciden |
| ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2838 (cuota 2838; los ficheros tocados, sin avisos) |
| mypy de A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 (cuota 109) |

`./tools/check_all.sh` entero no se ejecutó: A-Forex y B no se tocan y la suite de A se ejecutó una vez, aparte. `descargar_datos_bce.py` trae de antes un RUF100 (un `noqa: S310` sin uso) fuera de las cuotas; no se toca.

## Comandos

- `../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t150.py tests/test_t149.py tests/test_t147.py tests/test_t144.py tests/test_t142_cadena_b.py tests/test_t141_datos_bce.py tests/test_t135_motor.py`
- Desde la raíz: `.venv/bin/python -I .docs/tickets/T-149/revisores/r01_01_rejillas_qa.py`; `… r01_03_r8_y_g3_qa.py <tmp>`; `… r01_04_bce_qa.py <tmp>`; `.venv/bin/python .docs/tickets/T-149/revisores/r01_02_mutantes_qa.py <copia «t147_mut»>`; `.venv/bin/python .docs/tickets/T-150/mutantes.py <copia>`; `.venv/bin/python .docs/tickets/T-147/mutantes.py <copia>`; `.venv/bin/python .docs/tickets/T-147/revisores/r01_03_mutantes_qa.py <copia> --ticket T-144|T-147`; `.venv/bin/python -I .docs/tickets/T-150/medir_truncado.py --semillas 300 [--modulo <frontera_b.py de HEAD>]`; `.venv/bin/python -I .docs/tickets/T-149/medir_copias.py --semillas 300 [--modulo …]`.
- La copia desechable se hizo con `tar` desde la copia de trabajo (sin `.git` ni `.venv`) y se borró al acabar.
