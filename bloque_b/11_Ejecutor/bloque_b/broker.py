"""Servicios del Coordinador frente al Broker distintos de la petición: consultas N0 (CT-B-03), retroalimentación,
decisiones, credenciales y configuración (CT-B-04 y respuesta de CT-B-06), estado del servicio y mantenimiento del
conocimiento (HT-02 sobre F7, F8, F9 y FM, con los Documentadores y el Buscador; CT-B-24)."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Dict, List, Optional

from .contratos import MensajeRechazado, comprobar_sensibles, sanear
from .herramientas import ht02, ht08
from .prompts import AGENTES

PARAM_SERVICIO = ("consultas_broker", "seguimientos", "politica_autorizacion", "tope_autorizacion_automatica_min", "criterios_nivel_auto", "marco_invertibilidad", "top_n",
                  "idioma_usuario", "objetivos_tiempo")


def consulta(ent, coord, pregunta: str, contexto: Optional[str] = None) -> Dict:
    alm = ent.alm
    try:
        comprobar_sensibles({"pregunta": pregunta})
    except MensajeRechazado as e:
        alm.incidencia("SEGURIDAD", f"Consulta rechazada: {e.tipo}", "AG-B01", severidad="Crítica")
        return {"ruta": "RECHAZADA", "motivo": "DATOS_SENSIBLES"}
    pregunta = sanear(pregunta)
    qid = alm.nuevo_id("QRY-B")
    recs = [r for k, r in alm.estado("F3").items() if str(k).startswith("REC-B-")]
    if contexto:
        recs = [r for r in recs if r.get("id") == contexto or r.get("pet_id") == contexto] or recs
    refs = [r["id"] for r in recs[-3:]]
    cands = [k for k, c in alm.estado("F3").items() if str(k).startswith("CAND-B-") and c.get("rec_id") in refs and c.get("en_top_n")]
    extracto = [{"rec_id": r["id"], "ambito": (r.get("ambito") or {}).get("nombre"), "veredicto": r.get("veredicto"), "A": r.get("A"),
                 "E": r.get("E"), "C": r.get("C"), "estado_vigilancia": r.get("estado_vigilancia"), "fecha": r["_historial"][0]["fecha"]} for r in recs[-3:]]
    r = ent.inv.llamar("AG-B01", "CT-B-03", "consulta", {"query_id": qid, "pregunta": pregunta, "memoria": extracto,
                                                          "referencias_disponibles": refs + cands[:10]},
                       "Clasifica la consulta (7.7) y responde SOLO desde la memoria del bloque, citando identificadores. Si exige análisis, "
                       "propón una petición (no la inicies).", {"clase_consulta": "string", "ruta": "string", "respuesta": "string"},
                       coord._ctx("AG-B01"))
    clase = r.get("clase_consulta") if r.get("clase_consulta") in ("ACLARACION", "DATO", "METODO", "ESTADO", "CONTRASTE", "PROFUNDIZACION") else "ACLARACION"
    ruta = "PROPUESTA_DE_PETICION" if clase in ("CONTRASTE", "PROFUNDIZACION") else "N0"
    resp = {"query_id": qid, "clase_consulta": clase, "ruta": ruta, "respuesta": r.get("respuesta") or "Sin respuesta trazable en la memoria.",
            "referencias": [x for x in (r.get("referencias") or refs) if isinstance(x, str)], "confianza": r.get("confianza") or "probable",
            "caducidades_afectadas": []}
    if ruta == "PROPUESTA_DE_PETICION":
        resp["peticion_propuesta"] = {"nivel": "N2", "alcance": pregunta[:200], "estimacion_min_p80": 25}
    alm.escribir("F1", "AG-B01", {"tipo_entrada": "CONSULTA", "id": qid, "pregunta": pregunta, "respuesta": resp})
    # Pregunta repetida (3 veces en 4 semanas) → aviso al Evaluador (CT-B-26)
    hace4 = (dt.date.fromisoformat(ent.as_of) - dt.timedelta(days=28)).isoformat()
    iguales = [e for e in alm.leer("F1") if e.get("tipo_entrada") == "CONSULTA" and e["_fecha"] >= hace4
               and str(e.get("pregunta", "")).strip().lower() == pregunta.strip().lower()]
    if len(iguales) >= 3:
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "AVISO_EVALUADOR", "id": alm.nuevo_id("AVE-B"), "tipo": "PREGUNTA_REPETIDA", "pregunta": pregunta})
        alm.escribir("F5", "AG-B23", {"tipo_entrada": "LECCION", "id": alm.nuevo_id("LEC-B"), "ambito": "producto",
                                      "observacion": f"Pregunta repetida {len(iguales)} veces en 4 semanas: «{pregunta[:80]}»",
                                      "recomendacion": "Responderla de forma explícita en los entregables", "fuerza": "recurrente"})
        resp["pregunta_repetida"] = True
    return resp


def decision(ent, datos: Dict, coord=None) -> Dict:
    """CT-B-04 (decisiones, resultados, valoraciones, configuración y orden de forzar la continuación tras una puerta de
    viabilidad, 7.10) y respuestas de CT-B-06 (estado y alias)."""
    alm = ent.alm
    try:
        comprobar_sensibles(datos)
    except MensajeRechazado as e:
        alm.incidencia("CREDENCIAL_FUERA_DE_BOVEDA" if e.tipo == "CREDENCIAL" else "SEGURIDAD",
                       f"Mensaje CT-B-04/06 rechazado íntegro: {e.tipo} (no se reproduce; avisar al Broker para revocar)", "AG-B01", severidad="Crítica")
        return {"estado": "RECHAZADO", "motivo": str(e)}
    datos = sanear(datos)
    hecho = []
    da = datos.get("decision_ambito")
    if da:
        if da.get("decision") not in ("CANDIDATOS_ENVIADOS_A_C", "EN_VIGILANCIA", "DESCARTADO", "APLAZADO"):
            raise ValueError("decision_ambito.decision no válida")
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "DECISION", "id": alm.nuevo_id("DEC-B"), **da})
        alm.escribir("F3", "AG-B23", {"tipo_entrada": "DECISION_BROKER", "id": da["rec_id"], "decision_broker": da["decision"]})
        hecho.append("decision_ambito")
    for dc in datos.get("decisiones_candidatos") or []:
        if dc.get("decision") not in ("ENVIADO_A_C", "EN_VIGILANCIA", "DESCARTADO"):
            raise ValueError("decisiones_candidatos.decision no válida")
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "DECISION", "id": alm.nuevo_id("DEC-B"), **dc})
        alm.escribir("F3", "AG-B23", {"tipo_entrada": "DECISION_BROKER", "id": dc["cand_id"], "decision_broker": dc["decision"]})
        hecho.append(f"decision {dc['cand_id']}")
    ds = datos.get("decision_seguimiento")   # decisión posterior del Broker sobre un ciclo (archivo F11, entrada DEC)
    if ds:
        if ds.get("decision") not in ("MANTENER", "REACTIVAR_PETICION", "PASAR_A_C", "CANCELAR", "SIN_DECISION"):
            raise ValueError("decision_seguimiento.decision no válida")
        segs = alm.estado("F11", tipo="SEG")
        if ds.get("seg_id") not in segs:
            raise ValueError(f"{ds.get('seg_id')} no existe en el archivo F11")
        alm.escribir("F11", "AG-B01", {"tipo_entrada": "DEC", "id": f"DEC-{ds['seg_id']}-{str(ds.get('ciclo_id') or '')[-2:]}",
                                        "seg_id": ds["seg_id"], "ciclo_id": ds.get("ciclo_id"), "decision": ds["decision"],
                                        "motivo": ds.get("motivo"), "pet_id": ds.get("pet_id"), "cand_ids": ds.get("cand_ids") or []})
        if ds["decision"] == "CANCELAR" and segs[ds["seg_id"]].get("estado") in ("ACTIVO", "PAUSADO"):
            alm.escribir("F11", "AG-B01", {"tipo_entrada": "SEG", "id": ds["seg_id"], "accion": "CANCELACION", "estado": "CANCELADO",
                                            "motivo": ds.get("motivo") or "Decisión del Broker tras el ciclo", "proximo_ciclo": None})
        hecho.append(f"decision_seguimiento {ds['seg_id']}")
    for k in ("resultado_comunicado", "valoracion_entregables"):
        if datos.get(k):
            alm.escribir("F1", "AG-B01", {"tipo_entrada": k.upper(), "id": alm.nuevo_id("RES-B"), **datos[k]})
            hecho.append(k)
    if hecho:   # CT-B-26 al Evaluador
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "AVISO_EVALUADOR", "id": alm.nuevo_id("AVE-B"), "tipo": "RESULTADOS_BROKER", "contenido": hecho})
    cfg = datos.get("configuracion") or {}
    for k, v in cfg.items():
        if k not in PARAM_SERVICIO:
            raise ValueError(f"«{k}» no es un parámetro de servicio (los cambios de tipo 3 son del operador)")
        if k == "tope_autorizacion_automatica_min" and float(v) > 480:
            raise ValueError("El tope de autorización automática no puede superar 480 min (Anexo A)")
        if k == "politica_autorizacion":
            for r in v:
                if r.get("accion") not in ("AUTORIZAR_HASTA", "ELEGIR_OPCION", "NO_AUTORIZAR") or not str(r.get("regla_id", "")).startswith("POL-"):
                    raise ValueError("Regla de política no válida (regla_id POL-…; acción AUTORIZAR_HASTA | ELEGIR_OPCION | NO_AUTORIZAR)")
                if r.get("accion") == "ELEGIR_OPCION" and r.get("opcion") not in ht08.OPCIONES:
                    raise ValueError("Opción de política no válida")
        alm.escribir("F10", "AG-B01", {"tipo_entrada": "CFG", "id": alm.nuevo_id("CFG-B"), "parametro": k, "valor": v})
        hecho.append(f"configuracion {k}")
    for cr in datos.get("credenciales") or []:   # respuesta de CT-B-06: estado y alias, nunca la clave
        if set(cr) - {"cred_id", "estado", "credencial_ref", "caducidad", "restricciones"}:
            raise ValueError("La respuesta de CT-B-06 solo admite cred_id, estado, credencial_ref, caducidad y restricciones")
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "CREDENCIAL", "id": cr["cred_id"], "estado": cr.get("estado"),
                                      "credencial_ref": cr.get("credencial_ref"), "caducidad": cr.get("caducidad")})
        hecho.append(f"credencial {cr['cred_id']}")
    fc = datos.get("forzar_continuacion")
    out = {"estado": "COMPLETO", "registrado": hecho}
    if fc:
        if coord is None:
            raise ValueError("forzar_continuacion exige el Coordinador")
        out["forzar_continuacion"] = coord.forzar_continuacion(fc.get("pet_id"), fc.get("puerta"), fc.get("motivo"), "CT-B-04")
        hecho.append(f"forzar_continuacion {fc.get('pet_id')} {fc.get('puerta')}")
    return out


def estado(ent, coord, pet: Optional[str] = None, config: bool = False) -> Dict:
    coord._revisar_autorizaciones()
    alm = ent.alm
    pets = alm.estado("F1", tipo="PETICION")
    auts = alm.estado("F1", tipo="AUTORIZACION")
    out = {"fecha_corte": ent.as_of, "peticiones": {k: {"estado": v.get("estado"), "nivel": v.get("nivel"), "aut_id": v.get("aut_id")}
                                                    for k, v in pets.items()},
           "autorizaciones_pendientes": [{"aut_id": k, "pet_id": a.get("pet_id"), "puerta": a.get("puerta"), "momento": a.get("momento"),
                                          "recordatorio": bool(a.get("recordatorio_enviado"))} for k, a in auts.items() if a.get("estado") == "PENDIENTE"],
           "agentes": ent.prompts.estado(), "conectores": ent.boveda.estado(), "integridad": alm.verificar_integridad(),
           "incidencias": len([e for e in alm.leer("HA") if e.get("tipo_entrada") == "INC"]),
           "referencias": ent.refs.recuento(), "methodology_version": ent.f10().get("methodology_version"),
           "consultas_broker_pendientes": [{"cns_id": k, "pet_id": e.get("pet_id"), "modo": e.get("modo"), "plazo": e.get("plazo")}
                                           for k, e in alm.estado("F1", tipo="CONSULTA_BROKER").items() if e.get("estado") == "PENDIENTE"],
           "seguimientos_activos": [{"seg_id": k, "proximo_ciclo": s_.get("proximo_ciclo")} for k, s_ in alm.estado("F11", tipo="SEG").items()
                                    if s_.get("estado") == "ACTIVO"]}
    out["agentes_resumen"] = {s: sum(1 for a in out["agentes"].values() if a["estado"] == s) for s in ("CARGADO", "AUSENTE", "DEGRADADO")}
    if pet:
        p = pets.get(pet) or {}
        ejec = [e for e in alm.leer("F1") if e.get("pet_id") == pet and e.get("tipo_entrada") in ("PUNTO_CONTROL", "EJECUCION", "ENTREGA")]
        avt = [e for e in alm.leer("HA") if e.get("pet_id") == pet and e.get("tipo_entrada") == "AVT"]
        out["peticion"] = {"id": pet, "estado": p.get("estado"), "historial": p.get("_historial"),
                           "ultimo_punto_control": next((e for e in reversed(ejec) if e["tipo_entrada"] == "PUNTO_CONTROL"), None),
                           "ultima_proyeccion": avt[-1]["proyeccion"] if avt else None}
    if config:
        out["f10"] = ent.f10()
    return out


def verificar_enlaces(ent, coord, aplicar: bool = False, offline: bool = True, max_fichas: Optional[int] = None) -> Dict:
    informe = {}
    for k, p in ent.refs.rutas.items():
        if not p or not Path(p).exists():
            informe[k] = {"archivo": None, "fichas": 0}
            continue
        lineas = Path(p).read_text(encoding="utf-8").splitlines(keepends=True)
        fichas = ht02.leer_fichas(lineas)
        if offline:
            res = [{"id": f.id, "estado": "PENDIENTE_BARRIDO", "accion": "NINGUNA",
                    "tiene_enlace": bool(ht02.extraer_url(f.campo("URL", "DOI / URL", "Canal oficial (URL raíz)")) or
                                         ht02.extraer_doi(f.campo("DOI", "DOI / URL")))} for f in fichas[:max_fichas]]
        else:   # pragma: no cover - requiere red
            res = ht02.verificar_archivo(lineas, ht02.Config(), dt.date.fromisoformat(ent.as_of),
                                         [f.id for f in fichas[:max_fichas]] if max_fichas else None)
            if aplicar:
                Path(p).write_text("".join(ht02.aplicar_resultados(lineas, res)), encoding="utf-8")
        informe[k] = {"archivo": Path(p).name, "fichas": len(fichas), "sin_enlace": sum(1 for r in res if not r.get("tiene_enlace", True)),
                      "por_estado": {e: sum(1 for r in res if r.get("estado") == e) for e in {r.get("estado") for r in res}},
                      "acciones": {a: sum(1 for r in res if r.get("accion") == a) for a in {r.get("accion") for r in res}}}
    for ag, archivo in (("AG-B18", "F7"), ("AG-B19", "F8"), ("AG-B20", "F9")):
        ent.inv.llamar(ag, "CT-B-24", "mantenimiento", {"archivo": archivo, "resumen": informe.get(archivo), "resultados": []},
                       "Decide reparar, degradar o borrar según el barrido (13.4); deja Novedades y lagunas.", {"decisiones": "array"},
                       coord._ctx(ag))
    ent.alm.escribir("HA", "AG-B21", {"tipo_entrada": "MANTENIMIENTO", "id": ent.alm.nuevo_id("MAN-B"), "informe": informe, "offline": offline})
    ent.salida.mkdir(parents=True, exist_ok=True)
    (ent.salida / f"{ent.as_of}_verificacion-enlaces.json").write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"modo": "sin red (solo lectura de fichas)" if offline else "con red", "aplicado": aplicar and not offline, "informe": informe}
