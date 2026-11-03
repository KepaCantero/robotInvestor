"""Evaluador de Previsiones y Aprendizaje (AG-20) en el ejecutor: parte determinista.

- Resuelve los PRG-FX- de F4 cuya fecha de resolución es <= as_of, con datos HT-01 vistos con ese as_of
  (sin look-ahead) y el criterio congelado; escribe solo campos de resolución (matriz 5.1). En rentabilidad
  total suma al contado el carry congelado en la emisión.
- Referencias ingenuas obligatorias (8.4 y Anexo A; Catálogo 3.3): paseo aleatorio (RI-PA, p = 0,5 en sube/baja)
  y forward como predictor (RI-FWD: lognormal sin deriva centrada en el forward con la volatilidad EWMA conocida
  en la fecha de emisión). Brier, acierto y BSS frente a ambas (FX-RW-001, versión sencilla).
- Métricas por segmento × horizonte (FC-EVAL-001 / FC-CAL-001) y rentabilidad frente a la referencia del segmento
  (8.4: G10N, G10M y ESTR, rentabilidad en exceso nula; EMAS, EMLA y EMEA, cesta equiponderada del segmento).
- Certificados de horizonte con el criterio del Anexo A (n ≥ 100, IC 90 % del BSS > 0 con Holm, ECE ≤ q90
  del nulo y < 0,15); revocación por deterioro.
- Lecciones LEC- (predictivas, de calibración y de producto) y recalibración de pesos de RK dentro de
  bandas en modo sombra (o propuesta de tipo 3 si se sale de bandas).
"""
from __future__ import annotations

import math
import re
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats

from .configuracion import SEGMENTOS, HORIZONTES
from .herramientas.ht01_datos import DatosNoDisponibles
from .herramientas.ht05_planificador import dias_habiles_entre
from .motor import evaluacion as ev

BANDAS = [(0.80, "MUY_PROBABLE"), (0.60, "MAS_PROBABLE_QUE_NO"), (0.45, "INCIERTO"), (0.25, "POCO_PROBABLE"), (0.0, "MUY_POCO_PROBABLE")]
CADUCIDAD_MESES = {"anecdotica": 3, "recurrente": 6, "estadistica": 12}


def _version_menor_siguiente(v: str) -> str:
    """FX-1.1 → FX-1.2 (12.2: los ajustes dentro de bandas crean una versión menor)."""
    m = re.match(r"^FX-(\d+)\.(\d+)$", str(v or ""))
    return f"FX-{m.group(1)}.{int(m.group(2)) + 1}" if m else "FX-1.2"


def banda_de(p: float) -> str:
    """Banda verbal (F4) a partir de la probabilidad interna; los huecos entre bandas van a la más prudente."""
    if p >= 0.80:
        return "MUY_PROBABLE"
    if p >= 0.60:
        return "MAS_PROBABLE_QUE_NO"
    if p > 0.40:
        return "INCIERTO"
    if p >= 0.25:
        return "POCO_PROBABLE"
    return "MUY_POCO_PROBABLE"


def banda_publicable(p: float) -> str:
    """Vocabulario de bandas del paquete (esquema JSON del paquete Forex V1.0): tres valores."""
    if p >= 0.60:
        return "más probable que no"
    if p > 0.40:
        return "incierto"
    return "poco probable"


class Evaluador:
    def __init__(self, almacen, proveedor, motor, cfg: Dict, universo: pd.DataFrame) -> None:
        self.almacen = almacen
        self.proveedor = proveedor
        self.motor = motor
        self.cfg = cfg
        self.universo = universo
        self.ev_cfg = cfg.get("evaluacion") or {}

    # ------------------------------------------------------------------------------------
    # Rentabilidades y referencia ingenua
    # ------------------------------------------------------------------------------------
    def simbolos_segmento(self, segmento: str) -> List[str]:
        return [s for s in self.universo[self.universo["segmento"] == segmento]["simbolo"] if self.proveedor.tiene(s)]

    def rentabilidad(self, simbolo: str, segmento: str, f0, f1) -> Tuple[float, pd.Timestamp]:
        if simbolo == "CESTA":
            vals, fechas = [], []
            for s in self.simbolos_segmento(segmento):
                try:
                    r, f = self.rentabilidad(s, segmento, f0, f1)
                    vals.append(r)
                    fechas.append(f)
                except DatosNoDisponibles:
                    continue
            if not vals:
                raise DatosNoDisponibles(f"Cesta {segmento} sin datos")
            return float(np.mean(vals)), max(fechas)
        d0, v0 = self.proveedor.valor_en(simbolo, f0)
        d1, v1 = self.proveedor.valor_en(simbolo, f1)
        return v1 / v0 - 1, d1

    def volatilidad_conocida(self, proxy: str, as_of) -> Optional[float]:
        """Volatilidad EWMA (λ = 0,94) anualizada del indicador con datos hasta as_of (RI-EWMA)."""
        try:
            s = self.proveedor.cierres(proxy, pd.Timestamp(as_of) - pd.DateOffset(years=1), as_of)
        except DatosNoDisponibles:
            return None
        r = np.log(s.astype(float)).diff().dropna().values
        if len(r) < 20:
            return None
        var = float(np.var(r[:20], ddof=1))
        for x in r:
            var = 0.94 * var + 0.06 * x * x
        return float(math.sqrt(var * 252))

    def referencia_ingenua(self, proxy: str, segmento: str, sesiones: int, sentido_positivo: bool, as_of,
                           carry_indicador_pct: Optional[float] = None, run_id: Optional[str] = None) -> Dict:
        """RI-PA y RI-FWD del suceso «el indicador sube (o baja) en el horizonte» (Catálogo 3.3, FX-RW-001).
        RI-PA: p = 0,5 (paseo aleatorio sin deriva). RI-FWD: ln S_T ~ N(ln F, σ²·τ) con F = S·(1 − carry·τ) (paridad
        cubierta: el forward descuenta la depreciación de lo que rinde más) y σ EWMA conocida en as_of."""
        from .motor import operaciones as op
        anios = sesiones / 252.0
        vol = self.volatilidad_conocida(proxy, as_of)
        cambio_fwd = self.proveedor.cambio_forward(carry_indicador_pct, anios)
        p_fwd = None
        if cambio_fwd is not None and vol:
            p_fwd = op.prob_paseo_aleatorio(1.0, 1.0, vol, anios, sube=sentido_positivo, centro=1.0 + cambio_fwd)
            p_fwd = round(min(max(p_fwd, 0.05), 0.95), 4)
        calc_id = self.almacen.nuevo_id("CALC")
        self.almacen.escribir("RC", "AG-13", {
            "tipo_entrada": "SERVICIO", "calc_id": calc_id, "contrato": "CT-09", "run_id": run_id, "solicitante": "AG-10",
            "operacion": {"method_id": "RI-PA/RI-FWD", "ficha_id": "FX-RW-001", "ficha_version": "1.0", "catalog_version": "FX-1.0",
                          "op_sin_ficha": False}, "perfil": ["TRANSVERSAL"], "segmento": segmento, "modo": "SYNC_CALC",
            "plan": "PLAN_MIN", "as_of": str(pd.Timestamp(as_of).date()), "estado": "SERVED",
            "datos": [{"serie_ht01": proxy}, {"valores": {"carry_indicador_pct": carry_indicador_pct}}],
            "parametros": {"sesiones": sesiones, "sentido_positivo": sentido_positivo, "vol": "EWMA 0,94 conocida en as_of"},
            "semilla": None, "resultado": {"forma": "VALOR", "payload": {"prob_paseo_aleatorio": 0.5, "prob_forward": p_fwd,
                                                                         "cambio_forward": cambio_fwd, "vol_ewma": vol}},
            "clase_cifra": "ESTADISTICA", "referencia_ingenua": {"tipo": "RI-PA"}, "madurez_metodo": "IMPLEMENTADO",
            "consumo_uc": 0.0, "limitaciones": [] if p_fwd is not None else ["sin tipos o sin volatilidad: RI-FWD no disponible"]})
        return {"tipo": "PASEO_ALEATORIO", "valor_o_prob": 0.5, "prob_forward": p_fwd,
                "cambio_forward": None if cambio_fwd is None else round(cambio_fwd, 8), "vol_ewma": vol, "calc_id": calc_id}

    # ------------------------------------------------------------------------------------
    # Resolución
    # ------------------------------------------------------------------------------------
    def resolver(self, as_of, run_id: Optional[str] = None) -> List[Dict]:
        as_of = pd.Timestamp(as_of).normalize()
        abiertos = [p for p in self.almacen.estado("F4", as_of).values() if p.get("estado") == "ABIERTO"]
        # H5 no se resuelve por precio: se evalúa por sus hitos (resolver_hitos, V1.1)
        pendientes = [p for p in abiertos if p.get("horizonte") != "H5" and pd.Timestamp(p["fecha_resolucion"]) <= as_of]
        resueltos: List[Dict] = []
        filas = []
        for p in sorted(pendientes, key=lambda x: x["prg_id"]):
            f0, f1 = pd.Timestamp(p["fecha_emision"]), pd.Timestamp(p["fecha_resolucion"])
            try:
                rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["segmento"], f0, f1)
                rr = None
                if p.get("referencia_indice") == "CESTA":   # referencia del segmento (8.4), informativa
                    try:
                        rr, _ = self.rentabilidad("CESTA", p["segmento"], f0, f1)
                    except DatosNoDisponibles:
                        rr = None
            except DatosNoDisponibles:
                if dias_habiles_entre(f1, as_of) >= int(self.ev_cfg.get("dias_habiles_no_resoluble", 10)):
                    filas.append((p, None))
                continue
            if (f1 - d1).days > 7:   # el último dato es demasiado antiguo: esperar
                if dias_habiles_entre(f1, as_of) >= int(self.ev_cfg.get("dias_habiles_no_resoluble", 10)):
                    filas.append((p, None))
                continue
            anios = max((f1 - f0).days / 365.25, 0.0)
            carry = (p.get("variable") or {}).get("carry_anual_pct_indicador")
            x = rp + (carry / 100.0 * anios if (p["variable"].get("tipo_rentabilidad") == "RENTABILIDAD_TOTAL" and carry is not None) else 0.0)
            positivo = p["sentido"] == "POSITIVO"
            o = int((x > p.get("umbral", 0.0)) if positivo else (x < -p.get("umbral", 0.0)))
            fuga_ok = (pd.Timestamp(p["nivel_referencia"]["fecha"]) <= f0 and d1 <= as_of and f1 <= as_of)
            filas.append((p, {"rent_proxy": rp, "rent_referencia": rr, "exceso": x, "o": o, "fecha_dato": d1,
                              "fuga": "SUPERADA" if fuga_ok else "FALLIDA"}))
        if not filas:
            return []
        validas = [(p, r) for p, r in filas if r is not None]
        calc_id = None
        if validas:
            res = self.motor.servir({"operacion": "FC-EVAL-001", "plan": "PLAN_MIN", "datos": [{"valores": {
                "p": [p["prob_interna"] for p, _ in validas], "o": [r["o"] for _, r in validas],
                "p_ref": [p["referencia_ingenua"]["valor_o_prob"] for p, _ in validas]}}],
                "parametros": {"replicas": 200, "simulaciones": 200}, "fecha_corte": str(as_of.date())}, "AG-20", run_id)
            calc_id = res.get("calc_id")
        for p, r in filas:
            if r is None:
                e = {"prg_id": p["prg_id"], "tipo_entrada": "RESOLUCION", "estado": "NO_RESOLUBLE",
                     "resolucion": {"fecha_resuelto": str(as_of.date()), "motivo_no_resoluble": "sin dato tras 10 días hábiles",
                                    "comprobacion_fuga": "SUPERADA", "fallback_aplicado": False}}
            else:
                pi, pr = float(p["prob_interna"]), float(p["referencia_ingenua"]["valor_o_prob"])
                o = r["o"]
                e = {"prg_id": p["prg_id"], "tipo_entrada": "RESOLUCION", "estado": "RESUELTO",
                     "resolucion": {"fecha_resuelto": str(as_of.date()), "fecha_dato": str(r["fecha_dato"].date()),
                                    "valor_observado": round(r["exceso"], 8), "rent_proxy": round(r["rent_proxy"], 8),
                                    "tipo_rentabilidad": p["variable"].get("tipo_rentabilidad"),
                                    "rent_referencia": None if r["rent_referencia"] is None else round(r["rent_referencia"], 8),
                                    "unidad": "tanto por uno", "fuente_usada": f"HT-01:{self.proveedor.nombre}",
                                    "vintage": str(as_of.date()), "fallback_aplicado": False,
                                    "resultado": "OCURRIDO" if o else "NO_OCURRIDO", "resultado_binario": o,
                                    "puntuaciones": {"brier": (pi - o) ** 2, "log": -math.log(min(max(pi if o else 1 - pi, 0.01), 0.99)),
                                                     "brier_ref": (pr - o) ** 2,
                                                     "log_ref": -math.log(min(max(pr if o else 1 - pr, 0.01), 0.99)),
                                                     "brier_forward": None if p["referencia_ingenua"].get("prob_forward") is None
                                                     else (float(p["referencia_ingenua"]["prob_forward"]) - o) ** 2,
                                                     "acierto_forward": None if p["referencia_ingenua"].get("prob_forward") is None
                                                     else int((float(p["referencia_ingenua"]["prob_forward"]) >= 0.5) == bool(o))},
                                    "calc_id": calc_id, "comprobacion_fuga": r["fuga"]}}
            self.almacen.escribir("F4", "AG-20", e)
            resueltos.append({**p, **e})
        self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "RES", "id": f"RES-{as_of.date()}-{self.almacen.nuevo_id('RESL')[-4:]}",
                                              "fecha": str(as_of.date()),
                                              "prg_resueltos": [x["prg_id"] for x in resueltos if x["estado"] == "RESUELTO"],
                                              "prg_no_resolubles": [x["prg_id"] for x in resueltos if x["estado"] == "NO_RESOLUBLE"],
                                              "calc_id": calc_id,
                                              "comprobacion_fuga": "SUPERADA" if all(r is None or r["fuga"] == "SUPERADA" for _, r in filas) else "FALLIDA"})
        return resueltos

    # ------------------------------------------------------------------------------------
    # Métricas
    # ------------------------------------------------------------------------------------
    def resueltos(self, as_of=None, solo_informe: bool = False) -> List[Dict]:
        out = [p for p in self.almacen.estado("F4", as_of).values()
               if p.get("estado") == "RESUELTO" and (p.get("resolucion") or {}).get("comprobacion_fuga") == "SUPERADA"]
        return [p for p in out if p.get("en_informe")] if solo_informe else out

    def metricas(self, as_of=None, completas: bool = False, solo_informe: bool = False) -> Dict:
        """Métricas por segmento × horizonte. `completas` añade bootstrap del BSS, ECE con nulo y DM-HLN."""
        celdas: Dict[Tuple[str, str], List[Dict]] = defaultdict(list)
        for p in self.resueltos(as_of, solo_informe):
            celdas[(p["segmento"], p["horizonte"])].append(p)
        out = {}
        for (c, h), lst in sorted(celdas.items()):
            lst.sort(key=lambda x: (x["fecha_emision"], x["prg_id"]))
            pp = [float(x["prob_interna"]) for x in lst]
            oo = [int(x["resolucion"]["resultado_binario"]) for x in lst]
            pr = [float(x["referencia_ingenua"]["valor_o_prob"]) for x in lst]
            tasa_base = float(np.mean(pr))
            if completas:
                m = ev.evaluar_celda(pp, oo, pr, tasa_base, int(self.ev_cfg.get("bootstrap_replicas", 2000)),
                                     int(self.ev_cfg.get("simulaciones_ece", 2000)), float(self.ev_cfg.get("nivel_ic", 0.9)))
            else:
                m = {"n": len(lst), "brier": ev.brier(pp, oo), "brier_ref": ev.brier(pr, oo),
                     "acierto": ev.acierto_direccional(oo, tasa_base), "calibracion_global": {"p_media": float(np.mean(pp)), "frecuencia": float(np.mean(oo))},
                     "bss": {"valor": (1 - ev.brier(pp, oo) / ev.brier(pr, oo)) if ev.brier(pr, oo) > 0 else None, "ic": [None, None]}}
            bf = [x["resolucion"]["puntuaciones"].get("brier_forward") for x in lst]
            bf = [b for b in bf if b is not None]
            af = [x["resolucion"]["puntuaciones"].get("acierto_forward") for x in lst]
            af = [a for a in af if a is not None]
            m["brier_forward"] = float(np.mean(bf)) if bf else None
            m["tasa_forward"] = float(np.mean(af)) if af else None
            m["bss_forward"] = (1 - m["brier"] / m["brier_forward"]) if bf and m["brier_forward"] > 0 and len(bf) == len(lst) else None
            informe = [x for x in lst if x.get("en_informe")]
            sg = [(1 if x["sentido"] == "POSITIVO" else -1) for x in informe]
            rel = [x["resolucion"]["valor_observado"] * s_ for x, s_ in zip(informe, sg)]
            exc = [(x["resolucion"]["valor_observado"] - (x["resolucion"].get("rent_referencia") or 0.0)) * s_
                   for x, s_ in zip(informe, sg)]
            m["rentabilidad_media_top3"] = float(np.mean(rel)) if rel else None
            m["rentabilidad_relativa_media_top3"] = float(np.mean(exc)) if exc else None
            m["n_top3"] = len(informe)
            m["referencia"] = "paseo aleatorio y forward"
            m["referencia_segmento"] = lst[0].get("referencia_indice") or "rentabilidad en exceso nula"
            out[f"{c}|{h}"] = m
        return out

    def historial_aciertos(self, as_of, semanas: int = 12) -> Dict:
        """Historial publicable (R13 · 11): opciones del informe resueltas en la ventana, con tamaño muestral."""
        lim = pd.Timestamp(as_of) - pd.Timedelta(weeks=semanas)
        lst = [p for p in self.resueltos(as_of, solo_informe=True) if pd.Timestamp(p["resolucion"]["fecha_resuelto"]) >= lim]
        no_res = [p for p in self.almacen.estado("F4", as_of).values() if p.get("estado") == "NO_RESOLUBLE" and p.get("en_informe")]
        def celda(xs, ref_txt):
            n = len(xs)
            k = sum(int(x["resolucion"]["resultado_binario"]) for x in xs)
            pr = float(np.mean([x["referencia_ingenua"]["valor_o_prob"] for x in xs])) if xs else 0.5
            sig = bool(n >= 30 and stats.binomtest(k, n, pr, alternative="greater").pvalue < 0.10) if n else False
            ph = defaultdict(lambda: {"n": 0, "aciertos": 0})
            for x in xs:
                ph[x["horizonte"]]["n"] += 1
                ph[x["horizonte"]]["aciertos"] += int(x["resolucion"]["resultado_binario"])
            af = [x["resolucion"]["puntuaciones"].get("acierto_forward") for x in xs]
            af = [a for a in af if a is not None]
            return {"n": n, "aciertos": k, "tasa_acierto": round(k / n, 4) if n else None, "referencia": ref_txt,
                    "tasa_esperada_azar": round(pr, 4), "tasa_forward": round(float(np.mean(af)), 4) if af else None,
                    "significativo": sig, "por_horizonte": dict(ph)}
        por_segmento = {}
        for c in SEGMENTOS:
            xs = [x for x in lst if x["segmento"] == c]
            if xs:
                por_segmento[c] = celda(xs, "Paseo aleatorio (0,5 sin deriva) y forward como predictor")
        g = celda(lst, "Paseo aleatorio (0,5 sin deriva) y forward como predictor")
        nota = (f"Ventana de {semanas} semanas; {g['n']} pronósticos de opciones publicadas resueltos"
                + (f"; {len(no_res)} no resolubles excluidos y declarados" if no_res else "")
                + ("; muestra pequeña (< 30): la diferencia frente al azar puede deberse a la suerte" if g["n"] < 30 else ""))
        return {"ventana": f"{semanas} semanas", "referencia": "paseo aleatorio y forward", "global": g,
                "por_segmento": por_segmento, "nota": nota}

    # ------------------------------------------------------------------------------------
    # Certificados, lecciones y recalibración
    # ------------------------------------------------------------------------------------
    def certificados_vigentes(self, as_of=None) -> List[Dict]:
        return [c for c in self.almacen.estado("F6", as_of, clave="id").values()
                if c.get("tipo_entrada") in ("CERT", "CERT_REVOCACION") and c.get("estado") == "VIGENTE"]

    def revisar_certificados(self, as_of, run_id: Optional[str] = None) -> Dict:
        n_cert = int(self.ev_cfg.get("min_certificar", 100))
        celdas = defaultdict(list)
        for p in self.resueltos(as_of):
            celdas[(p["segmento"], p["horizonte"])].append(p)
        candidatas = {k: v for k, v in celdas.items() if len(v) >= n_cert}
        vigentes = {(c["celda"]["segmento"], c["celda"]["horizonte"]): c for c in self.certificados_vigentes(as_of)}
        emitidos, revocados, evaluadas = [], [], {}
        if candidatas:
            metr = {k: ev.evaluar_celda([float(x["prob_interna"]) for x in v], [int(x["resolucion"]["resultado_binario"]) for x in v],
                                        [float(x["referencia_ingenua"]["valor_o_prob"]) for x in v],
                                        float(np.mean([x["referencia_ingenua"]["valor_o_prob"] for x in v])),
                                        int(self.ev_cfg.get("bootstrap_replicas", 2000)), int(self.ev_cfg.get("simulaciones_ece", 2000)))
                    for k, v in sorted(candidatas.items())}
            umbrales = ev.holm({f"{k[0]}|{k[1]}": (m["dm_hln"]["p_unilateral"] if m["dm_hln"]["p_unilateral"] is not None else 1.0)
                                for k, m in metr.items()}, 0.10)
            for k, m in metr.items():
                crit = ev.criterio_certificado(m, n_cert, float(self.ev_cfg.get("ece_max", 0.15)),
                                               umbrales[f"{k[0]}|{k[1]}"] if len(metr) > 1 else None)
                evaluadas[f"{k[0]}|{k[1]}"] = crit
                if crit["certificable"] and k not in vigentes:
                    cert = {"tipo_entrada": "CERT", "id": self.almacen.nuevo_id("CERT"), "estado": "VIGENTE",
                            "celda": {"segmento": k[0], "horizonte": k[1], "metodo": None}, "n": m["n"],
                            "brier": m["brier"], "brier_ref": m["brier_ref"], "bss": m["bss"]["valor"], "bss_ic90": m["bss"]["ic"],
                            "holm_superado": True, "ece": m["calibracion"]["ece"], "ece_nulo_q90": m["ece_nulo"]["q90"],
                            "methodology_version": self.cfg.get("methodology_version", "FX-1.0"), "emitido": str(pd.Timestamp(as_of).date())}
                    self.almacen.escribir("F6", "AG-20", cert)
                    emitidos.append(cert)
                elif k in vigentes:
                    bssv = m["bss"]["valor"]
                    if (bssv is not None and bssv <= 0) or (m["calibracion"]["ece"] or 1) >= 0.12:
                        c = vigentes[k]
                        self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT_REVOCACION", "id": c["id"], "estado": "REVOCADO",
                                                              "motivo_cambio": "deterioro: BSS ≤ 0 o ECE ≥ 0,12", "fecha": str(pd.Timestamp(as_of).date())})
                        revocados.append(c["id"])
        no_cert = {f"{k[0]}|{k[1]}": f"n = {len(v)} < {n_cert}" for k, v in celdas.items() if k not in candidatas}
        return {"emitidos": emitidos, "revocados": revocados, "evaluadas": evaluadas, "insuficientes": no_cert}

    def lecciones_vigentes(self, as_of, segmento: Optional[str] = None, max_n: int = 10) -> List[Dict]:
        orden = {"estadistica": 0, "recurrente": 1, "anecdotica": 2}
        lst = []
        for l in self.almacen.estado("F6", as_of, clave="id").values():
            if l.get("tipo_entrada") != "LEC" or l.get("estado") != "VIGENTE":
                continue
            if pd.Timestamp(l["caducidad"]) < pd.Timestamp(as_of):
                continue
            amb = l.get("ambito") or {}
            if segmento and amb.get("segmento") not in (None, segmento):
                continue
            lst.append(l)
        lst.sort(key=lambda l: (orden.get(l["fuerza"], 3), l["id"]))
        return [{k: l.get(k) for k in ("id", "ambito", "tipo", "observacion", "recomendacion", "fuerza", "fecha")} for l in lst[:max_n]]

    def _nueva_leccion(self, as_of, ambito: Dict, tipo: str, obs: str, rec: str, fuerza: str, evidencia: List[str], n: int,
                       origen: str = "DETERMINISTA") -> Optional[Dict]:
        for l in self.almacen.estado("F6", as_of, clave="id").values():
            if l.get("tipo_entrada") == "LEC" and l.get("estado") == "VIGENTE" and l.get("tipo") == tipo \
                    and l.get("ambito") == ambito and pd.Timestamp(l["caducidad"]) >= pd.Timestamp(as_of):
                return None
        cad = pd.Timestamp(as_of) + pd.DateOffset(months=CADUCIDAD_MESES.get(fuerza, 3))
        lec = {"tipo_entrada": "LEC", "id": self.almacen.nuevo_id("LEC"), "fecha": str(pd.Timestamp(as_of).date()), "ambito": ambito,
               "nivel": "B" if tipo in ("PREDICTIVA", "CALIBRACION") else "A", "tipo": tipo, "observacion": obs, "evidencia": evidencia,
               "recomendacion": rec, "fuerza": fuerza, "n": n, "caducidad": str(cad.date()), "estado": "VIGENTE", "origen": origen}
        self.almacen.escribir("F6", "AG-20", lec)
        return lec

    def extraer_lecciones(self, as_of, metricas: Dict) -> List[Dict]:
        nuevas = []
        for celda, m in metricas.items():
            c, h = celda.split("|")
            n = m["n"]
            if n < 10:
                continue
            tasa = (m.get("acierto") or {}).get("tasa")
            fuerza = "estadistica" if n >= int(self.ev_cfg.get("min_calibrar", 30)) else "recurrente"
            if tasa is not None and tasa < 0.45:
                l = self._nueva_leccion(as_of, {"segmento": c, "horizonte": h}, "PREDICTIVA",
                                        f"Acierto {tasa:.0%} en {n} pronósticos de {c}×{h}, por debajo de la tasa base.",
                                        "Rebajar un nivel la banda verbal y exigir catalizador fechado antes de proponer en esta celda.",
                                        fuerza, [f"MET:{celda}"], n)
                if l:
                    nuevas.append(l)
            cg = m.get("calibracion_global") or {}
            if cg and cg.get("p_media") is not None and cg["p_media"] - cg["frecuencia"] >= 0.10:
                l = self._nueva_leccion(as_of, {"segmento": c, "horizonte": h}, "CALIBRACION",
                                        f"Sobreconfianza en {c}×{h}: probabilidad media {cg['p_media']:.2f} frente a frecuencia {cg['frecuencia']:.2f} (n = {n}).",
                                        "Acercar la probabilidad interna a la tasa base (máximo 0,60) hasta que la calibración mejore.",
                                        fuerza, [f"MET:{celda}"], n)
                if l:
                    nuevas.append(l)
        return nuevas

    def leccion_producto(self, as_of, tema: str, qry_ids: List[str]) -> Optional[Dict]:
        return self._nueva_leccion(as_of, {"segmento": None, "horizonte": None, "agente": ["AG-17", "AG-02"]}, "PRODUCTO",
                                   f"La pregunta «{tema}» se ha repetido {len(qry_ids)} veces en 4 semanas.",
                                   "Incorporar esa información al informe por defecto (sección de lectura del conjunto).",
                                   "recurrente", qry_ids, len(qry_ids))

    def recalibrar(self, as_of, run_id: Optional[str] = None) -> Optional[Dict]:
        """Propuesta de ajuste de pesos de RK dentro de bandas (modo sombra) a partir de la capacidad
        ordenadora (IC de Spearman) de A y E frente al resultado de las opciones publicadas."""
        res = self.resueltos(as_of, solo_informe=True)
        n_min = int(self.ev_cfg.get("min_calibrar", 30))
        if len(res) < n_min:
            return None
        f6 = self.almacen.estado("F6", as_of, clave="id").values()
        if any(a.get("tipo_entrada") == "AJU" and a.get("estado") == "EN_SOMBRA" for a in f6):
            return None
        A = [x.get("puntuaciones_opcion", {}).get("A") for x in res]
        E = [x.get("puntuaciones_opcion", {}).get("E") for x in res]
        y = [x["resolucion"]["valor_observado"] * (1 if x["sentido"] == "POSITIVO" else -1) for x in res]
        if any(v is None for v in A + E) or len(set(A)) < 2 or len(set(E)) < 2:
            return None
        ic_a = float(stats.spearmanr(A, y).statistic)
        ic_e = float(stats.spearmanr(E, y).statistic)
        if abs(ic_a - ic_e) <= 0.10:
            return None
        sube, baja = ("A", "E") if ic_a > ic_e else ("E", "A")
        trimestre = f"{pd.Timestamp(as_of).year}-T{(pd.Timestamp(as_of).month - 1) // 3 + 1}"
        acumulado = sum(abs(a.get("delta", 0)) for a in f6 if a.get("tipo_entrada") == "AJU" and a.get("parametro") == "P-11"
                        and a.get("estado") in ("EN_SOMBRA", "CONFIRMADO"))
        trimestral = sum(abs(a.get("delta", 0)) for a in f6 if a.get("tipo_entrada") == "AJU" and a.get("parametro") == "P-11"
                         and a.get("trimestre") == trimestre)
        delta = 0.05
        if trimestral + delta > 0.05 + 1e-9 or acumulado + delta > 0.15 + 1e-9:
            p3 = {"tipo_entrada": "P3", "id": self.almacen.nuevo_id("P3-EVAL"), "objeto": "P-11 pesos de RK",
                  "motivo": "fuera de banda", "evidencia": {"ic_A": ic_a, "ic_E": ic_e, "n": len(res)},
                  "impacto_esperado": f"Mayor peso de {sube}", "pruebas_regresion": ["PB-35", "PB-36"], "estado": "ENVIADA"}
            self.almacen.escribir("F6", "AG-20", p3)
            return p3
        pesos = dict((self.cfg.get("_parametros_ht03") or {}).get("pesos_rk") or {"A": 0.45, "E": 0.35, "T": 0.20})
        nuevos = dict(pesos)
        nuevos[sube] = round(nuevos[sube] + delta, 4)
        nuevos[baja] = round(nuevos[baja] - delta, 4)
        aju = {"tipo_entrada": "AJU", "id": self.almacen.nuevo_id("AJU"), "parametro": "P-11", "de": pesos, "a": nuevos,
               "delta": delta, "trimestre": trimestre, "banda": {"trimestral": 0.05, "total": 0.15}, "acumulado_vs_inicial": acumulado + delta,
               "evidencia": {"objetivo": "capacidad ordenadora de RK", "ic_A": ic_a, "ic_E": ic_e, "n": len(res)},
               "methodology_version": {"de": self.cfg.get("methodology_version", "FX-1.1"),
                                       "a": _version_menor_siguiente(self.cfg.get("methodology_version", "FX-1.1"))},
               "efecto_desde": str(pd.Timestamp(as_of).date()), "sombra_hasta": str((pd.Timestamp(as_of) + pd.DateOffset(months=3)).date()),
               "estado": "EN_SOMBRA", "aplicado_en_produccion": bool(self.ev_cfg.get("aplicar_recalibracion", False))}
        self.almacen.escribir("F6", "AG-20", aju)
        return aju

    def ajuste_en_sombra(self, as_of) -> Optional[Dict]:
        for a in self.almacen.estado("F6", as_of, clave="id").values():
            if a.get("tipo_entrada") == "AJU" and a.get("estado") == "EN_SOMBRA":
                return a
        return None

    def resolver_hitos(self, as_of, run_id: Optional[str] = None) -> List[Dict]:
        """V1.1 (12.1): los pronósticos H5 se evalúan por sus hitos HIT-FX-, cada uno en su fecha como un pronóstico ordinario
        sobre la serie HT-01 frente al paseo aleatorio (sin cambio). Publica en F6 el resultado de cada hito y el estado del PRG
        H5 (EN_CURSO_CONFORME, DESVIADO o INVALIDADO). F4 no se toca: el PRG H5 sigue ABIERTO hasta su fecha de resolución."""
        as_of = pd.Timestamp(as_of).normalize()
        ya = {r.get("hit_id") for r in self.almacen.leer("F6", as_of) if r.get("tipo_entrada") == "HIT"}
        out = []
        for p in self.almacen.estado("F4", as_of).values():
            if p.get("horizonte") != "H5" or p.get("estado") != "ABIERTO":
                continue
            nivel0 = (p.get("nivel_referencia") or {}).get("valor")
            res_prg = []
            for x in p.get("hitos") or []:
                if x.get("hit_id") in ya or pd.Timestamp(x["fecha"]) > as_of or nivel0 in (None, 0):
                    continue
                try:
                    d1, v1 = self.proveedor.valor_en(x.get("serie_ht01") or p["variable"]["serie_ht01"], pd.Timestamp(x["fecha"]))
                except DatosNoDisponibles:
                    continue
                cambio = float(v1) / float(nivel0) - 1.0
                u = float(x.get("umbral_rel") or 0.0)
                cumplido = cambio >= u if u >= 0 else cambio <= u
                e = {"tipo_entrada": "HIT", "id": f"HITRES-{x['hit_id']}", "hit_id": x["hit_id"], "prg_id": p["prg_id"],
                     "fecha": str(as_of.date()), "fecha_dato": str(pd.Timestamp(d1).date()), "valor_observado": round(cambio, 6),
                     "umbral_rel": u, "resultado": "CUMPLIDO" if cumplido else "NO_CUMPLIDO",
                     "referencia_ingenua": "paseo aleatorio (sin cambio): el hito no se cumple sin movimiento",
                     "comprobacion_fuga": "SUPERADA" if pd.Timestamp(d1) <= as_of else "FALLIDA", "run_id": run_id}
                self.almacen.escribir("F6", "AG-20", e)
                res_prg.append(e)
                out.append(e)
            if res_prg:
                todos = [r for r in self.almacen.leer("F6", as_of) if r.get("tipo_entrada") == "HIT" and r.get("prg_id") == p["prg_id"]]
                fallos = sum(1 for r in todos if r["resultado"] == "NO_CUMPLIDO")
                estado = "EN_CURSO_CONFORME" if fallos == 0 else ("INVALIDADO" if fallos >= 2 else "DESVIADO")
                self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "H5", "id": f"H5EST-{p['prg_id']}-{as_of.date()}",
                                                      "prg_id": p["prg_id"], "estado_h5": estado, "hitos_resueltos": len(todos),
                                                      "hitos_cumplidos": len(todos) - fallos, "fecha": str(as_of.date())})
        return out

    def ciclo(self, as_of, run_id: Optional[str] = None) -> Dict:
        """C5: resolución de vencidos, métricas, certificados, lecciones y recalibración (nunca bloquea C1–C3)."""
        resueltos = self.resolver(as_of, run_id)
        self.resolver_hitos(as_of, run_id)
        metr = self.metricas(as_of)
        if metr:
            self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "MET", "id": f"MET-{pd.Timestamp(as_of).date()}",
                                                  "ventana": f"hasta {pd.Timestamp(as_of).date()}", "metricas": metr,
                                                  "comprobacion_fuga": "SUPERADA", "madurez": "implementado"})
        certs = self.revisar_certificados(as_of, run_id)
        lecciones = self.extraer_lecciones(as_of, metr)
        aju = self.recalibrar(as_of, run_id)
        return {"resueltos": len([r for r in resueltos if r["estado"] == "RESUELTO"]),
                "no_resolubles": len([r for r in resueltos if r["estado"] == "NO_RESOLUBLE"]),
                "metricas": metr, "certificados": certs, "lecciones_nuevas": lecciones, "ajuste": aju}
