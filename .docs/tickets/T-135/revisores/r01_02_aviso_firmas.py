"""QA r01 de T-135 · el aviso de un dato movido (T-127 H-06 y H-07) y una vía de los precios de IDX-CONC-001.

 T. CHR-TOKEN-001: un token de oferta fija y entera en circulación (circulante = total = máxima) y una copia suya con UN
    dato de entrada movido ±4 % (cada uno por turno), con y sin staking y concentración. La firma del aviso deja en ``None``
    la total que repite la circulante: ¿mover la circulante convierte un dato movido en dos?
 N. REI-NAV-001: la sociedad A en dos partes con cada dato de entrada movido por turno, con y sin `otros_pasivos`.
 Z. IDX-CONC-001: un precio 0 (o negativo) en la misma fecha de un valor y de su copia, por `valores["precios"]`.
Uso: python -I .docs/tickets/T-135/revisores/r01_02_aviso_firmas.py bloque_a/11_Ejecutor
"""
import copy
import sys
import warnings
from pathlib import Path

EJE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJE))
import numpy as np
import pandas as pd
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import fichas_p2 as fp
from bloque_a.motor import fichas_reales as fr
from bloque_a.motor.operaciones import ErrorFicha

warnings.simplefilter("ignore", RuntimeWarning)
AVISO = "aviso (1.6)"
ok, hallazgos = 0, []


def comprobar(nombre, cond, detalle=""):
    global ok
    if cond:
        ok += 1
        print(f"  ok        {nombre}")
    else:
        hallazgos.append(nombre)
        print(f"  HALLAZGO  {nombre} · {detalle}")


def correr(mod, ficha, v, p):
    return mod.FICHAS[ficha]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(p or {}))


def caso(mod, ficha, i):
    v = {}
    for d in mod.CASOS_CONTROL[ficha][i]["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v, dict(mod.CASOS_CONTROL[ficha][i].get("parametros") or {})


def resultado(mod, ficha, v, p):
    try:
        _, lim = correr(mod, ficha, v, p)
    except ErrorFicha as e:
        return "R", str(e)[:90]
    return "S", len([x for x in lim if x.startswith(AVISO)])


# ------------------------------------------------------------------ T: CHR-TOKEN-001
print("[T] CHR-TOKEN-001: token de oferta fija y entera en circulación y una copia con un dato movido ±4 %")
for staking in (False, True):
    for campo, f in (("precio", 1.04), ("oferta_circulante", 0.96), ("oferta_total", 1.04), ("oferta_maxima", 1.04),
                     ("emision_anual", None), ("quema_anual", None)):
        v, p = caso(fp, "CHR-TOKEN-001", 1)
        base = copy.deepcopy(v["tokens"][0])
        base.update(id="FIJO", precio=3.3, oferta_circulante=4.2e8, oferta_total=4.2e8, oferta_maxima=4.2e8,
                    emision_anual=0.0, quema_anual=0.0, calendario={"fuente": "documentación", "desbloqueos": []})
        base.pop("staking_nominal", None)
        base.pop("concentracion_10_mayores", None)
        if staking:
            base.update(staking_nominal=0.037, concentracion_10_mayores=0.28)
        c = copy.deepcopy(base)
        c["id"] = "COPIA_SECRETA"
        if campo == "oferta_total":
            c["oferta_total"] = c["oferta_maxima"] = base["oferta_total"] * f     # la máxima ≥ total
        elif f is None:
            c[campo] = 1.2e6                                                       # de 0 a un valor
        else:
            c[campo] = base[campo] * f
        v["tokens"] += [base, c]
        st, av = resultado(fp, "CHR-TOKEN-001", v, p)
        print(f"    staking {'sí' if staking else 'no'} · {campo} movido: {st} · {av}")
        if campo in ("oferta_circulante",):
            comprobar(f"T: staking {'sí' if staking else 'no'}: copia con la oferta circulante −4 % da el aviso (antes de "
                      f"T-135 lo daba)", st == "R" or av >= 1, f"{st} {av}")
        elif campo in ("oferta_total", "oferta_maxima", "emision_anual", "quema_anual") or staking:
            comprobar(f"T: staking {'sí' if staking else 'no'}: copia con «{campo}» movido da el aviso o se rechaza",
                      st == "R" or av >= 1, f"{st} {av}")

# ------------------------------------------------------------------ N: REI-NAV-001
print("[N] REI-NAV-001: A en dos partes con un dato movido ±4 %")
for quitar in (True, False):
    for campo in ("nav_por_accion", "precio", "deuda_neta", "cap_rate_tasacion", "otros_pasivos", "gav"):
        if quitar and campo == "otros_pasivos":
            continue
        v, p = caso(fr, "REI-NAV-001", 2)
        a = v["componentes"][0]
        partes = []
        for j, s in enumerate((0.04, -0.04)):
            c = copy.deepcopy(a)
            c.update(id=f"PARTE_SECRETA_{j}", acciones=a["acciones"] / 2, deuda_neta=a["deuda_neta"] / 2, gav=a["gav"] / 2)
            if "otros_pasivos" in a:
                c["otros_pasivos"] = a["otros_pasivos"] / 2
            c[campo] = c[campo] / (1 + s)
            if quitar:
                c.pop("otros_pasivos", None)
            elif campo != "gav":                          # la identidad fija el GAV con otros pasivos
                c["gav"] = c["nav_por_accion"] * c["acciones"] + c["deuda_neta"] + c["otros_pasivos"]
            elif campo == "gav":
                c["otros_pasivos"] = c["gav"] - c["nav_por_accion"] * c["acciones"] - c["deuda_neta"]
            partes.append(c)
        v["componentes"] = partes
        st, av = resultado(fr, "REI-NAV-001", v, p)
        print(f"    {'sin' if quitar else 'con'} otros_pasivos · {campo} movido: {st} · {av}")
        comprobar(f"N: {'sin' if quitar else 'con'} otros_pasivos, «{campo}» movido: aviso o rechazo", st == "R" or av >= 1,
                  f"{st} {av}")

# ------------------------------------------------------------------ Z: IDX-CONC-001 con un precio 0
print("[Z] IDX-CONC-001: un precio no positivo por valores[precios]")
fechas = pd.bdate_range("2025-06-02", periods=320)
rng = np.random.default_rng(7)
A = 100 * np.exp(np.cumsum(rng.normal(0.0005, 0.01, len(fechas))))
for malo in (0.0, -1.0):
    precios = {}
    for k_, esc in (("C00", 1.0), ("SECRETA", 2.0)):
        precios[k_] = [{"fecha": str(d.date()), "precio": (malo if i == 100 else float(x) * esc)}
                       for i, (d, x) in enumerate(zip(fechas, A))]
    v = {"composicion": fm._composicion(10, igual=False), "precios": precios}
    try:
        res, lim = fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {"top_n": 5})
        amp = res["amplitud"]
        print(f"    precio {malo} en la sesión 100 de A y de su copia ×2: servida · amplitud "
              f"{None if amp is None else amp['porcentaje_sobre_media']}")
        comprobar(f"Z: precio {malo} en A y su copia: rechazo o amplitud null", amp is None, str(amp))
    except ErrorFicha as e:
        comprobar(f"Z: precio {malo} en A y su copia: rechazo o amplitud null", True, str(e)[:80])

print(f"\n== r01_02 T-135 aviso y firmas: {ok} ok · {len(hallazgos)} hallazgo(s): {'; '.join(hallazgos) or 'ninguno'}")
