# T-163 · Pruebas

Copia: worktree en la instantánea `a456e04` con `.venv` enlazado. Sin red ni gasto; cliente simulado. Máquina cargada (carga 8–15
en 4 núcleos, con otras suites en marcha).

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A completa (`pytest -q` en `bloque_a/11_Ejecutor`) | 6895 superadas y 2 omitidas (las mismas sin las 48 nuevas; ninguna se quita) | 6942 superadas, 2 omitidas y 1 fallo de carga (abajo) en 1 h 43 min; la que falló, sola: superada |
| `tests/test_t163_hallazgos_t160.py` (nuevo) | — | 48 superadas |
| `tests/test_t160_reejecucion_certificado.py` | 16 | 16 superadas (sin cambios) |
| Vecinas adaptadas (`test_fase4_huecos`, `test_t53…`, `test_t66_evaluacion`, `test_t66_propuestas`, `test_t87_datos`, filtro `pb33 or pb32 or r13 or ece_cero or umbral_de_revocacion or revoca or cert or pa10 or pa03`) | — | 43 superadas |
| `.docs/tickets/T-160/revisores/r01_01_ataques.py` | 4 `test_h0*` fallan (H-01 ×2, H-02, H-03) | 34 superadas, las `test_h0*` incluidas; 1 falla por diseño (abajo) |
| Mutantes del revisor (`r01_03_mutantes.py`, 26) | 22 muertos, M13 y M14 equivalentes, M12 y M17 vivos | 24 muertos, M13 y M14 equivalentes, ninguno vivo real, ninguno sin aplicar |
| Mutantes de T-163 (`.docs/tickets/T-163/mutantes_t163.py`, 15) | — | 14 muertos, T14 equivalente |

**El fallo de la suite completa:** `tests/test_t102_filtro.py::test_r05_h37_sufijo_en_tiempo_lineal`, una prueba de tiempo
(2,14 s frente a un tope de 2 s), la misma que falló por carga en la QA de T-160. Repetida sola: superada en 25 s (lo que tarda la
colección). Ni la prueba ni el código que prueba cambian aquí.

**La de r01_01 que falla por diseño:** `test_una_auditoria_ct10_posterior_que_no_coincide_no_impide_la_aprobacion` documentaba el
comportamiento de H-05 («pasa: documenta el comportamiento», qa.md de T-160). Con H-05 corregido, CT-04 rechaza con «una
re-ejecución CT-10 posterior de CALC-2026-0001 no coincide (CALC-2026-0003)», y la prueba nueva
`test_h05_una_ct10_posterior_del_mismo_soporte_que_no_coincide_impide_la_aprobacion` fija lo contrario. El script del revisor no
se toca; se ejecuta con `-k "not auditoria_ct10_posterior"`.

## Criterio de aceptación → prueba

| Criterio | Prueba (en `tests/test_t163_hallazgos_t160.py` salvo que se diga) |
| --- | --- |
| CA-1 (H-01) | `test_h01_ct04_no_aprueba_un_certificado_con_cifras_distintas_…` (8 cifras), `test_h01_dentro_de_la_tolerancia_…` (límite), `test_h01_…_de_otro_metodo_…`, `test_h01_un_soporte_sin_metodo_anterior_a_t163_no_vale`, `test_h01_…_con_otras_entradas`, `test_h01_cada_reejecucion_sirve_a_un_solo_certificado`, `test_h01_la_reejecucion_tiene_que_ser_posterior_al_soporte`, `test_h01_un_soporte_mal_formado_no_lanza_y_no_vale` (5); r01_01 `test_h01_*` |
| CA-2 (H-05) | `test_h05_una_ct10_posterior_…_no_coincide_impide_la_aprobacion`, `test_h05_una_ct10_posterior_que_coincide_no_impide_…`, `test_h05_un_vigente_cuyo_soporte_no_coincide_despues_deja_de_valer_y_se_vuelve_a_proponer` |
| CA-3 (H-02) | `test_h02_un_vigente_sin_reejecucion_no_habilita_probabilidades_y_la_revision_lo_revoca_y_vuelve_a_proponer`, `test_h02_mientras_no_haya_revision_…_bloquea_otra_aprobacion_…`; r01_01 `test_h02_*`; publicación con un VIGENTE legítimo: `test_t160…::test_ca6_pb32_de_punta_a_punta…`, `test_fase4_huecos.py::test_pb32_la_probabilidad_se_publica_solo_en_la_celda_certificada…`, `test_t87_datos.py::test_r13_certificado_por_metodo_en_la_entrega` |
| CA-4 (H-03) | `test_h03_un_si_que_no_esta_en_el_registro_no_deja_certificado` (true y false), `test_h03_sin_solo_endurecer_el_certificado_legitimo_nace_vigente`; r01_01 `test_h03_*` |
| CA-5 (H-04) | `test_h04_fc_eval_con_fechas_rechaza_…` (0, −1, 1, True, False, 1,5, 2,0, "x", "10", None, [10]), `test_h04_…_acepta_un_entero_desde_el_minimo` (2, 10, np.int64(10)), `test_h04_sin_fechas_el_minimo_no_se_lee_como_antes`, `test_h04_el_evaluador_usa_el_mismo_suelo_que_el_motor` |
| CA-6 (H-06) | `test_h06_m12_la_materialidad_mueve_el_q90_del_nulo` (mata M12), `test_h06_m17_ct04_no_aprueba_un_soporte_de_otra_ficha_…` (mata M17); ejecución de `r01_03_mutantes.py` |
| CA-7 | `r01_01_ataques.py` (arriba) |
| CA-8 | suite completa, vecinas, goldens, gates ligeros, cuotas y `evidencias_plan_a.py --pb PB-32` (abajo) |

## Regresiones

- **Mutantes de T-163** (`.docs/tickets/T-163/mutantes_t163.py`, copia desechable `…/scratchpad/t163b_mut`, borrada): cada
  comprobación nueva quitada hace fallar `test_t163_hallazgos_t160.py`: T01 método, T02 entradas, T03 orden, T04 CT-10
  posterior (H-05), T05 exclusividad, T06 cifras, T07 `certificados_vigentes`, T08 revocación en la revisión, T09 CT-04 con los
  VIGENTE de F6, T10 borrador antes de escribir (H-03), T11 método en la petición, T12 `huella_entradas`, T13 validación de
  FC-EVAL-001, T15 suelo a 1: muertos. T14 (aceptar booleanos) es equivalente: con el suelo en 2, `True` (1) y `False` (0) ya
  quedan por debajo; la exclusión solo importa si el suelo baja a 1 (T15 lo cubre).
- **Mutantes del revisor** (`r01_03_mutantes.py` con `.docs/scripts/mutantes_revisor_ampliado.py`, copia desechable
  `…/scratchpad/qa31_t163_mut`, borrada), contra sus tres ficheros, `test_t163_hallazgos_t160.py` y `r01_01_ataques.py` sin la
  prueba de H-05: los 26 aplican; M12 y M17 mueren ahora; M13 y M14 siguen siendo los equivalentes de la QA.
- **Las `test_h0*` de r01_01** fallan con el código de HEAD (qa.md de T-160) y pasan con T-163.
- **Pruebas adaptadas:** las que escribían un VIGENTE a mano sin re-ejecución ahora lo escriben con
  `conftest.certificado_con_reejecucion` (soporte y CT-10 de verdad). Sin ese cambio, con T-163, las de publicación no publican y
  las de revocación fallan o revocan por otro motivo («sin re-ejecución» en vez de «deterioro»). Sus aserciones no cambian.

## Gate

Sin `./tools/check_all.sh` completo (encargo: gates ligeros y suite de A por separado; hay otras suites corriendo):

| Comprobación | Resultado |
| --- | --- |
| `tests/goldens_ct.py` | coinciden |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | en verde |
| `tools/corpus_integridad.py` | 695 archivos coinciden |
| ruff (3 ejecutores, desde la raíz) | 2816 (≤ 2821; −5: dos avisos nuevos corregidos, cuatro `noqa` sin uso en `conftest.py` y el orden de imports de `test_t87_datos.py`). `tools/cuotas.txt` no se toca: lo baja la sesión coordinadora al juntar |
| mypy A (desde la raíz) | 109 (= cuota) |
| `evidencias_plan_a.py` (comprobar el mapa) | 67 pruebas del plan, 196 citadas y todas existen; el mapa no cambia, no se regenera |
| `evidencias_plan_a.py --pb PB-32` / `--pb PB-33` | PB-32 «Superada»; PB-33 «Superada en parte» (como antes) |

Comandos (desde la raíz de la copia):

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t163_hallazgos_t160.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t160_reejecucion_certificado.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-160/revisores/r01_01_ataques.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t66_evaluacion.py tests/test_t66_propuestas.py \
  tests/test_t53_evaluacion_y_almacen.py tests/test_t87_datos.py tests/test_fase4_huecos.py \
  -k "pb33 or pb32 or r13 or ece_cero or umbral_de_revocacion or revoca or cert or pa10 or pa03"
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider          # en segundo plano
cd ../..
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-32
# mutantes (copia con bloque_a/ entero y .docs/tickets/T-160/revisores/r01_01_ataques.py; nombre con «qa31_» y «_mut»)
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia> \
  tests/test_t163_hallazgos_t160.py ../../.docs/tickets/T-160/revisores/r01_01_ataques.py -k "not auditoria_ct10_posterior"
.venv/bin/python .docs/tickets/T-163/mutantes_t163.py <copia «…_mut»>
```
