"""QA r01 de T-187: recuento independiente del paso 3 desde los lotes (no usa el script del ticket).

Uso: python3 -I r01_01_recuento.py <carpeta del ticket> [--volcar]
Imprime los recuentos por lote y totales, los porcentajes con los dos denominadores y, con --volcar, la frase y la nota
de cada ERRONEA y de cada caso del comentario, para contrastar a mano la fidelidad de comentario.json.
"""
import collections
import json
import sys
from pathlib import Path

t = Path(sys.argv[1])
muestra = {a["id"]: a for a in json.loads((t / "muestra_afirmaciones.json").read_text(encoding="utf-8"))["afirmaciones"]}
vist: dict[str, dict] = {}
tot: collections.Counter = collections.Counter()
for f in sorted((t / "veredictos").glob("lote_*.json")):
    lote = json.loads(f.read_text(encoding="utf-8"))
    c = collections.Counter(v["veredicto"] for v in lote["veredictos"])
    print(f.name, dict(c), "n =", len(lote["veredictos"]))
    for v in lote["veredictos"]:
        assert v["id"] not in vist, ("repetido", v["id"])
        vist[v["id"]] = v | {"lote": lote["lote"]}
    tot += c
assert set(vist) == set(muestra), (set(muestra) ^ set(vist))
ver = tot["CORRECTA"] + tot["ERRONEA"]
print("total", dict(tot), f"verificables {ver}: {100*tot['CORRECTA']/ver:.2f} %; sobre 350: {100*tot['CORRECTA']/len(muestra):.2f} %")
por_prompt: dict = collections.defaultdict(collections.Counter)
for i, v in vist.items():
    por_prompt[muestra[i]["agente_id"]][v["veredicto"]] += 1
nv = sorted(((p, c["NO_VERIFICABLE"]) for p, c in por_prompt.items()), key=lambda x: -x[1])
print("NO_VERIFICABLE por prompt (mayores):", nv[:8])
if "--volcar" in sys.argv:
    com = json.loads((t / "veredictos" / "comentario.json").read_text(encoding="utf-8"))
    ids = [i for i, v in vist.items() if v["veredicto"] == "ERRONEA"] + list(com["dudosas"])
    for i in ids:
        a = muestra[i]
        print(f"\n## {i} [{vist[i]['veredicto']}] lote {vist[i]['lote']} · {a['agente']} l.{a['linea']}\nFRASE: {a['texto']}\nNOTA: {vist[i]['nota']}")
        if i in com["erratas"]:
            print("COMENTARIO.error:", com["erratas"][i]["error"], "\nCOMENTARIO.correccion:", com["erratas"][i]["correccion"])
        if i in com["dudosas"]:
            print("COMENTARIO.dudosa:", com["dudosas"][i])
