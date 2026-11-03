"""Vigía (función de AG-B23, fase F11): compara las señales del `plan_de_seguimiento` de cada REC-B vigente con sus
umbrales y avisa al Coordinador (CT-B-25), que transmite la alerta al Broker (CT-B-07). Nunca abre un análisis ni
modifica un veredicto entregado (R32): como mucho sugiere una petición nueva."""
from __future__ import annotations

import datetime as dt
import json
from typing import Dict, List, Optional

from .herramientas.ht01_datos import DatosNoDisponibles

ORDEN = {"FLUCTUACION": 0, "REVISION": 1, "INVALIDACION_PROBABLE": 2, "INVALIDACION_CONFIRMADA": 3}


def valor_senal(prov, serie: str, fecha_entrega: str) -> Optional[float]:
    """Interpreta las series del plan: «HT-01:REL:A/B» (rentabilidad relativa a 63 sesiones, %) y «HT-01:NIVEL:A»
    (variación % desde el cierre de la fecha de corte de la entrega)."""
    try:
        partes = serie.split(":")
        if len(partes) < 3:
            return None
        if partes[1] == "REL":
            a, b = partes[2].split("/")
            sa, sb = prov.cierres(a), prov.cierres(b)
            if len(sa) < 64 or len(sb) < 64:
                return None
            ra = sa.iloc[-1] / sa.iloc[-64] - 1
            rb = sb.iloc[-1] / sb.iloc[-64] - 1 if a != b else 0.0
            return round(100 * ((1 + ra) / (1 + rb) - 1), 2)
        if partes[1] == "NIVEL":
            _, v0 = prov.valor_en(partes[2], fecha_entrega)
            s = prov.cierres(partes[2])
            return round(100 * (float(s.iloc[-1]) / v0 - 1), 2)
    except (DatosNoDisponibles, ValueError, KeyError):
        return None
    return None


def clasificar(valor: float, s: Dict, previa: Optional[str]) -> Optional[str]:
    abajo = s["direccion"] == "por_debajo"
    pasa = (lambda u: valor <= u) if abajo else (lambda u: valor >= u)
    if pasa(s["umbral_invalidacion"]):
        return "INVALIDACION_CONFIRMADA" if previa in ("INVALIDACION_PROBABLE", "INVALIDACION_CONFIRMADA") else "INVALIDACION_PROBABLE"
    if pasa(s["umbral_revision"]):
        return "REVISION"
    f = s["umbral_fluctuacion"]
    if valor < f["min"] or valor > f["max"]:
        return "FLUCTUACION"
    return None


def ronda(ent, coord) -> Dict:
    alm = ent.alm
    hoy = ent.as_of
    previas: Dict[str, str] = {}
    for e in alm.leer("F3"):
        if e.get("tipo_entrada") == "ALERTA":
            previas[e["sig_id"]] = e["clasificacion"]
    alertas, lecturas = [], 0
    for rec_id, r in alm.estado("F3").items():
        if not str(rec_id).startswith("REC-B-") or r.get("estado_vigilancia") not in ("VIGENTE", "EN_REVISION"):
            continue
        plan = r.get("plan_de_seguimiento") or {}
        if plan.get("vigente_hasta") and hoy > plan["vigente_hasta"]:
            alm.escribir("F3", "AG-B23", {"tipo_entrada": "SEGUIMIENTO", "id": rec_id, "estado_vigilancia": "CERRADA", "motivo": "horizonte vencido"})
            continue
        fecha_entrega = r["_historial"][0]["fecha"]
        for s in plan.get("senales") or []:
            v = valor_senal(ent.prov, s["serie"], fecha_entrega)
            lecturas += 1
            if v is None:
                continue
            cl = clasificar(v, s, previas.get(s["sig_id"]))
            if cl is None:
                continue
            if cl == "FLUCTUACION":   # se registra y no se envía (B.7)
                alm.escribir("F3", "AG-B23", {"tipo_entrada": "ALERTA", "id": rec_id, "sig_id": s["sig_id"], "clasificacion": cl, "valor": v,
                                              "fecha_corte": hoy})
                continue
            if previas.get(s["sig_id"]) == cl:
                continue     # misma clasificación ya comunicada
            alr = alm.nuevo_id("ALR-B")
            interp = ent.inv.llamar("AG-B23", "CT-B-25", "interpretacion_alerta",
                                    {"rec_id": rec_id, "senal": s, "valor_observado": v, "clasificacion": cl},
                                    "Interpreta la señal (fluctuación frente a cambio estructural) y sugiere la acción; no abras análisis.",
                                    {"interpretacion": "string"}, coord._ctx("AG-B23"))
            sev = {"REVISION": "MEDIA", "INVALIDACION_PROBABLE": "ALTA", "INVALIDACION_CONFIRMADA": "ALTA"}[cl]
            accion = "CONSULTA_N0" if cl == "REVISION" else "NUEVA_PETICION_SUGERIDA"
            alerta = {"alr_id": alr, "rec_id": rec_id, "pet_id": r.get("pet_id"), "cand_ids": [x for x in s["afecta_a"] if x.startswith("CAND-B-")],
                      "fecha_corte": hoy, "senal": {"sig_id": s["sig_id"], "nombre": s["nombre"], "serie": s["serie"], "valor_observado": v,
                                                    "umbral": s["umbral_invalidacion"] if cl.startswith("INVALIDACION") else s["umbral_revision"],
                                                    "direccion": s["direccion"]},
                      "clasificacion": cl, "severidad": sev, "evidencia": [],
                      "interpretacion": interp.get("interpretacion") or "Señal fuera de su umbral.",
                      "efecto": {"veredicto_en_riesgo": cl != "REVISION", "candidatos_afectados": [x for x in s["afecta_a"] if x.startswith("CAND-B-")],
                                 "pronosticos_afectados": [p["prg_id"] for p in plan.get("pronosticos_a_resolver") or []]},
                      "accion_sugerida": accion,
                      "peticion_sugerida": {"nivel": "N1", "alcance": f"Revisión de {r.get('ambito', {}).get('nombre', rec_id)}", "estimacion_min_p80": 10}
                      if accion == "NUEVA_PETICION_SUGERIDA" else None,
                      "nota": "El bloque no ha iniciado ningún análisis."}
            alm.escribir("F3", "AG-B23", {"tipo_entrada": "ALERTA", "id": rec_id, "sig_id": s["sig_id"], "alr_id": alr, "clasificacion": cl,
                                          "valor": v, "fecha_corte": hoy})
            nuevo = {"REVISION": "EN_REVISION", "INVALIDACION_PROBABLE": "EN_REVISION", "INVALIDACION_CONFIRMADA": "INVALIDADA"}[cl]
            alm.escribir("F3", "AG-B23", {"tipo_entrada": "SEGUIMIENTO", "id": rec_id, "estado_vigilancia": nuevo, "ultima_alerta": alr})
            alm.escribir("F1", "AG-B01", {"tipo_entrada": "ALERTA_TRANSMITIDA", "id": alr, "rec_id": rec_id, "ct_b_07": alerta})
            dirs = ent.salida / "Alertas"
            dirs.mkdir(parents=True, exist_ok=True)
            (dirs / f"{hoy}_alerta_{alr}.json").write_text(json.dumps(alerta, ensure_ascii=False, indent=1), encoding="utf-8")
            alertas.append(alerta)
    return {"fecha_corte": hoy, "lecturas": lecturas, "alertas": alertas,
            "nota": "Ronda del Vigía: solo compara señales con umbrales; no abre análisis (R32)."}
