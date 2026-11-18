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
import os
import re
import socket
import threading
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from . import respuesta_final
from .configuracion import parametro
from .contratos import (
    CAMPOS_VALOR_CREDENCIAL,
    DatosSensibles,
    clave_normalizada,
    claves_valor_credencial,
    contiene_credenciales,
    retorno_con_credencial,
)
from .herramientas.ht01_boveda import Boveda, alias_de
from .herramientas.ht06_indice import normalizar

TIPOS_CONSULTA = ("ACLARACION_ALCANCE", "DATO_O_DOCUMENTO", "PREFERENCIA_O_CRITERIO", "CONFIRMACION_SUPUESTO", "OTRA")
MODOS = ("BLOQUEANTE", "NO_BLOQUEANTE")
ESTADOS_RESPUESTA = ("RESPONDIDA", "PARCIAL")
# T-174 r02: estados de una revisión C2 que aún no ha llegado al Broker
ESTADOS_REVISION_PENDIENTE = ("EN_CURSO", "INTERRUMPIDA", "PENDIENTE", "FALLIDA", "SIN_ALCANCE")
# T-174 r03 (QA r02, H-07): revisiones C2 que este proceso está ejecutando ahora, (carpeta del almacén, cns_id, msg_id);
# común a todas las instancias del proceso, para distinguir una EN_CURSO viva de una huérfana del mismo pid. Ronda de
# cierre: H-10, la carpeta resuelta en la clave (dos almacenes con los mismos ids en un proceso)
_EN_MARCHA: set[tuple[str, str, str]] = set()
_EN_MARCHA_LOCK = threading.Lock()


def _proceso() -> dict:
    return {"host": socket.gethostname(), "pid": os.getpid()}


def _pid_vivo(pid) -> bool | None:
    """True o False si se sabe; None si no se puede saber (Windows, donde la señal 0 no es una consulta)."""
    if os.name == "nt" or not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return None
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:   # existe, de otro usuario
        return True
    return True
ESTADOS_CREDENCIAL = ("PROVISTA", "DENEGADA", "APLAZADA")
# Campos que nunca pueden viajar en un mensaje CT-25 (el valor va solo a la bóveda)
# (claves normalizadas con `contratos.clave_normalizada`, T-177 r02)
CAMPOS_VALOR = CAMPOS_VALOR_CREDENCIAL


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

    def responder(self, cns_id: str, respuestas: list[dict], estado: str = "RESPONDIDA", as_of=None,
                  ejecutar_revision: bool = True) -> dict:
        """Respuesta del Broker (CT-23 retorno). Una respuesta que contesta un supuesto que ya figuraba en un informe entregado
        abre una revisión C2 y se comunica al Broker (7.9.4 y 7.9.5; T-174, PB-61, INC-T174-01)."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        c = self._todas().get(cns_id)
        if not c:
            raise KeyError(f"Consulta desconocida {cns_id}")
        if estado not in ESTADOS_RESPUESTA:
            raise ValueError(f"Estado no válido {estado!r}")
        msg = self.b.mensajeria.crear("CT-23", "BROKER", "AG-01", {"cns_id": cns_id, "estado": estado, "respuestas": respuestas},
                                      query_id=cns_id, tipo_mensaje="RETORNO", estado="COMPLETO")
        textos = self._contestadas(c, respuestas)   # solo depende de las preguntas, que no cambian: fuera del cerrojo
        # T-174 r02 (QA r01, H-01): comprobar y reservar de una vez, también entre procesos. Se relee la CNS-, se calcula lo
        # contestado de nuevo y lo entregado, y una sola entrada deja la respuesta, sus índices y la revisión EN_CURSO
        clave = None
        try:
            with self.b.almacen._transaccion():
                c = self._todas().get(cns_id) or c
                tardia = c.get("estado") == "VENCIDA"
                previos = set(c.get("indices_respondidos") or [])
                nuevos = sorted(set(textos) - previos)
                entregados = self._entregados_con(cns_id, as_of) if nuevos else []
                rev = (self._reserva(c, {i: textos[i] for i in nuevos}, entregados, msg["msg_id"], as_of,
                                     "EN_CURSO" if ejecutar_revision else "PENDIENTE") if entregados else None)
                if rev and ejecutar_revision:   # ronda de cierre (H-09): en marcha antes de escribir EN_CURSO, bajo el cerrojo
                    clave = self._en_marcha(cns_id, msg["msg_id"], True)
                self.b.almacen.escribir("F5", "AG-01", {
                    "tipo_entrada": "CNS", "id": self.b.almacen.nuevo_id("F5CNS"), "cns_id": cns_id, "estado": estado,
                    "respuestas": respuestas, "tardia": tardia, "indices_respondidos": sorted(previos | set(textos)),
                    **({"revisiones_c2": [*(c.get("revisiones_c2") or []), rev]} if rev else {})})
            if rev and ejecutar_revision:
                rev = self._ejecutar_revision(cns_id, rev, as_of)
        finally:
            if clave:
                self._en_marcha(cns_id, msg["msg_id"], False)
        out: dict = {"cns_id": cns_id, "estado": estado, "tardia": tardia, "revision_c2": None}
        if rev:
            out["revision_c2"] = rev
            out["accion"] = (f"La respuesta contesta un supuesto que ya figuraba en lo entregado ({', '.join(rev['revisa'])}): "
                             f"se abre una revisión C2{' (' + rev['run_id'] + ')' if rev['run_id'] else ''}, en estado "
                             f"{rev['estado']}" + (", entregada al Broker por CT-02" if rev["estado"] == "ENTREGADA" else "") + " (7.9.5)")
        elif tardia:
            out["accion"] = ("Respuesta tardía: ningún informe entregado llevaba su supuesto, así que no hace falta revisión C2; "
                             "la respuesta vale desde el siguiente análisis (7.9.5)")
        if ejecutar_revision:   # T-174 r02 (H-02): las de esta CNS- que quedaron INTERRUMPIDA o PENDIENTE se relanzan
            relanzadas = self.relanzar_revisiones(as_of, cns_id=cns_id, estados=("INTERRUMPIDA", "PENDIENTE"))
            if relanzadas:
                out["revisiones_relanzadas"] = relanzadas
        return out

    def _en_marcha(self, cns_id: str, msg_id: str, alta: bool) -> tuple[str, str, str]:
        """Da de alta (o de baja) una revisión en el conjunto de las que este proceso ejecuta (H-07, H-09 y H-10)."""
        clave = (str(Path(self.b.almacen.carpeta).resolve()), cns_id, msg_id)
        with _EN_MARCHA_LOCK:
            (_EN_MARCHA.add if alta else _EN_MARCHA.discard)(clave)
        return clave

    def _contestadas(self, c: dict, respuestas) -> dict[int, str]:
        """Índices de las preguntas de la consulta que la respuesta contesta con texto (los demás no cuentan)."""
        n = len(c.get("preguntas") or [])
        out: dict[int, str] = {}
        for r in respuestas if isinstance(respuestas, list) else []:
            i = r.get("indice") if isinstance(r, dict) else None
            texto = r.get("texto") if isinstance(r, dict) else None
            if isinstance(i, int) and not isinstance(i, bool) and 0 <= i < n and isinstance(texto, str) and texto.strip():
                out.setdefault(i, texto.strip())
        return out

    def _entregados_con(self, cns_id: str, as_of) -> list[dict]:
        """RUN- entregados hasta `as_of` (C1/C2 y C6) cuyos entregables llevaban el supuesto de la consulta (`supuestos_cns`
        en F5). T-174 r02 (H-04): con la fecha de la respuesta, sin mirar lo entregado después."""
        return [e for e in self.b.almacen.estado("F5", as_of, clave="id").values()
                if e.get("tipo_entrada") in ("RUN", "RUN_C6") and e.get("entrega") == "ENTREGADA" and cns_id in (e.get("supuestos_cns") or [])]

    def _reserva(self, c: dict, textos: dict[int, str], entregados: list[dict], msg_id: str, as_of, estado: str) -> dict:
        """La revisión C2 reservada (EN_CURSO), con su alcance: los tipos de la consulta que analizó lo entregado, o todos
        los que analizó si la consulta no declara ninguno. T-174 r02 (H-03): nunca más que lo entregado."""
        vistas: set[str] = set()
        for e in entregados:
            vistas |= set(e.get("nivel_por_clase") or {}) | ({e["clase"]} if e.get("clase") else set())
        clases = sorted(set(c["clases"]) & vistas) if c.get("clases") else sorted(vistas)
        return {"msg_id": msg_id, "estado": estado, "run_id": None, "revisa": sorted(e["id"] for e in entregados),
                "clases": clases, "supuestos_invalidados": [
                    {"indice": i, "supuesto": c["preguntas"][i]["supuesto_declarado"], "respuesta": t} for i, t in sorted(textos.items())],
                "fecha": str(pd.Timestamp(as_of).date()),
                # T-174 r03 (H-07 y H-08): quién la reclama y su número de intento, ya bajo el cerrojo
                **({"intentos": 1, "proceso": _proceso()} if estado == "EN_CURSO" else {"intentos": 0})}

    def _anotar_revision(self, cns_id: str, msg_id: str, cambios: dict) -> dict:
        """Cambia, bajo el cerrojo del almacén, la revisión de esa CNS- con ese `msg_id` y devuelve cómo queda."""
        with self.b.almacen._transaccion():
            revs = list((self._todas().get(cns_id) or {}).get("revisiones_c2") or [])
            i = next(k for k, r in enumerate(revs) if r.get("msg_id") == msg_id)
            revs[i] = {**revs[i], **cambios}
            self.b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": self.b.almacen.nuevo_id("F5CNS"), "cns_id": cns_id,
                                                     "revisiones_c2": revs})
            return revs[i]

    def _ejecutar_revision(self, cns_id: str, rev: dict, as_of) -> dict:
        """Lanza (fuera del cerrojo) el ciclo AD_HOC de una revisión ya reservada EN_CURSO y anota su estado final."""
        msg_id = rev["msg_id"]
        tratamiento = f"relanzar la revisión C2 de {cns_id} (consulta-broker relanzar --cns {cns_id})"
        if not rev["clases"]:   # sin tipo analizado que revisar (RUN- sin tipos): no se lanza un ciclo de todo el alcance
            self.b.almacen.incidencia("DATOS", f"La revisión C2 de {cns_id} no tiene tipos de activo que revisar", "AG-01",
                                      tratamiento=f"revisar a mano el alcance de la revisión C2 de {cns_id}", escalado_operador=True)
            return self._anotar_revision(cns_id, msg_id, {"estado": "SIN_ALCANCE"})
        pregunta = (f"Revisión C2 por la respuesta del Broker a {cns_id}: " +
                    "; ".join(f"«{x['respuesta']}» (sustituye al supuesto declarado «{x['supuesto']}»)" for x in rev["supuestos_invalidados"]))
        disparador = {"origen": "CT-23", "cns_id": cns_id, "msg_id": msg_id, "revisa": rev["revisa"],
                      "indices": [x["indice"] for x in rev["supuestos_invalidados"]], "intento": int(rev.get("intentos") or 1)}
        try:
            res = self.b.ciclo(as_of, tipo="AD_HOC", alcance={"clases": rev["clases"], "pregunta": pregunta}, disparador=disparador)
        except Exception as e:
            fallo = type(e).__name__   # solo la clase: el texto podría llevar datos (R8)
            if respuesta_final.para_la_consulta(self.b.almacen, e):
                # T-174 r02 (H-02): un error de control o de integridad se relanza; si el almacén sigue íntegro, antes queda
                # la revisión INTERRUMPIDA (que se relanza) y la incidencia; si no, queda EN_CURSO, que también es rastro
                if all(self.b.almacen.verificar_integridad().values()):
                    self._anotar_revision(cns_id, msg_id, {"estado": "INTERRUMPIDA", "fallo": fallo})
                    self.b.almacen.incidencia("HERRAMIENTA", f"La revisión C2 de {cns_id} se interrumpió ({fallo})", "AG-01",
                                              tratamiento=tratamiento, escalado_operador=True)
                raise
            # T-174 r02 (H-05): si el RUN- de la revisión llegó a F5, su estado es el de su entrega
            run = next((x for x in reversed(self.b.almacen.leer("F5")) if x.get("tipo_entrada") == "RUN"
                        and (x.get("disparador") or {}).get("msg_id") == msg_id
                        and (x.get("disparador") or {}).get("intento") == disparador["intento"]), None)
            estado_final = (run.get("entrega") or "FALLIDA") if run else "FALLIDA"
            if estado_final != "ENTREGADA":   # T-174 r02 (H-06): lo que no llegó al Broker va al operador para relanzarlo
                self.b.almacen.incidencia("HERRAMIENTA", f"La revisión C2 de {cns_id} falló ({fallo})", "AG-01",
                                          tratamiento=tratamiento, escalado_operador=True)
            return self._anotar_revision(cns_id, msg_id, {"estado": estado_final, "fallo": fallo, "run_id": run["id"] if run else None})
        return self._anotar_revision(cns_id, msg_id, {"estado": res.get("entrega", "ENTREGADA"), "run_id": res["run_id"]})

    def _es_huerfana(self, cns_id: str, r: dict) -> bool | None:
        """Una EN_CURSO de este host cuyo proceso ya no existe, o de este mismo proceso que no está en marcha (H-07): True.
        Sin umbral de tiempo. None si no se puede juzgar desde aquí (ronda de cierre, H-11, `[PROPUESTO]` en INC-T174-01):
        de otro host, sin `proceso` (anteriores a la r03) o donde no se puede consultar el pid. False en lo demás. Un pid
        muerto que reutiliza otro proceso se ve vivo (límite declarado)."""
        if r.get("estado") != "EN_CURSO":
            return False
        p = r.get("proceso") or {}
        if not p or p.get("host") != socket.gethostname():
            return None
        if p.get("pid") == os.getpid():
            with _EN_MARCHA_LOCK:
                return (str(Path(self.b.almacen.carpeta).resolve()), cns_id, r.get("msg_id")) not in _EN_MARCHA
        vivo = _pid_vivo(p.get("pid"))
        return None if vivo is None else not vivo

    def huerfanas(self) -> list[dict]:
        """T-174 r03 (QA r02, H-07): revisiones EN_CURSO cuyo proceso murió. Cada una se avisa al operador una sola vez (una
        incidencia escalada, con la marca `aviso_huerfana` en la revisión); se relanzan con `--incluir-en-curso`."""
        out = []
        for k, c in sorted(self._todas().items()):
            for r in c.get("revisiones_c2") or []:
                if self._es_huerfana(k, r) is not True:
                    continue
                with self.b.almacen._transaccion():   # una sola incidencia aunque dos procesos la vean a la vez
                    actual: dict = next((x for x in (self._todas().get(k) or {}).get("revisiones_c2") or []
                                         if x.get("msg_id") == r.get("msg_id")), {})
                    if self._es_huerfana(k, actual) is not True:
                        continue   # otro proceso la ha reclamado entretanto
                    if not actual.get("aviso_huerfana"):
                        inc = self.b.almacen.incidencia(
                            "HERRAMIENTA", f"La revisión C2 de {k} quedó EN_CURSO sin proceso que la ejecute", "AG-01",
                            tratamiento=f"consulta-broker relanzar --incluir-en-curso --cns {k}", escalado_operador=True)
                        actual = self._anotar_revision(k, r["msg_id"], {"aviso_huerfana": inc["id"]})
                    r = actual or r
                out.append({"cns_id": k, **r, "huerfana": True})
        return out

    def revisiones_pendientes(self, as_of=None, estados: Iterable[str] = ESTADOS_REVISION_PENDIENTE) -> list[dict]:
        """Revisiones C2 que no han llegado al Broker (EN_CURSO, INTERRUMPIDA, PENDIENTE, FALLIDA o SIN_ALCANCE), con su CNS-;
        las EN_CURSO huérfanas van con `huerfana: true` y su aviso (H-07)."""
        estados = set(estados)
        huerf = {(h["cns_id"], h["msg_id"]) for h in self.huerfanas()}
        out = []
        for k, c in sorted(self._todas(as_of).items()):
            for r in c.get("revisiones_c2") or []:
                if r.get("estado") not in estados:
                    continue
                if (k, r.get("msg_id")) in huerf:
                    out.append({"cns_id": k, **r, "huerfana": True})
                elif r.get("estado") == "EN_CURSO" and self._es_huerfana(k, r) is None:
                    # H-11: no se puede juzgar desde este host (otro host, sin proceso o pid no consultable)
                    out.append({"cns_id": k, **r, "huerfana": None, "nota_huerfana": "no se puede juzgar desde este host"})
                else:
                    out.append({"cns_id": k, **r})
        return out

    def relanzar_revisiones(self, as_of, cns_id: str | None = None,
                            estados: Iterable[str] = ("INTERRUMPIDA", "PENDIENTE", "FALLIDA")) -> list[dict]:
        """Relanza las revisiones C2 pendientes (T-174 r02, H-02 y H-06). Cada una se reclama bajo el cerrojo (pasa a EN_CURSO)
        antes de lanzarla, así que dos procesos no relanzan la misma. Una EN_CURSO solo se relanza si se pide expresamente
        (`estados` con EN_CURSO): puede estar ejecutándola otro proceso; hacerlo es decisión del operador."""
        as_of = self.b.fijar_fecha(as_of or pd.Timestamp.today())
        estados = set(estados)
        out = []
        for p in self.revisiones_pendientes(None, estados):
            if cns_id and p["cns_id"] != cns_id:
                continue
            with self.b.almacen._transaccion():
                actual = next((r for r in (self._todas().get(p["cns_id"]) or {}).get("revisiones_c2") or []
                               if r.get("msg_id") == p["msg_id"]), None)
                if not actual or actual.get("estado") not in estados:
                    continue   # otro proceso ya la ha reclamado o terminado
                # T-174 r03 (H-08): si un intento anterior ya entregó su RUN- (el proceso murió después), se anota sin otro ciclo
                hecho = next((x for x in reversed(self.b.almacen.leer("F5")) if x.get("tipo_entrada") == "RUN"
                              and (x.get("disparador") or {}).get("msg_id") == p["msg_id"] and x.get("entrega") == "ENTREGADA"), None)
                if hecho and actual.get("estado") in ("EN_CURSO", "INTERRUMPIDA"):
                    out.append({"cns_id": p["cns_id"], **self._anotar_revision(p["cns_id"], p["msg_id"], {
                        "estado": "ENTREGADA", "run_id": hecho["id"]})})
                    continue
                self._en_marcha(p["cns_id"], p["msg_id"], True)   # H-09: en marcha antes de escribir EN_CURSO
                try:
                    rev = self._anotar_revision(p["cns_id"], p["msg_id"], {"estado": "EN_CURSO", "proceso": _proceso(),
                                                                             "intentos": int(actual.get("intentos") or 0) + 1})
                except BaseException:
                    self._en_marcha(p["cns_id"], p["msg_id"], False)
                    raise
            try:
                out.append({"cns_id": p["cns_id"], **self._ejecutar_revision(p["cns_id"], rev, as_of)})
            finally:
                self._en_marcha(p["cns_id"], p["msg_id"], False)
        return out

    def nota_revision(self, disparador: dict | None) -> list[str]:
        """Lo que el paquete de una revisión C2 abierta por una respuesta CT-23 declara en sus limitaciones (7.9.5)."""
        d = disparador or {}
        if d.get("origen") != "CT-23" or not d.get("cns_id"):
            return []
        c = self._todas().get(d["cns_id"]) or {}
        supuestos = "; ".join(f"«{p['supuesto_declarado']}»" for i, p in enumerate(c.get("preguntas") or []) if i in (d.get("indices") or []))
        return [(f"Revisión C2 de {', '.join(d.get('revisa') or [])}: el Broker contestó a {d['cns_id']} después de la entrega y el "
                 f"supuesto declarado {supuestos} ya no se aplica (7.9.5)")]

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
                vencida = self._instante(c.get("plazo_respuesta"), plazo=True) <= ahora
            except (ValueError, TypeError):   # T-93 (H-38) y T-103 (H-43): un plazo que ya no se lee o que falta
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
        # T-177 r02 (QA r01, H-03): comprobar lo previo y escribir la CRD- de una vez, también entre procesos (dos C4 a la vez)
        with self.b.almacen._transaccion():
            # H-02: lo previo se busca por el alias de la bóveda, no por la grafía literal del servicio
            previas = [c for c in self._todas().values() if alias_de(str(c.get("servicio") or "")) == alias_de(servicio)]
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

    def desde_retorno(self, retorno, solicitante: str, as_of, origen: str | None = None) -> dict:
        """T-177 (PB-58, 7.10.1 y 7.10.2): el Coordinador lee las `solicitudes_credenciales` del retorno de un agente (hoy, el
        del BFA en el mantenimiento C4), las deduplica por alias de la bóveda, comprueba en HT-01 que faltan de verdad y emite
        el CT-25 con `solicitar`. Falla cerrado: un retorno con un campo de valor (o algo que parezca una credencial) se
        rechaza íntegro, con incidencia SEGURIDAD y sin copiar el dato (6.2.5); una solicitud mal formada se descarta con su
        motivo; sin retorno, no se pide nada. Devuelve lo resuelto de cada solicitud, sin valores."""
        if retorno is None:
            return {"solicitudes": [], "descartadas": [], "rechazo": None}
        try:
            sensible = bool(claves_valor_credencial(retorno)) or bool(contiene_credenciales(retorno))
        except RecursionError:   # demasiado anidado para comprobarlo: falla cerrado
            sensible = True
        if sensible:
            self.b.almacen.incidencia("SEGURIDAD", "Retorno con solicitudes de credenciales que trae un valor de credencial: "
                                      "rechazado íntegro sin copiarlo (R8, 6.2.5)", solicitante, origen=origen)
            return {"solicitudes": [], "descartadas": [], "rechazo": "VALOR_DE_CREDENCIAL_EN_EL_RETORNO"}
        # T-177 r02 (QA r01, H-06) y r03 (QA r02, H-08, H-10 y H-11): una ficha opaca en cualquier clave u hoja de texto de las
        # solicitudes (o del retorno, si pide algo), o un número bajo una clave de valor, rechaza el retorno entero antes de
        # pedir nada; es la misma regla que aplica `llm.respuesta_segura` antes de la caché
        try:
            opaca = retorno_con_credencial(retorno)
        except RecursionError:
            opaca = True
        if opaca:
            self.b.almacen.incidencia("SEGURIDAD", "Solicitud de credencial con una ficha opaca (posible valor): retorno "
                                      "rechazado íntegro sin copiarla (R8, 6.2.5)", solicitante, origen=origen)
            return {"solicitudes": [], "descartadas": [], "rechazo": "VALOR_DE_CREDENCIAL_EN_EL_RETORNO"}
        lista = retorno.get("solicitudes_credenciales") if isinstance(retorno, dict) else None
        if lista is None:
            return {"solicitudes": [], "descartadas": [], "rechazo": None}
        if not isinstance(lista, list):
            return {"solicitudes": [], "descartadas": [{"indice": None, "motivo": "solicitudes_credenciales no es una lista"}],
                    "rechazo": None}
        resueltas: list[dict] = []
        descartadas: list[dict] = []
        vistos: dict[str, int] = {}
        for i, s in enumerate(lista):
            if not isinstance(s, dict):
                descartadas.append({"indice": i, "motivo": "la solicitud no es un objeto"})
                continue
            campos = {"servicio": s.get("servicio"), "motivo": s.get("motivo"),
                      "impacto_si_falta": s.get("impacto_si_falta", s.get("impacto"))}
            textos = {k: v.strip() for k, v in campos.items() if isinstance(v, str) and v.strip()}
            faltan = [k for k in campos if k not in textos]
            if faltan:
                descartadas.append({"indice": i, "motivo": "faltan " + ", ".join(faltan)})
                continue
            servicio, motivo, impacto = textos["servicio"], textos["motivo"], textos["impacto_si_falta"]
            alias = alias_de(servicio)
            if alias in vistos:   # deduplicación (7.10.2): un mismo servicio de la bóveda, una sola solicitud
                descartadas.append({"indice": i, "motivo": f"duplicada de la solicitud {vistos[alias]}"})
                continue
            vistos[alias] = i
            urgencia = "ALTA" if s.get("urgencia") == "ALTA" else "NORMAL"
            r = self.solicitar(servicio, solicitante, motivo, impacto, urgencia, as_of=as_of)
            resueltas.append({"servicio": servicio, "resultado": r["estado"], "crd_id": r.get("crd_id"),
                              "credencial_ref": r.get("credencial_ref")})
        return {"solicitudes": resueltas, "descartadas": descartadas, "rechazo": None}

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
            con_valor = sorted(str(k) for k in respuesta if clave_normalizada(k) in CAMPOS_VALOR)   # T-177 r02 (H-05)
            if con_valor:
                self.b.almacen.incidencia("SEGURIDAD", "Respuesta CT-25 con un campo de valor de credencial rechazada íntegra (R8, 6.2.5)",
                                          "BROKER", campo_afectado=con_valor)
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

    def degradaciones(self, as_of) -> list[dict]:
        """Servicios en modo degradado que no se han provisto: por una credencial denegada (limitación de F10) o pendiente
        de una solicitud CT-25 abierta. Los entregables los declaran (PB-58 y PB-60, INC-T116-03): el modo degradado no
        queda solo en F10 ni en la respuesta a la solicitud."""
        as_of = pd.Timestamp(as_of)
        por_servicio: dict[str, dict] = {}
        for e in self.b.almacen.estado("F10", as_of).values():
            if e.get("tipo_entrada") == "LIMITACION_SERVICIO" and e.get("servicio"):
                por_servicio[e["servicio"]] = {"servicio": e["servicio"], "crd_id": e.get("crd_id"), "estado": "DENEGADA"}
        for c in self._todas(as_of).values():   # una solicitud abierta es posterior a la denegación (cambio de circunstancias)
            if c.get("estado") in ("SOLICITADA", "APLAZADA") and c.get("servicio"):
                por_servicio[c["servicio"]] = {"servicio": c["servicio"], "crd_id": c["crd_id"], "estado": c["estado"]}
        return [d for s, d in sorted(por_servicio.items()) if self.boveda.estado_servicio(s, as_of.date())["estado"] != "PROVISTA"]

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
