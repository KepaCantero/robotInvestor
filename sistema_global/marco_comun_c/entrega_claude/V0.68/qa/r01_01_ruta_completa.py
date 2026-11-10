"""QA r01 · sonda 01: un expediente DIRECTA que entra por D o por E, ¿llega hasta EJECUTADA por F y G («conserva las mismas
transiciones hacia delante», §4.1 regla 6)? La batería del implementador solo llega a PROPUESTA por D y E."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import (AHORA, ENTRADA, SALIDA, anotar_entrada, autorizar_op, chk, descartado_por_operador, dim, fin, informe_f, nuevo)


def ruta(bloque):
    o = nuevo()
    descartado_por_operador(o, 1)
    kw = {"motivo": "solo hay un candidato: lo pidió el operador"} if bloque == "E" else {}
    eid = f"EXP-D{bloque}-01"
    r = o.abrir_directa(eid, f"COR-{eid}", "TACTICA", bloque, "BROKER", AHORA, analisis="EV-SOB-0001", **kw)
    assert r["ok"], r
    if bloque == "D":
        r = o.comparar([eid], "D", AHORA)
        assert r["ok"], r
    r = o.proponer(eid, ENTRADA, SALIDA, "BROKER", AHORA, dim(o, eid))
    chk(f"{bloque}_PROPUESTA", r["ok"], r)
    r = autorizar_op(o, eid, informe_f(o, eid, 41), AHORA)
    chk(f"{bloque}_AUTORIZADA_por_F_y_el_operador", r["ok"], r)
    if not r["ok"]:
        return
    anotar_entrada(o, eid, "ORD-X-1", 100.0, AHORA)
    r = o.ejecutar(eid, {"orden_id": "ORD-X-1", "cantidad": 100.0, "precio": 1.1, "conciliada": True,
                         "proteccion_orden_ids": ["ORD-X-1-STOP"]}, "G", AHORA)
    e = o.expedientes[eid]
    chk(f"{bloque}_EJECUTADA_por_G_con_posicion", r["ok"] and e["estado"] == "EJECUTADA" and o.integridad() == [], r)
    # una vez invertido, el análisis no se reutiliza otra vez
    r = o.abrir_directa("EXP-OTRA", "COR-OTRA", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
    chk(f"{bloque}_invertido_no_se_reutiliza", not r["ok"] and r["codigo"] == "O-06", r)


ruta("D")
ruta("E")
sys.exit(fin())
