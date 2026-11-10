# T-80 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Marco común de C (`.docs/scripts/pruebas_marco.sh`) | 56 baterías en verde (V0.67) | 57 baterías en verde (V0.68) |
| `pruebas/pruebas_via_directa_t80.py` | — | 116 comprobaciones (93 en la r01, más 13 regresiones de la QA r01, 4 de la r02, 2 de la r03, 3 de la r04 y 1 de la r05) |
| `pruebas/pruebas_integracion_v053.py` | 32 | 33: esquema actual V0.68 y cadenas hasta MIG-006; lo de V0.67 sigue comprobado |
| `pruebas/pruebas_comparador_t17.py` | `PAR-0.4.0` | `PAR-0.5.0` (`o_max_analisis_consulta`) |
| `entrega_claude/V0.68/scripts/pc3_01_via_directa.py` | — (el de V0.67 daba FALLA) | CUMPLE |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `C_nace_EN_ANALISIS` … `C_EJECUTADA_por_G_y_nace_la_posicion`; `D_nace_VALIDADA_reutilizando_el_analisis` … `D_sigue_a_AUTORIZADA_y_EJECUTADA`; `E_nace_COMPARADA_frente_al_benchmark` … `E_sigue_a_PROPUESTA_y_el_dinero_sale_por_F_y_G` |
| CA-2 | `C_sin_encargo_no_nace`, `C_con_un_encargo_incompleto_no_nace`, `C_el_presupuesto_del_dia_es_el_mismo`; `D_un_analisis_en_juego_no_se_reutiliza`, `D_lo_apartado_por_el_gestor_no_vuelve_por_la_via_DIRECTA`, `D_analisis_caducado`, `D_no_reutiliza_un_sobre_cuyo_origen_se_volvio_a_encargar_H01`, `una_propuesta_caducada_no_vuelve_por_la_via_DIRECTA_H03`, `D_con_analisis_y_encargo_a_la_vez_no_H06`; `E_sin_motivo_de_no_comparar`, `E_con_otros_candidatos_se_devuelve_a_D`; `bloque_F_no_es_entrada`, `bloque_G_no_es_entrada` |
| CA-3 | `consulta_no_abre_expediente_ni_mueve_ninguno`, `consulta_deja_su_rastro_en_SC5`, `tocar_el_rastro_SC5_se_detecta`, `SC5_*_H02`, `consultar_con_el_rastro_tocado_da_O13_y_kill_H05` |
| CA-4 | `tocar_*_se_detecta`, `un_*_en_un_expediente_no_DIRECTA_se_detecta_H07` |
| CA-5 | `persistencia_conserva_los_DIRECTA_y_el_rastro`, `diario_anota_y_reproduce_consultar_y_abrir_directa`, `pruebas_integracion_v053.py` (MIG-006 desde V0.50 y V0.52) |
| CA-6 | `PC3_01_CUMPLE` |

## Regresiones

Las 13 comprobaciones nuevas de la QA r01 (H-01 a H-07) se ejecutaron contra el `orquestador.py` del commit `9a5225d` (el de la r01) y fallan todas con él: `D_no_reutiliza_un_sobre_cuyo_origen_se_volvio_a_encargar_H01`, `SC5_vaciarlo…`, `SC5_recortar_la_apertura…`, `SC5_recortar_la_consulta_y_la_apertura…` (H-02), `una_propuesta_caducada_no_vuelve_por_la_via_DIRECTA_H03`, `D_sin_analisis_con_encargo_de_nivel_bajo_nace_EN_ANALISIS` y `D_el_nivel_bajo_puede_acabar_en_una_orden_H04`, `consultar_con_el_rastro_tocado_da_O13_y_kill_H05`, `D_con_analisis_y_encargo_a_la_vez_no_H06` y las tres `un_*_en_un_expediente_no_DIRECTA_se_detecta_H07`. Con el código corregido pasan. Las sondas de la QA (`entrega_claude/V0.68/qa/r01_*`) dan SIN FALLOS, salvo la 03 y la 06, que esperaban el comportamiento anterior (la reutilización cruzada, que ahora se rechaza, y N1 como nivel bajo).

## Gate

Gate completo (`.docs/scripts/gate.sh` con la opción `--completo`), lanzado por `.docs/scripts/commit.sh` antes de cada commit:
- r01 (commit `9a5225d`): 12/12.
- Correcciones de la r01 y la r02: el resultado queda en el log del gate de su commit (`.docs/scripts/.logs/`). La QA r02 lo pasó sobre una copia limpia de T-80, sin T-65: 11/12, solo `refs-vivas` por las citas a T-65, ya corregidas (H-11).

Regresiones de la r02: `una_propuesta_caducada_y_descartada_por_OPERADOR_no_vuelve_H09` y `..._por_BROKER_...` fallan con el código de la r01 corregida (reutilizan) y pasan con la r02; `el_motivo_dice_que_caduco_H12_*` comprueba el motivo nuevo.

Regresiones de la r03: `D_un_analisis_superado_por_el_reanalisis_de_un_DIRECTA_no_vuelve_H13` y `D_el_motivo_dice_que_esta_superado_H13` fallan con el código del commit `f384bef` y pasan con la corrección. Las sondas `r03_*` dan SIN FALLOS.

Regresiones de la r04: `el_origen_no_se_reanaliza_con_su_analisis_en_juego_H16` y `y_lo_dice_H16` fallan con el código del commit `c482bf1` y pasan con la corrección; `apartado_el_DIRECTA_el_origen_si_se_reanaliza_H16` comprueba que no cierra de más. Las sondas `r04_01` (variantes a, c y e) y `r04_03` dan FALLA porque esperaban el reencargo, que ahora se rechaza, y H-17 (documentado). La `r02_02` se para ahora en su caso c), porque el reencargo que intenta es el que rechaza H-16; sus partes de H-01 las repite `r05_01`, y pasan.

Regresión de la r05: `el_gemelo_no_se_reanaliza_con_el_analisis_en_juego_en_otro_H19` falla con el código del commit `c482bf1` y pasa con el actual. La regresión de H-16 ya no permite mutaciones del estado.
