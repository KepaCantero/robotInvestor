# T-160 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`bloque_a/11_Ejecutor`, recogidas) | 6 729 | 6 745 (+16, `tests/test_t160_reejecucion_certificado.py`) |
| Bloque A, ejecución completa (`-p no:cacheprovider`, 28 min) | — | 6 743 superadas, 2 omitidas (skip), 0 fallos |
| Vecinas (T-160, T-66 evaluación y propuestas, T-53, T-87, T-157, T-112, T-118, T-121, unitarias, goldens de fase 3) | — | 572 superadas |
| Certificados, PB-32, PA-10, PA-03, PA-09 y Holm en `test_fase4_huecos`, `test_integracion` y vecinas (`-k`) | — | 52 superadas |
| Plan de pruebas (`evidencias_plan_a.py --ejecutar`) | Superada 22 · en parte 36 | Superada 23 · en parte 35; 184 de 184 pruebas citadas superadas; PB-32 «Superada» |
| Goldens de contratos (`tests/goldens_ct.py`) | coinciden | coinciden (sin re-congelar) |

Cuotas (desde la raíz): ruff 2828 → **2825** (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l`); mypy A 109 → **109** (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l`). `tools/cuotas.txt` no se toca (lo ajusta la sesión coordinadora).

## Criterio de aceptación → prueba

| Criterio | Prueba (`tests/test_t160_reejecucion_certificado.py` salvo indicación) |
| --- | --- |
| CA-1 nominal | `test_ca1_el_certificado_lleva_su_reejecucion_ct10_coincidente_y_el_calculo_que_lo_sostiene` |
| CA-2 no coincide | `test_ca2_una_reejecucion_que_no_coincide_no_deja_certificado_y_registra_la_incidencia` (y que en la revisión siguiente, ya coincidente, se propone) |
| CA-3 no se puede re-ejecutar | `test_ca3_sin_motor_no_hay_certificado`, `test_ca3_el_motor_no_sirve_la_ficha_que_sostiene_el_certificado`, `test_ca3_los_datos_del_artefacto_no_se_pueden_resolver_en_la_reejecucion`, `test_ca3_una_reejecucion_imposible_que_lanza_no_deja_certificado` |
| CA-4 cifras distintas y materialidad | `test_ca4_si_el_motor_no_reproduce_las_cifras_del_certificado_no_hay_certificado`, `test_ca4_dentro_de_tolerancia_y_lejos_de_los_umbrales_certifica`, `test_ca4_dentro_de_tolerancia_pero_material_no_certifica`, `test_ca4_la_materialidad_mueve_cada_cifra_en_contra_del_certificado` (límites: cada umbral a una fracción de la tolerancia) |
| CA-5 CT-04 | `test_ca5_ct04_no_pone_en_vigor_un_propuesto_sin_reejecucion_coincidente` (cuatro propuestas falsas, F6 sin cambios, y por `Bloque.decision`), `test_ca5_una_propuesta_antigua_sin_reejecucion_se_retira_y_la_celda_se_vuelve_a_proponer`; vecinas `test_t66_evaluacion.py::test_pa10_*` y `test_t66_propuestas.py::test_pa10_ct04_*` |
| CA-6 PB-32 de punta a punta | `test_ca6_pb32_de_punta_a_punta_con_el_cliente_simulado` (C5 del Evaluador → un CERT- de RF × H3 × método con CT-10 coincidente, ninguno de RV → CT-04 → `Bloque.ciclo` con `MockClient`: probabilidad solo en RF H3 con `certificado_ref`, G3 APTO, C10 en OK) |
| CA-7 D-1 | `test_ca7_la_tasa_base_escribe_la_version_vigente_del_catalogo`, `test_ca7_el_verificador_de_ids_ya_no_ve_la_version_escrita_a_mano` |
| (FC-EVAL-001 con conglomerados) | `test_fc_eval_con_fechas_da_la_muestra_efectiva_y_sin_fechas_como_antes` (con fechas, n_eff y el IC por conglomerados; sin ellas, como antes; con fechas sin mínimo, rechazo; CT-10 coincide) |
| CA-8 evidencias | `.docs/scripts/evidencias_plan_a.py --ejecutar` → PB-32 «Superada»; `tests/test_fase4_mapa.py` en la suite |
| CA-9 regresión | suite de A completa, vecinas, goldens, gates ligeros y cuotas (arriba y abajo) |

## Regresiones

Las 16 pruebas nuevas se ejecutaron contra una copia de HEAD (`git archive HEAD bloque_a`, en
`scratchpad/rev160`) a la que solo se añadieron los ayudantes puros nuevos de `evaluador.py` (`_num`, `cifras_certificado`,
`holgura_tolerancia`, `criterio_desfavorable`) para que el fichero de pruebas se pudiera importar, sin el cambio de
comportamiento: **15 fallan y 1 pasa** (`test_ca4_la_materialidad_mueve_cada_cifra_en_contra_del_certificado`, que prueba esos
ayudantes). Sin la corrección: se emite el certificado sin re-ejecución (CA-1 a CA-4 y CA-6), CT-04 aprueba propuestas sin ella
(CA-5), FC-EVAL-001 ignora las fechas (n_eff nulo) y la tasa base escribe 4.0 (CA-7, y el verificador da el ERROR).

Las cuatro pruebas de `test_t66_evaluacion.py` que esperan un certificado (`test_pa10_certificado_nace_propuesto…`,
`test_pa10_aprobar_certificados_por_ct04`, `test_pa10_desactivado…`, `test_pa03_certificado_guarda_n_y_n_eff`) fallaban con el
cambio porque construían el Evaluador sin Motor; ahora reciben uno (`_con_motor`) y sus aserciones no cambian.

## Gate

Gates ligeros desde la raíz, en verde: `tools/refs_vivas.py` (todas las rutas existen), `tools/secrets_scan.py` (sin hallazgos),
`tools/nfc_check.py` (NFC), `tools/corpus_integridad.py` (695 archivos coinciden). `git diff --check` limpio.
`./tools/check_all.sh` completo no se ejecuta en esta copia (hay otras suites corriendo); lo pasa la sesión coordinadora al
integrar.

Comandos:

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t160_reejecucion_certificado.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t160_reejecucion_certificado.py tests/test_t66_evaluacion.py \
  tests/test_t66_propuestas.py tests/test_t53_evaluacion_y_almacen.py tests/test_t87_datos.py tests/test_t157_verificador_ids.py \
  tests/test_t112_motor.py tests/test_t118_hallazgos.py tests/test_t121_hallazgos.py tests/test_unitarias.py tests/test_fase3_goldens.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t66_evaluacion.py tests/test_fase4_huecos.py \
  tests/test_t66_propuestas.py tests/test_t53_evaluacion_y_almacen.py tests/test_t87_datos.py tests/test_integracion.py \
  -k "cert or pb32 or pa10 or pa03 or pa09 or holm"
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider          # suite completa, en segundo plano
cd ../..
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
```
