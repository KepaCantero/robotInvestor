# T-128 · Pruebas

Copia `t127r02` (base `fb3ccd4`), hecha junto con la ronda r02 de T-127, con `.venv` enlazado al del repositorio. Por
instrucción no se lanza `./tools/check_all.sh` ni la suite completa de A: los pasa quien hace el commit.

| Suite | Antes (`fb3ccd4`) | Después |
| --- | --- | --- |
| Motor y vecinas: `tests/test_fase1_*`, `test_fase2_*`, `test_fase3_goldens.py`, `test_t106_*`, `test_t11*`, `test_t12*` | 4848 recogidas | **4912 recogidas** (+32 `test_t128_frontera.py`, +24 `test_t127_r02.py`, +8 parametrizadas por las claves nuevas de `UMBRALES` de REI-NAV y REI-FFO). `test_fase1_*`, `test_fase2_*` y goldens: 2747 (5 fallaban por el comportamiento nuevo: cambiadas, ver `analisis-tecnico.md`); `test_t106_*`, `test_t11*`, `test_t12*`: 2133 passed |
| Repetición: `test_fase1_fon_der.py`, `test_fase1_mon_idx.py`, `test_fase2_reales.py`, `test_t119_p2.py`, `test_t127_r02.py`, `test_t128_frontera.py`, `test_t127_hallazgos.py`, `test_fase3_goldens.py` | — | **2374 passed** |
| `python tests/goldens_ct.py` | coinciden | **coinciden** |
| `verificar_casos_control` (las 67) | 67/67 | **67/67** |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | La tabla de `analisis-tecnico.md` (80 fichas) y `revisores/impl_barrido_identificadores.py` (antes: REI-NAV, REI-FFO, IDX-REB y CHR-FUND con filas por componente; después: ninguna; CHR-FUND, los nombres de las plataformas sin cifra) |
| CA-2 | `tests/test_t128_frontera.py`: `test_ninguna_salida_ni_limitacion_lleva_el_identificador_de_un_componente` (cada caso de control de REI-NAV, REI-FFO, IDX-REB, FON-DISC y FON-TD con identificadores «SECRETO», incluidas las limitaciones que antes los citaban), `test_chr_fund_no_da_cifras_por_plataforma`, `test_las_claves_de_filas_por_componente_ya_no_estan`; reconstrucción: `test_rei_nav_dispersion_desde_tres_y_rango_desde_siete` (contra numpy), `test_rei_nav_copias_a_escala_cuentan_como_una`, `test_rei_nav_dominancia_y_aportacion`, `test_rei_nav_ajustado_que_aporta_una_sola_sociedad_no_se_entrega`, `test_rei_ffo_un_componente_se_rechaza`, `test_rei_ffo_cobertura_con_siete_distintos`, `test_rei_ffo_copias_dominancia_y_aportacion`, `test_idx_reb_la_cesta_de_un_valor_no_se_entrega`, `test_idx_reb_copias_con_los_mismos_dias_de_volumen_son_un_valor`, `test_fon_disc_minimo_maximo_y_rango_desde_siete_miembros`, `test_fon_disc_subcategoria_con_menos_miembros_que_el_minimo`, `test_fon_td_segmento_con_menos_miembros_que_el_minimo`, `test_las_reglas_son_las_de_frontera_b_y_la_peticion_no_las_cambia` |
| CA-3 | `test_casos_de_control_de_las_fichas_corregidas`; `verificar_casos_control` 67/67 (en `r01_01` de T-127); el gate 12/12, en el commit |

## Regresiones

`revisores/impl_mutantes.py` (copia desechable `t127r02_mut_t128`, borrada al acabar): **21 mutantes, 21 muertos** (el
F06, «sin la aportación al rendimiento FFO», vivía en la primera pasada; se añadió el caso de copias que solo comparten
esa cifra a `test_rei_ffo_copias_dominancia_y_aportacion` y muere). Los mutantes N01, N02, F02, F03, R02, P01 y D03
devuelven las filas por componente o el identificador en una limitación (el código de antes) y mueren.

## Scripts de otros tickets

| Script | Resultado |
| --- | --- |
| `.docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py` | 7/7 (ver `pruebas.md` de T-127) |
| `.docs/tickets/T-119/revisores/r02_01_frontera_b.py` | FIR-CRED 1/1 y parada en la línea 71, como en la QA r01 de T-127 (dispersión con 3 `null`) |
| `.docs/tickets/T-119/revisores/r02_02_cache.py` | 12/12 |

## Cuotas

| Cuota | Antes | Después |
| --- | --- | --- |
| ruff desde la raíz (`ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2902 | **2902** |
| mypy A como el gate (`cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l`) | 109 | **109** |

## Gate

No ejecutado (instrucción): `./tools/check_all.sh` en el commit.

## Ronda r02 (QA r01: H-01, H-02, H-03, H-04)

Copia `t127r03` (base `f7faa1b`), hecha junto con la ronda r03 de T-127: suites, mutantes, casos de control y cuotas en
`.docs/tickets/T-127/pruebas.md` («Ronda r03»; los mutantes de esta ronda son los F y C, y V09 y V10, de
`T-127/revisores/impl_r03_mutantes.py`).

### Criterio → prueba (`tests/test_t128_r02.py`, 17)

| Criterio | Pruebas |
| --- | --- |
| CA-4 (H-01, límite declarado) | `test_h01_rei_nav_simetrica_se_sirve_con_aviso_y_es_el_limite_declarado` (la vía «S» del revisor: la prima de A, con el aviso y sin identificadores; con dos datos movidos, sin aviso), `test_h01_rei_nav_los_casos_de_control_no_dan_aviso`, `test_h01_limite_declarado_rei_ffo_e_idx_reb_troceados_se_sirven` |
| CA-5 (H-02, CHR-FLOW-001) | `test_h02_una_sola_moneda_estable_se_rechaza` (la vía «U», también por el Motor, sin citar la moneda), `test_h02_dos_monedas_con_el_mismo_crecimiento_son_una`, `test_h02_dominancia_de_la_oferta` (0,01 % y 5,1 %: rechazo; 6 %: se sirve), `test_h02_un_crecimiento_que_aporta_casi_entero_una_moneda_no_se_entrega`, `test_h02_el_crecimiento_se_mide_desde_su_base`, `test_h02_el_caso_de_control_no_cambia`, `test_h02_la_capitalizacion_se_valida_aunque_el_crecimiento_no_se_entregue`, `test_h02_las_reglas_de_chr_flow_son_umbrales_fijos` |
| CA-5 (H-02, IDX-CONC-001) | `test_h02_idx_conc_amplitud_y_contribucion_de_un_componente_no_se_entregan` (también con rentabilidad nula), `test_h02_idx_conc_contribucion_dominada_no_se_entrega`, `test_h02_idx_conc_porcentaje_sobre_la_media_de_un_solo_valido` |
| CA-6 (H-03) | Declarado en INC-T128-01 («Límites declarados») |
| CA-7 | `test_casos_de_control_de_las_fichas_de_la_r02`; los scripts, abajo |

Ninguna prueba existente cambia. `test_fase2_reales.py` gana 4 pruebas parametrizadas (las claves nuevas de los
`UMBRALES` de CHR-FLOW-001: las tres de `FRONTERA_B` y `monedas_estables_minimas`).

### Scripts del revisor, uno a uno

| Script y vía | Antes | Después | Lectura |
| --- | --- | --- | --- |
| `r01_01_barrido_un_componente.py` | 235 casos; «UNO»: CHR-FLOW-001 con una moneda entre las que se sirven | código 0; **CHR-FLOW-001 ya no está** en «UNO»; las demás de la lista son ámbitos (categorías, pares, escenarios, variables, eventos comparables, contrastes, referencias), como aceptó la QA; «ID» sin cambios | — |
| `r01_02_troceo_y_una_moneda.py` (total) | **1/3** | **2/3** | — |
| · IDX-REB-001, la cesta de un valor (control) | ok | ok | — |
| · IDX-REB-001 T (IN en IN-a e IN-b) | FALLA | FALLA: **límite declarado** | Los dos trozos tienen otro volumen y otro peso: ni copias ni dominancia; un valor troceado por quien pide da su demanda (INC-T128-01 «Ronda r02», H-01). Fijado en `test_h01_limite_declarado_rei_ffo_e_idx_reb_troceados_se_sirven` |
| · CHR-FLOW-001 U (solo EURX) | FALLA | **ok** (rechazo: «1 moneda(s) estable(s) distinta(s) por su crecimiento (< 2)») | H-02 corregido |
| T-127 `r02_01_troceo_y_simetria.py`, vías de REI-NAV-001 y REI-FFO-001 | FALLA y FALLA | FALLA (con aviso) y FALLA: **límite declarado** | Ver `pruebas.md` de T-127, «Ronda r03» |
