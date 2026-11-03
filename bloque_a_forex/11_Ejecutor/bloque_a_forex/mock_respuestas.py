"""Respuestas sintéticas deterministas del MockClient, válidas frente a los esquemas de `contratos.ESQUEMAS`.

Reaccionan a la entrada lo suficiente para ejercitar las ramas: señales del universo → candidatas cambiarias con
par y dirección (o composición, o vista de volatilidad) coherentes con la señal, dimensiones de A Forex y carry;
informes transversales CT-06T (AG-09 y AG-21); contradicciones entre segmentos justificadas o no;
vigentes con invalidación → CERRAR; evidencia débil → objeción fuerte sin resolver; lecciones de calibración →
probabilidades más prudentes; preguntas de contraste → escalado. Simulan además un modelo «vulnerable» a las
instrucciones incrustadas (si llegara a ver una sin neutralizar, subiría todas las dimensiones de A a 100), para
comprobar que el saneamiento R9 del ejecutor funciona.
"""
from __future__ import annotations

import hashlib
import json
import copy
import random
from typing import Dict, List

import pandas as pd

from . import fx
from .prompts import extraer_encargo

PALABRAS_SEGMENTO = {"G10N": ["dólar", "euro", "yen", "libra", "franco suizo", "eur/usd", "usd/jpy", "g10"],
                     "G10M": ["australiano", "neozelandés", "canadiense", "corona", "materias primas"],
                     "EMAS": ["yuan", "rupia", "won", "asia"], "EMLA": ["peso mexicano", "real", "latinoam", "peso chileno"],
                     "EMEA": ["esloti", "florín", "lira", "rand", "shekel"], "ESTR": ["carry", "cesta", "estrategia", "momentum"]}
ANALISTAS_MOCK = ("AG-03", "AG-04", "AG-05", "AG-06", "AG-07", "AG-08")
TRANSVERSALES_MOCK = ("AG-09", "AG-21")
TIPOS_PAR = ("PAR", "CRUCE", "REGIMEN")
AHORRO = {"EUR": "euros", "USD": "dólares", "GBP": "libras", "CHF": "francos suizos", "JPY": "yenes"}


def _rng(semilla: int, *partes) -> random.Random:
    h = hashlib.sha256(json.dumps([semilla, *partes], sort_keys=True, default=str).encode()).digest()
    return random.Random(int.from_bytes(h[:8], "little"))


def _r10(x: float) -> int:
    return int(min(max(round(x / 10.0) * 10, 0), 100))


def responder(agente: str, mensajes: List[Dict], semilla: int) -> Dict:
    texto = mensajes[0]["content"]
    enc = extraer_encargo(texto)
    msg, ctx = enc["mensaje"], enc["contexto"]
    rng = _rng(semilla, agente, ctx.get("fecha_as_of"), json.dumps(msg, sort_keys=True, default=str)[:4000])
    inyectado = "ignora las instrucciones" in json.dumps(enc, ensure_ascii=False).lower()
    if agente in ANALISTAS_MOCK:
        return _analista(msg, ctx, rng, inyectado)
    if agente in TRANSVERSALES_MOCK:
        return _transversal(agente, msg, ctx, rng)
    return {"AG-10": _prospectiva, "AG-11": _contrarias, "AG-12": _curador, "AG-02": _integracion, "AG-17": _redactor,
            "AG-01": _coordinador, "AG-18": _orquestador, "AG-19": _auditor, "AG-20": _evaluador, "AG-14": _busqueda,
            "AG-16": _busqueda, "AG-15": _busqueda, "AG-13": _plan_motor}[agente](msg, ctx, rng)


# ------------------------------------------------------------------------------------------
def _horizontes(msg: Dict) -> List[str]:
    tabla = msg.get("horizontes_aplicables_segmento") or {}
    interes = msg.get("horizontes_interes") or ["H1", "H2", "H3", "H4"]
    si = [h for h in ("H2", "H3", "H4", "H1") if tabla.get(h) == "SI" and h in interes]
    return si[:2] or [h for h in ("H3", "H2") if tabla.get(h) not in ("NO", None)][:1] or ["H3"]


def _exposicion(u: Dict, sube: bool) -> Dict:
    """Notación y dirección (2.4) a partir del indicador del universo y del sentido de la señal."""
    tipo = u.get("tipo_opcion") or "PAR"
    if tipo == "VOLATILIDAD":
        return {"par": u.get("par"), "direccion": None, "composicion": [], "divisa_financiacion": None,
                "vista_volatilidad": {"sentido": "ALZA" if sube else "BAJA", "plazo": "1M"}}
    if tipo in TIPOS_PAR and u.get("par"):
        direc = "ALCISTA_BASE" if sube else "BAJISTA_BASE"
        comp = fx.composicion_par(u["par"], direc)
        return {"par": u["par"], "direccion": direc, "composicion": comp,
                "divisa_financiacion": next(c["divisa"] for c in comp if c["lado"] == "CORTO")}
    comp = copy.deepcopy(u.get("composicion_indicador") or [])
    if not sube:
        comp = fx.invertir(comp)
    cortos = sorted([c for c in comp if c["lado"] == "CORTO"], key=lambda c: (-c["peso"], c["divisa"]))
    return {"par": None, "direccion": None, "composicion": comp, "divisa_financiacion": cortos[0]["divisa"] if cortos else None}


def _ficha(u: Dict, msg: Dict, ctx: Dict, rng: random.Random, inyectado: bool) -> Dict:
    s = u["senales"]
    segmento, sym = msg["segmento"], u["simbolo"]
    sc = s.get("senal_compuesta") if s.get("senal_compuesta") is not None else 0.5
    sube = s.get("direccion_senal", "SUBE" if sc >= 0.5 else "BAJA") == "SUBE"
    fuerza = s.get("fuerza_senal") if s.get("fuerza_senal") is not None else abs(sc - 0.5) * 2
    pm = s.get("pct_momentum_segmento") if s.get("pct_momentum_segmento") is not None else 0.5
    pp = s.get("pct_precio_3a") if s.get("pct_precio_3a") is not None else 0.5
    cav = (s.get("carry_ajustado_vol") or 0.0) * (1 if sube else -1)
    tipo = u.get("tipo_opcion") or "PAR"
    expo = _exposicion(u, sube)
    e_base = rng.choice([60, 70, 70, 80])
    conv_dim = 90 if u.get("convertible") else (60 if u.get("ndf") else 40)
    dims = {"T": {k: _r10(50 + 40 * fuerza) for k in ("magnitud", "alcance", "velocidad", "duracion", "difusion", "posicion_cadena_valor",
                                                       "capacidad_transformadora", "claridad_causal")},
            "E": {"calidad_raices": e_base, "cobertura_variables": 70, "calidad_metodologica": 70, "trazabilidad": 80, "actualidad": 80,
                  "discrepancias_resueltas": _r10(e_base - 10), "objeciones_respondidas": 70},
            "M": {k: 50 for k in ("adopcion", "escalado", "indicadores_disponibles", "persistencia", "estabilidad_impulsores", "hitos_claros")},
            "A": {"asimetria": _r10(45 + 60 * fuerza), "valoracion": _r10(75 - 40 * pp if sube else 35 + 40 * pp),
                  "carry": _r10(50 + 40 * max(min(cav, 1.0), -1.0)) if tipo != "VOLATILIDAD" else "NA",
                  "catalizadores": 60, "momento_posicionamiento": _r10(30 + 60 * (pm if sube else 1 - pm)), "convertibilidad": conv_dim},
            "P": {"novedad": 60, "incertidumbre_reducible": 60, "coste_eficiencia": 70}}
    if inyectado:
        dims["A"] = {k: 100 for k in dims["A"]}
    precio = s.get("precio") or 100.0
    f = pd.Timestamp(ctx["fecha_as_of"]) + pd.DateOffset(months=1)
    refs = msg.get("referencias_disponibles") or []
    nombre_base = u.get("nombre") or sym
    if tipo in TIPOS_PAR and expo["par"]:
        nombre = f"{expo['par']} {'alcista' if sube else 'bajista'}"
    elif tipo == "VOLATILIDAD":
        nombre = f"{nombre_base}: volatilidad al {'alza' if sube else 'baja'}"
    else:
        nombre = nombre_base if sube else f"{nombre_base} (posición invertida)"
    sb = fx.sube_baja_llano(expo["composicion"])
    afirm = [{"afirmacion": f"La señal compuesta de {sym} es {sc:.2f} ({'sube' if sube else 'baja'}) con tendencia "
                            f"«{s.get('tendencia_26s', 'sin dato')}» a 26 semanas", "fuente": f"HT-01:{sym}", "direccion": "favorable"}]
    if s.get("carry_anual_pct") is not None:
        afirm.append({"afirmacion": f"El carry del indicador {sym} es {s['carry_anual_pct']:+.2f} % anual (FX-CARRY-001)",
                      "fuente": f"HT-01:{sym}", "direccion": "favorable" if cav >= 0 else "contraria"})
    if refs:
        afirm.append({"afirmacion": f"El marco de análisis del segmento {segmento} respalda la lectura de {sym}", "fuente": refs[0]["ref_id"],
                      "direccion": "favorable"})
    lado_inv = "por_debajo" if sube else "por_encima"
    umbral = round(precio * (0.95 if sube else 1.05), 4) if tipo != "VOLATILIDAD" else round(precio * (0.8 if sube else 1.2), 4)
    out = {"nombre": nombre, "nombre_llano": fx.nombre_llano(expo["composicion"], tipo, nombre_base),
           "tipo_opcion": tipo, **expo,
           "ambito": {"incluye": f"{u.get('indicador') or nombre_base}: tipo de cambio al contado y su rentabilidad total con carry",
                      "excluye": "Instrumentos concretos: su elección corresponde al Bloque B"},
           "indicador_seguimiento": {"nombre": u.get("indicador") or nombre_base, "simbolo": sym, "fuente": "HT-01"},
           "convertibilidad": {"convertible": bool(u.get("convertible", True)), "ndf": bool(u.get("ndf")),
                               "controles_capitales": bool(u.get("controles_capitales")),
                               "profundidad": {"alta": "alta", "media": "media", "baja": "baja"}.get(u.get("liquidez") or "alta", "alta"),
                               "nota": "Convertibilidad según el universo del ejecutor y las notas del Analista."},
           "consideraciones_implementacion": ["Liquidez máxima en el solape de las sesiones de Londres y Nueva York"],
           "metricas_clave": [f"Evolución del indicador de seguimiento ({sym})", "Diferencial de tipos y carry de la exposición"],
           "preguntas_para_B": [f"¿Qué forma de exposición a «{nombre}» ofrece mejor carry neto de costes para un inversor europeo?"],
           "tesis": f"{nombre}: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. {sb}".strip(),
           "mecanismo": "Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.",
           "valoracion": f"Indicador en el percentil {pp:.0%} de sus últimos tres años (ST-DESC-001).",
           "catalizadores": [{"evento": "Reunión de política monetaria del banco central de la divisa", "fecha": f.strftime("%Y-%m-%d")}],
           "riesgos": ["Giro de la política monetaria", "Episodio de aversión al riesgo"],
           "invalidacion": [f"Cierre de {sym} {'por debajo' if sube else 'por encima'} de {umbral} (nivel de invalidación, no de entrada)"],
           "invalidacion_cuantitativa": [{"simbolo": sym, "umbral": umbral, "direccion": lado_inv}],
           "horizontes_aplicables": _horizontes(msg),
           "dimensiones": dims, "saturacion_narrativa": False,
           "premortem": "Falla si cambia la política monetaria, si se deshace el carry o si la señal era ruido.",
           "afirmaciones": afirm, "lo_que_no_sabemos": ["Si el diferencial de tipos se mantendrá tras la próxima reunión"],
           "liquidez": u.get("liquidez") or "alta", "discrepancia_material": False,
           "tendencia": {"nombre_canonico": f"Divergencia de política monetaria en {segmento}", "categoria": "MONETARIA"}}
    if not sb:
        out.pop("sube_baja_llano", None)
    else:
        out["sube_baja_llano"] = sb
    if u.get("regimen"):
        out["regimen_cambiario_divisa"] = u["regimen"]
    # V1.1: tesis estructural H5 («limitado») sobre el dólar amplio solo si el Broker ha activado H5 en sus horizontes de interés
    if sym == "DOLAR-AMPLIO" and "H5" in (msg.get("horizontes_interes") or []) and \
            (msg.get("horizontes_aplicables_segmento") or {}).get("H5") == "LIMITADO":
        out["naturaleza_inversion"] = "ESTRUCTURAL"
        out["ambito_h5"] = "SISTEMA_MONETARIO_INTERNACIONAL"
        hs = [h for h in out["horizontes_aplicables"] if h != "H1"]
        if (msg.get("horizontes_aplicables_segmento") or {}).get("H4") == "SI" and "H4" not in hs:
            hs.append("H4")
        out["horizontes_aplicables"] = hs + ["H5"]
    if rng.random() < 0.8:
        out["segunda_pasada"] = {k: dict(v) for k, v in dims.items() if k in ("E", "A", "T")}
    return out


def _analista(msg: Dict, ctx: Dict, rng: random.Random, inyectado: bool) -> Dict:
    segmento, fase = msg["segmento"], msg["fase"]
    if fase == "RESPUESTA_OBJECIONES":
        res = []
        for o in msg.get("objeciones", []):
            e = o.get("dimensiones_E") or {}
            media = sum(v for v in e.values() if isinstance(v, int)) / max(len(e), 1)
            res.append({"objecion_id": o["objecion_id"], "respuesta": "Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento.",
                        "resuelta": not (o["fuerza"] == "fuerte" and media < 70)})
        return {"respuestas": res}
    revision = [{"opp_id": v["opp_id"], "invalidacion_activada": bool(v.get("invalidacion_activada")),
                 "recomendacion": "CERRAR" if v.get("invalidacion_activada") else "MANTENER"} for v in msg.get("opciones_vigentes", [])]
    universo = sorted(msg.get("universo", []), key=lambda u: (-(u["senales"].get("fuerza_senal") or 0), u["simbolo"]))
    regimen = {"diagnostico": f"Régimen de {segmento} a {ctx['fecha_as_of']}: fuerza media de la señal "
                              f"{(sum((u['senales'].get('fuerza_senal') or 0) for u in universo) / max(len(universo), 1)):.2f}."}
    if fase == "REVISION_VIGENTES":
        rot = [u for u in universo if u["simbolo"] in (msg.get("rotacion_exploratoria") or [])]
        expl = [_ficha(u, msg, ctx, rng, inyectado) for u in rot if (u["senales"].get("fuerza_senal") or 0) >= 0.5][:1]
        return {"segmento": segmento, "estado": "COMPLETO", "regimen_segmento": regimen, "revision_vigentes": revision, "exploratorias": expl,
                "autoevaluacion": "Arrastre verificado sin incidencias."}
    cand = universo[:int(msg.get("max_candidatas", 8))]
    umbral = 0.10
    cribado = [{"candidata": u["simbolo"], "tipo_opcion": u.get("tipo_opcion"), "senal": u["senales"].get("senal_compuesta"),
                "paso_gc1": (u["senales"].get("fuerza_senal") or 0) >= umbral, "motivo": "fuerza de la señal compuesta frente al umbral"}
               for u in cand]
    fin = [_ficha(u, msg, ctx, rng, inyectado) for u in cand
           if (u["senales"].get("fuerza_senal") or 0) >= umbral][:min(4, int(msg.get("max_finalistas", 5)))]
    if fin and msg.get("referencias_disponibles") and rng.random() < 0.5:
        fin[0]["peticiones_conocimiento"] = [{"tipo": "CT-08", "pregunta": f"¿Qué dice la literatura sobre el carry y el momentum en {segmento}?",
                                             "objetivo": "confirmar", "para": fin[0]["indicador_seguimiento"]["simbolo"]}]
    return {"segmento": segmento, "fase": fase, "estado": "COMPLETO", "regimen_segmento": regimen, "revision_vigentes": revision, "cribado": cribado,
            "finalistas": fin, "descartadas_relevantes": [{"nombre": u["simbolo"], "motivo": "señal débil"} for u in cand if u not in cand[:len(fin)]][:3],
            "senales_para_otros_segmentos": [], "lagunas": ["Sin datos de posicionamiento CFTC ni de volatilidad implícita en el proveedor"],
            "autoevaluacion": "Cribado basado en señales cuantitativas y carry; evidencia cualitativa limitada."}


def _transversal(agente: str, msg: Dict, ctx: Dict, rng: random.Random) -> Dict:
    destino = msg.get("segmentos_destino") or []
    resumen = msg.get("senales_por_segmento_ht01") or {}
    tipos = msg.get("tipos_por_divisa") or {}

    def media(c, k):
        xs = [v.get(k) for v in (resumen.get(c) or {}).values() if isinstance(v, dict) and v.get(k) is not None]
        return sum(xs) / len(xs) if xs else None
    senales = {}
    for c in destino:
        cm = media(c, "carry_anual_pct")
        vm = media(c, "vol_20d")
        senales[c] = (f"Carry medio {cm:+.2f} % anual" if cm is not None else "Carry no disponible") + \
                     (f"; volatilidad realizada media {vm:.1%}" if vm is not None else "")
    if agente == "AG-09":
        usd = (tipos.get("USD") or {}).get("tipo_pct")
        resto = [v["tipo_pct"] for k, v in tipos.items() if k != "USD" and v.get("tipo_pct") is not None]
        dif = (usd - sum(resto) / len(resto)) if usd is not None and resto else 0.0
        return {"regimen_global": {"dolar": "fuerte" if dif > 1.0 else ("debil" if dif < -1.0 else "neutro"), "riesgo": "neutro",
                                   "diagnostico": f"Diferencial medio del dólar frente al resto: {dif:+.2f} pp a {ctx['fecha_as_of']}."},
                "bancos_centrales": [{"banco": f"Banco central ({d})", "tipo_actual": v["tipo_pct"], "senda_descontada": "estable",
                                      "sesgo": "neutral", "proxima_reunion": None, "sorpresa_reciente": 0.0}
                                     for d, v in sorted(tipos.items())[:8]],
                "diferenciales": [], "calendario": [], "riesgos_intervencion": [], "senales_por_segmento": senales,
                "lagunas": ["Sin curvas OIS ni actas en el proveedor sintético"]}
    vols = [media(c, "vol_20d") for c in destino]
    vols = [v for v in vols if v is not None]
    vm = sum(vols) / len(vols) if vols else None
    return {"posicionamiento": [], "flujos": [], "volatilidad": [],
            "regimen_volatilidad": None if vm is None else ("baja" if vm < 0.07 else ("alta" if vm > 0.12 else "media")),
            "crowding_estrategias": [], "base_cruzada": [], "senales_por_segmento": senales,
            "lagunas": ["Sin datos CFTC, volatilidad implícita ni base cruzada en el proveedor sintético"]}


def _prospectiva(msg, ctx, rng):
    prudente = any(l.get("tipo") == "CALIBRACION" for l in ctx.get("lecciones", []))
    res = []
    for e in msg["encargos"]:
        d = e.get("datos") or {}
        vista = e.get("vista_esperada") or "alcista"
        fuerza = d.get("fuerza_senal") or 0.0
        prob = 0.60 if fuerza > 0.3 else 0.55
        if prudente:
            prob = min(prob, 0.55)
        sb = fx.sube_baja_llano(e.get("composicion") or [])
        if e.get("vista_volatilidad"):
            sb = f"La volatilidad de {e.get('par') or e['proxy']} {'sube' if vista == 'alcista' else 'baja'}."
        res.append({"ref": e["ref"], "escenarios": {h: {"base": "continuidad", "favorable": "aceleración", "adverso": "giro del diferencial"}
                                                    for h in e["horizontes"]},
                    "pronosticos": [{"horizonte": h, "vista": vista, "prob_interna": prob, "escenario_asociado": "BASE", "metodo": "FX-MOM-001",
                                     "afirmacion": f"{e['proxy']} {'sube' if vista == 'alcista' else 'baja'} en {h} frente al paseo aleatorio "
                                                   f"(sin cambio) y a lo que descuenta el forward. {sb}".strip()} for h in e["horizontes"]],
                    "hitos": [], "indicadores_adelantados": ["diferencial de tipos a 2 años", "momentum 12-1"],
                    "invalidacion": e.get("invalidacion_propuesta", [])})
    return {"resultados": res, "autoevaluacion": "Pronósticos sin certificado: bandas cualitativas frente al paseo aleatorio."}


def _contrarias(msg, ctx, rng):
    res = []
    for p in msg["peticiones"]:
        e = (p.get("dimensiones") or {}).get("E") or {}
        media = sum(v for v in e.values() if isinstance(v, int)) / max(len(e), 1)
        objs = [{"id": f"OBJ-{p['ref']}-01", "tipo": "explicacion_alternativa", "fuerza": "moderada",
                 "argumento": "El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe.", "evidencia": "historia de reversiones del carry",
                 "que_la_resolveria": "Confirmación del impulso en las próximas cuatro semanas"}]
        if media < 70:
            objs.append({"id": f"OBJ-{p['ref']}-02", "tipo": "evidencia_insuficiente", "fuerza": "fuerte",
                         "argumento": "La evidencia descansa en una sola familia de señales.", "evidencia": "raíces escasas",
                         "que_la_resolveria": "Una segunda raíz independiente de nivel A o B"})
        res.append({"ref": p["ref"], "objeciones": objs, "veredicto_global": "tesis frágil" if media < 70 else "tesis robusta"})
    return {"resultados": res, "autoevaluacion": "Refutación centrada en explicaciones alternativas."}


def _curador(msg, ctx, rng):
    return {"piezas": [{"indice": p["indice"], "tipo_afirmacion": "DATO" if str(p.get("fuente", "")).startswith(("HT-01", "CALC")) else "ANALISIS",
                        "nivel_confianza": "probable", "alertas": []} for p in msg["piezas"]]}


def _integracion(msg, ctx, rng):
    ins = msg.get("insumos_integracion") or {}
    clus = sorted({t.get("cluster") for v in ins.values() for t in v.get("top3", []) if t.get("cluster")})
    lados: Dict[str, Dict[str, List]] = {}
    for c, v in ins.items():
        for t in v.get("top3", []):
            for d, lado in (t.get("patas_activas") or {}).items():
                lados.setdefault(d, {"LARGO": [], "CORTO": []})[lado].append((c, t))
    contradicciones = []
    for d, l in sorted(lados.items()):
        pares = [(a, b) for a in l["LARGO"] for b in l["CORTO"] if a[0] != b[0]]
        # Solo se justifica si los horizontes no se solapan (mecanismos de plazo distinto); si coinciden, se deja sin
        # justificar para que el ejecutor la resuelva (sale la de menor RK)
        if pares and all(not set(a[1].get("horizontes") or []) & set(b[1].get("horizontes") or []) for a, b in pares):
            a, b = pares[0]
            contradicciones.append({"divisa": d, "justificacion_contradiccion":
                                    f"{d}: tesis de plazos distintos ({'/'.join(a[1].get('horizontes') or [])} en {a[0]} frente a "
                                    f"{'/'.join(b[1].get('horizontes') or [])} en {b[0]})."})
    base = msg.get("divisa_base_usuario") or "EUR"
    return {"regimen_macro": f"Régimen sintético a {ctx['fecha_as_of']}: lectura agregada de las señales de {len(ins)} segmentos.",
            "factores_dominantes": [{"cluster_id": c, "factor": f"Factor común del clúster {c}"} for c in clus],
            "contradicciones": contradicciones,
            "lectura_divisa_base": f"Para quien ahorra en {AHORRO.get(base, base)}, las ideas de esta semana cambian poco su poder de compra.",
            "lectura_conjunto": "Las opciones dependen sobre todo del dólar y del carry; las apuestas comparten riesgo de giro de tipos.",
            "cambios_vs_anterior": "Cambios derivados de la evolución de las señales y de los diferenciales.",
            "preguntas_sugeridas": ["¿Qué opciones comparten el mismo factor de riesgo?", "¿Qué haría cambiar el semáforo de cada segmento?"],
            "limitaciones": ["Datos sintéticos o de proveedor sin posicionamiento ni volatilidad implícita"], "autoevaluacion": "Integración breve."}


def _redactor(msg, ctx, rng):
    p = msg["paquete_sintesis"]
    n = sum(c["n"] for c in p["segmentos"].values())
    nc = sum(1 for c in p["segmentos"].values() if c["n"])
    tarjetas = []
    for c in p["segmentos"].values():
        for o in c["opciones"]:
            car = (o.get("carry") or {}).get("signo")
            tarjetas.append({"opp_id": o["opp_id"],
                             "por_que_llano": ("Esta moneda paga más interés que la otra." if car == "a favor"
                                               else "Su banco central va a otro ritmo que el de la otra moneda."),
                             "que_puede_salir_mal_llano": "Si el banco central cambia de idea, la moneda puede ir al revés.",
                             "sube_baja_llano": o.get("sube_baja_llano") or "Cambia el valor de una moneda frente a otra."})
    motivos = {k: f"Miramos {c['candidatas_analizadas']} ideas. Solo {c['n']} pasaron todos los filtros. Preferimos no rellenar el hueco."
               for k, c in p["segmentos"].items() if c["n"] < 3}
    return {"frases_30s": [f"Esta semana vemos {n} ideas en {nc} de los {len(p['segmentos'])} grupos de monedas.",
                           (f"Varias dependen de lo mismo: en realidad son {p['apuestas_independientes']} apuestas distintas."
                            if p["apuestas_independientes"] < n else "Cada idea depende de cosas distintas: no se repiten."),
                           "Cada idea puede salir mal. Mira su riesgo y su plazo."],
            "tarjetas": tarjetas, "motivos_llanos": motivos,
            "glosario": [{"termino": "Riesgo", "definicion": "Lo que puedes perder si la idea sale mal."},
                         {"termino": "Plazo", "definicion": "El tiempo que damos a la idea para cumplirse."},
                         {"termino": "Interés de la moneda", "definicion": "Lo que se cobra por tener una moneda que paga más interés que otra."}],
            "frase_historial": "Con pocos casos, la diferencia puede ser suerte. Aún no sabemos si acertamos más que el azar."}


def _coordinador(msg, ctx, rng):
    preg = msg["pregunta"].lower()
    mem = msg.get("memoria_bloque") or {}
    tema = " ".join(preg.split())[:60]
    if any(k in preg for k in ("qué opinas", "que opinas", "frente a", "profundiza", "analiza", "compara")):
        segmentos = [c for c, ws in PALABRAS_SEGMENTO.items() if any(w in preg for w in ws)] or ["G10N"]
        return {"clase_consulta": "PROFUNDIZACION" if "profundiza" in preg else "CONTRASTE", "ruta": "ANALITICA",
                "respuesta": "Respuesta provisional: la memoria del bloque no contiene ese contraste; se abre un análisis.",
                "referencias": [], "confianza": "especulativo", "tema_normalizado": tema,
                "escalado": {"nivel": "N2", "segmentos": segmentos, "pregunta": msg["pregunta"]}}
    refs = []
    ur = mem.get("ultimo_run") or {}
    if ur.get("run_id"):
        refs.append(ur["run_id"])
    for c, lst in (ur.get("top3_por_segmento") or {}).items():
        refs += [o["opp_id"] for o in lst][:2]
    refs += [r["id"] for r in mem.get("resultados_indice", []) if r.get("id")][:3]
    refs = list(dict.fromkeys(refs))
    return {"clase_consulta": "ACLARACION", "ruta": "N0",
            "respuesta": f"Según el último informe ({ur.get('run_id', 'sin informe')}), las opciones vigentes y sus motivos constan en los identificadores citados.",
            "referencias": refs, "confianza": "probable", "tema_normalizado": tema, "escalado": None}


def _orquestador(msg, ctx, rng):
    r = msg.get("resultado_ht09", {})
    if r.get("bloqueos"):
        return {"dictamen": "BLOQUEADO", "motivo": "Hay comprobaciones bloqueantes de G3.", "condiciones_para_apto": ["Retirar o corregir las opciones afectadas"]}
    return {"dictamen": "APTO_CON_ADVERTENCIAS", "motivo": "Solo advertencias; se entregan visibles.", "advertencias": [a["id"] for a in r.get("advertencias", [])]}


def _auditor(msg, ctx, rng):
    return {"hallazgos": [], "resumen": f"Revisión asíncrona de {len(msg.get('opciones', []))} opciones sin hallazgos materiales."}


def _evaluador(msg, ctx, rng):
    return {"resumen": f"Resueltos hoy {msg.get('resueltos_hoy')}; muestra aún insuficiente para certificar.", "lecciones": []}


def _busqueda(msg, ctx, rng):
    refs = [{"ref_id": r["ref_id"], "afirmacion": f"La referencia «{r['titulo'][:80]}» aporta contexto a la pregunta", "direccion": "favorable",
             "motivo": "temática del segmento"} for r in (msg.get("referencias_candidatas") or [])[:2]]
    return {"referencias": refs, "sintesis": "Contexto bibliográfico registrado; sin datos posteriores a la fecha límite.",
            "contradicciones": [], "lagunas": [] if refs else ["sin referencias registradas para la temática"]}


def _plan_motor(msg, ctx, rng):
    return {"ficha_id": "ST-DESC-001", "parametros": {}, "justificacion": "Alternativa del núcleo transversal."}
