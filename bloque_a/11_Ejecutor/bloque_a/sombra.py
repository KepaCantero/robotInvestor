"""Cierre de la comparación pareada de dos ordenaciones de RK ya congeladas."""
from collections import defaultdict

import numpy as np
from scipy import stats

from .configuracion import parametro
from .motor import evaluacion as ev


def comparar(evaluador, ajuste, as_of):
    hasta = ajuste["sombra_hasta"]
    runs = {r["id"]: r for r in evaluador.almacen.leer("F5", hasta) if r.get("tipo_entrada") == "RUN"
            and ajuste["efecto_desde"] <= r["_fecha"] <= hasta and r.get("entrega") == "ENTREGADA"}
    series = defaultdict(list)
    for p in evaluador.resueltos(hasta):
        run = runs.get(p.get("run_id"), {})
        sombra = (run.get("sombra") or {}).get(p["clase"], {})
        par = (sombra.get("rk_pareado") or {}).get(p.get("opp_id"))
        if sombra.get("aju_id") != ajuste["id"] or not par:
            continue
        dato = p["resolucion"]["valor_observado"] * (1 if p["sentido"] == "POSITIVO" else -1)
        if len(par) == 2 and all(isinstance(v, (int, float)) and np.isfinite(v) for v in (*par, dato)):
            series[run["_fecha"], p["run_id"], p["clase"], p["horizonte"]].append((*par, dato))
    por_dia = defaultdict(list)
    for (dia, _, _, _), filas in series.items():
        anterior, nueva, y = zip(*filas)
        if min(len(set(v)) for v in (anterior, nueva, y)) < 2:
            continue
        por_dia[dia].append([stats.spearmanr(anterior, y).statistic, stats.spearmanr(nueva, y).statistic])
    medias = [np.mean(por_dia[d], axis=0) for d in sorted(por_dia)]
    if len(medias) < parametro(evaluador.cfg, "evaluacion.min_calibrar"):
        return {"estado": "REVERTIDO", "dm_hln": None, "motivo_cierre": "Muestra pareada insuficiente; se conservan los pesos anteriores",
                "fechas_pareadas": sorted(por_dia)}
    ic_anterior, ic_nueva = np.array(medias).T
    dm = ev.diebold_mariano_hln(-ic_anterior, -ic_nueva)
    empeora = dm["p_unilateral"] is None or dm["p_unilateral"] < parametro(evaluador.cfg, "evaluacion.alfa_holm") or ic_nueva.mean() < ic_anterior.mean()
    return {"estado": "REVERTIDO" if empeora else "CONFIRMADO", "dm_hln": dm, "ic_anterior": float(ic_anterior.mean()),
            "ic_nueva": float(ic_nueva.mean()), "fechas_pareadas": sorted(por_dia), "motivo_cierre": "Comparación de la capacidad ordenadora"}
