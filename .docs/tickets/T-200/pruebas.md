# T-200 · Pruebas

## Ronda r02 (H-01 de la QA r01)

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t200.py` | 5 pruebas, 6 casos; con la r02 pasan 10 de 10 ejecuciones |
| La prueba nueva, `test_con_la_tabla_migrada_un_lector_no_espera_a_otra_escritura` (CA-5) | Falla con el `contratos.py` de la r01 (`4b33dbc8`): «database is locked». Pasa con la r02 |
| Con el `contratos.py` de develop (`b3be72d6`) | 4 de 6 fallan: las dos de concurrencia y las dos de fallo cerrado. La de migración y la nueva pasan, porque develop ya solo leía |
| `revisores/r05_lector_con_escritor.py` | `DESCONOCIDO` en 0,00 s, rc 0 |
| `revisores/r04_fugas.py` | 300 bloqueadas y 300 de E/S; 4 descriptores antes y 4 después, rc 0 |
| `revisores/r06_mutantes_qa.py` | Q1, Q2 y Q4 muertos; Q5 y Q6 vivos (los equivalentes). Q3 no se aplica a la sangría nueva (el `assert` del script lo detiene); se ejecutó con una copia sin Q3 fuera del repositorio y Q3 está cubierto por M11 |
| `mutantes.py` | 11 mutantes, 11 muertos. M7 es el código de la r01 y M9 está adaptado; M10 (sin comprobación interior) y M11 (Q3) son nuevos |
| Vecinas (`test_t92_revision.py`, `test_t87_contratos.py`) | 80 superadas |
| Gate completo r02 (`./tools/check_all.sh`, setsid nohup, log propio fuera del repo) | **12/12**: pytest A 8402, A-Forex 68, B 176; ruff 2806 (cuota 2806); mypy A, A-Forex y B en cuota (102, 174, 159) |
| Ciclo mock, backtest y dos peticiones frente a develop | Lo mismo que en la r01: rc 0; `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos; `consumo.csv` igual salvo `latencia_s`; F5 solo difiere en rutas (y hashes); `acuses.sqlite3` igual |

## Ronda r01

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t200.py` | — | 4 pruebas, 5 casos, en verde (10 de 10 ejecuciones) |
| Bloque A completo (gate) | — | 8401 superadas (línea base 607) |
| A-Forex, B | sin tocar | sin tocar |

## Criterio de aceptación → prueba

| Criterio | Prueba (`bloque_a/11_Ejecutor/tests/test_t200.py`) |
| --- | --- |
| CA-1 | `test_varios_procesos_abren_a_la_vez_un_almacen_sin_carrera[almacen_nuevo]`: 8 procesos reales (`python -c`), 25 almacenes nuevos; en cada ronda todos esperan la orden y entran a la vez en `_acuses`, la mitad por `procesar_una_vez` (ruta de `Bloque.peticion`) y la otra por `estado_reserva`; exige ningún fallo, las columnas `id, huella, respuesta, error` y las 4 reservas |
| CA-2 | `…[almacen_antiguo]` (lo mismo con la tabla sin `error` creada antes de cada ronda); `test_almacen_antiguo_sin_columna_error_se_migra` (migra, conserva la reserva antigua, anota `error` después y no vuelve a migrar) |
| CA-3 | `test_otro_error_de_sqlite_se_propaga_y_cierra_la_conexion` (otra conexión con `BEGIN EXCLUSIVE`, tiempo de espera 0: sale «database is locked», la conexión queda cerrada y no hay tabla; después abre bien); `test_un_fallo_dentro_de_la_migracion_deshace_la_tabla` (el `ALTER TABLE` lanza «disk I/O error»: sale tal cual y la tabla no queda creada) |
| CA-4 | mutantes, suite, ciclo mock, backtest y gate (abajo) |

## Que fallan sin el cambio

Con `contratos.py` de `origin/develop`: `[almacen_nuevo]` falla 10 de 10 ejecuciones y `[almacen_antiguo]` 10 de 10
(«duplicate column name: error» en varias rondas de cada ejecución y reservas perdidas); también fallan las dos de CA-3 (la
conexión no se cierra; el `CREATE TABLE` queda confirmado sin `error`). La de migración pasa también en develop: es de
regresión. Con el arreglo, el fichero entero pasa 10 de 10.

## Mutantes

`.docs/tickets/T-200/mutantes.py`, 9 mutantes, **9 muertos, 0 vivos**: M1 sin transacción (el código de develop), M2
transacción diferida (lo mata solo el caso del almacén antiguo, 10 de 10), M3 sin commit, M4 sin cerrar la conexión al
fallar, M5 se traga el `OperationalError`, M6 nunca migra, M7 siempre migra, M8 el arreglo alternativo de capturar el
`OperationalError` del `ALTER TABLE`, M9 la comprobación fuera de la transacción.

## Ciclo mock, backtest y petición

`python -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv` con
`--as-of 2026-06-05 ciclo`, con `backtest --desde 2024-01-05 --hasta 2024-03-29` y dos veces `peticion --json
ejemplos/peticiones/peticion_ad_hoc.json` sobre el mismo estado, en develop (`git archive origin/develop bloque_a`) y en
T-200: rc 0 todos. `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos byte a byte; `consumo.csv` igual salvo
`latencia_s`; informes técnicos y F5 difieren solo en la ruta de la carpeta de salida (y, por ella, los hashes de F5 y los
sellos); `acuses.sqlite3` con las mismas columnas y las mismas filas (huella, respuesta, `error` nulo).

## Gate

`./tools/check_all.sh` completo (lanzado con `setsid nohup`, log propio fuera del repo): **12/12 en verde**. Corpus, NFC,
YAML, secretos y refs-vivas OK; ruff 2806 (cuota 2806, sin cambio: `contratos.py` y `test_t200.py` limpios); mypy de A,
A-Forex y B dentro de cuota (102, 174, 159, sin cambio); pytest A 8401, A-Forex 68, B 176 superadas.
