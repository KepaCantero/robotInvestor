"""Respuestas sintéticas deterministas de los 24 agentes para el cliente simulado (MockClient).

Son reglas sencillas que leen el encargo (ámbito, dimensiones, datos y cálculos entregados) y devuelven JSON conforme a
los esquemas mínimos del ejecutor. Sirven para probar el flujo, los contratos, las puertas y los entregables; no dicen
nada de la capacidad analítica del bloque (eso solo se mide con el modelo real)."""
from __future__ import annotations

import hashlib
import random
from typing import Any, Dict, List

from .prompts import extraer_encargo

DIM_NOMBRE = {"D1": "definición y delimitación", "D2": "tamaño y demanda", "D3": "oferta y costes", "D4": "cadena de valor",
              "D5": "tecnología", "D6": "regulación", "D7": "macro y ciclo", "D8": "economía del sector",
              "D9": "valoración", "D10": "flujos y sentimiento", "D11": "sostenibilidad", "D12": "riesgos y catalizadores"}


def _rng(semilla: int, *claves) -> random.Random:
    return random.Random(int.from_bytes(hashlib.sha256("|".join(map(str, (semilla,) + claves)).encode()).digest()[:8], "little"))


def responder(agente: str, mensajes: List[Dict], semilla: int) -> Dict:
    texto = "".join(m["content"] if isinstance(m["content"], str) else "" for m in mensajes if m["role"] == "user")
    enc = extraer_encargo(texto)
    msg = enc.get("mensaje") or {}
    tarea = msg.get("tarea", "")
    f = _TAREAS.get((agente, tarea)) or _TAREAS.get(("*", tarea)) or _generico
    return f(msg, enc.get("contexto") or {}, _rng(semilla, agente, tarea, msg.get("pet_id"), msg.get("dim"), msg.get("tipo_activo")))


def _generico(msg, ctx, r) -> Dict:
    return {"estado": "COMPLETO", "resumen": "Encargo atendido por el agente simulado.", "autoevaluacion": "sin incidencias"}


# ------------------------------------------------------------------------------------------- Coordinador (AG-B01)
def _admision(msg, ctx, r):
    return {"clasificacion": "ADMITIDA", "motivo": None, "observaciones": "Petición de ámbito delimitado; sin datos sensibles.",
            "autoevaluacion": "admisión revisada con las reglas de 7.4 F0"}


def _justificacion(msg, ctx, r):
    p = msg.get("pendiente") or []
    return {"que_aporta": "Completar " + (", ".join(p[:4]) or "las fases pendientes") + " con la profundidad del plan.",
            "incertidumbres_que_reduce": [{"incertidumbre": "Robustez del ranking de candidatos y refutación de los finalistas",
                                           "efecto_posible": "candidatos PRIORITARIO_PARA_C ↔ SECUNDARIO"},
                                          {"incertidumbre": "Dimensiones de mayor peso aún en curso",
                                           "efecto_posible": "veredicto INVERTIR_ESCALONADO ↔ VIGILAR"}],
            "que_se_perderia": "Sin el tiempo adicional, la selección quedaría con un top-N reducido y una refutación limitada."}


def _consulta(msg, ctx, r):
    refs = msg.get("referencias_disponibles") or []
    clase = "ESTADO" if "estado" in (msg.get("pregunta") or "").lower() else "ACLARACION"
    if any(w in (msg.get("pregunta") or "").lower() for w in ("y si", "por qué a y no", "profundiza")):
        clase = "CONTRASTE"
    return {"clase_consulta": clase, "ruta": "PROPUESTA_DE_PETICION" if clase == "CONTRASTE" else "N0",
            "respuesta": ("Según el análisis registrado " + (refs[0] if refs else "en la memoria del bloque")
                          + ", la conclusión y sus candidatos constan con su fecha de corte; no se añade conocimiento propio."),
            "referencias": refs[:5], "confianza": "probable"}


# ------------------------------------------------------------------------------------------- Director (AG-B02)
def _plan(msg, ctx, r):
    disp = msg.get("ambitos_disponibles") or {}
    obj = msg.get("objeto") or {}
    clave = obj.get("clave_universo") or (msg.get("paquete_para_bloque_B") or {}).get("x_clave_universo")
    if clave not in disp:
        texto = (str(obj.get("descripcion", "")) + " " + str((msg.get("paquete_para_bloque_B") or {}).get("tesis", ""))).lower()
        clave = next((k for k, a in disp.items() if any(w in texto for w in str(a.get("nombre", "")).lower().split()[:3])),
                     next(iter(disp), None))
    a = disp.get(clave) or {}
    admitidos = msg.get("tipos_activo_admitidos") or a.get("tipos_activo") or ["RV"]
    aplicables = [t for t in admitidos if t in (a.get("tipos_activo") or admitidos)] or admitidos[:1]
    return {"clave_universo": clave, "tipo_objeto": a.get("tipo_objeto", "SECTOR"),
            "ambito": {"nombre": a.get("nombre", "Ámbito"), "nombre_llano": a.get("nombre_llano", "El ámbito pedido"),
                       "incluye": a.get("incluye", "—"), "excluye": a.get("excluye", "—"), "region": a.get("region", "Global")},
            "tipos_activo_aplicables": aplicables,
            "tipos_no_aplicables": {t: "Sin exposición material a la tesis del ámbito." for t in msg.get("tipos_todos", []) if t not in aplicables},
            "horizonte_dominante": a.get("horizonte", "H3"), "horizontes": [a.get("horizonte", "H3")],
            "tipos_materiales": aplicables[:1],
            "preguntas_decisivas": ["¿Qué parte de la cadena captura el valor?", "¿Cuánto descuenta ya el precio?"],
            "hipotesis": [{"enunciado": "Ventaja estructural sostenida del ámbito (tesis de partida)", "naturaleza": "estructural",
                           "discriminante": "persistencia de márgenes y de la demanda", "indicador_anticipado": "cartera de pedidos",
                           "invalidacion": "caída de pedidos dos trimestres"},
                          {"enunciado": "Repunte cíclico que se normaliza en 12 meses", "naturaleza": "cíclica",
                           "discriminante": "peso de contratos plurianuales", "indicador_anticipado": "nuevos pedidos frente a entregas",
                           "invalidacion": "pedidos plurianuales < 30 %"},
                          {"enunciado": "La oferta nueva cierra la brecha antes del horizonte", "naturaleza": "competitiva",
                           "discriminante": "capacidad anunciada y su calendario", "indicador_anticipado": "anuncios de capacidad",
                           "invalidacion": "capacidad nueva > 25 % del mercado"}],
            "rasgos_candidatos": {t: ["alta pureza de exposición", "balance sólido", "valoración no exigente"] for t in aplicables},
            "desviaciones": {}, "exclusiones": []}


def _informe_dimensional(msg, ctx, r):
    dims = msg.get("dimensiones") or [msg.get("dim", "D1")]
    datos = msg.get("datos_disponibles") or []
    calc = msg.get("calculos_disponibles") or []
    informes = []
    for d in dims:
        n = DIM_NOMBRE.get(d, d)
        notas = [{"afirmacion": f"La dimensión {n} del ámbito muestra señales coherentes con la tesis según los datos entregados.",
                  "etiqueta": "[HECHO]" if datos else "[INTERPRETACIÓN]", "usa_datos": datos[:2], "usa_calculos": calc[:1],
                  "contiene_cifra": False},
                 {"afirmacion": f"La lectura de {n} admite una explicación alternativa de carácter cíclico.",
                  "etiqueta": "[INTERPRETACIÓN]", "contiene_cifra": False}]
        if d in ("D9", "D12") and calc:
            notas.append({"afirmacion": f"El cálculo {calc[0]} sitúa la rentabilidad relativa mediana del escenario base en su rango histórico.",
                          "etiqueta": "[INTERPRETACIÓN]", "contiene_cifra": True, "clase_cifra": "estimacion_estadistica",
                          "usa_calculos": calc[:1]})
        informes.append({"dim": d, "notas": notas, "conclusion": f"La dimensión {n} apoya la tesis con matices.",
                         "confianza": {"nivel": r.choice(["media", "alta"]), "factores_a_favor": ["datos de mercado fechados"],
                                       "factores_en_contra": ["sin fuentes primarias sectoriales en el modo simulado"]},
                         "lagunas": ["Datos sectoriales primarios no disponibles en el cliente simulado"] if d in ("D2", "D3") else [],
                         "senales_para_otras_dimensiones": [], "pre_mortem": f"Si falla, será por un cambio en {n}."})
    return {"dim_informes": informes, "autoevaluacion": "informe simulado"}


def _reconocimiento(msg, ctx, r):
    cadena = msg.get("cadena_orientativa") or ["Insumos", "Fabricación", "Distribución", "Cliente final"]
    papeles = ["consume", "es", "es", "alimenta"]
    return {"definicion": "Mercado delimitado por la exposición económica real al ámbito, no por la clasificación sectorial.",
            "mapa_preliminar": [{"eslabon": e, "papel_del_ambito": papeles[min(i, 3)]} for i, e in enumerate(cadena)]}


def _integracion(msg, ctx, r):
    hips = msg.get("hipotesis") or []
    est = ["confirmada", "debilitada", "indeterminada", "debilitada"]
    esc = msg.get("escenarios_motor") or {}
    re_ = esc.get("RE", 50)
    asim = 70 if re_ >= 60 else 60 if re_ >= 50 else 40
    return {"tesis": {"enunciado": f"{msg.get('ambito_nombre', 'El ámbito')} mantiene una ventaja estructural que el precio solo descuenta en parte.",
                      "mecanismo": "La demanda planificada crece más deprisa que una oferta con plazos largos de ampliación.",
                      "premisas": [{"premisa": "La demanda del ámbito crece por encima del mercado amplio", "comprobacion": "Series de demanda y pedidos",
                                    "horizonte": msg.get("horizonte", "H3"), "invalidacion": "Dos trimestres de caída de pedidos", "dims": ["D2"]},
                                   {"premisa": "La oferta no se amplía antes del horizonte", "comprobacion": "Capacidad anunciada",
                                    "horizonte": msg.get("horizonte", "H3"), "invalidacion": "Capacidad nueva > 25 % del mercado", "dims": ["D3", "D4"]}]},
            "hipotesis_cierre": [{"indice": i, "estado": est[i % 4]} for i in range(len(hips))],
            "regimen": {"estado_confianza": "mixto", "variables_dominantes": ["tipos de interés", "ciclo industrial"],
                        "relaciones": [{"relacion": "Valoración del ámbito frente a tipos reales", "naturaleza": "historica_observada",
                                        "ventana_o_mecanismo": "últimos tres años"}],
                        "resumen": "Crecimiento moderado con tipos estabilizados."},
            "evaluaciones_separadas": {"mercado": "Atractivo: demanda estructural.", "calidad_ambito": "Buena: márgenes por encima de su media.",
                                       "atractivo_bursatil": "Moderado: parte del crecimiento ya está en el precio.",
                                       "accesibilidad": "Adecuada en los tipos de activo aplicables."},
            "componentes_A": {"asimetria": asim, "valoracion_expectativas": 50, "calidad_crecimiento": 70, "ventaja_estructural": 70,
                              "catalizadores": 60, "momento_flujos": 60 if re_ >= 50 else 40, "riesgos": 50},
            "componentes_E": {"calidad_raices": 60, "calidad_metodologica": 70, "discrepancias_resueltas": 70, "actualidad": 80},
            "flags": {"valoracion_parcialmente_descontada": True}, "saturacion_narrativa": False,
            "despliegue_estructural": {"cuellos_botella": [{"eslabon": "Fabricación", "causa": "capacidad", "persistencia": "2–3 años",
                                                             "senal_resolucion": "plazos de entrega en descenso", "favorecidos": ["fabricantes con capacidad"],
                                                             "perjudicados": ["compradores sin contratos"], "perdedores_sistematicos": ["proveedores sin escala"],
                                                             "reflejo_en_tesis": "premisa 2"}],
                                       "vigilancia_tecnologica": [{"horizonte_anos": "2-5", "avance": "Mejoras de productividad en fabricación",
                                                                   "madurez": "piloto", "etiqueta": "[INTERPRETACIÓN]", "implicacion": "alivio parcial del cuello"}],
                                       "efectos_segundo_orden": [{"pregunta": "¿Quién suministra materiales y equipos?",
                                                                  "respuesta": "Proveedores de insumos críticos, fuera del ámbito por delimitación.",
                                                                  "etiqueta": "[INTERPRETACIÓN]", "invertible": True}],
                                       "actores_emergentes": [{"actor": "Fabricante emergente (sin identificar en el modo simulado)", "eslabon": "Fabricación",
                                                               "tipo": "emergente", "invertibilidad": "privado_sin_salida", "evidencia": "anuncios de capacidad"}]},
            "steelman": "La tesis contraria sostiene que el ciclo de pedidos ya ha tocado techo y que la capacidad nueva llegará antes.",
            "lo_que_no_sabemos": ["Ritmo real de la capacidad nueva", "Elasticidad de la demanda a los precios"],
            "pre_mortem": "Si la tesis falla será por una pausa de la demanda coincidente con capacidad nueva."}


def _respuestas_objeciones(msg, ctx, r):
    out = {}
    for o in msg.get("objeciones") or []:
        res = o.get("fuerza") != "fuerte" or r.random() < 0.8
        out[o["obj_id"]] = {"respuesta": "Respondida con la evidencia y los cálculos del análisis; se refleja en premisas y escenarios.",
                            "resuelta": bool(res)}
    return {"respuestas": out}


def _sintesis(msg, ctx, r):
    v = msg.get("veredicto_provisional", "VIGILAR")
    return {"condiciones_entrada": ["Valoración relativa por debajo del percentil 90 de su historia"],
            "tramos": [{"tramo": 1, "condicion": "Inmediato si se mantienen las condiciones de entrada", "horizonte": msg.get("horizonte", "H3"), "peso_orientativo": "un tercio"},
                       {"tramo": 2, "condicion": "Tras el próximo catalizador fechado si la cartera de pedidos sigue creciendo", "horizonte": msg.get("horizonte", "H3"), "peso_orientativo": "un tercio"},
                       {"tramo": 3, "condicion": "Si la valoración relativa vuelve a su mediana", "horizonte": msg.get("horizonte", "H3"), "peso_orientativo": "un tercio"}],
            "cancelacion_tramos": "Cancelar los tramos pendientes si se cumple una condición de invalidación.",
            "disparadores": [{"disparador": "Mejora de la rentabilidad relativa a 3 meses por encima de su banda", "fecha_esperada": "próxima revisión trimestral"},
                             {"disparador": "Resolución de la discrepancia principal", "fecha_esperada": "próximos resultados"}],
            "motivo_descarte": "sin tesis defendible" if v == "DESCARTAR" else None,
            "que_cambiaria_la_conclusion": ["Caída de la demanda dos trimestres seguidos", "Capacidad nueva anunciada > 25 % del mercado"],
            "riesgos": [{"riesgo": "Pausa de la demanda", "mecanismo": "menos pedidos nuevos", "senal_temprana": "cartera de pedidos"},
                        {"riesgo": "Capacidad nueva", "mecanismo": "presión en precios", "senal_temprana": "anuncios de plantas"},
                        {"riesgo": "Subida de tipos reales", "mecanismo": "compresión del múltiplo", "senal_temprana": "tipo real a 10 años"}],
            "catalizadores": [{"evento": "Próximos resultados trimestrales del ámbito", "fecha": "próximo trimestre"}],
            "invalidacion": ["Rentabilidad relativa a 3 meses por debajo del umbral de invalidación", "Caída de la demanda dos trimestres seguidos"],
            "mapa_cobertura": {"directas": ["Candidatos prioritarios del ámbito"], "indirectas": ["Proveedores de insumos críticos"],
                               "perdedores_sistematicos": [{"objeto": "Compradores sin contratos de suministro", "mecanismo": "retrasos y sobrecostes"}],
                               "investigado": ["eslabones del plan", "tipos de activo aplicables"],
                               "excluido_con_motivo": [{"objeto": "Tipos de activo no aplicables", "motivo": "sin exposición material"}],
                               "vigilancia_informativa": [], "vigilancia_pre_salida": []},
            "respuestas_preguntas": [{"pregunta": q, "origen": "BLOQUE_A" if i else "BROKER",
                                      "respuesta": "Respondida en las dimensiones y en la selección del informe técnico.", "referencias": []}
                                     for i, q in enumerate(msg.get("preguntas") or [])],
            "preguntas_sugeridas": ["¿Cómo cambiaría el ranking con márgenes menores?", "¿Qué señal adelantaría la capacidad nueva?"],
            "reversibilidad": "media"}


def _subsanacion(msg, ctx, r):
    return {"correcciones": [{"hallazgo": h.get("id"), "accion": "corregido en el paquete de síntesis"} for h in msg.get("hallazgos") or []],
            "resuelto": True}


# ------------------------------------------------------------------------------------------- Otros agentes
def _seleccion(msg, ctx, r):
    cands = msg.get("finalistas") or []
    return {"traduccion_rasgos_metricas": [{"rasgo": x, "metricas": ["pureza"] if "pureza" in x else ["deuda_neta_ebitda"] if "balance" in x else ["per_relativo"],
                                            "componente": "PE" if "pureza" in x else "QL" if "balance" in x else "VA"}
                                           for x in (msg.get("rasgos") or ["alta pureza de exposición"])],
            "candidatos": {c["cand_id"]: {"rol_en_tesis": f"Captura la tesis por su exposición al ámbito ({c.get('subcluster') or 'núcleo'}).",
                                          "preguntas_para_C": ["¿Qué margen implica el precio frente al margen normalizado?",
                                                               "¿Qué parte de la cartera de pedidos tiene precio revisable?"],
                                          "supuestos_a_verificar": ["Pureza estimada a partir de segmentos publicados"],
                                          "riesgos_especificos": ["Ejecución de proyectos", "Coste de insumos no repercutido"],
                                          "invalidacion": ["Caída de su cartera de pedidos dos trimestres seguidos"]} for c in cands},
            "respuestas_objeciones": {o["obj_id"]: {"respuesta": "La métrica de pureza ya descuenta ese segmento.", "resuelta": True}
                                      for o in msg.get("objeciones") or []},
            "asignacion_eslabones": _asignar(msg),
            "consultas_propuestas": ([{"pregunta": "¿Admite bonos sin calificación crediticia pública en la selección de renta fija?",
                                       "tipo": "PREFERENCIA_O_CRITERIO", "por_que_importa": "Cambia el universo invertible de RF",
                                       "supuesto_si_no_hay_respuesta": "Solo bonos con calificación pública",
                                       "efecto_si_supuesto_falso": "Se omitirían emisiones sin calificación", "bloqueante": False}]
                                     if msg.get("tipo_activo") == "RF" else [])}


def _asignar(msg):
    esl = [e for e in msg.get("eslabones") or [] if e.get("nivel") != "insumo"]
    es = [e for e in esl if e.get("papel") == "ES"] or esl
    out = {}
    for c in msg.get("candidatos_para_eslabon") or []:
        if not es:
            break
        k = int(hashlib.sha256(str(c.get("subcluster") or c["cand_id"]).encode()).hexdigest(), 16) % len(es)
        pur = c.get("pureza") if isinstance(c.get("pureza"), (int, float)) else 0.5
        out[c["cand_id"]] = {"eslabon_id": es[k]["eslabon_id"], "pureza_eslabon": round(min(1.0, 0.9 * pur), 2),
                             "rol_en_eslabon": f"Exposición a {es[k]['nombre'][:40]} ({c.get('subcluster') or 'núcleo'})"}
    return out


def _prospectiva(msg, ctx, r):
    esc = msg.get("escenarios_motor") or {}
    p10, p50, p90 = esc.get("p10", -0.1), esc.get("p50", 0.02), esc.get("p90", 0.12)
    return {"escenarios": [{"nombre": "base", "premisas": "Continuidad de la demanda y de la oferta del plan", "regimen": "régimen vigente",
                            "disparadores": ["resultados trimestrales"], "resultado_vs_referencia": f"Rentabilidad relativa mediana {p50:+.1%}"},
                           {"nombre": "favorable", "premisas": "Aceleración de la demanda y precios al alza", "regimen": "régimen vigente",
                            "disparadores": ["nuevos contratos"], "resultado_vs_referencia": f"Rentabilidad relativa {p90:+.1%} (p90)"},
                           {"nombre": "adverso", "premisas": "Pausa de la demanda y capacidad nueva", "regimen": "transición",
                            "disparadores": ["caída de pedidos"], "resultado_vs_referencia": f"Rentabilidad relativa {p10:+.1%} (p10)"}],
            "proyecciones": {"activada": msg.get("proyectable", True), "motivo_exclusion": None if msg.get("proyectable", True) else "objeto sin premisas proyectables",
                             "etapas": [{"etapa": "1. Mercado", "contenido": "Demanda del ámbito por segmento"},
                                        {"etapa": "2. Agregado del ámbito", "contenido": "Ingresos = volumen × precio"},
                                        {"etapa": "3. Márgenes y caja", "contenido": "Margen normalizado del ciclo"},
                                        {"etapa": "4. Valor implícito", "contenido": "Múltiplos de salida de comparables"},
                                        {"etapa": "5. Contraste con el precio", "contenido": "DCF inverso del agregado"}],
                             "premisas": [{"premisa": "Crecimiento de la demanda", "valor": "rango del escenario base", "fuente": "escenarios del Motor",
                                           "sensibilidad": "alta", "invalidacion": "caída dos trimestres"}],
                             "brecha_expectativas": "El precio descuenta un crecimiento algo superior al del escenario base."}}


def _refutacion(msg, ctx, r):
    objs = [{"objeto": "TESIS", "tipo": "explicación alternativa", "fuerza": "moderada",
             "argumento": "El aumento de la demanda puede ser cíclico y no estructural.", "que_la_resolveria": "peso de contratos plurianuales"},
            {"objeto": "TESIS", "tipo": "riesgo omitido", "fuerza": "debil",
             "argumento": "La regulación podría retrasar inversiones.", "que_la_resolveria": "calendario regulatorio"}]
    fin = msg.get("finalistas") or []
    if fin:
        objs.append({"objeto": fin[0]["cand_id"], "tipo": "pureza", "fuerza": "moderada",
                     "argumento": "Parte de sus ingresos procede de segmentos ajenos al ámbito.", "que_la_resolveria": "segmentos publicados"})
    return {"objeciones": objs, "veredicto_tesis": "robusta",
            "veredicto_candidatos": {c["cand_id"]: "robusto" for c in fin[:5]}}


def _ingesta(msg, ctx, r):
    return {"piezas": [{"ref": p.get("ref"), "etiqueta_verificada": p.get("etiqueta"), "independiente": True, "discrepancia": None}
                       for p in msg.get("piezas") or []]}


def _conocimiento(msg, ctx, r):
    refs = msg.get("referencias_candidatas") or []
    return {"referencias": [{"ref_id": x.get("ref_id"), "motivo": "pertinente para la pregunta"} for x in refs[:3]],
            "sintesis": "Referencias de método seleccionadas del archivo vivo por calidad.", "lagunas": [], "requiere_credencial": None}


def _mantenimiento(msg, ctx, r):
    return {"decisiones": [{"id": x.get("id"), "accion": x.get("accion", "NINGUNA")} for x in msg.get("resultados") or []],
            "novedades": [], "lagunas": []}


def _supuestos(msg, ctx, r):
    return {"supuestos": ["Bootstrap de bloques de 21 sesiones sobre tres años", "Ruido del 10 % de la dispersión transversal"],
            "advertencias": ["Sin validación fuera de muestra en el modo simulado"]}


def _redaccion(msg, ctx, r):
    v = msg.get("veredicto", "VIGILAR")
    llano = msg.get("nombre_llano", "este mercado")
    f3 = {"INVERTIR": "La idea nos parece buena ahora.", "INVERTIR_ESCALONADO": "La idea es buena, pero mejor entrar poco a poco.",
          "VIGILAR": "Por ahora conviene mirar y esperar.", "DESCARTAR": "Por ahora no vemos una buena idea."}[v]
    return {"frases_30s": [f"Hemos estudiado {llano[0].lower() + llano[1:]}.", "Miramos quién gana, quién pierde y cuánto cuesta.", f3],
            "semaforo_explicacion": {"INVERTIR": "Los datos apoyan la idea.", "INVERTIR_ESCALONADO": "Conviene repartir la entrada en el tiempo.",
                                     "VIGILAR": "Falta una señal clara.", "DESCARTAR": "No hay una idea sólida."}[v],
            "por_que": "Hay más demanda que oferta y la oferta tarda en crecer.",
            "riesgo_texto": "Su precio puede bajar bastante en un mal año.", "horizonte_texto": "Es una idea para varios meses o años.",
            "conviccion_texto": "Los datos son buenos, pero hay dudas abiertas.",
            "riesgos_llanos": ["La demanda podría frenar.", "Nuevas fábricas podrían bajar los precios.",
                               "Si sube el precio del dinero, estas inversiones valdrían menos."],
            "siguiente_paso_llano": "Tu Broker decide si pide un estudio a fondo. Nosotros vigilamos las señales y te avisamos si cambian.",
            "glosario": [{"termino": "Riesgo", "definicion": "Lo que puede bajar el precio en un mal año."},
                         {"termino": "Fondo", "definicion": "Cesta con muchas empresas que compras de una vez."}],
            "tesis_3_frases": ["La demanda del ámbito crece más que la oferta.", "Quien tiene capacidad gana precio y margen.",
                               "El precio ya descuenta parte de esa ventaja."]}


def _auditoria(msg, ctx, r):
    hall = []
    if msg.get("vuelta", 1) == 1 and r.random() < 0.25:
        hall.append({"id": "AUD-H-1", "severidad": "Operativa", "foco": "trazabilidad",
                     "descripcion": "Una nota dimensional cita datos genéricos; conviene precisar la serie.",
                     "correccion_propuesta": "Citar la DAT-B concreta."})
    return {"hallazgos": hall, "recomendacion": "AUTORIZAR"}


def _dictamen(msg, ctx, r):
    return {"dictamen_comentado": "Revisadas las comprobaciones G3 fallidas; se devuelven al Director.", "acciones": []}


def _lecciones(msg, ctx, r):
    return {"lecciones": [{"ambito": "general", "observacion": "Resultados resueltos registrados en F4.",
                           "recomendacion": "Mantener la disciplina de bandas sin certificado.", "fuerza": "anecdotica"}]}


def _interpretacion(msg, ctx, r):
    return {"interpretacion": "La señal ha cruzado su umbral; puede ser fluctuación o el inicio de un cambio de régimen.",
            "accion_sugerida": "CONSULTA_N0" if msg.get("clasificacion") == "REVISION" else "NUEVA_PETICION_SUGERIDA"}


# ------------------------------------------------------------------------------------------- V2.1 · capas, cadena y emergentes
def _viabilidad(msg, ctx, r):
    m = msg.get("metricas_indicador") or {}
    return {"tesis_basica": "La demanda del ámbito crece más que la oferta disponible a medio plazo.",
            "ya_descontado": bool((m.get("momento_12_1") or 0) > 0.6), "sin_mecanismo": False, "alerta_integridad": False,
            "materialidad": "suficiente según el universo preliminar", "emergentes_materiales": True}


def _integracion_provisional(msg, ctx, r):
    base = _integracion(msg, ctx, r)
    return {"tesis": base["tesis"], "componentes_A": base["componentes_A"], "componentes_E": base["componentes_E"],
            "tesis_viva": True, "fuentes_para_cerrar_E": True, "saturacion_narrativa": False,
            "autorrefutacion": "La tesis sobrevive a la autorrefutación: el contraargumento cíclico no explica la cartera plurianual."}


_INDICADORES = [
    [{"indicador": "utilizacion", "valor": 0.93}, {"indicador": "book_to_bill", "valor": 1.25}, {"indicador": "plazo_entrega_ratio", "valor": 1.7}],
    [{"indicador": "utilizacion", "valor": 0.88}, {"indicador": "plazo_entrega_ratio", "valor": 1.6}, {"indicador": "hhi_proveedores", "valor": 2000}],
]


def _desglose_cadena(msg, ctx, r):
    out = []
    n_es = 0
    for i, c in enumerate(msg.get("mapa_preliminar") or [], start=1):
        papel = str(c.get("papel_del_ambito") or "es").upper()
        es = papel == "ES"
        ind = _INDICADORES[n_es] if es and n_es < len(_INDICADORES) else [{"indicador": "spot_contrato", "valor": 1.05}]
        comp = {"crecimiento": 80 if es else 50, "margen_roic": 70 if es else 40, "poder_negociacion": 70 if es else 50,
                "expectativas_inv": 50, "sustitucion_inv": 70 if es else 60}
        if es and n_es == 1:
            comp.update({"crecimiento": 60, "margen_roic": 50, "poder_negociacion": 50})
        out.append({"eslabon_id": f"ESL-{i:02d}", "padre": None, "nombre": c.get("eslabon"), "nivel": "macro",
                    "descripcion": f"Eslabón «{c.get('eslabon')}» del mapa preliminar.", "papel_ambito": papel,
                    "metricas": {"crecimiento_anual": 0.12 if es else 0.04, "poder_negociacion": "ALTO" if es else "MEDIO"},
                    "indicadores_cuello": ind, "persistencia_meses": 30 if (es and n_es == 0) else 18 if es else 3,
                    "relevancia_valor": 4 if (es and n_es == 0) else 3 if es else 1, "causa": "capacidad",
                    "senal_resolucion": "Plazos de entrega en descenso y book-to-bill por debajo de 1", "componentes_AE": comp})
        if es:
            n_es += 1
    crit = next((e["eslabon_id"] for e in out if e["papel_ambito"] == "ES"), out[0]["eslabon_id"] if out else None)
    return {"eslabones": out, "eslabon_critico": crit}


def _radar_emergentes(msg, ctx, r):
    esl = [e for e in msg.get("eslabones") or [] if e.get("papel") == "ES"] or (msg.get("eslabones") or [])[:1]
    univ = msg.get("universo_cotizado") or []
    out = []
    for k, e in enumerate(esl[:3]):
        out.append({"eslabon_id": e["eslabon_id"], "nombre": f"Startup de sensórica para «{e['nombre']}» (simulada)", "tipo": "STARTUP",
                    "financiacion_conocida": {"importe": 8.0 + k, "divisa": "EUR", "ultima_ronda": "Serie A", "fecha": None, "fuente": None},
                    "tecnologia_o_ventaja": "Monitorización y mantenimiento predictivo", "senales_traccion": ["pilotos con clientes anunciados"],
                    "via_exposicion": "NO_INVERTIBLE_HOY", "instrumento_exposicion": {},
                    "criterios": {"tecnologia": 70, "traccion": 50, "equipo": 60, "financiacion": 50, "posicion_cadena": 60, "via_exposicion": 0},
                    "riesgos": ["Financiación", "Ejecución"], "etiqueta": "[INTERPRETACIÓN]"})
    reciente = next((f for f in univ if str(f.get("salida_bolsa_reciente") or "").lower() in ("si", "sí", "true", "1")), None)
    cand = reciente or (sorted([f for f in univ if f.get("tipo") == "RV"], key=lambda f: float(f.get("capitalizacion_meur") or 1e12))[:1] or [None])[0]
    if cand and esl:
        out.append({"eslabon_id": esl[0]["eslabon_id"], "nombre": f"{cand['nombre']} (menor capitalización del eslabón)",
                    "tipo": "SALIDA_A_BOLSA_RECIENTE" if reciente else "SCALE_UP",
                    "financiacion_conocida": None, "tecnologia_o_ventaja": "Capacidad nueva en el eslabón crítico",
                    "senales_traccion": ["contratos nuevos publicados"], "via_exposicion": "COTIZADA_DIRECTA",
                    "instrumento_exposicion": {"nombre": cand["nombre"], "isin": cand.get("isin"), "id_universo": cand["id"]},
                    "criterios": {"tecnologia": 60, "traccion": 70, "equipo": 60, "financiacion": 60, "posicion_cadena": 70, "via_exposicion": 100},
                    "riesgos": ["Liquidez", "Concentración de clientes"], "etiqueta": "[INTERPRETACIÓN]"})
    return {"radar_emergentes": out}


def _paquete_parada(msg, ctx, r):
    elim = any(m.get("clase") == "ELIMINATORIO" for m in msg.get("motivos") or [])
    return {"que_lo_cambiaria": ["Aparición de instrumentos invertibles que superen PC1" if elim else "Una mejora material de la evidencia o de la valoración",
                                 "Un catalizador fechado que haga material la tesis"],
            "sugerencia": "DESCARTAR" if elim else "PONER_EN_SEGUIMIENTO",
            "seguimiento_propuesto": {"frecuencia": "MENSUAL", "senales_de_interes": ["rentabilidad relativa del indicador del ámbito"],
                                      "disparadores": ["valoración relativa por debajo de su mediana"]},
            "lo_que_ya_se_sabe": ["Ámbito delimitado y universo preliminar construido", "Lectura rápida de la valoración del indicador"]}


def _informe_parada(msg, ctx, r):
    i = msg.get("informe") or {}
    return {"resumen": f"El análisis se detuvo en {i.get('puerta')}: con lo verificado no merece seguir gastando tiempo ahora."}


def _ciclo_seguimiento(msg, ctx, r):
    return {"que_ha_cambiado": [{"dimension": d, "antes": "lectura del ciclo anterior", "ahora": "sin cambio material", "importancia": "BAJA"}
                                for d in (msg.get("dimensiones_clave") or ["D9"])[:2]],
            "disparadores": [{"descripcion": d.get("descripcion") if isinstance(d, dict) else str(d), "estado": "NO_ALCANZADO"}
                             for d in msg.get("disparadores_broker") or []],
            "autorrefutacion": "El cambio de semáforo se contrasta con la fluctuación normal del indicador.",
            "resumen": "Ciclo ligero: delta de las dimensiones clave y de las señales frente al ciclo anterior."}


def _informe_seguimiento(msg, ctx, r):
    return {"resumen": "Resumen breve del ciclo para el Broker; sin afirmaciones nuevas."}


_TAREAS = {
    ("AG-B01", "admision"): _admision, ("AG-B01", "justificacion_tiempo"): _justificacion, ("AG-B01", "consulta"): _consulta,
    ("AG-B02", "plan"): _plan, ("AG-B02", "cobertura_dimensiones"): _informe_dimensional, ("AG-B02", "integracion"): _integracion,
    ("AG-B02", "respuestas_objeciones"): _respuestas_objeciones, ("AG-B02", "sintesis"): _sintesis,
    ("AG-B02", "subsanacion"): _subsanacion, ("AG-B03", "reconocimiento"): _reconocimiento,
    ("*", "informe_dimensional"): _informe_dimensional, ("AG-B12", "seleccion"): _seleccion,
    ("AG-B12", "respuestas_objeciones"): _seleccion, ("AG-B13", "prospectiva"): _prospectiva,
    ("AG-B14", "refutacion"): _refutacion, ("AG-B15", "ingesta"): _ingesta, ("AG-B16", "supuestos_calculo"): _supuestos,
    ("AG-B17", "redaccion"): _redaccion, ("*", "conocimiento"): _conocimiento, ("*", "mantenimiento"): _mantenimiento,
    ("AG-B21", "dictamen_g3"): _dictamen, ("AG-B22", "auditoria"): _auditoria, ("AG-B23", "lecciones"): _lecciones,
    ("AG-B23", "interpretacion_alerta"): _interpretacion,
    ("AG-B02", "viabilidad"): _viabilidad, ("AG-B02", "integracion_provisional"): _integracion_provisional,
    ("AG-B03", "desglose_cadena"): _desglose_cadena, ("AG-B24", "radar_emergentes"): _radar_emergentes,
    ("AG-B02", "paquete_parada"): _paquete_parada, ("AG-B17", "informe_parada"): _informe_parada,
    ("AG-B02", "ciclo_seguimiento"): _ciclo_seguimiento, ("AG-B17", "informe_seguimiento"): _informe_seguimiento,
}
