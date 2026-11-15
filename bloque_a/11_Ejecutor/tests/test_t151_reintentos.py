"""T-151 · los reintentos ante un fallo del proveedor pasan por la reserva del presupuesto (QA r01 de T-146, H-09).

Antes, el SDK reintentaba solo (`max_retries` = `llm.max_reintentos_api`) y ningún reintento pasaba por `ReservaLlamada`: un
*timeout* que el servidor completó podía cobrarse sin reserva. Ahora el SDK sale con `max_retries=0` y reintenta el cliente
(`llm.ReglaReintentos`, de la configuración): cada reintento reserva su petición; la que el servidor rechazó sin ejecutar
(429, 529) suelta su reserva y la que pudo cobrarse (conexión, *timeout*, otro 5xx) se carga en la bolsa por su peor caso y
queda en `peticiones_sin_respuesta` del RUN en F5.

Sin red: el SDK real sobre un transporte falso (`httpx2.MockTransport`) o SDK falsos. Ningún identificador de modelo."""
from __future__ import annotations

import json
import types

import anthropic
import httpx2
import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, fusionar, parametro
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import (
    AnthropicClient,
    ReglaReintentos,
    clasificar_error,
    con_guarda,
    crear_cliente,
)
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas

from bloque_a import mock_respuestas

MODELO = "modelo-de-prueba"
SISTEMA = [{"type": "text", "text": "s" * 3600}]
MENSAJES = [{"role": "user", "content": "hola"}]


def _cfg(**extra):
    return config_pruebas(**fusionar({"modo": "vivo", "perfiles": {"activos": ["DIV"]}}, extra))


def _mensaje(texto="ok", entrada=100, salida=50):
    return {"id": "msg_prueba", "type": "message", "role": "assistant", "model": MODELO,
            "content": [{"type": "text", "text": texto}], "stop_reason": "end_turn", "stop_sequence": None,
            "usage": {"input_tokens": entrada, "output_tokens": salida}}


class Servidor:
    """Transporte falso: cada petición HTTP toma la siguiente respuesta de `guion` (un estado HTTP, una excepción de httpx2
    o 200 con un mensaje); la última se repite."""

    def __init__(self, *guion, cabeceras=None):
        self.guion, self.cabeceras, self.peticiones = list(guion), cabeceras or {}, 0

    def __call__(self, req):
        self.peticiones += 1
        paso = self.guion[min(self.peticiones, len(self.guion)) - 1]
        if isinstance(paso, Exception):
            raise paso
        if paso == 200:
            return httpx2.Response(200, json=_mensaje())
        return httpx2.Response(paso, headers=self.cabeceras.get(paso, {}),
                               json={"type": "error", "error": {"type": "api_error", "message": "fallo de prueba"}})


def _sdk(servidor, max_retries=5):
    """El SDK real, con sus propios reintentos activados a propósito: el cliente los pone a 0."""
    return anthropic.Anthropic(api_key="clave-falsa-de-prueba", max_retries=max_retries,
                               http_client=httpx2.Client(transport=httpx2.MockTransport(servidor)))


def _cliente(servidor, cfg=None, esperas=None):
    esperas = [] if esperas is None else esperas
    return AnthropicClient(sdk=_sdk(servidor), reintentos=ReglaReintentos.de_config(cfg or _cfg()), dormir=esperas.append), esperas


def _guarda(asignado, cfg=None):
    cfg = cfg or _cfg()
    p = Presupuesto({"DIV": asignado}, cfg)
    return p, ReservaLlamada(p, "DIV", Contabilidad(cfg), "AG-05")


def _generar(cli, g):
    mt = g.reservar(SISTEMA, MENSAJES, None, 1000)
    with con_guarda(g):
        r = cli.generar(agente="AG-05", modelo=MODELO, system=SISTEMA, mensajes=MENSAJES, max_tokens=mt)
    g.pagar_resto(r.uso)
    return r


def _timeout():
    return httpx2.ReadTimeout("timeout de prueba")


# ---------------------------------------------------------------- la regla, de la configuración
def test_la_regla_sale_de_la_configuracion_y_el_sdk_no_reintenta(monkeypatch):
    cfg = _cfg()
    regla = ReglaReintentos.de_config(cfg)
    assert regla.maximo == parametro(cfg, "llm.max_reintentos_api")
    assert regla.espera_inicial_s == parametro(cfg, "llm.reintentos.espera_inicial_s")
    assert regla.espera_max_s == parametro(cfg, "llm.reintentos.espera_max_s")
    assert regla.estados == frozenset(parametro(cfg, "llm.reintentos.estados_reintentables"))
    assert regla.sin_cobro == frozenset(parametro(cfg, "llm.reintentos.estados_sin_cobro")) and regla.sin_cobro <= regla.estados
    creados = []
    monkeypatch.setattr(anthropic, "Anthropic", lambda **kw: creados.append(kw) or types.SimpleNamespace(messages=None))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "clave-falsa-de-prueba")
    cli = crear_cliente("anthropic", cfg)
    assert creados and creados[0]["max_retries"] == 0 and cli.reintentos == regla


@pytest.mark.parametrize("clave, valor, error", [
    ("espera_inicial_s", -0.5, ValueError), ("espera_max_s", float("nan"), ValueError), ("espera_inicial_s", "0.5", ValueError),
    ("espera_inicial_s", 9, ValueError), ("estados_reintentables", [429, "500"], ValueError),
    ("estados_sin_cobro", [418], ValueError), ("estados_sin_cobro", 429, ValueError), ("espera_max_s", None, KeyError)])
def test_una_regla_invalida_falla_cerrado(clave, valor, error):
    cfg = _cfg()
    cfg["llm"]["reintentos"][clave] = valor
    with pytest.raises(error):
        ReglaReintentos.de_config(cfg)


@pytest.mark.parametrize("valor", [-1, True, 1.5])
def test_un_maximo_invalido_falla_cerrado(valor):
    cfg = _cfg()
    cfg["llm"]["max_reintentos_api"] = valor
    with pytest.raises(ValueError, match="max_reintentos_api"):
        ReglaReintentos.de_config(cfg)


def test_la_espera_dobla_hasta_la_maxima_o_es_la_del_servidor():
    regla = ReglaReintentos.de_config(_cfg())
    sin = types.SimpleNamespace()
    esperas = [regla.espera(n, sin) for n in range(1, 7)]
    assert esperas[0] == regla.espera_inicial_s and esperas[1] == 2 * regla.espera_inicial_s
    assert max(esperas) == regla.espera_max_s and esperas == sorted(esperas)
    con = types.SimpleNamespace(response=types.SimpleNamespace(headers={"retry-after": "3"}))
    assert regla.espera(1, con) == 3.0
    ms = types.SimpleNamespace(response=types.SimpleNamespace(headers={"retry-after-ms": "250", "retry-after": "3"}))
    assert regla.espera(1, ms) == 0.25
    fecha = types.SimpleNamespace(response=types.SimpleNamespace(headers={"retry-after": "Wed, 21 Oct 2026 07:28:00 GMT"}))
    assert regla.espera(2, fecha) == 2 * regla.espera_inicial_s   # una fecha no se interpreta: la de la regla


def test_la_clasificacion_de_los_errores():
    regla = ReglaReintentos.de_config(_cfg())
    req = httpx2.Request("POST", "https://api.invalid/v1/messages")

    def estado(n, cab=None):
        return anthropic.APIStatusError("x", response=httpx2.Response(n, request=req, headers=cab or {}), body=None)
    assert clasificar_error(anthropic.APITimeoutError(request=req), regla) == (True, True)
    assert clasificar_error(anthropic.APIConnectionError(request=req), regla) == (True, True)
    assert clasificar_error(estado(529), regla) == (True, False) and clasificar_error(estado(429), regla) == (True, False)
    assert clasificar_error(estado(500), regla) == (True, True)
    assert clasificar_error(estado(400), regla) == (False, False)
    assert clasificar_error(estado(500, {"x-should-retry": "false"}), regla) == (False, False)
    assert clasificar_error(estado(400, {"x-should-retry": "true"}), regla) == (True, True)
    assert clasificar_error(RuntimeError("no es del proveedor"), regla) == (False, False)
    # sin regla: no se reintenta, y lo del proveedor cuenta como cobrado (prudente)
    assert clasificar_error(anthropic.APITimeoutError(request=req), None) == (False, True)
    assert clasificar_error(estado(529), None) == (False, True)


# ---------------------------------------------------------------- con el SDK real sobre un transporte falso
def test_un_529_se_reintenta_con_su_reserva_y_suelta_la_que_fallo():
    srv = Servidor(529, 529, 200)
    cli, esperas = _cliente(srv)
    p, g = _guarda(100.0)
    r = _generar(cli, g)
    regla = cli.reintentos
    assert r.stop_reason == "end_turn" and srv.peticiones == 3          # el SDK no reintentó por su cuenta (max_retries=5)
    assert esperas == [regla.espera_inicial_s, 2 * regla.espera_inicial_s]
    assert g.peticiones == 3 and not p.sin_respuesta                    # cada intento reservó; los 529 no se cobran
    assert p.reservado["DIV"] == pytest.approx(g.apartado)              # solo lo real de la que respondió
    g.cerrar()
    assert p.reservado["DIV"] == 0 and p.consumido["DIV"] == 0          # lo real lo carga después `Bloque._cargar`


def test_un_timeout_se_carga_por_su_peor_caso_y_queda_declarado():
    srv = Servidor(_timeout(), 200)
    cli, _ = _cliente(srv)
    p, g = _guarda(100.0)
    r = _generar(cli, g)
    assert r.stop_reason == "end_turn" and srv.peticiones == 2 and g.peticiones == 2
    assert len(p.sin_respuesta) == 1 and p.sin_respuesta[0]["motivo"] == "APITimeoutError"
    peor = p.sin_respuesta[0]["reservado_uc"]
    assert peor > 0 and g.sin_respuesta == pytest.approx(peor, abs=1e-4)
    g.cerrar()
    assert p.reservado["DIV"] == 0 and p.consumido["DIV"] == pytest.approx(peor, abs=1e-4)


def test_agotados_los_reintentos_error_proveedor_y_cada_intento_cargado():
    srv = Servidor(500)
    cfg = _cfg()
    cli, esperas = _cliente(srv, cfg)
    p, g = _guarda(100.0, cfg)
    r = _generar(cli, g)
    n = parametro(cfg, "llm.max_reintentos_api") + 1
    assert r.stop_reason == "error_proveedor" and r.texto == "" and srv.peticiones == n == g.peticiones
    assert len(esperas) == n - 1 and len(p.sin_respuesta) == n          # un 500 pudo ejecutarse: se carga cada intento
    g.cerrar()
    assert p.reservado["DIV"] == 0 and p.consumido["DIV"] == pytest.approx(g.peor_total, abs=1e-3)


def test_un_error_no_reintentable_no_se_reintenta_y_suelta_su_reserva():
    srv = Servidor(400)
    cli, esperas = _cliente(srv)
    p, g = _guarda(100.0)
    r = _generar(cli, g)
    assert r.stop_reason == "error_proveedor" and srv.peticiones == 1 and not esperas and not p.sin_respuesta
    assert p.reservado["DIV"] == 0
    g.cerrar()
    assert p.consumido["DIV"] == 0


def test_el_reintento_que_no_cabe_no_sale():
    """Tras un timeout (cargado por su peor caso), el reintento reserva el suyo: si no cabe, no sale."""
    srv = Servidor(_timeout(), 200)
    cli, _ = _cliente(srv)
    p, g = _guarda(1.0)
    mt = g.reservar(SISTEMA, MENSAJES, None, 4000)
    assert mt is not None and p.disponible("DIV") < g.peor_total       # no caben dos peticiones así
    with con_guarda(g):
        r = cli.generar(agente="AG-05", modelo=MODELO, system=SISTEMA, mensajes=MENSAJES, max_tokens=mt)
    g.pagar_resto(r.uso)
    assert r.stop_reason == "presupuesto_agotado" and srv.peticiones == 1 and g.negada
    g.cerrar()
    assert p.consumido["DIV"] <= p.limite("DIV") + 1e-9 and p.reservado["DIV"] == 0


def test_la_continuacion_tambien_reintenta_con_su_reserva():
    """Un 529 en la continuación de `pause_turn`: se reintenta dentro de la reserva de la continuación."""
    pausa = dict(_mensaje(), stop_reason="pause_turn")
    pasos = [httpx2.Response(200, json=pausa), httpx2.Response(529, json={"type": "error", "error": {"type": "overloaded_error",
                                                                                                    "message": "x"}}),
             httpx2.Response(200, json=_mensaje())]

    def servidor(req):
        return pasos.pop(0)
    cli = AnthropicClient(sdk=_sdk(servidor), reintentos=ReglaReintentos.de_config(_cfg()), dormir=lambda s: None,
                          max_continuaciones=3)
    p, g = _guarda(100.0)
    r = _generar(cli, g)
    assert r.stop_reason == "end_turn" and not pasos and g.peticiones == 3 and not p.sin_respuesta
    g.cerrar()


def test_sin_regla_no_reintenta():
    srv = Servidor(529, 200)
    cli = AnthropicClient(sdk=_sdk(srv))
    p, g = _guarda(100.0)
    r = _generar(cli, g)
    assert r.stop_reason == "error_proveedor" and srv.peticiones == 1
    assert len(p.sin_respuesta) == 1                                     # sin regla, prudente: pudo cobrarse
    g.cerrar()


def test_lo_sin_respuesta_de_c5_pasa_a_la_bolsa_del_ciclo():
    """`Presupuesto.absorber` (lo de AG-20, que corre antes del reparto) también pasa las peticiones sin respuesta."""
    cfg = _cfg()
    c5 = Presupuesto({"COMUN": 10.0}, cfg)
    g = ReservaLlamada(c5, "COMUN", Contabilidad(cfg), "AG-20")
    g.reservar(SISTEMA, MENSAJES, None, 1000)
    g.fallida(True, "APITimeoutError")
    g.cerrar()
    ciclo = Presupuesto({"COMUN": 10.0, "DIV": 18.0}, cfg)
    ciclo.absorber(c5)
    assert ciclo.sin_respuesta == c5.sin_respuesta and len(ciclo.sin_respuesta) == 1
    assert ciclo.consumido["COMUN"] == pytest.approx(c5.sin_respuesta[0]["reservado_uc"], abs=1e-4)


# ---------------------------------------------------------------- en el ciclo: F5
class SDKConUnTimeout:
    """Responde como el simulado; la primera petición del Analista de divisas (AG-05) no responde (timeout)."""

    def __init__(self, semilla):
        self.semilla, self.messages, self.fallos, self.n = semilla, self, 0, 0
        self.req = httpx2.Request("POST", "https://api.invalid/v1/messages")

    def create(self, **kw):
        self.n += 1
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        if agente == "AG-05" and not self.fallos:
            self.fallos += 1
            raise anthropic.APITimeoutError(request=self.req)
        texto = json.dumps(mock_respuestas.responder(agente, kw["messages"][:1], self.semilla), ensure_ascii=False)
        uso = types.SimpleNamespace(input_tokens=2000, output_tokens=500, cache_creation_input_tokens=0, cache_read_input_tokens=0,
                                    server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


def test_en_el_ciclo_la_peticion_sin_respuesta_queda_en_f5_y_en_su_bolsa(tmp_path):
    cfg = _cfg(llm={"cache_resultados": False})
    sdk = SDKConUnTimeout(int(cfg["llm"]["semilla_mock"]))
    cli = AnthropicClient(sdk=sdk, reintentos=ReglaReintentos.de_config(cfg), dormir=lambda s: None)
    b = Bloque(cfg, ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli, tmp_path / "estado", tmp_path / "ent")
    r = b.ciclo(AS_OF, nivel_forzado="N2")
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    assert sdk.fallos == 1
    sin = run["peticiones_sin_respuesta"]
    assert len(sin) == 1 and sin[0]["clase"] == "DIV" and sin[0]["agente"] == "AG-05" and sin[0]["motivo"] == "APITimeoutError"
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"])
    total = sum(v["consumido"] for v in r["presupuesto"].values())   # con la auditoría, que corre después de F5
    assert total == pytest.approx(gastado + sin[0]["reservado_uc"], abs=0.01)   # lo que pudo cobrarse, en su bolsa
    assert run["presupuesto"]["DIV"]["consumido"] == pytest.approx(r["presupuesto"]["DIV"]["consumido"])
    pu = cfg["presupuesto_uc"]
    for v in r["presupuesto"].values():
        assert v["consumido"] <= v["asignado"] * (1 + pu["ampliacion_sin_autorizacion"]) + v["ampliado"] + 1e-6
