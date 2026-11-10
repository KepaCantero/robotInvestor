"""QA r01 · sonda 08: §4.1 regla 4, «una propuesta caducada no se ejecuta: vuelve a EN_ANÁLISIS o pasa a DESCARTADA». En la vía
discrecional, un expediente CADUCADA solo puede ir a EN_ANALISIS (análisis nuevo) o a DESCARTADA. ¿Puede la vía DIRECTA recuperar
el análisis de una propuesta caducada (CADUCADA es «reutilizable») y volver a proponerlo sin análisis nuevo?"""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, fin, hasta, nuevo  # noqa: E402
from pruebas_orquestador import CART_E  # noqa: E402

A2 = "2026-11-08T13:00:00+00:00"   # pasó la ventana de la propuesta (12:00) pero no la vigencia del sobre (18:00)
o = nuevo()
hasta(o, "PROPUESTA", 1)
print("sobre valid_until:", o.expedientes["EXP-0001"]["sobre"]["valid_until"], "ventana propuesta:", ENTRADA["ventana_hasta"])
r = o.barrer(A2)
print("barrer:", r["ok"], [c for c in r["cambios"] if c[0] == "expediente"])
x = o.expedientes["EXP-0001"]
print("origen:", x["estado"], "historial:", [(h["desde"], h["hasta"], h["actor"]) for h in x["historial"]][-2:])
r = o.proponer("EXP-0001", {**ENTRADA, "ventana_hasta": "2026-11-08T17:00:00+00:00"}, SALIDA, "GESTOR_TACTICA", A2)
print("el propio expediente CADUCADA no se vuelve a proponer:", r["ok"], r["codigo"])
r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", A2, analisis="EV-SOB-0001")
print("abrir_directa por D con el análisis de la propuesta caducada:", r["ok"], r["codigo"], r["motivo"][:90])
if r["ok"]:
    # el rival de la comparación (EXP-0002) lo descarta el operador (si no, ganaría él y la sonda no diría nada)
    assert o.descartar("EXP-0002", "el operador descarta al rival", "OPERADOR", A2)["ok"]
    vivos = sorted(k for k, y in o.expedientes.items() if y["estado"] in ("VALIDADA", "COMPARADA"))
    r = o.comparar(vivos, "D", A2)
    print("comparar", vivos, ":", r["ok"], r["codigo"], "ganador:", r.get("ganador"))
    if r["ok"] and not o.expedientes["EXP-DD-01"]["comparacion"]["ganador"]:
        o.elegir("EXP-DD-01", "OPERADOR", "elección de la sonda", A2)
    cart = {**copy.deepcopy(CART_E), "fecha_hora": "2026-11-08T12:55:00+00:00"}
    ce = {**ENTRADA, "ventana_hasta": "2026-11-08T17:00:00+00:00"}
    r = o.proponer("EXP-DD-01", ce, SALIDA, "BROKER", A2, dim(o, "EXP-DD-01", entrada=ce, cartera=cart, ahora=A2))
    print("proponer de nuevo el análisis de la propuesta caducada:", r["ok"], r["codigo"], r["motivo"][:100])
    chk("la_propuesta_caducada_no_vuelve_sin_analisis_nuevo", not r["ok"], r)
sys.exit(fin())
