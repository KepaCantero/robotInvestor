"""QA r01 de T-200: ¿se fugan descriptores o conexiones? 300 llamadas con la base bloqueada (timeout 0), 300 con el
ALTER fallando y 300 normales; se cuentan los descriptores abiertos de /proc/self/fd antes y después.
Uso: python r04_fugas.py <bloque_a/11_Ejecutor>"""
import gc
import os
import sqlite3
import sys
import tempfile
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a.contratos as c
from bloque_a.almacen import Almacen


def fds():
    return len(os.listdir("/proc/self/fd"))


conectar = sqlite3.connect
with tempfile.TemporaryDirectory() as d:
    ms = c.Mensajeria(Almacen(d))
    gc.disable()           # sin recolector: una conexión no cerrada se quedaría abierta
    antes = fds()
    otra = conectar(Path(d) / "acuses.sqlite3", isolation_level=None)
    otra.execute("BEGIN EXCLUSIVE")
    c.sqlite3.connect = lambda *a, **kw: conectar(*a, **{**kw, "timeout": 0})
    bloq = 0
    for _ in range(300):
        try:
            ms.estado_reserva("MSG-X")
        except sqlite3.OperationalError:
            bloq += 1
    otra.rollback()
    otra.close()

    class Conexion(sqlite3.Connection):
        def execute(self, sql, *a):
            if sql.startswith("ALTER"):
                raise sqlite3.OperationalError("disk I/O error")
            return super().execute(sql, *a)
    c.sqlite3.connect = lambda *a, **kw: conectar(*a, factory=Conexion, **kw)
    io = 0
    for _ in range(300):
        try:
            ms.estado_reserva("MSG-X")
        except sqlite3.OperationalError:
            io += 1
    c.sqlite3.connect = conectar
    for i in range(300):
        m = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": f"s{i}"})
        ms.procesar_una_vez(m, lambda _: {"ok": 1})
        ms.estado_reserva(m["msg_id"])
    despues = fds()
    print(f"bloqueadas={bloq} io={io} fds_antes={antes} fds_despues={despues}")
    sys.exit(0 if (bloq, io) == (300, 300) and despues == antes else 1)
