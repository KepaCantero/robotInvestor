"""T-196 · Cola de peticiones del Coordinador (AG-01): ninguna petición se rechaza por número; todas se encolan por prioridad
con envejecimiento y cada una lleva su nivel y su presupuesto proporcional (R5; 4.2, 7.1, 7.2, 7.6 y 10.3 del Documento 0
V5.3; prompt del Coordinador V5.0, 6.1 y 6.3; Plan de pruebas V3.0, PB-08).

- **Dos carriles** (6.1 del prompt). Las consultas N0 (CT-03) se responden al recibirse, sin pasar por aquí (`Bloque.consulta`).
  Aquí entran los CT-01 (`recibir`) y el análisis escalado de una CT-03 de ruta ANALITICA (`Bloque.consulta` con
  `encolar_escalado=True`, que llama a `encolar_consulta`).
- **Registro** (regla 2 del esquema de F5: «toda petición se registra, también las encoladas»). Cada petición es una entrada
  `PETICION` (`PET-`) de F5, de AG-01, con una entrada nueva (mismo `id`) por cambio de estado: ENCOLADA → EN_CURSO →
  ATENDIDA | FALLIDA. No es un RUN- ENCOLADO: el RUN- nace al servirse, y su `disparador` lleva el `pet_id`.
- **Prioridad efectiva** = base + envejecimiento + urgencia (6.1 del prompt): la base de la prioridad, `envejecimiento_por_hora`
  puntos por hora completa de espera hasta `envejecimiento_max`, y `urgencia_puntos` si a la `fecha_objetivo` le quedan menos
  de `urgencia_margen_h` horas. Se sirve de mayor a menor; a igualdad, el nivel menor y después el orden de llegada. Los
  números salen de `cola_peticiones` de la configuración ([PROPUESTO], INC-T196-01). El «+20 si el margen es menor que la
  duración estimada P80» no se aplica: el ejecutor no mide duraciones (declarado).
- **Presupuesto proporcional por nivel**: el del Anexo A (`presupuesto_uc`, P-17), con la misma regla que el ciclo
  (`presupuesto_por_clase`, que usa también `Bloque._reparto`).
- **Plazo comunicado**: la posición en la cola, las UC que hay por delante y la fecha objetivo. Sin hora estimada, porque no hay
  duraciones medidas ([PROPUESTO], INC-T196-01).
- **Falla cerrado.** Todo se valida antes de escribir nada. La toma de una petición, que la pasa a EN_CURSO, va en una
  transacción del almacén (exclusión también entre procesos). Si el ciclo falla, la PET- queda FALLIDA con la clase del error y
  una incidencia, y el error se relanza: nada se absorbe ni se descarta en silencio.
- **r02 (QA r01).** H-01: el orden y la toma solo ven las PET- ya recibidas en el instante (`recibida <= t`); una posterior
  aún no había llegado y no es un error, y `atender` admite un reloj para tomar cada una con un instante nuevo. H-02: el plazo
  nunca falla por la recepción de otra petición, y todo lo que puede fallar al recibir se valida antes de crear el mensaje y de
  reservar su `msg_id`. H-03: la toma guarda el proceso (`host`, `pid`); una EN_CURSO cuyo proceso ya no la sirve deja una
  incidencia Operativa, una sola vez, sin tocar su estado, y `reconciliar` (CLI `reconciliar-peticion --fallida`) la pasa a
  FALLIDA con su final FALLIDO. H-04: los nanosegundos se truncan a microsegundos, de forma explícita. H-05: sin zona, las horas
  inexistentes o ambiguas por el cambio de hora se rechazan con `PeticionInvalida`. H-06: lo que se toma con `tomar` se sirve con `servir`. H-07: un CT-01 sin ninguna clase activa se
  rechaza antes de crear el mensaje.
"""
from __future__ import annotations

import datetime as dt
import math
import os
import re
import threading
from typing import Any

import pandas as pd

from . import respuesta_final
from .configuracion import parametro, perfiles_activos
from .herramientas.ht08_monitor import PRIORIDADES
from .interfaz_broker import _pid_vivo, _proceso

TIPOS_CT01 = ("AD_HOC", "PROFUNDIZACION", "PERIODICO")
NIVELES = ("N1", "N2", "N3")   # los de la cola; N0 va por el carril rápido
ESTADOS = ("ENCOLADA", "EN_CURSO", "ATENDIDA", "FALLIDA")
EN_COLA = ("ENCOLADA", "EN_CURSO")
PERCENTIL_N0 = 0.9   # el p90 del criterio de PB-08 (definición, no un parámetro)
# Fecha-hora de CT-01 (Anexo B, «AAAA-MM-DDThh:mm»), con segundos (y fracción) y zona opcionales
RE_FECHA_HORA = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d{1,6})?)?(Z|[+-]\d{2}:\d{2})?")
# r02 (H-03): PET- que este proceso está sirviendo ahora, (carpeta del almacén, pet_id), como `interfaz_broker._EN_MARCHA`
# (T-174): una EN_CURSO con el pid de este proceso que no está aquí es huérfana (tomada y no servida)
_EN_MARCHA: set[tuple[str, str]] = set()
_EN_MARCHA_LOCK = threading.Lock()
ERROR_HUERFANA = "PROCESO_TERMINADO"


class PeticionInvalida(ValueError):
    pass


def presupuesto_por_clase(cfg: dict, tipo: str, clases: list[str], nivel: dict[str, str]) -> dict[str, float]:
    """UC de cada tipo de activo según su nivel (Anexo A, P-17): N1 y N2 por tipo, N3 por petición (repartido entre sus
    tipos en las que no son del ciclo periódico). La misma regla en la cola y en `Bloque._reparto`."""
    asign = {c: float(parametro(cfg, f"presupuesto_uc.{nivel[c]}")) for c in clases}
    if tipo != "PERIODICO" and any(nivel[c] == "N3" for c in clases):
        asign = {c: float(parametro(cfg, "presupuesto_uc.N3")) / max(len(clases), 1) for c in clases}
    return asign


def objetivo_n0(cfg: dict) -> float:
    """Objetivo de respuesta N0 en segundos (Anexo A, P-21: «< 2 minutos»)."""
    return float(parametro(cfg, "cola_peticiones.objetivo_respuesta_n0_s"))


def p90(tiempos: list[float]) -> float:
    """Percentil 90 por rango más próximo (el valor observado que deja por debajo el 90 % de la muestra)."""
    if not tiempos:
        raise ValueError("p90 de una muestra vacía")
    orden = sorted(float(t) for t in tiempos)
    return orden[max(math.ceil(PERCENTIL_N0 * len(orden)) - 1, 0)]


def _fecha_hora(valor, zona, que: str) -> pd.Timestamp:
    """Un instante con fecha y hora: un `datetime` o `Timestamp`, o un texto AAAA-MM-DDThh:mm[:ss][zona]. Sin zona, la del
    bloque. Lo demás (una fecha sola, NaT, otro tipo) se rechaza. r02: los nanosegundos se truncan a microsegundos (H-04: no
    caben en el texto que se guarda) y, sin zona, una hora que no existe o que se repite por el cambio de hora se rechaza (H-05:
    no se sabe cuál es). Lo que sale siempre se puede volver a leer (`isoformat` cumple `RE_FECHA_HORA`)."""
    if isinstance(valor, str):
        if not RE_FECHA_HORA.fullmatch(valor):
            raise PeticionInvalida(f"{que} {valor!r} no es AAAA-MM-DDThh:mm")
        try:
            valor = dt.datetime.fromisoformat(valor)
        except ValueError:
            raise PeticionInvalida(f"{que} {valor!r} no es una fecha-hora") from None
    if not isinstance(valor, dt.datetime) or pd.isna(valor):
        raise PeticionInvalida(f"{que} {valor!r} no es una fecha-hora")
    if getattr(valor, "nanosecond", 0):   # H-04: se truncan a microsegundos, de forma explícita (el texto guardado no los admite)
        valor = pd.Timestamp(valor).floor("us")
    if valor.tzinfo is None:
        d = valor.to_pydatetime() if isinstance(valor, pd.Timestamp) else valor
        cero, uno = d.replace(tzinfo=zona, fold=0), d.replace(tzinfo=zona, fold=1)
        if cero.utcoffset() != uno.utcoffset():   # hueco o solape del cambio de hora en la zona del bloque
            raise PeticionInvalida(f"{que} {valor!r} es una hora inexistente o ambigua en la zona del bloque; indique la zona")
        t = pd.Timestamp(cero)
    else:
        t = pd.Timestamp(valor).tz_convert(zona)
    if not RE_FECHA_HORA.fullmatch(t.isoformat()):   # lo que se guarda tiene que poder leerse otra vez
        raise PeticionInvalida(f"{que} {valor!r} no se puede guardar como AAAA-MM-DDThh:mm:ss")
    return t


class ColaPeticiones:
    def __init__(self, bloque) -> None:
        self.bloque = bloque
        self.almacen = bloque.almacen
        self.cfg = bloque.cfg

    # ------------------------------------------------------------------ parámetros y prioridad
    def _instante(self, valor) -> pd.Timestamp:
        return _fecha_hora(valor, self.bloque.reloj.zona, "instante")

    def _prioridad_de_consulta(self, urgencia: str) -> str:
        mapa = parametro(self.cfg, "cola_peticiones.prioridad_consulta")
        if urgencia not in mapa or mapa[urgencia] not in PRIORIDADES:
            raise PeticionInvalida(f"urgencia {urgencia!r} sin prioridad en `cola_peticiones.prioridad_consulta`")
        return mapa[urgencia]

    def prioridad(self, pet: dict, instante) -> dict[str, Any]:
        """Componentes de la prioridad efectiva de una petición en un instante. Un instante anterior a su recepción se
        rechaza: la espera no puede ser negativa."""
        t = self._instante(instante)
        recibida = self._instante(pet["recibida"])
        espera_h = (t - recibida).total_seconds() / 3600
        if espera_h < 0:
            raise PeticionInvalida(f"{pet['id']}: el instante {t.isoformat()} es anterior a su recepción ({pet['recibida']})")
        base = float(parametro(self.cfg, f"cola_peticiones.prioridad_base.{pet['prioridad']}"))
        envejecimiento = min(math.floor(espera_h) * float(parametro(self.cfg, "cola_peticiones.envejecimiento_por_hora")),
                             float(parametro(self.cfg, "cola_peticiones.envejecimiento_max")))
        urgencia = 0.0
        if pet.get("fecha_objetivo"):
            margen_h = (self._instante(pet["fecha_objetivo"]) - t).total_seconds() / 3600
            if margen_h < float(parametro(self.cfg, "cola_peticiones.urgencia_margen_h")):
                urgencia = float(parametro(self.cfg, "cola_peticiones.urgencia_puntos"))
        return {"base": base, "envejecimiento": envejecimiento, "urgencia": urgencia,
                "efectiva": base + envejecimiento + urgencia, "espera_h": round(espera_h, 4)}

    def _ordenar(self, pets: list[dict], t: pd.Timestamp) -> list[dict]:
        con = [{**p, "_prioridad": self.prioridad(p, t)} for p in pets]
        return sorted(con, key=lambda p: (-p["_prioridad"]["efectiva"], NIVELES.index(p["nivel"]),
                                          self._instante(p["recibida"]), p["_llegada"]))

    def _en_cola(self, estados=("ENCOLADA",), hasta: pd.Timestamp | None = None) -> list[dict]:
        """Las PET- en esos estados; con `hasta`, solo las ya recibidas en ese instante (r02, H-01 y H-02: una posterior aún
        no había llegado). Una `recibida` que no es una fecha-hora falla cerrado."""
        salida = []
        for pid, e in self.almacen.estado("F5").items():
            if e.get("tipo_entrada") == "PETICION" and e.get("estado") in estados:
                if hasta is not None and self._instante(e.get("recibida")) > hasta:
                    continue
                salida.append({**e, "id": pid, "_llegada": e["_historial"][0]["seq"]})
        return salida

    def orden(self, instante) -> list[dict]:
        """Las peticiones ENCOLADAS ya recibidas en `instante`, en orden de servicio, cada una con su prioridad efectiva
        (`_prioridad`). Las recibidas después no se ven todavía (r02, H-01)."""
        t = self._instante(instante)
        return self._ordenar(self._en_cola(hasta=t), t)

    def _plazo(self, nueva: dict, t: pd.Timestamp) -> dict[str, Any]:
        """Lo que se comunica al recibir: la posición que toma en la cola en ese instante, las UC por delante y el texto. Solo
        cuentan las recibidas hasta `t`: una petición recibida después nunca hace fallar esta (r02, H-02)."""
        orden = self._ordenar(self._en_cola(hasta=t) + [nueva], t)
        k = next(i for i, p in enumerate(orden) if p["id"] == nueva["id"])
        delante = round(sum(float(p["presupuesto_uc"]) for p in orden[:k]), 6)
        texto = (f"En cola: posición {k + 1} de {len(orden)}, con {delante:g} UC por delante; se atiende por prioridad con "
                 "envejecimiento, sin límite de peticiones")
        if nueva.get("fecha_objetivo"):
            texto += f"; fecha objetivo {nueva['fecha_objetivo']}"
        return {"posicion": k + 1, "en_cola": len(orden), "uc_por_delante": delante, "prioridad": orden[k]["_prioridad"],
                "plazo_estimado": texto}

    # ------------------------------------------------------------------ recepción
    def _validar_ct01(self, ct01: dict) -> dict[str, Any]:
        if not isinstance(ct01, dict):
            raise PeticionInvalida("CT-01: el cuerpo no es un objeto")
        tipo, prioridad = ct01.get("tipo"), ct01.get("prioridad")
        if tipo not in TIPOS_CT01:
            raise PeticionInvalida(f"CT-01: tipo {tipo!r} fuera de {'|'.join(TIPOS_CT01)}")
        if prioridad not in PRIORIDADES:
            raise PeticionInvalida(f"CT-01: prioridad {prioridad!r} fuera de {'|'.join(PRIORIDADES)}")
        forzado = ct01.get("nivel_forzado")
        if forzado is not None and forzado not in NIVELES:
            raise PeticionInvalida(f"CT-01: nivel_forzado {forzado!r} fuera de {'|'.join(NIVELES)} (N0 es una consulta CT-03)")
        alcance = ct01.get("alcance")
        if not isinstance(alcance, dict):
            raise PeticionInvalida("CT-01: alcance no es un objeto")
        fo = ct01.get("fecha_objetivo")
        fecha_objetivo = None if fo is None else _fecha_hora(fo, self.bloque.reloj.zona, "fecha_objetivo").isoformat()
        tipo = "AD_HOC" if tipo == "PERIODICO" else tipo   # como `Bloque.peticion`: el periódico lo dispara HT-05
        nivel = forzado or ("N3" if tipo == "PROFUNDIZACION" else "N2")   # la regla de `Bloque.ciclo`
        return {"tipo": tipo, "prioridad": prioridad, "nivel_forzado": forzado, "nivel": nivel, "alcance": alcance,
                "horizontes": ct01.get("horizontes"), "fecha_objetivo": fecha_objetivo}

    def _clases(self, alcance: dict, as_of) -> list[str]:
        activas = list(self.bloque.f10(as_of).get("P-02") or perfiles_activos(self.cfg))
        return [c for c in (alcance.get("clases") or activas) if c in activas]   # las que el ciclo analizará

    def _nueva(self, pet_id: str, datos: dict, t: pd.Timestamp, exigir_clases: bool = False) -> dict[str, Any]:
        clases = self._clases(datos["alcance"], t.date())
        if exigir_clases and not clases:   # r02 (H-07): sin nada que analizar no hay presupuesto proporcional
            raise PeticionInvalida(f"CT-01: el alcance {datos['alcance'].get('clases')!r} no tiene ninguna clase activa")
        pres = presupuesto_por_clase(self.cfg, datos["tipo"], clases, {c: datos["nivel"] for c in clases})
        return {"tipo_entrada": "PETICION", "id": pet_id, "estado": "ENCOLADA", "recibida": t.isoformat(), **datos,
                "clases": clases, "presupuesto_por_clase": pres, "presupuesto_uc": round(sum(pres.values()), 6),
                "_llegada": math.inf}

    def _registrar(self, nueva: dict, t: pd.Timestamp, **origen) -> dict[str, Any]:
        """Escribe la PET- ENCOLADA con su plazo; la posición y la escritura, sin otra recepción en medio."""
        with self.almacen._transaccion():
            plazo = self._plazo(nueva, t)
            entrada = {k: v for k, v in nueva.items() if not k.startswith("_")}
            self.almacen.escribir("F5", "AG-01", {**entrada, **origen, "plazo_comunicado": plazo["plazo_estimado"]})
        return plazo

    def recibir(self, ct01: dict, instante) -> dict[str, Any]:
        """CT-01 del Broker a la cola: nunca se rechaza por número. Devuelve la PET- y el acuse con nivel, presupuesto,
        posición y plazo. El mismo `msg_id` del Broker no duplica la petición (idempotencia de la mensajería)."""
        t = self._instante(instante)
        datos = self._validar_ct01(ct01)   # antes de tocar nada
        # r02 (H-02, H-04, H-07): todo lo que puede fallar, antes de crear el mensaje y de reservar su msg_id: las clases
        # activas, el presupuesto y la prioridad (la configuración); dentro de la reserva solo quedan el id y la escritura
        previa = self._nueva("PET-?", datos, t, exigir_clases=True)
        self.prioridad(previa, t)
        self.bloque.fijar_fecha(t.tz_localize(None).normalize())
        msg = self.bloque.mensajeria.crear("CT-01", "BROKER", "AG-01", ct01)

        def _proc(m):
            pet_id = self.almacen.nuevo_id("PET")
            nueva = {**previa, "id": pet_id}
            plazo = self._registrar(nueva, t, origen="CT-01", msg_id=m["msg_id"])
            return {"pet_id": pet_id, "estado": "ENCOLADA", "nivel": datos["nivel"], "clases": nueva["clases"],
                    "presupuesto_por_clase": nueva["presupuesto_por_clase"], "presupuesto_uc": nueva["presupuesto_uc"],
                    "cola": plazo}

        res, repetido = self.bloque.mensajeria.procesar_una_vez(msg, _proc)
        acuse = self.bloque.mensajeria.acuse(msg, res["pet_id"], nivel=res["nivel"], presupuesto_uc=res["presupuesto_uc"],
                                             cola={k: res["cola"][k] for k in ("posicion", "en_cola", "uc_por_delante",
                                                                               "plazo_estimado")},
                                             repetido=repetido)
        return {**res, "acuse": acuse}

    def plazo_consulta(self, pet_id: str, nivel: str | None, alcance: dict, urgencia: str, instante) -> dict[str, Any]:
        """La PET- (sin escribirla) del análisis escalado de una consulta y el plazo que se comunica en su provisional."""
        t = self._instante(instante)
        if nivel not in NIVELES:
            raise PeticionInvalida(f"escalado con nivel {nivel!r} fuera de {'|'.join(NIVELES)}")
        datos = {"tipo": "AD_HOC", "prioridad": self._prioridad_de_consulta(urgencia), "nivel_forzado": nivel,
                 "nivel": nivel, "alcance": dict(alcance), "horizontes": None, "fecha_objetivo": None}
        nueva = self._nueva(pet_id, datos, t)
        return {"nueva": nueva, "plazo": self._plazo(nueva, t)}

    def encolar_consulta(self, nueva: dict, qry_id: str, msg_id: str, instante) -> dict[str, Any]:
        """Escribe la PET- del análisis escalado de la consulta `qry_id` (después de su QRY- y de su provisional, para que la
        petición siempre tenga a quién responder)."""
        return self._registrar(nueva, self._instante(instante), origen="CT-03", qry_id=qry_id, msg_id=msg_id)

    # ------------------------------------------------------------------ servicio
    def _clave(self, pet_id: str) -> tuple[str, str]:
        return (str(self.almacen.carpeta.resolve()), pet_id)

    def _tomar(self, t: pd.Timestamp, k: int, en_marcha: bool = False) -> dict | None:
        """La siguiente petición en orden de servicio pasa a EN_CURSO, con el proceso que la toma (r02, H-03); leer y escribir
        en una sola sección crítica. Con `en_marcha`, queda anotada como servida ahora por este proceso."""
        with self.almacen._transaccion():
            orden = self.orden(t)
            if not orden:
                return None
            pet = orden[0]
            self.almacen.escribir("F5", "AG-01", {"tipo_entrada": "PETICION", "id": pet["id"], "estado": "EN_CURSO",
                                                  "inicio": t.isoformat(), "prioridad_al_servir": pet["_prioridad"],
                                                  "orden_servicio": k, **_proceso()})
            if en_marcha:
                with _EN_MARCHA_LOCK:
                    _EN_MARCHA.add(self._clave(pet["id"]))
            return {**pet, "orden_servicio": k}

    def tomar(self, instante) -> dict | None:
        """Toma la siguiente petición (EN_CURSO) sin servirla; None si la cola está vacía. r02 (H-06): lo tomado se sirve con
        `servir`; si no, `atender` no lo toca y queda como huérfana (incidencia, `huerfanas`)."""
        return self._tomar(self._instante(instante), 1)

    def servir(self, pet: dict, instante) -> dict[str, Any]:
        """Sirve una petición tomada con `tomar` (EN_CURSO, de este proceso)."""
        t = self._instante(instante)
        actual = self.almacen.estado("F5").get(pet.get("id")) or {}
        if actual.get("tipo_entrada") != "PETICION" or actual.get("estado") != "EN_CURSO" or actual.get("pid") != os.getpid():
            raise PeticionInvalida(f"{pet.get('id')}: solo se sirve una petición EN_CURSO tomada por este proceso")
        with _EN_MARCHA_LOCK:
            _EN_MARCHA.add(self._clave(pet["id"]))
        return self._servir(pet, t)

    def atender(self, instante, maximo: int | None = None) -> list[dict]:
        """Sirve las peticiones ENCOLADAS en orden de servicio (como mucho `maximo`), una detrás de otra. `instante` es un
        instante fijo o un reloj (sin argumentos, devuelve el instante): con un reloj, cada toma usa un instante nuevo y se
        sirven en la misma pasada las que llegan mientras tanto (r02, H-01). Antes, avisa de las huérfanas (`huerfanas`)."""
        if maximo is not None and (isinstance(maximo, bool) or not isinstance(maximo, int) or maximo < 1):
            raise PeticionInvalida(f"maximo {maximo!r} no es un entero ≥ 1")
        reloj = instante if callable(instante) else (lambda: instante)
        previo = self._instante(reloj())   # valida antes de nada
        self.huerfanas()
        servidas: list[dict] = []
        while maximo is None or len(servidas) < maximo:
            t = self._instante(reloj())
            if t < previo:   # r03 (QA r02, N-02): un reloj que retrocede no vería lo ya recibido; falla cerrado
                raise PeticionInvalida(f"el reloj retrocede: {t.isoformat()} es anterior a {previo.isoformat()}")
            previo = t
            self.bloque.fijar_fecha(t.tz_localize(None).normalize())   # r02: lo que se escribe en F5 es del día de la toma
            pet = self._tomar(t, len(servidas) + 1, en_marcha=True)
            if pet is None:
                break
            servidas.append(self._servir(pet, t))
        return servidas

    def _es_huerfana(self, pet_id: str, e: dict) -> bool:
        """Una EN_CURSO de este host cuyo proceso ya no vive, o de este proceso sin servirse ahora. De otro host o sin `pid`
        (anteriores a la r02) no se sabe: no lo es."""
        if e.get("estado") != "EN_CURSO" or e.get("host") != _proceso()["host"]:
            return False
        if e.get("pid") == os.getpid():
            with _EN_MARCHA_LOCK:
                return self._clave(pet_id) not in _EN_MARCHA
        return _pid_vivo(e.get("pid")) is False

    def huerfanas(self) -> list[str]:
        """r02 (H-03): las PET- EN_CURSO cuyo proceso ya no las sirve. Por cada una deja, una sola vez, una incidencia Operativa
        en HA (`peticion_huerfana`), sin tocar su estado (falla cerrado: no se sabe qué dejó hecho el ciclo); el operador la
        cierra con `reconciliar`. Mientras tanto, la final de su consulta no sale."""
        avisadas = {e.get("peticion_huerfana") for e in self.almacen.leer("HA") if e.get("peticion_huerfana")}
        salida = []
        for pid, e in self.almacen.estado("F5").items():
            if e.get("tipo_entrada") != "PETICION" or not self._es_huerfana(pid, e):
                continue
            salida.append(pid)
            if pid not in avisadas:
                self.almacen.incidencia("OTRO", f"Petición {pid} EN_CURSO huérfana (su proceso ya no la sirve)", "AG-01",
                                        severidad="Operativa", peticion_huerfana=pid,
                                        tratamiento="sin tocar (falla cerrado); revisar F5 y cerrarla con "
                                                    "`bloque-a reconciliar-peticion PET-… --fallida`")
        return sorted(salida)

    def reconciliar(self, pet_id: str, motivo: str, instante=None) -> dict[str, Any]:
        """r02 (H-03): una PET- huérfana pasa a FALLIDA (como `reconciliar-mensaje`): primero el rastro en HA, después el
        escalado FALLIDO de su consulta, la FALLIDA y la final FALLIDO. Solo una huérfana; nunca una que se está sirviendo."""
        if not isinstance(motivo, str) or not motivo.strip():
            raise PeticionInvalida("La reconciliación exige un motivo")
        fin = self._instante(instante if instante is not None else pd.Timestamp.now(tz=self.bloque.reloj.zona).floor("s"))
        self.bloque.fijar_fecha(fin.tz_localize(None).normalize())   # la FALLIDA y la final, del día de la reconciliación
        with self.almacen._transaccion():
            e = self.almacen.estado("F5").get(pet_id) or {}
            if e.get("tipo_entrada") != "PETICION" or not self._es_huerfana(pet_id, e):
                raise PeticionInvalida(f"{pet_id} no es una petición EN_CURSO huérfana que reconciliar")
            self.almacen.incidencia("OTRO", f"Petición {pet_id} huérfana cerrada como FALLIDA por el operador: {motivo.strip()}",
                                    "AG-01", severidad="Operativa", tratamiento="reconciliación manual de la cola (FALLIDA)")
            pet = {**e, "id": pet_id}
            self._cerrar_fallida(pet, ERROR_HUERFANA, fin, reconciliada=motivo.strip())
        final = None
        if pet["origen"] == "CT-03":
            final = respuesta_final.enviar(self.bloque, pet["qry_id"], None, fin.tz_localize(None).normalize())
        return {"pet_id": pet_id, "estado": "FALLIDA", "run_id": self.almacen.estado("F5")[pet_id].get("run_id"),
                "respuesta_final": final}

    def _run_de(self, pet_id: str) -> str | None:
        return next((x["id"] for x in reversed(self.almacen.leer("F5")) if x.get("tipo_entrada") == "RUN"
                     and (x.get("disparador") or {}).get("pet_id") == pet_id), None)

    def _servir(self, pet: dict, t: pd.Timestamp) -> dict[str, Any]:
        """r03 (QA r02, N-01): la PET- sigue «en marcha» (no huérfana) hasta que deja de estar EN_CURSO: después de la
        ATENDIDA y de la final, o de la FALLIDA."""
        try:
            return self._servir_en_marcha(pet, t)
        finally:
            with _EN_MARCHA_LOCK:
                _EN_MARCHA.discard(self._clave(pet["id"]))

    def _servir_en_marcha(self, pet: dict, t: pd.Timestamp) -> dict[str, Any]:
        disparador = {"origen": pet["origen"], "msg_id": pet["msg_id"], "pet_id": pet["id"]}
        if pet["origen"] == "CT-03":
            disparador["qry_id"] = pet["qry_id"]
        try:
            res = self.bloque.ciclo(t, tipo=pet["tipo"], alcance=pet["alcance"], nivel_forzado=pet["nivel_forzado"],
                                    horizontes=pet["horizontes"], disparador=disparador, prioridad=pet["prioridad"])
        except BaseException as e:   # se registra y se relanza: nada se absorbe
            self._fallida(pet, type(e).__name__, t)
            raise
        servida = {"pet_id": pet["id"], "origen": pet["origen"], "run_id": res["run_id"], "estado_run": res["estado"],
                   "orden_servicio": pet["orden_servicio"], "prioridad": pet["_prioridad"]}
        if pet["origen"] == "CT-03":   # primero el escalado de la QRY-, después ATENDIDA y la final (que ya no está en cola)
            self._escalado(pet["qry_id"], res["run_id"], res["estado"])
        self.almacen.escribir("F5", "AG-01", {"tipo_entrada": "PETICION", "id": pet["id"], "estado": "ATENDIDA",
                                              "run_id": res["run_id"], "estado_run": res["estado"]})
        if pet["origen"] == "CT-03":
            servida["respuesta_final"] = respuesta_final.enviar(self.bloque, pet["qry_id"], None, t.tz_localize(None).normalize())
        return servida

    def _escalado(self, qry_id: str, run_id: str | None, estado_run: str, fallo: str | None = None) -> None:
        qry = self.almacen.estado("F5")[qry_id]
        escalado = {**qry["escalado"], "run_id": run_id, "estado_run": estado_run}
        self.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": qry_id, "escalado": escalado,
                                              **({"fallo_analisis": fallo} if fallo else {})})

    def _fallida(self, pet: dict, error: str, t: pd.Timestamp) -> None:
        """Una petición cuyo ciclo falló: FALLIDA con la clase del error (no su texto, R8) e incidencia; si es de una
        consulta, su escalado queda FALLIDO y la final FALLIDO la envía `respuesta_final.enviar_pendientes`."""
        self.almacen.incidencia("HERRAMIENTA", f"La petición {pet['id']} de la cola falló al atenderse ({error})", "AG-01",
                                severidad="Operativa")
        self._cerrar_fallida(pet, error, t)

    def _cerrar_fallida(self, pet: dict, error: str, t: pd.Timestamp, **extra) -> None:
        run_id = self._run_de(pet["id"])
        if pet["origen"] == "CT-03":
            self._escalado(pet["qry_id"], run_id, "FALLIDO", error)
        self.almacen.escribir("F5", "AG-01", {"tipo_entrada": "PETICION", "id": pet["id"], "estado": "FALLIDA",
                                              "error": error, "run_id": run_id, "fin": t.isoformat(), **extra})

