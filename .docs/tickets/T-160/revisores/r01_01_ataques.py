"""T-160 QA r01 · ataques del revisor a la re-ejecución CT-10 antes de certificar (PB-32).

¿Sale algún certificado sin una re-ejecución CT-10 coincidente que lo sostenga? Se prueba por revisar_certificados y por CT-04
(`aprobar_certificados`, también por `Bloque.decision`) con propuestas falsas en F6, con re-ejecuciones de otro certificado,
con un Motor que falla a medias o que devuelve lo que no escribe, con la materialidad de extremo a extremo (un umbral de la
configuración a una fracción de la tolerancia), con FC-EVAL-001 con entradas malas y con la idempotencia.

Las pruebas `test_hNN_*` afirman lo esperado y FALLAN mientras el hallazgo NN sigue abierto (ver qa.md). El resto deben pasar.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-160/revisores/r01_01_ataques.py
"""
import sys
from pathlib import Path

import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))
from conftest import nuevo_bloque  # noqa: E402
from test_t160_reejecucion_certificado import REVISION, TOL, _alterar_ficha, _bloque, _certs, _con_ficha, _durante  # noqa: E402

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _propuesto(b):
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["estado"] == "PROPUESTO" and b.evaluador.motivo_sin_reejecucion(cert) is None
    return cert


def _forjar(b, cid, base, **cambios):
    """Un PROPUESTO escrito en F6 con la identidad del Evaluador (AG-20, el único propietario de F6)."""
    e = {k: v for k, v in base.items() if not k.startswith("_")}
    e.update({"tipo_entrada": "CERT", "id": cid, "estado": "PROPUESTO", **cambios})
    b.almacen.escribir("F6", "AG-20", e)
    return e


# ------------------------------------------------------------------------------------------------ CT-04 con propuestas falsas
def test_h01_ct04_no_aprueba_un_propuesto_que_cita_la_reejecucion_de_otro_certificado_con_otras_cifras(tmp_path, universo):
    """Un PROPUESTO falso de la misma celda y otro método, con cifras infladas, que cita el `calc_soporte` y la `reejecucion`
    del certificado legítimo: su re-ejecución coincide, pero no es la suya ni sostiene sus cifras."""
    b = _bloque(tmp_path, universo)
    legit = _propuesto(b)
    falso = _forjar(b, "CERT-2026-0950", legit, celda={"clase": "RF", "horizonte": "H3", "metodo": "ACC-MOM-001"},
                    bss=0.9, bss_ic90=[0.8, 0.95], n_eff=10_000)
    with pytest.raises(ValueError):
        b.evaluador.aprobar_certificados([falso["id"]], REVISION)
    assert b.evaluador.certificados_vigentes(REVISION) == []


def test_h01b_ct04_no_aprueba_dos_propuestos_con_la_misma_reejecucion(tmp_path, universo):
    """La re-ejecución de un certificado no puede sostener dos: con el legítimo ya aprobado, uno falso de otro método que cite
    sus mismos CALC- no debería entrar en vigor."""
    b = _bloque(tmp_path, universo)
    legit = _propuesto(b)
    b.evaluador.aprobar_certificados([legit["id"]], REVISION)
    falso = _forjar(b, "CERT-2026-0951", legit, celda={"clase": "RF", "horizonte": "H3", "metodo": "ACC-MOM-001"})
    r = b.decision({"aprobar_certificados": [falso["id"]]}, REVISION)
    assert r["certificados_aprobados"] == []


def test_ct04_rechaza_un_propuesto_que_cita_un_soporte_de_otra_celda(tmp_path, universo):
    b = _bloque(tmp_path, universo, clases=(("RF", "hábil"), ("RV", "hábil")))
    res = b.evaluador.revisar_certificados(REVISION)
    rf = next(c for c in res["emitidos"] if c["celda"]["clase"] == "RF")
    falso = _forjar(b, "CERT-2026-0952", rf, celda={"clase": "IDX", "horizonte": "H3", "metodo": None})
    with pytest.raises(ValueError, match="no es un servicio FC-EVAL-001 de la celda IDX"):
        b.evaluador.aprobar_certificados([falso["id"]], REVISION)


def test_ct04_rechaza_campos_de_tipo_raro(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    legit = _propuesto(b)
    for i, (rex, sop) in enumerate(((None, None), (["x"], legit["calc_soporte"]), (legit["reejecucion"], 7),
                                    ({"calc_id": legit["reejecucion"]}, legit["calc_soporte"]), ("", ""))):
        f = _forjar(b, f"CERT-2026-096{i}", legit, reejecucion=rex, calc_soporte=sop)
        with pytest.raises(ValueError, match="re-ejecución CT-10"):
            b.evaluador.aprobar_certificados([f["id"]], REVISION)


def test_ct04_un_lote_con_uno_malo_no_escribe_nada(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    legit = _propuesto(b)
    malo = _forjar(b, "CERT-2026-0970", legit, celda={"clase": "MP", "horizonte": "H3", "metodo": None})
    n = len(b.almacen.leer("F6"))
    with pytest.raises(ValueError):
        b.evaluador.aprobar_certificados([legit["id"], malo["id"]], REVISION)
    assert len(b.almacen.leer("F6")) == n and b.evaluador.certificados_vigentes(REVISION) == []


def test_h02_un_vigente_escrito_en_f6_sin_reejecucion_no_habilita_probabilidades(tmp_path, universo):
    """El control está solo en la emisión y en CT-04: `certificados_vigentes`, que es lo que leen la síntesis, G3 y el
    backtest, da por bueno cualquier CERT VIGENTE de F6 aunque no cite re-ejecución (límite declarado para los anteriores a
    T-160, pero vale igual para uno escrito hoy)."""
    b = _bloque(tmp_path, universo)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2026-0980", "estado": "VIGENTE",
                                       "celda": {"clase": "RF", "horizonte": "H3", "metodo": None}})
    assert [c["id"] for c in b.evaluador.certificados_vigentes(REVISION)] == []


# ------------------------------------------------------------------------------------------------ Motor que falla a medias
def test_reejecucion_que_escribe_si_y_luego_lanza_no_deja_certificado_y_se_reintenta(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    original = b.motor.reejecutar

    def escribe_y_lanza(calc_id, motivo, solicitante="AG-18"):
        original(calc_id, motivo, solicitante)
        raise OSError("disco lleno después de escribir")
    monkeypatch.setattr(b.motor, "reejecutar", escribe_y_lanza)
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b) and "imposible (OSError" in res["sin_reejecucion_coincidente"]["RF|H3"]
    monkeypatch.undo()
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert b.evaluador.motivo_sin_reejecucion(cert) is None


def test_servir_que_lanza_no_deja_certificado(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    monkeypatch.setattr(b.motor, "servir", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("caída")))
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and "no ha podido servir" in res["sin_reejecucion_coincidente"]["RF|H3"]


@pytest.mark.parametrize("respuesta", [None, [], "SI", {"estado": "SERVED"}, {"estado": "SERVED", "calc_id": 5},
                                       {"estado": "REJECTED", "calc_id": "CALC-2026-0001"}])
def test_servir_con_respuestas_raras_no_deja_certificado(tmp_path, universo, monkeypatch, respuesta):
    b = _bloque(tmp_path, universo)
    monkeypatch.setattr(b.motor, "servir", lambda *a, **k: respuesta)
    assert b.evaluador.revisar_certificados(REVISION)["emitidos"] == [] and not _certs(b)


@pytest.mark.parametrize("solo_endurecer", [True, False])
def test_h03_una_reejecucion_que_dice_si_sin_estar_en_el_registro_no_certifica(tmp_path, universo, monkeypatch, solo_endurecer):
    """Un Motor (o un doble) que responde `coincide: SI` sin haber escrito la REEJECUCION en el RC. Con solo_endurecer, CT-04
    lo para después; sin él, el certificado nace VIGENTE sin que nada mire el RC."""
    b = _bloque(tmp_path, universo)
    b.cfg["aprendizaje"]["solo_endurecer"] = solo_endurecer
    monkeypatch.setattr(b.motor, "reejecutar", lambda calc_id, motivo, solicitante="AG-18":
                        {"coincide": "SI", "categoria": None, "diferencias": [], "calc_id": "CALC-2026-9998", "diagnostico": "x"})
    res = b.evaluador.revisar_certificados(REVISION)
    assert "CALC-2026-9998" not in b.almacen.estado("RC")
    assert res["emitidos"] == [] and b.evaluador.certificados_vigentes(REVISION) == []


# ------------------------------------------------------------------------------------------------ materialidad, de extremo a extremo
def _con_ece_max_al_borde(b, factor):
    """ece_max de la configuración a una fracción de la tolerancia por encima del ECE real de la celda."""
    from bloque_a.motor import evaluacion as ev
    v = [p for p in b.evaluador.resueltos(REVISION) if (p["clase"], p["horizonte"]) == ("RF", "H3")]
    e, tb = b.evaluador._entradas_celda(v)
    prm = b.evaluador._parametros_certificado()
    m = ev.evaluar_celda(e["p"], e["o"], e["p_ref"], tb, prm["replicas"], prm["simulaciones"], prm["nivel"],
                         prm["semilla_bootstrap"], prm["h"], fechas=e["fechas"], min_conglomerados=prm["min_conglomerados"])
    ece = m["calibracion"]["ece"]
    assert ece < m["ece_nulo"]["q90"] and ece > 0
    b.cfg["evaluacion"]["ece_max"] = ece * (1 + factor)
    return ece


def test_materialidad_e2e_dentro_de_tolerancia_que_cruza_el_tope_de_ece_no_certifica(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _con_ece_max_al_borde(b, TOL / 10)
    _, alterada = _alterar_ficha(monkeypatch, 1 + TOL / 100)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))      # CT-10 DENTRO_TOLERANCIA
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b)
    assert "material" in res["sin_reejecucion_coincidente"]["RF|H3"] and "ECE" in res["sin_reejecucion_coincidente"]["RF|H3"]


def test_materialidad_e2e_el_mismo_borde_con_coincidencia_exacta_certifica(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _con_ece_max_al_borde(b, TOL / 10)
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["reejecucion_ct10"]["coincide"] == "SI" and "materialidad" not in cert["reejecucion_ct10"]


def test_materialidad_e2e_cifras_del_motor_dentro_de_tolerancia_suman_dos_pasos(tmp_path, universo, monkeypatch):
    from bloque_a.evaluador import holgura_tolerancia
    b = _bloque(tmp_path, universo)
    _, alterada = _alterar_ficha(monkeypatch, 1 + TOL / 100)
    _durante(b.motor, "servir", monkeypatch, _con_ficha(alterada))           # el servicio difiere; CT-10 recalcula sin alterar
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    d = cert["reejecucion_ct10"]
    assert d["cifras_frente_al_motor"] == "dentro de la tolerancia" and d["coincide"] == "DENTRO_TOLERANCIA"
    assert d["materialidad"]["holgura"] == pytest.approx(holgura_tolerancia(TOL, 2))


def test_fuera_de_tolerancia_por_poco_no_certifica(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _, alterada = _alterar_ficha(monkeypatch, 1 + 3 * TOL)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and "ERROR_ORIGINAL" in res["sin_reejecucion_coincidente"]["RF|H3"]


# ------------------------------------------------------------------------------------------------ idempotencia y orden
def test_dos_revisiones_seguidas_dejan_un_solo_certificado_y_no_vuelven_a_pedir_el_calculo(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _propuesto(b)
    n_rc = len(b.almacen.leer("RC"))
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and res["propuestas_retiradas"] == [] and len(_certs(b)) == 1
    assert len(b.almacen.leer("RC")) == n_rc


def test_aprobar_dos_veces_falla_la_segunda(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.evaluador.aprobar_certificados([c["id"]], REVISION)
    with pytest.raises(ValueError, match="no PROPUESTO"):
        b.evaluador.aprobar_certificados([c["id"]], REVISION)


def test_una_auditoria_ct10_posterior_que_no_coincide_no_impide_la_aprobacion(tmp_path, universo, monkeypatch):
    """Observación (bajo): CT-04 mira solo la re-ejecución que cita el certificado; si después otra CT-10 (del Auditor) del mismo
    cálculo de soporte da NO, la aprobación sigue adelante."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    _, alterada = _alterar_ficha(monkeypatch, 1 + 1e-3)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    assert b.motor.reejecutar(c["calc_soporte"], "auditoría", "AG-18")["coincide"] == "NO"
    monkeypatch.undo()
    assert [h["id"] for h in b.evaluador.aprobar_certificados([c["id"]], REVISION)] == [c["id"]]


# ------------------------------------------------------------------------------------------------ FC-EVAL-001 con entradas malas
@pytest.mark.parametrize("valores,params", [
    ({"fechas": ["2025-07-02"] * 3}, {"min_conglomerados": 2}),                     # menos fechas que pronósticos
    ({"fechas": ["2025-07-02"] * 80}, {"min_conglomerados": 2}),                    # más fechas que pronósticos
    ({"fechas": None}, {"min_conglomerados": 2}),
    ({"fechas": "2025-07-02"}, {"min_conglomerados": 2}),                           # una cadena, no una lista
    ({}, {"min_conglomerados": "x"}),                                               # sin fechas: el mínimo no se lee
])
def test_fc_eval_con_entradas_raras_no_lanza(tmp_path, universo, valores, params):
    b = nuevo_bloque(tmp_path, universo)
    p, o = [0.3, 0.7] * 30, [0, 1, 1, 1, 0, 0] * 10
    v = {"p": p, "o": o, **valores}
    r = b.motor.servir({"operacion": "FC-EVAL-001", "fecha_corte": REVISION, "datos": [{"valores": v}],
                        "parametros": {"replicas": 30, "simulaciones": 30, **params}}, "AG-20")
    assert isinstance(r, dict) and r.get("estado") in ("SERVED", "SERVED_WITH_LIMITATIONS", "RECHAZADO", "REJECTED"), r
    if valores.get("fechas") is not None and isinstance(valores["fechas"], list) and len(valores["fechas"]) != len(p):
        assert not str(r["estado"]).startswith("SERVED"), "fechas de otra longitud que los pronósticos y aun así servido"


@pytest.mark.parametrize("minimo", [0, -1, "x", None, True, 1.5])
def test_fc_eval_con_un_minimo_de_conglomerados_raro(tmp_path, universo, minimo):
    b = nuevo_bloque(tmp_path, universo)
    p, o = [0.3, 0.7] * 30, [0, 1, 1, 1, 0, 0] * 10
    fechas = [f"2025-07-{1 + i // 2:02d}" for i in range(60)]
    r = b.motor.servir({"operacion": "FC-EVAL-001", "fecha_corte": REVISION, "datos": [{"valores": {"p": p, "o": o, "fechas": fechas}}],
                        "parametros": {"replicas": 30, "simulaciones": 30, "min_conglomerados": minimo}}, "AG-20")
    assert isinstance(r, dict) and "estado" in r
    print(minimo, r["estado"], r.get("motivo"), (r.get("resultado") or {}).get("bss", {}).get("ic"))


def test_la_tolerancia_es_la_de_la_ficha_y_el_catalogo_dice_1e_8():
    texto = (RAIZ.parent / "04_Motor_conocimiento_y_catalogo" / "Catálogo de cálculos del Motor - V5.0.md").read_text(encoding="utf-8")
    ficha = texto.split("### FC-EVAL-001")[1].split("###")[0]
    assert "1e-8 en métricas; 1e-6 en IC" in ficha
    assert servicio.IMPLEMENTADAS["FC-EVAL-001"]["tol"] == 1e-8 == TOL
