"""QA r01 de T-118: utilidades comunes de los scripts del revisor.

Uso: .venv/bin/python -I .docs/tickets/T-118/revisores/r01_NN_*.py [carpeta del ejecutor]
El Motor se crea con un Almacén temporal: nada se escribe en el árbol.
"""
from __future__ import annotations

import copy
import sys
import tempfile
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parents[4]


def preparar(argv: list[str]) -> Path:
    args = [a for a in argv[1:] if not a.startswith("--") and Path(a).is_dir()]
    eje = Path(args[0]).resolve() if args else RAIZ_REPO / "bloque_a" / "11_Ejecutor"
    sys.path.insert(0, str(eje))
    import bloque_a  # noqa: F401
    assert Path(bloque_a.__file__).resolve().is_relative_to(eje), f"se importa {bloque_a.__file__}, no {eje}"
    return eje


class Proveedor:
    as_of = None
    nombre = "qa-t118-r01"


def motor(carpeta=None, **extra):
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import cargar_config
    from bloque_a.motor import servicio
    carpeta = carpeta or tempfile.mkdtemp(prefix="qa_t118_")
    return servicio.Motor(Almacen(Path(carpeta)), Proveedor(), cargar_config(extra=extra or None))


def peticion(ficha, i=0, **extra):
    from bloque_a.motor import servicio
    caso = servicio.CASOS_CONTROL[ficha][i]
    return {"operacion": ficha, "datos": copy.deepcopy(caso["datos"]), "parametros": dict(caso.get("parametros") or {}), **extra}


def valores(ficha, i=0):
    from bloque_a.motor import servicio
    v = {}
    for d in servicio.CASOS_CONTROL[ficha][i]["datos"]:
        v.update(copy.deepcopy(d.get("valores") or {}))
    return v


def servir_contando(m, pet, solicitante="AG-18"):
    """(respuesta o None, excepción o None, entradas nuevas en RC)."""
    antes = len(m.almacen.leer("RC"))
    try:
        r, exc = m.servir(pet, solicitante), None
    except BaseException as e:  # noqa: BLE001 — lo que se busca es justo lo que escapa
        if isinstance(e, KeyboardInterrupt):
            raise
        r, exc = None, e
    return r, exc, len(m.almacen.leer("RC")) - antes


class Contador:
    def __init__(self, titulo: str) -> None:
        self.titulo, self.ok, self.mal = titulo, 0, []

    def comprobar(self, nombre: str, cond: bool, detalle: str = "") -> bool:
        if cond:
            self.ok += 1
            print(f"  ok    {nombre}")
        else:
            self.mal.append(nombre)
            print(f"  FALLA {nombre} {detalle}")
        sys.stdout.flush()
        return bool(cond)

    def fin(self) -> int:
        tot = self.ok + len(self.mal)
        print(f"== {self.titulo}: {self.ok}/{tot}")
        for n in self.mal:
            print(f"   - {n}")
        return 0 if not self.mal else 1
