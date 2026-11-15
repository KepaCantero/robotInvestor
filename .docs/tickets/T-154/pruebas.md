# T-154 · Pruebas

Copia: git worktree en el scratchpad sobre `1ccffd5`, con `.venv` enlazado. Sin red, sin la API y sin coste (el SDK real sobre `httpx2.MockTransport` o SDK dobles). «Antes» es `git archive 1ccffd5 bloque_a`. El ticket se abrió como T-153 y quien coordina lo renumeró a T-154 a mitad del trabajo (T-153 es de otra sesión): la suite completa y los primeros mutantes corrieron con los nombres viejos (`test_t153.py`, `mutantes_t153.py`), con el mismo contenido.

| Suite | Antes (`1ccffd5`) | Después |
| --- | --- | --- |
| Suite completa de A (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6557 passed, 2 skipped (QA r01 de T-151) | **6624 passed, 2 skipped**, exit 0, 32 min 33 s (con mutantes en paralelo) |
| `tests/test_t154.py` (nuevo) | — | 67 |
| `tests/test_t151_reintentos.py` | 23 | 23 (la línea del 500 con `x-should-retry: false` corregida; casos de Q09 y Q10 añadidos a dos pruebas) |
| `test_t146_presupuesto.py` · `test_t148.py` · `test_t145.py` · `test_t88_consumo.py` · `test_t129_modo_sombra.py` · `test_fase4_huecos.py` · `test_integracion*` · `test_fase3_goldens.py` | 42 · 25 · 39 · 15 · 10 · 53 · 15 · 102 | iguales, en verde, con el código final (una a una); `python tests/goldens_ct.py`: «goldens de contratos: coinciden» |

Tras la suite completa solo cambiaron, en el código, la línea de `grupo` de `Bloque._cargar` (vuelve al texto de antes; mismo comportamiento) y los comentarios T-153 → T-154. Con el código final se repitieron las suites citadas, los goldens, los gates, las cuotas, `r01_02` y los mutantes que podían verse afectados (ver abajo).

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 (H-01) | `test_t154_h01_un_5xx_que_no_se_reintenta_se_carga_por_su_peor_caso` (501, 505, 520, 500 y 503 con `x-should-retry: false`), `test_t154_h01_lo_que_el_servidor_rechaza_sin_ejecutar_sigue_sin_cargarse` (529, 529 y 429 con `false`, 400, 404), `test_t154_h01_la_clasificacion_de_los_5xx_sale_de_la_configuracion`; `test_la_clasificacion_de_los_errores`; `r01_01` X9 | OK; X9: «cargado sin respuesta 1» en los cuatro (antes 0) |
| CA-2 (H-02) | `test_t154_h02_la_peticion_sin_respuesta_de_ag19_queda_en_f5`, `…_sin_nada_de_ag19_que_declarar_no_hay_entrada`, `…_los_cierres_y_excesos_tras_el_run_tambien`; `r01_02 … --veces 2` (DIV): F5 lleva el RUN (20,468 UC sin respuesta) y `PRESUPUESTO_F9` `F5F9-2024-0001` con AG-19 (4,2092), suma 24,6772 = lo cargado en total; `comparar_ciclos.sh`: F5 sin campos distintos ni entradas nuevas | OK |
| CA-3 (H-03) | `test_t154_h03_con_un_fallo_el_reparto_no_depende_del_orden` (y, sin la marca, el escenario sí depende del orden), `…_un_grupo_sin_fallos_reparte_como_antes`, `…_el_grupo_de_un_analista_en_v6`, `…_en_el_ciclo_la_peticion_sin_respuesta_marca_su_grupo`; `r01_02` (abajo) | OK; IGUAL en todos los órdenes |
| CA-4 (H-04) | `test_t154_h04_un_retry_after_no_finito_negativo_o_cero_no_vale` (18 casos), `…_el_tope_de_la_espera_del_servidor`, `…_si_el_servidor_pide_esperar_de_mas_no_se_reintenta`, `…_x_should_retry_no_distingue_mayusculas` (18), `…_retry_after_con_el_nombre_en_mayusculas`, `test_t154_las_claves_nuevas_invalidas_fallan_cerrado` (10); casos en `test_t151_reintentos.py`; `r01_03_mutantes_qa.py` | OK; **16/16** (Q09 y Q10 muertos; antes 14/16); `r01_01` X10: «retry-after 100000 → espera None» |
| CA-5 (H-05) | Lectura: CA-7 de `.docs/tickets/T-151/README.md`, sus `analisis-tecnico.md` y `pruebas.md`; INC-T129-01 (dos líneas); S5 de `estimar_coste_ciclo_a.py` (salida impresa) | OK; `grep "reintentos del SDK"` en `docs/incidencias.md`, el estimador y el README del ejecutor: nada |
| CA-6 | `mutantes_t154.py` · `mutantes_t151.py` · `r01_03` de T-151 · `mutantes_t146.py` · `r01_05` de T-146 · `r02_02` de T-146 · `r02_02` de T-148 | ver «Mutantes» |
| CA-7 | Esta página | OK |

## Regresiones

Cada corrección tiene su mutante en `.docs/tickets/T-154/mutantes_t154.py` y todos mueren (las pruebas fallan sin la corrección): P01–P03 y P09 (H-01: sin la rama de los 5xx, un 529 cargado, el umbral escrito a mano, sin validar), P04–P08 (H-04: sin tope, el tope sin efecto, nombre o valor de la cabecera con mayúsculas o espacios, sin validar), P10–P13 (H-03: el grupo marcado reparte lo visto, no se limpia la marca, no se marca, el grupo V6 equivocado), P14–P18 (H-02: sin la entrada F9, la marca tras la auditoría, el tramo desde el principio, la entrada sin nada que declarar, la entrada con el id del RUN). Además, la prueba unitaria de H-03 comprueba que sin la marca el mismo escenario da repartos distintos según el orden, y contra `1ccffd5` el `r01_02` con caché daba DISTINTO (firmas `8426771dbee9` y `c95463da2b97`).

## Mutantes (copias desechables de `bloque_a`, `.docs` y `tools` del árbol de trabajo, borradas al acabar)

| Script | Copia | Resultado |
| --- | --- | --- |
| `.docs/tickets/T-154/mutantes_t154.py` | `t153_mut` (nombre viejo) y, con el código final, `t154_mut` | **18/18** · 18/18 |
| `.docs/tickets/T-151/mutantes_t151.py` | `t151_mut` (con las pruebas ampliadas) | **18/18** |
| `.docs/tickets/T-151/revisores/r01_03_mutantes_qa.py` | `qa24_t151_mut` | 14/16 con solo `test_t154.py` (el script pasa `test_t151_reintentos.py` y `test_t146_presupuesto.py`); con los casos añadidos a `test_t151_reintentos.py`, **16/16** |
| `.docs/tickets/T-146/mutantes_t146.py` | `t146_mut`; con el código final, otra `t146_mut` | primera pasada: M07 «NO APLICA» (había partido la línea de `cargar_con_prima` que cita); con la línea restaurada, **35/35** |
| `.docs/tickets/T-146/revisores/r01_05_mutantes_qa.py` | `qa19_mut_t154` (código final) | **12/12** |
| `.docs/tickets/T-146/revisores/r02_02_mutantes_qa.py` | `qa21_t146_mut` | **10/10** |
| `.docs/tickets/T-148/revisores/r02_02_mutantes_qa.py` | `qa21_t148_mut` | **5/5** |

## Scripts del revisor y medidas (contra esta copia)

| Orden (desde la raíz) | Resultado |
| --- | --- |
| `.venv/bin/python -I .docs/tickets/T-151/revisores/r01_01_reintentos_unidad.py bloque_a/11_Ejecutor` | **9/9 OK**, 3 OBS (X9 y X10 ya con lo nuevo) |
| `… r01_02_ciclo_reintentos.py bloque_a/11_Ejecutor <tmp> --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo\|inverso --veces 3` | **IGUAL** (`dd00a82d0692`) en los dos órdenes y entre ellos (antes DISTINTO); repetido con el código final (`--veces 2`): igual |
| `… --tipos <12> --hilos 6 --cache --orden directo\|inverso --veces 2` | **IGUAL** (`6d904b8a497b`) en las cuatro |
| `… --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo\|inverso --veces 2 --fallo-escribe ninguno` | IGUAL (`dd00a82d0692`) |
| `… --veces 2` (DIV) · `--tipos RV,RF,DIV,MP --hilos 4` · `--sin-tipos` | IGUAL y sin violaciones · sin violaciones (consumido 99,8063 = 51,5926 + 48,2138) · sin violaciones (COMÚN 6,7019 en F5 = resultado) |
| `.venv/bin/python -I .docs/tickets/T-146/revisores/r02_01_arreglos_r02.py bloque_a/11_Ejecutor <tmp>` | **28/28 OK** |
| `bash .docs/tickets/T-146/comparar_ciclos.sh <1ccffd5>/bloque_a/11_Ejecutor bloque_a/11_Ejecutor <tmp> .venv/bin/python` | solo difieren `bt/salida/consumo.csv` y `doce/estado/cache_resultados.jsonl` (cambian también entre dos pasadas iguales); F5 sin campos distintos en ningún RUN |
| `cd bloque_a/11_Ejecutor && PYTHONPATH=$PWD ../../.venv/bin/python ../../.docs/scripts/medir_consumo_a.py <tmp>/m_div 2024-03-29` y `.venv/bin/python .docs/scripts/estimar_coste_ciclo_a.py <tmp>/m_div` | 8 llamadas; cota 28,04 USD (presupuesto 46,08): sin cambios; S5 con el texto nuevo |

## Gate

- `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py`: exit 0 los cuatro (con el árbol final); corpus **695** archivos coinciden.
- Cuotas, desde la raíz: ruff (tres ejecutores) **2831** (cuota 2831); mypy de A **109** (cuota 109). `tools/cuotas.txt` no se toca.
- No se ejecutó `./tools/check_all.sh` entero (A-Forex y B no se tocan): los gates ligeros, las cuotas y la suite de A, sí.
