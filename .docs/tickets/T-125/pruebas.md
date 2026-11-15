# T-125 · Pruebas

| Suite | Resultado |
| --- | --- |
| `test_t125_fiabilidad_fuentes.py` | 12 superadas |
| `test_integracion.py`, `test_t53_evaluacion_y_almacen.py`, `test_t66_evaluacion.py`, `test_t65_hallazgos.py` (con las de T-125) | 116 superadas |
| Goldens de contratos | coinciden |
| ruff · mypy A | 2902 · 109 |

Gate completo: lo pasa `commit_limpio.sh` al hacer el commit.

## Ronda r02 (15-11-2026)

| Suite | Antes | Después |
| --- | --- | --- |
| `test_t125_fiabilidad_fuentes.py` | 12 | 12 (re-sembradas: registro el día de la emisión y fuentes de F9; mismas afirmaciones) |
| `test_t125_r02.py` (nueva) | — | 43 |
| Vecinas (`test_t125*`, `test_t126*`, `test_t116_r05`, `test_fase4_*`, `test_fase3_goldens`, `test_integracion`, `test_t12*`) | — | 595: 594 superadas y 1 que fallaba solo porque el documento de evidencias estaba sin regenerar (`test_h05_…`); tras `--ejecutar`, en verde |
| Goldens de contratos (`python tests/goldens_ct.py`) | coinciden | coinciden (sin re-congelar) |
| ruff (tres `11_Ejecutor`) · mypy A | 2902 · 109 | 2902 · 109 |

### Hallazgo → prueba

| Hallazgo | Pruebas (`test_t125_r02.py`) |
| --- | --- |
| H-01 | `test_r02_h01_del_analista_a_f2_al_evaluador_a_la_fue_y_al_ct19` (dos ciclos: el Analista devuelve 8 pronósticos de REF-RF-0001, llegan a F2 con su bloque y su evidencia, y tras vencer salen en la FUE- con `calc_id` y en el CT-19 a AG-16), `…_la_referencia_del_buscador_trae_su_pronostico_a_f2`, `…_un_bloque_no_registrable_no_entra_y_queda_en_ha` (el caso de `r01_03`), `…_que_bloque_puede_registrarse` (9 casos) |
| H-02 | `…_h02_una_fecha_con_zona_u_hora_cuenta_sin_excepcion` (4), `…_una_pieza_con_zona_no_tumba_el_c5_del_ciclo`, `…_si_la_fiabilidad_falla_el_resto_del_c5_sigue` |
| H-03 | `…_h03_solo_cuenta_lo_registrado_antes_de_su_fecha_objetivo` (5), `…_cuenta_el_bloque_tal_como_se_registro` |
| H-04 | `…_h04_un_ref_id_que_no_es_una_fuente_de_f9_no_cuenta`, `…_sin_registro_de_referencias_no_cuenta_ninguno` |
| H-05 | `…_h05_el_mismo_pronostico_en_dos_afirmaciones_cuenta_una_vez` |
| H-06 | `…_h06_una_fuente_que_llega_a_la_muestra_a_mitad_de_mes_sale_ese_mes` |
| H-07 | `…_h07_ventana_de_24_meses_con_su_borde`, `…_no_cuenta_lo_que_no_ha_vencido_aunque_haya_cierre`, `…_no_cuenta_lo_emitido_en_su_fecha_objetivo`, `…_antiguedad_del_cierre_con_su_borde`, `…_los_bordes_del_rango_estan_dentro` (4), `…_una_probabilidad_de_0_o_1_no_cuenta` (4), `…_los_puntos_no_bajan_de_0` |
| H-08 | `…_h08_la_probabilidad_sin_declarar_es_la_de_la_banda_y_la_fue_lleva_calc_id`, `…_sin_el_motor_no_hay_fue` |

### Scripts del revisor, antes y después

| Script | r01 | r02 |
| --- | --- | --- |
| `r01_03_camino_de_entrada_a_f2.py` (tal cual) | con bloque 0, Evaluador 0 | con bloque 0, Evaluador 0: **correcto ahora**, porque su bloque tiene la fecha objetivo ya pasada y otra fuente que la de la pieza (H-03, H-04); los 8 rechazos quedan en HA con su motivo. Con un bloque registrable (`r02_camino_de_entrada_a_f2.py`): 8 CLM con bloque en F2 y, un ciclo después, FUE- de REF-RF-0001 (n = 8, 12,4 puntos, `calc_id`) comunicada por CT-19 y anotada |
| `r01_02_mutantes.py` tal cual (solo las 12 de la r01) | 6 de 14 muertos | 6 de 14 muertos (el script fija `PRUEBAS` en el fichero de la r01) |
| `r01_02_mutantes.py` con `test_t125_r02.py` (`.docs/scripts/mutantes_revisor_ampliado.py`) | — | **13 de 14 muertos**; K08 vivo y equivalente: la regla de H-03 (`emision <= registro < objetivo`) implica `emision < objetivo` |
| `r01_01_ataques_fiabilidad.py` | A1–A9 | No se repite tal cual: siembra con `REF-0001` y el reloj en `AS_OF`, así que con H-03 y H-04 no cuenta nada; cada ataque tiene su prueba en la tabla de arriba |

Regresión: con el código de `fb3ccd4` el fichero nuevo no llega a importarse (la validación del bloque no existía); regla a regla, los mutantes del revisor (K01 a K14 salvo K08) muestran que cada prueba falla sin su corrección, y `r02_camino_de_entrada_a_f2.py` daba 0 bloques en F2 con un pronóstico registrable (el ejecutor lo perdía).

### Comandos

```bash
cd bloque_a/11_Ejecutor
python -m pytest -q tests/test_t125_fiabilidad_fuentes.py tests/test_t125_r02.py
QA_TMP=<tmp> python ../../.docs/tickets/T-125/r02_camino_de_entrada_a_f2.py
cd ../.. && python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-125/revisores/r01_02_mutantes.py <copia con «_mut»>/bloque_a tests/test_t125_r02.py
```

Gate completo (`./tools/check_all.sh`) y suite entera de A: no ejecutados en esta ronda (encargo); los pasa quien hace el commit.

## Ronda r03

| Suite o script | Resultado |
| --- | --- |
| `tests/test_t125_r03.py` + `test_t125_r02.py` | 60 passed |
| `r02_01_ataques_ciclo.py` (B04 adaptada) | B01 con `run_id` en RC; B03, B04 y B11 rechazan las fechas no ISO; B07 un pronóstico por serie; B10 sin excepción; B12 sin `variable` o con «rentabilidad_12m» no entra ni cuenta |
| `r02_02_ciclos_sin_bloque.py` | iguales salvo la ruta de la carpeta temporal escrita en el informe |
