"""T-180 QA r01 · ataques del revisor al criterio que CT-04 aplica ahora al soporte de un certificado.

¿Entra en vigor un certificado de habilidad débil? ¿Vale un soporte que pidió otro agente? ¿Cruzan el criterio unas cifras
dentro de la tolerancia? ¿Salta la revocación con certificados legítimos (una celda, dos celdas con Holm, CT-10
DENTRO_TOLERANCIA de verdad, emisión directa, certificados de T-163 sin `horizonte`, revisiones posteriores con más PRG)?

Las pruebas `test_hNN_*` afirman lo esperado y FALLAN mientras el hallazgo NN de qa.md siga abierto. El resto deben pasar.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-180/revisores/r01_01_ataques.py
"""
import copy
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))
from conftest import certificado_con_reejecucion, nuevo_bloque  # noqa: E402
from test_fase4_huecos import _sembrar_celda  # noqa: E402
from test_t160_reejecucion_certificado import REVISION, TOL, _alterar_ficha, _bloque, _con_ficha, _durante  # noqa: E402

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.evaluador import campos_certificado  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from bloque_a.motor.servicio import Motor  # noqa: E402


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _propuesto(b):
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["estado"] == "PROPUESTO" and b.evaluador.motivo_sin_reejecucion(cert) is None
    return cert


def _peticion(b, celda, entradas, tasa_base, con_horizonte=True):
    prm = {**b.evaluador._parametros_certificado(), "tasa_base": tasa_base, "metodo": celda.get("metodo")}
    if con_horizonte:
        prm["horizonte"] = celda["horizonte"]
    return {"operacion": "FC-EVAL-001", "plan": "PLAN_MIN", "clase": celda["clase"], "horizonte": celda["horizonte"],
            "datos": [{"valores": entradas}], "parametros": prm, "fecha_corte": REVISION}


def _forjar(b, cid, celda, calc_id, rex_id, estado="PROPUESTO"):
    s = b.almacen.estado("RC")[calc_id]
    cert = {"tipo_entrada": "CERT", "id": cid, "estado": estado, "celda": dict(celda),
            **campos_certificado(s["resultado"]["payload"]), "holm_superado": True, "calc_soporte": calc_id,
            "curva_fiabilidad": calc_id, "huella_entradas": s["datos"][0]["huella"], "reejecucion": rex_id}
    b.almacen.escribir("F6", "AG-20", cert)
    return cert


def _con_payload(b, c, cambio_soporte, cambio_cert=None):
    """Contexto con el payload del soporte cambiado y el CERT- con sus cifras (o con `cambio_cert` aplicado)."""
    ctx = b.evaluador._contexto_reejecucion()
    s = copy.deepcopy(ctx["rc"][c["calc_soporte"]])
    cambio_soporte(s["resultado"]["payload"])
    ctx["rc"][c["calc_soporte"]] = s
    cert = {**c, **campos_certificado(s["resultado"]["payload"])}
    if cambio_cert:
        cambio_cert(cert)
    return ctx, cert


# ================================================================================ cifras dentro de la tolerancia que cruzan el criterio
@pytest.mark.parametrize("soporte, cert, fragmento", [
    # n_eff del soporte una parte en 10⁹ por debajo de 100; el CERT- dice 100 (dentro de la tolerancia de CT-10)
    (lambda m: m.update(n_eff=100 * (1 - 1e-9)), lambda c: c.update(n_eff=100.0), "n_eff"),
    # extremo inferior del IC −10⁻²¹ en el soporte y +10⁻²¹ en el CERT- (iguales para `comparar` por su suelo absoluto)
    (lambda m: m["bss"].update(ic=[-1e-21, m["bss"]["ic"][1]]), lambda c: c.update(bss_ic90=[1e-21, c["bss_ic90"][1]]),
     "extremo inferior del IC"),
    # ECE una parte en 10⁹ por encima del q90 del nulo en el soporte, una por debajo en el CERT-
    (lambda m: m["calibracion"].update(ece=m["ece_nulo"]["q90"] * (1 + 1e-9)),
     lambda c: c.update(ece=c["ece_nulo_q90"] * (1 - 1e-9)), "q90 nulo"),
])
def test_cifras_del_cert_dentro_de_tolerancia_no_tapan_un_soporte_que_no_cumple(tmp_path, universo, soporte, cert, fragmento):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    ctx, falso = _con_payload(b, c, soporte, cert)
    motivo = b.evaluador.motivo_sin_reejecucion(falso, ctx)
    assert motivo and "no cumple el criterio del certificado" in motivo and fragmento in motivo, motivo


def test_la_p_de_dm_justo_en_alfa_vale_con_si_y_no_con_dentro_de_tolerancia(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    alfa = float(b.evaluador._umbrales_certificado()[2])
    ctx, cert = _con_payload(b, c, lambda m: m["dm_hln"].update(p_unilateral=alfa))
    assert b.evaluador.motivo_sin_reejecucion(cert, ctx) is None
    r = copy.deepcopy(ctx["rc"][c["reejecucion"]])
    r["reejecucion"]["coincide"] = "DENTRO_TOLERANCIA"
    ctx["rc"][c["reejecucion"]] = r
    assert "alfa Holm" in b.evaluador.motivo_sin_reejecucion(cert, ctx)


# ================================================================================ habilidad débil
def test_una_celda_debil_por_la_via_normal_no_propone_y_su_soporte_forjado_no_entra(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar(REVISION)
    _sembrar_celda(b, "RV", 150, lambda p: 0.5 + 0.6 * (p - 0.5), 5001)
    assert b.evaluador.revisar_certificados(REVISION)["emitidos"] == []
    v = [p for p in b.evaluador.resueltos(REVISION) if p["clase"] == "RV"]
    e, tb = b.evaluador._entradas_celda(v)
    celda = {"clase": "RV", "horizonte": "H3", "metodo": None}
    res = b.motor.servir(_peticion(b, celda, e, tb), "AG-20")
    rex = b.motor.reejecutar(res["calc_id"], "forja", "AG-20")
    falso = _forjar(b, "CERT-2026-0960", celda, res["calc_id"], rex["calc_id"])
    with pytest.raises(ValueError, match="no cumple el criterio"):
        b.evaluador.aprobar_certificados([falso["id"]], REVISION)
    b.almacen.escribir("F6", "AG-20", {**{k: v for k, v in falso.items()}, "estado": "VIGENTE"})   # ni escrito VIGENTE
    assert b.evaluador.certificados_vigentes(REVISION) == []


def test_una_celda_debil_con_los_prg_buenos_elegidos_a_mano_entra_limite_declarado(tmp_path, universo):
    """Límite declarado (INC-T160-01): un soporte con un subconjunto escogido de los PRG REALES de la celda (los acertados) cumple
    el criterio y pasa CT-04. Exige pedir el soporte y la CT-10 como AG-20. Documenta el comportamiento (pasa)."""
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar(REVISION)
    _sembrar_celda(b, "RV", 300, lambda p: 0.5 + 0.6 * (p - 0.5), 5001)
    v = [p for p in b.evaluador.resueltos(REVISION) if p["clase"] == "RV"]
    buenos = [p for p in v if (p["prob_interna"] > 0.5) == bool(p["resolucion"]["resultado_binario"])]
    elegidos = buenos[:120] + [p for p in v if p not in buenos][:30]
    e, tb = b.evaluador._entradas_celda(elegidos)
    celda = {"clase": "RV", "horizonte": "H3", "metodo": None}
    res = b.motor.servir(_peticion(b, celda, e, tb), "AG-20")
    rex = b.motor.reejecutar(res["calc_id"], "forja", "AG-20")
    falso = _forjar(b, "CERT-2026-0961", celda, res["calc_id"], rex["calc_id"])
    assert b.evaluador.motivo_sin_reejecucion(falso) is None


# ================================================================================ soporte pedido por otro agente
@pytest.mark.parametrize("solicitante", ["AG-18", "AG-02", "ag-20", "AG-20 "])
def test_un_soporte_pedido_por_otro_no_vale(tmp_path, universo, solicitante):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    s = b.almacen.estado("RC")[c["calc_soporte"]]
    otro = Motor(b.almacen, None, b.cfg)
    res = otro.servir(_peticion(b, c["celda"], s["datos"][0]["valor"], s["parametros"]["tasa_base"]), solicitante)
    if not str(res.get("estado", "")).startswith("SERVED"):
        return                                                   # el Motor ya no lo sirve: tampoco hay soporte
    rex = b.motor.reejecutar(res["calc_id"], "forja", "AG-20")
    falso = _forjar(b, "CERT-2026-0962", c["celda"], res["calc_id"], rex["calc_id"])
    assert "no lo pidió el Evaluador" in b.evaluador.motivo_sin_reejecucion(falso)


def test_si_otro_agente_pide_antes_la_misma_peticion_la_celda_no_se_certifica_y_falla_cerrado(tmp_path, universo):
    """La clave de la caché no lleva el solicitante: si otro agente pidiera antes, en el mismo Motor y con la misma fecha,
    exactamente la petición del Evaluador, la celda recibe ese `calc_id` y no se certifica (falla cerrado). Documenta (pasa)."""
    b = _bloque(tmp_path, universo)
    k = ("RF", "H3", None)
    v = [p for p in b.evaluador.resueltos(REVISION) if (p["clase"], p["horizonte"], p.get("metodo")) == k]
    e, tb = b.evaluador._entradas_celda(v)
    r = b.motor.servir(_peticion(b, {"clase": "RF", "horizonte": "H3", "metodo": None}, e, tb), "AG-18")
    assert str(r["estado"]).startswith("SERVED")
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and "no lo pidió el Evaluador" in res["sin_reejecucion_coincidente"]["RF|H3"]


# ================================================================================ la revocación no salta con legítimos
def test_un_legitimo_aprobado_sigue_en_revisiones_posteriores_con_mas_prg(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.evaluador.aprobar_certificados([c["id"]], REVISION)
    for fecha, desde in (("2026-02-02", 7001), ("2026-03-02", 8001)):
        b.reloj.fijar(fecha)
        _sembrar_celda(b, "RF", 30, lambda p: p, desde)
        r = b.evaluador.revisar_certificados(fecha)
        assert r["revocados"] == [] and r["vigentes_sin_reejecucion"] == {} and r["emitidos"] == []
        assert [x["id"] for x in b.evaluador.certificados_vigentes(fecha)] == [c["id"]]


def test_dos_celdas_legitimas_con_holm_se_aprueban_y_siguen(tmp_path, universo):
    b = _bloque(tmp_path, universo, clases=(("RF", "hábil"), ("RV", "hábil")))
    res = b.evaluador.revisar_certificados(REVISION)
    ids = sorted(x["id"] for x in res["emitidos"])
    assert len(ids) == 2, res["evaluadas"]
    b.evaluador.aprobar_certificados(ids, REVISION)
    r2 = b.evaluador.revisar_certificados(REVISION)
    assert r2["revocados"] == [] and sorted(x["id"] for x in b.evaluador.certificados_vigentes(REVISION)) == ids


def test_un_legitimo_con_una_ct10_dentro_de_tolerancia_de_verdad_entra_y_sigue(tmp_path, universo, monkeypatch):
    """La CT-10 la hace una ficha que da el Brier una décima de tolerancia distinto: DENTRO_TOLERANCIA de verdad, en el RC."""
    b = _bloque(tmp_path, universo)
    _, alterada = _alterar_ficha(monkeypatch, 1 + TOL / 10)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    monkeypatch.undo()
    assert b.almacen.estado("RC")[cert["reejecucion"]]["reejecucion"]["coincide"] == "DENTRO_TOLERANCIA"
    assert [h["id"] for h in b.evaluador.aprobar_certificados([cert["id"]], REVISION)] == [cert["id"]]
    r = b.evaluador.revisar_certificados(REVISION)
    assert r["revocados"] == [] and [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == [cert["id"]]


def test_la_emision_directa_legitima_sigue_vigente(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    b.cfg["aprendizaje"]["solo_endurecer"] = False
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["estado"] == "VIGENTE"
    assert b.evaluador.revisar_certificados(REVISION)["revocados"] == []
    assert [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == [cert["id"]]


def test_un_certificado_de_t163_sin_horizonte_en_el_soporte_sigue_valiendo(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    k = ("RF", "H3", None)
    v = [p for p in b.evaluador.resueltos(REVISION) if (p["clase"], p["horizonte"], p.get("metodo")) == k]
    e, tb = b.evaluador._entradas_celda(v)
    celda = {"clase": "RF", "horizonte": "H3", "metodo": None}
    res = b.motor.servir(_peticion(b, celda, e, tb, con_horizonte=False), "AG-20")
    assert "horizonte" not in b.almacen.estado("RC")[res["calc_id"]]["parametros"]
    rex = b.motor.reejecutar(res["calc_id"], "certificado de T-163", "AG-20")
    viejo = _forjar(b, "CERT-2026-0963", celda, res["calc_id"], rex["calc_id"], estado="VIGENTE")
    r = b.evaluador.revisar_certificados(REVISION)
    assert r["revocados"] == [] and r["emitidos"] == []
    assert [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == [viejo["id"]]


def test_subir_un_umbral_de_la_configuracion_revoca_y_bajarlo_no_resucita(tmp_path, universo):
    """Endurecer la configuración revoca el VIGENTE (con su motivo); volver al valor de la entrega no lo devuelve a la vida:
    la celda se vuelve a proponer por la vía normal."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.evaluador.aprobar_certificados([c["id"]], REVISION)
    b.cfg["evaluacion"]["min_certificar"] = int(c["n_eff"]) + 1
    r = b.evaluador.revisar_certificados(REVISION)
    assert r["revocados"] == [c["id"]] and "n_eff" in r["vigentes_sin_reejecucion"][c["id"]]
    del b.cfg["evaluacion"]["min_certificar"]
    assert b.evaluador.certificados_vigentes(REVISION) == []
    nuevo, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert nuevo["estado"] == "PROPUESTO" and nuevo["id"] != c["id"]


def test_el_ayudante_no_debilita_las_pruebas_de_publicacion(tmp_path, universo):
    """El certificado del ayudante habilita probabilidades solo en su celda (control de lo que usan PB-32 y R13)."""
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha("2026-06-05")
    cert = certificado_con_reejecucion(b.almacen, {"clase": "RV", "horizonte": "H3", "metodo": "ACC-MOM-001"}, motor=b.motor)
    assert pd.notna(cert["n_eff"]) and cert["n_eff"] >= 100 and b.evaluador.motivo_sin_reejecucion(cert) is None
    r = b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
    altas = [p for p in b.almacen.estado("F4").values() if p.get("tipo_entrada") == "ALTA"]
    assert any(p["prob_publicada"] is not None for p in altas)
    for p in altas:
        assert (p["prob_publicada"] is not None) == (p["horizonte"] == "H3" and p.get("metodo") == "ACC-MOM-001")
    assert r["evaluacion"]["certificados"]["revocados"] == []


def test_en_el_borde_ct04_no_es_mas_estricto_que_la_propuesta_con_dentro_de_tolerancia(tmp_path, universo):
    """Mata V01 de r01_02_mutantes.py: ECE del soporte a q90·(1 − 3·tol) con la CT-10 DENTRO_TOLERANCIA. Con un paso de holgura
    (lo que aguantó la propuesta) cumple; con dos, no. Un CT-04 más estricto revocaría certificados legítimos en el borde."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    ctx, cert = _con_payload(b, c, lambda m: m["calibracion"].update(ece=m["ece_nulo"]["q90"] * (1 - 3 * TOL)))
    r = copy.deepcopy(ctx["rc"][c["reejecucion"]])
    r["reejecucion"]["coincide"] = "DENTRO_TOLERANCIA"
    ctx["rc"][c["reejecucion"]] = r
    assert b.evaluador.motivo_sin_reejecucion(cert, ctx) is None
