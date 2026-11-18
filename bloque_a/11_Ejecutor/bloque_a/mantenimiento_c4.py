"""Mantenimiento C4 del Buscador de Fuentes Avanzadas (AG-16): revisión de las credenciales de sus fuentes de pago y API
(T-177, PB-58; Documento 0 óptima V5.3, 7.10.1 y tabla del ciclo C4; prompt del BFA, 5.4, fila «Mensual (V5.1)»).

Paso 1 (7.10.1): el ejecutor da al BFA el estado en la bóveda de HT-01 (alias y estado; nunca el valor) de los servicios
que tiene declarados en `credenciales.servicios_bfa`, y el BFA devuelve con su retorno `solicitudes_credenciales`
(servicio, motivo, impacto si falta). Paso 2 (7.10.2): el Coordinador (AG-01) las lee con `Credenciales.desde_retorno`,
que deduplica, comprueba en HT-01 que faltan de verdad y emite el CT-25. Lo resuelto queda en F5 (entrada
`C4_CREDENCIALES`, C4-), sin valores.

El retorno del BFA no pasa por la mensajería (como el de CT-07): CT-25 solo existe entre el Coordinador y el Broker.
El ciclo C4 lo lanza el planificador (`bloque-a credencial c4`); no se llama desde el ciclo C1 (los C4 nunca bloquean
C1–C3, sección 7 del Documento 0).
"""
from __future__ import annotations

import os

import pandas as pd

from .configuracion import parametro
from .consumo import Presupuesto
from .herramientas.ht01_boveda import alias_de
from .herramientas.ht05_planificador import FRECUENCIAS

_SEMANA = FRECUENCIAS["semanal"]   # HT-05: una semana, en días
if not isinstance(_SEMANA, int):
    raise TypeError("HT-05: la frecuencia semanal debe ser un número de días")
DIAS_SEMANA: int = _SEMANA
AGENTE_BFA = "AG-16"
BOLSA_C4 = "C4"
INSTRUCCION_C4 = (
    "Mantenimiento C4 (5.4, revisión mensual de credenciales): revisa el estado en la bóveda de HT-01 de las credenciales "
    "de tus fuentes de pago y API (en `servicios`, solo alias y estado). Por cada una que falte (AUSENTE, CADUCADA o "
    "REVOCADA) y siga siendo necesaria, devuelve en `solicitudes_credenciales` un objeto {servicio, motivo, "
    "impacto_si_falta, urgencia: ALTA|NORMAL}, sin ningún valor de credencial. `referencias` va vacío; `sintesis` dice qué "
    "has revisado y `lagunas`, lo que trabajarás degradado mientras falte.")


def servicios_bfa(cfg: dict) -> list[dict]:
    """Servicios de pago o API del BFA (`credenciales.servicios_bfa`, [PROPUESTO] vacío: decisión del operador, INC-T177-01).
    Falla cerrado: una entrada sin `servicio`, `uso_previsto` o `impacto_si_falta` de texto es un error de configuración."""
    lista = (cfg.get("credenciales") or {}).get("servicios_bfa") or []
    if not isinstance(lista, list):
        raise TypeError("credenciales.servicios_bfa debe ser una lista")
    out, vistos = [], set()
    for i, s in enumerate(lista):
        if not isinstance(s, dict) or not all(isinstance(s.get(k), str) and s[k].strip()
                                              for k in ("servicio", "uso_previsto", "impacto_si_falta")):
            raise ValueError(f"credenciales.servicios_bfa[{i}]: se esperan servicio, uso_previsto e impacto_si_falta (texto)")
        alias = alias_de(s["servicio"].strip())
        if alias in vistos:
            raise ValueError(f"credenciales.servicios_bfa[{i}]: servicio repetido ({s['servicio']!r})")
        vistos.add(alias)
        out.append({k: s[k].strip() for k in ("servicio", "uso_previsto", "impacto_si_falta")})
    return out


def uc_c4_semana(bloque, as_of) -> float:
    """UC gastadas (o reservadas por una C4 en curso) por el BFA en las C4- de los últimos 7 días hasta `as_of` incluido
    (HT-05: una semana). T-177 r03: cada C4- cuenta una vez, con su último `uc` (la reserva se sustituye por lo gastado)."""
    hoy = pd.Timestamp(as_of).normalize()
    desde = hoy - pd.Timedelta(days=DIAS_SEMANA)
    total = 0.0
    for e in bloque.almacen.estado("F5").values():
        if (e.get("tipo_entrada") == "C4_CREDENCIALES" and e.get("agente") == AGENTE_BFA and e.get("fecha")
                and desde < pd.Timestamp(e["fecha"]) <= hoy):
            total += float(e.get("uc") or 0.0)
    return total


def reservas_huerfanas(bloque, as_of, c4_id: str) -> list[str]:
    """T-177 cierre (QA r03, H-16): las C4- `EN_CURSO` de la ventana que ocupan la bolsa. Por cada una cuyo proceso ya no vive
    (`interfaz_broker._pid_vivo` es False) se deja, una sola vez, una incidencia Operativa en HA, sin liberar la reserva (falla
    cerrado: no se sabe cuánto gastó). Devuelve los ids de todas las que siguen en curso."""
    from .interfaz_broker import _pid_vivo
    hoy = pd.Timestamp(as_of).normalize()
    desde = hoy - pd.Timedelta(days=DIAS_SEMANA)
    avisadas = {e.get("reserva_huerfana") for e in bloque.almacen.leer("HA") if e.get("reserva_huerfana")}
    ids = []
    for e in bloque.almacen.estado("F5").values():
        if (e.get("tipo_entrada") != "C4_CREDENCIALES" or e.get("agente") != AGENTE_BFA or e.get("estado_retorno") != "EN_CURSO"
                or not e.get("fecha") or not desde < pd.Timestamp(e["fecha"]) <= hoy or e.get("id") == c4_id):
            continue
        ids.append(e["id"])
        if _pid_vivo(e.get("pid")) is False and e["id"] not in avisadas:
            hasta = (pd.Timestamp(e["fecha"]) + pd.Timedelta(days=DIAS_SEMANA)).date()
            bloque.almacen.incidencia("OTRO", f"Reserva huérfana {e['id']} (proceso terminado): la bolsa semanal del BFA queda "
                                      f"bloqueada hasta {hasta}", AGENTE_BFA, severidad="Operativa",
                                      tratamiento="reserva sin liberar (falla cerrado); revisar el planificador del C4",
                                      reserva_huerfana=e["id"])
    return sorted(ids)


def mantenimiento_c4(bloque, as_of) -> dict:
    """Revisión C4 de credenciales del BFA y emisión de los CT-25 que falten. Devuelve el resumen de la C4- de F5."""
    servicios = servicios_bfa(bloque.cfg)   # valida antes de mutar
    as_of = bloque.fijar_fecha(as_of)
    hoy = as_of.date()
    c4_id = bloque.almacen.nuevo_id("C4")
    # Solo alias y estado (HT-01 «solo estado de la bóveda» para el BFA): nunca el valor ni la ficha completa del índice
    vista = []
    for s in servicios:
        e = bloque.credenciales.boveda.estado_servicio(s["servicio"], hoy)
        vista.append({**s, "credencial_ref": e.get("alias"), "estado": e.get("estado")})
    msg = {"tipo": "MANTENIMIENTO_C4", "tarea": "CREDENCIALES", "fecha": str(hoy), "servicios": vista}
    semana = float(parametro(bloque.cfg, "mantenimiento_c4.presupuesto_uc_semana.BFA"))
    base = {"tipo_entrada": "C4_CREDENCIALES", "id": c4_id, "agente": AGENTE_BFA, "fecha": str(hoy)}
    # T-177 r03 (observación de la QA r02): leer lo gastado y reservar lo que queda de una vez, dentro de la transacción del
    # almacén (también entre procesos). Una C4 a la vez que otra en curso ve la bolsa reservada y queda SIN_PRESUPUESTO, así
    # que entre las dos no gastan más que la bolsa semanal. La reserva es una C4- `EN_CURSO` con `uc` = lo que quedaba; al
    # terminar (o fallar) se sustituye por lo gastado. Si el proceso muere a mitad, la reserva se queda la semana (falla
    # cerrado, INC-T177-01).
    with bloque.almacen._transaccion():
        restante = semana - uc_c4_semana(bloque, as_of)
        reservado = bool(vista) and restante > 0
        if reservado:
            bloque.almacen.escribir("F5", "AG-01", {**base, "estado_retorno": "EN_CURSO", "uc": round(restante, 6),
                                                     "pid": os.getpid()})   # T-177 cierre (QA r03, H-16)
    uc = 0.0
    datos = None
    if not vista:   # T-177 r02 (QA r01, H-07 a): sin servicios que revisar, no se llama al BFA ni se gastan UC
        estado_retorno = "SIN_SERVICIOS"
    elif not reservado:   # H-07 b: la bolsa del Anexo A es semanal, no por llamada
        estado_retorno = "SIN_PRESUPUESTO"
    else:
        presupuesto = Presupuesto({BOLSA_C4: restante}, bloque.cfg)
        try:
            r = bloque._invocar(AGENTE_BFA, "C4", msg, "BUSQUEDA", INSTRUCCION_C4, as_of, c4_id, fase="mantenimiento_c4",
                                presupuesto=presupuesto, bolsa=BOLSA_C4)
        except BaseException:
            bloque.almacen.escribir("F5", "AG-01", {**base, "estado_retorno": "ERROR",
                                                     "uc": round(float(presupuesto.consumido.get(BOLSA_C4, 0.0)), 6)})
            raise
        uc = round(float(presupuesto.consumido.get(BOLSA_C4, 0.0)), 6)
        datos = r.datos if r is not None else None
        # sin datos porque la llamada no cabía en lo que queda de la bolsa semanal: SIN_PRESUPUESTO, no SIN_RESULTADO
        estado_retorno = "COMPLETO" if datos is not None else ("SIN_PRESUPUESTO" if presupuesto.cierres else "SIN_RESULTADO")
    extra = {"reservas_en_curso": reservas_huerfanas(bloque, as_of, c4_id)} if estado_retorno == "SIN_PRESUPUESTO" else {}
    resultado = bloque.credenciales.desde_retorno(datos, AGENTE_BFA, as_of, origen=c4_id)
    entrada = {**base, "servicios_revisados": [{"servicio": v["servicio"], "estado": v["estado"]} for v in vista],
               "estado_retorno": estado_retorno, "uc": uc, "uc_semana_disponible": round(max(restante, 0.0), 6), **extra, **resultado}
    bloque.almacen.escribir("F5", "AG-01", entrada)
    return entrada

