# T-101 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `bloque_a/11_Ejecutor/tests` (A) | 476 | 515 (476 sin cambios en sus expectativas + 39 de `tests/test_t101_v6.py`) |
| Cuota de ruff (tres ejecutores) | 3019 | 2987 |
| Cuota de mypy de A | 114 | 109 |

## `tests/test_t101_v6.py` (39)

| Criterio | Pruebas |
| --- | --- |
| CA-1 | La batería de la V5 con `diseno: v5` por defecto (`test_por_defecto_el_diseno_es_v5`); las 476 pasan sin tocarlas |
| CA-2 | `test_kit_completo_no_pierde_nada_y_no_inventa` (×12), `test_nucleo_identico_para_los_doce_y_sin_marcadores`, `test_dos_puntos_de_cache_para_los_analistas`, `test_kit_con_base_desconocida_falla` |
| CA-3 | `test_prospectiva_una_vez_por_lote_con_cobertura`, `test_una_omision_de_prospectiva_se_reintenta_y_se_declara` |
| CA-4 | `test_el_contradictor_solo_ve_la_seleccion_y_todo_lo_entregado_esta_criticado`, `test_si_cae_la_mejor_entra_otra_y_tambien_se_critica` |
| CA-5 | `test_el_sintetizador_escribe_una_vez_despues_de_g3`, `test_el_sintetizador_no_puede_cambiar_la_seleccion` |
| CA-6 | `test_gc1_por_codigo_limita_lo_que_ve_el_analista`, `test_gc1_no_descarta_lo_que_no_tiene_senal` |
| CA-7 | `test_registro_de_cobertura_de_cada_candidata`, `test_el_contrafactual_resuelve_la_muestra_al_vencer_su_horizonte` |
| CA-8 | `test_v6_hace_menos_llamadas_y_lee_mas_cache`, `test_el_simulador_lee_el_nucleo_de_la_cache_entre_analistas` |
| Otros | `test_diseno_desconocido_falla_cerrado`, `test_canales_de_la_v6_solo_con_la_v6`, `test_la_bolsa_del_ciclo_sale_de_los_tipos_sin_cambiar_el_total`, `test_auditor_por_muestreo_sembrado`, `test_tope_de_tokens_de_los_prompts_por_papel`, `test_v6_no_llama_a_los_papeles_que_pasan_a_codigo`, `test_v6_declara_sus_limitaciones`, `test_las_consultas_n0_las_responde_el_respondedor`, `test_contradictor_de_otro_proveedor`, `test_consumo_registra_intentos_y_latencia`, `test_ciclo_v6_entrega_y_valida` |

## Banco con el simulador (CA-8)

`.venv/bin/python .docs/scripts/comparar_disenos_a.py <carpeta> --semanas 2`: los doce perfiles, dos ciclos C1 desde el 2026-06-05, con los datos sintéticos de ejemplo. **Solo flujo y consumo; no dice nada de la calidad.**

| Métrica | V5 | V6 | V6 / V5 |
| --- | --- | --- | --- |
| Llamadas | 89 | 56 | 0,63 |
| Tokens de entrada (con caché) | 1.969.619 | 805.831 | 0,41 |
| Leídos de caché | 1.389.717 | 509.414 | 0,37 |
| Escritos en caché | 384.585 | 144.806 | 0,38 |
| Entrada sin caché | 195.317 | 151.611 | 0,78 |

Llamadas por papel en los dos ciclos:
- **Bajan:**
  - Prospectiva, de 12 a 3;
  - Contradictor, de 16 a 6;
  - Curador, de 12 a 0;
  - Analizador más Redactor, de 4 a 2 del Sintetizador.
- **Se mantienen:**
  - los Analistas, 36 en los dos diseños: cribado y respuesta a las objeciones;
  - el Lector de evidencia sustituye al Documentador, de 9 a 9.

**Opciones entregadas:**
- **Coinciden:** en DIV, IDX, FON, INM, CRI y ALT la selección es la misma.
- **Coinciden en dos de tres:** en RV y MP, porque el Contradictor simulado critica otras opciones.
- **La V6 entrega menos:**
  - RF: 1 frente a 3;
  - TCV: 1 frente a 3;
  - MON: 0 frente a 1.

  El motivo es GC1 por código con el umbral 0,75 de la configuración frente al 0,55 que aplica el Analista simulado de la V5 (límite del análisis técnico). La exploración de GC1 detectó los falsos negativos.

## Gate

`./tools/check_all.sh` completo con `commit_limpio.sh` en el commit.
