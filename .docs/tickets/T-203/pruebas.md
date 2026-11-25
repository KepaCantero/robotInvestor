# T-203 · Pruebas

Lo de arriba hasta «Ronda de cierre» es la r01 (sobre develop 7f92064a, sin T-201); la ronda de cierre, sobre develop 358576c3 (con T-201), está al final.

| Suite | Antes (develop 7f92064a) | Después |
| --- | --- | --- |
| Bloque A (`pytest -q bloque_a/11_Ejecutor`, recogidas) | 8439 | 8444 (+5 de `tests/test_t203_cuotas.py`) |
| Bloque A, ejecución completa (dentro del gate) | — | 8442 superadas, ningún fallo (las 2 que faltan hasta 8444 son omisiones, como en develop) |
| B | sin tocar | sin tocar |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | Gate `ruff (hallazgos)`; `ruff check --output-format=concise bloque_a/11_Ejecutor` filtrado por UP006, UP045, UP035, I001, F401, RUF100 y FURB167 en los ficheros permitidos | 2806 → 2735; 0 en los permitidos; `ruff=2735` en `tools/cuotas.txt` |
| CA-2 | `git diff --name-only origin/develop` frente a la lista de exclusión (PR 3, `wip/t196`, T-201 y `ht07_legibilidad.py`) | r01: «ningún fichero en común», pero era falso para T-201 (la lista era la de su primer objetivo; H-01 de la QA r01): compartían `ht02.py`, `ht03.py`, `ht07.py` y `operaciones.py`. Rehecho en la ronda de cierre (abajo) |
| CA-3 | mypy de los tres paquetes; diff de los avisos de A sin número de línea | A 102 → 102 (diff vacío), A-Forex 174, B 159 |
| CA-4 | `.docs/tickets/T-203/equivalencia.py` (backtest del README, ciclo `--as-of 2026-06-05`, `peticion` con `ejemplos/peticiones/peticion_ad_hoc.json` y `consulta`, 90 ficheros) | IGUALES; los cuatro con código de salida 0 |
| CA-5 | `tests/test_t203_cuotas.py`: `test_reexportacion_de_referencia_sin_cambios` (HT-02, HT-03, HT-07) y `test_anotaciones_sin_evaluar_y_resolubles` (`operaciones`, `mock_respuestas`); suite completa de A | 5/5; suite: ver arriba |
| CA-6 | `./tools/check_all.sh` completo (log en el scratchpad, `gate_t203.log`); grep de `noqa`, `type: ignore`, `cast(` y `Any` en el diff | 12/12 en verde; el diff no añade ninguno (solo quita `noqa` sin uso y reescribe el comentario de uno que se usa) |

## Equivalencia en lugar de mutantes

El cambio no debe alterar ningún comportamiento, así que no hay mutantes de lógica (reglas comunes de los tickets de cuotas). En su lugar:

1. **Prueba de equivalencia:** `.docs/tickets/T-203/equivalencia.py <base> <ticket> <trabajo>`. Ejecuta las cuatro órdenes en las dos copias en la misma carpeta temporal (así las rutas que el ejecutor escribe en F5, en los informes y en las cadenas de huellas coinciden sin normalizarlas) y compara byte a byte salida estándar, de error y todos los ficheros. Solo normaliza la latencia medida con el reloj real (`"latencia_s"` en JSON, la columna `latencia_s` de `consumo.csv`) y compara las bases SQLite por su volcado.
   - Develop contra develop sin cambios: IGUALES (lo único que variaba entre dos ejecuciones era la latencia).
   - Develop contra este ticket: IGUALES.
   - Develop contra una copia con este ticket y un cambio de un 0,01 % en `rentabilidad_periodo` (`motor/operaciones.py`): 60 DIFERENCIAS (el comparador detecta un cambio pequeño).
2. **Cambios no mecánicos, cada uno con su prueba:**

   | Cambio | Prueba | En develop |
   | --- | --- | --- |
   | Orden de imports y `noqa` sin uso de `herramientas/ht02.py`, `ht03.py` y `ht07.py` | `test_reexportacion_de_referencia_sin_cambios` (3 casos, intérprete nuevo sin `referencia/` en `sys.path`) | pasa (es de equivalencia: el comportamiento no cambia) |
   | Anotaciones de `motor/operaciones.py` y `mock_respuestas.py` | `test_anotaciones_sin_evaluar_y_resolubles` (2 casos: siguen aplazadas, se resuelven con `get_type_hints` y los módulos ya no exponen `Dict`, `List`, `Optional` ni `Tuple`) | falla en la última comprobación (los nombres de `typing` siguen ahí) |

## Gate

`./tools/check_all.sh` completo, 24-11-2026, con otros gates a la vez: **12/12**. corpus-integridad, nombres-nfc, yaml-configs, secrets y refs-vivas en verde; ruff 2735 (cuota 2735); mypy A 102, A-Forex 174 y B 159 (cuotas iguales); pytest A 8442, A-Forex 68 y B 176 superadas.

## Ciclo mock y backtest

Los dos dentro de `equivalencia.py`: rc 0 en develop y en el ticket, con las mismas salidas (`senales.csv`, `pronosticos.csv`, `metricas.json`, `consumo.csv` salvo latencia, F1–F6, F10, HA, RC, la caché, los acuses y los entregables).

## Ronda de cierre (2026-11-25, sobre develop 358576c3 con T-201)

| Suite | develop 358576c3 | wip/t203 rebasado |
| --- | --- | --- |
| Bloque A (recogidas) | 8546 | 8551 (+5 de `tests/test_t203_cuotas.py`) |
| Bloque A, ejecución completa (dentro del gate) | — | 8549 superadas, ningún fallo (las 2 que faltan hasta 8551 son las omisiones fijas de `test_t149.py`, como en la r01) |

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `cierre_r01_04.sh` (cuotas con `revisores/r01_03_cuotas.sh`) y diff de los hallazgos de ruff frente a develop | 2797 → 2735 (−62: UP006 30, I001 11, UP045 8, F401 7, UP035 6), ningún hallazgo nuevo; `ruff=2735` |
| CA-2 | `.docs/tickets/T-203/ca2_solapes.sh` (salida abajo) | PR 3 y T-196: solo la deuda técnica (una fila); T-201: `operaciones.py`, `tools/cuotas.txt` y la deuda técnica, resueltos en el rebase; T-204: `tools/cuotas.txt` y la deuda técnica; corpus: ninguno |
| CA-3 | `cierre_r01_04.sh` y diff de los avisos de mypy de A sin número de línea | A 67 (los mismos que develop), A-Forex 174, B 159 |
| CA-4 | `equivalencia.py`, develop 358576c3 contra `wip/t203` | IGUALES, 90 ficheros, los cuatro con código 0 |
| CA-5 | `test_t203_cuotas.py` con `TYPE_CHECKING` y `test_t201_cuotas.py` | 43 superadas (las de los dos tickets) |
| CA-6 | `./tools/check_all.sh` completo | **12/12** (25-11-2026): ruff 2735 (cuota 2735), mypy A 67, A-Forex 174 y B 159 (cuotas iguales); pytest A 8549, A-Forex 68 y B 176 |

Comprobaciones de `cierre_r01_04.sh` (el `r01_04` de la QA adaptado: ya no hay fusión que resolver): rebasada sobre origin/develop, contiene T-201, `merge-tree` con develop limpio, sin marcas de conflicto, envoltorios iguales a develop, firma de `posicion_historica`, cuotas = medido y pruebas de los dos tickets: TODO BIEN.

Salida de `ca2_solapes.sh`:

```text
T-203 toca 32 ficheros
== PR 3 de Astra (origin/develop...origin/astra/encargos-bloque-a-c38-c47, 2d99af69)
   sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md
== T-196 pendiente (origin/develop...wip/t196; ya integrado en be35f28e)
   sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md
== T-196 integrado (be35f28e)
   sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md
== T-201 integrado (358576c3)
   bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py
   sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md
   tools/cuotas.txt
== T-204 (origin/develop...wip/t204, 123118ea)
   sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md
   tools/cuotas.txt
== corpus congelado (tools/corpus_manifest.txt)
```

Logs (scratchpad de la sesión): `t203_cierre_r01_04.log`, `t203_equivalencia_cierre.log` y `gate_t203_cierre.log`.
