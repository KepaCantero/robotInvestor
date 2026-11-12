"""Comunicación fluida con el Broker (Documento 0 óptima V5.1): consultas del bloque al Broker (CT-23, 7.9, R26)
y solicitud y provisión de credenciales (CT-25, 7.10, R8) con la bóveda simulada de HT-01.

- Todo queda en F5 (CNS-, CRD-), escrito por el Coordinador (AG-01); los mensajes pasan por `Mensajeria`,
  que rechaza cualquier credencial o dato personal (6.2.5).
- `BLOQUEANTE`: pausa en el siguiente punto de control (F0 del siguiente análisis) los tipos de activo afectados;
  `NO_BLOQUEANTE`: el análisis sigue con el supuesto declarado. Al vencer el plazo sin respuesta se aplica el
  supuesto, que el paquete transporta en `supuestos_declarados` (6.2.9) y HT-09 comprueba (C19).
"""
from __future__ import annotations

import copy
import datetime as dt
import re
from collections.abc import Iterable

import pandas as pd

from .configuracion import parametro
from .contratos import DatosSensibles, contiene_credenciales
from .herramientas.ht01_boveda import Boveda, alias_de
from .herramientas.ht06_indice import normalizar

TIPOS_CONSULTA = ("ACLARACION_ALCANCE", "DATO_O_DOCUMENTO", "PREFERENCIA_O_CRITERIO", "CONFIRMACION_SUPUESTO", "OTRA")
MODOS = ("BLOQUEANTE", "NO_BLOQUEANTE")
ESTADOS_RESPUESTA = ("RESPONDIDA", "PARCIAL")
ESTADOS_CREDENCIAL = ("PROVISTA", "DENEGADA", "APLAZADA")
# Campos que nunca pueden viajar en un mensaje CT-25 (el valor va solo a la bóveda)
CAMPOS_VALOR = {"valor", "clave", "secreto", "valor_credencial", "password", "token", "api_key", "apikey"}


RE_SOLO_FECHA = re.compile(r"\d{4}-\d{2}-\d{2}|\d{8}")
RE_FECHA_ISO = re.compile(r"(\d{4}-\d{2}-\d{2}|\d{8})([T ]\d{2}:\d{2}(:\d{2}(\.\d{1,9})?)?(Z|[+-]\d{2}:?\d{2})?)?")

class ConsultasBroker:
    """CT-23 · Consulta al Broker (Coordinador ↔ Broker)."""

    def __init__(self, bloque) -> None:
        self.b = bloque
        self.cfg = bloque.cfg.get("consultas_broker") or {}

    # ------------------------------------------------------------------------------ utilidades
    def _todas(self, as_of=None) -> dict[str, dict]:
        return {k: v for k, v in self.b.almacen.estado("F5", as_of, clave="cns_id").items() if v.get("tipo_entrada", "").startswith("CNS")}

    def _instante(self, fecha, *, plazo: bool = False):
        """Instante en la zona del reloj. Con `plazo`, un plazo que solo trae la fecha vence al terminar ese día, como en la
        versión anterior (T-92, QA r01, H-15), y no a las 00:00."""
        # T-92 (QA r03, H-30): solo fechas ISO 8601 («2026-06-08», «20260608», con hora y zona opcionales); «2026», «2026-06»
        # o «8 June 2026» se rechazan en lugar de interpretarse
        # T-93 (H-37): un número o un booleano no es una fecha (20260608 se leería como nanosegundos de 1970); una `date`
        # sin hora es su fecha en texto, para que un plazo venza al terminar ese día y no al empezarlo
        if isinstance(fecha, bool) or (isinstance(fecha, (int, float)) and not isinstance(fecha, dt.datetime)) or (
                hasattr(fecha, "dtype") and getattr(fecha.dtype, "kind", "") in "biuf"):
            raise ValueError(f"Fecha u hora de consulta CT-23 no válida (se espera ISO 8601, no un número): {fecha!r}")
        if isinstance(fecha, dt.date) and not isinstance(fecha, dt.datetime):
            fecha = fecha.isoformat()
        if isinstance(fecha, str) and not RE_FECHA_ISO.fullmatch(fecha.strip()):
            raise ValueError(f"Fecha u hora de consulta CT-23 no válida (se espera ISO 8601): {fecha!r}")
        t = pd.Timestamp(fecha)
        if pd.isna(t):
            raise ValueError("Fecha u hora de consulta CT-23 no válida")
        # T-92 (QA r02, H-22): un plazo con solo fecha vence al terminar ese día en la zona del reloj (medianoche local
        # siguiente menos 1 µs), también en los cambios de hora; si la medianoche no existe en esa zona, la primera hora válida
        zona = self.b.reloj.zona
        if plazo and isinstance(fecha, str) and RE_SOLO_FECHA.fullmatch(fecha.strip()):
            siguiente = (t + pd.Timedelta(days=1)).normalize().tz_localize(zona, nonexistent="shift_forward", ambiguous=True)
            return siguiente - pd.Timedelta(microseconds=1)
        if t.tzinfo is None:
            return t.tz_localize(zona, nonexistent="shift_forward", ambiguous=True)
        return t.tz_convert(zona)

    def _plazo(self, modo: str, ahora) -> str:
        horas = (self.cfg.get("plazo_horas") or {}).get(modo, 4 if modo == "BLOQUEANTE" else 24)
        return (ahora + dt.timedelta(hours=float(horas))).isoformat(timespec="minutes")

    # ------------------------------------------------------------------------------ saliente
    def enviar(self, consulta: dict, as_of=None) -> dict:
        """Envía al Broker dudas ya filtradas y agrupadas por el Analizador (o de admisión, en F0)."""
        ahora = self._instante(as_of if as_of is not None else pd.Timestamp.now(tz=self.b.reloj.zona))
        as_of = self.b.fijar_fecha(ahora.date())
        tipo, modo = consulta.get("tipo"), consulta.get("modo", "NO_BLOQUEANTE")
        if tipo not in TIPOS_CONSULTA:
            raise ValueError(f"Tipo de consulta no válido {tipo!r} (válidos: {', '.join(TIPOS_CONSULTA)})")
        if modo not in MODOS:
            raise ValueError(f"Modo no válido {modo!r}")
        preguntas = consulta.get("preguntas") or []
        if not preguntas:
            raise ValueError("La consulta no lleva preguntas")
        for p in preguntas:
            if not p.get("texto") or not p.get("supuesto_declarado"):
                raise ValueError("Cada pregunta necesita «texto» y «supuesto_declarado» (7.9.2)")
        if contiene_credenciales(consulta):
            self.b.almacen.incidencia("SEGURIDAD", "Consulta CT-23 con datos protegidos rechazada (R8)", "AG-01")
            raise DatosSensibles("La consulta contiene datos protegidos")
        run_id = consulta.get("run_id")
        maximo = int(parametro(self.b.cfg, "consultas_broker.max_mensajes_por_run"))
        previas = [c for c in self._todas().values() if run_id and c.get("run_id") == run_id and c.get("sentido") == "SALIENTE"]
        if run_id and len(previas) >= maximo:
            # Agrupación: el Coordinador no supera el máximo de mensajes por análisis (Anexo A); añade las preguntas al último
            ult = sorted(previas, key=lambda c: c["cns_id"])[-1]
            e = self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS_AMPLIACION", "id": self.b.almacen.nuevo_id("F5CNS"),
                                                         "cns_id": ult["cns_id"], "preguntas": ult.get("preguntas", []) + preguntas,
                                                         "nota": f"Agrupada: máximo de {maximo} mensajes CT-23 por RUN- alcanzado"})
            return {"cns_id": ult["cns_id"], "estado": "AGRUPADA", "preguntas": len(e["preguntas"])}
        dado = consulta.get("plazo_respuesta")   # T-93 (H-37): sin plazo solo es None o «»; False o 0 se rechazan, no se ignoran
        plazo = self._plazo(modo, ahora) if dado is None or dado == "" else self._instante(dado, plazo=True).isoformat()
        cns_id = self.b.almacen.nuevo_id("CNS")
        cuerpo = {"cns_id": cns_id, "sentido": "SALIENTE", "run_id": run_id, "seg_id": consulta.get("seg_id"), "tipo": tipo, "modo": modo,
                  "preguntas": copy.deepcopy(preguntas), "clases": list(consulta.get("clases") or []),
                  "plazo_respuesta": plazo,
                  "punto_control": consulta.get("punto_control") or ("F0 del siguiente análisis de los tipos afectados" if modo == "BLOQUEANTE" else None),
                  "motivo": consulta.get("motivo") or normalizar(preguntas[0]["texto"])[:80]}
        msg = self.b.mensajeria.crear("CT-23", "AG-01", "BROKER", cuerpo, run_id=run_id, query_id=cns_id)
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": cns_id, **cuerpo, "estado": "ENVIADA", "msg_id": msg["msg_id"]})
        self._recurrencia(tipo, cuerpo["motivo"], as_of)
        return {"cns_id": cns_id, "estado": "ENVIADA", "plazo_respuesta": cuerpo["plazo_respuesta"], "modo": modo}

    def responder(self, cns_id: str, respuestas: list[dict], estado: str = "RESPONDIDA", as_of=None) -> dict:
        """Respuesta del Broker (CT-23 retorno). Una respuesta tardía que invalida un supuesto ya entregado abre una revisión (C2)."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        c = self._todas().get(cns_id)
        if not c:
            raise KeyError(f"Consulta desconocida {cns_id}")
        if estado not in ESTADOS_RESPUESTA:
            raise ValueError(f"Estado no válido {estado!r}")
        self.b.mensajeria.crear("CT-23", "BROKER", "AG-01", {"cns_id": cns_id, "estado": estado, "respuestas": respuestas},
                                query_id=cns_id, tipo_mensaje="RETORNO", estado="COMPLETO")
        tardia = c.get("estado") == "VENCIDA"
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": self.b.almacen.nuevo_id("F5CNS"), "cns_id": cns_id,
                                                 "estado": estado, "respuestas": respuestas, "tardia": tardia})
        out = {"cns_id": cns_id, "estado": estado, "tardia": tardia}
        if tardia:
            out["accion"] = ("Respuesta tardía: si invalida un supuesto de un informe ya entregado, se trata como petición de "
                             "revisión (C2) y se comunica al Broker (7.9.5)")
        return out

    def entrante(self, contenido: str, referencia: dict | None = None, as_of=None) -> dict:
        """Aportación espontánea del Broker (CT-23 entrante): se registra y se asocia a su RUN-, OPP- o SEG-."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        cns_id = self.b.almacen.nuevo_id("CNS")
        cuerpo = {"cns_id": cns_id, "sentido": "ENTRANTE", "tipo": "OTRA", "modo": "NO_BLOQUEANTE", "contenido": contenido,
                  "referencia": referencia or {}}
        self.b.mensajeria.crear("CT-23", "BROKER", "AG-01", cuerpo, query_id=cns_id)
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": cns_id, **cuerpo, "estado": "RECIBIDA",
                                                 "tratamiento": "evidencia con fuente BROKER (vía Analizador y Curador) si aporta datos"})
        return {"cns_id": cns_id, "estado": "RECIBIDA"}

    # ------------------------------------------------------------------------------ plazos y puntos de control
    def vencer(self, as_of) -> list[str]:
        """Marca VENCIDA toda consulta ENVIADA cuyo plazo ha pasado; el análisis sigue con el supuesto declarado."""
        ahora = self._instante(as_of)
        self.b.fijar_fecha(ahora.date())
        out = []
        for k, c in self._todas(ahora.date()).items():
            if c.get("estado") != "ENVIADA" or c.get("sentido") != "SALIENTE":
                continue
            try:
                vencida = self._instante(c["plazo_respuesta"], plazo=True) <= ahora
            except (ValueError, TypeError):   # T-93 (H-38): un plazo guardado por una versión anterior que ya no se lee
                self.b.almacen.incidencia("DATOS", f"Consulta CT-23 {k} con un plazo que no se puede leer ({str(c.get('plazo_respuesta'))[:40]!r}): "
                                                   "se da por vencida y el análisis sigue con el supuesto declarado", "AG-01")
                vencida = True
            if vencida:
                self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": self.b.almacen.nuevo_id("F5CNS"), "cns_id": k,
                                                         "estado": "VENCIDA", "supuestos_aplicados": [
                                                             {"indice": i, "supuesto": p["supuesto_declarado"]} for i, p in enumerate(c["preguntas"])]})
                out.append(k)
        return out

    def _afecta(self, c: dict, clases: Iterable[str]) -> bool:
        return not c.get("clases") or bool(set(c["clases"]) & set(clases))

    def clases_pausadas(self, as_of, clases: Iterable[str]) -> dict[str, str]:
        """Tipos de activo pausados en este punto de control por una consulta BLOQUEANTE sin respuesta ni vencimiento."""
        out: dict[str, str] = {}
        for k, c in sorted(self._todas(as_of).items()):
            if c.get("estado") == "ENVIADA" and c.get("modo") == "BLOQUEANTE" and c.get("sentido") == "SALIENTE":
                # Sin tipos declarados afecta a todo el alcance, igual que en `_afecta` (7.9, R26)
                for cl in (c.get("clases") or list(clases)):
                    if cl in clases:
                        out.setdefault(cl, k)
        return out

    def supuestos_declarados(self, as_of, clases: Iterable[str]) -> list[dict]:
        """6.2.9: supuestos de las consultas sin respuesta (NO_BLOQUEANTE pendientes o VENCIDAS) que afectan al análisis."""
        out = []
        clases = list(clases)
        for k, c in sorted(self._todas(as_of).items()):
            pendiente = c.get("estado") == "VENCIDA" or (c.get("estado") == "ENVIADA" and c.get("modo") == "NO_BLOQUEANTE")
            if c.get("sentido") != "SALIENTE" or not pendiente or not self._afecta(c, clases):
                continue
            for p in c.get("preguntas", []):
                s = {"supuesto": p["supuesto_declarado"], "cns_id": k, "efecto_si_falso": p.get("efecto_si_falso") or "No declarado"}
                if c.get("clases"):
                    s["clases"] = [x for x in c["clases"] if x in clases]
                out.append(s)
        return out

    def _recurrencia(self, tipo: str, motivo: str, as_of) -> None:
        n, semanas = int(parametro(self.b.cfg, "consultas_broker.recurrente.repeticiones")), int(parametro(self.b.cfg, "consultas_broker.recurrente.semanas"))
        desde = pd.Timestamp(as_of) - pd.Timedelta(weeks=semanas)
        iguales = [c for c in self.b.almacen.leer("F5", as_of) if c.get("tipo_entrada") == "CNS" and c.get("sentido") == "SALIENTE"
                   and c.get("tipo") == tipo and c.get("motivo") == motivo and pd.Timestamp(c["_fecha"]) >= desde]
        if len(iguales) == n:
            ids = [c["cns_id"] for c in iguales]
            self.b.mensajeria.crear("CT-22", "AG-01", "AG-20", {"tipo_aviso": "CONSULTA_RECURRENTE", "cns_ids": ids, "tipo_consulta": tipo,
                                                                "motivo": motivo, "repeticiones": n, "ventana": f"{semanas} semanas",
                                                                "propuesta": "Añadir una pregunta de admisión o un valor por defecto al CT-01 "
                                                                             "para no repetir esta consulta"},
                                    query_id=ids[-1])
            self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "AVISO_CT22", "id": self.b.almacen.nuevo_id("F5AV"),
                                                     "tipo_aviso": "CONSULTA_RECURRENTE", "cns_ids": ids})


class Credenciales:
    """CT-25 · Solicitud y provisión de credenciales (Coordinador ↔ Broker; clave en la bóveda de HT-01)."""

    def __init__(self, bloque, carpeta_boveda) -> None:
        self.b = bloque
        self.boveda = Boveda(carpeta_boveda)
        self.cfg = bloque.cfg.get("credenciales") or {}

    def _todas(self, as_of=None) -> dict[str, dict]:
        return {k: v for k, v in self.b.almacen.estado("F5", as_of, clave="crd_id").items() if v.get("tipo_entrada") == "CRD"}

    def estado(self, servicio: str | None = None) -> list[dict]:
        hoy = self.b.reloj.fecha
        if servicio:
            return [self.boveda.estado_servicio(servicio, hoy)]
        return self.boveda.listar(hoy)

    def solicitar(self, servicio: str, solicitante: str, uso_previsto: str, impacto_si_falta: str, urgencia: str = "NORMAL",
                  as_of=None, cambio_circunstancias: bool = False) -> dict:
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        e = self.boveda.estado_servicio(servicio, as_of.date())
        if e["estado"] == "PROVISTA":
            return {"estado": "PROVISTA", "credencial_ref": e["alias"], "solicitud": None}
        previas = [c for c in self._todas().values() if c.get("servicio") == servicio]
        abiertas = [c for c in previas if c.get("estado") in ("SOLICITADA", "APLAZADA")]
        if abiertas:
            return {"estado": "YA_SOLICITADA", "crd_id": abiertas[-1]["crd_id"], "modo": "DEGRADADO_DECLARADO"}
        if any(c.get("estado") == "DENEGADA" for c in previas) and not cambio_circunstancias:
            return {"estado": "DENEGADA", "modo": "DEGRADADO_DECLARADO",
                    "nota": "Credencial denegada: no se vuelve a pedir salvo cambio de circunstancias (Anexo A)"}
        crd_id = self.b.almacen.nuevo_id("CRD")
        cuerpo = {"crd_id": crd_id, "servicio": servicio, "herramienta": "HT-01", "uso_previsto": uso_previsto, "solicitante": solicitante,
                  "impacto_si_falta": impacto_si_falta, "urgencia": urgencia}
        msg = self.b.mensajeria.crear("CT-25", "AG-01", "BROKER", cuerpo, query_id=crd_id)
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CRD", "id": crd_id, **cuerpo, "estado": "SOLICITADA",
                                                 "credencial_ref": None, "recordatorios": 0, "msg_id": msg["msg_id"],
                                                 "estado_boveda": e["estado"]})
        return {"estado": "SOLICITADA", "crd_id": crd_id, "modo": "DEGRADADO_DECLARADO"}

    def responder(self, respuesta: dict, as_of=None) -> dict:
        """Respuesta del Broker (CT-25 retorno): solo estado y alias. Si trae el valor, se rechaza íntegra (6.2.5)."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        crd_id = respuesta.get("crd_id")
        if not isinstance(crd_id, str):
            raise ValueError("Se requiere el identificador de la solicitud CT-25")
        c = self._todas().get(crd_id)
        if not c:
            raise KeyError(f"Solicitud desconocida {crd_id}")
        try:
            if set(respuesta) & CAMPOS_VALOR:
                self.b.almacen.incidencia("SEGURIDAD", "Respuesta CT-25 con un campo de valor de credencial rechazada íntegra (R8, 6.2.5)",
                                          "BROKER", campo_afectado=sorted(set(respuesta) & CAMPOS_VALOR))
                raise DatosSensibles("Campo de valor de credencial en un mensaje")
            self.b.mensajeria.crear("CT-25", "BROKER", "AG-01", respuesta, query_id=crd_id, tipo_mensaje="RETORNO", estado="COMPLETO")
        except DatosSensibles:
            self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CRD", "id": self.b.almacen.nuevo_id("F5CRD"), "crd_id": crd_id,
                                                     "estado": c["estado"], "incidencia": "Respuesta con el valor de la credencial "
                                                     "rechazada sin copiarlo; se pide al Broker que la deposite en la bóveda y la renueve"})
            return {"crd_id": crd_id, "estado": "RECHAZADA_CREDENCIAL_EXPUESTA",
                    "accion": "Deposite la credencial en la bóveda de HT-01 y renuévela: ha quedado expuesta en un mensaje (7.10.3)"}
        estado = respuesta.get("estado_credencial", respuesta.get("estado"))
        if estado not in ESTADOS_CREDENCIAL:
            raise ValueError(f"Estado no válido {estado!r}")
        ref = respuesta.get("credencial_ref")
        if estado == "PROVISTA":
            ref = ref or alias_de(c["servicio"])
            if not isinstance(ref, str):
                raise ValueError("El alias de credencial debe ser texto")
            ficha = self.boveda.estado(ref, as_of.date())
            if ficha["estado"] != "PROVISTA" or ficha.get("servicio") != c["servicio"]:
                return {"crd_id": crd_id, "estado": "INCOHERENTE",
                        "nota": "El alias no corresponde a una credencial vigente del servicio solicitado"}
        self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CRD", "id": self.b.almacen.nuevo_id("F5CRD"), "crd_id": crd_id,
                                                 "estado": estado, "credencial_ref": ref, "caducidad": respuesta.get("caducidad")})
        if estado == "DENEGADA":
            self.b.almacen.escribir("F10", "AG-01", {"tipo_entrada": "LIMITACION_SERVICIO", "param_id": f"SRV-{alias_de(c['servicio'])[14:]}",
                                                      "servicio": c["servicio"], "valor_vigente": "DEGRADADO (credencial denegada)",
                                                      "crd_id": crd_id})
        return {"crd_id": crd_id, "estado": estado, "credencial_ref": ref}

    def depositar(self, crd_id: str, valor: str, caducidad: str | None = None, as_of=None) -> dict:
        """Simula el procedimiento seguro del Broker: deposita en la bóveda (fuera de banda) y responde PROVISTA con el alias."""
        c = self._todas().get(crd_id)
        if not c:
            raise KeyError(f"Solicitud desconocida {crd_id}")
        r = self.boveda.depositar(c["servicio"], valor, caducidad)
        return self.responder({"crd_id": crd_id, "estado": "PROVISTA", "credencial_ref": r["credencial_ref"], "caducidad": caducidad}, as_of)

    def recordatorios(self, as_of) -> list[str]:
        as_of = pd.Timestamp(as_of)
        dias, maximo = int(parametro(self.b.cfg, "credenciales.recordatorio_dias")), int(parametro(self.b.cfg, "credenciales.max_recordatorios"))
        out = []
        for k, c in self._todas(as_of).items():
            if c.get("estado") != "SOLICITADA" or int(c.get("recordatorios", 0)) >= maximo:
                continue
            if (as_of - pd.Timestamp(c["_ultima_fecha"])).days >= dias:
                self.b.mensajeria.crear("CT-25", "AG-01", "BROKER", {k2: c[k2] for k2 in ("crd_id", "servicio", "uso_previsto", "solicitante",
                                                                                         "impacto_si_falta")} | {"recordatorio": True},
                                        query_id=k)
                self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CRD", "id": self.b.almacen.nuevo_id("F5CRD"), "crd_id": k,
                                                         "estado": "SOLICITADA", "recordatorios": int(c.get("recordatorios", 0)) + 1})
                out.append(k)
        return out
