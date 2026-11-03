"""Seguimientos periódicos encargados por el Broker (CT-B-29, 7.13; R5, R35) y archivo F11 «Registro de seguimientos
encargados» (propietario AG-B01).

- `alta`, `modificar`, `pausar`, `reanudar` y `cancelar` (en cualquier momento) gestionan el encargo SEG-B en F11.
- `ciclo` ejecuta un ciclo ligero N1-SEG (objetivo < 10 min, PT30 aplicable): delta de las dimensiones clave y de las
  señales, disparadores del Broker y del plan, candidatos entregados, alertas del Vigía del periodo, semáforo con
  autorrefutación, recomendación (MANTENER_VIGILANCIA | REACTIVAR_ANALISIS_PROFUNDO | PROPONER_PASAR_A_C |
  CANCELAR_SEGUIMIENTO), informe de seguimiento (Markdown breve + JSON B.14) con G3 perfil CIC, actualización de la
  Biblioteca F6 con lo verificado y registro del ciclo CIC-B en F11 y del consumo en F1.
- `pendientes` ejecuta los ciclos vencidos según la agenda de HT-05 (frecuencia de cada SEG-B).

Distinto del Vigía (vigia.py, fase F11, R32): el Vigía es automático sobre las REC-B entregadas y solo genera
alertas; un ciclo de seguimiento lo ha pedido el Broker y es un análisis ligero. Un ciclo nunca inicia un análisis
profundo: reactivarlo exige una petición nueva (R35)."""
from __future__ import annotations

import datetime as dt
import json
import random
from typing import Dict, List, Optional

from .contratos import MensajeRechazado, comprobar_sensibles, controlado, sanear
from .herramientas import ht08, ht09
from .vigia import clasificar, valor_senal

FRECUENCIAS = ("DIARIA", "SEMANAL", "QUINCENAL", "MENSUAL", "TRIMESTRAL", "PERSONALIZADA")
ACCIONES = ("ALTA", "MODIFICACION", "PAUSA", "REANUDACION", "CANCELACION")
DIAS_VIGIA = {"diaria": 1, "cada_2_dias_habiles": 2, "semanal": 7, "mensual": 30, "trimestral": 91}


def _cfg(ent) -> Dict:
    return ent.cfg.get("seguimientos") or {}


def _dias(ent, frec: Dict) -> int:
    if frec.get("tipo") == "PERSONALIZADA":
        return max(1, int(frec.get("cada_dias") or 1))
    return int((_cfg(ent).get("dias_frecuencia") or {}).get(frec.get("tipo"), 30))


def _mas(fecha: str, dias: int) -> str:
    return (dt.date.fromisoformat(fecha) + dt.timedelta(days=dias)).isoformat()


def _seg(ent, seg_id: str) -> Dict:
    s = ent.alm.estado("F11", tipo="SEG").get(seg_id)
    if not s:
        raise KeyError(f"No existe el seguimiento {seg_id}")
    return s


def _escribir(ent, entrada: Dict) -> None:
    ent.alm.escribir("F11", "AG-B01", entrada)


def _evento_eval(ent, contenido: Dict) -> None:
    ent.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AVISO_EVALUADOR", "id": ent.alm.nuevo_id("AVE-B"), "tipo": "EVENTO_SEGUIMIENTO",
                                      "contenido": contenido})


def _resolver_objeto(ent, coord, obj: Dict) -> Dict:
    """Ámbito analizado (REC-B / MKT-B) o nuevo: devuelve rec, ficha F6, clave de universo, indicador y referencia."""
    rec = None
    if obj.get("rec_id"):
        rec = ent.alm.estado("F3").get(obj["rec_id"])
        if not rec:
            raise ValueError(f"REC-B {obj['rec_id']} inexistente en F3")
    fichas = ent.alm.leer("F6")
    ficha = None
    if rec:
        ficha = next((f for f in reversed(fichas) if f.get("pet_id") == rec.get("pet_id")), None)
    elif obj.get("mkt_id"):
        ficha = next((f for f in reversed(fichas) if f.get("id") == obj["mkt_id"]), None)
    clave = (ficha or {}).get("mkt_clave") or (obj.get("ambito") or {}).get("clave_universo") or obj.get("clave_universo")
    if clave and not ficha:
        ficha = next((f for f in reversed(fichas) if f.get("mkt_clave") == clave), None)
    if not clave:     # ámbito nuevo sin clave: el Director lo encuadra (capa 0)
        disp = {k: {kk: a.get(kk) for kk in ("nombre", "tipo_objeto", "tipos_activo", "horizonte")} for k, a in ent.ambitos.items()}
        r = ent.inv.llamar("AG-B02", "CT-B-08", "plan", {"objeto": {"descripcion": (obj.get("ambito") or {}).get("descripcion")},
                                                        "ambitos_disponibles": disp, "tipos_todos": [], "origen": "LIBRE"},
                           "Encuadra el ámbito del seguimiento encargado (capa 0).", {"clave_universo": "string"}, coord._ctx("AG-B02"))
        clave = r.get("clave_universo") if r.get("clave_universo") in ent.ambitos else next(iter(ent.ambitos))
    amb = ent.ambitos.get(clave) or {}
    ind = (rec or {}).get("indicador") or amb.get("indicador") or {}
    ref = (rec or {}).get("referencia") or amb.get("referencia") or ind
    return {"rec": rec, "ficha": ficha, "clave": clave, "ambito": amb, "indicador": ind, "referencia": ref}


# =============================================================================================================
# CT-B-29 · encargo (alta, modificación, pausa, reanudación, cancelación)
# =============================================================================================================
def encargo(ent, coord, datos: Dict) -> Dict:
    try:
        comprobar_sensibles(datos)
    except MensajeRechazado as e:
        ent.alm.incidencia("SEGURIDAD", f"Encargo de seguimiento rechazado íntegro: {e.tipo}", "AG-B01", severidad="Crítica")
        return {"seg_id": datos.get("seg_id"), "estado": "RECHAZADO", "motivo": str(e)}
    datos = sanear(datos)
    accion = datos.get("accion", "ALTA")
    if accion not in ACCIONES:
        raise ValueError(f"accion no válida: {accion}")
    if accion == "ALTA":
        return alta(ent, coord, datos)
    seg_id = datos.get("seg_id")
    s = _seg(ent, seg_id)
    if s.get("estado") in ("CANCELADO", "FINALIZADO"):
        return {"seg_id": seg_id, "estado": s["estado"], "motivo": "El seguimiento ya no está vigente"}
    if accion == "CANCELACION":
        _escribir(ent, {"tipo_entrada": "SEG", "id": seg_id, "estado": "CANCELADO", "accion": accion, "motivo": datos.get("motivo"),
                        "proximo_ciclo": None})
        _evento_eval(ent, {"seg_id": seg_id, "evento": "CANCELACION"})
        return {"seg_id": seg_id, "estado": "CANCELADO", "motivo": datos.get("motivo"),
                "nota": "Cancelación inmediata; un ciclo en curso se cierra en su siguiente punto de control sin informe (B.13)"}
    if accion == "PAUSA":
        _escribir(ent, {"tipo_entrada": "SEG", "id": seg_id, "estado": "PAUSADO", "accion": accion, "motivo": datos.get("motivo"),
                        "pausado_desde": ent.as_of})
        return {"seg_id": seg_id, "estado": "PAUSADO"}
    if accion == "REANUDACION":
        prox = _mas(ent.as_of, _dias(ent, s["frecuencia"]))
        _escribir(ent, {"tipo_entrada": "SEG", "id": seg_id, "estado": "ACTIVO", "accion": accion, "proximo_ciclo": prox, "pausado_desde": None})
        return {"seg_id": seg_id, "estado": "ACTIVO", "proximo_ciclo": prox}
    # MODIFICACION: solo los campos que cambian
    cambios = {k: datos[k] for k in ("frecuencia", "motivo", "senales_de_interes", "disparadores_broker", "dimensiones_clave",
                                     "candidatos_a_vigilar", "fecha_fin", "limite_ciclo") if k in datos}
    if "frecuencia" in cambios:
        _validar_frecuencia(cambios["frecuencia"])
        cambios["proximo_ciclo"] = _mas(ent.as_of, _dias(ent, cambios["frecuencia"]))
    _escribir(ent, {"tipo_entrada": "SEG", "id": seg_id, "accion": accion, **cambios})
    _evento_eval(ent, {"seg_id": seg_id, "evento": "MODIFICACION", "campos": sorted(cambios)})
    return {"seg_id": seg_id, "estado": s.get("estado"), "modificado": sorted(cambios), "proximo_ciclo": cambios.get("proximo_ciclo", s.get("proximo_ciclo"))}


def _validar_frecuencia(f: Dict) -> None:
    if not isinstance(f, dict) or f.get("tipo") not in FRECUENCIAS:
        raise ValueError("frecuencia.tipo debe ser DIARIA | SEMANAL | QUINCENAL | MENSUAL | TRIMESTRAL | PERSONALIZADA")
    if f["tipo"] == "PERSONALIZADA" and int(f.get("cada_dias") or 0) < 1:
        raise ValueError("Una frecuencia PERSONALIZADA exige cada_dias ≥ 1")


def alta(ent, coord, datos: Dict) -> Dict:
    obj = datos.get("objeto") or {}
    if obj.get("tipo") not in ("AMBITO_ANALIZADO", "AMBITO_NUEVO"):
        raise ValueError("objeto.tipo debe ser AMBITO_ANALIZADO o AMBITO_NUEVO")
    _validar_frecuencia(datos.get("frecuencia"))
    activos = [s for s in ent.alm.estado("F11", tipo="SEG").values() if s.get("estado") == "ACTIVO"]
    if len(activos) >= int(_cfg(ent).get("max_activos", 25)):
        return {"seg_id": None, "estado": "RECHAZADO", "motivo": f"Máximo de {_cfg(ent).get('max_activos', 25)} seguimientos activos (Anexo A)"}
    res = _resolver_objeto(ent, coord, obj)
    hz = datos.get("horizonte_principal") or (res["rec"] or {}).get("horizonte") or res["ambito"].get("horizonte", "H3")
    advert = []
    dias = _dias(ent, datos["frecuencia"])
    vig = DIAS_VIGIA.get(((ent.cfg.get("vigia") or {}).get("frecuencia") or {}).get(hz, "semanal"), 7)
    if dias < vig:
        advert.append(f"frecuencia superior a la del Vigía para el horizonte principal {hz} (aceptada con advertencia, 7.13)")
    if not datos.get("fecha_fin"):
        advert.append(f"sin fecha de fin: recordatorio de revisión al Broker cada {_cfg(ent).get('revision_sin_fecha_fin_meses', 6)} meses")
    linea_base = obj["tipo"] == "AMBITO_NUEVO" and not res["ficha"]
    seg_id = ent.alm.nuevo_id("SEG-B")
    prox = ent.as_of if linea_base else _mas(ent.as_of, dias)
    _escribir(ent, {"tipo_entrada": "SEG", "id": seg_id, "accion": "ALTA", "estado": "ACTIVO", "objeto": obj, "clave_universo": res["clave"],
                    "rec_id": obj.get("rec_id"), "mkt_id": (res["ficha"] or {}).get("id"), "frecuencia": datos["frecuencia"],
                    "motivo": datos.get("motivo"), "senales_de_interes": datos.get("senales_de_interes") or [],
                    "disparadores_broker": datos.get("disparadores_broker") or [], "dimensiones_clave": datos.get("dimensiones_clave") or ["D9", "D2"],
                    "candidatos_a_vigilar": datos.get("candidatos_a_vigilar") or [], "horizonte_principal": hz,
                    "fecha_fin": datos.get("fecha_fin"), "limite_ciclo": datos.get("limite_ciclo") or {"minutos": _cfg(ent).get("objetivo_ciclo_min", 10)},
                    "proximo_ciclo": prox, "linea_base_pendiente": linea_base, "ciclos": 0, "advertencias": advert, "alta": ent.as_of})
    if obj.get("rec_id"):
        ent.alm.escribir("F3", "AG-B23", {"tipo_entrada": "SEGUIMIENTO", "id": obj["rec_id"], "seguimientos": [seg_id]})
    _evento_eval(ent, {"seg_id": seg_id, "evento": "ALTA", "frecuencia": datos["frecuencia"]})
    est = {"minutos_p50": 6.0, "minutos_p80": 9.0, "uc_p80": float(_cfg(ent).get("uc_ciclo", 5))}
    return {"seg_id": seg_id, "estado": "ACTIVO", "motivo": datos.get("motivo"), "proximo_ciclo": prox, "estimacion_ciclo": est,
            "linea_base": {"necesaria": linea_base, "minutos_p80": float(_cfg(ent).get("linea_base_max_min", 20)) if linea_base else None},
            "advertencias": advert}


# =============================================================================================================
# Ciclo N1-SEG
# =============================================================================================================
def ciclo(ent, coord, seg_id: str) -> Dict:
    alm = ent.alm
    s = _seg(ent, seg_id)
    if s.get("estado") != "ACTIVO":
        return {"seg_id": seg_id, "estado": s.get("estado"), "nota": "Solo se ejecutan ciclos de seguimientos ACTIVOS (R35)"}
    if s.get("fecha_fin") and ent.as_of > s["fecha_fin"]:
        _escribir(ent, {"tipo_entrada": "SEG", "id": seg_id, "estado": "FINALIZADO", "proximo_ciclo": None})
        return {"seg_id": seg_id, "estado": "FINALIZADO"}
    curso = [c for c in alm.estado("F11", tipo="CIC").values() if c.get("seg_id") == seg_id and c.get("estado") == "EN_CURSO"]
    if curso:
        _escribir(ent, {"tipo_entrada": "CIC", "id": f"{curso[0]['id']}-omitido", "seg_id": seg_id, "estado": "CICLO_OMITIDO_SOLAPE"})
        return {"seg_id": seg_id, "estado": "CICLO_OMITIDO_SOLAPE"}
    n = int(s.get("ciclos") or 0) + 1
    num = seg_id[6:]
    ciclo_id, run_id = f"CIC-B-{num}-{n:02d}", f"RUN-B-{num}-c{n:02d}"
    linea_base = bool(s.get("linea_base_pendiente"))
    _escribir(ent, {"tipo_entrada": "CIC", "id": ciclo_id, "seg_id": seg_id, "run_id": run_id, "estado": "EN_CURSO", "linea_base": linea_base})
    alm.escribir("F1", "AG-B01", {"tipo_entrada": "EJECUCION", "id": run_id, "seg_id": seg_id, "ciclo_id": ciclo_id, "nivel": "N1-SEG",
                                  "as_of": ent.as_of})
    uc0 = ent.inv.uc_total + ent.motor.uc
    res = _resolver_objeto(ent, coord, s.get("objeto") or {})
    rec = res["rec"] or {}
    ind, ref = (res["indicador"] or {}).get("simbolo"), (res["referencia"] or {}).get("simbolo")
    previos = sorted([c for c in alm.estado("F11", tipo="CIC").values() if c.get("seg_id") == seg_id and c.get("estado") == "ENTREGADO"],
                     key=lambda c: c["id"])
    ultimo = previos[-1] if previos else None
    # Señales del plan de seguimiento de la REC-B y del Broker
    plan = rec.get("plan_de_seguimiento") or {}
    fecha_entrega = (rec.get("_historial") or [{}])[0].get("fecha") or ent.as_of
    senales = []
    for sg in plan.get("senales") or []:
        val = valor_senal(ent.prov, sg["serie"], fecha_entrega)
        cl = clasificar(val, sg, None) if val is not None else None
        senales.append({"sig_id": sg["sig_id"], "nombre": sg["nombre"], "valor": val,
                        "umbral": sg["umbral_revision"] if cl in (None, "FLUCTUACION", "REVISION") else sg["umbral_invalidacion"],
                        "estado": "ALCANZADO" if cl and cl.startswith("INVALIDACION") else "PROXIMO" if cl == "REVISION" else "NORMAL"})
    if ind and not senales:     # ámbito sin plan (nuevo o detenido en puerta): señal base del indicador frente a su referencia
        val = valor_senal(ent.prov, f"HT-01:REL:{ind}/{ref or ind}", ent.as_of)
        senales.append({"sig_id": f"SIG-{num}-00", "nombre": f"Rentabilidad relativa a 3 meses de {ind}", "valor": val, "umbral": None, "estado": "NORMAL"})
    mp = ent.motor.metricas_precio(ind, ref) if ind else {}
    # Delta de las dimensiones clave (Director) y disparadores del Broker
    d = ent.inv.llamar("AG-B02", "CT-B-08", "ciclo_seguimiento",
                       {"seg_id": seg_id, "ciclo_id": ciclo_id, "linea_base": linea_base, "dimensiones_clave": s.get("dimensiones_clave"),
                        "senales_de_interes": s.get("senales_de_interes"), "disparadores_broker": s.get("disparadores_broker"),
                        "metricas_indicador": mp, "senales": senales, "ultimo_ciclo": (ultimo or {}).get("resumen"),
                        "ficha_F6": (res["ficha"] or {}).get("id"), "veredicto_rec": rec.get("veredicto")},
                       "Ciclo N1-SEG (7.13): delta de las dimensiones clave (encarga rondas solo con valor informativo), estado de los "
                       "disparadores y autorrefutación del cambio de semáforo. No inicies análisis profundos.",
                       {"que_ha_cambiado": "array"}, coord._ctx("AG-B02"), run_id)
    cambios = [{"dimension": x.get("dimension"), "antes": str(x.get("antes")), "ahora": str(x.get("ahora")),
                "importancia": x.get("importancia") if x.get("importancia") in ("ALTA", "MEDIA", "BAJA") else "BAJA",
                "evidencia": [str(e) for e in x.get("evidencia") or []]}
               for x in d.get("que_ha_cambiado") or [] if isinstance(x, dict) and x.get("dimension")]
    disp_d = {str(x.get("descripcion")): x.get("estado") for x in d.get("disparadores") or [] if isinstance(x, dict)}
    disparadores = [{"descripcion": (x.get("descripcion") if isinstance(x, dict) else str(x)), "origen": "BROKER",
                     "estado": disp_d.get(x.get("descripcion") if isinstance(x, dict) else str(x)) if disp_d.get(
                         x.get("descripcion") if isinstance(x, dict) else str(x)) in ("NO_ALCANZADO", "PROXIMO", "ALCANZADO") else "NO_ALCANZADO"}
                    for x in s.get("disparadores_broker") or []]
    disparadores += [{"descripcion": c, "origen": "PLAN", "estado": "NO_ALCANZADO"} for c in (plan.get("condiciones_invalidacion_ambito") or [])[:2]]
    # Candidatos entregados y alertas del Vigía del periodo
    cands = []
    for cid, c in ent.alm.estado("F3").items():
        if str(cid).startswith("CAND-B-") and c.get("rec_id") == rec.get("id") and (c.get("en_top_n") or c.get("en_tabla_eslabon")):
            est = {"VIGENTE": "VIGENTE", "ALERTA": "ALERTA", "INVALIDADO": "INVALIDADO"}.get(c.get("estado_vigilancia"), "VIGENTE")
            cands.append({"cand_id": cid, "eslabon_id": c.get("eslabon_id") or "ESL-00", "cambio": "sin cambio material", "estado": est,
                          "veredicto": c.get("veredicto")})
    desde = (ultimo or {}).get("_ultima_fecha") or fecha_entrega
    alertas = [e.get("alr_id") for e in ent.alm.leer("F3") if e.get("tipo_entrada") == "ALERTA" and e.get("id") == rec.get("id")
               and e.get("alr_id") and e["_fecha"] >= desde]
    # Semáforo (autorrefutación declarada) y recomendación
    if any(x["estado"] == "ALCANZADO" for x in senales + disparadores):
        semaforo = "ROJO"
    elif any(x["estado"] == "PROXIMO" for x in senales + disparadores) or any(x["importancia"] == "ALTA" for x in cambios) or alertas:
        semaforo = "AMBAR"
    else:
        semaforo = "VERDE"
    verdes = 0
    for c in reversed(previos):
        if c.get("semaforo") != "VERDE":
            break
        verdes += 1
    peticion, prop_c = None, []
    rel = mp.get("momento_12_1")
    if semaforo == "ROJO":
        recom, motivo = "REACTIVAR_ANALISIS_PROFUNDO", "Disparador o umbral de invalidación alcanzado: la tesis está en riesgo"
        peticion = {"nivel": "N2", "alcance": f"Reanálisis de {(rec.get('ambito') or {}).get('nombre') or res['ambito'].get('nombre')}",
                    "estimacion_min_p80": 28}
    elif semaforo == "VERDE" and verdes + 1 >= int(_cfg(ent).get("ciclos_verdes_para_cancelar", 6)):
        recom, motivo = "CANCELAR_SEGUIMIENTO", f"{verdes + 1} ciclos seguidos sin novedad: el seguimiento ya no aporta (propuesta al Broker)"
    elif semaforo == "VERDE" and rec.get("veredicto") in ("INVERTIR", "INVERTIR_ESCALONADO") and isinstance(rel, (int, float)) and rel > 0.10 \
            and any(c["veredicto"] == "PRIORITARIO_PARA_C" and c["estado"] == "VIGENTE" for c in cands):
        recom, motivo = "PROPONER_PASAR_A_C", "Tesis reforzada y candidatos prioritarios vigentes"
        prop_c = [c["cand_id"] for c in cands if c["veredicto"] == "PRIORITARIO_PARA_C" and c["estado"] == "VIGENTE"]
    else:
        recom, motivo = "MANTENER_VIGILANCIA", ("Señal próxima a su umbral o cambio material: se mantiene la vigilancia" if semaforo == "AMBAR"
                                                else "Sin cambio material desde el ciclo anterior")
    if linea_base:
        motivo = "Línea base del ámbito nuevo (capas 0 y 1): señales y disparadores fijados para los próximos ciclos. " + motivo
    prox = _mas(ent.as_of, _dias(ent, s["frecuencia"]))
    # Tiempo: real o simulado (p50 de un ciclo × factor × ruido con semilla)
    rc = ent.cfg.get("reloj") or {}
    minutos = round((12.0 if linea_base else 6.0) * float(rc.get("factor_simulado", 1.0))
                    * (1 + 0.1 * random.Random(f"{ciclo_id}").uniform(-1, 1)), 1)
    uc = round(ent.inv.uc_total + ent.motor.uc - uc0, 2)
    mkt = (res["ficha"] or {}).get("id") or (rec.get("pet_id") or "").replace("PET-B-", "MKT-B-") or f"MKT-B-{num}"
    inf = {"seg_id": seg_id, "ciclo_id": ciclo_id, "run_id": run_id, "fecha": ent.as_of, "data_cutoff": ent.as_of,
           "objeto": {"rec_id": rec.get("id"), "mkt_id": mkt, "ambito": (rec.get("ambito") or {}).get("nombre") or res["ambito"].get("nombre")},
           "semaforo": semaforo, "resumen": d.get("resumen") or "Ciclo ligero de seguimiento encargado.",
           "que_ha_cambiado": cambios, "senales": senales, "disparadores": disparadores, "candidatos": [{k: v for k, v in c.items() if k != "veredicto"} for c in cands],
           "alertas_vigia_incluidas": alertas, "actualizacion_F6": {"mkt_id": mkt, "version": f"c{n:02d}", "dimensiones": s.get("dimensiones_clave") or []},
           "recomendacion": recom, "motivo": motivo, "peticion_sugerida": peticion, "candidatos_propuestos_para_C": prop_c,
           "proximo_ciclo": prox if recom != "CANCELAR_SEGUIMIENTO" else prox,
           "tiempo_consumo": {"minutos": minutos, "uc": uc, "estimado_p80_min": 9.0 if not linea_base else 20.0, "autorizaciones": []},
           "supuestos_aplicados": [], "limitaciones": ["Datos sintéticos: resultados sin valor analítico"] if ent.prov.nombre == "sintetico" else [],
           "autorrefutacion": d.get("autorrefutacion"), "nota": "El bloque no ha iniciado ningún análisis profundo."}
    red = ent.inv.llamar("AG-B17", "CT-B-20", "informe_seguimiento", {"seg_id": seg_id, "informe": inf},
                         "Redacta el resumen breve del informe de seguimiento (una página) sin añadir afirmaciones.", {"resumen": "string"},
                         coord._ctx("AG-B17"), run_id)
    from . import redaccion
    md = redaccion.informe_seguimiento_md(inf, red.get("resumen"))
    g3 = ht09.validar_informe_seguimiento(inf, md, seg_activo=True)
    alm.escribir("HA", "AG-B21", {"tipo_entrada": "G3V", "id": alm.nuevo_id("G3V-B"), "seg_id": seg_id, "run_id": run_id, "pasada": "CIC",
                                  "dictamen": g3["dictamen"], "resumen": g3["resumen"], "motivo": g3["motivo"]})
    if g3["dictamen"] == "BLOQUEADO":
        _escribir(ent, {"tipo_entrada": "CIC", "id": ciclo_id, "seg_id": seg_id, "estado": "BLOQUEADO", "motivo": g3["motivo"]})
        return {"seg_id": seg_id, "ciclo_id": ciclo_id, "estado": "BLOQUEADO", "motivo": g3["motivo"]}
    mu = float(((ent.cfg.get("auditoria") or {}).get("muestreo") or {}).get("N1-SEG", 0.2))
    if random.Random(f"{ciclo_id}|auditoria").random() < mu and ent.modo != "backtest":
        a = ent.inv.llamar("AG-B22", "CT-B-19", "auditoria", {"seg_id": seg_id, "vuelta": 1, "nivel": "N1-SEG", "informe_seguimiento": inf},
                           "Audita el informe de seguimiento (muestreo, 7.13).", {"hallazgos": "array", "recomendacion": "string"}, coord._ctx("AG-B22"), run_id)
        for h in [h for h in (a.get("hallazgos") or []) if isinstance(h, dict)]:
            alm.escribir("HA", "AG-B21", {"tipo_entrada": "AUD", "id": alm.nuevo_id("AUD-B"), "seg_id": seg_id, "vuelta": 1,
                                          "severidad": controlado(h.get("severidad"), "severidad", "Operativa"), "descripcion": h.get("descripcion")})
    auts = alm.nuevo_id("AUTS-B")
    alm.escribir("HA", "AG-B21", {"tipo_entrada": "AUTORIZACION_SALIDA", "id": auts, "seg_id": seg_id, "dictamen_g3": g3["dictamen"], "tipo": "INFORME_SEGUIMIENTO"})
    rutas = redaccion.escribir_informe_seguimiento(ent.salida, inf, md)
    # Biblioteca F6 con lo verificado (5.2, regla 2) y registro del ciclo (F11) y del consumo (F1)
    alm.escribir("F6", "AG-B02", {"tipo_entrada": "MKT", "id": mkt, "mkt_clave": res["clave"], "pet_id": rec.get("pet_id"),
                                  "ambito": rec.get("ambito") or {"nombre": res["ambito"].get("nombre")}, "veredicto": rec.get("veredicto"),
                                  "actualizado_por_ciclo": ciclo_id, "senales": senales, "dimensiones_actualizadas": s.get("dimensiones_clave") or [],
                                  "linea_base": linea_base})
    _escribir(ent, {"tipo_entrada": "CIC", "id": ciclo_id, "seg_id": seg_id, "run_id": run_id, "estado": "ENTREGADO", "semaforo": semaforo,
                    "recomendacion": recom, "resumen": inf["resumen"], "minutos": minutos, "uc": uc, "informe": rutas, "decision_broker": None,
                    "fecha_corte": ent.as_of})
    _escribir(ent, {"tipo_entrada": "SEG", "id": seg_id, "ciclos": n, "proximo_ciclo": prox, "ultimo_ciclo": ciclo_id, "linea_base_pendiente": False})
    alm.escribir("F1", "AG-B01", {"tipo_entrada": "CICLO_SEGUIMIENTO", "id": ciclo_id, "seg_id": seg_id, "run_id": run_id, "minutos": minutos,
                                  "uc": uc, "semaforo": semaforo, "recomendacion": recom, "autorizacion_salida": auts})
    _evento_eval(ent, {"seg_id": seg_id, "ciclo_id": ciclo_id, "evento": "CICLO", "semaforo": semaforo, "recomendacion": recom})
    return {"seg_id": seg_id, "ciclo_id": ciclo_id, "estado": "ENTREGADO", "semaforo": semaforo, "recomendacion": recom,
            "proximo_ciclo": prox, "informe_seguimiento": rutas, "estado_g3": g3["dictamen"], "tiempo_min": minutos, "uc": uc,
            "nota": "Ciclo N1-SEG encargado por el Broker (CT-B-29): el bloque no ha iniciado ningún análisis profundo."}


def pendientes(ent, coord) -> Dict:
    """Agenda HT-05: ejecuta los ciclos cuyo próximo ciclo ha vencido (solo seguimientos ACTIVOS; nunca por iniciativa propia)."""
    out = []
    for seg_id, s in sorted(ent.alm.estado("F11", tipo="SEG").items()):
        if s.get("estado") == "ACTIVO" and s.get("proximo_ciclo") and s["proximo_ciclo"] <= ent.as_of:
            out.append(ciclo(ent, coord, seg_id))
    return {"fecha_corte": ent.as_of, "ciclos": out}


def listar(ent) -> Dict:
    hoy = dt.date.fromisoformat(ent.as_of)
    meses = int(_cfg(ent).get("revision_sin_fecha_fin_meses", 6))
    out = []
    for seg_id, s in sorted(ent.alm.estado("F11", tipo="SEG").items()):
        rec = []
        if s.get("estado") == "ACTIVO" and not s.get("fecha_fin") and s.get("alta") and \
                (hoy - dt.date.fromisoformat(s["alta"])).days >= 30 * meses:
            rec.append("recordatorio de revisión: seguimiento sin fecha de fin")
        if s.get("estado") == "PAUSADO" and s.get("pausado_desde") and (hoy - dt.date.fromisoformat(s["pausado_desde"])).days >= 182:
            rec.append("pausado más de 6 meses: ¿cancelar o reanudar?")
        out.append({"seg_id": seg_id, "estado": s.get("estado"), "frecuencia": s.get("frecuencia"), "proximo_ciclo": s.get("proximo_ciclo"),
                    "ciclos": s.get("ciclos", 0), "ultimo_ciclo": s.get("ultimo_ciclo"), "rec_id": s.get("rec_id"), "recordatorios": rec,
                    "advertencias": s.get("advertencias") or []})
    return {"fecha_corte": ent.as_of, "seguimientos": out}
