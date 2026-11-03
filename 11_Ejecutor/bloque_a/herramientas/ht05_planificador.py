"""HT-05 · Planificador: fechas de ciclo, fechas de resolución de pronósticos y reprogramación.

Calendario simplificado: días hábiles de lunes a viernes (sin festivos de mercado; declarado).
"""
from __future__ import annotations

import datetime as dt
from typing import Dict, List

import pandas as pd

FRECUENCIAS = {"diaria": "B", "semanal": 7, "quincenal": 14, "mensual": "M"}
DIAS = {"LUN": 0, "MAR": 1, "MIE": 2, "MIÉ": 2, "JUE": 3, "VIE": 4, "SAB": 5, "SÁB": 5, "DOM": 6}


def fechas_ciclo(desde, hasta, frecuencia: str = "semanal", dia_semana: int = 4) -> List[pd.Timestamp]:
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


def fecha_resolucion(emision, horizonte: str, cfg_horizontes: Dict) -> pd.Timestamp:
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
