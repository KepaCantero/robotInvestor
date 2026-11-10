"""Ronda de regresión T-87: G3, mensajería, servicio y traspaso al Broker."""
import copy
import json
import re
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import jsonschema
import pytest
import yaml
from bloque_a.almacen import Almacen
from bloque_a.contratos import MensajeInvalido, Mensajeria
from bloque_a.encargo_b import preparar_encargo_b
from bloque_a.motor.servicio import ALTERNATIVAS, FICHAS_CATALOGO, IMPLEMENTADAS
from conftest import AS_OF, RAIZ, nuevo_bloque

from bloque_a import sintesis


def test_ct01_sobre_reservado_y_version(tmp_path):
    ms = Mensajeria(Almacen(tmp_path))
    with pytest.raises(MensajeInvalido):
        ms.crear("CT-01", "BROKER", "AG-01", {"contrato": "CT-04", "version_contrato": "0"})
    msg = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "prueba"})
    with pytest.raises(MensajeInvalido):
        ms.validar(dict(msg, version_contrato="0"))
    with pytest.raises(MensajeInvalido):
        ms.validar(dict(msg, tipo_mensaje="NO_EXISTE"))


def test_retorno_legacy_y_nuevo_no_pierden_estado_comun(tmp_path):
    ms = Mensajeria(Almacen(tmp_path))
    for cuerpo in [{"estado": "PROVISTA"}, {"estado": "COMPLETO", "estado_credencial": "PROVISTA"}]:
        m = ms.crear("CT-25", "BROKER", "AG-01", {"crd_id": "CRD-2026-0001", **cuerpo}, tipo_mensaje="RETORNO")
        assert (m["estado"], m["estado_credencial"]) == ("COMPLETO", "PROVISTA")
    with pytest.raises(MensajeInvalido):
        ms.crear("CT-25", "BROKER", "AG-01", {"crd_id": "CRD-2026-0001", "estado_credencial": "NUNCA"}, tipo_mensaje="RETORNO")


def test_peticion_idempotente_concurrente_durable_y_con_huella(tmp_path):
    ms = Mensajeria(Almacen(tmp_path))
    cuerpo = {"msg_id": "MSG-2026-000123", "tipo": "AD_HOC", "alcance": {"clases": ["DIV"]},
              "prioridad": "NORMAL", "horizontes": ["H3"]}
    m = ms.crear("CT-01", "BROKER", "AG-01", cuerpo)
    dentro, continuar = Event(), Event()
    efectos = []

    def efecto(_):
        efectos.append(1)
        dentro.set()
        assert continuar.wait(10)
        return {"run_id": "RUN-ejemplo"}

    with ThreadPoolExecutor(2) as pool:
        primero = pool.submit(ms.procesar_una_vez, m, efecto)
        assert dentro.wait(10)
        otro = pool.submit(ms.procesar_una_vez, m, efecto)
        continuar.set()
        assert [primero.result()[1], otro.result()[1]] == [False, True]
    ms = Mensajeria(Almacen(tmp_path))
    assert ms.procesar_una_vez(ms.crear("CT-01", "BROKER", "AG-01", cuerpo), efecto) == ({"run_id": "RUN-ejemplo"}, True)
    with pytest.raises(MensajeInvalido, match="contenido distinto"):
        ms.procesar_una_vez(dict(m, prioridad="BAJA"), efecto)
    assert efectos == [1]


def test_idempotencia_interrumpida_no_repite_efectos(tmp_path):
    ms = Mensajeria(Almacen(tmp_path))
    m = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "saldo"})
    with pytest.raises(RuntimeError):
        ms.procesar_una_vez(m, lambda _: (_ for _ in ()).throw(RuntimeError("efecto incompleto")))
    with pytest.raises(MensajeInvalido, match="interrumpido"):
        Mensajeria(Almacen(tmp_path)).procesar_una_vez(m, lambda _: pytest.fail("repetición incierta"))


def test_ct25_no_confunde_servicios(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    a, c = [b.credenciales.solicitar(s, "AG-16", "prueba", "prueba", as_of=AS_OF)["crd_id"] for s in ("A", "B")]
    ref = b.credenciales.depositar(c, "dato-ficticio", as_of=AS_OF)["credencial_ref"]
    assert b.credenciales.responder({"crd_id": a, "estado": "PROVISTA", "credencial_ref": ref}, AS_OF)["estado"] == "INCOHERENTE"
    assert b.credenciales._todas()[a]["estado"] == "SOLICITADA"


def test_ct04_conserva_frecuencia_y_aplica_desde_fecha_efecto(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.decision({"configuracion": {"periodicidad": "MENSUAL", "dia_hora_entrega": "LUN 10:00"}}, AS_OF)
    b.decision({"configuracion": {"dia_hora_entrega": "MAR 12:00"}}, AS_OF)
    assert b.f10(AS_OF).get("P-01") != "MENSUAL · MAR 12:00"
    assert b.f10("2026-06-06")["P-01"] == "MENSUAL · MAR 12:00"
    for cambio in [{"periodicidad": "PATATA"}, {"dia_hora_entrega": "LUN 27:04"}]:
        r = b.decision({"configuracion": cambio}, AS_OF)
        assert r["rechazos"] and not r["aplicado"]
    assert b.f10("2026-06-06")["P-01"] == "MENSUAL · MAR 12:00"


def test_catalogo_v5_despacho_y_alternativas(tmp_path, universo):
    catalogo = next((RAIZ.parent / "04_Motor_conocimiento_y_catalogo").glob("Catálogo*.md")).read_text()
    ids = set(re.findall(r"^### ([A-Z]+-[A-Z0-9]+-\d{3})\b", catalogo, re.MULTILINE))
    assert ids == set(FICHAS_CATALOGO) and len(FICHAS_CATALOGO) == len(ids)
    assert set(IMPLEMENTADAS) <= ids and set(ALTERNATIVAS.values()) <= set(IMPLEMENTADAS)
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    for ident in ids - set(IMPLEMENTADAS):
        r = b.motor.servir({"operacion": ident}, "AG-02")
        assert r["motivo"] == "METODO_NO_IMPLEMENTADO"
        assert r["alternativa"] is None or r["alternativa"] in IMPLEMENTADAS
    assert b.motor.servir({"operacion": "NO-EXISTE-001"}, "AG-02")["motivo"] == "OPERACION_SIN_FICHA"


def test_ejemplo_publicado_y_encargo_confirmado():
    schema = json.loads(next((RAIZ.parent / "06_Plantillas_entregables").glob("Esquema JSON - Paquete*.json")).read_text())
    ejemplo = json.loads(next((RAIZ / "ejemplos/salida_backtest_simulado/entregables_ultima_semana").glob("*.json")).read_text())
    jsonschema.validate(ejemplo, schema)
    # Ejemplo canónico: la India está definida en los dos bloques de esta entrega.
    paquete = json.loads(next((RAIZ.parent / "06_Plantillas_entregables").glob("Ejemplo - Paquete*.json")).read_text())
    ambitos = yaml.safe_load((RAIZ.parents[1] / "bloque_b/11_Ejecutor/config/ambitos_ejemplo.yaml").read_text())
    orden = next(o for o in paquete["paquete_para_bloque_B"] if o["tipo_activo"] == "IDX" and o["ambito"]["region"] == "India")
    d = {"run_id": paquete["run_id"], "opp_id": orden["opp_id"], "decision": "ENVIADA_A_BLOQUE_B", "clave_universo": "india",
         "ambito_a": orden["ambito"], "ambito_b": {k: ambitos["india"][k] for k in ("incluye", "excluye", "region")}}
    pet = preparar_encargo_b(paquete, d, ambitos)
    assert pet["objeto"]["clave_universo"] == pet["paquete_para_bloque_B"]["x_clave_universo"] == "india"
    assert "x_clave_universo" not in orden
    for invalida in [dict(d, decision="APLAZADA"), dict(d, run_id="otro"), dict(d, clave_universo="divisas_materias_primas"),
                     dict(d, ambito_a={}), dict(d, clave_universo="desconocido")]:
        with pytest.raises(ValueError):
            preparar_encargo_b(paquete, invalida, ambitos)


def test_r21_se_retira_la_propuesta_de_una_empresa_antes_de_entregar(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    original = sintesis.construir
    retirada = []

    def inyectar(*args, **kwargs):
        paquete, extras = original(*args, **kwargs)
        op = paquete["clases"]["RV"]["opciones"][0]
        retirada.append(op["opp_id"])
        op.update(nombre="Acciones de Microsoft Corporation", tesis="Comprar acciones de Microsoft Corporation.")
        enc = next(e for e in paquete["paquete_para_bloque_B"] if e["opp_id"] == op["opp_id"])
        enc.update(nombre=op["nombre"], tesis=op["tesis"])
        return paquete, extras

    monkeypatch.setattr(sintesis, "construir", inyectar)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r.get("entrega") != "BLOQUEADA" and retirada
    assert retirada[0] not in [e["opp_id"] for e in r["paquete"]["paquete_para_bloque_B"]]
    assert r["g3"]["intentos"] == 2


def test_r21_permite_ejemplos_e_indicadores_concretos():
    p = {"clases": {"RV": {"opciones": [{"opp_id": "OPP-2026-0001", "nombre": "Software empresarial de EE. UU.",
         "indicador_seguimiento": {"nombre": "Acciones de Microsoft Corporation"},
         "ejemplos_ilustrativos": ["Acciones de Microsoft Corporation"]}]}}, "paquete_para_bloque_B": []}
    res = {"dictamen": "APTO", "comprobaciones": [{"id": "C15", "resultado": "OK", "incidencias": []}]}
    assert sintesis._control_unitarias(p, copy.deepcopy(res)) == res
