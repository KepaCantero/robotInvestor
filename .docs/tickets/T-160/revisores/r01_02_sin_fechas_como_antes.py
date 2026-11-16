"""T-160 QA r01 · FC-EVAL-001 sin `fechas` da lo mismo que antes, y las cifras de un certificado no cambian.

Extrae `bloque_a/` de la versión anterior (por defecto HEAD~1) y de la actual (HEAD) en una carpeta desechable y, en cada una,
en un proceso aparte con su propio paquete:
  1. sirve FC-EVAL-001 por `Motor.servir` sin fechas con 12 combinaciones de entradas y parámetros (con p_ref y sin ella, con
     `min_conglomerados` en los parámetros pero sin fechas, n pequeño, n = 30, tasa base, nivel, semilla y h distintos) y llama a
     `f_fc_eval` directamente;
  2. revisa los certificados de dos celdas sembradas (RF hábil, RV sin habilidad) y guarda `evaluadas` y las cifras del CERT-.
Compara el JSON de las dos versiones: en (1) tiene que ser idéntico; en (2), idéntico salvo los campos nuevos de T-160.

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-160/revisores/r01_02_sin_fechas_como_antes.py <carpeta_desechable> [base]
Termina con 1 si algo difiere.
"""
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
DESTINO = Path(sys.argv[1]).resolve()
BASE = sys.argv[2] if len(sys.argv) > 2 else "HEAD~1"
assert not DESTINO.exists() or not any(DESTINO.iterdir()), "la carpeta tiene que estar vacía"
PY = str(RAIZ / ".venv" / "bin" / "python")

SONDA = r'''
import json, sys, random
from pathlib import Path
sys.path.insert(0, "."); sys.path.insert(0, "tests")
import numpy as np
from bloque_a.motor import servicio
from conftest import nuevo_bloque
from test_fase4_huecos import _sembrar_celda
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo
tmp = Path(sys.argv[1])
uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
rng = random.Random(7)
casos = []
for n in (5, 29, 30, 60, 150):
    p = [round(rng.random(), 3) for _ in range(n)]
    o = [int(rng.random() < x) for x in p]
    casos.append(({"p": p, "o": o}, {"replicas": 40, "simulaciones": 40}))
    casos.append(({"p": p, "o": o, "p_ref": [0.4] * n}, {"replicas": 40, "simulaciones": 40, "tasa_base": 0.3, "nivel": 0.8}))
p = [0.3, 0.7] * 40; o = [0, 1, 1, 1, 0, 0, 1, 0] * 10
casos.append(({"p": p, "o": o}, {"replicas": 40, "simulaciones": 40, "min_conglomerados": 10}))
casos.append(({"p": p, "o": o}, {"replicas": 40, "simulaciones": 40, "semilla_bootstrap": 7, "h": 3}))
b = nuevo_bloque(tmp / "m", uni)
out = {"servir": [], "directo": []}
for v, prm in casos:
    r = b.motor.servir({"operacion": "FC-EVAL-001", "fecha_corte": "2026-01-02", "datos": [{"valores": v}], "parametros": prm}, "AG-20")
    out["servir"].append({"estado": r.get("estado"), "resultado": r.get("resultado"), "limitaciones": r.get("limitaciones")})
    m, lim = servicio.f_fc_eval({"valores": v}, prm)
    out["directo"].append(json.loads(json.dumps({"m": m, "lim": lim}, default=float)))
b2 = nuevo_bloque(tmp / "c", uni)
b2.reloj.fijar("2026-01-02")
_sembrar_celda(b2, "RF", 150, lambda q: q, 5001)
_sembrar_celda(b2, "RV", 150, lambda q: 0.5, 6001)
res = b2.evaluador.revisar_certificados("2026-01-02")
nuevos = {"calc_soporte", "curva_fiabilidad", "reejecucion", "reejecucion_ct10"}
out["evaluadas"] = {k: {c: x for c, x in v.items() if c != "reejecucion_ct10"} for k, v in res["evaluadas"].items()}
out["certs"] = [{c: x for c, x in e.items() if c not in nuevos and c != "id"} for e in res["emitidos"]]
print(json.dumps(out, sort_keys=True, default=str))
'''


def extraer(rev: str, carpeta: Path) -> Path:
    carpeta.mkdir(parents=True)
    arch = subprocess.run(["git", "-C", str(RAIZ), "archive", rev, "bloque_a"], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(carpeta)], input=arch, check=True)
    return carpeta / "bloque_a" / "11_Ejecutor"


def correr(ejecutor: Path, tmp: Path) -> dict:
    tmp.mkdir(parents=True)
    r = subprocess.run([PY, "-c", SONDA, str(tmp)], cwd=ejecutor, capture_output=True, text=True, timeout=1800)
    if r.returncode:
        sys.exit(f"falla la sonda en {ejecutor}:\n{r.stderr[-3000:]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


DESTINO.mkdir(parents=True, exist_ok=True)
antes = correr(extraer(BASE, DESTINO / "antes"), DESTINO / "tmp_antes")
despues = correr(extraer("HEAD", DESTINO / "despues"), DESTINO / "tmp_despues")
mal = 0
for k in ("servir", "directo", "evaluadas", "certs"):
    igual = antes[k] == despues[k]
    mal += not igual
    detalle = f"{len(antes[k])} casos" if isinstance(antes[k], list) else f"{sorted(antes[k])}"
    print(f"{k:10s} {'IGUAL' if igual else 'DIFIERE'} ({detalle})")
    if not igual:
        print("  antes:  ", json.dumps(antes[k], sort_keys=True)[:1500])
        print("  después:", json.dumps(despues[k], sort_keys=True)[:1500])
print(f"certificados emitidos: antes {len(antes['certs'])}, después {len(despues['certs'])}")
sys.exit(1 if mal else 0)
