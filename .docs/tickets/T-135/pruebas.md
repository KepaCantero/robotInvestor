# T-135 · Pruebas

Copia de trabajo: rama `t135`, base `eb66257`, sin commit. Intérprete `/home/user/robotinvestor/.venv/bin/python` (en la raíz
de la copia, `.venv` enlazado a él mientras se probaba; enlace borrado al acabar). Sin red y con fechas fijas.

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t135_motor.py` (nueva) | — | 28 |
| Motor y vecinas: `tests/test_fase1_*`, `test_fase2_*`, `test_t106_*`, `test_t11*`, `test_t12*`, `test_fase3_goldens.py` y la nueva | 4945 | 4972 passed con 27 de la nueva (10 min 13 s); la nueva tiene 28 al acabar (una más, por el mutante T04) |
| Las de la frontera tras el último cambio: `test_t135_motor`, `test_t128_r02`, `test_t127_r03`, `test_t127_r02`, `test_t127_hallazgos`, `test_t128_frontera`, `test_fase1_mon_idx`, `test_fase2_reales`, `test_t119_p2`, `test_t119_r02` | — | **2173 passed** (2 min 5 s) |
| `python tests/goldens_ct.py` | coinciden | coinciden |
| Casos de control (`verificar_casos_control`) | 67/67 | 67/67, ninguno con aviso (`test_casos_de_control_no_cambian_ni_dan_aviso`) |

Dos pruebas existentes cambian, comentadas «T-135», sin quitar comprobaciones:
`tests/test_t128_r02.py::test_h02_idx_conc_porcentaje_sobre_la_media_de_un_solo_valido` (la copia ×0,5 que fijaba como
servida pasa a `null`; el caso servido es ahora el de dos series distintas, con `n_validos == 2`) y
`tests/test_t127_r03.py::test_h04_el_aviso_cuenta_los_datos_que_coinciden` (`AVISO_B` con su clave nueva).

## Scripts de los revisores

| Script | Antes (`eb66257`) | Después |
| --- | --- | --- |
| `.docs/tickets/T-128/revisores/r02_01_chr_flow_e_idx_conc.py` | 16/18 (FALLA: C00 + copia exacta y C00 + copia ×0,5 dan la amplitud de C00) | **18/18** (amplitud `null`) |
| `.docs/tickets/T-127/revisores/r03_01_cota_aviso_y_origen.py` | 10/11 (FALLA A3: falso aviso; A4: «sin aviso») | **11/11** (A3 sin aviso; A4: 1 aviso, «con aviso o rechazo») |
| `.docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py` | 7/7 | 7/7 |
| `.docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py` | 2/7 | 2/7 (las mismas cinco FALLA: límite declarado) |
| `.docs/tickets/T-128/revisores/r01_02_troceo_y_una_moneda.py` | 2/3 | 2/3 («T»: límite declarado) |

El bloque A2 de `r03_01` llama a `_aviso_casi_clones` con sus propias firmas de 6 datos, no con la de la ficha: su
frecuencia de CHR-TOKEN (46 % con 20 tokens) no cambia porque no pasa por la firma nueva. Con el mismo generador llevado a la
firma de la ficha (`revisores/impl_frecuencia_aviso_token.py`, semilla 11; 2000 peticiones por fila):

| Generador A2 del revisor | n = 5 | n = 10 | n = 20 |
| --- | --- | --- | --- |
| sin *staking* ni concentración (antes → T-135) | 4,3 % → 0,5 % | 15,4 % → 1,7 % | 45,8 % → 5,8 % |
| con *staking* y concentración | 3,8 % → 0,0 % | 15,0 % → 0,0 % | 46,4 % → 0,0 % |
| prudente (25 % redondas, 25 % fijas), sin *staking* | — | 1,2 % → 0,4 % | 5,1 % → 1,3 % |
| circulante con 3 cifras significativas, sin *staking* | — | 13,9 % → 1,2 % | 44,7 % → 5,7 % |

## Criterio de aceptación → prueba

| Criterio | Prueba (`tests/test_t135_motor.py` salvo indicación) |
| --- | --- |
| CA-1 (T-128 H-05) | `test_h05_un_valor_y_su_copia_no_dan_su_amplitud` (exacta, ×0,5, ×37, recortada), `test_h05_dos_valores_distintos_se_sirven_con_la_amplitud_a_mano`, `test_h05_con_un_valor_distinto_mas_las_copias_cuentan_cada_serie`, `test_h05_dominancia_de_un_grupo_de_copias` (19 se sirve, 20 no), `test_h05_el_porcentaje_cuenta_los_validos_distintos`, `test_h05_la_concentracion_no_cambia`, `test_h05_la_peticion_no_cambia_la_regla`, `test_h05_etiquetas_de_series_copiadas`; `test_t128_r02.py::test_h02_idx_conc_porcentaje_sobre_la_media_de_un_solo_valido`; `test_fase1_mon_idx.py::test_idx_conc_valores_a_mano` (sin cambios); `r02_01` 18/18 |
| CA-2 (T-128 H-06) | `test_h06_chr_flow_dominancia_de_un_grupo_de_copias` (mutante F01 muerto) |
| CA-3 (T-127 H-06) | `test_h06_dos_tokens_de_oferta_fija_y_redonda_no_dan_aviso` (con y sin *staking*), `test_h06_el_staking_distingue_a_dos_tokens_con_la_misma_concentracion`, `test_h06_una_copia_con_un_dato_movido_sigue_dando_aviso`, `test_h06_copia_de_un_token_fijo_con_el_precio_movido_y_su_staking`, `test_h06_coincidencias_triviales_no_bastan`; `test_t127_r03.py::test_h04_*` (sin cambios salvo `AVISO_B`); `r03_01` 11/11 |
| CA-4 (T-127 H-07) | `test_h07_rei_nav_un_dato_movido_da_aviso_con_o_sin_otros_pasivos`, `test_h07_rei_nav_sin_otros_pasivos_con_dos_datos_movidos_no_da_aviso`, `test_h07_rei_nav_sociedades_distintas_sin_otros_pasivos_no_dan_aviso`; `test_t128_r02.py::test_h01_rei_nav_*` (sin cambios) |
| CA-5 (T-127 H-08) | `test_h08_el_docstring_de_frontera_b_no_es_absoluto` |
| CA-6 | `test_casos_de_control_no_cambian_ni_dan_aviso` (67/67); mutantes (abajo); suites y cuotas (abajo); INC-T128-01 e INC-T127-01 «Ronda T-135» |

## Regresiones

- **Las pruebas fallan sin la corrección:** `impl_mutantes.py --base eb66257` pone los cuatro módulos del Motor de la base y
  ejecuta `tests/test_t135_motor.py`: **16 fallan y 12 pasan**. Fallan todas las de H-05 (9), las de T-127 H-06 que cambian
  el comportamiento (4), dos de H-07 y la de H-08. Pasan las que fijan lo que ya era correcto: la de T-128 H-06 (el código
  ya agrupaba; es la del mutante), las copias con un dato movido que siguen dando aviso, la de dos valores distintos, la de la
  concentración, la de sociedades distintas sin `otros_pasivos` y la de los casos de control.
- **Mutantes de los cambios:** `.docs/tickets/T-135/revisores/impl_mutantes.py`, 27 mutantes, **27 muertos** (copia
  desechable `t135_mut` en el scratchpad, borrada al acabar). En la primera pasada vivían cuatro: E04 (tolerancia por el
  menor; se añadió el borde 1,005 %), V06 (trivial si lo es en uno; se añadió el dato movido desde 0), T04 (sin el
  *staking* en la firma; se añadió la prueba de la misma concentración) y E06 (sin la diagonal, equivalente: se quitó la
  línea `np.fill_diagonal`, que sobraba).

## Gate

No se lanzó `./tools/check_all.sh` ni la suite completa de A (por instrucción). En su lugar:

| Comprobación | Resultado |
| --- | --- |
| ruff de los tres ejecutores desde la raíz (`ruff check --output-format=concise … \| wc -l`) | **2902** (cuota 2902; sin cambios) |
| mypy de A como el gate (`cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l`) | **109** (cuota 109); ninguna línea de los cuatro módulos tocados |
| `tools/refs_vivas.py`, `tools/secrets_scan.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py` | en verde (corpus 695) |
| A-Forex y B | no tocados, no lanzados |

## Comandos

```bash
C=/tmp/.../scratchpad/t135; PY=/home/user/robotinvestor/.venv/bin/python
cd $C && ln -s /home/user/robotinvestor/.venv .venv          # borrado al acabar
.venv/bin/python -I .docs/tickets/T-128/revisores/r02_01_chr_flow_e_idx_conc.py bloque_a/11_Ejecutor
.venv/bin/python -I .docs/tickets/T-127/revisores/r03_01_cota_aviso_y_origen.py bloque_a/11_Ejecutor
.venv/bin/python -I .docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py bloque_a/11_Ejecutor
.venv/bin/python -I .docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py bloque_a/11_Ejecutor
.venv/bin/python -I .docs/tickets/T-128/revisores/r01_02_troceo_y_una_moneda.py bloque_a/11_Ejecutor
.venv/bin/python .docs/tickets/T-135/revisores/impl_mutantes.py bloque_a/11_Ejecutor <scratchpad>/t135_mut --base eb66257
cd bloque_a/11_Ejecutor
$PY -m pytest -q -p no:cacheprovider tests/test_fase1_* tests/test_fase2_* tests/test_t106_* tests/test_t11* tests/test_t12* \
    tests/test_fase3_goldens.py tests/test_t135_motor.py
$PY -m pytest -q -p no:cacheprovider tests/test_t135_motor.py tests/test_t128_r02.py tests/test_t127_r03.py \
    tests/test_t127_r02.py tests/test_t127_hallazgos.py tests/test_t128_frontera.py tests/test_fase1_mon_idx.py \
    tests/test_fase2_reales.py tests/test_t119_p2.py tests/test_t119_r02.py
$PY tests/goldens_ct.py
cd ../.. && /home/user/robotinvestor/.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
cd bloque_a/11_Ejecutor && /home/user/robotinvestor/.venv/bin/mypy bloque_a --ignore-missing-imports --no-error-summary | wc -l
```
