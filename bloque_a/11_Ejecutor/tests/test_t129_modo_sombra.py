"""T-129 · Preparar el modo sombra sin gasto: lo que el cliente real envía a la API, los identificadores de modelo, la
herramienta de búsqueda web y la tarifa con la que se estima el coste. Sin red: el SDK es un doble que anota cada petición
y responde con el cliente simulado."""
import importlib.util
import json
import re
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from bloque_a.configuracion import cargar_config
from bloque_a.llm import AnthropicClient, MockClient, crear_cliente
from conftest import config_pruebas, nuevo_bloque

RAIZ = Path(__file__).resolve().parents[1]
PRECIOS = RAIZ / "config" / "precios_anthropic.yaml"
# Comprobados en la documentación de Anthropic el 15-11-2026 (página de modelos y de precios); se vuelven a comprobar antes
# de autorizar gasto (CLAUDE.md, «Identificadores de modelo sin verificar»)
MODELOS_VIGENTES = {"claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"}
# Versiones de la herramienta de búsqueda web documentadas el 15-11-2026
BUSQUEDA_WEB_VIGENTES = {"web_search_20250305", "web_search_20260209", "web_search_20260318"}
# Lo que el cliente puede enviar; lo demás (temperature, top_p, top_k, thinking, tool_choice…) lo rechazan con un 400 los
# modelos de la familia 5.5 en alguna de sus formas
CLAVES_PERMITIDAS = {"model", "max_tokens", "system", "messages", "metadata", "tools", "output_config"}


class SDKQueAnota:
    """Doble del SDK: anota cada petición y responde con el texto del cliente simulado para el mismo agente."""

    def __init__(self):
        self.messages = self
        self.peticiones: list[dict] = []
        self.mock = MockClient()

    def create(self, **kw):
        self.peticiones.append(json.loads(json.dumps(kw, default=str)))
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        r = self.mock.generar(agente=agente, modelo=kw["model"], system=kw["system"], mensajes=kw["messages"],
                              max_tokens=kw["max_tokens"], herramientas=kw.get("tools"), esquema=None)
        return SimpleNamespace(stop_reason="end_turn", usage=SimpleNamespace(input_tokens=100, output_tokens=50),
                               content=[SimpleNamespace(type="text", text=r.texto)])


@pytest.fixture(scope="module", params=["backtest", "vivo"])
def ciclo_con_cliente_real(request, tmp_path_factory, universo):
    # en vivo, como en el modo sombra: es donde se añade la búsqueda web (en backtest está desactivada, por fuga)
    sdk = SDKQueAnota()
    tmp = tmp_path_factory.mktemp("t129")
    b = nuevo_bloque(tmp, universo, cliente=AnthropicClient(sdk=sdk), cfg=config_pruebas(modo=request.param))
    run = b.ciclo("2026-06-05", alcance={"clases": ["RV", "DIV"]}, nivel_forzado="N2")
    return request.param, run, sdk.peticiones


def test_el_ciclo_con_el_cliente_real_termina(ciclo_con_cliente_real):
    modo, run, peticiones = ciclo_con_cliente_real
    assert run["estado"] == "COMPLETO" and len(peticiones) >= 10
    con_busqueda = [k for k in peticiones if k.get("tools")]
    if modo == "vivo":     # la búsqueda web llega a la API, y solo en los agentes que la tienen
        agentes = set(cargar_config()["busqueda_web"]["agentes"])
        assert con_busqueda and all(k["metadata"]["user_id"].removeprefix("bloque-a-") in agentes for k in con_busqueda)
    else:
        assert con_busqueda == []


def test_ninguna_peticion_lleva_parametros_que_la_api_rechaza(ciclo_con_cliente_real):
    _, _, peticiones = ciclo_con_cliente_real
    for kw in peticiones:
        assert set(kw) <= CLAVES_PERMITIDAS, set(kw) - CLAVES_PERMITIDAS
        assert kw["model"] in MODELOS_VIGENTES
        assert 0 < kw["max_tokens"] <= 16000          # sin streaming, por debajo del umbral de tiempo del SDK
        assert kw["messages"] and kw["messages"][0]["role"] == "user"
        assert kw["messages"][-1]["role"] == "user"   # sin «prefill» de asistente (400 en la familia 5.5)
        for h in kw.get("tools") or []:
            assert h.get("type") in BUSQUEDA_WEB_VIGENTES and h.get("name") == "web_search"


def test_la_metadata_no_lleva_datos_personales(ciclo_con_cliente_real):
    _, _, peticiones = ciclo_con_cliente_real
    for kw in peticiones:
        assert set(kw["metadata"]) == {"user_id"} and re.fullmatch(r"bloque-a-AG-\d{2}", kw["metadata"]["user_id"])


def test_sin_clave_el_cliente_real_no_arranca(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        crear_cliente("anthropic", config_pruebas())


def test_los_modelos_de_la_configuracion_son_los_vigentes_y_tienen_tarifa():
    cfg = cargar_config()
    usados = set(cfg["modelos"].values())
    assert usados <= MODELOS_VIGENTES, usados - MODELOS_VIGENTES
    tarifa = yaml.safe_load(PRECIOS.read_text(encoding="utf-8"))
    for m in usados:
        p = tarifa["precios_por_millon"][m]
        assert all(isinstance(p[k], float) and p[k] > 0 for k in ("entrada", "salida", "escritura_cache", "lectura_cache"))
        assert p["lectura_cache"] < p["entrada"] < p["salida"]
    assert tarifa["precio_busqueda_web_por_mil"] > 0
    assert cfg["busqueda_web"]["tipo_herramienta"] in BUSQUEDA_WEB_VIGENTES


def test_la_configuracion_por_defecto_sigue_sin_precios():
    # la entrega no inventa precios: la tarifa va aparte y se pasa con --config
    cfg = cargar_config()
    assert all(v is None for p in cfg["precios_por_millon"].values() for v in p.values())
    con = cargar_config(str(PRECIOS))
    assert con["precios_por_millon"]["claude-opus-5-5"]["entrada"] == 4.0


def _estimador():
    ruta = RAIZ.parents[1] / ".docs" / "scripts" / "estimar_coste_ciclo_a.py"
    spec = importlib.util.spec_from_file_location("estimar_coste_ciclo_a", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_el_estimador_aplica_la_tarifa_y_la_cota():
    est = _estimador()
    precios = {"m": {"entrada": 2.0, "salida": 10.0, "escritura_cache": 4.0, "lectura_cache": 0.1}}
    llamadas = [{"agente": "AG-03", "modelo": "m", "sys_tok": 1_000_000, "user_tok": 500_000, "out_tok": 100_000,
                 "max_tokens": 1_000_000, "cache_escr": 1_000_000, "cache_lect": 0},
                {"agente": "AG-16", "modelo": "m", "sys_tok": 1_000_000, "user_tok": 0, "out_tok": 0,
                 "max_tokens": 0, "cache_escr": 0, "cache_lect": 1_000_000}]
    r = est.estimar(llamadas, precios, 10.0, {"AG-16"}, 5)
    # 1.ª: 0,5 M de entrada (1) + 0,1 M de salida (1) + 1 M de escritura (4) = 6; 2.ª: 1 M de lectura = 0,1
    assert r["estimacion"] == pytest.approx(6.1)
    # cota: la salida hasta max_tokens (1 M × 10 = 10 en vez de 1) y 5 búsquedas a 10 USD/1000 en AG-16
    assert r["cota_superior"] == pytest.approx(6.1 - 1 + 10 + 0.05) and r["busquedas_cota"] == 5
    with pytest.raises(SystemExit):
        est.estimar([dict(llamadas[0], modelo="otro")], precios, 10.0, set(), 0)
