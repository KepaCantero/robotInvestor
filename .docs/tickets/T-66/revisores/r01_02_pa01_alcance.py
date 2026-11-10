"""T-66 · QA r01 · PA-01 y H-06: tipos no activos en CT-01, profundización y CT-03; CT-04 de clases activas seguido de un
ciclo; estado F10 anterior; configuración del llamador; backtest de un tipo no activo; determinismo."""
import copy
import json
import tempfile
from pathlib import Path

import pandas as pd
from r01_comun import AS_OF, CLASES, DATOS, RUTA_UNIVERSO_EJEMPLO, bloque, cfg, comprobar, fin, ultimo_run

from bloque_a.backtest import ejecutar_backtest
from bloque_a.configuracion import cargar_config

DEF = lambda: cargar_config(extra={"modo": "backtest"})   # noqa: E731 · valor por defecto: solo DIV
SIG = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date())

# 1 · CT-01 con un tipo no activo: PARCIAL, SIN_RESULTADO, NO_ESTIMABLE declarado, F5 íntegro
b = bloque(DEF())
r = b.peticion({"tipo": "AD_HOC", "alcance": {"clases": ["RV"]}, "horizontes": ["H2"], "prioridad": "NORMAL"}, AS_OF)
comprobar("CT-01 tipo no activo: PARCIAL y SIN_RESULTADO con NO_ESTIMABLE declarado",
          r["estado"] == "PARCIAL" and r["entrega"] == "SIN_RESULTADO" and any("NO_ESTIMABLE" in x for x in r["paquete"]["limitaciones"]),
          f"{r['estado']} {r['entrega']} {r['paquete']['limitaciones']}")
comprobar("CT-01 tipo no activo: acuse emitido y F5 íntegro", bool(r.get("acuse")) and all(b.almacen.verificar_integridad().values()))
r2 = b.peticion({"tipo": "AD_HOC", "alcance": {"clases": ["RV"]}, "horizontes": ["H2"], "prioridad": "NORMAL"}, AS_OF)
comprobar("CT-01 repetido con otro msg_id: run nuevo (la idempotencia es por msg_id, anterior a T-66)", r2["run_id"] == r["run_id"],
          f"{r['run_id']} / {r2['run_id']}", hallazgo=False)

# 2 · Profundización (CT-01 PROFUNDIZACION, N3) de un tipo no activo
b = bloque(DEF())
r = b.peticion({"tipo": "PROFUNDIZACION", "alcance": {"clases": ["CRI"]}, "nivel_forzado": "N3", "horizontes": ["H2"], "prioridad": "NORMAL"}, AS_OF)
comprobar("profundización de un tipo no activo: no analiza y lo declara",
          r["paquete"]["clases"] == {} and any("Cripto" in x for x in r["paquete"]["limitaciones"]), f"{r['estado']} {r['entrega']}")
llamadas = b.contabilidad.resumen(r["run_id"])["llamadas"]
comprobar("profundización de un tipo no activo: ninguna llamada al modelo", llamadas == 0, f"llamadas {llamadas}")

# 3 · Alcance con un tipo inexistente
b = bloque(DEF())
r = b.ciclo(AS_OF, alcance={"clases": ["XXX"]})
comprobar("alcance con un tipo inexistente: no analiza nada", r["paquete"]["clases"] == {}, f"limitaciones {r['paquete']['limitaciones']}")
comprobar("alcance con un tipo inexistente: se declara el tipo pedido", any("XXX" in x for x in r["paquete"]["limitaciones"]),
          f"limitaciones {r['paquete']['limitaciones']}", hallazgo=False)

# 4 · CT-03 que escala sin nombrar tipo (con el valor por defecto, solo DIV)
b = bloque(DEF())
q = b.consulta("Analiza qué conviene hacer ahora", as_of=AS_OF)
esc = q.get("escalado") or {}
comprobar("CT-03 escalado sin tipo: va a un tipo activo", set(esc.get("clases") or []) <= {"DIV"},
          f"clases del escalado {esc.get('clases')}, estado del run {esc.get('estado_run')}")

# 5 · CT-04 clases_activas → ciclo
b = bloque(DEF())
b.ciclo(AS_OF)
d = b.decision({"configuracion": {"clases_activas": ["RV"]}}, AS_OF)
r = b.ciclo(SIG)
comprobar("CT-04 clases_activas [RV] y ciclo: analiza RV y no DIV", list(r["paquete"]["clases"]) == ["RV"],
          f"{d['estado']} · clases {list(r['paquete']['clases'])}")
d = b.decision({"configuracion": {"clases_activas": ["RV", "ZZZ"]}}, SIG)
comprobar("CT-04 clases_activas con tipo desconocido: rechazado y P-02 intacto", d["rechazos"] and b.f10()["P-02"] == ["RV"])
b = bloque(DEF())
b.ciclo(AS_OF)
d = b.decision({"configuracion": {"clases_activas": []}}, AS_OF)
r = b.ciclo(SIG)
comprobar("CT-04 clases_activas [] (no analizar nada): se rechaza o el ciclo no analiza",
          bool(d["rechazos"]) or r["paquete"]["clases"] == {},
          f"CT-04 {d['estado']} rechazos {d['rechazos']}; P-02 {b.f10().get('P-02')!r}; el ciclo analiza {list(r['paquete']['clases'])}")

# 6 · Estado F10 anterior a T-66 (P-02 con los 12 tipos) y configuración nueva por defecto
tmp = tempfile.mkdtemp(prefix="r01_f10_")
b = bloque(cfg(), tmp=tmp)
b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
b2 = bloque(DEF(), tmp=tmp)
r = b2.ciclo(SIG)
comprobar("estado F10 con 12 tipos (anterior) + perfiles.activos [DIV]: qué se analiza", True,
          f"P-02 {len(b2.f10()['P-02'])} tipos con fecha de hoy; el ciclo de {SIG} analiza {list(r['paquete']['clases'])} "
          "(el F10 inicial lleva la fecha real y en un backtest no es visible: manda perfiles.activos; anterior a T-66)", hallazgo=False)

# 7 · La configuración del llamador no se muta
c = DEF()
c0 = copy.deepcopy(c)
b = bloque(c)
b.ciclo(AS_OF)
b.decision({"configuracion": {"clases_activas": ["RV"]}}, AS_OF)
comprobar("el ciclo y CT-04 no mutan la configuración del llamador", json.dumps(c, sort_keys=True, default=str) == json.dumps(c0, sort_keys=True, default=str))

# 8 · Backtest de un tipo no activo (todo SIN_RESULTADO) termina y lo dice
out = Path(tempfile.mkdtemp(prefix="r01_bt_"))
res = ejecutar_backtest(DEF(), "2026-03-06", "2026-04-03", str(DATOS), str(RUTA_UNIVERSO_EJEMPLO), str(out), clases=["RV"])
runs = res["metricas"]["runs"]
comprobar("backtest de un tipo no activo: termina, runs PARCIAL/SIN_RESULTADO y sin señales",
          runs and all(x["entrega"] == "SIN_RESULTADO" for x in runs) and res["metricas"]["pronosticos"]["total"] == 0,
          f"{len(runs)} runs, {res['metricas']['pronosticos']['total']} pronósticos")

# 9 · Determinismo: dos bloques idénticos dan el mismo paquete, la misma ablación y los mismos F3/F4
def huella(bb, rr):
    ign = ("_ts", "fecha_entrega", "timestamp", "fecha_recepcion", "fecha_respuesta", "_hash", "_hash_prev")
    lim = lambda x: {k: v for k, v in x.items() if k not in ign}   # noqa: E731
    return json.dumps({"paquete": rr["paquete"], "f3": [lim(x) for x in bb.almacen.leer("F3")],
                       "f4": [lim(x) for x in bb.almacen.leer("F4")], "abl": ultimo_run(bb).get("ablacion")},
                      sort_keys=True, default=str)


h = []
for _ in range(2):
    bb = bloque(cfg())
    rr = bb.ciclo(AS_OF, alcance={"clases": ["DIV", "RV"]})
    h.append(huella(bb, rr))
comprobar("determinismo: dos ejecuciones idénticas dan la misma salida", h[0] == h[1])
fin()
