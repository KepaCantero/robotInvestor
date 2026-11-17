"""QA r01 de T-173: ataques propios a la degradación DM-HLN (PB-50) y a la publicación EH5- (PB-64).
Uso (desde bloque_a/11_Ejecutor): python ../../.docs/tickets/T-173/revisores/r01_ataques.py"""
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


def sembrar(a, clase, h, n, desde=1, emision=lambda i: pd.Timestamp("2025-01-06") + pd.Timedelta(days=7 * i),
            resol=lambda i: "2026-05-29", o=lambda i: int(i % 3 == 0), p=0.85, ref=0.5):
    for i in range(n):
        pid = f"PRG-2025-{desde + i:04d}"
        a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-QA", "clase": clase, "horizonte": h,
                                   "prob_interna": p, "sentido": "POSITIVO", "en_informe": True,
                                   "fecha_emision": str(pd.Timestamp(emision(i)).date()), "fecha_resolucion": resol(i),
                                   "referencia_ingenua": {"valor_o_prob": ref}, "estado": "ABIERTO"})
        a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                   "resolucion": {"resultado_binario": o(i), "comprobacion_fuga": "SUPERADA",
                                                  "valor_observado": 0.01, "fecha_resuelto": resol(i)}})


# 1. DM-HLN a mano: 35 PRG, p = 0,85, ref = 0,5, aciertan 12 (i % 3 == 0)
a, e = nuevo(); sembrar(a, "RF", "H2", 35)
c = e.degradacion_dm("2026-06-05")["RF|H2"]
oo = np.array([int(i % 3 == 0) for i in range(35)], float)
d = (0.5 - oo) ** 2 - (0.85 - oo) ** 2
n = 35; dbar = d.mean(); var = np.mean((d - dbar) ** 2) / n
est = dbar / math.sqrt(var) * math.sqrt((n + 1 - 2 + 0) / n)
p = stats.t.cdf(est, n - 1)
R["1_dm_a_mano"] = {"dbar": round(dbar, 6), "est_mano": round(est, 4), "est_codigo": round(c["dm_hln"]["estadistico"], 4),
                    "p_mano": p, "p_codigo": c["dm_hln"]["p_valor"], "coincide": abs(p - c["dm_hln"]["p_valor"]) < 1e-12}

# 2. Lado: el pronóstico gana con significación -> p unilateral ~ 1, no degrada
a, e = nuevo(); sembrar(a, "RF", "H2", 35, o=lambda i: int(i % 10 != 0))
c = e.degradacion_dm("2026-06-05")["RF|H2"]
R["2_gana"] = {"p": c["dm_hln"]["p_valor"], "degradar": c["degradar"]}

# 3. Empate exacto (pronóstico = referencia): var = 0 -> p = 0,5, no degrada
a, e = nuevo(); sembrar(a, "RF", "H2", 35, p=0.5)
R["3_empate"] = e.degradacion_dm("2026-06-05")["RF|H2"]["degradar"]

# 4. UNA sola semana mala: 30 PRG de RF×H2 emitidos el mismo día y resueltos el mismo día (un solo conglomerado PA-03)
a, e = nuevo(); sembrar(a, "RF", "H2", 30, emision=lambda i: "2026-05-15", resol=lambda i: "2026-05-29")
c = e.degradacion_dm("2026-06-05")["RF|H2"]
hechos = e.aplicar_degradacion_dm("2026-06-05")
R["4_una_semana_mala"] = {"n": c["n"], "p": c["dm_hln"]["p_valor"], "degradar": c["degradar"], "degradada": len(hechos) == 1,
                          "conglomerados_PA03": len({"2026-05-29"})}

# 4b. Historia buena larga (60 semanas ganando) + una semana mala de 30 PRG
a, e = nuevo(); sembrar(a, "RF", "H2", 60, o=lambda i: int(i % 10 != 0))
sembrar(a, "RF", "H2", 30, desde=500, emision=lambda i: "2026-05-15", resol=lambda i: "2026-05-29", o=lambda i: 0)
c = e.degradacion_dm("2026-06-05")["RF|H2"]
R["4b_historia_buena_mas_semana_mala"] = {"n": c["n"], "brier": round(c["brier"], 4), "brier_ref": round(c["brier_ref"], 4),
                                          "p": c["dm_hln"]["p_valor"], "degradar": c["degradar"]}

# 5. Trimestres: fin de año y hora dentro del día
a, e = nuevo("2026-12-31"); sembrar(a, "RF", "H2", 35)
h1 = e.aplicar_degradacion_dm("2026-12-31 23:59")
R["5_trimestre_fin_de_anio"] = h1[0]["trimestre"] if h1 else None

# 6. Restitución tipo 3 en T1 tras degradar en T4 del año anterior: debe poder bajar en T1
import copy  # noqa: E402
a.reloj.fijar("2027-01-04")
m = copy.deepcopy(a.estado("F10")["P-31"]["valor_vigente"]); m["RF"]["H2"] = "SI"
a.escribir("F10", "AG-20", {"tipo_entrada": "CFG", "cfg_id": "CFG-T3-QA", "param_id": "P-31", "autor": "AG-20", "de": None, "a": m,
                            "valor_vigente": m, "regimen": "OPERADOR", "motivo": "tipo 3", "fecha_registro": "2027-01-04",
                            "fecha_efecto": "2027-01-04", "revierte_a": None})
h2 = e.aplicar_degradacion_dm("2027-01-04")
R["6_restituida_trimestre_nuevo"] = [(x["trimestre"], x["de"], x["a"]) for x in h2]
R["6_p30"] = a.estado("F10")["P-30"]["valor_vigente"]

# 7. Idempotencia: dos llamadas el mismo día
a, e = nuevo(); sembrar(a, "RF", "H2", 35)
R["7_idempotente"] = (len(e.aplicar_degradacion_dm("2026-06-05")), len(e.aplicar_degradacion_dm("2026-06-05")))

# 8. Un PRG con referencia None en OTRA celda: ¿bloquea la degradación de RF×H2?
a, e = nuevo(); sembrar(a, "RF", "H2", 35)
sembrar(a, "RV", "H3", 1, desde=900, ref=None)
try:
    R["8_ref_none_otra_celda"] = len(e.aplicar_degradacion_dm("2026-06-05"))
except Exception as ex:  # noqa: BLE001
    R["8_ref_none_otra_celda"] = f"EXCEPCION {type(ex).__name__}: {ex}"

# 9. NaN / inf en la probabilidad
for etq, val in (("nan", float("nan")), ("inf", float("inf"))):
    a, e = nuevo(); sembrar(a, "RF", "H2", 35, p=val)
    try:
        R[f"9_prob_{etq}"] = e.degradacion_dm("2026-06-05")["RF|H2"]["degradar"]
    except Exception as ex:  # noqa: BLE001
        R[f"9_prob_{etq}"] = f"EXCEPCION {type(ex).__name__}"

# 10. Fallo a mitad: la escritura del CFG de P-31 en F10 falla
a, e = nuevo(); sembrar(a, "RF", "H2", 35)
orig = a.escribir
def roto(archivo, autor, entrada):
    if archivo == "F10":
        raise OSError("disco lleno (simulado)")
    return orig(archivo, autor, entrada)
a.escribir = roto
try:
    e.aplicar_degradacion_dm("2026-06-05")
except OSError:
    pass
a.escribir = orig
aju = [x for x in a.leer("F6") if x.get("tipo_entrada") == "AJU" and x.get("parametro") == "P-31"]
R["10_fallo_f10"] = {"aju_en_f6": [(x["id"], x["estado"], x["aplicado_en_produccion"]) for x in aju],
                     "p31_en_f10": "P-31" in a.estado("F10")}
a.reloj.fijar("2026-06-12")
R["10_reintento_misma_trimestre"] = len(e.aplicar_degradacion_dm("2026-06-12"))
R["10_p31_en_f10_tras_reintento"] = "P-31" in a.estado("F10")

# 11. EH5 dos veces el mismo día
sys.path.insert(0, "tests"); sys.path.insert(0, ".")
import test_t173 as t  # noqa: E402
a, e = nuevo(); t._sembrar_h5(a)
e.publicar_estados_h5("2026-06-05"); e.publicar_estados_h5("2026-06-05")
R["11_eh5_mismo_dia"] = [x["id"] for x in a.leer("F6") if x.get("tipo_entrada") == "EH5"]

for k, v in R.items():
    print(k, "=>", v)

# 12. Contraste PA-03 de los casos 4 y 4b: n_eff (Kish) y DM-HLN sobre la media por conglomerado de fecha
from bloque_a.motor import evaluacion as ev  # noqa: E402
for etq, prep in (("4", lambda a: sembrar(a, "RF", "H2", 30, emision=lambda i: "2026-05-15", resol=lambda i: "2026-05-29")),
                  ("4b", lambda a: (sembrar(a, "RF", "H2", 60, o=lambda i: int(i % 10 != 0),
                                           resol=lambda i: str((pd.Timestamp("2025-03-03") + pd.Timedelta(days=7 * i)).date())),
                                    sembrar(a, "RF", "H2", 30, desde=500, emision=lambda i: "2026-05-15",
                                           resol=lambda i: "2026-05-29", o=lambda i: 0)))):
    a, e = nuevo(); prep(a)
    lst = sorted(e.resueltos("2026-06-05"), key=lambda x: (x["fecha_emision"], x["prg_id"]))
    fe = e._fechas_conglomerado(lst)
    pp = np.array([x["prob_interna"] for x in lst]); oo = np.array([x["resolucion"]["resultado_binario"] for x in lst], float)
    pr = np.array([x["referencia_ingenua"]["valor_o_prob"] for x in lst])
    ne = ev.n_efectiva(fe, oo - pp)
    df = pd.DataFrame({"f": fe, "d": (pr - oo) ** 2 - (pp - oo) ** 2}).groupby("f")["d"].mean()
    dmc = ev.diebold_mariano_hln(df.to_numpy(), np.zeros(len(df)), 1)
    R[f"12_{etq}_pa03"] = {"n": len(lst), "conglomerados": ne["conglomerados"], "n_eff": round(ne["n_eff"], 1),
                           "p_dm_por_conglomerado": dmc["p_unilateral"], "degrada_hoy": e.degradacion_dm("2026-06-05")["RF|H2"]["degradar"]}
    print(f"12_{etq}_pa03 =>", R[f"12_{etq}_pa03"])
