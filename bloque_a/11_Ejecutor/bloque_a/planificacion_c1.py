"""T-197 (PB-09) · HT-05 dispara el ciclo C1 según el P-01 de F10 (Documento 0 V5.3, 7.1 y 7.4; especificación de HT-05,
`bloque_a/10_Herramientas/ht05_planificador_ejemplo.md`, §4 y §5).

- El calendario es el P-01 vigente en cada fecha (F10, por su `fecha_efecto`): un cambio del Broker por CT-04 surte efecto
  desde el siguiente disparo y nunca a mitad de un RUN- (§5.5); el RUN- disparado lleva en su `disparador` el P-01 y el CFG-
  con que empezó.
- Idempotencia (§5.1): cada disparo es `C1-EJEC-<fecha programada ISO>` y queda en F5 (AG-01) antes de abrir el RUN-; un
  segundo disparo con el mismo identificador se descarta, también desde otro proceso (la reserva va en una transacción del
  almacén).
- Disparos perdidos (§5.2): solo el último C1 programado cuenta; se ejecuta una vez si su entrega no venció en más de
  `planificador.recuperacion_disparo_perdido_h` horas, y si no, queda en F5 como PERDIDO, sin ejecutar. Nunca se acumulan.
- Disparo huérfano (r02, H-02): la reserva guarda el `pid` del proceso que dispara; si ese proceso ya no vive y el disparo
  no se cerró, se cierra una vez como FALLIDO con una incidencia Operativa en HA, sin repetir el C1; si vive, EN_CURSO.
  Ronda de cierre (H-07): «vive» exige además el mismo arranque de la máquina (`boot_id`) y la misma hora de arranque del
  proceso que se guardaron en la reserva, y, si el pid es el propio, que este proceso la abriera (un pid reutilizado tras un
  reinicio no deja el disparo EN_CURSO para siempre). H-08: el cierre se lee como el de un ciclo cortado (`estado_run`).
Decisiones que el diseño no fija, en INC-T197-01.
"""
from __future__ import annotations

import datetime as dt
import os

import pandas as pd

from .configuracion import parametro
from .herramientas import ht05_planificador as ht05
from .interfaz_broker import _pid_vivo

ID_DISPARO = "C1-EJEC"
ESTADOS_DISPARADOS = ("EMITIDO", "RECUPERADO")
RUTA_BOOT_ID = "/proc/sys/kernel/random/boot_id"
_ABIERTOS: set[str] = set()   # disparos que este proceso tiene abiertos (reserva escrita, ciclo sin cerrar)


def _leer(ruta: str) -> str | None:
    try:
        with open(ruta, encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, ProcessLookupError):   # fuera de Linux, o el proceso ya no existe
        return None


def identidad_proceso(pid: int) -> dict:
    """`boot_id` de la máquina y hora de arranque del proceso (campo 22 de /proc/<pid>/stat, en tics desde el arranque);
    None si no se pueden leer."""
    boot = _leer(RUTA_BOOT_ID)
    stat = _leer(f"/proc/{pid}/stat")
    arranque = None
    if stat and ")" in stat:
        campos = stat.rsplit(")", 1)[1].split()
        arranque = int(campos[19]) if len(campos) > 19 and campos[19].isdigit() else None   # campo 22 (desde el 3.º)
    return {"boot_id": boot.strip() if boot else None, "arranque_proceso": arranque}


def _vive(previo: dict) -> bool | None:
    """True si el proceso que abrió el disparo sigue vivo; False si no; None si no se puede saber (r02 H-02, cierre H-07)."""
    pid = previo.get("pid")
    if pid == os.getpid():
        return previo.get("id") in _ABIERTOS   # el pid propio cuenta solo si este proceso abrió ese disparo
    vivo = _pid_vivo(pid)
    if vivo is not True or not isinstance(pid, int):   # _pid_vivo solo da True con un pid entero
        return vivo
    ahora = identidad_proceso(pid)
    guardada = {k: previo.get(k) for k in ("boot_id", "arranque_proceso")}
    if None in ahora.values() or None in guardada.values():
        return None
    return ahora == guardada   # otro arranque o la hora de arranque de otro proceso: el pid lo reutiliza otro


def _ahora(ahora) -> dt.datetime:
    """Instante local sin zona (la del usuario, la del reloj del bloque), al minuto."""
    t = pd.Timestamp(ahora)
    if t.tzinfo is not None:
        raise ValueError("el instante del planificador va en la hora local del usuario, sin zona")
    return t.to_pydatetime().replace(second=0, microsecond=0)


def _p01_en(bloque, conocido: dt.datetime, dia: dt.date) -> dict:
    """El P-01 que rige el `dia` con lo que F10 sabe en `conocido`: valor, CFG- que lo fijó y desde cuándo rige."""
    est = bloque.almacen.estado("F10", str(conocido.date()), efectivo_el=str(dia)).get("P-01")
    if not est or not est.get("valor_vigente"):
        raise ht05.P01Invalido("F10 no tiene P-01: HT-05 no programa el C1")
    periodicidad, ejecucion, entrega = ht05.leer_p01(est["valor_vigente"])
    if ejecucion is None:   # P-01 de dos partes (CT-04 anterior a T-197): la ejecución se deduce de la entrega (§4)
        ejecucion = ht05.ejecucion_para_entrega(periodicidad, entrega, parametro(bloque.cfg, "planificador"))
    inicio = dt.date.fromisoformat(str(est.get("fecha_efecto") or est["_historial"][0]["fecha"])[:10])
    # r02 (H-01): la quincena sigue el ancla guardada en F10, que un cambio de hora o de día de la entrega no mueve
    ancla = est.get("semana_ancla_quincenal") if periodicidad == "QUINCENAL" else None
    return {"valor": est["valor_vigente"], "cfg_id": est.get("cfg_id"), "periodicidad": periodicidad, "ejecucion": ejecucion,
            "entrega": entrega, "inicio": inicio, "ancla": dt.date.fromisoformat(ancla) if ancla else None}


def _fechas_de_cambio(bloque, conocido: dt.datetime) -> list[dt.date]:
    return sorted({dt.date.fromisoformat(e["fecha_efecto"][:10]) for e in bloque.almacen.leer("F10", str(conocido.date()))
                   if e.get("param_id") == "P-01" and e.get("fecha_efecto")})


def _programa(p: dict, ejecucion: dt.datetime) -> dict:
    entrega = ht05.entrega_de(ejecucion, p["periodicidad"], p["entrega"])
    return {"disparo_id": f"{ID_DISPARO}-{ejecucion.isoformat(timespec='minutes')}", "programado": ejecucion.isoformat(timespec="minutes"),
            "entrega": entrega.isoformat(timespec="minutes"), "p01": p["valor"], "cfg_id": p["cfg_id"]}


def proximo(bloque, ahora) -> dict:
    """El siguiente C1 programado después de `ahora`, con los cambios de P-01 ya conocidos que rijan para entonces."""
    t = _ahora(ahora)
    cambios = _fechas_de_cambio(bloque, t)
    desde, dia = t, t.date()
    for _ in range(len(cambios) + 1):
        p = _p01_en(bloque, t, dia)
        c = ht05.siguiente_ejecucion(desde, p["periodicidad"], p["ejecucion"], p["inicio"], p["ancla"])
        cambio = next((f for f in cambios if dia < f <= c.date()), None)
        if cambio is None:
            return _programa(p, c)
        desde, dia = dt.datetime.combine(cambio, dt.time()) - dt.timedelta(minutes=1), cambio
    raise ht05.P01Invalido("HT-05 no resuelve el siguiente C1 con los cambios de P-01")   # pragma: no cover - cota del bucle


def ultimo_programado(bloque, ahora) -> dict | None:
    """El último C1 programado en o antes de `ahora` (con el P-01 que regía su fecha); None si no hubo ninguno."""
    t = _ahora(ahora)
    hasta, dia = t, t.date()
    for _ in range(len(_fechas_de_cambio(bloque, t)) + 2):
        p = _p01_en(bloque, t, dia)
        c = ht05.ultima_ejecucion(hasta, p["periodicidad"], p["ejecucion"], p["inicio"], p["ancla"])
        if c is not None:
            return _programa(p, c)
        anterior = p["inicio"] - dt.timedelta(days=1)
        if bloque.almacen.estado("F10", str(t.date()), efectivo_el=str(anterior)).get("P-01") is None:
            return None
        hasta, dia = dt.datetime.combine(p["inicio"], dt.time()) - dt.timedelta(minutes=1), anterior
    return None


def _disparo_registrado(bloque, disparo_id: str) -> dict | None:
    return bloque.almacen.estado("F5", clave="id").get(disparo_id)


def _previo(bloque, previo: dict, ahora: str) -> dict:
    """Lo que dice un sondeo de un disparo ya reservado (r02, H-02). Cerrado (`estado_run`, PERDIDO o huérfano ya cerrado):
    duplicado. Abierto y con su proceso vivo: EN_CURSO, sin escribir. Abierto y con su proceso muerto (OOM, kill -9, corte):
    se cierra una sola vez como FALLIDO, con una incidencia Operativa en HA, y el C1 no se repite (lo lanza el operador)."""
    abierto = previo.get("estado") in ESTADOS_DISPARADOS and previo.get("estado_run") is None
    if not abierto:
        return {"estado": "DESCARTADO_DUPLICADO", "registrado": previo.get("estado"), "estado_run": previo.get("estado_run")}
    vivo = _vive(previo)
    if vivo is False:   # cierre H-08: se lee igual que un ciclo cortado (`estado_run` FALLIDO), con el motivo arriba
        bloque.almacen.escribir("F5", "AG-01", {"tipo_entrada": "DISPARO", "id": previo["id"], "estado_run": "FALLIDO",
                                                "motivo_cierre": "proceso terminado", "cierre_huerfano": {
            "pid": previo.get("pid"), "fecha_cierre": ahora}})
        bloque.almacen.incidencia("HERRAMIENTA", f"Disparo {previo['id']} huérfano: el proceso que abrió el C1 terminó sin "
                                  "cerrarlo", "HT-05", severidad="Operativa",
                                  tratamiento="C1 sin repetir (falla cerrado); el operador lo lanza con `ciclo`",
                                  disparo_huerfano=previo["id"])
        return {"estado": "FALLIDO", "motivo": "proceso terminado", "registrado": previo.get("estado")}
    if vivo is True:
        return {"estado": "EN_CURSO", "registrado": previo.get("estado")}
    return {"estado": "DESCARTADO_DUPLICADO", "registrado": previo.get("estado")}   # sin pid o sin forma de saberlo


def disparar(bloque, ahora, ejecutar: bool = True) -> dict:
    """Comprueba el C1 vencido y, con `ejecutar`, lo dispara una sola vez. Devuelve el disparo, su estado y el siguiente C1."""
    t = _ahora(ahora)
    cfg = parametro(bloque.cfg, "planificador")
    margen = dt.timedelta(hours=int(cfg["recuperacion_disparo_perdido_h"]))
    bloque.fijar_fecha(t)
    salida: dict = {"ahora": t.isoformat(timespec="minutes"), "proximo": proximo(bloque, t)}
    with bloque.almacen._transaccion():
        prog = ultimo_programado(bloque, t)
        if prog is None:
            return {**salida, "disparo": None, "estado": "SIN_DISPARO"}
        previo = _disparo_registrado(bloque, prog["disparo_id"])
        if previo is not None:
            return {**salida, "disparo": prog, **_previo(bloque, previo, salida["ahora"])}
        entrega = dt.datetime.fromisoformat(prog["entrega"])
        estado = "PERDIDO" if t > entrega + margen else ("RECUPERADO" if t >= entrega else "EMITIDO")
        if not ejecutar:
            return {**salida, "disparo": prog, "estado": "PENDIENTE" if estado != "PERDIDO" else "PERDIDO_SIN_REGISTRAR"}
        bloque.almacen.escribir("F5", "AG-01", {"tipo_entrada": "DISPARO", "id": prog["disparo_id"], "ciclo": "C1", "origen": "HT-05",
                                                "fecha_disparo": salida["ahora"], **{k: prog[k] for k in ("programado", "entrega", "p01", "cfg_id")},
                                                "estado": estado, "run_id": None, "pid": os.getpid(), **identidad_proceso(os.getpid())})
        if estado != "PERDIDO":
            _ABIERTOS.add(prog["disparo_id"])
    if estado == "PERDIDO":
        return {**salida, "disparo": prog, "estado": estado, "run_id": None}
    disparador = {"origen": "HT-05", "disparo_id": prog["disparo_id"], "programado": prog["programado"], "p01": prog["p01"],
                  "cfg_id": prog["cfg_id"]}
    res: dict | None = None
    try:
        res = bloque.ciclo(pd.Timestamp(t), disparador=disparador)
    finally:
        # falla cerrado: si el ciclo se corta, el disparo queda FALLIDO y no se repite solo (§5.1); el operador lanza `ciclo`
        bloque.almacen.escribir("F5", "AG-01", {"tipo_entrada": "DISPARO", "id": prog["disparo_id"],
                                                "run_id": res["run_id"] if res else None,
                                                "estado_run": res["estado"] if res else "FALLIDO"})
        _ABIERTOS.discard(prog["disparo_id"])
    return {**salida, "disparo": prog, "estado": estado, "run_id": res["run_id"], "estado_run": res["estado"]}
