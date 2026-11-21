import pandas as pd
import pytest
from conftest import AS_OF, config_pruebas, nuevo_bloque


def test_recalcular_referencia_sin_futuro(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    p = min((x for x in b.almacen.estado("F4").values() if x.get("prob_interna") is not None), key=lambda x: x["fecha_resolucion"])
    calc = p["referencia_ingenua"]["calc_id"]
    b.almacen.escribir("RC", "AG-13", {"tipo_entrada": "SERVICIO", "calc_id": calc, "as_of": "2026-06-06"})
    b.fijar_fecha("2026-07-10")
    b.evaluador.ciclo("2026-07-10")
    corr = [e for e in b.almacen.leer("F6") if e.get("tipo_entrada") == "CORRECCION_FUGA" and e["prg_id"] == p["prg_id"]]
    assert len(corr) == 1 and corr[0]["referencia_limpia"]["calc_id"] != calc
    assert b.almacen.estado("F4")[p["prg_id"]]["referencia_ingenua"]["calc_id"] == calc
    prg = next(x for x in b.evaluador.resueltos("2026-07-10") if x["prg_id"] == p["prg_id"])
    assert prg["referencia_ingenua"] == corr[0]["referencia_limpia"]


@pytest.mark.parametrize("mejor,estado", [(True, "CONFIRMADO"), (False, "REVERTIDO")])
def test_cierre_con_comparacion_pareada(tmp_path, universo, mejor, estado):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(evaluacion={"min_calibrar": 3}))
    b.fijar_fecha("2026-05-01")
    alm = b.almacen
    alm.escribir("F6", "AG-20", {"tipo_entrada": "AJU", "id": "AJU-1", "parametro": "P-11", "efecto_desde": "2026-05-01",
                "sombra_hasta": "2026-06-05", "estado": "EN_SOMBRA"})
    fechas = pd.date_range("2026-05-02", periods=4, freq="7D")
    for i, fecha in enumerate(fechas):
        b.fijar_fecha(fecha)
        rid = f"RUN-{i}"
        pesos = {"A": [1, 2], "B": [2, 1]}
        if not mejor:
            pesos = {k: v[::-1] for k, v in pesos.items()}
        alm.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": rid, "entrega": "ENTREGADA",
                     "sombra": {"RV": {"aju_id": "AJU-1", "rk_pareado": pesos}}})
        for opp, y in [("A", 1), ("B", 0)]:
            pid = f"PRG-{i}-{opp}"
            alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": opp, "clase": "RV", "run_id": rid,
                         "fecha_emision": str(fecha.date()), "horizonte": "H1", "sentido": "POSITIVO", "estado": "ABIERTO"})
            alm.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                         "resolucion": {"valor_observado": y, "fecha_dato": str(fecha.date()), "comprobacion_fuga": "SUPERADA"}})
    b.fijar_fecha(AS_OF)
    cierre = b.evaluador.cerrar_sombra(AS_OF)
    assert cierre["estado"] == estado and cierre["dm_hln"]["n"] == 4
    assert b.evaluador.cerrar_sombra(AS_OF) is None
