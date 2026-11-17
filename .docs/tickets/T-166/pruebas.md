# T-166 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t166_entrega_corpus.py` | — | 55 passed |
| `tests/test_fase3_goldens.py` | 192 | 192 passed (la de T-143 lee la V5.2 del histórico; huellas con la V5.3) |
| `test_t157_verificador_ids.py`, `test_t131_preparativos.py`, `test_t148.py` (con el anterior, 149) | pasan | pasan |
| Suite completa de A (`pytest -q -p no:cacheprovider tests`, una vez al final, con la máquina cargada por otros agentes) | 607 (línea base) | 7851 passed, 2 skipped en 47 min; ningún fallo |
| `.docs/scripts/pruebas_scripts.sh` | — | 231 passed |
| Verificador de IDs sobre el corpus | 2 errores, 2 avisos (sale 1) | 0 errores, 1 aviso (RF-1; sale 0) |
| `goldens_ct.py` | coinciden | coinciden (tras `--update --motivo`: solo `huellas.json`) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_ca1_ningun_md_vivo_del_corpus_cita_el_catalogo_v40`, `test_ca1_cada_prompt_mc_cita_el_catalogo_vigente_donde_citaba_el_v40` (×5), `test_ca1_el_patron_ve_las_formas_de_citar_el_v40` |
| CA-2 | `test_ca2_el_verificador_no_da_ningun_error_sobre_el_corpus` (corpus real, `vi.verificar`), `test_ca2_el_ejemplo_del_registro_de_calculos_cita_una_ficha_vigente_del_mc10` (contra `servicio.IMPLEMENTADAS` y `CATALOG_VERSION`), `test_ca2_el_ejemplo_del_evaluador_cita_una_rf_que_existe_en_f9` (ficha en F9, no en el Registro de bajas, TF-05, Aprobada) |
| CA-3 | `test_ca3_en_01_gobernanza_solo_la_v53_y_la_v52_en_el_historico`, `test_ca3_fuera_del_anexo_b_solo_cambian_la_cabecera_y_el_registro_de_cambios`, `test_ca3_dentro_del_anexo_b_solo_cambia_la_lectura_y_se_anade_la_final_de_ct03`; SHA-256 de la V5.2 en el histórico = el del manifiesto anterior (`d8f9e3d0…`, diff del manifiesto) |
| CA-4 | `test_ca4_cada_archivo_corregido_es_su_version_anterior_con_solo_la_sustitucion` (×8: deshacer la sustitución da el texto del histórico byte a byte; `.docx` en el histórico y no en vivo), `test_ca4_el_historico_solo_tiene_lo_que_sustituye_esta_entrega`; hashes del histórico = los del manifiesto anterior |
| CA-5 | `test_ca5_el_anexo_b_describe_la_respuesta_final_como_respuesta_final_py`; 12 mutantes de código (`test_ca5_un_cambio_en_respuesta_final_py_se_nota`) y 10 de prosa (`test_ca5_un_cambio_en_la_prosa_se_nota`); `test_ca5_el_resultado_sale_de_f5_como_dice_el_anexo_b` (×6, con `_resultado`), `test_ca5_la_confianza_es_la_mas_baja_como_dice_el_anexo_b` |
| CA-6 | `test_ca6_el_derivado_de_ct03_admite_y_valida_la_respuesta_final`; `test_t162_respuesta_final.py::test_ca1_la_final_sale_despues_de_la_provisional_enlazada_a_la_consulta_y_al_run` (la final real contra el derivado); `test_fase3_goldens.py` entero (prosa y derivado: opcionales marcados, listas de la prosa, campos en su párrafo, divergencias vacías) |
| CA-7 | `test_ca7_el_ejecutor_carga_el_prompt_corregido_del_evaluador`, `test_ca7_los_prompts_mc_se_encuentran_por_nombre_en_02_y_no_en_el_historico` |
| CA-8 | `tools/corpus_integridad.py` (705 coinciden), `git diff -U0 tools/corpus_manifest.txt` (18 quitadas, 27 puestas: solo rutas de la entrega y el README índice; análisis técnico), `tools/refs_vivas.py`, `.docs/scripts/prueba_refs_vivas.py` (25/25) |
| CA-9 | suite completa, cuotas y gates (abajo) |

## Regresiones

- **Sin la corrección fallan.** En una copia de `bloque_a/` (para no tocar la suite en marcha), con «Catálogo V4.0» repuesto en la regla 1 de MC-01, «FX-MC10-003» en el Registro de cálculos y «RF-0123» en el Evaluador: 8 fallan (CA-1 ×2, CA-2 ×3, CA-4 ×2, CA-7) y 47 pasan. Quitando del Documento 0 V5.3 la línea «Respuesta final (V5.3)»: 12 de las pruebas de CA-3 y CA-5 fallan (las nominales y los mutantes de prosa, que avisan de que su texto ya no está). La copia se borró después.
- **Las pruebas de la final fallan si el código o la prosa cambian:** los 22 mutantes de CA-5 están en la propia suite y todos dan diferencias.
- **La primera pasada del verificador tras la entrega dio 1 error y 1 aviso:** la entrada nueva del registro del README índice citaba los identificadores viejos (el verificador lee ese README). Se reescribió sin ellos; `test_ca1_ningun_md_vivo…` y `test_ca2_el_verificador…` lo cubren.

## Gate

- ruff: 2813 (cuota 2813); mypy de A: 109 (cuota 109). `ruff check` de los dos archivos tocados: limpio.
- `corpus_integridad.py`, `nfc_check.py`, `secrets_scan.py`, `refs_vivas.py`, los tres `por_defecto.yaml` parsean: en verde.
- `evidencias_plan_a.py` (comprobación): el mapa no cambia (67 pruebas del plan, 211 citadas, todas existen); no hace falta regenerar las evidencias.
- `.docs/scripts/borrador_anexo_b.py --comprobar`: 0.
- No se pasa `check_all.sh` completo: la suite de A-Forex y la de B no se tocan (otro bloque) y hay otros agentes con carga en la máquina; los gates de este ticket se pasaron uno a uno.

## Ronda r02 (QA r01 NO APTO, H-01 a H-06)

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t166_entrega_corpus.py` | 55 → 73 passed: 2 mutantes de código nuevos (H-01), 11 mutantes de prosa nuevos (6 de `r01_02`, H-04, y 5 de las frases corregidas), `test_ca5_los_errores_de_control_son_los_que_paran_la_consulta` (H-01) y `test_ca5_sin_resultado_la_confianza_…` ×4 (H-05) |
| `test_t166`, `test_fase3_goldens`, `test_t162_respuesta_final`, `test_t169_hallazgos_t162`, `test_t169_r02`, `test_t157_verificador_ids` juntos | 385 passed |
| `revisores/r01_01_final_contra_anexo_b.py` | 14 passed (las `hallazgo_*` fijan el comportamiento que ahora dice el texto) |
| `revisores/r01_02_mutantes_prosa.py` | vivos: 0 |
| `revisores/r01_03_mutantes_codigo.py --resto` | M1, M2, M4 y M5 muertos por T-166 (M4, antes vivo en todas, lo mata la prueba de H-05); M3 y M6 viven en T-166 y los matan T-162/T-169, como aceptó la QA r01; el código queda restaurado (`git status` de `bloque_a/` limpio) |
| `revisores/r01_04_prompts_y_huellas.py` | 28 agentes, ninguno fuera de `02`; AG-20 con RF-0046, sin RF-0123; huella estable |
| `revisores/r01_05_manifiesto.py` | base 696 → 705; quitadas 9, puestas 18, cambiadas 9; fuera de alcance: nada; fallos: ninguno |
| `goldens_ct.py` | coinciden (tras `--update --motivo "T-166 r02 …"`: solo `huellas.json`) |
| `corpus_integridad.py` | 705 coinciden; frente a la r01 solo cambia la línea de la V5.3; `git diff -- bloque_a/99_Historico_V5.2` vacío |
| Verificador de IDs | 0 errores, 1 aviso (RF-1); sale 0; auditoría regenerada |
| `refs_vivas.py`, `nfc_check.py`, `secrets_scan.py`, `borrador_anexo_b.py --comprobar` | en verde |
| Cuotas | ruff 2813 (≤ 2813), mypy de A 109 (≤ 109): no suben |

La suite completa de A no se repite en la r02: el cambio es de texto del Documento 0 y de una prueba nueva; las suites que leen el Documento 0, los goldens y la respuesta final (arriba) pasan. `origin/develop` no tiene commits nuevos sobre la base `a9210c0`: no hace falta rebasar.

## Ronda r03 (QA r02 NO APTO, H-07)

| Comprobación | Resultado |
| --- | --- |
| `test_t166_entrega_corpus.py` + `test_fase3_goldens.py` | 269 passed (T-166: 73 → 77) |
| `revisores/r01_01` + `revisores/r02_01` | 20 passed |
| `revisores/r01_02` | vivos: 0 |
| `revisores/r01_03 --resto` | M1, M2, M4 y M5 muertos por T-166; M3 y M6, por T-162/T-169; código restaurado |
| `revisores/r01_04` · `r01_05` | AG-20 con RF-0046, huella estable · 696 → 705, fallos: ninguno |
| `goldens_ct.py` · `corpus_integridad.py` · verificador | coinciden · 705 · 0 errores (rc 0) |
| `refs_vivas.py` · `nfc_check.py` · `borrador_anexo_b.py --comprobar` | en verde |
| Cuotas | ruff 2813 (≤ 2813), mypy de A 109 (≤ 109) |
