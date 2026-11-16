"""T-152 · QA r01 · H-01: semillas de `_en_tramo` (el generador de la prueba del borde) en las que el 2 % del código y un
umbral más alto (2,04 %, 2,5 %, 4 %, sin umbral) dan resultados distintos con una copia truncada a 0,01 que cruza por
poco el 2 % de q/p. Sirven para una prueba que fije también el lado de arriba del umbral (mata U2 de `mutantes.py`).

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-152/revisores/r01_05_semillas_qa.py
Solo informa: termina con 0."""
import sys, importlib.util, types
from pathlib import Path
import numpy as np
EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"; sys.path.insert(0, str(EJ)); sys.path.insert(0, str(EJ/"tests"))
spec = importlib.util.spec_from_file_location("t", EJ/"tests"/"test_t150.py"); t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
fb = t.fb
def mod(expr):
    src = Path(fb.__file__).read_text(); m = types.ModuleType("bloque_a.motor.fbx"); m.__package__="bloque_a.motor"; m.__file__=fb.__file__
    exec(compile(src.replace("    desplaza = rel <= tol\n", f"    desplaza = {expr}\n"), "fbx", "exec"), m.__dict__); return m
mods = {"2%": fb, "2,04%": mod("rel / (1 + rel) <= tol"), "2,5%": mod("2 * rel <= 0.025"), "4%": mod("rel <= 2 * tol"), "inf": mod("rel >= 0"), "1,98%": mod("rel <= 0.99 * tol")}
for lo, hi in ((0.48, 0.9), (0.47, 0.9), (0.4905, 0.9)):
    out = []
    for s in range(100):
        x = t._en_tramo(lo, hi, s); y = t._trunc(x, 0.01)
        r = {}
        for k, m in mods.items():
            t.fb = m; r[k] = t._juntas(x, y)
        t.fb = fb
        if r["2%"] != r["4%"] or r["2%"] != r["2,04%"]:
            out.append((s, "".join("T" if r[k] else "·" for k in mods)))
    print(f"[{lo}, {hi}] semillas donde el 2 % y uno más alto difieren ({'/'.join(mods)}; T = se agrupa):")
    print("  " + ", ".join(f"{s}:{v}" for s, v in out))
