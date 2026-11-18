# T-176 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `pytest -q bloque_a/11_Ejecutor` (desde la raíz, como el gate) | 8186 | 8199 passed (+13, `tests/test_t176_pb36_pb33.py`) |
| `pytest -q bloque_a_forex/11_Ejecutor` | 68 | 68 passed (no se toca) |
| `pytest -q bloque_b/11_Ejecutor` | 176 | 176 passed (no se toca) |
| Mutantes propios (`.docs/tickets/T-176/mutantes.py`) | — | 28/28 muertos |
| Archivos afines (goldens CT, fase 4, T-53, T-65, T-66, T-125, T-158, T-160, T-161, T-173), antes de la suite completa | — | 550 passed |

## Criterio de aceptación → prueba

Todas en `bloque_a/11_Ejecutor/tests/test_t176_pb36_pb33.py`.

| Criterio | Prueba |
| --- | --- |
| CA-1 (umbral E 48: P3- fuera de banda, F10 intacto) | `test_pb36_umbral_e_y_p05_fuera_de_banda_a_la_cola_de_ha_con_f10_intacto` (ciclo mock) |
| CA-2 (P-05 PENDIENTE_OPERADOR: P3- sin banda) | la misma; `test_proponer_ajuste_rechaza_no_calibrable_y_sin_banda_es_tipo_3` |
| CA-3 (CT-19 a AG-18, `elevada_via`, HA PENDING_OPERATOR, sin duplicar) | `test_pb36_umbral_e_…`, `test_pb36_un_segundo_ciclo_no_duplica_la_elevacion_ni_la_revision`, `test_p3_de_p11_tambien_se_eleva` |
| CA-4 (dentro de banda AJU- PROPUESTO; no CALIBRABLE rechazado; sin banda tipo 3) | `test_proponer_ajuste_banda_trimestral_de_p09_en_el_limite` (55, 65 dentro; 54, 66 fuera), `test_proponer_ajuste_dentro_de_banda_suma_lo_del_trimestre_y_el_total_frente_al_inicial`, `test_proponer_ajuste_rechaza_no_calibrable_y_sin_banda_es_tipo_3` |
| CA-5 (una revisión por trimestre; sin muestra no propone) | `test_pb36_un_segundo_ciclo_…`, `test_evidencia_umbral_e_youden_y_muestra_insuficiente`, `test_evidencia_umbral_e_empate_elige_el_mas_cercano_al_vigente_y_j_nulo_no_propone` |
| CA-6 (Novedades de la semana; la siguiente solo lo nuevo; T-173 intacto) | `test_pb33_novedades_de_la_semana_con_la_revocacion_y_la_leccion` (ciclo mock), `test_novedades_semana_siguiente_solo_lo_nuevo_y_misma_semana_rehace`; las tres `test_pb33_…` de `test_fase4_huecos.py` pasan |
| CA-7 (evidencias, suite, cuotas, mutantes) | `docs/evidencias_pruebas_bloque_a.md` regenerado: PB-33 y PB-36 «Superada» (37 superadas, 21 en parte); gate 12/12; ruff 2812 (cuota bajada de 2813), mypy A 102; 28/28 mutantes |

## Regresiones

- Sin el cambio (copia de `11_Ejecutor` con `evaluador.py`, `orquestacion.py` y `por_defecto.yaml` de `origin/develop`), `tests/test_t176_pb36_pb33.py` no se puede ni importar (`ESTIMADORES_TRIMESTRALES` no existe): fallan las 13.
- Cada pieza tiene su mutante muerto (M01–M28): validación CALIBRABLE, banda PENDIENTE, banda trimestral con lo del trimestre y en su límite, banda total, AJU- PROPUESTO, filtro de `ajuste_en_sombra`, empate y J ≤ 0 de Youden, muestra mínima, RTR- único y solo con evidencia, P3- ENVIADA y con plan de reversión, idempotencia, elevación (HA sin duplicar, `elevada_via`, PENDING_OPERATOR, receptor AG-18, llamada en el ciclo) y Novedades (corte, primera semana, cambios de estado, lecciones no vigentes, vacía, llamada en el ciclo, revocaciones).

## Ciclo simulado

`python -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv --salida <tmp> backtest --desde 2024-01-05 --hasta 2024-03-29` (desde `bloque_a/11_Ejecutor`): 13 ciclos COMPLETO, 33 pronósticos resueltos; F6 lleva `NOV-2024-W08` (una lección nueva); sin RTR- (la muestra con E no llega a 30) ni P3-.

## Gate

`./tools/check_all.sh` (con `.venv` enlazado al del proyecto): **12/12**. corpus 705 archivos íntegros, NFC, YAML, secretos, refs-vivas, ruff 2812 ≤ 2812, mypy A 102 ≤ 102, FX 174, B 159, pytest A 8199, FX 68, B 176.

Comandos:

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t176_pb36_pb33.py
.venv/bin/python .docs/tickets/T-176/mutantes.py
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
./tools/check_all.sh
```

## Ronda r02 (QA r01 NO APTO)

- `tests/test_t176_pb36_pb33.py`: 19 pasadas (13 + 6 de regresión de H-01, H-03 ×2, H-04 ×2 y H-06; H-02 y H-05 amplían dos existentes).
- `revisores/r01_ataques.py` (el del revisor, sin tocar): **17/17** sin hallazgo (antes 11/17).
- Mutantes `.docs/tickets/T-176/mutantes.py`: 37/37 muertos (M29–M37 nuevos; M15 reescrito sobre la línea de H-03).
- T-176, T-173, `test_fase4_huecos.py`, T-66 (evaluación y propuestas), T-129 (modo sombra), integración, T-65 QA r01 y goldens de la fase 3: 419 pasadas.
- Cuotas: ruff 2812 (≤ 2812), mypy A 102 (≤ 102).
- Backtest mock del CLAUDE.md, tras el rebase: ver abajo.
- Backtest mock (2024-01-05 → 2024-03-29) con el código de la r02: `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos byte a byte a los de la r01 (que la QA r01 comparó idénticos con develop `51d68f5`); el mismo resumen y las mismas entradas de F6.
- Evidencias regeneradas: 256 de 256 pruebas citadas superadas; PB-33 y PB-36 «Superada».
- Rebase: `origin/develop` sigue en `51d68f5` (T-173 y T-175 ya dentro; T-174 aún no): no hubo nada que rebasar.
- Suite completa de A y gate: no repetidos en la r02 (sí en la r01: 8199 y 12/12).

## Ronda de cierre de la QA r02 (H-07)

- `tests/test_t176_pb36_pb33.py`: 20 pasadas (+1, `test_r03_h07_…`).
- `revisores/r01_ataques.py` 17/17 y `revisores/r02_ataques.py` 7/7.
- Cuotas: ruff 2812, mypy A 102.
- Mutantes: 38/38 muertos (M38 nuevo).
