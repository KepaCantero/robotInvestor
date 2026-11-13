"""QA r03 de T-88 · 01: el registro RUN de F5 conserva todas sus claves (en especial `consumo`) y `Bloque.estado()` sigue
dando el consumo de los últimos runs.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r03_01_f5_consumo_y_claves.py [--ejecutor RUTA] [--control RUTA]

`--control` (opcional): otro 11_Ejecutor (p. ej. un worktree de d1a5a1b) cuyas claves de F5 se toman como referencia; se
ejecuta en un subproceso aparte. Esperado: las mismas claves que el control; `consumo` presente con su `uc` y
`estado()["ultimos_runs"][-1]["uc"]` no nulo (Documento 0, 10.3: «el consumo real se registra en F5»)."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import Marcador, bloque, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
from conftest import AS_OF, config_pruebas  # noqa: E402

control = None
if "--control" in resto:
    control = resto[resto.index("--control") + 1]


def claves(diseno):
    b = bloque(config_pruebas(diseno=diseno))
    b.ciclo(AS_OF)
    run = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]
    est = b.estado()["ultimos_runs"][-1]
    return {"claves": sorted(run), "consumo": run.get("consumo"), "uc_estado": est.get("uc")}


if "--solo-json" in resto:
    print(json.dumps({d: claves(d) for d in ("v5", "v6")}, default=str))
    sys.exit(0)

m = Marcador()
res = {d: claves(d) for d in ("v5", "v6")}
ref = None
if control:
    out = subprocess.run([sys.executable, "-I", __file__, "--ejecutor", control, "--solo-json"], capture_output=True, text=True)
    ref = json.loads(out.stdout.strip().splitlines()[-1])
for d, r in res.items():
    m.check(f"{d}: F5 RUN lleva `consumo`", r["consumo"] is not None, f"claves={r['claves']}")
    m.check(f"{d}: estado() da el consumo del último run", r["uc_estado"] is not None, f"uc={r['uc_estado']}")
    if ref:
        faltan = sorted(set(ref[d]["claves"]) - set(r["claves"]))
        sobran = sorted(set(r["claves"]) - set(ref[d]["claves"]))
        m.check(f"{d}: mismas claves de F5 que el control", not faltan and not sobran, f"faltan={faltan} sobran={sobran}")
sys.exit(m.fin())
