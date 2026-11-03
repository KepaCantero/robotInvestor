"""Pruebas de la actualización V5.1 (Documento 0 óptima V5.1): H5 con hitos y horizonte principal, seguimiento
encargado de opción (CT-24, ciclo C6, F11), consultas al Broker (CT-23) y credenciales en la bóveda de HT-01 (CT-25)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import AS_OF, DATOS, RAIZ, nuevo_bloque
from bloque_a.almacen import EscrituraFueraDeReserva
from bloque_a.configuracion import HORIZONTES, NATURALEZAS, TABLA_HORIZONTES, naturaleza_coherente
from bloque_a.contratos import CANALES, canal_permitido
from bloque_a.herramientas import ht09

SEMANA_SIG = "2026-06-12"


@pytest.fixture(scope="module")
def bloque_v51(tmp_path_factory, universo):
    tmp = tmp_path_factory.mktemp("v51")
    b = nuevo_bloque(tmp, universo)
    r = b.ciclo(AS_OF)
    return b, r, tmp


def opciones(r):
    return [o for d in r["paquete"]["clases"].values() for o in d["opciones"]]


# ------------------------------------------------------------------------------------------- H5 y horizonte principal
def test_tabla_y_naturalezas():
    assert HORIZONTES == ("H1", "H2", "H3", "H4", "H5")
    assert {c: TABLA_HORIZONTES[c]["H5"] for c in ("RV", "DER", "MON", "TCV", "ALT")} == \
        {"RV": "SI", "DER": "NO", "MON": "NO", "TCV": "NO", "ALT": "SI"}
    assert NATURALEZAS["ESTRUCTURAL"] == ("H4", "H5") and naturaleza_coherente("LIQUIDEZ", "H3")
    assert not naturaleza_coherente("TACTICA", "H3")


def test_horizonte_principal_y_naturaleza_en_cada_opcion(bloque_v51):
    _, r, _ = bloque_v51
    ops = opciones(r)
    assert ops
    for o in ops:
        assert o["horizonte_principal"] in o["horizontes"]
        assert naturaleza_coherente(o["naturaleza_inversion"], o["horizonte_principal"]) or o.get("justificacion_horizonte")
        if o["tipo_activo"] == "MON":
            assert o["naturaleza_inversion"] == "LIQUIDEZ"
    assert (r.get("g3_entregables") or r["g3"])["dictamen"] != "BLOQUEADO"


def test_h5_con_hitos_y_sin_probabilidad(bloque_v51):
    b, r, _ = bloque_v51
    h5 = [(o, o["horizontes"]["H5"]) for o in opciones(r) if "H5" in o["horizontes"]]
    assert h5, "el mock ofrece H5 en los tipos con aplicabilidad «Sí»"
    f4 = b.almacen.estado("F4")
    for o, v in h5:
        assert TABLA_HORIZONTES[o["tipo_activo"]]["H5"] != "NO"
        assert v["prob"] is None and not v["certificado_r13"] and len(v["hitos"]) >= 3
        prg = f4[v["prg_id"]]
        assert prg["prob_interna"] is None and prg["banda_verbal"] and len(prg["hit_ids"]) == len(v["hitos"])
        for h in prg["hit_ids"]:
            hito = f4[h]
            assert h.startswith("HIT-") and hito["es_hito"] and hito["prg_padre"] == v["prg_id"]
            assert hito["horizonte"] == "H4" and isinstance(hito["prob_interna"], float)
    # JSON entregado válido frente al esquema V5.1 (el H5 lleva hitos; prob nula)
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert all("naturaleza_inversion" in o for d in js["clases"].values() for o in d["opciones"])
    assert not (r.get("g3_entregables") or {}).get("errores_esquema")


def test_estado_h5_por_hitos(bloque_v51):
    b, _, _ = bloque_v51
    est = b.evaluador.estado_h5()
    assert est["pronosticos"] and all(v["estado"] == "EN_CURSO_CONFORME" for v in est["pronosticos"].values())


def test_ht09_bloquea_h5_sin_hitos(bloque_v51):
    b, r, _ = bloque_v51
    import copy
    p = copy.deepcopy(r["paquete"])
    o = next(o for d in p["clases"].values() for o in d["opciones"] if "H5" in o["horizontes"])
    o["horizontes"]["H5"]["hitos"] = []
    res = ht09.validar(p)
    assert next(c for c in res["comprobaciones"] if c["id"] == "C18")["resultado"] == "BLOQUEO"
    o["horizontes"]["H5"]["hitos"] = [{"hit_id": "HIT-2026-0001", "fecha": "2027-06-01", "indicador": "x", "criterio": "y"}] * 3
    o["horizonte_principal"] = "H1"   # CICLICA con principal H1: fuera de rango sin justificación
    res = ht09.validar(p)
    assert next(c for c in res["comprobaciones"] if c["id"] == "C17")["resultado"] == "BLOQUEO"


# ------------------------------------------------------------------------------------------- contratos y matriz
def test_canales_v51():
    for ct in ("CT-23", "CT-24", "CT-25"):
        assert ct in CANALES
    assert canal_permitido("CT-23", "AG-01", "BROKER") and canal_permitido("CT-23", "BROKER", "AG-01")
    assert canal_permitido("CT-24", "BROKER", "AG-01") and canal_permitido("CT-25", "AG-01", "BROKER")
    assert not canal_permitido("CT-23", "AG-02", "BROKER")          # solo el Coordinador habla con el Broker (R3)
    assert not canal_permitido("CT-25", "AG-16", "BROKER")


def test_f11_reserva_de_escritura(bloque_v51):
    b, _, _ = bloque_v51
    with pytest.raises(EscrituraFueraDeReserva):
        b.almacen.escribir("F11", "AG-02", {"tipo_entrada": "ALTA", "seg_id": "SEG-2026-9999"})


# ------------------------------------------------------------------------------------------- seguimiento encargado (C6)
def test_seguimiento_alta_ciclo_y_cancelacion(bloque_v51):
    b, r, _ = bloque_v51
    opp = opciones(r)[0]["opp_id"]
    a = b.seguimientos.procesar({"accion": "ALTA", "opp_id": opp, "frecuencia": "SEMANAL", "motivo": "Vigilar sin enviar a B",
                                 "senales_interes": ["Momentum relativo"]}, AS_OF)
    assert a["estado"] == "ACTIVO" and a["seg_id"].startswith("SEG-") and a["proximo_ciclo"] == SEMANA_SIG
    f3 = b.almacen.estado("F3")[opp]
    assert f3["seg_id"] == a["seg_id"] and f3["decision_broker"]["decision"] == "EN_SEGUIMIENTO"
    assert b.seguimientos.ejecutar("2026-06-08") == []                      # todavía no vence
    res = b.seguimientos.ejecutar(SEMANA_SIG)
    assert len(res) == 1 and res[0]["ejecutado"] and res[0]["g3"] != "BLOQUEADO"
    inf = res[0]["informe"]
    assert inf["recomendacion"] in ht09.RECOMENDACIONES_SEGUIMIENTO and inf["semaforo"] in ("VERDE", "AMBAR", "ROJO")
    assert Path(res[0]["rutas"]["informe"]).name == f"{SEMANA_SIG}_informe-seguimiento_{res[0]['run_id']}.md"
    assert len(Path(res[0]["rutas"]["informe"]).read_text(encoding="utf-8").split()) <= 300
    js = json.loads(Path(res[0]["rutas"]["json"]).read_text(encoding="utf-8"))
    assert ht09.validar_seguimiento(js)["dictamen"] != "BLOQUEADO"
    import jsonschema
    esquema = json.loads((RAIZ.parent / "06_Plantillas_entregables" / "Esquema JSON - Informe de seguimiento de opción - V5.1.json")
                         .read_text(encoding="utf-8"))
    assert not [e.message for e in jsonschema.Draft202012Validator(esquema).iter_errors(js)]
    enc = b.seguimientos.encargos()[a["seg_id"]]
    assert enc["ciclos"] == 1 and enc["ultimo_run_id"] == res[0]["run_id"]
    run = [x for x in b.almacen.leer("F5") if x.get("tipo_entrada") == "RUN_C6"]
    assert run and run[-1]["tipo"] == "SEGUIMIENTO" and run[-1]["seg_id"] == a["seg_id"]
    # pausa, reanudación y cancelación inmediata (R27)
    assert b.seguimientos.procesar({"accion": "PAUSA", "seg_id": a["seg_id"]}, SEMANA_SIG)["estado"] == "PAUSADO"
    assert b.seguimientos.ejecutar("2026-06-30") == []
    assert b.seguimientos.procesar({"accion": "REANUDACION", "seg_id": a["seg_id"]}, "2026-06-30")["estado"] == "ACTIVO"
    assert b.seguimientos.procesar({"accion": "CANCELACION", "seg_id": a["seg_id"]}, "2026-06-30")["estado"] == "CANCELADO"
    assert b.seguimientos.ejecutar("2026-08-30") == []
    r2 = b.seguimientos.ejecutar("2026-08-30", a["seg_id"], forzar=True)
    assert r2 and not r2[0]["ejecutado"]
    with pytest.raises(ValueError):
        b.seguimientos.procesar({"accion": "MODIFICACION", "seg_id": a["seg_id"], "frecuencia": "DIARIA"}, "2026-08-30")
    # respuesta del Broker → aviso al Evaluador (CT-22 DECISION_SEGUIMIENTO)
    b.seguimientos.respuesta_broker(a["seg_id"], "RECHAZADA", as_of="2026-08-30")
    assert any(m["contrato"] == "CT-22" for m in b.mensajeria.registro)


def test_seguimiento_frecuencia_corta_y_opp_inexistente(bloque_v51):
    b, r, _ = bloque_v51
    a = b.seguimientos.procesar({"accion": "ALTA", "opp_id": opciones(r)[-1]["opp_id"], "frecuencia": "DIARIA"}, AS_OF)
    assert a["aviso"] and "sin novedad" in a["aviso"]                    # aviso, no veto
    with pytest.raises(KeyError):
        b.seguimientos.procesar({"accion": "ALTA", "opp_id": "OPP-2026-9999", "frecuencia": "SEMANAL"}, AS_OF)


# ------------------------------------------------------------------------------------------- consultas al Broker (CT-23)
def test_consulta_bloqueante_pausa_y_vencimiento(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    c = b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": ["CRI"],
                            "preguntas": [{"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No se incluyen",
                                           "efecto_si_falso": "Se ampliaría el cribado de CRI"}]}, AS_OF)
    assert c["estado"] == "ENVIADA" and b.consultas.clases_pausadas(AS_OF, ["CRI", "RV"]) == {"CRI": c["cns_id"]}
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "CRI"]})
    assert "CRI" not in r["paquete"]["clases"] and any(c["cns_id"] in x for x in r["paquete"]["limitaciones"])
    # al vencer el plazo, el análisis sigue con el supuesto declarado y lo hace constar (6.2.9)
    r2 = b.ciclo(SEMANA_SIG, alcance={"clases": ["RV", "CRI"]})
    assert "CRI" in r2["paquete"]["clases"]
    assert any(s["cns_id"] == c["cns_id"] for s in r2["paquete"]["supuestos_declarados"])
    assert next(x for x in ht09.validar(r2["paquete"])["comprobaciones"] if x["id"] == "C19")["resultado"] == "OK"
    tardia = b.consultas.responder(c["cns_id"], [{"indice": 0, "texto": "Sí, inclúyelas"}], as_of=SEMANA_SIG)
    assert tardia["tardia"] and "revisión" in tardia["accion"]


def test_consulta_validaciones_agrupacion_y_entrante(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    with pytest.raises(ValueError):
        b.consultas.enviar({"tipo": "OTRA", "modo": "NO_BLOQUEANTE", "preguntas": [{"texto": "¿Sin supuesto?"}]}, AS_OF)
    with pytest.raises(ValueError):
        b.consultas.enviar({"tipo": "INVENTADA", "preguntas": [{"texto": "x", "supuesto_declarado": "y"}]}, AS_OF)
    base = {"tipo": "DATO_O_DOCUMENTO", "modo": "NO_BLOQUEANTE", "run_id": "RUN-2026-0099",
            "preguntas": [{"texto": "¿Tiene el último informe del fondo?", "supuesto_declarado": "Se usa el anterior"}]}
    ids = [b.consultas.enviar(dict(base), AS_OF)["cns_id"] for _ in range(3)]
    cuarta = b.consultas.enviar(dict(base), AS_OF)
    assert len(set(ids)) == 3 and cuarta["estado"] == "AGRUPADA" and cuarta["cns_id"] == ids[-1]   # máx. 3 por RUN-
    # tres consultas iguales en 8 semanas → lección de normalización (CT-22 CONSULTA_RECURRENTE)
    assert any(x.get("tipo_aviso") == "CONSULTA_RECURRENTE" for x in b.almacen.leer("F5"))
    e = b.consultas.entrante("El usuario prefiere excluir tabaco y armas", {"run_id": None}, AS_OF)
    assert e["estado"] == "RECIBIDA"


# ------------------------------------------------------------------------------------------- credenciales (CT-25)
def test_credenciales_boveda(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    s = b.credenciales.solicitar("API de fondos cerrados", "AG-16", "Cribado FON", "Datos públicos semanales", as_of=AS_OF)
    assert s["estado"] == "SOLICITADA" and s["modo"] == "DEGRADADO_DECLARADO"
    assert b.credenciales.solicitar("API de fondos cerrados", "AG-02", "x", "y", as_of=AS_OF)["estado"] == "YA_SOLICITADA"
    # un mensaje con el valor se rechaza íntegro y no se copia
    exp = b.credenciales.responder({"crd_id": s["crd_id"], "estado": "PROVISTA", "valor": "clave-filtrada-123"}, AS_OF)
    assert exp["estado"] == "RECHAZADA_CREDENCIAL_EXPUESTA"
    # el Broker deposita en la bóveda (fuera de banda) y responde solo con estado y alias
    ok = b.credenciales.depositar(s["crd_id"], "clave-secreta-XYZ", "2027-06-05", AS_OF)
    assert ok["estado"] == "PROVISTA" and ok["credencial_ref"].startswith("boveda://ht01/")
    assert b.credenciales.solicitar("API de fondos cerrados", "AG-16", "x", "y", as_of=AS_OF)["estado"] == "PROVISTA"
    assert b.credenciales.boveda.valor_para_herramienta(ok["credencial_ref"]) == "clave-secreta-XYZ"
    # el valor no aparece en ningún archivo del bloque ni en los mensajes
    estado = Path(tmp_path) / "estado"
    for p in estado.rglob("*"):
        if p.is_file() and p.name != "secretos.json":
            texto = p.read_text(encoding="utf-8", errors="ignore")
            assert "clave-secreta-XYZ" not in texto and "clave-filtrada-123" not in texto, p
    assert "clave-secreta-XYZ" not in json.dumps(b.mensajeria.registro)
    # denegada: no se vuelve a pedir y queda la limitación de servicio en F10
    s2 = b.credenciales.solicitar("API de crédito privado", "AG-09", "Cribado ALT", "Sin descuentos de secundario", as_of=AS_OF)
    assert b.credenciales.responder({"crd_id": s2["crd_id"], "estado": "DENEGADA", "credencial_ref": None}, AS_OF)["estado"] == "DENEGADA"
    assert b.credenciales.solicitar("API de crédito privado", "AG-09", "x", "y", as_of=AS_OF)["estado"] == "DENEGADA"
    assert any(e.get("tipo_entrada") == "LIMITACION_SERVICIO" for e in b.almacen.leer("F10"))
    # recordatorio a los 7 días mientras siga degradado (máx. 3)
    s3 = b.credenciales.solicitar("API de opciones", "AG-23", "Volatilidad implícita", "Sin superficie de volatilidad", as_of=AS_OF)
    assert b.credenciales.recordatorios("2026-06-13") == [s3["crd_id"]]


# ------------------------------------------------------------------------------------------- CLI
def test_cli_v51(tmp_path):
    base = [sys.executable, "-m", "bloque_a.cli", "--datos", str(DATOS), "--estado", str(tmp_path / "e"), "--salida", str(tmp_path / "s"),
            "--as-of", AS_OF]
    env = {"PYTHONPATH": str(RAIZ), "CLAVE_PRUEBA": "valor-entorno-777", "PATH": "/usr/bin:/bin"}

    def run(*args):
        out = subprocess.run(base + list(args), capture_output=True, text=True, cwd=RAIZ, env=env, timeout=600)
        assert out.returncode == 0, out.stderr[-2000:]
        return json.loads(out.stdout)

    c = run("consulta-broker", "enviar", "--json", json.dumps({"tipo": "PREFERENCIA_O_CRITERIO", "modo": "NO_BLOQUEANTE",
                                                              "preguntas": [{"texto": "¿Horizonte preferido?", "supuesto_declarado": "H3"}]}))
    assert c["estado"] == "ENVIADA"
    assert run("consulta-broker", "responder", "--cns", c["cns_id"], "--json", json.dumps({"respuestas": [{"indice": 0, "texto": "H3"}]}))["estado"] == "RESPONDIDA"
    s = run("credencial", "solicitar", "--servicio", "API de prueba")
    d = run("credencial", "depositar", "--crd", s["crd_id"], "--valor-desde-entorno", "CLAVE_PRUEBA")
    assert d["estado"] == "PROVISTA" and "valor-entorno-777" not in json.dumps(d)
    assert run("credencial", "estado")[0]["estado"] == "PROVISTA"
    assert (tmp_path / "e" / "boveda" / "indice.json").exists()            # la bóveda vive en la carpeta de estado indicada
    assert "valor-entorno-777" not in (tmp_path / "e" / "boveda" / "indice.json").read_text(encoding="utf-8")
    assert run("seguimiento", "listar") == {}
