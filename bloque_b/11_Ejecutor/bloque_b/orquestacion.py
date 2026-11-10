"""Orquestación de una petición del Bloque B (V2.1): capas 0–4 con puertas de viabilidad PV1–PV3 (7.10), fases F0–F10
(7.3–7.4), informe de parada (7.11) y continuación forzada por el Broker, consultas del bloque al Broker (CT-B-28,
7.12), puerta de tiempo PT30/PTA sobre el acumulado con puntos de control persistidos (9.9), opción `HASTA_PV2`,
política de autorización automática, reanudación por `autorizar`, división en fases y cancelación.

Cada tramo deja su resultado en el estado `st` (JSON), que se guarda como punto de control seguro (CKP-) al cerrarlo.
Los tramos se corresponden con las fases y las capas: F0 (capa 0) · F1 (capa 1, PV1) · F2L y F3P (capa 2: dimensiones
líderes y tesis provisional, PV2) · F2R, F3 y F5 (capa 3: resto de dimensiones, desglose de la cadena y cuellos, radar de
emergentes, tesis consolidada y selección con eslabones, PV3) · F4, F6–F10 (capa 4). Un análisis detenido se reanuda
desde su último punto de control con una ejecución nueva (RUN-B-AAAA-NNNN-rr)."""
from __future__ import annotations

import concurrent.futures
import copy
import datetime as dt
import hashlib
import json
import math
import random
import re
import time
from typing import Any, Dict, List, Optional, Tuple

from . import sintesis
from .configuracion import FRESCURA_MERCADO_DIAS, HORIZONTES, TIPOS_ACTIVO, TIPOS_OBJETO
from .contratos import RE_CARTERA, MensajeRechazado, comprobar_sensibles, controlado, multiplo10, sanear
from .fechas_evidencia import CAMPOS_FECHA, dia_local, fechas_de_fuente
from .herramientas import ht03, ht08, ht09, ht11
from .referencias import AREAS_DIM

TRAMOS = ["F0", "F1", "F2L", "F3P", "F2R", "F3", "F5", "F4", "F6", "F7", "F8", "F9", "F10"]
# Tramo → (fase de registro, fracción de su estimación) y capa (7.3, 7.10)
FASE_TRAMO = {"F2L": ("F2", 0.5), "F2R": ("F2", 0.5), "F3P": ("F3", 0.4), "F3": ("F3", 0.6)}
CAPA_TRAMO = {"F0": 0, "F1": 1, "F2L": 2, "F3P": 2, "F2R": 3, "F3": 3, "F5": 3, "F4": 4, "F6": 4, "F7": 4, "F8": 4, "F9": 4, "F10": 4}
PUERTA_TRAS = {"F1": "PV1", "F3P": "PV2", "F5": "PV3"}
TIPOS_CONSULTA = ("ACLARACION_ALCANCE", "DATO_O_DOCUMENTO", "PREFERENCIA_O_CRITERIO", "CONFIRMACION_SUPUESTO", "OTRA")
RE_ESL = re.compile(r"^ESL-\d{2}(\.\d{2}){0,2}(\.[a-z])?$")
MOTIVOS_RECHAZO = ("ACTIVO_INDIVIDUAL", "ASESORAMIENTO_PERSONAL", "TIEMPO_REAL_O_EJECUCION", "DATOS_SENSIBLES",
                   "AMBITO_INDETERMINADO", "FUERA_DE_ALCANCE")
RE_ISIN = re.compile(r"^\s*[A-Z]{2}[A-Z0-9]{9}[0-9]\s*$")
RE_TICKER = re.compile(r"^\s*[A-Z0-9.\-]{1,6}\s*$")
RE_ASESOR = re.compile(r"\b(mi cartera|mi perfil|cu[aá]nto (debo|deber[ií]a) (comprar|invertir)|qu[eé] (debo|deber[ií]a) comprar|"
                       r"tama[ñn]o de (mi )?posici[oó]n)\b", re.IGNORECASE)
RE_TIEMPO_REAL = re.compile(r"\b(tiempo real|intrad[ií]a en vivo|ejecuta la orden|lanza la orden|compra ahora)\b", re.IGNORECASE)
RE_NO_FIN = re.compile(r"\b(receta|f[uú]tbol|poema|horóscopo)\b", re.IGNORECASE)


def _j(o: Any) -> Any:
    """Convierte a tipos JSON nativos (numpy, fechas)."""
    return json.loads(json.dumps(o, default=lambda x: x.item() if hasattr(x, "item") else str(x)))


def _ahora() -> float:
    return time.perf_counter()


def banda_verbal(p: float) -> str:
    if p >= 0.80:
        return "muy probable"
    if p >= 0.58:
        return "más probable que no"
    if p >= 0.42:
        return "incierto"
    if p >= 0.21:
        return "poco probable"
    return "muy poco probable"


class Coordinador:
    """Servicio del bloque para una petición: AG-B01 frente al Broker y conducción de las fases por el Director."""

    def __init__(self, ent) -> None:
        self.ent = ent
        self.cfg = ent.cfg
        self.alm = ent.alm
        self.inv = ent.inv
        self.motor = ent.motor
        self.pt = self.cfg.get("puerta_tiempo") or {}

    # =========================================================================================================
    # Recepción (CT-B-01)
    # =========================================================================================================
    def recibir(self, peticion: Dict) -> Dict:
        ent, alm = self.ent, self.alm
        self._revisar_autorizaciones()
        try:
            comprobar_sensibles(peticion)
        except MensajeRechazado as e:
            pet_id = alm.nuevo_id("PET-B")
            alm.escribir("F1", "AG-B01", {"tipo_entrada": "PETICION", "id": pet_id, "estado": "RECHAZADA",
                                          "motivo": "DATOS_SENSIBLES", "detalle": str(e), "peticion": "(no se registra: contenido sensible)"})
            alm.incidencia("SEGURIDAD", f"Petición {pet_id} rechazada íntegra: {e.tipo}", "AG-B01", severidad="Crítica")
            return {"pet_id": pet_id, "admision": "RECHAZADA", "motivo": "DATOS_SENSIBLES", "detalle": str(e)}
        incid: List[str] = []
        pet = sanear(copy.deepcopy(peticion), incid)
        if incid:
            alm.incidencia("INSTRUCCION_INCRUSTADA", f"{len(incid)} instrucción(es) incrustada(s) neutralizada(s) en la petición",
                           "AG-B01", severidad="Material")
        # Idempotencia: misma petición en curso → se vincula
        huella = json.dumps({k: pet.get(k) for k in ("objeto", "paquete_para_bloque_B", "tipos_activo_admitidos", "horizontes")},
                            sort_keys=True, ensure_ascii=False)
        for e in alm.estado("F1", tipo="PETICION").values():
            if e.get("huella") == huella and e.get("estado") not in ("ENTREGADA", "RECHAZADA", "CANCELADA", "CADUCADA", "BLOQUEADO_AUDITORIA"):
                return {"pet_id": e["id"], "admision": "ADMITIDA", "vinculada_a": e["id"],
                        "nota": "Petición idéntica en curso: se vincula y no se duplica el análisis (6.2.2)"}
        pet_id = alm.nuevo_id("PET-B")
        motivo, extra = self._admisibilidad(pet)
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "PETICION", "id": pet_id, "estado": "RECIBIDA", "peticion": pet,
                                      "huella": huella, "origen": pet.get("origen", "LIBRE")})
        if motivo:
            alm.escribir("F1", "AG-B01", {"tipo_entrada": "PETICION", "id": pet_id, "estado": "RECHAZADA", "motivo": motivo, **extra})
            return {"pet_id": pet_id, "admision": "RECHAZADA", "motivo": motivo, **extra}
        r = self.inv.llamar("AG-B01", "CT-B-01", "admision", {"pet_id": pet_id, "peticion": pet},
                            "Clasifica la admisibilidad de la petición (7.4 F0, punto 2).", {"clasificacion": "string"},
                            self._ctx("AG-B01"))
        if r.get("clasificacion") == "RECHAZADA" and r.get("motivo") in MOTIVOS_RECHAZO:
            alm.escribir("F1", "AG-B01", {"tipo_entrada": "PETICION", "id": pet_id, "estado": "RECHAZADA", "motivo": r["motivo"],
                                          "detalle": r.get("observaciones")})
            return {"pet_id": pet_id, "admision": "RECHAZADA", "motivo": r["motivo"], "detalle": r.get("observaciones")}
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "PETICION", "id": pet_id, "estado": "ADMITIDA"})
        st = {"pet_id": pet_id, "peticion": pet, "run_ids": [], "consumido_min": 0.0, "siguiente": "F0",
              "autorizaciones": [], "puntos_control": [], "tiempos": {}, "estimado_hecho": 0.0, "fase_division": None,
              "recortes": [], "estados_degradados": [], "limitaciones": [], "incidencias_r12": len(incid),
              "pv": {}, "consultas": [], "aportes": [], "minutos_capa": {}, "continuacion_forzada": None}
        res = self.ejecutar(st)
        res.setdefault("acuse_inmediato", {"pet_id": pet_id, "admision": "ADMITIDA"})
        return res

    def _admisibilidad(self, pet: Dict) -> Tuple[Optional[str], Dict]:
        obj = pet.get("objeto") or {}
        desc = " ".join(str(x) for x in (obj.get("descripcion"), (obj.get("ambito") or {}).get("incluye"),
                                         " ".join(pet.get("preguntas") or [])) if x)
        if pet.get("origen") == "BLOQUE_A" and not pet.get("paquete_para_bloque_B"):
            return "AMBITO_INDETERMINADO", {"preguntas_aclaracion": ["Falta el paquete_para_bloque_B del origen BLOQUE_A"]}
        if pet.get("origen") != "BLOQUE_A" and not desc.strip() and not obj.get("clave_universo"):
            return "AMBITO_INDETERMINADO", {"preguntas_aclaracion": ["¿Qué ámbito (incluye/excluye/región) quiere analizar?"]}
        if RE_ASESOR.search(desc):
            return "ASESORAMIENTO_PERSONAL", {"detalle": "El Bloque B no conoce cartera ni perfil ni dimensiona posiciones (R4)"}
        if RE_TIEMPO_REAL.search(desc):
            return "TIEMPO_REAL_O_EJECUCION", {"detalle": "Sin datos en tiempo real ni decisiones de ejecución (R30)"}
        if RE_NO_FIN.search(desc):
            return "FUERA_DE_ALCANCE", {"detalle": "Objeto no financiero"}
        d = (obj.get("descripcion") or "").strip()
        if d and (RE_ISIN.match(d) or (RE_TICKER.match(d) and not obj.get("clave_universo"))):
            tipo = (pet.get("tipos_activo_admitidos") or ["RV"])[0]
            return "ACTIVO_INDIVIDUAL", {"bloque_c_sugerido": ht03.BLOQUE_C.get(tipo, "C.1"),
                                         "reformulacion": f"¿Desea analizar el ámbito de «{d}» y sus competidores?"}
        return None, {}

    # =========================================================================================================
    # Utilidades comunes
    # =========================================================================================================
    def _ctx(self, agente: str, st: Optional[Dict] = None) -> Dict:
        lec = [e for e in self.alm.leer("F5", self.ent.as_of) if e.get("tipo_entrada") == "LECCION"
               and agente in (e.get("agentes") or [agente])][-10:]
        return {"fecha_as_of": self.ent.as_of, "modo": self.ent.modo, "lecciones": [l.get("observacion") for l in lec],
                "f10": {"methodology_version": self.cfg.get("methodology_version")}}

    def _estado_pet(self, st: Dict, estado: str, **extra) -> None:
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "PETICION", "id": st["pet_id"], "estado": estado, **extra})

    def _guardar_ckp(self, st: Dict, tramo: str) -> str:
        ckp = self.alm.nuevo_id("CKP")
        ht08.guardar_punto_control(self.alm.dir_puntos_control, ckp, _j(st))
        st["puntos_control"].append(ckp)
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "PUNTO_CONTROL", "id": ckp, "pet_id": st["pet_id"], "run_id": st["run_id"],
                                           "tramo": tramo, "siguiente": st["siguiente"], "consumido_min": round(st["consumido_min"], 2)})
        return ckp

    def _duracion(self, st: Dict, tramo: str, t0: float) -> float:
        """Minutos del tramo: reales (reloj de pared) o simulados (p50 del modelo × factor × ruido con semilla)."""
        if not self.ent.reloj_simulado:
            return (_ahora() - t0) / 60.0
        est = st.get("estimacion_fases") or {}
        fase, frac = FASE_TRAMO.get(tramo, (tramo, 1.0))
        base = est.get(fase, 1.0) * frac
        rc = self.cfg.get("reloj") or {}
        rng = random.Random(f"{st['pet_id']}|{tramo}|{len(st['run_ids'])}")
        return base * float(rc.get("factor_simulado", 1.0)) * math.exp(rng.gauss(0, float(rc.get("sigma_ruido", 0.15))))

    # =========================================================================================================
    # Bucle de ejecución con puerta de tiempo
    # =========================================================================================================
    def ejecutar(self, st: Dict) -> Dict:
        if st["siguiente"] in ("F7", "F8", "F9", "F10") and any(
            o.get("fuerza") == "fuerte" and o.get("resuelta") and not o.get("x_fechas_evidencia")
            for o in (st.get("refutacion") or {}).get("objeciones", [])
        ):
            motivo = "Cierre anterior al control temporal: se necesita repetir el análisis."
            self._estado_pet(st, "BLOQUEADO_AUDITORIA", motivo=motivo)
            return {"pet_id": st["pet_id"], "estado_peticion": "BLOQUEADO_AUDITORIA", "motivo": motivo}
        st["run_id"] = self.alm.nuevo_run(st["pet_id"])
        st["run_ids"].append(st["run_id"])
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "EJECUCION", "id": st["run_id"], "pet_id": st["pet_id"],
                                           "desde": st["siguiente"], "as_of": self.ent.as_of})
        self._estado_pet(st, "EN_CURSO" if st["siguiente"] != "F0" else "PLANIFICADA", run_id=st["run_id"])
        idx = TRAMOS.index(st["siguiente"])
        for tramo in TRAMOS[idx:]:
            self._sincronizar_consultas(st)
            if self._bloqueantes_pendientes(st):         # consulta BLOQUEANTE: pausa en el punto de control (7.12)
                return self._pausa_consulta(st)
            t0 = _ahora()
            uc0 = self.inv.uc_total + self.motor.uc
            getattr(self, "_" + tramo.lower())(st)
            dur = self._duracion(st, tramo, t0)
            st["consumido_min"] += dur
            st["tiempos"][tramo] = round(st["tiempos"].get(tramo, 0) + dur, 2)
            capa = str(CAPA_TRAMO[tramo])
            st.setdefault("minutos_capa", {})[capa] = round(st["minutos_capa"].get(capa, 0) + dur, 2)
            st.setdefault("uc_tramos", {})[tramo] = round(self.inv.uc_total + self.motor.uc - uc0, 3)
            est_f = st.get("estimacion_fases") or {}
            fase, frac = FASE_TRAMO.get(tramo, (tramo, 1.0))
            st["estimado_hecho"] += est_f.get(fase, 0) * frac
            i = TRAMOS.index(tramo)
            st["siguiente"] = TRAMOS[i + 1] if i + 1 < len(TRAMOS) else "FIN"
            if st.get("terminado"):
                return st["resultado"]
            if tramo == "F10":
                return st["resultado"]
            self._guardar_ckp(st, tramo)
            if tramo in PUERTA_TRAS:                      # puertas de viabilidad entre capas (7.10)
                parada = getattr(self, "_" + PUERTA_TRAS[tramo].lower())(st)
                if parada:
                    return parada
            if tramo == "F0":
                pausa = self._puerta_previa(st)
            elif tramo == "F3P" and st.get("autorizado_hasta") == "PV2":
                st.pop("autorizado_hasta", None)          # HASTA_PV2: PV2 superada → nueva solicitud con el resto (A.2)
                rest = self._estimar_resto(st)
                est = {k: rest[k] for k in ("minutos_p50", "minutos_p80", "uc_p50", "uc_p80", "desglose_por_fase", "desglose_por_capa")}
                pausa = self._detener(st, "PT30", "EN_EJECUCION", est)
            else:
                pausa = self._puerta_en_ejecucion(st)
            if pausa:
                return pausa
        return st.get("resultado", {})

    def _fases_restantes(self, st: Dict, hasta: Optional[str] = None) -> List[str]:
        """Fases pendientes (en orden de FASES) desde el siguiente tramo; `hasta` limita al tramo indicado (incluido)."""
        i = TRAMOS.index(st["siguiente"]) if st["siguiente"] in TRAMOS else len(TRAMOS)
        j = TRAMOS.index(hasta) + 1 if hasta in TRAMOS else len(TRAMOS)
        fases = []
        for t in TRAMOS[i:j]:
            f = FASE_TRAMO.get(t, (t, 1.0))[0]
            if f not in fases:
                fases.append(f)
        if st.get("fase_division") == 1:
            fases = [f for f in fases if f != "F5"]
        return [f for f in ht08.FASES if f in fases]

    def _estimar_resto(self, st: Dict, hasta: Optional[str] = None) -> Dict:
        """Estimación HT-08 de lo pendiente, descontando la parte ya hecha de las fases repartidas entre capas (F2, F3)."""
        fases = self._fases_restantes(st, hasta)
        e = ht08.estimar(self._plan_ht08(st), self.pt.get("modelo"), fases)
        i = TRAMOS.index(st["siguiente"]) if st["siguiente"] in TRAMOS else len(TRAMOS)
        j = TRAMOS.index(hasta) + 1 if hasta in TRAMOS else len(TRAMOS)
        pend: Dict[str, float] = {}
        for t in TRAMOS[i:j]:
            f, fr = FASE_TRAMO.get(t, (t, 1.0))
            pend[f] = pend.get(f, 0.0) + fr
        dedu = sum(e["desglose_por_fase"].get(f, 0.0) * (1 - min(1.0, fr)) for f, fr in pend.items() if fr < 1)
        if dedu:
            disp = e["minutos_p80"] / e["minutos_p50"] if e["minutos_p50"] else 1.2
            e = dict(e, minutos_p50=round(max(0.0, e["minutos_p50"] - dedu), 1), minutos_p80=round(max(0.0, e["minutos_p80"] - dedu * disp), 1))
        return e

    def _plan_ht08(self, st: Dict) -> Dict:
        e = st["estrategia"]
        return {"nivel": st["nivel"], "profundidad": e["profundidad"], "pesos": e["pesos_efectivos"],
                "especialistas_activos": [a for a, v in e["activacion"].items() if v["activo"]],
                "tipos_activo": st["tipos_aplicables"], "top_n": st["top_n"][0],
                "universo_por_tipo": {t: st["universos"][t]["tamano_bruto"] for t in st["tipos_aplicables"]},
                "refutacion": st["nivel"] in ("N2", "N3") and not st.get("refutacion_limitada")}

    def _puerta_previa(self, st: Dict) -> Optional[Dict]:
        est = st["estimacion"]
        pet = st["peticion"]
        n3_expreso = st["nivel"] == "N3" and (pet.get("nivel") == "N3" or bool(pet.get("alto_impacto")))
        limite = (pet.get("limite") or {}).get("minutos")
        pp = ht08.puerta_previa(est, st["nivel"], limite, n3_expreso, float(self.pt.get("umbral_min", 30)))
        st["autorizado_min"] = pp["minutos_autorizados"]
        st["n3_expreso"] = n3_expreso
        if n3_expreso:
            aut = self.alm.nuevo_id("AUT-B")
            st["autorizaciones"].append(aut)
            self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AUTORIZACION", "id": aut, "pet_id": st["pet_id"], "run_id": st["run_id"],
                                               "tipo": "N3_EXPRESO", "puerta": "PT30", "momento": "PREVIO_F0",
                                               "estimacion": est, "justificacion": self._justificacion(st, est),
                                               "decision": {"opcion": "CONTINUAR", "minutos_autorizados": pp["minutos_autorizados"],
                                                            "decidido_por": "BROKER", "motivo": "N3 solicitado expresamente (9.9; A.2)"},
                                               "estado": "DECIDIDA"})
        if not pp["dispara"]:
            return None
        return self._detener(st, pp["puerta"], "PREVIO_F0", est)

    def _puerta_en_ejecucion(self, st: Dict) -> Optional[Dict]:
        if st["siguiente"] in ("F10", "FIN"):
            return None
        e_rest = self._estimar_resto(st, "F3P" if st.get("autorizado_hasta") == "PV2" else None)
        pr = ht08.proyectar(st["consumido_min"], max(st["estimado_hecho"], 0.1), e_rest, self.pt.get("modelo"))
        umbral = float(self.pt.get("umbral_min", 30))
        if st.get("opcion_autorizada") in ("CONTINUAR", "DIVIDIR_EN_FASES", "HASTA_PV2"):
            umbral = min(umbral, float(st["autorizado_min"]) - 1e-6)     # autorización expresa del Broker: rige la PTA (9.9)
        ev = ht08.evaluar_en_ejecucion(st["consumido_min"], pr["total_p80"], st["autorizado_min"], umbral)
        st["proyeccion"] = pr
        self.alm.escribir("HA", "AG-B21", {"tipo_entrada": "AVT", "id": self.alm.nuevo_id("AVT-B"), "pet_id": st["pet_id"],
                                           "run_id": st["run_id"], "consumido_min": round(st["consumido_min"], 2),
                                           "proyeccion": pr, "autorizado_min": st["autorizado_min"], "dispara": ev["dispara"]})
        if not ev["dispara"]:
            return None
        est = {"minutos_p50": round(pr["total_p50"] - st["consumido_min"], 1), "minutos_p80": round(pr["restante_p80"], 1),
               "uc_p50": e_rest["uc_p50"], "uc_p80": e_rest["uc_p80"], "desglose_por_fase": e_rest["desglose_por_fase"]}
        return self._detener(st, ev["puerta"], "EN_EJECUCION", est)

    def _justificacion(self, st: Dict, est: Dict) -> Dict:
        pend = self._fases_restantes(st)
        r = self.inv.llamar("AG-B01", "CT-B-05", "justificacion_tiempo",
                            {"pet_id": st["pet_id"], "pendiente": pend, "estimacion": est, "nivel": st.get("nivel"),
                             "ambito": (st.get("plan") or {}).get("ambito", {}).get("nombre")},
                            "Redacta la justificación argumentada de la ampliación (9.9, punto 1).",
                            {"que_aporta": "string", "incertidumbres_que_reduce": "array", "que_se_perderia": "string"},
                            self._ctx("AG-B01"), st.get("run_id"))
        return {"que_aporta": r.get("que_aporta") or f"Completar {', '.join(pend)} con la profundidad del plan",
                "incertidumbres_que_reduce": r.get("incertidumbres_que_reduce") or [],
                "que_se_perderia": r.get("que_se_perderia") or "Profundidad de la selección y de la refutación",
                "relevancia_decisional": st.get("relevancia_origen")}

    def _detener(self, st: Dict, puerta: str, momento: str, est: Dict) -> Optional[Dict]:
        """Punto de control seguro: justificación (siempre, R20), opciones, política automática o solicitud al Broker."""
        aut_id = self.alm.nuevo_id("AUT-B")
        plan = self._plan_ht08(st)
        rest = self._fases_restantes(st)
        ops = ht08.opciones(plan, est, st["consumido_min"] if momento == "EN_EJECUCION" else 0.0, self.pt.get("modelo"),
                            st.get("relevancia_origen") or "MEDIA", rest, pv2_pendiente="PV2" not in (st.get("pv") or {}))
        just = self._justificacion(st, est)
        total_p80 = (st["consumido_min"] if momento == "EN_EJECUCION" else 0.0) + float(est["minutos_p80"])
        politica = (self.ent.f10().get("politica_autorizacion") or [])
        tope = float(self.ent.f10().get("tope_autorizacion_automatica_min") or self.pt.get("tope_automatico_min", 240))
        ctx_pol = {"relevancia": st.get("relevancia_origen"), "nivel": st["nivel"], "origen": st["peticion"].get("origen"),
                   "siguiente_paso_A": (st["peticion"].get("paquete_para_bloque_B") or {}).get("siguiente_paso_sugerido"),
                   "puerta": puerta}
        pol = ht08.aplicar_politica(politica, ctx_pol, total_p80, tope)
        ckp = st["puntos_control"][-1] if st["puntos_control"] else None
        sol = {"tipo_entrada": "AUTORIZACION", "id": aut_id, "pet_id": st["pet_id"], "run_id": st["run_id"], "puerta": puerta,
               "momento": momento, "punto_control": {"checkpoint_id": ckp, "fase": st["siguiente"]},
               "hecho_hasta_ahora": {"fases_cerradas": [t for t in TRAMOS if t in st["tiempos"]],
                                     "conclusiones_provisionales": st.get("conclusiones_provisionales", []),
                                     "minutos_consumidos": round(st["consumido_min"], 1),
                                     "uc_consumidas": round(sum((st.get("uc_tramos") or {}).values()), 1)},
               "estimacion": est, "justificacion": just,
               "opciones": ops["opciones"], "recomendacion_bloque": ops["recomendacion_bloque"],
               "politica_aplicada": {"regla_id": pol.get("regla_id"), "resultado": pol["resultado"]},
               "solicitada": self.alm.reloj.ahora()}
        st["plan_recortado"] = ops["plan_recortado"]
        st["ultimas_opciones"] = ops["opciones"]
        st["autorizaciones"].append(aut_id)
        if pol["resultado"] == "AUTORIZA":
            sol.update({"tipo": "AUTORIZACION_AUTOMATICA_NOTIFICADA", "estado": "DECIDIDA",
                        "decision": {"opcion": pol["opcion"], "minutos_autorizados": pol["minutos_autorizados"],
                                     "decidido_por": "POLITICA_AUTOMATICA", "regla_id": pol["regla_id"],
                                     "timestamp": self.alm.reloj.ahora()}})
            self.alm.escribir("F1", "AG-B01", sol)
            self._aplicar_decision(st, pol["opcion"], pol["minutos_autorizados"], aut_id)
            if st.get("terminado"):
                return st["resultado"]
            return None
        sol.update({"tipo": "SOLICITUD", "estado": "PENDIENTE"})
        self.alm.escribir("F1", "AG-B01", sol)
        estado = "EN_PAUSA_AUTORIZACION" if momento == "PREVIO_F0" else "EN_PAUSA_PUNTO_CONTROL"
        self._estado_pet(st, estado, aut_id=aut_id, checkpoint_id=ckp)
        ckp2 = self._guardar_ckp(st, "PAUSA")
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AUTORIZACION", "id": aut_id, "checkpoint_reanudacion": ckp2})
        return {"pet_id": st["pet_id"], "estado": "EN_PAUSA", "estado_peticion": estado, "aut_id": aut_id,
                "checkpoint_id": ckp2, "puerta": puerta, "momento": momento, "estimacion": est,
                "requiere_autorizacion": True, "recomendacion": ops["recomendacion_bloque"],
                "opciones": [o["opcion"] for o in ops["opciones"]], "nivel": st["nivel"],
                "minutos_consumidos": round(st["consumido_min"], 1),
                "consultas_pendientes": [q["cns_id"] for q in st.get("consultas") or [] if q.get("estado") == "PENDIENTE"]}

    def _aplicar_decision(self, st: Dict, opcion: str, minutos: Optional[float], aut_id: str) -> None:
        st["opcion_autorizada"] = opcion
        if opcion == "CONTINUAR":
            rest = self._estimar_resto(st)
            pedido = next((float(o.get("minutos_p80") or 0) for o in st.get("ultimas_opciones") or [] if o.get("opcion") == "CONTINUAR"), 0.0)
            st["autorizado_min"] = float(minutos or max(st["consumido_min"] + rest["minutos_p80"], pedido))
        elif opcion == "VERSION_30_MIN":
            pr = st.get("plan_recortado") or {}
            st["estrategia"]["profundidad"] = pr.get("profundidad", st["estrategia"]["profundidad"])
            if pr.get("top_n") and pr["top_n"] < st["top_n"][0]:
                st["top_n"] = [int(pr["top_n"]), 0]
            omit = [t for t in st["tipos_aplicables"] if t not in (pr.get("tipos_activo") or st["tipos_aplicables"])]
            for t in omit:
                st["tipos_no_aplicables"][t] = "Omitido por la versión ≤ 30 min autorizada (alcance reducido declarado, R23)"
            st["tipos_aplicables"] = [t for t in st["tipos_aplicables"] if t not in omit]
            st["refutacion_limitada"] = bool(pr.get("refutacion_limitada"))
            st["recortes"] += [f"Versión ≤ 30 min ({aut_id})"] + (pr.get("recortes") or [])
            st["autorizado_min"] = float(self.pt.get("umbral_min", 30))
            e2 = ht08.estimar(self._plan_ht08(st), self.pt.get("modelo"))      # el resto se estima y se cronometra con el plan recortado
            for f in self._fases_restantes(st):
                st["estimacion_fases"][f] = e2["desglose_por_fase"].get(f, st["estimacion_fases"].get(f, 0))
        elif opcion == "HASTA_PV2":
            # Solo las capas 0–2; al superar PV2 se vuelve a pedir autorización con el resto (7.10, regla 1; A.2)
            st["autorizado_hasta"] = "PV2"
            rest = self._estimar_resto(st, "F3P")
            st["autorizado_min"] = float(minutos or (st["consumido_min"] + rest["minutos_p80"]))
        elif opcion == "DIVIDIR_EN_FASES":
            st["fase_division"] = 1
            st["recortes"].append(f"Análisis dividido en fases ({aut_id}): fase 1 = ámbito y veredicto; la selección de candidatos va en la fase 2")
            rest = self._estimar_resto(st)
            f1 = next((float(x.get("minutos_p80") or 0) for o in st.get("ultimas_opciones") or [] if o.get("opcion") == "DIVIDIR_EN_FASES"
                       for x in o.get("fases") or [] if x.get("fase") == 1), 0.0)
            st["autorizado_min"] = float(max(st["consumido_min"] + rest["minutos_p80"], f1))
            self._estado_pet(st, "DIVIDIDA")
        elif opcion == "CANCELAR":
            resumen = {"pet_id": st["pet_id"], "tipo": "RESUMEN_N0", "fases_cerradas": list(st["tiempos"]),
                       "conclusiones_provisionales": st.get("conclusiones_provisionales", []),
                       "minutos_consumidos": round(st["consumido_min"], 1), "nota": "Cancelada por el Broker; lo hecho queda registrado y reutilizable."}
            self.ent.salida.mkdir(parents=True, exist_ok=True)
            (self.ent.salida / f"{self.ent.as_of}_resumen-n0_{st['pet_id']}.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1), encoding="utf-8")
            self._estado_pet(st, "CANCELADA")
            st["terminado"] = True
            st["resultado"] = {"pet_id": st["pet_id"], "estado": "CANCELADA", "resumen_n0": resumen}

    # =========================================================================================================
    # Autorización del Broker (CT-B-05, respuesta) y reanudación
    # =========================================================================================================
    def autorizar(self, aut_id: str, opcion: str, minutos: Optional[float] = None, decidido_por: str = "BROKER",
                  motivo: Optional[str] = None) -> Dict:
        if opcion not in ht08.OPCIONES:
            raise ValueError(f"Opción no válida {opcion}")
        if decidido_por not in ("BROKER", "USUARIO_VIA_BROKER"):
            raise ValueError("decidido_por debe ser BROKER o USUARIO_VIA_BROKER")
        self._revisar_autorizaciones()
        a = self.alm.estado("F1", tipo="AUTORIZACION").get(aut_id)
        if not a:
            raise KeyError(f"No existe la autorización {aut_id}")
        if a.get("estado") != "PENDIENTE":
            return {"aut_id": aut_id, "estado": a.get("estado"), "nota": "La autorización no está pendiente"}
        if minutos is not None and float(minutos) <= 0:
            raise ValueError("minutos debe ser positivo")
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AUTORIZACION", "id": aut_id, "estado": "DECIDIDA",
                                           "decision": {"opcion": opcion, "minutos_autorizados": minutos, "decidido_por": decidido_por,
                                                        "motivo": motivo, "timestamp": self.alm.reloj.ahora()}})
        ruta = self.alm.dir_puntos_control / f"{a['checkpoint_reanudacion']}.json"
        st = ht08.cargar_punto_control(ruta)
        if st["siguiente"] == "FASE2":          # fase 2 de un análisis dividido: se reanuda en la selección (F5)
            st["siguiente"] = "F5"
        self._aplicar_decision(st, opcion, minutos, aut_id)
        if st.get("terminado"):
            return st["resultado"]
        return self.ejecutar(st)

    def _revisar_autorizaciones(self) -> None:
        """Recordatorio a las 24 h y CADUCADA a los 7 días (Anexo A)."""
        ahora = self.alm.reloj.ahora()
        for a in self.alm.estado("F1", tipo="AUTORIZACION").values():
            if a.get("estado") not in ("PENDIENTE",) or not a.get("solicitada"):
                continue
            e = ht08.estado_autorizacion(a["solicitada"], ahora, self.pt.get("recordatorio_h", 24), self.pt.get("caducidad_dias", 7))
            if e == "CADUCADA":
                self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AUTORIZACION", "id": a["id"], "estado": "CADUCADA"})
                self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "PETICION", "id": a["pet_id"], "estado": "CADUCADA"})
            elif e == "RECORDATORIO" and not a.get("recordatorio_enviado"):
                self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AUTORIZACION", "id": a["id"], "recordatorio_enviado": ahora})

    # =========================================================================================================
    # F0 · Recepción, estrategia, plan y estimación
    # =========================================================================================================
    def _f0(self, st: Dict) -> None:
        pet = st["peticion"]
        disp = {k: {kk: a.get(kk) for kk in ("nombre", "tipo_objeto", "tipos_activo", "horizonte", "region")}
                for k, a in self.ent.ambitos.items()}
        admitidos = [t for t in (pet.get("tipos_activo_admitidos") or list(TIPOS_ACTIVO)) if t in TIPOS_ACTIVO]
        r = self.inv.llamar("AG-B02", "CT-B-08", "plan",
                            {"pet_id": st["pet_id"], "objeto": pet.get("objeto"), "origen": pet.get("origen"),
                             "paquete_para_bloque_B": pet.get("paquete_para_bloque_B"), "tipos_activo_admitidos": admitidos,
                             "tipos_todos": list(TIPOS_ACTIVO), "horizontes": pet.get("horizontes"), "preguntas": pet.get("preguntas"),
                             "ambitos_disponibles": disp, "nivel": pet.get("nivel", "AUTO")},
                            "Encuadra el ámbito, elige la estrategia (8.3) y compón el plan de análisis PLAN-B (7.4 F0, puntos 3–6). "
                            "Elige «clave_universo» entre los ámbitos disponibles.",
                            {"clave_universo": "string", "tipo_objeto": "string", "ambito": "object",
                             "tipos_activo_aplicables": "array", "horizonte_dominante": "string", "hipotesis": "array"},
                            self._ctx("AG-B02"), st["run_id"])
        clave = r.get("clave_universo") if r.get("clave_universo") in self.ent.ambitos else \
            ((pet.get("objeto") or {}).get("clave_universo") or next(iter(self.ent.ambitos)))
        amb = self.ent.ambitos.get(clave, {})
        if r.get("_no_conforme"):
            st["estados_degradados"].append("Plan del Director no conforme: se aplica el plan por defecto del ámbito (degradado)")
        tipo_obj = r.get("tipo_objeto") if r.get("tipo_objeto") in TIPOS_OBJETO else amb.get("tipo_objeto", "SECTOR")
        hz = r.get("horizonte_dominante") if r.get("horizonte_dominante") in HORIZONTES else amb.get("horizonte", "H3")
        if pet.get("horizontes") and hz not in pet["horizontes"]:
            hz = next((h for h in pet["horizontes"] if h in HORIZONTES), hz)
        if ht09.TABLA_HORIZONTES_OBJETO.get(tipo_obj, ("SI",) * 5)[HORIZONTES.index(hz)] == "NO":
            hz_amb = amb.get("horizonte", "H3")
            st["limitaciones"].append(f"Horizonte {hz} no aplicable al tipo de objeto {tipo_obj} (8.6): horizonte principal {hz_amb}")
            hz = hz_amb
        con_universo = [t for t in TIPOS_ACTIVO if any(clave in (f.get("ambitos") or "").split(";") for f in self.ent.universos.get(t, []))]
        aplic = [t for t in (r.get("tipos_activo_aplicables") or amb.get("tipos_activo") or []) if t in admitidos and t in con_universo]
        noap: Dict[str, str] = {}
        for t in list(aplic):
            ap = ht09.TABLA_HORIZONTES[t][HORIZONTES.index(hz)]
            if ap == "NO":
                aplic.remove(t)
                noap[t] = f"Horizonte {hz} no aplicable a {t} (8.6)"
        if not aplic and con_universo:
            aplic = [t for t in con_universo if t in admitidos][:1]
        for t in TIPOS_ACTIVO:
            if t not in aplic:
                noap.setdefault(t, (r.get("tipos_no_aplicables") or {}).get(t) or
                                ("No admitido por el Broker" if t not in admitidos else "Sin exposición material a la tesis del ámbito"))
        nivel = self._nivel(pet, clave)
        materiales = [t for t in (r.get("tipos_materiales") or aplic[:1]) if t in aplic] or aplic[:1]
        desv = {k: int(v) for k, v in (r.get("desviaciones") or {}).items() if k in ht03.DIMENSIONES}
        estr = ht03.estrategia(tipo_obj, hz, materiales, nivel if nivel != "PERS" else "N2", desv or None,
                               segmento_tipo=aplic[0] if aplic else None)
        n_def = (self.cfg.get("top_n") or {}).get(nivel, [5, 2])
        top_n = [int(pet["top_n"]), n_def[1]] if pet.get("top_n") else list(n_def)
        a_ = amb or {}
        ambito = {"nombre": (r.get("ambito") or {}).get("nombre") or a_.get("nombre"),
                  "nombre_llano": (r.get("ambito") or {}).get("nombre_llano") or a_.get("nombre_llano"),
                  "incluye": (r.get("ambito") or {}).get("incluye") or a_.get("incluye"),
                  "excluye": (r.get("ambito") or {}).get("excluye") or a_.get("excluye"),
                  "region": (r.get("ambito") or {}).get("region") or a_.get("region")}
        hips = [h for h in (r.get("hipotesis") or []) if isinstance(h, dict) and h.get("enunciado")]
        minimo = {"N1": 2, "N2": 3, "N3": 3, "PERS": 2}[nivel]
        while len(hips) < minimo:
            hips.append({"enunciado": "Hipótesis competidora de naturaleza cíclica (añadida por el plan por defecto)",
                         "naturaleza": "cíclica", "discriminante": "persistencia de la señal", "indicador_anticipado": "tendencia del indicador",
                         "invalidacion": "reversión del indicador"})
        for i, h in enumerate(hips):
            h["hip_id"] = f"HIP-B-{st['pet_id'][6:]}-{i}"
        st["horizontes_secundarios"] = [h for h in (pet.get("horizontes") or []) if h in HORIZONTES and h != hz]
        st.update({"clave": clave, "nivel": nivel, "tipo_objeto": tipo_obj, "horizonte": hz, "tipos_aplicables": aplic,
                   "tipos_no_aplicables": noap, "tipos_materiales": materiales, "estrategia": estr, "top_n": top_n,
                   "plan": {"ambito": ambito, "preguntas": (pet.get("preguntas") or []) + list((pet.get("paquete_para_bloque_B") or {}).get("preguntas_para_B") or []),
                            "preguntas_decisivas": r.get("preguntas_decisivas") or [], "hipotesis": hips,
                            "rasgos": r.get("rasgos_candidatos") or {}, "exclusiones": [e for e in (r.get("exclusiones") or [])
                                                                                         if isinstance(e, dict) and e.get("dim") in ht03.DIMENSIONES and e.get("motivo")
                                                                                         and estr["profundidad"].get(e["dim"]) == "P0"]},
                   "relevancia_origen": (pet.get("paquete_para_bloque_B") or {}).get("relevancia_decisional")})
        # Universos (HT-11) para la estimación y F1
        marco = dict(self.cfg.get("marco_invertibilidad") or {})
        marco.update(pet.get("marco_invertibilidad") or {})
        st["marco"] = marco
        st["universos"] = {}
        for t in aplic:
            u = ht11.construir_universo(t, [{"nombre": f"universo_{t}.csv (HT-11)", "filas": self.ent.universos[t]}], self.ent.as_of,
                                        clave, hz, marco)
            st["universos"][t] = _j(u)
        # GC0: ficha vigente de la Biblioteca
        fichas = [e for e in self.alm.leer("F6", self.ent.as_of) if e.get("mkt_clave") == clave]
        st["gc0"] = ("Ficha MKT-B vigente reutilizada con re-verificación: " + fichas[-1]["id"]) if fichas and \
            (dt.date.fromisoformat(self.ent.as_of) - dt.date.fromisoformat(fichas[-1]["_fecha"])).days <= 30 else \
            "Sin ficha MKT-B vigente del ámbito: análisis completo"
        st["mkt_previa"] = fichas[-1]["id"] if fichas else None
        st["mkt_previa_descartar"] = bool(fichas) and fichas[-1].get("veredicto") == "DESCARTAR" and st["gc0"].startswith("Ficha")
        self._recibir_consultas(st, r.get("consultas_propuestas"), "AG-B02", 0)
        # Conocimiento metodológico (CT-B-12) en N2/N3
        if nivel in ("N2", "N3"):
            refs = self.ent.refs.por_areas(["TB-22", "TB-18", "TB-03"], 6, self._anio_max())
            k = self.inv.llamar("AG-B18", "CT-B-12", "conocimiento", {"pregunta": f"Método para un ámbito {tipo_obj}",
                                                                      "objetivo": "método", "referencias_candidatas": refs},
                                "Selecciona referencias de método de F7 para el plan.", {"referencias": "array"},
                                self._ctx("AG-B18"), st["run_id"])
            st["referencias_metodo"] = [x.get("ref_id") for x in (k.get("referencias") or []) if isinstance(x, dict)]
        # Estimación (HT-08)
        est = ht08.estimar(self._plan_ht08(st), self.pt.get("modelo"))
        st["estimacion"] = est
        st["estimacion_fases"] = est["desglose_por_fase"]
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "PETICION", "id": st["pet_id"], "estado": "PLANIFICADA", "nivel": nivel,
                                           "plan_id": f"PLAN-B-{st['pet_id'][6:]}-v1", "estimacion": est, "clave_universo": clave,
                                           "tipos_aplicables": aplic})

    def _nivel(self, pet: Dict, clave: str) -> str:
        n = pet.get("nivel", "AUTO")
        if n in ("N1", "N2", "N3", "PERS"):
            return n
        rel = (pet.get("paquete_para_bloque_B") or {}).get("relevancia_decisional")
        ficha = [e for e in self.alm.leer("F6", self.ent.as_of) if e.get("mkt_clave") == clave]
        vigente = bool(ficha) and (dt.date.fromisoformat(self.ent.as_of) - dt.date.fromisoformat(ficha[-1]["_fecha"])).days < \
            int(((self.cfg.get("niveles") or {}).get("criterio_auto") or {}).get("n1_ficha_dias", 30))
        if pet.get("alto_impacto") or (rel == "ALTA" and not vigente):
            return "N3"
        if vigente and len(pet.get("preguntas") or []) <= 1:
            return "N1"
        return "N2"

    def _anio_max(self) -> Optional[int]:
        return dt.date.fromisoformat(self.ent.as_of).year if self.ent.modo == "backtest" else None

    # =========================================================================================================
    # F1 · Reconocimiento y mapa del mercado
    # =========================================================================================================
    def _f1(self, st: Dict) -> None:
        amb = self.ent.ambitos.get(st["clave"], {})
        r = self.inv.llamar("AG-B03", "CT-B-09", "reconocimiento",
                            {"pet_id": st["pet_id"], "ambito": st["plan"]["ambito"], "cadena_orientativa": amb.get("cadena"),
                             "universo_preliminar": {t: [f.get("nombre") for f in st["universos"][t]["incluidos"]][:20] for t in st["tipos_aplicables"]}},
                            "Define el mercado y su mapa preliminar de cadena de valor (F1).", {"definicion": "string", "mapa_preliminar": "array"},
                            self._ctx("AG-B03"), st["run_id"])
        cadena = [x for x in (r.get("mapa_preliminar") or []) if isinstance(x, dict) and x.get("eslabon")]
        if not cadena:
            cadena = [{"eslabon": e, "papel_del_ambito": "es"} for e in (amb.get("cadena") or ["Ámbito"])]
        for c in cadena:
            if c.get("papel_del_ambito") not in ("es", "consume", "alimenta"):
                c["papel_del_ambito"] = "es"
        st["mapa_preliminar"] = cadena
        st["definicion"] = r.get("definicion")
        # Datos del ámbito: indicador, referencia y declaraciones DAT-B (Curador, parte determinista)
        ind = (amb.get("indicador") or {}).get("simbolo")
        ref = (amb.get("referencia") or {}).get("simbolo") or ind
        st["indicador"] = amb.get("indicador") or {"nombre": "Indicador del ámbito", "simbolo": ind}
        st["referencia"] = amb.get("referencia") or {"nombre": "Referencia", "simbolo": ref}
        st["dat"] = {}
        for t in st["tipos_aplicables"]:
            st["dat"][f"precios_{t}"] = self._dat(st, f"Precios de cierre HT-01 del universo {t}", "precios", t)
            st["dat"][f"fundamentales_{t}"] = self._dat(st, f"Métricas del universo {t} (instantánea en punto del tiempo)", "fundamentales", t)
        st["dat"]["indicador"] = self._dat(st, f"Serie del indicador {ind} y de la referencia {ref}", "precios", None)
        mp = self.motor.metricas_precio(ind, ref) if ind else {}
        st["indicador_metricas"] = _j(mp)
        H = int((self.cfg.get("horizontes_sesiones") or {}).get(st["horizonte"], 63))
        esc = self.motor.escenarios(ind, ref, min(H, 252), _semilla_pet(st, "esc")) if ind else {"disponible": False}
        st["escenarios_motor"] = _j(esc)
        if not esc.get("disponible"):
            st["estados_degradados"].append(f"Escenarios del Motor no disponibles: {esc.get('motivo')}")
        st["conclusiones_provisionales"] = [f"Ámbito delimitado: {st['plan']['ambito']['nombre']}"]
        # Prueba de viabilidad (capa 1): tesis básica, materialidad, ya descontado, alertas graves (7.10, PV1)
        v = self.inv.llamar("AG-B02", "CT-B-08", "viabilidad",
                            {"pet_id": st["pet_id"], "ambito": st["plan"]["ambito"], "tipo_objeto": st["tipo_objeto"], "horizonte": st["horizonte"],
                             "metricas_indicador": st["indicador_metricas"], "mapa_preliminar": cadena,
                             "universo_preliminar": {t: st["universos"][t]["tamano_invertible"] for t in st["tipos_aplicables"]},
                             "biblioteca": st.get("gc0"), "paquete_para_bloque_B": st["peticion"].get("paquete_para_bloque_B")},
                            "Prueba de viabilidad (capa 1): tesis básica y mecanismo, ¿ya descontado? (lectura rápida de D9), señales de alerta "
                            "graves de integridad y emergentes materiales por eslabón. PV1 la calcula el ejecutor con HT-03.",
                            {"tesis_basica": "string", "ya_descontado": "boolean", "sin_mecanismo": "boolean", "alerta_integridad": "boolean"},
                            self._ctx("AG-B02"), st["run_id"])
        self._recibir_consultas(st, v.get("consultas_propuestas"), "AG-B02", 1)
        st["viabilidad"] = {k: v.get(k) for k in ("tesis_basica", "ya_descontado", "sin_mecanismo", "alerta_integridad", "materialidad",
                                                 "emergentes_materiales") if k in v}

    def _dat(self, st: Dict, descripcion: str, clase: str, tipo: Optional[str]) -> str:
        did = self.alm.nuevo_id("DAT-B")
        ultimo = None
        self.alm.escribir("F2", "AG-B15", {"tipo_entrada": "DAT", "id": did, "pet_id": st["pet_id"], "descripcion": descripcion,
                                           "procedencia": "HT-01 (proveedor " + self.ent.prov.nombre + ")", "fecha_extraccion": self.ent.as_of,
                                           "periodo": f"hasta {self.ent.as_of}", "frecuencia": "diaria" if clase == "precios" else "instantánea",
                                           "version": "original", "fecha_corte": self.ent.as_of, "tipo_activo": tipo,
                                           "comprobaciones": {"unidades_divisas": True, "faltantes": True, "duplicados": True,
                                                              "sesgo_supervivencia": "universo en punto del tiempo (HT-11)",
                                                              "anticipacion": "guardia as_of de HT-01", "previsiones_separadas": True},
                                           "apta_cifra_critica": True})
        return did

    # =========================================================================================================
    # F2 · Análisis dimensional en paralelo
    # =========================================================================================================
    def _f2l(self, st: Dict) -> None:
        """Capa 2 · dimensiones líderes (8.3.4): estructura y cadena a nivel macro, demanda, economía y valoración."""
        dims = [d for d in (st["estrategia"].get("dimensiones_capa2") or ["D2", "D4", "D8", "D9"])]
        self._f2_dims(st, dims, 2)

    def _f2r(self, st: Dict) -> None:
        """Capa 3 · resto de dimensiones, desglose completo de la cadena y cuellos (8.7.1–8.7.2) y radar (8.7.3)."""
        hechas = {d["dim"] for d in st.get("dimensiones") or []}
        self._f2_dims(st, [d for d in ht03.DIMENSIONES if d not in hechas], 3)
        self._desglose(st)
        self._radar(st)

    def _f2_dims(self, st: Dict, dims_sel: List[str], capa: int) -> None:
        estr = st["estrategia"]
        excl = {e["dim"] for e in st["plan"]["exclusiones"]}
        sel = [d for d in dims_sel if d not in excl]
        activos = {a: v for a, v in estr["activacion"].items() if v["activo"] and v.get("dimensiones")}
        por_agente: Dict[str, List[str]] = {}
        cubiertas = set()
        for ag, v in activos.items():
            dims = [d for d in v["dimensiones"] if d in sel]
            if dims:
                por_agente[ag] = dims
                cubiertas |= set(dims)
        director = [d for d in sel if d not in cubiertas]
        datos = [st["dat"]["indicador"]] + [st["dat"][k] for k in st["dat"] if k != "indicador"][:2]
        calc = [c for c in [st["escenarios_motor"].get("calc_id")] if c]
        anio = self._anio_max()
        frescura = {"H1": "1 día", "H2": "3 días", "H3": "7 días", "H4": "30 días", "H5": "90 días"}[st["horizonte"]]

        def encargo(ag: str, dims: List[str], tarea: str) -> Tuple[str, Dict]:
            areas = sorted({a for d in dims for a in AREAS_DIM.get(d, [])})
            msg = {"pet_id": st["pet_id"], "dimensiones": dims, "capa": capa, "ambito": st["plan"]["ambito"], "tipo_objeto": st["tipo_objeto"],
                   "pesos": {d: estr["pesos_efectivos"][d] for d in dims}, "profundidad": {d: estr["profundidad"][d] for d in dims},
                   "preguntas_decisivas": st["plan"]["preguntas_decisivas"], "hipotesis_a_discriminar": [h["enunciado"] for h in st["plan"]["hipotesis"]],
                   "frescura_max": frescura, "datos_disponibles": datos, "calculos_disponibles": calc, "indicador": st["indicador"],
                   "metricas_indicador": st["indicador_metricas"], "referencias": self.ent.refs.por_areas(areas, 6, anio),
                   "items_lista_profesional": [i for i, x in sintesis.LISTA_PROFESIONAL.items() if set(x[1]) & set(dims)]}
            r = self.inv.llamar(ag, "CT-B-09", tarea, msg, "Elabora el informe dimensional de tus dimensiones (CT-B-09). En notas con fuente fechada, copia en fechas los campos fecha_fenomeno, fecha_publicacion y conocible_desde de la fuente. Omite lo desconocido.",
                                {"dim_informes": "array"}, self._ctx(ag), st["run_id"])
            return ag, r

        trabajos = [(ag, dims, "informe_dimensional") for ag, dims in por_agente.items()]
        if director:
            trabajos.append(("AG-B02", director, "cobertura_dimensiones"))
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
            res = list(ex.map(lambda x: encargo(*x), trabajos))
        informes: Dict[str, Dict] = {}
        for ag, r in res:
            self._recibir_consultas(st, r.get("consultas_propuestas"), ag, capa)
            for inf in r.get("dim_informes") or []:
                if isinstance(inf, dict) and inf.get("dim") in sel:
                    inf["especialista"] = "DIR" if ag == "AG-B02" else ag
                    informes[inf["dim"]] = inf
        for d in sel:   # dimensión sin informe conforme: se declara laguna (nunca se inventa)
            if d not in informes:
                ag = next((a for a, ds in por_agente.items() if d in ds), "DIR")
                informes[d] = {"dim": d, "especialista": ag, "notas": [{"afirmacion": "Informe no disponible: dimensión tratada solo con los datos de mercado del indicador.",
                                                                        "etiqueta": "[ESPECULACIÓN]"}],
                               "conclusion": "Sin conclusión sólida: laguna declarada.", "confianza": {"nivel": "baja"},
                               "lagunas": ["Informe dimensional no conforme"]}
                st["estados_degradados"].append(f"{d}: informe dimensional no conforme (laguna declarada)")
        # Curador: ingesta, CLM-B/EVD-B y verificación del etiquetado (CT-B-15)
        piezas = []
        dims_out = []
        for d in ht03.DIMENSIONES:
            if d not in informes:
                continue
            inf = informes[d]
            notas = []
            for n in inf.get("notas") or []:
                if not isinstance(n, dict) or not n.get("afirmacion"):
                    continue
                marcas = {}
                if "fechas" in n or any(k in n for k in CAMPOS_FECHA):
                    if not fechas_de_fuente(n, self.ent.as_of, self.ent.reloj.zona):
                        continue
                    marcas = {k: n.get("fechas", {}).get(k, n.get(k)) for k in CAMPOS_FECHA}
                et = controlado(n.get("etiqueta"), "etiqueta", "[INTERPRETACIÓN]")
                usa_d = [x for x in (n.get("usa_datos") or []) if str(x).startswith("DAT-B-")]
                usa_c = [x for x in (n.get("usa_calculos") or []) if str(x).startswith("CALC-B-")]
                if et == "[HECHO]" and not (usa_d or usa_c):
                    et = "[INTERPRETACIÓN]"     # el Curador rebaja un [HECHO] sin soporte (8.9)
                cifra = bool(n.get("contiene_cifra")) or bool(re.search(r"\d+(?:[.,]\d+)?\s?(%|M€|€|puntos)", n["afirmacion"]))
                clase = controlado(n.get("clase_cifra"), "clase_cifra", "juicio_experto") if cifra else None
                clm = self.alm.nuevo_id("CLM-B")
                evd = self.alm.nuevo_id("EVD-B")
                self.alm.escribir("F2", "AG-B15", {"tipo_entrada": "EVD", "id": evd, "pet_id": st["pet_id"], "fuente": "HT-01" if usa_d else inf["especialista"],
                                                   "raiz": usa_d[0] if usa_d else evd, "independiente": True, "nivel_fuente": "A" if usa_d else "C provisional",
                                                   "fechas": {"recuperacion": self.ent.as_of, **marcas}, "estado": "VIGENTE"})
                self.alm.escribir("F2", "AG-B15", {"tipo_entrada": "CLM", "id": clm, "pet_id": st["pet_id"], "dim": d, "afirmacion": n["afirmacion"][:500],
                                                   "etiqueta": et, "clase_cifra": clase, "evd": [evd], "dat": usa_d, "calc": usa_c})
                nota = {"afirmacion": n["afirmacion"], "etiqueta": et, "evidencias": [clm], "datos": usa_d, "calculos": usa_c,
                        "contiene_cifra": cifra}
                if clase:
                    nota["clase_cifra"] = clase
                notas.append(nota)
                piezas.append({"ref": clm, "etiqueta": et})
            if not notas:
                notas = [{"afirmacion": "Sin notas conformes: laguna declarada.", "etiqueta": "[ESPECULACIÓN]", "evidencias": []}]
            conf = inf.get("confianza") or {}
            dims_out.append({"dim": d, "nombre": sintesis.NOMBRE_DIM[d], "especialista": inf["especialista"], "capa": capa,
                             "profundidad_tratada": estr["profundidad"][d], "pregunta_central": sintesis.PREGUNTA_DIM[d], "notas": notas,
                             "conclusion": inf.get("conclusion") or "Sin conclusión declarada.",
                             "confianza": {"nivel": controlado(conf.get("nivel"), "confianza", "media"),
                                           "factores_a_favor": conf.get("factores_a_favor") or [], "factores_en_contra": conf.get("factores_en_contra") or []},
                             "lagunas": inf.get("lagunas") or [], "discrepancias": [], "senales_para_otras_dimensiones": inf.get("senales_para_otras_dimensiones") or []})
        if piezas:
            self.inv.llamar("AG-B15", "CT-B-15", "ingesta", {"pet_id": st["pet_id"], "piezas": piezas[:60]},
                            "Verifica etiquetas, raíces e independencia de las piezas ingeridas.", {"piezas": "array"},
                            self._ctx("AG-B15"), st["run_id"])
        previas = [d for d in st.get("dimensiones") or [] if d["dim"] not in informes]
        st["dimensiones"] = sorted(previas + dims_out, key=lambda d: ht03.DIMENSIONES.index(d["dim"]))
        st["gc1"] = {d["dim"]: ("laguna declarada" if d["lagunas"] else "suficiente") for d in st["dimensiones"]}
        lagunas = [l for d in dims_out for l in d["lagunas"]]
        if lagunas and capa == 3:   # Buscador de Fuentes Avanzadas (CT-B-11) sobre la laguna principal
            b = self.inv.llamar("AG-B20", "CT-B-11", "conocimiento",
                                {"pregunta": lagunas[0], "objetivo": "dato", "valor_informativo": "puede mover E",
                                 "referencias_candidatas": self.ent.refs.por_areas(["TFB-04", "TFB-01", "TFB-15"], 6, anio)},
                                "Busca fuentes gratuitas para la laguna declarada.", {"referencias": "array"}, self._ctx("AG-B20"),
                                st["run_id"], busqueda=True)
            if b.get("requiere_credencial") or self.ent.boveda.estado()["flujos_etf_diarios"]["estado"] == "SIN_CREDENCIAL":
                self._solicitar_credencial(st, "flujos_etf_diarios")

    # ---------------------------------------------------------------------------------------------------------
    # Capa 3 · desglose jerárquico de la cadena y cuellos de botella (8.7.1–8.7.2; VC-DESG-001, VC-BOT-001)
    # ---------------------------------------------------------------------------------------------------------
    def _desglose(self, st: Dict) -> None:
        estr = st["estrategia"]
        excl = {e["dim"] for e in st["plan"]["exclusiones"]}
        sin_cadena = estr["profundidad"].get("D4") == "P0" or "D4" in excl or not st.get("mapa_preliminar")
        if sin_cadena:
            st["desglose"] = [self._eslabon_unico(st)]
            st["eslabon_critico"] = "ESL-00"
            return
        univ = {t: [{"id": f.get("id"), "nombre": f.get("nombre"), "subcluster": f.get("subcluster")} for f in st["universos"][t]["incluidos"]][:30]
                for t in st["tipos_aplicables"]}
        d3 = next((d["conclusion"] for d in st["dimensiones"] if d["dim"] == "D3"), None)
        d5 = next((d["conclusion"] for d in st["dimensiones"] if d["dim"] == "D5"), None)
        r = self.inv.llamar("AG-B03", "CT-B-09", "desglose_cadena",
                            {"pet_id": st["pet_id"], "mapa_preliminar": st["mapa_preliminar"], "universo_preliminar": univ,
                             "nivel": st["nivel"], "alcance": {"N1": "eslabón crítico hasta actividad", "N3": "cadena completa hasta insumo"}.get(
                                 st["nivel"], "eslabones del plan hasta actividad e insumos críticos de los eslabones con cuello"),
                             "aportes_AG_B05": d3, "aportes_AG_B06": d5,
                             "indicadores_cuello": list(ht03.PARAMETROS_POR_DEFECTO["umbrales_cuello"])},
                            "Desglosa la cadena (macro-eslabón → sub-eslabón → actividad → insumo) con identificadores ESL-, métricas por "
                            "nivel, indicadores de cuello con su valor y la fuente, persistencia y relevancia para el valor, y componentes de AE "
                            "(8.7.1–8.7.2, 9.12). El ejecutor calcula PCB y AE con HT-03.",
                            {"eslabones": "array"}, self._ctx("AG-B03"), st["run_id"])
        self._recibir_consultas(st, r.get("consultas_propuestas"), "AG-B03", 3)
        crudos = [e for e in (r.get("eslabones") or []) if isinstance(e, dict) and RE_ESL.match(str(e.get("eslabon_id") or ""))
                  and e.get("nombre")]
        if not crudos:
            st["estados_degradados"].append("Desglose de la cadena no conforme: macro-eslabones del mapa preliminar sin indicadores (degradado)")
            crudos = [{"eslabon_id": f"ESL-{i:02d}", "nombre": c["eslabon"], "nivel": "macro",
                       "papel_ambito": c["papel_del_ambito"].upper(), "indicadores_cuello": [], "persistencia_meses": 3, "relevancia_valor": 1,
                       "componentes_AE": {}} for i, c in enumerate(st["mapa_preliminar"], start=1)]
        ids = {e["eslabon_id"] for e in crudos}
        calc_desg = self.motor._registrar("desglose_cadena", "MC-B03", {"eslabones": [e["eslabon_id"] for e in crudos]},
                                          {"n_eslabones": len(crudos)}, perfil="VC-DESG-001", plan="MIN")
        salida = []
        for e in crudos:
            ind = [{"indicador": x["indicador"], "valor": x.get("valor"), "fuente": x.get("fuente") or st["dat"]["indicador"]}
                   for x in e.get("indicadores_cuello") or [] if isinstance(x, dict) and x.get("indicador") in ht03.PARAMETROS_POR_DEFECTO["umbrales_cuello"]]
            rel = int(e.get("relevancia_valor") or 1) if str(e.get("relevancia_valor") or "1").isdigit() else 1
            cb = ht03.evaluar_cuello(ind, float(e.get("persistencia_meses") or 3), max(1, min(5, rel)))
            calc_bot = self.motor._registrar("cuello_botella", "MC-B04", {"eslabon_id": e["eslabon_id"], "indicadores": ind},
                                             {"PCB": cb["PCB"], "severidad": cb["severidad"]}, perfil="VC-BOT-001", plan="MIN")
            comp = {k: multiplo10((e.get("componentes_AE") or {}).get(k), 50) for k in ht03.PARAMETROS_POR_DEFECTO["pesos_AE"] if k != "cuello"}
            ae = ht03.calcular_AE(dict(comp, cuello=None), cb["PCB"])
            papel = str(e.get("papel_ambito") or "ES").upper()
            m = e.get("metricas") if isinstance(e.get("metricas"), dict) else {}
            salida.append({"eslabon_id": e["eslabon_id"], "padre": e.get("padre") if e.get("padre") in ids else None,
                           "nombre": e["nombre"], "nivel": e.get("nivel") if e.get("nivel") in ht03.NIVELES_ESLABON else "macro",
                           "descripcion": e.get("descripcion") or e["nombre"], "papel_ambito": papel if papel in ("ES", "CONSUME", "ALIMENTA") else "ES",
                           "metricas": {"tamano": m.get("tamano") or {"valor": None, "unidad": "M€", "fecha": None, "fuente": None},
                                        "crecimiento_anual": m.get("crecimiento_anual"), "margen_tipico": m.get("margen_tipico") or {"bruto": None, "operativo": None},
                                        "roic": m.get("roic"), "poder_negociacion": m.get("poder_negociacion") if m.get("poder_negociacion") in ("ALTO", "MEDIO", "BAJO") else "MEDIO",
                                        "hhi": m.get("hhi"), "concentracion_pais": m.get("concentracion_pais"), "capacidad": m.get("capacidad"),
                                        "utilizacion": m.get("utilizacion"), "plazo_entrega_semanas": m.get("plazo_entrega_semanas"),
                                        "sustitutos": m.get("sustitutos") or [], "actores": m.get("actores") or []},
                           "cuello_botella": {"es_cuello": cb["es_cuello"], "severidad": cb["severidad"], "persistencia": cb["persistencia"],
                                              "relevancia_valor": cb["relevancia_valor"], "PCB": cb["PCB"], "material": cb["material"],
                                              "indicadores": [{k: x.get(k) for k in ("indicador", "valor", "estado")} | {"fuente": next(
                                                  (y["fuente"] for y in ind if y["indicador"] == x["indicador"]), None)} for x in cb["indicadores"]],
                                              "causa": e.get("causa") if e.get("causa") in ("capacidad", "tecnologia", "regulacion", "geopolitica", "materia_prima") else "capacidad",
                                              "senal_resolucion": e.get("senal_resolucion") or "Indicadores del cuello de vuelta a verde", "calc_id": calc_bot},
                           "atractivo": {"AE": ae["total"], "desglose": ae["componentes"], "calc_id": calc_desg}})
        salida.sort(key=lambda e: (-e["atractivo"]["AE"], e["eslabon_id"]))
        st["desglose"] = salida
        crit = r.get("eslabon_critico") if r.get("eslabon_critico") in ids else None
        st["eslabon_critico"] = crit or max(salida, key=lambda e: (e["cuello_botella"]["PCB"], e["atractivo"]["AE"]))["eslabon_id"]

    def _eslabon_unico(self, st: Dict) -> Dict:
        """Objeto sin cadena (D4 en P0 o excluida): el ámbito es el eslabón único ESL-00 (8.7.1)."""
        return {"eslabon_id": "ESL-00", "padre": None, "nombre": st["plan"]["ambito"]["nombre"], "nivel": "macro",
                "descripcion": "Ámbito completo (objeto sin cadena de valor propia: D4 en P0 o excluida)", "papel_ambito": "ES",
                "metricas": {"tamano": {"valor": None, "unidad": None, "fecha": None, "fuente": None}, "crecimiento_anual": None,
                             "margen_tipico": {"bruto": None, "operativo": None}, "roic": None, "poder_negociacion": "MEDIO", "hhi": None,
                             "concentracion_pais": None, "capacidad": None, "utilizacion": None, "plazo_entrega_semanas": None, "sustitutos": [], "actores": []},
                "cuello_botella": {"es_cuello": False, "severidad": 1, "persistencia": 1, "relevancia_valor": 1, "PCB": 1, "material": False,
                                   "indicadores": [], "causa": "capacidad", "senal_resolucion": "No aplica (sin cuello)", "calc_id": None},
                "atractivo": {"AE": ht03.calcular_AE({k: 50 for k in ht03.PARAMETROS_POR_DEFECTO["pesos_AE"] if k != "cuello"} | {"cuello": None}, 1)["total"],
                              "desglose": {k: 50 for k in ht03.PARAMETROS_POR_DEFECTO["pesos_AE"] if k != "cuello"} | {"cuello": 0}, "calc_id": None}}

    # ---------------------------------------------------------------------------------------------------------
    # Capa 3 · radar de emergentes, startups y spin-offs (AG-B24, 8.7.3)
    # ---------------------------------------------------------------------------------------------------------
    def _radar(self, st: Dict) -> None:
        act = (st["estrategia"]["activacion"].get("AG-B24") or {})
        st["radar"] = []
        if not act.get("activo"):
            st["radar_motivo"] = f"AG-B24 no activado: {act.get('motivo') or 'no aplica'}"
            return
        esl = [e for e in st["desglose"] if e["nivel"] != "insumo"]
        if st["nivel"] == "N1":
            esl = [e for e in esl if e["eslabon_id"] == st.get("eslabon_critico")] or esl[:1]
        univ = [{"id": f.get("id"), "nombre": f.get("nombre"), "subcluster": f.get("subcluster"), "isin": f.get("isin"),
                 "salida_bolsa_reciente": f.get("salida_bolsa_reciente"), "capitalizacion_meur": f.get("capitalizacion_meur"), "tipo": t}
                for t in st["tipos_aplicables"] for f in st["universos"][t]["incluidos"]][:60]
        r = self.inv.llamar("AG-B24", "CT-B-09", "radar_emergentes",
                            {"pet_id": st["pet_id"], "eslabones": [{"eslabon_id": e["eslabon_id"], "nombre": e["nombre"], "papel": e["papel_ambito"]} for e in esl],
                             "tipos_emergente": list(ht03.TIPOS_EMERGENTE), "senales_prioritarias": ["rondas", "patentes", "subvenciones",
                                                                                                    "salidas a bolsa", "escisiones", "tracción"],
                             "max_emergentes_por_eslabon": 3 if st["nivel"] != "N3" else 6, "universo_cotizado": univ},
                            "Radar de emergentes por eslabón (8.7.3): tipo, financiación, ventaja, tracción, vía de exposición e instrumento, "
                            "criterios 0–100 en múltiplos de 10. El ejecutor calcula PEM con HT-03.", {"radar_emergentes": "array"},
                            self._ctx("AG-B24"), st["run_id"])
        self._recibir_consultas(st, r.get("consultas_propuestas"), "AG-B24", 3)
        ids = {e["eslabon_id"] for e in st["desglose"]}
        por_id = {f["id"]: f for f in univ}
        for g in r.get("radar_emergentes") or []:
            if not isinstance(g, dict) or g.get("eslabon_id") not in ids or not g.get("nombre"):
                continue
            tipo = g.get("tipo") if g.get("tipo") in ht03.TIPOS_EMERGENTE else "STARTUP"
            via = g.get("via_exposicion") if g.get("via_exposicion") in ht03.VIAS_EXPOSICION else "NO_INVERTIBLE_HOY"
            crit = {k: multiplo10((g.get("criterios") or {}).get(k), 50) for k in ht03.PARAMETROS_POR_DEFECTO["pesos_PEM"]}
            pem = ht03.calcular_PEM(crit)["total"]            # MC-B07 agrega con la aritmética de HT-03; el Director confirma con HT-03
            ie = g.get("instrumento_exposicion") if isinstance(g.get("instrumento_exposicion"), dict) else {}
            iu = ie.get("id_universo") if ie.get("id_universo") in por_id else None
            st["radar"].append({"emg_id": self.alm.nuevo_id("EMG-B"), "eslabon_id": g["eslabon_id"], "nombre": g["nombre"], "tipo": tipo,
                                "financiacion_conocida": g.get("financiacion_conocida") if isinstance(g.get("financiacion_conocida"), dict) else None,
                                "tecnologia_o_ventaja": g.get("tecnologia_o_ventaja") or "", "senales_traccion": [str(x) for x in g.get("senales_traccion") or []],
                                "via_exposicion": via,
                                "instrumento_exposicion": {"nombre": ie.get("nombre") or (por_id[iu]["nombre"] if iu else None),
                                                           "isin": ie.get("isin") or (por_id[iu].get("isin") if iu else None), "cand_id": None,
                                                           "id_universo": iu, "tipo_activo": por_id[iu]["tipo"] if iu else None,
                                                           "fuera_de_filtros": bool(via in ht03.VIAS_INVERTIBLES and not iu),
                                                           "motivo": None if iu or via not in ht03.VIAS_INVERTIBLES else "no figura en el universo invertible del Seleccionador (filtros del playbook)"},
                                "criterios": crit, "PEM": pem, "riesgos": [str(x) for x in g.get("riesgos") or []] or ["Ejecución y financiación"],
                                "etiqueta": controlado(g.get("etiqueta"), "etiqueta", "[INTERPRETACIÓN]")})
        if st["radar"]:
            self.motor._registrar("potencial_emergente", "MC-B07", {"emergentes": [g["emg_id"] for g in st["radar"]]},
                                  {"PEM": {g["emg_id"]: g["PEM"] for g in st["radar"]}}, perfil="HT-03 PEM", plan="MIN")

    def _solicitar_credencial(self, st: Dict, conector: str) -> None:
        from .herramientas.boveda import CONECTORES
        c = CONECTORES[conector]
        previas = [e for e in self.alm.estado("F1", tipo="CREDENCIAL").values() if e.get("conector") == conector]
        if not previas:
            cid = self.alm.nuevo_id("CRED-B")
            self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "CREDENCIAL", "id": cid, "pet_id": st["pet_id"], "conector": conector,
                                               "proveedor": c.get("proveedor"), "tipo_acceso": c["tipo_acceso"],
                                               "finalidad": {"dimensiones": c["dimensiones"], "decision_que_puede_cambiar": "E y D10"},
                                               "alcance": {"permisos": "SOLO_LECTURA"}, "degradacion_sin_clave": c.get("degradacion"),
                                               "urgencia": "MEJORA_CALIDAD", "estado": "SOLICITADA",
                                               "credencial_ref": f"alias-{conector.replace('_', '-')}"})
            cred = cid
        else:
            cred = previas[-1]["id"]
        st["estados_degradados"].append(f"Conector {conector} sin clave en la bóveda ({cred}): {c.get('degradacion')}")
        st["limitaciones"].append(f"{c.get('degradacion')} (credencial {cred} pendiente)")

    # =========================================================================================================
    # F3 · Integración, tesis y puntuaciones provisionales
    # =========================================================================================================
    def _f3p(self, st: Dict) -> None:
        """Capa 2 · integración provisional con las dimensiones líderes: tesis provisional, autorrefutación, A y E
        provisionales (7.4 F3; la decisión es PV2, que integra GC2)."""
        esc = st["escenarios_motor"]
        r = self.inv.llamar("AG-B02", "CT-B-08", "integracion_provisional",
                            {"pet_id": st["pet_id"], "ambito_nombre": st["plan"]["ambito"]["nombre"], "horizonte": st["horizonte"], "capa": 2,
                             "informes": [{"dim": d["dim"], "conclusion": d["conclusion"], "confianza": d["confianza"]["nivel"]} for d in st["dimensiones"]],
                             "hipotesis": st["plan"]["hipotesis"], "escenarios_motor": esc, "metricas_indicador": st["indicador_metricas"],
                             "mapa_preliminar": st["mapa_preliminar"], "viabilidad": st.get("viabilidad")},
                            "Integración provisional de la capa 2: tesis provisional, autorrefutación («tesis_viva»), componentes provisionales de "
                            "A y E y, si E es baja, si hay fuentes identificadas que podrían cerrarla («fuentes_para_cerrar_E»).",
                            {"tesis": "object", "componentes_A": "object", "tesis_viva": "boolean"}, self._ctx("AG-B02"), st["run_id"])
        self._recibir_consultas(st, r.get("consultas_propuestas"), "AG-B02", 2)
        compA = {k: multiplo10((r.get("componentes_A") or {}).get(k), 50) for k in ht03.PARAMETROS_POR_DEFECTO["pesos"]["A"]}
        dims_c2 = [d for d in st["estrategia"].get("dimensiones_capa2") or []]
        compE = self._componentes_E(st, r.get("componentes_E") or {}, dims_c2)
        A = ht03.calcular_A(compA, bool(r.get("saturacion_narrativa")))["total"]
        E = ht03.calcular_E(compE)["total"]
        st["capa2"] = {"A": A, "E": E, "tesis": (r.get("tesis") or {}).get("enunciado"), "tesis_viva": bool(r.get("tesis_viva", True)),
                       "fuentes_para_cerrar_E": bool(r.get("fuentes_para_cerrar_E")), "componentes_A": compA, "componentes_E": compE,
                       "autorrefutacion": r.get("autorrefutacion") or r.get("pre_mortem")}
        st["conclusiones_provisionales"].append(f"Capa 2: A provisional {A}, E provisional {E}, tesis {'viva' if st['capa2']['tesis_viva'] else 'refutada'}")

    def _f3(self, st: Dict) -> None:
        esc = st["escenarios_motor"]
        r = self.inv.llamar("AG-B02", "CT-B-08", "integracion",
                            {"pet_id": st["pet_id"], "ambito_nombre": st["plan"]["ambito"]["nombre"], "horizonte": st["horizonte"], "capa": 3,
                             "informes": [{"dim": d["dim"], "conclusion": d["conclusion"], "confianza": d["confianza"]["nivel"]} for d in st["dimensiones"]],
                             "hipotesis": st["plan"]["hipotesis"], "escenarios_motor": esc, "metricas_indicador": st["indicador_metricas"],
                             "mapa_preliminar": st["mapa_preliminar"],
                             "desglose": [{"eslabon_id": e["eslabon_id"], "nombre": e["nombre"], "AE": e["atractivo"]["AE"],
                                           "PCB": e["cuello_botella"]["PCB"], "material": e["cuello_botella"]["material"]} for e in st.get("desglose") or []],
                             "radar": [{"eslabon_id": g["eslabon_id"], "nombre": g["nombre"], "via": g["via_exposicion"], "PEM": g["PEM"]} for g in st.get("radar") or []]},
                            "Integra las dimensiones: tesis falsable, cierre de hipótesis, régimen, cuatro evaluaciones, componentes de A y E (9.1).",
                            {"tesis": "object", "hipotesis_cierre": "array", "regimen": "object", "evaluaciones_separadas": "object",
                             "componentes_A": "object"}, self._ctx("AG-B02"), st["run_id"])
        self._recibir_consultas(st, r.get("consultas_propuestas"), "AG-B02", 3)
        st["integracion"] = r
        cierre = {int(x.get("indice", -1)): controlado(x.get("estado"), "estado_hipotesis", "indeterminada")
                  for x in (r.get("hipotesis_cierre") or []) if isinstance(x, dict)}
        for i, h in enumerate(st["plan"]["hipotesis"]):
            h["estado"] = cierre.get(i, "indeterminada")
        compA = {k: multiplo10((r.get("componentes_A") or {}).get(k), 50) for k in ht03.PARAMETROS_POR_DEFECTO["pesos"]["A"]}
        st["componentes_A"] = compA
        st["componentes_E"] = self._componentes_E(st, r.get("componentes_E") or {})
        st["saturacion"] = bool(r.get("saturacion_narrativa"))
        st["flags"] = {k: bool(v) for k, v in (r.get("flags") or {}).items()
                       if k in ("catalizadores_escalonados", "valoracion_parcialmente_descontada", "dispersion_alta")}
        A = ht03.calcular_A(compA, st["saturacion"])["total"]
        E = ht03.calcular_E(st["componentes_E"])["total"]
        RE = esc.get("RE") if esc.get("disponible") else None
        C = ht03.calcular_C(A, E, 50, RE)["C"]
        st["punt_prov"] = {"A": A, "E": E, "C": C, "RE": RE}
        st.setdefault("gc2", True)     # GC2 se integra en PV2 (fin de la capa 2); una continuación forzada la deja en False
        prov = ht03.veredicto_ambito_provisional(A, E, C, {f"PA{i}": "OK" for i in range(1, 9)}, st["flags"])
        st["veredicto_provisional"] = prov["veredicto"]
        st["conclusiones_provisionales"].append(f"A, E y C provisionales: {A}, {E}, {C}; veredicto provisional {prov['veredicto']}")

    def _componentes_E(self, st: Dict, propuesta: Dict, dims_plan: Optional[List[str]] = None) -> Dict:
        estr = st["estrategia"]
        orden = ["P0", "P1", "P2", "P3"]
        base = [d for d in st["dimensiones"] if dims_plan is None or d["dim"] in dims_plan]
        peso_ok = sum(estr["pesos_efectivos"][d["dim"]] for d in base
                      if orden.index(d["profundidad_tratada"]) >= orden.index(estr["profundidad"][d["dim"]]) and not d["lagunas"])
        if dims_plan:      # capa 2: cobertura relativa a las dimensiones planificadas para la capa (declarado)
            total = sum(estr["pesos_efectivos"][d] for d in dims_plan) or 1
            peso_ok = 100 * peso_ok / total
        notas = [n for d in base for n in d["notas"]]
        traz = sum(1 for n in notas if n.get("evidencias")) / max(len(notas), 1)
        hips = st["plan"]["hipotesis"]
        cerr = sum(1.0 if h.get("estado") in ("confirmada", "debilitada", "invalidada") else 0.5 for h in hips) / max(len(hips), 1)
        fresca = self._dato_fresco(st)
        return {"calidad_raices": multiplo10(propuesta.get("calidad_raices"), 60),
                "cobertura_dimensional": multiplo10(peso_ok),
                "calidad_metodologica": multiplo10(propuesta.get("calidad_metodologica"), 60),
                "trazabilidad": multiplo10(100 * traz), "actualidad": 90 if fresca else 50,
                "discrepancias_resueltas": multiplo10(propuesta.get("discrepancias_resueltas"), 70),
                "hipotesis_cerradas": multiplo10(100 * cerr)}

    def _dato_fresco(self, st: Dict) -> bool:
        f = st["indicador_metricas"].get("ultima_fecha_precio")
        if not f:
            return False
        lim = FRESCURA_MERCADO_DIAS[st["horizonte"]]
        return (dt.date.fromisoformat(self.ent.as_of) - dt.date.fromisoformat(f)).days <= max(lim, 3)

    # =========================================================================================================
    # F4 ∥ F5 · Escenarios y selección
    # =========================================================================================================
    def _f4(self, st: Dict) -> None:
        if st.get("fase_division") == 2:      # fase 2 de un análisis dividido: escenarios ya hechos en la fase 1
            self._pronosticos_ranking(st)
            return
        esc = st["escenarios_motor"]
        proyectable = st["tipo_objeto"] in ("SECTOR", "TEMATICA", "CADENA_DE_VALOR", "MERCADO_GEOGRAFICO")
        r = self.inv.llamar("AG-B13", "CT-B-16", "prospectiva",
                            {"pet_id": st["pet_id"], "tesis": (st["integracion"].get("tesis") or {}).get("enunciado"),
                             "hipotesis": st["plan"]["hipotesis"], "escenarios_motor": esc, "proyectable": proyectable,
                             "cadena": st["mapa_preliminar"]},
                            "Construye escenarios base, favorable y adverso con régimen y disparadores; máquina de proyecciones (8.8).",
                            {"escenarios": "array", "proyecciones": "object"}, self._ctx("AG-B13"), st["run_id"])
        if st["nivel"] == "N3":
            self.inv.llamar("AG-B16", "CT-B-13", "supuestos_calculo", {"calc_id": esc.get("calc_id"), "metodo": "escenarios"},
                            "Declara supuestos e incertidumbre del cálculo (plan EXT).", {"supuestos": "array"}, self._ctx("AG-B16"), st["run_id"])
        st["prospectiva"] = r
        RE = esc.get("RE", 50) if esc.get("disponible") else 50
        bandas = {"base": banda_verbal(max(RE, 100 - RE) / 100 * 0.85 + 0.1), "favorable": "poco probable", "adverso": "poco probable"}
        escs = []
        porn = {e.get("nombre"): e for e in (r.get("escenarios") or []) if isinstance(e, dict)}
        for nom, q in (("base", "p50"), ("favorable", "p90"), ("adverso", "p10")):
            e = porn.get(nom) or {}
            val = esc.get(q)
            escs.append({"nombre": nom, "premisas": e.get("premisas") or f"Escenario {nom} del Motor",
                         "regimen": e.get("regimen") or "régimen vigente", "disparadores": e.get("disparadores") or [],
                         "probabilidad": None, "base_probabilidad": None, "banda": bandas[nom],
                         "resultado_vs_referencia": (f"Rentabilidad relativa frente a {st['referencia']['nombre']}: {val:+.1%} ({q} del Motor)"
                                                     if val is not None else e.get("resultado_vs_referencia") or "No disponible"),
                         "calculos": [esc["calc_id"]] if esc.get("calc_id") else []})
        st["escenarios"] = escs
        st["sensibilidades"] = self.motor.sensibilidades(esc)
        pr = r.get("proyecciones") or {}
        st["proyecciones"] = {"activada": bool(pr.get("activada", proyectable)) and bool(st["sensibilidades"]),
                              "motivo_exclusion": pr.get("motivo_exclusion") or (None if proyectable and st["sensibilidades"] else "Objeto sin premisas proyectables honestas o sin cálculo del Motor"),
                              "etapas": [x for x in (pr.get("etapas") or []) if isinstance(x, dict) and x.get("etapa") and x.get("contenido")],
                              "premisas": [x for x in (pr.get("premisas") or []) if isinstance(x, dict) and x.get("premisa") and x.get("valor") and x.get("fuente")],
                              "brecha_expectativas": pr.get("brecha_expectativas")}
        if st["proyecciones"]["activada"] and not (st["proyecciones"]["etapas"] and st["proyecciones"]["premisas"]):
            st["proyecciones"].update({"activada": False, "motivo_exclusion": "Proyección incompleta: se excluye con motivo (8.8)"})
        # Pronósticos (se congelan en F10)
        H = int((self.cfg.get("horizontes_sesiones") or {}).get(st["horizonte"], 63))
        f_res = (dt.date.fromisoformat(self.ent.as_of) + dt.timedelta(days=int(H * 365 / 252))).isoformat()
        prob = RE / 100 if esc.get("disponible") else 0.5
        pron = [{"prg_id": self.alm.nuevo_id("PRG-B"), "tipo": "AMBITO",
                 "afirmacion": f"El indicador {st['indicador']['simbolo']} supera a {st['referencia']['simbolo']} en rentabilidad total en el horizonte {st['horizonte']}",
                 "horizonte": st["horizonte"], "fecha_emision": self.ent.as_of, "fecha_resolucion": f_res,
                 "criterio": f"Rentabilidad relativa > 0 entre el cierre ≤ {self.ent.as_of} y el cierre ≤ {f_res}",
                 "referencia": st["referencia"]["simbolo"], "indicador": st["indicador"]["simbolo"], "tipo_activo": None,
                 "banda": banda_verbal(prob), "probabilidad_publicada": None, "celda": f"{st['tipo_objeto']}×{(st['tipos_aplicables'] or ['NA'])[0]}×{st['horizonte']}",
                 "referencia_ingenua": "paseo aleatorio (rentabilidad relativa nula)", "fuente": "HT-01", "_prob_interna": round(prob, 4)}]
        if st["horizonte"] == "H5":
            # H5: probabilidades siempre cualitativas y ≥ 3 hitos intermedios verificables a 1–5 años (8.6, R13, 12.8)
            n_h = int((self.cfg.get("capas") or {}).get("hitos_h5_minimos", 3))
            hitos = [h for h in ((r.get("hitos_h5") or []) if isinstance(r.get("hitos_h5"), list) else []) if isinstance(h, dict) and h.get("afirmacion")]
            for k in range(max(n_h, len(hitos[:5]))):
                h = hitos[k] if k < len(hitos) else {}
                anios = min(5, max(1, int(h.get("anios") or (k + 1))))
                f_h = (dt.date.fromisoformat(self.ent.as_of) + dt.timedelta(days=365 * anios)).isoformat()
                pron.append({"prg_id": self.alm.nuevo_id("PRG-B"), "tipo": "HITO_H5",
                             "afirmacion": h.get("afirmacion") or f"Hito {k + 1}: el indicador {st['indicador']['simbolo']} mantiene una rentabilidad relativa positiva frente a {st['referencia']['simbolo']} a {anios} año(s)",
                             "horizonte": "H5", "fecha_emision": self.ent.as_of, "fecha_resolucion": f_h,
                             "criterio": h.get("criterio") or f"Rentabilidad relativa > 0 entre el cierre ≤ {self.ent.as_of} y el cierre ≤ {f_h} (trayectoria del escenario base)",
                             "referencia": st["referencia"]["simbolo"], "indicador": st["indicador"]["simbolo"], "tipo_activo": None,
                             "banda": banda_verbal(prob), "probabilidad_publicada": None, "celda": f"{st['tipo_objeto']}×H5×hito",
                             "referencia_ingenua": "extrapolación lineal de la tendencia reciente (9.11)", "fuente": "HT-01",
                             "hito": {"orden": k + 1, "critico": k < 2}, "_prob_interna": round(prob, 4)})
        st["pronosticos"] = pron
        if st.get("fase_division") != 1 and (st.get("pv") or {}).get("PV3", {}).get("resultado") != "NO_SUPERADA":
            self._pronosticos_ranking(st)

    def _pronosticos_ranking(self, st: Dict) -> None:
        pron = st["pronosticos"]
        f_res = pron[0]["fecha_resolucion"]
        if True:
            for t in st["tipos_aplicables"]:
                pron.append({"prg_id": self.alm.nuevo_id("PRG-B"), "tipo": "RANKING",
                             "afirmacion": f"El top-N {t} equiponderado supera a la media equiponderada del universo {t} cribado en el horizonte {st['horizonte']}",
                             "horizonte": st["horizonte"], "fecha_emision": self.ent.as_of, "fecha_resolucion": f_res,
                             "criterio": "Rentabilidad media del top-N − media del universo cribado > 0",
                             "referencia": f"media equiponderada del universo {t} cribado", "indicador": None, "tipo_activo": t,
                             "banda": "incierto", "probabilidad_publicada": None, "celda": f"{ht03.PLAYBOOKS[t]['perfil']}×{st['horizonte']}",
                             "referencia_ingenua": "ranking aleatorio; ranking por momento", "universo_ref": f"universo {t} cribado a {self.ent.as_of} (anexo, hoja Universo_{t})",
                             "tratamiento_bajas": "un valor dado de baja se valora a su último precio y el importe queda en liquidez hasta la resolución",
                             "fuente": "HT-01", "_prob_interna": 0.5})

    def _f5(self, st: Dict) -> None:
        if st.get("fase_division") == 1:       # fase 1 de un análisis dividido: la selección va en la fase 2
            st["seleccion"] = {t: {"pendiente_fase2": True} for t in st["tipos_aplicables"]}
            for g in st.get("radar") or []:
                if g["instrumento_exposicion"].get("id_universo"):
                    g["instrumento_exposicion"]["motivo"] = "selección pendiente (fase 2 del análisis dividido)"
            return
        sel = {}
        for t in st["tipos_aplicables"]:
            sel[t] = self._seleccionar_tipo(st, t)
        st["seleccion"] = sel
        # Emergentes invertibles del radar enlazados con su candidato (8.7.3)
        por_fila = {(t, c["_fila"].get("id")): cid for t, s in sel.items() for cid, c in (s.get("candidatos") or {}).items()}
        for g in st.get("radar") or []:
            ie = g["instrumento_exposicion"]
            if ie.get("id_universo"):
                ie["cand_id"] = por_fila.get((ie.get("tipo_activo"), ie["id_universo"]))
                if ie["cand_id"] is None:
                    ie["fuera_de_filtros"] = True
                    ie["motivo"] = "no supera los filtros del playbook (PC1–PC4)"
        # Mejores opciones por eslabón provisionales: entran como finalistas en la refutación (9.13, GC3)
        pool = {t: [dict(c, puertas=ht03.puertas_candidato(c, t)) for c in (s.get("candidatos") or {}).values() if c.get("S") is not None]
                for t, s in sel.items()}
        mp = ht03.mejores_por_eslabon(st.get("desglose") or [], pool, st["nivel"] if st["nivel"] in ("N1", "N2", "N3") else "PERS",
                                      st["veredicto_provisional"], bool(st["peticion"].get("candidatos_aun_con_vigilar")), st.get("eslabon_critico"))
        st["mejores_prelim"] = {eid: [o["cand_id"] for o in tb["opciones"]] for eid, tb in mp["tablas"].items()}

    def _seleccionar_tipo(self, st: Dict, t: str) -> Dict:
        u = st["universos"][t]
        pb = ht03.PLAYBOOKS[t]
        N, NA = st["top_n"]
        lim_dias = {"H1": 4, "H2": 5, "H3": 7, "H4": 30, "H5": 90}[st["horizonte"]]
        filas = []
        ids_previos = {e.get("instrumento_id"): e["id"] for e in self.alm.leer("F3") if e.get("tipo_entrada") == "CAND"}
        for f in u["incluidos"]:
            f = dict(f)
            f["cand_id"] = ids_previos.get(f"{st['pet_id']}::{f['id']}") or self.alm.nuevo_id("CAND-B")
            filas.append(f)
        if not filas:
            return {"top_n": [], "alternativas": [], "universo": u, "candidatos": {}, "menos": "Universo invertible vacío"}
        ref = st["referencia"]["simbolo"]
        punt = self.motor.puntuar(t, filas, ref, st["horizonte"], _semilla_pet(st, t), "EXT" if st["nivel"] == "N3" else "STD")
        corr = self.motor.correlaciones({f["cand_id"]: f.get("simbolo") for f in filas})
        cands = []
        for f in filas:
            p = punt["candidatos"][f["cand_id"]]
            pr = p["precio"]
            fresco = pr.get("datos_precio") and (dt.date.fromisoformat(self.ent.as_of) - dt.date.fromisoformat(pr["ultima_fecha_precio"])).days <= lim_dias
            pur = float(f["pureza"]) if f.get("pureza") not in (None, "") else None
            alertas = [{"senal": a, "valor": "presente", "estado": "critica", "verificar_en_C": True} for a in (f.get("alertas_criticas") or "").split(";") if a]
            alertas += [{"senal": a, "valor": "presente", "estado": "no_critica", "verificar_en_C": True} for a in (f.get("alertas_no_criticas") or "").split(";") if a]
            alertas += [{"senal": av, "valor": "aviso de invertibilidad", "estado": "no_critica", "verificar_en_C": True} for av in f.get("avisos_invertibilidad") or []]
            cands.append({"cand_id": f["cand_id"], "S": p["S"], "componentes": p["componentes"], "ic90_S": p.get("ic90_S"),
                          "ic90_rango": p.get("ic90_rango"), "pureza": pur, "invertible": True, "datos_ok": bool(fresco),
                          "alertas": alertas, "emisor": f.get("emisor"), "subcluster": f.get("subcluster") or None,
                          "indice_replicado": f.get("indice_replicado") or None, "_fila": f, "_metricas": p["metricas"], "_precio": pr})
        prov_v = st["veredicto_provisional"]
        res = ht03.seleccionar([{k: v for k, v in c.items()} for c in cands], t, st["nivel"] if st["nivel"] in ("N1", "N2", "N3") else "N2",
                               prov_v, top_n=N, n_alternativas=NA, correlaciones=corr,
                               candidatos_aun_con_vigilar=bool(st["peticion"].get("candidatos_aun_con_vigilar")))
        fin, _ = ht03.lista_corta_gc3([dict(c, puertas=ht03.puertas_candidato(c, t)) for c in cands if c["S"] is not None], N)
        top_ids = [c["cand_id"] for c in res["top_n"]]
        finalistas = [c for c in cands if c["cand_id"] in top_ids or c["cand_id"] in {x["cand_id"] for x in fin}]
        r = self.inv.llamar("AG-B12", "CT-B-10", "seleccion",
                            {"pet_id": st["pet_id"], "tipo_activo": t, "playbook": pb["perfil"], "rasgos": st["plan"]["rasgos"].get(t) or [],
                             "tesis": (st["integracion"].get("tesis") or {}).get("enunciado"),
                             "finalistas": [{"cand_id": c["cand_id"], "nombre": c["_fila"].get("nombre"), "S": c["S"],
                                             "subcluster": c["subcluster"], "pureza": c["pureza"]} for c in finalistas][:2 * N + 2],
                             "eslabones": [{"eslabon_id": e["eslabon_id"], "nombre": e["nombre"], "nivel": e["nivel"], "papel": e["papel_ambito"]}
                                           for e in st.get("desglose") or []],
                             "candidatos_para_eslabon": [{"cand_id": c["cand_id"], "nombre": c["_fila"].get("nombre"), "subcluster": c["subcluster"],
                                                          "pureza": c["pureza"]} for c in cands]},
                            "Traduce los rasgos de la tesis a métricas, redacta el rol en la tesis y las preguntas del encargo C.x de cada finalista "
                            "y asigna cada candidato a su eslabón principal con su pureza de exposición al eslabón (9.4, paso 3 bis).",
                            {"traduccion_rasgos_metricas": "array", "candidatos": "object"}, self._ctx("AG-B12"), st["run_id"])
        self._recibir_consultas(st, r.get("consultas_propuestas"), "AG-B12", 3)
        esl = [e for e in st.get("desglose") or [] if e["nivel"] != "insumo"] or (st.get("desglose") or [])
        ids_esl = {e["eslabon_id"] for e in st.get("desglose") or []}
        asig = r.get("asignacion_eslabones") if isinstance(r.get("asignacion_eslabones"), dict) else {}
        for c in cands:
            a = asig.get(c["cand_id"]) if isinstance(asig.get(c["cand_id"]), dict) else {}
            if a.get("eslabon_id") in ids_esl:
                c["eslabon_id"] = a["eslabon_id"]
                pe = a.get("pureza_eslabon")
                c["pureza_eslabon"] = round(float(pe), 2) if isinstance(pe, (int, float)) and 0 <= pe <= 1 else c.get("pureza")
                c["rol_en_eslabon"] = a.get("rol_en_eslabon")
                c["eslabones_secundarios"] = [x for x in a.get("eslabones_secundarios") or [] if x in ids_esl and x != a["eslabon_id"]]
            else:      # asignación determinista declarada: eslabón «ES» por subclúster (estimada)
                es = [e for e in esl if e["papel_ambito"] == "ES"] or esl
                k = int(hashlib.sha256(str(c.get("subcluster") or c["cand_id"]).encode()).hexdigest(), 16) % max(len(es), 1)
                c["eslabon_id"] = es[k]["eslabon_id"] if es else "ESL-00"
                c["pureza_eslabon"] = round(0.8 * float(c.get("pureza") or 0), 2)
                c["rol_en_eslabon"] = None
                c["eslabones_secundarios"] = []
                c["eslabon_estimado"] = True
        trad = [x for x in (r.get("traduccion_rasgos_metricas") or []) if isinstance(x, dict) and x.get("rasgo")]
        for x in trad:
            x["metricas"] = [str(m) for m in (x.get("metricas") or ["pureza"])]
        return _j({"universo": u, "candidatos": {c["cand_id"]: {k: v for k, v in c.items()} for c in cands},
                   "correlaciones": corr, "calc_puntuar": punt["calc_id"], "seleccion_preliminar": {"top_n": top_ids,
                   "alternativas": [c["cand_id"] for c in res["alternativas"]]},
                   "finalistas": [c["cand_id"] for c in finalistas], "textos": r.get("candidatos") or {},
                   "traduccion": trad or [{"rasgo": "exposición al ámbito", "metricas": ["pureza"], "componente": "PE"}]})

    # =========================================================================================================
    # F6 · Refutación
    # =========================================================================================================
    def _f6(self, st: Dict) -> None:
        objs: List[Dict] = []
        if st["nivel"] in ("N2", "N3", "PERS") and not st.get("refutacion_limitada"):
            finalistas = []
            for t in st["tipos_aplicables"]:
                s = st["seleccion"].get(t) or {}
                for cid in (s.get("seleccion_preliminar") or {}).get("top_n", [])[:5]:
                    c = s["candidatos"][cid]
                    finalistas.append({"cand_id": cid, "tipo": t, "nombre": c["_fila"].get("nombre"), "S": c["S"], "pureza": c["pureza"],
                                       "eslabon_id": c.get("eslabon_id")})
            ya = {f["cand_id"] for f in finalistas}
            for eid, ids in (st.get("mejores_prelim") or {}).items():     # opciones por eslabón añadidas por cobertura (9.13)
                for cid in ids:
                    t = next((t for t in st["tipos_aplicables"] if cid in ((st["seleccion"].get(t) or {}).get("candidatos") or {})), None)
                    if t and cid not in ya:
                        c = st["seleccion"][t]["candidatos"][cid]
                        finalistas.append({"cand_id": cid, "tipo": t, "nombre": c["_fila"].get("nombre"), "S": c["S"], "pureza": c["pureza"],
                                           "eslabon_id": eid, "origen": "MEJORES_POR_ESLABON"})
                        ya.add(cid)
            mapa = {e["eslabon_id"]: e["nombre"] for e in st.get("desglose") or []}
            r = self.inv.llamar("AG-B14", "CT-B-17", "refutacion",
                                {"pet_id": st["pet_id"], "tesis": st["integracion"].get("tesis"), "hipotesis": st["plan"]["hipotesis"],
                                 "escenarios": st["escenarios"], "finalistas": finalistas, "eslabones": mapa},
                                "Refuta la tesis y los finalistas; gradúa las objeciones (fuerte, moderada, débil). Incluye fecha_incidente para cada objeción fuerte cuando esté documentada; omítela si se desconoce.",
                                {"objeciones": "array", "veredicto_tesis": "string"}, self._ctx("AG-B14"), st["run_id"])
            vt = controlado(r.get("veredicto_tesis"), "veredicto_tesis", "fragil")
            validos = {f["cand_id"] for f in finalistas}
            for o in r.get("objeciones") or []:
                if not isinstance(o, dict) or not o.get("argumento"):
                    continue
                objeto = o.get("objeto")
                alcance = {}
                if objeto in ("ESLABON", "CADENA") or (objeto == "TESIS" and "eslabon_id" in o and not o.get("emg_id")):
                    eid = o.get("eslabon_id")
                    if not isinstance(eid, str) or eid not in mapa or o.get("emg_id"):
                        motivo = "CT-B-17: eslabón ambiguo o ausente del mapa"
                        self._estado_pet(st, "BLOQUEADO_AUDITORIA", motivo=motivo)
                        st["terminado"] = True
                        st["resultado"] = {"pet_id": st["pet_id"], "estado_peticion": "BLOQUEADO_AUDITORIA", "motivo": motivo}
                        return
                    afectados = sorted(cid for grupo in st["seleccion"].values()
                                       for cid, cand in (grupo.get("candidatos") or {}).items()
                                       if eid == cand.get("eslabon_id") or eid in (cand.get("eslabones_secundarios") or []))
                    alcance = {"x_eslabon_id": eid, "x_nombre_eslabon": mapa[eid], "x_candidatos_afectados": afectados}
                    objeto = "CADENA"
                elif not isinstance(objeto, str) or objeto not in validos:
                    objeto = "TESIS"
                if controlado(o.get("fuerza"), "fuerza", "moderada") == "fuerte":
                    alcance["x_fecha_incidente"] = dia_local(o.get("fecha_incidente"), self.ent.reloj.zona)
                objs.append({"objeto": objeto, **alcance, "tipo": o.get("tipo") or "objeción",
                             "fuerza": controlado(o.get("fuerza"), "fuerza", "moderada"), "argumento": o["argumento"],
                             "evidencia": [], "que_la_resolveria": o.get("que_la_resolveria") or "", "respuesta": None, "resuelta": False})
            for o in objs:
                o["obj_id"] = self.alm.nuevo_id("OBJ-B")
            director_o = [o for o in objs if o["objeto"] in ("TESIS", "CADENA") and o["fuerza"] in ("fuerte", "moderada")]
            cand_o = [o for o in objs if o["objeto"] in validos and o["fuerza"] in ("fuerte", "moderada")]
            referencias = self._referencias_contraste(st) if any(o["fuerza"] == "fuerte" for o in objs) else {}
            instruccion = ("Para cerrar una objeción fuerte devuelve evidencia_nueva como lista de identificadores de "
                           "referencias_disponibles, con fecha del hecho posterior al incidente. Explica qué demuestra la fuente.")
            if director_o:
                rd = self.inv.llamar("AG-B02", "CT-B-17", "respuestas_objeciones", {"pet_id": st["pet_id"], "objeciones": director_o,
                                     "referencias_disponibles": referencias},
                                     "Responde con evidencia cada objeción fuerte o moderada sobre la tesis o el eslabón indicado. " + instruccion, {"respuestas": "object"},
                                     self._ctx("AG-B02"), st["run_id"])
                self._aplicar_respuestas(director_o, rd.get("respuestas") or {}, referencias)
            if cand_o:
                ids_objetados = {o["objeto"] for o in cand_o}
                rs = self.inv.llamar("AG-B12", "CT-B-17", "respuestas_objeciones",
                                     {"pet_id": st["pet_id"], "objeciones": cand_o, "referencias_disponibles": referencias,
                                      "finalistas": [f for f in finalistas if f["cand_id"] in ids_objetados]},
                                     "Responde cada objeción fuerte o moderada sobre los candidatos. " + instruccion, {"respuestas_objeciones": "object"},
                                     self._ctx("AG-B12"), st["run_id"])
                self._aplicar_respuestas(cand_o, rs.get("respuestas_objeciones") or {}, referencias)
            for o in objs:
                if o["fuerza"] == "debil":
                    o.update(estado_contraste="aceptada", resuelta=True,
                             respuesta="Aceptada como matiz; sin efecto en el veredicto.")
            st["refutacion"] = {"realizada_por": "AG-B14", "veredicto_tesis": vt,
                                "veredicto_candidatos": {k: v for k, v in (r.get("veredicto_candidatos") or {}).items()
                                                         if k in validos and v in ("robusto", "fragil", "descartable")},
                                "objeciones": objs, "pre_mortem": (st["integracion"].get("pre_mortem") or "")}
        else:
            st["refutacion"] = {"realizada_por": "AUTORREFUTACION", "veredicto_tesis": "fragil", "veredicto_candidatos": {},
                                "objeciones": [], "pre_mortem": st["integracion"].get("pre_mortem") or "Autorrefutación del Director (no independiente)."}
            if st.get("refutacion_limitada"):
                st["limitaciones"].append("Refutación limitada a la autorrefutación por la versión ≤ 30 min (R23: los controles no se recortan)")

    def _referencias_contraste(self, st):
        """Referencias trazables de esta petición disponibles en la fecha del análisis."""
        entradas = [e for e in self.alm.estado("F2", as_of=self.ent.as_of).values() if e.get("pet_id") == st["pet_id"]]
        referencias = {}
        for e in entradas:
            fechas = fechas_de_fuente(e, self.ent.as_of, self.ent.reloj.zona)
            if fechas is None:
                continue
            if e["tipo_entrada"] == "DAT":
                referencias[e["id"]] = {"descripcion": e["descripcion"], **fechas}
            elif e["tipo_entrada"] == "EVD" and e.get("estado") == "VIGENTE":
                referencias[e["id"]] = {"descripcion": e["fuente"], **fechas}
        for e in entradas:
            if e["tipo_entrada"] == "CLM":
                if ("fechas" in e or any(k in e for k in CAMPOS_FECHA)) and not fechas_de_fuente(e, self.ent.as_of, self.ent.reloj.zona):
                    continue
                for ref in e.get("evd") or []:
                    if ref in referencias:
                        referencias[ref]["descripcion"] = e["afirmacion"]

        calculos = {(st.get("escenarios_motor") or {}).get("calc_id")}
        calculos.update(grupo.get("calc_puntuar") for grupo in st["seleccion"].values())
        for e in self.alm.leer("RC", self.ent.as_of, lambda e: e.get("id") in calculos and e.get("estado") == "SERVIDO"):
            fechas = fechas_de_fuente(e, self.ent.as_of, self.ent.reloj.zona)
            if fechas:
                referencias[e["id"]] = {"descripcion": e["metodo"], **fechas}
        return referencias

    @staticmethod
    def _aplicar_respuestas(objs: list[dict], resp: dict, referencias: dict) -> None:
        for o in objs:
            if o["fuerza"] == "fuerte":
                o["x_evidencia_respuesta"] = []
            rr = resp.get(o["obj_id"])
            if isinstance(rr, dict) and isinstance(rr.get("respuesta"), str) and rr["respuesta"].strip():
                o["respuesta"] = rr["respuesta"]
                o["resuelta"] = rr.get("resuelta") is True
                if o["fuerza"] == "fuerte":
                    citas = rr.get("evidencia_nueva")
                    if not isinstance(citas, list):
                        citas = []
                    validas = [ref for ref in citas if isinstance(ref, str) and ref in referencias]
                    o["x_evidencia_respuesta"] = list(dict.fromkeys(validas))
                    o["x_fechas_evidencia"] = {ref: {k: referencias[ref][k] for k in CAMPOS_FECHA} for ref in validas}
                    if o["resuelta"]:
                        motivo = None
                        incidente = o.get("x_fecha_incidente")
                        if not validas or len(validas) != len(citas):
                            motivo = "Falta una cita de la petición con fechas verificables y disponible al corte."
                        elif not incidente:
                            motivo = "Falta una fecha válida del incidente para contrastar la recuperación."
                        elif any(referencias[ref]["fecha_fenomeno"] <= incidente for ref in validas):
                            motivo = "El hecho citado no es de un día posterior al incidente."
                        if motivo:
                            o["resuelta"] = False
                            o["x_motivo_abierta"] = motivo
            o["estado_contraste"] = "resuelta" if o["resuelta"] else "incertidumbre_abierta"

    # =========================================================================================================
    # Puertas de viabilidad PV1–PV3 (7.10), informe de parada (7.11) y continuación forzada
    # =========================================================================================================
    def _registrar_puerta(self, st: Dict, ev: Dict) -> None:
        st.setdefault("pv", {})[ev["puerta"]] = ev
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "PUERTA_VIABILIDAD", "id": f"{st['pet_id']}::{ev['puerta']}", "pet_id": st["pet_id"],
                                           "run_id": st["run_id"], "puerta": ev["puerta"], "resultado": ev["resultado"],
                                           "motivos": ev.get("motivos") or [], "insumos": ev.get("insumos")})

    def _forzada(self, st: Dict, puerta: str) -> bool:
        return (st.get("continuacion_forzada") or {}).get("puerta") == puerta

    def _pv1(self, st: Dict) -> Optional[Dict]:
        v = st.get("viabilidad") or {}
        cap = 0.0
        hay_cap = False
        for t in st["tipos_aplicables"]:
            for f in st["universos"][t]["incluidos"]:
                try:
                    cap += float(f.get("capitalizacion_meur") or f.get("patrimonio_meur") or 0)
                    hay_cap = hay_cap or bool(f.get("capitalizacion_meur") or f.get("patrimonio_meur"))
                except (TypeError, ValueError):
                    pass
        insumos = {"tipos_con_invertible": sum(1 for t in st["tipos_aplicables"] if st["universos"][t]["tamano_invertible"] > 0),
                   "instrumentos_invertibles": sum(st["universos"][t]["tamano_invertible"] for t in st["tipos_aplicables"]),
                   "capitalizacion_agregada_meur": round(cap, 1) if hay_cap else None,
                   "alerta_integridad": bool(v.get("alerta_integridad")), "biblioteca_descartar_sin_cambio": bool(st.get("mkt_previa_descartar")),
                   "ya_descontado": bool(v.get("ya_descontado")), "sin_mecanismo": bool(v.get("sin_mecanismo"))}
        ev = ht03.evaluar_pv1(insumos)
        self._registrar_puerta(st, ev)
        if ev["resultado"] == "SUPERADA" or self._forzada(st, "PV1"):
            return None
        return self._parada(st, ev)

    def _pv2(self, st: Dict) -> Optional[Dict]:
        c2 = st.get("capa2") or {}
        ev = ht03.evaluar_pv2(c2.get("A"), c2.get("E"), c2.get("tesis_viva", True), c2.get("fuentes_para_cerrar_E", False))
        self._registrar_puerta(st, ev)
        st["gc2"] = ev["resultado"] == "SUPERADA"
        if ev["resultado"] == "SUPERADA":
            return None
        if self._forzada(st, "PV2"):
            return None
        if ev["proponer_consulta"] and not st.get("pv2_consulta"):
            # Solo falla E y hay fuentes que podrían cerrarla: el Director propone continuar (CT-B-28, CONFIRMACION_SUPUESTO)
            q = self._enviar_consulta(st, {"pregunta": f"La evidencia provisional es baja (E = {c2.get('E')}), pero hay fuentes identificadas que "
                                                       "podrían cerrarla. ¿Desea forzar la continuación tras PV2?",
                                           "tipo": "CONFIRMACION_SUPUESTO", "por_que_importa": "Evita parar un ámbito con A suficiente por falta de evidencia",
                                           "supuesto_si_no_hay_respuesta": "Se detiene en PV2 y se entrega el informe de parada",
                                           "efecto_si_supuesto_falso": "Se perdería un análisis que el Broker querría completar"},
                                     "AG-B02", 2, "BLOQUEANTE", puede_forzar=True)
            st["pv2_consulta"] = q["cns_id"]
            return self._pausa_consulta(st)
        return self._parada(st, ev)

    def _pv3(self, st: Dict) -> None:
        if st.get("fase_division") == 1:
            st.setdefault("pv", {})["PV3"] = {"puerta": "PV3", "resultado": "NO_EVALUADA", "motivos": [],
                                               "nota": "Fase 1 de un análisis dividido: la selección va en la fase 2"}
            return
        cands = [dict(c, puertas=ht03.puertas_candidato(c, t)) for t, s in (st.get("seleccion") or {}).items()
                 for c in (s.get("candidatos") or {}).values()]
        ev = ht03.evaluar_pv3(st.get("desglose") or [self._eslabon_unico(st)], cands)
        self._registrar_puerta(st, ev)
        if ev["resultado"] == "NO_SUPERADA" and not st.get("gc2") is False:
            st["limitaciones"].append("PV3 no superada: ningún eslabón atractivo o con cuello material tiene opciones invertibles; "
                                      "capa 4 reducida y entrega con VIGILAR o DESCARTAR sin selección completa (7.10)")

    def _parada(self, st: Dict, ev: Dict) -> Dict:
        """Informe de parada (7.11, 14.7, B.15): paquete de parada del Director, redacción, G3 reducida, autorización
        de salida, entrega CT-B-02 y registro (F1, F3 con DETENIDO_EN_PUERTA, F6 mínimo)."""
        from . import redaccion
        alm = self.alm
        puerta = ev["puerta"]
        capa = {"PV1": 1, "PV2": 2}[puerta]
        ckp = self._guardar_ckp(st, f"PARADA_{puerta}")
        r = self.inv.llamar("AG-B02", "CT-B-20", "paquete_parada",
                            {"pet_id": st["pet_id"], "puerta": puerta, "motivos": ev["motivos"], "ambito": st["plan"]["ambito"],
                             "puntuaciones_provisionales": {k: (st.get("capa2") or {}).get(k) for k in ("A", "E")},
                             "viabilidad": st.get("viabilidad"), "horizonte": st["horizonte"]},
                            "Compón el paquete de parada (7.11): por qué no merece seguir (con evidencia y etiqueta), qué lo cambiaría, "
                            "sugerencia DESCARTAR o PONER_EN_SEGUIMIENTO (con frecuencia y señales) y lo que ya se sabe.",
                            {"que_lo_cambiaria": "array", "sugerencia": "string"}, self._ctx("AG-B02"), st["run_id"])
        sug = r.get("sugerencia") if r.get("sugerencia") in ("DESCARTAR", "PONER_EN_SEGUIMIENTO") else \
            ("DESCARTAR" if any(m["clase"] == "ELIMINATORIO" for m in ev["motivos"]) else "PONER_EN_SEGUIMIENTO")
        clm_por = {d["dim"]: [e for n in d["notas"] for e in n.get("evidencias", [])] for d in st.get("dimensiones") or []}
        motivos = []
        for m in ev["motivos"]:
            dims = {"MATERIALIDAD": ["D2"], "YA_DESCONTADO": ["D9"], "A_PROVISIONAL": ["D9", "D8"], "E_PROVISIONAL": ["D2"],
                    "SIN_MECANISMO": ["D4"], "TESIS_REFUTADA": ["D4"]}.get(m["criterio"], [])
            motivos.append({**m, "evidencia": [e for d in dims for e in clm_por.get(d, [])][:2] or [st["dat"]["indicador"]],
                            "calculos": [c for c in [st["escenarios_motor"].get("calc_id")] if c],
                            "etiqueta": "[HECHO]" if m["clase"] == "ELIMINATORIO" and m["criterio"] == "SIN_INVERTIBILIDAD" else "[INTERPRETACIÓN]"})
        rest = self._estimar_resto(st)
        plazo = int((self.cfg.get("capas") or {}).get("plazo_forzar_continuacion_dias", 7))
        hasta = (dt.date.fromisoformat(self.ent.as_of) + dt.timedelta(days=plazo)).isoformat()
        segp = r.get("seguimiento_propuesto") if isinstance(r.get("seguimiento_propuesto"), dict) else {}
        rec_id = st["pet_id"].replace("PET-B-", "REC-B-")
        self._cerrar_consultas_no_bloqueantes(st)
        inf = {"pet_id": st["pet_id"], "run_id": st["run_id"], "rec_id": rec_id, "fecha": self.ent.as_of, "data_cutoff": self.ent.as_of,
               "ambito": {"nombre": st["plan"]["ambito"]["nombre"], "tipo_objeto": st["tipo_objeto"], "horizonte_principal": st["horizonte"]},
               "capa": capa, "puerta": puerta, "motivos": motivos,
               "por_que_no_merece_seguir": (
                   [f"{m['criterio']} ({m['clase'].lower()}): {m['detalle']}" for m in motivos] +
                   [f"Puntuaciones provisionales: A {(st.get('capa2') or {}).get('A')}, E {(st.get('capa2') or {}).get('E')}" if capa == 2 else
                    f"Universo preliminar invertible: {sum(st['universos'][t]['tamano_invertible'] for t in st['tipos_aplicables'])} instrumentos",
                    f"Seguir costaría ≈ {rest['minutos_p80']} min más (p80) sin cambiar la conclusión previsible",
                    f"Tesis básica: {(st.get('viabilidad') or {}).get('tesis_basica') or 'sin mecanismo plausible declarado'}"])[:6],
               "puntuaciones_provisionales": {"A": (st.get("capa2") or {}).get("A"), "E": (st.get("capa2") or {}).get("E")},
               "que_lo_cambiaria": [str(x) for x in r.get("que_lo_cambiaria") or []] or ["Un cambio material en los criterios que fallaron"],
               "sugerencia": sug,
               "seguimiento_propuesto": ({"frecuencia": segp.get("frecuencia") if segp.get("frecuencia") in ("DIARIA", "SEMANAL", "QUINCENAL", "MENSUAL", "TRIMESTRAL") else "MENSUAL",
                                          "senales_de_interes": [str(x) for x in segp.get("senales_de_interes") or []] or [f"Rentabilidad relativa de {st['indicador']['simbolo']}"],
                                          "disparadores": [str(x) for x in segp.get("disparadores") or []]} if sug == "PONER_EN_SEGUIMIENTO" else None),
               "veredicto_registrado": "DESCARTAR" if sug == "DESCARTAR" else "VIGILAR", "resultado_del_analisis": "DETENIDO_EN_PUERTA",
               "lo_que_ya_se_sabe": [str(x) for x in r.get("lo_que_ya_se_sabe") or []] or list(st.get("conclusiones_provisionales") or []),
               "supuestos_aplicados": [{"cns_id": q["cns_id"], "supuesto": q["supuesto"]} for q in st.get("consultas") or [] if q.get("estado") == "SUPUESTO_APLICADO"],
               "tiempo_consumo": {"minutos": round(st["consumido_min"], 1), "uc": round(sum((st.get("uc_tramos") or {}).values()), 1),
                                  "por_capa_min": dict(st.get("minutos_capa") or {})},
               "forzar_continuacion": {"posible_hasta": hasta, "estimacion_resto_p80_min": rest["minutos_p80"], "checkpoint_id": ckp},
               "aviso": "Informe de parada del Bloque B: no es una recomendación personal."}
        red = self.inv.llamar("AG-B17", "CT-B-20", "informe_parada", {"pet_id": st["pet_id"], "informe": inf},
                              "Redacta el resumen breve del informe de parada (≤ 2 páginas) sin añadir afirmaciones.", {"resumen": "string"},
                              self._ctx("AG-B17"), st["run_id"])
        md = redaccion.informe_parada_md(inf, red.get("resumen"))
        g3 = ht09.validar_informe_parada(inf, md, self.alm.estado("F1", tipo="CONSULTA_BROKER"))
        alm.escribir("HA", "AG-B21", {"tipo_entrada": "G3V", "id": alm.nuevo_id("G3V-B"), "pet_id": st["pet_id"], "run_id": st["run_id"],
                                      "pasada": "INFORME_PARADA", "dictamen": g3["dictamen"], "resumen": g3["resumen"], "motivo": g3["motivo"]})
        mu = float(((self.cfg.get("auditoria") or {}).get("muestreo") or {}).get("PARADA", 0.3))
        if random.Random(f"{st['pet_id']}|auditoria_parada").random() < mu and self.ent.modo != "backtest":
            a = self.inv.llamar("AG-B22", "CT-B-19", "auditoria", {"pet_id": st["pet_id"], "vuelta": 1, "nivel": st["nivel"], "informe_parada": inf},
                                "Audita el informe de parada (muestreo, 7.11).", {"hallazgos": "array", "recomendacion": "string"},
                                self._ctx("AG-B22"), st["run_id"])
            for h in [h for h in (a.get("hallazgos") or []) if isinstance(h, dict)]:
                alm.escribir("HA", "AG-B21", {"tipo_entrada": "AUD", "id": alm.nuevo_id("AUD-B"), "pet_id": st["pet_id"], "vuelta": 1,
                                              "severidad": controlado(h.get("severidad"), "severidad", "Operativa"), "descripcion": h.get("descripcion")})
        if g3["dictamen"] == "BLOQUEADO":
            self._estado_pet(st, "BLOQUEADO_AUDITORIA", motivo="G3 del informe de parada")
            return {"pet_id": st["pet_id"], "estado_peticion": "BLOQUEADO_AUDITORIA", "motivo": g3["motivo"]}
        auts = alm.nuevo_id("AUTS-B")
        alm.escribir("HA", "AG-B21", {"tipo_entrada": "AUTORIZACION_SALIDA", "id": auts, "pet_id": st["pet_id"], "dictamen_g3": g3["dictamen"],
                                      "tipo": "INFORME_PARADA"})
        rutas = redaccion.escribir_informe_parada(self.ent.salida, inf, md)
        entrega = {"pet_id": st["pet_id"], "run_ids": st["run_ids"], "rec_id": rec_id,
                   "entregables": {"informe_tecnico": None, "informe_visual": None, "paquete_json": None, "memorando": None, "anexo_datos": None,
                                   "mapa_eslabones": None, "informe_parada": rutas},
                   "resumen": {"veredicto": inf["veredicto_registrado"], "A": inf["puntuaciones_provisionales"]["A"], "E": inf["puntuaciones_provisionales"]["E"],
                               "C": None, "resultado_del_analisis": "DETENIDO_EN_PUERTA", "prioritarios_por_bloque_C": {}, "eslabones_destacados": [],
                               "siguiente_paso_sugerido": "DESCARTAR" if sug == "DESCARTAR" else "VIGILAR", "relevancia_decisional": "BAJA"},
                   "puertas_viabilidad": {g: (st["pv"].get(g) or {}).get("resultado", "NO_EVALUADA") for g in ("PV1", "PV2", "PV3")} | {"continuacion_forzada": None},
                   "supuestos_aplicados": inf["supuestos_aplicados"], "estado_g3": g3["dictamen"], "auditoria": {"realizada": False, "reservas": []},
                   "tiempo": {"estimado_p80_min": st["estimacion"]["minutos_p80"], "real_min": round(st["consumido_min"], 1),
                              "por_capa_min": dict(st.get("minutos_capa") or {}), "autorizaciones": st["autorizaciones"]},
                   "consumo_uc": inf["tiempo_consumo"]["uc"], "estado_peticion": "DETENIDA_EN_PUERTA", "autorizacion_salida": auts,
                   "forzar_continuacion": inf["forzar_continuacion"]}
        self.ent.salida.mkdir(parents=True, exist_ok=True)
        (self.ent.salida / f"{self.ent.as_of}_entrega_{st['pet_id']}.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=1), encoding="utf-8")
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "ENTREGA", "id": alm.nuevo_id("ENT-B"), "pet_id": st["pet_id"], "ct_b_02": entrega,
                                      "tiempos_por_tramo": st["tiempos"], "estimacion_fases": st.get("estimacion_fases"), "uc_por_tramo": st.get("uc_tramos")})
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "PARADA_PUERTA", "id": alm.nuevo_id("PAR-B"), "pet_id": st["pet_id"], "puerta": puerta,
                                      "motivos": [m["criterio"] for m in motivos], "sugerencia": sug, "checkpoint_id": ckp, "plazo_forzar": hasta})
        alm.escribir("F3", "AG-B02", {"tipo_entrada": "REC", "id": rec_id, "pet_id": st["pet_id"], "ambito": st["plan"]["ambito"], "tipo_objeto": st["tipo_objeto"],
                                      "veredicto": inf["veredicto_registrado"], "resultado_del_analisis": "DETENIDO_EN_PUERTA", "puerta": puerta,
                                      "A": inf["puntuaciones_provisionales"]["A"], "E": inf["puntuaciones_provisionales"]["E"], "C": None,
                                      "horizonte": st["horizonte"], "estado_vigilancia": "CERRADA", "indicador": st["indicador"], "referencia": st["referencia"],
                                      "sugerencia": sug})
        alm.escribir("F6", "AG-B02", {"tipo_entrada": "MKT", "id": st["pet_id"].replace("PET-B-", "MKT-B-"), "mkt_clave": st["clave"], "pet_id": st["pet_id"],
                                      "ambito": st["plan"]["ambito"], "veredicto": inf["veredicto_registrado"],
                                      "ultima_parada": {"puerta": puerta, "motivos": [m["criterio"] for m in motivos], "fecha": self.ent.as_of},
                                      "nota": "Parada en puerta: solo se actualiza lo verificado (5.2, regla 2)"})
        alm.escribir("F1", "AG-B01", {"tipo_entrada": "AVISO_EVALUADOR", "id": alm.nuevo_id("AVE-B"), "tipo": "PARADA_PUERTA",
                                      "contenido": {"pet_id": st["pet_id"], "rec_id": rec_id, "puerta": puerta, "indicador": st["indicador"],
                                                    "referencia": st["referencia"], "horizonte": st["horizonte"]}})
        self._estado_pet(st, "DETENIDA_EN_PUERTA", rec_id=rec_id, checkpoint_id=ckp, puerta=puerta, plazo_forzar=hasta)
        st["parada"] = {"puerta": puerta, "checkpoint_id": ckp}
        return entrega

    def forzar_continuacion(self, pet_id: str, puerta: str, motivo: Optional[str] = None, origen: str = "CT-B-04") -> Dict:
        """Orden del Broker de forzar la continuación tras una parada en PV1 o PV2 (7.10, regla 3; R33)."""
        p = self.alm.estado("F1", tipo="PETICION").get(pet_id)
        if not p:
            raise KeyError(f"No existe la petición {pet_id}")
        if puerta not in ("PV1", "PV2"):
            return {"pet_id": pet_id, "estado": "RECHAZADO", "motivo": "Solo PV1 y PV2 detienen el análisis; tras PV3 la entrega ya se produjo "
                                                                       "(una selección completa exige una petición nueva)"}
        if p.get("estado") != "DETENIDA_EN_PUERTA" or p.get("puerta") != puerta:
            return {"pet_id": pet_id, "estado": "RECHAZADO", "motivo": f"La petición no está detenida en {puerta} (estado {p.get('estado')})"}
        if p.get("plazo_forzar") and self.ent.as_of > p["plazo_forzar"]:
            self._estado_pet({"pet_id": pet_id}, "ENTREGADA", motivo="plazo para forzar la continuación vencido")
            return {"pet_id": pet_id, "estado": "RECHAZADO", "motivo": "Plazo vencido (Anexo A): pida una petición nueva que reutilice lo hecho"}
        st = ht08.cargar_punto_control(self.alm.dir_puntos_control / f"{p['checkpoint_id']}.json")
        st["continuacion_forzada"] = {"puerta": puerta, "motivo": motivo or "sin motivo declarado", "fecha": self.ent.as_of, "por": "BROKER", "origen": origen}
        st["limitaciones"].append(f"Continuación forzada por el Broker tras {puerta} no superada ({motivo or 'sin motivo declarado'}); "
                                  "no se rebaja ningún umbral ni se recorta ningún control (R23, R33)")
        if puerta == "PV2":
            st["gc2"] = False
            st["limitaciones"].append("GC2/PV2 no superada con continuación forzada: escenarios cualitativos y universo indicativo sin ranking completo (9.8)")
        st.pop("parada", None)
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "CONTINUACION_FORZADA", "id": self.alm.nuevo_id("CFZ-B"), "pet_id": pet_id,
                                           "puerta": puerta, "motivo": motivo, "origen": origen, "decidido_por": "BROKER"})
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AVISO_EVALUADOR", "id": self.alm.nuevo_id("AVE-B"), "tipo": "CONTINUACION_FORZADA",
                                           "contenido": {"pet_id": pet_id, "puerta": puerta}})
        rest = self._estimar_resto(st)
        if st["consumido_min"] + rest["minutos_p80"] > float(st.get("autorizado_min") or 30):
            est = {k: rest[k] for k in ("minutos_p50", "minutos_p80", "uc_p50", "uc_p80", "desglose_por_fase", "desglose_por_capa")}
            st["run_id"] = self.alm.nuevo_run(pet_id)
            st["run_ids"].append(st["run_id"])
            return self._detener(st, "PTA" if float(st.get("autorizado_min") or 30) > 30 else "PT30", "EN_EJECUCION", est) or self.ejecutar(st)
        return self.ejecutar(st)

    # =========================================================================================================
    # Consultas del bloque al Broker (CT-B-28, 7.12) y aportes del Broker
    # =========================================================================================================
    def _recibir_consultas(self, st: Dict, propuestas: Any, origen: str, capa: int) -> None:
        """Filtro del Director (7.12, punto 2): descarta lo resoluble, agrupa duplicados, decide el modo y respeta los
        límites del Anexo A; el Coordinador asigna CNS-B y envía."""
        if not isinstance(propuestas, list):
            return
        cb = self.cfg.get("consultas_broker") or {}
        nivel = st.get("nivel") or "N2"
        lim = int((cb.get("limite_por_peticion") or {}).get(nivel, 3))
        lim_b = int((cb.get("bloqueantes_max") or {}).get(nivel, 1))
        ya = {q["pregunta"].strip().lower() for q in st.get("consultas") or []}
        for q in propuestas:
            if not isinstance(q, dict) or not q.get("pregunta") or not q.get("supuesto_si_no_hay_respuesta"):
                continue
            if q["pregunta"].strip().lower() in ya or len(st.get("consultas") or []) >= lim:
                continue
            try:          # nunca credenciales, datos personales, cartera ni perfil del inversor (17.3; R10, R11)
                comprobar_sensibles(q)
                if RE_CARTERA.search(json.dumps(q, ensure_ascii=False)):
                    raise MensajeRechazado("cartera o perfil", "DATOS_PERSONALES")
            except MensajeRechazado:
                self.alm.incidencia("SEGURIDAD", f"Consulta propuesta por {origen} descartada por el filtro: pide datos protegidos", origen,
                                    severidad="Material")
                continue
            n_b = sum(1 for x in st.get("consultas") or [] if x["modo"] == "BLOQUEANTE")
            modo = "BLOQUEANTE" if q.get("bloqueante") and n_b < lim_b else "NO_BLOQUEANTE"
            self._enviar_consulta(st, q, origen, capa, modo)
            ya.add(q["pregunta"].strip().lower())

    def _enviar_consulta(self, st: Dict, q: Dict, origen: str, capa: int, modo: str, puede_forzar: bool = False) -> Dict:
        cb = self.cfg.get("consultas_broker") or {}
        cns = self.alm.nuevo_id("CNS-B")
        h = float(cb.get("plazo_bloqueante_h", 4) if modo == "BLOQUEANTE" else cb.get("plazo_no_bloqueante_h", 48))
        ahora = dt.datetime.fromisoformat(self.alm.reloj.ahora())
        tipo = q.get("tipo") if q.get("tipo") in TIPOS_CONSULTA else "OTRA"
        reg = {"cns_id": cns, "tipo": tipo, "modo": modo, "pregunta": str(q["pregunta"])[:500], "origen_agente": origen, "capa": capa,
               "por_que_importa": q.get("por_que_importa"), "supuesto": str(q.get("supuesto_si_no_hay_respuesta")),
               "efecto_si_supuesto_falso": q.get("efecto_si_supuesto_falso"), "plazo": (ahora + dt.timedelta(hours=h)).isoformat(timespec="seconds"),
               "estado": "PENDIENTE", "respuesta": None, "efecto": None, "puede_forzar": puede_forzar}
        st.setdefault("consultas", []).append(reg)
        mensaje = {"cns_id": cns, "sentido": "SALIENTE", "pet_id": st.get("pet_id"), "run_id": st.get("run_id"), "seg_id": st.get("seg_id"),
                   "tipo": tipo, "modo": modo, "preguntas": [{"n": 1, "pregunta": reg["pregunta"], "origen_agente": origen,
                                                              "por_que_importa": reg["por_que_importa"], "opciones": q.get("opciones") or [],
                                                              "supuesto_si_no_hay_respuesta": reg["supuesto"],
                                                              "efecto_si_supuesto_falso": reg["efecto_si_supuesto_falso"]}],
                   "plazo": reg["plazo"], "punto_control": {"checkpoint_id": None, "capa": capa}, "puede_forzar_continuacion": puede_forzar}
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "CONSULTA_BROKER", "id": cns, "pet_id": st.get("pet_id"), "seg_id": st.get("seg_id"),
                                           "sentido": "SALIENTE", "estado": "PENDIENTE", "modo": modo, "tipo": tipo, "supuesto": reg["supuesto"],
                                           "plazo": reg["plazo"], "ct_b_28": mensaje})
        d = self.ent.salida / "Consultas al Broker"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{self.ent.as_of}_consulta_{cns}.json").write_text(json.dumps(mensaje, ensure_ascii=False, indent=1), encoding="utf-8")
        return reg

    def _sincronizar_consultas(self, st: Dict) -> None:
        """Lleva al estado de la petición las respuestas y aportes registrados en F1 mientras estaba en pausa."""
        f1 = self.alm.estado("F1", tipo="CONSULTA_BROKER")
        for q in st.get("consultas") or []:
            e = f1.get(q["cns_id"]) or {}
            if e.get("estado") in ("RESPONDIDA", "SUPUESTO_APLICADO", "RESPUESTA_TARDIA") and q["estado"] == "PENDIENTE":
                q.update({"estado": e["estado"], "respuesta": e.get("respuesta"), "efecto": e.get("efecto")})
        vistos = {a.get("cns_id") for a in st.get("aportes") or []}
        for e in f1.values():
            if e.get("sentido") == "ENTRANTE" and e.get("pet_id") == st.get("pet_id") and e["id"] not in vistos:
                st.setdefault("aportes", []).append({"cns_id": e["id"], "naturaleza": e.get("naturaleza"), "contenido": e.get("contenido")})
                vinc = e.get("naturaleza") in ("ALCANCE", "PREFERENCIA")
                st["limitaciones"].append(f"Aporte del Broker {e['id']} ({e.get('naturaleza')}): " + (
                    "vincula al análisis" if vinc else "tratado como pista y re-verificado (R31)"))

    def _bloqueantes_pendientes(self, st: Dict) -> List[Dict]:
        return [q for q in st.get("consultas") or [] if q["modo"] == "BLOQUEANTE" and q["estado"] == "PENDIENTE"]

    def _pausa_consulta(self, st: Dict) -> Dict:
        ckp = self._guardar_ckp(st, "PAUSA_CONSULTA")
        pend = self._bloqueantes_pendientes(st)
        for q in pend:
            self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "CONSULTA_BROKER", "id": q["cns_id"], "checkpoint_reanudacion": ckp})
        self._estado_pet(st, "EN_PAUSA_CONSULTA", checkpoint_id=ckp, cns_ids=[q["cns_id"] for q in pend])
        return {"pet_id": st["pet_id"], "estado": "EN_PAUSA", "estado_peticion": "EN_PAUSA_CONSULTA", "checkpoint_id": ckp,
                "cns_ids": [q["cns_id"] for q in pend], "consultas": [{k: q[k] for k in ("cns_id", "tipo", "pregunta", "supuesto", "plazo")} for q in pend],
                "nota": "Consulta BLOQUEANTE al Broker (CT-B-28): el reloj de la puerta de tiempo está detenido durante la espera (7.12)"}

    def _cerrar_consultas_no_bloqueantes(self, st: Dict) -> None:
        """Al inicio de F8 (o al vencer las 48 h) las NO_BLOQUEANTES sin respuesta pasan a SUPUESTO_APLICADO (7.12, punto 4)."""
        self._sincronizar_consultas(st)
        for q in st.get("consultas") or []:
            if q["estado"] == "PENDIENTE" and q["modo"] == "NO_BLOQUEANTE":
                self._cerrar_consulta(q, "SUPUESTO_APLICADO", None, "SIN_CAMBIO", st.get("pet_id"))
                st["limitaciones"].append(f"Supuesto aplicado por falta de respuesta ({q['cns_id']}): {q['supuesto']}")

    def _cerrar_consulta(self, q: Dict, resolucion: str, respuesta: Optional[str], efecto: str, pet_id: Optional[str]) -> None:
        q.update({"estado": resolucion, "respuesta": respuesta, "efecto": efecto})
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "CONSULTA_BROKER", "id": q["cns_id"], "estado": resolucion, "respuesta": respuesta,
                                           "efecto": efecto, "resolucion": resolucion})
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AVISO_EVALUADOR", "id": self.alm.nuevo_id("AVE-B"), "tipo": "CONSULTA_CERRADA",
                                           "contenido": {"cns_id": q["cns_id"], "tipo": q["tipo"], "resolucion": resolucion, "efecto": efecto}})
        self._consulta_recurrente(q, pet_id)

    def _consulta_recurrente(self, q: Dict, pet_id: Optional[str]) -> None:
        """Misma clase de duda (tipo y tema) en 3 peticiones distintas en 8 semanas → LEC-B de producto (12.7)."""
        cb = (self.cfg.get("consultas_broker") or {}).get("recurrente") or {}
        desde = (dt.date.fromisoformat(self.ent.as_of) - dt.timedelta(weeks=int(cb.get("semanas", 8)))).isoformat()
        tema = re.sub(r"[^a-záéíóúñ ]", "", q["pregunta"].lower())[:40]
        pets = {e.get("pet_id") for e in self.alm.leer("F1") if e.get("tipo_entrada") == "CONSULTA_BROKER" and e.get("sentido") == "SALIENTE"
                and e["_fecha"] >= desde and e.get("tipo") == q["tipo"]
                and re.sub(r"[^a-záéíóúñ ]", "", str((e.get("ct_b_28") or {}).get("preguntas", [{}])[0].get("pregunta", "")).lower())[:40] == tema}
        if len(pets - {None}) >= int(cb.get("peticiones", 3)):
            ya = [e for e in self.alm.leer("F5") if e.get("tipo_entrada") == "LECCION" and e.get("tema_consulta") == tema]
            if not ya:
                self.alm.escribir("F5", "AG-B23", {"tipo_entrada": "LECCION", "id": self.alm.nuevo_id("LEC-B"), "ambito": "producto",
                                                   "agentes": ["AG-B01"], "tema_consulta": tema,
                                                   "observacion": f"Consulta recurrente ({q['tipo']}) en {len(pets)} peticiones: «{q['pregunta'][:80]}»",
                                                   "recomendacion": "Preguntarlo o normalizarlo al admitir la petición", "fuerza": "recurrente"})
                self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "AVISO_EVALUADOR", "id": self.alm.nuevo_id("AVE-B"), "tipo": "CONSULTA_RECURRENTE",
                                                   "contenido": {"tipo": q["tipo"], "tema": tema, "peticiones": sorted(p for p in pets if p)}})

    def responder_consulta(self, cns_id: str, respuesta: str, forzar_continuacion: bool = False, motivo: Optional[str] = None) -> Dict:
        """Respuesta del Broker a una CT-B-28 saliente. Reanuda la petición si estaba en pausa por esa consulta."""
        e = self.alm.estado("F1", tipo="CONSULTA_BROKER").get(cns_id)
        if not e or e.get("sentido") != "SALIENTE":
            raise KeyError(f"No existe la consulta saliente {cns_id}")
        comprobar_sensibles({"respuesta": respuesta})
        respuesta = sanear(respuesta)
        sup = str(e.get("supuesto") or "").lower()
        r_l = respuesta.strip().lower()
        efecto = "SIN_CAMBIO" if (r_l.startswith(("sí", "si", "confirm", "de acuerdo")) or (sup and sup[:30] in r_l)) else "SUPUESTO_CAMBIADO"
        q = {"cns_id": cns_id, "tipo": e.get("tipo"), "modo": e.get("modo"), "pregunta": (e.get("ct_b_28") or {}).get("preguntas", [{}])[0].get("pregunta", ""),
             "supuesto": e.get("supuesto")}
        if e.get("estado") != "PENDIENTE":
            self._cerrar_consulta(q, "RESPUESTA_TARDIA", respuesta, efecto, e.get("pet_id"))
            return {"cns_id": cns_id, "estado": "RESPUESTA_TARDIA", "efecto": efecto,
                    "nota": "Respuesta tardía registrada; si cambia una conclusión, el Coordinador lo comunica como aporte y puede proponer una petición"}
        self._cerrar_consulta(q, "RESPONDIDA", respuesta, efecto, e.get("pet_id"))
        pet = self.alm.estado("F1", tipo="PETICION").get(e.get("pet_id")) or {}
        if pet.get("estado") == "EN_PAUSA_CONSULTA" and cns_id in (pet.get("cns_ids") or []):
            st = ht08.cargar_punto_control(self.alm.dir_puntos_control / f"{pet['checkpoint_id']}.json")
            self._sincronizar_consultas(st)
            if st.get("pv2_consulta") == cns_id:
                if forzar_continuacion:
                    st["continuacion_forzada"] = {"puerta": "PV2", "motivo": motivo or respuesta[:200], "fecha": self.ent.as_of, "por": "BROKER", "origen": "CT-B-28"}
                    st["limitaciones"].append(f"Continuación forzada por el Broker tras PV2 no superada (respuesta a {cns_id})")
                    self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "CONTINUACION_FORZADA", "id": self.alm.nuevo_id("CFZ-B"), "pet_id": st["pet_id"],
                                                       "puerta": "PV2", "motivo": motivo, "origen": "CT-B-28", "decidido_por": "BROKER"})
                else:
                    st["run_id"] = self.alm.nuevo_run(st["pet_id"])
                    st["run_ids"].append(st["run_id"])
                    return self._parada(st, st["pv"]["PV2"])
            if self._bloqueantes_pendientes(st):
                return self._pausa_consulta(st)
            return self.ejecutar(st)
        return {"cns_id": cns_id, "estado": "RESPONDIDA", "efecto": efecto}

    def revisar_consultas(self) -> List[Dict]:
        """Plazos vencidos (7.12, punto 4): las BLOQUEANTES aplican el supuesto y reanudan la petición."""
        ahora = dt.datetime.fromisoformat(self.alm.reloj.ahora())
        out = []
        for cns, e in self.alm.estado("F1", tipo="CONSULTA_BROKER").items():
            if e.get("sentido") != "SALIENTE" or e.get("estado") != "PENDIENTE" or not e.get("plazo"):
                continue
            if dt.datetime.fromisoformat(e["plazo"]) > ahora:
                continue
            q = {"cns_id": cns, "tipo": e.get("tipo"), "modo": e.get("modo"), "pregunta": (e.get("ct_b_28") or {}).get("preguntas", [{}])[0].get("pregunta", ""),
                 "supuesto": e.get("supuesto")}
            self._cerrar_consulta(q, "SUPUESTO_APLICADO", None, "SIN_CAMBIO", e.get("pet_id"))
            res = {"cns_id": cns, "estado": "SUPUESTO_APLICADO"}
            pet = self.alm.estado("F1", tipo="PETICION").get(e.get("pet_id")) or {}
            if pet.get("estado") == "EN_PAUSA_CONSULTA" and cns in (pet.get("cns_ids") or []):
                st = ht08.cargar_punto_control(self.alm.dir_puntos_control / f"{pet['checkpoint_id']}.json")
                self._sincronizar_consultas(st)
                st["limitaciones"].append(f"Supuesto aplicado por falta de respuesta ({cns}): {e.get('supuesto')}")
                if st.get("pv2_consulta") == cns:
                    st["run_id"] = self.alm.nuevo_run(st["pet_id"])
                    st["run_ids"].append(st["run_id"])
                    res["reanudacion"] = self._parada(st, st["pv"]["PV2"])
                elif not self._bloqueantes_pendientes(st):
                    res["reanudacion"] = self.ejecutar(st)
            out.append(res)
        return out

    def aporte_broker(self, datos: Dict) -> Dict:
        """Aporte entrante del Broker (CT-B-28 ENTRANTE o CT-B-03): se registra y se encamina al Director (7.12, punto 5)."""
        comprobar_sensibles(datos)
        datos = sanear(datos)
        nat = datos.get("naturaleza") if datos.get("naturaleza") in ("ALCANCE", "PREFERENCIA", "DATO", "DOCUMENTO") else "DATO"
        cns = self.alm.nuevo_id("CNS-B")
        self.alm.escribir("F1", "AG-B01", {"tipo_entrada": "CONSULTA_BROKER", "id": cns, "sentido": "ENTRANTE", "tipo": "APORTE_BROKER",
                                           "pet_id": datos.get("pet_id"), "seg_id": datos.get("seg_id"), "naturaleza": nat,
                                           "contenido": str(datos.get("contenido") or "")[:2000], "adjuntos": datos.get("adjuntos") or [],
                                           "estado": "REGISTRADO"})
        return {"cns_id": cns, "sentido": "ENTRANTE", "naturaleza": nat, "estado": "REGISTRADO",
                "efecto": "vincula (alcance o preferencia)" if nat in ("ALCANCE", "PREFERENCIA") else "pista que se re-verifica (R31) y entra en F2 por el Curador",
                "destino": datos.get("pet_id") or datos.get("seg_id")}

    # =========================================================================================================
    # F7 · Veredicto y síntesis
    # =========================================================================================================
    def _f7(self, st: Dict) -> None:
        sintesis.veredicto_y_paquete(self, st)

    # =========================================================================================================
    # F8 · Validación G3 y auditoría previa a la salida
    # =========================================================================================================
    def _f8(self, st: Dict) -> None:
        sintesis.validar_y_auditar(self, st)

    # =========================================================================================================
    # F9 · Redacción y F10 · Entrega
    # =========================================================================================================
    def _f9(self, st: Dict) -> None:
        from . import redaccion
        redaccion.redactar(self, st)

    def _f10(self, st: Dict) -> None:
        from . import redaccion
        redaccion.entregar(self, st)


def _semilla_pet(st: Dict, *claves) -> int:
    import hashlib
    return int.from_bytes(hashlib.sha256("|".join((st["pet_id"],) + tuple(map(str, claves))).encode()).digest()[:4], "little")
