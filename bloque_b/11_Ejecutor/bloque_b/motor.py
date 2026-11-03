"""Motor de Cálculo Avanzado de Mercados (AG-B16): servicio determinista del ejecutor.

Implementa los métodos que el ejecutor necesita de los módulos MC-B01 (series), MC-B07 (cribado, S con HT-03, IC del
rango por bootstrap, correlaciones y duplicación), MC-B08 (escenarios por bootstrap de bloques y robustez RE), MC-B09
(riesgo 1–5 y estrés histórico) y MC-B10 (métricas de evaluación: Brier, Spearman, IC por bootstrap). Cada servicio se
registra en RC como CALC-B con método, semilla, fecha de corte y huella de los datos (reproducible). Nunca usa datos
posteriores a la fecha de corte: todos los datos pasan por HT-01 con la guardia anti-anticipación.
"""
from __future__ import annotations

import hashlib
import json
import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from .herramientas import ht03
from .herramientas.ht01_datos import DatosNoDisponibles, ProveedorDatos

VERSION = "1.0"


def _semilla(*claves) -> int:
    return int.from_bytes(hashlib.sha256("|".join(map(str, claves)).encode()).digest()[:4], "little")


class Motor:
    def __init__(self, proveedor: ProveedorDatos, almacen=None, cfg: Optional[Dict] = None) -> None:
        self.prov = proveedor
        self.alm = almacen
        self.cfg = (cfg or {}).get("motor") or {}
        self.uc = 0.0

    # ------------------------------------------------------------------ registro RC
    def _registrar(self, metodo: str, modulo: str, insumos: Dict, resultado: Dict, semilla: Optional[int] = None,
                   clase_cifra: str = "determinista", perfil: Optional[str] = None, plan: str = "STD") -> str:
        self.uc += {"MIN": 0.3, "STD": 1.0, "EXT": 2.0}.get(plan, 1.0) * 0.1
        if self.alm is None:
            return "CALC-B-SIN-REGISTRO"
        cid = self.alm.nuevo_id("CALC-B")
        huella = hashlib.sha256(json.dumps(insumos, sort_keys=True, default=str).encode()).hexdigest()[:16]
        self.alm.escribir("RC", "AG-B16", {"tipo_entrada": "CALC", "id": cid, "metodo": metodo, "modulo": modulo,
                                           "perfil": perfil, "plan_calculo": plan, "semilla": semilla,
                                           "fecha_corte": str(self.prov.as_of.date()) if self.prov.as_of is not None else None,
                                           "huella_datos": huella, "insumos": insumos, "resultado": resultado,
                                           "clase_cifra": clase_cifra, "estado": "SERVIDO", "madurez": "implementado",
                                           "como_reproducir": f"bloque_b.motor.Motor.{metodo} con la semilla y la fecha de corte"})
        return cid

    # ------------------------------------------------------------------ MC-B01 · series
    def metricas_precio(self, simbolo: str, referencia: Optional[str] = None) -> Dict:
        try:
            s = self.prov.cierres(simbolo)
        except DatosNoDisponibles:
            return {"datos_precio": False}
        out: Dict = {"datos_precio": True, "ultima_fecha_precio": str(s.index[-1].date()), "n_obs": int(len(s))}
        if len(s) < 260:
            out["historial_corto"] = True
        r = np.log(s).diff().dropna()
        if len(s) > 252:
            out["momento_12_1"] = float(s.iloc[-22] / s.iloc[-253] - 1)
            out["momento_12m"] = float(s.iloc[-1] / s.iloc[-253] - 1)
            ventana = s.iloc[-253:]
            out["caida_maxima_1a"] = float((ventana / ventana.cummax() - 1).min() * -1)
        if len(s) > 63:
            out["momento_3m"] = float(s.iloc[-1] / s.iloc[-64] - 1)
        if len(r) > 60:
            out["volatilidad_1a"] = float(r.iloc[-252:].std() * math.sqrt(252))
        if referencia:
            try:
                rr = np.log(self.prov.cierres(referencia)).diff().dropna()
                j = pd.concat([r, rr], axis=1, join="inner").iloc[-252:]
                if len(j) > 60 and j.iloc[:, 1].var() > 0:
                    out["beta"] = float(j.cov().iloc[0, 1] / j.iloc[:, 1].var())
            except DatosNoDisponibles:
                pass
        return out

    def correlaciones(self, simbolos: Dict[str, str]) -> Dict[str, float]:
        """Correlación de rentabilidades diarias a 2 años (9.7, regla 4). `simbolos`: cand_id → serie."""
        series = {}
        for cid, sim in simbolos.items():
            try:
                series[cid] = np.log(self.prov.cierres(sim)).diff().dropna().iloc[-int(self.cfg.get("ventana_correlacion", 504)):]
            except DatosNoDisponibles:
                continue
        if len(series) < 2:
            return {}
        df = pd.DataFrame(series).dropna(how="any")
        if len(df) < 60:
            return {}
        c = df.corr()
        out = {}
        ids = list(c.columns)
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                out[f"{a}|{b}"] = round(float(c.loc[a, b]), 4)
        return out

    # ------------------------------------------------------------------ MC-B07 · cribado y S
    def puntuar(self, tipo: str, filas: List[Dict], referencia: Optional[str], horizonte: str, semilla: int,
                plan: str = "STD") -> Dict:
        """Calcula métricas de precio, componentes (HT-03), S, IC 90 % de S y del rango (bootstrap de insumos con
        ruido y perturbación de pesos ±5). `filas`: candidatos ya cribados por HT-11 (con `cand_id`)."""
        pb = ht03.PLAYBOOKS[tipo]
        metricas_pb = [m for comp in pb["metricas"].values() for (m, _, _) in comp]
        datos = []
        for f in filas:
            d = {"cand_id": f["cand_id"]}
            for m in metricas_pb:
                v = f.get(m)
                try:
                    d[m] = float(v) if v not in (None, "") else None
                except (TypeError, ValueError):
                    d[m] = None
            mp = self.metricas_precio(f.get("simbolo") or "", referencia)
            for k in ("momento_12_1", "momento_3m", "momento_12m", "volatilidad_1a", "caida_maxima_1a", "beta"):
                if k in metricas_pb and mp.get(k) is not None:
                    d[k] = mp[k]
            if tipo == "CRI" and d.get("volatilidad_1a") is None and f.get("volatilidad_1a_declarada"):
                d["volatilidad_1a"] = float(f["volatilidad_1a_declarada"])
            d["_precio"] = mp
            datos.append(d)
        comp = ht03.normalizar_universo(datos, tipo)
        base = {}
        for d in datos:
            rs = ht03.calcular_S(comp[d["cand_id"]], tipo)
            base[d["cand_id"]] = {"componentes": comp[d["cand_id"]], "S": rs["S"], "ne": len(rs["ne"]),
                                  "calculable": rs["calculable"], "precio": d["_precio"],
                                  "metricas": {k: v for k, v in d.items() if not k.startswith("_") and k != "cand_id"}}
        # Bootstrap: ruido en métricas (10 % de la desviación transversal) y pesos ±5
        B = int(self.cfg.get("bootstrap_replicas", 200)) if plan != "MIN" else 40
        rng = np.random.default_rng(semilla)
        ruido = float(self.cfg.get("ruido_metricas", 0.10))
        pert = float(self.cfg.get("perturbacion_pesos", 5))
        desv = {}
        for m in metricas_pb:
            vals = [d[m] for d in datos if d.get(m) is not None]
            desv[m] = float(np.std(vals)) if len(vals) > 1 else 0.0
        calc_ids = [c for c, b in base.items() if b["calculable"]]
        sims_S = {c: [] for c in calc_ids}
        sims_r = {c: [] for c in calc_ids}
        for _ in range(B):
            pert_datos = []
            for d in datos:
                e = {"cand_id": d["cand_id"]}
                for m in metricas_pb:
                    v = d.get(m)
                    e[m] = None if v is None else v + rng.normal(0, ruido * desv[m]) if desv[m] > 0 else v
                pert_datos.append(e)
            comp_b = ht03.normalizar_universo(pert_datos, tipo)
            pesos = {k: (None if w is None else max(0.0, w + rng.uniform(-pert, pert))) for k, w in pb["pesos"].items()}
            Sb = {}
            for c in calc_ids:
                r = ht03.calcular_S(comp_b[c], tipo, pesos)
                if r["S"] is not None:
                    Sb[c] = r["exacto"]
            orden = sorted(Sb, key=lambda c: -Sb[c])
            for i, c in enumerate(orden, 1):
                sims_S[c].append(Sb[c])
                sims_r[c].append(i)
        for c in calc_ids:
            if sims_S[c]:
                lo, hi = np.percentile(sims_S[c], [5, 95])
                rlo, rhi = np.percentile(sims_r[c], [5, 95])
                S = base[c]["S"]
                base[c]["ic90_S"] = [int(min(math.floor(lo), S)), int(max(math.ceil(hi), S))]
                base[c]["ic90_rango"] = [int(math.floor(rlo)), int(math.ceil(rhi))]
        cid = self._registrar("puntuar", "MC-B07", {"tipo": tipo, "candidatos": [f["cand_id"] for f in filas],
                                                    "referencia": referencia, "plan": plan, "B": B},
                             {c: {"S": b["S"], "ic90_S": b.get("ic90_S"), "ic90_rango": b.get("ic90_rango")} for c, b in base.items()},
                             semilla, "estimacion_estadistica", pb["perfil"], plan)
        return {"calc_id": cid, "candidatos": base}

    # ------------------------------------------------------------------ MC-B08 · escenarios
    def escenarios(self, indicador: str, referencia: str, horizonte_sesiones: int, semilla: int) -> Dict:
        """Distribución de la rentabilidad relativa indicador − referencia en el horizonte, por bootstrap de bloques de
        los últimos 3 años: p10/p50/p90, RE (fracción de simulaciones con rentabilidad relativa > 0, 0–100) y
        rentabilidad histórica de base."""
        try:
            a = np.log(self.prov.cierres(indicador)).diff().dropna()
            b = np.log(self.prov.cierres(referencia)).diff().dropna() if referencia != indicador else a * 0
        except DatosNoDisponibles as e:
            return {"disponible": False, "motivo": str(e)}
        rel = pd.concat([a, b], axis=1, join="inner").iloc[-756:]
        rel = (rel.iloc[:, 0] - rel.iloc[:, 1]).values
        if len(rel) < 126:
            return {"disponible": False, "motivo": "historial insuficiente"}
        n = int(self.cfg.get("montecarlo_simulaciones", 2000))
        bloque = int(self.cfg.get("bloque_bootstrap", 21))
        rng = np.random.default_rng(semilla)
        H = int(horizonte_sesiones)
        k = math.ceil(H / bloque)
        inicios = rng.integers(0, len(rel) - bloque, size=(n, k))
        sims = np.array([np.concatenate([rel[i:i + bloque] for i in fila])[:H].sum() for fila in inicios])
        rel_sim = np.expm1(sims)
        p10, p50, p90 = (float(x) for x in np.percentile(rel_sim, [10, 50, 90]))
        RE = int(round(100 * float((rel_sim > 0).mean())))
        vol = float(np.std(rel) * math.sqrt(252))
        res = {"disponible": True, "p10": round(p10, 4), "p50": round(p50, 4), "p90": round(p90, 4), "RE": RE,
               "vol_relativa_anual": round(vol, 4), "simulaciones": n, "horizonte_sesiones": H,
               "frecuencia_historica_positiva": round(float((pd.Series(rel).rolling(min(H, len(rel) - 1)).sum().dropna() > 0).mean()), 4)}
        res["calc_id"] = self._registrar("escenarios", "MC-B08", {"indicador": indicador, "referencia": referencia, "H": H,
                                                                  "n": n, "bloque": bloque}, res, semilla, "estimacion_estadistica")
        return res

    def sensibilidades(self, esc: Dict) -> List[Dict]:
        if not esc.get("disponible"):
            return []
        cid = esc.get("calc_id")
        vol = esc["vol_relativa_anual"]
        return [{"variable": "Volatilidad relativa del ámbito", "valor_base": f"{vol:.1%}", "valor_bajo": f"{vol * 0.75:.1%}",
                 "valor_alto": f"{vol * 1.25:.1%}", "efecto_bajo": f"p10 {esc['p10'] * 0.75:+.1%}",
                 "efecto_alto": f"p10 {esc['p10'] * 1.25:+.1%}", "unidad": "%", "calc_id": cid},
                {"variable": "Deriva relativa (rentabilidad mediana del escenario base)", "valor_base": f"{esc['p50']:+.1%}",
                 "valor_bajo": f"{esc['p50'] - 0.05:+.1%}", "valor_alto": f"{esc['p50'] + 0.05:+.1%}",
                 "efecto_bajo": "RE −15 a −25 puntos", "efecto_alto": "RE +15 a +25 puntos", "unidad": "%", "calc_id": cid}]

    # ------------------------------------------------------------------ MC-B09 · riesgo
    def riesgo_1a5(self, simbolo: str) -> Tuple[int, Dict]:
        """Escala 1–5 (Anexo A): volatilidad anualizada con ajuste por caída máxima. Ficha del ejecutor:
        < 5 % → 1 · < 10 % → 2 · < 20 % → 3 · < 35 % → 4 · resto → 5; +1 si la caída máxima a 1 año supera el 40 %."""
        mp = self.metricas_precio(simbolo)
        vol = mp.get("volatilidad_1a")
        if vol is None:
            return 3, {"motivo": "sin datos: valor central declarado"}
        n = 1 if vol < 0.05 else 2 if vol < 0.10 else 3 if vol < 0.20 else 4 if vol < 0.35 else 5
        if (mp.get("caida_maxima_1a") or 0) > 0.40:
            n = min(5, n + 1)
        return n, {"volatilidad_1a": round(vol, 4), "caida_maxima_1a": mp.get("caida_maxima_1a")}

    # ------------------------------------------------------------------ rentabilidades (evaluación y backtest)
    def rentabilidad(self, simbolo: str, desde, hasta) -> Optional[float]:
        """Rentabilidad entre el último cierre ≤ desde y el último cierre ≤ hasta. Un valor dado de baja antes de
        `hasta` se valora a su último precio (tratamiento de bajas declarado)."""
        try:
            _, v0 = self.prov.valor_en(simbolo, desde)
            _, v1 = self.prov.valor_en(simbolo, hasta)
        except DatosNoDisponibles:
            return None
        return float(v1 / v0 - 1)


# ---------------------------------------------------------------------- MC-B10 · métricas de evaluación
def spearman(x: Sequence[float], y: Sequence[float]) -> Optional[float]:
    if len(x) < 3:
        return None
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    if np.std(rx) == 0 or np.std(ry) == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def ic_bootstrap_media(valores: Sequence[float], B: int = 1000, nivel: float = 0.90, semilla: int = 7) -> Optional[List[float]]:
    v = np.asarray([x for x in valores if x is not None and not np.isnan(x)], dtype=float)
    if len(v) < 2:
        return None
    rng = np.random.default_rng(semilla)
    medias = rng.choice(v, size=(B, len(v)), replace=True).mean(axis=1)
    a = (1 - nivel) / 2
    return [round(float(np.quantile(medias, a)), 6), round(float(np.quantile(medias, 1 - a)), 6)]


def brier(p: Sequence[float], y: Sequence[int]) -> Optional[float]:
    if not p:
        return None
    return float(np.mean((np.asarray(p) - np.asarray(y)) ** 2))
