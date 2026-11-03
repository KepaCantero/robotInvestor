#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-10 · Generador de anexos de datos y cálculos (implementación de referencia).

Bloque B · Robot Investor · V2.0 (actualizado V2.1, 03/11/2026) · Subordinada al Documento 0 del Bloque B, óptima V2.1
(secciones 4.4, 8.7, 9.12–9.13, 14, 14.5 y 14.6).

Construye el entregable 5 (anexo de datos y cálculos) en XLSX (openpyxl) y en CSV (una hoja por archivo, UTF-8 con
BOM para que la abra cualquier hoja de cálculo) a partir del `paquete_analisis_mercado` y, si se proporcionan, de los
extractos de F2 y RC y del universo cribado completo (`datos_anexo`). Permite a un tercero rehacer cada cifra y cada
ranking:

  Leeme           · identificación (PET-B, RUN-B, REC-B, fecha de corte, metodología) y descripción de las hojas
  Puntuaciones    · componentes de A y E con sus pesos, RF, RE, C y veredicto (HT-03)
  Cifras          · valor, unidad, fecha, fuente, DAT-B/CALC-B, etiqueta epistémica y clase de cifra
  Fuentes         · referencias de F7–F9 y fuentes de datos usadas, con nivel y calidad
  Universo_<TIPO> · todos los activos cribados del tipo, con métricas, componentes de S, S, IC, rango, veredicto y
                    motivo de exclusión (una hoja por tipo de activo aplicable)
  Escenarios      · escenarios con premisas, régimen, probabilidad o banda y resultado frente a la referencia
  Sensibilidades  · variable, rango y efecto
  Pronosticos     · PRG-B congelados (sin probabilidad interna salvo certificado)
  Artefactos      · índice de artefactos reproducibles del Motor (CALC-B), con semilla, fecha de corte y huella
  Encargos_C      · resumen de los encargos para los Bloques C.x
  Eslabones       · (V2.1) desglose jerárquico del mapa por eslabón: métricas, indicadores de cuello en semáforo,
                    severidad, persistencia, relevancia, PCB, componentes de AE y AE (permite reconstruir PCB y AE)
  Opciones_eslabon· (V2.1) mejores opciones por eslabón: rango, candidato, tipo, pureza al eslabón, S, IC y veredicto
  Emergentes      · (V2.1) radar de emergentes: tipo, financiación, criterios, PEM y vía de exposición

CLI: python3 ht10_anexo_datos.py paquete.json --salida DIR [--datos datos_anexo.json] [--nombre BASE] [--plantilla]
Con --plantilla genera la plantilla vacía (cabeceras y hoja Leeme). Requiere openpyxl.
Estado de madurez (R26): implementada (referencia), pruebas unitarias superadas; integrada en el ejecutor.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

VERSION = "2.1"
TIPOS = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
COMPONENTES = ("PE", "QL", "VA", "MO", "RI", "LA", "CO")

COLUMNAS = {
    "Puntuaciones": ["puntuacion", "componente", "valor", "peso", "nota"],
    "Cifras": ["id", "descripcion", "valor", "unidad", "fecha", "fuente", "dat_calc", "etiqueta", "clase_cifra", "dimension"],
    "Fuentes": ["ref_id", "nombre", "archivo", "tematica", "nivel", "q", "url", "fecha_consulta", "uso"],
    "Universo": ["tipo_activo", "cand_id", "id", "nombre", "isin", "ticker", "mercado", "divisa", "subcluster", "emisor",
                 "invertible", "motivo_exclusion", "detalle_exclusion", "pureza", "pureza_metodo", "fecha_dato"]
                + [f"comp_{c}" for c in COMPONENTES] + ["S", "ic90_S_inf", "ic90_S_sup", "rango", "ic90_rango_inf",
                                                         "ic90_rango_sup", "frontera", "veredicto", "en_top_n",
                                                         "alternativa", "alertas"],
    "Escenarios": ["nombre", "premisas", "regimen", "probabilidad", "base_probabilidad", "banda", "resultado_vs_referencia",
                   "disparadores"],
    "Sensibilidades": ["variable", "valor_base", "valor_bajo", "valor_alto", "efecto_bajo", "efecto_alto", "unidad", "calc_id"],
    "Pronosticos": ["prg_id", "tipo", "afirmacion", "horizonte", "fecha_emision", "fecha_resolucion", "criterio", "referencia",
                    "banda", "probabilidad_publicada"],
    "Artefactos": ["calc_id", "metodo", "modulo", "perfil", "plan_calculo", "semilla", "fecha_corte", "huella_datos",
                   "insumos", "como_reproducir"],
    "Encargos_C": ["bloque_c", "cand_id", "tipo_activo", "nombre", "isin", "S", "rango", "veredicto", "eslabon_id",
                   "origen_seleccion", "preguntas_para_C"],
    "Eslabones": ["eslabon_id", "padre", "nivel", "nombre", "papel_ambito", "tamano", "unidad", "crecimiento_anual",
                  "margen_bruto", "margen_operativo", "poder_negociacion", "hhi", "concentracion_pais", "es_cuello",
                  "indicadores_rojo", "indicadores_ambar", "indicadores", "severidad", "persistencia", "relevancia_valor",
                  "PCB", "cuello_material", "senal_resolucion", "AE_crecimiento", "AE_margen_roic", "AE_poder_negociacion",
                  "AE_cuello", "AE_expectativas_inv", "AE_sustitucion_inv", "AE", "calc_cuello", "calc_AE"],
    "Opciones_eslabon": ["eslabon_id", "rango", "cand_id", "nombre", "tipo_activo", "rol_en_eslabon", "pureza_eslabon", "S",
                         "ic90_S_inf", "ic90_S_sup", "veredicto", "en_top_n_tipo", "motivo"],
    "Emergentes": ["eslabon_id", "emg_id", "nombre", "tipo", "financiacion_importe", "financiacion_divisa", "ultima_ronda",
                   "tecnologia_o_ventaja", "senales_traccion", "via_exposicion", "instrumento", "cand_id", "fuera_de_filtros",
                   "crit_tecnologia", "crit_traccion", "crit_equipo", "crit_financiacion", "crit_posicion_cadena",
                   "crit_via_exposicion", "PEM", "etiqueta"],
}
DESCRIPCION_HOJAS = {
    "Leeme": "Identificación del análisis y guía de las hojas.",
    "Puntuaciones": "Componentes de A y E (0–100 en múltiplos de 10, NA o NE) con sus pesos; RF, RE y C; veredicto (HT-03).",
    "Cifras": "Cada cifra entregada con valor, unidad, fecha, fuente, DAT-B o CALC-B, etiqueta epistémica y clase de cifra.",
    "Fuentes": "Referencias de F7, F8 y F9 y fuentes de datos usadas, con nivel (A–D) y calidad Q.",
    "Universo_<TIPO>": "Todos los activos cribados del tipo: métricas, componentes de S, S, IC 90 %, rango, veredicto y motivo de exclusión.",
    "Escenarios": "Escenarios base, favorable y adverso con premisas, régimen, probabilidad (solo con base calibrable o certificado) o banda.",
    "Sensibilidades": "Variables críticas, rango probado y efecto en el resultado.",
    "Pronosticos": "Pronósticos PRG-B congelados con criterio y fecha de resolución.",
    "Artefactos": "Artefactos reproducibles del Motor (CALC-B) con método, semilla, fecha de corte y huella de los datos.",
    "Encargos_C": "Resumen de los encargos preparados para los Bloques C.x, con su eslabón y su origen (top-N o tabla por eslabón).",
    "Eslabones": "Desglose de la cadena por eslabón: métricas, indicadores de cuello en semáforo, PCB y componentes de AE (9.12).",
    "Opciones_eslabon": "Hasta cinco mejores opciones por eslabón atractivo o con cuello material, adicionales al top-N (9.13).",
    "Emergentes": "Radar de emergentes, startups y spin-offs por eslabón: criterios, PEM y vía de exposición (8.7.3).",
}


def _txt(v: Any) -> Any:
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return " · ".join(str(_txt(x)) for x in v)
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False)
    return v


def _filas_puntuaciones(p: Dict) -> List[Dict]:
    pu = p.get("puntuaciones") or {}
    des = pu.get("desglose") or {}
    pesos = {"A": {"asimetria": 25, "valoracion_expectativas": 20, "calidad_crecimiento": 15, "ventaja_estructural": 10,
                   "catalizadores": 10, "momento_flujos": 10, "riesgos": 10},
             "E": {"calidad_raices": 25, "cobertura_dimensional": 15, "calidad_metodologica": 15, "trazabilidad": 15,
                   "actualidad": 10, "discrepancias_resueltas": 10, "hipotesis_cerradas": 10}}
    out = []
    for k in ("A", "E"):
        for comp, val in (des.get(k) or {}).items():
            out.append({"puntuacion": k, "componente": comp, "valor": val, "peso": pesos[k].get(comp), "nota": ""})
        out.append({"puntuacion": k, "componente": "TOTAL", "valor": pu.get(k), "peso": 100,
                    "nota": "media ponderada redondeada al múltiplo de 5"})
    out.append({"puntuacion": "RF", "componente": "TOTAL", "valor": pu.get("RF"), "peso": 25, "nota": "resultado de la refutación"})
    out.append({"puntuacion": "RE", "componente": "TOTAL", "valor": pu.get("RE"), "peso": 20, "nota": "robustez entre escenarios"})
    out.append({"puntuacion": "C", "componente": "TOTAL", "valor": pu.get("C"), "peso": None,
                "nota": "C = 0,20·A + 0,35·E + 0,25·RF + 0,20·RE; C ≤ E + 10"})
    v = p.get("veredicto") or {}
    out.append({"puntuacion": "VEREDICTO", "componente": v.get("valor"), "valor": None, "peso": None,
                "nota": f"{v.get('resultado_del_analisis')} · relevancia {v.get('relevancia_decisional')} · "
                        f"siguiente paso {v.get('siguiente_paso_sugerido')}"})
    return out


def _filas_universo(p: Dict, tipo: str, datos: Optional[Dict]) -> List[Dict]:
    filas = ((datos or {}).get("universo") or {}).get(tipo)
    if filas is not None:
        out = []
        for f in filas:
            g = dict(f)
            for c in COMPONENTES:
                if c in g and f"comp_{c}" not in g:
                    g[f"comp_{c}"] = g.pop(c)
            out.append(g)
        return out
    d = (p.get("candidatos_por_tipo") or {}).get(tipo) or {}
    out = []
    for c in d.get("top_n") or []:
        f = {"tipo_activo": tipo, "cand_id": c.get("cand_id"), "nombre": c.get("nombre"), "isin": c.get("isin"),
             "ticker": c.get("ticker"), "mercado": c.get("mercado"), "divisa": c.get("divisa"),
             "subcluster": c.get("subcluster"), "emisor": c.get("emisor"), "invertible": True,
             "pureza": (c.get("pureza") or {}).get("valor"), "pureza_metodo": (c.get("pureza") or {}).get("metodo"),
             "fecha_dato": c.get("fecha_dato"), "S": c.get("S"), "rango": c.get("rango"), "frontera": c.get("frontera"),
             "veredicto": c.get("veredicto"), "en_top_n": True, "alternativa": False,
             "alertas": [a.get("senal") for a in c.get("alertas") or []]}
        for k in COMPONENTES:
            f[f"comp_{k}"] = (c.get("desglose") or {}).get(k)
        ic, icr = c.get("ic90_S") or [None, None], c.get("ic90_rango") or [None, None]
        f.update({"ic90_S_inf": ic[0], "ic90_S_sup": ic[1], "ic90_rango_inf": icr[0], "ic90_rango_sup": icr[1]})
        out.append(f)
    return out


def construir_hojas(p: Dict, datos: Optional[Dict] = None, plantilla: bool = False) -> Dict[str, Dict]:
    """Devuelve {hoja: {"columnas": [...], "filas": [...]}} en orden."""
    datos = datos or {}
    hojas: Dict[str, Dict] = {}
    ident = [{"campo": k, "valor": _txt(p.get(k))} for k in ("pet_id", "run_ids", "rec_id", "fecha", "data_cutoff",
                                                            "methodology_version")]
    if not plantilla:
        amb = p.get("ambito") or {}
        ident += [{"campo": "ambito", "valor": amb.get("nombre")}, {"campo": "tipo_objeto", "valor": amb.get("tipo_objeto")},
                  {"campo": "veredicto", "valor": (p.get("veredicto") or {}).get("valor")}]
        if p.get("x_ejemplo"):
            ident.append({"campo": "AVISO", "valor": "DATOS ILUSTRATIVOS: ejemplo, no un análisis real"})
    ident.append({"campo": "generado_por", "valor": f"HT-10 v{VERSION}"})
    for h, d in DESCRIPCION_HOJAS.items():
        ident.append({"campo": f"hoja {h}", "valor": d})
    hojas["Leeme"] = {"columnas": ["campo", "valor"], "filas": ident}
    hojas["Puntuaciones"] = {"columnas": COLUMNAS["Puntuaciones"], "filas": [] if plantilla else _filas_puntuaciones(p)}
    hojas["Cifras"] = {"columnas": COLUMNAS["Cifras"], "filas": [] if plantilla else list(datos.get("cifras") or [])}
    hojas["Fuentes"] = {"columnas": COLUMNAS["Fuentes"], "filas": [] if plantilla else list(datos.get("fuentes") or [])}
    tipos = [] if plantilla else [t for t in TIPOS if ((p.get("candidatos_por_tipo") or {}).get(t) or {}).get("aplicable")]
    if plantilla:
        hojas["Universo_RV"] = {"columnas": COLUMNAS["Universo"], "filas": []}
    for t in tipos:
        filas = _filas_universo(p, t, datos)
        extra = sorted({k for f in filas for k in f} - set(COLUMNAS["Universo"]))
        hojas[f"Universo_{t}"] = {"columnas": COLUMNAS["Universo"] + extra, "filas": filas}
    hojas["Escenarios"] = {"columnas": COLUMNAS["Escenarios"], "filas": [] if plantilla else [
        {k: e.get(k) for k in COLUMNAS["Escenarios"]} for e in p.get("escenarios") or []]}
    hojas["Sensibilidades"] = {"columnas": COLUMNAS["Sensibilidades"], "filas": [] if plantilla else list(
        datos.get("sensibilidades") or p.get("sensibilidades") or [])}
    hojas["Pronosticos"] = {"columnas": COLUMNAS["Pronosticos"], "filas": [] if plantilla else [
        {k: x.get(k) for k in COLUMNAS["Pronosticos"]} for x in p.get("pronosticos_detalle") or []]}
    hojas["Artefactos"] = {"columnas": COLUMNAS["Artefactos"], "filas": [] if plantilla else list(datos.get("artefactos") or [])}
    enc = []
    if not plantilla:
        for b, lst in (p.get("paquete_para_bloque_C") or {}).items():
            for e in lst or []:
                ins = e.get("instrumento") or {}
                pu = e.get("puntuacion") or {}
                enc.append({"bloque_c": b, "cand_id": e.get("cand_id"), "tipo_activo": e.get("tipo_activo"),
                            "nombre": ins.get("nombre"), "isin": ins.get("isin"), "S": pu.get("S"), "rango": pu.get("rango"),
                            "veredicto": e.get("veredicto_candidato"), "eslabon_id": e.get("eslabon_id"),
                            "origen_seleccion": e.get("origen_seleccion"), "preguntas_para_C": e.get("preguntas_para_C")})
    hojas["Encargos_C"] = {"columnas": COLUMNAS["Encargos_C"], "filas": enc}
    esl, ops, emg = [], [], []
    for e in [] if plantilla else ((p.get("mapa_cadena_valor") or {}).get("eslabones") or []):
        m = e.get("metricas") or {}
        cb = e.get("cuello_botella") or {}
        at = e.get("atractivo") or {}
        de = at.get("desglose") or {}
        tam = m.get("tamano") if isinstance(m.get("tamano"), dict) else {"valor": m.get("tamano")}
        ind = cb.get("indicadores") or []
        esl.append({"eslabon_id": e.get("eslabon_id"), "padre": e.get("padre"), "nivel": e.get("nivel"), "nombre": e.get("nombre"),
                    "papel_ambito": e.get("papel_ambito"), "tamano": tam.get("valor"), "unidad": tam.get("unidad"),
                    "crecimiento_anual": m.get("crecimiento_anual"), "margen_bruto": (m.get("margen_tipico") or {}).get("bruto"),
                    "margen_operativo": (m.get("margen_tipico") or {}).get("operativo"), "poder_negociacion": m.get("poder_negociacion"),
                    "hhi": m.get("hhi"), "concentracion_pais": m.get("concentracion_pais"), "es_cuello": cb.get("es_cuello"),
                    "indicadores_rojo": sum(1 for x in ind if x.get("estado") == "ROJO"),
                    "indicadores_ambar": sum(1 for x in ind if x.get("estado") == "AMBAR"),
                    "indicadores": "; ".join(f"{x.get('indicador')}={x.get('valor')} ({x.get('estado')})" for x in ind),
                    "severidad": cb.get("severidad"), "persistencia": cb.get("persistencia"), "relevancia_valor": cb.get("relevancia_valor"),
                    "PCB": cb.get("PCB"), "cuello_material": cb.get("material"), "senal_resolucion": cb.get("senal_resolucion"),
                    **{f"AE_{k}": de.get(k) for k in ("crecimiento", "margen_roic", "poder_negociacion", "cuello", "expectativas_inv",
                                                      "sustitucion_inv")},
                    "AE": at.get("AE"), "calc_cuello": cb.get("calc_id"), "calc_AE": at.get("calc_id")})
        for o in e.get("opciones") or []:
            ic = o.get("ic90_S") or [None, None]
            ops.append({"eslabon_id": e.get("eslabon_id"), **{k: o.get(k) for k in ("rango", "cand_id", "nombre", "tipo_activo",
                        "rol_en_eslabon", "pureza_eslabon", "S", "veredicto", "en_top_n_tipo", "motivo")},
                        "ic90_S_inf": ic[0], "ic90_S_sup": ic[1]})
        for g in e.get("emergentes") or []:
            fi = g.get("financiacion_conocida") or {}
            ie = g.get("instrumento_exposicion") or {}
            cr = g.get("criterios") or {}
            emg.append({"eslabon_id": e.get("eslabon_id"), "emg_id": g.get("emg_id"), "nombre": g.get("nombre"), "tipo": g.get("tipo"),
                        "financiacion_importe": fi.get("importe"), "financiacion_divisa": fi.get("divisa"), "ultima_ronda": fi.get("ultima_ronda"),
                        "tecnologia_o_ventaja": g.get("tecnologia_o_ventaja"), "senales_traccion": g.get("senales_traccion"),
                        "via_exposicion": g.get("via_exposicion"), "instrumento": ie.get("nombre"), "cand_id": ie.get("cand_id"),
                        "fuera_de_filtros": ie.get("fuera_de_filtros"),
                        **{f"crit_{k}": cr.get(k) for k in ("tecnologia", "traccion", "equipo", "financiacion", "posicion_cadena", "via_exposicion")},
                        "PEM": g.get("PEM"), "etiqueta": g.get("etiqueta")})
    hojas["Eslabones"] = {"columnas": COLUMNAS["Eslabones"], "filas": esl}
    hojas["Opciones_eslabon"] = {"columnas": COLUMNAS["Opciones_eslabon"], "filas": ops}
    hojas["Emergentes"] = {"columnas": COLUMNAS["Emergentes"], "filas": emg}
    return hojas


def escribir(hojas: Dict[str, Dict], carpeta, nombre: str) -> Dict:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)
    dir_csv = carpeta / f"{nombre}_csv"
    dir_csv.mkdir(exist_ok=True)
    cab = Font(bold=True, color="FFFFFF")
    relleno = PatternFill("solid", fgColor="1F4E79")
    recuento = {}
    for hoja, d in hojas.items():
        ws = wb.create_sheet(hoja[:31])
        cols = d["columnas"]
        ws.append(cols)
        for c in ws[1]:
            c.font, c.fill = cab, relleno
            c.alignment = Alignment(vertical="center", wrap_text=True)
        for f in d["filas"]:
            ws.append([_txt(f.get(c)) for c in cols])
        ws.freeze_panes = "A2"
        if d["filas"]:
            ws.auto_filter.ref = ws.dimensions
        for i, c in enumerate(cols, start=1):
            largo = max([len(str(c))] + [min(len(str(_txt(f.get(c)))), 60) for f in d["filas"][:200]])
            ws.column_dimensions[get_column_letter(i)].width = max(10, min(largo + 2, 62))
        with open(dir_csv / f"{hoja}.csv", "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(cols)
            for f in d["filas"]:
                w.writerow([_txt(f.get(c)) for c in cols])
        recuento[hoja] = len(d["filas"])
    wb.properties.title = nombre
    wb.properties.creator = f"Bloque B · HT-10 v{VERSION}"
    ruta = carpeta / f"{nombre}.xlsx"
    wb.save(ruta)
    return {"herramienta": "HT-10", "version": VERSION, "xlsx": str(ruta), "csv": str(dir_csv), "filas_por_hoja": recuento}


def generar_anexo(paquete: Dict, carpeta, nombre: Optional[str] = None, datos: Optional[Dict] = None) -> Dict:
    nombre = nombre or f"{paquete.get('fecha', 'AAAA-MM-DD')}_anexo-datos_{paquete.get('pet_id', 'PET-B')}"
    return escribir(construir_hojas(paquete, datos), carpeta, nombre)


def generar_plantilla(carpeta, nombre: str) -> Dict:
    p = {"pet_id": "PET-B-AAAA-NNNN", "run_ids": ["RUN-B-AAAA-NNNN"], "rec_id": "REC-B-AAAA-NNNN", "fecha": "AAAA-MM-DD",
         "data_cutoff": "AAAA-MM-DD", "methodology_version": "2.1"}
    return escribir(construir_hojas(p, plantilla=True), carpeta, nombre)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-10 · Anexo de datos y cálculos (XLSX y CSV)")
    ap.add_argument("paquete", nargs="?", help="paquete_analisis_mercado (JSON)")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--datos", help="JSON datos_anexo {cifras, fuentes, universo{tipo:[...]}, sensibilidades, artefactos}")
    ap.add_argument("--nombre")
    ap.add_argument("--plantilla", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.plantilla:
            res = generar_plantilla(a.salida, a.nombre or "Plantilla - Anexo de datos y cálculos - Bloque B - V2.0")
        else:
            p = json.load(open(a.paquete, encoding="utf-8"))
            d = json.load(open(a.datos, encoding="utf-8")) if a.datos else None
            res = generar_anexo(p, a.salida, a.nombre, d)
    except (OSError, json.JSONDecodeError, KeyError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
