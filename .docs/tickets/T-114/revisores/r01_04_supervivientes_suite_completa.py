"""QA r01 de T-114 · Todos los mutantes que `goldens_ct.py` no ve, aplicados A LA VEZ en una copia, y la suite COMPLETA del
Bloque A una sola vez. Si la suite pasa entera, ninguno de ellos lo detecta ninguna prueba; si falla, las pruebas que fallan
dicen cuáles sí (se atribuyen a mano).

Uso:  python r01_04_supervivientes_suite_completa.py <copia_desechable> M18,M20,... E02,E03,...
Restaura los ficheros al acabar.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
AQUI = Path(__file__).resolve().parent


def cargar(nombre):
    spec = importlib.util.spec_from_file_location(nombre, AQUI / f"{nombre}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


copia = Path(sys.argv[1]).resolve()
assert "qa_f3_mut" in str(copia), "solo en la copia desechable"
ids_m, ids_e = set(sys.argv[2].split(",")), set(sys.argv[3].split(",")) if len(sys.argv) > 3 else set()
ej = copia / "bloque_a" / "11_Ejecutor"
cambios = [("bloque_a/contratos.py", mid, viejo, nuevo) for mid, _, viejo, nuevo in cargar("r01_01_mutantes_contratos").MUTANTES if mid in ids_m]
cambios += [(fich, mid, viejo, nuevo) for mid, fich, _, viejo, nuevo in cargar("r01_03_mutantes_emision").MUTANTES if mid in ids_e]
originales = {}
aplicados = []
try:
    for fich, mid, viejo, nuevo in cambios:
        ruta = ej / fich
        originales.setdefault(ruta, ruta.read_text(encoding="utf-8"))
        texto = ruta.read_text(encoding="utf-8")
        if texto.count(viejo) != 1:
            print(f"{mid}: no aplicable junto a los anteriores ({texto.count(viejo)} apariciones)")
            continue
        ruta.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
        aplicados.append(mid)
    print("aplicados a la vez: " + ", ".join(aplicados), flush=True)
    r = subprocess.run([PY, "tests/goldens_ct.py"], cwd=ej, capture_output=True, text=True)
    print(f"goldens_ct.py con todos a la vez: rc={r.returncode} · {(r.stdout + r.stderr).strip().splitlines()[-1][:120]}", flush=True)
    r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf", "--tb=no"], cwd=ej, capture_output=True, text=True)
    lineas = r.stdout.strip().splitlines()
    print(f"suite completa: rc={r.returncode} · {lineas[-1]}")
    for x in lineas:
        if x.startswith(("FAILED", "ERROR")):
            print("  " + x[:200])
finally:
    for ruta, texto in originales.items():
        ruta.write_text(texto, encoding="utf-8")
