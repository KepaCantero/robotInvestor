"""Seguimiento encargado de opción (Documento 0 óptima V5.1: CT-24, ciclo C6, F11, 7.11, 14.4 y R27).

- El Broker da de alta, modifica, pausa, reanuda o cancela (con efecto inmediato) el seguimiento de una OPP- de F3.
- El Coordinador (AG-01) es el propietario de F11 y programa los ciclos con la frecuencia del encargo (HT-05).
- Cada ciclo C6 es una revisión ligera («N1 de seguimiento», 2 UC; ≤ 0,5 UC si no hay novedad): delta del
  indicador de seguimiento y de las señales de interés, distancia a las condiciones de invalidación, catalizadores,
  puntuaciones T/E/A/RK reconstruidas con HT-03 con los umbrales vigentes y estado de los pronósticos abiertos y de
  sus hitos H5, sin congelar pronósticos nuevos. Emite el informe de seguimiento de opción (breve + JSON), validado
  con HT-09 (perfil SEGUIMIENTO), con una sola recomendación.
- Estado de madurez (R22): la revisión del ejecutor es determinista (sin llamada al Analista de tipo de activo);
  el encargo CT-06 en fase SEGUIMIENTO queda registrado para trazabilidad.
"""
from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from .configuracion import parametro
from .herramientas import ht03, ht09
from .herramientas.ht01_datos import DatosNoDisponibles
from .redaccion import carpeta_bloqueados

FRECUENCIAS = ("DIARIA", "SEMANAL", "QUINCENAL", "MENSUAL", "TRIMESTRAL", "PERSONALIZADA")
ACCIONES = ("ALTA", "MODIFICACION", "PAUSA", "REANUDACION", "CANCELACION")


def _simbolo(opp: dict) -> str | None:
    ind = opp.get("indicador_seguimiento")
    if isinstance(ind, dict) and ind.get("simbolo"):
        return ind["simbolo"]
    return opp.get("simbolo_seguimiento") or opp.get("proxy_backtest")


class Seguimientos:
    def __init__(self, bloque) -> None:
        self.b = bloque
        self.cfg = bloque.cfg.get("seguimiento") or {}

    # ================================================================================ registro (F11)
    def encargos(self, as_of=None) -> dict[str, dict]:
        return {k: v for k, v in self.b.almacen.estado("F11", as_of).items() if v.get("opp_id")}

    def _dias(self, enc: dict) -> int:
        if enc.get("frecuencia") == "PERSONALIZADA":
            return max(1, int((enc.get("calendario_personalizado") or {}).get("cada_dias", 7)))
        return int((self.cfg.get("frecuencias") or {}).get(enc["frecuencia"], 7))

    def _proximo(self, enc: dict, desde) -> str:
        return str((pd.Timestamp(desde) + pd.Timedelta(days=self._dias(enc))).date())

    def procesar(self, ct24: dict, as_of=None) -> dict:
        """Entrada única del CT-24 (Broker → Coordinador); devuelve el acuse del mismo contrato."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        accion = ct24.get("accion")
        if accion not in ACCIONES:
            raise ValueError(f"Acción no válida {accion!r} (válidas: {', '.join(ACCIONES)})")
        msg = self.b.mensajeria.crear("CT-24", "BROKER", "AG-01", ct24, query_id=ct24.get("seg_id") or "SEG-ALTA")
        if accion == "ALTA":
            r = self._alta(ct24, as_of)
        else:
            r = self._cambio(ct24, accion, as_of)
        self.b.mensajeria.crear("CT-24", "AG-01", "BROKER", r, query_id=r["seg_id"], tipo_mensaje="RETORNO", estado="COMPLETO")
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "SEG_ACCION", "id": self.b.almacen.nuevo_id("F5SEG"), "seg_id": r["seg_id"],
                                                 "accion": accion, "msg_id": msg["msg_id"], "acuse": r})
        return r

    def _alta(self, ct24: dict, as_of) -> dict:
        opp_id = ct24.get("opp_id")
        f3 = self.b.almacen.estado("F3", as_of)
        if opp_id not in f3:
            raise KeyError(f"{opp_id} no está registrada en F3: solo se admite el seguimiento de una OPP- existente (7.11.2)")
        frec = ct24.get("frecuencia") or "SEMANAL"
        if frec not in FRECUENCIAS:
            raise ValueError(f"Frecuencia no válida {frec!r}")
        seg_id = self.b.almacen.nuevo_id("SEG")
        enc = {"tipo_entrada": "ALTA", "seg_id": seg_id, "opp_id": opp_id, "clase": f3[opp_id].get("clase"), "frecuencia": frec,
               "calendario_personalizado": ct24.get("calendario_personalizado"), "motivo": ct24.get("motivo") or "",
               "senales_interes": list(ct24.get("senales_interes") or []), "fecha_fin": ct24.get("fecha_fin"), "estado": "ACTIVO",
               "fecha_alta": str(as_of.date()), "ciclos": 0}
        enc["proximo_ciclo"] = self._proximo(enc, as_of)
        aviso = None
        hp = f3[opp_id].get("horizonte_principal") or "H3"
        orient = int((self.cfg.get("frecuencia_orientativa_dias") or {}).get(hp, 7))
        if self._dias(enc) < orient:
            aviso = (f"Frecuencia más corta de lo que tiene sentido para el horizonte principal {hp} de la opción: "
                     "se acepta, y los ciclos sin cambio material serán «sin novedad» (7.11.2)")
        enc["aviso"] = aviso
        self.b.almacen.escribir("F11", "AG-01", enc)
        # Anotación en F3 a través del Analizador (propietario de F3): decision_broker = EN_SEGUIMIENTO y seg_id
        self.b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": opp_id, "seg_id": seg_id,
                                                 "decision_broker": {"decision": "EN_SEGUIMIENTO", "motivo": enc["motivo"],
                                                                     "fecha": str(as_of.date()), "seg_id": seg_id}})
        return {"seg_id": seg_id, "estado": "ACTIVO", "proximo_ciclo": enc["proximo_ciclo"], "aviso": aviso}

    def _cambio(self, ct24: dict, accion: str, as_of) -> dict:
        seg_id = ct24.get("seg_id")
        enc = self.encargos().get(seg_id)
        if not enc:
            raise KeyError(f"Encargo desconocido {seg_id}")
        if enc["estado"] in ("CANCELADO", "FINALIZADO"):
            raise ValueError(f"{seg_id} está {enc['estado']}: no admite {accion}")
        e = {"tipo_entrada": accion, "seg_id": seg_id}
        if accion == "MODIFICACION":
            for k in ("frecuencia", "calendario_personalizado", "motivo", "senales_interes", "fecha_fin"):
                if k in ct24 and ct24[k] is not None:
                    e[k] = ct24[k]
            if e.get("frecuencia") and e["frecuencia"] not in FRECUENCIAS:
                raise ValueError(f"Frecuencia no válida {e['frecuencia']!r}")
            if enc["estado"] == "ACTIVO":
                e["proximo_ciclo"] = self._proximo({**enc, **e}, as_of)
        elif accion == "PAUSA":
            e.update({"estado": "PAUSADO", "proximo_ciclo": None})
        elif accion == "REANUDACION":
            e.update({"estado": "ACTIVO", "proximo_ciclo": self._proximo(enc, as_of)})
        elif accion == "CANCELACION":
            # Efecto inmediato (R27): se anulan los ciclos programados; un ciclo en curso se detiene en su siguiente punto de control
            e.update({"estado": "CANCELADO", "proximo_ciclo": None, "fecha_cancelacion": str(as_of.date())})
        self.b.almacen.escribir("F11", "AG-01", e)
        nuevo = {**enc, **e}
        return {"seg_id": seg_id, "estado": nuevo["estado"], "proximo_ciclo": nuevo.get("proximo_ciclo"), "aviso": None}

    def respuesta_broker(self, seg_id: str, decision: str, run_id: str | None = None, as_of=None) -> dict:
        """Decisión del Broker sobre la recomendación de un ciclo: F11, F5 y CT-22 DECISION_SEGUIMIENTO al Evaluador."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        enc = self.encargos().get(seg_id)
        if not enc:
            raise KeyError(f"Encargo desconocido {seg_id}")
        self.b.almacen.escribir("F11", "AG-01", {"tipo_entrada": "RESPUESTA_BROKER", "seg_id": seg_id, "respuesta_broker":
                                                  {"run_id": run_id or enc.get("ultimo_run_id"), "decision": decision, "fecha": str(as_of.date())}})
        self.b.mensajeria.crear("CT-22", "AG-01", "AG-20", {"tipo_aviso": "DECISION_SEGUIMIENTO", "seg_id": seg_id, "opp_id": enc["opp_id"],
                                                            "recomendacion": enc.get("ultima_recomendacion"), "decision_seguimiento": decision},
                                query_id=seg_id)
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "AVISO_CT22", "id": self.b.almacen.nuevo_id("F5AV"),
                                                 "tipo_aviso": "DECISION_SEGUIMIENTO", "seg_id": seg_id, "decision": decision})
        return {"seg_id": seg_id, "decision": decision}

    # ================================================================================ ejecución (HT-05)
    def pendientes(self, as_of) -> list[dict]:
        as_of = pd.Timestamp(as_of)
        out = []
        for k, e in sorted(self.encargos().items()):
            if e["estado"] != "ACTIVO":
                continue
            if e.get("fecha_fin") and pd.Timestamp(e["fecha_fin"]) < as_of:
                self.b.almacen.escribir("F11", "AG-01", {"tipo_entrada": "FIN", "seg_id": k, "estado": "FINALIZADO", "proximo_ciclo": None})
                self.b.mensajeria.crear("CT-24", "AG-01", "BROKER", {"seg_id": k, "estado": "FINALIZADO", "proximo_ciclo": None,
                                                                     "aviso": "Fecha de fin alcanzada"}, query_id=k, tipo_mensaje="RETORNO")
                continue
            if e.get("proximo_ciclo") and pd.Timestamp(e["proximo_ciclo"]) <= as_of:
                out.append(e)
        return out

    def ejecutar(self, as_of=None, seg_id: str | None = None, forzar: bool = False) -> list[dict]:
        """Ejecuta los ciclos C6 vencidos (o uno concreto con `forzar`). Prioridad inferior a C1–C3: se llama fuera de ellos."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        if seg_id:
            enc = self.encargos().get(seg_id)
            if not enc:
                raise KeyError(f"Encargo desconocido {seg_id}")
            if enc["estado"] != "ACTIVO":
                return [{"seg_id": seg_id, "estado": enc["estado"], "ejecutado": False, "motivo": f"Encargo {enc['estado']}"}]
            lista = [enc] if forzar or seg_id in {e["seg_id"] for e in self.pendientes(as_of)} else []
        else:
            lista = self.pendientes(as_of)
        return [self.ciclo_c6(e, as_of) for e in lista]

    # ================================================================================ ciclo C6
    def ciclo_c6(self, enc: dict, as_of) -> dict:
        b, seg_id, opp_id = self.b, enc["seg_id"], enc["opp_id"]
        opp = b.almacen.estado("F3", as_of).get(opp_id) or {}
        clase = opp.get("clase") or enc.get("clase")
        # Absorción en C1 (7.11.5): si la opción vuelve a estar VIGENTE en el top-3, el ciclo se omite
        if opp.get("estado") == "VIGENTE":
            b.almacen.escribir("F11", "AG-01", {"tipo_entrada": "CICLO_OMITIDO", "seg_id": seg_id, "fecha": str(as_of.date()),
                                                 "motivo": "cubierto en C1: la opción está en el top-3", "proximo_ciclo": self._proximo(enc, as_of)})
            return {"seg_id": seg_id, "ejecutado": False, "motivo": "cubierto en C1"}
        run_id = b.almacen.nuevo_id("RUN")
        n_ciclo = int(enc.get("ciclos") or 0) + 1
        b.mensajeria.crear("CT-05", "AG-01", "AG-02", {"tipo": "SEGUIMIENTO", "seg_id": seg_id, "opp_id": opp_id,
                                                       "alcance": {"clases": [clase], "opp_id": opp_id}, "nivel_por_clase": {clase: "N1"},
                                                       "presupuesto_por_clase": {clase: float(parametro(b.cfg, "seguimiento.presupuesto_uc.normal"))},
                                                       "memoria": {"senales_interes": enc.get("senales_interes", [])}, "delta_gc0": {},
                                                       "fecha_objetivo": str(as_of.date())}, run_id=run_id, presupuesto={"uc": float(parametro(b.cfg, "seguimiento.presupuesto_uc.normal"))})
        b.mensajeria.crear("CT-06", "AG-02", b_agente(clase), {"clase": clase, "fase": "SEGUIMIENTO", "nivel": "N1",
                                                                "opciones_vigentes": [opp_id], "lecciones": [], "seg_id": seg_id,
                                                                "senales_interes": enc.get("senales_interes", [])},
                           run_id=run_id, presupuesto={"uc": float(parametro(b.cfg, "seguimiento.presupuesto_uc.normal"))})
        rev = self._revision(enc, opp, as_of)
        informe = self._informe(enc, opp, rev, run_id, n_ciclo, as_of)
        texto = self._texto(informe, opp)
        val = ht09.validar_seguimiento(informe, {"umbrales": b.params_ht03["umbrales"], "pesos_rk": b.params_ht03["pesos_rk"]}, texto)
        errores_esquema = _errores_esquema_seguimiento(b, informe)
        if errores_esquema:      # el informe C6 se valida contra su esquema V5.1 antes de entregarse
            val = dict(val, dictamen="BLOQUEADO", errores_esquema=errores_esquema)
        base = Path(b.carpeta_entregables) / ("Informes de seguimiento" if b.modo != "backtest" else str(as_of.date()))
        if val["dictamen"] == "BLOQUEADO":   # lo bloqueado no llega a la carpeta de entrega (G3)
            base = carpeta_bloqueados(b, as_of, run_id)   # la misma que la redacción (T-65, H-10 b)
        base.mkdir(parents=True, exist_ok=True)
        nombre = f"{as_of.date()}_informe-seguimiento_{run_id}"
        rutas = {"informe": str(base / f"{nombre}.md"), "json": str(base / f"{nombre}.json")}
        Path(rutas["json"]).write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
        Path(rutas["informe"]).write_text(texto, encoding="utf-8")
        entregado = val["dictamen"] != "BLOQUEADO"
        b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "G3V", "id": f"G3V-{run_id[4:]}-C6", "run_id": run_id, "fase": "C6",
                                           "tipo_control": "SINCRONO_DETERMINISTA", "dictamen_ht09": val["dictamen"],
                                           "comprobaciones": [{"id": c["id"], "resultado": c["resultado"]} for c in val["comprobaciones"]]})
        uc = float(parametro(b.cfg, "seguimiento.presupuesto_uc.sin_novedad")) if rev["sin_novedad"] else float(parametro(b.cfg, "seguimiento.presupuesto_uc." + ("material" if rev["material"] else "normal")))
        b.almacen.escribir("F11", "AG-01", {"tipo_entrada": "CICLO", "seg_id": seg_id, "ciclos": n_ciclo, "ultimo_run_id": run_id,
                                             "ultima_fecha": str(as_of.date()), "ultima_recomendacion": informe["recomendacion"],
                                             "ultimo_semaforo": informe["semaforo"], "ultimo_RK": informe["puntuaciones"].get("RK"),
                                             "ultimo_precio": rev.get("precio"), "sin_novedad_consecutivos": rev["sin_novedad_consecutivos"],
                                             "ciclo": {"n": n_ciclo, "run_id": run_id, "fecha": str(as_of.date()), "semaforo": informe["semaforo"],
                                                       "recomendacion": informe["recomendacion"], "ruta": rutas["informe"], "g3": val["dictamen"],
                                                       "entregado": entregado, "respuesta_broker": None},
                                             "proximo_ciclo": self._proximo(enc, as_of)})
        b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN_C6", "id": run_id, "run_id": run_id, "tipo": "SEGUIMIENTO", "seg_id": seg_id,
                                            "opp_id": opp_id, "clase": clase, "nivel": "N1 de seguimiento", "consumo": {"uc": uc},
                                            "entregables": rutas, "g3": val["dictamen"], "recomendacion": informe["recomendacion"],
                                            "entrega": "ENTREGADA" if entregado else "BLOQUEADA"})
        if informe["recomendacion"] == "CERRAR" and rev["invalidacion_activada"]:
            b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": opp_id, "estado": "CERRADA",
                                               "cierre": {"fecha": str(as_of.date()), "motivo": "INVALIDACION", "comentario": f"Verificada en el ciclo C6 {run_id}"},
                                               "run_ids_cierre": [run_id]})
        if entregado:
            b.mensajeria.crear("CT-24", "AG-01", "BROKER", {"seg_id": seg_id, "estado": "ACTIVO", "run_id": run_id, "informe": rutas,
                                                            "recomendacion": informe["recomendacion"], "semaforo": informe["semaforo"]},
                               query_id=seg_id, tipo_mensaje="RETORNO", estado="COMPLETO")
        return {"seg_id": seg_id, "run_id": run_id, "ejecutado": True, "entregado": entregado, "g3": val["dictamen"],
                "recomendacion": informe["recomendacion"], "semaforo": informe["semaforo"], "sin_novedad": rev["sin_novedad"],
                "rutas": rutas, "informe": informe, "validacion": val}

    # -------------------------------------------------------------------------------- revisión ligera
    def _revision(self, enc: dict, opp: dict, as_of) -> dict:
        b = self.b
        sym = _simbolo(opp)
        desde = pd.Timestamp(enc.get("ultima_fecha") or enc.get("fecha_alta") or as_of)
        rev: dict = {"limitaciones": [], "precio": None, "delta": None, "material": False}
        try:
            fd, precio = b.proveedor.valor_en(sym, as_of)
            rev.update({"precio": precio, "fecha_dato": str(fd.date())})
            # T-65 (CA-14 de T-53): ventana de σ y mínimo de semanas de la configuración; sin σ estimable, el delta cuenta
            # como material (revisión completa) y se declara, en lugar de un umbral inventado del 5 %
            serie = b.proveedor.cierres(sym, as_of - pd.Timedelta(weeks=int(parametro(b.cfg, "gc0.ventana_sigma_semanas"))), as_of)
            semanal = serie.resample("W").last().pct_change().dropna()
            min_sem = int(parametro(b.cfg, "seguimiento.min_semanas_sigma"))
            sd = float(semanal.std()) if len(semanal) >= min_sem else float("nan")
            previo = enc.get("ultimo_precio") or float(b.proveedor.valor_en(sym, desde)[1])
            delta = precio / previo - 1 if previo else 0.0
            semanas = max((as_of - desde).days / 7, 1)
            if math.isfinite(sd):
                umbral = float(parametro(b.cfg, "gc0.sigma_semanal")) * sd * np.sqrt(semanas)
                rev.update({"delta": round(delta, 4), "material": bool(abs(delta) > umbral), "umbral_material": round(umbral, 4)})
            else:
                rev.update({"delta": round(delta, 4), "material": True, "umbral_material": None})
                rev["limitaciones"].append(f"σ semanal de {sym} no estimable (menos de {min_sem} semanas): el delta se trata "
                                           "como material (falla cerrado)")
        except DatosNoDisponibles as e:
            rev["limitaciones"].append(f"HT-01 sin datos de {sym}: revisión degradada y declarada ({e})")
        # Condiciones de invalidación y su distancia
        inval, activada, cercana = [], False, False
        cuant = {i: x for i, x in enumerate(opp.get("invalidacion_cuantitativa") or [])}
        for i, texto in enumerate(opp.get("invalidacion") or []):
            x = cuant.get(i)
            item = {"condicion": texto, "distancia": "no cuantificada", "activada": False}
            if x and rev["precio"]:
                try:
                    p_x = float(b.proveedor.valor_en(x.get("simbolo") or sym, as_of)[1])
                    dist = (p_x - float(x["umbral"])) / p_x if x.get("direccion", "por_debajo") == "por_debajo" else (float(x["umbral"]) - p_x) / p_x
                    item.update({"distancia": f"{dist:.1%}", "activada": dist <= 0})
                    activada |= dist <= 0
                    cercana |= 0 < dist < float(parametro(b.cfg, "gc0.invalidacion_cercana"))
                except DatosNoDisponibles:
                    pass
            inval.append(item)
        rev.update({"invalidacion": inval, "invalidacion_activada": activada, "invalidacion_cercana": cercana})
        # Catalizadores
        cats, ocurrido_nuevo = [], False
        for c in opp.get("catalizadores") or []:
            f = str(c.get("fecha", ""))
            try:
                fc = pd.Timestamp(f + ("-28" if len(f) == 7 else ""))
            except ValueError:
                fc = None
            estado = "OCURRIDO" if fc is not None and fc <= as_of else "PENDIENTE"
            ocurrido_nuevo |= estado == "OCURRIDO" and fc is not None and fc > desde
            cats.append({"evento": c.get("evento"), "fecha": f, "estado": estado})
        rev["catalizadores"] = cats
        # Puntuaciones reconstruidas con HT-03 y umbrales vigentes (sin cambio de dimensiones: revisión ligera)
        pu_prev = opp.get("puntuaciones_totales") or {}
        if opp.get("dimensiones"):
            ev = ht03.evaluar_opcion({"opp_id": opp.get("opp_id"), "clase": opp.get("clase"), "dimensiones": opp["dimensiones"],
                                      "segunda_pasada": opp.get("segunda_pasada") or {}}, b.params_ht03)
            pu = {k: ev["puntuaciones"].get(k) for k in ("T", "E", "A", "RK")}
            # Elegibilidad de 9.2 con los umbrales vigentes de F10 (7.11.4)
            u = b.params_ht03["umbrales"]
            T, E, A = pu.get("T"), pu.get("E"), pu.get("A")
            if isinstance(E, (int, float)) and isinstance(A, (int, float)):
                elegible = E >= u["E"] and ((A >= u["A_si_T_NA"]) if T == "NA" or T is None else (A >= u["A"] and T >= u["T"]))
            else:
                elegible = False
        else:
            pu, elegible = {k: pu_prev.get(k) for k in ("T", "E", "A", "RK")}, bool(opp.get("elegible"))
            rev["limitaciones"].append("Ficha sin dimensiones: puntuaciones de la última revisión")
        rk_ant = enc.get("ultimo_RK") if enc.get("ultimo_RK") is not None else pu_prev.get("RK")
        pu["variacion_RK"] = (pu["RK"] - rk_ant) if isinstance(pu.get("RK"), (int, float)) and isinstance(rk_ant, (int, float)) else 0
        pu["elegible"] = elegible
        rev["puntuaciones"] = pu
        rev["objeciones_fuertes_abiertas"] = [o.get("objecion_id") for o in (opp.get("objeciones_internas") or [])
                                              if o.get("fuerza") == "fuerte" and not o.get("resuelta")]
        # Pronósticos abiertos e hitos (sin congelar nuevos)
        f4 = b.almacen.estado("F4", as_of)
        pron = []
        for p in sorted(f4.values(), key=lambda x: x["prg_id"]):
            if p.get("opp_id") != opp.get("opp_id") or p.get("es_hito") or p.get("tipo_entrada") not in ("ALTA", "RESOLUCION"):
                continue
            if p.get("estado") not in ("ABIERTO", "RESUELTO"):
                continue
            hitos = [{"hit_id": h, "fecha": (f4.get(h) or {}).get("fecha_resolucion"),
                      "estado": {"ABIERTO": "PENDIENTE", "RESUELTO": "CUMPLIDO" if ((f4.get(h) or {}).get("resolucion") or {}).get("resultado_binario")
                                 else "FALLADO"}.get((f4.get(h) or {}).get("estado"), "PENDIENTE")} for h in p.get("hit_ids", [])]
            estado = "EN_CURSO" if p.get("estado") == "ABIERTO" else "RESUELTO"
            if p.get("horizonte") == "H5":
                estado = (b.evaluador.estado_h5(as_of)["pronosticos"].get(p["prg_id"]) or {}).get("estado", "EN_CURSO_CONFORME")
            pron.append({"prg_id": p["prg_id"], "horizonte": p.get("horizonte"), "estado": estado, "hitos": hitos})
        rev["pronosticos_abiertos"] = [x for x in pron if x["estado"] != "RESUELTO"]
        # Sin novedad: ningún cambio material en precio, invalidación ni catalizadores
        rev["sin_novedad"] = not (rev["material"] or activada or cercana or ocurrido_nuevo)
        rev["sin_novedad_consecutivos"] = (int(enc.get("sin_novedad_consecutivos") or 0) + 1) if rev["sin_novedad"] else 0
        return rev

    def _recomendacion(self, rev: dict, opp: dict, as_of) -> (str, str):
        hp_vence = False
        pend_cat = any(c["estado"] == "PENDIENTE" for c in rev["catalizadores"])
        if rev["invalidacion_activada"]:
            return "CERRAR", "Se ha activado una condición de invalidación verificada con datos de HT-01."
        if rev["pronosticos_abiertos"] == [] and opp.get("horizontes_prg"):
            hp_vence = True
        if hp_vence:
            return "CERRAR", "Vence el horizonte: todos los pronósticos de la opción están resueltos."
        pu = rev["puntuaciones"]
        if pu.get("elegible") and not rev["objeciones_fuertes_abiertas"] and not rev["sin_novedad"] and pu.get("variacion_RK", 0) >= 0:
            return "PROPONER_ENVIO_A_B", "La opción vuelve a ser elegible con las puntuaciones actualizadas y sin objeciones fuertes abiertas."
        n = int(parametro(self.b.cfg, "seguimiento.ciclos_sin_novedad_para_proponer_cancelacion"))
        if rev["sin_novedad_consecutivos"] >= n and not pend_cat:
            return "PROPONER_CANCELACION", f"{rev['sin_novedad_consecutivos']} ciclos seguidos sin novedad y sin catalizadores pendientes."
        return "MANTENER_VIGILANCIA", "Sin cambio suficiente para proponer el envío al Bloque B; se mantiene la vigilancia."

    def _informe(self, enc: dict, opp: dict, rev: dict, run_id: str, n: int, as_of) -> dict:
        rec, motivo = self._recomendacion(rev, opp, as_of)
        umbral = float(parametro(self.b.cfg, "seguimiento.umbral_rk_semaforo"))
        var = rev["puntuaciones"].get("variacion_RK") or 0
        if rev["invalidacion_activada"] or rev["invalidacion_cercana"] or var <= -umbral:
            sem = "ROJO"
        elif var >= umbral or (rev["delta"] or 0) > 0 and rev["material"]:
            sem = "VERDE"
        else:
            sem = "AMBAR"
        cambios = []
        if rev["delta"] is not None:
            cambios.append(f"El indicador de seguimiento varía {rev['delta']:+.1%} desde el ciclo anterior"
                           + (" (cambio material)" if rev["material"] else " (dentro de su banda normal)"))
        cambios += [f"Catalizador ocurrido: {c['evento']} ({c['fecha']})" for c in rev["catalizadores"] if c["estado"] == "OCURRIDO"]
        if var:
            cambios.append(f"RK {var:+} puntos")
        paquete_b = None
        if rec == "PROPONER_ENVIO_A_B":
            hz = opp.get("horizontes_prg") or {}
            paquete_b = {"opp_id": opp["opp_id"], "tipo_activo": opp.get("clase"), "subtipo": opp.get("subtipo") or "Ámbito",
                         "ambito": opp.get("ambito"), "tesis": opp.get("tesis"), "mecanismo": opp.get("mecanismo"),
                         "horizonte_principal": opp.get("horizonte_principal"), "horizontes": sorted(hz),
                         "pronosticos": [v["prg_id"] for v in hz.values()], "catalizadores": opp.get("catalizadores") or [],
                         "riesgos": opp.get("riesgos") or [], "invalidacion": opp.get("invalidacion") or [],
                         "indicador_seguimiento": opp.get("indicador_seguimiento"),
                         "criterios_seleccion_sugeridos": opp.get("criterios_seleccion_sugeridos") or [],
                         "metricas_clave": opp.get("metricas_clave") or [], "preguntas_para_B": opp.get("preguntas_para_B") or [],
                         "evidencias": opp.get("evidencias") or [], "calculos": []}
        sugerir_n3 = rec == "PROPONER_ENVIO_A_B" and (rev["material"] or (pd.Timestamp(as_of) - pd.Timestamp(opp.get("_ultima_fecha") or as_of)).days > 30)
        return {"seg_id": enc["seg_id"], "opp_id": opp.get("opp_id"), "run_id": run_id, "ciclo": n, "fecha": str(pd.Timestamp(as_of).date()),
                "tipo_activo": opp.get("clase"), "horizonte_principal": opp.get("horizonte_principal") or "H3",
                "sin_novedad": rev["sin_novedad"], "semaforo": sem, "que_ha_cambiado": cambios or ["Sin novedad material"],
                "senales_interes": [{"senal": s, "estado": "sin dato estructurado en el ejecutor: revisar en el informe técnico de la opción"}
                                    for s in enc.get("senales_interes", [])],
                "invalidacion": rev["invalidacion"], "catalizadores": rev["catalizadores"], "puntuaciones": rev["puntuaciones"],
                "objeciones_fuertes_abiertas": rev["objeciones_fuertes_abiertas"],
                "pronosticos_abiertos": rev["pronosticos_abiertos"], "recomendacion": rec, "motivo": motivo,
                "sugerir_profundizacion_N3": bool(sugerir_n3), "paquete_para_bloque_B": paquete_b,
                "supuestos_declarados": self.b.consultas.supuestos_declarados(as_of, [opp.get("clase")]) if hasattr(self.b, "consultas") else [],
                "limitaciones": rev["limitaciones"] + ["Revisión ligera determinista del ejecutor (N1 de seguimiento): puntuaciones reconstruidas "
                                                       "con HT-03 sobre las dimensiones de la última revisión; no se congelan pronósticos nuevos"]}

    def _texto(self, inf: dict, opp: dict) -> str:
        sem = {"VERDE": "🟢 Verde", "AMBAR": "🟡 Ámbar", "ROJO": "🔴 Rojo"}[inf["semaforo"]]
        lin = [f"# Informe de seguimiento de opción · {inf['seg_id']} · ciclo {inf['ciclo']}", "",
               f"**{opp.get('nombre') or inf['opp_id']}** (`{inf['opp_id']}`, {inf['tipo_activo']}) · {inf['fecha']} · `{inf['run_id']}` · "
               f"horizonte principal {inf['horizonte_principal']}", ""]
        if inf["sin_novedad"]:
            lin += [f"**Sin novedad.** Semáforo {sem}. Recomendación: **{inf['recomendacion']}**. {inf['motivo']}", ""]
        else:
            pu = inf["puntuaciones"]
            lin += [f"**Semáforo:** {sem} · **Recomendación:** **{inf['recomendacion']}** — {inf['motivo']}", "",
                    "**Qué ha cambiado.** " + "; ".join(inf["que_ha_cambiado"]) + ".", "",
                    f"**Puntuaciones.** T {pu.get('T')} · E {pu.get('E')} · A {pu.get('A')} · RK {pu.get('RK')} ({pu.get('variacion_RK', 0):+}) · "
                    f"elegible: {'sí' if pu.get('elegible') else 'no'}.", "",
                    "**Invalidación.** " + "; ".join(f"{i['condicion']} (distancia {i['distancia']})" for i in inf["invalidacion"]) + ".", "",
                    "**Catalizadores.** " + ("; ".join(f"{c['evento']} {c['fecha']}: {c['estado']}" for c in inf["catalizadores"]) or "ninguno") + ".", "",
                    "**Pronósticos abiertos.** " + ("; ".join(f"{p['prg_id']} ({p['horizonte']}): {p['estado']}" for p in inf["pronosticos_abiertos"]) or "ninguno") + "."]
            if inf["sugerir_profundizacion_N3"]:
                lin += ["", "Antes del envío al Bloque B se sugiere una profundización N3."]
        if inf["supuestos_declarados"]:
            lin += ["", "**Supuestos declarados.** " + "; ".join(f"{s['supuesto']} ({s['cns_id']})" for s in inf["supuestos_declarados"])]
        lin += ["", "_Esto no es una recomendación personal; la decisión es del Broker Personal._", ""]
        return "\n".join(lin)


def b_agente(clase: str) -> str:
    from .contratos import AGENTE_CLASE
    return AGENTE_CLASE.get(clase, "AG-03")


def _errores_esquema_seguimiento(b, informe: dict) -> list[str]:
    """Errores del informe C6 frente al esquema «Informe de seguimiento de opción» (V5.1) de las plantillas."""
    import jsonschema

    from .configuracion import buscar_versionado, ruta
    esquema = buscar_versionado(ruta(b.cfg, "plantillas"), "Esquema JSON - Informe de seguimiento de opción", ".json")
    if esquema is None:
        return ["no se encuentra el esquema JSON del informe de seguimiento de opción"]
    validador = jsonschema.Draft202012Validator(json.loads(Path(esquema).read_text(encoding="utf-8")))
    return [f"{'/'.join(map(str, e.absolute_path))}: {e.message}"[:200] for e in validador.iter_errors(informe)][:10]
