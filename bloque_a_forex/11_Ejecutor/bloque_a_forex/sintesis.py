"""Paquete de síntesis (CT-15) y validación G3 con HT-09.

V1.1 (03/11/2026): cada opción declara `naturaleza_inversion` y `horizonte_principal` coherentes (regla de adecuación de 8.3,
módulo `horizontes`); H5 «limitado» con banda cualitativa e hitos HIT-FX- congelados en F4; `supuestos_declarados` y
`consultas_broker_sin_respuesta` (6.2.9) a partir de las consultas CT-23 del RUN.

El paquete de síntesis es un superconjunto del esquema `paquete_oportunidades` del Bloque A Forex V1.0 (Documento 0
Forex, Anexo B): cada opción es un ámbito cambiario con `segmento`, `par` (BASE/COTIZADA), `composicion` (LARGO/CORTO
y peso), `direccion` (solo en PAR, CRUCE y REGIMEN), `vista_volatilidad` (solo en VOLATILIDAD), `carry`,
`convertibilidad` e `indicador_seguimiento`; `paquete_para_bloque_B` es el encargo de 2.5 (consideraciones de
implementación, niveles de referencia con hora de fijación, carry esperado, métricas clave y preguntas). Añade por
opción los campos que HT-09 aprovecha (`puertas`, `cluster`, `vigente`, `horizontes.Hn.advertencia/metodo`,
`objeciones[].resuelta`). El entregable JSON se obtiene eliminando esos campos (ver `redaccion.entregable_json`).
"""
from __future__ import annotations

import copy
import re
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd

from . import fx
from . import horizontes as hzn
from .configuracion import NOMBRE_SEGMENTO, SEGMENTOS, TIPOS_CESTA
from .evaluador import banda_de, banda_publicable
from .herramientas import ht09
from .herramientas.ht05_planificador import fecha_resolucion
from .herramientas.ht06_indice import normalizar

RE_FECHA_CAT = re.compile(r"^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$|^[0-9]{4}-T[1-4]$|^[0-9]{4}-S[12]$")
ETIQUETA_SIN_CERT = "sin ventaja demostrada frente al paseo aleatorio"
ADVERTENCIA_H1 = "Previsión a días: la de menor fiabilidad esperada; sin ventaja demostrada frente al paseo aleatorio."
AVISO_LEGAL = ("Este informe describe oportunidades generales del mercado de divisas y no constituye asesoramiento "
               "personalizado; el Broker Personal valora si encaja con el usuario. El instrumento, el coste, la cobertura y "
               "la ejecución los analiza el Bloque B.")
SESIONES = {"H1": 5, "H2": 20, "H3": 126, "H4": 252}
TIPO_INDICADOR = {"PAR": "TIPO_DE_CAMBIO", "CRUCE": "TIPO_DE_CAMBIO", "REGIMEN": "TIPO_DE_CAMBIO", "CESTA": "INDICE_CESTA",
                  "BLOQUE": "INDICE_CESTA", "ESTRATEGIA": "INDICE_ESTRATEGIA", "VOLATILIDAD": "VOLATILIDAD_IMPLICITA"}
PROFUNDIDADES = ("muy alta", "alta", "media", "baja")
CAMPOS_CONVERTIBILIDAD = ("convertible", "ndf", "controles_capitales", "impiden_exposicion", "exposicion_alternativa",
                          "profundidad", "nota")
HORA_FIJACION_DEFECTO = "17:00 America/New_York"


def _menos_de_tres_texto(c: str, sel: Dict, n_opc: int) -> Optional[str]:
    m = sel["seleccion"].get("menos_de_tres_motivo")
    if n_opc >= 3:
        return None
    partes = [f"Se proponen {n_opc} opción(es) en {NOMBRE_SEGMENTO[c]}."]
    if m:
        partes.append(m["texto"])
        for x in m["no_llegaron"][:4]:
            partes.append(f"{x['opp_id']}: {'; '.join(x['motivos'][:2])} → {'; '.join(x['que_tendria_que_ocurrir'][:2])}.")
    else:
        partes.append("Ninguna candidata superó las puertas de continuidad y de selección en este ciclo (R14).")
    return " ".join(partes)


def _texto(v, defecto: str, minimo: int = 10) -> str:
    t = str(v or "").strip()
    return t if len(t) >= minimo else defecto


def _lista(v, defecto: List[str], minimo: int = 3) -> List[str]:
    if isinstance(v, str):
        v = [v]
    out = [str(x).strip() for x in (v or []) if isinstance(x, str) and len(x.strip()) >= minimo]
    return out or list(defecto)


def _ambito(f: Dict, c: str) -> Dict:
    a = f.get("ambito") if isinstance(f.get("ambito"), dict) else {}
    inc = str(a.get("incluye") or f.get("nombre") or "").strip()
    exc = str(a.get("excluye") or "").strip()
    out = {"incluye": inc if len(inc) >= 5 else f"Ámbito cambiario «{f.get('nombre')}» del segmento {c}",
           "excluye": exc if len(exc) >= 2 else "Instrumentos concretos: su elección corresponde al Bloque B"}
    reg = str(a.get("region") or "").strip()
    if len(reg) >= 2:
        out["region"] = reg
    return out


def _indicador(f: Dict, fuente: str) -> Dict:
    i = f.get("indicador_seguimiento") if isinstance(f.get("indicador_seguimiento"), dict) else {}
    out = {"nombre": _texto(i.get("nombre") or f.get("nombre"), f["proxy"], 3)[:200], "simbolo": f["proxy"], "fuente": fuente}
    tipo = TIPO_INDICADOR.get(f.get("tipo_opcion"))
    if tipo:
        out["tipo"] = tipo
    return out


def _convertibilidad(f: Dict) -> Dict:
    c = dict(f.get("convertibilidad") or {})
    out = {k: c[k] for k in CAMPOS_CONVERTIBILIDAD if k in c}
    out["convertible"] = bool(out.get("convertible", True))
    out["ndf"] = bool(out.get("ndf", False))
    out["controles_capitales"] = bool(out.get("controles_capitales", False))
    if out["convertible"] is False and not out["ndf"]:
        out["exposicion_alternativa"] = True        # PS3 superada: hay exposición alternativa
    if out.get("impiden_exposicion") is not False:
        out.pop("impiden_exposicion", None)
    if out.get("profundidad") not in PROFUNDIDADES:
        out["profundidad"] = "alta"
    out["nota"] = _texto(out.get("nota"), "Convertibilidad e invertibilidad según el universo y el Analista (PS3).", 5)
    return out


def _carry(f: Dict, sen: Dict, calcs: List[str]) -> Dict:
    """Carry de la exposición orientado a la tesis (FX-CARRY-001): el del indicador tal como cotiza si la tesis espera
    que suba; con el signo cambiado si espera que baje."""
    if f.get("tipo_opcion") == "VOLATILIDAD":
        return {"anual_pct": None, "signo": "no aplicable", "ajustado_vol": None}
    k = 1 if f.get("_sube", True) else -1
    v = sen.get("carry_anual_pct")
    if v is None:
        return {"anual_pct": 0.0, "signo": "neutro", "ajustado_vol": 0.0, "calc_id": calcs[0]}
    anual = round(k * float(v), 2)
    aj = sen.get("carry_ajustado_vol")
    aj = round(k * float(aj), 3) if aj is not None else 0.0
    if anual == 0 or aj == 0:
        aj = 0.0 if anual == 0 else aj
    out = {"anual_pct": anual, "signo": fx.signo_carry(anual, f.get("tipo_opcion")), "ajustado_vol": aj,
           "calc_id": sen.get("carry_calc_id") or calcs[0]}
    if f.get("tipo_opcion") in ("PAR", "CRUCE", "REGIMEN") and sen.get("tipo_largo_pct") is not None:
        out["diferencial_tipos_pct"] = round(float(sen["tipo_largo_pct"]) - float(sen["tipo_corto_pct"]), 2)
    return out


def _referencia_texto(c: str, tipo: str) -> str:
    if c == "ESTR" and tipo in TIPOS_CESTA:
        return "rentabilidad nula"
    if tipo == "VOLATILIDAD":
        return "paseo aleatorio"
    return "paseo aleatorio y forward"


def _reversibilidad(conv: Dict, liq: str) -> str:
    if conv.get("convertible") is False or conv.get("ndf") or conv.get("controles_capitales"):
        return "baja"
    return liq if liq in ("alta", "media", "baja") else "alta"


def _siguiente_paso(rel: str, E: int, RK: int) -> str:
    if rel == "ALTA" and E < 70:
        return "PROFUNDIZAR_EN_A"
    if RK >= 65:
        return "ENVIAR_A_BLOQUE_B"
    return "VIGILAR"


def _consideraciones(f: Dict, op: Dict) -> List[str]:
    propias = [x for x in _lista(f.get("consideraciones_implementacion"), []) if not ht09.RE_INSTRUMENTO.search(x)
               and not ht09.RE_EJECUCION.search(x)]
    conv = op["convertibilidad"]
    base = []
    if conv["convertible"]:
        base.append("Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York")
    else:
        base.append("Divisa no plenamente convertible: existe mercado no entregable (liquidación en otra divisa)")
    if conv["controles_capitales"]:
        base.append("Controles de capitales vigentes: posibles límites a la repatriación")
    ca = op["carry"]
    if ca.get("anual_pct") is not None:
        base.append(f"Carry de la exposición {ca['anual_pct']:+.2f} % anual ({ca['signo']})")
    else:
        base.append("Vista sobre la volatilidad del ámbito: sin carry asociado")
    return (propias + base)[:6]


def construir(bloque, run_id, tipo, as_of, segmentos, nivel, gc0, analisis, seleccion, clusteres, integ, historial, presupuesto,
              transversales: Optional[Dict] = None) -> Tuple[Dict, Dict]:
    cfg = bloque.cfg
    as_of = pd.Timestamp(as_of)
    transversales = transversales or {}
    certs = {(c["celda"]["segmento"], c["celda"]["horizonte"]): c["id"] for c in bloque.evaluador.certificados_vigentes(as_of)}
    prefer = cfg.get("horizonte_principal_preferente") or ["H3", "H2", "H4", "H1"]
    hora_fij = str((cfg.get("ht01") or {}).get("hora_fijacion") or HORA_FIJACION_DEFECTO)
    f10 = bloque.f10(as_of)
    divisa_base = str(f10.get("P-04") or cfg.get("divisa_base_usuario") or "EUR")
    prg_borradores: List[Dict] = []
    desgloses, paquete_segmentos, por_opp = {}, {}, {}
    segmentos_out: Dict[str, Dict] = {}
    bloque_b: List[Dict] = []
    fechas_dato = []
    f1 = bloque.almacen.estado("F1", as_of)
    tnd_por_nombre = {normalizar(t.get("nombre_canonico", "")): k for k, t in f1.items()}
    fuente = f"HT-01:{bloque.proveedor.nombre}"

    def borradores(f: Dict, c: str, en_informe: bool) -> Dict[str, str]:
        ids = {}
        sen = f["senales"]
        for h, d in f["_hz"].items():
            if h == "H5" and d.get("h5") and not d.get("prg_existente"):
                pid = bloque.almacen.nuevo_id("PRG")
                ids[h] = pid
                positivo = d["vista"] == "alcista"
                _, nivel_p = bloque.proveedor.valor_en(f["proxy"], as_of)
                hitos = hzn.hitos_h5(as_of, f["proxy"], float(nivel_p), positivo, d["ambito_h5"])
                for x in hitos:
                    x["hit_id"] = bloque.almacen.nuevo_id("HIT")
                d["_hitos"] = hitos
                fr = hzn.fecha_resolucion_h5(as_of)
                prg_borradores.append({
                    "tipo_entrada": "ALTA", "prg_id": pid, "version_de": None, "opp_id": f["opp_id"],
                    "tnd_ids": [f["tnd_id"]] if f.get("tnd_id") else [], "run_id": run_id, "segmento": c, "horizonte": "H5",
                    "estrategia": f"{c}-{f.get('tipo_opcion') or 'PAR'}", "tipo_opcion": f.get("tipo_opcion"), "par": f.get("par"),
                    "composicion": copy.deepcopy(f.get("composicion") or []), "direccion": f.get("direccion"),
                    "tipo_pronostico": "ESTRUCTURAL_H5", "ambito_h5": d["ambito_h5"], "afirmacion": d["afirmacion"],
                    "sentido": "POSITIVO" if positivo else "NEGATIVO", "vista": d["vista"],
                    "variable": {"serie_ht01": f["proxy"], "descripcion": f"cierre de {f['proxy']} ({hora_fij})",
                                 "tipo_rentabilidad": "PRECIO_CONTADO", "divisa": f.get("_divisa_medicion") or "USD"},
                    "tipo_rentabilidad": "PRECIO_CONTADO", "divisa_medicion": f.get("_divisa_medicion") or "USD",
                    "nivel_referencia": {"valor": nivel_p, "fecha": str(as_of.date()), "fuente": fuente, "hora_fijacion": hora_fij},
                    "fecha_emision": str(as_of.date()), "fecha_congelacion": bloque.reloj.ahora(), "fecha_resolucion": str(fr.date()),
                    "criterio_resolucion": "H5: se evalúa por sus hitos HIT-FX- (cada uno en su fecha, frente al paseo aleatorio); "
                                           "estado EN_CURSO_CONFORME / DESVIADO / INVALIDADO publicado por el Evaluador en F6",
                    "fuente_resolucion": fuente, "banda_verbal": "más probable que no", "prob_interna": None, "prob_publicada": None,
                    "certificado_ref": None, "metodo": d.get("metodo"), "hitos": hitos,
                    "referencia_ingenua": {"definicion": "paseo aleatorio (sin cambio del indicador) en cada hito", "valor_o_prob": None},
                    "escenario_asociado": "BASE", "en_informe": en_informe, "estado": "ABIERTO",
                    "puntuaciones_opcion": {k: f["_ht03"]["puntuaciones"].get(k) for k in ("T", "E", "A", "RK")}})
                continue
            if d.get("prg_existente"):
                ids[h] = d["prg_existente"]
                prg_borradores.append({"prg_id": d["prg_existente"], "prg_existente": d["prg_existente"], "opp_id": f["opp_id"],
                                       "horizonte": h, "vista": d["vista"]})
                continue
            pid = bloque.almacen.nuevo_id("PRG")
            ids[h] = pid
            positivo = d["vista"] == "alcista"
            ses = SESIONES[h]
            tipo_op = f.get("tipo_opcion")
            carry_ind = None if tipo_op == "VOLATILIDAD" else sen.get("carry_anual_pct")
            ri = bloque.evaluador.referencia_ingenua(f["proxy"], c, ses, positivo, as_of, carry_ind, run_id)
            fr = fecha_resolucion(as_of, h, cfg["horizontes"])
            _, nivel_p = bloque.proveedor.valor_en(f["proxy"], as_of)
            tr = f.get("_tipo_rentabilidad") or "PRECIO_CONTADO"
            dm = f.get("_divisa_medicion") or "USD"
            sb = fx.sube_baja_llano(f.get("composicion") or []) or ""
            texto_ev = (f"{'subida' if positivo else 'bajada'} de {f['proxy']} ({tr.lower().replace('_', ' ')}, medida en {dm}) "
                        f"entre {as_of.date()} y {fr.date()}" + (f": {sb}" if sb else ""))
            prg_borradores.append({
                "tipo_entrada": "ALTA", "prg_id": pid, "version_de": d.get("version_de"), "opp_id": f["opp_id"],
                "tnd_ids": [f["tnd_id"]] if f.get("tnd_id") else [], "run_id": run_id, "segmento": c, "horizonte": h,
                "estrategia": f"{c}-{tipo_op or 'PAR'}", "tipo_opcion": tipo_op, "par": f.get("par"),
                "composicion": copy.deepcopy(f.get("composicion") or []), "direccion": f.get("direccion"),
                "vista_volatilidad": f.get("vista_volatilidad"),
                "tipo_pronostico": "DIRECCIONAL", "afirmacion": d["afirmacion"], "evento": texto_ev, "sentido": "POSITIVO" if positivo else "NEGATIVO",
                "vista": d["vista"], "variable": {"serie_ht01": f["proxy"], "descripcion": f"cierre de {f['proxy']} ({hora_fij})",
                                                  "tipo_rentabilidad": tr, "divisa": dm, "carry_anual_pct_indicador": carry_ind},
                "tipo_rentabilidad": tr, "divisa_medicion": dm,
                "referencia_indice": f.get("_referencia"),
                "nivel_referencia": {"valor": nivel_p, "fecha": str(as_of.date()), "fuente": fuente, "hora_fijacion": hora_fij},
                "umbral": 0.0, "fecha_emision": str(as_of.date()), "fecha_congelacion": bloque.reloj.ahora(),
                "fecha_resolucion": str(fr.date()),
                "criterio_resolucion": f"Cierre HT-01 ({hora_fij}) de la última sesión ≤ {fr.date()} frente al de la última sesión ≤ "
                                       f"{as_of.date()}; suceso: {texto_ev}",
                "fuente_resolucion": fuente, "regla_fallback": "última sesión disponible ≤ fecha de resolución; NO_RESOLUBLE tras 10 días hábiles sin dato",
                "banda_verbal": banda_de(d["prob_interna"]), "prob_interna": d["prob_interna"],
                "prob_publicada": d["prob_interna"] if (c, h) in certs else None, "certificado_ref": certs.get((c, h)),
                "metodo": d.get("metodo"), "referencia_ingenua": ri, "referencias_8_4": _referencia_texto(c, tipo_op),
                "escenario_asociado": d.get("escenario", "BASE"), "en_informe": en_informe, "estado": "ABIERTO",
                "puntuaciones_opcion": {k: f["_ht03"]["puntuaciones"].get(k) for k in ("T", "E", "A", "RK")}})
        return ids

    for c in segmentos:
        an, sel = analisis[c], seleccion[c]
        por_id = {f["opp_id"]: f for f in sel["candidatos"]}
        opciones = []
        for t in sel["seleccion"]["top3"]:
            f = por_id[t["opp_id"]]
            if f.get("tendencia") and not f.get("tnd_id"):
                k = normalizar(f["tendencia"].get("nombre_canonico", ""))
                f["tnd_id"] = tnd_por_nombre.get(k) or bloque.almacen.nuevo_id("TND")
                f["_tnd_nuevo"] = k not in tnd_por_nombre
                tnd_por_nombre[k] = f["tnd_id"]
            ids = borradores(f, c, True)
            pu = f["_ht03"]["puntuaciones"]
            tipo_op = f.get("tipo_opcion") or "PAR"
            hz = {}
            for h, d in sorted(f["_hz"].items()):
                if h == "H5":
                    b_ = next((p for p in prg_borradores if p.get("prg_id") == ids[h]), {})
                    prev = {} if "fecha_resolucion" in b_ else bloque.almacen.estado("F4", as_of).get(ids[h], {})
                    src = b_ if "fecha_resolucion" in b_ else prev
                    hz[h] = {"vista": d["vista"], "banda": "más probable que no", "prob": None, "certificado_r13": False,
                             "referencia": "paseo aleatorio", "tipo_rentabilidad": "PRECIO_CONTADO",
                             "divisa_medicion": src.get("divisa_medicion") or f.get("_divisa_medicion") or "USD", "prg_id": ids[h],
                             "metodo": d.get("metodo"), "ambito_h5": d.get("ambito_h5") or src.get("ambito_h5"),
                             "etiqueta": "probabilidad siempre cualitativa en H5 (sin certificado posible); se evalúa por hitos",
                             "hitos": [{k: x[k] for k in ("hit_id", "fecha", "indicador", "criterio", "referencia_ingenua", "estado") if k in x}
                                       for x in (src.get("hitos") or d.get("_hitos") or [])]}
                    if src.get("fecha_resolucion"):
                        hz[h]["fecha_resolucion"] = src["fecha_resolucion"]
                        hz[h]["criterio_resolucion"] = src.get("criterio_resolucion")
                    continue
                cert = (c, h) in certs
                b_ = next((p for p in prg_borradores if p.get("prg_id") == ids[h]), {})
                prev = {} if "fecha_resolucion" in b_ else bloque.almacen.estado("F4", as_of).get(ids[h], {})
                hz[h] = {"vista": d["vista"], "banda": banda_publicable(d["prob_interna"]), "prob": d["prob_interna"] if cert else None,
                         "certificado_r13": cert, "referencia": _referencia_texto(c, tipo_op),
                         "tipo_rentabilidad": b_.get("tipo_rentabilidad") or prev.get("tipo_rentabilidad") or f.get("_tipo_rentabilidad") or "PRECIO_CONTADO",
                         "divisa_medicion": b_.get("divisa_medicion") or prev.get("divisa_medicion") or f.get("_divisa_medicion") or "USD",
                         "prg_id": ids[h], "metodo": d.get("metodo")}
                if not cert:
                    hz[h]["etiqueta"] = ETIQUETA_SIN_CERT
                src = b_ if "fecha_resolucion" in b_ else prev
                if src.get("fecha_resolucion"):
                    hz[h]["fecha_resolucion"] = src["fecha_resolucion"]
                    hz[h]["criterio_resolucion"] = src.get("criterio_resolucion")
                if h == "H1":
                    hz[h]["advertencia"] = ADVERTENCIA_H1
            # Regla de adecuación del horizonte al tipo de inversión (8.3 V1.1)
            pref_h = next((h for h in prefer if h in hz), sorted(hz)[0])
            nat = f.get("naturaleza_inversion") if f.get("naturaleza_inversion") in hzn.NATURALEZAS else None
            if "H5" in hz:
                nat = "ESTRUCTURAL"
            nat = nat or hzn.naturaleza_por_defecto(tipo_op, hz, pref_h)
            hp, just_h = hzn.elegir_principal(nat, hz, list(prefer) + ["H5"])
            if f.get("justificacion_horizonte") and just_h:
                just_h = str(f["justificacion_horizonte"])
            f["_naturaleza"], f["_hp"], f["_just_h"] = nat, hp, just_h
            sen = f["senales"]
            if sen.get("fecha_dato"):
                fechas_dato.append(sen["fecha_dato"])
            fd_precio, precio = bloque.proveedor.valor_en(f["proxy"], as_of)
            precio = float(precio)
            conv = _convertibilidad(f)
            liq = f.get("liquidez") if f.get("liquidez") in ("alta", "media", "baja") else "alta"
            objs = []
            for o in f.get("_objeciones", []):
                resp = o.get("respuesta")
                fz = "debil" if o["fuerza"] in ("débil", "debil") else o["fuerza"]
                ok = bool(resp and len(resp) >= 10) and (fz != "fuerte" or o["resuelta"])
                objs.append({"objecion_id": o["objecion_id"], "fuerza": fz, "resumen": o["resumen"], "respuesta": resp if ok else (resp or None),
                             "estado": "RESPONDIDA" if ok else "SIN_RESOLVER", "resuelta": bool(o["resuelta"]) if fz == "fuerte" else ok})
            calcs = [x for x in (sen.get("calc_ids") or []) if str(x).startswith("CALC-FX-")]
            if clusteres.get("calc_id"):
                calcs.append(clusteres["calc_id"])
            if not calcs:
                calcs = [x for x in (an.get("calc_ids") or []) if str(x).startswith("CALC-FX-")]
            calcs = list(dict.fromkeys(calcs))
            carry = _carry(f, sen, calcs)
            comp = copy.deepcopy(f.get("composicion") or [])
            if tipo_op in ("PAR", "CRUCE", "REGIMEN"):
                nombre_ll = fx.nombre_llano(comp, tipo_op, f.get("nombre") or f["proxy"])
            else:
                nombre_ll = _texto(f.get("nombre_llano"), fx.nombre_llano(comp, tipo_op, f.get("nombre") or f["proxy"]), 3)[:70]
            op = {"opp_id": f["opp_id"], "rango": t["rango"], "tipo_opcion": tipo_op, "segmento": c,
                  "nombre": _texto(f.get("nombre"), f["proxy"], 3), "nombre_llano": nombre_ll,
                  "sube_baja_llano": fx.sube_baja_llano(comp) or None,
                  "par": f.get("par"), "composicion": comp, "direccion": f.get("direccion") if tipo_op in ("PAR", "CRUCE", "REGIMEN") else None,
                  "divisa_financiacion": f.get("divisa_financiacion"),
                  "tesis": _texto(f.get("tesis"), f"Tesis cambiaria sobre {f['proxy']} (sin texto del Analista)"),
                  "mecanismo": _texto(f.get("mecanismo"), "Mecanismo de transmisión no detallado por el Analista"),
                  "tnd_ids": [f["tnd_id"]] if f.get("tnd_id") else [], "cluster_id": f["_cluster"] if re.match(r"^CL-[0-9]{1,3}$", f["_cluster"]) else "CL-99",
                  "puntuaciones": {"T": pu.get("T"), "E": pu["E"], "M": pu.get("M"), "A": pu["A"], "P": pu.get("P"), "RK": pu["RK"],
                                   "desglose_ref": f"HT03-{run_id[4:]}-{f['opp_id'].split('-')[-1]}"},
                  "naturaleza_inversion": nat, "horizontes": hz, "horizonte_principal": hp, "justificacion_horizonte": just_h,
                  "valoracion": _texto(f.get("valoracion"), f"Posición del indicador en su rango de 3 años: percentil "
                                       f"{(sen.get('pct_precio_3a') or 0.5):.0%} (ST-DESC-001)"),
                  "carry": carry,
                  "catalizadores": [{"evento": str(x.get("evento") or "Catalizador")[:200], "fecha": str(x.get("fecha"))}
                                    for x in (f.get("catalizadores") or []) if isinstance(x, dict) and RE_FECHA_CAT.match(str(x.get("fecha", "")))],
                  "riesgos": _lista(f.get("riesgos"), ["Riesgo de mercado del par o de la cesta"]),
                  "riesgo_1a5": int(sen.get("riesgo_1a5") or 3),
                  "invalidacion": _lista(f.get("invalidacion"), ["Cambio del régimen de tipos que sostiene la tesis"]),
                  "ambito": _ambito(f, c), "indicador_seguimiento": _indicador(f, fuente),
                  "convertibilidad": conv, "liquidez": liq, "reversibilidad": _reversibilidad(conv, liq),
                  "que_cambiaria_la_conclusion": (list(_lista(f.get("invalidacion"), []))[:2]
                                                  + [o["que_la_resolveria"] for o in f.get("_objeciones", []) if o.get("que_la_resolveria")][:2])
                  or ["Que se cumpla alguna condición de invalidación"],
                  "objeciones": objs, "lo_que_no_sabemos": _lista(f.get("lo_que_no_sabemos"), ["Persistencia del régimen actual"]),
                  "confianza": "probable" if pu["E"] >= 70 else "especulativo",
                  "evidencias": [x for x in (f.get("_evidencias") or []) if re.match(r"^(CLM|EVD)-FX-", str(x))],
                  "calculos": calcs,
                  "minigrafico": {"tipo": "PAR_UN_ANO", "serie_ref": f"HT01:{f['proxy']}", "equilibrio": None, "calc_id": calcs[0]},
                  "x_referencia": f.get("_referencia"), "x_indicador_sube": bool(f.get("_sube", True)),
                  # campos que usa HT-09 (se eliminan del entregable JSON)
                  "puertas": f["_puertas"], "cluster": f["_cluster"], "vigente": bool(f.get("_vigente"))}
            if not op["sube_baja_llano"]:
                op.pop("sube_baja_llano")
            if "H5" in hz:
                op["ambito_h5"] = hz["H5"]["ambito_h5"]
            if tipo_op == "VOLATILIDAD":
                op["vista_volatilidad"] = copy.deepcopy(f.get("vista_volatilidad")) or {"sentido": "ALZA", "plazo": "1M"}
            if f.get("regimen_cambiario_divisa") in ht09.REGIMENES:
                op["regimen_cambiario_divisa"] = f["regimen_cambiario_divisa"]
            if carry.get("calc_id") and carry["calc_id"] not in op["calculos"]:
                op["calculos"].append(carry["calc_id"])
            # Escala de riesgo (RISK-DD-001 v2.0) con el suelo de régimen de la nota 2 del Anexo A
            if ht09.riesgo_minimo(op) and op["riesgo_1a5"] < 4:
                op["riesgo_1a5"] = 4
            esperado = ht09.segmento_esperado(op)
            if esperado and esperado != c:
                op["motivo_asignacion_segmento"] = (f"Asignada a {c} por el universo del ejecutor (columna «segmento»); las reglas "
                                                    f"1–3 de 2.6 darían {esperado}")
            p = bloque.params_ht03
            motivos = ht09.relevancia_esperada_alta(op, c, op["vigente"], p)
            op["relevancia_decisional"] = "ALTA" if motivos else ("BAJA" if f.get("_arrastre") else "MEDIA")
            op["siguiente_paso_sugerido"] = _siguiente_paso(op["relevancia_decisional"], pu["E"], pu["RK"])
            if pu.get("T") == "NA":
                op["puntuaciones"]["T"] = "NA"
            if op["puntuaciones"].get("P") is None:
                op["puntuaciones"].pop("P")
            opciones.append(op)
            desgloses[f["opp_id"]] = {"dimensiones": f["dimensiones"], "segunda_pasada": f.get("segunda_pasada") or {},
                                      "saturacion_narrativa": bool(f.get("saturacion_narrativa"))}
            por_opp[f["opp_id"]] = f
            fecha_nivel = str(pd.Timestamp(fd_precio).date())
            nivel_base = {"unidad": "nivel del indicador de seguimiento", "fecha_dato": fecha_nivel, "fuente": fuente,
                          "hora_fijacion": hora_fij, "conocible_desde": fecha_nivel}
            niveles = {"nivel_actual": {"valor": precio, **nivel_base}}
            for i, x in enumerate(f.get("invalidacion_cuantitativa") or []):
                niveles[f"invalidacion_{i + 1}"] = {"valor": float(x["umbral"]), **nivel_base,
                                                    "unidad": f"nivel de {x.get('simbolo')} (invalidación, no de entrada)"}
            # Encargo para el Bloque B (2.5 y Anexo B Forex): el Bloque B elige instrumento, coste, cobertura y ejecución
            b = {"opp_id": f["opp_id"], "segmento": c, "tipo_opcion": tipo_op, "nombre": op["nombre"], "par": op["par"],
                 "composicion": copy.deepcopy(op["composicion"]), "direccion": op["direccion"],
                 "divisa_financiacion": op["divisa_financiacion"], "ambito": copy.deepcopy(op["ambito"]),
                 "tesis": op["tesis"], "mecanismo": op["mecanismo"], "horizontes": sorted(hz), "horizonte_principal": hp,
                 "pronosticos": [hz[h]["prg_id"] for h in sorted(hz)], "catalizadores": copy.deepcopy(op["catalizadores"]),
                 "riesgos": op["riesgos"], "invalidacion": op["invalidacion"],
                 "indicador_seguimiento": copy.deepcopy(op["indicador_seguimiento"]), "niveles_referencia": niveles,
                 "carry_esperado": {"anual_pct": carry.get("anual_pct"), "signo": carry["signo"]},
                 "consideraciones_implementacion": _consideraciones(f, op),
                 "metricas_clave": _lista(f.get("metricas_clave"), [f"Evolución de {op['indicador_seguimiento']['nombre']}",
                                                                    "Diferencial de tipos y carry de la exposición",
                                                                    "Condiciones de invalidación declaradas"]),
                 "preguntas_para_B": _lista(f.get("preguntas_para_B"),
                                            [f"¿Qué forma de exposición captura mejor «{op['nombre']}» con su carry y su coste?"]),
                 "evidencias": list(op["evidencias"]), "calculos": list(op["calculos"]),
                 "siguiente_paso_sugerido": op["siguiente_paso_sugerido"], "relevancia_decisional": op["relevancia_decisional"]}
            if tipo_op == "VOLATILIDAD":
                b["vista_volatilidad"] = copy.deepcopy(op["vista_volatilidad"])
            bloque_b.append(b)
        # finalistas no seleccionadas: pronósticos congelados con en_informe = false (aprendizaje sin sesgo de selección)
        sel_ids = {o["opp_id"] for o in opciones}
        for f in sel["candidatos"]:
            if f["opp_id"] not in sel_ids and not f.get("_arrastre") and f["_ht03"]["elegible"]:
                borradores(f, c, False)
        n = len(opciones)
        rk_max = max([o["puntuaciones"]["RK"] for o in opciones], default=0)
        sem = "GRIS" if n == 0 else ("VERDE" if n >= 2 or rk_max >= 70 else "AMBAR")
        fins = an["finalistas"]
        reg = an.get("regimen") or ""
        segmentos_out[c] = {"estado_semaforo": sem,
                            "regimen_segmento": reg[:600] if len(reg) >= 10 else "Régimen del segmento no disponible en este ciclo",
                            "candidatas_analizadas": max(len(an.get("cribado", [])), len(fins), len(sel["candidatos"]), n),
                            "embudo": {"gc0_delta_material": bool(gc0[c]["cambio_material"]), "cribadas": len(an.get("cribado", [])),
                                       "pasan_gc1": sum(1 for x in an.get("cribado", []) if x.get("paso_gc1")),
                                       "pasan_gc2": sum(1 for f in fins if f.get("_gc2")), "finalistas_gc3": min(sum(1 for f in fins if f.get("_gc3")), 5),
                                       "elegibles": sum(1 for e in sel["evaluadas"] if e["elegible"])},
                            "opciones": opciones, "menos_de_tres_motivo": _menos_de_tres_texto(c, sel, n)}
        paquete_segmentos[c] = [{"opp_id": o["opp_id"], "rango": o["rango"], "confianza": o["confianza"]} for o in opciones]

    todas = [o for c in segmentos_out for o in segmentos_out[c]["opciones"]]
    clust = {}
    for o in todas:
        clust.setdefault(o["cluster_id"], []).append(o["opp_id"])
    fact = {str(x.get("cluster_id")): x.get("factor") for x in integ.get("factores_dominantes", []) if isinstance(x, dict)}
    clusteres_exp = [{"cluster_id": k, "factor_dominante": fact.get(k) or f"Factor común de las opciones del clúster {k} "
                      "(correlación semanal ≥ 0,7, ML-CLUS-001)", "opp_ids": v} for k, v in sorted(clust.items())]
    for o in todas:
        o["factor_dominante"] = next(e["factor_dominante"] for e in clusteres_exp if o["opp_id"] in e["opp_ids"])
    # Exposición agregada por divisa (14.1; ML-CLUS-001 v2.0, paso iv) y contradicciones entre segmentos (9.6.6)
    neta = fx.exposicion_neta(todas)
    exposicion = {d: fx.categoria_exposicion(v) for d, v in sorted(neta.items())}
    lados: Dict[str, Dict[str, List[Tuple[str, str]]]] = {}
    for o in todas:
        for d, lado in ht09.patas_activas(o).items():      # 9.6.6: solo la pata activa de la tesis cuenta
            lados.setdefault(d, {"LARGO": [], "CORTO": []})[lado].append((o["segmento"], o["opp_id"]))
    just = {str(x.get("divisa")): str(x.get("justificacion_contradiccion")) for x in (integ.get("contradicciones") or [])
            if isinstance(x, dict) and len(str(x.get("justificacion_contradiccion") or "")) >= 10}
    contradicciones = []
    for d, l in sorted(lados.items()):
        if any(a[0] != b[0] for a in l["LARGO"] for b in l["CORTO"]) and d in just:
            contradicciones.append({"divisa": d, "opp_ids": sorted({x[1] for x in l["LARGO"] + l["CORTO"]}),
                                    "justificacion_contradiccion": just[d]})
    # Lectura para la divisa base del usuario (termómetro del euro, 14.2.2)
    nb = neta.get(divisa_base, 0.0)
    sentido = "se_aprecia" if nb > 1e-9 else ("se_deprecia" if nb < -1e-9 else "estable")
    llano_base = fx.llano(divisa_base)
    texto_def = {"se_aprecia": f"Las ideas de esta semana apuntan a que {llano_base} gane algo de valor.",
                 "se_deprecia": f"Las ideas de esta semana apuntan a que {llano_base} pierda algo de valor.",
                 "estable": f"Las ideas de esta semana no apuntan a un cambio claro de {llano_base}."}[sentido]
    # El texto se genera de forma determinista para que siempre coincida con el sentido calculado; la lectura del
    # Analizador se conserva en «x_lectura_divisa_base_analizador» (informe técnico)
    lectura = {"divisa": divisa_base, "sentido": sentido, "texto_llano": texto_def[:200]}
    # Régimen cambiario (AG-09 y AG-21; si faltan, lectura determinista HT-01)
    bcm = (transversales.get("BCM") or {}).get("datos") or {}
    pfv = (transversales.get("PFV") or {}).get("datos") or {}
    rg = bcm.get("regimen_global") or {}
    vols = [t.get("vol_20d") for an in analisis.values() for t in (an.get("senales") or {}).values() if t.get("vol_20d")]
    vol_media = sum(vols) / len(vols) if vols else None
    vol_det = None if vol_media is None else ("baja" if vol_media < 0.07 else ("alta" if vol_media > 0.12 else "media"))
    regimen_cambiario = {"dolar": rg.get("dolar") if rg.get("dolar") in ("fuerte", "neutro", "debil") else "neutro",
                         "riesgo": rg.get("riesgo") if rg.get("riesgo") in ("apetito", "neutro", "aversion") else "neutro",
                         "volatilidad": pfv.get("regimen_volatilidad") if pfv.get("regimen_volatilidad") in ("baja", "media", "alta")
                         else (vol_det or "media")}
    if not rg or not pfv.get("regimen_volatilidad"):
        regimen_cambiario["nota"] = ("Lectura determinista con datos HT-01 donde faltan los informes transversales"
                                     + (f" (volatilidad media realizada {vol_media:.1%})" if vol_media else ""))
    informes = {"BCM": (transversales.get("BCM") or {}).get("trv_id"), "PFV": (transversales.get("PFV") or {}).get("trv_id")}
    notas_trv = [v.get("nota") for v in transversales.values() if v.get("nota")]
    if notas_trv or not all(informes.values()):
        informes["nota"] = "; ".join(notas_trv) or "Informes transversales no disponibles en este ciclo"
    # Seguimiento de vigentes
    seguimiento = []
    f3 = bloque.almacen.estado("F3", as_of)
    sel_ids = {o["opp_id"] for o in todas}
    for c in segmentos:
        cerr = {x["opp_id"]: x for x in seleccion[c]["cerradas"]}
        for v in bloque.vigentes(as_of, c):
            dec = ((f3.get(v["opp_id"]) or {}).get("decision_broker") or {}).get("decision")
            if v["opp_id"] in sel_ids:
                seguimiento.append({"opp_id": v["opp_id"], "estado": "VIGENTE", "comentario": "Se mantiene en el top-3 (continuidad 9.6.4)", "decision_broker": dec})
            else:
                x = cerr.get(v["opp_id"], {"motivo_cierre": "SUSTITUCION", "comentario": "Sale del top-3: sustituida o ya no elegible"})
                seguimiento.append({"opp_id": v["opp_id"], "estado": "CERRADA", "motivo_cierre": x["motivo_cierre"], "comentario": x["comentario"], "decision_broker": dec})
    limit = [x for x in integ.get("limitaciones", []) if isinstance(x, str) and len(x) >= 5]
    limit += [x for x in (getattr(bloque, "_limitaciones_extra", None) or []) if x not in limit]
    for c in segmentos:
        if analisis[c].get("estado") == "PARCIAL":
            limit.append(f"{NOMBRE_SEGMENTO[c]}: alcance reducido declarado ({'; '.join(analisis[c].get('lagunas', [])[:2]) or 'salida parcial'})")
    for cz in presupuesto.cierres:
        limit.append(f"Presupuesto agotado en {cz['segmento']} (fase {cz['fase']}): {cz['motivo']}; alcance reducido, controles intactos (R16)")
    for d, l in sorted(lados.items()):
        if any(a[0] != b[0] for a in l["LARGO"] for b in l["CORTO"]) and d not in just:
            limit.append(f"{d} con dirección opuesta en dos segmentos sin justificación: pendiente de resolución (9.6.6)")
    if bloque.modo == "backtest":
        limit.append("Backtest: búsqueda web desactivada; evidencia limitada a datos HT-01 y referencias anteriores a la fecha as_of; "
                     "riesgo de fuga por conocimiento del modelo")
    if not limit:
        limit.append("Ninguna limitación adicional a las declaradas por opción")
    # Supuestos declarados (6.2.9): consultas CT-23 del RUN vencidas o pendientes con su supuesto
    sup_decl, sin_resp = [], []
    if getattr(bloque, "consultas", None) is not None:
        sup_decl, sin_resp = bloque.consultas.supuestos_de_run(run_id, as_of)
    hist = copy.deepcopy(historial)
    hist.setdefault("referencia", "paseo aleatorio y forward")
    hist.setdefault("por_segmento", {})
    paquete = {"run_id": run_id, "fecha": str(as_of.date()), "fecha_datos_mercado": max(fechas_dato) if fechas_dato else str(as_of.date()),
               "methodology_version": str(f10.get("P-30") or "FX-1.1"), "tipo": tipo, "nivel_por_segmento": nivel,
               "divisa_base_usuario": divisa_base,
               "regimen_macro": integ.get("regimen_macro") if len(integ.get("regimen_macro") or "") >= 10 else "Régimen macro no disponible",
               "regimen_cambiario": regimen_cambiario, "informes_transversales": informes,
               "apuestas_independientes": len(clust), "clusteres_exposicion": clusteres_exp, "exposicion_agregada": exposicion,
               "lectura_divisa_base": lectura, "contradicciones_entre_segmentos": contradicciones, "segmentos": segmentos_out,
               "seguimiento_vigentes": seguimiento, "historial_aciertos": hist, "paquete_para_bloque_B": bloque_b,
               "preguntas_sugeridas": [x for x in integ.get("preguntas_sugeridas", []) if isinstance(x, str) and len(x) >= 5][:6],
               "limitaciones": limit, "aviso_legal": AVISO_LEGAL,
               "supuestos_declarados": sup_decl, "consultas_broker_sin_respuesta": sin_resp,
               "x_lectura_conjunto": integ.get("lectura_conjunto", ""),
               "x_lectura_divisa_base_analizador": integ.get("lectura_divisa_base") or "", "x_cambios_vs_anterior": integ.get("cambios_vs_anterior", ""),
               "x_n_efectivo": clusteres.get("n_efectivo")}
    extras = {"prg_borradores": prg_borradores, "desgloses": desgloses, "paquete_segmentos": paquete_segmentos, "por_opp": por_opp,
              "seleccion": seleccion, "analisis": analisis, "gc0": gc0, "exposicion_neta": neta}
    return paquete, extras


def ht09_validar(bloque, paquete: Dict, extras: Dict, informe_visual: Optional[str]) -> Dict:
    certs = [{"segmento": c["celda"]["segmento"], "horizonte": c["celda"]["horizonte"], "vigente": True, "metodo": None}
             for c in bloque.evaluador.certificados_vigentes(paquete["fecha"])]
    f2 = bloque.almacen.estado("F2", clave="clm_id")
    trazas = {k: v.get("evidencias", []) for k, v in f2.items() if v.get("tipo_entrada") == "CLM"}
    artef = [e["calc_id"] for e in bloque.almacen.leer("RC") if e.get("estado") in ("SERVED", "SERVED_WITH_LIMITATIONS")]
    return ht09.validar(paquete, certs, informe_visual, extras["desgloses"], bloque.params_ht03, trazas, artef,
                        float((bloque.cfg.get("redaccion") or {}).get("umbral_fh", 70.0)))


def _recalcular_conjunto(p: Dict, extras: Dict) -> None:
    todas = [o for d in p["segmentos"].values() for o in d["opciones"]]
    neta = fx.exposicion_neta(todas)
    p["exposicion_agregada"] = {d: fx.categoria_exposicion(v) for d, v in sorted(neta.items())}
    extras["exposicion_neta"] = neta
    ids = {o["opp_id"] for o in todas}
    p["contradicciones_entre_segmentos"] = [x for x in p.get("contradicciones_entre_segmentos", [])
                                            if len([i for i in x["opp_ids"] if i in ids]) >= 2]
    for x in p["contradicciones_entre_segmentos"]:
        x["opp_ids"] = [i for i in x["opp_ids"] if i in ids]
    lb = p.get("lectura_divisa_base")
    if isinstance(lb, dict):
        nb = neta.get(lb["divisa"], 0.0)
        nuevo = "se_aprecia" if nb > 1e-9 else ("se_deprecia" if nb < -1e-9 else "estable")
        if nuevo != lb["sentido"]:
            lb["sentido"] = nuevo
            lb["texto_llano"] = {"se_aprecia": f"Las ideas de esta semana apuntan a que {fx.llano(lb['divisa'])} gane algo de valor.",
                                 "se_deprecia": f"Las ideas de esta semana apuntan a que {fx.llano(lb['divisa'])} pierda algo de valor.",
                                 "estable": f"Las ideas de esta semana no apuntan a un cambio claro de {fx.llano(lb['divisa'])}."}[nuevo]


def retirar_opciones(bloque, paquete: Dict, extras: Dict, afectadas: Set[str]) -> Tuple[Dict, Dict]:
    """Retira las opciones con bloqueo G3 (se conservan sus pronósticos con en_informe = false) y reajusta el paquete."""
    p = copy.deepcopy(paquete)
    for c, d in p["segmentos"].items():
        quedan = [o for o in d["opciones"] if o["opp_id"] not in afectadas]
        if len(quedan) != len(d["opciones"]):
            for i, o in enumerate(quedan):
                o["rango"] = i + 1
            d["opciones"] = quedan
            d["estado_semaforo"] = "GRIS" if not quedan else d["estado_semaforo"]
            if len(quedan) < 3:
                d["menos_de_tres_motivo"] = ((d.get("menos_de_tres_motivo") or f"Se proponen {len(quedan)} opción(es).")
                                             + " Opciones retiradas por la validación G3: " + ", ".join(sorted(afectadas)) + ".")
            extras["paquete_segmentos"][c] = [{"opp_id": o["opp_id"], "rango": o["rango"], "confianza": o["confianza"]} for o in quedan]
    p["paquete_para_bloque_B"] = [b for b in p["paquete_para_bloque_B"] if b["opp_id"] not in afectadas]
    for e in p["clusteres_exposicion"]:
        e["opp_ids"] = [x for x in e["opp_ids"] if x not in afectadas]
    p["clusteres_exposicion"] = [e for e in p["clusteres_exposicion"] if e["opp_ids"]]
    p["apuestas_independientes"] = len(p["clusteres_exposicion"])
    _recalcular_conjunto(p, extras)
    for b in extras["prg_borradores"]:
        if b["opp_id"] in afectadas:
            b["en_informe"] = False
    for k in afectadas:
        extras["desgloses"].pop(k, None)
    p["limitaciones"].append(f"Opciones retiradas por bloqueo G3: {', '.join(sorted(afectadas))}")
    return p, extras


def mensaje_redactor(paquete: Dict) -> Dict:
    return {"run_id": paquete["run_id"], "fecha": paquete["fecha"], "apuestas_independientes": paquete["apuestas_independientes"],
            "historial_aciertos": paquete["historial_aciertos"].get("global"),
            "divisa_base_usuario": paquete.get("divisa_base_usuario"), "lectura_divisa_base": paquete.get("lectura_divisa_base"),
            "exposicion_agregada": paquete.get("exposicion_agregada"),
            "segmentos": {c: {"semaforo": d["estado_semaforo"], "n": len(d["opciones"]), "candidatas_analizadas": d["candidatas_analizadas"],
                              "menos_de_tres_motivo": d["menos_de_tres_motivo"],
                              "opciones": [{"opp_id": o["opp_id"], "nombre_llano": o["nombre_llano"], "tesis": o["tesis"],
                                            "riesgos": o["riesgos"][:2], "tipo_opcion": o["tipo_opcion"], "par": o.get("par"),
                                            "composicion": o.get("composicion"), "vista_volatilidad": o.get("vista_volatilidad"),
                                            "sube_baja_llano": o.get("sube_baja_llano"), "carry": o.get("carry"),
                                            "riesgo_1a5": o["riesgo_1a5"], "horizontes": sorted(o["horizontes"]),
                                            "banda": o["horizontes"][o["horizonte_principal"]]["banda"]} for o in d["opciones"]]}
                          for c, d in paquete["segmentos"].items()}}
