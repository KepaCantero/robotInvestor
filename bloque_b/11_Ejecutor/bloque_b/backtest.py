"""Backtest de rankings de candidatos y de pronósticos del ámbito, sin anticipación.

Para cada fecha de corte (mensual o semanal) se ejecuta la petición completa como si esa fuera la fecha actual (HT-01
con guardia as_of; F1–F6 filtrados por fecha; búsqueda web desactivada) o, con `solo_seleccion`, solo la parte
determinista de la selección (HT-11 → Motor → HT-03). Al terminar se avanza la fecha hasta el final de los datos y se
miden, por fecha y tipo de activo: rentabilidad del top-N equiponderado frente a la media equiponderada del universo
cribado (referencia del ranking, 9.11) y frente a la referencia del ámbito, IC de rango (Spearman entre S y la
rentabilidad posterior relativa al universo) y tasa de acierto, con IC 90 % por bootstrap. Exporta rankings.csv,
pronosticos.csv, metricas.json, consumo.csv y los entregables de la última fecha."""
from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from . import evaluador
from .herramientas import ht03, ht11
from .motor import ic_bootstrap_media, spearman


def fechas_corte(desde: str, hasta: str, frecuencia: str = "mensual") -> List[str]:
    d = pd.bdate_range(desde, hasta)
    if frecuencia == "semanal":
        d = d[d.weekday == 4]
    elif frecuencia == "mensual":
        d = pd.Series(d).groupby([d.year, d.month]).max().values
    return [str(pd.Timestamp(x).date()) for x in d]


def seleccion_rapida(ent, clave: str, tipo: str, nivel: str = "N2", horizonte: str = "H3") -> List[Dict]:
    amb = ent.ambitos[clave]
    u = ht11.construir_universo(tipo, [{"nombre": f"universo_{tipo}", "filas": ent.universos[tipo]}], ent.as_of, clave, horizonte,
                                ent.cfg.get("marco_invertibilidad"))
    filas = [dict(f, cand_id=f"{tipo}:{f['id']}") for f in u["incluidos"]]
    if not filas:
        return []
    punt = ent.motor.puntuar(tipo, filas, (amb.get("referencia") or {}).get("simbolo"), horizonte, 7, "MIN")
    cands = [{"cand_id": f["cand_id"], "S": punt["candidatos"][f["cand_id"]]["S"], "componentes": punt["candidatos"][f["cand_id"]]["componentes"],
              "ic90_S": punt["candidatos"][f["cand_id"]].get("ic90_S"), "ic90_rango": punt["candidatos"][f["cand_id"]].get("ic90_rango"),
              "pureza": float(f["pureza"]) if f.get("pureza") else None, "subcluster": f.get("subcluster") or None, "emisor": f.get("emisor"),
              "indice_replicado": f.get("indice_replicado") or None,
              "alertas": [{"senal": a, "critica": True} for a in (f.get("alertas_criticas") or "").split(";") if a]} for f in filas]
    sel = ht03.seleccionar(cands, tipo, nivel, "INVERTIR")
    top = {c["cand_id"]: c for c in sel["top_n"]}
    out = []
    for f in filas:
        c = next(x for x in cands if x["cand_id"] == f["cand_id"])
        out.append({"cand_id": f["cand_id"], "tipo_activo": tipo, "simbolo": f.get("simbolo"), "nombre": f.get("nombre"), "S": c["S"],
                    "en_top_n": f["cand_id"] in top, "rango": (top.get(f["cand_id"]) or {}).get("rango"),
                    "veredicto": (top.get(f["cand_id"]) or {}).get("veredicto") or "FUERA_TOP_N"})
    return out


def _fin_horizonte(fecha: str, sesiones: int) -> str:
    return str((pd.Timestamp(fecha) + pd.offsets.BDay(sesiones)).date())


def backtest(ent, coord, peticion: Dict, desde: str, hasta: str, frecuencia: str = "mensual", solo_seleccion: bool = False,
             salida: Optional[str] = None) -> Dict:
    salida = Path(salida or ent.salida)
    salida.mkdir(parents=True, exist_ok=True)
    ent.modo = "backtest"
    ent.inv.modo = "backtest"
    if not ent.f10().get("politica_autorizacion"):
        ent.alm.escribir("F10", "AG-B01", {"tipo_entrada": "CFG", "id": ent.alm.nuevo_id("CFG-B"), "parametro": "politica_autorizacion",
                                           "valor": [{"regla_id": "POL-BT-1", "condicion": {}, "accion": "AUTORIZAR_HASTA", "minutos": 480}],
                                           "nota": "política del backtest: autorización automática hasta 480 min (decisión del ejecutor)"})
        ent.alm.escribir("F10", "AG-B01", {"tipo_entrada": "CFG", "id": ent.alm.nuevo_id("CFG-B"), "parametro": "tope_autorizacion_automatica_min",
                                           "valor": 480})
    clave = (peticion.get("objeto") or {}).get("clave_universo") or (peticion.get("paquete_para_bloque_B") or {}).get("x_clave_universo")
    amb = ent.ambitos.get(clave) or {}
    horizonte = (peticion.get("horizontes") or [amb.get("horizonte", "H3")])[0]
    H = int((ent.cfg.get("horizontes_sesiones") or {}).get(horizonte, 63))
    filas: List[Dict] = []
    ref_simbolo = (amb.get("referencia") or {}).get("simbolo")
    advertencias = []
    corte_modelo = (ent.cfg.get("backtest") or {}).get("fecha_corte_modelo")
    if corte_modelo and desde <= corte_modelo and not solo_seleccion and ent.tipo_cliente == "anthropic":
        advertencias.append(f"El periodo empieza antes de la fecha de corte del modelo ({corte_modelo}): posible fuga por conocimiento del modelo")
    ultima_entrega = None
    for f in fechas_corte(desde, hasta, frecuencia):
        ent.fijar_as_of(f)
        if solo_seleccion:
            for t in (peticion.get("tipos_activo_admitidos") or amb.get("tipos_activo") or ["RV"]):
                if t in ent.universos:
                    for x in seleccion_rapida(ent, clave, t, peticion.get("nivel") if peticion.get("nivel") in ("N1", "N2", "N3") else "N2", horizonte):
                        filas.append({"fecha_asof": f, "pet_id": "", **x})
            continue
        r = coord.recibir(peticion)
        pet_id = r.get("pet_id")
        if r.get("estado") == "EN_PAUSA":
            advertencias.append(f"{f}: {pet_id} en pausa (la política del backtest no la cubrió)")
            continue
        if r.get("entregables"):
            ultima_entrega = r
        rec = ent.alm.estado("F3").get(pet_id.replace("PET-B-", "REC-B-")) or {}
        for k, cnd in ent.alm.estado("F3").items():
            if str(k).startswith("CAND-B-") and cnd.get("pet_id") == pet_id:
                filas.append({"fecha_asof": f, "pet_id": pet_id, "cand_id": k, "tipo_activo": cnd.get("tipo_activo"), "simbolo": cnd.get("simbolo"),
                              "nombre": cnd.get("nombre"), "S": cnd.get("S"), "en_top_n": cnd.get("en_top_n"), "rango": cnd.get("rango"),
                              "veredicto": cnd.get("veredicto"), "veredicto_ambito": rec.get("veredicto"), "A": rec.get("A"), "E": rec.get("E"),
                              "C": rec.get("C")})
    # Evaluación: se avanza la fecha hasta el final de los datos disponibles
    try:
        fin_datos = max(str(ent.prov._serie_completa(s).index[-1].date()) for s in {x["simbolo"] for x in filas if x.get("simbolo")})
    except Exception:  # noqa: BLE001
        fin_datos = hasta
    ent.fijar_as_of(fin_datos)
    for x in filas:
        fh = _fin_horizonte(x["fecha_asof"], H)
        x["fecha_fin_horizonte"] = fh
        x["evaluable"] = fh <= fin_datos
        x["rent_fwd"] = ent.motor.rentabilidad(x["simbolo"], x["fecha_asof"], fh) if x["evaluable"] and x.get("simbolo") else None
    rf_ref = {}
    for f in sorted({x["fecha_asof"] for x in filas}):
        fh = _fin_horizonte(f, H)
        rf_ref[f] = ent.motor.rentabilidad(ref_simbolo, f, fh) if ref_simbolo and fh <= fin_datos else None
    por = {}
    for x in filas:
        por.setdefault((x["fecha_asof"], x["tipo_activo"]), []).append(x)
    serie = []
    for (f, t), xs in sorted(por.items()):
        ev = [x for x in xs if x.get("rent_fwd") is not None and x.get("S") is not None]
        top = [x for x in ev if x.get("en_top_n")]
        if len(ev) < 3 or not top:
            continue
        mu = float(np.mean([x["rent_fwd"] for x in ev]))
        mt = float(np.mean([x["rent_fwd"] for x in top]))
        for x in xs:
            x["rent_fwd_universo"] = round(mu, 6)
            x["rent_fwd_referencia_ambito"] = rf_ref.get(f)
        ic = spearman([x["S"] for x in ev], [x["rent_fwd"] - mu for x in ev])
        serie.append({"fecha_asof": f, "tipo_activo": t, "n_universo": len(ev), "n_top": len(top), "rent_top": mt, "rent_universo": mu,
                      "exceso_vs_universo": mt - mu, "rent_referencia_ambito": rf_ref.get(f),
                      "exceso_vs_referencia_ambito": None if rf_ref.get(f) is None else mt - rf_ref[f], "ic_rango": ic})
    metr = {}
    for t in sorted({s["tipo_activo"] for s in serie}):
        ss = [s for s in serie if s["tipo_activo"] == t]
        ex = [s["exceso_vs_universo"] for s in ss]
        exr = [s["exceso_vs_referencia_ambito"] for s in ss if s["exceso_vs_referencia_ambito"] is not None]
        ics = [s["ic_rango"] for s in ss if s["ic_rango"] is not None]
        metr[t] = {"n_rankings": len(ss), "horizonte": horizonte, "sesiones": H,
                   "exceso_medio_top_n_vs_universo": round(float(np.mean(ex)), 6) if ex else None, "ic90_exceso": ic_bootstrap_media(ex),
                   "acierto_top_n_vs_universo": round(float(np.mean([e > 0 for e in ex])), 4) if ex else None,
                   "exceso_medio_top_n_vs_referencia_ambito": round(float(np.mean(exr)), 6) if exr else None, "ic90_exceso_referencia": ic_bootstrap_media(exr),
                   "ic_rango_medio": round(float(np.mean(ics)), 4) if ics else None, "ic90_ic_rango": ic_bootstrap_media(ics),
                   "certificable": len(ss) >= 30 and (ic_bootstrap_media(ex) or [0])[0] > 0 and (ic_bootstrap_media(ics) or [0])[0] > 0,
                   "nota": "rankings solapados si el horizonte supera la frecuencia: los IC por bootstrap simple son optimistas"}
    # Pronósticos (F4) resueltos con los datos disponibles
    ev_res = evaluador.evaluar(ent, coord) if not solo_seleccion else None
    _csv(salida / "rankings.csv", filas)
    _csv(salida / "series_ranking.csv", serie)
    pron = []
    for k, p in ent.alm.estado("F4").items():
        r = p.get("resolucion") or {}
        pron.append({"prg_id": k, "pet_id": p.get("pet_id"), "tipo": p.get("tipo"), "fecha_emision": p.get("fecha_emision"),
                     "fecha_resolucion": p.get("fecha_resolucion"), "tipo_activo": p.get("tipo_activo"), "banda": p.get("banda"),
                     "probabilidad_interna": p.get("probabilidad_interna"), "estado": p.get("estado"), "acierto": r.get("acierto"),
                     "relativa": r.get("relativa"), "exceso": r.get("exceso"), "ic_rango": r.get("ic_rango"), "brier": r.get("brier")})
    _csv(salida / "pronosticos.csv", pron)
    cons = {}
    for r in ent.inv.registro:
        c = cons.setdefault(r["run_id"] or "fondo", {"run_id": r["run_id"] or "fondo", "llamadas": 0, "entrada": 0, "salida": 0, "cache_escritura": 0,
                                                       "cache_lectura": 0, "busquedas_web": 0, "uc": 0.0})
        c["llamadas"] += 1
        for k in ("entrada", "salida", "cache_escritura", "cache_lectura", "busquedas_web"):
            c[k] += r[k]
        c["uc"] = round(c["uc"] + r["uc"], 4)
    _csv(salida / "consumo.csv", list(cons.values()))
    if ultima_entrega:
        dest = salida / "entregables_ultima_fecha"
        dest.mkdir(exist_ok=True)
        for ruta in ultima_entrega["entregables"].values():
            shutil.copy2(ruta, dest / Path(ruta).name)
    res = {"desde": desde, "hasta": hasta, "frecuencia": frecuencia, "fechas": len({x["fecha_asof"] for x in filas}), "fin_datos": fin_datos,
           "modo": "solo_seleccion" if solo_seleccion else "completo", "cliente": ent.tipo_cliente, "metricas_rankings": metr,
           "evaluacion_pronosticos": (ev_res or {}).get("metricas"), "certificados": (ev_res or {}).get("certificados"),
           "consumo_uc_total": round(ent.inv.uc_total + ent.motor.uc, 2), "advertencias": advertencias,
           "aviso": "Con el cliente simulado y datos sintéticos, estas métricas no dicen nada de la capacidad del bloque."}
    (salida / "metricas.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return res


def _csv(ruta: Path, filas: List[Dict]) -> None:
    cols = []
    for f in filas:
        for k in f:
            if k not in cols:
                cols.append(k)
    with open(ruta, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols or ["vacio"])
        w.writeheader()
        for f in filas:
            w.writerow(f)
