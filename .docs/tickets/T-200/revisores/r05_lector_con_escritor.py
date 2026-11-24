"""QA r01 de T-200 (H-01, determinista): con la tabla de acuses ya creada y migrada, otra instancia tiene una escritura en
curso (cerrojo RESERVED, como el INSERT de la reserva de procesar_una_vez de otro proceso). estado_reserva solo lee: en
develop responde al momento; con el BEGIN IMMEDIATE incondicional espera el timeout de sqlite3.connect (5 s) y, si la
escritura dura más (aquí no se suelta), falla con «database is locked».
Uso: python r05_lector_con_escritor.py <bloque_a/11_Ejecutor>"""
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
from bloque_a.almacen import Almacen
from bloque_a.contratos import Mensajeria

with tempfile.TemporaryDirectory() as d:
    ms = Mensajeria(Almacen(d))
    ms.estado_reserva("MSG-X")                      # tabla creada y migrada
    otra = sqlite3.connect(Path(d) / "acuses.sqlite3", isolation_level=None)
    otra.execute("BEGIN IMMEDIATE")
    otra.execute("INSERT INTO acuses (id, huella) VALUES ('MSG-OTRO', 'h')")
    t = time.perf_counter()
    try:
        r = ms.estado_reserva("MSG-X")["estado"]
    except sqlite3.OperationalError as e:
        r = f"OperationalError: {e}"
    dur = time.perf_counter() - t
    otra.rollback()
    otra.close()
    print(f"estado_reserva con otra escritura en curso: {r} en {dur:.2f} s")
    sys.exit(0 if r == "DESCONOCIDO" and dur < 1 else 1)
