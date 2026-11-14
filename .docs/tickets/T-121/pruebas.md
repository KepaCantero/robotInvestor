# T-121 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t121_hallazgos.py` (nuevo) | — | 116 |
| `tests/test_t118_hallazgos.py` | 93 | 100 (siete nuevas para H-06; dos adaptadas para H-01 y H-05) |
| `tests/test_t106_motor.py`, `tests/test_t106_r03.py` | 32 · 45 | 32 · 45 (fecha de corte de las peticiones en la última fecha de los datos de control) |
| Suite completa de A (`pytest -q bloque_a/11_Ejecutor`) | 5258 (QA r01 de T-119, antes de su r02) | **5497** en verde (incluye la r02 de T-119) |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 (H-04) | `test_h04_son_las_catorce_fichas_…`; `test_h04_corte_en_la_ultima_fecha_se_sirve_igual_y_en_la_vispera_se_rechaza` (42 casos de control de las 14 fichas); `test_h04_cada_campo_fechado_posterior_al_corte_se_rechaza` (14 fichas, todas las fechas de sus casos); `test_h04_un_bloque_opcional_fechado_despues_del_corte_se_rechaza` (11 bloques que los casos no traen); `test_h04_el_dato_con_hora_del_dia_del_corte_es_conocible`; `test_h04_tcv_tp_una_segunda_via_posterior_al_corte_rechaza_la_peticion`; `test_h04_las_fechas_futuras_por_naturaleza_no_son_observaciones` | Sí. Con el corte en la última fecha, el resultado y las limitaciones son los de sin corte, y el caso de control pasa |
| CA-2 (H-01) | `test_h01_error_real_del_original_es_error_original_aunque_cambie_la_vigente` (clave leída y otra clave de la sección), `test_h01_riesgo_con_otra_clave_de_horizontes_es_error_original`, `test_h01_convencion_distinta_si_la_parte_de_por_defecto_que_se_uso_ya_no_es_la_de_entonces` (sin valor y valor parcial), `test_h01_un_cambio_de_por_defecto_que_el_valor_guardado_cubre_no_ablanda_la_categoria`, `test_h01_sin_la_configuracion_en_el_artefacto_sigue_siendo_convencion_distinta`; `test_t118_hallazgos.py::test_h11_error_original_con_la_configuracion_registrada_aunque_la_vigente_cambie` | Sí |
| CA-3 (H-02) | `test_h02_un_sustituto_unicode_suelto_…` (6 campos), `…_en_un_dato_de_ht01_…` (4), `test_h02_un_valor_que_no_es_json_o_no_es_texto_…` (7), `test_h02_argumentos_de_la_llamada_que_no_son_texto` (8, con el solicitante de 3 000 niveles de H-07 de T-119), `test_h02_la_peticion_bien_formada_se_sirve_igual` | Sí: RECHAZADO y una sola entrada en RC |
| CA-4 (H-03) | `test_h03_una_serie_de_ht01_que_ya_no_esta_…`, `test_h03_una_fecha_del_dato_posterior_al_as_of_…`, `test_h03_un_artefacto_alterado_…` (7 alteraciones), `test_h03_lo_imposible_sigue_siendo_imposible` | Sí: NO / ERROR_REEJECUCION con una entrada REEJECUCION |
| CA-5 (H-05) | `test_h05_la_cota_de_reg_hmm_sale_de_h5_en_semanas`; `test_t118_hallazgos.py::test_h12_las_cotas_de_s_y_p_salen_de_la_configuracion_por_defecto` | Sí: 520 por defecto, 260 con H5 en 60 meses |
| CA-6 (H-06) | `test_t118_hallazgos.py::test_h09_m05_…`, `test_h10_m38_…`, `test_h11_m50_…`, `test_h12_m68_…`, `test_h13_m78_…` (9, 20 y 31 niveles) | Sí: `r01_07_mutantes.py --solo M05,M38,M50,M68,M78 --todo`: 5 muertos, 0 vivos |
| CA-7 | `revisores/impl_mutantes.py`; ver «Gate» | Sí |

## Regresiones (fallan sin la corrección)

`.docs/tickets/T-121/revisores/impl_mutantes.py bloque_a/11_Ejecutor <carpeta desechable>`: deshace cada corrección en una copia y ejecuta `test_t121_hallazgos.py`, `test_t118_hallazgos.py` y `test_t112_motor.py` con `-x`.

- 30 mutantes de H-04, uno por cada comprobación del corte en los tres módulos (la llamada se neutraliza y sus argumentos se siguen evaluando), y 7 de su forma (`>` por `>=`, comparar con hora, segunda vía de TCV-TP, corte que no es fecha, `_dia` sin normalizar).
- 5 de H-01 (la regla de T-118, sin `por_defecto`, sin `sin_registro`, `_cubre` siempre falso y siempre verdadero), 6 de H-02, 3 de H-03 y 3 de H-05 (sin seguir a la configuración, 4 semanas por mes, H5 sin validar).
- Primera pasada (52): 11 vivos, todos de H-04 en bloques opcionales que los casos de control no traen (historia de diferenciales de MON-YLD, decisiones de MON-EXP, historia ex ante de MON-REAL, historia del BPA de IDX-ERP, precios, índices e historia de IDX-CONC, eventos comparables y activos indexados de IDX-REB, historia de TCV-BEI y serie publicada de TCV-TP). Corrección: `test_h04_un_bloque_opcional_fechado_despues_del_corte_se_rechaza`.
- Segunda pasada (los 11, los dos nuevos de `_cubre` y A02 reescrito tras afinar H-01): **ninguno vivo**. En total, 55 mutantes y ninguno vivo.

## Scripts del revisor (sin modificar), antes y después

| Script | Antes (QA r01 de T-118) | Después |
| --- | --- | --- |
| `r01_01_h09_fecha_corte.py` | Bloque 2: 14 fichas de la Fase 1 sirven con el corte en la víspera | **60/60**. Bloque 2: 148 casos con fechas; 20 se sirven con el corte en la víspera, y son todos fechas futuras por naturaleza (vencimientos de CHR-FUND, FIR-PRICE y REI-LEV; desbloqueos de CHR-TOKEN; efectividad de IDX-REB; reuniones de MON-EXP). Ninguna de las 14 |
| `r01_03_h11_ct10_configuracion.py` | Bloque 5: CONVENCION_DISTINTA con la clave leída, otra clave de la sección o `horizontes.H1` cambiados | **34/34**. Bloque 5: ERROR_ORIGINAL en los cuatro casos; bloque 6: la configuración guardada manipulada da NO / ERROR_ORIGINAL |
| `r01_04_h12_configuracion.py` | REG-HMM-001 en 520 con H5 en 60 meses | **47/47**. Con H5 en 60 meses: 260 («sigue a `horizontes.H5`») |
| `r01_05_h13_h14_fuzz.py` | Bloque 1: 104 escapes en 5 758 llamadas. Bloque 3: 33 de 124 artefactos alterados escapan | **8/8**. Bloque 1: 5 758 llamadas, 0 escapes, una entrada en RC por llamada. Bloque 3: de los 124, 0 excepciones fuera de las cuatro declaradas (74 NO / ERROR_REEJECUCION, 16 NO / ERROR_ORIGINAL, 5 NO / DATOS_DISTINTOS, 15 SI, 11 de las cuatro excepciones declaradas y 3 alteraciones que el propio script no llega a escribir en el RC); toda re-ejecución que termina deja su entrada REEJECUCION |
| `r01_07_mutantes.py --solo M05,M38,M50,M68,M78 --todo` | 5 vivos | **5 muertos, 0 vivos** |
| `r01_07_mutantes.py` (los 72) | 56 muertos, 16 vivos | **58 muertos, 11 vivos, 3 que ya no aplican**. Los 11 vivos son los que el revisor juzgó equivalentes (M19–M31, M52, M67). M42–M44 mutaban la regla de CT-10 que H-01 sustituye; sus equivalentes sobre la regla nueva (A01–A05 de `impl_mutantes.py`) mueren |

## Casos de control y resultados servidos

- Los 42 casos de control de las 14 fichas, con el corte en su última fecha: mismo resultado y mismas limitaciones que sin corte (`test_h04_corte_en_la_ultima_fecha_…`). Los de MON-EXP-001 e IDX-REB-001, con el corte en la víspera de sus fechas futuras: igual que sin corte.
- `verificar_casos_control` de las 80 fichas: en la suite (`test_t106_*`, `test_fase1_*`, `test_fase2_*`, `test_t112_motor.py`, `test_t119_*`), en verde.
- `python tests/goldens_ct.py` (desde `bloque_a/11_Ejecutor`): «goldens de contratos: coinciden»; no se re-congela nada.

## Gate

Desde la raíz de la copia de trabajo. El gate completo `./tools/check_all.sh` no se ha lanzado (máquina compartida, por instrucción): se pasan sus piezas.

| Comprobación | Resultado |
| --- | --- |
| `pytest -q` de `test_t121_hallazgos.py`, `test_t119_*.py`, `test_t118_hallazgos.py`, `test_t106_*.py`, `test_fase1_*.py`, `test_fase2_*.py`, `test_t112_motor.py`, `test_integracion.py`, `test_fase3_goldens.py` | 4399 en verde (9 min 35 s; antes de añadir las dos pruebas del solicitante) |
| Suite completa de A | **5497** en verde (21 min 34 s) |
| `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | 2902 (cuota 2902); `test_t121_hallazgos.py`, sin incidencias |
| `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | 109 (cuota 109) |
| `tools/corpus_integridad.py` | Íntegro, 695 archivos |
| `tools/refs_vivas.py` · `tools/secrets_scan.py` · `tools/nfc_check.py` | En verde los tres |

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/pytest -q tests/test_t121_hallazgos.py tests/test_t118_hallazgos.py
../../.venv/bin/python tests/goldens_ct.py
cd ../..
.venv/bin/pytest -q bloque_a/11_Ejecutor
.venv/bin/python .docs/tickets/T-121/revisores/impl_mutantes.py bloque_a/11_Ejecutor <carpeta desechable>
```
