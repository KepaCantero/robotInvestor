"""QA r01 de T-137 · el peor caso, pasado por el cliente real y por el corte de presupuesto del ciclo.

`AnthropicClient` (el cliente real, `llm.py`) con un SDK falso que no sale de la máquina (sin clave, sin red, sin coste): cada
petición declara como uso el peor caso que supone la cota (toda la entrada como escritura de caché, con
`factor_tokens_cota`, y `max_tokens` de salida); en los agentes con búsqueda devuelve `pause_turn` hasta agotar
`llm.max_continuaciones_pause_turn`, con el texto largo que se reenvía; el primer intento de cada llamada no es JSON (se paga
la reparación de `llm.reintento_reparacion`) y el segundo es la respuesta del simulado. Así el ciclo recorre el mismo camino
que con el modelo real: `agentes.Agentes.invocar`, el presupuesto en UC de `orquestacion.Bloque._invocar` (que corta llamadas
cuando la bolsa se agota) y la contabilidad.
Se compara el coste de las peticiones hechas con la cota de `estimar_coste_ciclo_a.py` sobre el ciclo simulado.
Con `--forzar-c12`, G3 bloquea la primera redacción por legibilidad (C12) y el ciclo pide la reescritura a AG-17, como
haría con un texto real por debajo de Fernández-Huerta 70.
Uso (desde bloque_a/11_Ejecutor): python -I <este script> <carpeta temporal> [--config yaml] [--forzar-c12]
"""
import collections
import contextlib
import importlib.util
import io
import json
import shutil
import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
import yaml  # noqa: E402
from bloque_a import cli, llm, mock_respuestas  # noqa: E402

spec = importlib.util.spec_from_file_location("est", RAIZ / ".docs" / "scripts" / "estimar_coste_ciclo_a.py")
est = importlib.util.module_from_spec(spec)
spec.loader.exec_module(est)

S = Path(sys.argv[1])
extra = ["--config", sys.argv[sys.argv.index("--config") + 1]] if "--config" in sys.argv else []
cfg = est._config(extra[1] if extra else None)
tarifa = yaml.safe_load((RAIZ / "bloque_a" / "11_Ejecutor" / "config" / "precios_anthropic.yaml").read_text(encoding="utf-8"))
P, PB, F = tarifa["precios_por_millon"], float(tarifa["precio_busqueda_web_por_mil"]), float(tarifa["factor_tokens_cota"])
CONT = int(cfg["llm"]["max_continuaciones_pause_turn"])
MU = int(cfg["busqueda_web"]["max_usos_por_llamada"])
SEMILLA = int(cfg["llm"]["semilla_mock"])

peticiones: list[dict] = []


def _tok(x) -> int:
    return max(1, int(len(x) / 3.6))


class _Mensajes:
    def create(self, **kw):
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        sys_txt = "".join(b.get("text", "") for b in kw["system"])
        msgs = kw["messages"]
        salida = int(kw["max_tokens"])
        # lo que escribió el modelo vuelve con sus propios tokens (los que se cobraron como salida, sin el margen F); el resto
        # (system, encargo y el mensaje de errores de la reparación) con el margen del tokenizador, como la cota
        reenviado = sum(1 for m in msgs if m["role"] == "assistant") * salida
        propio = [m for m in msgs if m["role"] == "user"]
        entrada = int((_tok(sys_txt) + _tok(json.dumps(propio, ensure_ascii=False))) * F) + reenviado
        con_web = bool(kw.get("tools"))
        pausas = sum(1 for m in msgs if m["role"] == "assistant" and isinstance(m["content"], list))
        intento = sum(1 for m in msgs if m["role"] == "user")
        largo = "análisis " * int(salida * 3.6 / 9)        # el texto que ocuparía max_tokens (y que se reenvía)
        if con_web and pausas < CONT:
            stop, texto = "pause_turn", largo
        elif intento == 1:
            stop, texto = "end_turn", largo                 # no es JSON: el ejecutor pide la reparación
        else:
            stop = "end_turn"
            texto = json.dumps(mock_respuestas.responder(agente, msgs[:1], SEMILLA), ensure_ascii=False)
        p = P[kw["model"]]
        usd = est._coste(p, 0, salida, entrada, 0) + (MU * PB / 1000 if con_web else 0)
        peticiones.append({"agente": agente, "modelo": kw["model"], "entrada": entrada, "salida": salida, "usd": usd,
                           "stop": stop, "web": con_web})
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=salida, cache_creation_input_tokens=entrada,
                                    cache_read_input_tokens=0,
                                    server_tool_use=types.SimpleNamespace(web_search_requests=MU if con_web else 0))
        return types.SimpleNamespace(stop_reason=stop, usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


falso = types.SimpleNamespace(messages=_Mensajes())
orig_crear = llm.crear_cliente


def crear(tipo, cfg_, replay=None, replay_modo="reproducir"):
    return llm.AnthropicClient(sdk=falso, max_continuaciones=int(cfg_["llm"]["max_continuaciones_pause_turn"]),
                               salida_estructurada=False)


llm.crear_cliente = crear
if "--forzar-c12" in sys.argv:
    # G3 bloquea la primera redacción por legibilidad (C12, Fernández-Huerta < 70): el ciclo pide una reescritura a AG-17
    from bloque_a import redaccion
    _gen = redaccion.Redaccion.generar
    _veces = {"n": 0}

    def _generar(self, *a, **k):
        entreg, g3b = _gen(self, *a, **k)
        _veces["n"] += 1
        if _veces["n"] == 1:
            g3b = dict(g3b, dictamen="BLOQUEADO", bloqueos=["C12"], legibilidad=60, frases_largas=[])
        return entreg, g3b
    redaccion.Redaccion.generar = _generar
shutil.rmtree(S, ignore_errors=True)
S.mkdir(parents=True)
with contextlib.redirect_stdout(io.StringIO()):
    cli.main(["--cliente", "anthropic", "--datos", "ejemplos/datos_sinteticos", "--estado", str(S / "estado"), "--salida",
              str(S / "salida"), "--as-of", "2024-03-29"] + extra + ["ciclo"])

total = sum(x["usd"] for x in peticiones)
por = collections.Counter(x["agente"] for x in peticiones)
web = sum(1 for x in peticiones if x["web"])
print(f"peticiones {len(peticiones)} (con búsqueda {web}) · coste del peor caso pasado por el ciclo {total:.2f} USD")
print("  por agente:", dict(sorted(por.items())))
ha = [json.loads(l) for f in (S / "estado").rglob("*.jsonl") for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
cortes = [x for x in ha if isinstance(x, dict) and "presupuesto insuficiente" in json.dumps(x, ensure_ascii=False)]
print(f"  registros con «presupuesto insuficiente» en el estado: {len(cortes)}")
for c in cortes[:8]:
    print("   ·", json.dumps(c, ensure_ascii=False)[:200])
print("  mayor entrada de una petición por modelo:",
      {m: max(x["entrada"] for x in peticiones if x["modelo"] == m) for m in {x["modelo"] for x in peticiones}})
