"""QA r01 de T-154 · H-02 en ciclos completos: lo que deja AG-19 en F5 (`PRESUPUESTO_F9`) con un SDK doble que falla en la
auditoría de varias formas (sin red, sin clave, sin coste).

Uso: python -I r01_02_ciclo_f9.py <ruta a 11_Ejecutor> <carpeta temporal>

Escenarios (DIV, N2, 29-03-2024; cada uno en un estado limpio salvo «dos»):
  ninguno   AG-19 responde: sin entrada F9 (referencia del RUN)
  timeout   AG-19: timeout y responde: F9 con una petición sin respuesta
  501       AG-19: 501 (no se reintenta, pudo cobrarse, H-01): F9 con una, la auditoría sin respuesta
  529       AG-19: 529 y responde: sin F9 (se soltó)
  529x      AG-19: 529 siempre: sin F9 (nada que declarar; la auditoría sin respuesta)
  exceso    AG-19 cobra 40 veces la entrada estimada: F9 con `excesos_reserva`
  mixto     AG-05 timeout (antes del RUN) y AG-19 timeout: el RUN lleva AG-05 y la F9 solo AG-19
  cierre    AG-17 (redacción, COMÚN) cobra 400 veces su entrada: COMÚN se agota y AG-19 no cabe: F9 solo con el cierre de AG-19
  dos       dos ciclos seguidos en el mismo estado (22-03 y 29-03) con AG-19 timeout: dos F9 con id propio y su run_id
Qué comprueba (FALLA si no): el RUN de F5 de cada escenario es idéntico al de «ninguno» (sin _hash, _hash_prev, _ts,
fecha_entrega, id y run_id) salvo `peticiones_sin_respuesta` de lo que falla antes del RUN; la F9 aparece solo cuando toca y
declara solo lo de AG-19; su `presupuesto` = el del resultado; lo declarado en F5 (RUN + F9) = todas las peticiones del SDK
que pudieron cobrarse; ninguna reserva colgada; `verificar_integridad()` en verde; los lectores de F5 (`estado` por id,
el RUN anterior del segundo ciclo y una consulta C3 después) siguen funcionando.
"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import types
from pathlib import Path

EJ, TMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(EJ))
import anthropic  # noqa: E402
import httpx2  # noqa: E402
from bloque_a import consumo, mock_respuestas, orquestacion  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.consumo import tokens_de_peticion  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import AnthropicClient, ReglaReintentos  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

CFG = cargar_config(extra={"modo": "vivo", "perfiles": {"activos": ["DIV"]}, "llm": {"cache_resultados": False}})
REQ = httpx2.Request("POST", "https://api.invalid/v1/messages")
FALLOS: list[str] = []
CREADOS: list = []


class PresupuestoEspia(consumo.Presupuesto):
    def __init__(self, *x, **k):
        super().__init__(*x, **k)
        CREADOS.append(self)


orquestacion.Presupuesto = PresupuestoEspia


def check(nombre, ok, detalle=""):
    print(("OK   " if ok else "FALLA") + f" {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def _error(n):
    return anthropic.Anthropic(api_key="clave-falsa-qa")._make_status_error("fallo de prueba", body=None,
                                                                            response=httpx2.Response(n, request=REQ))


class SDK:
    def __init__(self, semilla, planes):
        self.semilla, self.messages, self.planes = semilla, self, planes   # agente -> lista de pasos (None = responde)
        self.intentos: dict[str, int] = {}
        self.cobrables: list[str] = []

    def create(self, **kw):
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        i = self.intentos[agente] = self.intentos.get(agente, 0) + 1
        plan = self.planes.get(agente, [])
        paso = plan[min(i, len(plan)) - 1] if plan else None
        if paso == "timeout":
            self.cobrables.append(agente)
            raise anthropic.APITimeoutError(request=REQ)
        if isinstance(paso, int):
            if paso not in (429, 529):
                self.cobrables.append(agente)
            raise _error(paso)
        ent = int(tokens_de_peticion(kw["system"], kw["messages"], kw.get("tools")) * (int(paso[6:] or 40) if isinstance(paso, str) and paso.startswith("exceso") else 1.2))
        texto = json.dumps(mock_respuestas.responder(agente, kw["messages"][:1], self.semilla), ensure_ascii=False)
        uso = types.SimpleNamespace(input_tokens=ent, output_tokens=min(600, int(kw["max_tokens"])), cache_creation_input_tokens=0,
                                    cache_read_input_tokens=0, server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


def montar(nombre, planes, limpio=True):
    cfg = copy.deepcopy(CFG)
    d = TMP / nombre
    if limpio:
        shutil.rmtree(d, ignore_errors=True)
    sdk = SDK(int(cfg["llm"]["semilla_mock"]), planes)
    cli = AnthropicClient(sdk=sdk, reintentos=ReglaReintentos.de_config(cfg), dormir=lambda s: None)
    b = Bloque(cfg, ProveedorCSV(EJ / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli,
               d / "estado", d / "ent")
    return b, sdk


ESCENARIOS = ("ninguno", "timeout", "501", "529x", "529", "exceso", "mixto", "cierre", "dos")
IGNORA = {"_hash", "_hash_prev", "_ts", "fecha_entrega", "id", "run_id", "peticiones_sin_respuesta"}


def run_de(b, r):
    return b.almacen.estado("F5", clave="id")[r["run_id"]]


def limpio(run):
    """Sin los campos que cambian siempre; las rutas de los entregables, sin la carpeta del escenario."""
    texto = json.dumps({k: v for k, v in run.items() if k not in IGNORA}, sort_keys=True, default=str)
    for n in ESCENARIOS:
        texto = texto.replace(f"/{n}/ent/", "/ESCENARIO/ent/")
    return json.loads(texto)


def f9s(b):
    return [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "PRESUPUESTO_F9"]


def comun(b, r, sdk, nombre, f9_esperadas, ag19_en_f9):
    run = run_de(b, r)
    f9 = [e for e in f9s(b) if e["run_id"] == r["run_id"]]
    sin_run = [s["agente"] for s in run.get("peticiones_sin_respuesta", [])]
    sin_f9 = [s["agente"] for e in f9 for s in e.get("peticiones_sin_respuesta", [])]
    check(f"{nombre}: entradas F9", len(f9) == f9_esperadas, f"{len(f9)} (esperadas {f9_esperadas})")
    check(f"{nombre}: el RUN no declara a AG-19 y la F9 solo a AG-19", "AG-19" not in sin_run and all(a == "AG-19" for a in sin_f9)
          and (sin_f9.count("AG-19") == ag19_en_f9), f"RUN {sin_run} · F9 {sin_f9}")
    check(f"{nombre}: lo declarado en F5 = lo cobrable del SDK", sorted(sin_run + sin_f9) == sorted(sdk.cobrables),
          f"F5 {sorted(sin_run + sin_f9)} · SDK {sorted(sdk.cobrables)}")
    if f9:
        check(f"{nombre}: el presupuesto de la F9 es el del resultado", f9[-1]["presupuesto"] == r["presupuesto"])
        check(f"{nombre}: la F9 lleva su id propio y fase F9", all(e["id"].startswith("F5F9-") and e["fase"] == "F9" and e["id"] != r["run_id"]
                                                                  for e in f9))
    colg = [(k, v) for p in CREADOS for k, v in p.reservado.items() if abs(v) > 1e-6]
    check(f"{nombre}: sin reservas colgadas", not colg, f"{colg}")
    integ = b.almacen.verificar_integridad()
    check(f"{nombre}: verificar_integridad", all(integ.values()), f"{ {k: v for k, v in integ.items() if not v} }")
    return run, f9


# referencia
CREADOS.clear()
b, sdk = montar("ninguno", {})
r = b.ciclo("2024-03-29", nivel_forzado="N2")
ref, _ = comun(b, r, sdk, "ninguno", 0, 0)
print(f"     referencia: RUN {r['run_id']} estado {r['estado']}")

ESC = {"timeout": ({"AG-19": ["timeout", None]}, 1, 1), "501": ({"AG-19": [501]}, 1, 1), "529": ({"AG-19": [529, None]}, 0, 0),
       "529x": ({"AG-19": [529]}, 0, 0), "exceso": ({"AG-19": ["exceso"]}, 1, 0),
       "mixto": ({"AG-05": ["timeout", None], "AG-19": ["timeout", None]}, 1, 1),
       "cierre": ({"AG-17": ["exceso400", None]}, 1, 0)}
for nombre, (planes, n_f9, n_ag19) in ESC.items():
    CREADOS.clear()
    b, sdk = montar(nombre, planes)
    r = b.ciclo("2024-03-29", nivel_forzado="N2")
    run, f9 = comun(b, r, sdk, nombre, n_f9, n_ag19)
    diff = sorted(k for k in set(limpio(run)) | set(limpio(ref)) if limpio(run).get(k) != limpio(ref).get(k))
    check(f"{nombre}: el RUN de F5 es el de la referencia", not diff or (nombre in ("mixto", "cierre")), f"campos distintos {diff}")
    if nombre in ("mixto", "cierre"):
        print(f"     {nombre}: campos del RUN que cambian por lo de antes del RUN: {diff}")
    if nombre == "exceso":
        check("exceso: la F9 declara el exceso de AG-19", bool(f9) and any(x["agente"] == "AG-19" for x in f9[0].get("excesos_reserva", [])),
              f"{f9[0].get('excesos_reserva') if f9 else None}")
    if nombre == "cierre":
        print(f"     cierre: COMÚN {r['presupuesto'].get('COMUN')}")
        cie = [c for e in f9 for c in e.get("cierres_parciales", [])]
        print(f"     cierre: cierres en el RUN {len(run.get('cierres_parciales', []))} · en la F9 {[c['motivo'][:60] for c in cie]}")
        check("cierre: la F9 declara solo el cierre de AG-19 (el exceso de AG-17 está en el RUN)",
              bool(cie) and all("AG-19" in c["motivo"] for c in cie) and not any(e.get("excesos_reserva") for e in f9)
              and any(x["agente"] == "AG-17" for x in run.get("excesos_reserva", [])))
    if nombre in ("501", "529x"):
        aud = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUD" and e.get("objeto") == r["run_id"]]
        check(f"{nombre}: la auditoría queda sin respuesta declarada en HA", bool(aud) and aud[-1]["resumen"] == "auditor no disponible")

# dos ciclos seguidos en el mismo estado
CREADOS.clear()
b, sdk = montar("dos", {"AG-19": ["timeout", None]})
r1 = b.ciclo("2024-03-22", nivel_forzado="N2")
sdk.intentos.clear()
r2 = b.ciclo("2024-03-29", nivel_forzado="N2")
todas = f9s(b)
ids = [e["id"] for e in todas]
check("dos: dos F9 con id propio y el run_id de cada ciclo", len(todas) == 2 and len(set(ids)) == 2
      and [e["run_id"] for e in todas] == [r1["run_id"], r2["run_id"]], f"{[(e['id'], e['run_id']) for e in todas]}")
check("dos: estado(F5) por id sigue dando los RUN", run_de(b, r1)["tipo_entrada"] == "RUN" and run_de(b, r2)["tipo_entrada"] == "RUN")
check("dos: verificar_integridad", all(b.almacen.verificar_integridad().values()))
try:
    q = b.consulta("¿Qué pasó con la auditoría del último ciclo?", as_of="2024-03-29")
    check("dos: una consulta C3 después funciona", isinstance(q, dict), f"ruta {q.get('ruta') if isinstance(q, dict) else q}")
except Exception as e:  # noqa: BLE001
    check("dos: una consulta C3 después funciona", False, repr(e))
firma = hashlib.sha256(json.dumps([limpio(run_de(b, r2)), [{k: v for k, v in e.items() if not k.startswith("_")} for e in todas]],
                                  sort_keys=True, default=str).encode()).hexdigest()[:12]
print(f"     firma «dos» {firma}")
print("RESULTADO:", "FALLA " + ", ".join(FALLOS) if FALLOS else "todo OK")
sys.exit(1 if FALLOS else 0)
