"""QA r01 de T-121 · H-04: fecha de corte en las 22 fichas de la Fase 1, campo a campo.

Para cada caso de control de IDX, FON, DER, MON y TCV:
  0. sin corte y con el corte en la fecha más tardía de sus `valores` (D): se sirve (y el mismo resultado);
  1. por cada patrón de ruta con fechas (índices de lista quitados), la aparición más tardía pasa a D + 1 día (se conserva el
     orden de las listas crecientes) con el corte en D: ¿se rechaza? Las que se sirven se listan para clasificarlas a mano
     (vencimientos, reuniones, efectividad anunciada… son futuras por naturaleza);
  2. la misma aparición a «D 23:59:59» con el corte en D: se sirve (el dato del día del corte es conocible) o se rechaza por
     otro motivo que no es la fecha de corte.
Uso: .venv/bin/python -I r01_01_h04_campo_a_campo.py [--fichas A,B]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import pandas as pd  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

RE_F = re.compile(r"^(\d{4}-\d{2}-\d{2})(.*)$")
FAMILIAS = ("IDX", "FON", "DER", "MON", "TCV")
sel = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--fichas=")), None)
fichas = [f for f in servicio.CASOS_CONTROL if f.split("-")[0] in FAMILIAS and (sel is None or f in sel)]
m = C.motor()


def fechas_de(x, ruta=()):
    """(ruta concreta, patrón, fecha AAAA-MM-DD, resto) de cada texto con forma de fecha (también claves)."""
    if isinstance(x, dict):
        for k, v in x.items():
            if isinstance(k, str) and RE_F.match(k):
                yield ruta + (("K", k),), tuple(p for p, _ in ruta) + ("<clave>",), k[:10], k[10:]
            yield from fechas_de(v, ruta + ((k, k),))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from fechas_de(v, ruta + (("[]", i),))
    elif isinstance(x, str):
        mm = RE_F.match(x)
        if mm:
            yield ruta, tuple(p for p, _ in ruta), mm.group(1), mm.group(2)


def poner(raiz, ruta, nuevo):
    x = raiz
    for _, k in ruta[:-1]:
        x = x[k]
    tipo, k = ruta[-1]
    if tipo == "K":   # renombrar una clave fecha
        x[nuevo] = x.pop(k)
    else:
        x[k] = nuevo


def estado(pet):
    r, exc, n = C.servir_contando(m, pet)
    if exc is not None:
        return "X", f"{type(exc).__name__}: {exc}"[:160], n
    if str(r["estado"]).startswith("SERVED"):
        return "S", r, n
    return "R", r["detalle"][:200], n


def es_corte(detalle):
    return "posterior a la fecha de corte" in detalle or "FUGA" in detalle or "corte" in detalle


fallos, servidos_futuros, escapes, no_corte_hora = [], {}, [], []
n_pruebas = 0
for f in fichas:
    for i, caso in enumerate(servicio.CASOS_CONTROL[f]):
        todas = [(j, r, p, d, rest) for j, dd in enumerate(caso.get("datos") or [])
                 for r, p, d, rest in fechas_de(dd.get("valores") or {})]
        if not todas:
            print(f"  {f}#{i}: sin fechas en valores")
            continue
        D = max(d for *_, d, _ in todas)
        s0, r0, _ = estado(C.peticion(f, i))
        sD, rD, _ = estado(C.peticion(f, i, fecha_corte=D))
        igual = s0 == "S" and sD == "S" and json.dumps(r0["resultado"], sort_keys=True, default=str) == json.dumps(rD["resultado"], sort_keys=True, default=str)
        print(f"  {f}#{i}: D={D} sin corte {s0} · corte D {sD} · mismo resultado {igual} · {len(todas)} fechas")
        if not igual:
            fallos.append((f, i, "base", s0, sD))
            continue
        D1 = str((pd.Timestamp(D) + pd.Timedelta(days=1)).date())
        patrones = {}
        for j, r, p, d, rest in todas:
            if (j, p) not in patrones or d >= patrones[(j, p)][2]:
                patrones[(j, p)] = (j, r, d, rest)
        for (j, p), (j_, r, d, rest) in sorted(patrones.items(), key=lambda t: str(t[0])):
            nombre = "/".join(str(x) for x in p)
            for nuevo, que in ((D1 + rest, "D+1"), (D + "T23:59:59", "D 23:59:59")):
                pet = C.peticion(f, i, fecha_corte=D)
                poner(pet["datos"][j]["valores"], r, nuevo if r[-1][0] != "K" else nuevo)
                st, det, n = estado(pet)
                n_pruebas += 1
                print(f"      {que:11s} {nombre[:70]:70s} {st} {(det if st != chr(83) else chr(32))[:110]}")
                if st == "X" or n != 1:
                    escapes.append((f, i, nombre, que, st, det, n))
                if que == "D+1" and st == "S":
                    servidos_futuros.setdefault(f, set()).add(nombre)
                if que == "D+1" and st == "R" and not es_corte(det):
                    pass
                if que == "D 23:59:59" and st == "R" and "posterior a la fecha de corte" in det:
                    no_corte_hora.append((f, i, nombre, det))

print(f"\n== pruebas: {n_pruebas}; casos base con distinto resultado o no servidos: {len(fallos)} {fallos}")
print(f"== escapes o RC != 1: {len(escapes)}")
for e in escapes[:20]:
    print("   ", e)
print(f"== día del corte con hora rechazado por la fecha de corte: {len(no_corte_hora)}")
for e in no_corte_hora[:20]:
    print("   ", e)
print("== rutas con una fecha posterior al corte que se SIRVEN (clasificar: ¿futura por naturaleza?):")
for f, s in sorted(servidos_futuros.items()):
    for nombre in sorted(s):
        print(f"   {f}: {nombre}")
