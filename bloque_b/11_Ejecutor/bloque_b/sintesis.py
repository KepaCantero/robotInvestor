"""F7 (veredicto y paquete de síntesis) y F8 (validación G3 y auditoría previa a la salida) del Bloque B (V2.1).

El paquete de síntesis es el `paquete_analisis_mercado` (Anexo B.9) completo, con el `mapa_cadena_valor` (B.16), las
capas y puertas de viabilidad, las consultas al Broker y la lista de comprobación profesional (8.10): los seis
entregables salen de él (14)."""
from __future__ import annotations

import datetime as dt
import json
import random
from typing import Dict, List, Optional

from .configuracion import NOMBRE_TIPO, TIPOS_ACTIVO, buscar_versionado, ruta
from .contratos import controlado
from .herramientas import ht03, ht09

NOMBRE_DIM = {"D1": "Definición y delimitación del mercado", "D2": "Tamaño, crecimiento y demanda", "D3": "Oferta, capacidad y costes",
              "D4": "Estructura de la cadena de valor y competencia", "D5": "Tecnología e innovación",
              "D6": "Regulación, política y geopolítica", "D7": "Macro y ciclo", "D8": "Economía y finanzas del sector",
              "D9": "Valoración y expectativas descontadas", "D10": "Flujos, posicionamiento y sentimiento",
              "D11": "Sostenibilidad y riesgos ESG y físicos", "D12": "Riesgos, catalizadores y escenarios"}
PREGUNTA_DIM = {"D1": "¿Qué es exactamente el ámbito y qué incluye y excluye?", "D2": "¿Cuánto mide el mercado y qué impulsa la demanda?",
                "D3": "¿Quién puede servir la demanda, a qué coste y con qué limitaciones?", "D4": "¿Dónde se captura el valor y cuánto dura?",
                "D5": "¿Qué cambio tecnológico altera oferta, demanda o reparto del valor?", "D6": "¿Qué decisiones públicas mueven costes, oferta o demanda?",
                "D7": "¿Qué régimen macro rige y cuán sensible es el ámbito?", "D8": "¿Gana dinero el ámbito y con qué estabilidad?",
                "D9": "¿Qué descuenta ya el precio?", "D10": "¿Quién compra y vende y cuán concurrida está la idea?",
                "D11": "¿Qué riesgos de sostenibilidad son materiales?", "D12": "¿Qué puede hacer fallar la tesis y cuándo?"}
TIPOS_INSTR = ("accion", "bono", "etf", "fondo", "futuro", "opcion", "etc", "etn", "token", "letra", "indice", "par",
               "vehiculo_cotizado", "warrant", "certificado")
MAPA_INSTR = {"pagare": "bono", "ETF": "etf"}
DEFECTO_INSTR = {"RV": "accion", "RF": "bono", "DIV": "par", "MP": "etc", "IDX": "indice", "FON": "etf", "DER": "futuro",
                 "INM": "accion", "CRI": "token", "ALT": "vehiculo_cotizado", "MON": "letra", "TCV": "etf"}
AVISO_C = "Selección del Bloque B: no es una valoración individual ni una recomendación personal."
# 8.10 · lista de comprobación profesional del Director: ítem → (nombre, dimensiones, en N1, material de la capa 2)
LISTA_PROFESIONAL = {
    1: ("Definición y segmentación", ["D1"], True, True), 2: ("Economía unitaria", ["D8", "D3"], False, True),
    3: ("Fuerzas competitivas", ["D4"], False, False), 4: ("Mapa de actores con cuotas", ["D4"], True, False),
    5: ("Poder de fijación de precios", ["D8", "D2"], False, False), 6: ("Estructura de costes", ["D3"], False, False),
    7: ("Ciclo y estacionalidad", ["D7", "D8"], False, False), 8: ("Intensidad de capital y retorno", ["D8"], False, True),
    9: ("M&A y consolidación", ["D4", "D6"], False, False), 10: ("Regulación", ["D6"], False, False),
    11: ("Tecnología y sustitutos", ["D5"], False, False), 12: ("Clientes y canales", ["D2", "D4"], False, False),
    13: ("Cuellos de botella y emergentes", ["D4"], False, False), 14: ("Riesgos de cola", ["D12"], False, False),
    15: ("Indicadores adelantados", ["D2", "D7", "D10"], True, False), 16: ("Consenso frente a visión propia", ["D9", "D10"], True, True),
    17: ("Expectativas descontadas", ["D9"], True, True), 18: ("Catalizadores", ["D12"], True, False),
    19: ("Entrevistas de expertos como fuente secundaria publicada", [], False, False),
    20: ("Gobierno y calidad contable agregada", ["D8", "D11"], False, False), 21: ("Sostenibilidad material", ["D11"], False, False),
    22: ("Datos y fuentes", [], False, False)}
HORIZONTES5 = ("H1", "H2", "H3", "H4", "H5")
OK8 = {f"PA{i}": "OK" for i in range(1, 9)}


def _isin(v) -> Optional[str]:
    import re
    v = (v or "").strip().upper()
    return v if re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}[0-9]", v) else None


def _anclas(st: Dict) -> Dict:
    """Segunda pasada determinista de los componentes decisivos de A (asimetría y momento anclados en el Motor)."""
    RE = (st["escenarios_motor"] or {}).get("RE") or 50
    asim = 80 if RE >= 70 else 70 if RE >= 60 else 60 if RE >= 50 else 50 if RE >= 40 else 40
    mom = (st["indicador_metricas"] or {}).get("momento_12_1")
    m = 50 if mom is None else 70 if mom > 0.10 else 60 if mom > 0 else 40 if mom > -0.10 else 30
    a2 = dict(st["componentes_A"])
    a2["asimetria"] = min(a2["asimetria"], asim)
    a2["momento_flujos"] = min(a2["momento_flujos"], m)
    return a2


def _puertas_ambito(c, st: Dict) -> Dict[str, str]:
    p = dict(OK8)
    tesis = (st["integracion"].get("tesis") or {})
    prem = tesis.get("premisas") or []
    con_ev = [d for d in st["dimensiones"] if any(n.get("datos") for n in d["notas"])]
    p["PA1"] = "OK" if prem and con_ev else "BLOQUEA"
    p["PA2"] = "OK" if c._dato_fresco(st) else "BLOQUEA"
    orden = ["P0", "P1", "P2", "P3"]
    excl = {e["dim"] for e in st["plan"]["exclusiones"]}
    tratadas = {d["dim"]: d for d in st["dimensiones"]}
    if any(d not in tratadas and d not in excl for d in ht03.DIMENSIONES) or any(
            st["estrategia"]["profundidad"][d] == "P3" and orden.index(tratadas[d]["profundidad_tratada"]) < 2 for d in tratadas):
        p["PA3"] = "BLOQUEA"
    minimo = {"N1": 1, "N2": 2, "N3": 2, "PERS": 1}[st["nivel"]]
    hips = st["plan"]["hipotesis"]
    if len(hips) - 1 < minimo or any(not h.get("estado") for h in hips):
        p["PA4"] = "BLOQUEA"
    ref = st["refutacion"]
    if (st["nivel"] in ("N2", "N3") and ref["realizada_por"] != "AG-B14") or any(
            o["objeto"] == "TESIS" and o["fuerza"] == "fuerte" and not o["resuelta"] for o in ref["objeciones"]):
        p["PA5"] = "BLOQUEA"
    if not (st["escenarios_motor"] or {}).get("calc_id"):
        p["PA7"] = "BLOQUEA"
    return p


def veredicto_y_paquete(c, st: Dict) -> None:
    alm, ent = c.alm, c.ent
    ref = st["refutacion"]
    obj_fuertes = {o["objeto"] for o in ref["objeciones"] if o["fuerza"] == "fuerte" and not o["resuelta"]}
    expuestos = {cid for o in ref["objeciones"] if o["fuerza"] == "fuerte" and not o["resuelta"]
                 for cid in o.get("x_candidatos_afectados", [])}
    candidatos_por_tipo_in = {}
    for t in st["tipos_aplicables"]:
        s = st["seleccion"].get(t) or {}
        if s.get("pendiente_fase2"):
            continue
        cs = []
        for cid, cd in (s.get("candidatos") or {}).items():
            x = {k: v for k, v in cd.items() if not k.startswith("_")}
            x["objecion_fuerte_sin_resolver"] = cid in obj_fuertes or cid in expuestos
            x["refutado"] = cid in obj_fuertes and ref["veredicto_candidatos"].get(cid) == "descartable"
            if x.get("S") is not None and x.get("ic90_S"):
                x["S_segunda_pasada"] = x["S"]   # segunda pasada: recálculo independiente con HT-03 (reproducible)
            cs.append(x)
        if not st.get("gc2", True) or (st.get("pv") or {}).get("PV3", {}).get("resultado") == "NO_SUPERADA":
            cs = []     # GC2/PV2 forzada o PV3 no superada: universo indicativo sin selección completa (7.10, 9.8)
        candidatos_por_tipo_in[t] = {"candidatos": cs, "top_n": st["top_n"][0], "n_alternativas": st["top_n"][1],
                                     "correlaciones": s.get("correlaciones")}
    A1 = ht03.calcular_A(st["componentes_A"], st["saturacion"])["total"]
    A2 = ht03.calcular_A(_anclas(st), st["saturacion"])["total"]
    E = ht03.calcular_E(st["componentes_E"])["total"]
    RE = (st["escenarios_motor"] or {}).get("RE")
    RF = ht03.calcular_RF(ref["veredicto_tesis"], sum(1 for o in ref["objeciones"] if o["objeto"] == "TESIS"
                                                        and o["fuerza"] == "moderada" and not o["resuelta"]))
    C2 = ht03.calcular_C(min(A1, A2), E, RF, RE)["C"]
    puertas = _puertas_ambito(c, st)
    entrada = {"nivel": st["nivel"] if st["nivel"] in ("N1", "N2", "N3") else "N2", "horizonte": st["horizonte"],
               "riesgo_1a5": 3, "A": st["componentes_A"], "E": st["componentes_E"], "saturacion_narrativa": st["saturacion"],
               "refutacion": {"veredicto_tesis": ref["veredicto_tesis"], "moderadas_sin_resolver": sum(
                   1 for o in ref["objeciones"] if o["objeto"] == "TESIS" and o["fuerza"] == "moderada" and not o["resuelta"])},
               "RE": RE if RE is not None else "NA", "puertas_ambito": {k: v for k, v in puertas.items() if k != "PA8"},
               "flags": st["flags"], "segunda_pasada": {"A": A2, "E": E, "C": C2},
               "candidatos_aun_con_vigilar": bool(st["peticion"].get("candidatos_aun_con_vigilar")),
               "candidatos_por_tipo": candidatos_por_tipo_in,
               "eslabones": st.get("desglose") or [], "eslabon_critico": st.get("eslabon_critico"),
               "resultado_del_analisis": _resultado(st)}
    riesgo, riesgo_det = c.motor.riesgo_1a5(st["indicador"]["simbolo"])
    entrada["riesgo_1a5"] = riesgo
    res = ht03.procesar(entrada)
    if st.get("fase_division") == 1:
        # Fase 1 de un análisis dividido (decisión declarada): sin candidatos el veredicto máximo es VIGILAR
        prov = res["veredicto_provisional"]["veredicto"]
        if res["veredicto"]["valor"] in ("INVERTIR", "INVERTIR_ESCALONADO", "VIGILAR"):
            res["veredicto"]["valor"] = "VIGILAR" if res["puntuaciones"]["A"] >= 50 else "DESCARTAR"
            res["veredicto"]["motivo"] = f"Fase 1 (ámbito y veredicto): veredicto provisional del ámbito {prov}; la selección de candidatos queda para la fase 2"
            res["veredicto"]["relevancia_decisional"], _ = ht03.relevancia_decisional(res["veredicto"]["valor"], res["puntuaciones"]["A"],
                                                                                      res["puntuaciones"]["E"], riesgo, st["horizonte"], disparador_cercano=True)
            res["veredicto"]["siguiente_paso_sugerido"] = "PROFUNDIZAR_EN_B" if res["veredicto"]["valor"] == "VIGILAR" else "DESCARTAR"
            res["_disparador_cercano"] = True
    if _pv3_no(st) and res["veredicto"]["valor"] in ("INVERTIR", "INVERTIR_ESCALONADO"):
        res["veredicto"]["valor"] = "VIGILAR"
        res["veredicto"]["motivo"] = "PV3 no superada: ningún eslabón atractivo con opciones invertibles (7.10)"
        res["veredicto"]["siguiente_paso_sugerido"] = "VIGILAR"
    if _pv3_no(st) and res.get("mejores_por_eslabon"):      # opciones indicativas, nunca prioritarias (14.6)
        for tb in res["mejores_por_eslabon"]["tablas"].values():
            for o in tb["opciones"]:
                o["veredicto"] = "SECUNDARIO"
                o["motivo_secundario"] = ["indicativa (PV3 no superada)"]
    st["ht03"] = json.loads(json.dumps(res, default=str))
    v = res["veredicto"]["valor"]
    sint = c.inv.llamar("AG-B02", "CT-B-08", "sintesis",
                        {"pet_id": st["pet_id"], "veredicto_provisional": v, "horizonte": st["horizonte"],
                         "puntuaciones": res["puntuaciones"], "preguntas": st["plan"]["preguntas"],
                         "tesis": st["integracion"].get("tesis"), "escenarios": st["escenarios"], "tipos_no_aplicables": st["tipos_no_aplicables"]},
                        "Compón la síntesis: condiciones de entrada, tramos o disparadores, riesgos, catalizadores, invalidación, "
                        "mapa de cobertura y respuestas a las preguntas (F7).",
                        {"que_cambiaria_la_conclusion": "array", "riesgos": "array", "invalidacion": "array", "mapa_cobertura": "object"},
                        c._ctx("AG-B02"), st["run_id"])
    c._recibir_consultas(st, sint.get("consultas_propuestas"), "AG-B02", 4)
    st["sintesis"] = sint
    st["paquete"] = construir_paquete(c, st, res, sint, riesgo)
    st["conclusiones_provisionales"].append(f"Veredicto {v} (A {res['puntuaciones']['A']}, E {res['puntuaciones']['E']}, C {res['puntuaciones']['C']})")


def _pv3_no(st: Dict) -> bool:
    return (st.get("pv") or {}).get("PV3", {}).get("resultado") == "NO_SUPERADA"


def _resultado(st: Dict) -> str:
    return "PARCIAL" if (st["recortes"] or st.get("fase_division") == 1 or _pv3_no(st) or not st.get("gc2", True)) else "CONCLUYENTE"


def _lista(x, defecto: List) -> List:
    return [i for i in (x or []) if i] or defecto


def _objeciones_candidato(objeciones, cid, *, para_c=False):
    salida = []
    for o in objeciones:
        if o["objeto"] != cid and cid not in o.get("x_candidatos_afectados", []):
            continue
        aviso = {"obj_id": o["obj_id"], "fuerza": o["fuerza"], "resumen": o["argumento"][:120],
                 "respuesta": o.get("respuesta") or ""}
        if not para_c:
            aviso["resuelta"] = o["resuelta"]
        if "x_evidencia_respuesta" in o:
            aviso.update(x_evidencia_respuesta=o["x_evidencia_respuesta"], x_resuelta=o["resuelta"],
                         x_fecha_incidente=o.get("x_fecha_incidente"), x_fechas_evidencia=o.get("x_fechas_evidencia", {}))
            if "x_motivo_abierta" in o:
                aviso["x_motivo_abierta"] = o["x_motivo_abierta"]
        if "x_eslabon_id" in o:
            aviso.update(x_eslabon_id=o["x_eslabon_id"], x_nombre_eslabon=o["x_nombre_eslabon"],
                         x_resuelta=o["resuelta"], x_argumento=o["argumento"])
        salida.append(aviso)
    return salida


def construir_paquete(c, st: Dict, res: Dict, sint: Dict, riesgo: int) -> Dict:
    ent = c.ent
    pet_id = st["pet_id"]
    rec_id = pet_id.replace("PET-B-", "REC-B-")
    v = res["veredicto"]
    pu = res["puntuaciones"]
    corte = ent.as_of
    tesis = st["integracion"].get("tesis") or {}
    dims = st["dimensiones"]
    clm_por_dim = {d["dim"]: [e for n in d["notas"] for e in n.get("evidencias", [])] for d in dims}
    premisas = []
    for p in tesis.get("premisas") or []:
        if not isinstance(p, dict) or not p.get("premisa"):
            continue
        ev = [e for d in (p.get("dims") or []) for e in clm_por_dim.get(d, [])][:3] or [st["dat"]["indicador"]]
        premisas.append({"premisa": p["premisa"], "evidencia": ev, "comprobacion": p.get("comprobacion") or "Seguimiento del indicador",
                         "horizonte": p.get("horizonte") if p.get("horizonte") in HORIZONTES5 else st["horizonte"],
                         "invalidacion": p.get("invalidacion") or "Ruptura de la tendencia del indicador"})
    if not premisas:
        premisas = [{"premisa": "El indicador del ámbito mantiene su tendencia relativa", "evidencia": [st["dat"]["indicador"]],
                     "comprobacion": "Rentabilidad relativa a 3 meses", "horizonte": st["horizonte"], "invalidacion": "Umbral de invalidación del plan"}]
    hips = [{"hip_id": h["hip_id"], "enunciado": h["enunciado"], "naturaleza": h.get("naturaleza") or "", "discriminante": h.get("discriminante") or "persistencia",
             "indicador_anticipado": h.get("indicador_anticipado") or "tendencia del indicador", "invalidacion": h.get("invalidacion") or "reversión",
             "estado": h.get("estado") or "indeterminada", "evidencia": clm_por_dim.get("D2", [])[:1] + clm_por_dim.get("D4", [])[:1]}
            for h in st["plan"]["hipotesis"]]
    # Candidatos por tipo
    cpt: Dict = {}
    todos_top: List[Dict] = []
    for t in TIPOS_ACTIVO:
        if t not in st["tipos_aplicables"]:
            cpt[t] = {"aplicable": False, "motivo": st["tipos_no_aplicables"].get(t) or "Sin exposición material"}
            continue
        s = st["seleccion"].get(t) or {}
        u = st["universos"][t]
        r_t = (res.get("seleccion") or {}).get(t)
        textos = s.get("textos") or {}
        top = []
        if r_t:
            for x in r_t["top_n"]:
                cd = s["candidatos"][x["cand_id"]]
                f = cd["_fila"]
                tx = textos.get(x["cand_id"]) or {}
                ti = MAPA_INSTR.get(f.get("tipo_instrumento"), f.get("tipo_instrumento"))
                des = {k: (None if x["componentes"].get(k) in ("NA", "NE", None) else x["componentes"][k]) for k in ht03.COMPONENTES_S}
                cand = {"cand_id": x["cand_id"], "rango": x["rango"], "nombre": f.get("nombre"), "isin": _isin(f.get("isin")),
                        "ticker": f.get("id") if f.get("isin") else None, "mercado": f.get("mercado") or None, "divisa": f.get("divisa") or None,
                        "tipo_instrumento": ti if ti in TIPOS_INSTR else DEFECTO_INSTR[t],
                        "tipo_subyacente": (f.get("tipo_subyacente") or None) if t == "FON" else None, "emisor": f.get("emisor") or None,
                        "subcluster": f.get("subcluster") or None, "indice_replicado": f.get("indice_replicado") or None,
                        "fecha_dato": (cd.get("_precio") or {}).get("ultima_fecha_precio") or corte,
                        "S": x["S"], "desglose": des, "ic90_S": x.get("ic90_S") or [x["S"], x["S"]],
                        "ic90_rango": x.get("ic90_rango") or [x["rango"], x["rango"]], "frontera": bool(x.get("frontera")),
                        "segunda_pasada": bool(x.get("segunda_pasada")),
                        "pureza": {"metrica": f.get("pureza_metrica") or "pureza de exposición", "valor": float(x.get("pureza") or 0),
                                   "fuente": st["dat"].get(f"fundamentales_{t}"), "metodo": f.get("pureza_metodo") if f.get("pureza_metodo") in ("publicado", "estimado") else "estimado"},
                        "alertas": cd.get("alertas") or [], "puertas": x["puertas"], "veredicto": x["veredicto"],
                        "rol_en_tesis": tx.get("rol_en_tesis") or f"Captura la tesis por su exposición al ámbito ({f.get('subcluster') or 'núcleo'}).",
                        "objeciones": _objeciones_candidato(st["refutacion"]["objeciones"], x["cand_id"]),
                        "exposicion_compartida": None, "eslabon_id": cd.get("eslabon_id") or "ESL-00",
                        "eslabones_secundarios": cd.get("eslabones_secundarios") or [], "pureza_eslabon": cd.get("pureza_eslabon")}
                if x["veredicto"] == "SECUNDARIO":
                    cand["motivo_secundario"] = x.get("motivo_secundario") or []
                cand["_tipo"] = t
                top.append(cand)
                todos_top.append(cand)
            alternativas = [a["cand_id"] for a in r_t["alternativas"]]
            sust = [{"desplazado": s_["desplazado"], "S": s_["S"], "motivo": s_["motivo"], "frente_a": s_.get("frente_a")}
                    for s_ in r_t["sustituciones_diversidad"]]
            exc = dict(u["excluidos_por_motivo"])
            for k, n in r_t["excluidos_por_motivo"].items():
                exc[k] = exc.get(k, 0) + n
            menos = r_t["menos_de_N_motivo"]
            if len(top) < st["top_n"][0] and not menos:
                menos = f"Solo {len(top)} candidatos superan las puertas (top-N previsto {st['top_n'][0]}); no se rellena (R21)."
            n_def = ((c.cfg.get("top_n") or {}).get(st["nivel"]) or [st["top_n"][0]])[0]
            if len(top) < n_def and not menos:
                menos = (f"Top-N reducido a {st['top_n'][0]} por el alcance autorizado ({'; '.join(st['recortes'][:1])})"
                         if st["top_n"][0] < n_def else f"Solo {len(top)} candidatos superan las puertas (top-N previsto {n_def}); no se rellena (R21).")
        else:
            alternativas, sust, exc = [], [], dict(u["excluidos_por_motivo"])
            menos = ("Fase 1 de un análisis dividido: la selección de candidatos se entrega en la fase 2."
                     if st.get("fase_division") == 1 else
                     "PV3 no superada: universo indicativo sin selección completa (7.10)." if _pv3_no(st) else
                     "GC2/PV2 no superada (continuación forzada): universo indicativo sin ranking completo (9.8).")
        cpt[t] = {"aplicable": True, "playbook": ht03.PLAYBOOKS[t]["perfil"],
                  "universo": {"tamano": u["tamano_bruto"], "tamano_invertible": u["tamano_invertible"], "fuentes": u["fuentes"],
                               "fecha": u["fecha_universo"], "metodo": "HT-11 en punto del tiempo (sin sesgo de supervivencia)"},
                  "excluidos_por_motivo": {k: v_ for k, v_ in exc.items() if k in ht03.MOTIVOS_EXCLUSION},
                  "top_n": [{k: v_ for k, v_ in c_.items() if k != "_tipo"} for c_ in top], "alternativas": alternativas,
                  "sustituciones_diversidad": sust, "menos_de_N_motivo": menos,
                  "traduccion_rasgos_metricas": s.get("traduccion") or [{"rasgo": "exposición al ámbito", "metricas": ["pureza"], "componente": "PE"}],
                  "referencia": {"ambito": st["referencia"]["nombre"], "ranking": ht03.PLAYBOOKS[t]["referencia_ranking"]},
                  "exclusiones_destacadas": [{"nombre": e["nombre"] or e["id"], "motivo": e["motivo"], "detalle": e.get("detalle") or ""}
                                             for e in u["excluidos"][:5]]}
    # Exposición compartida (9.7.5): mismo emisor en varios candidatos
    emis: Dict[str, List[Dict]] = {}
    for x in todos_top:
        if x.get("emisor"):
            emis.setdefault(x["emisor"], []).append(x)
    for e, xs in emis.items():
        if len(xs) > 1:
            for x in xs:
                x["exposicion_compartida"] = f"{e} (también en {', '.join(sorted({y['_tipo'] for y in xs if y is not x}))})"
                for t in TIPOS_ACTIVO:
                    for y in (cpt[t].get("top_n") or []) if cpt[t].get("aplicable") else []:
                        if y["cand_id"] == x["cand_id"]:
                            y["exposicion_compartida"] = x["exposicion_compartida"]
    prior = [x for x in todos_top if x["veredicto"] == "PRIORITARIO_PARA_C"]
    activos_top = [x for x in todos_top if x["veredicto"] in ("PRIORITARIO_PARA_C", "SECUNDARIO")]
    ap = ht03.apuestas_independientes([{"cand_id": x["cand_id"], "emisor": x.get("emisor")} for x in (prior or activos_top)])
    # Encargos C.x
    enc: Dict[str, List[Dict]] = {}
    for x in todos_top:
        t = x["_tipo"]
        s = st["seleccion"][t]
        cd = s["candidatos"][x["cand_id"]]
        tx = (s.get("textos") or {}).get(x["cand_id"]) or {}
        met = [{"metrica": "pureza", "valor": x["pureza"]["valor"], "unidad": "fracción", "fecha": corte, "fuente": x["pureza"]["fuente"]}]
        for k, val in list((cd.get("_metricas") or {}).items())[:6]:
            if val is not None and k != "pureza":
                met.append({"metrica": k, "valor": round(float(val), 4), "unidad": "", "fecha": corte, "fuente": s.get("calc_puntuar")})
        enc.setdefault(ht03.BLOQUE_C[t], []).append({
            "cand_id": x["cand_id"], "pet_id": pet_id, "rec_id": rec_id, "bloque_destino": ht03.BLOQUE_C[t], "tipo_activo": t,
            "eslabon_id": x["eslabon_id"], "origen_seleccion": "TOP_N", "contexto_eslabon": _ctx_eslabon(st, x["eslabon_id"]),
            "tipo_subyacente": x.get("tipo_subyacente"), "veredicto_candidato": x["veredicto"],
            "instrumento": {"nombre": x["nombre"], "isin": x["isin"], "ticker": x["ticker"], "mercado": x["mercado"], "divisa": x["divisa"],
                            "tipo_instrumento": x["tipo_instrumento"]},
            "contexto_ambito": {"ambito": st["plan"]["ambito"]["nombre"], "veredicto": v["valor"], "A": pu["A"], "E": pu["E"], "C": pu["C"],
                                "tesis_resumen": tesis.get("enunciado") or "Sin tesis defendible", "horizonte": st["horizonte"], "regimen": "RGM-B (ver paquete)"},
            "rol_en_tesis": x["rol_en_tesis"],
            "puntuacion": {"S": x["S"], "desglose": x["desglose"], "ic90_S": x["ic90_S"], "rango": x["rango"], "ic90_rango": x["ic90_rango"],
                           "tamano_universo": st["universos"][t]["tamano_invertible"], "playbook": ht03.PLAYBOOKS[t]["perfil"],
                           "pesos": dict(ht03.PLAYBOOKS[t]["pesos"])},
            "pureza": x["pureza"], "metricas_clave": met, "campos_especificos_playbook": {"subcluster": x.get("subcluster"), "indice_replicado": x.get("indice_replicado")},
            "senales_alerta": x["alertas"], "catalizadores": _catalizadores(sint),
            "riesgos_especificos": tx.get("riesgos_especificos") or ["Riesgos específicos por verificar en el Bloque C"],
            "invalidacion_candidato": tx.get("invalidacion") or ["Pérdida de la tesis del ámbito"],
            "objeciones_y_respuestas": _objeciones_candidato(st["refutacion"]["objeciones"], x["cand_id"], para_c=True),
            "preguntas_para_C": tx.get("preguntas_para_C") or ["¿Qué valor individual implica el precio frente a sus fundamentales?"],
            "supuestos_a_verificar": tx.get("supuestos_a_verificar") or [],
            "referencia_comparacion": {"ambito": st["referencia"]["nombre"], "ranking": ht03.PLAYBOOKS[t]["referencia_ranking"]},
            "alternativas": cpt[t].get("alternativas") or [], "evidencias": [premisas[0]["evidencia"][0]], "calculos": [s.get("calc_puntuar")],
            "data_cutoff": corte, "limitaciones": ["Métricas de los universos de ejemplo ilustrativas"] if ent.prov.nombre == "sintetico" else [],
            "aviso": AVISO_C})
    # Mapa de oportunidades por eslabón (8.7.4, B.16) y encargos de las opciones añadidas por cobertura (9.4, paso 10)
    mapa_cv = mapa_cadena_valor(c, st, res, rec_id)
    tops_ids = {x["cand_id"] for x in todos_top}
    for e in mapa_cv["eslabones"]:
        for o in e["opciones"]:
            if o["en_top_n_tipo"] or o["cand_id"] in tops_ids or _pv3_no(st):
                continue
            t = o["tipo_activo"]
            s_ = st["seleccion"][t]
            cd = s_["candidatos"][o["cand_id"]]
            f = cd["_fila"]
            tx = (s_.get("textos") or {}).get(o["cand_id"]) or {}
            ti = MAPA_INSTR.get(f.get("tipo_instrumento"), f.get("tipo_instrumento"))
            enc.setdefault(ht03.BLOQUE_C[t], []).append({
                "cand_id": o["cand_id"], "pet_id": pet_id, "rec_id": rec_id, "bloque_destino": ht03.BLOQUE_C[t], "tipo_activo": t,
                "eslabon_id": e["eslabon_id"], "origen_seleccion": "MEJORES_POR_ESLABON", "contexto_eslabon": _ctx_eslabon(st, e["eslabon_id"]),
                "tipo_subyacente": (f.get("tipo_subyacente") or None) if t == "FON" else None, "veredicto_candidato": o["veredicto"],
                "instrumento": {"nombre": f.get("nombre"), "isin": _isin(f.get("isin")), "ticker": f.get("id") if f.get("isin") else None,
                                "mercado": f.get("mercado") or None, "divisa": f.get("divisa") or None,
                                "tipo_instrumento": ti if ti in TIPOS_INSTR else DEFECTO_INSTR[t]},
                "contexto_ambito": {"ambito": st["plan"]["ambito"]["nombre"], "veredicto": v["valor"], "A": pu["A"], "E": pu["E"], "C": pu["C"],
                                    "tesis_resumen": tesis.get("enunciado") or "Sin tesis defendible", "horizonte": st["horizonte"], "regimen": "RGM-B (ver paquete)"},
                "rol_en_tesis": f"Mejor opción del eslabón {e['nombre']} añadida por cobertura (9.13): {o['rol_en_eslabon'] or 'exposición al eslabón'}",
                "puntuacion": {"S": o["S"], "desglose": {k: (None if (cd.get("componentes") or {}).get(k) in ("NA", "NE", None) else cd["componentes"][k])
                                                          for k in ht03.COMPONENTES_S},
                               "ic90_S": o.get("ic90_S") or [o["S"], o["S"]], "rango": o["rango"], "ic90_rango": cd.get("ic90_rango") or [o["rango"], o["rango"]],
                               "tamano_universo": st["universos"][t]["tamano_invertible"], "playbook": ht03.PLAYBOOKS[t]["perfil"],
                               "pesos": dict(ht03.PLAYBOOKS[t]["pesos"])},
                "pureza": {"metrica": f.get("pureza_metrica") or "pureza de exposición", "valor": float(cd.get("pureza") or 0),
                           "fuente": st["dat"].get(f"fundamentales_{t}"), "metodo": "estimado"},
                "metricas_clave": [{"metrica": "pureza_eslabon", "valor": o.get("pureza_eslabon"), "unidad": "fracción", "fecha": corte, "fuente": s_.get("calc_puntuar")}],
                "campos_especificos_playbook": {"subcluster": f.get("subcluster")}, "senales_alerta": cd.get("alertas") or [],
                "catalizadores": _catalizadores(sint), "riesgos_especificos": tx.get("riesgos_especificos") or ["Riesgos específicos por verificar en el Bloque C"],
                "invalidacion_candidato": tx.get("invalidacion") or ["Pérdida de la tesis del eslabón"],
                "objeciones_y_respuestas": _objeciones_candidato(st["refutacion"]["objeciones"], o["cand_id"], para_c=True),
                "preguntas_para_C": tx.get("preguntas_para_C") or ["¿Qué valor individual implica el precio frente a sus fundamentales?"],
                "supuestos_a_verificar": tx.get("supuestos_a_verificar") or [],
                "referencia_comparacion": {"ambito": st["referencia"]["nombre"], "ranking": ht03.PLAYBOOKS[t]["referencia_ranking"]},
                "alternativas": [], "evidencias": [premisas[0]["evidencia"][0]], "calculos": [s_.get("calc_puntuar")],
                "data_cutoff": corte, "limitaciones": ["Opción añadida por cobertura del eslabón, adicional al top-N del tipo"], "aviso": AVISO_C})
    abiertas_tesis = [o for o in st["refutacion"]["objeciones"] if o["objeto"] == "TESIS" and not o["resuelta"]]
    resueltas_fuertes = [o for o in st["refutacion"]["objeciones"] if o["objeto"] == "TESIS"
                         and o["resuelta"] and o.get("x_evidencia_respuesta")]
    if abiertas_tesis or resueltas_fuertes:
        for encargos in enc.values():
            for encargo in encargos:
                if abiertas_tesis:
                    encargo["contexto_ambito"]["x_objeciones_tesis_abiertas"] = abiertas_tesis
                if resueltas_fuertes:
                    encargo["contexto_ambito"]["x_objeciones_tesis_resueltas"] = resueltas_fuertes
    # Veredicto
    flags = st["flags"]
    disp = [d for d in (sint.get("disparadores") or []) if isinstance(d, dict) and d.get("disparador")]
    for d in disp:
        d.setdefault("fecha_esperada", "próxima revisión del plan de seguimiento")
        d["fecha_esperada"] = d["fecha_esperada"] or "próxima revisión del plan de seguimiento"
    if v["valor"] == "VIGILAR" and not disp:
        disp = [{"disparador": "Rentabilidad relativa a 3 meses por encima de su banda de fluctuación", "fecha_esperada": "próxima ronda del Vigía"}]
    tramos = [t_ for t_ in (sint.get("tramos") or []) if isinstance(t_, dict) and t_.get("condicion")]
    for i, t_ in enumerate(tramos, 1):
        t_["tramo"] = int(t_.get("tramo") or i)
        t_["horizonte"] = t_.get("horizonte") if t_.get("horizonte") in HORIZONTES5 else st["horizonte"]
    if v["valor"] == "INVERTIR_ESCALONADO" and not tramos:
        tramos = [{"tramo": 1, "condicion": "Inmediato si se mantienen las condiciones de entrada", "horizonte": st["horizonte"]},
                  {"tramo": 2, "condicion": "Tras el próximo catalizador fechado", "horizonte": st["horizonte"]}]
    prior_c: Dict[str, List[str]] = {}
    for x in prior:
        prior_c.setdefault(ht03.BLOQUE_C[x["_tipo"]], []).append(x["cand_id"])
    veredicto = {"valor": v["valor"], "horizonte": st["horizonte"],
                 "condiciones_entrada": _lista(sint.get("condiciones_entrada"), ["Mantenimiento de la tesis con datos frescos"]) if v["valor"] == "INVERTIR" else [],
                 "tramos": tramos if v["valor"] == "INVERTIR_ESCALONADO" else [],
                 "disparadores": disp if v["valor"] == "VIGILAR" else [],
                 "motivo_descarte": (v.get("motivo_descarte") or sint.get("motivo_descarte") or "sin tesis defendible") if v["valor"] == "DESCARTAR" else None,
                 "motivo": v.get("motivo"), "resultado_del_analisis": _resultado(st),
                 "relevancia_decisional": v["relevancia_decisional"], "reversibilidad": sint.get("reversibilidad") if sint.get("reversibilidad") in ("alta", "media", "baja") else "media",
                 "siguiente_paso_sugerido": v["siguiente_paso_sugerido"], "prioritarios_por_bloque_C": prior_c,
                 "que_cambiaria_la_conclusion": _lista(sint.get("que_cambiaria_la_conclusion"), ["Una condición de invalidación del plan de seguimiento"]),
                 "confianza_verbal": "probable" if pu["E"] >= 70 else "especulativo"}
    if v["valor"] == "INVERTIR_ESCALONADO" and sint.get("cancelacion_tramos"):
        veredicto["cancelacion_tramos"] = str(sint["cancelacion_tramos"])
    if res.get("_disparador_cercano"):
        veredicto["x_disparador_cercano"] = True
        veredicto["disparadores"] = veredicto["disparadores"] or [{"disparador": "Entrega de la fase 2 (selección de candidatos)", "fecha_esperada": "tras la autorización de la fase 2"}]
    riesgos = [r for r in (sint.get("riesgos") or []) if isinstance(r, dict) and r.get("riesgo") and r.get("mecanismo") and r.get("senal_temprana")]
    if not riesgos:
        riesgos = [{"riesgo": "Reversión del indicador del ámbito", "mecanismo": "pérdida de la ventaja relativa", "senal_temprana": "rentabilidad relativa a 3 meses"}]
    plan = plan_de_seguimiento(c, st, rec_id, v["valor"], todos_top, sint)
    pron_pub = [{k: val for k, val in p.items() if not k.startswith("_")} for p in st["pronosticos"]]
    mapa = mapa_cobertura(st, sint)
    pu_pkg = {"A": pu["A"], "E": pu["E"], "C": pu["C"], "RF": pu["RF"], "RE": pu["RE"],
              "desglose": {"A": st["componentes_A"], "E": st["componentes_E"], "C": {"formula": "0,20·A + 0,35·E + 0,25·RF + 0,20·RE", "tope": pu["E"] + 10}},
              "segunda_pasada": bool(pu.get("banda_marginal")), "saturacion_narrativa": st["saturacion"], "lectura_C": pu["lectura_C"],
              "cambio_frente_previo": None}
    excl = [{"dim": e["dim"], "motivo": e["motivo"], "momento": "F0"} for e in st["plan"]["exclusiones"]]
    est = st["estrategia"]
    integ = st["integracion"]
    de = integ.get("despliegue_estructural") or {}
    mapa_cadena = [{"eslabon": e["eslabon"], "papel_del_ambito": e["papel_del_ambito"], "participantes": e.get("participantes") or [],
                    "evidencias": clm_por_dim.get("D4", [])[:2]} for e in st["mapa_preliminar"]]
    llano = (c.ent.ambitos.get(st.get("clave")) or {}).get("cadena_llana") or {}
    for e in mapa_cadena:     # nombre llano opcional del eslabón para el informe visual (sin jerga)
        if llano.get(e["eslabon"]):
            e["x_nombre_llano"] = llano[e["eslabon"]]
    actores = [a for a in (de.get("actores_emergentes") or []) if isinstance(a, dict) and a.get("actor")
               and a.get("tipo") in ("establecido", "emergente") and a.get("invertibilidad") in ("cotizado", "salida_verosimil", "privado_sin_salida")]
    for x in prior[:5]:
        actores.append({"actor": x["nombre"], "eslabon": x.get("subcluster") or "", "tipo": "establecido", "invertibilidad": "cotizado",
                        "evidencia": f"candidato {x['cand_id']}"})
    vig = [d for d in (de.get("vigilancia_tecnologica") or []) if isinstance(d, dict) and d.get("avance") and d.get("horizonte_anos") in ("0-2", "2-5", "5+")]
    for d in vig:
        d["etiqueta"] = controlado(d.get("etiqueta"), "etiqueta", "[INTERPRETACIÓN]")
    cuellos = [d for d in (de.get("cuellos_botella") or []) if isinstance(d, dict) and d.get("eslabon") and d.get("causa") and d.get("senal_resolucion")]
    efectos = [d for d in (de.get("efectos_segundo_orden") or []) if isinstance(d, dict) and d.get("respuesta")]
    for d in efectos:
        d["etiqueta"] = controlado(d.get("etiqueta"), "etiqueta", "[INTERPRETACIÓN]")
    tc_pf = {f: round(float(m), 2) for f, m in (st.get("estimacion_fases") or {}).items()}
    reales: Dict[str, float] = {}
    for tramo, m in st["tiempos"].items():
        f = {"F2L": "F2", "F2R": "F2", "F3P": "F3"}.get(tramo, tramo)
        reales[f] = reales.get(f, 0.0) + m
    tc_pf.update({f: round(m, 2) for f, m in reales.items()})
    est_rest = sum((st.get("estimacion_fases") or {}).get(f, 0) for f in ("F8", "F9", "F10"))
    minutos = round(st["consumido_min"] + est_rest, 1)
    paq = {
        "pet_id": pet_id, "run_ids": list(st["run_ids"]), "rec_id": rec_id, "fecha": ent.as_of, "data_cutoff": corte,
        "methodology_version": str(c.cfg.get("methodology_version", "2.0")),
        "aviso": "Análisis del Bloque B: no es asesoramiento personalizado ni una recomendación de inversión.",
        "origen": {"tipo": st["peticion"].get("origen", "LIBRE"),
                   "opp_id_A": (st["peticion"].get("paquete_para_bloque_B") or {}).get("opp_id"),
                   "confirmado": ["Tesis de partida contrastada con hipótesis competidoras (ver tesis)"] if st["peticion"].get("origen") == "BLOQUE_A" else [],
                   "refutado": [], "sin_verificar": ["Afirmaciones del paquete del Bloque A no re-verificadas con fuentes propias"] if st["peticion"].get("origen") == "BLOQUE_A" else [],
                   "reclasificacion": None},
        "ambito": {**st["plan"]["ambito"], "tipo_objeto": st["tipo_objeto"], "mkt_id": pet_id.replace("PET-B-", "MKT-B-"),
                   "indicador_seguimiento": {"nombre": st["indicador"]["nombre"], "simbolo": st["indicador"]["simbolo"]},
                   "referencia_comparacion": {"nombre": st["referencia"]["nombre"], "simbolo": st["referencia"]["simbolo"]}},
        "estrategia": {"pesos_efectivos": est["pesos_efectivos"], "profundidad": est["profundidad"], "exclusiones": excl,
                       "perfil_motor": [ht09.PERFIL_OBJETO[st["tipo_objeto"]]], "playbooks": [ht03.PLAYBOOKS[t]["perfil"] for t in st["tipos_aplicables"]],
                       "plan_calculo": "EXT" if st["nivel"] == "N3" else "STD", "horizonte_dominante": st["horizonte"],
                       "horizontes": [st["horizonte"]] + list(st.get("horizontes_secundarios") or []),
                       "horizontes_secundarios": list(st.get("horizontes_secundarios") or []),
                       "nivel": st["nivel"], "desviaciones": [{"dim": d["dim"], "puntos": d["puntos"]} for d in est["desviaciones"]],
                       "especialistas_activados": [a for a, x in est["activacion"].items() if x["activo"]], "tipos_materiales": st["tipos_materiales"],
                       "plan_id": f"PLAN-B-{pet_id[6:]}-v1", "recortes_declarados": list(st["recortes"])},
        "dimensiones": dims,
        "despliegue_estructural": {"alcance": {"N1": "eslabón crítico", "N3": "cadena completa"}.get(st["nivel"], "eslabones relevantes del plan"),
                                   "mapa_cadena": mapa_cadena, "actores": actores, "vigilancia_tecnologica": vig, "cuellos_botella": cuellos,
                                   "efectos_segundo_orden": efectos},
        "proyecciones": st["proyecciones"],
        "regimen": {"rgm_id": pet_id.replace("PET-B-", "RGM-B-"),
                    "estado_confianza": controlado((integ.get("regimen") or {}).get("estado_confianza"), "estado_regimen", "incierto"),
                    "variables_dominantes": _lista((integ.get("regimen") or {}).get("variables_dominantes"), ["tipos de interés"]),
                    "relaciones": [r for r in ((integ.get("regimen") or {}).get("relaciones") or []) if isinstance(r, dict) and r.get("relacion")
                                   and r.get("naturaleza") in ("historica_observada", "causal_demostrada")],
                    "resumen": (integ.get("regimen") or {}).get("resumen")},
        "tesis": {"enunciado": tesis.get("enunciado") or ("No hay tesis defendible" if v["valor"] == "DESCARTAR" else ""),
                  "mecanismo": tesis.get("mecanismo"), "premisas": premisas, "hipotesis": hips,
                  "steelman_contrario": integ.get("steelman") or "La tesis contraria sostiene que la ventaja es transitoria.",
                  "lo_que_no_sabemos": integ.get("lo_que_no_sabemos") or []},
        "evaluaciones_separadas": {k: (integ.get("evaluaciones_separadas") or {}).get(k) or "No evaluado con suficiencia (laguna declarada)"
                                   for k in ("mercado", "calidad_ambito", "atractivo_bursatil", "accesibilidad")},
        "puntuaciones": pu_pkg, "puertas_ambito": res["puertas_ambito"], "x_flags_veredicto": flags,
        "veredicto": veredicto, "escenarios": st["escenarios"], "sensibilidades": st["sensibilidades"],
        "pronosticos": [p["prg_id"] for p in pron_pub], "pronosticos_detalle": pron_pub, "riesgos": riesgos, "riesgo_1a5": int(riesgo),
        "catalizadores": _catalizadores(sint),
        "invalidacion": _lista(sint.get("invalidacion"), [s["nombre"] + ": umbral de invalidación" for s in plan["senales"]]),
        "refutacion": {k: st["refutacion"][k] for k in ("realizada_por", "veredicto_tesis", "veredicto_candidatos", "objeciones", "pre_mortem")},
        "candidatos_por_tipo": cpt, "apuestas_independientes": ap["apuestas_independientes"], "grupos_apuestas": ap["grupos"],
        "paquete_para_bloque_C": enc, "plan_de_seguimiento": plan, "mapa_cobertura": mapa,
        "historial_aciertos": historial(c), "tiempo_consumo": {
            "minutos": minutos, "uc": round(c.inv.consumo()["uc"] + c.motor.uc, 1), "estimado_p50_min": st["estimacion"]["minutos_p50"],
            "estimado_p80_min": st["estimacion"]["minutos_p80"], "autorizaciones": [a for a in st["autorizaciones"]], "por_fase_min": tc_pf,
            "puntos_control": list(st["puntos_control"]), "reloj": "simulado" if ent.reloj_simulado else "real",
            "minutos_autorizados": st.get("autorizado_min"), "n3_expreso": bool(st.get("n3_expreso")),
            "opcion_autorizada": st.get("opcion_autorizada"), "por_capa_min": dict(st.get("minutos_capa") or {})},
        "mapa_cadena_valor": mapa_cv,
        "capas": {"puertas_viabilidad": {g: (st.get("pv") or {}).get(g, {}).get("resultado", "NO_EVALUADA") for g in ("PV1", "PV2", "PV3")},
                  "continuacion_forzada": ({k: st["continuacion_forzada"].get(k) for k in ("puerta", "motivo", "fecha", "por")}
                                           if st.get("continuacion_forzada") else None),
                  "minutos_por_capa": dict(st.get("minutos_capa") or {}) or {"0": 0.0},
                  "detalle": {g: {k: x.get(k) for k in ("motivos", "debilidades", "A", "E", "tesis_viva", "eslabones") if k in x}
                              for g, x in (st.get("pv") or {}).items()}},
        "consultas_broker": consultas_paquete(st), "supuestos_aplicados": supuestos_paquete(st),
        "lista_profesional": lista_profesional(st, sint),
        "puertas_continuidad": {"GC0": st["gc0"], "GC1": st["gc1"],
                                "GC2": ("Integrada en PV2: tesis con mecanismo; A y E provisionales ≥ 50" if st.get("gc2", True) else "PV2 no superada (continuación forzada): universo indicativo")
                                + f" (A {(st.get('capa2') or {}).get('A')}, E {(st.get('capa2') or {}).get('E')})",
                                "GC3": "Finalistas: 2 × top-N por S que superan PC1–PC4"},
        "respuestas_preguntas": _respuestas(st, sint), "preguntas_sugeridas": _lista(sint.get("preguntas_sugeridas"), ["¿Qué cambiaría el veredicto?"]),
        "limitaciones": list(dict.fromkeys(st["limitaciones"] + (["Datos sintéticos y universos ilustrativos: resultados sin valor analítico"]
                                                                 if ent.prov.nombre == "sintetico" else []) + list(st["recortes"]))),
        "reservas_auditoria": [], "estados_degradados": list(dict.fromkeys(st["estados_degradados"])),
        "fechas_datos_criticos": [{"dato": f"Serie del indicador {st['indicador']['simbolo']}", "fecha": (st["indicador_metricas"] or {}).get("ultima_fecha_precio") or corte,
                                   "clase": "mercado", "justificacion": None if c._dato_fresco(st) else "dato fuera de frescura: PA2 bloquea"}],
        "auditoria": {"realizada": False},
    }
    if not paq["limitaciones"]:
        paq["limitaciones"] = ["Sin limitaciones adicionales a las declaradas por dimensión"]
    if st["peticion"].get("candidatos_aun_con_vigilar"):
        paq["x_candidatos_aun_con_vigilar"] = True
    return json.loads(json.dumps(paq, default=str))


def _ctx_eslabon(st: Dict, eid: str) -> Dict:
    e = next((x for x in st.get("desglose") or [] if x["eslabon_id"] == eid), None)
    if not e:
        return {"nombre": "Ámbito completo", "AE": None, "cuello_botella": False, "PCB": None}
    return {"nombre": e["nombre"], "AE": e["atractivo"]["AE"], "cuello_botella": bool(e["cuello_botella"]["material"]), "PCB": e["cuello_botella"]["PCB"]}


def mapa_cadena_valor(c, st: Dict, res: Dict, rec_id: str) -> Dict:
    """`mapa_cadena_valor` (B.16) compuesto por el Director en F7 sin afirmaciones nuevas: desglose (AG-B03 con AG-B05 y
    AG-B06), PCB y AE (HT-03), mejores opciones por eslabón (HT-03, 9.13) y radar de emergentes (AG-B24)."""
    import copy
    esl = copy.deepcopy(st.get("desglose") or [])
    if not esl:
        esl = [c._eslabon_unico(st)]
    tablas = ((res.get("mejores_por_eslabon") or {}).get("tablas") or {})
    for e in esl:
        tb = tablas.get(e["eslabon_id"])
        ops = []
        for o in (tb or {}).get("opciones") or []:
            t = o["tipo_activo"]
            cd = ((st["seleccion"].get(t) or {}).get("candidatos") or {}).get(o["cand_id"]) or {}
            f = cd.get("_fila") or {}
            ind = _pv3_no(st)
            ops.append({"rango": o["rango"], "cand_id": o["cand_id"], "nombre": f.get("nombre") or o["cand_id"],
                        "ticker": f.get("id") if f.get("isin") else None, "isin": _isin(f.get("isin")), "tipo_activo": t,
                        "rol_en_eslabon": cd.get("rol_en_eslabon") or f"Exposición al eslabón ({f.get('subcluster') or 'núcleo'})",
                        "pureza_eslabon": o.get("pureza_eslabon"), "S": o["S"], "ic90_S": o.get("ic90_S"), "veredicto": o["veredicto"],
                        "en_top_n_tipo": bool(o["en_top_n_tipo"]) and not ind,
                        "motivo": ("Indicativa (PV3 no superada): sin selección completa ni encargo C.x" if ind else
                                   "En el top-N de su tipo" if o["en_top_n_tipo"] else "Añadida por cobertura del eslabón (9.13), adicional al top-N")
                                  + (f"; {', '.join(o.get('motivo_secundario') or [])}" if o.get("motivo_secundario") and not ind else ""),
                        "riesgos_clave": [a["senal"] for a in cd.get("alertas") or []][:3] or ["Riesgos específicos por verificar en el Bloque C"]})
        e["opciones"] = ops
        q = ht03.eslabon_cualifica(e)
        e["sin_opciones_motivo"] = None if ops or not q["cualifica"] else "Sin opciones invertibles que superen los filtros (PC1–PC4 con S ≥ 50) en este eslabón (R21)"
        e["emergentes"] = [{k: v for k, v in g.items() if k not in ("eslabon_id",)} | {"instrumento_exposicion": {
            k: v for k, v in g["instrumento_exposicion"].items() if k in ("nombre", "isin", "cand_id", "fuera_de_filtros", "motivo")}}
            for g in sorted(st.get("radar") or [], key=lambda g: -g["PEM"]) if g["eslabon_id"] == e["eslabon_id"]]
    esl.sort(key=lambda e: (-e["atractivo"]["AE"], e["eslabon_id"]))
    atr = [e["nombre"] for e in esl if ht03.eslabon_cualifica(e)["cualifica"] and e["eslabon_id"] != "ESL-00"]
    omis = [{"eslabon": "Insumos y actividades por debajo del alcance del nivel", "motivo": f"profundidad del desglose del nivel {st['nivel']} (Anexo A)"}]
    if st.get("radar_motivo"):
        omis.append({"eslabon": "Radar de emergentes", "motivo": st["radar_motivo"]})
    sint = ("El valor se concentra en " + ", ".join(atr[:3]) + "." if atr else
            "Ningún eslabón es atractivo ni tiene un cuello material con opciones invertibles.") +         (" PV3 no superada: las opciones son indicativas." if _pv3_no(st) else "")
    return {"rec_id": rec_id, "data_cutoff": c.ent.as_of, "nivel_detalle": st["nivel"] if st["nivel"] in ("N1", "N2", "N3", "PERS") else "N2",
            "eslabon_critico": st.get("eslabon_critico"), "eslabones": esl, "omisiones": omis, "sintesis": sint}


def consultas_paquete(st: Dict) -> List[Dict]:
    return [{"cns_id": q["cns_id"], "tipo": q["tipo"], "modo": q["modo"], "origen_agente": q.get("origen_agente"), "pregunta": q["pregunta"],
             "supuesto": q["supuesto"], "resolucion": q["estado"] if q["estado"] != "PENDIENTE" else "SUPUESTO_APLICADO",
             "respuesta": q.get("respuesta"), "efecto": q.get("efecto") or "SIN_CAMBIO"} for q in st.get("consultas") or []]


def supuestos_paquete(st: Dict) -> List[Dict]:
    return [{"cns_id": q["cns_id"], "supuesto": f"{q['supuesto']} (supuesto aplicado por falta de respuesta)"}
            for q in st.get("consultas") or [] if q["estado"] in ("SUPUESTO_APLICADO", "PENDIENTE")]


def lista_profesional(st: Dict, sint: Dict) -> List[Dict]:
    """Lista de comprobación profesional (8.10): TRATADO, NO_APLICABLE (con motivo) o LAGUNA declarada."""
    dims = {d["dim"]: d for d in st.get("dimensiones") or []}
    excl = {e["dim"]: e["motivo"] for e in st["plan"]["exclusiones"]}
    dadas = {int(x["item"]): x for x in (sint.get("lista_profesional") or []) if isinstance(x, dict) and str(x.get("item", "")).isdigit()
             and x.get("estado") in ("TRATADO", "NO_APLICABLE", "LAGUNA") and x.get("referencia")}
    out = []
    for i, (nombre, ds, n1, _c2) in LISTA_PROFESIONAL.items():
        if st["nivel"] == "N1" and not n1:
            out.append({"item": i, "estado": "NO_APLICABLE", "referencia": "N1: solo los ítems marcados (N1) en 8.10"})
            continue
        if i in dadas:
            out.append({"item": i, "estado": dadas[i]["estado"], "referencia": str(dadas[i]["referencia"])})
            continue
        if i == 19:
            out.append({"item": 19, "estado": "LAGUNA", "referencia": "Sin transcripciones o paneles de expertos publicados incorporados en la fecha de corte"})
            continue
        if i == 22:
            out.append({"item": 22, "estado": "TRATADO", "referencia": "Declaraciones DAT-B y anexo de datos (hojas Cifras y Fuentes)"})
            continue
        if i == 13 and st.get("desglose"):
            out.append({"item": 13, "estado": "TRATADO", "referencia": "Mapa de oportunidades por eslabón (entregable 6): PCB, AE y radar de emergentes"})
            continue
        presentes = [d for d in ds if d in dims]
        if presentes and all(not dims[d]["lagunas"] for d in presentes):
            out.append({"item": i, "estado": "TRATADO", "referencia": f"Informe técnico, sección 5 ({', '.join(presentes)})"})
        elif presentes:
            out.append({"item": i, "estado": "LAGUNA", "referencia": f"Laguna declarada en {', '.join(d for d in presentes if dims[d]['lagunas'])}"})
        else:
            out.append({"item": i, "estado": "NO_APLICABLE", "referencia": "; ".join(f"{d} excluida: {excl[d]}" for d in ds if d in excl)
                        or "Dimensiones no tratadas en este nivel"})
    return out


def _catalizadores(sint: Dict) -> List[Dict]:
    out = [{"evento": c_["evento"], "fecha": str(c_.get("fecha") or "por determinar")} for c_ in (sint.get("catalizadores") or [])
           if isinstance(c_, dict) and c_.get("evento")]
    for c_ in out:
        if len(c_["fecha"]) < 4:
            c_["fecha"] = "por determinar"
    return out or [{"evento": "Próxima publicación de resultados del ámbito", "fecha": "próximo trimestre"}]


def _respuestas(st: Dict, sint: Dict) -> List[Dict]:
    dadas = {str(r.get("pregunta")).strip().lower(): r for r in (sint.get("respuestas_preguntas") or []) if isinstance(r, dict)}
    out = []
    pet = st["peticion"]
    origen_a = set((pet.get("paquete_para_bloque_B") or {}).get("preguntas_para_B") or [])
    for q in st["plan"]["preguntas"]:
        r = dadas.get(q.strip().lower()) or {}
        out.append({"pregunta": q, "origen": "BLOQUE_A" if q in origen_a else "BROKER",
                    "respuesta": r.get("respuesta") or "Respondida en las dimensiones, la tesis y la selección del informe técnico.",
                    "referencias": [x for x in (r.get("referencias") or []) if isinstance(x, str)]})
    return out


def mapa_cobertura(st: Dict, sint: Dict) -> Dict:
    m = sint.get("mapa_cobertura") if isinstance(sint.get("mapa_cobertura"), dict) else {}
    out = {}
    for k in ("directas", "indirectas", "perdedores_sistematicos", "investigado", "excluido_con_motivo", "vigilancia_informativa", "vigilancia_pre_salida"):
        items = []
        for x in m.get(k) or []:
            if isinstance(x, str) and x.strip():
                items.append(x)
            elif isinstance(x, dict) and x.get("objeto"):
                items.append({kk: vv for kk, vv in x.items() if kk in ("objeto", "tipo_activo", "invertibilidad", "mecanismo", "motivo", "caducidad", "detalle")
                              and (kk != "tipo_activo" or vv in TIPOS_ACTIVO)})
        out[k] = items
    out["investigado"] = out["investigado"] or [e["eslabon"] for e in st["mapa_preliminar"]] + [NOMBRE_TIPO[t] for t in st["tipos_aplicables"]]
    out["excluido_con_motivo"] = [x for x in out["excluido_con_motivo"] if not isinstance(x, dict) or x.get("motivo")] + \
        [{"objeto": f"Tipo {t}", "motivo": m_} for t, m_ in st["tipos_no_aplicables"].items()]
    for g in st.get("radar") or []:      # emergentes no invertibles hoy: vigilancia del mapa de cobertura (8.7, 8.7.3)
        if g["via_exposicion"] == "FUTURA_SALIDA_A_BOLSA":
            out["vigilancia_pre_salida"].append({"objeto": g["nombre"], "motivo": f"radar de emergentes (AG-B24), {g['eslabon_id']}",
                                                 "caducidad": "dos horizontes del análisis sin señal relevante"})
        elif g["via_exposicion"] == "NO_INVERTIBLE_HOY":
            out["vigilancia_informativa"].append({"objeto": g["nombre"], "motivo": f"radar de emergentes (AG-B24), {g['eslabon_id']}: no invertible hoy"})
    return out


def plan_de_seguimiento(c, st: Dict, rec_id: str, veredicto: str, top: List[Dict], sint: Dict) -> Dict:
    import numpy as np
    ind, ref = st["indicador"]["simbolo"], st["referencia"]["simbolo"]
    sigma = 0.08
    try:
        a = np.log(c.ent.prov.cierres(ind)).diff().dropna()
        b = np.log(c.ent.prov.cierres(ref)).diff().dropna() if ref != ind else a * 0
        rel = (a - b).dropna().iloc[-756:]
        r63 = rel.rolling(63).sum().dropna()
        sigma = float(np.expm1(r63).std()) or 0.08
    except Exception:  # noqa: BLE001
        pass
    s1 = round(100 * sigma, 1)
    alcista = veredicto in ("INVERTIR", "INVERTIR_ESCALONADO", "VIGILAR")
    pre = f"SIG-{st['pet_id'][6:]}"
    sen = [{"sig_id": f"{pre}-01", "nombre": f"Rentabilidad relativa a 3 meses de {ind} frente a {ref}", "serie": f"HT-01:REL:{ind}/{ref}",
            "frecuencia": (c.cfg.get("vigia") or {}).get("frecuencia", {}).get(st["horizonte"], "semanal"), "unidad": "%",
            "valor_entrega": None, "umbral_fluctuacion": {"min": -s1, "max": s1},
            "umbral_revision": -round(1.5 * s1, 1) if alcista else round(1.5 * s1, 1),
            "umbral_invalidacion": -round(2.5 * s1, 1) if alcista else round(2.5 * s1, 1),
            "direccion": "por_debajo" if alcista else "por_encima",
            "criterio_cambio_estructural": "Dos lecturas seguidas más allá del umbral de revisión con deterioro de la tesis en el informe de la dimensión D12",
            "afecta_a": ["AMBITO"], "transformacion": "rentabilidad relativa acumulada a 63 sesiones (%)"},
           {"sig_id": f"{pre}-02", "nombre": f"Caída de {ind} desde el nivel de la entrega", "serie": f"HT-01:NIVEL:{ind}",
            "frecuencia": (c.cfg.get("vigia") or {}).get("frecuencia", {}).get(st["horizonte"], "semanal"), "unidad": "%",
            "valor_entrega": 0.0, "umbral_fluctuacion": {"min": -8.0, "max": 8.0}, "umbral_revision": -12.0, "umbral_invalidacion": -20.0,
            "direccion": "por_debajo", "criterio_cambio_estructural": "Caída superior al 20 % sin recuperación en el siguiente ciclo de resultados",
            "afecta_a": ["AMBITO"] + [x["cand_id"] for x in top if x["veredicto"] == "PRIORITARIO_PARA_C"][:5],
            "transformacion": "variación (%) desde el cierre de la fecha de corte"}]
    for i, x in enumerate([x for x in top if x["veredicto"] == "PRIORITARIO_PARA_C"][:3], start=3):
        f = st["seleccion"][x["_tipo"]]["candidatos"][x["cand_id"]]["_fila"]
        if f.get("simbolo"):
            sen.append({"sig_id": f"{pre}-{i:02d}", "nombre": f"Rentabilidad relativa a 3 meses de {x['cand_id']} frente a {ref}",
                        "serie": f"HT-01:REL:{f['simbolo']}/{ref}", "frecuencia": "semanal", "unidad": "%", "valor_entrega": None,
                        "umbral_fluctuacion": {"min": -15.0, "max": 15.0}, "umbral_revision": -20.0, "umbral_invalidacion": -30.0,
                        "direccion": "por_debajo", "criterio_cambio_estructural": "Dos lecturas seguidas bajo el umbral de revisión",
                        "afecta_a": [x["cand_id"]], "transformacion": "rentabilidad relativa acumulada a 63 sesiones (%)"})
    hz_dias = {"H1": 14, "H2": 60, "H3": 365, "H4": 730, "H5": 1825}[st["horizonte"]]
    return {"rec_id": rec_id, "pet_id": st["pet_id"], "vigente_hasta": (dt.date.fromisoformat(c.ent.as_of) + dt.timedelta(days=hz_dias)).isoformat(),
            "horizonte": st["horizonte"], "frecuencia": (c.cfg.get("vigia") or {}).get("frecuencia", {}).get(st["horizonte"], "semanal"),
            "regimen_referencia": st["pet_id"].replace("PET-B-", "RGM-B-"), "senales": sen,
            "condiciones_invalidacion_ambito": _lista(sint.get("invalidacion"), [s["nombre"] + ": umbral de invalidación" for s in sen[:2]]),
            "condiciones_invalidacion_candidatos": [{"cand_id": x["cand_id"], "condiciones": ["Rentabilidad relativa a 3 meses por debajo del −30 %"]}
                                                    for x in top if x["veredicto"] == "PRIORITARIO_PARA_C"],
            "catalizadores": [{"evento": e["evento"], "fecha": e["fecha"], "que_vigilar": "efecto en la tesis"} for e in _catalizadores(sint)],
            "pronosticos_a_resolver": [{"prg_id": p["prg_id"], "fecha_resolucion": p["fecha_resolucion"]} for p in st["pronosticos"]],
            "acciones_al_disparo": {"REVISION": "alerta MEDIA", "INVALIDACION_PROBABLE": "alerta ALTA y sugerencia de petición N1",
                                    "INVALIDACION_CONFIRMADA": "alerta ALTA; REC-B a INVALIDADA"},
            "nota": "El Vigía avisa al Broker por el Coordinador; nunca abre un análisis (R32)."}


def historial(c) -> Dict:
    res = c.alm.estado("F4")
    resueltos = [p for p in res.values() if p.get("estado") == "RESUELTO"]
    amb = [p for p in resueltos if p.get("tipo") == "AMBITO"]
    rk = [p for p in resueltos if p.get("tipo") == "RANKING"]
    aciertos = sum(1 for p in amb if (p.get("resolucion") or {}).get("acierto"))
    certs = [e for e in c.alm.leer("F5") if e.get("tipo_entrada") == "CERTIFICADO" and e.get("tipo") == "ranking"]
    return {"ventana": f"hasta {c.ent.as_of}", "ambitos": {"resueltos": len(amb), "aciertos": aciertos},
            "rankings": {"resueltos": len(rk), "exceso_medio_top_n": round(sum((p.get("resolucion") or {}).get("exceso", 0) for p in rk) / len(rk), 4) if rk else None},
            "certificacion": "certificado vigente" if certs else "sin ventaja demostrada todavía",
            "nota": "Historial del almacén de estado de este ejecutor"}


# =============================================================================================================
# F8 · Validación G3 y auditoría previa a la salida
# =============================================================================================================
def esquema_paquete(cfg: Dict) -> Optional[Dict]:
    p = buscar_versionado(ruta(cfg, "plantillas"), "Esquema JSON - Paquete de análisis de mercado", ".json")
    return json.loads(p.read_text(encoding="utf-8")) if p else None


def extracto_f2(c, pet_id: str) -> Dict:
    ids, trazas, dat = [], {}, {}
    for e in c.alm.leer("F2"):
        if e.get("pet_id") != pet_id:
            continue
        ids.append(e["id"])
        if e.get("tipo_entrada") == "CLM":
            trazas[e["id"]] = e.get("evd") or []
        if e.get("tipo_entrada") == "DAT":
            dat[e["id"]] = {"apta_cifra_critica": e.get("apta_cifra_critica", True)}
    calc = {e["id"]: e.get("estado", "SERVIDO") for e in c.alm.leer("RC") if e.get("tipo_entrada") == "CALC"}
    return {"ids": ids + list(calc), "trazas": trazas, "dat": dat, "calc_estados": calc}


def validar_y_auditar(c, st: Dict) -> None:
    alm, cfg = c.alm, c.cfg
    paq = st["paquete"]
    # Consultas NO_BLOQUEANTES sin respuesta al inicio de F8: supuesto aplicado y declarado (7.12, punto 4)
    c._cerrar_consultas_no_bloqueantes(st)
    paq["consultas_broker"] = consultas_paquete(st)
    paq["supuestos_aplicados"] = supuestos_paquete(st)
    for x in paq["supuestos_aplicados"]:
        txt = f"Supuesto aplicado por falta de respuesta ({x['cns_id']})"
        if not any(txt in l for l in paq["limitaciones"]):
            paq["limitaciones"].append(f"{txt}: {x['supuesto']}")
    esq = esquema_paquete(cfg)
    f10 = {"methodology_version": c.ent.f10().get("methodology_version")}
    for vuelta in range(1, 4):
        g3 = ht09.validar(paq, esquema=esq, f2=extracto_f2(c, st["pet_id"]), parametros_f10=f10, preguntas=st["plan"]["preguntas"],
                          f1=alm.estado("F1", tipo="CONSULTA_BROKER"))
        alm.escribir("HA", "AG-B21", {"tipo_entrada": "G3V", "id": alm.nuevo_id("G3V-B"), "pet_id": st["pet_id"], "run_id": st["run_id"],
                                      "pasada": "PAQUETE_SINTESIS", "dictamen": g3["dictamen"], "resumen": g3["resumen"], "motivo": g3["motivo"],
                                      "fallos": [{"id": x["id"], "clase": x.get("clase_fallo"), "detalles": x.get("detalles")}
                                                 for x in g3["comprobaciones"] if x["resultado"] == "FALLA"]})
        if g3["dictamen"] != "BLOQUEADO":
            break
        c.inv.llamar("AG-B21", "CT-B-18", "dictamen_g3", {"pet_id": st["pet_id"], "fallos": [x for x in g3["comprobaciones"] if x["resultado"] == "FALLA"]},
                     "Comenta el dictamen G3 y ordena la subsanación.", {"dictamen_comentado": "string"}, c._ctx("AG-B21"), st["run_id"])
        c.inv.llamar("AG-B02", "CT-B-18", "subsanacion", {"pet_id": st["pet_id"], "hallazgos": [{"id": x["id"], "detalle": x["detalles"][:3]}
                                                                                                for x in g3["comprobaciones"] if x["resultado"] == "FALLA"]},
                     "Subsana los fallos G3 con los agentes necesarios.", {"correcciones": "array"}, c._ctx("AG-B02"), st["run_id"])
    st["g3"] = {"dictamen": g3["dictamen"], "resumen": g3["resumen"], "motivo": g3["motivo"]}
    if g3["dictamen"] == "BLOQUEADO":
        st["bloqueado"] = "G3"
        return
    # Auditoría experta previa (N2/N3 100 %; N1 por muestreo)
    mu = float(((cfg.get("auditoria") or {}).get("muestreo") or {}).get(st["nivel"], 1.0))
    rng = random.Random(f"{st['pet_id']}|auditoria")
    hacer = rng.random() < mu and not (c.ent.modo == "backtest" and not (cfg.get("auditoria") or {}).get("en_backtest", False))
    reservas, vueltas, abiertos = [], 0, []
    if hacer:
        for vuelta in range(1, int((cfg.get("auditoria") or {}).get("max_vueltas", 3)) + 1):
            vueltas = vuelta
            r = c.inv.llamar("AG-B22", "CT-B-19", "auditoria",
                             {"pet_id": st["pet_id"], "vuelta": vuelta, "nivel": st["nivel"], "veredicto": paq["veredicto"],
                              "puntuaciones": paq["puntuaciones"], "tesis": paq["tesis"]["enunciado"], "g3": st["g3"],
                              "candidatos": {t: [x["cand_id"] for x in d.get("top_n", [])] for t, d in paq["candidatos_por_tipo"].items() if d.get("aplicable")},
                              "focos": ["trazabilidad", "etiquetado", "proyecciones", "despliegue", "hipótesis", "steelman", "coherencia",
                                        "solidez de la selección", "frontera de rol", "frescura"]},
                             "Audita el paquete antes de la salida (11.2) y gradúa los hallazgos.", {"hallazgos": "array", "recomendacion": "string"},
                             c._ctx("AG-B22"), st["run_id"])
            hall = [h for h in (r.get("hallazgos") or []) if isinstance(h, dict)]
            for h in hall:
                h["severidad"] = controlado(h.get("severidad"), "severidad", "Operativa")
                alm.escribir("HA", "AG-B21", {"tipo_entrada": "AUD", "id": alm.nuevo_id("AUD-B"), "pet_id": st["pet_id"], "vuelta": vuelta, **{k: h.get(k) for k in ("severidad", "foco", "descripcion", "correccion_propuesta")}})
            abiertos = [h for h in hall if h["severidad"] in ("Crítica", "Material")]
            if not abiertos:
                break
            c.inv.llamar("AG-B02", "CT-B-19", "subsanacion", {"pet_id": st["pet_id"], "hallazgos": abiertos},
                         "Subsana los hallazgos Críticos y Materiales.", {"correcciones": "array"}, c._ctx("AG-B02"), st["run_id"])
        if abiertos:
            if any(h["severidad"] == "Crítica" for h in abiertos):
                st["bloqueado"] = "AUDITORIA"
                return
            reservas = [f"Reserva de auditoría: {h.get('descripcion')}" for h in abiertos]
    autc = alm.nuevo_id("AUTC-B")
    alm.escribir("HA", "AG-B21", {"tipo_entrada": "AUTORIZACION_CONTENIDO", "id": autc, "pet_id": st["pet_id"], "auditoria": hacer,
                                  "vueltas": vueltas, "reservas": reservas})
    paq["reservas_auditoria"] = reservas
    paq["auditoria"] = {"realizada": hacer, "muestreo": st["nivel"] == "N1", "vueltas": vueltas, "hallazgos_abiertos": [h.get("descripcion") for h in abiertos],
                        "dictamen_g3": g3["dictamen"], "autorizacion_contenido": autc, "autorizacion_salida": None}
