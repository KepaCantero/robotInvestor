"""QA r01 de T-121 · los casos de control de todas las fichas (y AUD-REX-001) siguen superados tras T-121, en dos pasadas.
Uso: .venv/bin/python -I .docs/tickets/T-121/revisores/r01_04_casos_control.py [ejecutor]"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a.motor import servicio  # noqa: E402

t0 = time.time()
m = C.motor()
res = m.verificar_casos_control()
mal = {f: r for f, r in res.items() if not r.get("superados", r.get("superado", r.get("ok")))}
claves = sorted({k for r in res.values() for k in r})
print(f"fichas verificadas: {len(res)} · manejadores: {len(servicio.IMPLEMENTADAS)} · claves de cada resultado: {claves}")
print(f"no superadas: {len(mal)} {sorted(mal)[:10]} · {time.time() - t0:.0f} s")
sys.exit(1 if mal else 0)
