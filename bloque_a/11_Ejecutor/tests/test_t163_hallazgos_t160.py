"""T-163 · hallazgos de la QA r01 de T-160 (`.docs/tickets/T-160/qa.md`).

- H-01: CT-04 ata la re-ejecución al certificado (cifras, método, celda, entradas, orden y exclusividad) contra el Registro de
  cálculos.
- H-02 (decidido, INC-T160-01): un VIGENTE sin re-ejecución CT-10 coincidente no habilita probabilidades; la revisión lo revoca y
  vuelve a proponer la celda.
- H-03: la emisión directa (sin `solo_endurecer`) pasa la misma comprobación que CT-04.
- H-04: FC-EVAL-001 valida `min_conglomerados`.
- H-05: una CT-10 posterior del mismo soporte que no coincide invalida el certificado.
- H-06: pruebas que matan los mutantes M12 (la materialidad no mueve el q90 del nulo) y M17 (no se mira la ficha del soporte).

Todo con el cliente simulado y sin red. Cada prueba de fallo cerrado falla sin el cambio que cubre (ver pruebas.md del ticket).
"""
import numpy as np
import pytest
from bloque_a.evaluador import criterio_desfavorable, holgura_tolerancia
from bloque_a.motor import evaluacion as ev
from bloque_a.motor import servicio
from conftest import nuevo_bloque
from test_fase4_huecos import BUENA
from test_t160_reejecucion_certificado import (
    REVISION,
    TOL,
    _alterar_ficha,
    _bloque,
    _certs,
    _con_ficha,
    _durante,
    _incidencias,
)


def _propuesto(b):
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["estado"] == "PROPUESTO" and b.evaluador.motivo_sin_reejecucion(cert) is None
    return cert


def _reescribir(b, cert, **cambios):
    """Una entrada CERT más en F6 con el mismo id y algún campo cambiado (lo que vería CT-04 si alguien la escribiera)."""
    e = {k: v for k, v in cert.items() if not k.startswith("_")}
    e.update({"tipo_entrada": "CERT", "estado": "PROPUESTO", **cambios})
    b.almacen.escribir("F6", "AG-20", e)
    return e


def _no_aprueba(b, cid, fragmento):
    n = len(b.almacen.leer("F6"))
    with pytest.raises(ValueError, match=f"re-ejecución CT-10 coincidente.*{fragmento}"):
        b.evaluador.aprobar_certificados([cid], REVISION)
    assert len(b.almacen.leer("F6")) == n and b.evaluador.certificados_vigentes(REVISION) == []


# ================================================================================ H-01 · la re-ejecución es la de este certificado
@pytest.mark.parametrize("campo, valor", [("bss", "x1.001"), ("bss_ic90", "inflado"), ("n_eff", "x1.001"), ("ece", "x1.001"),
                                          ("ece_nulo_q90", "x1.001"), ("brier", "x1.001"), ("n", "+1"), ("bss_ic_metodo", "otro")])
def test_h01_ct04_no_aprueba_un_certificado_con_cifras_distintas_de_las_de_su_soporte(tmp_path, universo, campo, valor):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    nuevo = {"x1.001": lambda x: x * 1.001, "+1": lambda x: x + 1, "inflado": lambda _: [0.8, 0.95],
             "otro": lambda _: "bootstrap estacionario"}[valor](c[campo])
    _reescribir(b, c, **{campo: nuevo})
    _no_aprueba(b, c["id"], "las cifras del certificado no son las de")


def test_h01_dentro_de_la_tolerancia_de_ct10_las_cifras_valen(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    _reescribir(b, c, bss=c["bss"] * (1 + TOL / 10))
    assert [h["id"] for h in b.evaluador.aprobar_certificados([c["id"]], REVISION)] == [c["id"]]
    assert [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == [c["id"]]


def test_h01_ct04_no_aprueba_un_certificado_de_otro_metodo_que_el_de_su_soporte(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    assert b.almacen.estado("RC")[c["calc_soporte"]]["parametros"]["metodo"] is None        # la petición lleva el método
    _reescribir(b, c, celda={**c["celda"], "metodo": "ACC-MOM-001"})
    _no_aprueba(b, c["id"], "no es del método ACC-MOM-001")


def test_h01_un_soporte_sin_metodo_anterior_a_t163_no_vale(tmp_path, universo):
    """Un certificado de T-160 (soporte sin `metodo` en los parámetros ni `huella_entradas`) falla cerrado."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    s = b.almacen.estado("RC")[c["calc_soporte"]]
    pet = {"operacion": "FC-EVAL-001", "plan": "PLAN_MIN", "clase": "RF", "horizonte": "H3", "fecha_corte": s["as_of"],
           "datos": [{"valores": s["datos"][0]["valor"]}],
           "parametros": {k: v for k, v in s["parametros"].items() if k not in ("metodo", "clase")}}
    viejo = b.motor.servir(pet, "AG-20")["calc_id"]
    rex = b.motor.reejecutar(viejo, "prueba T-163", "AG-20")["calc_id"]
    falso = _reescribir(b, c, id="CERT-2026-0990", calc_soporte=viejo, curva_fiabilidad=viejo, reejecucion=rex)
    _no_aprueba(b, falso["id"], "sin método en el cálculo")


def test_h01_ct04_no_aprueba_un_certificado_con_otras_entradas(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    _reescribir(b, c, huella_entradas="0" * 16)
    _no_aprueba(b, c["id"], "no son las mismas")


def test_h01_cada_reejecucion_sirve_a_un_solo_certificado(tmp_path, universo):
    """Una copia exacta del certificado legítimo con otro id: todo coincide salvo que su re-ejecución ya la citó otro."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    copia = _reescribir(b, c, id="CERT-2026-0991")
    _no_aprueba(b, copia["id"], f"ya sostiene {c['id']}")
    assert [h["id"] for h in b.evaluador.aprobar_certificados([c["id"]], REVISION)] == [c["id"]]   # el primero sí
    with pytest.raises(ValueError, match="ya tiene un certificado VIGENTE"):
        b.evaluador.aprobar_certificados([copia["id"]], REVISION)
    assert [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == [c["id"]]


def test_h01_la_reejecucion_tiene_que_ser_posterior_al_soporte(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    ctx = b.evaluador._contexto_reejecucion()
    assert b.evaluador.motivo_sin_reejecucion(c, ctx) is None
    ctx["seq"][c["reejecucion"]] = ctx["seq"][c["calc_soporte"]]
    assert "no es posterior a" in b.evaluador.motivo_sin_reejecucion(c, ctx)
    ctx["seq"][c["reejecucion"]] = None
    assert "no es posterior a" in b.evaluador.motivo_sin_reejecucion(c, ctx)


@pytest.mark.parametrize("cambio", [{"resultado": None}, {"resultado": {"forma": "TABLA"}}, {"datos": "x"}, {"datos": []},
                                    {"parametros": None}])
def test_h01_un_soporte_mal_formado_no_lanza_y_no_vale(tmp_path, universo, cambio):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    ctx = b.evaluador._contexto_reejecucion()
    ctx["rc"][c["calc_soporte"]] = {**ctx["rc"][c["calc_soporte"]], **cambio}
    assert b.evaluador.motivo_sin_reejecucion(c, ctx)


# ================================================================================ H-05 · una CT-10 posterior que no coincide
def test_h05_una_ct10_posterior_del_mismo_soporte_que_no_coincide_impide_la_aprobacion(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    _, alterada = _alterar_ficha(monkeypatch, 1 + 1e-3)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    auditoria = b.motor.reejecutar(c["calc_soporte"], "auditoría", "AG-18")
    assert auditoria["coincide"] == "NO"
    monkeypatch.undo()
    _no_aprueba(b, c["id"], f"posterior de {c['calc_soporte']} no coincide \\({auditoria['calc_id']}\\)")


def test_h05_una_ct10_posterior_que_coincide_no_impide_la_aprobacion(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    assert b.motor.reejecutar(c["calc_soporte"], "auditoría", "AG-18")["coincide"] == "SI"
    assert [h["id"] for h in b.evaluador.aprobar_certificados([c["id"]], REVISION)] == [c["id"]]


def test_h05_un_vigente_cuyo_soporte_no_coincide_despues_deja_de_valer_y_se_vuelve_a_proponer(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.evaluador.aprobar_certificados([c["id"]], REVISION)
    _, alterada = _alterar_ficha(monkeypatch, 1 + 1e-3)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    assert b.motor.reejecutar(c["calc_soporte"], "auditoría", "AG-18")["coincide"] == "NO"
    monkeypatch.undo()
    assert b.evaluador.certificados_vigentes(REVISION) == []
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["revocados"] == [c["id"]] and "no coincide" in res["vigentes_sin_reejecucion"][c["id"]]
    nuevo, = res["emitidos"]                         # el mismo soporte (caché del Motor) con una CT-10 nueva, posterior a la NO
    assert nuevo["calc_soporte"] == c["calc_soporte"] and nuevo["reejecucion"] != c["reejecucion"]
    assert b.evaluador.motivo_sin_reejecucion(nuevo) is None


# ================================================================================ H-02 · VIGENTE sin re-ejecución
def test_h02_un_vigente_sin_reejecucion_no_habilita_probabilidades_y_la_revision_lo_revoca_y_vuelve_a_proponer(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2025-0001", "estado": "VIGENTE",      # anterior a T-160
                                       "celda": {"clase": "RF", "horizonte": "H3", "metodo": None}})
    assert b.evaluador.certificados_vigentes(REVISION) == []
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["revocados"] == ["CERT-2025-0001"] and list(res["vigentes_sin_reejecucion"]) == ["CERT-2025-0001"]
    viejo = b.almacen.estado("F6", clave="id")["CERT-2025-0001"]
    assert viejo["estado"] == "REVOCADO" and "sin re-ejecución CT-10 coincidente" in viejo["motivo_cambio"]
    assert "no cita la re-ejecución" in viejo["motivo_cambio"]
    nuevo, = res["emitidos"]                                            # la celda vuelve por la vía normal, con su CT-10
    assert nuevo["estado"] == "PROPUESTO" and b.evaluador.motivo_sin_reejecucion(nuevo) is None
    assert [h["id"] for h in b.evaluador.aprobar_certificados([nuevo["id"]], REVISION)] == [nuevo["id"]]
    assert [c["id"] for c in b.evaluador.certificados_vigentes(REVISION)] == [nuevo["id"]]
    res2 = b.evaluador.revisar_certificados(REVISION)                   # y el legítimo se queda
    assert res2["revocados"] == [] and res2["vigentes_sin_reejecucion"] == {} and res2["emitidos"] == []


def test_h02_mientras_no_haya_revision_un_vigente_sin_reejecucion_bloquea_otra_aprobacion_de_su_celda(tmp_path, universo):
    """Lo que no se usa tampoco deja la puerta abierta a dos VIGENTE de la misma celda en F6."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2025-0001", "estado": "VIGENTE",
                                       "celda": {"clase": "RF", "horizonte": "H3", "metodo": None}})
    with pytest.raises(ValueError, match="ya tiene un certificado VIGENTE"):
        b.evaluador.aprobar_certificados([c["id"]], REVISION)


# ================================================================================ H-03 · la emisión directa también mira el RC
@pytest.mark.parametrize("solo_endurecer", [True, False])
def test_h03_un_si_que_no_esta_en_el_registro_no_deja_certificado(tmp_path, universo, monkeypatch, solo_endurecer):
    b = _bloque(tmp_path, universo)
    b.cfg["aprendizaje"]["solo_endurecer"] = solo_endurecer
    monkeypatch.setattr(b.motor, "reejecutar", lambda calc_id, motivo, solicitante="AG-18":
                        {"coincide": "SI", "categoria": None, "diferencias": [], "calc_id": "CALC-2026-9998", "diagnostico": "x"})
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b) and b.evaluador.certificados_vigentes(REVISION) == []
    motivo = res["sin_reejecucion_coincidente"]["RF|H3"]
    assert "no pasa la comprobación de CT-04" in motivo and "CALC-2026-9998" in motivo
    assert not res["evaluadas"]["RF|H3"]["certificable"]
    inc, = _incidencias(b, "RF|H3")
    assert inc["severidad"] == "Material"


def test_h03_sin_solo_endurecer_el_certificado_legitimo_nace_vigente(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    b.cfg["aprendizaje"]["solo_endurecer"] = False
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["estado"] == "VIGENTE" and [c["id"] for c in b.evaluador.certificados_vigentes(REVISION)] == [cert["id"]]
    assert cert["huella_entradas"] == b.almacen.estado("RC")[cert["calc_soporte"]]["datos"][0]["huella"]


# ================================================================================ H-04 · min_conglomerados de FC-EVAL-001
P, O = [0.3, 0.7] * 30, [0, 1, 1, 1, 0, 0] * 10
FECHAS = [f"2025-07-{1 + i // 2:02d}" for i in range(60)]


def _fc_eval(b, valores, minimo=None, con_minimo=True):
    prm = {"replicas": 30, "simulaciones": 30, **({"min_conglomerados": minimo} if con_minimo else {})}
    return b.motor.servir({"operacion": "FC-EVAL-001", "fecha_corte": REVISION, "datos": [{"valores": valores}],
                           "parametros": prm}, "AG-20")


@pytest.mark.parametrize("minimo", [0, -1, 1, True, False, 1.5, 2.0, "x", "10", None, [10]])
def test_h04_fc_eval_con_fechas_rechaza_un_minimo_de_conglomerados_que_no_es_un_entero_valido(tmp_path, universo, minimo):
    b = nuevo_bloque(tmp_path, universo)
    r = _fc_eval(b, {"p": P, "o": O, "fechas": FECHAS}, minimo)
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INSUFICIENTES", r
    assert "min_conglomerados" in r["detalle"], r


@pytest.mark.parametrize("minimo", [servicio.MIN_CONGLOMERADOS, 10, np.int64(10)])
def test_h04_fc_eval_con_fechas_acepta_un_entero_desde_el_minimo(tmp_path, universo, minimo):
    b = nuevo_bloque(tmp_path, universo)
    r = _fc_eval(b, {"p": P, "o": O, "fechas": FECHAS}, minimo)
    assert r["estado"].startswith("SERVED") and r["resultado"]["bss"]["min_conglomerados"] == int(minimo)


@pytest.mark.parametrize("minimo", [0, True, "x", None])
def test_h04_sin_fechas_el_minimo_no_se_lee_como_antes(tmp_path, universo, minimo):
    b = nuevo_bloque(tmp_path, universo)
    r = _fc_eval(b, {"p": P, "o": O}, minimo)
    assert r["estado"].startswith("SERVED") and r["resultado"]["n_eff"] is None


def test_h04_el_evaluador_usa_el_mismo_suelo_que_el_motor():
    assert servicio.MIN_CONGLOMERADOS == 2
    assert not servicio.min_conglomerados_valido(servicio.MIN_CONGLOMERADOS - 1)
    assert servicio.min_conglomerados_valido(servicio.MIN_CONGLOMERADOS)


# ================================================================================ H-06 · mutantes M12 y M17
def test_h06_m12_la_materialidad_mueve_el_q90_del_nulo():
    """ECE por debajo del q90 del nulo a 1,5 tolerancias: certifica tal cual, y no con el q90 movido en contra (QA r01, H-06)."""
    h = holgura_tolerancia(TOL, 1)
    q90 = BUENA["ece_nulo"]["q90"]
    borde = {**BUENA, "dm_hln": {"p_unilateral": 0.01}, "calibracion": {"ece": q90 * (1 - 1.5 * TOL)}}
    assert ev.criterio_certificado(borde, 100, 0.15, 0.05)["certificable"]
    r = criterio_desfavorable(borde, h, 100, 0.15, 0.05)
    assert not r["certificable"] and any("> q90 nulo" in x for x in r["motivos"]), r["motivos"]


def test_h06_m17_ct04_no_aprueba_un_soporte_de_otra_ficha_aunque_de_las_mismas_cifras(tmp_path, universo, monkeypatch):
    """Una ficha distinta (FC-CAL-001, aquí con el cálculo de FC-EVAL-001) con las mismas entradas, cifras y método, y su CT-10
    coincidente: todo cuadra salvo la ficha del soporte."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    monkeypatch.setitem(servicio.IMPLEMENTADAS, "FC-CAL-001", dict(servicio.IMPLEMENTADAS["FC-EVAL-001"]))
    s = b.almacen.estado("RC")[c["calc_soporte"]]
    pet = {"operacion": "FC-CAL-001", "plan": "PLAN_MIN", "clase": "RF", "horizonte": "H3", "fecha_corte": s["as_of"],
           "datos": [{"valores": s["datos"][0]["valor"]}], "parametros": {k: v for k, v in s["parametros"].items() if k != "clase"}}
    otra = b.motor.servir(pet, "AG-20")
    assert otra["estado"].startswith("SERVED") and otra["resultado"] == s["resultado"]["payload"]
    rex = b.motor.reejecutar(otra["calc_id"], "prueba T-163", "AG-20")
    assert rex["coincide"] == "SI"
    falso = _reescribir(b, c, id="CERT-2026-0992", calc_soporte=otra["calc_id"], curva_fiabilidad=otra["calc_id"],
                        reejecucion=rex["calc_id"])
    _no_aprueba(b, falso["id"], "no es un servicio FC-EVAL-001 de la celda RF")
