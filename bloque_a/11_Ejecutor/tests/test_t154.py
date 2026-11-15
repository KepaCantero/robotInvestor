"""T-154 · hallazgos bajos de la QA r01 de T-151 (`.docs/tickets/T-151/qa.md`).

- H-01: un 5xx que no está en `estados_reintentables` (501, 505, 520) o un 500 con `x-should-retry: false` no se reintenta,
  pero el servidor pudo ejecutarlo: se carga por su peor caso, como dicen el README e INC-T146-01 («5xx salvo 529»).
- H-02: lo que la auditoría (AG-19) deja en el presupuesto después de escribir el RUN en F5 queda en una entrada
  `PRESUPUESTO_F9` de F5.
- H-03: si una llamada de un grupo de prefijos tuvo una petición sin respuesta que pudo cobrarse, el reparto de las primas
  de caché no depende de qué hilo llegó antes (cada bolsa paga su prima «solo»).
- H-04: un `retry-after` no finito, negativo o cero no vale como espera; uno mayor que `espera_servidor_max_s` no se
  reintenta; `x-should-retry` no distingue mayúsculas (ni en el nombre ni en el valor).

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
    Uso,
    clasificar_error,
    con_guarda,
)
from bloque_a.orquestacion import Bloque, grupo_primas
from conftest import AS_OF, DATOS, config_pruebas

from bloque_a import mock_respuestas

MODELO = "modelo-de-prueba"
SISTEMA = [{"type": "text", "text": "s" * 3600}]
MENSAJES = [{"role": "user", "content": "hola"}]
REQ = httpx2.Request("POST", "https://api.invalid/v1/messages")


def _cfg(**extra):
    return config_pruebas(**fusionar({"modo": "vivo", "perfiles": {"activos": ["DIV"]}}, extra))


def _mensaje():
    return {"id": "msg_prueba", "type": "message", "role": "assistant", "model": MODELO,
            "content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "stop_sequence": None,
            "usage": {"input_tokens": 100, "output_tokens": 50}}


class Servidor:
    """Transporte falso: cada petición HTTP toma el siguiente paso del guion (estado HTTP, con sus cabeceras); la última se
    repite. 200 responde con un mensaje."""

    def __init__(self, *guion, cabeceras=None):
        self.guion, self.cabeceras, self.peticiones = list(guion), cabeceras or {}, 0

    def __call__(self, req):
        self.peticiones += 1
        paso = self.guion[min(self.peticiones, len(self.guion)) - 1]
        if paso == 200:
            return httpx2.Response(200, json=_mensaje())
        return httpx2.Response(paso, headers=self.cabeceras,
                               json={"type": "error", "error": {"type": "api_error", "message": "fallo de prueba"}})


def _cliente(servidor, cfg=None):
    esperas: list[float] = []
    sdk = anthropic.Anthropic(api_key="clave-falsa-de-prueba", max_retries=5,
                              http_client=httpx2.Client(transport=httpx2.MockTransport(servidor)))
    return AnthropicClient(sdk=sdk, reintentos=ReglaReintentos.de_config(cfg or _cfg()), dormir=esperas.append), esperas


def _guarda(asignado=100.0, cfg=None):
    cfg = cfg or _cfg()
    p = Presupuesto({"DIV": asignado}, cfg)
    return p, ReservaLlamada(p, "DIV", Contabilidad(cfg), "AG-05")


def _generar(cli, g):
    mt = g.reservar(SISTEMA, MENSAJES, None, 1000)
    with con_guarda(g):
        r = cli.generar(agente="AG-05", modelo=MODELO, system=SISTEMA, mensajes=MENSAJES, max_tokens=mt)
    g.pagar_resto(r.uso)
    return r


def _estado(n, cabeceras=None):
    return anthropic.APIStatusError("x", response=httpx2.Response(n, request=REQ, headers=cabeceras or {}), body=None)


def _con(cabeceras):
    """Un error con una respuesta cuyas cabeceras son un diccionario simple (distingue mayúsculas en el nombre)."""
    return types.SimpleNamespace(response=types.SimpleNamespace(headers=cabeceras))


# ---------------------------------------------------------------- H-01: el cobro de los 5xx
@pytest.mark.parametrize("estado, cabeceras", [(501, {}), (505, {}), (520, {}), (500, {"x-should-retry": "false"}),
                                               (503, {"x-should-retry": "false"})])
def test_t154_h01_un_5xx_que_no_se_reintenta_se_carga_por_su_peor_caso(estado, cabeceras):
    srv = Servidor(estado, 200, cabeceras=cabeceras)
    cli, esperas = _cliente(srv)
    p, g = _guarda()
    r = _generar(cli, g)
    assert r.stop_reason == "error_proveedor" and srv.peticiones == 1 and not esperas    # no se reintenta
    assert len(p.sin_respuesta) == 1 and p.sin_respuesta[0]["reservado_uc"] > 0              # pero pudo cobrarse
    peor = p.sin_respuesta[0]["reservado_uc"]
    g.cerrar()
    assert p.reservado["DIV"] == 0 and p.consumido["DIV"] == pytest.approx(peor, abs=1e-4)


@pytest.mark.parametrize("estado, cabeceras", [(529, {}), (529, {"x-should-retry": "false"}), (429, {"x-should-retry": "false"}),
                                               (400, {}), (404, {"x-should-retry": "false"})])
def test_t154_h01_lo_que_el_servidor_rechaza_sin_ejecutar_sigue_sin_cargarse(estado, cabeceras):
    srv = Servidor(estado, cabeceras=cabeceras)
    cli, _ = _cliente(srv)
    p, g = _guarda()
    _generar(cli, g)
    assert not p.sin_respuesta and p.reservado["DIV"] == 0
    g.cerrar()
    assert p.consumido["DIV"] == 0


def test_t154_h01_la_clasificacion_de_los_5xx_sale_de_la_configuracion():
    cfg = _cfg()
    regla = ReglaReintentos.de_config(cfg)
    desde = parametro(cfg, "llm.reintentos.cobro_posible_desde")
    assert regla.cobro_posible == desde
    assert clasificar_error(_estado(desde + 1), regla) == (False, True)       # 501: no se reintenta, pudo cobrarse
    assert clasificar_error(_estado(desde - 1), regla) == (False, False)      # 499: lo rechazó, no se cobró
    assert clasificar_error(_estado(desde), regla) == (True, True)            # 500: se reintenta y pudo cobrarse
    cfg["llm"]["reintentos"]["cobro_posible_desde"] = 600                     # otro valor de la configuración, otra regla
    otra = ReglaReintentos.de_config(cfg)
    assert clasificar_error(_estado(501), otra) == (False, False)


# ---------------------------------------------------------------- H-04: la espera del servidor y las mayúsculas
@pytest.mark.parametrize("clave", ["retry-after", "retry-after-ms"])
@pytest.mark.parametrize("valor", ["inf", "+inf", "-inf", "nan", "1e400", "-5", "0", "", "  "])
def test_t154_h04_un_retry_after_no_finito_negativo_o_cero_no_vale(clave, valor):
    regla = ReglaReintentos.de_config(_cfg())
    assert regla.espera(1, _con({clave: valor})) == regla.espera_inicial_s
    assert regla.espera(3, _con({clave: valor})) == min(4 * regla.espera_inicial_s, regla.espera_max_s)


def test_t154_h04_el_tope_de_la_espera_del_servidor():
    cfg = _cfg()
    regla = ReglaReintentos.de_config(cfg)
    tope = parametro(cfg, "llm.reintentos.espera_servidor_max_s")
    assert regla.espera_servidor_max_s == tope
    assert regla.espera(1, _con({"retry-after": str(tope)})) == tope                       # el tope exacto vale
    assert regla.espera(1, _con({"retry-after": str(tope + 1)})) is None                   # más: no se reintenta
    assert regla.espera(1, _con({"retry-after-ms": str((tope + 1) * 1000)})) is None
    assert regla.espera(1, _con({"retry-after-ms": str(tope * 1000)})) == tope


def test_t154_h04_si_el_servidor_pide_esperar_de_mas_no_se_reintenta():
    tope = parametro(_cfg(), "llm.reintentos.espera_servidor_max_s")
    srv = Servidor(429, 200, cabeceras={"retry-after": str(10 * tope)})
    cli, esperas = _cliente(srv)
    p, g = _guarda()
    r = _generar(cli, g)
    assert r.stop_reason == "error_proveedor" and srv.peticiones == 1 and not esperas
    assert not p.sin_respuesta and p.reservado["DIV"] == 0                                # un 429 no se cobró
    g.cerrar()
    srv = Servidor(429, 200, cabeceras={"retry-after": "2"})                             # lo que admite: espera y reintenta
    cli, esperas = _cliente(srv)
    p, g = _guarda()
    assert _generar(cli, g).stop_reason == "end_turn" and esperas == [2.0] and srv.peticiones == 2
    g.cerrar()


@pytest.mark.parametrize("nombre", ["x-should-retry", "X-Should-Retry", "X-SHOULD-RETRY"])
@pytest.mark.parametrize("valor, reintenta", [("true", True), ("True", True), (" TRUE ", True), ("false", False),
                                              ("False", False), (" FALSE ", False)])
def test_t154_h04_x_should_retry_no_distingue_mayusculas(nombre, valor, reintenta):
    regla = ReglaReintentos.de_config(_cfg())
    # con las cabeceras de httpx (el nombre ya no distingue mayúsculas) y con un diccionario simple
    assert clasificar_error(_estado(400, {nombre: valor}), regla)[0] is reintenta
    error = _estado(400)
    error.response = types.SimpleNamespace(headers={nombre: valor})   # type: ignore[assignment]
    assert clasificar_error(error, regla)[0] is reintenta
    assert clasificar_error(_estado(503, {nombre: valor}), regla) == (reintenta, True)   # un 5xx pudo cobrarse siempre


def test_t154_h04_retry_after_con_el_nombre_en_mayusculas():
    regla = ReglaReintentos.de_config(_cfg())
    assert regla.espera(1, _con({"Retry-After": "3"})) == 3.0
    assert regla.espera(1, _con({"RETRY-AFTER-MS": "250", "Retry-After": "3"})) == 0.25
    assert regla.espera(1, _con(None)) == regla.espera_inicial_s and regla.espera(1, _con("no-es-un-diccionario")) == regla.espera_inicial_s


@pytest.mark.parametrize("clave, valor, error", [
    ("espera_servidor_max_s", -1, ValueError), ("espera_servidor_max_s", float("inf"), ValueError),
    ("espera_servidor_max_s", "600", ValueError), ("espera_servidor_max_s", True, ValueError),
    ("espera_servidor_max_s", None, KeyError), ("cobro_posible_desde", True, ValueError),
    ("cobro_posible_desde", "500", ValueError), ("cobro_posible_desde", -1, ValueError), ("cobro_posible_desde", 500.0, ValueError),
    ("cobro_posible_desde", None, KeyError)])
def test_t154_las_claves_nuevas_invalidas_fallan_cerrado(clave, valor, error):
    cfg = _cfg()
    cfg["llm"]["reintentos"][clave] = valor   # nula = ausente (`parametro`: sin respaldo, falla cerrado)
    with pytest.raises(error):
        ReglaReintentos.de_config(cfg)


# ---------------------------------------------------------------- H-03: el reparto de las primas con un fallo
def _r(escrito, leido):
    return types.SimpleNamespace(uso=Uso(entrada=500, salida=100, cache_escritura=escrito, cache_lectura=leido), cache_hit=False,
                                 intentos=1, uc=0.0)


def _reparto(orden, marcar=True):
    """Tres bolsas llaman a un agente compartido (AG-14, prefijo de 20 000 tokens). La primera petición de DIV no responde y
    se reintenta. Orden «fallo_primero»: esa petición escribió el prefijo (nadie lo ve) y todas leen; orden «otro_primero»:
    MP lo escribe y lo ve, y la de DIV lee. El reintento de DIV lee en los dos."""
    cfg = _cfg()
    fake = types.SimpleNamespace(contabilidad=Contabilidad(cfg), v6=False)
    p = Presupuesto({"DIV": 50.0, "MP": 50.0, "RV": 50.0, "COMUN": 50.0}, cfg)
    if marcar:
        p.grupo_sin_respuesta(grupo_primas(False, "AG-14"))
    llamadas = {"fallo_primero": [("DIV", _r(0, 20000)), ("MP", _r(0, 20000)), ("RV", _r(0, 20000))],
                "otro_primero": [("MP", _r(20000, 0)), ("DIV", _r(0, 20000)), ("RV", _r(0, 20000))]}[orden]
    for bolsa, r in llamadas:
        Bloque._cargar(fake, p, bolsa, "AG-14", r, prefijo=20000)
    p.liquidar_primas()
    return {k: round(v, 6) for k, v in p.consumido.items()}, p


def test_t154_h03_con_un_fallo_el_reparto_no_depende_del_orden():
    a, pa = _reparto("fallo_primero")
    b, _ = _reparto("otro_primero")
    assert a == b
    prima = pa._uc_prima(20000)
    lectura = Contabilidad(_cfg()).uc_de(Uso(entrada=500, salida=100, cache_lectura=20000))
    for bolsa in ("DIV", "MP", "RV"):   # cada bolsa: lo leído más su prima «solo» entera (la cota, ya retenida)
        assert a[bolsa] == pytest.approx(lectura + prima, abs=1e-6)
    assert not pa.retenido and not pa._grupos_sin_respuesta   # la liquidación lo suelta todo
    # sin la marca (antes de T-154), el escenario sí depende del orden: es el de la QA
    assert _reparto("fallo_primero", marcar=False)[0] != _reparto("otro_primero", marcar=False)[0]


def test_t154_h03_un_grupo_sin_fallos_reparte_como_antes():
    cfg = _cfg()
    fake = types.SimpleNamespace(contabilidad=Contabilidad(cfg), v6=False)
    p = Presupuesto({"DIV": 50.0, "MP": 50.0}, cfg)
    p.grupo_sin_respuesta("AG-99")   # otro grupo: no cambia el de AG-14
    Bloque._cargar(fake, p, "MP", "AG-14", _r(20000, 0), prefijo=20000)
    Bloque._cargar(fake, p, "DIV", "AG-14", _r(0, 20000), prefijo=20000)
    p.liquidar_primas()
    prima = p._uc_prima(20000)
    lectura = Contabilidad(cfg).uc_de(Uso(entrada=500, salida=100, cache_lectura=20000))
    assert p.consumido["DIV"] == pytest.approx(lectura + prima / 2, abs=1e-6) == pytest.approx(p.consumido["MP"], abs=1e-6)


def test_t154_h03_el_grupo_de_un_analista_en_v6():
    assert grupo_primas(True, "AG-05") == "ANALISTAS" and grupo_primas(False, "AG-05") == "AG-05"
    assert grupo_primas(True, "AG-14") == "AG-14"


# ---------------------------------------------------------------- en el ciclo
class SDKSimulado:
    """Responde como el simulado; la primera petición de `agente_que_falla` no responde (timeout). Con `cache`, simula la
    caché por prefijo (la primera petición con un `system` lo escribe, también la que no responde; las demás lo leen)."""

    def __init__(self, semilla, agente_que_falla, cache=False):
        self.semilla, self.messages, self.agente, self.cache = semilla, self, agente_que_falla, cache
        self.fallos, self.vistos = 0, set()

    def create(self, **kw):
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        pref = json.dumps(kw["system"], sort_keys=True)
        escrito = leido = 0
        if self.cache:
            escrito, leido = (0, 1500) if pref in self.vistos else (1500, 0)
            self.vistos.add(pref)
        if agente == self.agente and not self.fallos:
            self.fallos += 1
            raise anthropic.APITimeoutError(request=REQ)
        texto = json.dumps(mock_respuestas.responder(agente, kw["messages"][:1], self.semilla), ensure_ascii=False)
        uso = types.SimpleNamespace(input_tokens=2000, output_tokens=500, cache_creation_input_tokens=escrito,
                                    cache_read_input_tokens=leido, server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


def _ciclo(tmp_path, agente_que_falla, cache=False, monkeypatch=None):
    cfg = _cfg(llm={"cache_resultados": False})
    sdk = SDKSimulado(int(cfg["llm"]["semilla_mock"]), agente_que_falla, cache)
    cli = AnthropicClient(sdk=sdk, reintentos=ReglaReintentos.de_config(cfg), dormir=lambda s: None)
    b = Bloque(cfg, ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli, tmp_path / "estado", tmp_path / "ent")
    r = b.ciclo(AS_OF, nivel_forzado="N2")
    return b, r, sdk


def test_t154_h02_la_peticion_sin_respuesta_de_ag19_queda_en_f5(tmp_path):
    b, r, sdk = _ciclo(tmp_path, "AG-19")
    assert sdk.fallos == 1
    f5 = b.almacen.leer("F5")
    run = next(e for e in f5 if e.get("tipo_entrada") == "RUN" and e["id"] == r["run_id"])
    assert not any(s["agente"] == "AG-19" for s in run.get("peticiones_sin_respuesta", []))   # el RUN no cambia
    f9 = [e for e in f5 if e.get("tipo_entrada") == "PRESUPUESTO_F9"]
    assert len(f9) == 1 and f9[0]["run_id"] == r["run_id"] and f9[0]["fase"] == "F9" and f9[0]["id"] != r["run_id"]
    sin = f9[0]["peticiones_sin_respuesta"]
    assert [(s["clase"], s["agente"], s["motivo"]) for s in sin] == [("COMUN", "AG-19", "APITimeoutError")]
    assert f9[0]["presupuesto"] == r["presupuesto"]          # el resumen tras la auditoría, el del resultado
    assert f9[0]["cierres_parciales"] == []                  # solo lo nuevo de la auditoría
    assert b.almacen.estado("F5", clave="id")[r["run_id"]]["tipo_entrada"] == "RUN"
    # lo consumido de F5 (RUN y su entrada F9) = la contabilidad + lo cargado sin respuesta
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"])
    cargado = sum(s["reservado_uc"] for s in run.get("peticiones_sin_respuesta", []) + sin)
    assert sum(v["consumido"] for v in f9[0]["presupuesto"].values()) == pytest.approx(gastado + cargado, abs=0.01)


def test_t154_h02_sin_nada_de_ag19_que_declarar_no_hay_entrada(tmp_path):
    b, r, sdk = _ciclo(tmp_path, "AG-05")                     # el fallo es de otro agente, antes del RUN
    f5 = b.almacen.leer("F5")
    assert sdk.fallos == 1 and not [e for e in f5 if e.get("tipo_entrada") == "PRESUPUESTO_F9"]
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    assert [s["agente"] for s in run["peticiones_sin_respuesta"]] == ["AG-05"]


def test_t154_h02_los_cierres_y_excesos_tras_el_run_tambien(tmp_path):
    b, r, _ = _ciclo(tmp_path, "ninguno")
    assert not [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "PRESUPUESTO_F9"]
    p = Presupuesto({"COMUN": 5.0}, b.cfg)
    p.cierre_parcial("COMUN", "anterior", "de antes de la marca")
    marca = p.marca()
    p.cierre_parcial("COMUN", "CT-17", "presupuesto insuficiente para AG-19")
    p.anotar("excesos", {"clase": "COMUN", "agente": "AG-19", "reservado_uc": 1.0, "real_uc": 1.5, "busquedas_web": 0})
    p.anotar("recortes", {"clase": "COMUN", "agente": "AG-19", "peticion": 1, "max_tokens": 9, "max_tokens_enviado": 8,
                          "peor_caso_uc": 1.0, "reservado_uc": 0.9})
    b._registrar_f9(r["run_id"], p, marca)
    f9 = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "PRESUPUESTO_F9"]
    assert len(f9) == 1
    assert [c["motivo"] for c in f9[0]["cierres_parciales"]] == ["presupuesto insuficiente para AG-19"]
    assert len(f9[0]["excesos_reserva"]) == 1 and len(f9[0]["recortes_salida"]) == 1 and "peticiones_sin_respuesta" not in f9[0]
    b._registrar_f9(r["run_id"], p, p.marca())                # nada nuevo desde la marca: nada que escribir
    assert len([e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "PRESUPUESTO_F9"]) == 1


def test_t154_h03_en_el_ciclo_la_peticion_sin_respuesta_marca_su_grupo(tmp_path, monkeypatch):
    marcados: list[str] = []
    orig = Presupuesto.grupo_sin_respuesta
    monkeypatch.setattr(Presupuesto, "grupo_sin_respuesta", lambda self, g: (marcados.append(g), orig(self, g))[1])
    b, r, sdk = _ciclo(tmp_path, "AG-05", cache=True)
    assert sdk.fallos == 1 and marcados == ["AG-05"]
    pu = b.cfg["presupuesto_uc"]
    for v in r["presupuesto"].values():
        assert v["consumido"] <= v["asignado"] * (1 + pu["ampliacion_sin_autorizacion"]) + v["ampliado"] + 1e-6
