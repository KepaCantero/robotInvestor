"""Carga y fusión de la configuración del ejecutor del Bloque A Forex (YAML) y resolución de rutas."""
from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

DIR_PAQUETE = Path(__file__).resolve().parent            # .../11_Ejecutor/bloque_a_forex
DIR_EJECUTOR = DIR_PAQUETE.parent                         # .../11_Ejecutor
RUTA_CONFIG_POR_DEFECTO = DIR_EJECUTOR / "config" / "por_defecto.yaml"
RUTA_UNIVERSO_EJEMPLO = DIR_EJECUTOR / "config" / "universo_ejemplo.csv"

# Los seis segmentos de divisas del Documento 0 del Bloque A Forex V1.1 (2.6), en el orden canónico de la tabla.
SEGMENTOS = ("G10N", "G10M", "EMAS", "EMLA", "EMEA", "ESTR")
NOMBRE_SEGMENTO = {
    "G10N": "G10 núcleo", "G10M": "G10 de materias primas y escandinavas", "EMAS": "Emergentes de Asia",
    "EMLA": "Emergentes de Latinoamérica", "EMEA": "Emergentes de Europa, Oriente Medio y África",
    "ESTR": "Estrategias y cestas cambiarias",
}
SEGMENTOS_EMERGENTES = ("EMAS", "EMLA", "EMEA")
# Tipos de opción cambiaria (2.4): granularidad máxima par, cruce, cesta, bloque, estrategia o régimen (nunca un instrumento, R21)
TIPOS_OPCION = ("PAR", "CRUCE", "CESTA", "BLOQUE", "ESTRATEGIA", "VOLATILIDAD", "REGIMEN")
TIPOS_CON_PAR = ("PAR", "CRUCE", "VOLATILIDAD", "REGIMEN")
TIPOS_CESTA = ("CESTA", "BLOQUE", "ESTRATEGIA")
# Horizontes cuantitativos (pronósticos de precio resolubles en un backtest) y H5 «limitado» (V1.1, 8.3): décadas,
# solo para naturaleza ESTRUCTURAL en tres ámbitos, sin probabilidad numérica y evaluado por hitos (horizontes.py).
HORIZONTES = ("H1", "H2", "H3", "H4")
HORIZONTE_H5 = "H5"
HORIZONTES_TODOS = HORIZONTES + (HORIZONTE_H5,)
# Tabla 8.3 del Documento 0 Forex V1.1: SI · LIMITADO · NO
TABLA_HORIZONTES = {
    "G10N": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
    "G10M": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
    "EMAS": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"},
    "EMLA": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"},
    "EMEA": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"},
    "ESTR": {"H1": "NO", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
}


def fusionar(base: Dict, extra: Optional[Dict]) -> Dict:
    """Fusión recursiva (extra prevalece)."""
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = fusionar(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def raiz_paquete(cfg: Dict) -> Path:
    r = (cfg.get("rutas") or {}).get("raiz_paquete") or os.environ.get("BLOQUE_A_FOREX_RAIZ") or os.environ.get("BLOQUE_A_RAIZ")
    return Path(r).resolve() if r else DIR_EJECUTOR.parent


def ruta(cfg: Dict, clave: str) -> Path:
    """Ruta de una carpeta del paquete (prompts, plantillas, archivos_operativos)."""
    valor = (cfg.get("rutas") or {}).get(clave)
    p = Path(valor)
    return p if p.is_absolute() else raiz_paquete(cfg) / p


def buscar_versionado(carpeta: Path, bases, extension: str = ".md") -> Optional[Path]:
    """Busca «<base> - … V<x.y><ext>» (o «<base> - V<x.y><ext>», o «<base><ext>») con cualquier sufijo de versión.

    `bases` puede ser un texto o una lista de nombres alternativos de un mismo agente o plantilla; se prefiere el
    archivo cuyo nombre contiene «Bloque A Forex» y, entre ellos, el de versión más alta (a igual versión, el del
    primer nombre de la lista). Robusto a cambios de sufijo de versión, a mayúsculas y a variantes NFC/NFD de los
    nombres de archivo. Devuelve None si no hay ninguno."""
    import re
    import unicodedata
    if isinstance(bases, str):
        bases = [bases]
    if not carpeta.is_dir():
        return None
    archivos = [p for p in carpeta.iterdir() if p.is_file() and p.suffix.lower() == extension.lower()]
    candidatos = []
    for orden, base in enumerate(bases):
        nb = unicodedata.normalize("NFC", base).casefold()
        for p in archivos:
            tallo = unicodedata.normalize("NFC", p.stem)
            t = tallo.casefold()
            forex = 1 if "bloque a forex" in t else 0
            if t == nb:
                candidatos.append((forex, (0, 0), -orden, p.name, p))
                continue
            if not t.startswith(nb):
                continue
            m = re.fullmatch(r"\s*[-–—]\s*(?:.*?\s)?V(\d+)\.(\d+)\s*", tallo[len(base):], flags=re.IGNORECASE)
            if m:
                candidatos.append((forex, (int(m.group(1)), int(m.group(2))), -orden, p.name, p))
    if not candidatos:
        return None
    return max(candidatos, key=lambda x: x[:4])[4]


def cargar_config(ruta_yaml: Optional[str] = None, extra: Optional[Dict] = None) -> Dict:
    with open(RUTA_CONFIG_POR_DEFECTO, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    if ruta_yaml:
        with open(ruta_yaml, encoding="utf-8") as fh:
            cfg = fusionar(cfg, yaml.safe_load(fh) or {})
    if extra:
        cfg = fusionar(cfg, extra)
    return cfg


def modelo_de(cfg: Dict, agente: str) -> str:
    m = cfg.get("modelos") or {}
    return m.get(agente) or m.get("por_defecto")


def max_tokens_de(cfg: Dict, agente: str) -> int:
    m = cfg.get("max_tokens") or {}
    return int(m.get(agente) or m.get("por_defecto") or 8000)


def aplicabilidad(cfg: Dict, segmento: str, horizonte: str) -> str:
    tabla = cfg.get("_tabla_horizontes") or TABLA_HORIZONTES
    return tabla[segmento][horizonte]
