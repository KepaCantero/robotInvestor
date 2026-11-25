"""Cierre de la comparación pareada de dos ordenaciones de RK ya congeladas."""
from collections import defaultdict

import numpy as np
from scipy import stats

from .configuracion import parametro
from .evaluador import _numero_finito
from .motor import evaluacion as ev


def comparar(evaluador, ajuste, as_of):
    hasta = ajuste["sombra_hasta"]
    runs = {r["id"]: r for r in evaluador.almacen.leer("F5", hasta) if r.get("tipo_entrada") == "RUN"
            and ajuste["efecto_desde"] <= r["_fecha"] <= hasta and r.get("entrega") == "ENTREGADA"}
    cambios = sum(s.get("cambios", 0) for r in runs.values() for s in (r.get("sombra") or {}).values()
                  if s.get("aju_id") == ajuste["id"])
    series = defaultdict(list)
    for p in evaluador.resueltos(hasta):
        run = runs.get(p.get("run_id"), {})
        sombra = (run.get("sombra") or {}).get(p.get("clase"), {})
        par = (sombra.get("rk_pareado") or {}).get(p.get("opp_id"))
        if sombra.get("aju_id") != ajuste["id"] or not par:
            continue
        valor = (p.get("resolucion") or {}).get("valor_observado")
        if (p.get("sentido") not in ("POSITIVO", "NEGATIVO") or not p.get("horizonte") or not _numero_finito(valor)
                or not isinstance(par, (tuple, list)) or len(par) != 2 or not all(_numero_finito(v) for v in par)):
            continue
        dato = valor * (1 if p["sentido"] == "POSITIVO" else -1)
        series[run["_fecha"], p["run_id"], p["clase"], p["horizonte"]].append((*par, dato))
    por_dia = defaultdict(list)
    for (dia, _, _, _), filas in series.items():
        anterior, nueva, y = zip(*filas)
        if min(len(set(v)) for v in (anterior, nueva, y)) < 2:
            continue
        por_dia[dia].append([stats.spearmanr(anterior, y).statistic, stats.spearmanr(nueva, y).statistic])
    medias = [np.mean(por_dia[d], axis=0) for d in sorted(por_dia)]
    n_pares = sum(len(filas) for filas in series.values())
    dm, ic_previo, ic_actual = None, None, None
    estado = "REVERTIDO"
    motivo = "Muestra pareada insuficiente; se conservan los pesos anteriores"
    if n_pares >= parametro(evaluador.cfg, "evaluacion.min_calibrar") and medias:
        ic_anterior, ic_nueva = np.array(medias).T
        dm = ev.diebold_mariano_hln(-ic_anterior, -ic_nueva)
        ic_previo, ic_actual = float(ic_anterior.mean()), float(ic_nueva.mean())
        p = dm["p_unilateral"]
        if p is not None:  # El motor devuelve None con menos de tres fechas.
            if p < parametro(evaluador.cfg, "evaluacion.recalibracion_rk.p_reversion"):
                motivo = "La comparación DM-HLN favorece los pesos anteriores"
            elif ic_actual < ic_previo:
                motivo = "La capacidad ordenadora media ha disminuido"
            else:
                estado = "CONFIRMADO"
                motivo = "Se conserva o mejora la capacidad ordenadora media"
    resultado = {"metrica_nueva": ic_actual, "metrica_anterior": ic_previo, "dm_hln_p": dm and dm["p_unilateral"],
                 "decisiones_top3_cambiadas": cambios, "decision": estado}
    return {"estado": estado, "dm_hln": dm, "ic_anterior": ic_previo, "ic_nueva": ic_actual,
            "n_pares": n_pares, "n_fechas": len(medias), "fechas_pareadas": sorted(por_dia),
            "resultado_sombra": resultado, "motivo_cierre": motivo}
