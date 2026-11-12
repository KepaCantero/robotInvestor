"""Backtest: bucle sobre fechas as_of (ciclo C1 en cada una, sin fuga) y exportación para un backtester externo.

Salida: `senales.csv`, `pronosticos.csv`, `metricas.json`, `consumo.csv`, `entregables/<fecha>/` (tres entregables)
y `estado/` (F1–F6, F10, RC, HA en JSONL)."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from .configuracion import fusionar, parametro
from .herramientas.ht01_datos import ProveedorCSV, cargar_universo
from .herramientas.ht05_planificador import fechas_ciclo
from .llm import LLMClient, crear_cliente
from .orquestacion import Bloque

# senales.csv (V1.1, Documento 0 óptima V5.0): «clase» es el tipo de activo (doce códigos de 2.6) y se repite en
# «tipo_activo» por claridad; «indicador_seguimiento_simbolo» sustituye a «proxy_backtest» (V1.0). Compatibilidad: la
# columna «proxy_backtest» se mantiene al final, con el mismo valor, como alias obsoleto que se retirará en V1.2.
COLUMNAS_SENALES = ["fecha_asof", "run_id", "clase", "tipo_activo", "subtipo", "rango", "opp_id", "tipo_opcion", "nombre", "ambito",
                    "indicador_seguimiento_simbolo", "direccion", "horizontes", "horizonte_principal", "banda", "prob_interna",
                    "RK", "A", "E", "T", "riesgo_1a5", "relevancia_decisional", "siguiente_paso", "vigente_nueva", "proxy_backtest"]
COLUMNAS_PRONOSTICOS = ["prg_id", "opp_id", "run_id", "fecha_emision", "clase", "simbolo", "horizonte", "fecha_resolucion",
                        "tipo_pronostico", "direccion", "referencia", "umbral", "banda_verbal", "prob_interna", "prob_publicada",
                        "prob_referencia_ingenua", "nivel_referencia", "nivel_referencia_indice", "en_informe", "estado",
                        "fecha_resuelto", "rent_proxy", "rent_referencia", "valor_observado", "resultado_binario", "brier",
                        "log_score", "brier_ref", "comprobacion_fuga", "version_de"]
COLUMNAS_CONSUMO = ["run_id", "fecha_asof", "llamadas", "tokens_entrada", "tokens_salida", "tokens_cache_escritura",
                    "tokens_cache_lectura", "busquedas_web", "uc_llm", "uc_motor", "uc", "coste_estimado", "reintentos", "latencia_s"]


def _direccion(vista: str) -> str:
    return {"alcista": "LARGO", "relativa_favorable": "LARGO", "bajista": "CORTO", "relativa_desfavorable": "CORTO"}.get(vista, "NEUTRAL")


def _escribir_csv(ruta: Path, columnas: List[str], filas: List[Dict]) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow({k: ("" if f.get(k) is None else f.get(k)) for k in columnas})


def filas_senales(res: Dict, f4: Dict) -> List[Dict]:
    out = []
    for c, d in res["paquete"]["clases"].items():
        for o in d["opciones"]:
            hp = o["horizonte_principal"]
            v = o["horizontes"][hp]
            pu = o["puntuaciones"]
            sym = (o.get("indicador_seguimiento") or {}).get("simbolo")
            amb = o.get("ambito") or {}
            out.append({"fecha_asof": res["as_of"], "run_id": res["run_id"], "clase": c, "tipo_activo": o.get("tipo_activo", c),
                        "subtipo": o.get("subtipo"), "rango": o["rango"], "opp_id": o["opp_id"], "tipo_opcion": o["tipo_opcion"],
                        "nombre": o["nombre"], "ambito": " · ".join(x for x in (amb.get("incluye"), amb.get("region")) if x),
                        "indicador_seguimiento_simbolo": sym, "proxy_backtest": sym,
                        "direccion": _direccion(v["vista"]), "horizontes": "|".join(sorted(o["horizontes"])), "horizonte_principal": hp,
                        "banda": v["banda"], "prob_interna": (f4.get(v["prg_id"]) or {}).get("prob_interna"), "RK": pu["RK"], "A": pu["A"],
                        "E": pu["E"], "T": pu["T"], "riesgo_1a5": o["riesgo_1a5"], "relevancia_decisional": o["relevancia_decisional"],
                        "siguiente_paso": o["siguiente_paso_sugerido"], "vigente_nueva": "VIGENTE" if o.get("vigente") else "NUEVA"})
    return out


def filas_pronosticos(f4: Dict) -> List[Dict]:
    out = []
    for p in sorted(f4.values(), key=lambda x: x["prg_id"]):
        r = p.get("resolucion") or {}
        pt = r.get("puntuaciones") or {}
        out.append({"prg_id": p["prg_id"], "opp_id": p.get("opp_id"), "run_id": p.get("run_id"), "fecha_emision": p.get("fecha_emision"),
                    "clase": p.get("clase"), "simbolo": (p.get("variable") or {}).get("serie_ht01"), "horizonte": p.get("horizonte"),
                    "fecha_resolucion": p.get("fecha_resolucion"), "tipo_pronostico": p.get("tipo_pronostico"),
                    "direccion": _direccion(p.get("vista", "")), "referencia": p.get("referencia_indice"), "umbral": p.get("umbral"),
                    "banda_verbal": p.get("banda_verbal"), "prob_interna": p.get("prob_interna"), "prob_publicada": p.get("prob_publicada"),
                    "prob_referencia_ingenua": (p.get("referencia_ingenua") or {}).get("valor_o_prob"),
                    "nivel_referencia": (p.get("nivel_referencia") or {}).get("valor"), "nivel_referencia_indice": p.get("nivel_referencia_indice"),
                    "en_informe": p.get("en_informe"), "estado": p.get("estado"), "fecha_resuelto": r.get("fecha_resuelto"),
                    "rent_proxy": r.get("rent_proxy"), "rent_referencia": r.get("rent_referencia"), "valor_observado": r.get("valor_observado"),
                    "resultado_binario": r.get("resultado_binario"), "brier": pt.get("brier"), "log_score": pt.get("log"),
                    "brier_ref": pt.get("brier_ref"), "comprobacion_fuga": r.get("comprobacion_fuga"), "version_de": p.get("version_de")})
    return out


def _resumen_celda(m: Dict) -> Dict:
    ac = m.get("acierto") or {}
    return {"n": m["n"], "acierto": {"tasa": ac.get("tasa"), "ic90_wilson": ac.get("ic"), "p_binomial_vs_tasa_base": ac.get("p_binomial"),
                                     "tasa_base": ac.get("tasa_base")},
            "brier": m.get("brier"), "brier_ref": m.get("brier_ref"), "log_score": m.get("log_score"),
            "bss": {"valor": (m.get("bss") or {}).get("valor"), "ic90": (m.get("bss") or {}).get("ic")},
            "ece": {"valor": (m.get("calibracion") or {}).get("ece"), "nulo_media": (m.get("ece_nulo") or {}).get("media"),
                    "nulo_q90": (m.get("ece_nulo") or {}).get("q90")},
            "dm_hln": m.get("dm_hln"), "calibracion_global": m.get("calibracion_global"),
            "rentabilidad_relativa_media_top3_vs_indice": m.get("rentabilidad_relativa_media_top3"), "n_top3": m.get("n_top3"),
            "referencia": m.get("referencia")}


def ejecutar_backtest(cfg: Dict, desde: str, hasta: str, datos: str, universo: str, salida: str, frecuencia: Optional[str] = None,
                      clases: Optional[List[str]] = None, cliente: Optional[LLMClient] = None, tipo_cliente: str = "mock",
                      replay: Optional[str] = None, replay_modo: str = "reproducir", anonimizar: Optional[bool] = None,
                      resolver_al_final: Optional[bool] = None, proveedor=None, progreso=None) -> Dict:
    cfg = fusionar(cfg, {"modo": "backtest"})
    bt = cfg.get("backtest") or {}
    salida_p = Path(salida)
    salida_p.mkdir(parents=True, exist_ok=True)
    reservados = ("estado", "entregables", "senales.csv", "pronosticos.csv", "consumo.csv", "metricas.json")
    if any((salida_p / nombre).exists() for nombre in reservados):
        raise FileExistsError("La salida ya contiene un backtest; elija otra carpeta para una ejecución independiente.")
    prov = proveedor or ProveedorCSV(datos)
    uni = cargar_universo(universo)
    cli = cliente or crear_cliente(tipo_cliente, cfg, replay, replay_modo)
    # Reserva atómica frente a dos ejecuciones concurrentes en la misma salida.
    (salida_p / "estado").mkdir()
    bloque = Bloque(cfg, prov, uni, cli, salida_p / "estado", salida_p / "entregables",
                    anonimizar=bt.get("anonimizar", "auto") if anonimizar is None else anonimizar)
    fechas = fechas_ciclo(desde, hasta, frecuencia or bt.get("frecuencia", "semanal"), int(parametro(cfg, "backtest.dia_semana")))
    senales, consumo, runs = [], [], []
    for f in fechas:
        res = bloque.ciclo(f, alcance={"clases": clases} if clases else None)
        f4 = bloque.almacen.estado("F4", f)
        if res.get("entrega") != "BLOQUEADA":
            senales += filas_senales(res, f4)
        c = bloque.contabilidad.resumen(res["run_id"])
        consumo.append({"run_id": res["run_id"], "fecha_asof": res["as_of"], "llamadas": c["llamadas"], "tokens_entrada": c["entrada"],
                        "tokens_salida": c["salida"], "tokens_cache_escritura": c["cache_escritura"], "tokens_cache_lectura": c["cache_lectura"],
                        "busquedas_web": c["busquedas_web"], "uc_llm": c["uc_llm"], "uc_motor": c["uc_motor"], "uc": c["uc"],
                        "coste_estimado": c["coste_estimado"], "reintentos": c.get("reintentos", 0), "latencia_s": c.get("latencia_s", 0.0)})
        runs.append({"run_id": res["run_id"], "as_of": res["as_of"], "estado": res["estado"], "entrega": res.get("entrega", "ENTREGADA"),
                     "nivel_por_clase": res["nivel_por_clase"], "g3": (res.get("g3_entregables") or res["g3"]).get("dictamen")})
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
    # PA-09 (T-66): los PRG con contaminacion_posible no cuentan como evidencia; se muestran aparte, solo descriptivos
    excl = bloque.evaluador.excluidos_contaminacion(fecha_final)
    metr_no_admisibles = None
    if excl.get("total"):
        metr_no_admisibles = bloque.evaluador.metricas(fecha_final, completas=False, admisibles=False)
        advert.append(f"{excl['total']} pronósticos hechos con un modelo real antes de su fecha de corte: no cuentan para "
                      "certificados ni aprendizaje (PA-09). Sus métricas van aparte, solo como descripción.")
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
                "por_clase_horizonte": {k: _resumen_celda(m) for k, m in metr.items()},
                "excluidos_contaminacion": excl,
                "por_clase_horizonte_con_no_admisibles": ({k: _resumen_celda(m) for k, m in metr_no_admisibles.items()}
                                                          if metr_no_admisibles is not None else None),
                "solo_opciones_publicadas": {k: {"n": m["n"], "acierto": (m.get("acierto") or {}).get("tasa"), "brier": m.get("brier"),
                                                 "bss": (m.get("bss") or {}).get("valor"),
                                                 "rentabilidad_relativa_media_top3_vs_indice": m.get("rentabilidad_relativa_media_top3")}
                                             for k, m in metr_top.items()},
                "certificados": {"emitidos": [c["id"] for c in certs["emitidos"]] + [c["id"] for c in bloque.evaluador.certificados_vigentes(fecha_final)],
                                 "propuestos_pendientes_de_aprobacion": [c["id"] for c in bloque.evaluador.certificados_propuestos(fecha_final)],
                                 "celdas_evaluadas": certs["evaluadas"], "celdas_con_muestra_insuficiente": certs["insuficientes"],
                                 "criterio": "Anexo A: n ≥ 100 efectivas (n_eff por fechas, T-66), IC 90 % del BSS > 0 (Holm), "
                                             "ECE ≤ q90 del nulo y < 0,15; con aprendizaje.solo_endurecer, nace PROPUESTO "
                                             "y lo aprueba el operador por CT-04"},
                "consumo_total": tot, "runs": runs}
    metricas["certificados"]["emitidos"] = sorted(set(metricas["certificados"]["emitidos"]))
    (salida_p / "metricas.json").write_text(json.dumps(metricas, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return {"salida": str(salida_p), "ciclos": len(fechas), "senales": len(senales), "pronosticos": len(pron), "resueltos": n_res,
            "advertencias": advert, "bloque": bloque, "metricas": metricas}
