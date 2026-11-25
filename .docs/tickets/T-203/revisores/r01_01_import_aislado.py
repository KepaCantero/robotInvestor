"""QA r01 T-203 · 01: los envoltorios HT-02/03/07 cargan en un intérprete nuevo y aislado (-I), desde fuera del repo,
como primer import del paquete, y reexportan los mismos objetos que la referencia. Se ejecuta contra una o varias copias.

Uso: python -I r01_01_import_aislado.py <copia_repo> [<copia_repo> ...]   (lanza un intérprete -I por módulo)
"""
import json
import subprocess
import sys
import tempfile

SONDA = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
assert "bloque_a" not in sys.modules
import importlib
h = importlib.import_module("bloque_a.herramientas." + sys.argv[2])
ref = h._ref
pub = sorted(n for n in vars(ref) if not n.startswith("_"))
extra = sorted(set(vars(h)) - set(pub) - {n for n in vars(h) if n.startswith("__")})
print(json.dumps({"ref": ref.__name__, "fichero": ref.__file__, "n": len(pub),
                  "mismos": all(getattr(h, n) is getattr(ref, n) for n in pub), "extra": extra,
                  "modulo": h.modulo is ref}))
"""

fallos = 0
for copia in sys.argv[1:]:
    ejecutor = copia.rstrip("/") + "/bloque_a/11_Ejecutor"
    for m, nombre in (("ht02", "ht02_verificador_enlaces"), ("ht03", "ht03_puntuaciones"), ("ht07", "ht07_legibilidad")):
        with tempfile.TemporaryDirectory() as fuera:
            r = subprocess.run([sys.executable, "-I", "-c", SONDA, ejecutor, m], cwd=fuera, capture_output=True, text=True)
        if r.returncode:
            print("FALLO", copia, m, r.stderr.strip().splitlines()[-1]); fallos += 1; continue
        d = json.loads(r.stdout)
        ok = (d["ref"] == nombre and d["fichero"].startswith(ejecutor) and d["mismos"] and d["modulo"]
              and d["extra"] == ["DIR_REFERENCIA", "_ref", "modulo"] and d["n"] > 0)
        fallos += not ok
        print("OK " if ok else "FALLO", copia, m, d["n"], "nombres públicos", d["extra"])
sys.exit(1 if fallos else 0)
