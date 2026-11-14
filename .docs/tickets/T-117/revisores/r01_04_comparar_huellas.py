"""QA r01 de T-117 · Compara dos o más salidas de r01_03_ciclo_huella.py. Uso: python <este fichero> a.json b.json [...]"""
import json
import sys

def difs(x, y, p=""):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            yield from difs(x.get(k), y.get(k), f"{p}/{k}")
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for i, (u, v) in enumerate(zip(x, y)):
            yield from difs(u, v, f"{p}[{i}]")
    elif x != y:
        yield f"{p}: {str(x)[:70]!r} | {str(y)[:70]!r}"


datos = [json.load(open(f, encoding="utf-8")) for f in sys.argv[1:]]
ref = datos[0]
for nombre, d in zip(sys.argv[2:], datos[1:]):
    iguales = all(ref[k] == d[k] for k in ref if k != "codigo")
    if ref["resultado_norm"] != d["resultado_norm"]:
        print("  resultado devuelto, primeras diferencias: " + " ;; ".join(list(difs(ref["resultado_norm"], d["resultado_norm"]))[:4]))
    dif = sorted(k for k in set(ref["ficheros"]) | set(d["ficheros"]) if ref["ficheros"].get(k) != d["ficheros"].get(k))
    print(f"{sys.argv[1].split('/')[-1]} ({ref['codigo']}, {ref['diseno']}, {ref['estado']}, {ref['n_ficheros']} ficheros) frente a "
          f"{nombre.split('/')[-1]} ({d['codigo']}, {d['diseno']}): {'IGUALES' if iguales else 'DISTINTOS'}"
          + ("" if iguales else f" · ficheros distintos: {dif} · gc1 {ref['gc1']} / {d['gc1']} · top {ref['top'] == d['top']}"))
