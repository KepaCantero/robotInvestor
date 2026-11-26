"""Lectura de F7, F8, F9 y FM (Markdown de 05_Archivos_operativos) con el lector de fichas de HT-02.

En backtest solo se ofrecen a los agentes referencias conocibles al corte; cuando solo consta el año se usa el 31 de diciembre; las
fuentes de F9 sin año (canales institucionales) se ofrecen como catálogo, sin contenido.
Todo texto pasa por el saneamiento R9 antes de llegar a un agente.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from .configuracion import parametro, ruta
from .contratos import MARCA_RETIRADA, sanear_contenido_externo
from .herramientas import ht02

# Prefijos de nombre; se toma el archivo con la versión más alta («… - V3.1.md», «… - V3.2.md», …)
ARCHIVOS_REF = {
    "F7": "Documentación para el Analizador de Tendencias de Inversión",
    "F8": "Documentación para el Motor de Cálculo Avanzado",
    "F9": "Registro de Fuentes para el Analizador de Tendencias de Inversión",
    "FM": "Fondo Metodológico Bibliográfico",
}


def nivel_de_q(q, cfg=None):
    for nivel in ("A", "B", "C"):
        if q >= parametro(cfg, f"referencias.niveles_q.{nivel}"):
            return nivel
    return "D"


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


def metadatos_ficha(ficha, archivo):
    tem = ficha.campo("Temática", "Ámbito metodológico") or ""
    m = re.search(r"\b(T[AMF]-\d{2}|MB-\d{2})\b", tem)
    return {"ref_id": ficha.id, "archivo": archivo, "titulo": ficha.titulo, "q": ficha.q, "nivel": ficha.nivel,
            "tematica": m.group(1) if m else None, "anio": _anio(ficha),
            "tipologia": (ficha.campo("Tipología", "Tipo de documento", "Tipo de fuente") or "")[:80],
            "fuente_original": ficha.campo("Fuente original", "Referencia original"),
            "estado_enlace": ficha.campo("Estado del enlace")}


MARCA_HISTORIAL = "<!-- RI-ficha-retirada-v1 "


def lineas_registro(lineas):
    nivel = 0
    for numero, linea in enumerate(lineas, 1):
        titulo = ht02.modulo.RE_TITULO.match(linea)
        if titulo:
            profundidad = len(titulo.group(1))
            if "registro de bajas" in ht02.modulo._norm_clave(linea):
                nivel = profundidad
            elif profundidad <= nivel:
                nivel = 0
        elif nivel:
            yield numero, linea


def historial_bajas(lineas, bajas, archivo):
    """Solo admite instantáneas acompañadas por su baja en la tabla del mismo catálogo."""
    for numero, linea in lineas_registro(lineas):
        texto = linea.rstrip()
        if texto.startswith(MARCA_HISTORIAL) and texto.endswith(" -->"):
            try:
                registro = json.loads(texto[len(MARCA_HISTORIAL):-4])
                ficha = registro["ficha"]
                clave = (ficha["ref_id"], registro["fecha"])
                coincide = ficha["archivo"] == archivo and clave in bajas
            except (TypeError, ValueError, KeyError) as exc:
                raise ValueError(f"{archivo}, fila {numero}: instantánea de baja inválida") from exc
            if coincide:
                yield registro


class Referencias:
    registro_bajas_f9: Path | None = None

    def __init__(self, cfg: Dict, rutas: Optional[Dict[str, Path]] = None, *, reloj=None) -> None:
        self.reloj = reloj
        base = ruta(cfg, "archivos_operativos")
        self.rutas = rutas or {k: localizar(base, v) for k, v in ARCHIVOS_REF.items()}
        self.fichas: Dict[str, List[Dict]] = {}
        self.historicas: dict[str, list[dict]] = {}
        self.bajas: dict[str, list[tuple[str, str]]] = {}
        self.motivos_bajas: dict[tuple[str, str, str], str] = {}
        self._firmas: dict[str, tuple | None] = {}
        self.actualizar()

    def actualizar(self):
        from .mantenimiento_fuentes import CUSTODIOS, detalle_bajas
        for k, p in self.rutas.items():
            p = Path(p)
            stat = p.stat() if p.exists() else None
            firma = (stat.st_ino, stat.st_mtime_ns, stat.st_size) if stat else None
            if k in self._firmas and firma == self._firmas[k]:
                continue
            self.fichas[k] = []
            self.historicas[k] = []
            self.bajas[k] = []
            self.motivos_bajas = {clave: m for clave, m in self.motivos_bajas.items() if clave[0] != k}
            if not stat:
                self._firmas[k] = firma
                continue
            lineas = Path(p).read_text(encoding="utf-8").splitlines()
            if k in CUSTODIOS:
                for rid, dia, motivo in detalle_bajas(lineas, p):
                    self.bajas[k].append((rid, dia))
                    self.motivos_bajas[k, "REF-" + rid, dia] = motivo
                self.historicas[k] = list(historial_bajas(lineas, set(self.bajas[k]), k))
            for f in ht02.leer_fichas(lineas):
                self.fichas[k].append(metadatos_ficha(f, k))

            self._firmas[k] = firma

    def retiradas_f9(self, as_of):
        from .mantenimiento_fuentes import bajas_registradas
        ruta = self.registro_bajas_f9
        if ruta is None or not ruta.exists():
            return set()
        return {"REF-" + rid for rid, dia in bajas_registradas(ruta.read_text(encoding="utf-8").splitlines())
                if dia <= str(as_of)[:10]}

    def _fichas_al_corte(self, archivo, as_of):
        yield from self.fichas.get(archivo, [])
        for registro in self.historicas.get(archivo, []):
            if str(as_of)[:10] < registro["fecha"]:
                yield registro["ficha"]

    def por_id(self, ref_id: str, as_of=None) -> Optional[Dict]:
        if as_of is None:
            as_of = self.reloj.fecha if self.reloj is not None else "9999-12-31"
        rid = ref_id.replace("REF-", "")
        for archivo in self.fichas:
            for r in self._fichas_al_corte(archivo, as_of):
                if r["ref_id"] == rid:
                    if r["archivo"] == "F9" and "REF-" + rid in self.retiradas_f9(as_of):
                        return {**r, "estado_enlace": "RETIRADA"}
                    return r
        return None

    def para_clase(self, clase: str, as_of, modo: str, max_n: int = 6, archivos=("F7", "F9")) -> Dict:
        """Referencias de la clase ordenadas por Q (desc.), filtradas por año en backtest y saneadas (R9)."""
        corte = str(as_of)[:10]
        tem = set(TEMATICAS_CLASE.get(clase, []))
        sel, hallazgos = [], []
        retiradas = self.retiradas_f9(as_of)
        for a in archivos:
            cand = [r for r in self._fichas_al_corte(a, corte) if r["tematica"] in tem and "REF-" + r["ref_id"] not in retiradas]
            if modo == "backtest":
                cand = [r for r in cand if ((conocible_desde(r) or "9999") <= corte) or (a == "F9" and r["anio"] is None)]
            cand.sort(key=lambda r: (-(r["q"] or 0), r["ref_id"]))
            for r in cand[:max_n // len(archivos) + 1]:
                titulo, h = sanear_contenido_externo(r["titulo"], f"{a}:{r['ref_id']}")
                hallazgos += h
                sel.append({"ref_id": f"REF-{r['ref_id']}", "archivo": a, "titulo": MARCA_RETIRADA if h else titulo, "q": r["q"], "nivel": r["nivel"],
                            "tematica": r["tematica"], "anio": r["anio"],
                            "nota": "canal sin fecha: solo catálogo, contenido no accesible en backtest" if (a == "F9" and modo == "backtest") else None})
        return {"referencias": sel[:max_n], "hallazgos_r9": hallazgos}
