"""Clientes (simulado, repetición y Anthropic con un SDK falso), búsqueda web solo en vivo y para los agentes de
conocimiento, copias literales de las herramientas de referencia y la CLI `bloque-b`."""
import filecmp
import json
import types
from pathlib import Path

import pytest
import yaml

from bloque_b import cli
from bloque_b.agentes import Invocador
from bloque_b.configuracion import DIR_EJECUTOR
from bloque_b.herramientas import DIR_REFERENCIA
from bloque_b.llm import AnthropicClient, MockClient, ReplayClient, ReplayFaltante
from bloque_b.orquestacion import Coordinador
from bloque_b.prompts import CatalogoPrompts

from conftest import PETICION_REDES, peticion_redes

DIR_HERRAMIENTAS = DIR_EJECUTOR.parent / "10_Herramientas"


# ------------------------------------------------------------------------------------------ copias de referencia
@pytest.mark.parametrize("nombre", sorted(p.name for p in DIR_REFERENCIA.glob("ht*.py")))
def test_copias_identicas_a_10_herramientas(nombre):
    assert filecmp.cmp(DIR_REFERENCIA / nombre, DIR_HERRAMIENTAS / nombre, shallow=False), nombre


def test_estan_todas_las_herramientas_de_referencia():
    assert {p.name for p in DIR_REFERENCIA.glob("ht*.py")} == {p.name for p in DIR_HERRAMIENTAS.glob("ht*.py")}


# ------------------------------------------------------------------------------------------ clientes
def test_mock_determinista_y_cache_simulada():
    m = MockClient(1)
    kw = dict(agente="AG-B22", modelo="x", system=[{"type": "text", "text": "S"}], max_tokens=10,
              mensajes=[{"role": "user", "content": "## Encargo (JSON)\n```json\n{\"mensaje\": {\"tarea\": \"auditoria\"}}\n```"}])
    a, b = m.generar(**kw), m.generar(**kw)
    assert a.texto == b.texto
    assert a.uso.cache_escritura > 0 and b.uso.cache_lectura > 0 and b.uso.cache_escritura == 0


def test_replay_graba_y_reproduce(hacer_entorno, rapido, tmp_path, monkeypatch):
    grab = tmp_path / "grabacion.jsonl"
    monkeypatch.setenv("BLOQUE_B_CLIENTE_BASE", "mock")
    e1 = hacer_entorno(rapido, cliente="replay", replay=str(grab), replay_modo="grabar")
    r1 = Coordinador(e1).recibir(peticion_redes())
    assert grab.exists() and len(grab.read_text(encoding="utf-8").splitlines()) > 20
    e2 = hacer_entorno(rapido, cliente="replay", replay=str(grab), replay_modo="reproducir")
    r2 = Coordinador(e2).recibir(peticion_redes())
    assert r1["resumen"] == r2["resumen"]
    p1 = json.loads(Path(r1["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    p2 = json.loads(Path(r2["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert p1["veredicto"] == p2["veredicto"] and p1["puntuaciones"] == p2["puntuaciones"] and p1["candidatos_por_tipo"] == p2["candidatos_por_tipo"]
    rp = ReplayClient(grab, "reproducir")
    with pytest.raises(ReplayFaltante):
        rp.generar(agente="AG-B01", modelo="m", system=[], mensajes=[{"role": "user", "content": "nuevo"}], max_tokens=5)
    with pytest.raises(FileNotFoundError):
        ReplayClient(tmp_path / "no.jsonl", "reproducir")


class _SDKFalso:
    """Imita `anthropic.Anthropic().messages.create`: la primera respuesta es pause_turn y la segunda end_turn."""

    def __init__(self, texto='{"clasificacion": "ADMITIDA"}'):
        self.llamadas = []
        self.texto = texto
        self.messages = types.SimpleNamespace(create=self._create)

    def _create(self, **kw):
        self.llamadas.append(kw)
        stop = "pause_turn" if len(self.llamadas) == 1 else "end_turn"
        uso = types.SimpleNamespace(input_tokens=100, output_tokens=50, cache_creation_input_tokens=1000, cache_read_input_tokens=0,
                                    server_tool_use=types.SimpleNamespace(web_search_requests=1))
        bloque = types.SimpleNamespace(type="text", text=self.texto if stop == "end_turn" else "")
        return types.SimpleNamespace(content=[bloque], usage=uso, stop_reason=stop)


def test_cliente_anthropic_con_sdk_falso():
    sdk = _SDKFalso()
    c = AnthropicClient(sdk=sdk)
    r = c.generar(agente="AG-B01", modelo="claude-haiku-5-5", system=[{"type": "text", "text": "S"}],
                  mensajes=[{"role": "user", "content": "hola"}], max_tokens=100)
    assert r.texto == '{"clasificacion": "ADMITIDA"}' and r.stop_reason == "end_turn"
    assert len(sdk.llamadas) == 2 and sdk.llamadas[1]["messages"][-1]["role"] == "assistant"   # continuación de pause_turn
    assert r.uso.entrada == 200 and r.uso.busquedas_web == 2
    assert sdk.llamadas[0]["metadata"] == {"user_id": "bloque-b-AG-B01"}


def test_cliente_anthropic_sin_clave(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    pytest.importorskip("anthropic")
    with pytest.raises(RuntimeError):
        AnthropicClient()


def test_busqueda_web_solo_en_vivo_y_para_agentes_de_conocimiento(hacer_cfg, tmp_path):
    cfg = hacer_cfg()
    sdk = _SDKFalso('{"referencias": []}')
    inv = Invocador(cfg, AnthropicClient(sdk=sdk), CatalogoPrompts(cfg, "mock"), None, "vivo")
    inv.llamar("AG-B20", "CT-B-14", "busqueda", {}, "x", {"referencias": "array"}, {}, busqueda=True)
    assert sdk.llamadas[-1]["tools"][0]["name"] == "web_search"
    n = len(sdk.llamadas)
    inv.llamar("AG-B12", "CT-B-14", "busqueda", {}, "x", {}, {}, busqueda=True)
    assert "tools" not in sdk.llamadas[-1]
    inv.modo = "backtest"
    inv.llamar("AG-B20", "CT-B-14", "busqueda", {}, "x", {}, {}, busqueda=True)
    assert "tools" not in sdk.llamadas[-1] and len(sdk.llamadas) > n
    texto = sdk.llamadas[-1]["messages"][0]["content"]
    assert "búsqueda web desactivada" in texto


# ------------------------------------------------------------------------------------------ CLI
@pytest.fixture
def cfg_yaml(tmp_path, dir_prompts_vacio):
    p = tmp_path / "cfg.yaml"
    p.write_text(yaml.safe_dump({"rutas": {"prompts": str(dir_prompts_vacio)}}), encoding="utf-8")
    return str(p)


def _cli(capsys, *args):
    assert cli.main(list(args)) == 0
    return json.loads(capsys.readouterr().out)


def test_cli_flujo_completo(tmp_path, cfg_yaml, capsys):
    g = ["--config", cfg_yaml, "--estado", str(tmp_path / "e"), "--salida", str(tmp_path / "s"), "--as-of", "2026-11-03"]
    r = _cli(capsys, *g, "analizar", "--json", str(PETICION_REDES))
    assert r["estado"] == "EN_PAUSA"
    e = _cli(capsys, *g, "estado", "--pet", r["pet_id"])
    assert e["autorizaciones_pendientes"][0]["aut_id"] == r["aut_id"]
    f = _cli(capsys, *g, "autorizar", "--aut", r["aut_id"], "--opcion", "CONTINUAR", "--decidido-por", "BROKER", "--motivo", "ok")
    assert f["estado_peticion"] == "ENTREGADA"
    s = _cli(capsys, *g, "vigia")
    assert "alertas" in s
    q = _cli(capsys, *g, "consulta", "¿Qué tipo de activo domina?", "--contexto", f["rec_id"])
    assert q["query_id"].startswith("QRY-B-")
    d = tmp_path / "decision.json"
    d.write_text(json.dumps({"decision_ambito": {"rec_id": f["rec_id"], "decision": "EN_VIGILANCIA"}}), encoding="utf-8")
    assert _cli(capsys, *g, "decision", "--json", str(d))["estado"] == "COMPLETO"
    assert "resueltos" in _cli(capsys, *g, "evaluar")
    assert _cli(capsys, *g, "verificar-enlaces", "--max-fichas", "3")["modo"].startswith("sin red")
    assert _cli(capsys, *g, "estado", "--config")["f10"]


def test_cli_sinteticos_csv_y_backtest(tmp_path, cfg_yaml, capsys):
    datos = tmp_path / "datos"
    r = _cli(capsys, "--config", cfg_yaml, "generar-sinteticos", "--salida", str(datos))
    assert r["series"] > 100
    g = ["--config", cfg_yaml, "--datos", str(datos), "--estado", str(tmp_path / "e"), "--salida", str(tmp_path / "s")]
    b = _cli(capsys, *g, "backtest", "--peticion", str(PETICION_REDES), "--desde", "2024-01-01", "--hasta", "2024-03-31", "--solo-seleccion")
    assert b["fechas"] == 3 and (tmp_path / "s" / "rankings.csv").exists()


def test_cli_rechaza_opcion_invalida(capsys):
    with pytest.raises(SystemExit):
        cli.main(["autorizar", "--aut", "AUT-B-2026-0001", "--opcion", "SEGUIR"])
