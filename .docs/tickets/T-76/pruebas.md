# T-76 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `pruebas/pruebas_sombra_t76.py` | — | 45 (V0.71), 55 (V0.73, con las regresiones de la QA r01) |
| `pruebas/pruebas_integracion_v053.py` | 34 | 35 (V0.71), 36 (V0.73) |

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

## Gate

El gate completo (`.docs/scripts/gate.sh` con la opción `--completo`) se pasa antes de cada commit, a través de `.docs/scripts/commit.sh`.
