# T-178 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`pytest -q bloque_a/11_Ejecutor`, recogidas) | 8188 | 8205 (+17 de `tests/test_t178.py`) |
| Bloque A, ejecución completa (una vez, al final) | — | 8202 superadas, 2 omitidas, 1 fallo esperado (`test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`: el documento de evidencias aún no estaba regenerado). Tras `evidencias_plan_a.py --ejecutar`, `tests/test_fase4_mapa.py` 23/23 |
| A-Forex, B | sin tocar | sin tocar |

La línea base de A (607) se respeta con holgura.

## Criterio de aceptación → prueba

| Criterio | Prueba (`tests/test_t178.py`) |
| --- | --- |
| CA-1 | `test_pb19_seis_ct05_sin_ord_y_la_cola_queda_reordenada_por_prioridad`, `test_pb19_dos_ciclos_con_el_analizador_saturado_reordenan_avisan_y_proponen_tipo_3`; y las de antes (`test_fase4_huecos.py::test_pb19_…`, `test_unitarias.py::test_ht04_y_ht06_y_ht08`, `test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos`) |
| CA-2 | `…_seis_ct05_sin_ord_y_la_cola_queda_reordenada_por_prioridad`, `…_el_orden_es_estable_y_una_cola_ya_ordenada_no_cambia`, `…_la_cola_sin_detalle_se_cuenta_y_el_ct01_baja_tras_la_c6_no`, `…_sin_saturacion_no_hay_car_ni_reordenacion` |
| CA-3 | `…_aviso_al_coordinador_solo_de_los_agentes_del_camino_de_la_entrega`, `…_el_coordinador_lee_su_aviso_en_ha` |
| CA-4 | `…_la_primera_saturacion_no_propone_y_la_segunda_en_otro_run_si`, `…_dos_lecturas_del_mismo_run_no_son_una_repeticion`, `…_la_propuesta_abierta_no_se_duplica_y_tras_rechazarla_hace_falta_otra_repeticion`, `…_la_repeticion_es_por_agente_y_cuenta_los_car_anteriores_a_t178`, la de integración con dos ciclos |
| CA-5 | `…_una_orden_invalida_se_rechaza_sin_tocar_la_cola` (4 casos), `…_una_orden_ya_en_la_cola_se_rechaza_y_retirar_la_saca`, `…_un_agente_con_estado_nunca_recibe_ord_ni_con_umbral_cero` |
| CA-6 | suite completa, gates y cuotas (abajo); `evidencias_plan_a.py --pb PB-19` → «Superada»; `--ejecutar` → 254 de 254 citadas superadas |

## Regresiones y mutantes

- Sin la corrección las pruebas nuevas fallan: en `origin/develop` no existe `bloque_a/carga.py` ni `Monitor.encolar(…, ordenes=)`; y cada pieza tiene su mutante muerto.
- `.docs/tickets/T-178/mutantes.py`: 27 mutantes (orden de la cola, validaciones, aviso, repetición, re-armado, lectura del Coordinador, la llamada del ciclo), **27 muertos, 0 vivos**.

## Ciclo mock

`bloque-a --cliente mock … backtest --desde 2024-01-05 --hasta 2024-03-29` (con `python -m bloque_a.cli` desde el worktree): rc 0, con `senales.csv`, `pronosticos.csv`, `metricas.json`. Ningún CAR- en ese backtest (no hay saturación), así que HA no cambia en el caso normal.

## Gate

Ejecutados por separado (la suite de A ya se pasó completa una vez; A-Forex y B no se tocan):

- corpus-integridad, nombres-nfc, secrets, refs-vivas: OK.
- ruff (A + A-Forex + B, como el gate): 2813 (cuota 2813, sin subir; `carga.py`, `ht08_monitor.py` y `test_t178.py` limpios).
- mypy de A: 102 (cuota 102, sin subir; ningún error en los ficheros tocados).

Comandos: los de `analisis-tecnico.md`, más `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` y, desde `bloque_a/11_Ejecutor`, `../../.venv/bin/python -m pytest -q -p no:cacheprovider .`.

## Ronda r02 (QA r01 NO APTO)

| Suite | r01 | r02 |
| --- | --- | --- |
| `tests/test_t178.py` | 17 | 35 (+6 casos del `parametrize` de órdenes inválidas por H-03 y H-04, +12 pruebas `test_r02_…`) |
| Bloque A, recogidas | 8205 | 8223 |
| `test_t178`, `test_fase4_huecos`, `test_t53_evaluacion_y_almacen`, `test_unitarias` | 117 passed | 135 passed |
| `test_fase4_mapa.py` | 23 | 23 (el mapa y las evidencias no cambian en la r02: los nombres citados son los mismos) |

- La suite completa de A no se ha vuelto a pasar en la r02: se pasó en la r01 y el cambio no sale de `ht08_monitor.py` y `carga.py`, cuyos usuarios son los cuatro ficheros de arriba.
- **Mutantes:** 36, todos muertos. Son los 27 de la r01, con M25 ajustado a `CERRADAS` y M19 a la condición nueva, y 9 nuevos, de M28 a M36, uno o más por hallazgo.
- **`revisores/r01_ataques.py` sin cambiar:** 11 de 12 entradas OK. Dan OK A1, A2 (×3), A4, A5, A5b, A6, A7, A8 y A9. El fallo es «a3 (excepción)»: el primer `encolar` de A3 se rechaza, como pide la corrección de H-03, fuera del `try` del script, y A3b no llega a ejecutarse. Detalle en `analisis-tecnico.md`; los rechazos de A3 y A3b los comprueba el `parametrize`.
- **Ciclos mock:** `ciclo`, `peticion --json ejemplos/peticiones/peticion_ad_hoc.json`, `evaluar` y `estado` (`--as-of 2026-06-05`), más el backtest 2024-01-05 → 2024-03-29: los cinco con rc 0. HA no tiene ningún CAR- (no hay saturación).
- **Gates:** corpus-integridad, nombres-nfc, secrets y refs-vivas OK; ruff 2813 (cuota 2813) y mypy de A 102 (cuota 102).
- **Rebase:** `origin/develop` no ha avanzado desde `51d68f5`; no hace falta.
