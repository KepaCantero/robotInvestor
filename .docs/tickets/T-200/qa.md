# T-200 · QA

## Ronda r01 (24-11-2026, claude, revisor independiente)

**Veredicto: NO APTO** (un hallazgo medio, H-01).

Base del diff: `git merge-base wip/t200 origin/develop` = `b3be72d6` (no 6045913). Commit revisado: `4b33dbc8`. Worktree de
la QA separado de la copia del implementador; la copia del implementador no se ha tocado.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t200.py` con el cambio | 5 passed (varias veces, ≈3 s) |
| `tests/test_t200.py` sobre el código de `b3be72d6` | 4 failed, 1 passed, 5 de 5 veces: «duplicate column name: error» en las dos de concurrencia, conexión sin cerrar y tabla a medias en las de fallo cerrado |
| Pruebas vecinas (test_t200, t92_revision, t87_contratos, fase3_goldens, fase4_huecos, unitarias, t65_resto_t53, t166_entrega_corpus) | 451 passed |
| `mutantes.py` del ticket | 9/9 muertos |
| Mutantes propios (`revisores/r06_mutantes_qa.py`) | Q1 timeout 0, Q2 rollback en vez de cerrar, Q3 commit antes del ALTER, Q4 tragarse el error devolviendo la conexión: muertos. Q5 `BEGIN EXCLUSIVE` y Q6 `except Exception`: vivos, equivalentes |
| Fugas (`revisores/r04_fugas.py`, 300 + 300 fallos + 300 usos normales, recolector parado) | 4 descriptores antes y 4 después. En `b3be72d6`, 4 → 604: el cambio además corrige una fuga previa |
| Ciclo mock backtest del README (2024-01-05 → 2024-03-29) | mismos ficheros; `metricas.json`, `senales.csv` y `pronosticos.csv` idénticos byte a byte a los de `b3be72d6` |
| ruff / mypy | `test_t200.py` limpio; `mypy bloque_a/contratos.py` sin errores; el gate informa ruff 2806/2806 y mypy A 102/102 (la cuota de ruff es 2806 desde T-199, no 2807) |
| Gate del implementador (`gate_t200.log`) | 12/12, pytest A 8401 passed. Nota: el log es de las 20:13:36 y el commit de las 20:14:13; el log no registra el hash, así que se da por bueno con la copia sin cambios pendientes |
| Choques con otras ramas | `wip/t196` no toca `contratos.py`; su `bb.mensajeria._acuses().close()` en `test_t196.py` sigue siendo válido (devuelve una conexión confirmada). `origin/astra/encargos-bloque-a-c38-c47` cambia `contratos.py` lejos de `_acuses`. `git merge-tree` con las dos ramas: sin conflictos en código; solo en documentos (deuda, evidencias, incidencias), que se resuelven al integrar |
| Mismo patrón en otros sitios | No hay. `almacen.py` no usa SQLite y hace todas sus comprobaciones y escrituras dentro de `_transaccion()` (flock). En `contratos.py` el único SQLite es `acuses.sqlite3` y el resto de sus accesos son sentencias sueltas o bloques `with db:` |
| Determinismo de la prueba de concurrencia | Con el cambio, pasa siempre: no depende del azar, salvo un «database is locked» por encima de 5 s (ver H-01). Para matar el código antiguo depende del reparto del planificador, pero la barrera «listo»/«ya» con 8 procesos y 25 rondas lo detecta 5 de 5 veces aquí (10 de 10 según el implementador). Es aceptable |

### Hallazgos

#### H-01 · media · `BEGIN IMMEDIATE` incondicional: cada apertura toma el cerrojo de escritura aunque la tabla ya esté migrada

**Qué pasa.** Antes, con la tabla ya creada y con `error`, `_acuses` solo leía: el `CREATE TABLE IF NOT EXISTS` no escribe y
`PRAGMA table_info` es una lectura. Ahora todas las llamadas (`procesar_una_vez`, `estado_reserva`, `reconciliar`) toman el
cerrojo RESERVED de `acuses.sqlite3` y esperan el `busy_timeout` por defecto de `sqlite3.connect` (5 s) si otra instancia
está escribiendo. Hay dos consecuencias:

- `estado_reserva` (y `reconciliar`, que lo llama) era de solo lectura y ahora falla con «database is locked» si otra
  escritura dura más de 5 s, cuando antes respondía al momento.
- Cada iteración `procesar_una_vez` + `estado_reserva` pasa de 2 a 4 transacciones de escritura, así que la contención se
  duplica.

El tiempo de espera es el mismo que antes, como dice el README, pero el cerrojo de escritura en cada apertura es nuevo y no
está declarado.

**Reproducción determinista:** `revisores/r05_lector_con_escritor.py`. Con la tabla migrada, otra conexión deja abierta una
escritura (BEGIN IMMEDIATE + INSERT) y se llama a `estado_reserva`:

| Árbol | Resultado |
| --- | --- |
| `b3be72d6` | `DESCONOCIDO` en 0.00 s |
| `wip/t200` | `OperationalError: database is locked` en 5.01 s |
| corrección propuesta | `DESCONOCIDO` en 0.00 s |

**Reproducción con carga:** `revisores/r01_estres_contencion.py <ejecutor> 150 12`, con 8 procesos sobre el mismo almacén,
12 quemadores de CPU y otros gates corriendo en la máquina. Mientras la máquina estaba más cargada, `wip/t200` falló en 2 de
7 corridas («database is locked», 3 fallos, peor iteración 5.37 s) y `b3be72d6` en 0 de 7 (peor iteración 4.67 s). Con
menos carga, ninguno de los dos falla en 6 corridas. Por eso la prueba de regresión debe ser la determinista y no esta.

**Corrección exacta.** Mirar primero, fuera de la transacción, si la tabla ya tiene la columna, y solo si no la tiene tomar
`BEGIN IMMEDIATE` y repetir dentro la creación y la comprobación (doble comprobación). Se conserva la protección contra la
carrera y el uso normal vuelve a ser de solo lectura. El diff está en `revisores/r03_correccion_propuesta.diff`:

```python
        try:
            if "error" not in {fila[1] for fila in db.execute("PRAGMA table_info(acuses)")}:
                db.execute("BEGIN IMMEDIATE")
                db.execute("CREATE TABLE IF NOT EXISTS acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)")
                if "error" not in {fila[1] for fila in db.execute("PRAGMA table_info(acuses)")}:
                    db.execute("ALTER TABLE acuses ADD COLUMN error TEXT")
                db.commit()
        except BaseException:
            db.close()   # cerrar sin commit deshace la transacción
            raise
```

Ya comprobado sobre un prototipo (worktree `qa_t200_fix`):
- las 5 pruebas de `test_t200.py` pasan;
- un mutante que quita la comprobación interior muere (2 fallos en las de concurrencia);
- r05 da `DESCONOCIDO` en 0.00 s.

Al aplicarla hay que:
- ajustar el comentario de `_acuses` y el apartado «Diseño» del README;
- adaptar M9 de `mutantes.py`, que con la doble comprobación deja de aplicar tal cual, y añadir el mutante «sin la
  comprobación interior»;
- explicar en el README por qué la lectura previa sin cerrojo es segura: solo decide si hace falta el camino lento, y
  dentro del cerrojo se vuelve a comprobar.

**Prueba de regresión.** Añadir a `tests/test_t200.py` una prueba determinista equivalente a r05:
- tabla migrada;
- otra conexión con `BEGIN IMMEDIATE` y un INSERT abiertos;
- `sqlite3.connect` parcheado con `timeout=0` para que no espere 5 s;
- `estado_reserva` debe responder `DESCONOCIDO` sin error.

Con el código actual de `wip/t200` falla al momento con «database is locked».

### Criterios de aceptación

| CA | Estado |
| --- | --- |
| CA-1 | Cumplido (concurrencia nueva: 0 fallos con el cambio y fallos 5 de 5 con `b3be72d6`) |
| CA-2 | Cumplido |
| CA-3 | Cumplido (y sin fugas, r04) |
| CA-4 | Cumplido (mutantes, gate 12/12, cuotas, mock idéntico). La regresión de H-01 queda fuera de los criterios y es la que motiva el NO APTO |

### Scripts de la ronda (`revisores/`)

Se ejecutan con `python -I <script> <ruta a bloque_a/11_Ejecutor>`.

| Script | Qué hace |
| --- | --- |
| `r01_estres_contencion.py` | Contención con carga; probabilístico, informativo |
| `r03_correccion_propuesta.diff` | Corrección propuesta para H-01 |
| `r04_fugas.py` | Descriptores y conexiones tras fallos |
| `r05_lector_con_escritor.py` | H-01, determinista; debe salir con 0 |
| `r06_mutantes_qa.py` | Mutantes propios de la QA |

En la ronda de cierre se vuelven a ejecutar r04, r05 y r06 sobre la corrección.

## Ronda r02 (24-11-2026, claude, mismo revisor)

**Veredicto: APTO, sin hallazgos abiertos.** H-01 está corregido. Commit revisado: `58cef91b`, encima de `4b33dbc8`.

### Corrección de H-01

`_acuses` lee primero `PRAGMA table_info(acuses)` fuera de cualquier transacción. Solo si falta la columna `error` toma
`BEGIN IMMEDIATE`, hace el `CREATE TABLE IF NOT EXISTS`, vuelve a comprobar y hace el `ALTER TABLE`. El código coincide con
`revisores/r03_correccion_propuesta.diff`. Además, el README (Diseño, CA-5, plan) y el comentario del código están al día.

### ¿Tiene la lectura sin cerrojo alguna ventana de carrera?

No. Hay tres casos:

- **Fuera se ve `error`.** El esquema solo crece y ninguna ruta borra la columna. SQLite, sin caché compartida, no deja ver
  un esquema sin confirmar a otra conexión. Por tanto, lo que se ve está confirmado y es definitivo.
- **Fuera no se ve `error`.** Esa lectura solo elige el camino lento. Dentro del cerrojo de escritura se vuelve a comprobar:
  si otra instancia migró entre la lectura y el cerrojo, la segunda comprobación lo ve y no repite el `ALTER TABLE`. Lo
  matan M10 (sin comprobación interior) y M9 (comprobación interior antes del cerrojo) con la prueba de 8 procesos sobre
  almacenes antiguos.
- **Hay una migración ajena en curso o muerta a medias** (`revisores/r07_caida_y_lectores.py`, sale con 0):
  - Si un proceso muere con `os._exit` tras `BEGIN IMMEDIATE` + `ALTER` + `UPDATE` sin confirmar, queda un journal
    caliente. La siguiente apertura deshace ese journal, ve la tabla antigua, la migra y conserva la reserva
    (`COMPLETADO`, columnas completas).
  - Con un `ALTER` ajeno sin confirmar y `timeout=0`, la lectura de fuera ve el esquema confirmado (sin `error`), así que
    va por el camino lento. Ahí falla cerrado con «database is locked» y nunca responde sobre un esquema a medias. Cuando
    la otra conexión deshace, migra y responde.

### Reproducción y regresiones

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t200.py` | 6 passed, 3 de 3 veces. La prueba nueva `test_con_la_tabla_migrada_un_lector_no_espera_a_otra_escritura` falla con el código de la r01 (es M7, muerto) |
| `mutantes.py` | 11/11 muertos. M9 está adaptado; M10 y M11 son nuevos, y M11 es mi Q3 con la sangría nueva |
| `revisores/r06_mutantes_qa.py` | Arreglado para que corra entero: Q3 anclado con la sangría de la doble comprobación. Añadidos Q7 (camino lento sin CREATE), Q8 (la lectura de fuera mira otra columna) y Q9 (el camino rápido deja una transacción abierta). Q1-Q4 y Q7-Q9 muertos; Q5 y Q6 vivos, equivalentes |
| `revisores/r05_lector_con_escritor.py` | `DESCONOCIDO` en 0.00 s (sale con 0) |
| `revisores/r04_fugas.py` | 4 descriptores antes y 4 después; 300/300 bloqueadas y 300/300 de E/S fallan cerradas |
| `revisores/r01_estres_contencion.py 150 12` | 3 corridas, 0 fallos, peor iteración 2.5 s |
| ruff / mypy | `test_t200.py` sin avisos de ruff; `mypy bloque_a/contratos.py` sin errores |
| Gate `gate_t200_r02.log` | 12/12; ruff 2806/2806, mypy A 102/102, pytest A 8402 passed. El log (21:35:27) es anterior al commit (21:36:05); la copia del implementador está en `58cef91b` sin cambios pendientes |
| Ramas vecinas | El cambio sigue limitado a `_acuses`, así que no cambia lo visto en r01: `wip/t196` (`_acuses().close()`) es compatible, y la rama de Astra no toca esta función |

### Ficheros de esta ronda

- `revisores/r06_mutantes_qa.py`: modificado (Q3 reanclado; Q7, Q8 y Q9 nuevos).
- `revisores/r07_caida_y_lectores.py`: nuevo.

Ninguno tiene commit.
