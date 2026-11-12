# T-99 · Pruebas

Ejecutadas el 12-11-2026 por Claude, con el `.venv` de T-96.

| Suite | Antes | Después |
| --- | --- | --- |
| `pruebas_registro_experimentos.py` | — | 20 |
| `pruebas_banco_medida.py` | 10 | 12 (integración con el registro, intento fallido y veredicto conjunto) |
| `pruebas_borradores_contratos.py` | — | 22 |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `test_prerregistro_mal_formado_no_escribe_nada` (9 casos), `test_prerregistro_incompleto` | OK |
| CA-2 | `test_sin_prerregistro_no_hay_intento_ni_resultado`, `test_un_resultado_no_se_reescribe_ni_lleva_un_veredicto_inventado` | OK |
| CA-3 | `test_reescribir_una_linea_rompe_la_cadena`, `test_quitar_un_intento_fallido_rompe_la_cadena`, `test_cambiar_el_criterio_despues_rompe_la_cadena`, `test_linea_que_no_es_json` | OK |
| CA-4 | `test_cuentan_todos_los_intentos_y_las_variantes_de_mas`, `test_adoptable_solo_si_mejor_dentro_del_maximo_y_despues_del_prerregistro` | OK |
| CA-5 | `test_integracion_bloque_a` (dos ejecuciones, la segunda con `--experimento`), `test_un_intento_que_falla_tambien_queda_anotado` | OK |
| CA-6 | `test_ct24_todo_lo_que_escribe_el_registro_valida` y los casos mal formados | OK |
| CA-7 | `test_integracion_bloque_a` (sin cambios en `bloque_a`, `bloque_b` ni el marco) y ninguna carpeta «.docs/experimentos/» tras las pruebas | OK |

## Regresiones

Las pruebas encontraron un fallo propio: un intento nuevo de una variante ya contada se marcaba fuera del máximo porque se contaban todas las variantes vistas hasta entonces. Corregido: cuenta el orden en que aparece cada variante.

## Gate

Pasa en la copia limpia de `.docs/scripts/commit_limpio.sh`.
