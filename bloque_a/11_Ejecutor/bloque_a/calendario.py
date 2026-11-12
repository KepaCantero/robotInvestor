"""Calendario de sesiones de PS2 (Anexo A, P-13): festivos de mercado y sesiones hábiles entre dos fechas. Lo usan PS2 al
emitir (`Bloque._puertas`) y la resolución de los pronósticos (`Evaluador.motivo_no_fresca`), para que cuenten igual (T-91,
QA r05 de T-65, H-26)."""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

CLAVES_FESTIVOS_PS2 = {"viernes_santo": bool, "lunes_de_pascua": bool, "fijos": list}
RE_MM_DD = re.compile(r"[0-9]{2}-[0-9]{2}", re.ASCII)


def validar_festivos_ps2(festivos) -> dict:
    """T-65 (QA de T-53, H-17): `ps2_festivos` se valida al crear el Bloque. Exige las tres claves con su tipo (booleanos
    de verdad, no el texto «false») y una lista de fechas «MM-DD» válidas; si falta o está mal, ValueError con el motivo
    (antes, PS2 volvía en silencio al cálculo anterior o el ciclo caía con TypeError)."""
    errores: list[str] = []
    if isinstance(festivos, dict):
        faltan = sorted(set(CLAVES_FESTIVOS_PS2) - set(festivos))
        sobran = sorted(set(festivos) - set(CLAVES_FESTIVOS_PS2))
        if faltan or sobran:
            errores.append(f"faltan {faltan} o sobran {sobran}")
        errores += [f"{k} debe ser {tipo.__name__}, no {festivos.get(k)!r}" for k, tipo in CLAVES_FESTIVOS_PS2.items()
                    if k in festivos and not isinstance(festivos[k], tipo)]
        fijos = festivos.get("fijos")
        for d in fijos if isinstance(fijos, list) else []:
            try:
                # QA r01 de T-65, H-04: «MM-DD» estricto (dígitos ASCII, sin espacios), y además una fecha real (2024: admite 02-29)
                ok = isinstance(d, str) and bool(RE_MM_DD.fullmatch(d)) and bool(pd.Timestamp(f"2024-{d}"))
            except (ValueError, TypeError):
                ok = False
            if not ok:
                errores.append(f"fijos: {d!r} no es una fecha «MM-DD»")
    else:
        errores.append(f"debe ser un diccionario con {sorted(CLAVES_FESTIVOS_PS2)}, no {festivos!r}")
    if errores:
        raise ValueError("ps2_festivos: " + "; ".join(errores))
    return {"viernes_santo": festivos["viernes_santo"], "lunes_de_pascua": festivos["lunes_de_pascua"],
            "fijos": sorted(set(festivos["fijos"]))}


def _sesiones_entre(desde, hasta, festivos: dict) -> int:
    """Sesiones hábiles en [desde, hasta) sin los cierres habituales de mercado (`ps2_festivos`, [PROPUESTO]): Viernes
    Santo, lunes de Pascua y fechas fijas MM-DD. Así el dato de la última sesión real vale en H1 tras un puente o un
    festivo. `festivos` ya validado con `validar_festivos_ps2`."""
    d0, d1 = pd.Timestamp(desde).normalize(), pd.Timestamp(hasta).normalize()
    if d1 <= d0:
        return 0
    cierres = [d for d in pd.date_range(d0, d1) if d.strftime("%m-%d") in set(festivos["fijos"])]
    if festivos["viernes_santo"]:
        from pandas.tseries.holiday import GoodFriday
        cierres += list(GoodFriday.dates(d0, d1))
    if festivos["lunes_de_pascua"]:
        from pandas.tseries.holiday import EasterMonday
        cierres += list(EasterMonday.dates(d0, d1))
    return int(np.busday_count(d0.date(), d1.date(), holidays=[d.date() for d in cierres]))
