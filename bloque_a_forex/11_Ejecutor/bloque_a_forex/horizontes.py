"""Regla de adecuación del horizonte al tipo de inversión y horizonte H5 «limitado» (Documento 0 Forex V1.1, 8.3 y Anexo A).

- `naturaleza_por_defecto`: naturaleza de la inversión cuando el Analista no la declara (o la declara mal).
- `elegir_principal`: horizonte principal coherente con la naturaleza entre los horizontes ofrecidos.
- `hitos_h5`: hitos intermedios verificables (HIT-FX-) de un pronóstico H5: ≥ 3, el primero a ≤ 12 meses y ≤ 24 meses
  entre hitos consecutivos. Cada hito se resuelve en su fecha como un pronóstico ordinario sobre la serie HT-01.

Las comprobaciones deterministas de esta regla las hace HT-09 (C17 y C18); este módulo solo construye datos coherentes.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd

RANGO_NATURALEZA = {"TACTICA": ("H1", "H2"), "CICLICA": ("H2", "H3", "H4"), "PRIMA_RIESGO": ("H2", "H3", "H4"),
                    "VALORACION": ("H3", "H4"), "ESTRUCTURAL": ("H4", "H5")}
NATURALEZAS = tuple(RANGO_NATURALEZA)
AMBITOS_H5 = ("EQUILIBRIO_LARGO_PLAZO", "REGIMEN_CAMBIARIO", "SISTEMA_MONETARIO_INTERNACIONAL")
# Anexo A: frecuencia orientativa del seguimiento encargado según el horizonte principal (aviso, no veto)
FRECUENCIA_ORIENTATIVA = {"H1": ("DIARIA",), "H2": ("DIARIA", "SEMANAL"), "H3": ("SEMANAL", "QUINCENAL", "MENSUAL"),
                          "H4": ("MENSUAL", "TRIMESTRAL"), "H5": ("TRIMESTRAL",)}
ORDEN_FRECUENCIA = ("DIARIA", "SEMANAL", "QUINCENAL", "MENSUAL", "TRIMESTRAL")
H5_MESES_HITOS = (6, 30, 54)          # primer hito a 6 meses; 24 meses entre hitos (Anexo A: ≤ 12 y ≤ 24)
H5_ANIOS_RESOLUCION = 10


def naturaleza_por_defecto(tipo_opcion: Optional[str], horizontes: Iterable[str], preferida: Optional[str] = None) -> str:
    """Naturaleza coherente con el tipo de opción y con el horizonte que se prefiere como principal."""
    hs = set(horizontes)
    if "H5" in hs and preferida in (None, "H5", "H4"):
        return "ESTRUCTURAL"
    if tipo_opcion == "ESTRATEGIA":
        return "PRIMA_RIESGO"
    h = preferida if preferida in hs else (sorted(hs)[0] if hs else "H3")
    return {"H1": "TACTICA", "H2": "CICLICA", "H3": "CICLICA", "H4": "VALORACION", "H5": "ESTRUCTURAL"}.get(h, "CICLICA")


def elegir_principal(naturaleza: str, horizontes: Iterable[str], preferencia: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """(horizonte_principal, justificacion). Toma el primero de `preferencia` dentro del rango de la naturaleza; si ninguno
    de los ofrecidos cae en el rango, toma el preferido y devuelve una justificación (HT-09 lo dejará en advertencia)."""
    hs = list(horizontes)
    if not hs:
        return None, None
    orden = list(preferencia) + [h for h in ("H3", "H2", "H4", "H1", "H5") if h not in preferencia]
    rango = RANGO_NATURALEZA.get(naturaleza, ())
    dentro = [h for h in orden if h in hs and h in rango]
    if dentro:
        return dentro[0], None
    h = next(h for h in orden if h in hs)
    return h, (f"Único horizonte ofrecido compatible con la tabla 8.3 del segmento; la tesis {naturaleza.lower()} se mide en {h} "
               f"(fuera del rango {rango[0]}–{rango[-1]}) y se revisará al siguiente ciclo")


def aviso_frecuencia(frecuencia: str, horizonte_principal: Optional[str]) -> Optional[str]:
    """Aviso (nunca veto, R5) si la frecuencia del seguimiento es más corta que la orientativa para el horizonte principal."""
    f = str(frecuencia or "").upper()
    if not horizonte_principal or f not in ORDEN_FRECUENCIA or f == "PERSONALIZADA":
        return None
    minima = FRECUENCIA_ORIENTATIVA.get(horizonte_principal, ("SEMANAL",))[0]
    if ORDEN_FRECUENCIA.index(f) < ORDEN_FRECUENCIA.index(minima):
        return (f"Frecuencia {f.lower()} más corta que la orientativa para el horizonte principal {horizonte_principal} "
                f"({'/'.join(x.lower() for x in FRECUENCIA_ORIENTATIVA[horizonte_principal])}): se acepta; los ciclos sin cambio "
                "material se entregarán como «sin novedad»")
    return None


def hitos_h5(as_of, serie: str, nivel: Optional[float], sube: bool, ambito: str) -> List[Dict]:
    """Tres hitos medibles sobre la serie de seguimiento (HT-01): el indicador debe moverse en la dirección de la tesis al menos
    un 2 %, 5 % y 8 % frente al nivel de referencia. Los `hit_id` los asigna el almacén al congelar."""
    a = pd.Timestamp(as_of).normalize()
    out = []
    for i, (meses, umbral) in enumerate(zip(H5_MESES_HITOS, (0.02, 0.05, 0.08))):
        f = (a + pd.DateOffset(months=meses)).normalize()
        out.append({"fecha": str(f.date()), "indicador": f"{serie} (HT-01), cierre de la última sesión ≤ {f.date()}",
                    "criterio": (f"{serie} {'al menos un' if sube else 'al menos un'} {umbral:.0%} "
                                 f"{'por encima' if sube else 'por debajo'} del nivel de referencia"
                                 + (f" ({nivel:.6g})" if isinstance(nivel, (int, float)) else "")),
                    "referencia_ingenua": "paseo aleatorio (sin cambio del indicador)",
                    "serie_ht01": serie, "umbral_rel": umbral if sube else -umbral, "sentido": "POSITIVO" if sube else "NEGATIVO",
                    "ambito_h5": ambito, "orden": i + 1, "estado": "ABIERTO"})
    return out


def fecha_resolucion_h5(as_of) -> pd.Timestamp:
    return (pd.Timestamp(as_of).normalize() + pd.DateOffset(years=H5_ANIOS_RESOLUCION)).normalize()
