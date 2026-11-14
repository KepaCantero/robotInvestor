"""QA r01 de T-119 · los 33 casos de control por CT-09, en RC, re-ejecutados por CT-10, y en dos procesos.

 1. Cada caso de control de las 10 fichas se sirve por `Motor.servir` (no RECHAZADO), su `comprobar` pasa sobre lo
    servido, deja una entrada SERVICIO en RC, y `reejecutar` da coincide = SI. Tiempo de cada uno.
 2. `verificar_casos_control` de las 10: superados y una entrada CASOS_CONTROL en RC por ficha.
 3. Con `--huella`, imprime la huella de todos los resultados (para compararla entre dos procesos con distinto
    PYTHONHASHSEED). Sin él, lanza dos subprocesos y compara.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

eje = C.preparar(sys.argv)
from bloque_a.motor import servicio  # noqa: E402


def todos():
    m = C.motor()
    out = {}
    for f in C.P2:
        for i, c in enumerate(servicio.CASOS_CONTROL[f]):
            v, p = C.caso(f, i)
            t0 = time.time()
            r = C.servir(m, f, v, p)
            out[(f, i)] = (r, time.time() - t0, c)
    return m, out


if "--huella" in sys.argv:
    _, out = todos()
    print(hashlib.sha256(json.dumps({f"{f}/{i}": r.get("resultado") for (f, i), (r, _, _) in out.items()},
                                    sort_keys=True).encode()).hexdigest())
    sys.exit(0)

K = C.Contador("r01_01 casos de control por CT-09, RC y CT-10")
m, out = todos()
n = 0
for (f, i), (r, dt, c) in out.items():
    n += 1
    ok = r["estado"] in ("SERVED", "SERVED_WITH_LIMITATIONS")
    comp = ok and bool(c["comprobar"](r["resultado"]))
    e = m.almacen.estado("RC").get(r.get("calc_id")) if ok else None
    rc = bool(e) and e["tipo_entrada"] == "SERVICIO" and e["operacion"]["ficha_id"] == f
    re_ = m.reejecutar(r["calc_id"], "QA r01 T-119") if ok else {}
    K.comprobar(f"{f}[{i}] {r['estado']} {dt:5.2f}s comprobar={comp} RC={rc} CT-10={re_.get('coincide')}",
                ok and comp and rc and re_.get("coincide") == "SI", str(r.get("detalle"))[:200])
K.comprobar(f"son 33 casos ({n})", n == 33)
m2 = C.motor()
v = m2.verificar_casos_control(list(C.P2))
K.comprobar("verificar_casos_control: las 10 superan", all(x.get("superados") for x in v.values()) and len(v) == 10,
            str({k: x for k, x in v.items() if not x.get("superados")})[:300])
ent = [e for e in m2.almacen.leer("RC") if e.get("tipo_entrada") == "CASOS_CONTROL"]
K.comprobar(f"una entrada CASOS_CONTROL en RC por ficha ({len(ent)})", len(ent) == 10)
print("   ejemplo:", {k: ent[0].get(k) for k in ("operacion", "estado", "resultado")} if ent else None)
hs = []
for semilla in ("1", "4242"):
    pr = subprocess.run([sys.executable, __file__, str(eje), "--huella"], capture_output=True, text=True,
                        env={**os.environ, "PYTHONHASHSEED": semilla})
    hs.append(pr.stdout.strip().splitlines()[-1] if pr.stdout.strip() else pr.stderr[-200:])
K.comprobar(f"dos procesos (PYTHONHASHSEED 1 y 4242): misma huella {hs[0][:16]}", hs[0] == hs[1] and len(hs[0]) == 64, str(hs))
sys.exit(K.fin())
