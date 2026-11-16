# T-158 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A, `bloque_a/11_Ejecutor` (recogidas) | 6640 | 6695 (+55, `tests/test_t158_guias.py`) |
| Bloque A, suite completa (una ejecución, 15-11-2026, 30 min) | — | 6692 superadas, 2 omitidas, 1 fallo: `test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`, esperado porque el documento de evidencias aún no estaba regenerado; tras regenerarlo, se repitió solo esa y pasa (ver abajo) |
| `tests/test_t158_guias.py` | — | 55 superadas |
| Vecinas: `test_t126_pb26_pb48.py`, `test_t126_r02.py`, `test_fase3_goldens.py`, `test_fase4_mapa.py`, `test_t158_guias.py`, `test_t120_r8_y_lecciones.py` | — | 218 superadas (antes de cambiar el mapa) |
| Goldens de contratos (`tests/goldens_ct.py`) | coinciden | coinciden (sin re-congelar) |
| ruff (cuota 2831) | 2831 | 2828 |
| mypy de A (cuota 109) | 109 | 109 |

Línea base del gate: A ≥ 607 (sin cambio; la suite no baja). Ninguna prueba existente se ha quitado ni debilitado.

## Criterio de aceptación → prueba

| Criterio | Prueba (`tests/test_t158_guias.py` salvo otra indicación) |
| --- | --- |
| CA-1 emisión, acuse, CT-18, versión | `test_emitir_deja_la_guia_en_ha_con_su_acuse_y_la_envia_por_ct18`, `test_la_version_siguiente_sustituye_a_la_vigente`, `test_el_ejemplo_del_prompt_del_orquestador_cumple_el_esquema` |
| CA-2 fallo cerrado | `test_el_esquema_rechaza_cuerpos_mal_formados` (14 casos), `test_una_guia_mal_formada_no_se_emite_y_nada_cambia` (9 casos: HA y mensajería sin cambios), `test_un_dato_protegido_en_la_guia_lo_rechaza_la_mensajeria_r8`, `test_una_guia_de_ha_que_no_cumple_el_esquema_no_se_aplica`, `test_si_la_revision_falla_no_se_aplica_ninguna_guia` |
| CA-3 aplicación solo al receptor, F5, fechas | `test_un_item_valido_llega_solo_al_contexto_del_receptor_y_f5_lo_anota`, `test_una_guia_futura_o_caducada_no_se_aplica` (límites: el día de aplicación sí, el de caducidad sí, el siguiente no) |
| CA-4 PB-48 de extremo a extremo (cliente simulado) | `test_pb48_la_guia_que_omite_la_segunda_pasada_se_registra_se_escala_y_se_retira`, `test_pb48_una_guia_ya_vigente_se_revisa_tambien_en_el_siguiente_run`, `test_el_item_de_pb48_cita_la_regla_9_1`, `test_el_receptor_reconoce_los_items_que_contradicen_una_regla` (12 casos), `test_una_guia_corriente_no_es_un_conflicto` (5 casos) |
| CA-5 versión siguiente con el ítem válido | `test_pb48_con_otro_item_valido_la_version_siguiente_conserva_solo_el_valido` |
| CA-6 sin guías no cambia nada | `test_sin_guias_el_ciclo_no_escribe_ni_envia_nada_de_ct18`; `tests/goldens_ct.py` (coinciden); `test_fase3_goldens.py`; suite completa |
| CA-7 determinismo y números de configuración | `test_determinismo_misma_entrada_mismas_entradas_de_ha`, `test_los_limites_salen_de_la_configuracion` |

## Regresiones

- Con el detector anulado (`conflicto_del_item` devuelve siempre `None`, en una copia temporal de `guias.py`), fallan las cuatro pruebas de PB-48 (`-k pb48`: 4 failed); con el código restaurado, pasan (4 passed). Es decir, sin la corrección el ítem de PB-48 llegaría al contexto del Analizador y no quedaría ni COR- ni P3-.
- Las pruebas de T-126 de PB-48 (R23 por construcción, lección que no llega a HT-03) siguen pasando y siguen citadas en el mapa.

## Plan de pruebas (PB-48) y documento de evidencias

- `tests/mapa_plan_pruebas.json`: PB-48 pasa de PARCIAL a AUTOMATICA con cuatro pruebas nuevas; «no comprueba» deja lo que solo existe con el modelo real.
- `.docs/scripts/evidencias_plan_a.py --ejecutar` regenera **todo** `docs/evidencias_pruebas_bloque_a.md` (no hay modo de regenerar una sola fila; `--pb` solo ejecuta y enseña). Se ejecutaron las 175 pruebas citadas: 175 superadas. **Qué cambia en el documento** (diff contra la versión anterior): la cabecera (fecha 2026-11-16 y commit `899ae9e` en lugar de 2026-11-15 y `5098b09`); el resumen («Superada en parte» 37 → 36, «Superada» 21 → 22); la fila de PB-48 («Superada en parte» → «Superada», con el nuevo «comprueba» y «no comprueba»), y su sección (la orden con las cuatro pruebas nuevas y sus cuatro líneas SUPERADA). Ninguna otra fila cambia.
- Tras regenerarlo, `tests/test_fase4_mapa.py` (la única que había fallado en la suite completa) pasa: 23 superadas.

## Gate

- Gates ligeros desde la raíz: `tools/refs_vivas.py` (todas las rutas existen), `tools/secrets_scan.py` (sin hallazgos), `tools/nfc_check.py` (NFC correcto), `tools/corpus_integridad.py` (695 archivos coinciden).
- `./tools/check_all.sh` completo no se ha ejecutado en esta copia (lo hace quien integra; las suites de A-Forex y B no se tocan). Sus piezas de A sí: suite de A, cuotas de ruff y mypy de A, goldens y gates ligeros.

## Comandos usados

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t158_guias.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t126_pb26_pb48.py tests/test_t126_r02.py \
  tests/test_fase3_goldens.py tests/test_fase4_mapa.py tests/test_t158_guias.py tests/test_t120_r8_y_lecciones.py
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider          # suite completa, una vez
cd ../..
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
```
