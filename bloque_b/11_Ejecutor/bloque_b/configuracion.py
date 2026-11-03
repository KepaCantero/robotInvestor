"""Configuración, rutas, constantes y búsqueda robusta de archivos versionados del ejecutor del Bloque B."""
from __future__ import annotations

import copy
import os
import re
import unicodedata
from pathlib import Path
from typing import Dict, Optional, Sequence, Union

import yaml

DIR_PAQUETE = Path(__file__).resolve().parent             # .../11_Ejecutor/bloque_b
DIR_EJECUTOR = DIR_PAQUETE.parent                          # .../11_Ejecutor
RUTA_CONFIG_POR_DEFECTO = DIR_EJECUTOR / "config" / "por_defecto.yaml"

TIPOS_ACTIVO = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
NOMBRE_TIPO = {
    "RV": "Renta variable", "RF": "Renta fija", "DIV": "Divisas", "MP": "Materias primas", "IDX": "Índices bursátiles",
    "FON": "Fondos y vehículos de inversión colectiva", "DER": "Derivados financieros",
    "INM": "Activos inmobiliarios cotizados", "CRI": "Criptoactivos", "ALT": "Capital privado y alternativos",
    "MON": "Monetarios y liquidez", "TCV": "Tipos de interés, crédito y volatilidad",
}
NOMBRE_LLANO_TIPO = {
    "RV": "Acciones", "RF": "Bonos", "DIV": "Monedas", "MP": "Materias primas", "IDX": "Bolsas enteras", "FON": "Fondos",
    "DER": "Derivados", "INM": "Inmuebles", "CRI": "Criptomonedas", "ALT": "Alternativos", "MON": "Ahorro a corto",
    "TCV": "Tipos y nervios",
}
TIPOS_OBJETO = ("SECTOR", "TEMATICA", "MERCADO_GEOGRAFICO", "SEGMENTO_DE_CLASE", "ESTRATEGIA_FACTOR", "CADENA_DE_VALOR")
HORIZONTES = ("H1", "H2", "H3", "H4", "H5")
FASES = ("F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10")
CAPAS = (0, 1, 2, 3, 4)                                   # V2.1 (7.10)
NOMBRE_HORIZONTE_LLANO = {"H1": "Días", "H2": "Semanas", "H3": "Meses", "H4": "Años", "H5": "Décadas"}
DIAS_HORIZONTE = {"H1": 14, "H2": 60, "H3": 365, "H4": 730, "H5": 1825}
FRESCURA_MERCADO_DIAS = {"H1": 1, "H2": 3, "H3": 7, "H4": 30, "H5": 90}


def fusionar(base: Dict, extra: Optional[Dict]) -> Dict:
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = fusionar(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def cargar_config(ruta_yaml: Optional[str] = None, extra: Optional[Dict] = None) -> Dict:
    with open(RUTA_CONFIG_POR_DEFECTO, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    if ruta_yaml:
        with open(ruta_yaml, encoding="utf-8") as fh:
            cfg = fusionar(cfg, yaml.safe_load(fh) or {})
    if extra:
        cfg = fusionar(cfg, extra)
    return cfg


def raiz_paquete(cfg: Dict) -> Path:
    r = (cfg.get("rutas") or {}).get("raiz_paquete") or os.environ.get("BLOQUE_B_RAIZ")
    return Path(r).resolve() if r else DIR_EJECUTOR.parent


def ruta(cfg: Dict, clave: str) -> Path:
    valor = (cfg.get("rutas") or {}).get(clave)
    p = Path(valor)
    if p.is_absolute():
        return p
    if clave in ("universos", "ambitos"):
        return DIR_EJECUTOR / p
    return raiz_paquete(cfg) / p


def _nfc(t: str) -> str:
    return unicodedata.normalize("NFC", t)


def buscar_versionado(carpeta: Path, bases: Union[str, Sequence[str]], extension: str = ".md") -> Optional[Path]:
    """Busca «<base> - … V<x.y><ext>» (o «<base><ext>») con cualquier texto intermedio («- Bloque B - Versión óptima
    V2.0»), tolerando mayúsculas, NFC/NFD y guiones largos; devuelve la versión más alta y, a igual versión, el primer
    nombre de la lista. None si no hay ninguno."""
    if isinstance(bases, str):
        bases = [bases]
    carpeta = Path(carpeta)
    if not carpeta.is_dir():
        return None
    archivos = [p for p in carpeta.iterdir() if p.is_file() and p.suffix.lower() == extension.lower()]
    cands = []
    for orden, base in enumerate(bases):
        nb = _nfc(base).casefold()
        for p in archivos:
            tallo = _nfc(p.stem)
            t = tallo.casefold()
            if t == nb:
                cands.append(((0, 0), -orden, p.name, p))
                continue
            if not t.startswith(nb):
                continue
            m = re.fullmatch(r"\s*[-–—]\s*(?:.*?\s)?V(\d+)\.(\d+)\s*", tallo[len(base):], flags=re.IGNORECASE)
            if m:
                cands.append(((int(m.group(1)), int(m.group(2))), -orden, p.name, p))
    if not cands:
        return None
    return max(cands, key=lambda x: x[:3])[3]


def modelo_de(cfg: Dict, agente: str) -> str:
    m = cfg.get("modelos") or {}
    return m.get(agente) or m.get("por_defecto")


def max_tokens_de(cfg: Dict, agente: str) -> int:
    m = cfg.get("max_tokens") or {}
    return int(m.get(agente) or m.get("por_defecto") or 8000)


def cargar_ambitos(cfg: Dict) -> Dict:
    p = ruta(cfg, "ambitos")
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}
