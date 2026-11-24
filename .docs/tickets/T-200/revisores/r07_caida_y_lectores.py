"""QA r02 de T-200: la lectura sin cerrojo del camino rápido frente a (a) una migración que muere a medias y (b) lectores
que leen mientras otra instancia migra.
(a) Un proceso hace BEGIN IMMEDIATE + ALTER TABLE sobre una tabla antigua y muere con os._exit sin confirmar (queda el
    journal caliente). Después Mensajeria abre el almacén: debe ver la tabla sin `error`, migrarla y conservar la reserva.
(b) Una conexión ajena tiene un ALTER TABLE sin confirmar; con timeout 0, estado_reserva (camino rápido NO: la tabla
    confirmada sigue sin `error`) debe fallar cerrado con «database is locked», nunca ver la columna sin confirmar ni
    responder sobre un esquema a medias; tras deshacer la ajena, migra y responde.
Uso: python -I r07_caida_y_lectores.py <bloque_a/11_Ejecutor>"""
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a.contratos as c  # noqa: E402
from bloque_a.almacen import Almacen  # noqa: E402

MUERE = r"""
import os, sqlite3, sys
db = sqlite3.connect(sys.argv[1], isolation_level=None)
db.execute("BEGIN IMMEDIATE")
db.execute("ALTER TABLE acuses ADD COLUMN error TEXT")
db.execute("UPDATE acuses SET error='X'")
os._exit(9)
"""
ok = True
with tempfile.TemporaryDirectory() as d:
    ruta = Path(d) / "acuses.sqlite3"
    ms = c.Mensajeria(Almacen(d))
    with sqlite3.connect(ruta) as db:
        db.execute("CREATE TABLE acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)")
        db.execute("INSERT INTO acuses (id, huella, respuesta) VALUES ('MSG-V', 'h', '{}')")
    r = subprocess.run([sys.executable, "-c", MUERE, str(ruta)], check=False)
    journal = (Path(d) / "acuses.sqlite3-journal").exists()
    est = ms.estado_reserva("MSG-V")
    cols = [f[1] for f in sqlite3.connect(ruta).execute("PRAGMA table_info(acuses)")]
    print(f"(a) salida={r.returncode} journal_caliente={journal} estado={est} columnas={cols}")
    ok &= r.returncode == 9 and est == {"msg_id": "MSG-V", "estado": "COMPLETADO", "error": None} and cols[-1] == "error"

with tempfile.TemporaryDirectory() as d:
    ruta = Path(d) / "acuses.sqlite3"
    ms = c.Mensajeria(Almacen(d))
    with sqlite3.connect(ruta) as db:
        db.execute("CREATE TABLE acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)")
    otra = sqlite3.connect(ruta, isolation_level=None)
    otra.execute("BEGIN IMMEDIATE")
    otra.execute("ALTER TABLE acuses ADD COLUMN error TEXT")
    conectar = sqlite3.connect
    c.sqlite3.connect = lambda *a, **kw: conectar(*a, **{**kw, "timeout": 0})
    try:
        res = ms.estado_reserva("MSG-X")
    except sqlite3.OperationalError as e:
        res = f"OperationalError: {e}"
    otra.rollback()
    otra.close()
    despues = ms.estado_reserva("MSG-X")
    c.sqlite3.connect = conectar
    cols = [f[1] for f in sqlite3.connect(ruta).execute("PRAGMA table_info(acuses)")]
    print(f"(b) con ALTER ajeno sin confirmar: {res}; después: {despues}; columnas={cols}")
    ok &= res == "OperationalError: database is locked" and despues["estado"] == "DESCONOCIDO" and cols[-1] == "error"
sys.exit(0 if ok else 1)
