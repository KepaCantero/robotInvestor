"""T-125 · PB-46, fiabilidad de las fuentes de opinión (FUE-): el Evaluador resuelve los pronósticos explícitos de las
fuentes registrados en F2, calcula su BSS contraído y sus puntos de historial, y los comunica al Buscador por CT-19."""
import pandas as pd
import pytest
from bloque_a.configuracion import parametro
from conftest import AS_OF, config_pruebas, nuevo_bloque

SERIE = "SPY"
# T-125 r02 (QA r01, H-04): los pronósticos son de fuentes registradas en F9 (antes, «REF-0001» y «REF-0002», que no existen)
FUENTE_A, FUENTE_B = "REF-RF-0001", "REF-RF-0003"


def _escribir_clm(b, entrada, registro):
    """T-125 r02 (QA r01, H-03): la pieza entra en F2 en su fecha de registro (antes de su fecha objetivo), como en un ciclo."""
    b.reloj.fijar(registro)
    try:
        b.almacen.escribir("F2", "AG-12", entrada)
    finally:
        b.reloj.fijar(AS_OF)


def _sembrar(b, ref_id, aciertos, fallos, prob=0.7, desde="2025-01-06", inicio_id=1):
    """Pronósticos «SPY por encima de X» con fecha objetivo en días hábiles: X por debajo del cierre real (acierta) o por
    encima (falla). Cada uno se registra en F2 el día de su emisión."""
    fechas = pd.bdate_range(desde, periods=aciertos + fallos)
    for i, f in enumerate(fechas):
        _, valor = b.proveedor.valor_en(SERIE, f)
        acierta = i < aciertos
        emision = str((f - pd.Timedelta(days=30)).date())
        _escribir_clm(b, {
            "tipo_entrada": "CLM", "clm_id": f"CLM-2025-{inicio_id + i:04d}", "afirmacion": f"{ref_id}: SPY sube ({i})",
            "tipo_afirmacion": "PRONOSTICO_FUENTE", "clase": "RV", "evidencias": [],
            "pronostico_fuente": {"ref_id": ref_id, "variable": "cierre", "serie_ht01": SERIE, "fecha_objetivo": str(f.date()),
                                  "umbral_o_rango": valor - 1 if acierta else valor + 1, "direccion": "por_encima",
                                  "probabilidad": prob, "fecha_emision": emision}}, emision)


def _bloque(tmp_path, universo, **cfg):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(**cfg) if cfg else None)
    b.fijar_fecha(AS_OF)
    return b


def test_pb46_dos_fuentes_una_con_habilidad_y_otra_sin_ella(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)                       # acierta el 80 % diciendo 0,7
    _sembrar(b, FUENTE_B, 13, 12, inicio_id=101)       # acierta la mitad
    fue = {f["ref_id"]: f for f in b.evaluador.fiabilidad_fuentes(AS_OF)}
    assert set(fue) == {FUENTE_A, FUENTE_B}
    par = parametro(b.cfg, "fiabilidad_fuentes")
    for ref_id, (ok, mal) in {FUENTE_A: (20, 5), FUENTE_B: (13, 12)}.items():
        f = fue[ref_id]
        n = ok + mal
        brier = (ok * 0.3 ** 2 + mal * 0.7 ** 2) / n
        bss = 1 - brier / 0.25
        assert (f["n"], f["aciertos"]) == (n, ok)
        assert f["bss"] == pytest.approx(bss, abs=1e-6)
        assert f["bss_contraido"] == pytest.approx(n / (n + par["k_contraccion"]) * bss, abs=1e-6)
        assert f["puntos_historial"] == pytest.approx(par["puntos_neutro"] * (1 + f["bss_contraido"]), abs=1e-4)
        assert f["periodo"] == AS_OF[:7] and f["fue_id"].startswith("FUE-") and len(f["pronosticos"]) == n
    assert fue[FUENTE_A]["puntos_historial"] > par["puntos_neutro"] > fue[FUENTE_B]["puntos_historial"]
    assert 11 <= fue[FUENTE_A]["puntos_historial"] <= 12.5 and 9 <= fue[FUENTE_B]["puntos_historial"] <= 10.5


def test_pb46_las_fue_quedan_en_f6_y_se_comunican_al_buscador_por_ct19(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["run_id"]
    f6 = [e for e in b.almacen.estado("F6", clave="id").values() if e.get("tipo_entrada") == "FUE"]
    assert len(f6) == 1 and f6[0]["ref_id"] == FUENTE_A and f6[0]["comunicado_ct19"]
    msgs = [m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-16"]
    assert [m["msg_id"] for m in msgs] == [f6[0]["comunicado_ct19"]]


def test_pb46_una_vez_al_mes(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)
    assert len(b.evaluador.fiabilidad_fuentes(AS_OF)) == 1
    assert b.evaluador.fiabilidad_fuentes(AS_OF) == []                                 # el mismo mes, nada nuevo


def test_pb46_sin_muestra_suficiente_no_hay_fue(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    n_min = parametro(b.cfg, "fiabilidad_fuentes.n_min")
    _sembrar(b, FUENTE_A, n_min - 1, 0)
    assert b.evaluador.fiabilidad_fuentes(AS_OF) == []
    b2 = _bloque(tmp_path / "b", universo)
    _sembrar(b2, FUENTE_A, n_min, 0)
    assert len(b2.evaluador.fiabilidad_fuentes(AS_OF)) == 1


def test_pb46_no_se_resuelve_lo_que_no_ha_vencido_ni_lo_mal_formado(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 10, 0)
    base = {"ref_id": FUENTE_A, "variable": "cierre", "serie_ht01": SERIE, "umbral_o_rango": 1.0, "direccion": "por_encima",
            "probabilidad": 0.7, "fecha_emision": "2025-01-01", "fecha_objetivo": "2025-06-02"}
    raros = [{**base, "fecha_objetivo": "2026-12-31"},                         # no ha vencido
             {**base, "fecha_emision": "2025-07-01"},                          # emitido después de su fecha objetivo
             {**base, "direccion": "sube"}, {**base, "umbral_o_rango": "1"}, {**base, "umbral_o_rango": float("nan")},
             {**base, "umbral_o_rango": [3, 1], "direccion": "dentro"}, {**base, "probabilidad": 1.5}, {**base, "probabilidad": True},
             {**base, "serie_ht01": "NO-EXISTE"}, {**base, "fecha_objetivo": "2020-01-01", "fecha_emision": "2019-01-01"},   # fuera de ventana
             {k: v for k, v in base.items() if k != "ref_id"}]
    for i, pf in enumerate(raros):
        _escribir_clm(b, {"tipo_entrada": "CLM", "clm_id": f"CLM-2025-09{i:02d}", "afirmacion": f"raro {i}",
                          "tipo_afirmacion": "PRONOSTICO_FUENTE", "pronostico_fuente": pf},
                      min(pf["fecha_emision"], "2025-01-01"))
    ps = b.evaluador.pronosticos_de_fuentes(AS_OF)
    assert len(ps) == 10 and all(p["clm_id"].startswith("CLM-2025-00") for p in ps)


@pytest.mark.parametrize("direccion, rango, ocurre", [("dentro", [-1, 1], 1), ("fuera", [-1, 1], 0), ("dentro", [1, 2], 0),
                                                       ("fuera", [1, 2], 1), ("por_debajo", 1, 1), ("por_debajo", -1, 0)])
def test_pb46_cada_direccion_se_resuelve_bien(tmp_path, universo, direccion, rango, ocurre):
    b = _bloque(tmp_path, universo)
    _, valor = b.proveedor.valor_en(SERIE, "2025-06-02")
    umbral = [valor + x for x in rango] if isinstance(rango, list) else valor + rango
    _escribir_clm(b, {"tipo_entrada": "CLM", "clm_id": "CLM-2025-0001", "afirmacion": "x", "tipo_afirmacion": "PRONOSTICO_FUENTE",
                      "pronostico_fuente": {"ref_id": FUENTE_A, "variable": "cierre", "serie_ht01": SERIE,
                                            "fecha_objetivo": "2025-06-02", "umbral_o_rango": umbral,
                                            "direccion": direccion, "fecha_emision": "2025-05-01"}}, "2025-05-01")
    ps = b.evaluador.pronosticos_de_fuentes(AS_OF)
    assert [(p["resultado"], p["prob"]) for p in ps] == [(ocurre, parametro(b.cfg, "fiabilidad_fuentes.prob_sin_declarar"))]


def test_pb46_sin_pronosticos_de_fuentes_el_ciclo_no_cambia(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert not [e for e in b.almacen.leer("F6") if e.get("tipo_entrada") == "FUE"]
    assert not [m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-16"]
