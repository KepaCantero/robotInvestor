# T-100 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `pruebas/pruebas_embudo_sequia_t75.py` | 41 | 45 |
| `pruebas/pruebas_sombra_t76.py` | 74 | 94 (con la regresión de H-03 reescrita) |
| `pruebas/pruebas_catalogo_codigos.py` | 23 | 23 (texto de O-03) |

## Regresiones

| Hallazgo | Prueba |
| --- | --- |
| T-75 H-15 | `tras_un_analisis_nuevo_el_veto_no_es_la_causa_mire_el_periodo_que_mire_H15` |
| T-75 H-17 | `tras_el_veto_de_la_pantalla_el_reloj_se_queda_en_el_veto_H17`, `y_nada_anterior_al_veto_de_la_pantalla_entra_H17`, `un_rechazo_que_no_anota_sigue_sin_adelantar_el_reloj_H17` |
| T-76 H-17 | `el_mismo_movimiento_declarado_dos_veces_cuenta_una_H17`, `y_un_aporte_repetido_no_da_la_vuelta_al_juicio_H17`, `la_misma_referencia_con_*_es_O03_con_kill_switch_H17`, `movimiento_*_no_H17`, `otra_referencia_es_otro_movimiento_H17`, `las_entradas_sin_referencia_de_la_V075_se_conservan_H17` |
| T-76 H-19 | `barrer_con_el_registro_roto_*_para_y_no_calcula_lo_pendiente_H19` |
| T-76 H-18 | Las siete `*_H18` y `resultados_no_finitos_no_se_anotan_H03` reescrita |

## Mutantes

- `.docs/tickets/T-76/revisores/r03_04_mutantes.py`: 0 vivos de 31. M15 ya no se aplica porque el texto cambió; lo cubre el mutante manual «barrer calcula lo pendiente».
- `.docs/tickets/T-75/revisores/r03_mutantes.py`: 0 vivos. El del reinicio del veto ya no se aplica.
- Siete mutantes manuales sobre las correcciones (veto no borrado antes del periodo o nunca, barrido sin kill-switch o calculando lo pendiente, sin detección de duplicados, conflicto sin kill-switch, duplicado solo por tipo): todos mueren.

## Gate

Las 62 baterías del marco (`.docs/scripts/pruebas_marco.sh`) y el LEEME frente al disco (`.docs/scripts/leeme_marco.py`). El gate completo se pasa en el commit, con `.docs/scripts/commit_limpio.sh`.
