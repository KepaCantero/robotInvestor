# T-205 · Pruebas

| Suite | Antes (`origin/develop` 358576c3) | Después |
| --- | --- | --- |
| Bloque A (`pytest bloque_a/11_Ejecutor`, recogidas) | 8546 | 8571 (+25 de `tests/test_t205_clase_seguimiento.py`; `test_t201_cuotas.py` mantiene sus casos) |
| B | sin tocar | sin tocar |

La línea base de A (607) se respeta con holgura.

## Criterio de aceptación → prueba

| Criterio | Prueba (`tests/test_t205_clase_seguimiento.py`, salvo que se diga otra cosa) |
| --- | --- |
| CA-1 | `test_b_agente_falla_con_una_clase_que_no_es_uno_de_los_doce_tipos` (7 casos: «XYZ», `""`, None, `"rv"`, `" RV"`, 3, `["RV"]`), `test_b_agente_da_el_analista_de_cada_uno_de_los_doce_tipos`, `test_t201_cuotas.py::test_b_agente_da_el_analista_de_su_clase_o_falla` (actualizada) |
| CA-2 | `test_alta_con_clase_no_admitida_se_rechaza_sin_escribir_nada_mas_que_su_inc` (desconocida, vacía, None, ausente): solo cambian HA (un INC-), el contador `INC-2026` y los sellos; ni mensajes ni encargo. `test_alta_con_clase_buena_sigue_igual_y_cada_alta_rechazada_deja_su_inc`, `test_alta_de_una_opp_que_no_esta_en_f3_sigue_siendo_keyerror_sin_inc`, `test_alta_directa_tambien_comprueba_la_clase` |
| CA-3 | `test_c6_salta_la_opcion_con_clase_no_admitida_y_el_resto_del_ciclo_sigue_igual` (desconocida, vacía, None), con un gemelo sin la opción estropeada: los otros dos encargos dan los mismos resultados, informes JSON byte a byte, mensajes CT-05, CT-06 y CT-24 (salvo `msg_id`, hora y carpeta) y F11. `test_c6_de_un_encargo_cuya_opp_no_esta_en_f3_tambien_se_salta`, `test_c6_forzado_tambien_se_salta` |
| CA-4 | `test_c6_una_sola_incidencia_mientras_nada_cambie` (mismo día, día siguiente, F3 sin tocar la clase, otra clase no admitida, corregida y vuelta a estropear), `test_c6_un_inc_de_otra_fase_con_la_misma_clave_no_tapa_el_del_c6`, `test_c6_varios_procesos_a_la_vez_dejan_una_sola_incidencia` (6 procesos reales, 5 rondas; sin mensajería en el proceso, así que un CT-05 o un CT-06 daría AttributeError) |
| CA-5 | `test_c6_un_fallo_al_escribir_la_incidencia_no_deja_nada_a_medias` (todos los ficheros del estado iguales y ningún mensaje) |
| CA-6 | `test_el_defecto_de_la_qa_r01_de_t201_ya_no_se_reproduce`; las suites de seguimiento (abajo); ciclo mock y backtest; gate completo |

## Regresiones y mutantes

- **Sin la corrección fallan 22 de 24.** Se probó con `seguimiento.py` de `origin/develop`, al que solo se le añadieron los nombres `ClaseNoAdmitida` y `clase_admitida`, sin comportamiento, para que las pruebas se pudieran recoger. Las dos que pasan son de regresión y tienen que pasar igual: las doce clases buenas y la OPP- inexistente con `KeyError`. La 25.ª prueba se escribió después, para matar M22. El mutante M22 es justo quitar la condición que esa prueba comprueba.
- **`.docs/tickets/T-205/mutantes.py`: 22 mutantes, 22 muertos, 0 vivos.** Cubren `b_agente`, `clase_admitida`, las dos comprobaciones del alta, el tipo, el campo, el valor en el detalle y el escalado del INC-, el respaldo de F11, la comprobación del C6, la deduplicación y su clave, la transacción, `_seq_clase` e `incidencia_nueva`. En la primera pasada M22 sobrevivió (la deduplicación no miraba la fase); se añadió `test_c6_un_inc_de_otra_fase_con_la_misma_clave_no_tapa_el_del_c6` y en la segunda pasada murió. M16 (sin transacción) lo mata la prueba de seis procesos.
- **Suites que tocan el seguimiento**, con el cambio: `test_t201_cuotas.py`, `test_v51.py`, `test_t87_controles.py`, `test_t65_hallazgos.py`, `test_t65_qa_r01.py`, `test_t65_resto_t53.py`, `test_t174_pb61_revision_c2.py`, `test_t159_extremo_a_extremo.py` y `test_fase4_huecos.py` (con PB-66 y PB-67): **233 superadas**.
- **Reproducción de la QA r01 de T-201** (`.docs/tickets/T-201/revisores/r06_b_agente.py`):
  - En develop, «XYZ» y `""` mandan el CT-06 al AG-03, sin INC-.
  - Con T-205, las dos altas dan `ClaseNoAdmitida` con su INC- y la DIV de control sigue igual.

## Ciclo mock y backtest

El script `scratchpad/t205_mock.sh` se ejecutó en `origin/develop` 358576c3 y en esta copia. Pasos:
1. El backtest del README (`--cliente mock … backtest --desde 2024-01-05 --hasta 2024-03-29`).
2. Un ciclo C1 a 2024-03-29.
3. Un `seguimiento alta` de OPP-2024-0001.
4. Un `seguimiento ejecutar` a 2024-04-05, que da un C6 entregado (APTO, MANTENER_VIGILANCIA).

Resultado: rc 0 en los cuatro pasos en los dos árboles.
- `senales.csv`, `pronosticos.csv` y `metricas.json`: idénticos.
- La salida de los cuatro pasos, idéntica.
- F1, F2, F3, F4, F6, F10, HA, RC y la caché: idénticos byte a byte.
- F5 y F11, y los informes técnicos: solo cambian por la ruta de la carpeta de cada árbol (y los `_hash` que la incluyen).
- `consumo.csv`: solo cambia `latencia_s`, que es tiempo de reloj.

Con una clase buena, nada cambia.

## Gate y cuotas

- **ruff:** 2797, igual que la cuota. Los 3 ISC004 de `seguimiento.py` son anteriores, en líneas que no se tocan; las pruebas nuevas no suman ninguno.
- **mypy de A:** 67, igual que la cuota (`clase_admitida` devuelve `TypeGuard[str]`, así que `AGENTE_CLASE[clase]` tipa).
- **Las cuotas no bajan:** el ticket no tenía margen para hacerlo sin tocar código ajeno.
- **`./tools/check_all.sh` completo:** lanzado con `setsid nohup`, log en `scratchpad/gate_t205.log`. El resultado está en la sección siguiente.

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q tests/test_t205_clase_seguimiento.py tests/test_t201_cuotas.py tests/test_v51.py tests/test_t87_controles.py \
  tests/test_t65_hallazgos.py tests/test_t65_qa_r01.py tests/test_t65_resto_t53.py tests/test_t174_pb61_revision_c2.py \
  tests/test_t159_extremo_a_extremo.py tests/test_fase4_huecos.py
../../.venv/bin/python ../../.docs/tickets/T-205/mutantes.py .
cd ../.. && setsid nohup ./tools/check_all.sh > gate_t205.log 2>&1 < /dev/null &
```

## Resultado del gate

`./tools/check_all.sh` completo, 25-11-2026, en la copia `wip/t205`, mientras corrían otras dos sesiones: **12 de 12 en verde, 0 fallos y 0 omitidos**.
- corpus-integridad (705 archivos), nombres-nfc, yaml-configs, secrets y refs-vivas.
- ruff (2797 ≤ 2797), mypy A (67 ≤ 67), mypy A-Forex (174) y mypy B (159).
- pytest A: 8569 superadas de 8571 recogidas; las 2 restantes no son fallos, porque el gate exige que pytest salga con 0; son omitidas.
- pytest A-Forex: 68. pytest B: 176.

## Ronda de cierre de la QA r01 (25-11-2026)

Se corrigen H-01, H-02 y H-03 (`qa.md`). `seguimiento.py` no cambia.

| Pieza | Antes | Después |
| --- | --- | --- |
| `tests/test_t205_clase_seguimiento.py` | 25 | 28 |
| Bloque A, recogidas | 8571 | 8574 |
| `mutantes.py` | 22 de 22 | 25 de 25 muertos (con Q1, Q2 y Q11 del revisor) |

Las tres pruebas nuevas:
- `test_c6_una_opcion_vigente_con_clase_no_admitida_no_se_omite_cubierta_en_c1` (H-01, CA-3).
- `test_alta_con_ha_rota_sube_el_error_de_ha_y_solo_cambia_el_contador_de_inc` (H-02, CA-5).
- `test_c6_la_lectura_de_ha_y_el_inc_van_en_la_misma_transaccion` (CA-4). Es la que mata Q11 siempre; la de seis procesos solo lo ve si la carrera llega a darse.

H-03: la prueba de T-201 se llama ahora `test_b_agente_da_el_analista_de_su_clase_o_falla`, y M1 a M3 siguen muriendo con ella.

Ejecutado en esta ronda:
- **Pruebas del ticket y vecinas (las de la QA):** `test_t205_clase_seguimiento`, `test_t201_cuotas`, `test_fase3_goldens`, `test_fase4_huecos`, `test_t159_extremo_a_extremo`, `test_t174_pb61_revision_c2`, `test_t65_hallazgos`, `test_t65_qa_r01`, `test_t65_resto_t53`, `test_t87_controles`, `test_v51`, `test_v5` y `test_integracion`. **477 superadas.**
- **`mutantes.py`:** 25 de 25 muertos, Q1 y Q2 incluidos.
- **`revisores/r01_mutantes.py`:** 11 de 11 muertos, Q1, Q2 y Q11 incluidos. Se ejecutó con una copia temporal que solo cambia el nombre de la prueba de T-201 en `PRUEBAS`; con el nombre antiguo, pytest no la encuentra y todos «morirían» sin ejecutar nada. El script del revisor no se toca.
- **`revisores/r01_02_ataques.py`:** 29 PASA, 0 FALLA.
- **`revisores/r01_04_testigo.py`:** Q1 detectado por A4 y Q2 por A6, rc 0.
- **ruff de las dos pruebas tocadas:** limpio.
- **Gate completo:** no se relanza, por orden del coordinador.
