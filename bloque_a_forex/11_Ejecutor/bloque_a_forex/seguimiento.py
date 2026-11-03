"""Seguimiento encargado de opción (CT-24, ciclo C6 y F11) — Documento 0 Forex V1.1, R27, 7.11 y 14.4.

El Broker encarga por CT-24 el seguimiento periódico de una OPP-FX- que no envió al Bloque B (alta, modificación, pausa,
reanudación y **cancelación en cualquier momento**). El Coordinador (AG-01) lo registra en F11 (SEG-FX-), lo programa con
HT-05 y, en cada ciclo C6, ordena una revisión ligera («N1 de seguimiento») al Analizador, que la encarga al Analista del
segmento (CT-06 fase SEGUIMIENTO). El ciclo produce el **informe de seguimiento de opción** (breve + JSON), que HT-09 valida
(`validar_seguimiento`) y el Coordinador entrega por CT-24.

En el ejecutor la revisión de cada ciclo es **determinista** (HT-01 + HT-03, sin llamada al modelo): delta del indicador,
distancia a las condiciones de invalidación, catalizadores, puntuaciones T/E/A/RK recalculadas con HT-03 a partir de las
dimensiones de F3 (actualidad y asimetría ajustadas por el tiempo y el movimiento), pronósticos abiertos de F4 y sus hitos
H5 (resultados en F6). Estado de madurez (R22): implementado con pruebas; la redacción narrativa del Analista con el modelo
real no está conectada (declarado en `limitaciones`).
"""
from __future__ import annotations

import copy
import json
import math
import re
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from . import horizontes as hzn
from .contratos import AGENTE_SEGMENTO
from .herramientas import ht03, ht09
from .herramientas.ht01_datos import DatosNoDisponibles
from .herramientas.ht05_planificador import FRECUENCIAS_SEGUIMIENTO, proximo_ciclo_seguimiento

ACCIONES = ("ALTA", "MODIFICACION", "PAUSA", "REANUDACION", "CANCELACION")
CARPETA_INFORMES = "Informes de seguimiento"
RE_SENAL = re.compile(r"(?i)\b(por debajo|por encima)\s+de\s+([0-9]+(?:[.,][0-9]+)?)")


def _r10(x: float) -> int:
    return int(max(0, min(100, round(x / 10.0) * 10)))


class Seguimientos:
    def __init__(self, bloque) -> None:
        self.b = bloque
        cfg = bloque.cfg.get("seguimiento") or {}
        self.uc_ciclo = float(cfg.get("uc_ciclo", 2))
        self.uc_material = float(cfg.get("uc_material", 5))
        self.uc_sin_novedad = float(cfg.get("uc_sin_novedad", 0.5))
        self.ciclos_sin_novedad_cancelar = int(cfg.get("ciclos_sin_novedad_para_proponer_cancelacion", 6))

    # ================================================================================
    # Registro F11
    # ================================================================================
    def encargos(self, as_of=None) -> Dict[str, Dict]:
        return self.b.almacen.estado("F11", as_of)

    def _f11(self, entrada: Dict) -> Dict:
        return self.b.almacen.escribir("F11", "AG-01", entrada)

    def _acuse(self, seg: Dict, aviso: Optional[str] = None) -> Dict:
        cuerpo = {"seg_id": seg["seg_id"], "estado_encargo": seg["estado"], "proximo_ciclo": seg.get("proximo_ciclo"), "aviso": aviso}
        self.b.mensajeria.crear("CT-24", "AG-01", "BROKER", cuerpo, tipo_mensaje="RETORNO", estado="COMPLETO")
        return {"seg_id": seg["seg_id"], "estado": seg["estado"], "proximo_ciclo": seg.get("proximo_ciclo"), "aviso": aviso}

    def tramitar(self, ct24: Dict, as_of=None) -> Dict:
        """Punto de entrada del CT-24 (Broker → Coordinador)."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        accion = str(ct24.get("accion") or "").upper()
        if accion not in ACCIONES:
            raise ValueError(f"Acción CT-24 no válida {accion!r} ({', '.join(ACCIONES)})")
        if accion == "ALTA":
            return self.alta(ct24, as_of)
        seg_id = ct24.get("seg_id")
        segs = self.encargos(as_of)
        if seg_id not in segs:
            raise KeyError(f"Encargo {seg_id} no encontrado en F11")
        seg = segs[seg_id]
        self.b.mensajeria.crear("CT-24", "BROKER", "AG-01", {**ct24, "opp_id": seg["opp_id"]})
        if seg["estado"] in ("CANCELADO", "FINALIZADO"):
            return {**self._acuse(seg), "aviso": f"El encargo ya estaba {seg['estado'].lower()}"}
        nuevo: Dict = {"tipo_entrada": accion, "seg_id": seg_id, "fecha": str(as_of.date())}
        aviso = None
        if accion == "MODIFICACION":
            for k in ("frecuencia", "calendario_personalizado", "senales_interes", "fecha_fin", "motivo"):
                if k in ct24:
                    nuevo[k] = ct24[k]
            if "frecuencia" in nuevo and str(nuevo["frecuencia"]).upper() not in FRECUENCIAS_SEGUIMIENTO:
                raise ValueError(f"Frecuencia no válida {nuevo['frecuencia']!r}")
            frec = str(nuevo.get("frecuencia", seg["frecuencia"])).upper()
            nuevo["frecuencia"] = frec
            ref = seg.get("ultimo_ciclo") or str(as_of.date())
            prox = proximo_ciclo_seguimiento(ref, frec, nuevo.get("calendario_personalizado", seg.get("calendario_personalizado")))
            nuevo["proximo_ciclo"] = str(prox.date()) if prox is not None else None
            aviso = hzn.aviso_frecuencia(frec, seg.get("horizonte_principal"))
            nuevo["aviso"] = aviso
        elif accion == "PAUSA":
            nuevo.update({"estado": "PAUSADO", "proximo_ciclo": None})
        elif accion == "REANUDACION":
            prox = proximo_ciclo_seguimiento(as_of, seg["frecuencia"], seg.get("calendario_personalizado"))
            nuevo.update({"estado": "ACTIVO", "proximo_ciclo": str(prox.date()) if prox is not None else None})
        elif accion == "CANCELACION":
            # Efecto inmediato (R27): no se programan más ciclos y el ciclo en curso se detiene en su siguiente punto de control
            nuevo.update({"estado": "CANCELADO", "proximo_ciclo": None, "motivo_cancelacion": ct24.get("motivo")})
        self._f11(nuevo)
        seg = self.encargos(as_of)[seg_id]
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "SEG", "id": f"{seg_id}-{accion}-{as_of.date()}", "seg_id": seg_id,
                                                "accion": accion, "fecha": str(as_of.date())})
        return self._acuse(seg, aviso)

    def alta(self, ct24: Dict, as_of) -> Dict:
        opp_id = ct24.get("opp_id")
        f3 = self.b.almacen.estado("F3", as_of)
        if opp_id not in f3:
            raise KeyError(f"{opp_id} no está registrada en F3: solo se admite seguimiento de opciones existentes (7.11.2)")
        frec = str(ct24.get("frecuencia") or "SEMANAL").upper()
        if frec not in FRECUENCIAS_SEGUIMIENTO:
            raise ValueError(f"Frecuencia no válida {frec!r} ({', '.join(FRECUENCIAS_SEGUIMIENTO)})")
        self.b.mensajeria.crear("CT-24", "BROKER", "AG-01", {**ct24, "accion": "ALTA"})
        op = f3[opp_id]
        hp = op.get("horizonte_principal") or next(iter(op.get("horizontes_prg") or {}), None)
        aviso = hzn.aviso_frecuencia(frec, hp)
        seg_id = self.b.almacen.nuevo_id("SEG")
        prox = proximo_ciclo_seguimiento(as_of, frec, ct24.get("calendario_personalizado"))
        e = {"tipo_entrada": "ALTA", "seg_id": seg_id, "opp_id": opp_id, "segmento": op.get("segmento"), "motivo": ct24.get("motivo"),
             "frecuencia": frec, "calendario_personalizado": ct24.get("calendario_personalizado"),
             "senales_interes": list(ct24.get("senales_interes") or []), "fecha_fin": ct24.get("fecha_fin"),
             "horizonte_principal": hp, "aviso": aviso, "estado": "ACTIVO", "fecha_alta": str(as_of.date()),
             "proximo_ciclo": str(prox.date()) if prox is not None else None, "ciclos": 0, "ultimo_ciclo": None,
             "ciclos_sin_novedad_seguidos": 0}
        self._f11(e)
        # El Analizador (propietario de F3) anota la decisión del Broker y el seg_id (7.11.1)
        self.b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "DECISION_BROKER", "opp_id": opp_id, "seg_id": seg_id,
                                                "decision_broker": {"fecha": str(as_of.date()), "decision": "EN_SEGUIMIENTO",
                                                                    "motivo": ct24.get("motivo"), "seg_id": seg_id}})
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "SEG", "id": f"{seg_id}-ALTA", "seg_id": seg_id, "accion": "ALTA",
                                                "opp_id": opp_id, "fecha": str(as_of.date())})
        return self._acuse(e, aviso)

    # ================================================================================
    # Ciclo C6
    # ================================================================================
    def pendientes(self, as_of) -> List[str]:
        as_of = pd.Timestamp(as_of).normalize()
        return sorted(k for k, s in self.encargos(as_of).items()
                      if s.get("estado") == "ACTIVO" and s.get("proximo_ciclo") and pd.Timestamp(s["proximo_ciclo"]) <= as_of)

    def ejecutar_pendientes(self, as_of) -> List[Dict]:
        return [self.ejecutar(s, as_of) for s in self.pendientes(as_of)]

    def ejecutar(self, seg_id: str, as_of=None, forzar: bool = False) -> Dict:
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        segs = self.encargos(as_of)
        if seg_id not in segs:
            raise KeyError(f"Encargo {seg_id} no encontrado en F11")
        seg = segs[seg_id]
        if seg["estado"] != "ACTIVO":
            return {"seg_id": seg_id, "estado": "RECHAZADO", "motivo": f"Encargo {seg['estado'].lower()}: no se ejecuta (R27)"}
        if seg.get("fecha_fin") and pd.Timestamp(seg["fecha_fin"]) < as_of:
            self._f11({"tipo_entrada": "FINALIZACION", "seg_id": seg_id, "estado": "FINALIZADO", "proximo_ciclo": None,
                       "fecha": str(as_of.date())})
            self._acuse(self.encargos(as_of)[seg_id], "Encargo finalizado por fecha de fin")
            return {"seg_id": seg_id, "estado": "FINALIZADO"}
        f3 = self.b.almacen.estado("F3", as_of)
        op = f3.get(seg["opp_id"]) or {}
        prox = proximo_ciclo_seguimiento(as_of, seg["frecuencia"], seg.get("calendario_personalizado"))
        if op.get("estado") == "VIGENTE" and not forzar:
            # Vuelve a estar en el top-3: su seguimiento se cubre en C1 (7.11.5)
            self._f11({"tipo_entrada": "CICLO_OMITIDO", "seg_id": seg_id, "fecha": str(as_of.date()),
                       "motivo": "Opción VIGENTE en el top-3: seguimiento cubierto por C1", "proximo_ciclo": str(prox.date()) if prox is not None else None})
            return {"seg_id": seg_id, "estado": "OMITIDO", "motivo": "cubierto por C1"}
        run_id = self.b.almacen.nuevo_id("RUN")
        segmento = op.get("segmento") or seg.get("segmento")
        ciclo = int(seg.get("ciclos", 0)) + 1
        self.b.mensajeria.crear("CT-05", "AG-01", "AG-02", {"tipo": "SEGUIMIENTO", "seg_id": seg_id, "opp_id": seg["opp_id"],
                                                            "alcance": {"segmentos": [segmento]}, "nivel_por_segmento": {segmento: "N1"},
                                                            "presupuesto_por_segmento": {segmento: self.uc_ciclo},
                                                            "memoria": {"f11": seg_id}, "delta_gc0": {}, "fecha_objetivo": str(as_of.date())},
                                run_id=run_id, presupuesto={"uc": self.uc_ciclo})
        agente = AGENTE_SEGMENTO.get(segmento, "AG-03")
        self.b.mensajeria.crear("CT-06", "AG-02", agente, {"segmento": segmento, "fase": "SEGUIMIENTO", "nivel": "N1",
                                                          "opciones_vigentes": [seg["opp_id"]], "lecciones": [], "seg_id": seg_id,
                                                          "senales_interes": seg.get("senales_interes")},
                                run_id=run_id, presupuesto={"uc": self.uc_ciclo})
        inf = self._revision(seg, op, as_of, run_id, ciclo)
        texto = self.informe_md(inf, op)
        g3 = ht09.validar_seguimiento(inf, texto=texto)
        if g3["dictamen"] == "BLOQUEADO":
            inf["limitaciones"].append("HT-09 bloqueó el informe: entrega retenida para el dictamen del Orquestador (CT-14)")
            entrega = "BLOQUEADA"
        else:
            entrega = "ENTREGADA"
        carpeta = self.b.carpeta_entregables / CARPETA_INFORMES
        carpeta.mkdir(parents=True, exist_ok=True)
        base = f"{as_of.date()}_informe-seguimiento_{run_id}"
        ruta_md, ruta_js = carpeta / f"{base}.md", carpeta / f"{base}.json"
        uc = self.uc_sin_novedad if inf["sin_novedad"] else (self.uc_material if inf["x_material"] else self.uc_ciclo)
        nivel_actual = inf.pop("x_nivel", None)
        inf.pop("x_material", None)
        ruta_md.write_text(texto, encoding="utf-8")
        ruta_js.write_text(json.dumps(inf, ensure_ascii=False, indent=1), encoding="utf-8")
        if entrega == "ENTREGADA":
            self.b.mensajeria.crear("CT-24", "AG-01", "BROKER", {"seg_id": seg_id, "estado_encargo": "ACTIVO", "run_id_ref": run_id,
                                                                "informe": str(ruta_md), "json": str(ruta_js), "semaforo": inf["semaforo"],
                                                                "recomendacion": inf["recomendacion"]}, tipo_mensaje="RETORNO", estado="COMPLETO")
        sin_nov = int(seg.get("ciclos_sin_novedad_seguidos", 0)) + 1 if inf["sin_novedad"] else 0
        self._f11({"tipo_entrada": "CICLO", "seg_id": seg_id, "run_id": run_id, "fecha": str(as_of.date()), "ciclo_n": ciclo,
                   "ciclos": ciclo, "ultimo_ciclo": str(as_of.date()), "semaforo": inf["semaforo"], "recomendacion": inf["recomendacion"],
                   "ruta_informe": str(ruta_md), "ruta_json": str(ruta_js), "dictamen_ht09": g3["dictamen"], "entrega": entrega,
                   "consumo_uc": uc, "ciclos_sin_novedad_seguidos": sin_nov, "ultimo_nivel": nivel_actual,
                   "ultimo_RK": inf["puntuaciones"]["RK"], "proximo_ciclo": str(prox.date()) if prox is not None else None,
                   "respuesta_broker": None})
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN_SEGUIMIENTO", "id": run_id, "run_id": run_id, "tipo": "SEGUIMIENTO",
                                                "seg_id": seg_id, "opp_id": seg["opp_id"], "fecha": str(as_of.date()), "nivel": "N1",
                                                "presupuesto_uc": self.uc_ciclo, "consumo": {"uc": uc}, "semaforo": inf["semaforo"],
                                                "recomendacion": inf["recomendacion"], "entregables": {"informe_seguimiento": str(ruta_md),
                                                                                                       "json": str(ruta_js)},
                                                "g3": {"dictamen": g3["dictamen"], "motivo": g3["motivo"]}, "entrega": entrega})
        if inf["recomendacion"] == "CERRAR" and any(x.get("activada") for x in inf["invalidacion"]):
            # Único cambio de estado analítico permitido a un seguimiento: cierre por invalidación verificada (7.11.5)
            self.b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": seg["opp_id"], "estado": "CERRADA",
                                                    "cierre": {"fecha": str(as_of.date()), "motivo": "INVALIDACION",
                                                               "comentario": f"Invalidación verificada en el ciclo C6 {run_id}"},
                                                    "run_ids_cierre": [run_id]})
        return {"seg_id": seg_id, "run_id": run_id, "estado": "COMPLETO", "entrega": entrega, "dictamen_ht09": g3["dictamen"],
                "semaforo": inf["semaforo"], "recomendacion": inf["recomendacion"], "informe": str(ruta_md), "json": str(ruta_js),
                "consumo_uc": uc, "informe_json": inf}

    def responder(self, seg_id: str, run_id: str, decision: str, as_of=None, comentario: Optional[str] = None) -> Dict:
        """Respuesta del Broker a la recomendación de un ciclo: F11 y CT-22 DECISION_SEGUIMIENTO al Evaluador (12.4)."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        self._f11({"tipo_entrada": "RESPUESTA_BROKER", "seg_id": seg_id, "run_id_respuesta": run_id, "respuesta_broker": decision,
                   "comentario": comentario, "fecha": str(as_of.date())})
        self.b.mensajeria.crear("CT-22", "AG-01", "AG-20", {"tipo_aviso": "DECISION_SEGUIMIENTO", "seg_id": seg_id, "decision": decision,
                                                            "comentario": comentario}, run_id=run_id)
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "SEG", "id": f"{seg_id}-RESP-{run_id}", "seg_id": seg_id,
                                                "accion": "RESPUESTA_BROKER", "decision": decision, "fecha": str(as_of.date())})
        return {"seg_id": seg_id, "run_id": run_id, "respuesta_broker": decision}

    # ================================================================================
    # Revisión ligera (determinista)
    # ================================================================================
    def _nivel(self, sym: str, fecha) -> Optional[float]:
        try:
            return float(self.b.proveedor.valor_en(sym, pd.Timestamp(fecha))[1])
        except (DatosNoDisponibles, KeyError, IndexError, ValueError):
            return None

    def _vol_semanal(self, sym: str, as_of) -> Optional[float]:
        try:
            s = self.b.proveedor.cierres(sym, None, pd.Timestamp(as_of)).tail(61)
        except (DatosNoDisponibles, KeyError):
            return None
        r = (s / s.shift(1)).apply(lambda x: math.log(x) if x and x > 0 else float("nan")).dropna()
        return float(r.std() * math.sqrt(5)) if len(r) > 10 else None

    def _revision(self, seg: Dict, op: Dict, as_of: pd.Timestamp, run_id: str, ciclo: int) -> Dict:
        sym = op.get("simbolo_seguimiento") or (op.get("indicador_seguimiento") or {}).get("simbolo")
        sube = bool(op.get("indicador_sube", True))
        ahora = self._nivel(sym, as_of) if sym else None
        ref_prev = seg.get("ultimo_nivel")
        alta = self._nivel(sym, seg.get("fecha_alta") or as_of) if sym else None
        prev = ref_prev if isinstance(ref_prev, (int, float)) else alta
        cambios, limit = [], ["Revisión determinista del ejecutor (HT-01 + HT-03); sin redacción del Analista con el modelo real (R22)"]
        rend = (ahora / prev - 1.0) if (ahora and prev) else None
        rend_alta = (ahora / alta - 1.0) if (ahora and alta) else None
        vol = self._vol_semanal(sym, as_of) if sym else None
        if rend is not None:
            cambios.append(f"{sym}: {rend:+.2%} desde el ciclo anterior ({rend_alta:+.2%} desde el alta del encargo)")
        else:
            limit.append(f"Sin dato fechado de {sym} en HT-01 (PS2): delta no disponible")
        material = bool(rend is not None and vol and abs(rend) > 1.5 * vol)
        favorable = rend_alta is not None and ((rend_alta > 0) == sube) and abs(rend_alta) > 0.005
        # Invalidación
        invalid = []
        for x in op.get("invalidacion_cuantitativa") or []:
            u = float(x.get("umbral"))
            if ahora is None:
                invalid.append({"condicion": f"{x.get('simbolo')} {x.get('direccion')} {u}", "distancia": "no disponible", "activada": False})
                continue
            act = ahora < u if x.get("direccion") == "por_debajo" else ahora > u
            dist = abs(ahora - u) / abs(alta - u) if (alta and abs(alta - u) > 1e-12) else None
            invalid.append({"condicion": f"{x.get('simbolo')} {'por debajo' if x.get('direccion') == 'por_debajo' else 'por encima'} de {u:g}",
                            "distancia": f"{dist:.0%} de la distancia inicial" if dist is not None else f"{abs(ahora - u) / u:.1%}",
                            "activada": bool(act), "x_cercana": bool(dist is not None and dist < 0.10)})
        if not invalid:
            for t in op.get("invalidacion") or []:
                invalid.append({"condicion": t, "distancia": "cualitativa", "activada": False})
        activada = any(x.get("activada") for x in invalid)
        cercana = any(x.get("x_cercana") for x in invalid)
        # Catalizadores
        cats = []
        for c in op.get("catalizadores") or []:
            f = str(c.get("fecha") or "")
            try:
                ocurrido = pd.Timestamp(f[:10]) <= as_of if re.match(r"^\d{4}-\d{2}-\d{2}", f) else False
            except ValueError:
                ocurrido = False
            cats.append({"evento": c.get("evento"), "fecha": f, "estado": "OCURRIDO" if ocurrido else "PENDIENTE"})
        # Señales de interés del encargo (si son umbrales del indicador, se evalúan con HT-01)
        senales = []
        for s in seg.get("senales_interes") or []:
            m = RE_SENAL.search(str(s))
            if m and ahora is not None:
                u = float(m.group(2).replace(",", "."))
                act = ahora < u if m.group(1).lower() == "por debajo" else ahora > u
                senales.append({"senal": s, "estado": f"{'activada' if act else 'no activada'} ({sym} = {ahora:.6g})"})
            else:
                senales.append({"senal": s, "estado": "sin evaluación automática; se revisa en el informe del Analista"})
        if any(str(x["estado"]).startswith("activada") for x in senales):
            material = True
            cambios.append("Se ha activado al menos una señal de interés del encargo")
        # Puntuaciones con HT-03 (dimensiones de F3; actualidad y asimetría ajustadas)
        dims = copy.deepcopy(op.get("dimensiones") or {})
        semanas = max((as_of - pd.Timestamp(seg.get("fecha_alta") or as_of)).days / 7.0, 0)
        if isinstance(dims.get("E"), dict) and isinstance(dims["E"].get("actualidad"), int):
            dims["E"]["actualidad"] = _r10(max(dims["E"]["actualidad"] - 10 * int(semanas // 4), 40))
        if isinstance(dims.get("A"), dict) and isinstance(dims["A"].get("asimetria"), int) and rend_alta is not None:
            ajuste = 10 if favorable and abs(rend_alta) > 0.02 else (-10 if (not favorable) and abs(rend_alta) > 0.02 else 0)
            dims["A"]["asimetria"] = _r10(dims["A"]["asimetria"] + ajuste - (20 if cercana else 0))
        objs = op.get("objeciones_internas") or []
        fuertes = sum(1 for o in objs if o.get("fuerza") == "fuerte" and not o.get("resuelta"))
        entrada = {"opp_id": op.get("opp_id") or seg["opp_id"], "segmento": op.get("segmento"), "cluster": op.get("cluster_id") or "CL-99",
                   "vigente": False, "par": op.get("par"), "direccion": op.get("direccion"), "composicion": op.get("composicion") or [],
                   "riesgo_cola": op.get("riesgo_1a5"), "saturacion_narrativa": bool(op.get("saturacion_narrativa")),
                   "dimensiones": dims, "segunda_pasada": op.get("segunda_pasada") or {}, "anterior": op.get("puntuaciones_totales") or {},
                   "puertas": op.get("puertas") or {}, "objeciones_fuertes_abiertas": fuertes}
        try:
            ev = ht03.evaluar_opcion(entrada, self.b.params_ht03)
            pu = ev["puntuaciones"]
            elegible = bool(ev["elegible"]) and not activada
        except Exception as e:   # noqa: BLE001 — sin dimensiones no hay recálculo: se declara
            pu = {k: (op.get("puntuaciones_totales") or {}).get(k) or 0 for k in ("T", "E", "A", "RK")}
            elegible = False
            limit.append(f"HT-03 no pudo recalcular las puntuaciones ({e}); se arrastran las de F3")
        rk_prev = seg.get("ultimo_RK") if isinstance(seg.get("ultimo_RK"), (int, float)) else (op.get("puntuaciones_totales") or {}).get("RK")
        var_rk = (pu.get("RK") - rk_prev) if isinstance(pu.get("RK"), (int, float)) and isinstance(rk_prev, (int, float)) else 0
        if abs(var_rk) >= 5:
            material = True
            cambios.append(f"RK {rk_prev} → {pu.get('RK')} (HT-03)")
        nuevos_cat = [c for c in cats if c["estado"] == "OCURRIDO" and (not seg.get("ultimo_ciclo") or c["fecha"][:10] > seg["ultimo_ciclo"])]
        if nuevos_cat:
            material = True
            cambios.append("Catalizador ocurrido: " + "; ".join(c["evento"] for c in nuevos_cat))
        # Pronósticos abiertos de F4 y sus hitos H5 (resultados del Evaluador en F6); no se congelan pronósticos nuevos
        f4 = self.b.almacen.estado("F4", as_of)
        hits = {r.get("hit_id"): r for r in self.b.almacen.leer("F6", as_of) if r.get("tipo_entrada") == "HIT"}
        prons = []
        for p in sorted(f4.values(), key=lambda x: x["prg_id"]):
            if p.get("opp_id") != seg["opp_id"]:
                continue
            hs = [{"hit_id": h.get("hit_id"), "fecha": h.get("fecha"), "estado": (hits.get(h.get("hit_id")) or {}).get("resultado", "ABIERTO")}
                  for h in p.get("hitos") or []]
            prons.append({"prg_id": p["prg_id"], "horizonte": p.get("horizonte"),
                          "estado": "EN_CURSO" if p.get("estado") == "ABIERTO" else p.get("estado"), "fecha_resolucion": p.get("fecha_resolucion"),
                          "hitos": hs})
        abiertos = [p for p in prons if p["estado"] == "EN_CURSO"]
        sin_novedad = not material and not activada and not cercana
        # Semáforo y recomendación (7.11.4)
        if activada or cercana or var_rk <= -10:
            sem = "ROJO"
        elif favorable and var_rk >= 0 and material:
            sem = "VERDE"
        else:
            sem = "AMBAR"
        hp = op.get("horizonte_principal") or seg.get("horizonte_principal")
        n_sin = int(seg.get("ciclos_sin_novedad_seguidos", 0)) + (1 if sin_novedad else 0)
        paquete_b, motivo_cierre, sugerir_n3 = None, None, False
        if activada:
            rec, motivo = "CERRAR", "Se ha activado una condición de invalidación verificada con HT-01"
            motivo_cierre = "INVALIDACION"
        elif prons and not abiertos:
            rec, motivo = "CERRAR", "Han vencido todos los pronósticos de la opción: el horizonte principal ha concluido"
            motivo_cierre = "HORIZONTE_VENCIDO"
        elif elegible and sem == "VERDE" and fuertes == 0:
            rec, motivo = "PROPONER_ENVIO_A_B", "Vuelve a ser elegible (9.2) con las puntuaciones actualizadas y sin objeciones fuertes abiertas"
            paquete_b = self._paquete_b(op, hp)
            sugerir_n3 = semanas > 4 or material
        elif n_sin >= self.ciclos_sin_novedad_cancelar:
            rec, motivo = "PROPONER_CANCELACION", f"{n_sin} ciclos seguidos sin novedad: la vigilancia ya no aporta valor"
        else:
            rec, motivo = "MANTENER_VIGILANCIA", ("Sin cambio material en la tesis" if sin_novedad else "Cambios sin efecto decisivo en la tesis")
        for x in invalid:
            x.pop("x_cercana", None)
        sup, _ = (self.b.consultas.supuestos_de_run(run_id, as_of, seg["seg_id"]) if getattr(self.b, "consultas", None) else ([], []))
        sup = [s for s in sup if s.get("cns_id")]
        limit += self.b.credenciales.limitaciones(as_of) if getattr(self.b, "credenciales", None) else []
        carry = op.get("carry") or {}
        inf = {"seg_id": seg["seg_id"], "opp_id": seg["opp_id"], "run_id": run_id, "ciclo": ciclo, "fecha": str(as_of.date()),
               "segmento": op.get("segmento"), "par": op.get("par"), "direccion": op.get("direccion"),
               "composicion": op.get("composicion"), "horizonte_principal": hp, "naturaleza_inversion": op.get("naturaleza_inversion"),
               "sin_novedad": sin_novedad, "semaforo": sem, "que_ha_cambiado": cambios or ["Sin cambio material desde el ciclo anterior"],
               "senales_interes": senales, "invalidacion": invalid, "catalizadores": cats,
               "puntuaciones": {"T": pu.get("T"), "E": pu.get("E"), "A": pu.get("A"), "RK": pu.get("RK"), "variacion_RK": var_rk,
                                "elegible": elegible, "fuente": "HT-03"},
               "carry": {"anual_pct": carry.get("anual_pct"), "signo": carry.get("signo")},
               "pronosticos_abiertos": prons, "recomendacion": rec, "motivo": motivo, "motivo_cierre": motivo_cierre,
               "sugerir_profundizacion_N3": sugerir_n3, "paquete_para_bloque_B": paquete_b,
               "objeciones_fuertes_abiertas": fuertes, "supuestos_declarados": sup, "limitaciones": limit,
               "x_material": material, "x_nivel": ahora}
        return inf

    def _paquete_b(self, op: Dict, hp: Optional[str]) -> Dict:
        b = {k: copy.deepcopy(op.get(k)) for k in ("segmento", "tipo_opcion", "par", "composicion", "direccion", "divisa_financiacion",
                                                    "ambito", "tesis", "mecanismo", "catalizadores", "riesgos", "invalidacion",
                                                    "indicador_seguimiento", "consideraciones_implementacion", "metricas_clave",
                                                    "preguntas_para_B", "evidencias")}
        b.update({"opp_id": op.get("opp_id"), "horizonte_principal": hp, "horizontes": sorted((op.get("horizontes_prg") or {}).keys()),
                  "pronosticos": [d.get("prg_id") for d in (op.get("horizontes_prg") or {}).values()],
                  "carry_esperado": {"anual_pct": (op.get("carry") or {}).get("anual_pct"), "signo": (op.get("carry") or {}).get("signo")},
                  "calculos": [x for x in [(op.get("carry") or {}).get("calc_id")] if x]})
        return b

    # ================================================================================
    # Informe breve (plantilla de 06_Plantillas_entregables, ≤ 300 palabras)
    # ================================================================================
    @staticmethod
    def informe_md(inf: Dict, op: Dict) -> str:
        nombre = op.get("nombre_llano") or op.get("nombre") or inf["opp_id"]
        sem = {"VERDE": "VERDE (la tesis mejora)", "AMBAR": "ÁMBAR (sin cambio material o señales mixtas)",
               "ROJO": "ROJO (la tesis se deteriora o se acerca una invalidación)"}[inf["semaforo"]]
        pu = inf["puntuaciones"]
        L = [f"# Informe de seguimiento de opción · {inf['seg_id']} · ciclo {inf['ciclo']}", "",
             f"**{inf['fecha']}** · `{inf['opp_id']}` · {inf.get('par') or 'cesta/estrategia'} {inf.get('direccion') or ''} · "
             f"segmento {inf['segmento']} · horizonte principal {inf.get('horizonte_principal')} · `{inf['run_id']}`", "",
             f"**{nombre}**", "", f"**Semáforo:** {sem}", ""]
        if inf["sin_novedad"]:
            L += ["**Sin novedad.** " + "; ".join(inf["que_ha_cambiado"][:1]), "",
                  f"**Recomendación: {inf['recomendacion']}.** {inf['motivo']}.", ""]
        else:
            L += ["**Qué ha cambiado:** " + "; ".join(inf["que_ha_cambiado"][:4]), ""]
            if inf["senales_interes"]:
                L += ["**Señales de interés:** " + "; ".join(f"{s['senal']} → {s['estado']}" for s in inf["senales_interes"][:3]), ""]
            L += ["**Invalidación:** " + "; ".join(f"{x['condicion']} ({'ACTIVADA' if x['activada'] else x['distancia']})"
                                                for x in inf["invalidacion"][:3]), "",
                  "**Catalizadores:** " + ("; ".join(f"{c['evento']} {c['fecha']} ({c['estado'].lower()})" for c in inf["catalizadores"][:3]) or "—"), "",
                  f"**Puntuaciones (HT-03):** T {pu['T']} · E {pu['E']} · A {pu['A']} · RK {pu['RK']} ({pu['variacion_RK']:+}) · "
                  f"{'elegible' if pu['elegible'] else 'no elegible'}", "",
                  "**Pronósticos abiertos:** " + ("; ".join(f"{p['prg_id']} {p['horizonte']} {p['estado'].lower()}"
                                                           + (f" ({sum(1 for h in p['hitos'] if h['estado'] == 'CUMPLIDO')}/{len(p['hitos'])} hitos)" if p["hitos"] else "")
                                                           for p in inf["pronosticos_abiertos"][:3]) or "—"), "",
                  f"**Recomendación: {inf['recomendacion']}.** {inf['motivo']}."
                  + (" Se sugiere una profundización N3 antes del envío." if inf.get("sugerir_profundizacion_N3") else ""), ""]
        if inf.get("supuestos_declarados"):
            L += ["**Supuestos declarados:** " + "; ".join(s["supuesto"] for s in inf["supuestos_declarados"][:2]), ""]
        L += ["*La decisión es siempre del Broker. Este informe no es asesoramiento personalizado.*", ""]
        return "\n".join(L)
