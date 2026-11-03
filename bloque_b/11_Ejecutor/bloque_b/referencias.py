"""HT-06 (parte de referencias): índice de F7, F8, F9 y FM (Markdown de 05_Archivos_operativos) con el lector de fichas
de HT-02. Ofrece a cada agente las mejores referencias de sus áreas (correspondencia D.4 del Documento 0), ordenadas por
calidad Q. En backtest solo se ofrecen referencias con año ≤ año de la fecha de corte (las fuentes de F9 sin año se
ofrecen como catálogo). Todo texto pasa por el saneamiento R12 antes de llegar a un agente."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from .configuracion import ruta
from .contratos import sanear
from .herramientas import ht02

ARCHIVOS_REF = {
    "F7": "Documentación para el Analizador de Mercados",
    "F8": "Documentación para el Motor de Cálculo Avanzado de Mercados",
    "F9": "Registro de Fuentes para el Analizador de Mercados",
    "FM": "Fondo Metodológico Bibliográfico",
}
# Anexo D.4: dimensión → áreas de F7 (TB), F8 (TMB) y F9 (TFB)
AREAS_DIM = {
    "D1": ["TB-01", "TB-11", "TMB-04", "TFB-01", "TFB-04"], "D2": ["TB-04", "TB-05", "TMB-02", "TMB-03", "TFB-01", "TFB-04", "TFB-05"],
    "D3": ["TB-03", "TB-13", "TMB-05", "TMB-10", "TFB-05", "TFB-12"], "D4": ["TB-01", "TB-02", "TB-03", "TMB-04", "TMB-10", "TFB-03", "TFB-04"],
    "D5": ["TB-05", "TMB-03", "TMB-05", "TFB-09"], "D6": ["TB-09", "TMB-09", "TFB-03", "TFB-16"],
    "D7": ["TB-06", "TB-16", "TMB-01", "TMB-02", "TFB-02"], "D8": ["TB-07", "TB-08", "TB-12", "TMB-06", "TFB-07"],
    "D9": ["TB-07", "TB-17", "TMB-06", "TFB-06", "TFB-08"], "D10": ["TB-19", "TMB-01", "TMB-12", "TFB-15", "TFB-10"],
    "D11": ["TB-10", "TMB-09", "TFB-17"], "D12": ["TB-21", "TB-22", "TMB-08", "TMB-09", "TFB-11"],
    "SEL": ["TB-17", "TB-18", "TB-20", "TMB-07", "TMB-11", "TMB-13", "TFB-06", "TFB-07", "TFB-08", "TFB-14"],
}
RE_AREA = re.compile(r"\b(TB-\d{2}|TMB-\d{2}|TFB-\d{2})\b")
RE_ANIO = re.compile(r"\b(19[5-9]\d|20[0-4]\d)\b")


def localizar(base: Path, prefijo: str) -> Optional[Path]:
    def n(t: str) -> str:
        return unicodedata.normalize("NFC", t)
    cands = []
    for f in Path(base).glob("*.md"):
        nom = n(f.name)
        if nom.startswith(n(prefijo) + " - V"):
            m = re.search(r" - V(\d+)\.(\d+)\.md$", nom)
            if m:
                cands.append(((int(m.group(1)), int(m.group(2))), f))
    return max(cands)[1] if cands else None


class Referencias:
    def __init__(self, cfg: Dict, rutas: Optional[Dict[str, Path]] = None) -> None:
        base = ruta(cfg, "archivos_operativos")
        self.rutas = rutas or {k: localizar(base, v) for k, v in ARCHIVOS_REF.items()}
        self.fichas: Dict[str, List[Dict]] = {}
        for k, p in self.rutas.items():
            self.fichas[k] = []
            if not p or not Path(p).exists():
                continue
            for f in ht02.leer_fichas(Path(p).read_text(encoding="utf-8").splitlines()):
                tem = f.campo("Temática", "Ámbito metodológico") or ""
                m = RE_AREA.search(tem)
                anio = None
                v = f.campo("Año", "Cita normalizada", "Versión")
                if v and RE_ANIO.search(v):
                    anio = int(RE_ANIO.search(v).group(1))
                self.fichas[k].append({"ref_id": f.id, "archivo": k, "titulo": f.titulo, "q": f.q, "nivel": f.nivel,
                                       "area": m.group(1) if m else None, "anio": anio,
                                       "acceso": (f.campo("Acceso", "Restricciones de uso") or "")[:120],
                                       "url": (f.campo("URL", "DOI / URL", "Canal oficial (URL raíz)") or "")[:200]})

    def recuento(self) -> Dict[str, int]:
        return {k: len(v) for k, v in self.fichas.items()}

    def por_areas(self, areas: Sequence[str], n: int = 6, anio_max: Optional[int] = None) -> List[Dict]:
        out = []
        for lst in self.fichas.values():
            for f in lst:
                if f["area"] in areas and (anio_max is None or f["anio"] is None or f["anio"] <= anio_max):
                    out.append(f)
        out.sort(key=lambda f: (-(f["q"] or 0), f["ref_id"]))
        return sanear([{k: f[k] for k in ("ref_id", "archivo", "titulo", "q", "nivel", "area", "anio")} for f in out[:n]])

    def por_id(self, ref_id: str) -> Optional[Dict]:
        for lst in self.fichas.values():
            for f in lst:
                if f["ref_id"] == ref_id:
                    return f
        return None
