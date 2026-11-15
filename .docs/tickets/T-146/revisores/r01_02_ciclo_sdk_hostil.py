"""QA r01 de T-146 · un ciclo C1 con el cliente real (`AnthropicClient`) sobre un SDK falso hostil (sin red, sin clave, sin coste).

Uso: python -I r01_02_ciclo_sdk_hostil.py <ruta a 11_Ejecutor> <carpeta temporal> [opciones]
  --tipos RV,RF,DIV,MP   tipos activos (por defecto, solo DIV)
  --hilos N              hilos de los analistas
  --v6                   diseño V6
  --factor F             tokens reales = F × la medida del ejecutor (3,6 caracteres por token); 1,35 = lo que se reserva
  --lectura N            tokens que trae cada búsqueda (se cobran como entrada en la misma petición)
  --cache                caché de prompts como la API: el primero que envía un system prompt lo escribe y los demás lo leen
  --orden directo|inverso  fuerza qué hilo llega antes a los agentes compartidos (retardo por hilo)
  --veces K              repite el ciclo K veces con el mismo orden y compara F5 (determinismo)

Cada petición: salida = max_tokens; búsquedas = max_uses; los agentes con búsqueda devuelven pause_turn hasta agotar las
continuaciones; el primer intento de cada llamada no es JSON (se paga la reparación). Imprime por bolsa consumido / límite
(con la escala de `tope_total`), la suma frente a 240 × 1,5, lo gastado frente a lo cargado, excesos, recortes y cierres."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import threading
import time
import types
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("ej")
ap.add_argument("tmp")
ap.add_argument("--tipos", default="DIV")
ap.add_argument("--hilos", type=int)
ap.add_argument("--v6", action="store_true")
ap.add_argument("--factor", type=float, default=1.35)
ap.add_argument("--lectura", type=int, default=0)
ap.add_argument("--cache", action="store_true")
ap.add_argument("--orden", choices=["directo", "inverso"])
ap.add_argument("--veces", type=int, default=1)
ap.add_argument("--as-of", default="2024-03-29")
a = ap.parse_args()

EJ = Path(a.ej).resolve()
TMP = Path(a.tmp).resolve()
sys.path.insert(0, str(EJ))
from bloque_a import mock_respuestas  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
try:
    from bloque_a.consumo import tokens_de_peticion  # noqa: E402
except ImportError:   # código anterior a T-146: la misma medida, copiada
    def _volcar(o):
        return o.model_dump() if hasattr(o, "model_dump") else (vars(o) if hasattr(o, "__dict__") else str(o))

    def tokens_de_peticion(system, mensajes, herramientas):
        texto = "".join(str(b.get("text", "")) for b in system or []) + json.dumps(mensajes, ensure_ascii=False, default=_volcar)
        if herramientas:
            texto += json.dumps(herramientas, ensure_ascii=False, default=_volcar)
        return max(1, int(len(texto) / 3.6))
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import AnthropicClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

extra = {"modo": "vivo", "perfiles": {"activos": a.tipos.split(",")}, "llm": {"cache_resultados": False}}
if a.hilos:
    extra["paralelismo"] = {"hilos_analistas": a.hilos}
if a.v6:
    extra["diseno"] = "v6"
CFG = cargar_config(extra=extra)


class SDK:
    def __init__(self, cont: int, usos: int, semilla: int) -> None:
        self.cont, self.usos, self.semilla = cont, usos, semilla
        self.n = 0
        self.vistos: set[str] = set()
        self.lock = threading.Lock()
        self.messages = self

    def create(self, **kw):
        if a.orden:
            nombre = threading.current_thread().name
            idx = int(nombre.rsplit("_", 1)[1]) if "ThreadPoolExecutor" in nombre else 0
            n = int(a.hilos or 1)
            time.sleep(0.02 * (idx if a.orden == "directo" else n - 1 - idx))
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        msgs, salida = kw["messages"], int(kw["max_tokens"])
        herr = kw.get("tools")
        total = int(tokens_de_peticion(kw["system"], msgs, herr) * a.factor)
        sys_tok = int(tokens_de_peticion(kw["system"], [], herr) * a.factor)
        lectura = escritura = 0
        if a.cache:
            clave = hashlib.sha256((kw["model"] + json.dumps(herr) + json.dumps(kw["system"])).encode()).hexdigest()
            with self.lock:
                if clave in self.vistos:
                    lectura = sys_tok
                else:
                    escritura = sys_tok
                    self.vistos.add(clave)
            entrada = total - sys_tok
        else:
            escritura, entrada = total, 0
        web = bool(herr)
        busq = self.usos if web else 0
        entrada += busq * a.lectura
        pausas = sum(1 for m in msgs if m["role"] == "assistant" and not isinstance(m["content"], str))
        propio = [m for m in msgs if m["role"] == "user"]
        largo = "análisis " * int(salida * 3.6 / 9)
        if web and pausas < self.cont:
            stop, texto = "pause_turn", largo
        elif len(propio) == 1:
            stop, texto = "end_turn", largo
        else:
            stop, texto = "end_turn", json.dumps(mock_respuestas.responder(agente, msgs[:1], self.semilla), ensure_ascii=False)
        with self.lock:
            self.n += 1
        uso = types.SimpleNamespace(input_tokens=entrada, output_tokens=salida, cache_creation_input_tokens=escritura,
                                    cache_read_input_tokens=lectura, server_tool_use=types.SimpleNamespace(web_search_requests=busq))
        return types.SimpleNamespace(stop_reason=stop, usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


def un_ciclo(k: int):
    cfg = copy.deepcopy(CFG)
    cont = int(cfg["llm"]["max_continuaciones_pause_turn"])
    sdk = SDK(cont, int(cfg["busqueda_web"]["max_usos_por_llamada"]), int(cfg["llm"]["semilla_mock"]))
    d = TMP / f"c{k}"
    b = Bloque(cfg, ProveedorCSV(EJ / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
               AnthropicClient(sdk=sdk, max_continuaciones=cont), d / "estado", d / "ent")
    capt = {}
    original = Bloque._validar_g3
    if "presupuesto" not in original.__code__.co_varnames:   # código anterior a T-146
        return b, b.ciclo(a.as_of, nivel_forzado="N2"), sdk, None

    def espia(self, paquete, extras, as_of, run_id, presupuesto=None):   # para leer la escala de la bolsa real
        capt["p"] = presupuesto
        return original(self, paquete, extras, as_of, run_id, presupuesto=presupuesto)
    Bloque._validar_g3 = espia
    try:
        r = b.ciclo(a.as_of, nivel_forzado="N2")
    finally:
        Bloque._validar_g3 = original
    return b, r, sdk, capt.get("p")


fallos = []
firmas = set()
for k in range(a.veces):
    b, r, sdk, p = un_ciclo(k)
    pu = CFG["presupuesto_uc"]
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    print(f"--- ciclo {k}: estado {r['estado']} · peticiones {sdk.n} · llamadas {len(b.contabilidad.llamadas)} · "
          f"cierres {len(run['cierres_parciales'])} · recortes {len(run.get('recortes_salida', []))} · "
          f"excesos {len(run.get('excesos_reserva', []))}")
    tot = 0.0
    for bolsa, v in sorted(r["presupuesto"].items()):
        lim = p.limite(bolsa) if p is not None else v["asignado"] * (1 + pu["ampliacion_sin_autorizacion"]) + v["ampliado"]
        mx = p.limite_maximo(bolsa) if p is not None else v["asignado"] * (1 + pu["ampliacion_max_autorizable"])
        tot += v["consumido"]
        pasa = v["consumido"] > lim + 1e-4 or lim > mx + 1e-4   # resumen redondea a 4 decimales
        if pasa:
            fallos.append(f"ciclo {k} {bolsa}: consumido {v['consumido']:.3f} límite {lim:.3f} máximo {mx:.3f}")
        print(f"  {bolsa:9} consumido {v['consumido']:8.3f} · límite {lim:8.3f} · máximo {mx:8.3f}" + ("  ← PASA" if pasa else ""))
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"])
    tope = pu["ciclo_semanal_max"] * (1 + pu["ampliacion_max_autorizable"])
    print(f"  suma {tot:.3f} · gastado {gastado:.3f} · tope del ciclo {tope:.1f}")
    if tot > tope + 1e-6:
        fallos.append(f"ciclo {k}: la suma {tot:.3f} pasa del tope {tope}")
    if abs(tot - gastado) > 0.01:
        fallos.append(f"ciclo {k}: gastado {gastado:.3f} ≠ cargado {tot:.3f}")
    for e in run.get("excesos_reserva", [])[:5]:
        print("  exceso", e)
    from collections import Counter
    print("  llamadas por agente", dict(sorted(Counter(x["agente"] for x in b.contabilidad.llamadas).items())),
          "· búsquedas", sum(x.get("busquedas_web", 0) for x in b.contabilidad.llamadas))
    firmas.add(json.dumps([run["presupuesto"], run["cierres_parciales"], run.get("recortes_salida"), run.get("excesos_reserva")],
                          sort_keys=True))
    print("  firma F5", hashlib.sha256(sorted(firmas)[-1].encode()).hexdigest()[:12] if len(firmas) == 1 else "varias")
    (TMP / f"firma_{a.orden or 'libre'}_{k}.json").write_text(
        json.dumps([run["presupuesto"], run["cierres_parciales"], run.get("recortes_salida"), run.get("excesos_reserva")],
                   sort_keys=True, ensure_ascii=False, indent=1), encoding="utf-8")
if a.veces > 1:
    print("determinismo:", "IGUAL" if len(firmas) == 1 else f"DISTINTO ({len(firmas)} firmas)")
print("VIOLACIONES:" if fallos else "sin violaciones de cotas")
for f in fallos:
    print("  ", f)
