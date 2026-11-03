"""Respuestas sintéticas deterministas del MockClient, válidas frente a los esquemas de `contratos.ESQUEMAS`.

Reaccionan a la entrada lo suficiente para ejercitar las ramas: señales del universo → candidatas y dimensiones;
vigentes con invalidación → CERRAR; evidencia débil → objeción fuerte sin resolver; lecciones de calibración →
probabilidades más prudentes; preguntas de contraste → escalado. Simulan además un modelo «vulnerable» a las
instrucciones incrustadas (si llegara a ver una sin neutralizar, subiría todas las dimensiones de A a 100), para
comprobar que el saneamiento R9 del ejecutor funciona.
"""
from __future__ import annotations

import hashlib
import json
import random
from typing import Dict, List

import pandas as pd

from .prompts import extraer_encargo

BASE_LLANO = {"RV": "Acciones", "RF": "Bonos", "DIV": "Monedas", "MP": "Materias primas", "IDX": "Bolsa entera",
              "FON": "Fondos", "DER": "Derivados", "INM": "Inmuebles en bolsa", "CRI": "Monedas digitales",
              "ALT": "Inversión alternativa", "MON": "Ahorro a corto plazo", "TCV": "Tipos y nervios del mercado"}
PALABRAS_CLASE = {"RV": ["acciones", "renta variable", "sector"], "RF": ["bonos", "renta fija", "deuda"],
                  "DIV": ["divisa", "moneda", "yen", "dólar"], "MP": ["oro", "petróleo", "materias", "plata"],
                  "IDX": ["índice", "indices", "índices", "bolsa entera"], "FON": ["fondo", "etf"], "DER": ["derivado", "opcion", "opción", "futuro"],
                  "INM": ["inmobiliario", "reit", "inmuebles"], "CRI": ["cripto", "bitcoin"], "ALT": ["alternativ", "capital privado"],
                  "MON": ["letras", "liquidez", "monetari", "depósito"], "TCV": ["volatilidad", "vix", "curva", "crédito", "breakeven"]}
REG_CORTA = {"NAM": "EE. UU.", "LAT": "América Latina", "EUR": "Europa", "AFR": "África", "ORM": "Oriente Medio", "CHN": "China",
             "ASE": "Asia", "JPN": "Japón", "OCE": "Australia", "GLB": "todo el mundo"}
ANALISTAS_MOCK = ("AG-03", "AG-04", "AG-05", "AG-06", "AG-07", "AG-08", "AG-09", "AG-21", "AG-22", "AG-23", "AG-24", "AG-25")
REG_TEXTO = {"NAM": "Norteamérica", "LAT": "Latinoamérica", "EUR": "Europa", "AFR": "África", "ORM": "Oriente Medio", "CHN": "China",
             "ASE": "Asia emergente", "JPN": "Japón", "OCE": "Oceanía", "GLB": "Global"}


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
    return {"AG-10": _prospectiva, "AG-11": _contrarias, "AG-12": _curador, "AG-02": _integracion, "AG-17": _redactor,
            "AG-01": _coordinador, "AG-18": _orquestador, "AG-19": _auditor, "AG-20": _evaluador, "AG-14": _busqueda,
            "AG-16": _busqueda, "AG-15": _busqueda, "AG-13": _plan_motor}[agente](msg, ctx, rng)


# ------------------------------------------------------------------------------------------
def _horizontes(msg: Dict) -> List[str]:
    tabla = msg.get("horizontes_aplicables_clase") or {}
    interes = msg.get("horizontes_interes") or ["H1", "H2", "H3", "H4"]
    si = [h for h in ("H2", "H3", "H4", "H1") if tabla.get(h) == "SI" and h in interes]
    out = si[:2] or [h for h in ("H3", "H4") if tabla.get(h) != "NO"][:1]
    if tabla.get("H5") == "SI" and "H5" in interes:      # V5.1: H5 solo como horizonte secundario estructural
        out.append("H5")
    return out


def _ficha(u: Dict, msg: Dict, ctx: Dict, rng: random.Random, inyectado: bool) -> Dict:
    s = u["senales"]
    clase, sym = msg["clase"], u["simbolo"]
    sc = s.get("senal_compuesta") or 0.5
    pm = s.get("pct_momentum_clase") if s.get("pct_momentum_clase") is not None else 0.5
    pp = s.get("pct_precio_3a") if s.get("pct_precio_3a") is not None else 0.5
    e_base = rng.choice([60, 70, 70, 80])
    dims = {"T": {k: _r10(50 + 30 * sc) for k in ("magnitud", "alcance", "velocidad", "duracion", "difusion", "posicion_cadena_valor",
                                                  "capacidad_transformadora", "claridad_causal")},
            "E": {"calidad_raices": e_base, "cobertura_variables": 70, "calidad_metodologica": 70, "trazabilidad": 80, "actualidad": 80,
                  "discrepancias_resueltas": _r10(e_base - 10), "objeciones_respondidas": 70},
            "M": {k: 50 for k in ("adopcion", "escalado", "indicadores_disponibles", "persistencia", "estabilidad_impulsores", "hitos_claros")},
            "A": {"asimetria": _r10(35 + 55 * sc), "valoracion": _r10(75 - 40 * pp), "catalizadores": 60, "momento": _r10(30 + 60 * pm),
                  "invertibilidad": 80},
            "P": {"novedad": 60, "incertidumbre_reducible": 60, "coste_eficiencia": 70}}
    if inyectado:
        dims["A"] = {k: 100 for k in dims["A"]}
    precio = s.get("precio") or 100.0
    f = pd.Timestamp(ctx["fecha_as_of"]) + pd.DateOffset(months=1)
    refs = msg.get("referencias_disponibles") or []
    afirm = [{"afirmacion": f"La señal compuesta de {sym} es {sc:.2f} con tendencia «{s.get('tendencia_26s', 'sin dato')}» a 26 semanas",
              "fuente": f"HT-01:{sym}", "direccion": "favorable" if sc >= 0.5 else "contraria"}]
    if refs:
        afirm.append({"afirmacion": f"El marco de análisis de la clase {clase} respalda la lectura de {sym}", "fuente": refs[0]["ref_id"],
                      "direccion": "favorable"})
    region = REG_TEXTO.get(u.get("region") or "GLB", "Global")
    out = {"nombre": u["nombre"], "nombre_llano": f"{BASE_LLANO[clase]} de {REG_CORTA.get(u.get('region') or 'GLB', 'todo el mundo')}"[:70], "tipo_opcion": u.get("tipo_opcion") or "MERCADO",
           "subtipo": u.get("subtipo") or u.get("sector") or "Ámbito",
           "ambito": {"incluye": u.get("ambito_incluye") or u["nombre"],
                      "excluye": u.get("ambito_excluye") or "Activos concretos: su selección corresponde al Bloque B", "region": region},
           "indicador_seguimiento": {"nombre": u.get("indicador") or u["nombre"], "simbolo": sym, "fuente": "HT-01"},
           "invertibilidad": {"universo_suficiente": True,
                              "nota": "Existe un universo negociable amplio y accesible para un inversor minorista europeo en este ámbito."},
           "criterios_seleccion_sugeridos": [f"Exposición alta y directa a «{u['nombre']}»", "Liquidez diaria suficiente"],
           "metricas_clave": [f"Evolución del indicador de seguimiento ({sym})", "Momentum relativo frente a la referencia del tipo"],
           "preguntas_para_B": [f"¿Qué activos del ámbito «{u['nombre']}» capturan mejor la tendencia con menor riesgo?"],
           "tesis": f"{u['nombre']}: el impulso relativo y la tendencia sostienen una evolución favorable del ámbito en los próximos meses.",
           "mecanismo": "Persistencia del impulso de precios y flujos coherentes con la señal compuesta de la clase.",
           "valoracion": f"Precio en el percentil {pp:.0%} de sus últimos tres años (ST-DESC-001).",
           "catalizadores": [{"evento": "Publicación de datos mensuales de la clase", "fecha": f.strftime("%Y-%m")}],
           "riesgos": ["Reversión brusca del impulso", "Cambio de régimen de mercado"],
           "invalidacion": [f"Cierre de {sym} por debajo de {precio * 0.85:.2f}"],
           "invalidacion_cuantitativa": [{"simbolo": sym, "umbral": round(precio * 0.85, 4), "direccion": "por_debajo"}],
           "horizontes_aplicables": _horizontes(msg),
           "dimensiones": dims, "saturacion_narrativa": False,
           "premortem": "Falla si el impulso se agota, si cambia el régimen o si la señal era ruido.",
           "afirmaciones": afirm, "lo_que_no_sabemos": ["Si el impulso reciente persistirá tras el próximo dato relevante"],
           "regiones": [u.get("region") or "GLB"], "liquidez": "alta",
           "discrepancia_material": False,
           "tendencia": {"nombre_canonico": f"Impulso de precios en {u.get('sector') or clase} ({u.get('region') or 'GLB'})", "categoria": "SECTORIAL"}}
    if rng.random() < 0.8:
        out["segunda_pasada"] = {k: dict(v) for k, v in dims.items() if k in ("E", "A", "T")}
    return out


def _analista(msg: Dict, ctx: Dict, rng: random.Random, inyectado: bool) -> Dict:
    clase, fase = msg["clase"], msg["fase"]
    if fase == "RESPUESTA_OBJECIONES":
        res = []
        for o in msg.get("objeciones", []):
            e = o.get("dimensiones_E") or {}
            media = sum(v for v in e.values() if isinstance(v, int)) / max(len(e), 1)
            res.append({"objecion_id": o["objecion_id"], "respuesta": "Respondida con la evidencia de datos HT-01 y los cálculos CALC- de la clase.",
                        "resuelta": not (o["fuerza"] == "fuerte" and media < 70)})
        return {"respuestas": res}
    revision = [{"opp_id": v["opp_id"], "invalidacion_activada": bool(v.get("invalidacion_activada")),
                 "recomendacion": "CERRAR" if v.get("invalidacion_activada") else "MANTENER"} for v in msg.get("opciones_vigentes", [])]
    universo = sorted(msg.get("universo", []), key=lambda u: (-(u["senales"].get("senal_compuesta") or 0), u["simbolo"]))
    regimen = {"diagnostico": f"Régimen de {clase} a {ctx['fecha_as_of']}: señal compuesta media "
                              f"{(sum((u['senales'].get('senal_compuesta') or 0) for u in universo) / max(len(universo), 1)):.2f}."}
    if fase == "REVISION_VIGENTES":
        rot = [u for u in universo if u["simbolo"] in (msg.get("rotacion_exploratoria") or [])]
        expl = [_ficha(u, msg, ctx, rng, inyectado) for u in rot if (u["senales"].get("senal_compuesta") or 0) >= 0.75][:1]
        return {"clase": clase, "estado": "COMPLETO", "regimen_clase": regimen, "revision_vigentes": revision, "exploratorias": expl,
                "autoevaluacion": "Arrastre verificado sin incidencias."}
    cand = universo[:int(msg.get("max_candidatas", 8))]
    umbral = 0.55
    cribado = [{"candidata": u["simbolo"], "tipo_opcion": u.get("tipo_opcion"), "senal": u["senales"].get("senal_compuesta"),
                "paso_gc1": (u["senales"].get("senal_compuesta") or 0) >= umbral, "motivo": "señal compuesta frente al umbral"} for u in cand]
    fin = [_ficha(u, msg, ctx, rng, inyectado) for u in cand if (u["senales"].get("senal_compuesta") or 0) >= umbral][:min(4, int(msg.get("max_finalistas", 5)))]
    if fin and msg.get("referencias_disponibles") and rng.random() < 0.5:
        fin[0]["peticiones_conocimiento"] = [{"tipo": "CT-08", "pregunta": f"¿Qué dice la literatura sobre la persistencia del impulso en {clase}?",
                                             "objetivo": "confirmar", "para": fin[0]["indicador_seguimiento"]["simbolo"]}]
    return {"clase": clase, "fase": fase, "estado": "COMPLETO", "regimen_clase": regimen, "revision_vigentes": revision, "cribado": cribado,
            "finalistas": fin, "descartadas_relevantes": [{"nombre": u["simbolo"], "motivo": "señal débil"} for u in cand if u not in cand[:len(fin)]][:3],
            "senales_para_otras_clases": [], "lagunas": ["Sin datos de flujos ni de posicionamiento en el proveedor"],
            "autoevaluacion": "Cribado basado en señales cuantitativas; evidencia cualitativa limitada."}


def _prospectiva(msg, ctx, rng):
    prudente = any(l.get("tipo") == "CALIBRACION" for l in ctx.get("lecciones", []))
    res = []
    for e in msg["encargos"]:
        d = e.get("datos") or {}
        if e["tipo_pronostico"] == "RELATIVO":
            z = d.get("z_momentum_clase") or 0.0
            vista = "relativa_favorable" if z >= 0 else "relativa_desfavorable"
        else:
            z = d.get("momentum_12_1") or 0.0
            vista = "alcista" if z >= 0 else "bajista"
        prob = 0.65 if abs(z) > 0.5 else 0.55
        if prudente:
            prob = min(prob, 0.55)
        res.append({"ref": e["ref"], "escenarios": {h: {"base": "continuidad", "favorable": "aceleración", "adverso": "reversión"} for h in e["horizontes"]},
                    "pronosticos": [{"horizonte": h, "vista": vista, "prob_interna": prob, "escenario_asociado": "BASE", "metodo": "ACC-MOM-001",
                                     "afirmacion": f"{e['proxy']} {'bate' if vista in ('alcista', 'relativa_favorable') else 'queda por debajo de'} "
                                                   f"{e.get('referencia_indice') or 'cero'} en {h}"} for h in e["horizontes"]],
                    "hitos": [], "indicadores_adelantados": ["momentum 12-1"], "invalidacion": e.get("invalidacion_propuesta", [])})
    return {"resultados": res, "autoevaluacion": "Pronósticos sin certificado: bandas cualitativas."}


def _contrarias(msg, ctx, rng):
    res = []
    for p in msg["peticiones"]:
        e = (p.get("dimensiones") or {}).get("E") or {}
        media = sum(v for v in e.values() if isinstance(v, int)) / max(len(e), 1)
        objs = [{"id": f"OBJ-{p['ref']}-01", "tipo": "explicacion_alternativa", "fuerza": "moderada",
                 "argumento": "El impulso puede reflejar un rebote técnico y no un cambio de tendencia.", "evidencia": "historia de reversiones",
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
    return {"regimen_macro": f"Régimen sintético a {ctx['fecha_as_of']}: lectura agregada de las señales de {len(ins)} clases.",
            "factores_dominantes": [{"cluster_id": c, "factor": f"Factor común del clúster {c}"} for c in clus],
            "lectura_conjunto": "Las opciones dependen sobre todo del impulso de precios; las apuestas comparten riesgo de reversión.",
            "cambios_vs_anterior": "Cambios derivados de la evolución de las señales.",
            "preguntas_sugeridas": ["¿Qué opciones comparten el mismo factor de riesgo?", "¿Qué haría cambiar el semáforo de cada clase?"],
            "limitaciones": ["Datos sintéticos o de proveedor sin flujos ni posicionamiento"], "autoevaluacion": "Integración breve."}


def _redactor(msg, ctx, rng):
    p = msg["paquete_sintesis"]
    n = sum(c["n"] for c in p["clases"].values())
    nc = sum(1 for c in p["clases"].values() if c["n"])
    tarjetas = [{"opp_id": o["opp_id"], "por_que_llano": "Su precio sube más que el de otras ideas parecidas desde hace meses.",
                 "que_puede_salir_mal_llano": "Si el mercado cae, esta idea también puede caer.",
                 "ambito_llano": "Una zona del mercado, no un producto concreto. Otro equipo elegirá qué comprar."}
                for c in p["clases"].values() for o in c["opciones"]]
    motivos = {k: f"Miramos {c['candidatas_analizadas']} ideas. Solo {c['n']} pasaron todos los filtros. Preferimos no rellenar el hueco."
               for k, c in p["clases"].items() if c["n"] < 3}
    return {"frases_30s": [f"Esta semana vemos {n} ideas en {nc} de los {len(p['clases'])} tipos de inversión.",
                           (f"Varias dependen de lo mismo: en realidad son {p['apuestas_independientes']} apuestas distintas." if p['apuestas_independientes'] < n else "Cada idea depende de cosas distintas: no se repiten."),
                           "Cada idea puede salir mal. Mira su riesgo y su plazo."],
            "tarjetas": tarjetas, "motivos_llanos": motivos,
            "glosario": [{"termino": "Riesgo", "definicion": "Lo que puedes perder si la idea sale mal."},
                         {"termino": "Plazo", "definicion": "El tiempo que damos a la idea para cumplirse."},
                         {"termino": "Zona de interés", "definicion": "Precios en los que la idea nos parece razonable."}],
            "frase_historial": "Con pocos casos, la diferencia puede ser suerte. Aún no sabemos si acertamos más que el azar."}


def _coordinador(msg, ctx, rng):
    preg = msg["pregunta"].lower()
    mem = msg.get("memoria_bloque") or {}
    tema = " ".join(preg.split())[:60]
    if any(k in preg for k in ("qué opinas", "que opinas", "frente a", "profundiza", "analiza", "compara")):
        clases = [c for c, ws in PALABRAS_CLASE.items() if any(w in preg for w in ws)] or ["RV"]
        return {"clase_consulta": "PROFUNDIZACION" if "profundiza" in preg else "CONTRASTE", "ruta": "ANALITICA",
                "respuesta": "Respuesta provisional: la memoria del bloque no contiene ese contraste; se abre un análisis.",
                "referencias": [], "confianza": "especulativo", "tema_normalizado": tema,
                "escalado": {"nivel": "N2", "clases": clases, "pregunta": msg["pregunta"]}}
    refs = []
    ur = mem.get("ultimo_run") or {}
    if ur.get("run_id"):
        refs.append(ur["run_id"])
    for c, lst in (ur.get("top3_por_clase") or {}).items():
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
             "motivo": "temática de la clase"} for r in (msg.get("referencias_candidatas") or [])[:2]]
    return {"referencias": refs, "sintesis": "Contexto bibliográfico registrado; sin datos posteriores a la fecha límite.",
            "contradicciones": [], "lagunas": [] if refs else ["sin referencias registradas para la temática"]}


def _plan_motor(msg, ctx, rng):
    return {"ficha_id": "ST-DESC-001", "parametros": {}, "justificacion": "Alternativa del núcleo transversal."}
