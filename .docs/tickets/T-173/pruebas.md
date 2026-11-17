# T-173 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`pytest -q bloque_a/11_Ejecutor`, recogidas) | 7 975 | 7 991 (+16 de `tests/test_t173.py`): 7 988 superadas, 2 omitidas y 1 que pasa al regenerar las evidencias (ver «Gate») |
| `tests/test_t173.py` | — | 16 superadas |
| Línea base del gate (A ≥ 607) | cumple | cumple |
| A-Forex, B | sin tocar | sin tocar (no se ejecutan: ningún archivo de esos bloques cambia) |

## Criterio de aceptación → prueba

| Criterio | Prueba (`tests/test_t173.py`, salvo indicación) |
| --- | --- |
| CA-1 | `test_pb50_rf_h2_pierde_con_significacion_y_baja_a_limitado` |
| CA-2 | `test_pb50_sin_muestra_o_sin_perdida_significativa_no_degrada` (n = 29, gana, contaminados) · `test_pb50_con_p_por_encima_de_alfa_no_degrada` · `test_pb50_ningun_cambio_hacia_o_desde_no` (RF × H1 «Limitado», MON × H4 «No») · `test_pb50_h5_no_entra_en_la_degradacion_por_dm` · `test_pb50_un_escalon_por_trimestre_y_nunca_sube` · `test_pb50_restituida_a_si_no_vuelve_a_bajar_en_el_mismo_trimestre` · `test_pb50_un_fallo_de_la_degradacion_dm_no_tumba_el_c5` |
| CA-3 | `test_pb50_el_c5_degrada_y_el_ciclo_lee_limitado_sin_bloqueo_de_g3` (dos ciclos mock) |
| CA-4 | `test_pb64_c5_publica_los_estados_h5_en_f6` · `test_pb64_sin_h5_no_publica_nada` · `test_estado_hito_publicable` |
| CA-5, CA-6 | `test_pb64_paquete_y_tecnico_publican_los_estados_h5` (ciclo mock; el paquete valida contra `Esquema JSON - Paquete de oportunidades - V5.0.json`) |
| CA-7 | Las pruebas de H5 existentes pasan sin cambios (`test_t53_*`, `test_t65_hallazgos`, `test_v51`, `test_fase4_huecos::test_pb64_*`); la suite completa; cuotas abajo |
| CA-8 | `.docs/scripts/evidencias_plan_a.py --ejecutar`: PB-50 y PB-64 «Superada»; 224 de 224 pruebas citadas superadas; Superada 32 → 34 y en parte 26 → 24 |

## Regresiones y mutantes

`.docs/tickets/T-173/mutantes.py` aplica 14 mutaciones al código nuevo, ejecuta `tests/test_t173.py` y restaura el archivo. Con el código sin la corrección las pruebas fallan. Resultado: las 14 mueren.

| Mutante | Resultado |
| --- | --- |
| M1 nunca degrada · M2 cola contraria de DM · M3 degrada desde «Limitado» · M4 sin muestra mínima | muertos |
| M5 sin el límite de un escalón por trimestre | muerto (vivo en la primera pasada; muere con `test_pb50_restituida_a_si_…`, añadida por eso) |
| M6 cuentan los contaminados · M7 H5 entra en la DM · M8 publica los H5 no abiertos · M9 sin entrada EH5- | muertos |
| M10 paquete sin `x_estados_h5` · M11 estado de hito invertido · M12 técnico sin tabla H5 · M13 sin estado de hito en el técnico · M14 C5 sin degradación DM | muertos |

**Cambio de una prueba existente:** `test_fase4_huecos.py::test_pb33_…`. Con sus datos, la celda RV × H3 también pierde frente a la referencia con significación (dice 0,65, acierta el 50 %, n = 120). Por 12.2 ahora baja a «Limitado» en el mismo C5. La prueba afirma esa degradación y que ninguna vista publicada de RV lleva probabilidad, con una lista que no está vacía. Antes miraba solo las vistas H3, que ya no se ofrecen. Lo que pide PB-33 sigue afirmado.

## Ciclo mock (CLI)

Con `bloque-a --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv --salida <scratchpad>/salida_mock backtest --desde 2024-01-05 --hasta 2024-03-29`, el ciclo termina con 39 señales, 33 pronósticos y 33 resueltos. Con el perfil por defecto (DIV) no hay H5 ni celdas con 30 resueltos que pierdan: no se escribe ninguna entrada EH5- ni ningún AJU- de H1–H4, como se esperaba.

## Gate

- La suite completa de A, una vez: `.venv/bin/python -m pytest -q -p no:cacheprovider bloque_a/11_Ejecutor` dio 7 988 superadas, 2 omitidas y 1 fallida (43 min 46 s).
  - La fallida es `test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`, que se espera hasta regenerar `docs/evidencias_pruebas_bloque_a.md`.
  - Después de `evidencias_plan_a.py --ejecutar`, `pytest -q tests/test_fase4_mapa.py` da 23 superadas.
- Cuotas: ruff 2 813 (≤ 2 813, igual que la base) y mypy de A 109 (≤ 109); mypy de A-Forex 174, sin tocar.
- `tools/corpus_integridad.py`, `tools/nfc_check.py`, `tools/secrets_scan.py` y `tools/refs_vivas.py` salen en 0.
- `./tools/check_all.sh --core` no terminó en 10 minutos de herramienta: incluye las suites y la de A dura unos 44 min. Sus piezas se ejecutaron por separado, como se lista arriba. El gate completo (12/12) queda para la QA o el cierre, en una máquina sin otras sesiones.

## Ronda r02 (QA r01 NO APTO)

Rebase sobre `origin/develop` (`375d24b`) antes de los cambios.

| Suite | r01 | r02 |
| --- | --- | --- |
| Bloque A completa (recogidas) | 7 991 | 8 174 (develop trae T-171 y T-165; +8 en `test_t173.py` y +1 en `test_fase4_huecos.py`) |
| `tests/test_t173.py` | 16 | 24 superadas |
| `test_t173` + `test_t53_*` + `test_t65_hallazgos` + `test_fase4_huecos` | — | 177 superadas |

**Hallazgo → prueba (`tests/test_t173.py`, salvo indicación)**

| Hallazgo | Prueba |
| --- | --- |
| H-01 | `test_pb50_r02_h01_una_sola_semana_mala_no_degrada` (§4) · `test_pb50_r02_h01_historia_buena_mas_una_semana_mala_no_degrada` (§4b/§12: 61 conglomerados, p > 0,99) · `test_pb50_r02_h01_sin_fechas_de_conglomerado_ni_conglomerados_minimos_no_degrada` · `test_pb50_r02_h01_n_suficiente_pero_n_eff_insuficiente_no_degrada`; en el nominal, n_eff, conglomerados y `n_conglomerados` de la DM en la evidencia |
| H-02 | `test_pb50_r02_h02_un_fallo_en_f10_anula_el_ajuste_y_el_reintento_degrada` (§10: ANULADO, sin RDM-, el reintento del 2026-06-12 degrada) · `test_pb50_r02_h02_si_falla_el_cfg_de_p30_se_revierte_el_de_p31` |
| H-03 | `test_pb50_r02_h03_solo_en_la_revision_mensual` · `test_pb50_r02_h03_holm_entre_las_celdas_de_la_misma_revision` (p = 0,061 degrada sola y no con otra celda en la revisión, umbral α/2); `test_pb50_ningun_cambio_hacia_o_desde_no` (fuera de la familia) |
| H-04 | `test_fase4_huecos.py::test_pb33_con_la_degradacion_dm_neutralizada_la_vista_h3_decertificada_no_publica_probabilidad` |

**Scripts del revisor**

- **`revisores/r01_ataques.py`**, ejecutado sección a sección con `r02_ejecutar_ataques_r01.py`:
  - Tal cual, §1 falla al leer `dm_hln`, porque sus 35 PRG tienen una sola fecha de resolución y ya no hay DM; §6 falla porque §5 no degradó.
  - §4 da un conglomerado y no degrada. §4b no degrada. §12: el caso 4 tiene 1 conglomerado (n_eff = 1, `degrada_hoy` False); el 4b, 61 conglomerados, n_eff 61, p por conglomerado 0,999998 y `degrada_hoy` False.
  - Con `--fechas-distintas` (una fecha por PRG):
    - §1: la DM a mano coincide, con p = 1,286·10⁻⁴;
    - §2: p = 0,99976, no degrada; §3: empate, no degrada;
    - §5: 2026-T4; §6: 2027-T1 SI → LIMITADO, P-30 5.3;
    - §7: idempotente (1, 0);
    - §8: la celda con una referencia None ya no aborta las demás (1);
    - §9: NaN o infinito, no degrada;
    - §10: el AJU- en bruto aparece CONFIRMADO, pero la vista consolidada por id lo da ANULADO (prueba H-02); el reintento degrada (1) y P-31 queda en F10;
    - §11: dos EH5- el mismo día, como en la r01.
- **`revisores/r01_test_pb33.py`:** 1 superada.
- **`revisores/r01_regresion.sh`**, base `origin/develop` frente a la rama, perfil por defecto y perfil con H5:
  - `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos en los dos perfiles;
  - F6 solo gana `REVISION_DM` ×3 (enero, febrero y marzo, sin ajustes: n_eff de 1 a 10,5, por debajo de 30) y, con H5, `EH5` ×12;
  - no hay ningún P-31 en F10.
- **Tasas falsas.**
  - `revisores/r01_tasa_falsa.py` (la regla de la r01): 8 % en una mirada, 15,5 % por trimestre y 24,2 % por año.
  - `r02_tasa_falsa.py` (12 celdas sin pérdida, 1 000 simulaciones):

| Regla | Por celda, trimestre | Por celda, año | Familia, por revisión | Familia, año |
| --- | --- | --- | --- | --- |
| r01: cada C5, sin Holm | 15,2 % | 22,4 % | 66,5 % | 96,2 % |
| Solo mensual, sin Holm | 12,8 % | 20,4 % | 63,9 % | 92,9 % |
| r02: mensual y con Holm | 0,9 % | 1,5 % | 4,3 % | 15,8 % |

Con una sola celda en la revisión, Holm es la prueba a α (la fila «solo mensual»). Queda en INC-T173-01.

**Mutantes.** `mutantes.py` tiene 24: los 14 de la r01, reescritos sobre el código nuevo, y 10 de H-01, H-02 y H-03 (DM por PRG, sin conglomerados mínimos, n en lugar de n_eff, sin fechas, sin ANULADO, sin reversión, ANULADO que cuenta, sin Holm, en cada C5 y familia con celdas que no bajan). Mueren los 24.
- En la primera pasada sobrevivieron tres:
  - M3 era equivalente: el segundo control de «Sí» era redundante; se quitó y M3 pasa a «la familia admite "Limitado"»;
  - M16 y M17 murieron al reforzar la prueba de conglomerados (con `min_calibrar` = 5) y al añadir la de n_eff < 30.

**Cuotas:** ruff 2 813 y mypy de A 109, iguales a la cuota. Se corrigieron un RUF059 y un arg-type nuevos.

**Suite completa de A, una vez:** 8 171 superadas, 2 omitidas y 1 fallida (46 min 17 s). La fallida es `test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`, que se espera hasta regenerar las evidencias; después pasa (ver abajo).

**Evidencias:** `.docs/scripts/evidencias_plan_a.py --ejecutar` da 233 de 233 pruebas citadas superadas. PB-50 y PB-64 salen «Superada»; en total, Superada 34 y en parte 24. Después, `tests/test_fase4_mapa.py` da 23 superadas. `corpus_integridad`, `nfc_check`, `secrets_scan` y `refs_vivas` salen en 0. El gate 12/12 completo queda para la QA o el cierre, porque incluye la suite de A (≈ 46 min).

## Ronda de cierre de la QA r02

- **H-05:** `test_pb50_r02_h02_si_falla_el_cfg_de_p30_se_revierte_el_de_p31` afirma que la `methodology_version` de la reversión tiene `a` igual a `de` y que P-30 no se movió. Mutante M25 muerto.
- **H-06:** `test_pb50_cierre_h06_la_familia_es_fija_y_cuenta_las_celdas_sin_muestra`, más la prueba de Holm rehecha: p = 0,061 con una sola celda evaluable no degrada, porque su umbral es α/32. Mutante M26 muerto.
- **Pruebas:**
  - `test_t173.py`: 25 superadas.
  - `test_t173`, `test_t53_*`, `test_t65_hallazgos` y `test_fase4_huecos`: 178 superadas, después de adaptar `test_pb33_…` a la familia fija (RV × H3 vuelve a quedarse en «Sí»).
  - `mutantes.py`: 26 de 26 muertos.
- **Regresión:** `r01_regresion.sh` contra `origin/develop` (`375d24b`, que no ha avanzado). Las tres salidas del backtester son idénticas en los dos perfiles. F6 solo gana `REVISION_DM` ×3 y `EH5` ×12, y no aparece ningún P-31.
- **Tasas falsas** (por celda, trimestre y año):
  - con `revisores/r02_tasa_falsa_una_celda.py`, α entero y una celda: 13,6 % y 21,1 %;
  - con `r02_tasa_falsa.py`, la familia fija de 32 con 12 evaluables: 0,2 % y 0,4 % por celda, y 5,9 % al año en la familia;
  - con una sola celda evaluable: 14,1 % y 22,4 % con α entero, frente a 0,1 % y 0,3 % con la familia fija.
- **Potencia** (una celda que pierde, en la primera revisión, en un trimestre y en un año):
  - σ = 0,18: con α entero 18,3 %, 27,2 % y 42,5 %; con α/32, 0,4 %, 0,7 % y 1,4 %;
  - σ = 0,25: con α entero 32,3 %, 47,1 % y 69,5 %; con α/32, 0,7 %, 2,6 % y 10 %.
- **Cuotas:** ruff 2 813 y mypy de A 109.
