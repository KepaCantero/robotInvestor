"""QA r01 de T-187: muestreo reproducible (semilla de texto) de NO_VERIFICABLE y CORRECTA para contrastarlas a mano.

Uso: python3 -I r01_02_muestreo.py <carpeta del ticket> <veredicto> <n>
"""
import hashlib
import json
import sys
from pathlib import Path

t, ver, n = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
m = {a["id"]: a for a in json.loads((t / "muestra_afirmaciones.json").read_text(encoding="utf-8"))["afirmaciones"]}
v = {x["id"]: x for f in sorted((t / "veredictos").glob("lote_*.json"))
     for x in json.loads(f.read_text(encoding="utf-8"))["veredictos"]}
ids = sorted((i for i in v if v[i]["veredicto"] == ver), key=lambda i: hashlib.sha256(f"QA r01 T-187 {i}".encode()).hexdigest())
for i in ids[:n]:
    a = m[i]
    print(f"## {i} · {a['agente']} · {a['subarea'] or a['seccion']} l.{a['linea']}\nFRASE: {a['texto']}\nNOTA: {v[i]['nota']}\n")
