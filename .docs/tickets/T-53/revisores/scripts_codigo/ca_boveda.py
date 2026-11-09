"""Bóveda HT-01: (a) caducidad ignorada si no se pasa 'hoy'; (b) caducidad sin validar rompe estado(); (c) secretos.json
se crea con los permisos del umask antes del chmod 0600 (y si chmod falla, se queda así sin aviso)."""
import datetime as dt, os, stat, tempfile
from bloque_a.herramientas import ht01_boveda as hb
d = tempfile.mkdtemp(dir=".")
b = hb.Boveda(d)
r = b.depositar("API X", "VALOR-SECRETO-1", caducidad="2020-01-01")
print("(a) estado con hoy:", b.estado(r["credencial_ref"], dt.date(2026, 11, 9))["estado"],
      "| valor_para_herramienta sin hoy:", b.valor_para_herramienta(r["credencial_ref"]))
b.depositar("API Y", "VALOR-SECRETO-2", caducidad="31/12/2026")   # aceptado sin validar
try:
    b.listar(dt.date(2026, 11, 9)); print("(b) listar OK")
except Exception as e:
    print("(b) listar() falla tras depositar una caducidad no ISO:", type(e).__name__, e)
modos = []
real = os.chmod
def espia(p, m):
    modos.append(oct(stat.S_IMODE(os.stat(p).st_mode))); real(p, m)
os.chmod = espia
d2 = tempfile.mkdtemp(dir=".")
hb.Boveda(d2).depositar("API Z", "VALOR-SECRETO-3")
os.chmod = real
print("(c) permisos de secretos.json justo antes del chmod:", modos[0], "(umask", oct(os.umask(0o022)), ")")
