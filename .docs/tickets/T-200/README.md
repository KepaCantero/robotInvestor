# T-200 · Bloque A: carrera al crear y migrar la tabla de acuses de la mensajería

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (24-11-2026, QA r02 APTO sin hallazgos abiertos) |
| Pieza | bloque_a (ejecutor): `bloque_a/11_Ejecutor/bloque_a/contratos.py`, `Mensajeria._acuses` |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | Deuda técnica sin caso del plan de pruebas; encargo del 24-11-2026, sin decisión nueva del operador |
| Deuda técnica | T-200 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (origen: QA r02 de T-196, 24-11-2026) |

## Objetivo

Que varias instancias del almacén, en procesos o hilos distintos, puedan abrir a la vez la tabla de acuses
(`acuses.sqlite3`, idempotencia de CT-01 y CT-03 desde T-92) sin fallar. Hasta ahora `Mensajeria._acuses` hacía
`CREATE TABLE IF NOT EXISTS`, comprobaba la columna `error` con `PRAGMA table_info` y la añadía con `ALTER TABLE`, todo
fuera de cualquier cerrojo y en modo autocommit: dos procesos veían la tabla sin `error` y el segundo `ALTER TABLE` fallaba
con `sqlite3.OperationalError: duplicate column name: error`. El revisor de T-196 lo reprodujo con seis instancias (3 de cada
15 intentos). Afecta a `procesar_una_vez` (y por tanto a `Bloque.peticion` y a la consulta CT-03), `estado_reserva` y
`reconciliar`.

## Fuentes

- QA r02 de T-196 (rama `wip/t196`, sin integrar): reproducción con seis instancias; la prueba de concurrencia de T-196 lo
  esquiva creando la tabla antes (no se toca aquí: se limpia al integrar).
- T-92: tabla de acuses con la columna `error` y migración de las tablas anteriores.
- Documento 0 V5.3: R5/R7 no fijan nada sobre la persistencia de la idempotencia; no hay número ni formato nuevo.

## Alcance

- **Entra:** `_acuses` lee el esquema y, solo si falta la tabla o la columna `error`, la crea, la vuelve a comprobar y la
  migra dentro de una única transacción `BEGIN IMMEDIATE` (doble comprobación, r02); si algo falla,
  la conexión se cierra (deshace la transacción) y el error sale tal cual. Revisión de `contratos.py` y `almacen.py` en busca
  del mismo patrón (comprobar y después cambiar fuera de un cerrojo).
- **No entra:** la prueba de T-196 que crea la tabla antes (`wip/t196`); cambiar el esquema de la tabla; el plan de pruebas
  (no hay caso: el mapa y las evidencias no cambian).

## Diseño

- **Por qué `BEGIN IMMEDIATE` y no `almacen._transaccion()`:** el cerrojo de escritura de SQLite protege el propio fichero
  `acuses.sqlite3`, entre hilos y entre procesos, sin anidar el cerrojo del almacén dentro de `Mensajeria._procesar` (que
  `procesar_una_vez` mantiene mientras el ciclo, que sí toma el del almacén, se ejecuta). La comprobación con
  `PRAGMA table_info` va dentro de la misma transacción, después de tomar el cerrojo de escritura. Una transacción diferida
  no basta: con una tabla antigua el `CREATE TABLE IF NOT EXISTS` no escribe y dos procesos leerían la tabla sin la columna
  (lo mata M2 con la prueba del almacén antiguo).
- **Doble comprobación (r02, H-01 de la QA r01):** en la r01 el `BEGIN IMMEDIATE` se tomaba en cada apertura, y un lector
  como `estado_reserva` esperaba a cualquier escritura en curso (y fallaba con «database is locked» a los 5 s). Ahora
  `_acuses` lee primero `PRAGMA table_info(acuses)` fuera de cualquier transacción: con la tabla ya migrada (el caso normal)
  no toma ningún cerrojo de escritura y se comporta como en develop. Solo si falta la columna (o la tabla) toma
  `BEGIN IMMEDIATE`, crea la tabla y **vuelve a comprobar dentro**. La lectura de fuera sin cerrojo es segura porque no
  decide nada definitivo: solo elige si hace falta el camino lento. Si otra instancia migra entre esa lectura y el cerrojo,
  la segunda comprobación, ya con el cerrojo, ve la columna y no repite el `ALTER TABLE`. La columna nunca desaparece una vez
  añadida, así que ver `error` fuera también es definitivo. Lo prueban M7 (cerrojo siempre), M9 (comprobación interior antes
  del cerrojo) y M10 (sin comprobación interior).
- **Falla cerrado:** no hay ningún `except` que se trague nada. `except BaseException: db.close(); raise` solo cierra la
  conexión (sin commit: la transacción se deshace, no queda una tabla a medias) y vuelve a lanzar el mismo error. Si la base
  está bloqueada más allá del tiempo de espera por defecto de `sqlite3` (5 s), sale el `OperationalError` «database is
  locked».
- **Números:** ninguno nuevo (el tiempo de espera es el de `sqlite3.connect`, el mismo que antes).
- **Mismo patrón en otros sitios:** no hay. `almacen.py` hace todas sus comprobaciones y escrituras (sellos, marca de formato,
  `nuevo_id`, `escribir`) dentro de `_transaccion()`; en `contratos.py` el único SQLite es la tabla de acuses y el resto de
  sus lecturas y escrituras (`INSERT OR IGNORE`, `UPDATE`, `DELETE`) ya van en transacciones de una sola sentencia o en
  `with db:`.
- **Incidencias:** ninguna; el spec no fija la persistencia de los acuses.

## Criterios de aceptación (binarios)

1. CA-1: ocho procesos reales que abren a la vez 25 almacenes nuevos (la mitad por `procesar_una_vez`, la ruta de
   `Bloque.peticion`, la otra mitad por `estado_reserva`) no fallan nunca, cada tabla queda con `id, huella, respuesta, error`
   y con las cuatro reservas. La misma prueba falla con el código de develop.
2. CA-2: una tabla de acuses antigua (sin `error`) se migra al abrirla, conserva sus reservas y vuelve a abrirse sin migrar
   otra vez; y la migración concurrente de 25 almacenes antiguos por ocho procesos tampoco falla.
3. CA-3: un `OperationalError` distinto (base bloqueada por otra escritura, o un fallo del `ALTER TABLE`) se propaga tal
   cual, la conexión se cierra y la transacción se deshace entera (no queda la tabla creada a medias).
4. CA-4: mutantes de lo esencial muertos (`mutantes.py`); suite de A ≥ 607 sin fallos; ruff ≤ 2806 (la cuota desde T-199) y mypy de A ≤ 102;
   ciclo mock y backtest del README iguales que en develop; `./tools/check_all.sh` 12/12.
5. CA-5 (r02, H-01): con la tabla ya migrada, `_acuses` no toma el cerrojo de escritura: `estado_reserva` responde al
   momento aunque otra instancia tenga una escritura en curso sin confirmar.

## Plan de pruebas

| Prueba (`tests/test_t200.py`) | Tipo | Criterio |
| --- | --- | --- |
| `test_varios_procesos_abren_a_la_vez_un_almacen_sin_carrera[almacen_nuevo]` | concurrencia (8 procesos × 25) | CA-1 |
| `test_varios_procesos_abren_a_la_vez_un_almacen_sin_carrera[almacen_antiguo]` | concurrencia, migración | CA-2 |
| `test_almacen_antiguo_sin_columna_error_se_migra` | migración, regresión | CA-2 |
| `test_otro_error_de_sqlite_se_propaga_y_cierra_la_conexion` | fallo cerrado | CA-3 |
| `test_un_fallo_dentro_de_la_migracion_deshace_la_tabla` | fallo cerrado | CA-3 |
| `test_con_la_tabla_migrada_un_lector_no_espera_a_otra_escritura` (r02, equivalente a `revisores/r05_lector_con_escritor.py`) | regresión, contención | CA-5 |
| `.docs/tickets/T-200/mutantes.py` (11 mutantes) | robustez | todos |
| Suites existentes (T-87, T-92), suite de A, ciclo mock, gate | regresión | CA-4 |

## Registro

- 2026-11-24 · claude: planificado, implementado y probado; EN QA (r01).
- 2026-11-24 · QA r01: NO APTO, H-01 (media): `BEGIN IMMEDIATE` en cada apertura; `estado_reserva` esperaba a otras escrituras.
- 2026-11-24 · claude (r02): doble comprobación, prueba de regresión de H-01, M7 y M9 adaptados, M10 y M11 nuevos; EN QA (r02).
- 2026-11-24 · QA r02 · APTO sin hallazgos abiertos (`qa.md`).
- 2026-11-24 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
