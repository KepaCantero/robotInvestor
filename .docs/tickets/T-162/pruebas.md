# T-162 · Pruebas

Todo con el cliente simulado (`MockClient`), sin red ni coste, con el reloj del almacén fijado (`AS_OF` 2026-06-05).

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`bloque_a/11_Ejecutor`, `pytest -q`) | 6897 recogidas (6919 menos las 22 nuevas; línea base del gate: 607) | 6919 recogidas: 6900 pasan, 2 omitidas y 17 fallan (1 h 38 min, con otras suites en la máquina, carga ≈ 11): las 14 de goldens (abajo); `test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`, que pasa tras regenerar las evidencias (23/23 en `test_fase4_mapa.py`); y `test_t102_filtro.py::test_textos_largos_en_tiempo_lineal` y `::test_r05_h37_sufijo_en_tiempo_lineal`, de tiempo, que repetidas solas pasan (2/2): eran de carga |
| `tests/test_t162_respuesta_final.py` (nueva) | — | 22 pasan |
| Vecinas: `test_integracion`, `test_fase4_huecos`, `test_t65_qa_r01`, `test_t66_propuestas`, `test_t101_v6`, `test_t87_contratos`, `test_t92_revision` y las 22 nuevas | — | todas pasan |
| Goldens `tests/test_fase3_goldens.py` | pasan | 14 fallan, todas por la misma diferencia esperada (`formas_flujos_mock.json`, flujo `consulta_que_escala`): ver abajo |

## Criterio de aceptación → prueba

| Criterio | Prueba (en `tests/test_t162_respuesta_final.py` salvo que se diga) |
| --- | --- |
| CA-1 final enlazada y validada | `test_ca1_la_final_sale_despues_de_la_provisional_enlazada_a_la_consulta_y_al_run` (orden tras la provisional y tras el CT-02 del RUN-, `query_id`, `run_id`, `provisional_msg_id`, `respuesta_final.ESQUEMA`, `Mensajeria.validar` y el esquema derivado del Anexo B); `test_ca1_una_final_que_no_cumple_el_esquema_no_sale_ni_se_registra` (4 casos: referencia de otro prefijo, ruta N0, estado incoherente y un IBAN que rechaza la mensajería por R8; ni mensaje ni F5, y sin el defecto sale una vez); `test_ca1_una_consulta_n0_o_inexistente_no_admite_final` |
| CA-2 referencias del RUN- que existen | `test_ca2_las_referencias_son_las_del_run_y_existen_en_la_memoria` (RUN- primero; OPP- del top-3 en su orden; sus TND-, CLM- y PRG-; cada una es la clave de una entrada; confianza la más baja); `test_ca2_la_final_queda_en_f5_en_la_misma_qry`; `test_ca3_una_referencia_que_no_existe_no_se_cita` |
| CA-3 fallo cerrado | `test_ca3_si_el_run_falla_la_final_lo_dice_sin_referencias` (FALLIDO, sin referencias, incidencia HERRAMIENTA con la clase y sin el texto del error, que llevaba un IBAN); `test_ca3_un_run_sin_entrega_da_sin_entrega` (RUN- real sin tipos analizables); `test_ca3_un_run_bloqueado_o_sin_registro_da_sin_entrega` (2 casos: G3 bloqueó y RUN- que no consta en F5); `test_ca3_sin_escalado_la_final_dice_que_no_se_ejecuto`; `test_ca3_sin_escalado_por_la_cli` (`bloque-a consulta --sin-escalado`) |
| CA-4 idempotencia | `test_ca4_enviar_dos_veces_no_duplica` (la segunda devuelve la misma con `repetido`, sin mensaje ni F5 nuevos); `test_ca4_dos_hilos_a_la_vez_envian_una_sola_final` |
| CA-5 determinismo | `test_ca5_dos_ejecuciones_dan_la_misma_final` (dos almacenes nuevos, mismas entradas: las dos CT-03 RETORNO iguales byte a byte) |
| CA-6 nada de lo anterior cambia | `test_ca6_la_provisional_no_cambia` (mismas claves que en el golden congelado y el mismo contenido que su F5); `test_ca6_la_pregunta_repetida_no_cuenta_la_final`; `test_ca6_la_consulta_n0_no_lleva_final`; vecinas (`test_consulta_que_escala_y_pregunta_repetida`, `test_pb07_la_consulta_de_contraste_responde_provisional_con_nivel_y_plazo`, `test_r01_h08_pregunta_repetida_con_las_veces_de_la_configuracion`, `test_h02_un_escalado_sin_tipo_va_a_un_tipo_activo`, la del Respondedor V6) |
| CA-7 PB-07 de punta a punta | `test_pb07_de_punta_a_punta_con_el_simulado` (la pregunta del plan; CT-03 encargo → CT-05 AD_HOC → CT-02 → provisional → final); el mapa la da por AUTOMATICA y `docs/evidencias_pruebas_bloque_a.md` por «Superada» |
| CA-8 cuotas y gates | ver «Gate» |

## Regresiones

Con `orquestacion.py` sin el cambio de T-162 (y el resto igual), `tests/test_t162_respuesta_final.py` da **19 fallan y 3 pasan**
(`KeyError: 'respuesta_final'` y ninguna segunda CT-03). Las 3 que pasan no dependen de la consulta: la guarda de la provisional
(`test_ca6_la_provisional_no_cambia`, que tiene que pasar igual antes y después) y dos que llaman a `respuesta_final.enviar`
directamente (`test_ca4_dos_hilos_…`, `test_ca1_una_consulta_n0_o_inexistente_…`). Restaurado el cambio, pasan las 22.

## Goldens (sin re-congelar)

`../../.venv/bin/python tests/goldens_ct.py` da 1 diferencia: `formas_flujos_mock.json` (diff exacto en `analisis-tecnico.md`).
En `test_fase3_goldens.py` eso hace fallar 14 pruebas, todas con esa misma diferencia como motivo (las que comparan lo generado con
lo congelado, las que mutan un golden y esperan exactamente su diferencia, las de re-congelado y la de orden de las formas).
Comprobación aparte (sin re-congelar en esta copia): en una copia del scratchpad con `bloque_a/`, `docs/` y `sistema_global/seguimiento/` y el `formas_flujos_mock.json` generado en lugar del congelado, `test_fase3_goldens.py` pasa entera (102/102). Es decir, al re-congelar ese fichero no queda nada más en rojo.

## Gate

| Comprobación | Resultado |
| --- | --- |
| `tools/refs_vivas.py`, `tools/secrets_scan.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py` | los cuatro en verde (código de salida 0); el corpus, 695 archivos íntegros |
| ruff (`.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l`) | 2821 (cuota 2821; igual que al empezar) |
| mypy de A (`.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 109 (cuota 109; igual que al empezar) |
| `.docs/scripts/evidencias_plan_a.py` (comprobación y `--ejecutar`) | comprobación: 67 pruebas del plan, 201 automáticas citadas, todas existen (AUTOMATICA 32, PARCIAL 26, PENDIENTE_API 7, DOCUMENTAL 1, REQUIERE_USUARIOS 1); `--ejecutar`: 201 de 201 superadas, PB-07 «Superada» (33 filas «Superada», antes 32) |
| `./tools/check_all.sh` completo | no se ejecuta en esta copia: los goldens quedan en rojo hasta el re-congelado coordinado |

## Comandos usados

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t162_respuesta_final.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t162_respuesta_final.py tests/test_integracion.py \
  tests/test_fase4_huecos.py tests/test_t65_qa_r01.py tests/test_t66_propuestas.py tests/test_t101_v6.py tests/test_t87_contratos.py \
  tests/test_t92_revision.py tests/test_fase3_goldens.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider          # suite completa de A
../../.venv/bin/python tests/goldens_ct.py
cd ../..
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/python .docs/scripts/evidencias_plan_a.py && .venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
```
