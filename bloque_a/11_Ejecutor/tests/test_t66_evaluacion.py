"""T-66 · Evaluador: PA-09 (contaminación), PA-10 (aprendizaje que solo endurece), PA-03 (muestra efectiva) y PA-21
(Brier del Analista frente al de Prospectiva).

Cada prueba falla sin el cambio que cubre (comprobado revirtiendo el cambio en una copia).
"""
import math

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.evaluador import Evaluador, contaminacion_posible
from bloque_a.motor import evaluacion as ev
from conftest import config_pruebas

AS_OF = "2026-01-02"


def _cfg(**evaluacion_o_aprendizaje):
    extra: dict = {}
    for k, v in evaluacion_o_aprendizaje.items():
        seccion = "aprendizaje" if k == "solo_endurecer" else "evaluacion"
        extra.setdefault(seccion, {})[k] = v
    return config_pruebas(**extra)


def _alta(a: Almacen, pid: str, **campos) -> None:
    base = {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-1", "clase": "RF", "horizonte": "H3", "prob_interna": 0.65,
            "sentido": "POSITIVO", "en_informe": True, "fecha_emision": "2025-01-02", "referencia_ingenua": {"valor_o_prob": 0.5},
            "estado": "ABIERTO"}
    a.escribir("F4", "AG-10", {**base, **campos})


def _resolver(a: Almacen, pid: str, o: int, fecha: str = "2025-12-31", valor: float | None = None) -> None:
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                               "resolucion": {"resultado_binario": o, "comprobacion_fuga": "SUPERADA",
                                              "valor_observado": valor if valor is not None else (0.01 if o else -0.01),
                                              "fecha_resuelto": fecha}})


def _celda_habil(a: Almacen, n: int = 150, contaminados: int = 0, fechas=None, prefijo: str = "PRG-2025") -> None:
    """Pronosticador hábil y calibrado (el mismo de la prueba PB-32 de integración): certifica con 150 PRG independientes."""
    rng = np.random.default_rng(1)
    for i in range(n):
        p = float(rng.choice([0.3, 0.7]))
        o = int(rng.random() < p)
        pid = f"{prefijo}-{i + 1:04d}"
        fr = fechas[i] if fechas is not None else str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date())
        _alta(a, pid, prob_interna=p, fecha_resolucion=fr, contaminacion_posible=i < contaminados)
        _resolver(a, pid, o)


def _almacen(tmp_path) -> Almacen:
    a = Almacen(tmp_path)
    a.reloj.fijar(AS_OF)
    return a


# ================================================================================================ PA-09 · contaminación
def test_pa09_valor_del_campo_y_registros_antiguos():
    assert not contaminacion_posible({})                                  # registro anterior a T-66: false
    assert not contaminacion_posible({"contaminacion_posible": None})
    assert not contaminacion_posible({"contaminacion_posible": False})
    assert contaminacion_posible({"contaminacion_posible": True})
    for dudoso in ("true", "false", 1, 0, "sí"):                          # ante la duda, se marca
        assert contaminacion_posible({"contaminacion_posible": dudoso})


def test_pa09_contaminados_se_registran_pero_no_cuentan_en_metricas_ni_historial(tmp_path):
    a = _almacen(tmp_path)
    for i in range(6):
        campos = {} if i == 0 else {"contaminacion_posible": i >= 3}      # PRG-0001 sin el campo: cuenta como false
        _alta(a, f"PRG-2025-{i + 1:04d}", fecha_resolucion=f"2025-12-{10 + i}", **campos)
        _resolver(a, f"PRG-2025-{i + 1:04d}", 1)
    e = Evaluador(a, None, None, _cfg(), None)
    assert [p["prg_id"] for p in e.resueltos(AS_OF)] == ["PRG-2025-0001", "PRG-2025-0002", "PRG-2025-0003"]
    assert len(e.resueltos(AS_OF, admisibles=False)) == 6                  # se siguen resolviendo y registrando
    m = e.metricas(AS_OF)["RF|H3"]
    assert m["n"] == 3 and m["excluidos_contaminacion"] == 3
    assert e.excluidos_contaminacion(AS_OF) == {"total": 3, "por_celda": {"RF|H3": 3}}
    assert e.metricas(AS_OF, admisibles=False)["RF|H3"]["n"] == 6
    h = e.historial_aciertos(AS_OF, semanas=52)
    assert h["global"]["n"] == 3 and "3 con contaminación posible" in h["nota"]
    # el ciclo C5 deja el recuento en la entrada MET de F6
    r = e.ciclo(AS_OF)
    assert r["excluidos_contaminacion"]["total"] == 3
    assert a.estado("F6", clave="id")[f"MET-{AS_OF}"]["excluidos_contaminacion"]["total"] == 3


def test_pa09_contaminados_no_cuentan_para_certificados(tmp_path):
    a = _almacen(tmp_path)
    _celda_habil(a, contaminados=60)                                      # 150 PRG, 60 contaminados: 90 admisibles
    res = Evaluador(a, None, None, _cfg(), None).revisar_certificados(AS_OF)
    assert res["emitidos"] == [] and res["insuficientes"] == {"RF|H3": "n = 90 < 100"}
    assert res["excluidos_contaminacion"]["total"] == 60


def _celda_recalibrable(a: Almacen, contaminados: int) -> None:
    for i in range(40):
        pid = f"PRG-2025-{i + 1:04d}"
        _alta(a, pid, puntuaciones_opcion={"A": float(i), "E": float(40 - i)}, fecha_resolucion="2025-12-01",
              contaminacion_posible=i < contaminados)
        _resolver(a, pid, 1, valor=0.001 * i)                             # A ordena bien; E, al revés


def test_pa09_contaminados_no_cuentan_para_la_recalibracion(tmp_path):
    a = _almacen(tmp_path)
    _celda_recalibrable(a, contaminados=15)                               # 25 admisibles < min_calibrar (30)
    assert Evaluador(a, None, None, _cfg(), None).recalibrar(AS_OF) is None
    b = _almacen(tmp_path / "b")
    _celda_recalibrable(b, contaminados=0)
    assert Evaluador(b, None, None, _cfg(), None).recalibrar(AS_OF)["parametro"] == "P-11"


def test_pa09_contaminados_no_generan_lecciones(tmp_path):
    a = _almacen(tmp_path)
    for i in range(12):                                                    # acierto 0 %: daría una lección PREDICTIVA
        _alta(a, f"PRG-2025-{i + 1:04d}", fecha_resolucion=f"2025-11-{i + 1:02d}", contaminacion_posible=True)
        _resolver(a, f"PRG-2025-{i + 1:04d}", 0)
    e = Evaluador(a, None, None, _cfg(), None)
    assert e.extraer_lecciones(AS_OF, e.metricas(AS_OF)) == []
    assert e.ciclo(AS_OF)["lecciones_nuevas"] == []
    assert not [x for x in a.leer("F6") if x.get("tipo_entrada") == "LEC"]


def _h5(a: Almacen, padre: str, cumplidos: int, fallados: int, padre_contaminado=False, hitos_contaminados: int = 0) -> None:
    ids = []
    for i, o in enumerate([1] * cumplidos + [0] * fallados):
        hid = f"HIT-2026-{padre[-4:]}{i + 1:03d}"
        ids.append(hid)
        _alta(a, hid, clase="RV", prg_padre=padre, es_hito=True, horizonte="H4", fecha_resolucion="2025-12-05",
              contaminacion_posible=i < hitos_contaminados)
        _resolver(a, hid, o)
    _alta(a, padre, clase="RV", horizonte="H5", prob_interna=None, hit_ids=ids, fecha_resolucion="2035-06-05",
          contaminacion_posible=padre_contaminado)


def test_pa09_contaminados_no_cuentan_para_la_degradacion_de_h5(tmp_path):
    a = _almacen(tmp_path)
    _h5(a, "PRG-2025-0901", 5, 15, padre_contaminado=True)               # 25 % con 20 hitos: degradaría
    e = Evaluador(a, None, None, _cfg(), None)
    est = e.estado_h5(AS_OF)
    assert est["celdas"]["RV"]["n"] == 0 and est["celdas"]["RV"]["excluidos_contaminacion"] == 20
    assert not est["celdas"]["RV"]["degradar"]
    assert est["pronosticos"]["PRG-2025-0901"]["hitos_resueltos"] == 20   # el estado del PRG sí los usa
    assert e.aplicar_degradacion_h5(AS_OF) == []
    b = _almacen(tmp_path / "b")
    _h5(b, "PRG-2025-0902", 5, 15, hitos_contaminados=1)                 # 19 hitos admisibles < 20
    eb = Evaluador(b, None, None, _cfg(), None)
    assert eb.estado_h5(AS_OF)["celdas"]["RV"]["n"] == 19 and eb.aplicar_degradacion_h5(AS_OF) == []


# ================================================================================================ PA-10 · solo endurecer
def test_pa10_clave_en_la_configuracion_por_defecto():
    assert config_pruebas()["aprendizaje"]["solo_endurecer"] is True


def test_pa10_certificado_nace_propuesto_y_no_habilita_probabilidades(tmp_path):
    a = _almacen(tmp_path)
    _celda_habil(a)
    e = Evaluador(a, None, None, _cfg(), None)
    res = e.revisar_certificados(AS_OF)
    assert [(c["celda"]["clase"], c["celda"]["horizonte"], c["estado"]) for c in res["emitidos"]] == [("RF", "H3", "PROPUESTO")]
    assert e.certificados_vigentes(AS_OF) == []
    assert [c["id"] for c in e.certificados_propuestos(AS_OF)] == [res["emitidos"][0]["id"]]
    assert e.revisar_certificados(AS_OF)["emitidos"] == []                # no se repite la propuesta


def test_pa10_aprobar_certificados_por_ct04(tmp_path):
    a = _almacen(tmp_path)
    _celda_habil(a)
    e = Evaluador(a, None, None, _cfg(), None)
    cid = e.revisar_certificados(AS_OF)["emitidos"][0]["id"]
    n_f6 = len(a.leer("F6"))
    for malos, motivo in (([], "vacía"), ([cid, cid], "repetidos"), ("CERT-2026-0001", "lista"),
                          ([cid, "CERT-2099-9999"], "no existe")):
        with pytest.raises(ValueError, match=motivo):
            e.aprobar_certificados(malos, AS_OF)
    assert len(a.leer("F6")) == n_f6 and e.certificados_vigentes(AS_OF) == []   # valida antes de mutar
    hechos = e.aprobar_certificados([cid], AS_OF)
    assert [(h["tipo_entrada"], h["id"], h["aprobado_por"]) for h in hechos] == [("CERT_APROBACION", cid, "BROKER")]
    vig = e.certificados_vigentes(AS_OF)
    assert [c["id"] for c in vig] == [cid] and vig[0]["celda"] == {"clase": "RF", "horizonte": "H3", "metodo": None}
    assert a.leer("F6")[-1]["tipo_entrada"] == "CERT_APROBACION"
    with pytest.raises(ValueError, match="no PROPUESTO"):
        e.aprobar_certificados([cid], AS_OF)


def test_pa10_desactivado_mantiene_el_comportamiento_anterior(tmp_path):
    a = _almacen(tmp_path)
    _celda_habil(a)
    e = Evaluador(a, None, None, _cfg(solo_endurecer=False), None)
    res = e.revisar_certificados(AS_OF)
    assert [c["estado"] for c in res["emitidos"]] == ["VIGENTE"]
    assert [c["id"] for c in e.certificados_vigentes(AS_OF)] == [res["emitidos"][0]["id"]]


def test_pa10_valor_no_booleano_falla_cerrado():
    with pytest.raises(ValueError, match="solo_endurecer"):
        Evaluador(None, None, None, _cfg(solo_endurecer="si"), None)


def test_pa10_recalibracion_siempre_propuesta(tmp_path):
    a = _almacen(tmp_path)
    _celda_recalibrable(a, contaminados=0)
    aju = Evaluador(a, None, None, _cfg(aplicar_recalibracion=True), None).recalibrar(AS_OF)
    assert aju["aplicado_en_produccion"] is False and aju["propuesta"] is True
    b = _almacen(tmp_path / "b")
    _celda_recalibrable(b, contaminados=0)
    aju_b = Evaluador(b, None, None, _cfg(aplicar_recalibracion=True, solo_endurecer=False), None).recalibrar(AS_OF)
    assert aju_b["aplicado_en_produccion"] is True and aju_b["propuesta"] is False


def test_pa10_revocar_y_retirar_siguen_siendo_automaticos(tmp_path):
    a = _almacen(tmp_path)
    for i in range(100):                                                   # celda sin habilidad (BSS ≤ 0)
        pid = f"PRG-2025-{i + 1:04d}"
        _alta(a, pid, prob_interna=0.65, clase="RV", fecha_resolucion=str((pd.Timestamp("2025-01-02") + pd.Timedelta(days=i)).date()))
        _resolver(a, pid, i % 2)
        pid = f"PRG-2025-{i + 101:04d}"
        _alta(a, pid, prob_interna=0.65, clase="MP", fecha_resolucion=str((pd.Timestamp("2025-01-02") + pd.Timedelta(days=i)).date()))
        _resolver(a, pid, i % 2)
    a.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2025-0001", "estado": "VIGENTE",
                               "celda": {"clase": "RV", "horizonte": "H3", "metodo": None}})
    a.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2025-0002", "estado": "PROPUESTO",
                               "celda": {"clase": "MP", "horizonte": "H3", "metodo": None}})
    res = Evaluador(a, None, None, _cfg(), None).revisar_certificados(AS_OF)
    assert res["revocados"] == ["CERT-2025-0001"] and res["propuestas_retiradas"] == ["CERT-2025-0002"]
    f6 = a.estado("F6", clave="id")
    assert f6["CERT-2025-0001"]["estado"] == "REVOCADO" and f6["CERT-2025-0002"]["estado"] == "REVOCADO"


# ================================================================================================ PA-03 · muestra efectiva
def _icc_a_mano(grupos: list[list[float]]) -> float:
    """ICC(1) por ANOVA escrita con bucles, independiente de la implementación vectorizada."""
    y = [v for g in grupos for v in g]
    n, k = len(y), len(grupos)
    media = sum(y) / n
    medias = [sum(g) / len(g) for g in grupos]
    msb = sum(len(g) * (mg - media) ** 2 for g, mg in zip(grupos, medias)) / (k - 1)
    msw = sum((v - mg) ** 2 for g, mg in zip(grupos, medias) for v in g) / (n - k)
    n0 = (n - sum(len(g) ** 2 for g in grupos) / n) / (k - 1)
    return min(max((msb - msw) / (msb + (n0 - 1) * msw), 0.0), 1.0)


def test_pa03_n_efectiva_kish_con_icc_por_anova():
    grupos = [[0.3, 0.5, -0.2], [-0.6, -0.4], [0.7, 0.1, 0.4, 0.6], [-0.3, -0.5, -0.1]]
    fechas = [f"2025-0{j + 1}-01" for j, g in enumerate(grupos) for _ in g]
    r = ev.n_efectiva(fechas, [v for g in grupos for v in g])
    rho = _icc_a_mano(grupos)
    assert 0 < rho < 1 and r["rho"] == pytest.approx(rho)
    assert r["conglomerados"] == 4 and r["m_medio"] == pytest.approx(12 / 4)
    assert r["n_eff"] == pytest.approx(12 / (1 + (3 - 1) * rho))
    # casos límite: una fecha por PRG ⇒ n_eff = n; misma fecha ⇒ ρ no estimable, 1 (falla cerrado) ⇒ n_eff = 1
    assert ev.n_efectiva([f"d{i}" for i in range(7)], np.linspace(-0.5, 0.5, 7))["n_eff"] == pytest.approx(7)
    assert ev.n_efectiva(["d"] * 7, np.linspace(-0.5, 0.5, 7))["n_eff"] == pytest.approx(1)
    # ρ negativa se recorta a 0
    assert ev.n_efectiva(["a", "a", "b", "b"], [1.0, -1.0, 1.0, -1.0])["rho"] == 0.0


def test_pa03_n_efectiva_falla_cerrado():
    with pytest.raises(ValueError):
        ev.n_efectiva(["2025-01-01", None], [0.1, 0.2])
    with pytest.raises(ValueError):
        ev.n_efectiva(["2025-01-01"], [0.1, 0.2])
    with pytest.raises(ValueError):
        ev.n_efectiva(["2025-01-01", "2025-01-02"], [0.1, float("nan")])
    with pytest.raises(ValueError):
        ev.n_efectiva(None, [0.1])


def test_pa03_bootstrap_por_conglomerados_de_fecha():
    rng = np.random.default_rng(3)
    p = rng.choice([0.3, 0.7], 60)
    o = (rng.random(60) < p).astype(int)
    fechas = [f"2025-01-{1 + i // 3:02d}" for i in range(60)]           # 20 fechas de 3 PRG
    a = ev.bss_conglomerados(p, o, [0.5] * 60, fechas, 300, 0.9, 7, 10)
    b = ev.bss_conglomerados(p, o, [0.5] * 60, fechas, 300, 0.9, 7, 10)
    assert a == b and a["conglomerados"] == 20 and None not in a["ic"] and a["ic"][0] <= a["valor"] <= a["ic"][1]
    assert a["metodo"] == "bootstrap por conglomerados de fecha"
    pocas = ev.bss_conglomerados(p, o, [0.5] * 60, fechas, 300, 0.9, 7, 21)  # 20 fechas < 21: sin IC
    assert pocas["ic"] == [None, None] and pocas["valor"] == a["valor"]
    m = ev.evaluar_celda(p, o, [0.5] * 60, 0.5, 300, 50, fechas=fechas, min_conglomerados=10)
    assert m["bss"]["metodo"] == "bootstrap por conglomerados de fecha" and m["n_eff"] <= 60
    with pytest.raises(ValueError, match="min_conglomerados"):
        ev.evaluar_celda(p, o, [0.5] * 60, 0.5, 50, 50, fechas=fechas)


def test_pa03_criterio_exige_n_eff():
    base = {"n": 200, "bss": {"ic": [0.1, 0.2]}, "calibracion": {"ece": 0.01}, "ece_nulo": {"q90": 0.05}}
    assert ev.criterio_certificado({**base, "n_eff": 150.0}, 100)["certificable"]
    crit = ev.criterio_certificado({**base, "n_eff": 60.0}, 100)
    assert not crit["certificable"] and crit["motivos"] == ["n_eff = 60.0 < 100 (n nominal = 200)"]
    assert (crit["n"], crit["n_eff"]) == (200, 60.0)
    sin = ev.criterio_certificado(base, 100)                               # sin n_eff no se certifica
    assert not sin["certificable"] and "n_eff no disponible" in sin["motivos"][0]


def test_pa03_certificado_guarda_n_y_n_eff(tmp_path):
    a = _almacen(tmp_path)
    _celda_habil(a, fechas=None)
    cert = Evaluador(a, None, None, _cfg(), None).revisar_certificados(AS_OF)["emitidos"][0]
    assert cert["n"] == 150 and cert["n_eff"] == pytest.approx(150) and cert["muestra_efectiva"]["conglomerados"] == 150
    assert cert["bss_ic_metodo"] == "bootstrap por conglomerados de fecha"


def test_pa03_pronosticos_duplicados_en_la_misma_fecha_no_certifican(tmp_path):
    """90 pronósticos hábiles e independientes replicados dos veces en su fecha (mismo p y mismo resultado): con la n
    nominal (180) la celda certificaba; con n_eff = 90 < 100, no."""
    a = _almacen(tmp_path)
    rng = np.random.default_rng(1)
    for i in range(90):
        p = float(rng.choice([0.3, 0.7]))
        o = int(rng.random() < p)
        for j in range(2):
            pid = f"PRG-2025-{2 * i + j + 1:04d}"
            _alta(a, pid, prob_interna=p, fecha_resolucion=str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date()))
            _resolver(a, pid, o)
    res = Evaluador(a, None, None, _cfg(), None).revisar_certificados(AS_OF)
    crit = res["evaluadas"]["RF|H3"]
    assert res["emitidos"] == [] and crit["n"] == 180 and crit["n_eff"] == pytest.approx(90)
    assert crit["motivos"] == ["n_eff = 90.0 < 100 (n nominal = 180)"]


def test_pa03_conglomerado_por_fecha_de_resolucion_y_si_falta_de_emision(tmp_path):
    a = _almacen(tmp_path)
    for i in range(20):                       # 4 fechas de emisión × 5 PRG con el mismo residuo dentro de cada fecha
        g = i // 5
        pid = f"PRG-2025-{i + 1:04d}"
        _alta(a, pid, clase="RV", prob_interna=0.65, fecha_emision=f"2025-0{g + 1}-01")
        _resolver(a, pid, g % 2)
        pid = f"PRG-2025-{i + 21:04d}"        # mismas emisiones, pero cada uno con su fecha de resolución
        _alta(a, pid, clase="MP", prob_interna=0.65, fecha_emision=f"2025-0{g + 1}-01",
              fecha_resolucion=str((pd.Timestamp("2025-07-01") + pd.Timedelta(days=i)).date()))
        _resolver(a, pid, g % 2)
    m = Evaluador(a, None, None, _cfg(), None).metricas(AS_OF)
    assert m["RV|H3"]["n_eff"] == pytest.approx(4) and m["RV|H3"]["muestra_efectiva"]["conglomerados"] == 4
    assert m["MP|H3"]["n_eff"] == pytest.approx(20)


def test_pa03_minimo_de_conglomerados_desde_la_configuracion(tmp_path):
    a = _almacen(tmp_path)
    _celda_habil(a)
    assert config_pruebas()["evaluacion"]["min_conglomerados_bootstrap"] == 10
    res = Evaluador(a, None, None, _cfg(min_conglomerados_bootstrap=151), None).revisar_certificados(AS_OF)
    assert res["emitidos"] == [] and any("IC del BSS None" in m for m in res["evaluadas"]["RF|H3"]["motivos"])
    for malo in (1, 2.5, True, "10"):
        with pytest.raises(ValueError, match="min_conglomerados_bootstrap"):
            Evaluador(None, None, None, _cfg(min_conglomerados_bootstrap=malo), None)


# ================================================================================================ PA-21 · Analista
def test_pa21_brier_del_analista_frente_a_prospectiva(tmp_path):
    a = _almacen(tmp_path)
    casos = [(0.65, 0.9, 1), (0.65, 0.8, 1), (0.65, 0.2, 0), (0.65, 0.6, 0), (0.65, None, 1), (0.65, 1.5, 1), (0.65, "x", 0)]
    for i, (pi, pa, o) in enumerate(casos):
        pid = f"PRG-2025-{i + 1:04d}"
        _alta(a, pid, prob_interna=pi, prob_analista=pa, fecha_resolucion=f"2025-11-{i + 1:02d}")
        _resolver(a, pid, o)
    _alta(a, "PRG-2025-0100", clase="MP", fecha_resolucion="2025-11-20")   # celda sin prob_analista
    _resolver(a, "PRG-2025-0100", 1)
    e = Evaluador(a, None, None, _cfg(), None)
    m = e.metricas(AS_OF)
    av = m["RF|H3"]["analista_vs_prospectiva"]
    validos = casos[:4]
    b_a = sum((pa - o) ** 2 for _, pa, o in validos) / 4
    b_p = sum((pi - o) ** 2 for pi, _, o in validos) / 4
    assert av["n"] == 4 and av["invalidos"] == 2
    assert av["brier_analista"] == pytest.approx(b_a) and av["brier_prospectiva"] == pytest.approx(b_p)
    assert av["diferencia"] == pytest.approx(b_a - b_p) and av["diferencia"] < 0
    assert "analista_vs_prospectiva" not in m["MP|H3"]
    # solo se informa: el resto de las métricas de la celda no cambia
    assert m["RF|H3"]["n"] == 7 and m["RF|H3"]["brier"] == pytest.approx(np.mean([(0.65 - o) ** 2 for _, _, o in casos]))
    assert math.isfinite(e.metricas(AS_OF, completas=True)["RF|H3"]["analista_vs_prospectiva"]["brier_analista"])
