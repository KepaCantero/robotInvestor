# T-75 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `pruebas/pruebas_embudo_sequia_t75.py` | — | 24 (V0.70), 34 (V0.73, con las regresiones de la QA r01) |
| `pruebas/pruebas_integracion_v053.py` | 33 | 34 (V0.70), 36 (V0.73: hasta MIG-009) |
| `pruebas/pruebas_catalogo_codigos.py` | 40 avisos | 41 (O-40); 43 en V0.73 (O-41, O-42 de T-76) |

## Regresiones de la QA r01

- **H-08:** `con_barridos_diarios_la_alarma_salta_H08`, `y_se_repite_una_vez_por_plazo_mientras_dure` y `la_sequia_sigue_hasta_la_siguiente_inversion_H08`.
- **H-01:** `el_veto_de_F_queda_anotado_y_el_embudo_lo_dice_H01` y `y_su_caducidad_lleva_el_veto_como_causa_previa_H01`.
- **H-03 y H-04:** `un_analisis_reutilizado_cuenta_una_vez_H03`, `una_oportunidad_que_sale_dos_veces_cuenta_una_H04` y `dos_periodos_seguidos_no_cuentan_dos_veces_el_borde_H04`.
- **H-07:** `plazo_ilegible_no_juzga_H07` e `informe_con_dias_ilegibles_no_vale_H07`.

Todas fallan con el código de la V0.70 (commit `d6fbdb6`).

## Gate

El gate completo (`.docs/scripts/gate.sh` con la opción `--completo`) se pasa antes de cada commit, a través de `.docs/scripts/commit.sh`. La V0.70 lo pasó con 12/12 sobre una copia limpia.
