# T-177 · Pruebas

## Recuentos

| Suite | Antes | Después |
| --- | --- | --- |
| `bloque_a/11_Ejecutor` (recogidas) | 8 188 | 8 204 (+16, `tests/test_t177_c4_credenciales.py`) |
| `bloque_a/11_Ejecutor` (superadas en el gate) | — | 8 202 passed (base ≥ 607) |
| `bloque_b/11_Ejecutor` | 176 | 176 (sin tocar) |
| Evidencias del plan (pruebas citadas) | 240 | 250 de 250 superadas |

## Matriz criterio → prueba

| Criterio | Pruebas |
| --- | --- |
| CA-1 (el BFA recibe la bóveda sin valores y devuelve la solicitud) | `test_t177_pb58_c4_bfa_solicita_y_coordinador_emite_ct25`, `test_t177_pb58_criterio_completo` (claves exactas del encargo), `test_t177_cli_credencial_c4` |
| CA-2 (CT-25 AG-01 → BROKER con AG-16, uso, impacto; CRD- sin valor; C4- en F5) | `test_t177_pb58_c4_bfa_solicita_y_coordinador_emite_ct25` |
| CA-3 (deduplicación, HT-01, segunda C4) | `test_t177_desde_retorno_deduplica_y_comprueba_ht01`, `test_t177_urgencia_y_denegada_no_se_vuelve_a_pedir`, `test_t177_pb58_criterio_completo` |
| CA-4 (fallo cerrado) | `test_t177_retorno_con_valor_se_rechaza_integro` (×3), `test_t177_c4_con_valor_en_el_retorno_del_bfa_no_emite_nada`, `test_t177_solicitudes_mal_formadas_se_descartan_con_motivo`, `test_t177_retorno_vacio_o_sin_solicitudes_no_pide_nada`, `test_t177_configuracion_invalida_falla_antes_de_mutar` (×4), `test_t177_por_defecto_sin_servicios_no_pide_nada` |
| CA-5 (PB-58 pasos 1 a 4; el valor en ningún sitio) | `test_t177_pb58_criterio_completo` (espía de todos los contextos de los agentes y de los mensajes completos; todo el estado salvo `secretos.json`; entregables de dos ciclos), `ciclo_mock_t177.sh` |
| CA-6 (mapa, evidencias, cuotas, goldens) | `evidencias_plan_a.py --ejecutar` (PB-58 «Superada», 250/250), `goldens_ct.py` («coinciden»), gate |

## Regresión: la corrección de `agentes.py`

`test_t177_c4_con_valor_en_el_retorno_del_bfa_no_emite_nada` falló antes de la corrección: el retorno del BFA con `valor` dentro de `solicitudes_credenciales` se guardaba en `estado/cache_resultados.jsonl` (lo encontró la propia prueba). El mutante M04 (quitar la comprobación) lo confirma: la prueba falla sin la corrección.

## Mutantes propios (`.docs/tickets/T-177/mutantes_t177.py`): 12/12 muertos

M01 sin deduplicar · M02 sin comprobar HT-01 · M03 sin rechazo del valor en el Coordinador · M04 sin bloqueo R8 en la capa de agentes · M05 solicitante distinto · M06 sin C4- en F5 · M07 el Coordinador no lee el retorno · M08 urgencia sin filtrar · M09 el BFA ve la ficha entera del índice (vivo en la primera pasada; muerto tras añadir la comprobación de las claves exactas del encargo) · M10 sin validar la configuración · M11 impacto ausente rellenado · M12 el simulado pide también lo PROVISTA.

## Ciclos simulados

- `.docs/tickets/T-177/ciclo_mock_t177.sh`: CLI con `--cliente mock` de punta a punta: `credencial c4` (CRD-2024-0001 SOLICITADA) → `ciclo` (limitación con el CRD-) → `credencial depositar --valor-desde-entorno` → `credencial c4` (PROVISTA, sin solicitud) → `ciclo` (sin la limitación) → el valor no está en ningún archivo salvo `boveda/secretos.json`. Resultado: OK.
- Los ciclos de `test_t177_pb58_criterio_completo` (RV, dos semanas).

## Gate

`./tools/check_all.sh` (completo) en verde: corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas, ruff 2813 (cuota 2813), mypy A 102 (cuota 102), mypy FX 174, mypy B 159, pytest A 8202 passed, FX 68, B 176. Sin `goldens_ct.py --update`.

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q tests/test_t177_c4_credenciales.py
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q tests/test_v51.py tests/test_fase3_goldens.py tests/test_fase4_huecos.py -k "v51 or golden or pb58 or pb59 or pb60 or pb21 or credencial"   # 209 passed
cd ../..
.venv/bin/python .docs/tickets/T-177/mutantes_t177.py
.docs/tickets/T-177/ciclo_mock_t177.sh
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
./tools/check_all.sh
```

## Ronda r02 (QA r01 NO APTO)

| Suite | r01 | r02 |
| --- | --- | --- |
| `tests/test_t177_c4_credenciales.py` | 16 | 43 |
| `bloque_a/11_Ejecutor` en el gate | 8 202 passed | 8 229 passed |
| `revisores/r01_ataques_r8.py` (HALLAZGO invertidos; los límites de detección, con aserción) | 15 (los HALLAZGO pasaban con el fallo) | 15 passed, con los fallos corregidos |
| Evidencias del plan | 250/250 | 263/263 |

| Hallazgo | Prueba (falla sin la corrección: mutante) |
| --- | --- |
| H-01 | `test_t177_r02_h01_valor_en_cualquier_sitio_no_llega_a_la_cache[valor_en_raiz, clave_en_mayusculas]`, `test_t177_r02_solicitud_con_valor_limites`, revisor H01 (M13, M14, M15) |
| H-04 | `test_t177_r02_h04_la_cinta_de_grabacion_no_guarda_el_valor`, revisor H04 (M13) |
| H-02 | `test_t177_r02_h02_otra_grafia_en_la_segunda_c4_no_duplica`, revisor H02 (M16) |
| H-03 | `test_t177_r02_h03_dos_c4_a_la_vez_un_solo_ct25`, revisor `c4_concurrente` con `len(crd) == 1` (M17) |
| H-05 | `test_t177_r02_h05_grafias_de_campos_de_valor` (×11), `test_t177_r02_h05_credencial_ref_no_es_un_valor_y_el_broker_tampoco_lo_cuela`, revisor `campo_credencial` (M18, M19, M24) |
| H-06 | `test_t177_r02_h06_ficha_opaca_en_texto_libre_se_rechaza` (×4, con el LEI), `test_t177_r02_h06_textos_corrientes_y_urls_no_se_rechazan`, `test_t177_r02_ficha_opaca_en_el_retorno_no_llega_a_la_cache`, revisor `motivo_sin_etiqueta` (M20, M21) |
| H-07 | `test_t177_por_defecto_sin_servicios_no_pide_nada` (SIN_SERVICIOS, sin llamada), `test_t177_r02_h07_tope_semanal_real` (M22, M23) |
| Segunda barrera y caché | `test_t177_r02_segunda_barrera_en_agentes` (M04), `test_t177_r02_la_cache_envenenada_no_se_sirve` (M25) |

- **Mutantes:** 25/25 muertos (`.docs/tickets/T-177/mutantes_t177.py`). En la primera pasada, M15 y M24 sobrevivieron. Murieron al añadir un JSON ilegible con llaves y al usar «Credencial» en la respuesta del Broker: «API-Key» lo cazaba también la mensajería.
- **Sin falsos positivos:** backtest mock 2024-01-05 → 2024-02-02 en `origin/develop` (`51d68f5`) y en la r02: `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos byte a byte. Ninguna incidencia de contenido sensible ni «bloqueada por R8».
- **Ciclo de punta a punta** (`ciclo_mock_t177.sh`): OK.
- `test_t177`, el revisor, `test_v51` y `test_fase3_goldens`: 263 passed. `goldens_ct.py`: coinciden.
- **Gate `./tools/check_all.sh`** (antes del rebase): 12/12 en verde. ruff 2813 (cuota 2813), mypy A 102, FX 174, B 159; pytest A 8229, FX 68, B 176.

### Tras el rebase sobre `origin/develop` (`c9daa4e`, con T-174, T-176, T-178 y el encargo a Astra), 18-11-2026

El reinicio del contenedor cortó la serie anterior y dejó aplicado el mutante M23 en `mantenimiento_c4.py`. Se restauró con `git checkout` antes de rebasar. Conflictos solo de documentación: en la deuda técnica y en el README del ejecutor se conservan los dos lados, y las evidencias se regeneran. Se relanzó una vez, en serie (`serie177.sh`, en el scratchpad):

| Comprobación | Resultado |
| --- | --- |
| `evidencias_plan_a.py --ejecutar` | 319 de 319 pruebas citadas superadas; PB-58 «Superada», con su preparación; Superada 40, Superada en parte 18 |
| `./tools/check_all.sh` | 12/12 en verde: ruff 2807 (cuota 2807), mypy A 102, FX 174, B 159; pytest A 8310 passed, FX 68, B 176 |
| `mutantes_t177.py` | 25/25 muertos |
| `ciclo_mock_t177.sh` | OK |
| Backtest mock 2024-01-05 → 2024-02-02, `origin/develop` frente a la r02 | `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos; 0 incidencias de contenido sensible |
| `test_t177`, el revisor y `goldens_ct.py` (antes de la serie) | 58 passed; los goldens coinciden |


## Ronda r03 (QA r02 NO APTO)

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t177_c4_credenciales.py` | 68 (43 en la r02) |
| `r01_ataques_r8.py`, `r02_ataques_r8.py` (HALLAZGO_* invertidos), `r02_concurrencia_presupuesto.py`, `test_t177`, `test_v51` y los vecinos T-174, T-176, T-178 y T-165, las suites R8 (T-103, T-120, T-123, T-130, T-136) y `test_fase3_goldens` | 729 passed; `goldens_ct.py`: coinciden |
| `r02_falsos_positivos.py`, 12 perfiles | V5 y V6, con `texto` y con `sin` (el simulado emite ya `solicitudes_credenciales: []` e `indicadores[].valor` de texto): COMPLETO, 0 bloqueos, 0 informes descartados, limitaciones 2 (V5) y 3 (V6), las mismas que en `c9daa4e` |
| Mutantes (`mutantes_t177.py`) | 33/33 muertos. 12 nuevos: M14, M15, M20 y M27 a M35, sobre el código de la r03 |
| `ciclo_mock_t177.sh` | OK |
| Backtest mock 2024-01-05 → 2024-02-02 frente a `c9daa4e` | `senales.csv` y `pronosticos.csv` idénticos. `metricas.json` difiere solo en el consumo (`tokens_salida` 21 952 → 22 152, `uc` 27,09 → 27,16): son los `indicadores` nuevos del simulado. 0 incidencias de contenido sensible |
| Evidencias | 331/331 |
| `./tools/check_all.sh` | 12/12 en verde. ruff 2807 (cuota 2807); mypy A 102, A-Forex 174 y B 159; pytest A 8335 passed, A-Forex 68 y B 176 |

- **Mutantes M21 y M26** (primera pasada): sobrevivieron porque eran equivalentes. La ficha opaca del subárbol ya la ve la pasada sobre el retorno entero, así que se quitó la comprobación duplicada.
- **M03:** murió con `test_t177_r03_el_coordinador_rechaza_una_clave_de_valor_en_cualquier_sitio`.
- **Regresión de la primera pasada del gate:** `test_t146_presupuesto::test_r02_h05_un_json_muy_anidado…`. Un JSON demasiado anidado para leerlo hacía sensible la respuesta en lugar de dejarla PARCIAL por «JSON no válido». Se corrigió: ahora cuenta como ilegible y decide el prefiltro textual. Su prueba es `test_t177_r03_json_demasiado_anidado`.

## Ronda de cierre de la QA r03 (APTO con H-14 a H-17)

| Comprobación | Resultado |
| --- | --- |
| `test_t177_c4_credenciales.py` | 79 pruebas (68 en la r03). Una `test_t177_cierre_*` por hallazgo, y se ajusta la de `credencial_ref` con texto (H-17) |
| `r03_ataques_regla_comun.py` (HALLAZGO invertidos), r01, r02, la concurrencia, `test_t177`, `test_v51`, los vecinos, las suites R8 y `test_fase3_goldens` | 768 passed. `goldens_ct.py`: coinciden |
| `r03_corpus_formatos.py` | 97 ejemplos; 0 bloqueados tal cual y 0 con una solicitud válida |
| `r02_falsos_positivos.py`, 12 perfiles, V5 y V6, con `texto` y con `sin` | COMPLETO y 0 bloqueos (limitaciones: 2 en V5 y 3 en V6) |
| Mutantes | 39/39 muertos (M36 a M41 son los nuevos; M15, M29 y M34 se reescribieron sobre el código nuevo) |
| `ciclo_mock_t177.sh` | OK |
| Backtest mock frente a `c9daa4e` | `senales.csv` y `pronosticos.csv` idénticos. `metricas.json` cambia solo en el consumo, por los `indicadores` del simulado, como en la r03. 0 incidencias sensibles |
| Evidencias | 335/335 |
| `./tools/check_all.sh` | 12/12 en verde: ruff 2807 (cuota 2807); mypy A 102, A-Forex 174 y B 159; pytest A 8346 passed, A-Forex 68 y B 176. La primera pasada la cortó el límite de 2 h de la serie y se relanzó sola |

## Segunda ronda de cierre de la QA r03 (H-18)

| Comprobación | Resultado |
| --- | --- |
| `test_t177_c4_credenciales.py` | 83 pruebas: `test_t177_cierre2_h18_*` (×4) y dos pruebas ajustadas (urgencia `MUY_ALTA`, `impacto` con `impacto_si_falta`) |
| `r03c_ataques_cierre.py` (los tres HALLAZGO_H18 invertidos: SIN_RESULTADO y el valor en ningún fichero), `r03_ataques_regla_comun.py`, r01, r02, la concurrencia, `test_v51`, los vecinos, las suites R8, `test_t146_presupuesto` y `test_fase3_goldens` | 834 passed. `goldens_ct.py`: coinciden |
| `r03_corpus_formatos.py` | 97 ejemplos y 0 bloqueos |
| Mutantes | 41/42 en la pasada. M42, M43 y M44 (H-18) mueren. M08 sobrevive y se retiró como equivalente, **lo que era un error** (QA, H-19): una urgencia sin contenido (`" "`, `[""]`, `{"": ""}`) pasa la barrera y llega a esa línea. Se restituye en la tercera ronda de cierre |
| `ciclo_mock_t177.sh` | OK |
| Evidencias | 337/337 |
| `./tools/check_all.sh` | 12/12 en verde: ruff 2807 (cuota 2807); mypy A 102, A-Forex 174 y B 159; pytest A 8350 passed, A-Forex 68 y B 176 |

## Tercera ronda de cierre de la QA r03 (H-19)

| Comprobación | Resultado |
| --- | --- |
| `test_t177_cierre3_h19_urgencia_sin_contenido_se_reduce_a_normal` (`" "`, `[""]`, `{"": ""}`) | SOLICITADA; la urgencia es NORMAL en la CRD- y en el CT-25 |
| `test_t177`, `r03d_cierre2.py` (su caso H19 ya pasaba con el código actual), `r03c` y `r03` | 155 passed |
| Mutantes | 42/42 muertos, con M08 restituido (lo mata la prueba nueva) |
| Evidencias | 338/338 |
| `./tools/check_all.sh` | 12/12 en verde: ruff 2807 (cuota 2807); mypy A 102, A-Forex 174 y B 159; pytest A 8353 passed, A-Forex 68 y B 176 |
