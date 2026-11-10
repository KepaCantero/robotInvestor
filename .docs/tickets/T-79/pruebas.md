# T-79 · Pruebas

| Suite | Antes (V0.53) | V0.66 de GLM | Después (V0.67) |
| --- | --- | --- | --- |
| Marco común de C (`sistema_global/marco_comun_c`) | 49 baterías | 56 baterías | 56 baterías en verde; `pruebas_consola_sistema.py` pasa de 42 a 46 comprobaciones y `pruebas_integracion_v053.py` gana una |
| Bloques A, A Forex y B | 201 · 68 · 174 | — | 201 · 68 · 174 (no se tocan) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1: la V0.66 contiene las anteriores | Comparación por SHA-256 de los siete ZIP (Documento 0, §2). Desde el repositorio lo repite la QA con los manifiestos de la V0.62 y la V0.66 |
| CA-2: 56 baterías y gate 12/12 | `.docs/scripts/pruebas_marco.sh` da 56 en verde; gate completo 12/12 |
| CA-3: cada corrección falla con el código anterior | `r01_umbral_nan_inf_o_bool_es_rojo` falla con la V0.66. `r02_degradadas_ilegible_es_rojo` y `r02_estado_del_reloj_conserva_un_bloqueo_ilegible` fallan con `250ddb7`. Sin MIG-005 fallan `hay_camino_desde_V0_45_hasta_este_codigo` y `v067_esquema_actual_y_MIG005_sin_cambios` (`revisores/r01_regresiones_fallan_sin_correccion.py`) |
| CA-4: deuda sin choques y pendientes con fila | 86 filas `T-NN` sin repetir; de T-69 a T-86 |

## Otras comprobaciones

- Un estado y un diario guardados por la V0.53 real migran a la V0.67, y MIG-005 rechaza los registros hostiles contra `PROHIBIDAS`: `revisores/r01_migracion_v053_a_v067.py`, 80 comprobaciones.
- Dos ejecuciones de las baterías nuevas y de las que cambian dan la misma salida: `revisores/r01_determinismo.py`.
- El LEEME coincide con el disco, tanto en la lista de ejecución como en las comprobaciones de cada batería: `.docs/scripts/leeme_marco.py`.

## Gate

Se ejecutó `.docs/scripts/gate.sh` con `--completo` antes de cada commit. Los registros quedan en `.docs/scripts/.logs/`.
