"""HT-06 · Índice y caché del bloque.

- Búsqueda por identificadores y palabras en F1–F6 y RC (para respuestas N0 y reutilización).
- Caché de resultados idénticos (idempotencia): clave = hash de la petición; valor = respuesta.
"""
from __future__ import annotations

import hashlib
import json
import re
import threading
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional

RE_ID = re.compile(r"\b(?:RUN|QRY|OPP|TND|PRG|CLM|EVD|CALC|LEC|CERT|MET|RET|AJU)-\d{4}-\d{4,}\b")


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\-\s]", " ", t)


def clave_hash(*partes: Any) -> str:
    h = hashlib.sha256()
    for p in partes:
        h.update(json.dumps(p, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8"))
        h.update(b"\x1e")
    return h.hexdigest()


class CacheResultados:
    """Caché persistente (JSONL) de respuestas por clave de hash."""

    def __init__(self, ruta: Optional[Path]) -> None:
        self.ruta = Path(ruta) if ruta else None
        self._mem: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self.aciertos = 0
        if self.ruta and self.ruta.exists():
            for linea in self.ruta.read_text(encoding="utf-8").splitlines():
                if linea.strip():
                    d = json.loads(linea)
                    self._mem[d["clave"]] = d["valor"]

    def obtener(self, clave: str) -> Optional[Any]:
        with self._lock:
            if clave in self._mem:
                self.aciertos += 1
                return json.loads(json.dumps(self._mem[clave]))
        return None

    def guardar(self, clave: str, valor: Any) -> None:
        with self._lock:
            self._mem[clave] = valor
            if self.ruta:
                self.ruta.parent.mkdir(parents=True, exist_ok=True)
                with open(self.ruta, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps({"clave": clave, "valor": valor}, ensure_ascii=False, default=str) + "\n")


class Indice:
    """Índice de búsqueda sobre las entradas del almacén (vista as_of)."""

    def __init__(self, almacen, as_of=None, archivos=("F1", "F3", "F4", "F5", "F6", "RC")) -> None:
        self.docs: List[Dict] = []
        for a in archivos:
            for e in almacen.leer(a, as_of=as_of):
                texto = json.dumps(e, ensure_ascii=False, default=str)
                self.docs.append({"archivo": a, "entrada": e, "texto": normalizar(texto), "ids": set(RE_ID.findall(texto))})

    def por_id(self, ident: str) -> List[Dict]:
        return [d["entrada"] for d in self.docs if ident in d["ids"]]

    def buscar(self, consulta: str, max_resultados: int = 8) -> List[Dict]:
        ids = set(RE_ID.findall(consulta))
        terminos = [t for t in normalizar(consulta).split() if len(t) > 3]
        puntuados = []
        for d in self.docs:
            p = 5 * len(ids & d["ids"]) + sum(d["texto"].count(t) for t in terminos)
            if p:
                puntuados.append((p, d))
        puntuados.sort(key=lambda x: -x[0])
        return [{"archivo": d["archivo"], "entrada": d["entrada"], "puntuacion": p} for p, d in puntuados[:max_resultados]]
