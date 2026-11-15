# T-144 · Pruebas

Copia `t147` (base `dd166b3`), intérprete `/home/user/robotinvestor/.venv/bin/python`, sin red ni coste. No se lanzó `./tools/check_all.sh` ni la suite completa de A.

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t144.py` (nuevo) | — | 33 pasan |
| `test_t135_motor.py`, `test_t127_hallazgos.py`, `test_t127_r02.py`, `test_t127_r03.py`, `test_t128_frontera.py`, `test_t128_r02.py`, `test_fase1_mon_idx.py`, `test_t119_p2.py` | — | 1557 pasan (tres pruebas cambiadas, abajo) |
| Vecinas pedidas (`test_t12*`, `test_t13*`, `test_t14*`, `test_fase2_*`, `test_fase3_goldens.py`) | — | 3061 pasan, 0 fallan |
| `Motor.verificar_casos_control()` (`test_t135_motor.py::test_casos_de_control_no_cambian_ni_dan_aviso`) | 67/67 | **67/67**, ninguno con aviso |
| `python tests/goldens_ct.py` | coinciden | coinciden |

**Pruebas cambiadas (no se debilitan).** `test_t135_motor.py::test_h05_etiquetas_de_series_copiadas`: los precios de la base eran enteros (paso 1, un 0,5 % de redondeo a 100) y la regla nueva de niveles agrupaba a «lejos», que a esa resolución es una copia; se multiplican por un factor de muchos decimales y la prueba sigue fijando la regla de rentabilidades sin tocar ninguna aserción. `test_t127_hallazgos.py` y `test_t127_r02.py`: la igualdad exacta de `FRONTERA_B` gana `tolerancia_numerica_copias` (los tres números de antes, iguales).

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_h01_la_misma_serie_de_otra_fuente_es_una_copia` (7 vías, amplitud `null` y sin identificadores), `test_h01_la_regla_de_niveles_a_mano`, `test_h01_paso_de_precio`, `test_h01_la_cota_no_es_mas_laxa_que_la_de_los_casi_clones`, `test_h01_tolerancia_numerica_es_la_de_la_ficha`, `test_h01_series_distintas_muy_correladas_no_son_copias` (100 semillas × sin redondear, 3 y 2 decimales), `test_h01_la_regla_de_rentabilidades_sigue_viva`, `test_h01_el_desfase_de_una_sesion_sigue_siendo_un_limite_declarado` |
| CA-2 | `test_h02_un_dato_movido_de_un_token_de_oferta_fija_da_el_aviso` (circulante, total con máxima, máxima, con y sin *staking*; el precio con *staking*), `test_h02_lo_que_repiten_los_dos_no_es_coincidencia_informativa` |
| CA-3 | `test_h03_el_tramo_no_cambia_el_resultado` (tramos de 1, 7, 64 y 10 000), `test_h03_indice_grande_con_salida_y_exclusion_sin_fechas_comunes` (n = 2000) |
| CA-4 | `test_h04_precios_no_positivos_se_rechazan` (0, −1, ∞ × dos vías) |
| CA-5 | revisores, casos de control y mutantes (abajo) |

## Scripts del revisor (antes → después)

| Script | Antes (QA r01 de T-135) | Después |
| --- | --- | --- |
| `T-135/revisores/r01_01_copias_idx_conc.py bloque_a/11_Ejecutor` | 34 ok · 5 hallazgos (H-01 ×4, H-04) | **39 ok · 0 hallazgos**; n = 1000 con salida y exclusión: 0,9 s |
| `T-135/revisores/r01_02_aviso_firmas.py bloque_a/11_Ejecutor` | 20 ok · 4 hallazgos (H-02 ×2, H-04 ×2) | **24 ok · 0 hallazgos** |

Falsos positivos con datos redondeados y coste con n = 2000 (script desechable en el scratchpad, ya borrado; cifras en `analisis-tecnico.md`): índices con ρ ≈ 0,995 y precio frente a rentabilidad total, 0 de 300 en los nueve casos (niveles 100, 12 y 2 × sin redondear, 3 y 2 decimales); n = 2000, T = 2520 con una salida y una exclusión sin fechas comunes: **2,7 s** (T-135: 164 s), 590 MB el proceso.

## Regresiones (mutantes)

`.docs/tickets/T-147/mutantes.py <copia t147_mut> --ticket T-144`: **8 de 8 muertos** (sin la regla de niveles, cota sin tope, paso de precio siempre 1, sin el año mínimo en común, precios ≤ 0 aceptados, lo repetido en los dos no iguala, CHR-TOKEN sin marcar lo repetido, lo repetido cuenta como informativo). Con el código de la base (`dd166b3`), `test_t144.py` sin la prueba de n = 2000 da 19 fallos de 32: H-01 (seis de las siete vías; la de otra divisa a cambio fijo ya se agrupaba), H-02, H-03 (el tramo) y H-04.

## Cuotas

ruff 2838 (cuota 2838); mypy A 109 (cuota 109; la línea nueva de `frontera_b.py` se anotó).

## Comandos

```bash
cd bloque_a/11_Ejecutor; PY=/home/user/robotinvestor/.venv/bin/python
$PY -m pytest -q -p no:cacheprovider tests/test_t144.py tests/test_t135_motor.py tests/test_t127_hallazgos.py tests/test_t127_r02.py tests/test_t127_r03.py tests/test_t128_frontera.py tests/test_t128_r02.py tests/test_fase1_mon_idx.py tests/test_t119_p2.py
cd ../..
.venv/bin/python -I .docs/tickets/T-135/revisores/r01_01_copias_idx_conc.py bloque_a/11_Ejecutor
.venv/bin/python -I .docs/tickets/T-135/revisores/r01_02_aviso_firmas.py bloque_a/11_Ejecutor
.venv/bin/python .docs/tickets/T-147/mutantes.py <copia t147_mut> --ticket T-144
```
