"""QA r01 de T-129 · el cliente real con el SDK de verdad (anthropic 2.8.0) y un transporte HTTP en memoria: sin red, sin gasto.

La prueba del implementador usa un doble del SDK que acepta cualquier **kw; aquí lo que se comprueba es el cuerpo HTTP que el
SDK instalado construye de verdad (serialización, cabeceras, comprobación de tiempo sin streaming) y qué hace el cliente con
`pause_turn` (continuación) y con un 400 del servidor.

 1. Ciclo en vivo (RV y DIV, N2) con `anthropic.Anthropic(api_key=<falsa>, http_client=<MockTransport>)`: ningún cuerpo lleva
    temperature, top_p, top_k, thinking, tool_choice ni prefill; la herramienta es la de la configuración; cabecera
    `anthropic-version`; ningún error del SDK escondido como `error_proveedor`.
 2. `pause_turn`: cuántas peticiones genera una sola llamada de un agente con búsqueda (hasta 1 + max_continuaciones) y qué
    `max_tokens` lleva cada una: es lo que la cota superior del estimador cuenta una sola vez.
 3. Un 400 del servidor (el que daría un parámetro rechazado) acaba como `error_proveedor`, sin el mensaje (R8).
Uso (desde la raíz de la copia): python -I .docs/tickets/T-129/revisores/r01_01_sdk_real_sin_red.py [ejecutor]
"""
import json
import sys
import tempfile
from pathlib import Path

import httpx2 as httpx  # el SDK 2.x usa httpx2

RAIZ = Path(__file__).resolve().parents[4]
EJE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJE))
sys.path.insert(0, str(EJE / "tests"))
import anthropic  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.llm import AnthropicClient, MockClient  # noqa: E402
from conftest import config_pruebas, nuevo_bloque  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

FALLOS: list[str] = []
OK = 0


def comprobar(cond, msg):
    global OK
    if cond:
        OK += 1
        print("  ok  ", msg)
    else:
        FALLOS.append(msg)
        print("  FALLO", msg)


PROHIBIDAS = {"temperature", "top_p", "top_k", "thinking", "tool_choice", "stop_sequences", "service_tier"}
mock = MockClient()


def mensaje(texto, stop="end_turn", modelo="claude-sonnet-5-5"):
    return {"id": "msg_qa", "type": "message", "role": "assistant", "model": modelo,
            "content": [{"type": "text", "text": texto}], "stop_reason": stop, "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 5}}


class Servidor:
    def __init__(self, modo_pause=False, codigo=200):
        self.cuerpos, self.cabeceras, self.modo_pause, self.codigo = [], [], modo_pause, codigo

    def __call__(self, req: httpx.Request) -> httpx.Response:
        cuerpo = json.loads(req.content)
        self.cuerpos.append(cuerpo)
        self.cabeceras.append(dict(req.headers))
        if self.codigo != 200:
            return httpx.Response(self.codigo, json={"type": "error", "error": {
                "type": "invalid_request_error", "message": "temperature: no admitido (clave sk-ant-api03-SECRETO)"}})
        if self.modo_pause:
            return httpx.Response(200, json=mensaje("", stop="pause_turn", modelo=cuerpo["model"]))
        agente = cuerpo["metadata"]["user_id"].removeprefix("bloque-a-")
        r = mock.generar(agente=agente, modelo=cuerpo["model"], system=cuerpo["system"], mensajes=cuerpo["messages"],
                         max_tokens=cuerpo["max_tokens"], herramientas=cuerpo.get("tools"), esquema=None)
        return httpx.Response(200, json=mensaje(r.texto, modelo=cuerpo["model"]))


def cliente(servidor, **kw):
    sdk = anthropic.Anthropic(api_key="clave-falsa-qa", max_retries=0,
                              http_client=httpx.Client(transport=httpx.MockTransport(servidor)))
    return AnthropicClient(sdk=sdk, **kw)


print(f"anthropic {anthropic.__version__}")
cfg_def = cargar_config()
print("1. ciclo en vivo con el SDK real")
srv = Servidor()
tmp = tempfile.mkdtemp(prefix="qa_t129_")
universo = cargar_universo(EJE / "config" / "universo_ejemplo.csv")
b = nuevo_bloque(tmp, universo, cliente=cliente(srv), cfg=config_pruebas(modo="vivo"))
run = b.ciclo("2026-06-05", alcance={"clases": ["RV", "DIV"]}, nivel_forzado="N2")
comprobar(run["estado"] == "COMPLETO", f"ciclo COMPLETO ({run['estado']}), {len(srv.cuerpos)} peticiones HTTP")
claves = set().union(*(set(c) for c in srv.cuerpos))
comprobar(not (claves & PROHIBIDAS), f"ningún cuerpo con {sorted(PROHIBIDAS)}; claves enviadas {sorted(claves)}")
comprobar(all(c["messages"][-1]["role"] == "user" for c in srv.cuerpos), "sin prefill de asistente")
tipos = {h["type"] for c in srv.cuerpos for h in c.get("tools") or []}
comprobar(tipos == {cfg_def["busqueda_web"]["tipo_herramienta"]}, f"herramienta enviada {tipos}")
comprobar(all(h.get("max_uses") == cfg_def["busqueda_web"]["max_usos_por_llamada"]
              for c in srv.cuerpos for h in c.get("tools") or []), "max_uses de la configuración")
versiones = {h.get("anthropic-version") for h in srv.cabeceras}
print("     anthropic-version:", versiones)
ttl = {bl.get("cache_control", {}).get("ttl") for c in srv.cuerpos for bl in c["system"] if bl.get("cache_control")}
comprobar(ttl == {"1h"}, f"cache_control ttl {ttl} (la tarifa usa la escritura de 1 h)")
orden_ok = all(
    [bl["cache_control"].get("ttl") for bl in c["system"] if bl.get("cache_control")]
    == sorted([bl["cache_control"].get("ttl") for bl in c["system"] if bl.get("cache_control")], key=lambda t: t != "1h")
    for c in srv.cuerpos)
comprobar(orden_ok, "las entradas de 1 h van antes que las de 5 min")
n_puntos = max(sum(1 for bl in c["system"] if bl.get("cache_control")) for c in srv.cuerpos)
comprobar(n_puntos <= 4, f"como mucho 4 puntos de caché por petición ({n_puntos})")

print("2. pause_turn: peticiones por llamada")
srv2 = Servidor(modo_pause=True)
c2 = cliente(srv2, max_continuaciones=cfg_def["llm"]["max_continuaciones_pause_turn"])
herr = [{"type": cfg_def["busqueda_web"]["tipo_herramienta"], "name": "web_search",
         "max_uses": cfg_def["busqueda_web"]["max_usos_por_llamada"]}]
r = c2.generar(agente="AG-14", modelo="claude-sonnet-5-5", system=[{"type": "text", "text": "s"}],
               mensajes=[{"role": "user", "content": "u"}], max_tokens=4000, herramientas=herr)
n = len(srv2.cuerpos)
print(f"     una llamada con pause_turn continuo -> {n} peticiones HTTP, max_tokens {[c['max_tokens'] for c in srv2.cuerpos]}"
      f", stop_reason final {r.stop_reason!r}")
comprobar(n == 1, "la cota del estimador cuenta 1 petición y max_usos búsquedas por llamada (aquí hay "
          f"{n} peticiones: hasta {n}× la salida máxima; con filtrado dinámico, las búsquedas desde ejecución de código "
          "de peticiones anteriores del turno no cuentan para max_uses)")
comprobar(srv2.cuerpos[-1]["messages"][-1]["role"] == "assistant",
          "la continuación de pause_turn termina en el turno de asistente (lo documentado, no un prefill)")

print("3. un 400 del servidor")
srv3 = Servidor(codigo=400)
r3 = cliente(srv3).generar(agente="AG-03", modelo="claude-sonnet-5-5", system=[{"type": "text", "text": "s"}],
                           mensajes=[{"role": "user", "content": "u"}], max_tokens=100)
comprobar(r3.stop_reason == "error_proveedor" and "SECRETO" not in json.dumps(r3.__dict__, default=str),
          f"400 -> {r3.stop_reason!r}, sin el mensaje del servidor")

print(f"\nr01_01 T-129: {OK} ok, {len(FALLOS)} fallos")
for f in FALLOS:
    print("  -", f)
