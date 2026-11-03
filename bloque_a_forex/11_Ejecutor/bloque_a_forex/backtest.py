"""Backtest del Bloque A Forex: bucle sobre fechas as_of (ciclo C1 en cada una, sin fuga) y exportación para un
backtester externo (señales por par o cesta con su dirección, pronósticos con las referencias del paseo aleatorio y
del forward).

Salida: `senales.csv`, `pronosticos.csv`, `metricas.json`, `consumo.csv`, `entregables/<fecha>/` (tres entregables)
y `estado/` (F1–F6, F10, RC, HA en JSONL)."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from .configuracion import fusionar
from .herramientas.ht01_datos import ProveedorCSV, cargar_universo
from .herramientas.ht05_planificador import fechas_ciclo
from .llm import LLMClient, crear_cliente
from .orquestacion import Bloque

# senales.csv (ejecutor Forex V1.0): una fila por opción publicada. «segmento» es uno de los seis segmentos de 2.6;
# «par» va en notación BASE/COTIZADA; «direccion» es ALCISTA_BASE/BAJISTA_BASE en PAR, CRUCE y REGIMEN y vacía en el
# resto; «composicion» lista «DIVISA:LADO:PESO» separados por «;»; «indicador_sube» dice si la tesis espera que suba la
# serie del indicador de seguimiento (lo que hay que comprar en el backtester es la serie, o su inversa si es «no»).
COLUMNAS_SENALES = ["fecha_asof", "run_id", "segmento", "rango", "opp_id", "tipo_opcion", "nombre", "par", "direccion",
                    "composicion", "divisa_financiacion", "vista_volatilidad", "indicador_seguimiento_simbolo", "indicador_sube",
                    "tipo_rentabilidad", "divisa_medicion", "carry_anual_pct", "carry_signo", "horizontes", "horizonte_principal",
                    "banda", "prob_interna", "RK", "A", "E", "T", "riesgo_1a5", "relevancia_decisional", "siguiente_paso",
                    "vigente_nueva"]
COLUMNAS_PRONOSTICOS = ["prg_id", "opp_id", "run_id", "fecha_emision", "segmento", "simbolo", "par", "direccion", "composicion",
                        "horizonte", "fecha_resolucion", "sentido_indicador", "tipo_rentabilidad", "divisa_medicion",
                        "carry_anual_pct_indicador", "referencia_segmento", "umbral", "banda_verbal", "prob_interna",
                        "prob_publicada", "prob_paseo_aleatorio", "prob_forward", "cambio_forward", "nivel_referencia",
                        "hora_fijacion", "en_informe", "estado", "fecha_resuelto", "rent_proxy", "rent_referencia",
                        "valor_observado", "resultado_binario", "brier", "log_score", "brier_ref", "brier_forward",
                        "acierto_forward", "comprobacion_fuga", "version_de"]
COLUMNAS_CONSUMO = ["run_id", "fecha_asof", "llamadas", "tokens_entrada", "tokens_salida", "tokens_cache_escritura",
                    "tokens_cache_lectura", "busquedas_web", "uc_llm", "uc_motor", "uc", "coste_estimado"]


def _comp(c) -> str:
    return ";".join(f"{x['divisa']}:{x['lado']}:{x['peso']:g}" for x in (c or []))


def _escribir_csv(ruta: Path, columnas: List[str], filas: List[Dict]) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow({k: ("" if f.get(k) is None else f.get(k)) for k in columnas})


def filas_senales(res: Dict, f4: Dict) -> List[Dict]:
    out = []
    for c, d in res["paquete"]["segmentos"].items():
        for o in d["opciones"]:
            hp = o["horizonte_principal"]
            v = o["horizontes"][hp]
            pu = o["puntuaciones"]
            ca = o.get("carry") or {}
            vv = o.get("vista_volatilidad") or {}
            out.append({"fecha_asof": res["as_of"], "run_id": res["run_id"], "segmento": c, "rango": o["rango"], "opp_id": o["opp_id"],
                        "tipo_opcion": o["tipo_opcion"], "nombre": o["nombre"], "par": o.get("par"), "direccion": o.get("direccion"),
                        "composicion": _comp(o.get("composicion")), "divisa_financiacion": o.get("divisa_financiacion"),
                        "vista_volatilidad": f"{vv['sentido']}:{vv['plazo']}" if vv else None,
                        "indicador_seguimiento_simbolo": (o.get("indicador_seguimiento") or {}).get("simbolo"),
                        "indicador_sube": "si" if o.get("x_indicador_sube", True) else "no",
                        "tipo_rentabilidad": v.get("tipo_rentabilidad"), "divisa_medicion": v.get("divisa_medicion"),
                        "carry_anual_pct": ca.get("anual_pct"), "carry_signo": ca.get("signo"),
                        "horizontes": "|".join(sorted(o["horizontes"])), "horizonte_principal": hp,
                        "banda": v["banda"], "prob_interna": (f4.get(v["prg_id"]) or {}).get("prob_interna"), "RK": pu["RK"], "A": pu["A"],
                        "E": pu["E"], "T": pu["T"], "riesgo_1a5": o["riesgo_1a5"], "relevancia_decisional": o["relevancia_decisional"],
                        "siguiente_paso": o["siguiente_paso_sugerido"], "vigente_nueva": "VIGENTE" if o.get("vigente") else "NUEVA"})
    return out


def filas_pronosticos(f4: Dict) -> List[Dict]:
    out = []
    for p in sorted(f4.values(), key=lambda x: x["prg_id"]):
        r = p.get("resolucion") or {}
        pt = r.get("puntuaciones") or {}
        ri = p.get("referencia_ingenua") or {}
        var = p.get("variable") or {}
        out.append({"prg_id": p["prg_id"], "opp_id": p.get("opp_id"), "run_id": p.get("run_id"), "fecha_emision": p.get("fecha_emision"),
                    "segmento": p.get("segmento"), "simbolo": var.get("serie_ht01"), "par": p.get("par"), "direccion": p.get("direccion"),
                    "composicion": _comp(p.get("composicion")), "horizonte": p.get("horizonte"),
                    "fecha_resolucion": p.get("fecha_resolucion"),
                    "sentido_indicador": "SUBE" if p.get("sentido") == "POSITIVO" else ("BAJA" if p.get("sentido") else None),
                    "tipo_rentabilidad": var.get("tipo_rentabilidad"), "divisa_medicion": var.get("divisa"),
                    "carry_anual_pct_indicador": var.get("carry_anual_pct_indicador"), "referencia_segmento": p.get("referencia_indice"),
                    "umbral": p.get("umbral"), "banda_verbal": p.get("banda_verbal"), "prob_interna": p.get("prob_interna"),
                    "prob_publicada": p.get("prob_publicada"), "prob_paseo_aleatorio": ri.get("valor_o_prob"),
                    "prob_forward": ri.get("prob_forward"), "cambio_forward": ri.get("cambio_forward"),
                    "nivel_referencia": (p.get("nivel_referencia") or {}).get("valor"),
                    "hora_fijacion": (p.get("nivel_referencia") or {}).get("hora_fijacion"),
                    "en_informe": p.get("en_informe"), "estado": p.get("estado"), "fecha_resuelto": r.get("fecha_resuelto"),
                    "rent_proxy": r.get("rent_proxy"), "rent_referencia": r.get("rent_referencia"), "valor_observado": r.get("valor_observado"),
                    "resultado_binario": r.get("resultado_binario"), "brier": pt.get("brier"), "log_score": pt.get("log"),
                    "brier_ref": pt.get("brier_ref"), "brier_forward": pt.get("brier_forward"), "acierto_forward": pt.get("acierto_forward"),
                    "comprobacion_fuga": r.get("comprobacion_fuga"), "version_de": p.get("version_de")})
    return out


def _resumen_celda(m: Dict) -> Dict:
    ac = m.get("acierto") or {}
    return {"n": m["n"], "acierto": {"tasa": ac.get("tasa"), "ic90_wilson": ac.get("ic"), "p_binomial_vs_tasa_base": ac.get("p_binomial"),
                                     "tasa_base": ac.get("tasa_base")},
            "brier": m.get("brier"), "brier_ref": m.get("brier_ref"), "log_score": m.get("log_score"),
            "bss": {"valor": (m.get("bss") or {}).get("valor"), "ic90": (m.get("bss") or {}).get("ic")},
            "ece": {"valor": (m.get("calibracion") or {}).get("ece"), "nulo_media": (m.get("ece_nulo") or {}).get("media"),
                    "nulo_q90": (m.get("ece_nulo") or {}).get("q90")},
            "brier_forward": m.get("brier_forward"), "bss_forward": m.get("bss_forward"), "tasa_forward": m.get("tasa_forward"),
            "dm_hln": m.get("dm_hln"), "calibracion_global": m.get("calibracion_global"),
            "rentabilidad_media_top3": m.get("rentabilidad_media_top3"),
            "rentabilidad_relativa_media_top3_vs_referencia_segmento": m.get("rentabilidad_relativa_media_top3"), "n_top3": m.get("n_top3"),
            "referencia": m.get("referencia"), "referencia_segmento": m.get("referencia_segmento")}


def ejecutar_backtest(cfg: Dict, desde: str, hasta: str, datos: str, universo: str, salida: str, frecuencia: Optional[str] = None,
                      segmentos: Optional[List[str]] = None, cliente: Optional[LLMClient] = None, tipo_cliente: str = "mock",
                      replay: Optional[str] = None, replay_modo: str = "reproducir", anonimizar: Optional[bool] = None,
                      resolver_al_final: Optional[bool] = None, proveedor=None, progreso=None) -> Dict:
    cfg = fusionar(cfg, {"modo": "backtest"})
    bt = cfg.get("backtest") or {}
    salida_p = Path(salida)
    salida_p.mkdir(parents=True, exist_ok=True)
    prov = proveedor or ProveedorCSV(datos)
    uni = cargar_universo(universo)
    cli = cliente or crear_cliente(tipo_cliente, cfg, replay, replay_modo)
    bloque = Bloque(cfg, prov, uni, cli, salida_p / "estado", salida_p / "entregables",
                    anonimizar=bt.get("anonimizar", False) if anonimizar is None else anonimizar)
    fechas = fechas_ciclo(desde, hasta, frecuencia or bt.get("frecuencia", "semanal"), int(bt.get("dia_semana", 4)))
    senales, consumo, runs = [], [], []
    for f in fechas:
        res = bloque.ciclo(f, alcance={"segmentos": segmentos} if segmentos else None)
        bloque.seguimientos.ejecutar_pendientes(f)   # V1.1: ciclos C6 vencidos (solo si el Broker los ha encargado; nunca antes de C1)
        f4 = bloque.almacen.estado("F4", f)
        if res.get("entrega") != "BLOQUEADA":
            senales += filas_senales(res, f4)
        c = bloque.contabilidad.resumen(res["run_id"])
        consumo.append({"run_id": res["run_id"], "fecha_asof": res["as_of"], "llamadas": c["llamadas"], "tokens_entrada": c["entrada"],
                        "tokens_salida": c["salida"], "tokens_cache_escritura": c["cache_escritura"], "tokens_cache_lectura": c["cache_lectura"],
                        "busquedas_web": c["busquedas_web"], "uc_llm": c["uc_llm"], "uc_motor": c["uc_motor"], "uc": c["uc"],
                        "coste_estimado": c["coste_estimado"]})
        runs.append({"run_id": res["run_id"], "as_of": res["as_of"], "estado": res["estado"], "entrega": res.get("entrega", "ENTREGADA"),
                     "nivel_por_segmento": res["nivel_por_segmento"], "g3": (res.get("g3_entregables") or res["g3"]).get("dictamen")})
        if progreso:
            progreso(res)
    fecha_final = pd.Timestamp(fechas[-1]) if fechas else pd.Timestamp(hasta)
    if resolver_al_final if resolver_al_final is not None else bt.get("resolver_al_final", True):
        ult = []
        prov.fijar_as_of(pd.Timestamp.max.normalize() - pd.Timedelta(days=1))
        for s in uni["simbolo"]:
            if prov.tiene(s):
                u = prov.ultima_fecha(s)
                if u is not None:
                    ult.append(u)
        if ult:
            fin = min(max(ult), pd.Timestamp(hasta) + pd.DateOffset(months=13))
            if fin > fecha_final:
                bloque.fijar_fecha(fin)
                bloque.evaluador.resolver(fin, "RESOLUCION-FINAL")
                fecha_final = fin
    bloque.fijar_fecha(fecha_final)
    f4 = bloque.almacen.estado("F4")
    pron = filas_pronosticos(f4)
    _escribir_csv(salida_p / "senales.csv", COLUMNAS_SENALES, senales)
    _escribir_csv(salida_p / "pronosticos.csv", COLUMNAS_PRONOSTICOS, pron)
    _escribir_csv(salida_p / "consumo.csv", COLUMNAS_CONSUMO, consumo)
    metr = bloque.evaluador.metricas(fecha_final, completas=True)
    metr_top = bloque.evaluador.metricas(fecha_final, completas=False, solo_informe=True)
    certs = bloque.evaluador.revisar_certificados(fecha_final)
    advert = []
    corte = bt.get("fecha_corte_modelo")
    if corte and pd.Timestamp(desde) < pd.Timestamp(corte):
        advert.append(f"FUGA POR CONOCIMIENTO DEL MODELO: el periodo empieza el {desde}, antes de la fecha de corte configurada "
                      f"({corte}). El modelo puede conocer hechos posteriores a cada fecha as_of; los resultados pueden estar "
                      f"sesgados al alza. Backtestee periodos posteriores a la fecha de corte o use --anonimizar (mitigación parcial).")
    if tipo_cliente == "mock" or getattr(cli, "nombre", "") == "mock":
        advert.append("Cliente simulado (mock): las señales proceden de reglas sintéticas, no de un modelo de lenguaje; sirve para probar la tubería, no para medir la capacidad predictiva.")
    n_res = sum(1 for p in pron if p["estado"] == "RESUELTO")
    tot = {k: sum((c[k] or 0) for c in consumo) for k in ("llamadas", "tokens_entrada", "tokens_salida", "tokens_cache_escritura", "tokens_cache_lectura", "uc")}
    metricas = {"periodo": {"desde": desde, "hasta": hasta, "frecuencia": frecuencia or bt.get("frecuencia", "semanal"),
                            "fecha_evaluacion": str(fecha_final.date()), "ciclos": len(fechas)},
                "advertencias": advert, "anonimizado": bool(bloque.anon),
                "pronosticos": {"total": len(pron), "resueltos": n_res, "abiertos": sum(1 for p in pron if p["estado"] == "ABIERTO"),
                                "no_resolubles": sum(1 for p in pron if p["estado"] == "NO_RESOLUBLE")},
                "por_segmento_horizonte": {k: _resumen_celda(m) for k, m in metr.items()},
                "solo_opciones_publicadas": {k: {"n": m["n"], "acierto": (m.get("acierto") or {}).get("tasa"), "brier": m.get("brier"),
                                                 "bss_paseo_aleatorio": (m.get("bss") or {}).get("valor"), "bss_forward": m.get("bss_forward"),
                                                 "tasa_forward": m.get("tasa_forward"),
                                                 "rentabilidad_relativa_media_top3_vs_referencia_segmento": m.get("rentabilidad_relativa_media_top3")}
                                             for k, m in metr_top.items()},
                "certificados": {"emitidos": [c["id"] for c in certs["emitidos"]] + [c["id"] for c in bloque.evaluador.certificados_vigentes(fecha_final)],
                                 "celdas_evaluadas": certs["evaluadas"], "celdas_con_muestra_insuficiente": certs["insuficientes"],
                                 "criterio": "Anexo A: n ≥ 100, IC 90 % del BSS > 0 (Holm), ECE ≤ q90 del nulo y < 0,15"},
                "consumo_total": tot, "runs": runs}
    metricas["certificados"]["emitidos"] = sorted(set(metricas["certificados"]["emitidos"]))
    (salida_p / "metricas.json").write_text(json.dumps(metricas, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return {"salida": str(salida_p), "ciclos": len(fechas), "senales": len(senales), "pronosticos": len(pron), "resueltos": n_res,
            "advertencias": advert, "bloque": bloque, "metricas": metricas}
