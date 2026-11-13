# T-117 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t117_gc1.py` | — | 43 superadas |
| `tests/test_t101_v6.py`, `test_t102_filtro.py`, `test_t113_deuda.py`, `test_t88_consumo.py` (usan la V6) | en verde | en verde (399 con las de T-116 y T-117, 13-11-2026) |
| `tests/test_fase3_goldens.py` (ciclo V5) | 51 | 51: el diseño por defecto no cambia |
| ruff (cuenta del gate) | 2902 | 2902 |
| mypy `bloque_a` | 109 | 109 |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_los_valores_por_defecto_son_los_decididos`, `test_en_el_diseno_v5_nada_cambia` |
| CA-2 | `test_el_umbral_del_tipo_manda_y_los_demas_usan_el_general`, `test_cada_tipo_usa_su_umbral` (12), `test_el_borde_del_umbral_pasa_y_un_pelo_menos_no`, `test_para_volver_al_umbral_general_en_un_tipo_se_le_pone_ese_valor` |
| CA-3 | `test_sin_el_recuento_de_familias_no_se_descarta_por_ello`, `test_con_familias_min_cero_no_se_exige_concordancia`, `test_la_concordancia_solo_se_exige_cuando_manda_la_senal_compuesta`, `test_con_tres_familias_y_075_la_concordancia_no_cambia_nada`, `test_un_descartado_por_familias_puede_llegar_como_exploracion` |
| CA-4 | `test_una_configuracion_invalida_se_rechaza` (15), `test_una_configuracion_valida_se_acepta` (5) |
| CA-5 | `test_en_un_ciclo_el_registro_de_gc1_lleva_el_umbral_de_cada_tipo` |
| CA-6 | Suites de la tabla de arriba; gate, abajo |

## Regresiones

No aplica: es una función nueva del diseño aspirante.

## Gate

El gate completo 12/12 lo pasa `commit_limpio.sh` al hacer el commit; su resultado se anota en el registro del ticket.
