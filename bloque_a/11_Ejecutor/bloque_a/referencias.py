"""Lectura de F7, F8, F9 y FM (Markdown de 05_Archivos_operativos) con el lector de fichas de HT-02.

En backtest solo se ofrecen a los agentes referencias conocibles al corte; cuando solo consta el año se usa el 31 de diciembre; las
fuentes de F9 sin año (canales institucionales) se ofrecen como catálogo, sin contenido.
Todo texto pasa por el saneamiento R9 antes de llegar a un agente.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

from .configuracion import ruta
from .contratos import sanear_contenido_externo
from .herramientas import ht02

# Prefijos de nombre; se toma el archivo con la versión más alta («… - V3.1.md», «… - V3.2.md», …)
ARCHIVOS_REF = {
    "F7": "Documentación para el Analizador de Tendencias de Inversión",
    "F8": "Documentación para el Motor de Cálculo Avanzado",
    "F9": "Registro de Fuentes para el Analizador de Tendencias de Inversión",
    "FM": "Fondo Metodológico Bibliográfico",
}


def localizar(base: Path, prefijo: str) -> Path:
    """Devuelve el archivo «<prefijo> - Vx.y.md» de versión más alta; si no hay, la ruta esperada (inexistente)."""
    import unicodedata
    def norm(t: str) -> str:
        return unicodedata.normalize("NFC", t)
    cands = []
    for f in Path(base).glob("*.md"):
        n = norm(f.name)
        if n.startswith(norm(prefijo) + " - V"):
            m = re.search(r" - V(\d+)\.(\d+)\.md$", n)
            if m:
                cands.append(((int(m.group(1)), int(m.group(2))), f))
    if not cands:
        return Path(base) / f"{prefijo} - V0.0.md"
    return max(cands)[1]
TEMATICAS_CLASE = {
    "RV": ["TA-05", "TF-05", "TF-06", "TF-04"], "RF": ["TA-06", "TF-01", "TF-06"], "DIV": ["TA-07", "TF-01", "TF-06"],
    "MP": ["TA-08", "TF-08"], "INM": ["TA-09", "TF-09"], "CRI": ["TA-10", "TF-10"], "ALT": ["TA-11", "TF-11", "TF-04"],
    "IDX": ["TA-19", "TM-15", "TF-15", "TA-05", "TF-06"], "FON": ["TA-20", "TM-16", "TF-16", "TA-11", "TF-04"],
    "DER": ["TA-21", "TM-06", "TF-17", "TF-06"], "MON": ["TA-22", "TM-17", "TF-18", "TF-01"],
    "TCV": ["TA-23", "TM-18", "TF-19", "TA-06", "TF-01"],
}
RE_ANIO = re.compile(r"\b(19[5-9]\d|20[0-4]\d)\b")


def _anio(ficha) -> Optional[int]:
    for campo in ("Año", "Cita normalizada", "Versión"):
        v = ficha.campo(campo)
        if v:
            m = RE_ANIO.search(v)
            if m:
                return int(m.group(1))
    return None


def conocible_desde(ref: dict) -> str | None:
    """Cota superior conservadora: la ficha solo acredita el año, no el día de publicación."""
    anio = ref.get("anio")
    return f"{anio:04d}-12-31" if anio is not None else None


class Referencias:
    def __init__(self, cfg: Dict, rutas: Optional[Dict[str, Path]] = None) -> None:
        base = ruta(cfg, "archivos_operativos")
        self.rutas = rutas or {k: localizar(base, v) for k, v in ARCHIVOS_REF.items()}
        self.fichas: Dict[str, List[Dict]] = {}
        for k, p in self.rutas.items():
            self.fichas[k] = []
            if not Path(p).exists():
                continue
            for f in ht02.leer_fichas(Path(p).read_text(encoding="utf-8").splitlines()):
                tem = f.campo("Temática", "Ámbito metodológico") or ""
                m = re.search(r"\b(T[AMF]-\d{2}|MB-\d{2})\b", tem)
                self.fichas[k].append({"ref_id": f.id, "archivo": k, "titulo": f.titulo, "q": f.q, "nivel": f.nivel,
                                       "tematica": m.group(1) if m else None, "anio": _anio(f),
                                       "tipologia": (f.campo("Tipología", "Tipo de documento", "Tipo de fuente") or "")[:80],
                                       "estado_enlace": f.campo("Estado del enlace")})

    def por_id(self, ref_id: str) -> Optional[Dict]:
        rid = ref_id.replace("REF-", "")
        for lst in self.fichas.values():
            for r in lst:
                if r["ref_id"] == rid:
                    return r
        return None

    def para_clase(self, clase: str, as_of, modo: str, max_n: int = 6, archivos=("F7", "F9")) -> Dict:
        """Referencias de la clase ordenadas por Q (desc.), filtradas por año en backtest y saneadas (R9)."""
        corte = str(as_of)[:10]
        tem = set(TEMATICAS_CLASE.get(clase, []))
        sel, hallazgos = [], []
        for a in archivos:
            cand = [r for r in self.fichas.get(a, []) if r["tematica"] in tem]
            if modo == "backtest":
                cand = [r for r in cand if ((conocible_desde(r) or "9999") <= corte) or (a == "F9" and r["anio"] is None)]
            cand.sort(key=lambda r: (-(r["q"] or 0), r["ref_id"]))
            for r in cand[:max_n // len(archivos) + 1]:
                titulo, h = sanear_contenido_externo(r["titulo"], f"{a}:{r['ref_id']}")
                hallazgos += h
                sel.append({"ref_id": f"REF-{r['ref_id']}", "archivo": a, "titulo": titulo, "q": r["q"], "nivel": r["nivel"],
                            "tematica": r["tematica"], "anio": r["anio"],
                            "nota": "canal sin fecha: solo catálogo, contenido no accesible en backtest" if (a == "F9" and modo == "backtest") else None})
        return {"referencias": sel[:max_n], "hallazgos_r9": hallazgos}
