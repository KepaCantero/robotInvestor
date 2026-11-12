# T-75 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `pruebas/pruebas_embudo_sequia_t75.py` | — | 24 (V0.70), 34 (V0.73, con las regresiones de la QA r01), 41 (V0.75, con las de la QA r02) |
| `pruebas/pruebas_integracion_v053.py` | 33 | 34 (V0.70), 36 (V0.73: hasta MIG-009), 38 (V0.75: hasta MIG-011) |
| `pruebas/pruebas_catalogo_codigos.py` | 40 avisos | 41 (O-40); 43 en V0.73 (O-41, O-42 de T-76); 45 en V0.75 (O-43 de T-97, O-44 de T-76) |

## Regresiones de la QA r01

- **H-08:** `con_barridos_diarios_la_alarma_salta_H08`, `y_se_repite_una_vez_por_plazo_mientras_dure` y `la_sequia_sigue_hasta_la_siguiente_inversion_H08`.
- **H-01:** `el_veto_de_F_queda_anotado_y_el_embudo_lo_dice_H01` y `y_su_caducidad_lleva_el_veto_como_causa_previa_H01`.
- **H-03 y H-04:** `un_analisis_reutilizado_cuenta_una_vez_H03`, `una_oportunidad_que_sale_dos_veces_cuenta_una_H04` y `dos_periodos_seguidos_no_cuentan_dos_veces_el_borde_H04`.
- **H-07:** `plazo_ilegible_no_juzga_H07` e `informe_con_dias_ilegibles_no_vale_H07`.

Todas fallan con el código de la V0.70 (commit `d6fbdb6`).

## Regresiones de la QA r02 (V0.75)

| Hallazgo | Prueba |
| --- | --- |
| H-09 | `el_veto_visto_en_la_pantalla_queda_anotado_H09`, `y_el_informe_no_se_puede_volver_a_usar_H09`, `y_la_caducidad_lleva_el_veto_como_causa_previa_H09` |
| H-10 | `la_propuesta_tras_el_veto_es_la_misma_y_valida_H10` |
| H-11 | `tras_el_veto_no_se_anota_nada_anterior_H11`, `y_despues_del_veto_si_se_puede_descartar_H11` |
| H-14 | `la_edad_se_mide_desde_el_primer_instante_real_H14` |

H-12 y H-13 son de documentación (LEEME, Documentos 0 de la V0.70 y la V0.75, deuda, este informe y el docstring de `embudo()`).

**Con el código de la V0.74:** las regresiones nuevas fallan, salvo `y_el_informe_no_se_puede_volver_a_usar_H09`. Esa ya pasaba y protege que el informe se siga consumiendo.

## Gate

El gate completo (`.docs/scripts/gate.sh` con la opción `--completo`) se pasa antes de cada commit, a través de `.docs/scripts/commit.sh`. La V0.70 lo pasó con 12/12 sobre una copia limpia.

**V0.75:** las 62 baterías del marco pasan (`.docs/scripts/pruebas_marco.sh`) y el LEEME coincide con el disco (`.docs/scripts/leeme_marco.py`). El gate completo se pasa en el commit, con `.docs/scripts/commit_limpio.sh`.
