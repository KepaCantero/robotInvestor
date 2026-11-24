# T-200 · Análisis técnico

## Causa raíz

`Mensajeria._acuses` (`bloque_a/11_Ejecutor/bloque_a/contratos.py`, desde T-92) abría `acuses.sqlite3` y, en modo
autocommit (el módulo `sqlite3` no abre transacción implícita antes de una sentencia DDL ni de un `PRAGMA`), hacía:

1. `CREATE TABLE IF NOT EXISTS acuses (id, huella, respuesta)`;
2. `PRAGMA table_info(acuses)` para ver si falta `error`;
3. `ALTER TABLE acuses ADD COLUMN error TEXT` si faltaba.

Cada paso era una transacción suelta. Entre el 2 y el 3 de un proceso cabe el 3 de otro: los dos ven la tabla sin `error`,
el primero la añade y el segundo falla con `sqlite3.OperationalError: duplicate column name: error`. Pasa con un almacén
nuevo (la tabla nace sin `error` en el paso 1) y con uno antiguo (anterior a T-92). El cerrojo del almacén no ayudaba: `_acuses`
no lo toma, y `Mensajeria._procesar` es un `threading.Lock` de cada instancia.

Evidencia: con el código de develop, `tests/test_t200.py::test_varios_procesos_abren_a_la_vez_un_almacen_sin_carrera` falla
10 de 10 veces con el almacén nuevo y 10 de 10 con el antiguo (8 procesos, 25 almacenes por ejecución; en cada ejecución
fallan varias rondas con «duplicate column name: error» y alguna reserva perdida). Con el arreglo, 0 de 10.

## Implementación

Archivo cambiado: `bloque_a/11_Ejecutor/bloque_a/contratos.py`, solo `_acuses`. Versión de la r01 (la de la r02 está en
«Ronda r02», abajo):

```python
db = sqlite3.connect(self.almacen.carpeta / "acuses.sqlite3")
try:
    db.execute("BEGIN IMMEDIATE")
    db.execute("CREATE TABLE IF NOT EXISTS acuses (...)")
    if "error" not in {fila[1] for fila in db.execute("PRAGMA table_info(acuses)")}:
        db.execute("ALTER TABLE acuses ADD COLUMN error TEXT")
    db.commit()
except BaseException:
    db.close()   # cerrar sin commit deshace la transacción
    raise
return db
```

- `BEGIN IMMEDIATE` toma el cerrojo de escritura (RESERVED) de SQLite antes de leer el esquema; otro proceso o hilo espera
  en su propio `BEGIN IMMEDIATE` (tiempo de espera por defecto de `sqlite3.connect`, 5 s) y, cuando entra, ya ve la columna.
- Un `BEGIN DEFERRED` no bastaría: con una tabla antigua el `CREATE TABLE IF NOT EXISTS` no escribe, dos procesos leen el
  esquema con cerrojo compartido y el segundo que intenta escribir recibe `database is locked` (interbloqueo que SQLite no
  espera). Lo mata el mutante M2 con la prueba del almacén antiguo.
- Ninguna excepción se captura para seguir: el bloque `except BaseException` cierra la conexión y relanza la misma. Así una
  base bloqueada, un disco lleno o un `ALTER TABLE` que falla por otro motivo salen tal cual y no dejan la tabla creada sin
  la columna (antes el `CREATE` ya estaba confirmado). Tampoco se fuga la conexión: antes, si `_acuses` fallaba,
  `closing(...)` no llegaba a envolverla.
- La conexión que se devuelve está fuera de transacción, como antes: `procesar_una_vez`, `estado_reserva` y `reconciliar` no
  cambian. La prueba de T-196 que llama a `mensajeria._acuses().close()` sigue funcionando.

## Decisiones y desviaciones

- **`BEGIN IMMEDIATE` en vez de `almacen._transaccion()`** (las dos opciones del encargo). Las dos son seguras entre
  procesos; se elige la de SQLite porque protege el fichero que se migra sin depender de que todo el que lo abra tome el
  cerrojo del almacén, y porque no anida ese cerrojo dentro de `Mensajeria._procesar` (que `procesar_una_vez` sostiene
  mientras el ciclo toma el del almacén): no crea un orden de cerrojos nuevo.
- **Coste (corregido en la r02):** en la r01 cada apertura tomaba el cerrojo de escritura (H-01). Desde la r02 solo lo
  toma la apertura que tiene que crear o migrar la tabla; las demás solo leen el esquema, como en develop.

## Búsqueda del mismo patrón

- `contratos.py`: el único SQLite es la tabla de acuses. `INSERT OR IGNORE` + `SELECT` de `procesar_una_vez` van en el mismo
  `with db:` (transacción implícita desde el `INSERT`); `UPDATE` y `DELETE` son sentencias únicas. Ninguna otra comprobación
  seguida de un cambio en disco.
- `almacen.py`: la apertura (sellos, `ARCHIVOS_NUEVOS`, marca de formato, recuperación de líneas cortadas), `nuevo_id`,
  `escribir`, `leer` y `verificar_integridad` van todas dentro de `_transaccion()`. `self.carpeta.mkdir(exist_ok=True)` es
  idempotente. No hay nada que corregir.
- Ningún otro módulo de `bloque_a/` usa SQLite.

## Límites conocidos

- Si otra conexión mantiene una escritura más de 5 s, `_acuses` falla con `database is locked` (falla cerrado; antes pasaba
  lo mismo con el `CREATE`).
- La prueba de concurrencia de `wip/t196` sigue creando la tabla antes; se limpia al integrar T-196 (fuera de este ticket).

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q tests/test_t200.py
../../.venv/bin/python ../../.docs/tickets/T-200/mutantes.py .
# que falla con develop: sustituir contratos.py por el de origin/develop y repetir la primera orden
```

## Ronda r02 (QA r01 NO APTO, H-01)

**H-01 (media).** El `BEGIN IMMEDIATE` de la r01 se tomaba en cada apertura: `estado_reserva` (y `reconciliar`), de solo
lectura, esperaba a cualquier escritura en curso y fallaba con «database is locked» a los 5 s
(`revisores/r05_lector_con_escritor.py`: develop `DESCONOCIDO` en 0,00 s, r01 error en 5,01 s).

**Corrección** (la de `revisores/r03_correccion_propuesta.diff`, doble comprobación):

```python
try:
    if "error" not in {fila[1] for fila in db.execute("PRAGMA table_info(acuses)")}:
        db.execute("BEGIN IMMEDIATE")
        db.execute("CREATE TABLE IF NOT EXISTS acuses (...)")
        if "error" not in {fila[1] for fila in db.execute("PRAGMA table_info(acuses)")}:
            db.execute("ALTER TABLE acuses ADD COLUMN error TEXT")
        db.commit()
except BaseException:
    db.close()
    raise
```

- Con la tabla migrada solo se ejecuta el primer `PRAGMA` (lectura, sin transacción abierta): el mismo coste y la misma
  contención que en develop.
- La lectura de fuera, sin cerrojo, es segura porque solo decide si hace falta el camino lento. La decisión que importa (si
  hay que hacer el `ALTER TABLE`) se toma dentro, con el cerrojo de escritura, con una segunda comprobación. Ver la columna
  fuera también es definitivo: una vez añadida no se quita.
- En una tabla que no existe, `PRAGMA table_info` devuelve una lista vacía, así que entra en el camino lento.

**Pruebas y mutantes:**
- Prueba nueva `test_con_la_tabla_migrada_un_lector_no_espera_a_otra_escritura`, equivalente a r05: otra conexión con
  `BEGIN IMMEDIATE` + `INSERT` sin confirmar y conexiones de la mensajería con tiempo de espera 0. `estado_reserva` da
  `DESCONOCIDO` sin error. Falla con el código de la r01 (`4b33dbc8`) y pasa con el de la r02.
- `mutantes.py`: M7 pasa a «siempre toma el cerrojo de escritura» (el código de la r01; lo mata la prueba nueva). M9 se adapta
  (la comprobación interior hecha antes de tomar el cerrojo). Nuevos: M10 «sin la comprobación interior» y M11, que es el Q3
  de la QA con la sangría nueva. 11 mutantes, 11 muertos.
- Scripts de la QA:
  - r05 sale con 0 (`DESCONOCIDO` en 0,00 s).
  - r04 no deja fugas: 4 descriptores antes y 4 después.
  - r06: Q1, Q2 y Q4 muertos; Q5 y Q6 vivos, que son los dos equivalentes declarados.
  - Q3 no se aplica tal cual: su texto lleva la sangría de la r01 y el `assert` del script lo detiene. Se ha ejecutado sin
    cambiar el script, con una copia fuera del repositorio que solo quita Q3. Q3 queda cubierto por M11 en `mutantes.py`.
