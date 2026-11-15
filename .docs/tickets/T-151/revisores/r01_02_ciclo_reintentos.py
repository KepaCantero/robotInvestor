"""QA r01 de T-151 · ciclos completos con un SDK doble que falla (timeout, 503, 529, 500) en peticiones fijadas por su
contenido, con hilos, caché por prefijo y orden de hilos forzado (sin red, sin clave, sin coste).

Uso: python -I r01_02_ciclo_reintentos.py <ruta a 11_Ejecutor> <carpeta temporal> [opciones]
  --tipos RV,RF,DIV,MP   tipos activos (por defecto DIV)
  --hilos N              hilos de los Analistas
  --cache                el SDK simula la caché por prefijo (la primera petición con un `system` lo escribe; las demás lo leen;
                         un timeout que el servidor completó también lo escribe)
  --orden directo|inverso  retardo por hilo para forzar qué hilo llega antes
  --veces N              ciclos seguidos (compara la firma de F5, con `peticiones_sin_respuesta`)
  --sin-tipos            alcance con un tipo no activo: solo corre AG-20 (H-12); su primera petición no responde
  --fallo-escribe cobrables|ninguno  con --cache, si una petición que falla con timeout o 5xx distinto de 529 escribe el
                         prefijo en la caché del servidor (lo completó) o no; un 529 no lo escribe nunca (por defecto cobrables)

Qué comprueba (VIOLA si no):
  - cada fallo de la lista lo ve el RUN de F5: timeout, 503 y 500 en `peticiones_sin_respuesta`; 529 no;
  - cada petición HTTP del SDK doble tuvo su reserva (peticiones del SDK = reservas hechas por las `ReservaLlamada`);
  - ninguna reserva colgada al acabar (`reservado` 0 en todas las bolsas de todos los `Presupuesto` creados);
  - sin caché: lo consumido = lo de la contabilidad + lo cargado sin respuesta (ningún cobro doble ni perdido);
  - ninguna bolsa pasa de su límite;
  - con --veces > 1: la firma de F5 (presupuesto, cierres, recortes, excesos y peticiones sin respuesta) no cambia.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
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
ap.add_argument("--cache", action="store_true")
ap.add_argument("--orden", choices=["directo", "inverso"])
ap.add_argument("--veces", type=int, default=1)
ap.add_argument("--sin-tipos", action="store_true")
ap.add_argument("--fallo-escribe", choices=["cobrables", "ninguno"], default="cobrables")
a = ap.parse_args()
EJ, TMP = Path(a.ej).resolve(), Path(a.tmp).resolve()
sys.path.insert(0, str(EJ))
import anthropic  # noqa: E402
import httpx2  # noqa: E402
from bloque_a import consumo, mock_respuestas, orquestacion  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.consumo import tokens_de_peticion  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import AnthropicClient, ReglaReintentos  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

extra = {"modo": "vivo", "perfiles": {"activos": a.tipos.split(",")}, "llm": {"cache_resultados": False}}
if a.hilos:
    extra["paralelismo"] = {"hilos_analistas": a.hilos}
CFG = cargar_config(extra=extra)
REQ = httpx2.Request("POST", "https://api.invalid/v1/messages")

CREADOS: list = []
RESERVAS = [0]
_lock = threading.Lock()


class PresupuestoEspia(consumo.Presupuesto):
    def __init__(self, *x, **k):
        super().__init__(*x, **k)
        CREADOS.append(self)


class ReservaEspia(consumo.ReservaLlamada):
    def _abrir(self, w, bruto, mt):
        with _lock:
            RESERVAS[0] += 1
        return super()._abrir(w, bruto, mt)


orquestacion.Presupuesto = PresupuestoEspia
orquestacion.ReservaLlamada = ReservaEspia


def _error(estado: int):
    resp = httpx2.Response(estado, request=REQ)
    return anthropic.Anthropic(api_key="clave-falsa-qa")._make_status_error("fallo de prueba", body=None, response=resp)


class SDK:
    """Responde como el simulado. Por cada petición (agente + mensajes) lleva la cuenta de intentos y falla según su huella:
    huella % 4 == 0: timeout, luego 529, luego responde; % 4 == 1: 503 y responde; % 4 == 2 y AG-20: 500 hasta agotar."""

    def __init__(self, semilla: int):
        self.semilla, self.messages = semilla, self
        self.n = 0
        self.intentos: dict[str, int] = {}
        self.fallos: list[tuple[str, int, str]] = []
        self.vistos: set[str] = set()
        self.lock = threading.Lock()

    def plan(self, agente: str, huella: int, intento: int):
        if a.sin_tipos:
            return "timeout" if (agente == "AG-20" and intento == 1) else None
        r = huella % 4
        if r == 0:
            return {1: "timeout", 2: 529}.get(intento)
        if r == 1:
            return {1: 503}.get(intento)
        if r == 2 and agente == "AG-20":
            return 500
        return None

    def create(self, **kw):
        if a.orden:
            nombre = threading.current_thread().name
            idx = int(nombre.rsplit("_", 1)[1]) if "ThreadPoolExecutor" in nombre else 0
            time.sleep(0.02 * (idx if a.orden == "directo" else int(a.hilos or 1) - 1 - idx))
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        msgs, herr = kw["messages"], kw.get("tools")
        clave = hashlib.sha256((agente + json.dumps(msgs, sort_keys=True, default=str)).encode()).hexdigest()
        with self.lock:
            self.n += 1
            self.intentos[clave] = self.intentos.get(clave, 0) + 1
            intento = self.intentos[clave]
        total = int(tokens_de_peticion(kw["system"], msgs, herr) * 1.35)
        sys_tok = int(tokens_de_peticion(kw["system"], [], herr) * 1.35)
        lectura = escritura = 0
        pref = hashlib.sha256((kw["model"] + json.dumps(herr) + json.dumps(kw["system"])).encode()).hexdigest()
        fallo = self.plan(agente, int(clave[:8], 16), intento)
        escribe = fallo is None or (a.fallo_escribe == "cobrables" and fallo != 529)
        if a.cache:
            with self.lock:
                if pref in self.vistos:
                    lectura = sys_tok
                else:
                    escritura = sys_tok
                    if escribe:
                        self.vistos.add(pref)
            entrada = total - sys_tok
        else:
            escritura, entrada = total, 0
        if fallo is not None:
            with self.lock:
                self.fallos.append((agente, intento, str(fallo)))
            if fallo == "timeout":
                raise anthropic.APITimeoutError(request=REQ)
            raise _error(fallo)
        texto = json.dumps(mock_respuestas.responder(agente, msgs[:1], self.semilla), ensure_ascii=False)
        uso = types.SimpleNamespace(input_tokens=entrada, output_tokens=min(800, int(kw["max_tokens"])),
                                    cache_creation_input_tokens=escritura, cache_read_input_tokens=lectura, server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


def un_ciclo(k: int):
    cfg = copy.deepcopy(CFG)
    sdk = SDK(int(cfg["llm"]["semilla_mock"]))
    d = TMP / f"c{k}"
    shutil.rmtree(d, ignore_errors=True)   # estado limpio: cada ciclo parte de cero
    esperas: list[float] = []
    cli = AnthropicClient(sdk=sdk, reintentos=ReglaReintentos.de_config(cfg), dormir=esperas.append)
    b = Bloque(cfg, ProveedorCSV(EJ / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli,
               d / "estado", d / "ent")
    if a.sin_tipos:
        b.evaluador.ciclo = lambda as_of, run_id: {
            "resueltos": 3, "metricas": {"RV|H2": {"n": 3, "brier": 0.2, "brier_ref": 0.25, "acierto": {"tasa": 0.66},
                                                   "calibracion_global": None}},
            "certificados": {"emitidos": [], "insuficientes": []}, "lecciones_nuevas": []}
        r = b.ciclo("2024-03-29", alcance={"clases": ["RF"]})
    else:
        r = b.ciclo("2024-03-29", nivel_forzado="N2")
    return b, r, sdk, esperas


fallos_qa: list[str] = []
firmas = set()
pu = CFG["presupuesto_uc"]
if a.sin_tipos and "RF" in CFG["perfiles"]["activos"]:
    sys.exit("--sin-tipos necesita que RF no esté en --tipos")
for k in range(a.veces):
    CREADOS.clear()
    RESERVAS[0] = 0
    b, r, sdk, esperas = un_ciclo(k)
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    sin = run.get("peticiones_sin_respuesta", [])
    esperados = [f for f in sdk.fallos if f[2] in ("timeout", "503", "500")]
    print(f"--- ciclo {k}: estado {r['estado']} · peticiones del SDK {sdk.n} · reservas {RESERVAS[0]} · fallos "
          f"{len(sdk.fallos)} (timeout {sum(f[2] == 'timeout' for f in sdk.fallos)}, 503 {sum(f[2] == '503' for f in sdk.fallos)}, "
          f"529 {sum(f[2] == '529' for f in sdk.fallos)}, 500 {sum(f[2] == '500' for f in sdk.fallos)}) · sin respuesta en F5 "
          f"{len(sin)} · esperas {len(esperas)} · cierres {len(run.get('cierres_parciales', []))}")
    print("  fallos del SDK:", [(ag, i, f) for ag, i, f in sdk.fallos])
    print("  sin respuesta en F5:", [(s["clase"], s["agente"], s["peticion"], s["motivo"]) for s in sin])
    # Lo de después de escribir F5 (la auditoría, AG-19) no puede estar en F5: se cuenta aparte
    tras_f5 = [f for f in esperados if f[0] == "AG-19"]
    if tras_f5:
        print(f"  OBS: {len(tras_f5)} fallo(s) de AG-19 (corre después de escribir F5): cargados en la bolsa, no declarados en F5")
    if len(sin) != len(esperados) - len(tras_f5):
        fallos_qa.append(f"ciclo {k}: F5 tiene {len(sin)} peticiones sin respuesta y el SDK dio {len(esperados)} fallos que pudieron cobrarse")
    if sdk.n != RESERVAS[0]:
        fallos_qa.append(f"ciclo {k}: {sdk.n} peticiones al SDK y {RESERVAS[0]} reservas")
    colgado = [(i, kk, v) for i, p in enumerate(CREADOS) for kk, v in p.reservado.items() if abs(v) > 1e-6]
    if colgado:
        fallos_qa.append(f"ciclo {k}: reservas colgadas {colgado}")
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"])
    tot = sum(v["consumido"] for v in r["presupuesto"].values())
    cargado_sin = sum(s["reservado_uc"] for s in sin)
    # el presupuesto del ciclo (el que absorbió el de C5) lleva también lo de AG-19, que corre después de escribir F5
    principal = max(CREADOS, key=lambda p: len(p.sin_respuesta))
    cargado_total = sum(s["reservado_uc"] for s in principal.sin_respuesta)
    print(f"  consumido {tot:.4f} · contabilidad {gastado:.4f} · sin respuesta {cargado_sin:.4f} en F5, {cargado_total:.4f} en total · presupuestos creados "
          f"{len(CREADOS)} · reservado al final {sum(sum(p.reservado.values()) for p in CREADOS):.6f}")
    if not a.cache and abs(tot - (gastado + cargado_total)) > 0.01:
        fallos_qa.append(f"ciclo {k}: consumido {tot:.4f} ≠ contabilidad {gastado:.4f} + sin respuesta {cargado_total:.4f}")
    for bolsa, v in sorted(r["presupuesto"].items()):
        lim = v["asignado"] * (1 + pu["ampliacion_sin_autorizacion"]) + v["ampliado"]
        if v["consumido"] > lim + 1e-4:
            fallos_qa.append(f"ciclo {k} {bolsa}: consumido {v['consumido']:.3f} pasa del límite {lim:.3f}")
    if a.sin_tipos:
        en_run = run.get("presupuesto") or {}
        print(f"  RUN sin análisis: presupuesto en F5 {en_run}; resultado {r.get('presupuesto')}; cierres {run.get('cierres_parciales')}")
        if not en_run or en_run != r.get("presupuesto") or abs(sum(v['consumido'] for v in en_run.values()) - (gastado + cargado_sin)) > 1e-3:
            fallos_qa.append(f"ciclo {k}: el RUN sin análisis no lleva lo de AG-20 (con lo sin respuesta) en F5")
    motivos = sorted({c["motivo"] for c in run.get("cierres_parciales", [])})
    for m in motivos[:4]:
        print("  cierre:", m)
    firma = json.dumps([run.get("presupuesto"), run.get("cierres_parciales"), run.get("recortes_salida"), run.get("excesos_reserva"),
                        sin], sort_keys=True)
    firmas.add(firma)
    print("  firma F5", hashlib.sha256(firma.encode()).hexdigest()[:12])
    (TMP / f"firma_{a.orden or 'libre'}_{k}.json").write_text(firma, encoding="utf-8")
if a.veces > 1:
    print("determinismo:", "IGUAL" if len(firmas) == 1 else f"DISTINTO ({len(firmas)} firmas)")
print("VIOLA:" if fallos_qa else "OK: sin violaciones")
for f in fallos_qa:
    print("  ", f)
sys.exit(1 if fallos_qa else 0)
