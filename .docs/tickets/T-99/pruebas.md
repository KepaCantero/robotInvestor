# T-99 · Pruebas

## Ronda r03 (15-11-2026)

| Suite | r02 | r03 |
| --- | --- | --- |
| `.docs/scripts/pruebas_registro_experimentos.py` | 50 | 66 en verde |
| Todas las de `.docs/scripts` | 158 | 175 en verde |
| Mutantes `.docs/tickets/T-99/mutantes_r03.py` | 0 de 30 vivos | 0 de 48 vivos |

Una prueba por hallazgo de la QA r02:
- `test_h13_*`: recorte subido, veredicto cambiado y subido, registro sacado de HEAD y fusión resuelta con un lado;
- `test_h14_*` a `test_h22_*`;
- `test_qa_r02_variantes_nfd_de_un_registro_antiguo` y `test_t99_h24_*`, este último en las pruebas del banco.

`revisores/r02_00_todos.sh` frente al registro 0.3.0: dan 0 hallazgos `r02_02` (ancla en git, 18 de 18), `r02_04` (adopción, 40 de 40), `r02_06` (línea de órdenes, 34 de 34) y `r02_09` (contrato). Los que aún marcan algo son por diseño (`analisis-tecnico.md`, «Ronda r03»).


## Ronda r02 (15-11-2026)

| Suite | r01 | r02 |
| --- | --- | --- |
| `.docs/scripts/pruebas_registro_experimentos.py` | 20 | 50 en verde |
| `.docs/scripts/pruebas_borradores_contratos.py` | 22 | 22 |
| `.docs/scripts/pruebas_banco_medida.py` | 82 | 86 (4 de la interfaz con el registro, H-08) |
| Todas las de `.docs/scripts` (las que ahora ejecuta `commit_limpio.sh`) | — | 158 en verde |
| Mutantes `.docs/tickets/T-99/mutantes_r02.py` | — | 0 de 30 vivos |

Scripts del revisor de la r01 contra el registro 0.2.0: `r01_05` (intentos y resultados) da 30 de 30. Los que aún marcan algo son por diseño y se explican en `analisis-tecnico.md`, «Ronda r02»: truncar fuera de git rehaciendo el sello, fusionar dos ramas y la variante por defecto.


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
