# T-180 · Pruebas

Copia de trabajo: worktree en la instantánea `192499e` con `.venv` enlazado. Sin red y con el cliente simulado. La máquina estaba
compartida con otras dos suites de A (otras sesiones), así que los tiempos son largos.

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t180_hallazgos_t163.py` (nuevo) | — | 27 superadas |
| `tests/test_t163_hallazgos_t160.py` y `tests/test_t160_reejecucion_certificado.py` | 48 + 16 | 64 superadas |
| `test_t66_evaluacion.py`, `test_t66_propuestas.py`, `test_fase4_huecos.py`, `test_t53_evaluacion_y_almacen.py`, `test_t87_datos.py` | — | 175 superadas (las que usan el ayudante, sin cambiar sus aserciones; t53 y t66 con el motivo, también en la suite completa) |
| `.docs/tickets/T-163/revisores/r01_01_ataques.py` | 29 superadas, 2 fallan a propósito (H-01, H-02) | 28 superadas; las `test_h01_*` y `test_h02_*` pasan; 3 fallan **por diseño** (abajo) |
| `.docs/tickets/T-160/revisores/r01_01_ataques.py` | — | 34 superadas; falla solo `test_una_auditoria_ct10_posterior_que_no_coincide_no_impide_la_aprobacion`, por diseño desde T-163 (H-05) |
| Suite completa de A (`pytest -q` en `bloque_a/11_Ejecutor`, una vez) | ≥ 607 (línea base; 7180 + 2 omitidas antes de las 27 nuevas) | **7207 superadas y 2 omitidas** en 46 min, sin fallos |
| Goldens (`tests/goldens_ct.py`) | coinciden | coinciden |

### Las tres de r01_01 de T-163 que fallan por diseño

`test_falso_desde_cero_con_su_propio_soporte_entra_en_vigor_limite_declarado`, `test_un_lote_con_dos_propuestos_validos_de_la_misma_celda_no_aprueba_ninguno`
y `test_ct04_no_aprueba_un_segundo_certificado_de_una_celda_con_un_vigente_legitimo` forjan un certificado «válido por sí mismo»
con `_fabricadas()`: p 0,9 y 0,1 con frecuencias reales 1,0 y 0,2. Esas cifras no cumplen el criterio del certificado
(`ev.criterio_certificado`: «ECE 0,0999… > q90 nulo 0,0400…»), y desde T-180 CT-04 lo comprueba, que es lo que pide H-01. Las
pruebas del ticket cubren lo mismo con datos que sí lo cumplen (el ayudante de `conftest.py`): N07 y el segundo certificado de
una celda (`test_h03_n07_…`) y el límite declarado (`test_limite_declarado_…`).

## Criterio de aceptación → prueba

| Criterio | Prueba (en `tests/test_t180_hallazgos_t163.py` salvo que se diga) |
| --- | --- |
| CA-1 | `test_h01_ct04_no_aprueba_un_certificado_cuyo_soporte_no_cumple_el_criterio` (celda débil, entradas reales); `test_h01_cada_condicion_del_criterio_cuenta_en_el_soporte` (8: n_eff 99,9 y None, IC 0 y −0,01, ECE > q90, ECE = 0,15, p 0,2 y None); `test_h01_los_umbrales_del_criterio_salen_de_la_configuracion` (3); `test_h01_ct04_no_aprueba_un_soporte_que_no_pidio_el_evaluador`; `test_h01_con_una_ct10_dentro_de_tolerancia_el_soporte_se_mira_con_la_materialidad`; `test_h01_un_soporte_con_cifras_de_otra_forma_no_lanza_y_no_vale` (2); r01_01 de T-163 `test_h01_*` |
| CA-2 | `test_h01_la_revision_revoca_un_vigente_cuyo_soporte_no_cumple_el_criterio` (y la idempotencia); el VIGENTE legítimo sigue: `test_h02_un_vigente_sin_reejecucion_…` de T-163 (`res2`) |
| CA-3 | `test_h01_con_una_sola_celda_candidata_tambien_se_aplica_holm` |
| CA-4 | `test_h01_el_ayudante_de_pruebas_escribe_un_certificado_que_cumple_el_criterio`; la aserción del criterio dentro del ayudante; las 175 vecinas |
| CA-5 | `test_h02_dos_horizontes_con_las_mismas_entradas_tienen_cada_uno_su_soporte`; r01_01 de T-163 `test_h02_*` |
| CA-6 | `test_t53_…::test_umbral_de_revocacion_ece_sale_de_la_configuracion` y `test_t66_evaluacion.py::test_pa10_revocar_y_retirar_siguen_siendo_automaticos` (con el motivo); `test_h03_n03_n04_…` (5) y `test_h03_n07_…` |
| CA-7 | r01_01 de T-163 (arriba) |
| CA-8 | mutantes de r01_02 y r01_03 (abajo) |
| CA-9 | vecinas, goldens, gates ligeros, suite completa, cuotas, PB-32 (abajo) |

## Regresiones

- **Sin la corrección** (copia desechable con el `evaluador.py` de HEAD y las pruebas nuevas): de las 27 del ticket y las dos de
  H-03 (a), **fallan 17**: todas las de H-01 (`ct04_no_aprueba…`, `la_revision_revoca…`, las 8 condiciones, los 3 umbrales, el
  solicitante, la materialidad, una sola celda) y la de H-02. Pasan las 10 que no dependen de la corrección: las de mutantes (N03 y
  N04 ×5, N07), las dos de H-03 (a), el ayudante y el límite declarado.
- **El ayudante viejo con el Evaluador nuevo** (n = 60): fallan 5 de las 7 pruebas que lo usan (PB-33 ×2, PB-32, ECE = 0, R13): el
  certificado se revocaba o no publicaba porque su soporte no cumple el criterio. Las 2 que seguían pasando son justo las de H-03 (a)
  en su versión anterior (solo afirmaban «se revoca»); con el motivo, fallarían.
- **Mutantes propios** (`.docs/tickets/T-180/mutantes_t180.py`, contra `tests/test_t180_hallazgos_t163.py`): **9 de 9 muertos**:
  U01 (sin el solicitante del soporte), U02 (sin el criterio), U03 (sin la materialidad de una CT-10 DENTRO_TOLERANCIA), U04 (CT-04
  sin la p de DM), U05 (una sola celda sin Holm), U06 (umbrales a mano), U07 (cifras de otra forma que lanzan), U08 (petición sin
  horizonte) y U09 (el ayudante con 60 pronósticos).

## Mutantes de los revisores

Cada lote en su copia desechable (`bloque_a/` entero y `.docs/tickets/T-160` y `T-163`), borrada al acabar.

| Lote | Resultado |
| --- | --- |
| `r01_03_mutantes.py` de T-160 (26), con `test_t163_…`, `test_t180_…` y r01_01 de T-160 sin la de H-05 | **24 muertos**; viven solo M13 y M14, los equivalentes de su QA; ninguno sin aplicar. Se cortó tras M05 (límite de 2 h de la tarea) y se retomó con `--solo M06,…,M26` desvinculado; la copia, que quedó con M06 aplicado, se restauró antes |
| `r01_02_mutantes.py` de T-163 (12), con `test_t180_…` | **todos aplican; 11 muertos por las pruebas** (N03, N04 y N07 por las del ticket, como pedía H-03). N05 (ayudante roto) mata ahora **las 7** pruebas adaptadas (antes 5: las de t53 y t66 ya afirman el motivo). N11 sale «muerto por r01_01», pero es espurio: lo matan las tres de r01_01 que fallan por diseño; sin ellas (`-k "not test_h0 and not falso_desde_cero and not un_lote_con_dos and not segundo_certificado"`) vive (26 superadas): sigue siendo el equivalente de la QA |

`.docs/scripts/mutantes_revisor_ampliado.py` acepta ahora una lista `PRUEBAS` en varias líneas (la de r01_02 ocupa dos) y pasa
`--solo` al script del revisor.

## Gate

| Comprobación | Resultado |
| --- | --- |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | en verde |
| `tools/corpus_integridad.py` | 695 archivos coinciden |
| ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | **2813** (≤ 2813) |
| mypy A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | **109** (≤ 109) |
| Mapa del plan de pruebas (`.docs/scripts/evidencias_plan_a.py`) | 67 pruebas del plan, 204 citadas y todas existen |
| PB-32 (`.docs/scripts/evidencias_plan_a.py --pb PB-32`) | **Superada**; ningún fichero cambia |

No se ejecuta `./tools/check_all.sh` completo (el encargo pide los gates ligeros, la suite de A y las cuotas; el commit es local).

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t180_hallazgos_t163.py tests/test_t163_hallazgos_t160.py tests/test_t160_reejecucion_certificado.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t66_evaluacion.py tests/test_t66_propuestas.py tests/test_fase4_huecos.py tests/test_t53_evaluacion_y_almacen.py tests/test_t87_datos.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rf ../../.docs/tickets/T-163/revisores/r01_01_ataques.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rf ../../.docs/tickets/T-160/revisores/r01_01_ataques.py
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider                         # suite completa, una vez
cd ../..
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/python .docs/scripts/evidencias_plan_a.py && .venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-32
# mutantes, cada uno en su copia desechable con bloque_a/ entero y .docs/tickets/T-160 y T-163:
.venv/bin/python .docs/tickets/T-180/mutantes_t180.py <copia «…_mut»>
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-163/revisores/r01_02_mutantes.py <copia «…_mut»> tests/test_t180_hallazgos_t163.py
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia «qa31_…_mut»> \
  tests/test_t163_hallazgos_t160.py tests/test_t180_hallazgos_t163.py ../../.docs/tickets/T-160/revisores/r01_01_ataques.py -k "not auditoria_ct10_posterior"
```

## Ronda de cierre (QA r01 APTO; H-01 bajo subsanado, por la regla del operador del 16-11-2026)

- **H-01:** nueva prueba `test_cierre_h01_en_el_borde_ct04_no_es_mas_estricto_que_la_propuesta` en `tests/test_t180_hallazgos_t163.py`. El fichero da 28 passed.
- **Mutantes:** `revisores/r01_02_mutantes.py --solo V01` deja V01 muerto con las pruebas del ticket: 14 mutantes, 0 vivos.
- **Cuotas:** ruff 2813.
