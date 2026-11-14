"""QA r01 de T-118 · H-09: datos fechados después de la fecha de corte.

 1. ML-PRED-001 y ML-CAL-001 por Motor.servir: borde (el día del corte se sirve, el siguiente se rechaza), el corte con
    hora, formatos raros de la fecha de corte y de las fechas de los datos, zonas horarias.
 2. Barrido de las 56 fichas con caso de control: toda cadena con forma de fecha dentro de `valores`; con el corte en la
    víspera de la más tardía, ¿alguna sirve sin decir nada? (los vencimientos son posteriores por naturaleza: se listan).
 3. ML-CAL-001: fechas que no son texto (entero AAAAMMDD, epoch) — ¿burlan el corte?
Uso: .venv/bin/python -I r01_01_h09_fecha_corte.py
"""
import copy
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_01 H-09")
m = C.motor()


def estado(pet):
    r, exc, n = C.servir_contando(m, pet)
    if exc is not None:
        return f"EXCEPCION {type(exc).__name__}: {str(exc)[:120]}", n
    return ("SERVIDO" if str(r["estado"]).startswith("SERVED") else f"RECHAZADO · {r['detalle'][:110]}"), n


# ------------------------------------------------------------------ 1
print("[1] ML-PRED-001: borde y formatos de la fecha de corte (última fecha de los datos: 2020-08-10)")
esperado = {
    "2020-08-09": "R", "2020-08-10": "S", "2020-08-11": "S", "2020-08-10T00:00:00": "S", "2020-08-10 23:59:59": "S",
    "2020-08-09T23:59:59.999999": "R", "20200810": "S", "20200809": "R", "2020/08/10": "S", "10/08/2020": "?", "08/09/2020": "?",
    "2020-08-10T00:00:00Z": "?", "2020-08-10T00:00:00+14:00": "?", "2020-08-09T23:00:00-05:00": "?", "2020-W33-1": "?",
    "2020-08": "R", "2020": "R", "0001-01-01": "R", "9999-12-31": "S", "1e10": "?", "": "?", "   ": "?", "nan": "?", "NaT": "?",
    "hoy": "?", "now": "?", "today": "?",
}
sirve_tarde = []
for corte, esp in esperado.items():
    e, n = estado(C.peticion("ML-PRED-001", fecha_corte=corte))
    s = "S" if e == "SERVIDO" else ("X" if e.startswith("EXCEPCION") else "R")
    print(f"    corte {corte!r:34} → {e[:150]}")
    if esp in "SR":
        K.comprobar(f"corte {corte!r}: {'se sirve' if esp == 'S' else 'se rechaza'}", s == esp and n == 1, e)
    else:
        K.comprobar(f"corte {corte!r} (formato raro): sin excepción y una entrada en RC", s != "X" and n == 1, e)
    if s == "S":
        try:
            t = pd.Timestamp(corte) if corte.strip() else None
            if t is not None and not pd.isna(t) and t.tz_localize(None).normalize() < pd.Timestamp("2020-08-10"):
                sirve_tarde.append(corte)
        except Exception:  # noqa: BLE001
            sirve_tarde.append(corte + " (ilegible y servido)")
K.comprobar("ningún corte anterior al 2020-08-10 (leído como lo lee pandas) sirve", not sirve_tarde, str(sirve_tarde))
for corte in (20200809, 1.0, True, ["2020-08-09"], {"a": 1}, np.datetime64("2020-08-09"), pd.Timestamp("2020-08-09"),
              __import__("datetime").date(2020, 8, 9)):
    e, n = estado(C.peticion("ML-PRED-001", fecha_corte=corte))
    print(f"    corte {corte!r:34} → {e[:150]}")
    K.comprobar(f"corte de tipo {type(corte).__name__}: sin excepción, una entrada en RC", not e.startswith("EXCEPCION") and n == 1, e)
    if type(corte).__name__ in ("datetime64", "Timestamp", "date"):
        K.comprobar(f"corte {type(corte).__name__} del 2020-08-09: no se sirve", e != "SERVIDO", e)

print("\n[1b] ML-PRED-001: fechas de los datos con hora y zona horaria (corte 2020-08-10)")


def pred_con(fechas_fn, cd_fn=None):
    pet = C.peticion("ML-PRED-001", fecha_corte="2020-08-10")
    v = pet["datos"][0]["valores"]
    f0 = list(v["fechas"])
    v["fechas"] = [fechas_fn(i, f) for i, f in enumerate(f0)]
    for d in v["variables"].values():
        d["conocible_desde"] = [(cd_fn or fechas_fn)(i, f) for i, f in enumerate(f0)]
    return pet


n = len(C.valores("ML-PRED-001")["fechas"])
casos = {
    "última fecha 2020-08-10T23:59:59 (mismo día)": (lambda i, f: f + "T23:59:59" if i == n - 1 else f, "S"),
    "última fecha 2020-08-11T00:00:00": (lambda i, f: "2020-08-11T00:00:00" if i == n - 1 else f, "R"),
    "todas con zona -05:00, la última 2020-08-10T23:00-05:00 (ya es día 11 en UTC)": (lambda i, f: f + "T23:00:00-05:00", "noS?"),
    "última 2020-08-11T00:30+14:00 (día 10 en UTC), el resto sin zona": (lambda i, f: "2020-08-11T00:30:00+14:00" if i == n - 1 else f, "R"),
    "todas +14:00, la última 2020-08-11T00:30+14:00": (lambda i, f: (f if i < n - 1 else "2020-08-11") + "T00:30:00+14:00", "R"),
    "última fecha 'NaT'": (lambda i, f: "NaT" if i == n - 1 else f, "R"),
    "última fecha '2020-08-10 ' con espacio": (lambda i, f: f + " " if i == n - 1 else f, "?"),
}
for nombre, (fn, esp) in casos.items():
    e, k = estado(pred_con(fn))
    print(f"    {nombre}: {e[:160]}")
    s = "S" if e == "SERVIDO" else ("X" if e.startswith("EXCEPCION") else "R")
    K.comprobar(nombre, k == 1 and s != "X" and (esp in ("?", "noS?") or s == esp), e)
# solo `conocible_desde` posterior
e, k = estado(pred_con(lambda i, f: f, lambda i, f: "2020-08-11" if i == n - 1 else f))
K.comprobar("solo conocible_desde posterior al corte: rechazado", e.startswith("RECHAZADO") and k == 1, e)

print("\n[1c] ML-CAL-001 por el Motor: pares fechados")
fechas = [str(d.date()) for d in pd.bdate_range("2024-01-01", periods=40)]
y = [0.1 * i + float(np.sin(i)) for i in range(40)]


def cal(fn=lambda f: f, corte=None, fpred=None):
    d = {"tipo": "nivel", "realizaciones": [{"fecha": fn(f), "valor": a} for f, a in zip(fechas, y)],
         "predicciones": [{"fecha": (fpred or fn)(f), "valor": a + 0.3} for f, a in zip(fechas, y)]}
    return {"operacion": "ML-CAL-001", "datos": [{"valores": {"ensayos": 1, "horizontes": {"H2": d}}}], "parametros": {},
            "fecha_corte": corte}


for nombre, pet, esp in (
        ("corte el último día", cal(corte=fechas[-1]), "S"),
        ("corte la víspera", cal(corte=fechas[-2]), "R"),
        ("corte la víspera a las 23:59:59", cal(corte=fechas[-2] + "T23:59:59"), "R"),
        ("sin corte", cal(), "S"),
        ("fechas con hora 23:59 y corte ese día", cal(lambda f: f + "T23:59:00", fechas[-1]), "S"),
        ("fechas con zona -10:00 a las 23:00 (día siguiente en UTC), corte ese día local", cal(lambda f: f + "T23:00:00-10:00", fechas[-1]), "?"),
        ("fechas como entero AAAAMMDD, corte la víspera", cal(lambda f: int(f.replace("-", "")), fechas[-2]), "noS"),
        ("fechas como epoch en segundos (float), corte la víspera", cal(lambda f: float(pd.Timestamp(f).timestamp()), fechas[-2]), "noS"),
        ("fechas como epoch en ns (int), corte la víspera", cal(lambda f: int(pd.Timestamp(f).value), fechas[-2]), "R"),
        ("fechas DD/MM/AAAA, corte la víspera", cal(lambda f: f"{f[8:10]}/{f[5:7]}/{f[0:4]}", fechas[-2]), "noS"),
        ("fecha None en un par", cal(lambda f: None if f == fechas[3] else f, fechas[-1]), "R"),
        ("año 10000", cal(lambda f: "10000-01-01" if f == fechas[-1] else f, fechas[-1]), "R")):
    e, k = estado(pet)
    print(f"    {nombre}: {e[:170]}")
    s = "S" if e == "SERVIDO" else ("X" if e.startswith("EXCEPCION") else "R")
    if esp == "noS":
        K.comprobar(f"ML-CAL-001 {nombre}: no se sirve un dato posterior al corte", s == "R" and k == 1, e)
    else:
        K.comprobar(f"ML-CAL-001 {nombre}", k == 1 and s != "X" and (esp == "?" or s == esp), e)

# ------------------------------------------------------------------ 2
print("\n[2] barrido: fechas en los `valores` de los casos de control de las fichas servibles")
RE_F = re.compile(r"^\d{4}-\d{2}-\d{2}")


def fechas_de(x, camino=""):
    if isinstance(x, dict):
        for k, v in x.items():
            if isinstance(k, str) and RE_F.match(k):
                yield camino + "/<clave>", k[:10]
            yield from fechas_de(v, f"{camino}/{k}" if not (isinstance(k, str) and RE_F.match(k)) else camino + "/<clave>")
    elif isinstance(x, list):
        for v in x:
            yield from fechas_de(v, camino + "[]")
    elif isinstance(x, str) and RE_F.match(x):
        yield camino, x[:10]


fichas = sorted(f for f in servicio.CASOS_CONTROL if servicio.servible(f))
sirven, con_fechas = [], 0
for f in fichas:
    for i, caso in enumerate(servicio.CASOS_CONTROL[f]):
        fs = [(c, d) for dd in caso.get("datos") or [] for c, d in fechas_de(dd.get("valores") or {})]
        if not fs:
            continue
        ultima = max(d for _, d in fs)
        base, _ = estado(C.peticion(f, i, fecha_corte=None))
        if base != "SERVIDO":
            continue
        con_fechas += 1
        vispera = str((pd.Timestamp(ultima) - pd.Timedelta(days=1)).date())
        e, k = estado(C.peticion(f, i, fecha_corte=vispera))
        if e == "SERVIDO":
            donde = sorted({c for c, d in fs if d > vispera})
            sirven.append((f, i, ultima, donde))
print(f"    casos servidos con alguna fecha en sus valores: {con_fechas}; se sirven con el corte en la víspera de la última: {len(sirven)}")
for f, i, u, donde in sirven:
    print(f"      {f} caso {i}: última {u} en {donde}")
del_grupo_r = [s for s in sirven if servicio.IMPLEMENTADAS[s[0]]["fn"].__module__.endswith("fichas_riesgo")]
K.comprobar("ninguna ficha del grupo R sirve con una fecha de sus datos posterior al corte", not del_grupo_r, str(del_grupo_r))
VENCIMIENTOS = ("vencimiento", "expir", "fecha_fin", "proxim", "pago", "cupon", "entrega", "liquidacion", "calendario", "futuro",
                "hasta", "objetivo", "evento")
dudosos = [s for s in sirven if not all(any(p in c.lower() for p in VENCIMIENTOS) for c in s[3])]
print(f"    de ellos, con campos que no parecen un vencimiento o una fecha futura por naturaleza: {[(s[0], s[1], s[3]) for s in dudosos]}")

sys.exit(K.fin())
