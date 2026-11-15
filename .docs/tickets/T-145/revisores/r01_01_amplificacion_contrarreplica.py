"""QA r01 de T-145 · ¿el supuesto S4 («la salida de cada llamada anterior, copiada una vez») acota el encargo de la
respuesta a objeciones y de la contrarréplica? ¿Y la cota del ciclo, el coste total?

El cliente real (`llm.AnthropicClient`) con un SDK falso local (sin clave, sin red, sin coste). Las respuestas son las del
simulado, válidas frente a su esquema y de largo ≤ `max_tokens` (con el margen del tokenizador: como mucho
`max_tokens · 3,6 / factor_tokens_cota` caracteres), salvo tres, que un modelo real podría dar:
 · el Analista, en el cribado, escribe en cada finalista K afirmaciones largas con fuentes propias (en modo vivo, cualquier
   fuente vale como evidencia citable);
 · el Contradictor, en la refutación, da N objeciones fuertes (cortas) repartidas entre las finalistas;
 · el Analista, en la respuesta, da por resueltas todas y cita sus K fuentes en cada una.
La contrarréplica (`orquestacion._refutacion`) copia el contenido de cada evidencia citada en cada objeción: el encargo
crece con N·K·L, no con la suma de las salidas. El presupuesto en UC de la bolsa del tipo lo para antes de la llamada
(estimación con el encargo real): se barre N para ver qué pasa justo por debajo.
Cada petición se cobra como la API: el prompt de sistema como escritura de caché la primera vez por modelo y agente y como
lectura después, el resto como entrada (`--modo cota`: toda la entrada como escritura, como S2); la entrada con el margen
`factor_tokens_cota`; la salida, `max_tokens` (con `--salida real`, lo escrito con el margen). Con `--reparar`, el primer intento de cada llamada no es JSON.

Uso (desde bloque_a/11_Ejecutor):
  python -I <este script> <carpeta temporal> <carpeta de medir_consumo_a> [--config yaml] [--n 40,80,...] [--k 2]
         [--modo realista|cota] [--reparar | --reparar-papel P] [--salida max|real]
"""
import argparse
import collections
import contextlib
import copy
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
from bloque_a.prompts import extraer_encargo  # noqa: E402

spec = importlib.util.spec_from_file_location("est", RAIZ / ".docs" / "scripts" / "estimar_coste_ciclo_a.py")
est = importlib.util.module_from_spec(spec)
spec.loader.exec_module(est)

ap = argparse.ArgumentParser()
ap.add_argument("tmp")
ap.add_argument("medida")
ap.add_argument("--config", default=None)
ap.add_argument("--n", default="20,60,120,240")
ap.add_argument("--k", type=int, default=2)
ap.add_argument("--modo", default="realista", choices=["realista", "cota"])
ap.add_argument("--reparar", action="store_true")
ap.add_argument("--reparar-papel", default=None, help="solo ese papel falla el primer intento (p. ej. contrarreplica)")
ap.add_argument("--salida", default="max", choices=["max", "real"], help="max: cada respuesta cobra max_tokens; real: lo escrito")
A = ap.parse_args()

cfg = est._config(A.config)
tarifa = yaml.safe_load((RAIZ / "bloque_a" / "11_Ejecutor" / "config" / "precios_anthropic.yaml").read_text(encoding="utf-8"))
P, PB, F = tarifa["precios_por_millon"], float(tarifa["precio_busqueda_web_por_mil"]), float(tarifa["factor_tokens_cota"])
CONT = int(cfg["llm"]["max_continuaciones_pause_turn"])
MU = int(cfg["busqueda_web"]["max_usos_por_llamada"])
SEMILLA = int(cfg["llm"]["semilla_mock"])


def _tok(x) -> int:
    return max(1, int(len(x) / 3.6))


def _cabe(obj, max_tokens) -> bool:
    return len(json.dumps(obj, ensure_ascii=False)) <= max_tokens * 3.6 / F


def _papel(agente, msg):
    if "contrarreplicas" in msg:
        return "contrarreplica"
    if msg.get("fase") == "RESPUESTA_OBJECIONES":
        return "respuesta_objeciones"
    if msg.get("fase") in ("CRIBADO_E_INVESTIGACION", "REVISION_VIGENTES"):
        return "cribado"
    if "peticiones" in msg and agente == "AG-11":
        return "refutacion"
    return {"AG-10": "prospectiva", "AG-12": "curacion", "AG-14": "peticion", "AG-16": "peticion", "AG-02": "integracion",
            "AG-17": "redaccion", "AG-18": "dictamen_g3", "AG-19": "auditoria", "AG-20": "aprendizaje"}.get(agente, agente)


class Escenario:
    def __init__(self, n_obj, k):
        self.n_obj, self.k = n_obj, k
        self.peticiones: list[dict] = []
        self.vistos: set = set()

    # ---------------------------------------------------------------- respuestas amplificadas, válidas y ≤ max_tokens
    def cribado(self, d, max_tokens):
        fins = d.get("finalistas") or []
        if not fins:
            return d
        base = copy.deepcopy(d)
        for f in base["finalistas"]:
            f["afirmaciones"] = [{"afirmacion": "x", "fuente": f"F{i}", "direccion": "favorable"} for i in range(self.k)]
        largo = 1
        while True:   # el mayor L que cabe
            prueba = copy.deepcopy(base)
            for f in prueba["finalistas"]:
                for a in f["afirmaciones"]:
                    a["afirmacion"] = "dato " * (largo * 2)
            if not _cabe(prueba, max_tokens):
                break
            mejor, largo = prueba, largo * 2
        lo, hi = largo // 2, largo
        while hi - lo > 1:
            m = (lo + hi) // 2
            prueba = copy.deepcopy(base)
            for f in prueba["finalistas"]:
                for a in f["afirmaciones"]:
                    a["afirmacion"] = "dato " * (m * 2)
            if _cabe(prueba, max_tokens):
                mejor, lo = prueba, m
            else:
                hi = m
        return mejor

    def refutacion(self, d, msg, max_tokens):
        refs = [p["ref"] for p in msg.get("peticiones", [])]
        if not refs:
            return d
        out = {"resultados": [], "autoevaluacion": "r"}
        por = [self.n_obj // len(refs) + (1 if i < self.n_obj % len(refs) else 0) for i in range(len(refs))]
        for r, n in zip(refs, por):
            out["resultados"].append({"ref": r, "veredicto_global": "tesis frágil", "objeciones": [
                {"id": f"o{j}", "tipo": "t", "fuerza": "fuerte", "argumento": "a", "que_la_resolveria": "q"} for j in range(n)]})
        if not _cabe(out, max_tokens):
            raise SystemExit(f"N={self.n_obj} no cabe en la salida del Contradictor")
        return out

    def respuesta(self, msg, max_tokens):
        out = {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "r", "resuelta": True,
                               "evidencia_citada": [f"F{i}" for i in range(self.k)]} for o in msg.get("objeciones", [])]}
        if not _cabe(out, max_tokens):
            raise SystemExit(f"N={self.n_obj}, K={self.k} no cabe en la salida del Analista")
        return out

    # ---------------------------------------------------------------- SDK falso
    def create(self, **kw):
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        msgs = kw["messages"]
        salida = int(kw["max_tokens"])
        sys_t = _tok("".join(b.get("text", "") for b in kw["system"])) * F
        primero = msgs[0]["content"] if isinstance(msgs[0]["content"], str) else ""
        msg = extraer_encargo(primero)["mensaje"] if primero else {}
        papel = _papel(agente, msg)
        def _texto(c):
            return c if isinstance(c, str) else "".join(getattr(b, "text", "") for b in c)
        reenviado = sum(salida if A.salida == "max" else min(salida, int(_tok(_texto(m["content"])) * F) + 1)
                        for m in msgs if m["role"] == "assistant")
        propio = _tok(json.dumps([m for m in msgs if m["role"] == "user"], ensure_ascii=False)) * F
        con_web = bool(kw.get("tools"))
        pausas = sum(1 for m in msgs if m["role"] == "assistant" and isinstance(m["content"], list))
        intento = sum(1 for m in msgs if m["role"] == "user")
        clave = (kw["model"], agente)
        if A.modo == "cota":
            escr, lect, ent = sys_t + propio + reenviado, 0, 0
        elif clave in self.vistos:
            escr, lect, ent = 0, sys_t, propio + reenviado
        else:
            escr, lect, ent = sys_t, 0, propio + reenviado
        self.vistos.add(clave)
        if con_web and pausas < CONT:
            stop, texto = "pause_turn", "busco " * int(salida * 3.6 / 6 / F)
        elif (A.reparar or A.reparar_papel == papel) and intento == 1:
            stop, texto = "end_turn", "texto " * int(salida * 3.6 / 6 / F)
        else:
            stop = "end_turn"
            d = mock_respuestas.responder(agente, msgs[:1], SEMILLA)
            if papel == "cribado" and agente not in ("AG-10", "AG-11"):
                d = self.cribado(d, salida)
            elif papel == "refutacion":
                d = self.refutacion(d, msg, salida)
            elif papel == "respuesta_objeciones":
                d = self.respuesta(msg, salida)
            texto = json.dumps(d, ensure_ascii=False)
        if A.salida == "real":
            salida = min(salida, int(_tok(texto) * F) + 1)
        p = P[kw["model"]]
        usd = est._coste(p, ent, salida, escr, lect) + (MU * PB / 1000 if con_web else 0)
        usd_s2 = est._coste(p, 0, salida, escr + lect + ent, 0) + (MU * PB / 1000 if con_web else 0)
        self.peticiones.append({"agente": agente, "papel": papel, "intento": intento, "entrada": escr + lect + ent,
                                "encargo": propio / F, "usd": usd, "usd_s2": usd_s2})
        uso = types.SimpleNamespace(input_tokens=int(ent), output_tokens=salida, cache_creation_input_tokens=int(escr),
                                    cache_read_input_tokens=int(lect),
                                    server_tool_use=types.SimpleNamespace(web_search_requests=MU if con_web else 0))
        return types.SimpleNamespace(stop_reason=stop, usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


llamadas = json.loads((Path(A.medida) / "llamadas.json").read_text(encoding="utf-8"))
cota = est.cota_ciclo(llamadas, cfg, P, PB, F)
s4 = {}
for x in cota["papeles"]:
    s4[x["papel"]] = max(s4.get(x["papel"], 0), x["encargo_tok"])
print(f"cota del ciclo {cota['cota']:.2f} USD (por llamadas {cota['cota_llamadas']:.2f}); encargo S4 de la contrarréplica "
      f"{s4['contrarreplica']} tok y de la respuesta {s4['respuesta_objeciones']} tok (sin el margen {F})")
print(f"modo {A.modo}, reparación {'sí' if A.reparar else 'no'}, K={A.k}")
for n in [int(x) for x in A.n.split(",")]:
    esc = Escenario(n, A.k)
    sdk = types.SimpleNamespace(messages=esc)
    llm.crear_cliente = lambda tipo, c, replay=None, replay_modo="reproducir": llm.AnthropicClient(
        sdk=sdk, max_continuaciones=int(c["llm"]["max_continuaciones_pause_turn"]), salida_estructurada=False)
    S = Path(A.tmp) / f"n{n}"
    shutil.rmtree(S, ignore_errors=True)
    S.mkdir(parents=True)
    extra = ["--config", A.config] if A.config else []
    with contextlib.redirect_stdout(io.StringIO()):
        cli.main(["--cliente", "anthropic", "--datos", "ejemplos/datos_sinteticos", "--estado", str(S / "estado"), "--salida",
                  str(S / "salida"), "--as-of", "2024-03-29"] + extra + ["ciclo"])
    tot, tot_s2 = sum(x["usd"] for x in esc.peticiones), sum(x["usd_s2"] for x in esc.peticiones)
    por = collections.Counter(x["papel"] for x in esc.peticiones if x["intento"] == 1 and not x.get("cont"))
    enc = collections.defaultdict(float)
    for x in esc.peticiones:
        enc[x["papel"]] = max(enc[x["papel"]], x["encargo"])
    cortes = sum(json.dumps(json.loads(l), ensure_ascii=False).count("presupuesto insuficiente")
                 for f in (S / "estado").rglob("*.jsonl") for l in f.read_text(encoding="utf-8").splitlines() if l.strip())
    print(f"N={n:4}: coste {tot:6.2f} USD (al precio de S2 {tot_s2:6.2f}) · cota {cota['cota']:.2f} · encargo de la "
          f"contrarréplica {enc.get('contrarreplica', 0):9.0f} tok (S4 {s4['contrarreplica']}) · respuesta "
          f"{enc.get('respuesta_objeciones', 0):8.0f} (S4 {s4['respuesta_objeciones']}) · cortes por presupuesto {cortes} · "
          f"peticiones por papel {dict(sorted(por.items()))}")
    S4N = {"peticion": "peticion_conocimiento", "aprendizaje": "informe_aprendizaje"}
    print("         encargo medido / S4 por papel: " + ", ".join(
        f"{q} {v:.0f}/{s4.get(S4N.get(q, q), 0)}" for q, v in sorted(enc.items())))
    for papel in ("contrarreplica", "respuesta_objeciones"):
        u = sum(x["usd"] for x in esc.peticiones if x["papel"] == papel)
        c = sum(x["usd"] for x in cota["papeles"] if x["papel"] == papel)
        print(f"         {papel}: {u:.2f} USD (la cota le da {c:.2f})")
