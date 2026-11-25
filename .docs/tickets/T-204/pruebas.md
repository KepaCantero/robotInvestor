# T-204 · Pruebas

| Suite | Antes (develop `d23afe0`) | Después |
| --- | --- | --- |
| `.docs/scripts/pruebas_scripts.sh` | 399 (línea base 399) | 432 (+33 de `pruebas_gate_bloques.py`; línea base 432). No se quita ni cambia ninguna prueba: ninguna era del Forex |
| `.docs/scripts/prueba_refs_vivas.py` (fuera de pytest; ahora lo ejecuta `pruebas_gate_bloques.py`) | 25 casos | 43 casos (+18 del bloque retirado) |
| pytest Bloque A (gate) | línea base 607 | 8443 passed (≥ 607) |
| pytest Bloque B (gate) | línea base 174 | 176 passed (≥ 174), las mismas que en develop. No se quita ninguna prueba de B: B no tenía ninguna del Forex |
| pytest A-Forex (gate) | 68 | ya no existe (el bloque se elimina por orden del operador) |
| Marco común de C, `pruebas_parametros_doc_t83.py` (lee la Constitución y la deuda) | 109 | 109, con la deuda nueva y también con el parche de la enmienda 4 aplicado |

## Criterio de aceptación → prueba

| Criterio | Cómo se comprueba |
| --- | --- |
| CA-1 | `git ls-files bloque_a_forex` vacío. `grep -rn bloque_a_forex bloque_a/11_Ejecutor bloque_b/11_Ejecutor` solo da `tests/goldens/README.md` de A, que es texto y queda fuera (INC-T204-04). `test_preparar_entorno_instala_justo_los_ejecutores_del_gate` y `test_qa_rama_prueba_justo_los_paquetes_del_gate` comprueban las listas. El gate, con A y B en verde |
| CA-2 | `test_el_gate_y_sus_scripts_no_nombran_el_forex` (6 ficheros), `test_el_detector_ve_las_formas_de_nombrar_el_forex` (11 formas de develop), `test_el_detector_no_salta_con_lo_que_no_es_el_forex` (7), `test_el_gate_solo_nombra_bloques_que_existen`, `test_las_cuotas_son_de_bloques_que_existen`, `test_el_gate_completo_son_diez_comprobaciones_sobre_a_y_b`, `test_el_gate_core_son_siete_comprobaciones` y `test_cada_bloque_se_mide_con_su_propia_linea_base` (×2). El gate real da 10/10. Ruff, medido como el gate, da 1604 |
| CA-3 | Antes de re-congelar, `corpus_integridad.py` dio 180 «ELIMINADO» de `bloque_a_forex/` y ninguna otra diferencia. Tras `--update-corpus`, el diff del manifiesto solo tiene esas 180 líneas borradas (525 huellas). corpus-integridad en verde en el gate |
| CA-4 | `refs-vivas` en verde. `tools/refs_allowlist.txt` sin cambios. Los 18 casos «bloque retirado» de `prueba_refs_vivas.py` y `test_la_prueba_de_refs_vivas_pasa_con_los_casos_del_bloque_retirado` |
| CA-5 | Con `tools/check_all.sh` y `tools/cuotas.txt` de develop, `pruebas_gate_bloques.py` da 12 fallos, entre ellos los dos de «no nombran el forex» de esos ficheros. Mutantes M1, M2, M7, M10 y M11 |
| CA-6 | `pruebas_scripts.sh`: 432 passed ≥ 432. B: 176 ≥ 174 |
| CA-7 | Revisión de `CLAUDE.md`, `prompts/00_ENTORNO.md` y `prompts/README.md` (10/10). `AGENTS.md` sin menciones. `refs-vivas` en verde |
| CA-8 | La fila T-204 de la deuda y el estado del README |

## Regresiones: fallan sin el cambio

- **`pruebas_gate_bloques.py`.** Copiada a una extracción limpia de `origin/develop`, da **12 fallos y 21 pasadas**. Fallan las 6 de «no nombran el forex», `test_el_gate_solo_nombra_bloques_que_existen`, las del gate real (10 y 7 comprobaciones), las dos de línea base por bloque y la de `prueba_refs_vivas`. Las que pasan en develop son las del detector y las de coherencia entre listas, que en develop eran coherentes con tres bloques.
- **`prueba_refs_vivas.py`.** Con el `refs_vivas.py` de develop da **35 de 43**: fallan 8 casos del bloque retirado.

## Mutantes

`.docs/tickets/T-204/mutantes.py`: **29 mutantes, 29 muertos y 0 vivos**.
- **Gate y cuotas:** del M1 al M12.
- **Scripts que enumeran los bloques:** del M13 al M16.
- **`refs_vivas.py`:** del M17 al M29. Incluye la marca, los registros, las palabras de una orden, `--opcion=`, `./`, las abreviaturas, la comprobación de las demás rutas de la cita y los límites de la línea.

M28 salió vivo en la primera versión, cuando una cita con el bloque retirado se saltaba entera. Era equivalente con las raíces de entonces, pero dejaba sin comprobar las demás rutas de esa cita. Se cambió el código para que las compruebe, con dos casos nuevos («en un ticket, el otro argumento roto falla» y «línea marcada, script roto falla»), y el mutante pasó a ser lo contrario (saltarse la cita entera): muerto.

## Gate

`./tools/check_all.sh` completo sobre la copia de trabajo, lanzado con `setsid nohup` y con log propio (`gate_t204_r2.log` en el scratchpad de la sesión): **10/10, «TODOS LOS GATES PASARON»**. La primera ejecución (`gate_t204.log`) se perdió con un reinicio del contenedor, en la suite de A, y se relanzó entera.

| Comprobación | Resultado |
| --- | --- |
| corpus-integridad | 525 archivos coinciden con el manifiesto |
| nombres-nfc, yaml-configs (2), secrets, refs-vivas | en verde |
| ruff | 1604 (cuota 1604; antes 2806 con el Forex) |
| mypy bloque_a · bloque_b | 102 · 159 (cuotas 102 · 159, sin cambios) |
| pytest bloque_a · bloque_b | 8443 · 176 passed (líneas base 607 · 174) |

Antes del gate pasaron `pruebas_scripts.sh` (432 passed) y los 29 mutantes, que se volvieron a ejecutar tras el reinicio: siguen los 29 muertos.

## Lo que no se ejecutó, y por qué

- **El ciclo mock y el backtest del README del Bloque A:** no se tocó código de A, solo el gate, y la suite de A pasa en el gate.
- **`evidencias_plan_a.py --ejecutar`:** este ticket no tiene caso del plan.
- **Las 62 suites de `pruebas_marco.sh`:** el marco no cambia. Se ejecutó solo `pruebas_parametros_doc_t83.py`, la única que lee los documentos de `sistema_global/` que cambian.

## Comandos

Los de `analisis-tecnico.md`, más:

```bash
git worktree add --detach <scratchpad>/dev204 origin/develop
cp .docs/scripts/pruebas_gate_bloques.py <scratchpad>/dev204/.docs/scripts/
(cd <scratchpad>/dev204 && .venv/bin/python -m pytest -q .docs/scripts/pruebas_gate_bloques.py)     # 12 failed, 21 passed
git show origin/develop:tools/refs_vivas.py > <scratchpad>/refs_vivas_develop.py
.venv/bin/python .docs/scripts/prueba_refs_vivas.py <scratchpad>/refs_vivas_develop.py               # 35/43
```

## Ronda r02 (QA r01 NO APTO)

| Suite | r01 | r02 |
| --- | --- | --- |
| `.docs/scripts/pruebas_scripts.sh` | 432 | **449** (+17 en `pruebas_gate_bloques.py`, de `test_h01` a `test_h08`); línea base 449 |
| `pruebas_gate_bloques.py` | 33 | 50 |
| `prueba_refs_vivas.py` | 43 casos | 46 (+3 de H-06) |
| `mutantes.py` | 29, todos muertos | **36, todos muertos**: M18, M19 y M25 ajustados al código nuevo; M30 y M31 (H-06); M32 a M36 (`limpiar_docs.py`, H-03) |
| Mutantes del revisor (`r02_mutantes_revisor.py`, Q1 adaptado) | 8 de 10 | **10 de 10**, todos muertos por las pruebas |

**Scripts del revisor, sin cambiarlos.** Q1 de `r01_03` se escribió sobre el texto viejo. Se ejecuta adaptado con `r02_mutantes_revisor.py` (ver `analisis-tecnico.md`).

| Script | r01 | r02 |
| --- | --- | --- |
| `r01_01_propuesta_limpieza.py limpiar_docs_propuesta.txt` | 3 casos (299 cambios) | **0 casos** (107 cambios) |
| `r01_02_ataques_refs_vivas.py` | 8/11 | **11/11** |
| `r01_03_mutantes.py` | 8 de 10 | **10 de 10** |
| `r01_04_parche_constitucion.py` | 4 casos | **0 casos** |
| `r01_05_coherencia_docs.py` | 4 casos | **0 casos** |

**Regresiones: fallan sin la corrección.**
- `test_h01`, `test_h04`, `test_h05` y `test_h08`: son los mismos textos que detecta `r01_05` y la incidencia de la r01.
- `test_h02`: el parche de la r01 dice «enmienda 4».
- `test_h03`: con el `limpiar_docs.py` de la r01, la fila T-204 de `.docs/knowledge/01_…` se borraba y las líneas de gate se reescribían. Lo confirman M32 y M33.
- `test_h07`: lo confirma Q4.

**Parche de la Constitución.** `git apply --check` está en verde y `generar_enmienda.py --comprobar` también. Aplicado en una copia aparte de `sistema_global/`, la cabecera queda en V0.7 con fecha del 25-11-2026, y `pruebas_parametros_doc_t83.py` da «TODAS LAS PRUEBAS PASAN».

**Gate r02.** Es `./tools/check_all.sh` completo, lanzado con `setsid nohup` y con log propio (`gate_t204_r02.log` en el scratchpad). La primera ejecución, `gate_t204_r02_intento1.log`, se cortó en la suite de A al pararse la sesión por el límite de uso, y se relanzó entera. Resultado: **10/10, «TODOS LOS GATES PASARON»**.
- Corpus: 525 archivos.
- NFC, YAML, secretos y refs-vivas: en verde.
- ruff: 1604, igual a la cuota.
- mypy: A 102 y B 159.
- pytest: A 8443 y B 176.

**Develop ha avanzado** (T-201, `358576c3`: ruff 2797 y mypy A 67). Esta rama no se rebasa, por indicación de la coordinación, y las cifras de ruff y mypy de arriba son las de la base `d23afe0`. Al integrar, la cuota de ruff tiene que ser la medida sobre A y B con el código de T-201, y `test_h07` la exigirá igual a esa medida.

## Ronda r03 (QA r02 NO APTO)

| Suite | r02 | r03 |
| --- | --- | --- |
| `.docs/scripts/pruebas_scripts.sh` | 449 | **455** (+6: `test_h09` y 5 casos de `test_h03`; `test_h02` se reescribe). Línea base 455 |
| `pruebas_gate_bloques.py` | 50 | 56 |
| `prueba_refs_vivas.py` | 46 casos | 48 (+2 de H-12) |
| `mutantes.py` | 36 | **38, todos muertos**: M31 ajustado; M37 (H-11) y M38 (H-12) nuevos |
| Mutantes del revisor (`r02_mutantes_revisor.py`) | 10 de 10 | 10 de 10 |
| `.docs/scripts/pruebas_marco.sh` | — | 62 pasan, 0 fallan |

**Scripts del revisor.**

| Script | Resultado |
| --- | --- |
| `r01_01_propuesta_limpieza.py limpiar_docs_propuesta.txt` | 0 casos (107 cambios, la propuesta que se aplicó) |
| `r01_02_ataques_refs_vivas.py` | 11/11 |
| `r01_03_mutantes.py` (con `r02_mutantes_revisor.py`) | 10 de 10 |
| `r01_04_parche_constitucion.py` | 0 casos, sobre una extracción de `253f33fd` (V0.6), como en la QA r02. Sobre el árbol actual no puede pasar, porque el parche ya está aplicado. Lo aplicado es exactamente el parche: `git apply -R --check .docs/tickets/T-204/enmienda4_constitucion.patch` en verde |
| `r01_05_coherencia_docs.py` | 0 casos |
| `r02_01_limpieza_aplicada.py 253f33fd 80d152ec` | **0 casos** (103 líneas). Por defecto mira los commits fijos `253f33fd..ba651950`, que es la historia, y sigue dando sus 5 casos. Los nombres de fichero que da van uno por detrás: los casos que atribuye a T-113, T-194, T-200 y T-167 son de T-106, T-187, T-199 y T-166 |
| `r02_02_estado_aplicado.py` | 0 casos |
| `r02_03_ataques_r02.py` | 3 de 3 OK (las dos asignaciones de entorno, y `test_h02` con la cabecera en V0.8) |

**Regresiones: fallan sin la corrección.**
- `test_h09`: con los textos de la r02b daría «V0.6» en `sistema_global/README.md` y «Pendiente del operador» en la fila y en la memoria.
- `test_h02` reescrita: la de la r02b falla con V0.8, como muestra `r02_03`.
- Casos nuevos de `test_h03`: los mata M37.
- Casos de H-12: los mata M38, y `r02_03` fallaba en la r02.

**Gate r03.** Es `./tools/check_all.sh` completo sobre `901a2c1d`, lanzado con `setsid nohup` y con log propio (`gate_t204_r03.log` en el scratchpad). Resultado: **10/10, «TODOS LOS GATES PASARON»**.
- Corpus: 525 archivos.
- NFC, YAML, secretos y refs-vivas: en verde.
- ruff: 1604, igual a la cuota.
- mypy: A 102 y B 159.
- pytest: A 8443 y B 176.

## Ronda de cierre de la QA r03

| Comprobación | Resultado |
| --- | --- |
| `r03_02_etiquetas_h11_y_t54.py` (por defecto, y con el `fad84daf` rebasado) | 0 casos |
| `r01_02` · `r01_05` · `r02_02` | 11/11 · 0 · 0 |
| `r02_03` | 3 de 3 OK |
| `r03_01 253f33fd f8df1129` y, tras el rebase, `r03_01 2980b8c6 HEAD` | 5 casos, todos de la memoria de T-204 (`2026-11-25_bloque-a-forex-eliminado`): los cambios de H-09 que el revisor da por esperados. No hay ninguno más |
| `pruebas_gate_bloques.py` | 56 passed (`test_h07`: cuota 1533 = medida) |
| `.docs/scripts/pruebas_scripts.sh` | 455 passed (línea base 455; develop sigue en 399) |
| Tras el rebase: ruff · mypy A · mypy B · corpus | 1533 · 67 · 159 · 525 |

**Gate de cierre.** Es `./tools/check_all.sh` completo sobre `344fdd5f` (ya rebasado), lanzado con `setsid nohup` y con log propio (`gate_t204_cierre.log` en el scratchpad). Resultado: **10/10, «TODOS LOS GATES PASARON»**.
- Corpus: 525 archivos.
- NFC, YAML, secretos y refs-vivas: en verde.
- ruff: 1533, igual a la cuota.
- mypy: A 67 y B 159, iguales a sus cuotas.
- pytest: A 8549 (incluye las pruebas de T-196, T-201 y T-203) y B 176.

## Cierre 2

| Comprobación | Resultado |
| --- | --- |
| `r04_02_limpieza_tras_rebase.py` | 0 casos |
| `r04_01_mutantes_revisor_cierre.py` | 10 de 10 muertos |
| `mutantes.py` | 41 de 41 muertos (M40 y M41 nuevos; M37 ajustado) |
| `r01_02` · `r01_05` · `r02_02` · `r03_02 2aa4290a` (el H-11 rebasado) | 11/11 · 0 · 0 · 0 |
| `pruebas_gate_bloques.py` | 61 passed (`test_h07`: cuota 1533 = medida, igual tras T-205) |
| `.docs/scripts/pruebas_scripts.sh` | 460 passed (línea base 460) |
| `limpiar_docs.py`, sin opciones | 5 líneas: las de los tickets del rebase, declaradas en INC-T204-03 |

**Gate de cierre 2.** Es `./tools/check_all.sh` completo sobre `ef3fd250`, lanzado con `setsid nohup` y con log propio (`gate_t204_cierre2.log` en el scratchpad). Resultado: **10/10, «TODOS LOS GATES PASARON»**.
- Corpus: 525 archivos.
- ruff: 1533, igual a la cuota.
- mypy: A 67 y B 159.
- pytest: A 8577 (con las pruebas de T-205) y B 176.
