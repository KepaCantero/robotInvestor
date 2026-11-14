"""QA r01 de T-113 · alcance real de H-01: ¿llega hoy a la API un encargo con un par «"clave": "valor"» de R8 dentro de una
lista? Por `Agentes.invocar` (el encargo viaja también como texto JSON) y por `AnthropicClient.generar` llamado directamente
con contenido estructurado (SDK simulado).
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r01_13_r8_camino_real.py"""
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import AnthropicClient, MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import DATOS, config_pruebas  # noqa: E402

CLAVE = "api" + "_key"
t = Path(tempfile.mkdtemp(prefix="qa_t113_r8_", dir=os.environ.get("QA_TMP")))
cli = MockClient()
b = Bloque(config_pruebas(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli, t / "e", t / "n")
for nombre, msg in (("dict directo", {CLAVE: "abcdef123456"}), ("lista > dict", {"piezas": [{CLAVE: "abcdef123456"}]}),
                    ("lista > lista > dict", {"piezas": [[{CLAVE: "abcdef123456"}]]}), ("tupla > dict", {"piezas": ({CLAVE: "abcdef123456"},)})):
    n0 = len(cli.llamadas)
    r = b.agentes.invocar("AG-12", "CT-11", msg, "CURACION", "Clasifica.", {"fecha_as_of": "2026-06-05", "modo": "backtest"})
    print(f"Agentes.invocar · {nombre}: estado={r.estado} errores={r.errores} · llamadas al cliente: {len(cli.llamadas) - n0} (esperado 0, bloqueado por R8)")

enviados = []
sdk = SimpleNamespace(messages=SimpleNamespace(create=lambda **k: (enviados.append(k), SimpleNamespace(usage=None, stop_reason="end_turn", content=[]))[1]))
c = AnthropicClient.__new__(AnthropicClient)
c.sdk, c.salida_estructurada, c.max_continuaciones = sdk, False, 0
for nombre, mensajes in (("contenido texto con el par", [{"role": "user", "content": '{"' + CLAVE + '": "abcdef123456"}'}]),
                         ("contenido estructurado con el par", [{"role": "user", "content": [{"type": "tool_result", "content": {CLAVE: "abcdef123456"}}]}]),
                         ("par en el propio mensaje", [{"role": "user", "content": "hola", CLAVE: "abcdef123456"}])):
    n0 = len(enviados)
    try:
        r = c.generar(agente="AG-01", modelo="m", system=[{"type": "text", "text": "s"}], mensajes=mensajes, max_tokens=10)
        print(f"AnthropicClient.generar · {nombre}: stop={r.stop_reason} · enviado al SDK: {len(enviados) - n0} (esperado 0)")
    except Exception as e:  # noqa: BLE001
        print(f"AnthropicClient.generar · {nombre}: EXC {type(e).__name__}: {str(e)[:80]}")
