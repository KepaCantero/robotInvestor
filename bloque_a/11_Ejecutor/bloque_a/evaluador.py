"""Evaluador de Previsiones y Aprendizaje (AG-20) en el ejecutor: parte determinista.

- Resuelve los PRG- de F4 cuya fecha de resolución es <= as_of, con datos HT-01 vistos con ese as_of
  (sin look-ahead) y el criterio congelado; escribe solo campos de resolución (matriz 5.1).
- Métricas por clase × horizonte (FC-EVAL-001 / FC-CAL-001) y rentabilidad relativa del top-3.
- Certificados de horizonte con el criterio del Anexo A (n ≥ 100, IC 90 % del BSS > 0 con Holm, ECE ≤ q90
  del nulo y < 0,15); revocación por deterioro.
- Lecciones LEC- (predictivas, de calibración y de producto) y recalibración de pesos de RK dentro de
  bandas en modo sombra (o propuesta de tipo 3 si se sale de bandas).
"""
from __future__ import annotations

import math
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats

from .configuracion import CLASES, HORIZONTES
from .herramientas.ht01_datos import DatosNoDisponibles
from .herramientas.ht05_planificador import dias_habiles_entre
from .motor import evaluacion as ev

BANDAS = [(0.80, "MUY_PROBABLE"), (0.60, "MAS_PROBABLE_QUE_NO"), (0.45, "INCIERTO"), (0.25, "POCO_PROBABLE"), (0.0, "MUY_POCO_PROBABLE")]
CADUCIDAD_MESES = {"anecdotica": 3, "recurrente": 6, "estadistica": 12}


def _version_menor_siguiente(v) -> str:
    """12.2: todo ajuste se aplica con una versión menor nueva (p. ej., 5.1 → 5.2)."""
    try:
        mayor, menor = str(v).split(".")[:2]
        return f"{int(mayor)}.{int(menor) + 1}"
    except ValueError:
        return str(v)


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


# Probabilidad representativa de cada banda verbal (Anexo A): solo para uso interno cuando un PRG H5 no
# registra probabilidad interna (V5.1: en H5 solo se registra la banda)
PROB_DE_BANDA = {"MUY_PROBABLE": 0.85, "MAS_PROBABLE_QUE_NO": 0.65, "INCIERTO": 0.5, "POCO_PROBABLE": 0.35, "MUY_POCO_PROBABLE": 0.15}


def banda_publicable(p: float) -> str:
    """Vocabulario de bandas del paquete (esquema JSON del paquete, V4.0–V5.0): tres valores."""
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
    def simbolos_clase(self, clase: str) -> List[str]:
        return [s for s in self.universo[self.universo["clase"] == clase]["simbolo"] if self.proveedor.tiene(s)]

    def rentabilidad(self, simbolo: str, clase: str, f0, f1) -> Tuple[float, pd.Timestamp]:
        if simbolo == "CESTA":
            vals, fechas = [], []
            for s in self.simbolos_clase(clase):
                try:
                    r, f = self.rentabilidad(s, clase, f0, f1)
                    vals.append(r)
                    fechas.append(f)
                except DatosNoDisponibles:
                    continue
            if not vals:
                raise DatosNoDisponibles(f"Cesta {clase} sin datos")
            return float(np.mean(vals)), max(fechas)
        d0, v0 = self.proveedor.valor_en(simbolo, f0)
        d1, v1 = self.proveedor.valor_en(simbolo, f1)
        return v1 / v0 - 1, d1

    def tasa_base(self, proxy: str, referencia: Optional[str], clase: str, sesiones: int, sentido_positivo: bool,
                  as_of, run_id: Optional[str] = None) -> Dict:
        """RI-TB: frecuencia histórica (ventanas no solapadas de 3 años hasta as_of) del suceso pronosticado."""
        ini = pd.Timestamp(as_of) - pd.DateOffset(years=3)
        s = self.proveedor.cierres(proxy, ini, as_of)
        serie = s.pct_change(sesiones).iloc[sesiones::sesiones] if len(s) > sesiones else pd.Series(dtype=float)
        if referencia and referencia != proxy:
            if referencia == "CESTA":
                comp = [self.proveedor.cierres(x, ini, as_of).pct_change(sesiones) for x in self.simbolos_clase(clase)]
                ref = pd.concat(comp, axis=1).mean(axis=1)
            else:
                ref = self.proveedor.cierres(referencia, ini, as_of).pct_change(sesiones)
            serie = (serie - ref.reindex(serie.index)).dropna()
        serie = serie.dropna()
        if len(serie) < 5:
            p = 0.5
        else:
            p = float(np.mean(serie > 0)) if sentido_positivo else float(np.mean(serie < 0))
        p = min(max(p, 0.05), 0.95)
        # Registro en RC (operación de la familia FC-EVAL-001: referencia RI-TB)
        calc_id = self.almacen.nuevo_id("CALC")
        self.almacen.escribir("RC", "AG-13", {
            "tipo_entrada": "SERVICIO", "calc_id": calc_id, "contrato": "CT-09", "run_id": run_id, "solicitante": "AG-10",
            "operacion": {"method_id": "RI-TB", "ficha_id": "FC-EVAL-001", "ficha_version": "1.0", "catalog_version": "4.0",
                          "op_sin_ficha": False}, "perfil": ["TRANSVERSAL"], "clase": clase, "modo": "SYNC_CALC",
            "plan": "PLAN_MIN", "as_of": str(pd.Timestamp(as_of).date()), "estado": "SERVED",
            "datos": [{"serie_ht01": proxy, "fecha_dato": str(s.index[-1].date()) if len(s) else None, "n": int(len(s))},
                      {"serie_ht01": referencia}],
            "parametros": {"sesiones": sesiones, "sentido_positivo": sentido_positivo, "ventana": "3 años, no solapadas"},
            "semilla": None, "resultado": {"forma": "VALOR", "payload": {"tasa_base": p, "n_ventanas": int(len(serie))}},
            "clase_cifra": "ESTADISTICA", "referencia_ingenua": {"tipo": "RI-TB"}, "madurez_metodo": "IMPLEMENTADO",
            "consumo_uc": 0.0, "limitaciones": [] if len(serie) >= 5 else ["menos de 5 ventanas: tasa base 0,5 por defecto"]})
        return {"tipo": "TASA_BASE", "valor_o_prob": round(p, 4), "calc_id": calc_id, "n_ventanas": int(len(serie))}

    # ------------------------------------------------------------------------------------
    # Resolución
    # ------------------------------------------------------------------------------------
    def resolver(self, as_of, run_id: Optional[str] = None) -> List[Dict]:
        as_of = pd.Timestamp(as_of).normalize()
        abiertos = [p for p in self.almacen.estado("F4", as_of).values() if p.get("estado") == "ABIERTO"]
        # V5.1: los PRG H5 (sin probabilidad interna) no se puntúan con Brier: se evalúan por sus hitos HIT-,
        # que son pronósticos ordinarios de su propio horizonte y se resuelven aquí como los demás
        pendientes = [p for p in abiertos if pd.Timestamp(p["fecha_resolucion"]) <= as_of and p.get("prob_interna") is not None]
        resueltos: List[Dict] = []
        filas = []
        for p in sorted(pendientes, key=lambda x: x["prg_id"]):
            f0, f1 = pd.Timestamp(p["fecha_emision"]), pd.Timestamp(p["fecha_resolucion"])
            try:
                rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["clase"], f0, f1)
                rr = None
                if p["tipo_pronostico"] == "RELATIVO":
                    rr, d1b = self.rentabilidad(p["referencia_indice"], p["clase"], f0, f1)
                    d1 = max(d1, d1b)
            except DatosNoDisponibles:
                if dias_habiles_entre(f1, as_of) >= int(self.ev_cfg.get("dias_habiles_no_resoluble", 10)):
                    filas.append((p, None))
                continue
            if (f1 - d1).days > 7:   # el último dato es demasiado antiguo: esperar
                if dias_habiles_entre(f1, as_of) >= int(self.ev_cfg.get("dias_habiles_no_resoluble", 10)):
                    filas.append((p, None))
                continue
            x = rp - rr if rr is not None else rp
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
                                    "rent_referencia": None if r["rent_referencia"] is None else round(r["rent_referencia"], 8),
                                    "unidad": "tanto por uno", "fuente_usada": f"HT-01:{self.proveedor.nombre}",
                                    "vintage": str(as_of.date()), "fallback_aplicado": False,
                                    "resultado": "OCURRIDO" if o else "NO_OCURRIDO", "resultado_binario": o,
                                    "puntuaciones": {"brier": (pi - o) ** 2, "log": -math.log(min(max(pi if o else 1 - pi, 0.01), 0.99)),
                                                     "brier_ref": (pr - o) ** 2,
                                                     "log_ref": -math.log(min(max(pr if o else 1 - pr, 0.01), 0.99))},
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
        """Métricas por clase × horizonte. `completas` añade bootstrap del BSS, ECE con nulo y DM-HLN."""
        celdas: Dict[Tuple[str, str], List[Dict]] = defaultdict(list)
        for p in self.resueltos(as_of, solo_informe):
            celdas[(p["clase"], p["horizonte"])].append(p)
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
            informe = [x for x in lst if x.get("en_informe")]
            rel = [x["resolucion"]["valor_observado"] * (1 if x["sentido"] == "POSITIVO" else -1) for x in informe]
            m["rentabilidad_relativa_media_top3"] = float(np.mean(rel)) if rel else None
            m["n_top3"] = len(informe)
            m["referencia"] = lst[0].get("referencia_indice")
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
            return {"n": n, "aciertos": k, "tasa_acierto": round(k / n, 4) if n else None, "referencia": ref_txt,
                    "tasa_esperada_azar": round(pr, 4), "significativo": sig, "por_horizonte": dict(ph)}
        por_clase = {}
        for c in CLASES:
            xs = [x for x in lst if x["clase"] == c]
            if xs:
                por_clase[c] = celda(xs, f"Tasa base sin fuga del mismo suceso (RI-TB) frente a {xs[0].get('referencia_indice') or 'el propio activo'}")
        g = celda(lst, "Tasa base sin fuga (RI-TB) de cada pronóstico")
        nota = (f"Ventana de {semanas} semanas; {g['n']} pronósticos de opciones publicadas resueltos"
                + (f"; {len(no_res)} no resolubles excluidos y declarados" if no_res else "")
                + ("; muestra pequeña (< 30): la diferencia frente al azar puede deberse a la suerte" if g["n"] < 30 else ""))
        return {"ventana": f"{semanas} semanas", "global": g, "por_clase": por_clase, "nota": nota}

    # ------------------------------------------------------------------------------------
    # Certificados, lecciones y recalibración
    # ------------------------------------------------------------------------------------
    def estado_h5(self, as_of=None) -> Dict[str, Dict]:
        """V5.1 (12.1): estado de cada PRG H5 a partir de sus hitos resueltos y tasa de hitos cumplidos por celda tipo × H5.
        EN_CURSO_CONFORME: como mucho un hito fallado y no el último; DESVIADO: dos o más fallados o el último fallado;
        INVALIDADO: falla un hito marcado como necesario."""
        f4 = self.almacen.estado("F4", as_of)
        out: Dict[str, Dict] = {}
        celdas: Dict[str, List[int]] = defaultdict(list)
        for p in f4.values():
            if p.get("horizonte") != "H5" or p.get("es_hito"):
                continue
            hitos = sorted((f4.get(h) or {} for h in p.get("hit_ids", [])), key=lambda x: str(x.get("fecha_resolucion")))
            res = [int(h["resolucion"]["resultado_binario"]) for h in hitos if h.get("estado") == "RESUELTO" and h.get("resolucion")]
            fallos = res.count(0)
            if any(h.get("necesario") and h.get("estado") == "RESUELTO" and not (h.get("resolucion") or {}).get("resultado_binario")
                   for h in hitos):
                est = "INVALIDADO"
            elif fallos >= 2 or (res and res[-1] == 0):
                est = "DESVIADO"
            else:
                est = "EN_CURSO_CONFORME"
            out[p["prg_id"]] = {"estado": est, "hitos_resueltos": len(res), "hitos_cumplidos": sum(res), "hitos_totales": len(hitos)}
            celdas[p["clase"]].extend(res)
        resumen = {c: {"n": len(v), "tasa_cumplidos": round(sum(v) / len(v), 4) if v else None,
                       "degradar": bool(len(v) >= 20 and sum(v) / len(v) < 0.5)} for c, v in celdas.items()}
        return {"pronosticos": out, "celdas": resumen}

    def certificados_vigentes(self, as_of=None) -> List[Dict]:
        return [c for c in self.almacen.estado("F6", as_of, clave="id").values()
                if c.get("tipo_entrada") in ("CERT", "CERT_REVOCACION") and c.get("estado") == "VIGENTE"]

    def revisar_certificados(self, as_of, run_id: Optional[str] = None) -> Dict:
        n_cert = int(self.ev_cfg.get("min_certificar", 100))
        celdas = defaultdict(list)
        for p in self.resueltos(as_of):
            celdas[(p["clase"], p["horizonte"])].append(p)
        candidatas = {k: v for k, v in celdas.items() if len(v) >= n_cert}
        vigentes = {(c["celda"]["clase"], c["celda"]["horizonte"]): c for c in self.certificados_vigentes(as_of)}
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
                            "celda": {"clase": k[0], "horizonte": k[1], "metodo": None}, "n": m["n"],
                            "brier": m["brier"], "brier_ref": m["brier_ref"], "bss": m["bss"]["valor"], "bss_ic90": m["bss"]["ic"],
                            "holm_superado": True, "ece": m["calibracion"]["ece"], "ece_nulo_q90": m["ece_nulo"]["q90"],
                            "methodology_version": self.cfg.get("methodology_version", "4.0"), "emitido": str(pd.Timestamp(as_of).date())}
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

    def lecciones_vigentes(self, as_of, clase: Optional[str] = None, max_n: int = 10) -> List[Dict]:
        orden = {"estadistica": 0, "recurrente": 1, "anecdotica": 2}
        lst = []
        for l in self.almacen.estado("F6", as_of, clave="id").values():
            if l.get("tipo_entrada") != "LEC" or l.get("estado") != "VIGENTE":
                continue
            if pd.Timestamp(l["caducidad"]) < pd.Timestamp(as_of):
                continue
            amb = l.get("ambito") or {}
            if clase and amb.get("clase") not in (None, clase):
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
                l = self._nueva_leccion(as_of, {"clase": c, "horizonte": h}, "PREDICTIVA",
                                        f"Acierto {tasa:.0%} en {n} pronósticos de {c}×{h}, por debajo de la tasa base.",
                                        "Rebajar un nivel la banda verbal y exigir catalizador fechado antes de proponer en esta celda.",
                                        fuerza, [f"MET:{celda}"], n)
                if l:
                    nuevas.append(l)
            cg = m.get("calibracion_global") or {}
            if cg and cg.get("p_media") is not None and cg["p_media"] - cg["frecuencia"] >= 0.10:
                l = self._nueva_leccion(as_of, {"clase": c, "horizonte": h}, "CALIBRACION",
                                        f"Sobreconfianza en {c}×{h}: probabilidad media {cg['p_media']:.2f} frente a frecuencia {cg['frecuencia']:.2f} (n = {n}).",
                                        "Acercar la probabilidad interna a la tasa base (máximo 0,60) hasta que la calibración mejore.",
                                        fuerza, [f"MET:{celda}"], n)
                if l:
                    nuevas.append(l)
        return nuevas

    def leccion_producto(self, as_of, tema: str, qry_ids: List[str]) -> Optional[Dict]:
        return self._nueva_leccion(as_of, {"clase": None, "horizonte": None, "agente": ["AG-17", "AG-02"]}, "PRODUCTO",
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
               "methodology_version": {"de": self.cfg.get("methodology_version", "5.1"), "a": _version_menor_siguiente(self.cfg.get("methodology_version", "5.1"))},
               "efecto_desde": str(pd.Timestamp(as_of).date()), "sombra_hasta": str((pd.Timestamp(as_of) + pd.DateOffset(months=3)).date()),
               "estado": "EN_SOMBRA", "aplicado_en_produccion": bool(self.ev_cfg.get("aplicar_recalibracion", False))}
        self.almacen.escribir("F6", "AG-20", aju)
        return aju

    def ajuste_en_sombra(self, as_of) -> Optional[Dict]:
        for a in self.almacen.estado("F6", as_of, clave="id").values():
            if a.get("tipo_entrada") == "AJU" and a.get("estado") == "EN_SOMBRA":
                return a
        return None

    def ciclo(self, as_of, run_id: Optional[str] = None) -> Dict:
        """C5: resolución de vencidos, métricas, certificados, lecciones y recalibración (nunca bloquea C1–C3)."""
        resueltos = self.resolver(as_of, run_id)
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
