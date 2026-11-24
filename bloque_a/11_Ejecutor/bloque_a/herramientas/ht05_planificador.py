"""HT-05 · Planificador: fechas de ciclo, fechas de resolución de pronósticos y reprogramación.

Calendario simplificado: días hábiles de lunes a viernes (sin festivos de mercado; declarado).
"""
from __future__ import annotations

import datetime as dt
import re

import pandas as pd

FRECUENCIAS = {"diaria": "B", "semanal": 7, "quincenal": 14, "mensual": "M"}
DIAS = {"LUN": 0, "MAR": 1, "MIE": 2, "MIÉ": 2, "JUE": 3, "VIE": 4, "SAB": 5, "SÁB": 5, "DOM": 6}


def fechas_ciclo(desde, hasta, frecuencia: str = "semanal", dia_semana: int = 4) -> list[pd.Timestamp]:
    """Fechas as_of de un backtest: la primera fecha >= desde que cae en `dia_semana` y luego cada periodo."""
    d0, d1 = pd.Timestamp(desde).normalize(), pd.Timestamp(hasta).normalize()
    if frecuencia == "diaria":
        return list(pd.bdate_range(d0, d1))
    if frecuencia == "mensual":
        fechas = pd.date_range(d0, d1, freq="BME")
        return [f.normalize() for f in fechas]
    paso = FRECUENCIAS.get(frecuencia)
    if not isinstance(paso, int):
        raise ValueError(f"Frecuencia no admitida: {frecuencia}")
    f = d0 + pd.Timedelta(days=(dia_semana - d0.weekday()) % 7)
    out = []
    while f <= d1:
        out.append(f)
        f = f + pd.Timedelta(days=paso)
    return out


def fecha_resolucion(emision, horizonte: str, cfg_horizontes: dict) -> pd.Timestamp:
    """H1 = n sesiones hábiles; H2 = n semanas; H3/H4 = n meses (por defecto 5 s, 4 sem, 6 m, 12 m)."""
    e = pd.Timestamp(emision).normalize()
    h = cfg_horizontes[horizonte]
    if "sesiones" in h:
        return (e + pd.offsets.BDay(int(h["sesiones"]))).normalize()
    if "semanas" in h:
        return e + pd.Timedelta(weeks=int(h["semanas"]))
    if "meses" in h:
        return (e + pd.DateOffset(months=int(h["meses"]))).normalize()
    if "dias" in h:
        return e + pd.Timedelta(days=int(h["dias"]))
    raise ValueError(f"Horizonte mal configurado: {horizonte}")


def dias_habiles_entre(a, b) -> int:
    return max(len(pd.bdate_range(pd.Timestamp(a), pd.Timestamp(b))) - 1, 0)


def proxima_ejecucion(desde: dt.datetime, periodicidad: str = "SEMANAL", dia_hora: str = "SAB 06:00") -> dt.datetime:
    """Próxima ejecución del ciclo C1 según F10 (P-01)."""
    dia, hora = (dia_hora.split() + ["06:00"])[:2]
    hh, mm = (int(x) for x in hora.split(":"))
    objetivo = DIAS.get(dia.upper()[:3], 5)
    base = desde.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if periodicidad.upper() == "DIARIA":
        return base if base > desde else base + dt.timedelta(days=1)
    delta = (objetivo - desde.weekday()) % 7
    cand = base + dt.timedelta(days=delta)
    if cand <= desde:
        cand += dt.timedelta(days=7)
    if periodicidad.upper() == "QUINCENAL":
        cand += dt.timedelta(days=7) if cand.isocalendar()[1] % 2 else dt.timedelta(0)
    if periodicidad.upper() == "MENSUAL":
        while cand.day > 7:
            cand += dt.timedelta(days=7)
    return cand


# ====================================================================================
# T-197 (PB-09) · Calendario del ciclo C1 a partir del P-01 de F10
# ====================================================================================
# Especificación: `bloque_a/10_Herramientas/ht05_planificador_ejemplo.md` (§2 franja sin disparos, §4 periodicidades del
# C1 y adelanto de la ejecución sobre la entrega, §5 idempotencia y disparos perdidos). Los números (adelanto, franja,
# recuperación) salen de `planificador` en `config/por_defecto.yaml`; las decisiones, de INC-T197-01.
P01_INICIAL = "SEMANAL · SAB 06:00 · entrega LUN 07:00"   # valor por defecto de P-01 (esquema de F10 V3.0)
PERIODICIDADES_C1 = ("DIARIA", "SEMANAL", "QUINCENAL", "MENSUAL")   # las que HT-05 programa (CT-04)
NOMBRES_DIA = ("LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM")
RE_DIA_HORA = re.compile(r"(LUN|MAR|MIE|MIÉ|JUE|VIE|SAB|SÁB|DOM) ([01]\d|2[0-3]):([0-5]\d)")
MIN_DIA, MIN_SEMANA = 24 * 60, 7 * 24 * 60


class P01Invalido(ValueError):
    """P-01 de F10 (o pedido por CT-04) que HT-05 no sabe programar: no se escribe ni se dispara nada."""


def dia_hora(texto) -> tuple[int, int, int]:
    """«MIE 08:00» → (2, 8, 0). Falla cerrado con `P01Invalido`."""
    m = RE_DIA_HORA.fullmatch(texto) if isinstance(texto, str) else None
    if not m:
        raise P01Invalido(f"se espera día de la semana y hora HH:MM, no {texto!r}")
    return DIAS[m.group(1)], int(m.group(2)), int(m.group(3))


def ejecucion_para_entrega(periodicidad: str, entrega: str, cfg_planificador: dict) -> str:
    """Día y hora de la ejecución del C1 para una entrega (§4): la entrega menos el adelanto de su periodicidad, redondeada
    hacia abajo a la hora en punto. Falla cerrado si la ejecución cae en la franja sin disparos (§2) o, en la diaria, en el día
    anterior al de la entrega."""
    if periodicidad not in PERIODICIDADES_C1:
        raise P01Invalido(f"periodicidad no programable por HT-05: {periodicidad!r}")
    d, hh, mm = dia_hora(entrega)
    desde_h, hasta_h = (int(x) for x in cfg_planificador["franja_sin_disparos_h"])
    if desde_h <= hh < hasta_h:   # T-197 r02 (H-04): la entrega (C1-ENTREGA) también es un disparo de HT-05 (§2 y §3)
        raise P01Invalido(f"la entrega a las {hh:02d}:{mm:02d} cae en la franja sin disparos de HT-05")
    adelanto = int(cfg_planificador["adelanto_ejecucion_h"][periodicidad]) * 60
    if periodicidad == "DIARIA" and hh * 60 + mm - adelanto < 0:
        raise P01Invalido("la ejecución diaria quedaría en el día anterior al de la entrega")
    minuto = (d * MIN_DIA + hh * 60 + mm - adelanto) % MIN_SEMANA
    dia, hora = divmod(minuto, MIN_DIA)   # la hora se escribe en punto (hora // 60): redondeo hacia abajo
    if desde_h <= hora // 60 < hasta_h:
        raise P01Invalido(f"la ejecución quedaría a las {hora // 60:02d}:00, en la franja sin disparos de HT-05")
    return f"{NOMBRES_DIA[dia]} {hora // 60:02d}:00"


def componer_p01(periodicidad: str | None, ejecucion: str | None, entrega: str | None) -> str:
    """El P-01 de tres partes; falla cerrado si falta alguna (nunca escribe «None» en F10)."""
    if not (periodicidad and ejecucion and entrega):
        raise P01Invalido("P-01 incompleto: hacen falta la periodicidad, la ejecución y la entrega")
    return f"{periodicidad} · {ejecucion} · entrega {entrega}"


def leer_p01(valor) -> tuple[str, str | None, str]:
    """(periodicidad, ejecución, entrega) de un P-01. Admite el formato de tres partes y el de dos que escribía el CT-04 antes
    de T-197 («QUINCENAL · MIE 08:00», con la entrega y sin la ejecución: ejecución None)."""
    partes = valor.split(" · ") if isinstance(valor, str) else []
    if len(partes) == 3 and partes[2].startswith("entrega "):
        periodicidad, ejecucion, entrega = partes[0], partes[1], partes[2].removeprefix("entrega ")
        dia_hora(ejecucion)
    elif len(partes) == 2:
        periodicidad, ejecucion, entrega = partes[0], None, partes[1]
    else:
        raise P01Invalido(f"P-01 con un formato que HT-05 no conoce: {valor!r}")
    if periodicidad not in PERIODICIDADES_C1:
        raise P01Invalido(f"periodicidad no programable por HT-05: {periodicidad!r}")
    dia_hora(entrega)
    return periodicidad, ejecucion, entrega


def _ancla(ejecucion: str, inicio: dt.date) -> dt.date:
    """Lunes de la semana de la primera ejecución en o después de `inicio` (la guarda quincenal de §4)."""
    d = dia_hora(ejecucion)[0]
    primero = inicio + dt.timedelta(days=(d - inicio.weekday()) % 7)
    return primero - dt.timedelta(days=primero.weekday())


def ancla_quincenal(ejecucion: str | None, inicio: dt.date) -> dt.date:
    """`semana_ancla_quincenal` (§4 y §6) de una quincenal nueva: el lunes de la semana de su primera ejecución."""
    if not ejecucion:
        raise P01Invalido("sin ejecución no hay ancla quincenal")
    return _ancla(ejecucion, inicio)


def ancla_de_p01(entrada: dict, cfg_planificador: dict) -> dt.date:
    """El ancla de una entrada quincenal de F10: la guardada (`semana_ancla_quincenal`) o, en las anteriores a T-197 r02, la
    semana de su primera ejecución desde que rige (su `fecha_efecto`, o la fecha de la entrada)."""
    if entrada.get("semana_ancla_quincenal"):
        return dt.date.fromisoformat(str(entrada["semana_ancla_quincenal"])[:10])
    periodicidad, ejecucion, entrega = leer_p01(entrada.get("valor_vigente"))
    if ejecucion is None:
        ejecucion = ejecucion_para_entrega(periodicidad, entrega, cfg_planificador)
    inicio = dt.date.fromisoformat(str(entrada.get("fecha_efecto") or entrada["_fecha"])[:10])
    return _ancla(ejecucion, inicio)


def es_dia_de_ejecucion(dia: dt.date, periodicidad: str, ejecucion: str, inicio: dt.date, ancla: dt.date | None = None) -> bool:
    """Si el C1 se ejecuta ese día (§4): diaria de lunes a viernes; semanal el día de la ejecución; quincenal, además, en
    semanas pares desde el ancla (la guardada en F10, `semana_ancla_quincenal`, o, si no la hay, la semana de la primera
    ejecución desde `inicio`); mensual, además, solo entre los días 1 y 7 del mes. Nunca antes de `inicio`."""
    if dia < inicio:
        return False
    if periodicidad == "DIARIA":
        return dia.weekday() < 5
    if dia.weekday() != dia_hora(ejecucion)[0]:
        return False
    if periodicidad == "QUINCENAL":
        base = _ancla(ejecucion, inicio) if ancla is None else ancla - dt.timedelta(days=ancla.weekday())
        return ((dia - base).days // 7) % 2 == 0
    if periodicidad == "MENSUAL":
        return dia.day <= 7
    return True


def _en_hora(dia: dt.date, ejecucion: str) -> dt.datetime:
    _, hh, mm = dia_hora(ejecucion)
    return dt.datetime.combine(dia, dt.time(hh, mm))


def siguiente_ejecucion(desde: dt.datetime, periodicidad: str, ejecucion: str, inicio: dt.date,
                        ancla: dt.date | None = None) -> dt.datetime:
    """Primera ejecución estrictamente posterior a `desde` (y no anterior a `inicio`)."""
    dia = max(desde.date(), inicio)
    for _ in range(MIN_SEMANA):   # cota holgada: una mensual está siempre a menos de seis semanas
        if es_dia_de_ejecucion(dia, periodicidad, ejecucion, inicio, ancla) and _en_hora(dia, ejecucion) > desde:
            return _en_hora(dia, ejecucion)
        dia += dt.timedelta(days=1)
    raise P01Invalido("HT-05 no encuentra la siguiente ejecución del C1")


def ultima_ejecucion(hasta: dt.datetime, periodicidad: str, ejecucion: str, inicio: dt.date,
                     ancla: dt.date | None = None) -> dt.datetime | None:
    """Última ejecución en o antes de `hasta` y no anterior a `inicio`; None si no hay ninguna."""
    dia = hasta.date()
    while dia >= inicio:
        if es_dia_de_ejecucion(dia, periodicidad, ejecucion, inicio, ancla) and _en_hora(dia, ejecucion) <= hasta:
            return _en_hora(dia, ejecucion)
        dia -= dt.timedelta(days=1)
    return None


def entrega_de(ejecucion_dt: dt.datetime, periodicidad: str, entrega: str) -> dt.datetime:
    """La entrega que sigue a una ejecución: la primera vez, después de ella, que llega el día y la hora de entrega (en la
    diaria, la hora de entrega de ese mismo día o del siguiente)."""
    d, hh, mm = dia_hora(entrega)
    dia = ejecucion_dt.date()
    for _ in range(8):
        cand = dt.datetime.combine(dia, dt.time(hh, mm))
        if cand > ejecucion_dt and (periodicidad == "DIARIA" or dia.weekday() == d):
            return cand
        dia += dt.timedelta(days=1)
    raise P01Invalido("HT-05 no encuentra la entrega de la ejecución")
