# T-169 · Pruebas

Todo con el cliente simulado (`MockClient`), sin red ni coste, con el reloj del almacén fijado (`AS_OF` 2026-06-05).

| Suite | Antes (`3533cb7`, T-162) | Después |
| --- | --- | --- |
| Bloque A (`bloque_a/11_Ejecutor`, `pytest -q`) | 6919 recogidas | 6946 recogidas (las 27 primeras de T-169; la 28.ª, `test_h02_la_pendiente_se_construye_con_la_fecha_de_su_consulta`, se añadió después y pasa aparte): 6929 pasan, 2 omitidas y 15 fallan (1 h 9 min, con carga): las 14 de goldens de T-162 y `test_fase4_mapa.py::test_h05_…`, que pasa tras regenerar las evidencias. Después, `test_fase4_mapa.py` + T-169 (28) + T-162 (22): 73 pasan. `test_t102_filtro` no falló esta vez |
| `tests/test_t169_hallazgos_t162.py` (nueva) | — | 28 pasan; con el código de T-162, 21 de las 27 primeras fallan (las de H-01 a H-03) |
| `tests/test_t162_respuesta_final.py` | 22 pasan | 22 pasan (tres ajustadas al diseño nuevo, ver `analisis-tecnico.md`) |
| `r01_01_sondas.py` del revisor de T-162 | 11 pasan y 2 xfail estrictos | 10 pasan; las 2 `test_s02b_*` dan XPASS(strict) (H-03 corregido) y `test_s08_*` falla porque afirmaba lo que H-02 corrige (F5 no guardaba la provisional) |
| Goldens `tests/test_fase3_goldens.py` | 14 fallan por `formas_flujos_mock.json` (T-162, sin re-congelar) | igual: el generado es byte a byte el de T-162 |

## Criterio de aceptación → prueba

| Criterio | Prueba (en `tests/test_t169_hallazgos_t162.py`) |
| --- | --- |
| CA-1 (H-01) | `test_h01_un_fallo_de_integridad_para_la_consulta_como_en_la_base` (la sonda del bloque 4 de `r01_02_procesos_y_base.py`: sello de F2 manipulado con el bloque abierto → `ValueError` «Fallo de integridad en el sello de F2», sin QRY en F5, sin CT-03 RETORNO, sin HERRAMIENTA); `test_h01_un_error_de_control_del_run_se_relanza` (6 clases); `test_h01_un_error_corriente_tras_registrar_el_run_sigue_dando_fallido` |
| CA-2 (H-02) | `test_h02_la_provisional_queda_en_f5`; `test_h02_enviar_rechaza_una_provisional_inventada_o_sin_registrar`; `test_h02_la_siguiente_consulta_envia_la_final_pendiente`; `test_h02_el_siguiente_ciclo_envia_la_final_pendiente`; `test_h02_un_bloque_reabierto_envia_la_final_pendiente`; `test_h02_la_final_recuperada_es_la_que_habria_salido` (una semana después, igual salvo `timestamp`); `test_h02_una_pendiente_que_la_mensajeria_rechaza_se_aparta_una_vez`; `test_h02_un_error_que_no_es_un_rechazo_para_la_consulta_y_no_aparta` |
| CA-3 (H-03) | `test_h03_un_id_de_otro_tipo_en_las_evidencias_no_se_cita` (RUN-, HIT- y PRG- existentes); `test_h03_un_id_de_otro_tipo_en_las_tendencias_no_se_cita`; `test_h03_un_run_que_no_lanzo_la_consulta_no_se_cita` (la sonda s10); `r01_01_sondas.py::test_s02b_*` en XPASS |
| CA-4 (H-04) | `test_h04_la_confianza_es_la_mas_baja_de_las_citadas` (M01), `test_h04_una_confianza_no_valida_cuenta_como_especulativo` (M16), `test_h04_los_prg_son_solo_los_de_su_run` (M02), `test_h04_un_run_parcial_da_entregado_parcial` (M11, M12) y `test_h01_un_error_corriente_tras_registrar_el_run_sigue_dando_fallido` (M07) |
| CA-5 | T-162, goldens, cuotas, gates y suite (abajo) |

## Mutantes del revisor (`.docs/tickets/T-169/scripts/mutantes_t169.py`)

| Mutante | Resultado con las pruebas de T-169 |
| --- | --- |
| M01 confianza más alta | MUERTO (`test_h04_la_confianza_es_la_mas_baja_de_las_citadas`) |
| M02 PRG- de cualquier RUN- | MUERTO (`test_h03_un_id_de_otro_tipo_en_las_evidencias_no_se_cita[PRG-2026-0001]`; también lo mata `test_h04_los_prg_son_solo_los_de_su_run`) |
| M07 sin buscar el RUN- registrado | MUERTO (`test_h01_un_error_corriente_tras_registrar_el_run_sigue_dando_fallido`) |
| M11 ENTREGADO_PARCIAL → COMPLETO | MUERTO (`test_h04_un_run_parcial_da_entregado_parcial`) |
| M12 RUN- PARCIAL como completo | MUERTO (`test_h04_un_run_parcial_da_entregado_parcial`) |
| M16 confianza no válida → establecido | MUERTO (`test_h04_una_confianza_no_valida_cuenta_como_especulativo[alta]`) |

El resto de los mutantes del revisor, contra T-169 y T-162: M04, M05, M06, M08, M09, M10, M13, M14 y M17–M23 y M25 MUERTO; M15 VIVO (equivalente, declarado así por el revisor). M03 y M24 ya no se aplican (su texto cambió con T-169): sus equivalentes sobre el texto nuevo, M03b y M24b, mueren. Los 16 propios de T-169 (`--propios`: N01–N15 más esos dos; H-01, H-02 y H-03 deshechos uno a uno) mueren todos; N08 (pendiente con la fecha de hoy) sobrevivió a la primera tanda y lo mata la 28.ª prueba

## Regresiones

Con `respuesta_final.py` y `orquestacion.py` de `3533cb7` (y las pruebas de ahora), `tests/test_t169_hallazgos_t162.py` da
**21 fallan y 6 pasan**: fallan todas las de H-01, H-02 y H-03; pasan las 6 de H-04, que no son regresiones sino pruebas que matan
mutantes (sin los mutantes, el código de T-162 ya las cumplía). Restaurado el código, pasan las 27.

## Gate

| Comprobación | Resultado |
| --- | --- |
| `tools/refs_vivas.py`, `tools/secrets_scan.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py` | los cuatro en verde (código de salida 0); el corpus, 695 archivos íntegros |
| ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2821 (cuota 2821) |
| mypy de A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 (cuota 109) |
| `tests/goldens_ct.py` | 1 diferencia, `formas_flujos_mock.json`, idéntica a la de T-162 (huella `6b7339b2…6c24`) |
| `.docs/scripts/evidencias_plan_a.py` (comprobación y `--ejecutar`) | 67 pruebas del plan, 203 automáticas citadas, todas existen; `--ejecutar`: 203 de 203 superadas; PB-07 sigue «Superada» (33 filas «Superada») |
| `./tools/check_all.sh` completo | no se ejecuta: los goldens siguen en rojo hasta el re-congelado coordinado de T-162 |

## Comandos usados

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t169_hallazgos_t162.py tests/test_t162_respuesta_final.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rX ../../.docs/tickets/T-162/revisores/r01_01_sondas.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider          # suite completa de A
../../.venv/bin/python tests/goldens_ct.py
cd ../..
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/python .docs/scripts/evidencias_plan_a.py && .venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
.venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py .docs/tickets/T-162/revisores/r01_03_mutantes.py <tmp>/t169_mut M01 M02 M07 M11 M12 M16
```

## Ronda r02 (hallazgos de la QA r01 de T-169)

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t169_r02.py` (nueva) | 8 pasan. Con el `respuesta_final.py` de la r01 (`ab10556`) fallan las 4 de H-01 a H-03; las 3 de H-04 pasan con los dos, porque solo matan mutantes. La 8.ª (lista de pendientes vieja) se añadió para matar R04 |
| `tests/test_t169_hallazgos_t162.py` y `tests/test_t162_respuesta_final.py` | 28 y 22 pasan. Una de la r01 pasa a comprobar un error de control, que es lo que ahora para (ver `analisis-tecnico.md`) |
| `revisores/r01_01_sondas.py` (QA r01 de T-169) | 5 pasan y las 3 xfail estrictas (p04, p05 y p06) dan XPASS(strict): H-01, H-02 y H-03 corregidos |
| `revisores/r01_02_procesos_y_base.py` (base `3533cb7`) | 0 fallos: con 4 procesos, una pendiente enviable sale una vez y una rechazada se aparta una vez, con una incidencia; comparaciones con la base, en verde |
| Mutantes del revisor de T-169 (`scripts/mutantes_t169.py revisores/r01_03_mutantes.py`) | Q01, Q06, Q07, Q08 y Q10 MUERTO; Q02, Q03, Q04, Q05 y Q09 ya no se aplican porque su texto cambió en la r02, y sus versiones sobre el texto nuevo (`--propios`: Q02b, Q03b, Q04b, Q05b y Q09b) mueren todas |
| Mutantes de la r02 (`--propios`) | R01 (ReplayFaltante fuera), R02 (cualquier error para), R03 (sin transacción) y R04 (sin volver a mirar si está apartada) MUERTO |
| Goldens | `formas_flujos_mock.json` generado, byte a byte el de T-162; ningún otro cambia |
| ruff · mypy de A | 2821 (cuota 2821) · 109 (cuota 109) |
| Gates ligeros | `refs_vivas`, `secrets_scan`, `nfc_check` y `corpus_integridad` (695), código de salida 0 |
| Mapa del plan | 67 pruebas, 203 citadas, todas existen (sin cambios en la r02) |
| Suite completa de A | 6955 recogidas (relanzada una vez tras el reinicio del contenedor, que cortó la primera al 40 %): 6939 pasan, 2 omitidas y 14 fallan, todas de `test_fase3_goldens.py` por `formas_flujos_mock.json` de T-162 sin re-congelar (39 min). `test_t102_filtro` no falló |

## Ronda de cierre (hallazgos de la QA r02 de T-169)

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t169_r02.py`, `tests/test_t169_hallazgos_t162.py` y `tests/test_t162_respuesta_final.py` | Pasan las 63: las 58 de antes y 5 nuevas (`test_cierre_h02_*` ×3, `test_cierre_h01_*` ×2), en 88 s |
| Las 2 de H-01 con el `respuesta_final.py` de `d845e3c` (orden antiguo: marca y luego incidencia) | Fallan las dos; con el orden nuevo pasan |
| `revisores/r02_01_sondas.py` y `revisores/r02_03_sondas.py` | 15 pasan; `test_a07_*` y `test_b01_*` dan XPASS(strict), es decir, H-01 corregido. En `b01`, tras reparar `contadores.json`, la final sale en el ciclo siguiente (sin marca ni incidencia, sin pendientes) |
| Mutante S01 (`--propios`, copia desechable `cierre_t169_mut` desde el árbol de trabajo) | MUERTO por `test_cierre_h02_un_error_corriente_con_el_almacen_roto_para_y_no_aparta[KeyError]` |
| R02 (`--propios`) y S03, S04 y S05 (`revisores/r02_02_mutantes.py`), sobre el `_apartar` reordenado | MUERTO los cuatro |
| ruff | `All checks passed!` en `respuesta_final.py`, `test_t169_r02.py` y `mutantes_t169.py`. Total de los tres ejecutores: 2821, igual que en `d845e3c` (delta 0). La cuota 2813 es la de `develop`, que ya incluye las limpiezas de T-161, T-163 y T-165, posteriores a esta rama; al integrar queda la de `develop` |
| mypy de A | 109 (cuota 109) |
| Suite completa de A y gate | No se pasan: hay otros agentes en la máquina. Quedan para la integración, con el re-congelado de `formas_flujos_mock.json` de T-162 |

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t169_r02.py tests/test_t169_hallazgos_t162.py tests/test_t162_respuesta_final.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rxX ../../.docs/tickets/T-169/revisores/r02_01_sondas.py ../../.docs/tickets/T-169/revisores/r02_03_sondas.py
cd ../..
.venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py --propios <tmp>/cierre_t169_mut S01 R02
.venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py .docs/tickets/T-169/revisores/r02_02_mutantes.py <tmp>/cierre_t169_mut S03 S04 S05
```
