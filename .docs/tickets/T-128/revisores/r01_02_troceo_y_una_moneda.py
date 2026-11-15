"""QA r01 de T-128 · ¿una sola petición da la cifra de un valor o de un token en las fichas revisadas?

 T. IDX-REB-001: un cambio de composición con UNA inclusión (su demanda ya no se entrega, INC-T128-01) se pide con esa
    inclusión troceada en dos «valores» (0,0007 y 0,0003 del peso con 3e8 y 2e8 de volumen): días de volumen distintos
    (2,33 y 1,5), ninguno aporta más del 95 %, y la cesta da la demanda y los días de volumen del valor incluido.
 U. CHR-FLOW-001: `oferta_stablecoins` con UNA moneda estable (sin mínimo ni dominancia): el crecimiento a 30 días y la
    oferta son los de ese token (INC-T128-01 dice «la oferta agregada, sin cifra por moneda»).
REI-NAV-001 y REI-FFO-001 (troceo y simetría): `.docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py`.
Uso: .venv/bin/python -I .docs/tickets/T-128/revisores/r01_02_troceo_y_una_moneda.py [ejecutor]
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import pandas as pd  # noqa: E402

K = C.Contador("r01_02 T-128 troceo y una moneda")
m = C.motor()


def servir(f, i, cambiar):
    p = C.peticion(f, i)
    cambiar(p["datos"][0]["valores"])
    r, exc, _ = C.servir_contando(m, p)
    if exc is not None:
        return "X", str(exc)
    return ("S", r["resultado"]) if str(r["estado"]).startswith("SERVED") else ("R", r["detalle"])


def cerca(a, b, tol=1e-9):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b))


# ------------------------------------------------------------------ IDX-REB-001
print("[IDX-REB-001]")
aum = None


def una(v, cambios):
    global aum
    v["evento"]["cambios"] = cambios
    aum = v["evento"]["activos_indexados"]["valor"]


st, r = servir("IDX-REB-001", 0, lambda v: una(v, [{"id": "IN", "delta_peso": 0.001, "volumen_medio": 5e8},
                                                  {"id": "OUT", "delta_peso": -0.001, "volumen_medio": 2e8}]))
inc = r["demanda_estimada"]["inclusiones"] if st == "S" else None
print(f"    una inclusión: {st} · {inc}")
K.comprobar("IDX-REB-001: la cesta de un valor no da su demanda (control de T-128)", st == "S" and inc["demanda"] is None)
st, r = servir("IDX-REB-001", 0, lambda v: una(v, [{"id": "IN-a", "delta_peso": 0.0007, "volumen_medio": 3e8},
                                                  {"id": "IN-b", "delta_peso": 0.0003, "volumen_medio": 2e8},
                                                  {"id": "OUT-a", "delta_peso": -0.0006, "volumen_medio": 1.0e8},
                                                  {"id": "OUT-b", "delta_peso": -0.0004, "volumen_medio": 1.0e8}]))
dem_in, dias_in = 0.001 * aum, 0.001 * aum / 5e8
dem_out, dias_out = -0.001 * aum, -0.001 * aum / 2e8
if st == "S":
    inc, exc = r["demanda_estimada"]["inclusiones"], r["demanda_estimada"]["exclusiones"]
    print(f"    IN y OUT troceados en dos: SERVIDO · inclusiones {inc} (IN: {dem_in:g}, {dias_in:g} días) · exclusiones {exc} "
          f"(OUT: {dem_out:g}, {dias_out:g} días)")
    fuga = cerca(inc["demanda"], dem_in) and cerca(inc["dias_volumen_cesta"], dias_in) and cerca(exc["dias_volumen_cesta"], dias_out)
else:
    print(f"    {st} {str(r)[:160]}")
    fuga = False
K.comprobar("IDX-REB-001 T: un valor troceado en dos no da su demanda ni sus días de volumen", not fuga)

# ------------------------------------------------------------------ CHR-FLOW-001
print("\n[CHR-FLOW-001]")
v0 = C.valores("CHR-FLOW-001", 0)
nombre = sorted(v0["oferta_stablecoins"])[0]
serie = pd.Series({pd.Timestamp(x["fecha"]): x["oferta"] for x in v0["oferta_stablecoins"][nombre]}).sort_index()
T = serie.index[-1]
previo = serie[serie.index <= T - pd.Timedelta(days=30)].iloc[-1]
crec = (serie.iloc[-1] / previo - 1) * 100
st, r = servir("CHR-FLOW-001", 0, lambda v: v.update(oferta_stablecoins={nombre: v["oferta_stablecoins"][nombre]}))
if st == "S":
    print(f"    solo {nombre}: SERVIDO · crecimiento {r['crecimiento_stablecoins_pct']:.9f} % (el suyo {crec:.9f} %) · oferta "
          f"{r['oferta_stablecoins']:g} (la suya {serie.iloc[-1]:g})")
    fuga = cerca(r["crecimiento_stablecoins_pct"], crec)
else:
    print(f"    {st} {str(r)[:160]}")
    fuga = False
K.comprobar("CHR-FLOW-001 U: una sola moneda estable no da su crecimiento ni su oferta", not fuga)
sys.exit(K.fin())
