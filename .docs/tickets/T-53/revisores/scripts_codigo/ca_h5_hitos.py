"""C18: tres copias del mismo hito (mismo HIT-, misma fecha) cuentan como «≥ 3 hitos»; hitos posteriores al horizonte también."""
from bloque_a.herramientas.referencia import ht09_validador_g3 as v
h = {"hit_id": "HIT-2026-0001", "fecha": "2027-06-05", "indicador": "Rentabilidad de SPY", "criterio": "superior a ACWI"}
for nombre, hitos in (("tres copias", [dict(h), dict(h), dict(h)]),
                      ("fechas fuera de orden y > 30 años", [dict(h, hit_id="HIT-1", fecha="2070-01-01"), dict(h, hit_id="HIT-2", fecha="2027-01-01"), dict(h, hit_id="HIT-3", fecha="2028-01-01")])):
    R = v.Registro()
    v._validar_h5(R, "clases.RV.OPP-1.horizontes.H5", {"prg_id": "PRG-1", "banda": "más probable que no", "prob": None, "hitos": hitos}, "2026-06-05")
    inc = [(c["id"], c["resultado"], [i["detalle"] for i in c["incidencias"]]) for c in R.comprobaciones() if c["resultado"] != "OK"]
    print(nombre, "->", inc or "sin incidencias")
