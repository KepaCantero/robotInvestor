"""QA r02 de T-106 · Entradas hostiles de punta a punta por el Motor (CT-09) y controles que una petición no debe relajar.

1. Umbrales de rechazo y rangos de parámetros que manda la ficha («Entradas mínimas», «Aclaración y rechazo»,
   «Parámetros» con rango) frente a una petición que los cambia en `parametros`: se prueban casos concretos en
   MON-EXP, MON-FIX, MON-REAL, IDX-ERP, IDX-CONC, IDX-REL e IDX-REB y, como contraste, TCV (UMBRALES fijos) y FON/DER
   (MINIMOS y RANGOS fuera de los parámetros). Un control que la petición puede bajar no es un control.
2. Peticiones mal formadas al Motor (datos, parámetros, plan, fecha de corte, operación): RECHAZADO y entrada en RC,
   o excepción al llamador.
3. Parámetros hostiles (NaN, ±inf, bool, texto, None, listas, dicts, negativos, 0, 1e308) en cada parámetro de cada una
   de las 21 fichas, por el Motor: ninguna excepción y ningún número no finito servido.
4. Cifras no finitas: política del Motor (rechazo en MON/IDX/FON/DER) frente a TCV (None con limitación).
5. MON-EXP-001: `precision_cotizacion` hostil y una curva suave servida con precisión declarada amplia; incertidumbre
   de la senda servida sin limitación.
6. Tamaños límite: tiempo por llamada con entradas grandes.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_03_ataques.py [RAIZ]
"""
from __future__ import annotations

import copy
import math
import shutil
import sys
import tempfile
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

M = C.preparar(sys.argv[1] if len(sys.argv) > 1 else None)
S, EF = M["servicio"], M["ErrorFicha"]
MI, FD, TC = M["mods"]
warnings.simplefilter("ignore")
TMP = Path(tempfile.mkdtemp(prefix="qa_r02_t106_at_"))
MO = C.motor(TMP)


def caso(ficha, i=0):
    c = S.CASOS_CONTROL[ficha][i]
    return C.entrada(c)["valores"], dict(c.get("parametros") or {})


def servir(ficha, valores, params):
    n = len(MO.almacen.leer("RC"))
    try:
        r = MO.servir({"operacion": ficha, "datos": [{"valores": valores}], "parametros": params,
                       "fecha_corte": "2026-11-12"}, "AG-21")
        return r, len(MO.almacen.leer("RC")) - n, None
    except Exception as e:  # noqa: BLE001
        return None, len(MO.almacen.leer("RC")) - n, f"{type(e).__name__}: {e}"[:160]


# ------------------------------------------------------------------ 1. umbrales y rangos que la petición no debe bajar
def recortar_historia(v, claves, n):
    for k in claves:
        v[k]["historia"] = v[k]["historia"][-n:]
    return v


v, p = caso("IDX-ERP-001")
v["historia_multiplo"] = v["historia_multiplo"][-24:]
pruebas = [
    ("IDX-ERP-001", "historia del múltiplo de 2 años (rechazo < 10)", copy.deepcopy(v), p, {"anios_historia_min": 1}),
]
v, p = caso("IDX-ERP-001")
v["rf"] = {**v["rf"], "plazo_anios": 3}
pruebas.append(("IDX-ERP-001", "N = 3 (rango 5–10)", v, {**p, "N": 3}, {"N_rango": [1, 100]}))
v, p = caso("IDX-ERP-001")
pruebas.append(("IDX-ERP-001", "λ = 2 (rango 0–1)", v, {**p, "lambda_reversion": 2}, {"lambda_reversion_rango": [-9, 9]}))
v, p = caso("IDX-REL-001")
pruebas.append(("IDX-REL-001", "historia común de 3 años (≥ 15; 10 con limitación)", recortar_historia(v, ("indice_a", "indice_b"), 36),
                p, {"anios_min": 1}))
v, p = caso("IDX-CONC-001")
pruebas.append(("IDX-CONC-001", "top_n = 1 (rango 5–50)", v, {**p, "top_n": 1}, {"top_n_rango": [0, 10 ** 6]}))
v, p = caso("MON-FIX-001")
pruebas.append(("MON-FIX-001", "T = 1 mes (rango 3–24)", v, {**p, "T_meses": 1}, {"T_meses_rango": [0, 600]}))
v, p = caso("MON-FIX-001")
v["curva"] = [v["curva"][0], v["curva"][-1]]   # 3 y 12 meses: dos nodos hasta T = 12 meses
pruebas.append(("MON-FIX-001", "dos nodos hasta T (≥ 3)", v, p, {"nodos_min": 1}))
v, p = caso("MON-EXP-001")
pruebas.append(("MON-EXP-001", "«≥ 3 nodos en 12 meses» (umbral subido a 99 por la petición)", v, p, {"nodos_min": 99}))
v, p = caso("MON-REAL-001")
pruebas.append(("MON-REAL-001", "historia exigida (≥ 10 años)", v, p, {"anios_min": 10 ** 6}))
for ficha, que, v, p, relaja in pruebas:
    r0, _, e0 = servir(ficha, copy.deepcopy(v), dict(p))
    r1, n_rc, e1 = servir(ficha, copy.deepcopy(v), {**p, **relaja})
    est0 = e0 or r0["estado"]
    est1 = e1 or r1["estado"]
    if ficha in ("MON-REAL-001", "MON-EXP-001"):   # aquí se sube el umbral: debe rechazar, y si rechaza es que el umbral es de la petición
        C.informe(f"{ficha}: {que}: el umbral no es un parámetro de la petición", est1 != "RECHAZADO" or est0 == "RECHAZADO",
                  f"defecto {est0} · con {relaja} → {est1}: la petición mueve el umbral")
        continue
    C.informe(f"{ficha}: {que}: la petición no relaja el control ({sorted(relaja)})",
              est0 == "RECHAZADO" and est1 == "RECHAZADO",
              f"defecto {est0} · con {relaja} → {est1}" + (f" ({r0['detalle'][:90]})" if r0 and est0 == "RECHAZADO" else ""))

# contraste: TCV rechaza los umbrales en la petición; FON/DER los ignoran (MINIMOS y RANGOS aparte)
v, p = caso("TCV-VIXTS-001")
r, _, e = servir("TCV-VIXTS-001", v, {**p, "vencimientos_minimos": 1})
C.informe("TCV: un umbral fijo en la petición se rechaza", r is not None and r["estado"] == "RECHAZADO", (e or r.get("detalle", ""))[:120])
v, p = caso("FON-DISC-001")
v["miembros"] = dict(list(v["miembros"].items())[:3])
r, _, e = servir("FON-DISC-001", v, {**p, "miembros": 1})
C.informe("FON: «≥ 5 miembros» no se baja por parámetro", r is not None and r["estado"] == "RECHAZADO", (e or r.get("detalle", ""))[:120])

# ------------------------------------------------------------------ 2. peticiones mal formadas
dat = S.CASOS_CONTROL["MON-YLD-001"][0]["datos"]
malas = {
    "datos = [5]": {"datos": [5]},
    "datos = [{'valores': 5}]": {"datos": [{"valores": 5}]},
    "datos = [{'valores': [1, 2]}]": {"datos": [{"valores": [1, 2]}]},
    "parametros = 'x'": {"datos": dat, "parametros": "x"},
    "parametros = [1, 2]": {"datos": dat, "parametros": [1, 2]},
    "plan = 'PLAN_X'": {"datos": dat, "plan": "PLAN_X"},
    "fecha_corte = 'mañana' con una serie": {"datos": [{"serie": "X", "fin": "2030-01-01"}], "fecha_corte": "mañana"},
    "operacion = {'ficha_id': ['x']}": {"operacion": {"ficha_id": ["x"]}},
}
for nombre, extra in malas.items():
    pet = {"operacion": "MON-YLD-001", "fecha_corte": "2026-11-12", **extra}
    n = len(MO.almacen.leer("RC"))
    try:
        r = MO.servir(pet, "AG-21")
        ok, det = r["estado"] == "RECHAZADO" and len(MO.almacen.leer("RC")) == n + 1, f"{r['estado']} {r.get('motivo')}"
    except Exception as exc:  # noqa: BLE001
        ok, det = False, f"excepción {type(exc).__name__}: {str(exc)[:90]} (sin entrada en RC)"
    C.informe(f"CT-09 con {nombre}: RECHAZADO registrado en RC", ok, det)

# ------------------------------------------------------------------ 3. parámetros hostiles en las 21
HOSTILES = [float("nan"), float("inf"), -float("inf"), True, "x", None, [], {}, [float("nan")], -1, 0, 1e308]
excepciones, no_finitos, n_llamadas = [], [], 0
defectos = {**MI.PARAMETROS_POR_DEFECTO, **FD.PARAMETROS_POR_DEFECTO, **TC.PARAMETROS_POR_DEFECTO}
for ficha in sorted(S.CASOS_CONTROL):
    v, p = caso(ficha)
    for clave in sorted(defectos[ficha]):
        for h in HOSTILES:
            n_llamadas += 1
            r, n_rc, e = servir(ficha, copy.deepcopy(v), {**p, clave: h})
            if e:
                excepciones.append(f"{ficha}.{clave}={h!r}: {e}")
            elif r["estado"] != "RECHAZADO" and S._no_finito(r["resultado"]):
                no_finitos.append(f"{ficha}.{clave}={h!r}")
            elif n_rc != 1:
                excepciones.append(f"{ficha}.{clave}={h!r}: {n_rc} entradas en RC")
C.informe(f"parámetros hostiles por el Motor ({n_llamadas} llamadas): sin excepciones y una entrada en RC por llamada",
          not excepciones, "; ".join(excepciones[:4]))
C.informe("parámetros hostiles: ningún número no finito servido", not no_finitos, "; ".join(no_finitos[:4]))

# ------------------------------------------------------------------ 4. cifras no finitas: TCV frente al resto
v, p = caso("TCV-VIXTS-001")
v["indices_plazo"] = {"VIX3M": 1e-320}
r, _, e = servir("TCV-VIXTS-001", v, p)
print(f"      (informativo) TCV-VIXTS-001 con VIX3M = 1e-320: {r['estado'] if r else e}; ratio spot/VIX3M = "
      f"{(r or {}).get('resultado', {}).get('ratios', {}).get('spot/VIX3M', '—')} (TCV sirve None con limitación; MON/IDX/FON/DER rechazan)")

# ------------------------------------------------------------------ 5. MON-EXP-001: precision_cotizacion
v, p = caso("MON-EXP-001", 1)
for prec in (float("nan"), -1e-6, "0.0001", True, 1.0):
    r, _, e = servir("MON-EXP-001", {**copy.deepcopy(v), "precision_cotizacion": prec}, p)
    C.informe(f"MON-EXP precision_cotizacion = {prec!r}: no sirve una senda relajada", r is not None and (
        r["estado"] == "RECHAZADO" or (r["resultado"]["verificacion"]["error_reproduccion_nodos_max"] <= 1e-10)),
        (e or f"{r['estado']} {r.get('detalle', '')[:100]}"))
fecha = pd.Timestamp("2026-11-12")
reun = ["2026-12-17", "2027-02-04", "2027-04-29", "2027-07-22", "2027-10-28"]
cortes = [(pd.Timestamp(m) - fecha).days for m in reun]
suave = [{"dias": d, "tipo": 0.0192 + (0.0160 - 0.0192) * d / 365} for d in cortes + [cortes[-1] + 60]]
vs = {"fecha": "2026-11-12", "base_curva": 360, "curva": suave, "tipo_oficial": 0.0192, "diferencial_estable": 0.0,
      "reuniones": reun}
for prec in (None, 1e-4, 5e-4):
    vv = {**vs, **({"precision_cotizacion": prec} if prec else {})}
    r, _, e = servir("MON-EXP-001", vv, {})
    if r and r["estado"] != "RECHAZADO":
        s = r["resultado"]["senda"]
        print(f"      (informativo) curva OIS suave 1,92 → 1,60 % (nodos en las reuniones), precisión {prec}: {r['estado']}; "
              f"movimientos {[round(x['movimientos_en_reunion'], 2) for x in s]}; incertidumbre "
              f"{[round(x['incertidumbre_redondeo_pb'], 2) for x in s]} pb; limitaciones {r['limitaciones']}")
    else:
        print(f"      (informativo) curva OIS suave, precisión {prec}: {(r or {}).get('estado', e)} {(r or {}).get('detalle', '')[:100]}")
# incertidumbre de redondeo cercana a Δ servida sin limitación ni advertencia
base, r0 = 360.0, 0.0192
senda = [r0, r0 - 0.0025, r0 - 0.005, r0 - 0.005, r0 - 0.0025, r0 - 0.005]
cc = [0] + cortes


def tipo(d):
    lg = sum((min(b, d) - a) * math.log1p(t / base) for a, b, t in zip(cc, cc[1:] + [10 ** 9], senda) if a < d)
    return math.expm1(lg) * base / d


nodos = sorted({c + 12 for c in cortes} | {c + 30 for c in cortes} | {20})
vr = {"fecha": "2026-11-12", "base_curva": 360, "curva": [{"dias": d, "tipo": round(tipo(d), 4)} for d in nodos],
      "tipo_oficial": r0, "diferencial_estable": 0.0, "reuniones": reun, "precision_cotizacion": 5e-5}
r, _, e = servir("MON-EXP-001", vr, {})
if r and r["estado"] != "RECHAZADO":
    s = r["resultado"]["senda"]
    inc = max(x["incertidumbre_redondeo_pb"] for x in s)
    err = max(abs(x["tipo_mercado_implicito"] - t) * 1e4 for x, t in zip(s, senda[1:]))
    aviso = [x for x in r["limitaciones"] + r["resultado"].get("advertencias", []) if "redondeo" in x or "incertidumbre" in x]
    C.informe("MON-EXP: una senda con incertidumbre de redondeo cercana a Δ se sirve con una limitación que lo diga",
              inc < 12.5 or bool(aviso), f"{r['estado']}; incertidumbre máx. {inc:.1f} pb (Δ = 25 pb), error real máx. {err:.1f} pb; "
              f"movimientos {[round(x['movimientos_en_reunion'], 2) for x in s]} (verdad [−1, −1, 0, 1, −1]); limitaciones {r['limitaciones']}")
else:
    print(f"      (informativo) curva redondeada a 1 pb con precisión 0,5 pb: {(r or {}).get('detalle', e)}")

# ------------------------------------------------------------------ 6. tamaños límite
grandes = {}
v, p = caso("IDX-CONC-001")
n = 200_000
w = np.random.default_rng(1).dirichlet(np.ones(n))
w[-1] = 1 - float(np.sum(w[:-1]))
v["composicion"]["componentes"] = [{"id": f"C{i:06d}", "peso": float(x), "sector": f"S{i % 11}"} for i, x in enumerate(w)]
grandes["IDX-CONC-001 con 200 000 componentes"] = ("IDX-CONC-001", v, p)
v, p = caso("MON-EXP-001", 1)
d_max = max(n["dias"] for n in v["curva"])
v["curva"] = [{"dias": d, "tipo": v["curva"][0]["tipo"]} for d in range(1, d_max + 1)]
grandes["MON-EXP-001 con un nodo por día"] = ("MON-EXP-001", v, p)
for nombre, (ficha, v, p) in grandes.items():
    t0 = time.perf_counter()
    r, _, e = servir(ficha, v, p)
    dt = time.perf_counter() - t0
    C.informe(f"tamaño límite: {nombre} responde (< 30 s) sin excepción", e is None and dt < 30,
              f"{(r or {}).get('estado', e)} en {dt:.1f} s")

shutil.rmtree(TMP, ignore_errors=True)
sys.exit(C.resumen())
