"""Comunicación fluida con el Broker (Documento 0 Forex V1.1, R26, R8, 7.9 y 7.10).

- `Consultas` (CT-23): consultas del bloque al Broker (SALIENTE) y aportaciones espontáneas del Broker (ENTRANTE). Tipos
  ACLARACION_ALCANCE, DATO_O_DOCUMENTO, PREFERENCIA_O_CRITERIO, CONFIRMACION_SUPUESTO y OTRA; modo BLOQUEANTE (pausa la parte
  afectada —un segmento— en su punto de control, sin consumir presupuesto) o NO_BLOQUEANTE (sigue con un supuesto declarado).
  Si vence el plazo sin respuesta, se sigue con el supuesto declarado, que pasa a `supuestos_declarados` de los entregables.
  Registro en F5 (CNS-FX-); las consultas recurrentes se avisan al Evaluador (CT-22 CONSULTA_RECURRENTE).
- `Credenciales` (CT-25): el Coordinador solicita al Broker la credencial que falta; el Broker la deposita en la bóveda de
  HT-01 y responde solo con estado y alias. Registro en F5 (CRD-FX-, sin valores); una credencial DENEGADA se anota en F10
  como limitación de servicio y no se vuelve a pedir salvo cambio de circunstancias.
"""
from __future__ import annotations

import datetime as dt
from typing import Dict, List, Optional, Tuple

import pandas as pd

from .contratos import DatosSensibles
from .herramientas.ht05_planificador import vencimiento_consulta

TIPOS_CONSULTA = ("ACLARACION_ALCANCE", "DATO_O_DOCUMENTO", "PREFERENCIA_O_CRITERIO", "CONFIRMACION_SUPUESTO", "OTRA")
MODOS = ("BLOQUEANTE", "NO_BLOQUEANTE")
ESTADOS_RESPUESTA_CRD = ("PROVISTA", "DENEGADA", "APLAZADA")


def _ahora(bloque) -> dt.datetime:
    return dt.datetime.fromisoformat(bloque.reloj.ahora())


class Consultas:
    def __init__(self, bloque) -> None:
        self.b = bloque
        cfg = (bloque.cfg.get("consultas_broker") or {})
        self.max_por_run = int(cfg.get("max_por_run", 3))
        self.horas_bloq = int(cfg.get("horas_bloqueante", 4))
        self.horas_no_bloq = int(cfg.get("horas_no_bloqueante", 24))
        self.recurrente_n = int(cfg.get("recurrente_n", 3))
        self.recurrente_semanas = int(cfg.get("recurrente_semanas", 8))

    # --------------------------------------------------------------------------------
    def todas(self, as_of=None) -> Dict[str, Dict]:
        return {k: v for k, v in self.b.almacen.estado("F5", as_of, clave="cns_id").items() if v.get("tipo_entrada", "").startswith("CNS")}

    def crear(self, preguntas: List[Dict], tipo: str, modo: str, as_of=None, run_id: Optional[str] = None,
              seg_id: Optional[str] = None, segmento: Optional[str] = None, punto_control: Optional[str] = None,
              motivo: Optional[str] = None, tipo_run: str = "AD_HOC") -> Dict:
        """Envía una consulta CT-23 (ya filtrada y agrupada por el Analizador). Cada pregunta lleva su supuesto declarado."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        if tipo not in TIPOS_CONSULTA:
            raise ValueError(f"Tipo de consulta no válido {tipo!r} ({', '.join(TIPOS_CONSULTA)})")
        if modo not in MODOS:
            raise ValueError(f"Modo no válido {modo!r} ({', '.join(MODOS)})")
        if not preguntas:
            raise ValueError("Consulta sin preguntas")
        for i, p in enumerate(preguntas):
            if not str(p.get("texto") or "").strip():
                raise ValueError(f"Pregunta {i} sin texto")
            if not str(p.get("supuesto_declarado") or "").strip():
                raise ValueError(f"Pregunta {i} sin supuesto declarado (R26: el análisis debe poder seguir sin respuesta)")
            p.setdefault("efecto_si_falso", "Habría que revisar las conclusiones que dependen de este supuesto")
            p.setdefault("origen", "AG-02")
        # Agrupación: máximo de mensajes CT-23 por RUN (Anexo A); el excedente se agrupa en el último pendiente
        if run_id:
            del_run = [c for c in self.todas(as_of).values() if c.get("run_id") == run_id and c.get("sentido") == "SALIENTE"]
            if len(del_run) >= self.max_por_run:
                pend = [c for c in del_run if c.get("estado") == "PENDIENTE"]
                if pend:
                    c = sorted(pend, key=lambda x: x["cns_id"])[-1]
                    nuevas = list(c.get("preguntas") or []) + preguntas
                    self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS_AGRUPACION", "cns_id": c["cns_id"], "preguntas": nuevas,
                                                            "nota": f"Agrupada por el máximo de {self.max_por_run} CT-23 por RUN"})
                    return {**c, "preguntas": nuevas, "agrupada": True}
                raise ValueError(f"{run_id} ya ha enviado {self.max_por_run} consultas CT-23 (máximo del Anexo A)")
        cns_id = self.b.almacen.nuevo_id("CNS")
        emitida = _ahora(self.b)
        plazo = vencimiento_consulta(emitida, modo, tipo_run, None, self.horas_bloq, self.horas_no_bloq)
        cuerpo = {"cns_id": cns_id, "sentido": "SALIENTE", "run_id_ref": run_id, "seg_id": seg_id, "tipo": tipo, "modo": modo,
                  "preguntas": preguntas, "plazo_respuesta": plazo.isoformat(timespec="minutes"), "punto_control": punto_control}
        msg = self.b.mensajeria.crear("CT-23", "AG-01", "BROKER", cuerpo)
        e = {"tipo_entrada": "CNS", "cns_id": cns_id, "msg_id": msg["msg_id"], "sentido": "SALIENTE", "run_id": run_id, "seg_id": seg_id,
             "segmento": segmento, "tipo": tipo, "modo": modo, "motivo": motivo or tipo, "preguntas": preguntas,
             "plazo_respuesta": cuerpo["plazo_respuesta"], "punto_control": punto_control, "estado": "PENDIENTE",
             "fecha": str(as_of.date())}
        self.b.almacen.escribir("F5", "AG-01", e)
        self._recurrentes(as_of, tipo, e["motivo"])
        return {**e, "mensaje": msg}

    def entrante(self, contenido: str, as_of=None, run_id: Optional[str] = None, opp_id: Optional[str] = None,
                 seg_id: Optional[str] = None) -> Dict:
        """Aportación espontánea del Broker (CT-23 entrante): se registra y se trata como evidencia con fuente BROKER (dato)."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        cns_id = self.b.almacen.nuevo_id("CNS")
        try:
            msg = self.b.mensajeria.crear("CT-23", "BROKER", "AG-01", {"cns_id": cns_id, "sentido": "ENTRANTE", "tipo": "OTRA",
                                                                       "modo": "NO_BLOQUEANTE", "plazo_respuesta": None,
                                                                       "contenido": contenido, "run_id_ref": run_id,
                                                                       "opp_id": opp_id, "seg_id": seg_id})
        except DatosSensibles:
            return {"cns_id": cns_id, "estado": "RECHAZADO", "motivo": "Mensaje con credenciales o datos personales (R8): rechazado íntegro"}
        from .contratos import sanear_contenido_externo
        limpio, hallazgos = sanear_contenido_externo(contenido, f"CT-23:{cns_id}")
        if hallazgos:
            self.b._registrar_r9(hallazgos, run_id)
        e = {"tipo_entrada": "CNS", "cns_id": cns_id, "msg_id": msg["msg_id"], "sentido": "ENTRANTE", "run_id": run_id, "opp_id": opp_id,
             "seg_id": seg_id, "tipo": "OTRA", "contenido": limpio, "fuente_evidencia": "BROKER", "estado": "RECIBIDA",
             "fecha": str(as_of.date())}
        self.b.almacen.escribir("F5", "AG-01", e)
        return e

    def responder(self, cns_id: str, respuestas: List[Dict], as_of=None, parcial: bool = False) -> Dict:
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        c = self.todas(as_of).get(cns_id)
        if not c or c.get("sentido") != "SALIENTE":
            raise KeyError(f"Consulta {cns_id} no encontrada")
        if c.get("estado") not in ("PENDIENTE", "VENCIDA"):
            return {**c, "aviso": "La consulta ya estaba respondida"}
        try:
            self.b.mensajeria.crear("CT-23", "BROKER", "AG-01", {"cns_id": cns_id, "estado_consulta": "PARCIAL" if parcial else "RESPONDIDA",
                                                                 "respuestas": respuestas}, tipo_mensaje="RETORNO", estado="COMPLETO")
        except DatosSensibles:
            return {"cns_id": cns_id, "estado": "RECHAZADO", "motivo": "Respuesta con credenciales o datos personales (R8): rechazada íntegra"}
        tardia = c.get("estado") == "VENCIDA"
        entregado = bool(c.get("run_id")) and any(r.get("tipo_entrada") == "RUN" and r.get("run_id") == c["run_id"]
                                                  for r in self.b.almacen.leer("F5", as_of))
        e = {"tipo_entrada": "CNS_RESPUESTA", "cns_id": cns_id, "estado": "PARCIAL" if parcial else "RESPONDIDA", "respuestas": respuestas,
             "fecha_respuesta": str(as_of.date()), "tardia": tardia,
             "revision_C2_sugerida": bool(tardia and entregado),
             "nota": ("Respuesta tardía a un supuesto ya entregado: se trata como petición de revisión (C2) y se comunica al Broker"
                      if tardia and entregado else None)}
        self.b.almacen.escribir("F5", "AG-01", e)
        return {**c, **e}

    def vencer(self, as_of=None) -> List[str]:
        """Marca VENCIDA toda consulta pendiente cuyo plazo ha pasado: el análisis sigue con el supuesto declarado."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        ahora = _ahora(self.b)
        out = []
        for c in self.todas(as_of).values():
            if c.get("estado") != "PENDIENTE" or not c.get("plazo_respuesta"):
                continue
            plazo = dt.datetime.fromisoformat(c["plazo_respuesta"])
            if plazo.tzinfo is None and ahora.tzinfo is not None:
                plazo = plazo.replace(tzinfo=ahora.tzinfo)
            if plazo <= ahora:
                self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS_VENCIDA", "cns_id": c["cns_id"], "estado": "VENCIDA",
                                                        "supuestos_aplicados": [{"indice": i, "supuesto": p["supuesto_declarado"]}
                                                                                for i, p in enumerate(c.get("preguntas") or [])],
                                                        "fecha": str(as_of.date())})
                out.append(c["cns_id"])
        return out

    # --------------------------------------------------------------------------------
    def segmentos_pausados(self, as_of=None) -> Dict[str, str]:
        """Segmentos con una consulta BLOQUEANTE pendiente y en plazo: se pausan en su punto de control (7.9.4)."""
        self.vencer(as_of)
        return {c["segmento"]: c["cns_id"] for c in self.todas(as_of).values()
                if c.get("modo") == "BLOQUEANTE" and c.get("estado") == "PENDIENTE" and c.get("segmento")}

    def supuestos_de_run(self, run_id: str, as_of=None, seg_id: Optional[str] = None) -> Tuple[List[Dict], List[str]]:
        """Supuestos declarados que rigen un RUN: los de sus consultas sin respuesta y los de las consultas sin RUN (de admisión o
        del Broker para el siguiente ciclo) pendientes o vencidas en la fecha del RUN."""
        sup, sin_resp = [], []
        for c in sorted(self.todas(as_of).values(), key=lambda x: x["cns_id"]):
            if c.get("sentido") != "SALIENTE" or c.get("estado") not in ("PENDIENTE", "VENCIDA") or c.get("seg_id") != seg_id:
                continue
            if c.get("run_id") not in (None, run_id):
                continue
            sin_resp.append(c["cns_id"])
            for p in c.get("preguntas") or []:
                sup.append({"supuesto": p["supuesto_declarado"], "cns_id": c["cns_id"], "efecto_si_falso": p.get("efecto_si_falso")})
        return sup, sin_resp

    def _recurrentes(self, as_of, tipo: str, motivo: str) -> None:
        desde = pd.Timestamp(as_of) - pd.Timedelta(weeks=self.recurrente_semanas)
        mismas = [c for c in self.todas(as_of).values() if c.get("sentido") == "SALIENTE" and c.get("tipo") == tipo
                  and c.get("motivo") == motivo and pd.Timestamp(c.get("fecha", str(as_of.date()))) >= desde]
        if len(mismas) == self.recurrente_n:
            ids = sorted(c["cns_id"] for c in mismas)
            self.b.mensajeria.crear("CT-22", "AG-01", "AG-20", {"tipo_aviso": "CONSULTA_RECURRENTE", "cns_ids": ids,
                                                                 "tema": f"{tipo}/{motivo}"}, query_id=ids[-1])
            try:
                self.b.evaluador.leccion_producto(pd.Timestamp(as_of), f"CONSULTA_RECURRENTE {tipo}/{motivo}: normalizar la petición", ids)
            except Exception:   # noqa: BLE001 — el aprendizaje nunca bloquea (C5)
                pass


class Credenciales:
    def __init__(self, bloque) -> None:
        self.b = bloque
        cfg = (bloque.cfg.get("credenciales") or {})
        self.dias_recordatorio = int(cfg.get("dias_recordatorio", 7))
        self.max_recordatorios = int(cfg.get("max_recordatorios", 3))

    def todas(self, as_of=None) -> Dict[str, Dict]:
        return {k: v for k, v in self.b.almacen.estado("F5", as_of, clave="crd_id").items() if v.get("tipo_entrada", "").startswith("CRD")}

    def estado_servicio(self, servicio: str) -> Dict:
        return self.b.boveda.estado(servicio, self.b.reloj.fecha)

    def solicitar(self, servicio: str, uso_previsto: str, solicitante: str, impacto_si_falta: str, urgencia: str = "NORMAL",
                  as_of=None, forzar: bool = False) -> Dict:
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        est = self.estado_servicio(servicio)
        if est["estado"] == "PROVISTA":
            return {"servicio": servicio, "estado": "PROVISTA", "credencial_ref": est["credencial_ref"], "crd_id": None,
                    "nota": "La credencial ya está en la bóveda de HT-01: no se molesta al Broker"}
        previas = [c for c in self.todas(as_of).values() if c.get("servicio") == servicio]
        abierta = next((c for c in previas if c.get("estado") in ("SOLICITADA", "APLAZADA")), None)
        if abierta:
            return {**abierta, "nota": "Solicitud ya en curso (deduplicada)"}
        denegada = next((c for c in previas if c.get("estado") == "DENEGADA"), None)
        if denegada and not forzar:
            return {**denegada, "nota": "Denegada antes: no se vuelve a pedir salvo cambio de circunstancias (forzar)"}
        crd_id = self.b.almacen.nuevo_id("CRD")
        cuerpo = {"crd_id": crd_id, "servicio": servicio, "herramienta": "HT-01", "uso_previsto": uso_previsto, "solicitante": solicitante,
                  "impacto_si_falta": impacto_si_falta, "urgencia": urgencia}
        if solicitante in ("AG-16", "AG-02"):
            self.b.mensajeria.crear("CT-25", solicitante, "AG-01", cuerpo)      # origen: Buscador (directo) o Analizador
        msg = self.b.mensajeria.crear("CT-25", "AG-01", "BROKER", cuerpo)
        e = {"tipo_entrada": "CRD", **cuerpo, "msg_id": msg["msg_id"], "estado": "SOLICITADA", "estado_boveda": est["estado"],
             "fecha_solicitud": str(as_of.date()), "recordatorios": 0, "servicio_degradado": True}
        self.b.almacen.escribir("F5", "AG-01", e)
        return e

    def responder(self, crd_id: str, estado: str, as_of=None, valor: Optional[str] = None, caducidad: Optional[str] = None,
                  valor_en_mensaje: bool = False) -> Dict:
        """Respuesta del Broker. Con PROVISTA, el valor se deposita en la bóveda (procedimiento seguro); el mensaje CT-25 solo
        lleva estado y alias. `valor_en_mensaje=True` simula el error de enviar la clave en el mensaje: se rechaza (6.2.5)."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        c = self.todas(as_of).get(crd_id)
        if not c:
            raise KeyError(f"Solicitud {crd_id} no encontrada")
        if estado not in ESTADOS_RESPUESTA_CRD:
            raise ValueError(f"Estado no válido {estado!r} ({', '.join(ESTADOS_RESPUESTA_CRD)})")
        if valor_en_mensaje:
            try:
                self.b.mensajeria.crear("CT-25", "BROKER", "AG-01", {"crd_id": crd_id, "estado_credencial": estado, "clave_api": valor or ""},
                                        tipo_mensaje="RETORNO", estado="COMPLETO")
            except DatosSensibles:
                self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CRD_INCIDENCIA", "crd_id": crd_id,
                                                        "incidencia": "Clave recibida en un mensaje: rechazado íntegro sin copiar el valor; "
                                                                      "se pide depositarla en la bóveda de HT-01 y renovarla (expuesta)",
                                                        "fecha": str(as_of.date())})
                return {"crd_id": crd_id, "estado": "RECHAZADO",
                        "motivo": "La clave no puede viajar en un mensaje (R8, 6.2.5): deposítela en la bóveda de HT-01 y renuévela"}
        ref = None
        if estado == "PROVISTA":
            if valor:
                ref = self.b.boveda.depositar(c["servicio"], valor, caducidad)
            est = self.estado_servicio(c["servicio"])
            if est["estado"] != "PROVISTA":
                raise ValueError("PROVISTA sin depósito en la bóveda de HT-01")
            ref = est["credencial_ref"]
        self.b.mensajeria.crear("CT-25", "BROKER", "AG-01", {"crd_id": crd_id, "estado_credencial": estado, "credencial_ref": ref,
                                                             "caducidad": caducidad}, tipo_mensaje="RETORNO", estado="COMPLETO")
        e = {"tipo_entrada": "CRD_RESPUESTA", "crd_id": crd_id, "estado": estado, "credencial_ref": ref, "caducidad": caducidad,
             "fecha_respuesta": str(as_of.date()), "servicio_degradado": estado != "PROVISTA"}
        self.b.almacen.escribir("F5", "AG-01", e)
        if estado == "DENEGADA":
            self.b.almacen.escribir("F10", "AG-01", {"tipo_entrada": "LIMITACION_SERVICIO", "param_id": f"LIM-{c['servicio']}",
                                                     "nombre": f"Servicio degradado: {c['servicio']}",
                                                     "valor_vigente": "DEGRADADO (credencial denegada; fuentes alternativas declaradas)",
                                                     "crd_id": crd_id, "regimen": "SERVICIO"})
        return {**c, **e}

    def recordatorios(self, as_of=None) -> List[str]:
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        out = []
        for c in self.todas(as_of).values():
            if c.get("estado") not in ("SOLICITADA", "APLAZADA") or int(c.get("recordatorios", 0)) >= self.max_recordatorios:
                continue
            dias = (pd.Timestamp(as_of) - pd.Timestamp(c["fecha_solicitud"])).days
            debidos = min(dias // self.dias_recordatorio, self.max_recordatorios)
            if debidos > int(c.get("recordatorios", 0)):
                self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CRD_RECORDATORIO", "crd_id": c["crd_id"], "recordatorios": debidos,
                                                        "fecha": str(as_of.date())})
                out.append(c["crd_id"])
        return out

    def limitaciones(self, as_of=None) -> List[str]:
        """Texto para `limitaciones` de los entregables: servicios degradados por credenciales que faltan (R8, 17.5)."""
        out = []
        for c in self.todas(as_of).values():
            if c.get("servicio_degradado") and c.get("estado") in ("SOLICITADA", "APLAZADA", "DENEGADA"):
                out.append(f"Servicio «{c['servicio']}» degradado: credencial {c['estado'].lower()} ({c['crd_id']}); se usan fuentes "
                           "alternativas de calidad declarada y nunca se simula el acceso (R8)")
        return out
