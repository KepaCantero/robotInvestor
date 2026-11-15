"""T-146 · UC por bolsa de un ciclo C1 con el peor caso pasado por el cliente real (SDK falso: sin red, sin clave, sin coste).

Cada petición declara su peor caso (la entrada con el margen 1,35 como escritura de caché y lo reenviado con sus tokens,
`max_tokens` de salida, las búsquedas al máximo), los agentes con búsqueda devuelven `pause_turn` hasta agotar las
continuaciones y el primer intento de cada llamada no es JSON (se paga la reparación). El mismo SDK de
`tests/test_t146_presupuesto.py`, copiado aquí para poder correrlo también contra el código anterior a T-146.

Uso: python -I peor_caso_por_bolsa.py <ruta a 11_Ejecutor> <carpeta temporal> [--doce] [--hilos N]
Imprime, por bolsa: consumido, límite actual (asignado × 1,25 + ampliado) y límite con la ampliación máxima; y la suma."""
import json
import sys
import types
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
TMP = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(EJ))
from bloque_a import mock_respuestas  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import AnthropicClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

DOCE = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
extra = {"modo": "vivo", "perfiles": {"activos": DOCE if "--doce" in sys.argv else ["DIV"]}}
if "--hilos" in sys.argv:
    extra["paralelismo"] = {"hilos_analistas": int(sys.argv[sys.argv.index("--hilos") + 1])}
cfg = cargar_config(extra=extra)


def _tok(t):
    return max(1, int(len(t) / 3.6))


def _texto(c):
    return c if isinstance(c, str) else "".join(getattr(b, "text", "") or "" for b in c)


class SDK:
    def __init__(self, cont, usos, semilla):
        self.cont, self.usos, self.semilla, self.n = cont, usos, semilla, 0
        self.messages = self

    def create(self, **kw):
        self.n += 1
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        msgs, salida = kw["messages"], int(kw["max_tokens"])
        sys_txt = "".join(b.get("text", "") for b in kw["system"])
        propio = [m for m in msgs if m["role"] == "user"]
        reenviado = sum(_tok(_texto(m["content"])) for m in msgs if m["role"] == "assistant")
        entrada = int((_tok(sys_txt) + _tok(json.dumps(propio, ensure_ascii=False))) * 1.35) + reenviado
        web = bool(kw.get("tools"))
        pausas = sum(1 for m in msgs if m["role"] == "assistant" and not isinstance(m["content"], str))
        largo = "análisis " * int(salida * 3.6 / 9)
        if web and pausas < self.cont:
            stop, texto = "pause_turn", largo
        elif len(propio) == 1:
            stop, texto = "end_turn", largo
        else:
            stop, texto = "end_turn", json.dumps(mock_respuestas.responder(agente, msgs[:1], self.semilla), ensure_ascii=False)
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=salida, cache_creation_input_tokens=entrada, cache_read_input_tokens=0,
                                    server_tool_use=types.SimpleNamespace(web_search_requests=self.usos if web else 0))
        return types.SimpleNamespace(stop_reason=stop, usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


cont = int(cfg["llm"]["max_continuaciones_pause_turn"])
sdk = SDK(cont, int(cfg["busqueda_web"]["max_usos_por_llamada"]), int(cfg["llm"]["semilla_mock"]))
b = Bloque(cfg, ProveedorCSV(EJ / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
           AnthropicClient(sdk=sdk, max_continuaciones=cont), TMP / "estado", TMP / "ent")
r = b.ciclo("2024-03-29", nivel_forzado="N2")
pu = cfg["presupuesto_uc"]
tot = 0.0
print(f"estado {r['estado']} · peticiones {sdk.n} · llamadas {len(b.contabilidad.llamadas)}")
for bolsa, v in sorted(r["presupuesto"].items()):
    lim = v["asignado"] * (1 + pu["ampliacion_sin_autorizacion"]) + v["ampliado"]
    mx = v["asignado"] * (1 + pu["ampliacion_max_autorizable"])
    tot += v["consumido"]
    print(f"  {bolsa:7} consumido {v['consumido']:8.2f} · límite {lim:7.2f} · con la ampliación máxima {mx:7.2f}"
          + ("  ← PASA" if v["consumido"] > lim + 1e-6 else ""))
gastado = sum(x["uc"] for x in b.contabilidad.llamadas)
print(f"  suma de las bolsas {tot:.2f} · gastado (contabilidad, todas las llamadas) {gastado:.2f} · "
      f"ciclo con la ampliación máxima {pu['ciclo_semanal_max'] * (1 + pu['ampliacion_max_autorizable']):.2f}")
