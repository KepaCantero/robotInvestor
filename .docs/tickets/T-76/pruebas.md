# T-76 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `pruebas/pruebas_sombra_t76.py` | — | 45 (V0.71), 55 (V0.73, con las regresiones de la QA r01), 74 (V0.75, con las de la QA r02) |
| `pruebas/pruebas_integracion_v053.py` | 34 | 35 (V0.71), 36 (V0.73), 38 (V0.75: hasta MIG-011) |

## Regresiones de la QA r01

| Hallazgo | Prueba |
| --- | --- |
| H-01 | `un_aporte_de_la_vispera_paga_un_dia_de_coste_H01`, `una_retirada_no_borra_el_coste_devengado_H01` |
| H-02 | `no_se_compara_un_mes_sin_terminar_H02` |
| H-03 | `resultados_no_finitos_no_se_anotan_H03` |
| H-04 | `si_I_deja_de_comparar_barrer_lo_avisa_H04`, `y_no_lo_repite_cada_barrido` |
| H-05 | `con_el_registro_tocado_comparar_da_O13_antes_de_leerlo_H05` |
| H-06 | `retirar_mas_de_lo_que_hay_con_precios_enormes_no_H06` |
| H-07 | `el_indice_de_precios_del_inicio_no_cambia_H07` |
| H-08 | `O41_una_vez_al_pasar_a_no_superarla_no_cada_mes_H08` |

## Regresiones de la QA r02 (V0.75)

| Hallazgo | Prueba |
| --- | --- |
| H-10 | `una_retirada_tras_el_cierre_no_cambia_el_juicio_H10` (J5), `un_aporte_tras_el_cierre_no_cambia_el_juicio_H10` (J5c) |
| H-11 | `inicio_con_unidades_no_finitas_no_H11`, `un_movimiento_no_finito_no_se_confunde_con_una_retirada_mayor_H11` |
| H-12 | `registro_tocado_*_es_O13_H12` (cada toque, en `iniciar_sombra` y `movimiento_sombra`), `barrer_avisa_de_un_registro_de_la_sombra_roto_H12` |
| H-13 | `antes_del_plazo_de_gracia_no_hay_O42_H13`, `y_justo_al_acabar_el_plazo_si_H13`, `dice_cuantos_meses_faltan_H13`, `y_el_aviso_lo_dice_H13`, `falta_el_mes_de_juicio_es_O44_en_ALTA_H13` |
| H-14 | `el_mes_de_inicio_es_el_de_UTC_en_el_borde_H14`, `y_no_se_puede_empezar_por_el_mes_siguiente_H14`, `pendiente_no_salta_el_ultimo_instante_del_mes_H14`, `la_tolerancia_es_relativa_con_unidades_diminutas_H14`, `estado_sombra_con_un_resultado_infinito_es_None_H14` |

H-15 y H-16 son de documentación (LEEME, Documentos 0 de la V0.71 y la V0.75, deuda, este informe y la descripción de MIG-009).

**Con el código de la V0.74:** las regresiones de H-10 y H-11 fallan. Después, la batería se para con un AssertionError, porque faltan las funciones nuevas (`comparaciones_sombra_pendientes`, O-44).

## Gate

El gate completo (`.docs/scripts/gate.sh` con la opción `--completo`) se pasa antes de cada commit, a través de `.docs/scripts/commit.sh`.

**V0.75:** las 62 baterías del marco pasan (`.docs/scripts/pruebas_marco.sh`) y el LEEME coincide con el disco (`.docs/scripts/leeme_marco.py`). El gate completo se pasa en el commit, con `.docs/scripts/commit_limpio.sh`.
