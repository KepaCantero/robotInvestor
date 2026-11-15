# T-146 · Pruebas

Copia de trabajo sobre `19f3f3b`, con el intérprete del proyecto (`/home/user/robotinvestor/.venv/bin/python`). Sin red y sin la API: el «cliente real» es `AnthropicClient` sobre un SDK falso. No se ejecutan `./tools/check_all.sh` ni la suite completa de A (lo pide quien coordina); sí las suites vecinas, los goldens, ruff y mypy como el gate.

## Recuentos

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t146_presupuesto.py` (nueva) | 0 | 22 |
| `test_integracion.py` | 15 | 15 |
| `test_unitarias.py`, `test_t87_*` (4), `test_t88_consumo.py`, `test_fase4_huecos.py`, `test_fase4_mapa.py` | 153 | 153 (dos cambiadas, comentadas «T-146») |
| `test_t113_deuda.py`, `test_t120` a `test_t126*` | 478 | 478 |
| `test_t127*` a `test_t136*`, `test_fase3_goldens.py` | 334 | 334 |
| Además: `test_t101_v6.py`, `test_t92_revision.py`, `test_t102_filtro.py` | 403 | 403 |
| Además: `test_t65_qa_r01.py`, `test_t140.py`, `test_t136_coste.py`; `test_v5.py` | 37; 9 | 37; 9 |
| Bloque A completo (recuento, no ejecutado) | 607 + lo de otras copias | + 22 |

Todo en verde. Las dos pruebas cambiadas (el cambio es del comportamiento que pide el ticket, no un debilitamiento):

- `test_t88_consumo.py::test_r04_h13_en_la_v5_cada_tipo_paga_las_reescrituras_de_su_analista`: la reescritura del prompt (fuera del prefijo de la primera llamada) se carga ya y no al liquidar; la «base» de la prueba resta las dos escrituras. El total que paga RV y lo que paga RF no cambian.
- `test_fase4_huecos.py::test_pb17_en_un_ciclo_la_ampliacion_denegada_cierra_con_alcance_reducido`: con 6 UC, cada petición pide la ampliación de su peor caso; la de prospectiva cabe en el tope y se autoriza, y las siguientes se deniegan (antes solo había denegadas). La prueba exige ahora al menos una denegada, lo ampliado igual a lo autorizado y dentro del tope, el consumo dentro del límite y el cierre declarado.

## Matriz criterio → prueba

| Criterio | Pruebas |
| --- | --- |
| CA-1 (peor caso, divisas) | `test_ca1_peor_caso_divisas_ninguna_bolsa_pasa_de_su_limite`, `test_ca1_las_ampliaciones_nunca_pasan_de_la_maxima` |
| CA-2 (12 tipos, hilos, V6) | `test_ca2_peor_caso_doce_tipos_con_hilos`, `test_ca2_determinista_con_hilos_cerca_del_limite`, `test_ca2_v6_peor_caso_ninguna_bolsa_pasa_de_su_limite` |
| CA-3 (AG-18/19/20) | `test_ca3_ag18_ag19_y_ag20_cargan_en_la_bolsa_comun`, `test_ca3_el_dictamen_g3_de_ag18_carga_en_la_bolsa_comun`, `test_ca3_sin_sitio_ag20_no_sale_y_se_declara`, `test_ca3_los_controles_admiten_ampliacion` |
| CA-4 (búsquedas) | `test_ca4_las_busquedas_cuentan_en_uc` |
| CA-5 (reserva petición a petición) | `test_ca5_reserva_el_peor_caso_y_cobra_lo_real`, `…_si_no_cabe_recorta_la_salida_y_por_debajo_del_minimo_no_sale`, `…_pide_la_ampliacion_antes_de_recortar`, `…_cada_continuacion_reserva_la_suya_…`, `…_el_factor_observado_sube_…`, `…_la_reserva_cuenta_en_la_ampliacion`, `…_agentes_la_continuacion_que_no_cabe_…`, `…_agentes_sin_sitio_para_la_primera_…` |
| CA-6 (liquidación, suma del ciclo) | `test_ca6_la_escritura_fuera_del_prefijo_…`, `test_ca6_la_suma_de_limites_no_pasa_del_ciclo` |
| CA-7 (ciclos simulados) | `test_ca7_con_el_simulado_un_ciclo_n2_…`, `test_ca7_con_el_simulado_un_ciclo_n1_…`; `comparar_ciclos.sh` (abajo) |
| CA-8 (vecinas, goldens) | tabla de recuentos; `python tests/goldens_ct.py` → «goldens de contratos: coinciden» |
| CA-9 (mutantes) | `mutantes_t146.py` (abajo) |
| CA-10 (cuotas) | abajo |

## Regresión: falla sin la corrección

`peor_caso_por_bolsa.py` con el código de antes (19f3f3b): DIV 48,36 UC con límite 26,30, y con los 12 tipos las doce bolsas pasan (46,97–57,98 frente a 22,50–26,46) y la suma (653,01) pasa de las 360 del ciclo con la ampliación máxima; las pruebas de CA-1 y CA-2 lo comprueban sobre el mismo SDK falso. Los mutantes M01 a M07 y M09 a M11 (que devuelven partes del comportamiento de antes) las hacen fallar. Con el código nuevo: DIV 24,87 / 25,09; tipos 24,00–25,72 dentro de su límite; COMÚN 32,19 / 32,37; suma 328,27 = lo gastado.

## Ciclos simulados de antes y de después

`comparar_ciclos.sh <antes> <después> <tmp>` (ciclo de divisas del 29-03-2024, backtest del 05-01 al 29-03-2024 y ciclo de los 12 tipos). Entregables iguales salvo la línea de consumo del informe técnico de los 12 tipos (62,46 → 64,38 UC: 6 búsquedas × 0,32). En F5: recortes de la salida del Analista en las 9 semanas N1 (12 000 → 11 785–11 820 tokens), COMÚN con AG-20 (4 semanas) y con AG-18 (12 tipos); en HA, un AUT- DENEGADA por semana N1; marcas de hora un tic después. Detalle y motivos en `analisis-tecnico.md`.

## Mutantes

`python .docs/tickets/T-146/mutantes_t146.py <copia>` en una copia desechable de `bloque_a/` dentro del scratchpad (`…/scratchpad/t146_mut`), borrada al acabar. Pruebas: `test_t146_presupuesto.py` y `test_t88_consumo.py`.

26 mutantes (M01–M26, descritos en el script). Primera pasada: **25 muertos, 1 vivo (M25: el dictamen G3 de AG-18 sin presupuesto)**: en los ciclos de las pruebas G3 daba APTO y AG-18 no llegaba a llamarse. Se añadió `test_ca3_el_dictamen_g3_de_ag18_carga_en_la_bolsa_comun` (los 12 tipos con los datos del 29-03-2024, donde G3 da advertencias y dictamina AG-18) y M25 se volvió a aplicar a mano en la copia: la prueba nueva falla con él y pasa sin él. Resultado: **26/26 muertos**. Los M01–M07 y M09–M11 son regresiones: devuelven partes del comportamiento de antes de T-146.

## Cuotas

- ruff desde la raíz (`ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l`): 2838 (cuota 2838; las mismas líneas que antes en A, ninguna nueva).
- mypy de A como el gate (`mypy --ignore-missing-imports --no-error-summary bloque_a`, desde `bloque_a/11_Ejecutor`): 109 (cuota 109), los mismos 109 errores que antes.

## Comandos

```bash
py=/home/user/robotinvestor/.venv/bin/python
cd bloque_a/11_Ejecutor
$py -m pytest -q -p no:cacheprovider tests/test_t146_presupuesto.py tests/test_integracion.py
$py -m pytest -q -p no:cacheprovider tests/test_unitarias.py tests/test_t87_*.py tests/test_t88_consumo.py tests/test_fase4_*.py
$py -m pytest -q -p no:cacheprovider tests/test_t113_deuda.py tests/test_t12*.py
$py -m pytest -q -p no:cacheprovider tests/test_t13*.py tests/test_fase3_goldens.py
$py -m pytest -q -p no:cacheprovider tests/test_t101_v6.py tests/test_t92_revision.py tests/test_t102_filtro.py tests/test_t65_qa_r01.py tests/test_t140.py tests/test_v5.py
$py tests/goldens_ct.py
/home/user/robotinvestor/.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a | wc -l
cd ../.. && /home/user/robotinvestor/.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
```

## Ronda r02 (QA r01 NO APTO)

Copia `t146r02` (git worktree, HEAD `5759ffd`, `.venv` enlazado), sin red, sin la API y sin coste. «r01» es el código de HEAD (extraído con `git archive` para comparar); «r02», el de esta ronda.

### Recuentos

| Suite | r01 | r02 |
| --- | --- | --- |
| `tests/test_t146_presupuesto.py` | 22 | 35 (13 nuevas `test_r02_*`; con el código de la r01 fallan 12 de ellas: la que queda es la de Q12, que la r01 ya cumplía) |
| `tests/test_t145.py` | 39 | 39 (H-07: cambia `test_h01_la_cota_cubre…`, más fuerte) |
| `tests/test_t148.py` | 20 | 23 (r02 de T-148; `test_h04_r04_r05…` pone AG-18/19/20 en la COMÚN) |
| `test_t146`, `test_t145`, `test_t148`, `test_t88_consumo`, `test_t136_coste`, `test_t129_modo_sombra` | — | 127 passed |
| `test_fase4_huecos.py`, `test_integracion.py` | — | 68 passed |
| `python tests/goldens_ct.py` | coinciden | coinciden |
| Suite completa de A, una vez (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6338 (QA r01 de T-148) | **6350 passed, 1 failed** en 22 min 53 s: el fallo es `test_t148.py::test_h04_r04_r05…`, porque la suite se lanzó con la `test_t148.py` de la r01 ya cargada y a mitad cambió el estimador (la r02 de T-148, que se hizo mientras corría). Con los dos ficheros de la r02, ese fichero pasa entero (23) y las vecinas también (127, arriba). No se repitió la suite entera |

### Matriz de la r02

| Hallazgo | Pruebas |
| --- | --- |
| H-01 | `test_r02_h01_lo_que_leen_las_busquedas_no_sube_el_factor_de_la_bolsa`, `test_r02_h01_en_un_ciclo_la_lectura_de_las_busquedas_no_cierra_fases` |
| H-02 | `test_r02_h02_con_cache_compartida_el_orden_de_los_hilos_no_cambia_f5` (SDK con caché por prefijo y lectura, hilos en un orden fijo y en el contrario), `test_r02_h02_lo_apartado_cuenta_lo_leido_como_escrito` |
| H-03 y H-06 | `test_r02_h03_y_h06_con_un_reparto_por_encima_del_ciclo_ag20_cabe_en_comun_escalada`, `test_r02_h03_con_el_reparto_normal_la_bolsa_de_c5_no_cambia` |
| H-04 | `test_r02_h04_la_lectura_por_busqueda_se_reserva_si_se_configura` |
| H-05 | `test_r02_h05_un_json_muy_anidado_deja_la_llamada_parcial_y_lo_pagado_en_la_bolsa`, `test_r02_h05_si_la_llamada_se_cae_lo_pagado_queda_en_la_bolsa` |
| H-07 | `_comprobar_cotas` (lo asignado escalado y la suma de los límites máximos), `test_t145.py::test_h01_la_cota_cubre_el_peor_camino_con_el_cliente_real` |
| H-08 | `test_r02_h08_lo_real_se_carga_antes_de_soltar_lo_apartado` |
| H-10 | `test_r02_h10_cada_continuacion_se_paga_por_separado`, `test_r02_h10_pagar_resto_suelta_las_reservas_que_no_salieron`, `test_r02_h10_cargar_usa_el_prefijo_de_la_primera_peticion` |

Regresión: con el código de la r01 y el fichero de pruebas de la r02, fallan 12 de las 13 `test_r02_*` (la de H-02 con «2 firmas»; la de H-01 con el factor 4,74; la de H-03 con COMÚN 9,78 sobre 5,88; la de H-05 con `RecursionError`; las demás por la API nueva o la configuración).

### Scripts del revisor: r01 → r02

| Orden (desde la raíz, `.venv/bin/python -I …`) | r01 | r02 |
| --- | --- | --- |
| `r01_01_reserva_unidad.py bloque_a/11_Ejecutor` | 8/12 OK (VIOLA U2, U3, U4, U9) | **10/12 OK**: U4 OK (factor observado 0; 1,676 UC igual que en una bolsa limpia), U9 OK (sin excepción; lo pagado, 4,682, en la bolsa). Siguen **U2** (el script reproduce a mano `cerrar` → `cargar`; `_invocar` ya carga antes) y **U3** (la lectura de las búsquedas no se reserva con `tokens_lectura_por_busqueda` = 0: salvedad declarada, H-04) |
| `r01_02_ciclo_sdk_hostil.py … ` (solo DIV) | DIV 25,355; suma = gastado = 57,316 | igual |
| `r01_02 … --tipos <12> --hilos 6 --lectura 0` | 54 peticiones; AG-10 18; suma 333,336 | igual |
| `r01_02 … --tipos <12> --hilos 6 --lectura 3000` | AG-10 **14**; 53 peticiones; 6 excesos | AG-10 **18** (como sin lectura); 54 peticiones; 6 excesos (AG-14, ahora con `busquedas_web: 5`); sin violaciones |
| `r01_02 … --tipos <12> --hilos 6 --lectura 6000 --factor 1.6` | 5 bolsas pasan (hasta 23,97 / 22,50) | igual (tokenizador 1,6 > 1,35 en la primera petición de cada bolsa: salvedad declarada, H-04) |
| `r01_02 … --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo --veces 2` | **DISTINTO** (2 firmas) | **IGUAL**, y la misma firma que con `--orden inverso` (20ad04339dc9) |
| `r01_02 … --cache --orden inverso --veces 2` | IGUAL (por azar del orden) | IGUAL, misma firma que el directo |
| `r01_03_c5_con_escala.py bloque_a/11_Ejecutor <tmp>` | **VIOLA**: COMÚN 9,782 con límite 5,882 | **OK**: COMÚN 4,551 con límite 5,882 (AG-20 hace una petición; la reparación no cabe y se cierra declarada). El script imprime «asignado (sin escalar) 4.705882» porque F5 da ya lo escalado (H-06) |
| `r01_04_t88_h13_absoluto.py` | totales iguales a los de antes de T-146 | no se toca `_cargar` en la r02 (no se repite) |
| `r01_05_mutantes_qa.py <copia «qa19_mut»>` | 9/12 (vivos Q01, Q09, Q12) | **12/12 muertos** |

### Mutantes y ciclos simulados

- `mutantes_t146.py <copia «t146_mut»>`: **35/35 muertos** (M01–M26 de la r01 y M27–M35, uno por corrección de la r02).
- `comparar_ciclos.sh <r01> <r02> <tmp>`: los tres escenarios (divisas, backtest de 13 semanas, 12 tipos) dan **los mismos entregables y el mismo F5** que la r01; solo difieren F10 (la configuración trae `tokens_lectura_por_busqueda`), los sellos y lo que también difiere entre dos pasadas iguales (`consumo.csv`, `cache_resultados.jsonl`).

### Gates y cuotas

- ruff desde la raíz (tres ejecutores, `| wc -l`): **2838** (cuota 2838). mypy de A (`--ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l`): **109** (cuota 109).
- `tools/corpus_integridad.py` 695 archivos coinciden; `secrets_scan.py`, `refs_vivas.py`, `nfc_check.py` en verde; los tres YAML parsean. No se lanzó `./tools/check_all.sh` entero (lo hace quien coordina).
