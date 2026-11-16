"""T-163 QA r01 · ataques del revisor a CT-04, `certificados_vigentes`, la revisión y FC-EVAL-001 tras T-163.

¿Entra en vigor un PROPUESTO falso, o sale una probabilidad certificada sin su re-ejecución CT-10 coincidente? Se prueba con
propuestas forjadas en F6 (que imitan la huella, que citan un soporte propio, con cifras de una celda que no cumple el criterio),
dos celdas con las mismas entradas, el orden del Registro manipulado, una re-ejecución citada por dos certificados en los dos
órdenes, CT-10 posteriores con NO y con SI (del mismo soporte y de otro), VIGENTE sin re-ejecución por el ciclo completo (síntesis,
CT-05), la idempotencia de la revocación, CT-04 con un VIGENTE en la celda y `min_conglomerados` raros.

Las pruebas `test_hNN_*` afirman lo esperado y FALLAN mientras el hallazgo NN de qa.md sigue abierto. El resto deben pasar.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-163/revisores/r01_01_ataques.py
"""
import json
import sys
from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))
from conftest import AS_OF, nuevo_bloque  # noqa: E402
from test_t160_reejecucion_certificado import REVISION, _alterar_ficha, _bloque, _con_ficha, _durante  # noqa: E402

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.evaluador import campos_certificado  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from bloque_a.motor import evaluacion as ev  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _propuesto(b):
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["estado"] == "PROPUESTO" and b.evaluador.motivo_sin_reejecucion(cert) is None
    return cert


def _sembrar(b, clase, horizonte, n, prob_real, desde, metodo=None, semilla=1):
    """Como `_sembrar_celda` de test_fase4_huecos, con el horizonte como parámetro."""
    rng = np.random.default_rng(semilla)
    for i in range(n):
        p = float(rng.choice([0.3, 0.7]))
        o = int(rng.random() < prob_real(p))
        pid = f"PRG-2026-{desde + i:04d}"
        b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": clase, "horizonte": horizonte,
                                           "prob_interna": p, "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True,
                                           "sentido": "POSITIVO", "fecha_emision": "2025-01-02", "estado": "ABIERTO",
                                           "fecha_resolucion": str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date()),
                                           **({"metodo": metodo} if metodo else {})})
        b.almacen.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                           "resolucion": {"resultado_binario": o, "valor_observado": 0.01,
                                                          "comprobacion_fuga": "SUPERADA", "fecha_resuelto": "2025-07-02"}})


def _soporte_propio(b, clase, horizonte, metodo, entradas, tasa_base):
    """Lo que haría quien tenga los permisos del Evaluador: un FC-EVAL-001 como AG-20 con las entradas que quiera, y su CT-10."""
    pet = {"operacion": "FC-EVAL-001", "plan": "PLAN_MIN", "clase": clase, "horizonte": horizonte,
           "datos": [{"valores": entradas}],
           "parametros": {**b.evaluador._parametros_certificado(), "tasa_base": tasa_base, "metodo": metodo},
           "fecha_corte": REVISION}
    res = b.motor.servir(pet, "AG-20")
    assert str(res["estado"]).startswith("SERVED"), res
    rex = b.motor.reejecutar(res["calc_id"], "forja del revisor", "AG-20")
    assert rex["coincide"] == "SI", rex
    return res, rex


def _forjar(b, cid, celda, res, rex, huella=None):
    s = b.almacen.estado("RC")[res["calc_id"]]
    cert = {"tipo_entrada": "CERT", "id": cid, "estado": "PROPUESTO", "celda": dict(celda), **campos_certificado(res["resultado"]),
            "holm_superado": True, "calc_soporte": res["calc_id"], "curva_fiabilidad": res["calc_id"],
            "huella_entradas": huella or s["datos"][0]["huella"], "reejecucion": rex["calc_id"]}
    b.almacen.escribir("F6", "AG-20", cert)
    return cert


def _sin_cambios_en_f6(b, cid, fragmento):
    n = len(b.almacen.leer("F6"))
    with pytest.raises(ValueError, match=fragmento):
        b.evaluador.aprobar_certificados([cid], REVISION)
    assert len(b.almacen.leer("F6")) == n


def _fabricadas(n=150):
    """Entradas inventadas con habilidad clara y 150 fechas distintas (≥ 10 conglomerados)."""
    p = [0.9 if i % 2 else 0.1 for i in range(n)]
    o = [1 if (i % 2 and i % 10) or (not i % 2 and not i % 10) else 0 for i in range(n)]
    fechas = [str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date()) for i in range(n)]
    return {"p": p, "o": o, "p_ref": [0.5] * n, "fechas": fechas}


# ================================================================================ PROPUESTO falso
def test_falso_que_imita_la_huella_del_legitimo_con_otro_soporte_no_entra(tmp_path, universo):
    """Copia la huella del legítimo pero cita un soporte propio (otras entradas, cifras mejores) y su CT-10."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    res, rex = _soporte_propio(b, "RF", "H3", None, _fabricadas(), 0.5)
    falso = _forjar(b, "CERT-2026-0900", c["celda"], res, rex, huella=c["huella_entradas"])
    _sin_cambios_en_f6(b, falso["id"], "no son las mismas")


def test_falso_que_cita_el_soporte_legitimo_con_la_ct10_de_otro_soporte_no_entra(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    _, rex = _soporte_propio(b, "RF", "H3", None, _fabricadas(), 0.5)
    e = {k: v for k, v in c.items() if not k.startswith("_")}
    b.almacen.escribir("F6", "AG-20", {**e, "id": "CERT-2026-0901", "reejecucion": rex["calc_id"]})
    _sin_cambios_en_f6(b, "CERT-2026-0901", "no re-ejecuta")


def test_falso_desde_cero_con_su_propio_soporte_entra_en_vigor_limite_declarado(tmp_path, universo):
    """Límite declarado en el README (no se ata el soporte a F4): con los permisos del Evaluador (Motor como AG-20 y F6 como
    AG-20), un certificado con entradas inventadas, su soporte y su CT-10 pasa CT-04. Documenta el comportamiento (pasa)."""
    b = _bloque(tmp_path, universo, clases=(("RV", "azar"),))           # la celda real no tiene habilidad
    assert b.evaluador.revisar_certificados(REVISION)["emitidos"] == []
    res, rex = _soporte_propio(b, "RV", "H3", None, _fabricadas(), 0.5)
    falso = _forjar(b, "CERT-2026-0902", {"clase": "RV", "horizonte": "H3", "metodo": None}, res, rex)
    assert [h["id"] for h in b.evaluador.aprobar_certificados([falso["id"]], REVISION)] == [falso["id"]]
    assert [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == [falso["id"]]


def test_h01_ct04_no_aprueba_un_certificado_cuyas_cifras_no_cumplen_el_criterio(tmp_path, universo):
    """Soporte y CT-10 de las entradas REALES de una celda sin habilidad (el extremo inferior del IC del BSS ≤ 0): el CERT- con
    las cifras de ese soporte no cumple el criterio y CT-04 no lo comprueba."""
    b = _bloque(tmp_path, universo, clases=(("RV", "azar"),))
    k = ("RV", "H3", None)
    v = [p for p in b.evaluador.resueltos(REVISION) if (p["clase"], p["horizonte"], p.get("metodo")) == k]
    entradas, tb = b.evaluador._entradas_celda(v)
    res, rex = _soporte_propio(b, "RV", "H3", None, entradas, tb)
    crit = ev.criterio_certificado(res["resultado"], int(b.cfg["evaluacion"]["min_certificar"]),
                                   float(b.cfg["evaluacion"]["ece_max"]), None)
    assert not crit["certificable"], crit                                  # la celda real no certifica
    falso = _forjar(b, "CERT-2026-0903", {"clase": "RV", "horizonte": "H3", "metodo": None}, res, rex)
    _sin_cambios_en_f6(b, falso["id"], "criterio|extremo inferior|no cumple")


def test_un_propuesto_falso_escrito_entre_la_comprobacion_y_la_escritura_no_gana_nada(tmp_path, universo, monkeypatch):
    """Una copia exacta escrita justo antes que el legítimo «gana» la exclusividad: el legítimo no entra en vigor y la copia
    entra con las mismas cifras, soporte y CT-10 (no hay ganancia de fondo). Documenta el comportamiento."""
    b = _bloque(tmp_path, universo)
    original = b.almacen.escribir
    hecho = []

    def escribir(archivo, autor, entrada):
        if archivo == "F6" and entrada.get("tipo_entrada") == "CERT" and not hecho:
            hecho.append(1)
            original(archivo, autor, {**entrada, "id": "CERT-2026-0904"})
        return original(archivo, autor, entrada)
    monkeypatch.setattr(b.almacen, "escribir", escribir)
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    monkeypatch.undo()
    assert "ya sostiene CERT-2026-0904" in b.evaluador.motivo_sin_reejecucion(cert)
    assert b.evaluador.motivo_sin_reejecucion(b.almacen.estado("F6", clave="id")["CERT-2026-0904"]) is None


# ================================================================================ dos celdas que comparten entradas
def test_dos_metodos_con_las_mismas_entradas_cada_uno_con_su_soporte(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar(REVISION)
    _sembrar(b, "RF", "H3", 150, lambda p: p, 5001, metodo="ACC-MOM-001")
    _sembrar(b, "RF", "H3", 150, lambda p: p, 6001, metodo="OTRO-METODO")      # mismas p, o y fechas (misma semilla)
    res = b.evaluador.revisar_certificados(REVISION)
    certs = {c["celda"]["metodo"]: c for c in res["emitidos"]}
    assert set(certs) == {"ACC-MOM-001", "OTRO-METODO"}, res["sin_reejecucion_coincidente"]
    a, o = certs["ACC-MOM-001"], certs["OTRO-METODO"]
    assert a["huella_entradas"] == o["huella_entradas"] and a["calc_soporte"] != o["calc_soporte"]
    e = {k: v for k, v in o.items() if not k.startswith("_")}            # cruzar soportes entre métodos no vale
    b.almacen.escribir("F6", "AG-20", {**e, "id": "CERT-2026-0905", "calc_soporte": a["calc_soporte"],
                                       "curva_fiabilidad": a["calc_soporte"], "reejecucion": a["reejecucion"]})
    _sin_cambios_en_f6(b, "CERT-2026-0905", "no es del método OTRO-METODO|ya sostiene")


def test_h02_dos_horizontes_con_las_mismas_entradas_se_certifican_los_dos(tmp_path, universo):
    """La clave de la caché del Motor no lleva el horizonte: la segunda celda recibe el soporte de la primera (de otro
    horizonte) y su borrador no pasa la comprobación de CT-04; nunca se certifica mientras sus entradas coincidan."""
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar(REVISION)
    _sembrar(b, "RF", "H3", 150, lambda p: p, 5001)
    _sembrar(b, "RF", "H2", 150, lambda p: p, 6001)
    res = b.evaluador.revisar_certificados(REVISION)
    assert {c["celda"]["horizonte"] for c in res["emitidos"]} == {"H2", "H3"}, res["sin_reejecucion_coincidente"]


# ================================================================================ orden del Registro y exclusividad
def test_un_campo_seq_en_la_entrada_no_cambia_el_orden(tmp_path, universo):
    """`_seq` lo pone el almacén: un CERT- con `_seq` propio no se cuela como «primero» que cita la re-ejecución."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    e = {k: v for k, v in c.items() if not k.startswith("_")}
    escrita = b.almacen.escribir("F6", "AG-20", {**e, "id": "CERT-2026-0906", "_seq": 0, "_fecha": "2000-01-01"})
    assert escrita["_seq"] > 1 and escrita["_fecha"] == REVISION
    _sin_cambios_en_f6(b, "CERT-2026-0906", f"ya sostiene {c['id']}")
    assert [h["id"] for h in b.evaluador.aprobar_certificados([c["id"]], REVISION)] == [c["id"]]


def test_reordenar_el_registro_de_calculos_en_disco_falla_cerrado(tmp_path, universo):
    """Intercambiar en el fichero del RC el soporte y su CT-10 rompe la cadena de huellas: nada da el certificado por bueno."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.evaluador.aprobar_certificados([c["id"]], REVISION)
    ruta = next(Path(b.almacen.carpeta).glob("RC_*.jsonl"))
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    i = next(n for n, x in enumerate(lineas) if json.loads(x).get("calc_id") == c["calc_soporte"])
    j = next(n for n, x in enumerate(lineas) if json.loads(x).get("calc_id") == c["reejecucion"])
    lineas[i], lineas[j] = lineas[j], lineas[i]
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    assert b.almacen.verificar_integridad("RC") == {"RC": False}
    try:                                                  # una excepción o una lista vacía: lo que no vale es devolverlo
        vig = b.evaluador.certificados_vigentes(REVISION)
    except Exception:  # noqa: BLE001
        vig = []
    assert vig == []


def test_una_reejecucion_citada_por_dos_certificados_en_los_dos_ordenes(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    e = {k: v for k, v in c.items() if not k.startswith("_")}
    b.almacen.escribir("F6", "AG-20", {**e, "id": "CERT-2026-0907"})
    for lote in ([c["id"], "CERT-2026-0907"], ["CERT-2026-0907", c["id"]]):   # en un lote: nada se escribe
        n = len(b.almacen.leer("F6"))
        with pytest.raises(ValueError):
            b.evaluador.aprobar_certificados(lote, REVISION)
        assert len(b.almacen.leer("F6")) == n
    # por CT-04 del Broker (uno a uno): primero la copia, después el legítimo
    r1 = b.decision({"aprobar_certificados": ["CERT-2026-0907", c["id"]]}, REVISION)
    assert r1["certificados_aprobados"] == [c["id"]] and [x["parametro"] for x in r1["rechazos"]] == ["certificado:CERT-2026-0907"]
    assert [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == [c["id"]]


def test_la_reejecucion_de_un_certificado_revocado_no_la_hereda_una_copia(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.evaluador.aprobar_certificados([c["id"]], REVISION)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT_REVOCACION", "id": c["id"], "estado": "REVOCADO",
                                       "motivo_cambio": "prueba", "fecha": REVISION})
    e = {k: v for k, v in c.items() if not k.startswith("_")}
    b.almacen.escribir("F6", "AG-20", {**e, "id": "CERT-2026-0908", "estado": "PROPUESTO"})
    _sin_cambios_en_f6(b, "CERT-2026-0908", f"ya sostiene {c['id']}")


@pytest.mark.parametrize("campo", ["muestra_efectiva", "brier_ref"])
def test_cifras_que_las_pruebas_del_ticket_no_alteran_tambien_se_comparan(tmp_path, universo, campo):
    """Mata N03 y N04 de r01_02_mutantes.py: la muestra efectiva y el Brier de referencia del CERT- también son del soporte."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    e = {k: v for k, v in c.items() if not k.startswith("_")}
    cambio = {**c["muestra_efectiva"], "rho": 0.5} if campo == "muestra_efectiva" else c["brier_ref"] * 1.001
    b.almacen.escribir("F6", "AG-20", {**e, campo: cambio})
    _sin_cambios_en_f6(b, c["id"], "las cifras del certificado no son las de")


def test_un_lote_con_dos_propuestos_validos_de_la_misma_celda_no_aprueba_ninguno(tmp_path, universo):
    """Mata N07 de r01_02_mutantes.py: dos PROPUESTO de la misma celda, cada uno con su soporte y su CT-10, en un lote."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    res, rex = _soporte_propio(b, "RF", "H3", None, _fabricadas(), 0.5)
    otro = _forjar(b, "CERT-2026-0910", c["celda"], res, rex)
    assert b.evaluador.motivo_sin_reejecucion(otro) is None and b.evaluador.motivo_sin_reejecucion(c) is None
    n = len(b.almacen.leer("F6"))
    with pytest.raises(ValueError, match="ya tiene un certificado VIGENTE"):
        b.evaluador.aprobar_certificados([c["id"], otro["id"]], REVISION)
    assert len(b.almacen.leer("F6")) == n and b.evaluador.certificados_vigentes(REVISION) == []


# ================================================================================ H-05 · CT-10 posteriores
def _auditoria_no(b, monkeypatch, calc):
    _, alterada = _alterar_ficha(monkeypatch, 1 + 1e-3)
    _durante(b.motor, "reejecutar", monkeypatch, _con_ficha(alterada))
    r = b.motor.reejecutar(calc, "auditoría", "AG-18")
    monkeypatch.undo()
    assert r["coincide"] == "NO"
    return r


def test_una_ct10_si_de_otro_calculo_posterior_a_la_no_no_la_tapa(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    _auditoria_no(b, monkeypatch, c["calc_soporte"])
    otro, _ = _soporte_propio(b, "RF", "H3", None, _fabricadas(), 0.5)          # una CT-10 «SI» más reciente, de otra cosa
    assert b.motor.reejecutar(otro["calc_id"], "otra", "AG-20")["coincide"] == "SI"
    _sin_cambios_en_f6(b, c["id"], "posterior de .* no coincide")


def test_una_ct10_si_del_mismo_soporte_posterior_a_la_no_no_rehabilita_el_certificado_que_cita_la_anterior(tmp_path, universo,
                                                                                                       monkeypatch):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    _auditoria_no(b, monkeypatch, c["calc_soporte"])
    assert b.motor.reejecutar(c["calc_soporte"], "otra vez", "AG-18")["coincide"] == "SI"
    _sin_cambios_en_f6(b, c["id"], "posterior de .* no coincide")


def test_una_ct10_fallida_posterior_tambien_cuenta(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.evaluador.aprobar_certificados([c["id"]], REVISION)
    monkeypatch.setitem(servicio.IMPLEMENTADAS["FC-EVAL-001"], "fn",
                        lambda ent, params: (_ for _ in ()).throw(ValueError("caída")))
    assert b.motor.reejecutar(c["calc_soporte"], "auditoría", "AG-18")["categoria"] == "ERROR_REEJECUCION"
    monkeypatch.undo()
    assert b.evaluador.certificados_vigentes(REVISION) == []


# ================================================================================ H-02 · VIGENTE sin re-ejecución, por todos los caminos
def test_un_vigente_a_mano_no_publica_probabilidad_en_el_ciclo_ni_va_en_ct05(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2026-0001", "estado": "VIGENTE",
                                       "celda": {"clase": "RV", "horizonte": "H3", "metodo": "ACC-MOM-001"}})
    assert b.evaluador.certificados_vigentes(AS_OF) == []
    ct05, crear = [], b.mensajeria.crear

    def espia(contrato, *a, **k):
        if contrato == "CT-05":
            ct05.append(json.dumps(a, ensure_ascii=False, default=str))
        return crear(contrato, *a, **k)
    b.mensajeria.crear = espia
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["evaluacion"]["certificados"]["revocados"] == ["CERT-2026-0001"]
    assert b.almacen.estado("F6", clave="id")["CERT-2026-0001"]["estado"] == "REVOCADO"
    altas = [p for p in b.almacen.estado("F4").values() if p.get("tipo_entrada") == "ALTA"]
    assert altas and all(p["prob_publicada"] is None and p["certificado_ref"] is None for p in altas)
    for o in r["paquete"]["clases"]["RV"]["opciones"]:
        assert all(v["prob"] is None and not v["certificado_r13"] for v in o["horizontes"].values())
    assert ct05 and all('"certificados": []' in m and "CERT-2026-0001" not in m for m in ct05)


def test_sin_revision_un_vigente_a_mano_no_llega_a_la_sintesis_ni_a_ht09(tmp_path, universo, monkeypatch):
    """Si C5 no llega a revocar (la revisión se salta), la síntesis y HT-09 siguen sin verlo: leen `certificados_vigentes`."""
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2026-0001", "estado": "VIGENTE",
                                       "celda": {"clase": "RV", "horizonte": "H3", "metodo": "ACC-MOM-001"}})
    monkeypatch.setattr(b.evaluador, "revisar_certificados", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("C5 caído")))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})               # C5 no bloquea: el ciclo sigue (modo degradado)
    assert b.almacen.estado("F6", clave="id")["CERT-2026-0001"]["estado"] == "VIGENTE"     # no se revocó
    altas = [p for p in b.almacen.estado("F4").values() if p.get("tipo_entrada") == "ALTA"]
    assert altas and all(p["prob_publicada"] is None and p["certificado_ref"] is None for p in altas)
    for o in r["paquete"]["clases"]["RV"]["opciones"]:
        assert all(v["prob"] is None and not v["certificado_r13"] for v in o["horizontes"].values())


def test_la_revocacion_de_un_vigente_sin_reejecucion_es_idempotente(tmp_path, universo):
    b = _bloque(tmp_path, universo, clases=(("RV", "azar"),))              # la celda no se vuelve a proponer
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2025-0001", "estado": "VIGENTE",
                                       "celda": {"clase": "RV", "horizonte": "H3", "metodo": None}})
    r1 = b.evaluador.revisar_certificados(REVISION)
    n = len(b.almacen.leer("F6"))
    r2 = b.evaluador.revisar_certificados(REVISION)
    assert r1["revocados"] == ["CERT-2025-0001"] and r1["emitidos"] == []
    assert r2["revocados"] == [] and r2["vigentes_sin_reejecucion"] == {} and len(b.almacen.leer("F6")) == n
    revs = [e for e in b.almacen.leer("F6") if e.get("id") == "CERT-2025-0001" and e.get("tipo_entrada") == "CERT_REVOCACION"]
    assert len(revs) == 1


def test_ct04_no_aprueba_un_segundo_certificado_de_una_celda_con_un_vigente_legitimo(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    b.evaluador.aprobar_certificados([c["id"]], REVISION)
    res, rex = _soporte_propio(b, "RF", "H3", None, _fabricadas(), 0.5)
    otro = _forjar(b, "CERT-2026-0909", c["celda"], res, rex)
    assert b.evaluador.motivo_sin_reejecucion(otro) is None                  # válido por sí mismo
    _sin_cambios_en_f6(b, otro["id"], "ya tiene un certificado VIGENTE")
    assert b.evaluador.revisar_certificados(REVISION)["emitidos"] == []        # y la revisión no propone otro


# ================================================================================ H-04 · min_conglomerados
P, O = [0.3, 0.7] * 30, [0, 1, 1, 1, 0, 0] * 10
FECHAS = [f"2025-07-{1 + i // 2:02d}" for i in range(60)]


@pytest.mark.parametrize("minimo", [np.bool_(True), np.float64(2.0), Decimal(2), float("nan"), float("inf"), 2 + 0j, "2"])
def test_fc_eval_rechaza_minimos_raros(minimo):
    with pytest.raises(Exception):                              # noqa: B017 — ErrorFicha u otra: no se sirve
        servicio.f_fc_eval({"valores": {"p": P, "o": O, "fechas": FECHAS}}, {"min_conglomerados": minimo})


@pytest.mark.parametrize("minimo", [np.int8(2), np.uint64(3), 10 ** 6])
def test_fc_eval_acepta_enteros_de_numpy_y_grandes(minimo):
    m, _ = servicio.f_fc_eval({"valores": {"p": P, "o": O, "fechas": FECHAS}}, {"min_conglomerados": minimo, "replicas": 20,
                                                                                  "simulaciones": 20})
    assert m["bss"]["min_conglomerados"] == int(minimo)
    if int(minimo) > 30:                                        # 30 fechas distintas: con un mínimo mayor, sin IC
        assert m["bss"]["ic"] is None or None in m["bss"]["ic"], m["bss"]
