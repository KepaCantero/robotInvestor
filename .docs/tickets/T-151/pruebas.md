# T-151 · Pruebas

Copia: git worktree en el scratchpad (`t151`), sobre `e1a8f87`, con `.venv` enlazado. Sin red, sin la API y sin coste (el SDK real sobre `httpx2.MockTransport` o SDK falsos). Para comparar, `git archive` de `e1a8f87` (antes de T-151) y de `19f3f3b` (antes de T-146).

| Suite | Antes (`e1a8f87`) | Después |
| --- | --- | --- |
| Suite completa de A (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6444 + 2 omitidas (6476 − 32 nuevas) | **6476 passed, 2 skipped**, exit 0, 35 min 29 s (con mutantes en paralelo) |
| `tests/test_t146_presupuesto.py` | 35 | 42 (H-11 ×3, H-12, V01, V04, V05) |
| `tests/test_t148.py` | 23 | 25 (W04, W05) |
| `tests/test_t151_reintentos.py` | — | 23 (H-09) |
| `test_t145.py`, `test_t88_consumo.py`, `test_fase4_huecos.py`, `test_integracion*`, `test_fase3_goldens.py` | en verde | en verde (dentro de la suite completa); `python tests/goldens_ct.py`: «goldens de contratos: coinciden» |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 (H-11) | `test_t151_h11_la_continuacion_de_una_generacion_que_busco_no_observa`, `test_t151_h11_con_el_cliente_real_la_ultima_continuacion_no_observa`, `test_t151_h11_la_reparacion_tras_buscar_si_observa`; R9 y R3 de `T-146/revisores/r02_01_arreglos_r02.py` | OK (R9: factor 0,00; R3: 1,80 donde debe) |
| CA-2 (H-12) | `test_t151_h12_sin_tipos_lo_de_ag20_esta_en_f5` (también sin sitio: el cierre de AG-20 en el RUN); R7 de `r02_01` | OK (R7: gastado 4,551 = en las bolsas de F5 4,551) |
| CA-3 (H-13) | Lectura: CA-1 de `.docs/tickets/T-146/README.md`, «Límites declarados» y ronda T-151 de INC-T146-01; R8 de `r02_01` | OK |
| CA-4 | `T-146/revisores/r02_02_mutantes_qa.py` (copia `qa21_t146v_mut`) · `T-148/revisores/r02_02_mutantes_qa.py` (copia `qa21_t148w_mut`) | **10/10** (antes 7/10) · **4/5**: W04 y W05 muertos; vive W02, equivalente (cada bolsa tiene un solo papel con búsqueda en `LLAMADAS_POR_TIPO`; lo dijo la QA r02) |
| CA-5 (H-09) | `tests/test_t151_reintentos.py`: la regla sale de la configuración y `crear_cliente` crea el SDK con `max_retries=0`; regla inválida (8 casos) y máximo inválido (3) fallan cerrado; esperas (dobla hasta la máxima, `retry-after-ms`, `retry-after`, fecha no interpretada); clasificación (timeout, conexión, 529, 429, 500, 400, `x-should-retry`, error ajeno, sin regla); con el SDK real (con `max_retries=5` a propósito): 529 ×2 → 3 peticiones HTTP, cada una con su reserva y ninguna cargada; timeout → cargado por su peor caso y en `sin_respuesta`; 500 hasta agotar → 5 peticiones cargadas, `error_proveedor`; 400 no se reintenta; el reintento que no cabe no sale; 529 en una continuación; sin regla no reintenta; `absorber` pasa lo de C5; en el ciclo, `peticiones_sin_respuesta` en F5 y lo de AG-05 en la bolsa DIV, sin pasar de su límite | 23 passed |
| CA-6 | `.docs/tickets/T-146/mutantes_t146.py` (copia `t146_mut_t151`) · `T-146/revisores/r01_05_mutantes_qa.py` (`qa19_mut_t151`) · `.docs/tickets/T-147/mutantes.py --ticket T-148` (`t147_mut_t151`) · `.docs/tickets/T-151/mutantes_t151.py` (`t151_mut`) | **35/35** · **12/12** · **13/13** (M25–M37, «0 vivos») · **18/18** |
| CA-7 | Ver abajo (scripts r01/r02, `comparar_ciclos.sh`, gates, cuotas) | OK |

## Regresiones

Cada corrección tiene su mutante en `mutantes_t151.py`, y todos mueren con las pruebas nuevas (es decir, las pruebas fallan sin la corrección): N01/N02 (H-11: se vuelve a observar en la continuación), N03 (H-12: `_run_sin_analisis` sin `pres_c5`), N04–N18 (H-09: el SDK con sus reintentos, un SDK recibido sin `with_options`, cobro posible soltado o no cobrado cargado, `cerrar` sin cargar, reintento sin reserva, sin reintentos, 429/529 cobrados, espera doblada desde el principio, F5 sin `peticiones_sin_respuesta`, `absorber` sin ellas, validación, `x-should-retry`, `retry-after`, sin regla). V01, V04 y V05 (QA r02 de T-146) y W04 y W05 (QA r02 de T-148) son los mutantes del revisor, que ahora mueren. Contra el código de `e1a8f87`, `r02_01` daba VIOLA en R7 y R9 (informe de la QA r02).

## Scripts del revisor (contra esta copia)

| Orden (desde la raíz) | Resultado |
| --- | --- |
| `.venv/bin/python -I .docs/tickets/T-146/revisores/r02_01_arreglos_r02.py bloque_a/11_Ejecutor <tmp>` | **28/28 OK** (en la r02, 26/28: R7 y R9 ahora OK) |
| `… r01_01_reserva_unidad.py bloque_a/11_Ejecutor` | 10/12, como en la r02 (U2 hace a mano el orden viejo; U3 es la salvedad de la lectura a 0) |
| `… r01_02_ciclo_sdk_hostil.py bloque_a/11_Ejecutor <tmp>` (solo DIV) | DIV 25,355 / 25,355; suma = gastado 57,316; sin violaciones |
| `… --tipos <12> --hilos 6 --lectura 0 / 3000 / 6000` | AG-10: 18 / 18 / 15 (+1 AG-11); sin violaciones (igual que la r02) |
| `… --tipos <12> --hilos 6 --lectura 6000 --factor 1.6` | pasan DIV, IDX, MP, RV y TCV (la salvedad del CA-1 de T-146, igual que la r02) |
| `… --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo|inverso --veces 2` | IGUAL en los dos órdenes y entre ellos (firma `fce20f7854fb`; con `e1a8f87`, `20ad04339dc9`: la única diferencia, comprobada campo a campo, es el texto del motivo de los cierres, «reparación, continuación o reintento») |
| `… r01_03_c5_con_escala.py bloque_a/11_Ejecutor <tmp>` | OK: COMÚN 4,551 / 5,882 |
| `… r01_04_t88_h13_absoluto.py <19f3f3b> bloque_a/11_Ejecutor` (y `--compartido`) | IGUAL (y DISTINTO a propósito), como en la r02 |
| `PYTHONPATH=bloque_a/11_Ejecutor .venv/bin/python -I .docs/tickets/T-148/revisores/r01_01_tope_y_cota_con_t146.py <m_div> <m_12> <doce.yaml> <tmp>` | A 6 OK, B 4 OK, D 4 OK; C «HALLAZGO» como en la r02 (la salvedad declarada de la lectura) |
| `.venv/bin/python -I .docs/tickets/T-148/revisores/r02_01_peso_y_textos.py <m_div> <m_12> <doce.yaml> <tmp>` | 0 hallazgos |
| Medidas (`medir_consumo_a.py` con `PYTHONPATH=$PWD` desde `bloque_a/11_Ejecutor`) y `estimar_coste_ciclo_a.py` | 28,04 y 46,08 USD (y 248,02 con `--sin-t146`); pesos 0,40 / 0,08 y 0,96 / 4,80: sin cambios |
| `bash .docs/tickets/T-146/comparar_ciclos.sh <e1a8f87> bloque_a/11_Ejecutor <tmp> .venv/bin/python` | solo difieren `bt/salida/consumo.csv` y `doce/estado/cache_resultados.jsonl` (cambian también entre dos pasadas iguales); F5 sin campos distintos en ningún RUN |

## Gate

- `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py`: exit 0 los cuatro; corpus **695** archivos coinciden.
- Cuotas, desde la raíz: ruff (tres ejecutores) **2831** (cuota 2838; −7 por el `import typing` sin usar de `orquestacion.py`); mypy de A **109** (cuota 109). `tools/cuotas.txt` no se toca.
- No se ejecutó `./tools/check_all.sh` entero (A-Forex y B no se tocan; los gates ligeros, las cuotas y la suite de A, sí).
