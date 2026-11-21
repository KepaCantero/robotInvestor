from conftest import AS_OF, config_pruebas, nuevo_bloque


def test_rotacion_presupuestada_en_f5(tmp_path, universo):
    cfg = config_pruebas(presupuesto_uc={"rotacion_exploratoria": 0.2})
    b = nuevo_bloque(tmp_path, universo, cfg=cfg)
    b.ciclo(AS_OF, alcance={"clases": ["RF"]})
    r = b.ciclo("2026-06-12", tipo="AD_HOC", alcance={"clases": ["RF"]}, nivel_forzado="N1")
    plan = b.almacen.estado("F5")[r["run_id"]]["cribado_n1"]["RF"]
    assert plan["uc_rotacion"] / plan["uc_cribado"] == 0.2
    assert plan["uc_vigentes"] + plan["uc_rotacion"] == plan["uc_cribado"]
    assert plan["simbolos"]
