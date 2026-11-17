"""QA r02 de T-173: ataques propios a la r02 (DM por conglomerado, revisión mensual RDM-, Holm, reversión transaccional).
Uso (desde bloque_a/11_Ejecutor): PYTHONPATH=. python ../../.docs/tickets/T-173/revisores/r02_ataques.py"""
import copy
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, "tests"); sys.path.insert(0, ".")
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.evaluador import Evaluador  # noqa: E402
from conftest import config_pruebas  # noqa: E402

CFG = config_pruebas(evaluacion={"bootstrap_replicas": 50, "simulaciones_ece": 50})
R = {}


def nuevo(fecha="2026-06-05"):
    a = Almacen(Path(tempfile.mkdtemp()) / "estado")
    a.reloj.fijar(fecha)
    return a, Evaluador(a, None, None, CFG, None)


def sembrar(a, clase, h, filas, desde=1):
    """filas: lista de (fecha_resolucion, p, o)."""
    for i, (fr, p, o) in enumerate(filas):
        pid = f"PRG-2025-{desde + i:04d}"
        a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-QA", "clase": clase, "horizonte": h,
                                   "prob_interna": p, "sentido": "POSITIVO", "en_informe": True,
                                   "fecha_emision": str((pd.Timestamp(fr) - pd.Timedelta(days=14)).date()), "fecha_resolucion": fr,
                                   "referencia_ingenua": {"valor_o_prob": 0.5}, "estado": "ABIERTO"})
        a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                   "resolucion": {"resultado_binario": o, "comprobacion_fuga": "SUPERADA",
                                                  "valor_observado": 0.01, "fecha_resuelto": fr}})


def malo(n_fechas=15, por_fecha=4, inicio="2025-03-07", desde=1):
    """Dice 0,8 y acierta 1 de cada 4 (pierde), con distinta suerte por fecha. Fechas en orden NO cronológico al sembrar."""
    fechas = [str((pd.Timestamp(inicio) + pd.Timedelta(days=7 * k)).date()) for k in range(n_fechas)][::-1]
    return [(f, 0.8, int((k * por_fecha + j) % 4 == 0 or (k % 5 == 0 and j == 1))) for k, f in enumerate(fechas)
            for j in range(por_fecha)]


# 1. DM-HLN sobre medias por fecha, a mano (h = 1), con 4 PRG por fecha y la siembra en orden inverso
a, e = nuevo(); filas = malo(); sembrar(a, "RF", "H2", filas)
c = e.degradacion_dm("2026-06-05")["RF|H2"]
df = pd.DataFrame(filas, columns=["f", "p", "o"])
df["d"] = (0.5 - df.o) ** 2 - (df.p - df.o) ** 2
d = df.groupby("f")["d"].mean().sort_index().to_numpy()
k = len(d); dbar = d.mean(); var = np.mean((d - dbar) ** 2) / k
est = dbar / math.sqrt(var) * math.sqrt((k + 1 - 2) / k)
p = stats.t.cdf(est, k - 1)
R["1_dm_por_fecha"] = {"k": k, "dbar": round(dbar, 6), "est_mano": round(est, 5), "est_codigo": round(c["dm_hln"]["estadistico"], 5),
                       "p_mano": p, "p_codigo": c["dm_hln"]["p_valor"], "coincide": abs(p - c["dm_hln"]["p_valor"]) < 1e-12,
                       "n_eff": round(c["n_eff"], 2), "conglomerados": c["conglomerados"], "degradar": c["degradar"],
                       "umbral_holm": c["umbral_holm"]}

# 1b. Con h = 2 el orden importa: la serie del código debe ser la cronológica
from bloque_a.motor import evaluacion as ev  # noqa: E402
R["1b_orden_cronologico"] = (ev.diebold_mariano_hln(d.tolist(), [0.0] * k, 2)["p_unilateral"],
                             ev.diebold_mariano_hln(df.groupby("f", sort=False)["d"].mean().tolist(), [0.0] * k, 2)["p_unilateral"])

# 2. Revisión mensual: dos C5 en junio, uno el 30-06 y otro el 01-07
a, e = nuevo(); sembrar(a, "RF", "H2", malo())
r = [len(e.aplicar_degradacion_dm("2026-06-05"))]
a.reloj.fijar("2026-06-30"); r.append(len(e.aplicar_degradacion_dm("2026-06-30")))
rdm = sorted(x["id"] for x in a.leer("F6") if x.get("tipo_entrada") == "REVISION_DM")
R["2_mes"] = {"degradaciones": r, "rdm": rdm}
a.reloj.fijar("2026-07-01"); e.aplicar_degradacion_dm("2026-07-01")
R["2_cambio_de_mes_rdm"] = sorted(x["id"] for x in a.leer("F6") if x.get("tipo_entrada") == "REVISION_DM")
a.reloj.fijar("2027-01-04"); e.aplicar_degradacion_dm("2027-01-04")
R["2_cambio_de_anio_rdm"] = sorted(x["id"] for x in a.leer("F6") if x.get("tipo_entrada") == "REVISION_DM")[-1]

# 3. La revisión falla en el primer C5 del mes: no hay RDM y el siguiente C5 del mes la repite y degrada
a, e = nuevo(); sembrar(a, "RF", "H2", malo())
orig = e.degradacion_dm
e.degradacion_dm = lambda *x, **k: (_ for _ in ()).throw(RuntimeError("roto"))
res = e.ciclo("2026-06-05")
e.degradacion_dm = orig
sin_rdm = not [x for x in a.leer("F6") if x.get("tipo_entrada") == "REVISION_DM"]
a.reloj.fijar("2026-06-12")
R["3_fallo_y_repeticion"] = {"dm_primer_c5": res["degradacion_dm"], "sin_rdm_tras_fallo": sin_rdm,
                             "segundo_c5": [(x["celda"]["horizonte"], x["a"]) for x in e.aplicar_degradacion_dm("2026-06-12")]}

# 4. Backtest con saltos: C5 en mayo y luego en agosto (sin junio ni julio): agosto revisa
a, e = nuevo("2026-05-29"); sembrar(a, "RF", "H2", malo(n_fechas=8))      # aún sin muestra
e.aplicar_degradacion_dm("2026-05-29")
sembrar(a, "RF", "H2", malo(n_fechas=10, inicio="2025-06-06"), desde=500)
a.reloj.fijar("2026-08-07")
R["4_salto_de_meses"] = {"agosto": len(e.aplicar_degradacion_dm("2026-08-07")),
                         "rdm": sorted(x["id"] for x in a.leer("F6") if x.get("tipo_entrada") == "REVISION_DM")}

# 5. Reloj por delante del as_of: C5 con as_of 2026-06-05 dos veces con el reloj en 2026-06-20
a, e = nuevo("2026-06-20"); sembrar(a, "RF", "H2", malo())
R["5_reloj_adelantado"] = (len(e.aplicar_degradacion_dm("2026-06-05")), len(e.aplicar_degradacion_dm("2026-06-05")),
                           len([x for x in a.leer("F6") if x.get("tipo_entrada") == "AJU"]))

# 6. Reversión: falla el CFG de P-30 -> sin huérfanos; el reintento degrada una sola vez
a, e = nuevo(); sembrar(a, "RF", "H2", malo())
ow = a.escribir
def roto30(arch, aut, ent):
    if arch == "F10" and ent.get("param_id") == "P-30":
        raise OSError("disco lleno (simulado)")
    return ow(arch, aut, ent)
a.escribir = roto30
try:
    e.aplicar_degradacion_dm("2026-06-05"); R["6_excepcion"] = False
except OSError:
    R["6_excepcion"] = True
a.escribir = ow
f10 = a.leer("F10"); f6 = a.leer("F6")
R["6_tras_fallo"] = {"f10": [(x["param_id"], x.get("revierte_a"), x["valor_vigente"]["RF"]["H2"] if x["param_id"] == "P-31" else x["valor_vigente"],
                              x["methodology_version"]) for x in f10 if x.get("tipo_entrada") == "CFG"],
                     "p31_vigente": a.estado("F10")["P-31"]["valor_vigente"]["RF"]["H2"], "p30_en_f10": "P-30" in a.estado("F10"),
                     "aju_vigente": {k: v.get("estado") for k, v in a.estado("F6", clave="id").items() if k.startswith("AJU")},
                     "rdm": [x["id"] for x in f6 if x.get("tipo_entrada") == "REVISION_DM"]}
a.reloj.fijar("2026-06-12")
h = e.aplicar_degradacion_dm("2026-06-12")
R["6_reintento"] = {"n": len(h), "p31": a.estado("F10")["P-31"]["valor_vigente"]["RF"]["H2"], "p30": a.estado("F10")["P-30"]["valor_vigente"],
                    "integridad": all(a.verificar_integridad().values())}

# 7. Doble fallo: falla F10 y también la escritura del ANULADO en F6
a, e = nuevo(); sembrar(a, "RF", "H2", malo())
ow = a.escribir                                   # el escribir de ESTE almacén
def roto_todo(arch, aut, ent):
    if arch == "F10" or (arch == "F6" and ent.get("estado") == "ANULADO"):
        raise OSError("disco lleno (simulado)")
    return ow(arch, aut, ent)
a.escribir = roto_todo
try:
    e.aplicar_degradacion_dm("2026-06-05")
except OSError:
    pass
a.escribir = ow
R["7_doble_fallo"] = {k: v.get("estado") for k, v in a.estado("F6", clave="id").items() if k.startswith("AJU")}
a.reloj.fijar("2026-06-12")
R["7_reintento_mismo_trimestre"] = len(e.aplicar_degradacion_dm("2026-06-12"))

# 8. Holm escalonado con dos celdas: la de p mayor solo baja si la primera se rechaza
a, e = nuevo(); sembrar(a, "RF", "H2", malo()); sembrar(a, "RV", "H3", malo(), desde=700)
rev = e.degradacion_dm("2026-06-05")
R["8_holm_dos_celdas"] = {k: (round(v["dm_hln"]["p_valor"], 6), v["umbral_holm"], v["degradar"]) for k, v in rev.items()}

for k, v in R.items():
    print(k, "=>", v)
