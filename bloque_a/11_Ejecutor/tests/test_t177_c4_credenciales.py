"""T-177 · PB-58 pasos 1 y 2: el Buscador de Fuentes Avanzadas (AG-16) envía `solicitudes_credenciales` en el mantenimiento
C4 y el Coordinador (AG-01) las deduplica, comprueba en HT-01 y emite el CT-25 (Documento 0 V5.3, 7.10.1 y 7.10.2).

Los valores de prueba van partidos en dos cadenas (como en el resto del repo) y nunca son credenciales reales."""
import importlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.mantenimiento_c4 import mantenimiento_c4, servicios_bfa
from conftest import AS_OF, DATOS, RAIZ, config_pruebas, nuevo_bloque

mock_respuestas = importlib.import_module("bloque_a.mock_respuestas")
SERVICIO = "API de fondos cerrados"
OTRO = "Datos de posicionamiento de pago"
FICHA = {"servicio": SERVICIO, "uso_previsto": "Cribado de FON con descuentos sobre el NAV",
         "impacto_si_falta": "Datos públicos semanales con su calidad declarada"}
FICHA_OTRO = {"servicio": OTRO, "uso_previsto": "Posicionamiento CFTC ampliado", "impacto_si_falta": "Solo el informe público"}
VALOR = "valor-de-prueba-" + "t177-QWE"


def _bloque(tmp, universo, servicios=(FICHA,)):
    b = nuevo_bloque(tmp, universo, cfg=config_pruebas(credenciales={"servicios_bfa": list(servicios)}))
    _mensajes(b)
    return b


def _mensajes(b):
    """Los mensajes completos que crea la mensajería (su `registro` solo guarda la traza)."""
    if not hasattr(b, "_t177_mensajes"):
        b._t177_mensajes, crear = [], b.mensajeria.crear

        def espia(*a, **kw):
            m = crear(*a, **kw)
            b._t177_mensajes.append(m)
            return m
        b.mensajeria.crear = espia
    return b._t177_mensajes


def _ct25(b, emisor="AG-01"):
    return [m for m in _mensajes(b) if m["contrato"] == "CT-25" and m["emisor"] == emisor]


def _espiar(b):
    vistos, generar = [], b.cliente.generar

    def espia(**kw):
        vistos.append({"agente": kw["agente"], "texto": json.dumps([kw["system"], kw["mensajes"]], ensure_ascii=False, default=str)})
        return generar(**kw)
    b.cliente.generar = espia
    return vistos


def _sin_valor_en_ningun_sitio(tmp, b, valor, entregables=()):
    for p in (Path(tmp) / "estado").rglob("*"):
        if p.is_file() and p.name != "secretos.json":
            assert valor not in p.read_text(encoding="utf-8", errors="ignore"), p
    for ruta in entregables:
        assert valor not in Path(ruta).read_text(encoding="utf-8"), ruta
    assert valor not in json.dumps(_mensajes(b), default=str) and valor not in json.dumps(b.mensajeria.registro, default=str)


# ---------------------------------------------------------------- CA-1 y CA-2 · paso 1 (BFA en C4) y paso 2 (CT-25)
def test_t177_pb58_c4_bfa_solicita_y_coordinador_emite_ct25(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    vistos = _espiar(b)
    r = mantenimiento_c4(b, AS_OF)
    # Paso 1: AG-16 recibe el estado de la bóveda (alias y estado, sin valor) y devuelve la solicitud
    bfa = [v for v in vistos if v["agente"] == "AG-16"]
    assert len(bfa) == 1 and "MANTENIMIENTO_C4" in bfa[0]["texto"] and "AUSENTE" in bfa[0]["texto"]
    assert "boveda://ht01/api-de-fondos-cerrados" in bfa[0]["texto"]
    assert r["estado_retorno"] == "COMPLETO" and r["servicios_revisados"] == [{"servicio": SERVICIO, "estado": "AUSENTE"}]
    # Paso 2: un CT-25 del Coordinador al Broker con el servicio, el uso, el solicitante y el impacto
    ct25 = _ct25(b)
    assert len(ct25) == 1 and ct25[0]["receptor"] == "BROKER"
    cuerpo = ct25[0]
    assert cuerpo["servicio"] == SERVICIO and cuerpo["solicitante"] == "AG-16"
    assert cuerpo["uso_previsto"] == FICHA["uso_previsto"] and cuerpo["impacto_si_falta"] == FICHA["impacto_si_falta"]
    [sol] = r["solicitudes"]
    assert sol["resultado"] == "SOLICITADA" and sol["crd_id"].startswith("CRD-") and cuerpo["crd_id"] == sol["crd_id"]
    crd = b.almacen.estado("F5", clave="crd_id")[sol["crd_id"]]
    assert crd["tipo_entrada"] == "CRD" and crd["estado"] == "SOLICITADA" and crd["credencial_ref"] is None
    assert crd["solicitante"] == "AG-16" and crd["estado_boveda"] == "AUSENTE"
    c4 = b.almacen.estado("F5")[r["id"]]
    assert c4["tipo_entrada"] == "C4_CREDENCIALES" and c4["agente"] == "AG-16" and c4["solicitudes"][0]["crd_id"] == sol["crd_id"]
    assert b.credenciales.degradaciones(AS_OF) == [{"servicio": SERVICIO, "crd_id": sol["crd_id"], "estado": "SOLICITADA"}]


# ---------------------------------------------------------------- CA-3 · deduplicación y comprobación en HT-01
def test_t177_desde_retorno_deduplica_y_comprueba_ht01(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    b.credenciales.boveda.depositar(OTRO, VALOR, "2027-12-31")   # ya PROVISTA: no se pide
    retorno = {"solicitudes_credenciales": [
        {"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i"},
        {"servicio": "  api de FONDOS cerrados ", "motivo": "m2", "impacto_si_falta": "i2"},   # mismo alias de la bóveda
        {"servicio": OTRO, "motivo": "m", "impacto_si_falta": "i", "urgencia": "ALTA"}]}
    r = b.credenciales.desde_retorno(retorno, "AG-16", AS_OF, origen="C4-prueba")
    assert [s["resultado"] for s in r["solicitudes"]] == ["SOLICITADA", "PROVISTA"]
    assert r["solicitudes"][1]["credencial_ref"] == "boveda://ht01/datos-de-posicionamiento-de-pago"
    assert r["descartadas"] == [{"indice": 1, "motivo": "duplicada de la solicitud 0"}]
    assert len(_ct25(b)) == 1 and _ct25(b)[0]["servicio"] == SERVICIO
    # Segunda C4 con la solicitud abierta: ningún CT-25 nuevo
    r2 = b.credenciales.desde_retorno(retorno, "AG-16", AS_OF)
    assert r2["solicitudes"][0]["resultado"] == "YA_SOLICITADA" and len(_ct25(b)) == 1


def test_t177_urgencia_y_denegada_no_se_vuelve_a_pedir(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    # segunda ronda de cierre (H-18): una urgencia fuera de la lista ya no se reduce a NORMAL, sino que rechaza el retorno
    r0 = b.credenciales.desde_retorno({"solicitudes_credenciales": [
        {"servicio": SERVICIO, "motivo": "m", "impacto": "i", "urgencia": "MUY_ALTA"}]}, "AG-16", AS_OF)
    assert r0["rechazo"] == "VALOR_DE_CREDENCIAL_EN_EL_RETORNO" and not _ct25(b)
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [
        {"servicio": SERVICIO, "motivo": "m", "impacto": "i", "urgencia": "ALTA"}]}, "AG-16", AS_OF)
    assert r["solicitudes"][0]["resultado"] == "SOLICITADA" and _ct25(b)[0]["urgencia"] == "ALTA"
    b.credenciales.responder({"crd_id": r["solicitudes"][0]["crd_id"], "estado": "DENEGADA"}, AS_OF)
    r2 = mantenimiento_c4(b, AS_OF)
    assert r2["solicitudes"][0]["resultado"] == "DENEGADA" and len(_ct25(b)) == 1   # sin cambio de circunstancias


# ---------------------------------------------------------------- CA-4 · fallo cerrado
@pytest.mark.parametrize("solicitud", [
    {"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i", "valor": VALOR},
    {"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i", "detalle": {"api_key": VALOR}},
    {"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i", "Token": VALOR},
])
def test_t177_retorno_con_valor_se_rechaza_integro(tmp_path, universo, solicitud):
    b = _bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    otra = {"servicio": OTRO, "motivo": "m", "impacto_si_falta": "i"}
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [otra, solicitud]}, "AG-16", AS_OF, origen="C4-x")
    assert r == {"solicitudes": [], "descartadas": [], "rechazo": "VALOR_DE_CREDENCIAL_EN_EL_RETORNO"}
    assert not _ct25(b)                                                        # íntegro: tampoco la solicitud limpia
    inc = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]
    assert len(inc) == 1 and inc[0]["objeto"] == "AG-16"
    _sin_valor_en_ningun_sitio(tmp_path, b, VALOR)


def test_t177_c4_con_valor_en_el_retorno_del_bfa_no_emite_nada(tmp_path, universo, monkeypatch):
    """Por el camino entero: el retorno simulado de AG-16 trae el valor; no sale ningún CT-25 y el valor no queda en nada."""
    original = mock_respuestas._mantenimiento_c4

    def con_valor(msg):
        d = original(msg)
        d["solicitudes_credenciales"][0]["valor"] = VALOR
        return d
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", con_valor)
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    assert r["solicitudes"] == [] and not _ct25(b)
    # `llm.respuesta_segura` la bloquea antes de la caché y de la cinta (T-177 r02, H-01 y H-04)
    assert r["estado_retorno"] == "SIN_RESULTADO"
    assert [e for e in b.almacen.leer("HA") if e.get("objeto") == "AG-16"
            and "turno no utilizable (contenido_sensible)" in e.get("detalle", "")]
    _sin_valor_en_ningun_sitio(tmp_path, b, VALOR)


def test_t177_solicitudes_mal_formadas_se_descartan_con_motivo(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [
        "texto suelto", {"servicio": "", "motivo": "m", "impacto_si_falta": "i"}, {"servicio": SERVICIO, "motivo": "m"},
        {"servicio": SERVICIO, "motivo": 3, "impacto_si_falta": "i"}]}, "AG-16", AS_OF)
    assert r["solicitudes"] == [] and not _ct25(b)
    assert [d["motivo"] for d in r["descartadas"]] == ["la solicitud no es un objeto", "faltan servicio", "faltan impacto_si_falta",
                                                       "faltan motivo"]
    r2 = b.credenciales.desde_retorno({"solicitudes_credenciales": {"servicio": SERVICIO}}, "AG-16", AS_OF)
    assert r2["descartadas"] == [{"indice": None, "motivo": "solicitudes_credenciales no es una lista"}] and not _ct25(b)


def test_t177_retorno_vacio_o_sin_solicitudes_no_pide_nada(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    assert b.credenciales.desde_retorno(None, "AG-16", AS_OF) == {"solicitudes": [], "descartadas": [], "rechazo": None}
    assert b.credenciales.desde_retorno({"sintesis": "x"}, "AG-16", AS_OF)["solicitudes"] == []
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: {"referencias": []})   # no cumple BUSQUEDA
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "SIN_RESULTADO" and r["solicitudes"] == [] and not _ct25(b)


@pytest.mark.parametrize("servicios", [
    "no es una lista", [{"servicio": SERVICIO}], [{**FICHA, "uso_previsto": "  "}], [FICHA, {**FICHA, "servicio": SERVICIO.upper()}]])
def test_t177_configuracion_invalida_falla_antes_de_mutar(tmp_path, universo, servicios):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(credenciales={"servicios_bfa": servicios}))
    _mensajes(b)
    antes = len(b.almacen.leer("F5")), len(b.mensajeria.registro)
    with pytest.raises((ValueError, TypeError)):
        mantenimiento_c4(b, AS_OF)
    assert (len(b.almacen.leer("F5")), len(b.mensajeria.registro)) == antes


def test_t177_por_defecto_sin_servicios_no_pide_nada(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    _mensajes(b)
    vistos = _espiar(b)
    assert servicios_bfa(b.cfg) == []
    r = mantenimiento_c4(b, AS_OF)
    assert r["servicios_revisados"] == [] and r["solicitudes"] == [] and not _ct25(b)
    # T-177 r02 (QA r01, H-07 a): sin servicios no se llama al BFA ni se gastan UC
    assert r["estado_retorno"] == "SIN_SERVICIOS" and r["uc"] == 0 and not vistos


# ---------------------------------------------------------------- CA-5 · PB-58, criterio completo (pasos 1 a 4)
def test_t177_pb58_criterio_completo(tmp_path, universo):
    b = _bloque(tmp_path, universo, servicios=(FICHA, FICHA_OTRO))
    vistos = _espiar(b)
    # 1) y 2): el BFA detecta en C4 las dos credenciales AUSENTE y el Coordinador emite dos CT-25
    r1 = mantenimiento_c4(b, AS_OF)
    crd = {s["servicio"]: s["crd_id"] for s in r1["solicitudes"]}
    assert set(crd) == {SERVICIO, OTRO} and len(_ct25(b)) == 2
    # Mientras falte: servicio degradado y declarado en los entregables
    c1 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert [x for x in c1["paquete"]["limitaciones"] if SERVICIO in x and crd[SERVICIO] in x]
    # 3) El Broker deposita en la bóveda (fuera de banda) y responde PROVISTA con el alias
    d = b.credenciales.depositar(crd[SERVICIO], VALOR, "2027-12-31", AS_OF)
    assert d == {"crd_id": crd[SERVICIO], "estado": "PROVISTA", "credencial_ref": "boveda://ht01/api-de-fondos-cerrados"}
    retorno = _ct25(b, "BROKER")
    assert len(retorno) == 1 and VALOR not in json.dumps(retorno)
    # La herramienta (y solo ella) obtiene el valor de la bóveda
    assert b.credenciales.boveda.valor_para_herramienta(d["credencial_ref"], pd.Timestamp(AS_OF).date()) == VALOR
    # 4) Se repite la petición: la segunda C4 se resuelve sin molestar al Broker
    n = len(_ct25(b))
    encargos, invocar = [], b._invocar
    b._invocar = lambda agente, contrato, msg, *a, **kw: (encargos.append(msg), invocar(agente, contrato, msg, *a, **kw))[1]
    r2 = mantenimiento_c4(b, str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()))
    assert {s["servicio"]: s["resultado"] for s in r2["solicitudes"]} == {OTRO: "YA_SOLICITADA"}
    assert {s["servicio"]: s["estado"] for s in r2["servicios_revisados"]} == {SERVICIO: "PROVISTA", OTRO: "AUSENTE"}
    assert len(_ct25(b)) == n
    # El BFA solo ve alias y estado de la bóveda (HT-01, «solo estado»): ni el índice entero ni, por supuesto, el valor
    [enc] = encargos
    assert [set(s) for s in enc["servicios"]] == [{"servicio", "uso_previsto", "impacto_si_falta", "credencial_ref", "estado"}] * 2
    c2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()), alcance={"clases": ["RV"]})
    assert not [x for x in c2["paquete"]["limitaciones"] if SERVICIO in x]
    assert [x for x in c2["paquete"]["limitaciones"] if OTRO in x]
    # Cero apariciones del valor: contextos de agentes, F1–F11, HA, mensajes y entregables
    assert vistos and not [v for v in vistos if VALOR in v["texto"]]
    _sin_valor_en_ningun_sitio(tmp_path, b, VALOR, list(c1["entregables"].values()) + list(c2["entregables"].values()))


# ---------------------------------------------------------------- CLI · `credencial c4` con el cliente simulado
def test_t177_cli_credencial_c4(tmp_path):
    cfg = tmp_path / "c.yaml"
    cfg.write_text(json.dumps({"credenciales": {"servicios_bfa": [FICHA]}}, ensure_ascii=False), encoding="utf-8")
    base = [sys.executable, "-m", "bloque_a.cli", "--config", str(cfg), "--datos", str(DATOS), "--estado", str(tmp_path / "e"),
            "--salida", str(tmp_path / "s"), "--as-of", AS_OF]
    env = {"PYTHONPATH": str(RAIZ), "PATH": "/usr/bin:/bin"}

    def run(*args):
        out = subprocess.run(base + list(args), capture_output=True, text=True, cwd=RAIZ, env=env, timeout=600, check=False)
        assert out.returncode == 0, out.stderr[-2000:]
        return json.loads(out.stdout)
    r = run("credencial", "c4")
    assert r["tipo_entrada"] == "C4_CREDENCIALES" and r["solicitudes"][0]["resultado"] == "SOLICITADA"
    assert run("credencial", "c4")["solicitudes"][0]["resultado"] == "YA_SOLICITADA"


# ---------------------------------------------------------------- T-177 r02 · hallazgos de la QA r01
S2 = "QaFicticioR02" + "x9Yy8Ww"


def _aparece(tmp, valor):
    return sorted(str(p.relative_to(tmp)) for p in Path(tmp).rglob("*")
                  if p.is_file() and p.name != "secretos.json" and valor in p.read_text(encoding="utf-8", errors="ignore"))


@pytest.mark.parametrize("retorno", [
    {"referencias": [], "sintesis": "s", "lagunas": [], "solicitudes_credenciales": [{"servicio": SERVICIO, "motivo": "m",
                                                                                     "impacto_si_falta": "i"}], "valor": S2},
    {"referencias": [], "sintesis": "s", "lagunas": [], "Solicitudes_Credenciales": [{"servicio": SERVICIO, "motivo": "m",
                                                                                     "impacto_si_falta": "i", "valor": S2}]},
], ids=["valor_en_raiz", "clave_en_mayusculas"])
def test_t177_r02_h01_valor_en_cualquier_sitio_no_llega_a_la_cache(tmp_path, universo, monkeypatch, retorno):
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: retorno)
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "SIN_RESULTADO" and r["solicitudes"] == [] and not _ct25(b)
    assert _aparece(tmp_path, S2) == []


def test_t177_r02_h04_la_cinta_de_grabacion_no_guarda_el_valor(tmp_path, universo, monkeypatch):
    from bloque_a.llm import MockClient, ReplayClient
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: {
        "referencias": [], "sintesis": "s", "lagunas": [],
        "solicitudes_credenciales": [{"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i", "valor": S2}]})
    cinta = tmp_path / "cinta.jsonl"
    b = nuevo_bloque(tmp_path, universo, cliente=ReplayClient(cinta, "grabar", MockClient()),
                     cfg=config_pruebas(credenciales={"servicios_bfa": [FICHA]}))
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "SIN_RESULTADO" and cinta.exists()
    assert _aparece(tmp_path, S2) == []


def test_t177_r02_solicitud_con_valor_limites():
    from bloque_a.llm import solicitud_con_valor
    sol = {"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i"}
    assert not solicitud_con_valor(json.dumps({"referencias": [{"valor": 3.2, "token": "x"}]}))   # sin el campo: no se mira
    assert not solicitud_con_valor(json.dumps({"solicitudes_credenciales": [sol], "senales": {"valor": 3.2}}))   # numérico
    # cierre (QA r03, H-17): un campo de más con contenido en una solicitud descarta el retorno, también `credencial_ref`
    assert not solicitud_con_valor(json.dumps({"solicitudes_credenciales": [{**sol, "credencial_ref": None}]}))
    assert solicitud_con_valor(json.dumps({"solicitudes_credenciales": [{**sol, "credencial_ref": "boveda://ht01/x"}]}))
    assert solicitud_con_valor(json.dumps({"solicitudes_credenciales": [sol], "x": {"API-Key": S2}}))
    assert solicitud_con_valor('{"solicitudes_credenciales": [ roto')                                 # ilegible: falla cerrado
    assert solicitud_con_valor('{"solicitudes_credenciales": [ roto }')                               # con llaves, ilegible
    assert solicitud_con_valor("```json\n" + json.dumps({"SOLICITUDES-CREDENCIALES": [{**sol, "Contraseña": S2}]}) + "\n```")


def test_t177_r02_h02_otra_grafia_en_la_segunda_c4_no_duplica(tmp_path, universo, monkeypatch):
    grafias = iter([SERVICIO, SERVICIO.lower()])
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: {
        "referencias": [], "sintesis": "s", "lagunas": [],
        "solicitudes_credenciales": [{"servicio": next(grafias), "motivo": "m", "impacto_si_falta": "i"}]})
    b = _bloque(tmp_path, universo)
    r1, r2 = mantenimiento_c4(b, AS_OF), mantenimiento_c4(b, AS_OF)
    assert r1["solicitudes"][0]["resultado"] == "SOLICITADA" and r2["solicitudes"][0]["resultado"] == "YA_SOLICITADA"
    assert len(_ct25(b)) == 1


def test_t177_r02_h03_dos_c4_a_la_vez_un_solo_ct25(tmp_path, universo):
    """H-03 en el Coordinador: dos `desde_retorno` a la vez (barrera en `solicitar`) dan una sola CRD-. Y dos C4 a la vez
    (r03): la segunda ve la bolsa reservada (SIN_PRESUPUESTO) o la solicitud abierta (YA_SOLICITADA); un solo CT-25."""
    import threading
    b1, b2 = _bloque(tmp_path, universo), _bloque(tmp_path, universo)
    barrera = threading.Barrier(2)
    for b in (b1, b2):
        orig = b.credenciales.solicitar

        def solicitar(*a, _o=orig, **kw):
            barrera.wait(timeout=30)
            return _o(*a, **kw)
        b.credenciales.solicitar = solicitar
    retorno = {"solicitudes_credenciales": [{"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i"}]}
    res = []
    hilos = [threading.Thread(target=lambda b=b: res.append(b.credenciales.desde_retorno(retorno, "AG-16", AS_OF)))
             for b in (b1, b2)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join(60)
    crd = [c for c in b1.almacen.estado("F5").values() if c.get("tipo_entrada") == "CRD"]
    assert len(res) == 2 and len(crd) == 1
    assert sorted(x["solicitudes"][0]["resultado"] for x in res) == ["SOLICITADA", "YA_SOLICITADA"]
    assert len(_ct25(b1)) + len(_ct25(b2)) == 1
    b3, b4 = _bloque(tmp_path / "c4", universo), _bloque(tmp_path / "c4", universo)
    res2 = []
    hilos = [threading.Thread(target=lambda b=b: res2.append(mantenimiento_c4(b, AS_OF))) for b in (b3, b4)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join(120)
    assert len(res2) == 2 and len(_ct25(b3)) + len(_ct25(b4)) == 1
    assert "COMPLETO" in [x["estado_retorno"] for x in res2]


def test_t177_r03_reserva_de_la_bolsa_en_curso_y_tras_un_error(tmp_path, universo, monkeypatch):
    """La C4 en curso reserva lo que queda de la bolsa: otra C4 a la vez no tiene nada (SIN_PRESUPUESTO). Si la llamada falla,
    la reserva se sustituye por lo gastado (ERROR) y la bolsa vuelve."""
    import bloque_a.mantenimiento_c4 as mc4
    b = _bloque(tmp_path, universo)
    otra = []
    invocar = b._invocar

    def durante(*a, **kw):
        otra.append(mc4.mantenimiento_c4(_bloque(tmp_path, universo), AS_OF))   # otra C4 mientras esta está en curso
        return invocar(*a, **kw)
    b._invocar = durante
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "COMPLETO" and otra[0]["estado_retorno"] == "SIN_PRESUPUESTO"
    assert mc4.uc_c4_semana(b, AS_OF) == pytest.approx(r["uc"])                  # la reserva ya no cuenta
    b2 = _bloque(tmp_path, universo)

    def falla(*a, **kw):
        raise RuntimeError("caída simulada")
    b2._invocar = falla
    with pytest.raises(RuntimeError):
        mantenimiento_c4(b2, AS_OF)
    ultima = [e for e in b2.almacen.estado("F5").values() if e.get("tipo_entrada") == "C4_CREDENCIALES"][-1]
    assert ultima["estado_retorno"] == "ERROR" and ultima["uc"] == 0
    assert mc4.uc_c4_semana(b2, AS_OF) == pytest.approx(r["uc"])


@pytest.mark.parametrize("campo", ["credencial", "credential", "secret", "contraseña", "Contrasena", "passwd", "pwd",
                                   "access_token", "api-key", "ApiKey", "VALOR_CREDENCIAL"])
def test_t177_r02_h05_grafias_de_campos_de_valor(tmp_path, universo, campo):
    b = _bloque(tmp_path, universo)
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [
        {"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i", campo: S2}]}, "AG-16", AS_OF)
    assert r["rechazo"] == "VALOR_DE_CREDENCIAL_EN_EL_RETORNO" and not _ct25(b)


def test_t177_r02_h05_credencial_ref_no_es_un_valor_y_el_broker_tampoco_lo_cuela(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [
        {"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i", "credencial_ref": None}]}, "AG-16", AS_OF)
    assert r["rechazo"] is None and r["solicitudes"][0]["resultado"] == "SOLICITADA"
    # La respuesta del Broker con «Credencial» (otra grafía, que los patrones de texto no reconocen) se rechaza íntegra
    x = b.credenciales.responder({"crd_id": r["solicitudes"][0]["crd_id"], "estado": "PROVISTA", "Credencial": S2}, AS_OF)
    assert x["estado"] == "RECHAZADA_CREDENCIAL_EXPUESTA"
    assert _aparece(tmp_path, S2) == []


@pytest.mark.parametrize("campo,texto", [("motivo", "usar " + S2), ("servicio", "API " + S2),
                                         ("impacto_si_falta", "sin " + S2), ("motivo", "LEI 5493001KJTIIGC8Y1R12")])
def test_t177_r02_h06_ficha_opaca_en_texto_libre_se_rechaza(tmp_path, universo, campo, texto):
    b = _bloque(tmp_path, universo)
    sol = {"servicio": OTRO, "motivo": "m", "impacto_si_falta": "i", campo: texto}
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [{**FICHA_OTRO, "motivo": "m", "impacto_si_falta": "i"}, sol]},
                                     "AG-16", AS_OF, origen="C4-x")
    assert r["rechazo"] == "VALOR_DE_CREDENCIAL_EN_EL_RETORNO" and not _ct25(b)   # íntegro: tampoco la primera
    assert [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]
    assert _aparece(tmp_path, texto.split()[-1]) == []


def test_t177_r02_h06_textos_corrientes_y_urls_no_se_rechazan(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [{
        "servicio": "API de posicionamiento CFTC 2026", "motivo": "Series semanales desde 2010 en https://www.cftc.gov/x.html",
        "impacto_si_falta": "Solo el informe público del COT"}]}, "AG-16", AS_OF)
    assert r["rechazo"] is None and r["solicitudes"][0]["resultado"] == "SOLICITADA"


def test_t177_r02_h07_tope_semanal_real(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    llamadas = []
    invocar = b._invocar
    b._invocar = lambda *a, **kw: (llamadas.append(kw["presupuesto"].asignado["C4"]), invocar(*a, **kw))[1]
    r1 = mantenimiento_c4(b, AS_OF)
    assert r1["estado_retorno"] == "COMPLETO" and r1["uc"] > 0
    r2 = mantenimiento_c4(b, AS_OF)
    assert llamadas[1] == pytest.approx(llamadas[0] - r1["uc"])        # la bolsa es la semanal menos lo gastado
    # Con lo gastado de la semana igual a la bolsa, no se llama: SIN_PRESUPUESTO
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "C4_CREDENCIALES", "id": "C4-prueba", "agente": "AG-16",
                                        "fecha": AS_OF, "uc": float(b.cfg["mantenimiento_c4"]["presupuesto_uc_semana"]["BFA"])})
    n = len(llamadas)
    r3 = mantenimiento_c4(b, AS_OF)
    assert r3["estado_retorno"] == "SIN_PRESUPUESTO" and r3["uc"] == 0 and len(llamadas) == n
    # Pasada la semana (7 días de HT-05), la bolsa vuelve entera
    dia8 = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date())
    r4 = mantenimiento_c4(b, dia8)
    assert r4["estado_retorno"] == "COMPLETO" and r2["uc"] > 0
    assert llamadas[-1] == pytest.approx(float(b.cfg["mantenimiento_c4"]["presupuesto_uc_semana"]["BFA"]))


def test_t177_r02_ficha_opaca_en_el_retorno_no_llega_a_la_cache(tmp_path, universo, monkeypatch):
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: {
        "referencias": [], "sintesis": "s", "lagunas": [],
        "solicitudes_credenciales": [{"servicio": SERVICIO, "motivo": "usar " + S2, "impacto_si_falta": "i"}]})
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "SIN_RESULTADO" and not _ct25(b) and _aparece(tmp_path, S2) == []


def test_t177_r02_segunda_barrera_en_agentes(tmp_path, universo, monkeypatch):
    """Sin la primera barrera (`respuesta_segura`), `agentes.invocar` tampoco guarda ni sirve una solicitud con valor."""
    import bloque_a.agentes as ag
    monkeypatch.setattr(ag, "respuesta_segura", lambda r: r)
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: {
        "referencias": [], "sintesis": "s", "lagunas": [],
        "solicitudes_credenciales": [{"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i", "valor": S2}]})
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "SIN_RESULTADO" and not _ct25(b) and _aparece(tmp_path, S2) == []


def test_t177_r02_la_cache_envenenada_no_se_sirve(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    envenenado = {"referencias": [], "sintesis": "s", "lagunas": [],
                  "solicitudes_credenciales": [{"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i", "valor": S2}]}
    b.agentes.cache.obtener = lambda clave: envenenado
    r = mantenimiento_c4(b, AS_OF)
    # no se sirve lo envenenado: se pide de nuevo al simulado, que contesta limpio
    assert r["estado_retorno"] == "COMPLETO" and r["solicitudes"][0]["resultado"] == "SOLICITADA"
    assert _aparece(tmp_path, S2) == []


# ---------------------------------------------------------------- T-177 r03 · hallazgos de la QA r02
S3 = "QaFicticioR03" + "k7Jm2Pq"
SOL = {"servicio": SERVICIO, "motivo": "m", "impacto_si_falta": "i"}


def _ret3(sol, **top):
    return json.dumps({"referencias": [], "sintesis": "s", "lagunas": [], "solicitudes_credenciales": sol, **top},
                      ensure_ascii=False)


def test_t177_r03_h12_informe_de_analista_canonico_no_se_descarta():
    from bloque_a.llm import solicitud_con_valor
    inf = {"clase": "RF", "estado": "COMPLETO", "regimen_clase": {"diagnostico": "d", "indicadores": [
        {"nombre": "Tipo a 10 años", "valor": "4,25 %", "fecha": "2024-03-01", "fuente": "HT-01"}]},
        "finalistas": [{"token": "ETH", "clave": "CURVA-USD-2S10S-TR", "credencial": "sin credencial de pago"}],
        "consultas_broker": [], "solicitudes_credenciales": [], "lagunas": [], "autoevaluacion": "ok"}
    assert not solicitud_con_valor(json.dumps(inf, ensure_ascii=False))
    # Fuera del subárbol: una clave inequívoca con texto, o una ambigua con ficha opaca, sí
    assert solicitud_con_valor(json.dumps({**inf, "password": "corta"}))
    assert solicitud_con_valor(json.dumps({**inf, "regimen_clase": {"indicadores": [{"valor": S3}]}}))


def test_t177_r03_el_mock_de_analistas_ejerce_la_barrera():
    """El simulado de los Analistas devuelve `solicitudes_credenciales: []` e `indicadores[].valor` de texto (H-12)."""
    import random
    d = mock_respuestas._analista({"clase": "RV", "fase": "CRIBADO", "universo": []}, {"fecha_as_of": "2024-03-01"},
                                  random.Random(0), False)
    assert d["solicitudes_credenciales"] == [] and isinstance(d["regimen_clase"]["indicadores"][0]["valor"], str)


@pytest.mark.parametrize("clave", ["value", "wert", "senha", "key", "secret_value", "パスワード", "clé", "vａlor", "urgencia"])
def test_t177_r03_h08_cualquier_clave_del_subarbol(clave):
    from bloque_a.llm import solicitud_con_valor
    assert solicitud_con_valor(_ret3([{**SOL, clave: S3}]))


@pytest.mark.parametrize("sol", [json.dumps([{**SOL, "valor": S3}]), [{**SOL, "motivo": {"texto": "usar " + S3}}],
                                 [{**SOL, S3: "x"}]], ids=["lista_como_texto", "motivo_dict", "en_la_clave"])
def test_t177_r03_h08_texto_json_dict_y_claves(tmp_path, universo, sol):
    from bloque_a.llm import solicitud_con_valor
    assert solicitud_con_valor(_ret3(sol))
    b = _bloque(tmp_path, universo)
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": sol}, "AG-16", AS_OF)   # también en el Coordinador
    assert r["rechazo"] == "VALOR_DE_CREDENCIAL_EN_EL_RETORNO" and not _ct25(b)


def test_t177_r03_h08_solicitud_no_vacia_mira_el_retorno_entero():
    from bloque_a.llm import solicitud_con_valor
    assert solicitud_con_valor(_ret3([SOL], lagunas=["usar " + S3]))
    assert not solicitud_con_valor(_ret3([], lagunas=["huella " + S3]))   # sin solicitudes, el texto libre no se mira aquí


def test_t177_r03_h09_escape_unicode_en_la_clave():
    from bloque_a.llm import solicitud_con_valor
    texto = '{"solicitudes\\u005fcredenciales": [{"servicio": "s", "motivo": "m", "impacto_si_falta": "i", "valor": "x"}]}'
    assert solicitud_con_valor(texto)
    assert solicitud_con_valor("solicitudes_credenciales: valor sin JSON")          # ilegible y nombra el campo
    assert not solicitud_con_valor("texto libre sin JSON")


@pytest.mark.parametrize("cod", ["QaR0/2Fict+icio8/8YyWw+Zz9k/Lm3n", "UWFSMDNGaWN0aWNpbzg4WXlXdw"], ids=["b64_barras", "b64"])
def test_t177_r03_h10_base64(cod):
    from bloque_a.contratos import ficha_opaca
    assert ficha_opaca("usar " + cod)
    assert not ficha_opaca("https://www.cftc.gov/MarketReports/CommitmentsofTraders/index2024.htm")


def test_t177_r03_h11_numero_bajo_clave_de_valor(tmp_path, universo, monkeypatch):
    from bloque_a.llm import solicitud_con_valor
    assert solicitud_con_valor(_ret3([{**SOL, "valor": 4041773129}]))
    assert not solicitud_con_valor(_ret3([{**SOL, "valor": True}]))   # un booleano no es un valor
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: json.loads(_ret3([{**SOL, "valor": 4041773129}])))
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "SIN_RESULTADO" and _aparece(tmp_path, "4041773129") == []


@pytest.mark.parametrize("motivo", ["Serie CURVA-USD-2S10S-TR del universo", "Índice ICE-BofA-US-HY-2024",
                                    "id 123e4567-e89b-12d3-a456-426614174000"])
def test_t177_r03_h13_guiones_y_uuid_no_son_fichas(motivo):
    from bloque_a.llm import solicitud_con_valor
    assert not solicitud_con_valor(_ret3([{**SOL, "motivo": motivo}]))   # el UUID: límite declarado en INC-T177-01
    assert solicitud_con_valor(_ret3([{**SOL, "motivo": "usar " + S3}]))


def test_t177_r03_el_coordinador_rechaza_una_clave_de_valor_en_cualquier_sitio(tmp_path, universo):
    """En el Coordinador, una clave de valor fuera de las solicitudes también rechaza el retorno, aunque sea ambigua y corta
    (más estricto que la barrera de `respuesta_segura`, que la dejaría pasar en un informe corriente)."""
    b = _bloque(tmp_path, universo)
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [SOL], "valor": "corto"}, "AG-16", AS_OF)
    assert r["rechazo"] == "VALOR_DE_CREDENCIAL_EN_EL_RETORNO" and not _ct25(b)


def test_t177_r03_json_demasiado_anidado():
    """Un JSON demasiado anidado para leerlo se trata como ilegible: sin el campo, no es sensible (la llamada queda PARCIAL por
    JSON no válido, T-146); si nombra el campo, sí (falla cerrado)."""
    from bloque_a.llm import solicitud_con_valor
    assert not solicitud_con_valor("[" * 200000 + "]" * 200000)
    assert solicitud_con_valor('{"solicitudes_credenciales": ' + "[" * 200000 + "]" * 200000 + "}")



# ---------------------------------------------------------------- T-177 · ronda de cierre de la QA r03
def test_t177_cierre_h14_texto_ilegible_con_la_clave_escapada():
    from bloque_a.llm import solicitud_con_valor
    assert solicitud_con_valor('{"solicitudes\\u005fcredenciales": [{"servicio": "x"}] ,,, }')
    assert not solicitud_con_valor('{"sin\\u005fcampo": 1 ,,, }')


@pytest.mark.parametrize("informe,bloqueado", [
    ({"activos": [{"token": "0x" + "ab12" * 10}], "solicitudes_credenciales": []}, False),           # dirección pública
    ({"emisores": [{"clave": "5493001KJTIIGC8Y1R12"}], "solicitudes_credenciales": []}, False),     # LEI válido
    ({"activos": [{"token": "0x" + "ab12" * 16}], "solicitudes_credenciales": []}, True),            # clave privada de 64
    ({"emisores": [{"clave": "5493001KJTIIGC8Y1R13"}], "solicitudes_credenciales": []}, True),      # LEI con módulo erróneo
    ({"finalistas": [{"lei": "5493001KJTIIGC8Y1R12"}], "solicitudes_credenciales": [SOL]}, True),   # con solicitud: se mira entero
], ids=["dir_0x_40", "lei_valido", "clave_0x_64", "lei_invalido", "lei_con_solicitud"])
def test_t177_cierre_h15_identificadores_publicos_solo_fuera(informe, bloqueado):
    from bloque_a.llm import solicitud_con_valor
    assert solicitud_con_valor(json.dumps(informe)) is bloqueado
    # dentro del subárbol el LEI sigue cayendo
    assert solicitud_con_valor(json.dumps({"solicitudes_credenciales": [{**SOL, "motivo": "LEI 5493001KJTIIGC8Y1R12"}]}))


def test_t177_cierre_h16_reserva_huerfana_avisada_una_vez(tmp_path, universo):
    import bloque_a.mantenimiento_c4 as mc4
    b = _bloque(tmp_path, universo)
    # una reserva EN_CURSO de un proceso que ya no existe, con toda la bolsa
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "C4_CREDENCIALES", "id": "C4-2026-9999", "agente": "AG-16", "fecha": AS_OF,
                                        "estado_retorno": "EN_CURSO", "uc": 3.0, "pid": 2 ** 22 + 12345})
    r1, r2 = mantenimiento_c4(b, AS_OF), mantenimiento_c4(b, AS_OF)
    assert r1["estado_retorno"] == r2["estado_retorno"] == "SIN_PRESUPUESTO"
    assert r1["reservas_en_curso"] == ["C4-2026-9999"]
    avisos = [e for e in b.almacen.leer("HA") if e.get("reserva_huerfana") == "C4-2026-9999"]
    assert len(avisos) == 1 and avisos[0]["severidad"] == "Operativa" and "bloqueada hasta" in avisos[0]["detalle"]
    assert mc4.uc_c4_semana(b, AS_OF) == pytest.approx(3.0)                    # no se libera
    # la reserva de un proceso vivo (el propio) no se avisa
    b2 = _bloque(tmp_path / "vivo", universo)
    import os
    b2.almacen.escribir("F5", "AG-01", {"tipo_entrada": "C4_CREDENCIALES", "id": "C4-2026-9998", "agente": "AG-16", "fecha": AS_OF,
                                         "estado_retorno": "EN_CURSO", "uc": 3.0, "pid": os.getpid()})
    assert mantenimiento_c4(b2, AS_OF)["reservas_en_curso"] == ["C4-2026-9998"]
    assert not [e for e in b2.almacen.leer("HA") if e.get("reserva_huerfana")]


@pytest.mark.parametrize("extra", [{"value": "SoloLetrasSinCifras"}, {"pin": 1234}, {"nota": "corta"}, {"credencial_ref": "x"}])
def test_t177_cierre_h17_campo_de_mas_en_una_solicitud(tmp_path, universo, monkeypatch, extra):
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: {
        "referencias": [], "sintesis": "s", "lagunas": [], "solicitudes_credenciales": [{**SOL, **extra}]})
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "SIN_RESULTADO" and not _ct25(b)
    # los cinco campos que lee el Coordinador, y uno vacío de más, siguen pasando
    from bloque_a.llm import solicitud_con_valor
    assert not solicitud_con_valor(json.dumps({"solicitudes_credenciales": [{**SOL, "urgencia": "ALTA", "nota": ""}]}))



# ---------------------------------------------------------------- T-177 · segunda ronda de cierre de la QA r03 (H-18)
CORTO18 = "Hunt" + "er2x!"


@pytest.mark.parametrize("sol", [{**SOL, "urgencia": CORTO18}, {**SOL, "impacto": CORTO18}, {**SOL, "Servicio": CORTO18}],
                         ids=["urgencia_no_enum", "impacto_junto_a_impacto_si_falta", "clave_con_otra_grafia"])
def test_t177_cierre2_h18_campo_admitido_que_no_se_copia(tmp_path, universo, monkeypatch, sol):
    from bloque_a.llm import MockClient, ReplayClient
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: {
        "referencias": [], "sintesis": "s", "lagunas": [], "solicitudes_credenciales": [sol]})
    b = nuevo_bloque(tmp_path, universo, cliente=ReplayClient(tmp_path / "cinta.jsonl", "grabar", MockClient()),
                     cfg=config_pruebas(credenciales={"servicios_bfa": [FICHA]}))
    r = mantenimiento_c4(b, AS_OF)
    assert r["estado_retorno"] == "SIN_RESULTADO" and _aparece(tmp_path, CORTO18) == []


def test_t177_cierre2_h18_lo_que_se_copia_pasa():
    from bloque_a.llm import solicitud_con_valor
    for sol in ({**SOL, "urgencia": "ALTA"}, {**SOL, "urgencia": "NORMAL"},
                {"servicio": "s", "motivo": "m", "impacto": "solo impacto"}, {**SOL, "urgencia": ""}):
        assert not solicitud_con_valor(json.dumps({"solicitudes_credenciales": [sol]})), sol



# ---------------------------------------------------------------- T-177 · tercera ronda de cierre de la QA r03 (H-19)
@pytest.mark.parametrize("urg", [" ", [""], {"": ""}], ids=["espacio", "lista_vacia", "dict_vacio"])
def test_t177_cierre3_h19_urgencia_sin_contenido_se_reduce_a_normal(tmp_path, universo, urg):
    """Una urgencia sin contenido pasa la barrera (no es un valor) y llega a `desde_retorno`, que la reduce a NORMAL: ni la CRD-
    de F5 ni el CT-25 llevan el valor crudo (mata M08)."""
    b = _bloque(tmp_path, universo)
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [{**SOL, "urgencia": urg}]}, "AG-16", AS_OF)
    crd = [c for c in b.almacen.estado("F5").values() if c.get("tipo_entrada") == "CRD"]
    assert r["solicitudes"][0]["resultado"] == "SOLICITADA"
    assert [c["urgencia"] for c in crd] == ["NORMAL"] and [m["urgencia"] for m in _ct25(b)] == ["NORMAL"]
