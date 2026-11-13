# T-88 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t88_consumo.py` | — | 5 (determinismo V5 y V6, total real en V6, liquidación a mano y caso sin primas «solo») |
| Pruebas de presupuesto e integración (`test_integracion`, `test_t65_qa_r01`, `test_t87_agentes`, `test_t92_revision`, `test_v5`) | 128 | 128 |
| A | 714 | 719 |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_dos_ejecuciones_iguales_dan_el_mismo_consumo_por_tipo[v5]` y `[v6]` (seis perfiles); a mano, también con los doce |
| CA-2 | `test_v6_el_total_cargado_es_el_coste_real` (29,219 frente a 29,219 UC con los doce perfiles) |
| CA-3 | `test_la_prima_solo_es_prudente_y_la_liquidacion_conserva_el_total`, `test_sin_primas_solo_lo_real_va_a_la_bolsa_comun` |
| CA-4 | Gate de `commit_limpio.sh` |

## Regresiones

Con el código anterior, el determinismo falla en la V5: con los doce perfiles cambian DIV, FON, RF y RV entre tres ejecuciones. El total cargado en la V5 (51,933 UC) es el mismo antes y después; la diferencia con el coste real (54,892) son las llamadas posteriores al registro de F5 (límite declarado).

## Gate

`./tools/check_all.sh` completo con `commit_limpio.sh`.

## Ronda r03

| Suite | r02 | r03 |
| --- | --- | --- |
| `tests/test_t88_consumo.py` | 5 | 11 |
| `r02_04_mutantes.py` (QA r02) | sobreviven P1, P2, P3, P7, P8, P9 y P10 | mueren los 11 que se aplican; P3 y P4 no se aplican (la línea del grupo cambió; los cubren las pruebas de grupos de la V5 y de la V6) |

## Ronda r04

| Suite | r03 | r04 |
| --- | --- | --- |
| `tests/test_t88_consumo.py` | 11 | 15 (claves del RUN de F5 en V5 y V6, reescritura de un analista V5, orden de `cierres_parciales`) |
| `r03_03_mutantes.py` (QA r03) | sobreviven R1, R4 y R5 | mueren R1 a R5 |
| Gate (`commit_limpio.sh`, commit `102aaae`) | 12/12, A 1283 | 12/12, A 1288 |

La línea de «Regresiones» que atribuía la diferencia entre lo cargado en la V5 (51,933 UC) y el coste real (54,892) a las llamadas posteriores a F5 se corrige: es la curación de AG-12, sin presupuesto (H-14 de la QA r04).
