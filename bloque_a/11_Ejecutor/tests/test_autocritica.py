"""PB-38 (objeción fuerte sin resolver fuera del top-3) y PB-14 (arrastre con invalidación activada)."""
import pandas as pd

from conftest import AS_OF, nuevo_bloque


def test_objecion_fuerte_sin_resolver_excluye_del_top3(ciclo_semanal):
    b, r, _ = ciclo_semanal
    sel = {o["opp_id"] for d in r["paquete"]["clases"].values() for o in d["opciones"]}
    f3 = [e for e in b.almacen.leer("F3", AS_OF) if e.get("objeciones_internas")]
    abiertas = [e for e in f3 if any(o["fuerza"] == "fuerte" and not o["resuelta"] for o in e["objeciones_internas"])]
    assert abiertas, "el mock debe generar al menos una objeción fuerte sin resolver"
    for e in abiertas:
        assert e["opp_id"] not in sel and not e["elegible"]
        assert any("objeción" in m for m in e["motivos_no_elegible"])
    for d in r["paquete"]["clases"].values():
        for o in d["opciones"]:
            assert all(ob["estado"] == "RESPONDIDA" for ob in o["objeciones"] if ob["fuerza"] == "fuerte")


def test_arrastre_con_invalidacion_activada(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    r1 = b.ciclo(AS_OF, alcance={"clases": ["MP"]})
    o = r1["paquete"]["clases"]["MP"]["opciones"][0]
    sym = o["indicador_seguimiento"]["simbolo"]
    precio = b.proveedor.valor_en(sym, AS_OF)[1]
    # El Analizador corrige la condición cuantitativa (entrada nueva, append-only): umbral por encima del precio
    b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": o["opp_id"],
                                       "invalidacion_cuantitativa": [{"simbolo": sym, "umbral": precio * 2, "direccion": "por_debajo"}]})
    prgs = [h["prg_id"] for h in o["horizontes"].values()]
    r2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()), alcance={"clases": ["MP"]})
    assert r2["gc0"]["MP"]["cambio_material"] and o["opp_id"] in r2["gc0"]["MP"]["invalidadas"]
    f3 = b.almacen.estado("F3")[o["opp_id"]]
    assert f3["estado"] == "CERRADA" and f3["cierre"]["motivo"] == "INVALIDACION"
    seg = {s["opp_id"]: s for s in r2["paquete"]["seguimiento_vigentes"]}
    assert seg[o["opp_id"]]["estado"] == "CERRADA" and seg[o["opp_id"]]["motivo_cierre"] == "INVALIDACION"
    f4 = b.almacen.estado("F4")
    assert all(f4[p]["estado"] == "ABIERTO" for p in prgs)              # los PRG no se anulan (R11)
