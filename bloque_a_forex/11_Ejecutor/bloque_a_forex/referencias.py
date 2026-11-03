"""Lectura de F7, F8, F9 (archivos de referencias del Bloque A Forex: áreas TX-, TMX- y TFX-) y FM (Markdown de
05_Archivos_operativos) con el lector de fichas de HT-02.

En backtest solo se ofrecen a los agentes referencias cuyo año (campo «Año» o cita) es ≤ año as_of; las
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
    "F7": "Documentación para el Analizador de Oportunidades en Divisas",
    "F8": "Documentación para el Motor de Cálculo Avanzado (Forex)",
    "F9": "Registro de Fuentes para el Analizador de Oportunidades en Divisas",
    "FM": "Fondo Metodológico Bibliográfico",
}
RE_AREA = re.compile(r"\b(TX-\d{2}|TMX-\d{2}|TFX-\d{2}|MB-\d{2})\b")


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
# Áreas de F7 (TX-), F8 (TMX-) y F9 (TFX-) que consulta cada segmento y cada capa transversal (Anexo D del Documento 0 Forex)
TEMATICAS_SEGMENTO = {
    "G10N": ["TX-02", "TX-04", "TX-12", "TX-03", "TFX-01", "TFX-05"],
    "G10M": ["TX-11", "TX-04", "TX-02", "TX-03", "TFX-01", "TFX-05"],
    "EMAS": ["TX-10", "TX-08", "TX-07", "TX-14", "TFX-02", "TFX-04"],
    "EMLA": ["TX-10", "TX-11", "TX-08", "TX-09", "TFX-02", "TFX-09"],
    "EMEA": ["TX-10", "TX-09", "TX-14", "TX-08", "TFX-02", "TFX-09"],
    "ESTR": ["TX-05", "TX-04", "TX-13", "TMX-06", "TMX-07", "TFX-06", "TFX-10"],
    "BCM": ["TX-02", "TX-07", "TX-01", "TFX-01", "TFX-02", "TFX-03"],
    "PFV": ["TX-06", "TX-09", "TMX-05", "TMX-02", "TFX-05", "TFX-06"],
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


class Referencias:
    def __init__(self, cfg: Dict, rutas: Optional[Dict[str, Path]] = None) -> None:
        base = ruta(cfg, "archivos_operativos")
        self.rutas = rutas or {k: localizar(base, v) for k, v in ARCHIVOS_REF.items()}
        self.fichas: Dict[str, List[Dict]] = {}
        for k, p in self.rutas.items():
            self.fichas[k] = []
            if not Path(p).exists():
                continue
            lineas = Path(p).read_text(encoding="utf-8").splitlines()
            seccion = {}
            actual = None
            for n, ln in enumerate(lineas):      # área de la sección «## TX-02 …» en que está cada ficha
                if ln.startswith("## "):
                    ms = RE_AREA.search(ln)
                    actual = ms.group(1) if ms else None
                seccion[n] = actual
            for f in ht02.leer_fichas(lineas):
                tem = f.campo("Temática", "Ámbito metodológico", "Área") or ""
                m = RE_AREA.search(tem)
                if m is None and seccion.get(f.linea_inicio):
                    m = re.match(r"(.*)", seccion[f.linea_inicio])
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

    def para_segmento(self, segmento: str, as_of, modo: str, max_n: int = 6, archivos=("F7", "F9")) -> Dict:
        """Referencias del segmento ordenadas por Q (desc.), filtradas por año en backtest y saneadas (R9)."""
        anio_lim = int(str(as_of)[:4])
        tem = set(TEMATICAS_SEGMENTO.get(segmento, []))
        sel, hallazgos = [], []
        for a in archivos:
            cand = [r for r in self.fichas.get(a, []) if r["tematica"] in tem]
            if modo == "backtest":
                cand = [r for r in cand if (r["anio"] is not None and r["anio"] <= anio_lim) or (a == "F9" and r["anio"] is None)]
            cand.sort(key=lambda r: (-(r["q"] or 0), r["ref_id"]))
            for r in cand[:max_n // len(archivos) + 1]:
                titulo, h = sanear_contenido_externo(r["titulo"], f"{a}:{r['ref_id']}")
                hallazgos += h
                sel.append({"ref_id": f"REF-{r['ref_id']}", "archivo": a, "titulo": titulo, "q": r["q"], "nivel": r["nivel"],
                            "tematica": r["tematica"], "anio": r["anio"],
                            "nota": "canal sin fecha: solo catálogo, contenido no accesible en backtest" if (a == "F9" and modo == "backtest") else None})
        return {"referencias": sel[:max_n], "hallazgos_r9": hallazgos}
