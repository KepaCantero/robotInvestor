"""Carga y fusión de la configuración del ejecutor (YAML) y resolución de rutas."""
from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any

import yaml

DIR_PAQUETE = Path(__file__).resolve().parent            # .../11_Ejecutor/bloque_a
DIR_EJECUTOR = DIR_PAQUETE.parent                         # .../11_Ejecutor
RUTA_CONFIG_POR_DEFECTO = DIR_EJECUTOR / "config" / "por_defecto.yaml"
RUTA_UNIVERSO_EJEMPLO = DIR_EJECUTOR / "config" / "universo_ejemplo.csv"

# Los doce tipos de activo del Documento 0 óptima V5.0–V5.1 (2.6), en el orden canónico de la tabla.
# «Clase» se mantiene en el código como sinónimo de «tipo de activo» (2.6).
CLASES = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
TIPOS_ACTIVO = CLASES
NOMBRE_CLASE = {
    "RV": "Renta variable", "RF": "Renta fija", "DIV": "Divisas", "MP": "Materias primas",
    "IDX": "Índices bursátiles", "FON": "Fondos y vehículos de inversión colectiva", "DER": "Derivados financieros",
    "INM": "Activos inmobiliarios cotizados", "CRI": "Criptoactivos y activos digitales",
    "ALT": "Capital privado y activos alternativos", "MON": "Instrumentos monetarios y liquidez",
    "TCV": "Tipos de interés, crédito y volatilidad",
}
# Granularidad del ámbito (2.4): nunca un activo concreto (R21)
TIPOS_OPCION = ("MERCADO", "SECTOR", "SUBSECTOR", "TEMATICA", "SEGMENTO", "FACTOR", "ESTILO", "ESTRATEGIA")
# Compatibilidad con universos V4.x: valores retirados y su equivalente V5.0
TIPOS_OPCION_RETIRADOS = {"INSTRUMENTO_GENERICO": "SEGMENTO", "INDUSTRIA": "SUBSECTOR"}
HORIZONTES = ("H1", "H2", "H3", "H4", "H5")   # H4 años (1–5) · H5 décadas (5–30), V5.1
# Tabla 8.3 del Documento 0 óptima V5.1 (con H5): SI · LIMITADO · NO
TABLA_HORIZONTES = {
    "RV": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "SI"},
    "RF": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
    "DIV": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"},
    "MP": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "SI"},
    "IDX": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "SI"},
    "FON": {"H1": "NO", "H2": "LIMITADO", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
    "DER": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "NO", "H5": "NO"},
    "INM": {"H1": "NO", "H2": "LIMITADO", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
    "CRI": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"},
    "ALT": {"H1": "NO", "H2": "NO", "H3": "LIMITADO", "H4": "SI", "H5": "SI"},
    "MON": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "NO", "H5": "NO"},
    "TCV": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "NO"},
}
# Regla de adecuación del horizonte al tipo de inversión (8.3, V5.1): rango admisible del horizonte principal
NATURALEZAS = {"TACTICA": ("H1", "H2"), "LIQUIDEZ": ("H1", "H3"), "CICLICA": ("H2", "H4"),
               "PRIMA_RIESGO": ("H2", "H4"), "VALORACION": ("H3", "H4"), "ESTRUCTURAL": ("H4", "H5")}
# Naturaleza por defecto de cada tipo de activo cuando el Analista no la declara (decisión del ejecutor)
NATURALEZA_POR_DEFECTO = {"MON": "LIQUIDEZ", "DER": "PRIMA_RIESGO", "ALT": "ESTRUCTURAL"}
# La antigüedad máxima de los datos de mercado por horizonte (PS2, Anexo A) está en `ps2_antiguedad_maxima_dias` de la
# configuración (T-65: ya no se repite aquí).


def naturaleza_coherente(naturaleza: str, horizonte: str) -> bool:
    lo, hi = NATURALEZAS[naturaleza]
    return HORIZONTES.index(lo) <= HORIZONTES.index(horizonte) <= HORIZONTES.index(hi)


def naturaleza_para(horizonte: str) -> str:
    """Naturaleza mínima coherente con un horizonte principal dado (para cuadrar la regla de 8.3)."""
    return {"H1": "TACTICA", "H2": "TACTICA", "H3": "CICLICA", "H4": "CICLICA", "H5": "ESTRUCTURAL"}[horizonte]


def fusionar(base: dict, extra: dict | None) -> dict:
    """Fusión recursiva (extra prevalece)."""
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = fusionar(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def raiz_paquete(cfg: dict) -> Path:
    r = (cfg.get("rutas") or {}).get("raiz_paquete") or os.environ.get("BLOQUE_A_RAIZ")
    return Path(r).resolve() if r else DIR_EJECUTOR.parent


def ruta(cfg: dict, clave: str) -> Path:
    """Ruta de una carpeta del paquete (prompts, plantillas, archivos_operativos)."""
    valor = (cfg.get("rutas") or {}).get(clave)
    p = Path(valor)
    return p if p.is_absolute() else raiz_paquete(cfg) / p


def buscar_versionado(carpeta: Path, bases, extension: str = ".md") -> Path | None:
    """Busca «<base> - … V<x.y><ext>» (o «<base> - V<x.y><ext>», o «<base><ext>») con cualquier sufijo de versión.

    `bases` puede ser un texto o una lista de nombres alternativos (p. ej., el nombre V5.0 de un agente y su
    nombre anterior); se devuelve el archivo de versión más alta y, a igual versión, el del primer nombre de la
    lista. Robusto al renombrado de «V4.0» a «V5.0» (y posteriores), a mayúsculas y a variantes NFC/NFD de los
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
            if t == nb:
                candidatos.append(((0, 0), -orden, p.name, p))
                continue
            if not t.startswith(nb):
                continue
            m = re.fullmatch(r"\s*[-–—]\s*(?:.*?\s)?V(\d+)\.(\d+)\s*", tallo[len(base):], flags=re.IGNORECASE)
            if m:
                candidatos.append(((int(m.group(1)), int(m.group(2))), -orden, p.name, p))
    if not candidatos:
        return None
    return max(candidatos, key=lambda x: x[:3])[3]


def cargar_config(ruta_yaml: str | None = None, extra: dict | None = None) -> dict:
    with open(RUTA_CONFIG_POR_DEFECTO, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    if ruta_yaml:
        with open(ruta_yaml, encoding="utf-8") as fh:
            cfg = fusionar(cfg, yaml.safe_load(fh) or {})
    if extra:
        cfg = fusionar(cfg, extra)
    return cfg


_SIN_VALOR = object()
_CONFIG_POR_DEFECTO: dict | None = None


def config_por_defecto() -> dict:
    """`config/por_defecto.yaml` leído una vez (solo lectura: se devuelve el mismo objeto; no se modifica)."""
    global _CONFIG_POR_DEFECTO
    if _CONFIG_POR_DEFECTO is None:
        with open(RUTA_CONFIG_POR_DEFECTO, encoding="utf-8") as fh:
            _CONFIG_POR_DEFECTO = yaml.safe_load(fh)
    return _CONFIG_POR_DEFECTO


def _buscar(cfg: Any, partes: list) -> Any:
    v = cfg
    for p in partes:
        if not isinstance(v, dict) or p not in v:
            return _SIN_VALOR
        v = v[p]
    return v


def parametro(cfg: dict | None, ruta_clave: str) -> Any:
    """Valor de un parámetro de configuración por su ruta («seccion.clave»). T-65 (QA de T-53, H-08): el número sale
    siempre de la configuración recibida o, si una configuración parcial no lo trae, de `config/por_defecto.yaml`; nunca
    de un literal del código. Si tampoco está en `por_defecto.yaml`, falla cerrado con `KeyError`."""
    partes = ruta_clave.split(".")
    v = _buscar(cfg or {}, partes)
    if v is _SIN_VALOR:
        v = _buscar(config_por_defecto(), partes)
    if v is _SIN_VALOR or v is None:   # una clave presente pero nula tampoco vale (falla cerrado)
        raise KeyError(f"falta el parámetro de configuración `{ruta_clave}` (ni en la configuración ni en por_defecto.yaml)")
    return copy.deepcopy(v) if isinstance(v, (dict, list)) else v


def parametros_ht03(cfg: dict | None) -> dict:
    """Parámetros de HT-03 de la configuración (T-65, CS-11 de T-53): la sección `parametros_ht03` del YAML (o de
    `por_defecto.yaml`) con, encima, la clave interna `_parametros_ht03` que usan algunas pruebas para forzar un caso."""
    p = parametro(cfg, "parametros_ht03")
    # Misma regla de fusión que `ht03.fusionar_parametros`: un juego de pesos se sustituye entero
    for k, v in ((cfg or {}).get("_parametros_ht03") or {}).items():
        if isinstance(v, dict) and isinstance(p.get(k), dict):
            for k2, v2 in v.items():
                p[k][k2] = dict(v2) if isinstance(v2, dict) and isinstance(p[k].get(k2), dict) else v2
        else:
            p[k] = copy.deepcopy(v)
    return p


def sesiones_horizonte(cfg: dict | None, horizonte: str) -> int:
    """Sesiones hábiles de un horizonte (CA-14 de T-53): salen de `horizontes` y de `calendario` (sesiones por semana y por
    mes), no de una tabla repetida en el código."""
    h = parametro(cfg, f"horizontes.{horizonte}")
    if "sesiones" in h:
        return int(h["sesiones"])
    if "semanas" in h:
        return int(h["semanas"]) * int(parametro(cfg, "calendario.sesiones_por_semana"))
    if "meses" in h:
        return int(h["meses"]) * int(parametro(cfg, "calendario.sesiones_por_mes"))
    raise ValueError(f"horizonte {horizonte} mal configurado: {h!r}")


def modelo_de(cfg: dict, agente: str) -> str:
    m = cfg.get("modelos") or {}
    v = m.get(agente) or m.get("por_defecto")
    if not v:   # falla cerrado: sin modelo configurado no se llama a ninguno
        raise ValueError(f"sin modelo configurado para {agente} ni `modelos.por_defecto`")
    return str(v)


def max_tokens_de(cfg: dict, agente: str) -> int:
    m = cfg.get("max_tokens") or {}
    return int(m.get(agente) or m.get("por_defecto") or 8000)


def perfiles_activos(cfg: dict) -> list:
    """Tipos de activo con perfil activo (PA-01, T-66; `perfiles.activos`, [PROPUESTO]). Falla cerrado: sin la clave, o con
    un tipo desconocido, no se inventa un alcance."""
    act = (cfg.get("perfiles") or {}).get("activos")
    if not act:
        raise ValueError("configuración sin `perfiles.activos`: declara los tipos de activo con perfil activo")
    malos = [c for c in act if c not in CLASES]
    if malos:
        raise ValueError(f"`perfiles.activos` con tipos desconocidos: {malos}")
    return [c for c in CLASES if c in act]


def aplicabilidad(cfg: dict, clase: str, horizonte: str) -> str:
    tabla = cfg.get("_tabla_horizontes") or TABLA_HORIZONTES
    return tabla[clase][horizonte]
