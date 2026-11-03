"""Evaluador de Previsiones, Aprendizaje y Seguimiento (AG-B23, fase F12): resuelve los PRG-B vencidos sin fuga de
información, evalúa los rankings de candidatos (rentabilidad del top-N frente a la media equiponderada del universo
cribado e IC de rango de Spearman), mide calibración, emite certificados solo con las condiciones de R13/12.3, extrae
lecciones y recalibra el modelo de tiempos en modo sombra (dentro de bandas)."""
from __future__ import annotations

import datetime as dt

import math
from typing import Dict, List, Optional

import numpy as np

from .herramientas import ht08
from .motor import brier, ic_bootstrap_media, spearman


def _media(xs: List[float]) -> Optional[float]:
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None


def resolver_pendientes(ent) -> List[Dict]:
    alm, motor = ent.alm, ent.motor
    hoy = ent.as_of
    resueltos = []
    for prg_id, p in alm.estado("F4").items():
        if p.get("estado") != "ABIERTO" or p.get("fecha_resolucion", "9999") > hoy:
            continue
        ini, fin = p["fecha_emision"], p["fecha_resolucion"]
        res: Dict = {"fecha_resuelto": hoy, "comprobacion_fuga": f"datos ≤ {fin} con fecha de corte {hoy}"}
        if p.get("tipo") in ("AMBITO", "HITO_H5"):      # HITO_H5: hito intermedio de una tesis H5 (12.8; referencia ingenua RI-LIN)
            ra = motor.rentabilidad(p.get("indicador"), ini, fin)
            rb = motor.rentabilidad(p.get("referencia"), ini, fin) if p.get("referencia") != p.get("indicador") else 0.0
            if ra is None or rb is None:
                alm.escribir("F4", "AG-B23", {"tipo_entrada": "RESOLUCION", "id": prg_id, "estado": "NO_RESOLUBLE", "resolucion": {"motivo": "sin datos"}})
                continue
            rel = (1 + ra) / (1 + rb) - 1
            y = int(rel > 0)
            q = p.get("probabilidad_interna") or 0.5
            res.update({"rent_indicador": round(ra, 6), "rent_referencia": round(rb, 6), "relativa": round(rel, 6), "acierto": bool(y),
                        "brier": round((q - y) ** 2, 6), "brier_ref": 0.25})
            if p.get("tipo") == "HITO_H5":
                res["hito"] = "CUMPLIDO" if y else "NO_CUMPLIDO"
        else:
            top = [s for s in p.get("top_n_simbolos") or [] if s]
            uni = [s for s in p.get("universo_simbolos") or [] if s]
            r_top = [motor.rentabilidad(s, ini, fin) for s in top]
            r_uni = [motor.rentabilidad(s, ini, fin) for s in uni]
            mt, mu = _media(r_top), _media(r_uni)
            if mt is None or mu is None:
                alm.escribir("F4", "AG-B23", {"tipo_entrada": "RESOLUCION", "id": prg_id, "estado": "NO_RESOLUBLE", "resolucion": {"motivo": "sin datos"}})
                continue
            S = p.get("universo_S") or {}
            pares = [(S.get(s), r) for s, r in zip(uni, r_uni) if S.get(s) is not None and r is not None]
            ic = spearman([a for a, _ in pares], [b - mu for _, b in pares]) if len(pares) >= 3 else None
            res.update({"rent_top_n": round(mt, 6), "rent_universo": round(mu, 6), "exceso": round(mt - mu, 6), "acierto": mt > mu,
                        "ic_rango": None if ic is None else round(ic, 4), "tratamiento_bajas": "último precio disponible"})
        alm.escribir("F4", "AG-B23", {"tipo_entrada": "RESOLUCION", "id": prg_id, "estado": "RESUELTO", "resolucion": res})
        alm.escribir("F3", "AG-B23", {"tipo_entrada": "RESULTADO", "id": p.get("rec_id"), "prg_id": prg_id, "acierto": res.get("acierto")})
        resueltos.append({"prg_id": prg_id, **res})
    return resueltos


def metricas(ent) -> Dict:
    cfg = ent.cfg.get("evaluacion") or {}
    celdas: Dict[str, Dict[str, List]] = {}
    for prg_id, p in ent.alm.estado("F4").items():
        if p.get("estado") != "RESUELTO":
            continue
        r = p.get("resolucion") or {}
        c = celdas.setdefault(f"{p.get('tipo')}|{p.get('celda')}", {"y": [], "q": [], "exceso": [], "ic": []})
        c["y"].append(int(bool(r.get("acierto"))))
        c["q"].append(p.get("probabilidad_interna") or 0.5)
        if r.get("exceso") is not None:
            c["exceso"].append(r["exceso"])
        if r.get("ic_rango") is not None:
            c["ic"].append(r["ic_rango"])
    out, certificados = {}, []
    for k, c in celdas.items():
        n = len(c["y"])
        b = brier(c["q"], c["y"])
        base = float(np.mean(c["y"])) if n else None
        bss = None if not n or base in (0, 1) else 1 - b / (base * (1 - base))
        m = {"n": n, "acierto": round(float(np.mean(c["y"])), 4) if n else None, "brier": None if b is None else round(b, 4),
             "bss_frente_a_climatologia": None if bss is None else round(bss, 4)}
        if c["exceso"]:
            m.update({"exceso_medio_top_n": round(float(np.mean(c["exceso"])), 6), "ic90_exceso": ic_bootstrap_media(c["exceso"], int(cfg.get("bootstrap_replicas", 1000)))})
        if c["ic"]:
            m.update({"ic_rango_medio": round(float(np.mean(c["ic"])), 4), "ic90_ic_rango": ic_bootstrap_media(c["ic"], int(cfg.get("bootstrap_replicas", 1000)))})
        if k.startswith("RANKING") and n >= int(cfg.get("certificado_ranking_n", 30)) and (m.get("ic90_exceso") or [0])[0] > 0 \
                and (m.get("ic90_ic_rango") or [0])[0] > 0:
            certificados.append({"tipo": "ranking", "celda": k.split("|", 1)[1], "n": n})
        if k.startswith("AMBITO") and n >= int(cfg.get("certificado_probabilidad_n", 100)) and bss is not None and bss > 0:
            m["nota_certificado"] = "candidata: falta IC 90 % del BSS > 0, ECE frente a su nulo y Holm (implementación pendiente)"
        m["muestra_suficiente_recalibrar"] = n >= (int(cfg.get("muestra_minima_recalibrar_rankings", 15)) if k.startswith("RANKING")
                                                   else int(cfg.get("muestra_minima_recalibrar_pronosticos", 30)))
        out[k] = m
    return {"celdas": out, "certificados": certificados}


def recalibrar_tiempos(ent) -> Dict:
    hist = []
    for e in ent.alm.leer("F1"):
        if e.get("tipo_entrada") != "ENTREGA" or not e.get("tiempos_por_tramo"):
            continue
        est = e.get("estimacion_fases") or {}
        for tramo, real in e["tiempos_por_tramo"].items():
            if tramo in ("F2L", "F2R", "F3P"):          # V2.1: tramos de capa que reparten una fase (7.3)
                fase, frac = {"F2L": ("F2", 0.5), "F2R": ("F2", 0.5), "F3P": ("F3", 0.4)}[tramo]
                if est.get(fase):
                    hist.append({"fase": fase, "estimado_p50": est[fase] * frac, "real": real})
            elif tramo == "F3" and est.get("F3"):
                hist.append({"fase": "F3", "estimado_p50": est["F3"] * 0.6, "real": real})
            elif tramo == "F4F5":
                hist.append({"fase": "F5", "estimado_p50": max(est.get("F4", 0), est.get("F5", 0)), "real": real})
            elif est.get(tramo):
                hist.append({"fase": tramo, "estimado_p50": est[tramo], "real": real})
    return ht08.recalibrar(hist, (ent.cfg.get("puerta_tiempo") or {}).get("modelo"))


def puertas_consultas_seguimientos(ent) -> Dict:
    """Aprendizaje de las puertas, las consultas y los seguimientos (12.7) y evaluación de H5 por hitos (12.8)."""
    alm, motor = ent.alm, ent.motor
    f1 = alm.leer("F1")
    paradas = [e for e in f1 if e.get("tipo_entrada") == "PARADA_PUERTA"]
    recs = alm.estado("F3")
    fn, evaluadas = [], 0
    for e in paradas:
        rec = recs.get(e["pet_id"].replace("PET-B-", "REC-B-")) or {}
        hz = rec.get("horizonte") or "H3"
        dias = {"H1": 14, "H2": 60, "H3": 365, "H4": 730, "H5": 1825}[hz]
        fin = (dt.date.fromisoformat(e["_fecha"]) + dt.timedelta(days=dias)).isoformat()
        if fin > ent.as_of:
            continue
        ind, ref = (rec.get("indicador") or {}).get("simbolo"), (rec.get("referencia") or {}).get("simbolo")
        ra, rb = motor.rentabilidad(ind, e["_fecha"], fin), motor.rentabilidad(ref, e["_fecha"], fin) if ref and ref != ind else 0.0
        if ra is None or rb is None:
            continue
        evaluadas += 1
        exceso_anual = ((1 + ra) / (1 + rb)) ** (365 / dias) - 1
        if exceso_anual > 0.10:
            fn.append({"pet_id": e["pet_id"], "puerta": e["puerta"], "exceso_anualizado": round(exceso_anual, 4)})
    cons = [e for e in alm.estado("F1", tipo="CONSULTA_BROKER").values() if e.get("sentido") == "SALIENTE"]
    cics = [c for c in alm.estado("F11", tipo="CIC").values() if c.get("estado") == "ENTREGADO"]
    hitos = [p for p in alm.estado("F4").values() if p.get("tipo") == "HITO_H5" and p.get("estado") == "RESUELTO"]
    return {"puertas": {"paradas": {g: sum(1 for e in paradas if e.get("puerta") == g) for g in ("PV1", "PV2")},
                        "continuaciones_forzadas": sum(1 for e in f1 if e.get("tipo_entrada") == "CONTINUACION_FORZADA"),
                        "evaluadas": evaluadas, "falsos_negativos": fn},
            "consultas": {"n": len(cons), "respondidas": sum(1 for e in cons if e.get("estado") == "RESPONDIDA"),
                          "supuesto_aplicado": sum(1 for e in cons if e.get("estado") == "SUPUESTO_APLICADO"),
                          "supuesto_cambiado": sum(1 for e in cons if e.get("efecto") in ("SUPUESTO_CAMBIADO", "CONCLUSION_CAMBIADA"))},
            "seguimientos": {"ciclos": len(cics), "por_semaforo": {k: sum(1 for c in cics if c.get("semaforo") == k) for k in ("VERDE", "AMBAR", "ROJO")},
                             "uc_media_ciclo": round(float(np.mean([c.get("uc") or 0 for c in cics])), 2) if cics else None},
            "hitos_h5": {"resueltos": len(hitos), "cumplidos": sum(1 for p in hitos if (p.get("resolucion") or {}).get("acierto")),
                         "tasa": round(sum(1 for p in hitos if (p.get("resolucion") or {}).get("acierto")) / len(hitos), 4) if hitos else None}}


def evaluar(ent, coord) -> Dict:
    resueltos = resolver_pendientes(ent)
    v21 = puertas_consultas_seguimientos(ent)
    ent.alm.escribir("F5", "AG-B23", {"tipo_entrada": "METRICAS_V21", "id": ent.alm.nuevo_id("MET-B"), **v21})
    for x in v21["puertas"]["falsos_negativos"]:
        ent.alm.escribir("F5", "AG-B23", {"tipo_entrada": "LECCION", "id": ent.alm.nuevo_id("LEC-B"), "ambito": "puertas", "agentes": ["AG-B02"],
                                          "observacion": f"Falso negativo de {x['puerta']} en {x['pet_id']}: exceso anualizado {x['exceso_anualizado']:+.1%}",
                                          "recomendacion": "Revisar los criterios de la puerta en celdas similares", "fuerza": "anecdotica"})
    m = metricas(ent)
    rt = recalibrar_tiempos(ent)
    alm = ent.alm
    for cert in m["certificados"]:
        alm.escribir("F5", "AG-B23", {"tipo_entrada": "CERTIFICADO", "id": alm.nuevo_id("CERT-B"), **cert})
    alm.escribir("F5", "AG-B23", {"tipo_entrada": "METRICAS", "id": alm.nuevo_id("MET-B"), "metricas": m["celdas"]})
    alm.escribir("F5", "AG-B23", {"tipo_entrada": "MODELO_TIEMPOS", "id": alm.nuevo_id("MOD-B"), "propuesta": rt,
                                  "aplicado": bool((ent.cfg.get("evaluacion") or {}).get("aplicar_recalibracion")), "modo": "sombra"})
    lec = []
    if resueltos:
        r = ent.inv.llamar("AG-B23", "CT-B-22", "lecciones", {"resueltos": resueltos[:30], "metricas": m["celdas"]},
                           "Extrae lecciones verificables (LEC-B) de los resultados resueltos.", {"lecciones": "array"}, coord._ctx("AG-B23"))
        for l in r.get("lecciones") or []:
            if isinstance(l, dict) and l.get("observacion"):
                lid = alm.nuevo_id("LEC-B")
                alm.escribir("F5", "AG-B23", {"tipo_entrada": "LECCION", "id": lid, **{k: l.get(k) for k in ("ambito", "observacion", "recomendacion", "fuerza")}})
                lec.append(lid)
    return {"fecha_corte": ent.as_of, "resueltos": len(resueltos), "metricas": m["celdas"], "certificados": m["certificados"],
            "lecciones": lec, "modelo_tiempos": rt, "puertas_consultas_seguimientos": v21}
