# T-72 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Marco común de C (`.docs/scripts/pruebas_marco.sh`) | 57 baterías (V0.68) | 58 baterías (V0.69) |
| `pruebas/pruebas_reloj_diario_t72.py` | — | 32 comprobaciones (24 en la r01, más 8 regresiones de la QA r01) |
| `pruebas/pruebas_consola_sistema.py` | 46 | 46: el diario falso con `_n` booleano gana `estado_diario()` con el mismo caso |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `un_cambio_por_fuera_se_ve_desincronizado_H05`, `y_el_panel_lo_pinta_ROJO_antes_de_operar_H05`, `mirar_no_bloquea_el_diario`, `la_operacion_siguiente_da_DI06_como_avisaba`, `fichero_reescrito_por_fuera_desincronizado` |
| CA-2 | `la_consola_usa_la_foto_publica`, `una_foto_ilegible_es_ROJO_sin_lanzar`, `si_estado_diario_lanza_es_ROJO`, `una_foto_no_operativa_es_ROJO_H04` |
| CA-3 | `*_es_de_solo_lectura`, `contraste_NaN_*`, `salto_NaN_*`, `desfase_NaN_*`, `tolerancia_que_no_se_compara_*`, `*_no_da_instantes_ni_lanza_H01_H02` |
| CA-4 | Las 58 baterías y el gate |

## Regresiones

- **Batería nueva con el código de la V0.68:** falla. `setattr` cambia la tolerancia, el panel no ve el diario desincronizado y `estado_diario()` no existe.
- **Regresiones de la QA r01 (H-01, H-02, H-04):** fallan con el código del commit `61d3973` y pasan con la corrección.
- **Sonda `r01_02`:** con la corrección solo queda el caso del contraste finito sin tope (H-03, en T-89).
- **Sonda `r01_01`:** el reloj sano da lo mismo que antes en 33.452 comparaciones.

## Gate

El gate completo (`.docs/scripts/gate.sh` con la opción `--completo`) se pasa antes de cada commit, a través de `.docs/scripts/commit.sh`. La QA r01 obtuvo 12/12 en un worktree limpio del commit `61d3973`.
