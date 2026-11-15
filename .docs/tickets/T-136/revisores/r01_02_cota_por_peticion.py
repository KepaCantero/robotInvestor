"""QA r01 de T-133 · ¿la cota superior de `estimar_coste_ciclo_a.py` acota lo que el cliente real puede pedir?

El cliente real (`llm.AnthropicClient.generar`) hace hasta 1 + `llm.max_continuaciones_pause_turn` peticiones por llamada
de un agente con búsqueda; cada petición es un `messages.create` con su propio `max_tokens` de salida, y la siguiente
reenvía como entrada el contenido del asistente de la anterior. `agentes.Agentes` repite además la llamada entera
`llm.reintento_reparacion` veces si el JSON no cumple su esquema, reenviando la respuesta anterior y los errores.

Se recalcula, sobre el mismo `llamadas.json` del README, una cota «por petición» (sin lo leído por cada búsqueda, que el
estimador declara fuera):
 A. cada vuelta con hasta `max_tokens` de salida y la entrada creciendo con la salida de las vueltas anteriores;
 B. A más una reparación de JSON por llamada (que el estimador también declara fuera, pero está acotada en la
    configuración: `llm.reintento_reparacion`).
Uso (desde la raíz de la copia): python -I r01_02_cota_por_peticion.py <carpeta de medir_consumo_a> [--config yaml]
"""
import importlib.util
import json
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("est", RAIZ / ".docs" / "scripts" / "estimar_coste_ciclo_a.py")
est = importlib.util.module_from_spec(spec)
spec.loader.exec_module(est)

carpeta = Path(sys.argv[1])
extra = sys.argv[sys.argv.index("--config") + 1] if "--config" in sys.argv else None
ll = json.loads((carpeta / "llamadas.json").read_text(encoding="utf-8"))
tarifa = yaml.safe_load((RAIZ / "bloque_a" / "11_Ejecutor" / "config" / "precios_anthropic.yaml").read_text(encoding="utf-8"))
cfg = est._config(extra)
bw = cfg["busqueda_web"]
agentes = set(bw["agentes"]) if bw.get("habilitada_en_vivo") else set()
mu, cont = int(bw["max_usos_por_llamada"]), int(cfg["llm"]["max_continuaciones_pause_turn"])
rep = int(cfg["llm"]["reintento_reparacion"])
P, PB, F = tarifa["precios_por_millon"], float(tarifa["precio_busqueda_web_por_mil"]), float(tarifa["factor_tokens_cota"])

oficial = est.estimar(ll, P, PB, agentes, mu, F, cont)
print(f"cota del estimador: {oficial['cota_superior']:.2f} USD ({oficial['llamadas']} llamadas, {oficial['busquedas_cota']} búsquedas)")


def llamada(x, entrada_extra=0.0):
    """Coste máximo de una llamada `generar`: vueltas de pause_turn, cada una con max_tokens de salida."""
    p = P[x["modelo"]]
    vueltas = 1 + (cont if x["agente"] in agentes else 0)
    entrada = (x["sys_tok"] + x["user_tok"]) * F + entrada_extra
    total, busq = 0.0, 0
    for v in range(vueltas):
        total += est._coste(p, 0, x["max_tokens"], entrada + v * x["max_tokens"], 0)   # la salida previa vuelve como entrada
        if x["agente"] in agentes:
            busq += mu
            total += mu * PB / 1000
    return total, busq, vueltas * x["max_tokens"]


a = b = 0.0
for x in ll:
    c1, _, salida1 = llamada(x)
    a += c1
    b += c1
    for _ in range(rep):   # la reparación reenvía la conversación con la respuesta anterior (hasta su salida) y los errores
        c2, _, salida1 = llamada(x, entrada_extra=salida1)
        b += c2
print(f"A. cada petición con su max_tokens de salida y la salida previa reenviada: {a:.2f} USD "
      f"({100 * (a / oficial['cota_superior'] - 1):+.1f} %)")
print(f"B. A + {rep} reparación de JSON por llamada (llm.reintento_reparacion): {b:.2f} USD "
      f"({100 * (b / oficial['cota_superior'] - 1):+.1f} %)")
print(f"{'FALLA' if a > oficial['cota_superior'] else 'ok   '} la cota del estimador cubre A")
