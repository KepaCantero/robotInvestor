# T-145 · Pruebas

Copia git `t145` sobre `19f3f3b`, intérprete del repositorio (`py`). Sin red ni API: el cliente real, con un SDK falso.

| Suite o script | Antes (19f3f3b) | Después |
| --- | --- | --- |
| `tests/test_t145.py` | — | **39 passed** |
| `test_t12*`, `test_t13*`, `test_t140.py`, `test_t141_datos_bce.py` (+ `test_t145.py`) | 620 recogidas | **659 passed** (2 min 19 s) |
| Suite completa de A (solo recogida, no lanzada por instrucción) | 6092 | 6131 |
| `tests/goldens_ct.py` | coinciden | coinciden |
| ruff (los tres ejecutores, desde la raíz) | 2838 | **2838** |
| mypy A (como el gate) | 109 | **109** |
| `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py` | — | en verde |
| T-140 `r01_01_cota_ciclo_real.py` (div / 12) | la cota del README (4,58 / 56,79) no cubría 8,85–9,81 / 79,18–79,33 | sigue comparando con `estimar` (sin cambio); la cota nueva (19,54 / 166,56) cubre todos sus escenarios |
| T-140 `r01_02_peor_caso_con_cliente_real.py` (div, div C12, 12, 12 C12) | 4,57 · **5,04 > 4,58** · 36,02 · 36,53 | las mismas cifras, todas por debajo de 19,54 y 166,56 |
| T-140 `r01_03_tarjetas_series_largas.py <contratos de T-136>` | 884 falsos positivos nuevos en filas; 11 962 negativos no declarados | **14** (la fila de 8, declarada); los negativos que quedan, declarados en INC-T123-01 |
| T-140 `r01_04_ventana_fechas_y_borrador.py` | 17 ok, 2 fallos (H-04, H-05) | **19 ok, 0 fallos** |
| T-140 `r01_05_mutantes.py` | vivos K04, V02, T06, T07 | ya no aplica (el código de T01–T09 no existe); ver `mutantes_t145.py` |
| `mutantes_t145.py` (19 mutantes, con K04, V02, T06 y T07 reescritos) | — | **19 de 19 muertos** |
| T-136 `r01_01_iban_tarjetas_formas.py` | 25 ok, 1 fallo (fila de 8, declarada) | 24 ok, 2 fallos: la fila de 8 y «año delante» (deja de detectarse por decisión, H-02; declarado) |
| T-136 `r01_02_cota_por_peticion.py` | cubre A; 56,79 = B | igual (mide `estimar`, sin cambio) |
| `contraste_cota.py` (supuesto S4, div / 12) | — | ningún encargo alargado pasa del supuesto |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_t145.py` (39) y las vecinas: 659 passed; goldens coinciden |
| CA-2 | `test_h01_la_tabla_de_llamadas_del_ciclo`, `test_h01_la_cota_cubre_el_peor_camino_con_el_cliente_real` (peor camino con C12: 5,04 USD > 4,58 de T-140 y ≤ 19,54), `test_h01_el_presupuesto_se_pasa_y_la_cota_por_presupuesto_lo_cuenta`, `test_h01_falla_cerrado`, `test_h01_peor_llamada_…`; `r01_01` y `r01_02` del revisor |
| CA-3 | `test_h02_una_fila_con_la_fecha_delante_no_es_una_tarjeta` (6 formas × 2 separadores × 3000), `test_h02_limite_declarado_…`, `test_h03_tarjetas_con_su_caducidad_detras`, `test_h03_limites_declarados`; `r01_03` del revisor |
| CA-4 | `test_h04_…` (3), `test_h05_el_borrador_separa_los_retornos_del_motor`; `r01_04` del revisor |
| CA-5 | `test_h06_k04_…`, `test_h06_t06_t07_…`, `test_h06_v02_…`; `mutantes_t145.py` |
| CA-6 | ruff 2838, mypy A 109 |

## Regresiones (fallan sin la corrección)

Confirmado con `mutantes_t145.py`, que reintroduce cada error en una copia desechable: T10 (el año vuelve a ser fecha, H-02) lo mata `test_h02_…`; T12 (un grupo delante vale) y T11/T14, `test_h02_…`/`test_h03_…`; K05, K06 y K09 (sin las llamadas condicionales o sin la entrada que leen) los mata `test_h01_la_tabla_…`; K04, `test_h06_k04_…`; V02, `test_h06_v02_…`; V04 (H-04 sin corregir), `test_h04_…`; B02 (H-05 sin corregir), `test_h05_…`. Además `test_h01_la_cota_cubre_…` comprueba que el peor camino pasa la cifra de T-140, que era la del hallazgo.

## Pruebas cambiadas

- `test_t140.py::test_h02_tarjeta_con_caducidad_ano_o_otra_tarjeta`: «2027 <tarjeta>» y «<tarjeta> 1999» pasan de detectarse a no detectarse (comentado «T-145»). Es la decisión de H-02 (un año ya no cuenta como fecha), declarada en INC-T123-01; las otras tres formas siguen igual.

## Gate

No se lanzó `./tools/check_all.sh` ni la suite completa de A (instrucción del encargo). Lanzados: las suites vecinas, goldens, ruff, mypy de A y los gates ligeros de secretos, referencias y NFC.

## Comandos

```bash
cd bloque_a/11_Ejecutor
py -m pytest -q -p no:cacheprovider tests/test_t12*.py tests/test_t13*.py tests/test_t140.py tests/test_t141_datos_bce.py tests/test_t145.py
py tests/goldens_ct.py
cd ../.. && .venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
```
Los de los scripts del revisor y de este ticket, en `analisis-tecnico.md`.
