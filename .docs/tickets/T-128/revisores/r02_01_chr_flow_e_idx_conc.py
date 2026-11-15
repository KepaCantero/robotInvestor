"""QA r02 de T-128 · CHR-FLOW-001 (H-02: mínimo de 2 monedas, dominancia, crecimiento a null) e IDX-CONC-001 (amplitud y
contribución con 1 componente o dominadas), con vías que no prueba el implementador.

 F. CHR-FLOW-001: caso de control; una moneda; dos copias a escala; una de más del 95 %; un crecimiento que aporta una sola
    (también con dos rellenos que se compensan: la aportación con signo); dos monedas reales planas (crecimiento 0); la
    petición no cambia `monedas_estables_minimas` ni `FRONTERA_B`; una moneda troceada (límite declarado).
 C. IDX-CONC-001: precios de 1 componente; precios de 2 que son el mismo valor (copia exacta y copia a escala: la regla de
    copias a escala que la r03 de T-127 declara cubierta); índice de 1 componente; contribución de dos copias con la misma
    rentabilidad; contribución de un índice real de 3.
Uso: .venv/bin/python -I .docs/tickets/T-128/revisores/r02_01_chr_flow_e_idx_conc.py [ejecutor]
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from bloque_a.motor import fichas_mon_idx as fm  # noqa: E402
from bloque_a.motor import fichas_reales as fr  # noqa: E402
from bloque_a.motor import frontera_b as fb  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402
from bloque_a.motor.operaciones import ErrorFicha  # noqa: E402

K = C.Contador("r02_01 T-128 CHR-FLOW e IDX-CONC")


def correr(mod, ficha, v, p=None, series=None):
    ent = {"valores": copy.deepcopy(v), "series": series or {}, "series_rol": {}}
    try:
        res, lim = mod.FICHAS[ficha]["fn"](ent, dict(p or {}))
        return "S", res, lim
    except ErrorFicha as e:
        return "R", str(e), []


def serie(v, nombre):
    return pd.Series({pd.Timestamp(x["fecha"]): x["oferta"] for x in v["oferta_stablecoins"][nombre]}).sort_index()


def crec(s):
    return (s.iloc[-1] / s[s.index <= s.index[-1] - pd.Timedelta(days=30)].iloc[-1] - 1) * 100


# ------------------------------------------------------------------ F: CHR-FLOW-001
print("[CHR-FLOW-001]")
v0 = C.valores("CHR-FLOW-001", 0)
p0 = dict(servicio.CASOS_CONTROL["CHR-FLOW-001"][0].get("parametros") or {})
usd, eur = v0["oferta_stablecoins"]["USDX"], v0["oferta_stablecoins"]["EURX"]
st, r, lim = correr(fr, "CHR-FLOW-001", v0, p0)
tot = serie(v0, "USDX") + serie(v0, "EURX")
K.comprobar("F: el caso de control se sirve con el crecimiento del total", st == "S" and abs(r["crecimiento_stablecoins_pct"] - crec(tot)) < 1e-9)


def con(ofertas):
    v = copy.deepcopy(v0)
    v["oferta_stablecoins"] = ofertas
    return correr(fr, "CHR-FLOW-001", v, p0)


st, r, _ = con({"EURX": eur})
K.comprobar("F: una moneda se rechaza", st == "R" and "EURX" not in r, r[:120])
st, r, _ = con({"EURX": eur, "B": [{**x, "oferta": x["oferta"] * 3.7} for x in eur], "C": [{**x, "oferta": x["oferta"] * 0.2} for x in eur]})
K.comprobar("F: tres copias a escala de una moneda se rechazan", st == "R", str(r)[:120])
k96 = 0.04 / 0.96 * usd[-1]["oferta"] / eur[-1]["oferta"]
st, r, _ = con({"USDX": usd, "EURX": [{**x, "oferta": x["oferta"] * k96 * 0.99} for x in eur]})
K.comprobar("F: una moneda de más del 95 % de la oferta se rechaza", st == "R" and "95%" in r, str(r)[:120])
# un relleno A creciendo y otros dos que se compensan (+Δ y −Δ en 30 días): con signo, el crecimiento es el de A
fechas = [x["fecha"] for x in eur]
n = len(fechas)
s_e = serie(v0, "EURX")
idx30 = s_e.index[s_e.index <= s_e.index[-1] - pd.Timedelta(days=30)][-1]
sube = [{"fecha": f, "oferta": 5e10 * (1 + (0.02 if pd.Timestamp(f) > idx30 else 0.0))} for f in fechas]
baja = [{"fecha": f, "oferta": 6e10 * (1 - (0.02 * 5 / 6 if pd.Timestamp(f) > idx30 else 0.0))} for f in fechas]
st, r, lim = con({"EURX": eur, "MAS": sube, "MENOS": baja})
crec_eur = crec(s_e)
print(f"    EURX + MAS (+1e9) + MENOS (−1e9): {st} · crecimiento {r['crecimiento_stablecoins_pct'] if st == 'S' else r[:100]}"
      f" (EURX {crec_eur:.6f} %)")
K.comprobar("F: con dos rellenos que se compensan, el crecimiento no se entrega (aportación con signo)",
            st == "R" or r["crecimiento_stablecoins_pct"] is None)
# dos monedas reales planas en los 30 días (oferta constante): crecimiento 0 de las dos
plano_u = [{"fecha": f, "oferta": 8e10} for f in fechas]
plano_e = [{"fecha": f, "oferta": 2.5e10} for f in fechas]
st, r, _ = con({"USDX": plano_u, "EURX": plano_e})
print(f"    dos monedas planas (crecimiento 0 y 0): {st} · {str(r)[:140] if st == 'R' else r['crecimiento_stablecoins_pct']}")
plana_rechazo = st == "R"
# la petición no cambia las reglas
for clave in ("monedas_estables_minimas", "peso_maximo_componente", "tolerancia_clon"):
    st, r, _ = correr(fr, "CHR-FLOW-001", {**v0, "oferta_stablecoins": {"EURX": eur}}, {**p0, clave: 1})
    K.comprobar(f"F: «{clave}» en la petición se rechaza como umbral fijo", st == "R" and "umbrales fijos" in r, str(r)[:100])
# troceo (límite declarado): EURX en dos partes con crecimientos distintos
a = [{"fecha": x["fecha"], "oferta": x["oferta"] * (0.3 + 0.2 * i / n)} for i, x in enumerate(eur)]
b = [{"fecha": x["fecha"], "oferta": x["oferta"] - y["oferta"]} for x, y in zip(eur, a, strict=True)]
st, r, _ = con({"EURX-a": a, "EURX-b": b})
troceo = st == "S" and r["crecimiento_stablecoins_pct"] is not None and abs(r["crecimiento_stablecoins_pct"] - crec_eur) < 1e-9
print(f"    EURX troceada en dos (límite declarado): {st} · {'da el crecimiento de EURX' if troceo else str(r)[:100]}")

# ------------------------------------------------------------------ C: IDX-CONC-001
print("\n[IDX-CONC-001]")
fechas = pd.bdate_range("2025-06-02", periods=320)
rng = np.random.default_rng(7)
x00 = pd.Series(100 * np.exp(np.cumsum(rng.normal(0.0005, 0.01, 320))), index=fechas)
x01 = pd.Series(100 * np.exp(np.cumsum(rng.normal(-0.0005, 0.01, 320))), index=fechas)


def conc(nc, rent=None):
    comp = fm._composicion(nc, igual=False)
    ini = {"fecha": "2025-10-31", "componentes": [{"id": c["id"], "peso": c["peso"]} for c in comp["componentes"]]}
    v = {"composicion": comp, "composicion_inicio": ini}
    if rent is not None:
        v["rentabilidades_periodo"] = dict(zip([c["id"] for c in comp["componentes"]], rent, strict=True))
    return v


sobre00 = float(x00.iloc[-1] > x00.iloc[-200:].mean())
linea00 = float(np.sign(x00.pct_change().iloc[1:]).cumsum().iloc[-1])
st, r, _ = correr(fm, "IDX-CONC-001", conc(10), {"top_n": 5}, series={"C00": x00})
K.comprobar("C: precios de 1 componente: amplitud null", st == "S" and r["amplitud"] is None)
st, r, _ = correr(fm, "IDX-CONC-001", conc(10), {"top_n": 5}, series={"C00": x00, "C01": x01})
K.comprobar("C: precios de 2 valores distintos: amplitud servida", st == "S" and r["amplitud"] is not None)
for nombre, otra in (("copia exacta", x00.copy()), ("copia a escala ×0,5", x00 * 0.5)):
    st, r, lim = correr(fm, "IDX-CONC-001", conc(10), {"top_n": 5}, series={"C00": x00, "C01": otra})
    a_ = r["amplitud"] if st == "S" else None
    print(f"    C00 + {nombre}: {st} · amplitud {a_} · C00: sobre su media {sobre00:g}, línea {linea00:g}")
    fuga = a_ is not None and a_["porcentaje_sobre_media"] == sobre00 and a_["linea_avance_retroceso"] == 2 * linea00
    K.comprobar(f"C: C00 + {nombre} no da la amplitud de C00 (copias a escala, «cubiertas» en INC-T127-01 r03)", not fuga,
                "(la da: porcentaje y línea de C00)")
st, r, _ = correr(fm, "IDX-CONC-001", conc(1, rent=[0.13]), {"top_n": 5})
K.comprobar("C: índice de 1 componente: contribución null", st == "S" and r["contribucion"] is None)
st, r, _ = correr(fm, "IDX-CONC-001", conc(2, rent=[0.13, 0.13 * 1.004]), {"top_n": 5})
K.comprobar("C: dos componentes con la misma rentabilidad (a < 1 %): contribución null", st == "S" and r["contribucion"] is None)
st, r, _ = correr(fm, "IDX-CONC-001", conc(3, rent=[0.2, -0.1, 0.05]), {"top_n": 5})
K.comprobar("C: un índice de 3 con rentabilidades corrientes: contribución servida", st == "S" and r["contribucion"] is not None)
st, r, lim = correr(fm, "IDX-CONC-001", conc(3, rent=[0.2, 0.1, -0.1]), {"top_n": 5})
w = [c["peso"] for c in conc(3)["composicion_inicio"]["componentes"]]
print(f"    3 con rentabilidades 0,2 / 0,1 / −0,1 y pesos {np.round(w, 3).tolist()}: contribución "
      f"{None if st != 'S' else r['contribucion']}")
for i in range(len(servicio.CASOS_CONTROL["IDX-CONC-001"])):
    v = C.valores("IDX-CONC-001", i)
    st, r, _ = correr(fm, "IDX-CONC-001", v, servicio.CASOS_CONTROL["IDX-CONC-001"][i].get("parametros"))
    K.comprobar(f"C: caso de control {i} servido", st == "S", str(r)[:100])
print(f"\n    notas: dos monedas planas → {'rechazo' if plana_rechazo else 'servido'}; troceo de EURX → "
      f"{'da su crecimiento (límite declarado)' if troceo else 'no'}; IDX_CONC_COMPONENTES_MINIMOS = "
      f"{fm.IDX_CONC_COMPONENTES_MINIMOS}; monedas_estables_minimas = {fr.UMBRALES['CHR-FLOW-001']['monedas_estables_minimas']};"
      f" AVISO_B = {fb.AVISO_B}")
sys.exit(K.fin())
