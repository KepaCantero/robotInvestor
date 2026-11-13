"""QA r01 de T-112: utilidades comunes de los scripts del revisor.

Uso: los scripts r01_* reciben como primer argumento la carpeta del ejecutor que se prueba (por defecto, la del repo):
    .venv/bin/python -I .docs/tickets/T-112/revisores/r01_02_oraculos_S.py <worktree>/bloque_a/11_Ejecutor
El Motor se crea con un Almacén temporal, así que nada se escribe en el árbol.
"""
from __future__ import annotations

import copy
import sys
import tempfile
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parents[4]


def preparar(argv: list[str]) -> Path:
    eje = Path(argv[1]).resolve() if len(argv) > 1 else RAIZ_REPO / "bloque_a" / "11_Ejecutor"
    sys.path.insert(0, str(eje))
    import bloque_a  # noqa: F401
    assert Path(bloque_a.__file__).resolve().is_relative_to(eje), f"se importa {bloque_a.__file__}, no {eje}"
    return eje


class Proveedor:
    as_of = None
    nombre = "qa-r01"


def motor():
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import cargar_config
    from bloque_a.motor import servicio
    tmp = tempfile.mkdtemp(prefix="qa_r01_")
    return servicio.Motor(Almacen(Path(tmp)), Proveedor(), cargar_config())


def servir(m, ficha, valores=None, parametros=None, solicitante="AG-21", **extra):
    pet = {"operacion": ficha, "datos": [{"valores": copy.deepcopy(valores)}] if valores is not None else [],
           "parametros": copy.deepcopy(parametros) if parametros is not None else {}, "fecha_corte": None, **extra}
    return m.servir(pet, solicitante)


class Contador:
    def __init__(self, titulo: str) -> None:
        self.titulo, self.ok, self.mal = titulo, 0, []

    def comprobar(self, nombre: str, cond: bool, detalle: str = "") -> bool:
        if cond:
            self.ok += 1
            print(f"  ok   {nombre}")
        else:
            self.mal.append(nombre)
            print(f"  FALLA {nombre} {detalle}")
        return cond

    def fin(self) -> int:
        tot = self.ok + len(self.mal)
        print(f"== {self.titulo}: {self.ok}/{tot}")
        for n in self.mal:
            print(f"   - {n}")
        return 0 if not self.mal else 1
