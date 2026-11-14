"""T-116 · Fase 4: cláusulas del Plan de pruebas V3.0 que ninguna prueba comprobaba (huecos del mapa verificado).

Cada prueba sigue los pasos del plan para su PB y afirma la cláusula del criterio de aprobación que faltaba.
"""
import hashlib
import json

import pandas as pd
import pytest
from bloque_a.almacen import Almacen, EscrituraFueraDeReserva
from bloque_a.configuracion import aplicabilidad
from bloque_a.consumo import Presupuesto
from bloque_a.contratos import CanalNoPrevisto, DatosSensibles, Mensajeria
from bloque_a.evaluador import Evaluador
from conftest import AS_OF, config_pruebas, nuevo_bloque


def _huellas(carpeta):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(carpeta.iterdir()) if p.is_file()}


# ---------------------------------------------------------------- PB-10 · qué cambia en F10 y HA sin incidencia de escritura
def test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas(tmp_path, universo):
    """El plan pide H1 «para ALT»; el CT-04 del ejecutor solo tiene una lista global de horizontes. La celda ALT×H1 se rechaza
    y sigue sin aplicarse, pero la lista se guarda en F10 junto con P-02 (INC-T116-01): no cambia ningún otro parámetro."""
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    antes = b.f10("2026-12-31")
    activas = [c for c in antes["P-02"] if c != "CRI"] if "CRI" in antes["P-02"] else [*antes["P-02"], "CRI"]
    assert "ALT" in activas and aplicabilidad(b.cfg, "ALT", "H1") == "NO"
    d = b.decision({"configuracion": {"clases_activas": activas, "horizontes": ["H1", "H3"], "umbral_E": 50}}, AS_OF)
    assert d["estado"] == "APLICADA_PARCIALMENTE"
    rechazos = {x["parametro"]: x["motivo"] for x in d["rechazos"]}
    assert "CALIBRABLE" in rechazos["umbral_E"] and "«No» para ALT" in rechazos["horizontes:ALT:H1"]
    despues = b.f10("2026-12-31")
    cambiados = {k for k in set(antes) | set(despues) if antes.get(k) != despues.get(k)}
    assert cambiados == {"P-02", "P-03"} and despues["P-02"] == activas and despues["P-03"] == ["H1", "H3"]
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
    assert auts and {e["decision"] for e in auts} == {"DENEGADA"}
    assert r["estado"] == "PARCIAL" and any("MP" in x for x in r["paquete"]["limitaciones"])
    tope = 6.0 * (1 + config_pruebas()["presupuesto_uc"]["ampliacion_sin_autorizacion"])
    assert 0 < r["presupuesto"]["MP"]["consumido"] <= tope and r["presupuesto"]["MP"]["ampliado"] == 0.0
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
    a.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2025-0001", "estado": "VIGENTE",
                               "celda": {"clase": "RV", "horizonte": "H3", "metodo": None}})
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
