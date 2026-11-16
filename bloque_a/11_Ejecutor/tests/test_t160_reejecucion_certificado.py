"""T-160 · PB-32: un certificado de horizonte solo se propone o emite con una re-ejecución CT-10 coincidente del cálculo que lo
sostiene (EVAL-F05 y punto 5 de §6.6 del prompt del Evaluador), y solo entra en vigor por CT-04 con ella en el Registro de
cálculos. D-1 de T-157: la tasa base RI-TB escribe en el RC la versión vigente del Catálogo.

Todo con el cliente simulado y sin red. Cada prueba de fallo cerrado falla sin el cambio que cubre (ver pruebas.md del ticket).
"""
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.evaluador import Evaluador, criterio_desfavorable, holgura_tolerancia
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles
from bloque_a.motor import evaluacion as ev
from bloque_a.motor import servicio
from conftest import AS_OF, nuevo_bloque
from test_fase4_huecos import BUENA, _g3v_de, _sembrar_celda

from bloque_a import evaluador

REVISION = "2026-01-02"
TOL = servicio.IMPLEMENTADAS["FC-EVAL-001"]["tol"]


def _bloque(tmp_path, universo, clases=(("RF", "hábil"),), metodo=None):
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar(REVISION)
    for i, (clase, tipo) in enumerate(clases):
        # identificadores lejos de los que da el ciclo (PRG-2026-0001…), que corre después en la prueba de punta a punta
        _sembrar_celda(b, clase, 150, (lambda p: p) if tipo == "hábil" else (lambda p: 0.5), 5001 + 1000 * i, metodo=metodo)
    return b


def _certs(b):
    return [c for c in b.almacen.estado("F6", clave="id").values() if c.get("tipo_entrada") == "CERT"]


def _incidencias(b, objeto):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and e.get("objeto") == objeto]


def _alterar_ficha(monkeypatch, factor):
    """FC-EVAL-001 con el Brier multiplicado por `factor`: otra implementación que da otra cifra."""
    original = servicio.IMPLEMENTADAS["FC-EVAL-001"]["fn"]

    def alterada(ent, params):
        m, lim = original(ent, params)
        return {**m, "brier": m["brier"] * factor}, lim
    return original, alterada


def _durante(objeto, metodo, monkeypatch, antes):
    """Envuelve `objeto.metodo` para que `antes()` cambie algo solo mientras dura esa llamada (y lo deshaga después)."""
    original = getattr(objeto, metodo)

    def envoltura(*a, **k):
        deshacer = antes()
        try:
            return original(*a, **k)
        finally:
            deshacer()
    monkeypatch.setattr(objeto, metodo, envoltura)


def _con_ficha(alterada):
    def antes():
        meta = servicio.IMPLEMENTADAS["FC-EVAL-001"]
        previa = meta["fn"]
        meta["fn"] = alterada

        def deshacer():
            meta["fn"] = previa
        return deshacer
    return antes


# ================================================================================ CA-1 · nominal
def test_ca1_el_certificado_lleva_su_reejecucion_ct10_coincidente_y_el_calculo_que_lo_sostiene(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    res = b.evaluador.revisar_certificados(REVISION)
    cert, = res["emitidos"]
    assert res["sin_reejecucion_coincidente"] == {} and cert["estado"] == "PROPUESTO"
    rc = b.almacen.estado("RC")
    rex, soporte = rc[cert["reejecucion"]], rc[cert["calc_soporte"]]
    assert (rex["tipo_entrada"], rex["contrato"], rex["solicitante"]) == ("REEJECUCION", "CT-10", "AG-20")
    assert rex["reejecucion"]["coincide"] == "SI" and rex["reejecucion"]["calc_original"] == cert["calc_soporte"]
    assert (soporte["tipo_entrada"], soporte["contrato"], soporte["solicitante"]) == ("SERVICIO", "CT-09", "AG-20")
    assert soporte["operacion"]["ficha_id"] == "FC-EVAL-001" and (soporte["clase"], soporte["horizonte"]) == ("RF", "H3")
    assert soporte["operacion"]["catalog_version"] == servicio.CATALOG_VERSION
    assert cert["curva_fiabilidad"] == cert["calc_soporte"]
    # las cifras del certificado son las del cálculo del Motor que se re-ejecutó
    pay = soporte["resultado"]["payload"]
    assert cert["bss"] == pay["bss"]["valor"] and cert["bss_ic90"] == pay["bss"]["ic"] and cert["n_eff"] == pay["n_eff"]
    assert cert["ece"] == pay["calibracion"]["ece"] and cert["ece_nulo_q90"] == pay["ece_nulo"]["q90"]
    # con las fechas de conglomerado (PA-03) y los parámetros de la configuración
    assert soporte["parametros"]["min_conglomerados"] == b.cfg["evaluacion"]["min_conglomerados_bootstrap"]
    assert soporte["parametros"]["replicas"] == b.cfg["evaluacion"]["bootstrap_replicas"]
    assert soporte["parametros"]["nivel"] == b.cfg["evaluacion"]["nivel_ic"]
    d = cert["reejecucion_ct10"]
    assert d["coincide"] == "SI" and d["tolerancia"] == TOL == d["tolerancia_ct10"] and "FC-EVAL-001" in d["origen_tolerancia"]
    assert d["cifras_frente_al_motor"] == "iguales" and "materialidad" not in d
    assert not _incidencias(b, "RF|H3")


# ================================================================================ CA-2 · no coincide
def test_ca2_una_reejecucion_que_no_coincide_no_deja_certificado_y_registra_la_incidencia(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _, alterada = _alterar_ficha(monkeypatch, 1 + 1e-3)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))       # solo el recálculo CT-10 da otra cifra
    n_f6 = len(b.almacen.leer("F6"))
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b) and len(b.almacen.leer("F6")) == n_f6
    crit = res["evaluadas"]["RF|H3"]
    assert not crit["certificable"] and "ERROR_ORIGINAL" in crit["motivos"][-1] and "CT-10" in crit["motivos"][-1]
    assert "RF|H3" in res["sin_reejecucion_coincidente"]
    rex = b.almacen.estado("RC")[crit["reejecucion_ct10"]["reejecucion"]]
    assert rex["reejecucion"]["coincide"] == "NO" and rex["reejecucion"]["categoria"] == "ERROR_ORIGINAL"
    inc, = _incidencias(b, "RF|H3")
    assert (inc["tipo"], inc["severidad"]) == ("HERRAMIENTA", "Material") and "no coincide" in inc["detalle"]
    # en la revisión siguiente, con la re-ejecución ya coincidente, se propone
    monkeypatch.undo()
    assert [c["celda"]["clase"] for c in b.evaluador.revisar_certificados(REVISION)["emitidos"]] == ["RF"]


# ================================================================================ CA-3 · no se puede re-ejecutar
def test_ca3_sin_motor_no_hay_certificado(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    e = Evaluador(b.almacen, b.proveedor, None, b.cfg, b.universo)
    res = e.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b)
    assert "sin Motor" in res["sin_reejecucion_coincidente"]["RF|H3"]
    inc, = _incidencias(b, "RF|H3")
    assert inc["severidad"] == "Operativa" and "sin Motor" in inc["detalle"]


def test_ca3_el_motor_no_sirve_la_ficha_que_sostiene_el_certificado(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    servible = servicio.servible
    monkeypatch.setattr(servicio, "servible", lambda f, raiz=None: f != "FC-EVAL-001" and servible(f, raiz))
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b)
    assert "no sirve FC-EVAL-001: METODO_NO_IMPLEMENTADO" in res["sin_reejecucion_coincidente"]["RF|H3"]
    assert [i["severidad"] for i in _incidencias(b, "RF|H3")] == ["Operativa"]


def test_ca3_los_datos_del_artefacto_no_se_pueden_resolver_en_la_reejecucion(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)

    def sin_datos():
        original = b.motor._resolver_datos

        def falla(*a, **k):
            raise DatosNoDisponibles("HT-01: serie retirada")
        b.motor._resolver_datos = falla

        def deshacer():
            b.motor._resolver_datos = original
        return deshacer
    _durante(b.motor, "reejecutar", monkeypatch, sin_datos)
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b)
    motivo = res["sin_reejecucion_coincidente"]["RF|H3"]
    assert "ERROR_REEJECUCION" in motivo and "no coincide" in motivo
    assert [i["severidad"] for i in _incidencias(b, "RF|H3")] == ["Operativa"]


def test_ca3_una_reejecucion_imposible_que_lanza_no_deja_certificado(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    original = b.motor.reejecutar
    monkeypatch.setattr(b.motor, "reejecutar", lambda calc_id, motivo, solicitante="AG-18": original("CALC-0000-0000", motivo, solicitante))
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b)
    assert "imposible (KeyError" in res["sin_reejecucion_coincidente"]["RF|H3"]


# ================================================================================ CA-4 · cifras distintas y materialidad
def test_ca4_si_el_motor_no_reproduce_las_cifras_del_certificado_no_hay_certificado(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _, alterada = _alterar_ficha(monkeypatch, 1 + 1e-3)
    _durante(b.motor, "servir", monkeypatch, _con_ficha(alterada))           # el cálculo servido da otro Brier
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b)
    motivo = res["sin_reejecucion_coincidente"]["RF|H3"]
    assert "no reproduce las cifras del certificado" in motivo and ".brier" in motivo
    assert [i["severidad"] for i in _incidencias(b, "RF|H3")] == ["Material"]


def test_ca4_dentro_de_tolerancia_y_lejos_de_los_umbrales_certifica(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _, alterada = _alterar_ficha(monkeypatch, 1 + TOL / 100)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    d = cert["reejecucion_ct10"]
    assert d["coincide"] == "DENTRO_TOLERANCIA" and d["materialidad"]["certificable"]
    assert d["materialidad"]["holgura"] == pytest.approx(TOL)


def test_ca4_dentro_de_tolerancia_pero_material_no_certifica(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _, alterada = _alterar_ficha(monkeypatch, 1 + TOL / 100)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    vistos = []

    def al_borde(m, holgura, n_min, ece_max, alfa):
        vistos.append(holgura)
        return {"certificable": False, "motivos": [f"ECE 0.1499999999 ≥ {ece_max}"]}
    monkeypatch.setattr(evaluador, "criterio_desfavorable", al_borde)
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["emitidos"] == [] and not _certs(b) and vistos == [pytest.approx(TOL)]
    assert "material" in res["sin_reejecucion_coincidente"]["RF|H3"]


def test_ca4_la_materialidad_mueve_cada_cifra_en_contra_del_certificado():
    h = holgura_tolerancia(TOL, 1)
    assert holgura_tolerancia(TOL, 0) == 0 and h == pytest.approx(TOL / (1 - TOL))
    assert holgura_tolerancia(TOL, 2) > 2 * TOL
    for malo in ((-1e-9, 1), (1.0, 1), (TOL, -1)):
        with pytest.raises(ValueError):
            holgura_tolerancia(*malo)
    lejos = {**BUENA, "dm_hln": {"p_unilateral": 0.01}}
    assert criterio_desfavorable(lejos, h, 100, 0.15, 0.05)["certificable"]
    for cambio, fragmento in (({"calibracion": {"ece": 0.15 * (1 - TOL / 10)}, "ece_nulo": {"q90": 0.30}}, "≥ 0.15"),
                              ({"calibracion": {"ece": 0.06 * (1 - TOL / 10)}}, "> q90 nulo"),
                              ({"n_eff": 100 * (1 + TOL / 10)}, "< 100"),
                              ({"dm_hln": {"p_unilateral": 0.05 * (1 - TOL / 10)}}, "> alfa Holm")):
        borde = {**lejos, **cambio}
        assert ev.criterio_certificado(borde, 100, 0.15, 0.05)["certificable"], cambio     # con la cifra tal cual, certifica
        r = criterio_desfavorable(borde, h, 100, 0.15, 0.05)                              # movida lo que permite la tolerancia, no
        assert not r["certificable"] and any(fragmento in x for x in r["motivos"]), (cambio, r["motivos"])


# ================================================================================ CA-5 · CT-04 y propuestas antiguas
def _propuesto_a_mano(b, cid, **campos):
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": cid, "estado": "PROPUESTO",
                                       "celda": {"clase": "RF", "horizonte": "H3", "metodo": None}, **campos})


def test_ca5_ct04_no_pone_en_vigor_un_propuesto_sin_reejecucion_coincidente(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    # una re-ejecución que no coincide y un servicio de FC-EVAL-001 de verdad, para citarlos en propuestas falsas
    _, alterada = _alterar_ficha(monkeypatch, 1 + 1e-3)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    fallida = b.evaluador.revisar_certificados(REVISION)["evaluadas"]["RF|H3"]["reejecucion_ct10"]
    monkeypatch.undo()
    otra = b.motor.servir({"operacion": "FC-EVAL-001", "datos": [{"valores": {"p": [0.6, 0.4], "o": [1, 0]}}], "clase": "RF",
                           "horizonte": "H3", "fecha_corte": REVISION}, "AG-20")["calc_id"]
    casos = {"CERT-2026-0901": ({}, "no cita la re-ejecución"),
             "CERT-2026-0902": ({"reejecucion": fallida["calc_soporte"], "calc_soporte": fallida["calc_soporte"]}, "no es una re-ejecución"),
             "CERT-2026-0903": ({"reejecucion": fallida["reejecucion"], "calc_soporte": otra}, "no re-ejecuta"),
             "CERT-2026-0904": ({"reejecucion": fallida["reejecucion"], "calc_soporte": fallida["calc_soporte"]}, "no coincide")}
    for cid, (campos, _) in casos.items():
        _propuesto_a_mano(b, cid, **campos)
    n_f6 = len(b.almacen.leer("F6"))
    for cid, (_, motivo) in casos.items():
        with pytest.raises(ValueError, match=f"re-ejecución CT-10 coincidente.*{motivo}"):
            b.evaluador.aprobar_certificados([cid], REVISION)
    assert len(b.almacen.leer("F6")) == n_f6 and b.evaluador.certificados_vigentes(REVISION) == []
    r = b.decision({"aprobar_certificados": ["CERT-2026-0904"]}, REVISION)                    # por el Broker, igual
    assert r["certificados_aprobados"] == [] and "re-ejecución CT-10" in r["rechazos"][0]["motivo"]


def test_ca5_una_propuesta_antigua_sin_reejecucion_se_retira_y_la_celda_se_vuelve_a_proponer(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _propuesto_a_mano(b, "CERT-2025-0001")                                                     # anterior a T-160
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["propuestas_retiradas"] == ["CERT-2025-0001"]
    viejo = b.almacen.estado("F6", clave="id")["CERT-2025-0001"]
    assert viejo["estado"] == "REVOCADO" and "sin re-ejecución CT-10 coincidente" in viejo["motivo_cambio"]
    nuevo, = res["emitidos"]
    assert nuevo["id"] != "CERT-2025-0001" and nuevo["celda"] == {"clase": "RF", "horizonte": "H3", "metodo": None}
    assert b.evaluador.motivo_sin_reejecucion(nuevo) is None
    assert [h["id"] for h in b.evaluador.aprobar_certificados([nuevo["id"]], REVISION)] == [nuevo["id"]]
    assert [c["id"] for c in b.evaluador.certificados_vigentes(REVISION)] == [nuevo["id"]]


# ================================================================================ CA-6 · PB-32 de punta a punta
def test_ca6_pb32_de_punta_a_punta_con_el_cliente_simulado(tmp_path, universo):
    """Preparación del plan: RF × H3 de un método con habilidad real y RV × H3 del mismo método sin ella. Paso 1, revisión
    del Evaluador (C5): un certificado, el de RF × H3 × método, con su re-ejecución CT-10 coincidente; ninguno para RV. El
    operador lo aprueba por CT-04. Paso 2, el RUN- siguiente: probabilidad publicada solo en RF H3, con `certificado_ref`, y
    G3-CON-10 (C10) en OK."""
    b = _bloque(tmp_path, universo, clases=(("RF", "hábil"), ("RV", "sin habilidad")), metodo="ACC-MOM-001")
    c5 = b.evaluador.ciclo(REVISION)
    cert, = c5["certificados"]["emitidos"]
    assert cert["celda"] == {"clase": "RF", "horizonte": "H3", "metodo": "ACC-MOM-001"}
    rv = c5["certificados"]["evaluadas"]["RV|H3|ACC-MOM-001"]
    assert not rv["certificable"] and not any("CT-10" in m for m in rv["motivos"])         # RV no llega a la re-ejecución
    assert b.evaluador.motivo_sin_reejecucion(cert) is None
    assert b.almacen.estado("RC")[cert["reejecucion"]]["reejecucion"]["coincide"] == "SI"
    r = b.decision({"aprobar_certificados": [cert["id"]]}, REVISION)
    assert r["certificados_aprobados"] == [cert["id"]] and r["estado"] == "APLICADA"
    b.fijar_fecha(AS_OF)
    run = b.ciclo(AS_OF, alcance={"clases": ["RF", "RV"]})
    altas = [p for p in b.almacen.estado("F4").values() if p.get("tipo_entrada") == "ALTA" and p.get("run_id") == run["run_id"]]
    rf = [p for p in altas if (p["clase"], p["horizonte"], p.get("metodo")) == ("RF", "H3", "ACC-MOM-001")]
    assert rf and all(p["prob_publicada"] is not None and p["certificado_ref"] == cert["id"] for p in rf)
    otros = [p for p in altas if p not in rf]
    assert otros and all(p["prob_publicada"] is None and p["certificado_ref"] is None for p in otros)
    assert [c["id"] for c in b.evaluador.certificados_vigentes(AS_OF)] == [cert["id"]]
    assert run["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS")
    assert all(res["C10"] == "OK" for res in _g3v_de(b, run["run_id"]).values() if "C10" in res)


# ================================================================================ FC-EVAL-001 con conglomerados (PA-03)
def test_fc_eval_con_fechas_da_la_muestra_efectiva_y_sin_fechas_como_antes(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    p, o = [0.3, 0.7] * 30, [0, 1, 1, 1, 0, 0] * 10
    fechas = [str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i // 2)).date()) for i in range(60)]
    pet = {"operacion": "FC-EVAL-001", "fecha_corte": REVISION, "parametros": {"replicas": 50, "simulaciones": 50}}
    sin = b.motor.servir({**pet, "datos": [{"valores": {"p": p, "o": o}}]}, "AG-20")
    con = b.motor.servir({**pet, "datos": [{"valores": {"p": p, "o": o, "fechas": fechas}}],
                          "parametros": {**pet["parametros"], "min_conglomerados": 10}}, "AG-20")
    assert sin["estado"].startswith("SERVED") and sin["resultado"]["n_eff"] is None
    assert con["resultado"]["n_eff"] == pytest.approx(ev.evaluar_celda(p, o, [0.5] * 60, 0.5, 50, 50, fechas=fechas,
                                                                       min_conglomerados=10)["n_eff"])
    assert con["resultado"]["bss"]["metodo"] == "bootstrap por conglomerados de fecha"
    falta = b.motor.servir({**pet, "datos": [{"valores": {"p": p, "o": o, "fechas": fechas}}]}, "AG-20")
    assert falta["estado"] == "RECHAZADO" and falta["motivo"] == "DATOS_INSUFICIENTES"       # con fechas, el mínimo es obligatorio
    assert b.motor.reejecutar(con["calc_id"], "prueba T-160", "AG-20")["coincide"] == "SI"


# ================================================================================ CA-7 · D-1 de T-157
def test_ca7_la_tasa_base_escribe_la_version_vigente_del_catalogo(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    ri = b.evaluador.tasa_base("SPY", "ACWI", "RV", 5, True, AS_OF, "RUN-2026-0001")
    assert b.almacen.estado("RC")[ri["calc_id"]]["operacion"]["catalog_version"] == servicio.CATALOG_VERSION == "5.0"
    monkeypatch.setattr(servicio, "CATALOG_VERSION", "9.9")                                     # sigue a la constante
    ri = b.evaluador.tasa_base("SPY", "ACWI", "RV", 5, True, AS_OF, "RUN-2026-0001")
    assert b.almacen.estado("RC")[ri["calc_id"]]["operacion"]["catalog_version"] == "9.9"


def test_ca7_el_verificador_de_ids_ya_no_ve_la_version_escrita_a_mano():
    from bloque_a.herramientas import verificador_ids as vi
    informe = vi.verificar(Path(__file__).resolve().parents[2])
    motivos = {h["codigo"] for h in informe["hallazgos"] if h["clase"] == "d"}
    assert "CATALOG_VERSION_LITERAL" not in motivos and "MENCION_OTRA_VERSION_CODIGO" not in motivos
