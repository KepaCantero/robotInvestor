"""QA r01 de T-121 · H-04: bordes de la fecha de corte en los tres módulos de la Fase 1 (zonas horarias, formatos de la fecha
de corte, eventos comparables con la efectividad posterior al corte).

Una ficha por módulo: MON-YLD-001 (fichas_mon_idx), TCV-CDS-001 (fichas_tcv) y FON-FLOW-001 (fichas_fon_der); en cada una se
cambia la ÚLTIMA fecha observada.
Uso: .venv/bin/python -I r01_03_h04_bordes.py
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import pandas as pd  # noqa: E402

K = C.Contador("r01_03 T-121 H-04 bordes")
m = C.motor()


def estado(pet):
    r, exc, n = C.servir_contando(m, pet)
    if exc is not None:
        return "X", f"{type(exc).__name__}: {exc}"[:150], n
    return ("S", r, n) if str(r["estado"]).startswith("SERVED") else ("R", r["detalle"][:150], n)


# (ficha, caso, función que devuelve el contenedor y la clave de la última fecha)
def ult_yld(v):
    s = v["instrumentos"][0] if "instrumentos" in v else None
    return s, "fecha"


FICHAS = {
    "MON-YLD-001": (1, lambda v: (v, "fecha", None)),
    "TCV-CDS-001": (0, lambda v: (v["historia"]["fechas"], -1, None)),
    "FON-FLOW-001": (0, lambda v: (v["fechas"], -1, None)),
}


def localizar_mon_yld(v):
    """La única fecha de MON-YLD-001#1 (búsqueda genérica)."""
    def rec(x):
        if isinstance(x, dict):
            for k, y in x.items():
                if isinstance(y, str) and len(y) >= 10 and y[4] == "-" and y[7] == "-":
                    return x, k
                r = rec(y)
                if r:
                    return r
        if isinstance(x, list):
            for y in x:
                r = rec(y)
                if r:
                    return r
        return None
    return rec(v)


def pet_con(ficha, i, nueva=None, corte=None):
    p = C.peticion(ficha, i, fecha_corte=corte)
    v = p["datos"][0]["valores"]
    if ficha == "MON-YLD-001":
        cont, k = localizar_mon_yld(v)
    elif ficha == "TCV-CDS-001":
        cont, k = v["historia"]["fechas"], -1
    else:
        cont, k = v["fechas"], -1
    actual = cont[k]
    if nueva is not None:
        cont[k] = nueva(actual[:10])
    return p, actual[:10]


def d(x, n):
    return str((pd.Timestamp(x) + pd.Timedelta(days=n)).date())


print("[1] zonas horarias y formatos (resultado por módulo)")
resumen = {}
for f, (i, _) in FICHAS.items():
    _, D = pet_con(f, i)
    casos = [
        ("dato D, corte D", None, D, "S"),
        ("dato D+1, corte D", lambda x: d(x, 1), D, "R"),
        ("dato DT23:59:59.999, corte D", lambda x: x + "T23:59:59.999", D, "S"),
        ("dato (D+1)T00:30+14:00 (día D en UTC), corte D", lambda x: d(x, 1) + "T00:30:00+14:00", D, "?"),
        ("dato DT23:00-05:00 (día D+1 en UTC), corte D", lambda x: x + "T23:00:00-05:00", D, "?"),
        ("dato D+1, corte DT23:00-05:00 (D+1 en UTC)", lambda x: d(x, 1), D + "T23:00:00-05:00", "?"),
        ("dato D+1, corte (D+1)T00:30+14:00 (día D en UTC)", lambda x: d(x, 1), d(D, 1) + "T00:30:00+14:00", "?"),
        ("dato D+1, corte int AAAAMMDD", lambda x: d(x, 1), int(D.replace("-", "")), "R"),
        ("dato D+1, corte D+1 con espacio final", lambda x: d(x, 1), d(D, 1) + " ", "?"),
        ("dato D+1, corte 'AAAAMMDD' de la víspera", lambda x: d(x, 1), D.replace("-", ""), "R"),
        ("dato D+1, corte True", lambda x: d(x, 1), True, "R"),
        ("dato D+1 sin corte en la petición (as_of del proveedor None)", lambda x: d(x, 1), None, "S"),
    ]
    for nombre, nueva, corte, esp in casos:
        p, _ = pet_con(f, i, nueva, corte)
        st, det, n = estado(p)
        resumen.setdefault(nombre, {})[f] = st
        print(f"    {f:13s} {nombre:52s} {st} {'' if st == 'S' else det}")
        K.comprobar(f"{f}: {nombre}", st != "X" and n == 1 and (esp == "?" or st == esp), f"{st} {det}")
print("\n  coherencia entre módulos (mismo veredicto en las tres):")
for nombre, por in resumen.items():
    if len(set(por.values())) > 1:
        print(f"    DISTINTO · {nombre}: {por}")

print("\n[2] IDX-REB-001: un evento comparable con anuncio y efectividad posteriores al corte (rentabilidades hasta el corte)")
base = C.peticion("IDX-REB-001", 2)
comps = base["datos"][0]["valores"]["eventos_comparables"]
D = max(r["fecha"] for c in comps for r in c["rentabilidades"])
D = max(D, base["datos"][0]["valores"]["evento"]["fecha_anuncio"], base["datos"][0]["valores"]["evento"]["activos_indexados"]["fecha"])
st0, r0, _ = estado(C.peticion("IDX-REB-001", 2, fecha_corte=D))
p = C.peticion("IDX-REB-001", 2, fecha_corte=D)
c = p["datos"][0]["valores"]["eventos_comparables"][-1]
c["fecha_anuncio"], c["fecha_efectividad"] = d(D, 1), d(D, 5)
st1, r1, _ = estado(p)
p2 = C.peticion("IDX-REB-001", 2, fecha_corte=D)
p2["datos"][0]["valores"]["eventos_comparables"].pop()
st2, r2, _ = estado(p2)
print(f"    base {st0} · comparable futuro {st1} · sin ese comparable {st2}")
if st1 == "S" and st2 == "S":
    e1 = json.dumps(r1["resultado"].get("estudio_eventos") or r1["resultado"].get("estudio"), sort_keys=True, default=str)
    e2 = json.dumps(r2["resultado"].get("estudio_eventos") or r2["resultado"].get("estudio"), sort_keys=True, default=str)
    print(f"    claves del resultado: {sorted(r1['resultado'])[:12]}")
    print(f"    limitaciones con el comparable futuro: {[x for x in r1['limitaciones'] if 'excluid' in x]}")
    K.comprobar("el comparable con efectividad posterior al corte no entra en el estudio (igual que quitarlo)", e1 == e2,
                f"{e1[:200]} != {e2[:200]}")
sys.exit(K.fin())
