"""T-200: la tabla de acuses de la mensajería (`acuses.sqlite3`) se crea y se migra sin carrera entre procesos.

Antes, `Mensajeria._acuses` comprobaba la columna `error` con `PRAGMA table_info` y la añadía con `ALTER TABLE` fuera de
cualquier cerrojo: varias instancias que abrían a la vez un almacén nuevo podían ver las dos la tabla sin la columna y la
segunda fallaba con «duplicate column name: error» (QA r02 de T-196). Ahora, si falta la columna, la creación, una segunda
comprobación y el cambio van en la misma transacción `BEGIN IMMEDIATE`; con la tabla ya migrada solo se lee (r02, H-01).
Sin red ni claves.
"""
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
from bloque_a.almacen import Almacen
from bloque_a.contratos import Mensajeria

RAIZ = Path(__file__).resolve().parents[1]
PROCESOS = 8      # procesos reales que abren a la vez cada almacén nuevo
RONDAS = 25       # almacenes nuevos, uno por ronda

# Cada trabajador abre su almacén, avisa con «listo» y espera la orden «ya» para tocar la tabla de acuses: así todos llegan a
# `_acuses` a la vez. Los pares hacen `procesar_una_vez` (la ruta de `Bloque.peticion`) y los impares `estado_reserva`.
TRABAJADOR = r"""
import sys, traceback
sys.path.insert(0, sys.argv[1])
from bloque_a.almacen import Almacen
from bloque_a.contratos import Mensajeria
par = int(sys.argv[2]) % 2 == 0
for linea in sys.stdin:
    carpeta = linea.strip()
    if not carpeta:
        break
    ms = Mensajeria(Almacen(carpeta))
    print("listo", flush=True)
    sys.stdin.readline()
    try:
        if par:
            m = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "saldo"})
            assert ms.procesar_una_vez(m, lambda _: {"ok": 1}) == ({"ok": 1}, False)
        else:
            assert ms.estado_reserva("MSG-NINGUNO")["estado"] == "DESCONOCIDO"
        print("ok", flush=True)
    except BaseException as e:
        print("fallo " + type(e).__name__ + ": " + str(e).replace("\n", " "), flush=True)
"""


def _columnas(ruta):
    with sqlite3.connect(ruta) as db:
        return [fila[1] for fila in db.execute("PRAGMA table_info(acuses)")]


@pytest.mark.parametrize("antiguo", [False, True], ids=["almacen_nuevo", "almacen_antiguo"])
def test_varios_procesos_abren_a_la_vez_un_almacen_sin_carrera(tmp_path, antiguo):
    """CA-1: 8 procesos abren a la vez 25 almacenes nuevos; ninguno falla y la tabla queda con su columna `error`.
    CA-2: lo mismo con 25 almacenes antiguos (tabla de acuses sin `error`): la migración concurrente tampoco falla. Con el
    almacén antiguo el `CREATE TABLE IF NOT EXISTS` no escribe, así que solo un `BEGIN IMMEDIATE` (no uno diferido) evita
    que dos procesos lean la tabla sin la columna antes de que uno la añada."""
    trabajadores = [subprocess.Popen([sys.executable, "-c", TRABAJADOR, str(RAIZ), str(i)], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, text=True, bufsize=1) for i in range(PROCESOS)]
    fallos = []
    try:
        for ronda in range(RONDAS):
            carpeta = tmp_path / f"almacen_{ronda}"
            Almacen(carpeta)      # el almacén existe; la tabla de acuses todavía no
            assert not (carpeta / "acuses.sqlite3").exists()
            if antiguo:
                with sqlite3.connect(carpeta / "acuses.sqlite3") as db:
                    db.execute("CREATE TABLE acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)")
            for t in trabajadores:
                t.stdin.write(f"{carpeta}\n")
            assert [t.stdout.readline().strip() for t in trabajadores] == ["listo"] * PROCESOS
            for t in trabajadores:
                t.stdin.write("ya\n")
            for t in trabajadores:
                respuesta = t.stdout.readline().strip()
                if respuesta != "ok":
                    fallos.append((ronda, respuesta))
            if (columnas := _columnas(carpeta / "acuses.sqlite3")) != ["id", "huella", "respuesta", "error"]:
                fallos.append((ronda, columnas))
            with sqlite3.connect(carpeta / "acuses.sqlite3") as db:
                if (n := db.execute("SELECT COUNT(*) FROM acuses").fetchone()[0]) != PROCESOS // 2:
                    fallos.append((ronda, f"{n} reservas"))
    finally:
        for t in trabajadores:
            t.stdin.close()
        for t in trabajadores:
            t.wait(timeout=60)
    assert not fallos, fallos


def test_almacen_antiguo_sin_columna_error_se_migra(tmp_path):
    """CA-2: una tabla de acuses anterior a T-92 (sin `error`) gana la columna al abrirse y conserva sus reservas."""
    ms = Mensajeria(Almacen(tmp_path))
    m = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "saldo"})
    with sqlite3.connect(tmp_path / "acuses.sqlite3") as db:
        db.execute("CREATE TABLE acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)")
        db.execute("INSERT INTO acuses (id, huella, respuesta) VALUES ('MSG-VIEJO', 'h', '{\"ok\": 2}')")
    assert ms.estado_reserva("MSG-VIEJO") == {"msg_id": "MSG-VIEJO", "estado": "COMPLETADO", "error": None}
    assert _columnas(tmp_path / "acuses.sqlite3") == ["id", "huella", "respuesta", "error"]
    with pytest.raises(RuntimeError):
        ms.procesar_una_vez(m, lambda _: (_ for _ in ()).throw(RuntimeError("x")))
    assert ms.estado_reserva(m["msg_id"])["estado"] == "FALLIDO"
    # abrirla otra vez no vuelve a migrar ni falla
    assert Mensajeria(Almacen(tmp_path)).estado_reserva("MSG-VIEJO")["estado"] == "COMPLETADO"
    assert _columnas(tmp_path / "acuses.sqlite3") == ["id", "huella", "respuesta", "error"]


def test_otro_error_de_sqlite_se_propaga_y_cierra_la_conexion(tmp_path, monkeypatch):
    """CA-3: un `OperationalError` distinto (aquí, la base bloqueada por otra escritura) no se traga: sale tal cual, la
    conexión se cierra y no queda ninguna tabla a medias."""
    ms = Mensajeria(Almacen(tmp_path))
    ruta = tmp_path / "acuses.sqlite3"
    abiertas = []
    conectar = sqlite3.connect

    def _conectar(*a, **kw):
        db = conectar(*a, **{**kw, "timeout": 0})
        abiertas.append(db)
        return db
    otra = sqlite3.connect(ruta, isolation_level=None)
    otra.execute("BEGIN EXCLUSIVE")     # otra escritura en curso tiene la base
    try:
        monkeypatch.setattr("bloque_a.contratos.sqlite3.connect", _conectar)
        with pytest.raises(sqlite3.OperationalError, match="locked"):
            ms.estado_reserva("MSG-NINGUNO")
    finally:
        otra.rollback()
        otra.close()
    assert len(abiertas) == 1
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        abiertas[0].execute("SELECT 1")
    assert _columnas(ruta) == []
    monkeypatch.undo()
    assert ms.estado_reserva("MSG-NINGUNO")["estado"] == "DESCONOCIDO"
    assert _columnas(ruta) == ["id", "huella", "respuesta", "error"]


def test_un_fallo_dentro_de_la_migracion_deshace_la_tabla(tmp_path, monkeypatch):
    """CA-3: si el `ALTER TABLE` falla por otro motivo, el error sale y la transacción se deshace entera (falla cerrado)."""
    ms = Mensajeria(Almacen(tmp_path))
    real, conectar = sqlite3.Connection, sqlite3.connect

    class Conexion(real):
        def execute(self, sql, *a):
            if sql.startswith("ALTER TABLE"):
                raise sqlite3.OperationalError("disk I/O error")
            return super().execute(sql, *a)
    monkeypatch.setattr("bloque_a.contratos.sqlite3.connect", lambda *a, **kw: conectar(*a, factory=Conexion, **kw))
    with pytest.raises(sqlite3.OperationalError, match="disk I/O"):
        ms.estado_reserva("MSG-NINGUNO")
    monkeypatch.undo()
    assert _columnas(tmp_path / "acuses.sqlite3") == []


def test_con_la_tabla_migrada_un_lector_no_espera_a_otra_escritura(tmp_path, monkeypatch):
    """r02 (QA r01, H-01): con la tabla ya migrada, `_acuses` solo lee el esquema y no toma el cerrojo de escritura:
    `estado_reserva` responde aunque otra instancia tenga una escritura en curso (BEGIN IMMEDIATE + INSERT sin confirmar).
    Con tiempo de espera 0 en las conexiones de la mensajería, un cerrojo de escritura incondicional falla al momento con
    «database is locked» (antes esperaba 5 s)."""
    ms = Mensajeria(Almacen(tmp_path))
    assert ms.estado_reserva("MSG-X")["estado"] == "DESCONOCIDO"      # tabla creada y migrada
    conectar = sqlite3.connect
    otra = conectar(tmp_path / "acuses.sqlite3", isolation_level=None)
    otra.execute("BEGIN IMMEDIATE")
    otra.execute("INSERT INTO acuses (id, huella) VALUES ('MSG-OTRO', 'h')")
    try:
        monkeypatch.setattr("bloque_a.contratos.sqlite3.connect", lambda *a, **kw: conectar(*a, **{**kw, "timeout": 0}))
        assert ms.estado_reserva("MSG-X") == {"msg_id": "MSG-X", "estado": "DESCONOCIDO"}
        assert ms.estado_reserva("MSG-OTRO") == {"msg_id": "MSG-OTRO", "estado": "DESCONOCIDO"}   # sin confirmar: no se ve
    finally:
        monkeypatch.undo()
        otra.rollback()
        otra.close()
    assert _columnas(tmp_path / "acuses.sqlite3") == ["id", "huella", "respuesta", "error"]
