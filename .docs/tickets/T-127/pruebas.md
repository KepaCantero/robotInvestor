# T-127 · Pruebas

Copia de trabajo con `.venv` enlazado al del repositorio; «antes» es `git archive` de la base `d1ff926` (con el Catálogo al
lado). Por instrucción no se ha lanzado `./tools/check_all.sh` ni la suite completa de A: los pasa quien hace el commit.

| Suite | Antes | Después |
| --- | --- | --- |
| Motor y vecinas: `tests/test_fase1_*`, `test_fase2_*`, `test_fase3_goldens.py`, `test_fase4_huecos.py`, `test_t106_*`, `test_t11*`, `test_t12*`, `test_unitarias.py` | 4785 | **4836 passed** (9 min 5 s): +41 de `test_t127_hallazgos.py` y +10 de `test_t119_p2.py::test_ningun_umbral_se_cambia_desde_la_peticion` (parametrizada por cada clave de `UMBRALES`: 3 × 3 de `FRONTERA_B` y `redes_propias`) |
| Repetición tras los últimos cambios: `test_t112_motor.py`, `test_t118_hallazgos.py`, `test_t119_motor.py`, `test_t119_p2.py`, `test_t119_r02.py`, `test_t121_hallazgos.py`, `test_t127_hallazgos.py` | — | **1672 passed** (2 min 35 s) |
| `python tests/goldens_ct.py` | coinciden | **coinciden** |
| `verificar_casos_control` (todas: `r01_04_casos_control.py` de T-121) | 67/67 | **67/67** (80 manejadores) |

Ninguna prueba se ha quitado. Se han cambiado, por el comportamiento nuevo, las que lista `analisis-tecnico.md` (cinco de
T-119 y dos de T-121), con su comentario «T-127».

## Criterio de aceptación → prueba

| Criterio | Prueba (`tests/test_t127_hallazgos.py`, salvo que se diga) |
| --- | --- |
| CA-1 | `test_h10_casi_clones_de_un_emisor_se_rechazan` (×3), `test_h10_borde_de_la_tolerancia_de_clon` (1,0100 clon; 1,0102 no), `test_h10_un_solo_dato_distinto_basta_para_no_ser_clon`, `test_h10_una_cadena_de_casi_clones_es_un_solo_componente`, `test_h10_la_tolerancia_compara_por_el_mayor_y_los_ceros_son_iguales` |
| CA-2 | `test_h10_un_componente_de_peso_casi_total_se_rechaza` (REI-LEV ×3, CHR-TOKEN, FIR-CRED, por el Motor sin identificadores), `test_h10_borde_de_la_dominancia_y_bases_de_rei_lev` (19/20 = 95 % se admite; EBITDA, gastos financieros, deuda y FFO; FFO negativo en valor absoluto) |
| CA-3 | `test_h10_con_tres_componentes_no_se_entregan_sus_cifras_individuales`, `test_h10_la_dispersion_de_rei_lev_empieza_en_siete_componentes` (6 no, 7 sí, contra numpy), `test_h10_la_dispersion_de_chr_token_empieza_en_siete_tokens`, `test_h10_fir_cred_conserva_su_dispersion_con_diez_o_mas` |
| CA-4 | `test_h10_covenants_de_menos_componentes_que_el_minimo_no_se_calculan`, `test_h10_staking_y_concentracion_de_un_solo_token_o_dominados_no_se_calculan`, `test_h10_la_propia_red_es_una_red_de_la_ficha_con_su_token`; `test_t119_r02.py::test_h01_chr_token_un_solo_token_solo_si_el_ambito_es_la_propia_red` |
| CA-5 | `test_h10_los_casos_de_control_siguen_superados`, `test_h10_las_reglas_de_la_frontera_son_umbrales_fijos_de_las_tres_fichas`; `test_t119_r02.py::test_h01_los_casos_de_control_de_las_cuatro_fichas_siguen_superados`; `r01_04_casos_control.py` 67/67 |
| CA-6 | `test_h11_la_tupla_no_sale_de_la_cache_de_la_lista_en_ningun_orden`, `test_h11_la_firma_distingue_contenedores_y_claves`; `test_t119_r02.py::test_h06_*` sin cambios |
| CA-7 | `test_h07_una_clave_nueva_de_por_defecto_que_la_ficha_no_lee_no_ablanda_el_error` (A2, A2b, A5), `test_h07_convencion_distinta_si_la_ruta_leida_salio_del_fichero_y_este_cambio`, `test_h07_la_configuracion_leida_apunta_solo_lo_que_sale_del_fichero`; `test_t121_hallazgos.py::test_h01_*` |
| CA-8 | `test_h08_un_solo_criterio_de_dia_en_los_cuatro_modulos` (×5), `test_h08_mismo_veredicto_en_mon_tcv_y_fon` (×4), `test_h08_tcv_rechaza_un_texto_con_basura_tras_la_fecha_y_fon_admite_zonas_mezcladas`, `test_h09_fon_disc_un_nav_del_ultimo_dia_con_hora_se_sirve`; `test_t121_hallazgos.py::test_h04_*` |
| CA-9 | Tablas de abajo |

## Scripts del revisor (sin modificar)

Desde la raíz de la copia: `.venv/bin/python -I .docs/tickets/<ticket>/revisores/<script> bloque_a/11_Ejecutor`.

| Script | Antes | Después |
| --- | --- | --- |
| T-119 `r02_01_frontera_b.py` | 0/5 | **Se detiene** en la línea 71 (`TypeError: 'NoneType' object is not subscriptable`) tras el primer bloque (FIR-CRED-001: 1/1, «10 casi clones no dan su DD»): el script lee `resultado["dispersion"]["ltv_pct"]` del caso de control de REI-LEV-001, y con 3 componentes la dispersión es ahora `null`, que es justo lo que ese bloque comprueba. Con una copia en el scratchpad que solo cambia esa lectura (dispersión ausente = sin las tres cifras), **5/5** y «vías que dan las cifras de un solo emisor o token: ninguna»; también se rechazan los dos ejemplos informativos (relleno de precio 1e-9 en CHR-TOKEN y nueve emisores a escala 1e-6 en FIR-CRED, por dominancia) |
| T-119 `r02_02_cache.py` | 11/12 (la tupla) | **12/12** |
| T-121 `r01_02_h01_ct10.py` | 8/11 (A2, A2b, A5) | **11/11** |
| T-121 `r01_03_h04_bordes.py` | 36/37; 5 líneas «DISTINTO» | 36/37 (el que falla es el caso mal planteado que el revisor señala: FON-FLOW-001 con la última fecha corrida un día rompe su frecuencia mensual); **3** líneas «DISTINTO», las tres de FON-FLOW-001 con el dato en D + 1 por esa misma frecuencia. Las dos de zona horaria desaparecen: «(D+1)T00:30+14:00, corte D» se sirve en las tres y «DT23:00−05:00, corte D» se rechaza en las tres |
| T-121 `r01_01_h04_campo_a_campo.py` | «día del corte con hora rechazado»: 20 | **0**: las 20 eran `fecha_nav` de FON-DISC-001 con hora (H-09), ahora servidas; las de D + 1 siguen rechazadas, con el mensaje nuevo. Ninguna otra diferencia en las 206 pruebas |
| T-121 `r01_04_casos_control.py` | 67/67 | **67/67** |

## Mutantes

`.venv/bin/python .docs/tickets/T-127/revisores/impl_mutantes.py bloque_a/11_Ejecutor <scratchpad>/t127_mut` (copia
desechable, borrada al acabar; pruebas: `test_t127_hallazgos.py` y `test_t119_r02.py`): **37 mutantes, 36 muertos**. El
vivo, S02 (*staking* calculado con un solo token), es equivalente mientras `peso_maximo_componente` < 1: un token es el
100 % de su subconjunto y la dominancia ya lo deja sin calcular. En una primera pasada quedaron vivos D08 (dominancia sin
valor absoluto), A04 (sección por prefijo sin el punto) y F04 (TCV con el día local de un `Timestamp`): se añadieron las
pruebas que los matan (FFO de −20, `_respaldo_en` con «ucx», `_fecha` con un `Timestamp` con zona) y se volvieron a pasar.

## Regresiones

Cada hallazgo tiene una prueba que falla sin su corrección: los mutantes K05 (comparación exacta de la r02), D01 y D05 a
D07 (sin dominancia), O03 a O05 (dispersión siempre), R02 (cualquier ámbito como red, la regla de la r02), C03 (la firma de
la r02), A02 (la regla de T-121) y F01 a F03 y N01 (los criterios de día anteriores) reproducen el código de antes y mueren.

## Cuotas

| Cuota | Antes | Después |
| --- | --- | --- |
| ruff (`ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`, desde la raíz) | 2902 | **2902** |
| mypy A como el gate (`mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 | **109** |

Con `cd bloque_a/11_Ejecutor && mypy bloque_a` (sin `--ignore-missing-imports`) salen 147 antes y 148 después: la de más es
`import-untyped` de `scipy.sparse` (la importación nueva de `fichas_p2.py`), que el gate no cuenta.

## Gate

No ejecutado (instrucción): `./tools/check_all.sh` y la suite completa de A, en el commit. `tools/refs_vivas.py` en verde.

## Ronda r02 (QA r01: H-01, H-02, H-03)

Copia `t127r02` (base `fb3ccd4`) con `.venv` enlazado; hecha junto con T-128 (las cuentas de suites incluyen las dos).
Por instrucción no se lanza `./tools/check_all.sh` ni la suite completa de A.

| Suite | Antes (`fb3ccd4`) | Después |
| --- | --- | --- |
| Motor y vecinas: `tests/test_fase1_*`, `test_fase2_*`, `test_fase3_goldens.py`, `test_t106_*`, `test_t11*`, `test_t12*` | 4848 recogidas | **4912 recogidas** (+24 `test_t127_r02.py`, +32 `test_t128_frontera.py`, +8 de la prueba parametrizada por cada clave de `UMBRALES` de `test_fase2_reales.py`: REI-NAV y REI-FFO ganan cuatro). En verde: `test_fase1_*`, `test_fase2_*` y `test_fase3_goldens.py` 2747 (5 fallos de T-128 corregidos en sus pruebas y repetidos abajo); `test_t106_*`, `test_t11*` y `test_t12*` 2133 passed |
| Repetición tras los últimos cambios: `test_fase1_fon_der.py`, `test_fase1_mon_idx.py`, `test_fase2_reales.py`, `test_t119_p2.py`, `test_t127_r02.py`, `test_t128_frontera.py`, `test_t127_hallazgos.py`, `test_fase3_goldens.py` | — | **2374 passed** |
| `python tests/goldens_ct.py` | coinciden | **coinciden** |
| `verificar_casos_control` (las 67) | 67/67 | **67/67** (en `r01_01` de T-127) |

### Criterio → prueba (`tests/test_t127_r02.py`)

| Hallazgo | Pruebas |
| --- | --- |
| H-01 (copias a escala) | `test_h01_copias_a_escala_de_un_emisor_se_rechazan` (FIR-CRED 10 y 12, REI-LEV 3 y 7, CHR-TOKEN 2 y 7; también por el Motor, sin identificadores), `test_h01_las_copias_se_comparan_por_sus_cifras_no_por_sus_datos`, `test_h01_la_tolerancia_de_las_cifras_es_la_de_clon` (1 % sí, 1,02 % no, ausente ≠ 0, cadena), `test_h01_un_grupo_de_copias_es_un_componente_para_la_dominancia` (REI-LEV 97,7 % del GAV; FIR-CRED con 80 copias), `test_h01_una_copia_que_no_domina_cuenta_una_vez` (4 = 3 distintos; dispersión con 7 distintos, no con 7 componentes), `test_h01_los_subconjuntos_cuentan_componentes_distintos_por_sus_cifras`, `test_h01_la_red_propia_no_cuenta_copias`, `test_h01_copias_que_solo_comparten_una_cifra_no_la_dan` |
| H-02 (aportación) | `test_h02_rellenos_de_pd_nula_se_rechazan` (30 % y 60 %, el ataque del revisor, también por el Motor), `test_h02_rellenos_de_deuda_neta_nula_se_rechazan`, `test_h02_borde_de_la_aportacion` (95 % justo se entrega; vecindario; valor absoluto; agregado nulo; ÷ 0), `test_h02_un_segmento_casi_sin_riesgo_no_se_rechaza_por_la_aportacion`, `test_h02_vencimientos_e_impacto_de_un_solo_componente_no_se_entregan`, `test_h02_un_sector_sin_dilucion_no_da_la_cifra_de_cada_token`, `test_h02_staking_concentrado_en_un_token_no_se_entrega` |
| Casos de control | `test_casos_de_control_con_sus_datos_de_la_r02` (y con los datos de antes, la inflación y los desbloqueos a 30 días no se entregarían) |
| H-03 (declarado) | `test_h03_con_siete_o_mas_el_maximo_es_la_cifra_de_un_componente_sin_identificarlo` |
| Números fijos | `test_ninguna_regla_nueva_se_cambia_desde_la_peticion` |

### Scripts del revisor

| Script | Antes | Después |
| --- | --- | --- |
| `.venv/bin/python -I .docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py bloque_a/11_Ejecutor` | **2/11** | **7/7**: las vías E (copias a escala) se rechazan en las tres fichas; las Z (rellenos de PD 0) se rechazan, y por eso no llegan a ejecutarse las cuatro comprobaciones que dependían de que se sirvieran (Z y O al 30 % y al 60 %); casos de control 67/67 |
| `.venv/bin/python -I .docs/tickets/T-119/revisores/r02_01_frontera_b.py bloque_a/11_Ejecutor` | FIR-CRED 1/1 y parada en la línea 71 (la dispersión con 3 es `null`, lo esperado desde la r01) | igual |
| `.venv/bin/python -I .docs/tickets/T-119/revisores/r02_02_cache.py bloque_a/11_Ejecutor` | 12/12 | **12/12** |

### Mutantes y regresiones

`impl_r02_mutantes.py` (copia desechable `t127r02_mut` en el scratchpad, borrada al acabar): **41 mutantes, 40 muertos**;
vive E11, equivalente (con `tokens_minimos_sector` = 2, un subconjunto de un solo grupo de copias pesa el 100 % de su
capitalización y lo rechaza la dominancia por grupos, con el mismo mensaje). Incluye, adaptados a su texto nuevo, los
mutantes de la r01 que ya no se aplicaban tal cual (K01–K05, D01–D03, D05, D07, D08, O01–O05, S01, S03: «r» al final).
El `impl_mutantes.py` de la r01 sigue dando 18 muertos en los que aún aplica y «no se aplica» en los movidos.

Regresión: con el `fichas_p2.py` de antes de la r02 (`--antes`), `tests/test_t127_r02.py` da **20 failed, 4 passed**; las
cuatro que pasan no son regresiones (la propia red, H-03 declarado, las reglas fijas y el segmento casi sin riesgo).

### Cuotas

| Cuota | Antes | Después |
| --- | --- | --- |
| ruff desde la raíz (`ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2902 | **2902** |
| mypy A como el gate (`cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l`) | 109 | **109** |
