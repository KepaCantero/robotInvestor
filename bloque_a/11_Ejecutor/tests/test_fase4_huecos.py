"""T-116 · Fase 4: cláusulas del Plan de pruebas V3.0 que ninguna prueba comprobaba (huecos del mapa verificado).

Cada prueba sigue los pasos del plan para su PB y afirma la cláusula del criterio de aprobación que faltaba.
"""
import hashlib
import itertools
import json
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.almacen import Almacen, EscrituraFueraDeReserva
from bloque_a.configuracion import aplicabilidad
from bloque_a.consumo import Presupuesto
from bloque_a.contratos import CanalNoPrevisto, DatosSensibles, Mensajeria
from bloque_a.evaluador import Evaluador
from conftest import AS_OF, certificado_con_reejecucion, config_pruebas, nuevo_bloque


def _huellas(carpeta):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(carpeta.iterdir()) if p.is_file()}


# ---------------------------------------------------------------- PB-10 · qué cambia en F10 y HA sin incidencia de escritura
def test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas(tmp_path, universo):
    """El plan pide H1 «para ALT»; el CT-04 del ejecutor solo tiene una lista global de horizontes. La celda ALT×H1 se rechaza
    y la lista global se conserva; solo cambia P-02 (T-189)."""
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    antes = b.f10("2026-12-31")
    activas = [c for c in antes["P-02"] if c != "CRI"] if "CRI" in antes["P-02"] else [*antes["P-02"], "CRI"]
    assert "ALT" in activas and aplicabilidad(b.cfg, "ALT", "H1") == "NO"
    d = b.decision({"configuracion": {"clases_activas": activas, "horizontes": antes["P-03"], "umbral_E": 50}}, AS_OF)
    assert d["estado"] == "APLICADA_PARCIALMENTE"
    rechazos = {x["parametro"]: x["motivo"] for x in d["rechazos"]}
    assert "CALIBRABLE" in rechazos["umbral_E"] and "«No» para ALT" in rechazos["horizontes:ALT:H1"]
    despues = b.f10("2026-12-31")
    cambiados = {k for k in set(antes) | set(despues) if antes.get(k) != despues.get(k)}
    assert not [x for x in b.almacen.leer("F10") if x.get("tipo_entrada") == "CFG" and x["param_id"] == "P-03"]
    assert cambiados == {"P-02"} and despues["P-02"] == activas and despues["P-03"] == antes["P-03"]
    assert aplicabilidad(b.cfg, "ALT", "H1") == "NO"                                  # la celda rechazada sigue sin aplicarse
    assert not [e for e in b.almacen.leer("HA") if e.get("tipo") in ("ACCESO_FUERA_DE_MATRIZ", "CANAL_NO_PREVISTO")]
    assert all(b.almacen.verificar_integridad().values())


# ---------------------------------------------------------------- PB-16 · G3 sin comprobaciones saltadas por falta de presupuesto
def _g3v(b, run_id):
    return {e["fase"]: e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V" and e["run_id"] == run_id}


def test_pb16_con_el_presupuesto_agotado_g3_hace_las_mismas_comprobaciones(tmp_path, universo):
    b1, b2 = nuevo_bloque(tmp_path / "a", universo), nuevo_bloque(tmp_path / "b", universo)
    completo = b1.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    recortado = b2.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]}, presupuesto_override={"RV": 0.3})
    assert completo["estado"] == "COMPLETO" and recortado["estado"] == "PARCIAL"
    g_completo, g_recortado = _g3v(b1, completo["run_id"]), _g3v(b2, recortado["run_id"])
    assert set(g_completo) == set(g_recortado) == {"F6", "F7"}
    for fase in ("F6", "F7"):
        ids_completo = [c["id"] for c in g_completo[fase]["comprobaciones"]]
        ids_recortado = [c["id"] for c in g_recortado[fase]["comprobaciones"]]
        assert ids_recortado == ids_completo and len(ids_completo) >= 15                  # ni una comprobación de menos
        assert all(c["resultado"] in ("OK", "ADVERTENCIA", "BLOQUEO") for c in g_recortado[fase]["comprobaciones"])   # ningún NO_APLICA
        assert g_recortado[fase]["tipo_control"] == g_completo[fase]["tipo_control"]
        assert {c["id"]: c["resultado"] for c in g_recortado[fase]["comprobaciones"]}["C08"] == "OK"   # ninguna cifra sin origen
    # Ronda r04: menos candidatas investigadas en RV y la laguna declarada en F5
    en_completo, en_recortado = ([x for x in b.almacen.estado("F5", clave="id")[r["run_id"]]["decisiones_puertas"] if x["clase"] == "RV"]
                                 for b, r in ((b1, completo), (b2, recortado)))
    assert len(en_recortado) < len(en_completo)
    cierres = b2.almacen.estado("F5", clave="id")[recortado["run_id"]]["cierres_parciales"]
    assert [c["clase"] for c in cierres] == ["RV"] and all(c["motivo"] for c in cierres)


# ---------------------------------------------------------------- PB-17 · ampliación autorizada y denegada, con su AUT- en HA
def test_pb17_ampliacion_autorizada_y_denegada_dejan_su_aut_en_ha(tmp_path, universo):
    """Los dos casos del plan sobre el propio decisor: una fase que puede cambiar el top-3 dentro del tope (AUTORIZADA) y otra
    que no puede cambiarlo o que supera el tope (DENEGADA)."""
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    cfg = config_pruebas()
    sin_aut, maximo = cfg["presupuesto_uc"]["ampliacion_sin_autorizacion"], cfg["presupuesto_uc"]["ampliacion_max_autorizable"]
    base = 10.0
    p = Presupuesto({"MP": base}, cfg)
    p.consumido["MP"] = base * 0.9                                                    # consumo al 90 %, como prepara el plan
    pedido = base * (1 + sin_aut) - p.consumido["MP"] + base * 0.10                   # pasa del margen automático en un 10 % de la base
    assert not p.puede("MP", pedido)
    assert b._solicitar_ampliacion(p, "MP", pedido, "RUN-2026-0001", "refutacion") is True
    assert p.ampliado["MP"] == pytest.approx(base * 0.10) and p.puede("MP", pedido)
    assert b._solicitar_ampliacion(p, "MP", pedido + 1, "RUN-2026-0001", "investigacion") is False      # no puede cambiar el top-3
    assert b._solicitar_ampliacion(p, "MP", base * (1 + maximo), "RUN-2026-0001", "prospectiva") is False   # supera el tope
    assert p.ampliado["MP"] == pytest.approx(base * 0.10)                             # las denegadas no amplían nada
    auts = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT"]
    assert [e["decision"] for e in auts] == ["AUTORIZADA", "DENEGADA", "DENEGADA"]
    for e in auts:
        assert e["_autor"] == "AG-18" and e["solicitante"] == "AG-02" and e["bolsa"] == "MP" and e["presupuesto_base"] == base
        assert e["id"].startswith("AUT-") and e["motivo"] and "top-3" in e["valor_informacion"] and e["run_id"] == "RUN-2026-0001"
    assert auts[0]["ampliacion_uc"] == pytest.approx(base * 0.10) and auts[0]["motivo"] == "dentro del tope de ampliación"
    assert all("supera el tope o la fase no cambia la decisión" == e["motivo"] for e in auts[1:])


def test_pb17_en_un_ciclo_la_ampliacion_denegada_cierra_con_alcance_reducido(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["MP"]}, presupuesto_override={"MP": 6.0})
    auts = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT" and e["run_id"] == r["run_id"]]
    # T-146: cada petición pide la ampliación de su peor caso; con 6 UC, la de prospectiva cabe en el tope y se autoriza, y
    # las siguientes se deniegan (antes, con la estimación de 2 500 tokens de salida, solo había denegadas)
    assert auts and "DENEGADA" in {e["decision"] for e in auts}
    assert r["estado"] == "PARCIAL" and any("MP" in x for x in r["paquete"]["limitaciones"])
    pu = config_pruebas()["presupuesto_uc"]
    v = r["presupuesto"]["MP"]
    assert v["ampliado"] <= 6.0 * (pu["ampliacion_max_autorizable"] - pu["ampliacion_sin_autorizacion"]) + 1e-9
    assert v["ampliado"] == pytest.approx(sum(e["ampliacion_uc"] for e in auts if e["decision"] == "AUTORIZADA"), abs=1e-3)
    assert 0 < v["consumido"] <= 6.0 * (1 + pu["ampliacion_sin_autorizacion"]) + v["ampliado"]
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    assert run["presupuesto"]["MP"]["consumido"] == r["presupuesto"]["MP"]["consumido"]     # consumo real en F5


# ---------------------------------------------------------------- PB-22 · tres INC- CANAL_NO_PREVISTO y cero efectos en archivos
def test_pb22_tres_mensajes_por_canales_no_previstos_tres_incidencias_y_ningun_efecto(tmp_path):
    alm = Almacen(tmp_path)
    alm.reloj.fijar(AS_OF)
    ms = Mensajeria(alm)
    ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "¿qué tal?"})                  # un mensaje válido, para tener estado previo
    antes = _huellas(tmp_path)
    intentos = [("CT-17", "AG-19", "AG-02", {}),                                      # Auditor → Analizador
                ("CT-06", "AG-03", "AG-04", {"clase": "RV", "fase": "CRIBADO", "nivel": "N2", "opciones_vigentes": [], "lecciones": []}),
                ("CT-02", "AG-17", "BROKER", {"entregables": {}, "resumen": {}, "estado_g3": "APTO"})]   # Redactor → Broker
    registrados = len(ms.registro)
    for contrato, emisor, receptor, cuerpo in intentos:
        with pytest.raises(CanalNoPrevisto):
            ms.crear(contrato, emisor, receptor, cuerpo, run_id="RUN-2026-0001", tipo_mensaje="RETORNO" if contrato == "CT-02" else "ENCARGO")
    incs = [e for e in alm.leer("HA") if e.get("tipo_entrada") == "INC" and e.get("tipo") == "CANAL_NO_PREVISTO"]
    assert len(incs) == 3 and [e["objeto"] for e in incs] == ["AG-19", "AG-03", "AG-17"]
    assert all(e["escalado_operador"] and e["tratamiento"] == "rechazada y registrada" for e in incs)   # R2: y se escala (r04)
    assert len(ms.registro) == registrados                                            # ninguno se dio por creado
    despues = _huellas(tmp_path)
    cambiados = {n for n in set(antes) | set(despues) if antes.get(n) != despues.get(n)}
    assert cambiados and all(n.startswith(("HA_", "contadores", "sellos_")) for n in cambiados), cambiados
    assert all(alm.verificar_integridad().values())


# ---------------------------------------------------------------- PB-33 · la revocación lleva su estado, su motivo y su fecha
def test_pb33_la_revocacion_registra_estado_motivo_y_fecha_de_efecto(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar("2026-01-02")
    for i in range(100):                                                              # celda sin habilidad: BSS ≤ 0
        pid = f"PRG-2025-{i + 1:04d}"
        a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": "RV", "horizonte": "H3", "prob_interna": 0.65,
                                   "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True, "sentido": "POSITIVO",
                                   "fecha_emision": "2025-01-02", "estado": "ABIERTO",
                                   "fecha_resolucion": str((pd.Timestamp("2025-01-02") + pd.Timedelta(days=i)).date())})
        a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                   "resolucion": {"resultado_binario": i % 2, "valor_observado": 0.01, "comprobacion_fuga": "SUPERADA",
                                                  "fecha_resuelto": "2025-07-02"}})
    a.reloj.fijar("2025-12-01")
    certificado_con_reejecucion(a, {"clase": "RV", "horizonte": "H3", "metodo": None}, "CERT-2025-0001")  # T-163 (H-02): con su soporte y su CT-10
    a.reloj.fijar("2026-01-02")
    f4_antes = hashlib.sha256((tmp_path / "F4_registro_pronosticos.jsonl").read_bytes()).hexdigest()
    cfg = config_pruebas(evaluacion={"bootstrap_replicas": 50, "simulaciones_ece": 50})
    res = Evaluador(a, None, None, cfg, None).revisar_certificados("2026-01-02")
    assert res["revocados"] == ["CERT-2025-0001"]
    cert = a.estado("F6", clave="id")["CERT-2025-0001"]
    assert cert["estado"] == "REVOCADO" and cert["fecha"] == "2026-01-02" and "deterioro" in cert["motivo_cambio"]
    assert a.estado("F6", "2026-01-01", clave="id")["CERT-2025-0001"]["estado"] == "VIGENTE"          # antes de la fecha seguía vigente
    assert hashlib.sha256((tmp_path / "F4_registro_pronosticos.jsonl").read_bytes()).hexdigest() == f4_antes   # PRG congelados intactos


# ---------------------------------------------------------------- PB-45 · el encargo lleva 10 lecciones como máximo, las de más fuerza
def test_pb45_el_encargo_lleva_diez_lecciones_como_maximo_y_las_de_mas_fuerza(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    fuerzas = ["anecdotica"] * 9 + ["recurrente"] * 4 + ["estadistica"]
    for i, fuerza in enumerate(fuerzas, start=1):
        b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": f"LEC-2026-{i:04d}", "fecha": AS_OF,
                                           "ambito": {"clase": "DIV", "horizonte": "H2" if fuerza == "estadistica" else None},
                                           "nivel": "B", "tipo": "CALIBRACION", "observacion": f"Observación {i}", "evidencia": [],
                                           "recomendacion": f"Recomendación {i}", "fuerza": fuerza, "n": 30, "caducidad": "2027-06-05",
                                           "estado": "VIGENTE", "origen": "DETERMINISTA"})
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": "LEC-2026-0099", "fecha": AS_OF, "ambito": {"clase": "RV"},
                                       "nivel": "B", "tipo": "CALIBRACION", "observacion": "De otro tipo", "evidencia": [],
                                       "recomendacion": "x", "fuerza": "estadistica", "n": 30, "caducidad": "2027-06-05",
                                       "estado": "VIGENTE", "origen": "DETERMINISTA"})
    encargos = []
    crear = b.mensajeria.crear

    def anotar(contrato, emisor, receptor, cuerpo, **kw):
        msg = crear(contrato, emisor, receptor, cuerpo, **kw)
        if contrato == "CT-06" and receptor == "AG-05":
            encargos.append(json.loads(json.dumps(msg, default=str)))
        return msg
    b.mensajeria.crear = anotar
    b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    con_lecciones = [m for m in encargos if m["lecciones"]]
    assert con_lecciones
    for m in con_lecciones:
        assert len(m["lecciones"]) == 10 and len(set(m["lecciones"])) == 10
        assert m["lecciones"][0] == "LEC-2026-0014"                                   # la estadística, primero
        assert set(m["lecciones"][1:5]) == {f"LEC-2026-{i:04d}" for i in range(10, 14)}   # después, las cuatro recurrentes
        assert "LEC-2026-0099" not in m["lecciones"]                                  # la de otro tipo de activo no viaja


# ---------------------------------------------------------------- PB-59 · credencial expuesta: incidencia en HA sin el valor
def test_pb59_la_credencial_expuesta_deja_incidencia_en_ha_sin_copiar_el_valor(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    s = b.credenciales.solicitar("API de fondos cerrados", "AG-16", "Cribado FON", "Datos públicos semanales", as_of=AS_OF)
    antes = len([e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"])
    exp = b.credenciales.responder({"crd_id": s["crd_id"], "estado": "PROVISTA", "valor": "clave-filtrada-123"}, AS_OF)
    assert exp["estado"] == "RECHAZADA_CREDENCIAL_EXPUESTA" and "bóveda" in exp["accion"] and "renuévela" in exp["accion"]
    incs = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]
    assert len(incs) == antes + 1 and incs[-1]["tipo_entrada"] == "INC" and incs[-1]["campo_afectado"] == ["valor"]
    for p in (tmp_path / "estado").rglob("*"):
        if p.is_file():
            assert "clave-filtrada-123" not in p.read_text(encoding="utf-8", errors="ignore"), p
    assert "clave-filtrada-123" not in json.dumps(b.mensajeria.registro)
    assert b.credenciales.solicitar("API de fondos cerrados", "AG-16", "x", "y", as_of=AS_OF)["estado"] == "YA_SOLICITADA"   # sigue pendiente


# ================================================================================ QA r01 de T-116 (H-01): cuatro filas que el
# mapa daba por automáticas sin que ninguna prueba afirmase una cláusula del criterio, y dos más repasadas con la misma regla
CLAVE_API = "sk-" + "ant-abcdefghijklmnopqrstuvwxyz123456"   # ficticia y partida, para el gate de secretos
IBAN = "ES91 2100 0418 4502 0005 1332"                         # el IBAN de ejemplo de la documentación bancaria


def _en_archivos(carpeta, textos):
    hallados = {}
    for p in carpeta.rglob("*"):
        if p.is_file():
            cuerpo = p.read_text(encoding="utf-8", errors="ignore")
            for t in textos:
                if t in cuerpo:
                    hallados.setdefault(t, []).append(p.name)
    return hallados


# ---------------------------------------------------------------- PB-21 · CT-04 con una clave y un IBAN: ningún archivo los guarda
def test_pb21_un_ct04_con_una_clave_y_un_iban_se_rechaza_y_no_queda_en_ningun_archivo(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    f5_antes = len(b.almacen.leer("F5"))
    with pytest.raises(DatosSensibles):
        b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1,
                                           "comentario": f"mi clave es {CLAVE_API} y mi IBAN {IBAN}"}}, AS_OF)
    incs = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]
    assert len(incs) == 1 and incs[0]["tipo_entrada"] == "INC" and incs[0]["campo_afectado"] == ["valoracion_informe"]
    assert len(b.almacen.leer("F5")) == f5_antes                                     # rechazado íntegro: nada en F5
    assert _en_archivos(tmp_path, [CLAVE_API, IBAN, IBAN.replace(" ", ""), "2100 0418", CLAVE_API[7:]]) == {}
    assert CLAVE_API not in json.dumps(b.mensajeria.registro) and IBAN not in json.dumps(b.mensajeria.registro)


# ---------------------------------------------------------------- PB-23 · los tres intentos del plan; la huella de F4 no cambia
def test_pb23_los_tres_intentos_del_plan_se_rechazan_y_f4_no_cambia(tmp_path):
    alm = Almacen(tmp_path)
    alm.reloj.fijar("2026-01-02")
    alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "estado": "ABIERTO", "prob_interna": 0.6,
                                 "afirmacion": "x"})
    f4 = tmp_path / "F4_registro_pronosticos.jsonl"
    antes = hashlib.sha256(f4.read_bytes()).hexdigest()
    intentos = [("AG-02", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0002"}),                       # el Analizador escribe en F4
                ("AG-10", {"tipo_entrada": "RESOLUCION", "prg_id": "PRG-2026-0001", "estado": "RESUELTO",
                           "resolucion": {"x": 1}}),                                                  # Prospectiva, un campo de resolución
                ("AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": "PRG-2026-0001", "afirmacion": "otra"})]   # el Evaluador, la afirmación
    for autor, entrada in intentos:
        with pytest.raises(EscrituraFueraDeReserva):
            alm.escribir("F4", autor, entrada)
        assert hashlib.sha256(f4.read_bytes()).hexdigest() == antes
    incs = [e for e in alm.leer("HA") if e.get("tipo_entrada") == "INC"]
    assert [e["tipo"] for e in incs] == ["ACCESO_FUERA_DE_MATRIZ"] * 3
    assert alm.estado("F4")["PRG-2026-0001"]["afirmacion"] == "x" and alm.verificar_integridad("F4")["F4"]


# ---------------------------------------------------------------- PB-37 · un pronóstico corregido es otro pronóstico
def test_pb37_la_correccion_es_un_prg_nuevo_y_el_original_no_cambia(tmp_path):
    alm = Almacen(tmp_path)
    alm.reloj.fijar("2026-01-02")
    alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "estado": "ABIERTO", "prob_interna": 0.6,
                                 "nivel_referencia": {"valor": 101.0}, "fecha_resolucion": "2026-03-02"})
    f4 = tmp_path / "F4_registro_pronosticos.jsonl"
    original = f4.read_bytes()
    with pytest.raises(EscrituraFueraDeReserva):                                     # el alta congelada no se reescribe
        alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "nivel_referencia": {"valor": 110.0}})
    assert f4.read_bytes() == original
    alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0002", "version_de": "PRG-2026-0001", "estado": "ABIERTO",
                                 "prob_interna": 0.6, "nivel_referencia": {"valor": 110.0}, "fecha_resolucion": "2026-03-02"})
    assert f4.read_bytes().startswith(original)                                      # la entrada original, byte a byte
    alm.reloj.fijar("2026-03-03")
    for pid in ("PRG-2026-0001", "PRG-2026-0002"):
        alm.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO", "resolucion": {"resultado_binario": 1}})
    f4_estado = alm.estado("F4")
    assert f4_estado["PRG-2026-0001"]["estado"] == f4_estado["PRG-2026-0002"]["estado"] == "RESUELTO"
    assert f4_estado["PRG-2026-0001"]["nivel_referencia"] == {"valor": 101.0} and f4_estado["PRG-2026-0002"]["version_de"] == "PRG-2026-0001"
    assert f4.read_bytes().startswith(original) and alm.verificar_integridad("F4")["F4"]


# ---------------------------------------------------------------- PB-49 · una entrada borrada también se detecta
@pytest.mark.parametrize("cual", ["la del medio", "la última"])
def test_pb49_una_entrada_borrada_rompe_la_integridad(tmp_path, cual):
    alm = Almacen(tmp_path)
    alm.reloj.fijar("2026-01-02")
    for i in range(3):
        alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": f"PRG-2026-000{i + 1}", "estado": "ABIERTO", "prob_interna": 0.6})
    assert Almacen(tmp_path).verificar_integridad("F4")["F4"]
    ruta = tmp_path / "F4_registro_pronosticos.jsonl"
    lineas = ruta.read_text(encoding="utf-8").splitlines(keepends=True)
    ruta.write_text("".join(lineas[:1] + lineas[2:] if cual == "la del medio" else lineas[:-1]), encoding="utf-8")
    with pytest.raises(ValueError, match="integridad"):
        Almacen(tmp_path).verificar_integridad("F4")


# ---------------------------------------------------------------- PB-54 · los once campos del encargo, presentes y no vacíos
def test_pb54_cada_encargo_para_b_lleva_sus_once_campos_no_vacios(ciclo_semanal):
    _, r, _ = ciclo_semanal
    encargos = r["paquete"]["paquete_para_bloque_B"]
    assert encargos
    campos = ("ambito", "tesis", "horizontes", "pronosticos", "catalizadores", "riesgos", "invalidacion", "indicador_seguimiento",
              "criterios_seleccion_sugeridos", "metricas_clave", "preguntas_para_B")
    for e in encargos:
        vacios = [c for c in campos if not e.get(c)]
        assert not vacios, (e["opp_id"], vacios)
        assert all(e["ambito"].get(k) for k in ("incluye", "excluye", "region")) and e["indicador_seguimiento"].get("simbolo")


# ---------------------------------------------------------------- PB-64 · ningún certificado para H5
def test_pb64_la_revision_de_certificados_no_emite_ninguno_para_h5(tmp_path):
    from test_t53_evaluacion_y_almacen import _h5_con_hitos
    a = Almacen(tmp_path)
    a.reloj.fijar("2027-06-04")
    _h5_con_hitos(a, "MP", "PRG-2026-0901", 8, 12)                                   # 20 hitos resueltos, 40 % cumplidos
    e = Evaluador(a, None, None, config_pruebas(evaluacion={"bootstrap_replicas": 50, "simulaciones_ece": 50}), None)
    assert e.estado_h5("2027-06-04")["celdas"]["MP"]["degradar"]
    res = e.revisar_certificados("2027-06-04")
    assert not [c for c in res["emitidos"] if c["celda"]["horizonte"] == "H5"]
    assert not [c for c in a.estado("F6", clave="id").values() if c.get("tipo_entrada") == "CERT" and c["celda"]["horizonte"] == "H5"]


# ================================================================================ QA r02 de T-116 (H-06): PB-32
def _sembrar_celda(b, clase, n, prob_real, desde, metodo=None):
    """`n` pronósticos resueltos de la celda `clase` × H3 (× `metodo`); `prob_real(p)` es la frecuencia real de acierto cuando
    se dijo `p`."""
    import numpy as np
    rng = np.random.default_rng(1)
    for i in range(n):
        p = float(rng.choice([0.3, 0.7]))
        o = int(rng.random() < prob_real(p))
        pid = f"PRG-2026-{desde + i:04d}"
        b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": clase, "horizonte": "H3", "prob_interna": p,
                                           "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True, "sentido": "POSITIVO",
                                           "fecha_emision": "2025-01-02", "estado": "ABIERTO",
                                           "fecha_resolucion": str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date()),
                                           **({"metodo": metodo} if metodo else {})})
        b.almacen.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                           "resolucion": {"resultado_binario": o, "valor_observado": 0.01, "comprobacion_fuga": "SUPERADA",
                                                          "fecha_resuelto": "2025-07-02"}})


def test_pb32_se_certifica_la_celda_con_habilidad_y_no_la_que_no_la_tiene(tmp_path, universo):
    """El caso del plan: RF × H3 con habilidad real y RV × H3 sin ella, en el mismo almacén: un certificado, el de RF."""
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar("2026-01-02")
    _sembrar_celda(b, "RF", 150, lambda p: p, 1)                 # acierta con la frecuencia que dice
    _sembrar_celda(b, "RV", 150, lambda p: 0.5, 1001)            # acierta a cara o cruz, diga lo que diga
    res = b.evaluador.revisar_certificados("2026-01-02")
    assert [c["celda"] for c in res["emitidos"]] == [{"clase": "RF", "horizonte": "H3", "metodo": None}]
    certs = [c for c in b.almacen.estado("F6", clave="id").values() if c.get("tipo_entrada") == "CERT"]
    assert [c["celda"]["clase"] for c in certs] == ["RF"]
    evaluadas = {k: v for k, v in res["evaluadas"].items() if "RV" in k}
    assert evaluadas and all(not v["certificable"] and v["motivos"] for v in evaluadas.values())


BUENA = {"n": 150, "n_eff": 150.0, "bss": {"ic": [0.05, 0.25]}, "calibracion": {"ece": 0.03}, "ece_nulo": {"q90": 0.06}}


@pytest.mark.parametrize("cambio, motivo", [
    ({"bss": {"ic": [0.0, 0.2]}}, "extremo inferior del IC del BSS"),          # sin habilidad demostrada
    ({"bss": {"ic": [-0.02, 0.2]}}, "extremo inferior del IC del BSS"),
    ({"bss": {"ic": [None, None]}}, "extremo inferior del IC del BSS"),
    ({"calibracion": {"ece": 0.07}}, "> q90 nulo"),                             # calibración rechazada frente al nulo
    ({"calibracion": {"ece": 0.20}, "ece_nulo": {"q90": 0.30}}, "≥ 0.15"),      # ECE por encima del tope, aunque el nulo lo admita
    ({"calibracion": {"ece": 0.15}, "ece_nulo": {"q90": 0.30}}, "≥ 0.15"),      # el tope es estricto
    ({"n_eff": 99.9}, "n_eff = 99.9 < 100"),
    ({"n_eff": None}, "n_eff no disponible"),
])
def test_pb32_cada_condicion_del_certificado_cuenta_por_separado(cambio, motivo):
    from bloque_a.motor.evaluacion import criterio_certificado
    assert criterio_certificado(BUENA) == {"certificable": True, "motivos": [], "n": 150, "n_eff": 150.0}
    r = criterio_certificado({**BUENA, **cambio})
    assert not r["certificable"] and len(r["motivos"]) == 1 and motivo in r["motivos"][0], r["motivos"]


# ================================================================================ QA r03 de T-116 (H-07 y H-08) y repaso
# cláusula a cláusula de la ronda r04: cada prueba afirma una cláusula del plan que ninguna citada afirmaba
def _ct25(b, servicio):
    """Solicitudes CT-25 del Coordinador al Broker: todas las de la traza (la prueba solo pide un servicio), y las de F5 de
    `servicio` deben ser las mismas."""
    msgs = [m["msg_id"] for m in b.mensajeria.registro if m["contrato"] == "CT-25" and m["emisor"] == "AG-01" and m["receptor"] == "BROKER"]
    crd = [c["msg_id"] for c in b.almacen.leer("F5") if c.get("tipo_entrada") == "CRD" and c.get("servicio") == servicio and c.get("msg_id")]
    assert crd == msgs
    return msgs


# ---------------------------------------------------------------- PB-60 · credencial denegada: no se vuelve a pedir y se declara
def test_pb60_credencial_denegada_no_se_vuelve_a_pedir_y_los_entregables_declaran_la_degradacion(tmp_path, universo):
    servicio = "API de crédito privado"
    b = nuevo_bloque(tmp_path, universo)
    s = b.credenciales.solicitar(servicio, "AG-09", "Cribado ALT", "Sin descuentos de secundario", as_of=AS_OF)
    assert len(_ct25(b, servicio)) == 1
    b.credenciales.responder({"crd_id": s["crd_id"], "estado": "DENEGADA", "credencial_ref": None}, AS_OF)
    lim = [e for e in b.almacen.leer("F10") if e.get("tipo_entrada") == "LIMITACION_SERVICIO"]
    assert [(e["servicio"], e["crd_id"]) for e in lim] == [(servicio, s["crd_id"])]
    otra = b.credenciales.solicitar(servicio, "AG-09", "Cribado ALT", "Sin descuentos de secundario", as_of=AS_OF)   # nueva necesidad
    assert otra["estado"] == "DENEGADA" and otra["modo"] == "DEGRADADO_DECLARADO" and len(_ct25(b, servicio)) == 1   # ninguna CT-25 nueva
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS") and r["entregables"]
    declarada = [x for x in r["paquete"]["limitaciones"] if servicio in x and s["crd_id"] in x and "degradado" in x]
    assert len(declarada) == 1                                                        # limitación visible en el paquete
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    visual = Path(r["entregables"]["informe_visual"]).read_text(encoding="utf-8")
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert declarada[0] in tecnico and declarada[0] in js["limitaciones"] and f"«{servicio}»" in visual
    # Con cambio de circunstancias sí se vuelve a pedir; una vez provista, el ciclo siguiente ya no declara la degradación
    nueva = b.credenciales.solicitar(servicio, "AG-09", "Cribado ALT", "Sin descuentos de secundario", as_of=AS_OF,
                                     cambio_circunstancias=True)
    assert nueva["estado"] == "SOLICITADA" and len(_ct25(b, servicio)) == 2
    b.credenciales.depositar(nueva["crd_id"], "valor-de-prueba-pb60", "2027-12-31", AS_OF)
    semana2 = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date())
    r2 = b.ciclo(semana2, alcance={"clases": ["RV"]})
    assert not [x for x in r2["paquete"]["limitaciones"] if servicio in x]
    assert servicio not in Path(r2["entregables"]["informe_visual"]).read_text(encoding="utf-8")


# ---------------------------------------------------------------- PB-33 · revisión mensual y RUN- posterior con la celda deteriorada
def _pb33_revision_y_run(tmp_path, universo):
    """PB-33: la celda certificada RV × H3 pierde la habilidad; C5 (revisión) y después el RUN-. Devuelve el bloque y el RUN-
    tras comprobar la revocación, la alerta de sobreconfianza y que los PRG congelados siguen intactos."""
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar("2025-06-02")
    certificado_con_reejecucion(b.almacen, {"clase": "RV", "horizonte": "H3", "metodo": "ACC-MOM-001"}, "CERT-2025-0001",
                                motor=b.motor)  # T-163 (H-02): con su soporte y su CT-10
    b.reloj.fijar("2026-01-02")
    for i in range(120):                                  # la celda pierde la habilidad: dice 0,65 y acierta la mitad de las veces
        pid = f"PRG-2025-{i + 1:04d}"
        b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": "RV", "horizonte": "H3", "prob_interna": 0.65,
                                           "metodo": "ACC-MOM-001", "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True,
                                           "sentido": "POSITIVO", "fecha_emision": "2025-01-02", "estado": "ABIERTO",
                                           "fecha_resolucion": str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date())})
        b.almacen.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                           "resolucion": {"resultado_binario": i % 2, "valor_observado": 0.01, "comprobacion_fuga": "SUPERADA",
                                                          "fecha_resuelto": "2025-07-02"}})
    f4 = (tmp_path / "estado" / "F4_registro_pronosticos.jsonl").read_bytes()
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})                                   # C5 (revisión) y después el RUN-
    assert r["evaluacion"]["certificados"]["revocados"] == ["CERT-2025-0001"]
    cert = b.almacen.estado("F6", clave="id")["CERT-2025-0001"]
    assert cert["estado"] == "REVOCADO" and cert["fecha"] == AS_OF and "deterioro" in cert["motivo_cambio"]
    alertas = [l for l in r["evaluacion"]["lecciones_nuevas"] if l["tipo"] == "CALIBRACION" and l["ambito"] == {"clase": "RV", "horizonte": "H3"}]
    assert len(alertas) == 1 and alertas[0]["observacion"].startswith("Sobreconfianza en RV×H3")            # alerta de sobreconfianza
    assert alertas[0]["id"] in b.almacen.estado("F6", clave="id")
    assert (tmp_path / "estado" / "F4_registro_pronosticos.jsonl").read_bytes().startswith(f4)     # PRG congelados intactos
    return b, r


def test_pb33_tras_la_revocacion_hay_alerta_de_sobreconfianza_y_el_run_siguiente_no_publica_probabilidad(tmp_path, universo):
    b, r = _pb33_revision_y_run(tmp_path, universo)
    # T-173 (PB-50, 12.2): la celda pierde frente a la referencia (p ≈ 0,05), pero no supera el umbral de Holm de la revisión
    # mensual con la familia fija de las celdas H1–H4 en «Sí» (cierre de la QA r02, H-06): sigue en «Sí» y el RUN- ofrece H3
    rev = b.almacen.estado("F6", clave="id")[f"RDM-{AS_OF[:7]}"]["celdas"]["RV|H3"]
    assert r["evaluacion"]["degradacion_dm"] == [] and not rev["degradar"] and rev["dm_hln"]["p_valor"] > rev["umbral_holm"]
    publicadas = [v for o in r["paquete"]["clases"]["RV"]["opciones"] for h, v in o["horizontes"].items() if h == "H3"]
    assert publicadas and all(v["prob"] is None for v in publicadas)                 # sin certificado vigente, sin probabilidad
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS")


def test_pb33_con_la_degradacion_dm_neutralizada_la_vista_h3_decertificada_no_publica_probabilidad(tmp_path, universo,
                                                                                                   monkeypatch):
    """T-173 r02 (QA r01, H-04): el criterio original de PB-33 sobre la celda decertificada. Sin la degradación DM de 12.2
    (neutralizada aquí), RV × H3 sigue en «Sí»: el RUN- la ofrece y ninguna de sus vistas lleva probabilidad (G3-CON-10, HT-09)."""
    monkeypatch.setattr(Evaluador, "aplicar_degradacion_dm", lambda self, *a, **k: [])
    b, r = _pb33_revision_y_run(tmp_path, universo)
    assert r["evaluacion"]["degradacion_dm"] == [] and aplicabilidad(b.cfg, "RV", "H3") == "SI"
    publicadas = [v for o in r["paquete"]["clases"]["RV"]["opciones"] for h, v in o["horizontes"].items() if h == "H3"]
    assert publicadas and all(v["prob"] is None for v in publicadas)                 # sin certificado vigente, sin probabilidad
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS")


# ---------------------------------------------------------------- PB-56 · dos Analistas proponen el mismo ámbito en un C1
def test_pb56_en_un_c1_el_mismo_ambito_propuesto_por_rv_e_idx_queda_en_un_solo_top3(tmp_path, universo):
    from bloque_a.herramientas import ht09
    u = universo.copy()
    rv = u[u["simbolo"] == "XLU"].iloc[0]
    fila = u["simbolo"] == "ACWI"                         # el índice que sin el duplicado entra en el top-3 de IDX
    u.loc[fila, ["ambito_incluye", "region"]] = [rv["ambito_incluye"], rv["region"]]
    b = nuevo_bloque(tmp_path, universo, universo_df=u)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "IDX"]})
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS")
    top = {c: d["opciones"] for c, d in r["paquete"]["clases"].items()}
    claves = [(c, ht09.clave_ambito(o)) for c, ops in top.items() for o in ops]
    assert len({k for _, k in claves}) == len(claves)                                  # ninguna oportunidad en dos top-3
    nombres = [ht09.normalizar_texto(o["nombre"]) for ops in top.values() for o in ops]
    assert len(set(nombres)) == len(nombres)
    simbolos = {c: [o["indicador_seguimiento"]["simbolo"] for o in ops] for c, ops in top.items()}
    assert ("XLU" in simbolos["RV"]) != ("ACWI" in simbolos["IDX"])                    # se queda una de las dos
    quitada = "ACWI" if "XLU" in simbolos["RV"] else "XLU"
    f3 = [e for e in b.almacen.leer("F3") if (e.get("indicador_seguimiento") or {}).get("simbolo") == quitada]
    motivos = [m for e in f3 for m in (e.get("motivos_no_elegible") or [])]
    assert any("DUPLICADA_EN_OTRO_TIPO" in json.dumps(m, ensure_ascii=False) or "Duplicada de" in json.dumps(m, ensure_ascii=False)
               for m in motivos), motivos                                              # el motivo queda registrado


# ---------------------------------------------------------------- PB-06 · cada referencia de la respuesta N0 existe en la memoria
def test_pb06_la_respuesta_n0_es_una_aclaracion_y_cada_referencia_existe_en_f1_a_f6(ciclo_semanal):
    b, _, r2 = ciclo_semanal
    b.consulta("¿Cuál es el último informe?", as_of=r2["as_of"])                     # calienta la caché del prompt del Coordinador
    q = b.consulta("¿Por qué la deuda emergente no aparece esta semana?", as_of=r2["as_of"])
    assert q["clase_consulta"] == "ACLARACION" and q["ruta"] == "N0" and q["referencias"]
    propios = set()
    for a in ("F1", "F2", "F3", "F4", "F5", "F6"):
        for e in b.almacen.leer(a, r2["as_of"]):
            propios |= {e.get(k) for k in ("id", "opp_id", "prg_id", "run_id", "tnd_id", "clm_id", "calc_id")} - {None}
    assert set(q["referencias"]) <= propios, set(q["referencias"]) - propios        # referencias existentes, no solo con prefijo
    qry = b.almacen.estado("F5", clave="id")[q["query_id"]]
    assert qry["tipo_entrada"] == "QRY" and qry["referencias"] == q["referencias"] and qry["clase_consulta"] == "ACLARACION"


# ---------------------------------------------------------------- PB-32 · Holm y el método (H-08 de la QA r03)
def test_pb32_una_celda_habil_que_no_supera_holm_no_se_certifica_y_el_certificado_lleva_su_metodo(tmp_path, universo, monkeypatch):
    """Dos celdas con habilidad del mismo método: si el procedimiento de Holm se detiene antes de la segunda (umbral 0), esa
    no se certifica aunque su IC del BSS sea positivo; la otra sí, con la celda × método."""
    from bloque_a import evaluador
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar("2026-01-02")
    for clase, desde in (("RF", 1), ("DIV", 1001)):
        _sembrar_celda(b, clase, 150, lambda p: p, desde)
    original = evaluador.ev.holm

    def holm_detenido_en_div(p, alfa):
        return {k: (0.0 if k.startswith("DIV") else u) for k, u in original(p, alfa).items()}
    monkeypatch.setattr(evaluador.ev, "holm", holm_detenido_en_div)
    res = b.evaluador.revisar_certificados("2026-01-02")
    div = [v for k, v in res["evaluadas"].items() if k.startswith("DIV")]
    assert len(div) == 1 and not div[0]["certificable"] and div[0]["motivos"] == [m for m in div[0]["motivos"] if "Holm" in m]
    assert [c["celda"]["clase"] for c in res["emitidos"]] == ["RF"]


@pytest.mark.parametrize("alfa, p, certificable, fragmento", [
    (0.05, 0.04, True, None), (0.05, 0.05, True, None),             # p ≤ alfa corregido: supera Holm
    (0.05, 0.06, False, "> alfa Holm"), (0.05, None, False, "> alfa Holm"),
    (0.0, 0.001, False, "se detuvo"),                               # Holm detenido en una celda anterior
])
def test_pb32_el_criterio_exige_el_alfa_de_holm(alfa, p, certificable, fragmento):
    from bloque_a.motor.evaluacion import criterio_certificado
    r = criterio_certificado({**BUENA, "dm_hln": {"p_unilateral": p}}, alfa_holm=alfa)
    assert r["certificable"] is certificable
    assert certificable or (len(r["motivos"]) == 1 and fragmento in r["motivos"][0]), r["motivos"]


def test_pb32_el_certificado_es_de_la_celda_por_metodo(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar("2026-01-02")
    _sembrar_celda(b, "RF", 150, lambda p: p, 1, metodo="ACC-MOM-001")
    _sembrar_celda(b, "RF", 60, lambda p: p, 2001, metodo="OTRO-METODO")             # el mismo tipo y horizonte, otro método
    res = b.evaluador.revisar_certificados("2026-01-02")
    assert [c["celda"] for c in res["emitidos"]] == [{"clase": "RF", "horizonte": "H3", "metodo": "ACC-MOM-001"}]
    assert set(res["insuficientes"]) == {"RF|H3|OTRO-METODO"}


def test_pb32_la_probabilidad_se_publica_solo_en_la_celda_certificada_y_con_su_certificado_ref(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    certificado_con_reejecucion(b.almacen, {"clase": "RV", "horizonte": "H3", "metodo": "ACC-MOM-001"}, "CERT-2026-0001",
                                motor=b.motor)  # T-163 (H-02): con su soporte y su CT-10
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    altas = [p for p in b.almacen.estado("F4").values() if p.get("clase") == "RV" and p.get("tipo_entrada") == "ALTA"]
    assert {p["horizonte"] for p in altas if p.get("metodo") == "ACC-MOM-001"} >= {"H3"}
    for p in altas:
        en_celda = p["horizonte"] == "H3" and p.get("metodo") == "ACC-MOM-001"
        assert (p["prob_publicada"] is not None) == en_celda and p["certificado_ref"] == ("CERT-2026-0001" if en_celda else None)
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS")


# ================================================================================ Ronda r04: repaso cláusula a cláusula de las
# filas AUTOMATICA (lo que el ejecutor podría comprobar y ninguna prueba citada afirmaba)
def _g3v_de(b, run_id):
    return {e["fase"]: {c["id"]: c["resultado"] for c in e["comprobaciones"]} for e in b.almacen.leer("HA")
            if e.get("tipo_entrada") == "G3V" and e["run_id"] == run_id}


# ---------------------------------------------------------------- PB-01 · niveles según GC0, mensajes del catálogo y congelación tras G3
def test_pb01_con_memoria_el_nivel_sigue_a_gc0_y_todos_los_mensajes_son_del_catalogo(ciclo_semanal):
    from bloque_a.contratos import CANALES
    b, _, r2 = ciclo_semanal
    niveles = r2["nivel_por_clase"]
    assert {"N1", "N2"} <= set(niveles.values())                                     # con un ciclo anterior en memoria
    for c, nivel in niveles.items():
        assert nivel == ("N2" if r2["gc0"][c]["cambio_material"] else "N1"), (c, r2["gc0"][c])
    contratos = [m["contrato"] for m in b.mensajeria.registro]
    assert set(contratos) <= set(CANALES)                                            # cero mensajes fuera del catálogo
    assert {"CT-02", "CT-05", "CT-06", "CT-11", "CT-12", "CT-13", "CT-15"} <= set(contratos)
    entregas = [m for m in b.mensajeria.registro if m["contrato"] == "CT-02" and m["receptor"] == "BROKER"]
    assert len(entregas) == 2 and all(m["emisor"] == "AG-01" for m in entregas)


def test_pb01_sin_g3_apto_no_se_congela_ningun_pronostico_ni_se_entrega(tmp_path, universo, monkeypatch):
    from bloque_a import redaccion
    monkeypatch.setattr(redaccion, "coherencia", lambda rutas, js: ["incoherencia simulada entre entregables"])
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["g3_entregables"]["dictamen"] == "BLOQUEADO" and r["entrega"] == "BLOQUEADA" and not r.get("prg_congelados")
    assert not [e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA"]   # los PRG se congelan solo tras G3
    assert not [m for m in b.mensajeria.registro if m["contrato"] == "CT-02"]
    assert b.almacen.estado("F5", clave="id")[r["run_id"]]["prg_congelados"] == []


# ---------------------------------------------------------------- PB-07 · la respuesta provisional lleva nivel y plazo
def test_pb07_la_consulta_de_contraste_responde_provisional_con_nivel_y_plazo(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})                                       # informe entregado
    q = b.consulta("¿Qué opinas de la renta variable india frente a la indonesia a 6 meses?", as_of=AS_OF)
    esc = q["escalado"]
    assert q["clase_consulta"] == "CONTRASTE" and q["ruta"] == "ANALITICA"
    assert esc["nivel"] in ("N1", "N2", "N3") and esc["plazo_estimado"] and esc["respuesta_provisional"] == q["respuesta"]
    run = b.almacen.estado("F5", clave="id")[esc["run_id"]]
    assert run["disparador"]["qry_id"] == q["query_id"] and list(run["nivel_por_clase"]) == ["RV"]   # alcance mínimo
    respuesta = next(m for m in b.mensajeria.registro if m["msg_id"] == q["msg_id"])
    assert (respuesta["contrato"], respuesta["emisor"], respuesta["receptor"]) == ("CT-03", "AG-01", "BROKER")


# ---------------------------------------------------------------- PB-12 · relevancia según la regla y el encargo con los datos de su opción
def test_pb12_relevancia_segun_la_regla_y_el_encargo_para_b_repite_los_datos_de_su_opcion(ciclo_semanal):
    from bloque_a.herramientas import ht09
    b, r1, r2 = ciclo_semanal
    todas = {r["run_id"]: [(c, o) for c, d in r["paquete"]["clases"].items() for o in d["opciones"]] for r in (r1, r2)}
    for c, o in todas[r1["run_id"]] + todas[r2["run_id"]]:
        motivos = ht09.relevancia_esperada_alta(o, c, o["vigente"], b.params_ht03)
        assert (o["relevancia_decisional"] == "ALTA") == bool(motivos), (o["opp_id"], motivos)
        assert o["relevancia_decisional"] in ("ALTA", "MEDIA", "BAJA") and o["siguiente_paso_sugerido"] and o["reversibilidad"]
        assert o["que_cambiaria_la_conclusion"]
    assert any(c == "CRI" and not o["vigente"] and o["relevancia_decisional"] == "ALTA" for c, o in todas[r1["run_id"]])   # CRI nueva
    assert any(c == "RF" and o["vigente"] and o["relevancia_decisional"] in ("MEDIA", "BAJA") for c, o in todas[r2["run_id"]])
    ops = todas[r2["run_id"]]
    encargos = r2["paquete"]["paquete_para_bloque_B"]
    assert [e["opp_id"] for e in encargos] == [o["opp_id"] for _, o in ops]             # una entrada por opción del top-3
    por_id = {o["opp_id"]: o for _, o in ops}
    for e in encargos:
        o = por_id[e["opp_id"]]
        for k in set(e) & set(o) - {"horizontes"}:
            assert e[k] == o[k], (e["opp_id"], k)                                          # los mismos datos
        assert set(e["horizontes"]) == set(o["horizontes"])
    for fase, res in _g3v_de(b, r2["run_id"]).items():
        assert res["C10"] == res["C11"] == res["C01"] == "OK", fase


# ---------------------------------------------------------------- PB-55 · un apartado con su semáforo por cada uno de los doce tipos
def test_pb55_el_tecnico_tiene_un_apartado_con_semaforo_por_cada_tipo_y_el_motivo_de_menos_de_tres(ciclo_semanal):
    import re

    from bloque_a.configuracion import CLASES, NOMBRE_CLASE
    _, r, _ = ciclo_semanal
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    apartados = re.findall(r"^### 4\.(\d+) (.+) \((\w+)\) — semáforo (\w+)$", tecnico, flags=re.MULTILINE)
    assert [(int(i), n, c) for i, n, c, _ in apartados] == [(i + 1, NOMBRE_CLASE[c], c) for i, c in enumerate(CLASES)]
    assert all(s in ("VERDE", "AMBAR", "ROJO", "GRIS") for *_, s in apartados)
    for c, d in r["paquete"]["clases"].items():
        assert len(d["opciones"]) <= 3
        if len(d["opciones"]) < 3:
            assert d["menos_de_tres_motivo"] and d["menos_de_tres_motivo"] in tecnico, c


# ---------------------------------------------------------------- PB-58 · degradado y declarado hasta la provisión; el valor en ningún contexto
def test_pb58_el_servicio_pendiente_se_declara_hasta_la_provision_y_el_valor_no_llega_a_ningun_contexto(tmp_path, universo):
    servicio, valor = "API de fondos cerrados", "valor-de-prueba-pb58-XYZ"
    b = nuevo_bloque(tmp_path, universo)
    vistos = []
    generar = b.cliente.generar

    def espiar(**kw):
        vistos.append(json.dumps([kw["system"], kw["mensajes"]], ensure_ascii=False, default=str))
        return generar(**kw)
    b.cliente.generar = espiar
    s = b.credenciales.solicitar(servicio, "AG-16", "Cribado FON", "Datos públicos semanales", as_of=AS_OF)
    assert s["estado"] == "SOLICITADA" and s["modo"] == "DEGRADADO_DECLARADO"
    crd = b.almacen.estado("F5", clave="crd_id")[s["crd_id"]]
    assert crd["tipo_entrada"] == "CRD" and crd["credencial_ref"] is None
    r1 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert [x for x in r1["paquete"]["limitaciones"] if servicio in x and "pendiente" in x and s["crd_id"] in x]
    b.credenciales.depositar(s["crd_id"], valor, "2027-12-31", AS_OF)
    n_ct25 = sum(1 for m in b.mensajeria.registro if m["contrato"] == "CT-25" and m["emisor"] == "AG-01")
    assert b.credenciales.solicitar(servicio, "AG-16", "x", "y", as_of=AS_OF)["estado"] == "PROVISTA"       # sin molestar al Broker
    assert sum(1 for m in b.mensajeria.registro if m["contrato"] == "CT-25" and m["emisor"] == "AG-01") == n_ct25
    r2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()), alcance={"clases": ["RV"]})
    assert not [x for x in r2["paquete"]["limitaciones"] if servicio in x]
    assert vistos and not [t for t in vistos if valor in t]                           # ningún contexto de agente
    for p in (tmp_path / "estado").rglob("*"):
        if p.is_file() and p.name != "secretos.json":
            assert valor not in p.read_text(encoding="utf-8", errors="ignore"), p
    for ruta in list(r1["entregables"].values()) + list(r2["entregables"].values()):
        assert valor not in Path(ruta).read_text(encoding="utf-8")
    assert valor not in json.dumps(b.mensajeria.registro)


# ---------------------------------------------------------------- PB-61 · el supuesto figura en los entregables y el resto sigue
def test_pb61_solo_cri_se_pausa_y_al_vencer_el_supuesto_figura_en_los_entregables(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    c = b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": ["CRI"],
                            "preguntas": [{"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No se incluyen",
                                           "efecto_si_falso": "Se ampliaría el cribado de CRI"}]}, AS_OF)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "CRI"]})
    assert list(r["paquete"]["clases"]) == ["RV"] and r["paquete"]["clases"]["RV"]["opciones"]   # el resto sigue
    r2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()), alcance={"clases": ["RV", "CRI"]})
    assert set(r2["paquete"]["clases"]) == {"RV", "CRI"}
    tecnico = Path(r2["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    js = json.loads(Path(r2["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert "No se incluyen" in tecnico and c["cns_id"] in tecnico
    assert [s["cns_id"] for s in js["supuestos_declarados"]] == [c["cns_id"]]
    assert _g3v_de(b, r2["run_id"])["F7"]["C19"] == "OK"


# ---------------------------------------------------------------- PB-63 · hitos con fecha, indicador y criterio y su espaciado
def test_pb63_los_hitos_h5_del_ciclo_tienen_fecha_indicador_criterio_y_el_espaciado_del_anexo_a(ciclo_semanal):
    from bloque_a.herramientas.referencia import ht09_validador_g3 as ht09
    b, r, _ = ciclo_semanal
    f4 = b.almacen.estado("F4")
    h5 = [o["horizontes"]["H5"] for d in r["paquete"]["clases"].values() for o in d["opciones"] if "H5" in o["horizontes"]]
    assert h5
    for v in h5:
        hitos = v["hitos"]
        assert len(hitos) >= 3 and v["prob"] is None and v["banda"]
        assert all(h["hit_id"].startswith("HIT-") and h["fecha"] and h["indicador"] and h["criterio"] for h in hitos)
        fechas = sorted(h["fecha"] for h in hitos)
        assert ht09._meses_entre(r["as_of"], fechas[0]) <= ht09.H5_PRIMER_HITO_MESES
        assert all(ht09._meses_entre(a, c) <= ht09.H5_MAX_ENTRE_HITOS_MESES for a, c in itertools.pairwise(fechas))
        assert all(f4[h["hit_id"]]["prg_padre"] == v["prg_id"] for h in hitos)        # congelados con su PRG padre
    assert _g3v_de(b, r["run_id"])["F7"]["C18"] == "OK"


# ---------------------------------------------------------------- PB-64 · los tres estados de H5 y MP × H5 de «Sí» a «Limitado»
def test_pb64_los_tres_estados_h5_por_hitos_y_mp_baja_de_si_a_limitado_en_f6_y_f10(tmp_path):
    from test_t53_evaluacion_y_almacen import _alta, _h5_con_hitos, _resolver
    a = Almacen(tmp_path)
    a.reloj.fijar("2027-06-04")
    _h5_con_hitos(a, "MP", "PRG-2026-0901", 8, 12)                                   # 20 hitos, 40 % cumplidos
    for padre, resultados, necesario in (("PRG-2026-0902", [0, 1, 1], None), ("PRG-2026-0903", [0, 0, 1], None),
                                         ("PRG-2026-0904", [1, 0, 1], 1)):
        ids = []
        for i, o in enumerate(resultados):
            hid = f"HIT-2026-{padre[-3:]}{i}"
            _alta(a, hid, clase="RV", prg_padre=padre, es_hito=True, horizonte="H4", fecha_resolucion=f"2027-0{i + 1}-04",
                  necesario=(i == necesario))
            _resolver(a, hid, o, f"2027-0{i + 1}-04")
            ids.append(hid)
        _alta(a, padre, clase="RV", horizonte="H5", prob_interna=None, hit_ids=ids, fecha_resolucion="2036-06-05")
    e = Evaluador(a, None, None, config_pruebas(evaluacion={"bootstrap_replicas": 50, "simulaciones_ece": 50}), None)
    est = e.estado_h5("2027-06-04")["pronosticos"]
    assert [est[p]["estado"] for p in ("PRG-2026-0902", "PRG-2026-0903", "PRG-2026-0904")] == [
        "EN_CURSO_CONFORME", "DESVIADO", "INVALIDADO"]
    assert aplicabilidad(config_pruebas(), "MP", "H5") == "SI"
    aju = [h for h in e.aplicar_degradacion_h5("2027-06-04") if h["tipo_entrada"] == "AJU" and h["celda"]["clase"] == "MP"]
    assert len(aju) == 1 and (aju[0]["parametro"], aju[0]["de"], aju[0]["a"]) == ("P-31", "SI", "LIMITADO")
    assert aju[0]["id"] in a.estado("F6", clave="id")                                 # ajuste registrado en F6
    assert a.estado("F10")["P-31"]["valor_vigente"]["MP"]["H5"] == "LIMITADO"        # y aplicado en F10


# ---------------------------------------------------------------- PB-66 · dos ciclos C6, el registro en F11 y ninguno tras cancelar
def test_pb66_dos_ciclos_c6_con_registro_en_f11_y_ninguno_tras_la_cancelacion(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    opp = r["paquete"]["clases"]["RV"]["opciones"][0]["opp_id"]
    a = b.seguimientos.procesar({"accion": "ALTA", "opp_id": opp, "frecuencia": "SEMANAL", "motivo": "Vigilar"}, AS_OF)
    assert [e["seg_id"] for e in b.almacen.leer("F11") if e.get("tipo_entrada") == "ALTA"] == [a["seg_id"]]   # SEG- en F11
    fechas = [str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7 * k)).date()) for k in (1, 2, 3)]
    for f in fechas[:2]:
        res = b.seguimientos.ejecutar(f)
        assert len(res) == 1 and res[0]["ejecutado"] and res[0]["g3"] != "BLOQUEADO"
        assert len(Path(res[0]["rutas"]["informe"]).read_text(encoding="utf-8").split()) <= 300
    enc = b.seguimientos.encargos()[a["seg_id"]]
    assert enc["ciclos"] == 2 and enc["proximo_ciclo"] == fechas[2]
    assert b.seguimientos.procesar({"accion": "PAUSA", "seg_id": a["seg_id"]}, fechas[1])["proximo_ciclo"] is None
    assert b.seguimientos.procesar({"accion": "REANUDACION", "seg_id": a["seg_id"]}, fechas[1])["proximo_ciclo"] == fechas[2]
    c = b.seguimientos.procesar({"accion": "CANCELACION", "seg_id": a["seg_id"]}, fechas[1])
    assert c["estado"] == "CANCELADO" and c["proximo_ciclo"] is None                  # efecto inmediato
    assert b.seguimientos.ejecutar(fechas[2]) == [] and b.seguimientos.encargos()[a["seg_id"]]["ciclos"] == 2


# ---------------------------------------------------------------- PB-53 · el Analista RV propone una empresa concreta en un C1
def test_pb53_la_empresa_concreta_que_propone_el_analista_rv_no_llega_al_top3(tmp_path, universo, monkeypatch):
    from bloque_a import mock_respuestas
    original = mock_respuestas._ficha
    propuestas = []

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        if msg["clase"] == "RV" and not propuestas:
            f.update(nombre="Acciones de Microsoft Corporation", tesis="Comprar acciones de Microsoft Corporation.")
            propuestas.append(u["simbolo"])
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert propuestas and r.get("entrega") != "BLOQUEADA" and r["entregables"]
    entregado = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    for o in entregado["clases"]["RV"]["opciones"]:
        assert "Microsoft" not in json.dumps({k: v for k, v in o.items() if k != "ejemplos_ilustrativos"}, ensure_ascii=False)
    assert "Microsoft" not in json.dumps(entregado["paquete_para_bloque_B"], ensure_ascii=False)
    for ruta in (r["entregables"]["informe_tecnico"], r["entregables"]["informe_visual"]):
        assert "Microsoft Corporation" not in Path(ruta).read_text(encoding="utf-8")


# ================================================================================ Ronda r04: filas PARCIAL con una cláusula que el
# ejecutor puede comprobar con el cliente simulado (hueco menor de la deuda)
# ---------------------------------------------------------------- PB-11 · los PRG de la opción descartada se resuelven y cuentan
def test_pb11_la_opcion_descartada_se_resuelve_y_cuenta_en_el_historial(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ops = r["paquete"]["clases"]["RV"]["opciones"]
    enviada, descartada = ops[0]["opp_id"], ops[1]["opp_id"]
    estados = {o: b.almacen.estado("F3")[o]["estado"] for o in (enviada, descartada)}
    b.decision({"decisiones": [{"opp_id": enviada, "decision": "ENVIADA_A_BLOQUE_B"},
                               {"opp_id": descartada, "decision": "DESCARTADA", "motivo": "no encaja"}]}, AS_OF)
    f3 = b.almacen.estado("F3")
    assert {o: f3[o]["estado"] for o in estados} == estados and f3[descartada]["decision_broker"]["decision"] == "DESCARTADA"
    despues = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=35)).date())
    vencen = {o["opp_id"]: [v["prg_id"] for v in o["horizontes"].values()
                            if b.almacen.estado("F4")[v["prg_id"]]["fecha_resolucion"] <= despues] for o in ops[:2]}
    b.ciclo(despues, alcance={"clases": ["RV"]})
    f4 = b.almacen.estado("F4", despues)
    prg = {o: [f4[p] for p in vencen[o]] for o in (enviada, descartada)}
    assert all(prg.values()) and all(p["estado"] == "RESUELTO" for ps in prg.values() for p in ps)   # ambos PRG RESUELTO
    resueltos = b.evaluador.resueltos(despues, solo_informe=True)
    assert set(vencen[descartada]) <= {p["prg_id"] for p in resueltos}
    hist = b.evaluador.historial_aciertos(despues)
    assert hist["global"]["n"] == len(resueltos) and hist["global"]["n"] >= len(prg[descartada]) + len(prg[enviada])
    assert all(m["receptor"] == "BROKER" or m["receptor"].startswith("AG-") for m in b.mensajeria.registro)   # nada al Bloque B


# ---------------------------------------------------------------- PB-31 · sin certificado, ninguna cifra ni confianza «alta»
def test_pb31_sin_certificado_ningun_entregable_da_una_cifra_de_probabilidad_ni_confianza_alta(ciclo_semanal):
    b, r, _ = ciclo_semanal
    assert not b.evaluador.certificados_vigentes(AS_OF)
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    import re
    visual = re.sub(r"<!--.*?-->", "", Path(r["entregables"]["informe_visual"]).read_text(encoding="utf-8"), flags=re.DOTALL)
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert "sin ventaja demostrada todavía" in tecnico and "sin ventaja demostrada todavía" in visual
    for d in js["clases"].values():
        for o in d["opciones"]:
            assert o["confianza"] != "establecido"                                     # la única que se pinta «Alta»
            assert all(h["prob"] is None and h["etiqueta"] == "sin ventaja demostrada todavía" for h in o["horizontes"].values())
    assert "<b>Alta</b>" not in visual and "de cada 10 casos parecidos" not in visual
    assert all(p.get("prob_publicada") is None for p in b.almacen.estado("F4", AS_OF).values() if p.get("tipo_entrada") == "ALTA")


# ---------------------------------------------------------------- PB-37 · el original y su corrección cuentan los dos en las métricas
def test_pb37_el_pronostico_original_y_su_correccion_entran_los_dos_en_las_metricas(tmp_path):
    from test_t53_evaluacion_y_almacen import _alta, _resolver
    a = Almacen(tmp_path)
    a.reloj.fijar("2026-01-02")
    _alta(a, "PRG-2026-0001", nivel_referencia={"valor": 101.0}, fecha_resolucion="2026-03-02")
    original = (tmp_path / "F4_registro_pronosticos.jsonl").read_bytes()
    _alta(a, "PRG-2026-0002", version_de="PRG-2026-0001", nivel_referencia={"valor": 110.0}, fecha_resolucion="2026-03-02")
    a.reloj.fijar("2026-03-03")
    _resolver(a, "PRG-2026-0001", 1, "2026-03-02")
    _resolver(a, "PRG-2026-0002", 0, "2026-03-02")
    assert (tmp_path / "F4_registro_pronosticos.jsonl").read_bytes().startswith(original)
    e = Evaluador(a, None, None, config_pruebas(evaluacion={"bootstrap_replicas": 50, "simulaciones_ece": 50}), None)
    assert {p["prg_id"] for p in e.resueltos("2026-03-03")} == {"PRG-2026-0001", "PRG-2026-0002"}
    m = e.metricas("2026-03-03")
    assert sum(v["n"] for v in m.values()) == 2                                        # ambos en métricas


# ---------------------------------------------------------------- PB-43 · la lección de producto enlaza las tres consultas
def test_pb43_la_leccion_de_producto_enlaza_las_tres_consultas_repetidas(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV", "MP"]})
    qs = [b.consulta("¿Cuál es el estado de las opciones vigentes?", as_of=AS_OF) for _ in range(3)]
    assert [q["repeticion"] is not None for q in qs] == [False, False, True]
    lec = b.almacen.estado("F6", clave="id")[qs[-1]["repeticion"]["lec_id"]]
    assert lec["tipo"] == "PRODUCTO" and lec["evidencia"] == [q["query_id"] for q in qs]   # enlazada a las tres QRY-
    temas = {b.almacen.estado("F5", clave="id")[q["query_id"]]["tema_normalizado"] for q in qs}
    assert len(temas) == 1                                                             # tema normalizado común en F5


# ---------------------------------------------------------------- PB-49 · instantáneas semanales: solo añadidos en F1–F6, RC y HA
def test_pb49_en_ocho_semanas_simuladas_las_entradas_de_f1_a_f6_rc_y_ha_solo_se_anaden(tmp_path, universo):
    from bloque_a.almacen import ARCHIVOS
    b = nuevo_bloque(tmp_path, universo)
    vigilados = [ARCHIVOS[k] for k in ("F1", "F2", "F3", "F4", "F5", "F6", "RC", "HA")]
    anterior: dict[str, bytes] = {}
    for semana in range(8):
        b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7 * semana)).date()), alcance={"clases": ["MP"]})
        foto = {n: (tmp_path / "estado" / n).read_bytes() for n in vigilados if (tmp_path / "estado" / n).exists()}
        for n, contenido in anterior.items():
            assert foto[n].startswith(contenido), f"semana {semana}: {n} perdió o cambió entradas"   # cero modificadas o borradas
        anterior = foto
        assert all(Almacen(tmp_path / "estado").verificar_integridad().values())
    assert {ARCHIVOS[k] for k in ("F1", "F3", "F4", "F5", "F6", "HA")} <= set(anterior)


# ---------------------------------------------------------------- PB-19 · el Analizador saturado: ninguna instancia nueva y su CAR- en HA
def test_pb19_el_analizador_saturado_no_abre_instancias_y_deja_su_registro_car_en_ha(tmp_path, universo):
    from bloque_a.herramientas.ht08_monitor import Monitor
    m = Monitor(umbral_cola=3)
    m.encolar("AG-02", 6)                                                             # seis órdenes CT-05 en cola
    ordenes = m.evaluar_instancias()
    assert not [o for o in ordenes if o["tipo_entrada"] == "ORD" and o["agente"] == "AG-02"] and m.instancias["AG-02"] == 1
    assert [(o["tipo_entrada"], o["agente"], o["cola"]) for o in ordenes] == [("CAR", "AG-02", 6)]
    b = nuevo_bloque(tmp_path, universo)
    b.monitor.encolar("AG-02", 6)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ha = [e for e in b.almacen.leer("HA") if e.get("run_id") == r["run_id"] and e.get("agente") == "AG-02"]
    assert [e["tipo_entrada"] for e in ha] == ["CAR"] and ha[0]["id"].startswith("CAR-")   # la saturación queda en HA
