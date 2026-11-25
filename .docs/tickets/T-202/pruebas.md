# T-202 · Pruebas

Todo con el `.venv` propio de la copia (`python3.12 -m venv` a través de `preparar_entorno.sh`), no con el común. develop, en una copia aparte de `origin/develop` (7f92064a) con el `.venv` común, que solo se lee.

| Suite | Antes (develop) | Después |
| --- | --- | --- |
| Bloque A (`pytest --collect-only`) | 8439 | 8447 (+8 de `tests/test_t202_alternativas_rangos.py`) |
| `.docs/scripts` (`pruebas_scripts.sh`) | 399 | 400 (+1 de `pruebas_preparar_entorno.py`); línea base 399 → 400 |
| A-Forex, B | sin tocar | sin tocar |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | mypy como el gate con el conjunto elegido, comparado con develop | A 102, A-Forex 174, B 159. Los mismos errores que develop, quitando el número de línea: `diff` vacío en los tres |
| CA-2 | mypy sin `--ignore-missing-imports`, `grep -c import-untyped` | A de 49 a 27, A-Forex de 23 a 15, B de 7 a 6. Stub a stub y los cinco juntos en `analisis-tecnico.md`; pandas-stubs (+26, +22, +13) y types-openpyxl (B +1), anotados y no fijados |
| CA-3 | `pip freeze` antes y después de cada instalación; `preparar_entorno.sh --comprobar` | Solo altas: los cinco paquetes nuevos. Ninguna versión fijada cambia. Conforme: 54 paquetes |
| CA-4 | `preparar_entorno.sh` sobre un `.venv` con lo de develop (antes, `--comprobar` da «falta …» de los cinco y código 1) | Código 0, conforme con 54 |
| CA-4 | `preparar_entorno.sh` desde cero (`rm -rf .venv`) | Código 0 en 53 s, conforme con 54 |
| CA-4 | `pruebas_preparar_entorno.py::test_t202_el_script_instala_cada_stub_de_tipos_fijado` | Pasa. Falla si se quita la línea de los stubs del script (comprobado y restaurado) |
| CA-5 | `equivalencia.py`: develop con su `.venv` frente a la rama con el suyo. Ciclo mock (`--as-of 2026-06-05`), consulta CT-03 sobre ese estado, backtest del README (2024-01-05 a 2024-03-29), petición `peticion_ad_hoc.json`, la batería de fichas tocadas y los casos de control de sus tres módulos (102 resultados) | Código 0. 107 ficheros iguales y 0 diferencias. Se normalizan solo la ruta de cada copia y `latencia_s` |
| CA-6 | `mutantes.py` | 8 de 8 muertos (abajo) |
| CA-6 | ruff como el gate | 2806 (cuota 2806) |
| CA-6 | `./tools/check_all.sh` completo | ver «Gate» |

## Equivalencia (en lugar de mutantes de lógica)

`.docs/tickets/T-202/equivalencia.py` ejecuta lo mismo en las dos copias y en la misma carpeta de trabajo, fuera del repositorio. Así F5 y su cadena de huellas, que guardan las rutas de salida, se pueden comparar. Compara cada fichero byte a byte: salidas, estado F1–F11, HA, sellos y los acuses en SQLite por su volcado. Lo único que se normaliza es la ruta de cada copia y las latencias medidas con el reloj: `"latencia_s"` en JSON, en los acuses y en la última columna de `consumo.csv`. Son tiempos de reloj, así que varían de una ejecución a otra. Antes de normalizarlas, las únicas diferencias eran esas latencias.

Comprueba también que cada lado carga las fichas de su copia (`PYTHONPATH`).

## Cambios no mecánicos y sus pruebas

| Cambio | Pruebas que lo ejercitan | Mutantes (`mutantes.py`) |
| --- | --- | --- |
| `_SCIPY_ALT` con tipo `Literal` (ST-INF-001) | `test_fase2_series.py`: casos de control de ST-INF-001 (Mann-Whitney exacto) y `test_st_inf_oraculo_wilcoxon_exacto`. Nueva: `test_t202_alternativas_rangos.py` | M01 («mayor» ↔ «menor»), muerto por la prueba nueva. **Con la suite de antes vivía** (`--solo-suite-anterior M01`: VIVO), porque ninguna prueba usaba una alternativa unilateral en los contrastes de rangos. M02 («bilateral» → «greater»), muerto |
| `res_u` en mann_whitney | Caso de control «Mann-Whitney exacto con muestras separadas (3 y 3)» | M03 (estadístico ← p-valor) y M04 (p-valor ← estadístico), muertos |
| `holgura` en lugar de la `lambda` (ALT-DESMOOTH-001, GLM) | `test_fase2_reales.py`: `test_alt_glm_*` | M05 (cambio de signo) y M06 (Σθ ≤ 2), muertos |
| `residuo` en lugar de la `lambda` (DER-SKEW-001, SVI) | `test_fase1_fon_der.py`: caso de control «SVI sin arbitraje de mariposa» y `test_skew_metodo_svi_y_asimetria` | M07 (suma en vez de resta) y M08 (primera derivada), muertos |

La prueba nueva pasa en develop y en la rama. Es un hueco de cobertura anterior a T-202, no una regresión. La de `pruebas_preparar_entorno.py` sí falla sin el cambio del script.

```
M01 _SCIPY_ALT: «mayor» y «menor» cambiados: MUERTO  tests/test_t202_alternativas_rangos.py::test_wilcoxon_con_cada_alternativa_coincide_con_scipy[mayor]
M02 _SCIPY_ALT: «bilateral» pasa a «greater»: MUERTO  test_fase2_series.py::test_casos_de_control[ST-INF-001:Mann-Whitney exacto …]
M03 mann_whitney: el estadístico sale del p-valor: MUERTO  (ídem)
M04 mann_whitney: el p-valor sale del estadístico: MUERTO  (ídem)
M05 GLM: la restricción cambia de signo: MUERTO  test_fase2_reales.py::test_alt_glm_no_invertible_se_rechaza
M06 GLM: la restricción se relaja a Σθ ≤ 2: MUERTO  test_fase2_reales.py::test_alt_glm_con_el_optimo_en_el_borde_se_sirve
M07 SVI: el residuo suma en vez de restar: MUERTO  test_fase1_fon_der.py::test_caso_control[DER-SKEW-001:SVI sin arbitraje de mariposa]
M08 SVI: el residuo usa la primera derivada: MUERTO  (ídem)
```

## Mapa y evidencias

`evidencias_plan_a.py` sin opciones: 67 pruebas del plan y 398 automáticas citadas; todas existen. No se regenera `docs/evidencias_pruebas_bloque_a.md` ni se toca el mapa, porque los cambian T-196 y el pull request 3 y ningún caso del plan cambia.

## Gate

`./tools/check_all.sh` completo, con el `.venv` propio de la copia. Lanzado con `setsid nohup` y log en `scratchpad/gate_t202.log`, del 24-11-2026 22:58 al 25-11-2026 00:07 UTC, con otros gates en marcha. **12/12 en verde.**

| Gate | Resultado |
| --- | --- |
| corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas | ✓ |
| ruff | 2806, cuota 2806 |
| mypy bloque_a · bloque_a_forex · bloque_b | 102 · 174 · 159, con cuotas 102 · 174 · 159 |
| pytest bloque_a · bloque_a_forex · bloque_b | 8445 · 68 · 176 superadas, con bases 607 · 68 · 174 |

Las cuotas no cambian en `tools/cuotas.txt`: el gate da los mismos valores que develop.

Después del gate solo cambiaron los documentos del ticket y la fila de la deuda técnica. Por eso se repitieron los gates que los leen: corpus-integridad, nombres-nfc, secrets y refs-vivas, en verde.

## Ronda r02 (QA r01 NO APTO)

| Suite | r01 | r02 |
| --- | --- | --- |
| Bloque A (`--collect-only`) | 8447 | 8448 (+1, `tests/test_t202_svi.py`) |
| `.docs/scripts` (`pruebas_scripts.sh`) | 400 | 405 (+5, `pruebas_gate_entorno.py`); línea base 400 → 405 |

| Hallazgo | Prueba | Sin la corrección | Mutante |
| --- | --- | --- | --- |
| H-03 | `.docs/scripts/pruebas_gate_entorno.py`: `check_all.sh` real con un `.venv` falso. Con el entorno conforme: ✓ en cada mypy y mypy se ejecuta una vez por paquete. Sin scipy-stubs, types-PyYAML o types-jsonschema: código 1; «✗ mypy <paquete>: el .venv no coincide con tools/requisitos_entorno.txt (stubs incluidos): ejecuta .docs/scripts/preparar_entorno.sh» en cada uno; la salida de `--comprobar` dice qué falta; mypy no se llama; `Fallaron` es el número de paquetes; el total de gates es el mismo que con el entorno conforme; ruff y pytest siguen ✓. Con un paquete sin fijar (pandas-stubs), lo mismo | Con el `check_all.sh` de la r01, 4 de 5 fallan (el caso conforme pasa) | M12: muerto |
| H-01 | `tests/test_t202_svi.py::test_svi_rmse_publicado_es_el_de_los_parametros_sin_pesos` | Pasa (es de cobertura: el comportamiento no cambia) | M09 (= RQ05): muerto; con `--solo-suite-anterior`, VIVO |
| H-02 | `pruebas_preparar_entorno.py::test_t202_el_script_instala_cada_stub_de_tipos_fijado`, con el filtro de `revisores/r04_…` | — | M10 y M11 (= RQ11 y RQ12): muertos |

- **`mutantes.py`:** 12 de 12 muertos (M01 a M12).
- **`revisores/r01_mutantes.py`:** 11 de 12 muertos. RQ05 sigue vivo **en ese script** porque sus pruebas de SVI son solo `tests/test_fase1_fon_der.py` y no incluyen `tests/test_t202_svi.py`, el fichero nuevo que propone el propio qa.md. El mismo cambio es M09, ejecutado con las dos, y muere. No meto la prueba en `test_fase1_fon_der.py` porque lo cambia T-203; el script del revisor no se toca. RQ11 y RQ12 ya mueren.
- El contenedor se reinició en medio de la primera ejecución de `r01_mutantes.py` y dejó RQ02 aplicado en `fichas_series.py`. Se restauró con `git checkout` y se repitió el script entero: el resultado de arriba es el de la segunda ejecución.
- **Fusión con T-204:** `git merge-file` del `check_all.sh` de la r02 con el de la copia de T-204, sobre la misma base, no da conflictos.

**Gate r02:** `./tools/check_all.sh` completo, con el `.venv` propio de la copia y la comprobación del entorno nueva (conforme: 54). Lanzado con `setsid nohup` y log en `scratchpad/gate_t202_r02.log`, el 25-11-2026 de 01:23 a 02:11 UTC. **12/12 en verde:** ruff 2806; mypy 102 · 174 · 159; pytest 8446 · 68 · 176. Después solo cambió este fichero, y se repitieron en verde corpus-integridad, nombres-nfc, secrets y refs-vivas.

## Ronda de cierre (QA r02 APTO, H-04)

Sobre `origin/develop` `eda55e1b` (T-204, T-205, T-203 y T-201 integrados), tras el rebase y la resolución de `revisores/r07_resolucion_fusion_t204.diff`:

| Comprobación | Resultado |
| --- | --- |
| `.venv` propio rehecho desde cero con el `preparar_entorno.sh` fusionado | 54 paquetes conformes en 56 s; editables, solo `bloque_a` y `bloque_b` |
| `pruebas_gate_bloques.py` (T-204), `pruebas_gate_entorno.py` y `pruebas_preparar_entorno.py` | 76 de 76 |
| `.docs/scripts/pruebas_scripts.sh` | 466 superadas, igual que la línea base sumada (460 + 6) |
| mypy como el gate | A 67 y B 159, iguales a sus cuotas; los mismos errores con stubs que sin ellos (el `.venv` común, que no los tiene) |
| `[import-untyped]` | A de 50 a 28 (el código de develop tiene un import de pandas más que el 24-11) y B de 7 a 6 |
| ruff | 1533, igual a la cuota |

**`mutantes.py`** sobre el código fusionado: 12 de 12 muertos (M01 a M12). Se ejecutó después del gate, para no cambiar ficheros mientras corría.

**Gate de cierre:** `./tools/check_all.sh` completo, con el `.venv` propio y la comprobación del entorno conforme. Lanzado con `setsid nohup` y log en `scratchpad/gate_t202_cierre.log`, el 25-11-2026 de 13:19 a 14:17 UTC. **10/10 en verde** (desde T-204 el gate tiene 10 comprobaciones): ruff 1533; mypy A 67 y B 159; pytest A 8586 y B 176. Después solo cambió este fichero, y se repitieron en verde corpus-integridad, nombres-nfc, secrets y refs-vivas.

## Comandos

Los de `analisis-tecnico.md`, y además:

- `.docs/scripts/pruebas_scripts.sh`;
- `.venv/bin/python .docs/scripts/evidencias_plan_a.py`;
- con el log en `scratchpad/gate_t202.log`: `setsid nohup ./tools/check_all.sh`.
