"""Paquete de síntesis (CT-15) y validación G3 con HT-09.

El paquete de síntesis es un superconjunto del esquema `paquete_oportunidades` V5.0 (Documento 0 óptima V5.0,
Anexo B): cada opción es un ámbito con `tipo_activo`, `subtipo`, `ambito`, `indicador_seguimiento` e `invertibilidad`,
y `paquete_para_bloque_B` es el encargo de 2.5 (criterios de selección sugeridos, métricas clave y preguntas). Añade por opción los
campos que HT-09 aprovecha (`puertas`, `cluster`, `vigente`, `horizontes.Hn.advertencia/metodo`,
`objeciones[].resuelta`). El entregable JSON se obtiene eliminando esos campos (ver `redaccion.entregable_json`).
"""
from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Set, Tuple

import pandas as pd

from .configuracion import (
    CLASES,
    HORIZONTES,
    NATURALEZA_POR_DEFECTO,
    NATURALEZAS,
    NOMBRE_CLASE,
    naturaleza_coherente,
    naturaleza_para,
    parametro,
    sesiones_horizonte,
)
from .contratos import REGIONES
from .herramientas import ht09
from .herramientas.ht05_planificador import fecha_resolucion
from .herramientas.ht06_indice import normalizar

RE_FECHA_CAT = re.compile(r"^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$|^[0-9]{4}-T[1-4]$|^[0-9]{4}-S[12]$")
ETIQUETA_SIN_CERT = "sin ventaja demostrada todavía"
ADVERTENCIA_H1 = "Previsión a días: la de menor fiabilidad esperada; sin ventaja demostrada todavía."
AVISO_LEGAL = ("Este informe describe oportunidades generales de mercado y no constituye asesoramiento personalizado; "
               "el Broker Personal valora si encaja con el usuario.")


def _menos_de_tres_texto(c: str, sel: dict, n_opc: int) -> str | None:
    m = sel["seleccion"].get("menos_de_tres_motivo")
    if n_opc >= 3:
        return None
    partes = [f"Se proponen {n_opc} opción(es) en {NOMBRE_CLASE[c]}."]
    if m:
        partes.append(m["texto"])
        for x in m["no_llegaron"][:4]:
            partes.append(f"{x['opp_id']}: {'; '.join(x['motivos'][:2])} → {'; '.join(x['que_tendria_que_ocurrir'][:2])}.")
    else:
        partes.append("Ninguna candidata superó las puertas de continuidad y de selección en este ciclo (R14).")
    return " ".join(partes)


TIPOS_INDICADOR = ("INDICE", "SERIE", "CESTA")
EXCLUYE_POR_DEFECTO = "Activos e instrumentos concretos: su selección corresponde al Bloque B"


def _ambito(f: dict, c: str) -> dict:
    a = f.get("ambito") if isinstance(f.get("ambito"), dict) else {}
    inc = str(a.get("incluye") or f.get("nombre") or "").strip()
    exc = str(a.get("excluye") or "").strip()
    reg = str(a.get("region") or "").strip()
    return {"incluye": inc if len(inc) >= 5 else f"Ámbito «{f.get('nombre')}» del tipo {c}",
            "excluye": exc if len(exc) >= 2 else EXCLUYE_POR_DEFECTO,
            "region": reg if len(reg) >= 2 else ", ".join(f.get("regiones") or ["Global"])}


def _indicador(f: dict, fuente: str) -> dict:
    i = f.get("indicador_seguimiento") if isinstance(f.get("indicador_seguimiento"), dict) else {}
    out = {"nombre": str(i.get("nombre") or f.get("nombre") or f["proxy"])[:200], "simbolo": f["proxy"], "fuente": fuente}
    if str(i.get("tipo", "")).upper() in TIPOS_INDICADOR:
        out["tipo"] = str(i["tipo"]).upper()
    return out


def _invertibilidad(f: dict) -> dict:
    i = f.get("invertibilidad") if isinstance(f.get("invertibilidad"), dict) else {}
    nota = str(i.get("nota") or "").strip()
    return {"universo_suficiente": True,   # en el top-3 solo hay ámbitos que superan PS3
            "nota": nota if len(nota) >= 5 else "Universo negociable suficiente y accesible según el Analista (PS3 superada)"}


def _lista(f: dict, k: str, defecto: list[str]) -> list[str]:
    v = [str(x) for x in (f.get(k) or []) if isinstance(x, str) and len(x.strip()) >= 3]
    return v or defecto


def _siguiente_paso(op: dict, umbrales: dict) -> str:
    """Prompt del Analizador, 6.16: ENVIAR_A_BLOQUE_B solo con tesis madura (E ≥ umbral), sin objeción moderada abierta
    y con un catalizador dentro del horizonte principal; PROFUNDIZAR_EN_A si es atractiva con incertidumbre reducible;
    si no, VIGILAR. Los umbrales salen de la configuración (`seleccion.siguiente_paso`)."""
    pu = op["puntuaciones"]
    E, A = pu["E"], pu["A"]
    moderada_abierta = any(o.get("fuerza") == "moderada" and o.get("estado") != "RESPONDIDA" for o in op.get("objeciones") or [])
    fin = ((op.get("horizontes") or {}).get(op.get("horizonte_principal")) or {}).get("fecha_resolucion")
    catalizador = bool(fin) and any(str(c.get("fecha", "")) <= str(fin) for c in op.get("catalizadores") or [])
    if E >= umbrales["E_enviar"] and not moderada_abierta and catalizador:
        return "ENVIAR_A_BLOQUE_B"
    if E < umbrales["E_enviar"] and (op.get("relevancia_decisional") == "ALTA" or A >= umbrales["A_profundizar"]):
        return "PROFUNDIZAR_EN_A"
    return "VIGILAR"


def _prob_analista(f: dict, h: str) -> float | None:
    """Probabilidad propia del Analista para el horizonte h (PA-21), si la declaró y está en el rango de AG-10."""
    from .contratos import FINALISTA
    props: Any = FINALISTA["properties"]
    rango = props["probabilidades_propias"]["additionalProperties"]   # única definición (QA H-08)
    v = (f.get("probabilidades_propias") or {}).get(h)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not rango["minimum"] <= float(v) <= rango["maximum"]:
        return None
    return float(v)


def _semaforo(opciones: list, umbrales: dict) -> str:
    """Prompt del Analizador, 6.15.5: VERDE con ≥ 1 opción de E ≥ E_verde y A ≥ A_verde; ÁMBAR con opciones inciertas o
    marginales; GRIS sin opciones."""
    if not opciones:
        return "GRIS"
    e_v, a_v = umbrales.get("E_verde", umbrales.get("E_enviar")), umbrales.get("A_verde", umbrales.get("A_profundizar"))
    solida = any(o["puntuaciones"]["E"] >= e_v and o["puntuaciones"]["A"] >= a_v for o in opciones)
    return "VERDE" if solida else "AMBAR"


def _umbrales_presentacion(cfg: dict) -> tuple[dict, dict]:
    """Umbrales del siguiente paso y del semáforo ([PROPUESTO], INC-T53-05): de la configuración, sin literales de respaldo
    (T-65, H-08). Si falta uno, falla cerrado."""
    paso = {k: parametro(cfg, f"seleccion.siguiente_paso.{k}") for k in ("E_enviar", "A_profundizar")}
    semaforo = {k: parametro(cfg, f"seleccion.semaforo.{k}") for k in ("E_verde", "A_verde")}
    return paso, semaforo


def construir(bloque, run_id, tipo, as_of, clases, nivel, gc0, analisis, seleccion, clusteres, integ, historial, presupuesto) -> tuple[dict, dict]:
    cfg = bloque.cfg
    umbral_paso, umbral_sem = _umbrales_presentacion(cfg)
    dias_nr = int(parametro(cfg, "evaluacion.dias_habiles_no_resoluble"))   # QA r01 de T-65, H-05
    pres = parametro(cfg, "presentacion")   # [PROPUESTO] INC-T53-05: confianza y zona de interés (T-65, CA-14)
    avisos_hp: list[str] = []   # horizontes del Analista sustituidos (8.3): se declaran como limitación
    as_of = pd.Timestamp(as_of)
    certs = {(c["celda"]["clase"], c["celda"]["horizonte"]): c["id"] for c in bloque.evaluador.certificados_vigentes(as_of)}
    prefer = parametro(cfg, "horizonte_principal_preferente")
    meses_hitos = parametro(cfg, "h5.meses_hitos")
    prg_borradores: list[dict] = []
    desgloses, paquete_clases, por_opp = {}, {}, {}
    clases_out: dict[str, dict] = {}
    bloque_b: list[dict] = []
    fechas_dato = []
    f1 = bloque.almacen.estado("F1", as_of)
    tnd_por_nombre = {normalizar(t.get("nombre_canonico", "")): k for k, t in f1.items()}

    def borradores(f: dict, c: str, en_informe: bool) -> dict[str, str]:
        ids = {}
        for h, d in f["_hz"].items():
            if d.get("prg_existente"):
                ids[h] = d["prg_existente"]
                prg_borradores.append({"prg_id": d["prg_existente"], "prg_existente": d["prg_existente"], "opp_id": f["opp_id"],
                                       "horizonte": h, "vista": d["vista"]})
                continue
            pid = bloque.almacen.nuevo_id("PRG")
            ids[h] = pid
            positivo = d["vista"] in ("alcista", "relativa_favorable")
            ses = sesiones_horizonte(cfg, h)   # T-65 (CA-14 de T-53): de `horizontes` y `calendario`
            ref = f.get("_referencia")
            ri = bloque.evaluador.tasa_base(f["proxy"], ref, c, ses, positivo, as_of, run_id)
            fr = fecha_resolucion(as_of, h, cfg["horizontes"])
            _, nivel_p = bloque.proveedor.valor_en(f["proxy"], as_of)
            nivel_r = None
            if ref and ref != "CESTA":
                nivel_r = bloque.proveedor.valor_en(ref, as_of)[1]
            tp = f.get("_tipo_pronostico", "RELATIVO")
            texto_ev = (f"rentabilidad de {f['proxy']} {'superior' if positivo else 'inferior'} a la de {ref} entre {as_of.date()} y {fr.date()}"
                        if tp == "RELATIVO" else f"rentabilidad de {f['proxy']} {'positiva' if positivo else 'negativa'} entre {as_of.date()} y {fr.date()}")
            prg_borradores.append({
                "tipo_entrada": "ALTA", "prg_id": pid, "version_de": d.get("version_de"), "opp_id": f["opp_id"],
                "tnd_ids": [f["tnd_id"]] if f.get("tnd_id") else [], "run_id": run_id, "clase": c, "horizonte": h,
                "estrategia": f"{c}-{(f.get('tipo_opcion') or 'MERCADO')}", "tipo_opcion": f.get("tipo_opcion"),
                "tipo_pronostico": tp, "afirmacion": d["afirmacion"], "evento": texto_ev, "sentido": "POSITIVO" if positivo else "NEGATIVO",
                "vista": d["vista"], "variable": {"serie_ht01": f["proxy"], "descripcion": f"cierre de {f['proxy']}", "tipo_rentabilidad": "PRECIO", "divisa": None},
                "referencia_indice": ref if tp == "RELATIVO" else None, "nivel_referencia": {"valor": nivel_p, "fecha": str(as_of.date()), "fuente": f"HT-01:{bloque.proveedor.nombre}"},
                "nivel_referencia_indice": nivel_r, "umbral": 0.0, "fecha_emision": str(as_of.date()), "fecha_congelacion": bloque.reloj.ahora(),
                "fecha_resolucion": str(fr.date()),
                "criterio_resolucion": f"Cierre HT-01 de la última sesión ≤ {fr.date()} frente al cierre de la última sesión ≤ {as_of.date()}; suceso: {texto_ev}",
                "fuente_resolucion": f"HT-01:{bloque.proveedor.nombre}", "regla_fallback": f"última sesión disponible ≤ fecha de resolución; NO_RESOLUBLE tras {dias_nr} días hábiles sin dato",
                "banda_verbal": bloque.evaluador.banda_de(d["prob_interna"]), "prob_interna": d["prob_interna"],
                "prob_publicada": d["prob_interna"] if (c, h) in certs else None, "certificado_ref": certs.get((c, h)),
                "metodo": d.get("metodo"), "referencia_ingenua": ri, "escenario_asociado": d.get("escenario", "BASE"),
                "en_informe": en_informe, "estado": "ABIERTO",
                # PA-09 (T-66): un backtest con un modelo real anterior a su fecha de corte puede «acertar» de memoria
                "contaminacion_posible": bloque.contaminacion_posible(as_of),
                # PA-21 (T-66): probabilidad propia del Analista, segunda opinión que el Evaluador mide frente a AG-10
                "prob_analista": _prob_analista(f, h),
                "puntuaciones_opcion": {k: f["_ht03"]["puntuaciones"].get(k) for k in ("T", "E", "A", "RK")}})
            if h == "H5":
                _h5_con_hitos(prg_borradores[-1], f, c, ref, tp, positivo, d)
        return ids

    def _h5_con_hitos(b: dict, f: dict, c: str, ref, tp: str, positivo: bool, d: dict) -> None:
        """V5.1 (8.3, R13): el PRG H5 solo registra la banda (sin probabilidad ni certificado) y lleva ≥ 3 hitos HIT-,
        cada uno un pronóstico ordinario de su propio horizonte (H4) que el Evaluador resuelve en su fecha."""
        b.update({"prob_interna": None, "prob_publicada": None, "certificado_r13": False, "certificado_ref": None,
                  "referencia_ingenua": {"tipo": "NO_APLICA", "nota": "H5 se evalúa por sus hitos HIT-"},
                  "tesis_estructural": f.get("tesis"), "hit_ids": [], "hitos": []})
        for m in meses_hitos:
            hid = bloque.almacen.nuevo_id("HIT")
            fh = (as_of + pd.DateOffset(months=int(m))).normalize()
            ev = (f"rentabilidad acumulada de {f['proxy']} {'superior' if positivo else 'inferior'} a la de {ref} entre {as_of.date()} y {fh.date()}"
                  if tp == "RELATIVO" else f"rentabilidad acumulada de {f['proxy']} {'positiva' if positivo else 'negativa'} entre {as_of.date()} y {fh.date()}")
            hito = copy.deepcopy({k: v for k, v in b.items() if k not in ("hit_ids", "hitos", "tesis_estructural")})
            hito.update({"prg_id": hid, "prg_padre": b["prg_id"], "es_hito": True, "prob_analista": None, "necesario": m == meses_hitos[-1], "horizonte": "H4",
                         "afirmacion": f"Hito de la senda H5: {ev}", "evento": ev, "fecha_resolucion": str(fh.date()),
                         "criterio_resolucion": f"Cierre HT-01 de la última sesión ≤ {fh.date()} frente al cierre de la última sesión ≤ {as_of.date()}; suceso: {ev}",
                         "prob_interna": d["prob_interna"], "banda_verbal": bloque.evaluador.banda_de(d["prob_interna"]), "prob_publicada": None,
                         "referencia_ingenua": {"tipo": "RI-TB", "valor_o_prob": float(parametro(cfg, "tasa_base.sin_historia")),
                                                "nota": "tasa base neutra (ventana superior a la historia disponible)"}})
            prg_borradores.append(hito)
            b["hit_ids"].append(hid)
            b["hitos"].append({"hit_id": hid, "fecha": str(fh.date()), "indicador": f"Rentabilidad acumulada de {f['proxy']}"
                               + (f" frente a {ref}" if tp == "RELATIVO" else "") + " (HT-01)", "criterio": ev,
                               "banda": bloque.evaluador.banda_publicable(d["prob_interna"])})

    for c in clases:
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
            hz = {}
            for h, d in sorted(f["_hz"].items()):
                cert = (c, h) in certs
                hz[h] = {"vista": d["vista"], "banda": bloque.evaluador.banda_publicable(d["prob_interna"]), "prob": d["prob_interna"] if cert else None,
                         "certificado_r13": cert, "prg_id": ids[h], "metodo": d.get("metodo")}
                if not cert:
                    hz[h]["etiqueta"] = ETIQUETA_SIN_CERT
                b = next(p for p in prg_borradores if p.get("prg_id") == ids[h])
                if "fecha_resolucion" in b:
                    hz[h]["fecha_resolucion"], hz[h]["criterio_resolucion"] = b["fecha_resolucion"], b["criterio_resolucion"]
                else:
                    prev = bloque.almacen.estado("F4", as_of).get(ids[h], {})
                    hz[h]["fecha_resolucion"], hz[h]["criterio_resolucion"] = prev.get("fecha_resolucion"), prev.get("criterio_resolucion")
                if h == "H1":
                    hz[h]["advertencia"] = ADVERTENCIA_H1
                if h == "H5":
                    b5 = b if "hitos" in b else bloque.almacen.estado("F4", as_of).get(ids[h], {})
                    hz[h].update({"prob": None, "certificado_r13": False, "etiqueta": ETIQUETA_SIN_CERT,
                                  "hitos": copy.deepcopy(b5.get("hitos") or [])})
                    if b5.get("tesis_estructural"):
                        hz[h]["tesis_estructural"] = b5["tesis_estructural"]
            # V5.1 (8.3): naturaleza de la inversión y horizonte principal coherentes
            # Lo declara el Analista y HT-09 (C17) dictamina; el ejecutor solo lo propone si el Analista no lo declara.
            nat_ag = f.get("naturaleza_inversion") if f.get("naturaleza_inversion") in NATURALEZAS else None
            hp_ag = f.get("horizonte_principal") if f.get("horizonte_principal") in hz else None
            just = f.get("justificacion_horizonte") or None
            if f.get("horizonte_principal") and hp_ag is None:
                avisos_hp.append(f"{f['opp_id']}: el horizonte principal declarado por el Analista "
                                 f"({f.get('horizonte_principal')}) no está entre los ofrecidos; lo propone el ejecutor (8.3)")
            if hp_ag is not None:
                # Sin naturaleza declarada, el ejecutor propone la coherente con el horizonte del Analista (no inventa
                # una que haga fallar C17)
                nat, hp = nat_ag or naturaleza_para(hp_ag), hp_ag
            else:
                nat = nat_ag or NATURALEZA_POR_DEFECTO.get(c, "CICLICA")
                hp = next((h for h in prefer if h in hz and naturaleza_coherente(nat, h)), None)
                if hp is None:
                    hp = next((h for h in prefer if h in hz), sorted(hz)[0])
                    if nat_ag is None:
                        nat = naturaleza_para(hp)   # naturaleza por defecto: se elige la coherente con el horizonte
                    # con naturaleza declarada por el Analista no se cambia en silencio: HT-09 lo dictamina
                just = None
            f["_naturaleza"], f["_hp"], f["_just_hp"] = nat, hp, just
            sen = f["senales"]
            if sen.get("fecha_dato"):
                fechas_dato.append(sen["fecha_dato"])
            precio = float(bloque.proveedor.valor_en(f["proxy"], as_of)[1])
            liq = f.get("liquidez") or "alta"
            objs = []
            for o in f.get("_objeciones", []):
                resp = o.get("respuesta")
                ok = bool(resp and len(resp) >= 10) and (o["fuerza"] != "fuerte" or o["resuelta"])
                objs.append({"objecion_id": o["objecion_id"], "fuerza": o["fuerza"], "resumen": o["resumen"], "respuesta": resp,
                             "estado": "RESPONDIDA" if ok else "SIN_RESOLVER", "resuelta": bool(o["resuelta"]) if o["fuerza"] == "fuerte" else ok})
            calcs = [x for x in (sen.get("calc_ids") or []) if str(x).startswith("CALC-")]
            if clusteres.get("calc_id"):
                calcs.append(clusteres["calc_id"])
            if not calcs:
                calcs = list(an.get("calc_ids") or [])
            fuente = f"HT-01:{bloque.proveedor.nombre}"
            op = {"opp_id": f["opp_id"], "rango": t["rango"], "tipo_opcion": f.get("tipo_opcion", "MERCADO"), "tipo_activo": c,
                  "subtipo": str(f.get("subtipo") or (f.get("tipo_opcion") or "Ámbito").capitalize()), "nombre": f.get("nombre"),
                  "nombre_llano": (f.get("nombre_llano") or f.get("nombre"))[:70], "tesis": f.get("tesis"), "mecanismo": f.get("mecanismo"),
                  "tnd_ids": [f["tnd_id"]] if f.get("tnd_id") else [], "cluster_id": f["_cluster"],
                  "regiones": [r for r in (f.get("regiones") or []) if r in REGIONES] or ["GLB"],
                  "puntuaciones": {"T": pu.get("T"), "E": pu["E"], "M": pu.get("M"), "A": pu["A"], "P": pu.get("P"), "RK": pu["RK"],
                                   "desglose_ref": f"HT03-{run_id[4:]}-{f['opp_id'][4:]}"},
                  "horizontes": hz, "naturaleza_inversion": nat, "horizonte_principal": hp, "justificacion_horizonte": f.get("_just_hp"),
                  "valoracion": f.get("valoracion"),
                  "catalizadores": [x for x in (f.get("catalizadores") or []) if RE_FECHA_CAT.match(str(x.get("fecha", "")))],
                  "riesgos": f.get("riesgos") or ["riesgo de mercado"], "riesgo_1a5": int(sen.get("riesgo_1a5") or 3),
                  "invalidacion": f.get("invalidacion"), "ambito": _ambito(f, c), "indicador_seguimiento": _indicador(f, fuente),
                  "invertibilidad": _invertibilidad(f), "liquidez": liq,
                  "reversibilidad": liq, "que_cambiaria_la_conclusion": list(f.get("invalidacion") or [])[:2]
                  + [o["que_la_resolveria"] for o in f.get("_objeciones", []) if o.get("que_la_resolveria")][:2],
                  "objeciones": objs, "lo_que_no_sabemos": f.get("lo_que_no_sabemos"),
                  "confianza": "probable" if pu["E"] >= pres["confianza_probable_E"] else "especulativo", "evidencias": list(f.get("_evidencias") or []),
                  "calculos": calcs,
                  "minigrafico": {"tipo": "PRECIO_CON_ZONA", "serie_ref": f"HT01:{f['proxy']}",
                                  "zona_interes": {"min": round(precio * (1 - pres["zona_interes"]), 6), "max": round(precio * (1 + pres["zona_interes"]), 6),
                                                   "unidad": "nivel del indicador de seguimiento"},
                                  "calc_id": calcs[0]},
                  "x_referencia": f.get("_referencia"),
                  # campos que usa HT-09 (se eliminan del entregable JSON)
                  "puertas": f["_puertas"], "cluster": f["_cluster"], "vigente": bool(f.get("_vigente"))}
            p = bloque.params_ht03
            motivos = ht09.relevancia_esperada_alta(op, c, op["vigente"], p)
            op["relevancia_decisional"] = "ALTA" if motivos else ("BAJA" if f.get("_arrastre") else "MEDIA")
            if f.get("_veredicto") == "tesis frágil":
                # PA-05 (T-66): una tesis frágil según la regla de Contrarias es especulativa. La relevancia sigue la regla
                # del Anexo A (C10), que no tiene ese disparador (INC-T66-01)
                op["confianza"] = "especulativo"
            op["siguiente_paso_sugerido"] = _siguiente_paso(op, umbral_paso)
            if pu.get("T") == "NA":
                op["puntuaciones"]["T"] = "NA"
            if op["puntuaciones"].get("P") is None:
                op["puntuaciones"].pop("P")
            ej = [str(x) for x in (f.get("ejemplos_ilustrativos") or []) if isinstance(x, str) and len(x) >= 2][:8]
            if ej:
                op["ejemplos_ilustrativos"] = ej
            opciones.append(op)
            desgloses[f["opp_id"]] = {"dimensiones": f["dimensiones"], "segunda_pasada": f.get("segunda_pasada") or {},
                                      "saturacion_narrativa": bool(f.get("saturacion_narrativa"))}
            por_opp[f["opp_id"]] = f
            nivel_inv = {f"invalidacion_{i + 1}": {"valor": float(x["umbral"]), "unidad": f"nivel de {x.get('simbolo')}", "fecha_dato": str(as_of.date()),
                                                   "fuente": fuente} for i, x in enumerate(f.get("invalidacion_cuantitativa") or [])}
            # Encargo para el Bloque B (2.5 y Anexo B V5.0): el Bloque B localiza los mejores activos del ámbito
            b = {"opp_id": f["opp_id"], "tipo_activo": c, "subtipo": op["subtipo"], "tipo_opcion": op["tipo_opcion"], "nombre": op["nombre"],
                 "ambito": copy.deepcopy(op["ambito"]), "tesis": op["tesis"], "mecanismo": op["mecanismo"], "horizontes": sorted(hz),
                 "horizonte_principal": hp, "pronosticos": [hz[h]["prg_id"] for h in sorted(hz)], "catalizadores": copy.deepcopy(op["catalizadores"]),
                 "riesgos": op["riesgos"], "invalidacion": op["invalidacion"], "indicador_seguimiento": copy.deepcopy(op["indicador_seguimiento"]),
                 "niveles_referencia": {"nivel_actual": {"valor": precio, "unidad": "nivel del indicador de seguimiento",
                                                         "fecha_dato": sen.get("fecha_dato") or str(as_of.date()), "fuente": fuente}, **nivel_inv},
                 "criterios_seleccion_sugeridos": _lista(f, "criterios_seleccion_sugeridos",
                                                         [f"Activos con exposición alta y directa a «{op['nombre']}»",
                                                          "Liquidez suficiente para un inversor minorista europeo"]),
                 "metricas_clave": _lista(f, "metricas_clave", [f"Evolución de {op['indicador_seguimiento']['nombre']}",
                                                                "Condiciones de invalidación declaradas"]),
                 "preguntas_para_B": _lista(f, "preguntas_para_B", [f"¿Qué activos del ámbito capturan mejor la tesis «{(op['tesis'] or '')[:80]}»?"])}
            if op.get("ejemplos_ilustrativos"):
                b["ejemplos_ilustrativos"] = list(op["ejemplos_ilustrativos"])
            b.update({"evidencias": list(op["evidencias"]), "calculos": list(op["calculos"]),
                      "siguiente_paso_sugerido": op["siguiente_paso_sugerido"], "relevancia_decisional": op["relevancia_decisional"]})
            bloque_b.append(b)
        # finalistas no seleccionadas: pronósticos congelados con en_informe = false (aprendizaje sin sesgo de selección)
        sel_ids = {o["opp_id"] for o in opciones}
        for f in sel["candidatos"]:
            if f["opp_id"] not in sel_ids and not f.get("_arrastre") and f["_ht03"]["elegible"]:
                borradores(f, c, False)
        n = len(opciones)
        sem = _semaforo(opciones, umbral_sem)
        fins = an["finalistas"]
        clases_out[c] = {"estado_semaforo": sem,
                         "regimen_clase": (an.get("regimen") or "Régimen de la clase no disponible en este ciclo")[:600] if len(an.get("regimen") or "") >= 10 else "Régimen de la clase no disponible en este ciclo",
                         "candidatas_analizadas": max(len(an.get("cribado", [])), len(fins), len(sel["candidatos"]), n),
                         "embudo": {"gc0_delta_material": bool(gc0[c]["cambio_material"]), "cribadas": len(an.get("cribado", [])),
                                    "pasan_gc1": sum(1 for x in an.get("cribado", []) if x.get("paso_gc1")),
                                    "pasan_gc2": sum(1 for f in fins if f.get("_gc2")), "finalistas_gc3": min(sum(1 for f in fins if f.get("_gc3")), 5),
                                    "elegibles": sum(1 for e in sel["evaluadas"] if e["elegible"])},
                         "opciones": opciones, "menos_de_tres_motivo": _menos_de_tres_texto(c, sel, n)}
        paquete_clases[c] = [{"opp_id": o["opp_id"], "rango": o["rango"], "confianza": o["confianza"]} for o in opciones]

    todas = [o for c in clases_out for o in clases_out[c]["opciones"]]
    clust: dict = {}
    for o in todas:
        clust.setdefault(o["cluster_id"], []).append(o["opp_id"])
    fact = {str(x.get("cluster_id")): x.get("factor") for x in integ.get("factores_dominantes", []) if isinstance(x, dict)}
    clusteres_exp = [{"cluster_id": k if re.match(r"^CL-[0-9]{1,3}$", k) else "CL-99",
                      "factor_dominante": fact.get(k) or f"Factor común de las opciones del clúster {k} (correlación semanal ≥ 0,7, ML-CLUS-001)",
                      "opp_ids": v} for k, v in sorted(clust.items())]
    # Seguimiento de vigentes
    seguimiento = []
    f3 = bloque.almacen.estado("F3", as_of)
    sel_ids = {o["opp_id"] for o in todas}
    for c in clases:
        cerr = {x["opp_id"]: x for x in seleccion[c]["cerradas"]}
        for v in bloque.vigentes(as_of, c):
            dec = ((f3.get(v["opp_id"]) or {}).get("decision_broker") or {}).get("decision")
            if v["opp_id"] in sel_ids:
                seguimiento.append({"opp_id": v["opp_id"], "estado": "VIGENTE", "comentario": "Se mantiene en el top-3 (continuidad 9.6.4)", "decision_broker": dec})
            else:
                x = cerr.get(v["opp_id"], {"motivo_cierre": "SUSTITUCION", "comentario": "Sale del top-3: sustituida o ya no elegible"})
                seguimiento.append({"opp_id": v["opp_id"], "estado": "CERRADA", "motivo_cierre": x["motivo_cierre"], "comentario": x["comentario"], "decision_broker": dec})
    limit = [x for x in integ.get("limitaciones", []) if isinstance(x, str) and len(x) >= 5] + avisos_hp
    for c in clases:
        if analisis[c].get("estado") == "PARCIAL":
            limit.append(f"{NOMBRE_CLASE[c]}: alcance reducido declarado ({'; '.join(analisis[c].get('lagunas', [])[:2]) or 'salida parcial'})")
    for cz in presupuesto.cierres:
        limit.append(f"Presupuesto agotado en {cz['clase']} (fase {cz['fase']}): {cz['motivo']}; alcance reducido, controles intactos (R16)")
    if bloque.modo == "backtest":
        limit.append("Backtest: búsqueda web desactivada; evidencia limitada a datos HT-01 y referencias anteriores a la fecha as_of; "
                     "riesgo de fuga por conocimiento del modelo")
    if not limit:
        limit.append("Ninguna limitación adicional a las declaradas por opción")
    hist = copy.deepcopy(historial)
    paquete = {"run_id": run_id, "fecha": str(as_of.date()), "fecha_datos_mercado": max(fechas_dato) if fechas_dato else str(as_of.date()),
               "methodology_version": str(bloque.f10(as_of).get("P-30") or "4.0"), "tipo": tipo, "nivel_por_clase": nivel,
               "regimen_macro": integ.get("regimen_macro") if len(integ.get("regimen_macro") or "") >= 10 else "Régimen macro no disponible",
               "apuestas_independientes": len(clust), "clusteres_exposicion": clusteres_exp, "clases": clases_out,
               "seguimiento_vigentes": seguimiento, "historial_aciertos": hist, "paquete_para_bloque_B": bloque_b,
               "preguntas_sugeridas": [x for x in integ.get("preguntas_sugeridas", []) if isinstance(x, str) and len(x) >= 5][:6],
               "limitaciones": limit, "supuestos_declarados": bloque.consultas.supuestos_declarados(as_of, clases) if hasattr(bloque, "consultas") else [],
               "aviso_legal": AVISO_LEGAL,
               "x_lectura_conjunto": integ.get("lectura_conjunto", ""), "x_cambios_vs_anterior": integ.get("cambios_vs_anterior", ""),
               "x_n_efectivo": clusteres.get("n_efectivo")}
    extras = {"prg_borradores": prg_borradores, "desgloses": desgloses, "paquete_clases": paquete_clases, "por_opp": por_opp,
              "seleccion": seleccion, "analisis": analisis, "gc0": gc0}
    return paquete, extras


def ht09_validar(bloque, paquete: dict, extras: dict, informe_visual: str | None) -> dict:
    certs = [{"clase": c["celda"]["clase"], "horizonte": c["celda"]["horizonte"], "vigente": True, "metodo": None}
             for c in bloque.evaluador.certificados_vigentes(paquete["fecha"])]
    f2 = bloque.almacen.estado("F2", clave="clm_id")
    trazas = {k: v.get("evidencias", []) for k, v in f2.items() if v.get("tipo_entrada") == "CLM"}
    artef = [e["calc_id"] for e in bloque.almacen.leer("RC") if e.get("estado") in ("SERVED", "SERVED_WITH_LIMITATIONS")]
    return ht09.validar(paquete, certs, informe_visual, extras["desgloses"], bloque.params_ht03, trazas, artef,
                        float(parametro(bloque.cfg, "redaccion.umbral_fh")))


def retirar_opciones(bloque, paquete: dict, extras: dict, afectadas: set[str]) -> tuple[dict, dict]:
    """Retira las opciones con bloqueo G3 (se conservan sus pronósticos con en_informe = false) y reajusta el paquete."""
    p = copy.deepcopy(paquete)
    for c, d in p["clases"].items():
        quedan = [o for o in d["opciones"] if o["opp_id"] not in afectadas]
        if len(quedan) != len(d["opciones"]):
            for i, o in enumerate(quedan):
                o["rango"] = i + 1
            d["opciones"] = quedan
            d["estado_semaforo"] = "GRIS" if not quedan else d["estado_semaforo"]
            if len(quedan) < 3:
                d["menos_de_tres_motivo"] = ((d.get("menos_de_tres_motivo") or f"Se proponen {len(quedan)} opción(es).")
                                             + " Opciones retiradas por la validación G3: " + ", ".join(sorted(afectadas)) + ".")
            extras["paquete_clases"][c] = [{"opp_id": o["opp_id"], "rango": o["rango"], "confianza": o["confianza"]} for o in quedan]
    p["paquete_para_bloque_B"] = [b for b in p["paquete_para_bloque_B"] if b["opp_id"] not in afectadas]
    for e in p["clusteres_exposicion"]:
        e["opp_ids"] = [x for x in e["opp_ids"] if x not in afectadas]
    p["clusteres_exposicion"] = [e for e in p["clusteres_exposicion"] if e["opp_ids"]]
    p["apuestas_independientes"] = len(p["clusteres_exposicion"])
    for b in extras["prg_borradores"]:
        if b["opp_id"] in afectadas:
            b["en_informe"] = False
    for k in afectadas:
        extras["desgloses"].pop(k, None)
    p["limitaciones"].append(f"Opciones retiradas por bloqueo G3: {', '.join(sorted(afectadas))}")
    return p, extras


def mensaje_redactor(paquete: dict) -> dict:
    return {"run_id": paquete["run_id"], "fecha": paquete["fecha"], "apuestas_independientes": paquete["apuestas_independientes"],
            "historial_aciertos": paquete["historial_aciertos"].get("global"),
            "clases": {c: {"semaforo": d["estado_semaforo"], "n": len(d["opciones"]), "candidatas_analizadas": d["candidatas_analizadas"],
                           "menos_de_tres_motivo": d["menos_de_tres_motivo"],
                           "opciones": [{"opp_id": o["opp_id"], "nombre_llano": o["nombre_llano"], "tesis": o["tesis"], "riesgos": o["riesgos"][:2],
                                         "ambito": o["ambito"],
                                         "riesgo_1a5": o["riesgo_1a5"], "horizontes": sorted(o["horizontes"]),
                                         "banda": o["horizontes"][o["horizonte_principal"]]["banda"]} for o in d["opciones"]]}
                       for c, d in paquete["clases"].items()}}
