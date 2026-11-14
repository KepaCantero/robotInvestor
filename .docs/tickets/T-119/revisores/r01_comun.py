"""QA r01 de T-119: utilidades comunes de los scripts del revisor.

Uso: los scripts r01_NN_* reciben como primer argumento la carpeta del ejecutor que se prueba (por defecto, la del árbol
donde están): .venv/bin/python .docs/tickets/T-119/revisores/r01_NN_x.py [<copia>/bloque_a/11_Ejecutor]
El Motor se crea con un Almacén temporal: nada se escribe en el árbol.
"""
from __future__ import annotations

import copy
import sys
import tempfile
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parents[4]
P2 = ("FIR-CRED-001", "FX-BEER-001", "CMD-REAL-001", "REI-LEV-001", "CHR-ONCHAIN-001", "CHR-TOKEN-001", "PRV-PME-001",
      "PRV-CF-001", "ALT-HF-001", "ALT-AUC-001")


def preparar(argv: list[str]) -> Path:
    eje = Path(argv[1]).resolve() if len(argv) > 1 and not argv[1].startswith("-") else RAIZ_REPO / "bloque_a" / "11_Ejecutor"
    sys.path.insert(0, str(eje))
    import bloque_a  # noqa: F401
    assert Path(bloque_a.__file__).resolve().is_relative_to(eje), f"se importa {bloque_a.__file__}, no {eje}"
    return eje


class Proveedor:
    as_of = None
    nombre = "qa-r01"


def motor(cfg=None):
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import cargar_config
    from bloque_a.motor import servicio
    tmp = tempfile.mkdtemp(prefix="qa_t119_")
    return servicio.Motor(Almacen(Path(tmp)), Proveedor(), cfg if cfg is not None else cargar_config())


def peticion(ficha, valores=None, parametros=None, **extra):
    return {"operacion": ficha, "datos": [{"valores": copy.deepcopy(valores)}] if valores is not None else [],
            "parametros": copy.deepcopy(parametros) if parametros is not None else {}, "fecha_corte": None, **extra}


def servir(m, ficha, valores=None, parametros=None, solicitante="AG-21", **extra):
    return m.servir(peticion(ficha, valores, parametros, **extra), solicitante)


def caso(ficha, i=0):
    """(valores, parametros) del caso de control i de la ficha, copiados."""
    from bloque_a.motor import servicio
    c = servicio.CASOS_CONTROL[ficha][i]
    return copy.deepcopy(c["datos"][0]["valores"]), copy.deepcopy(dict(c.get("parametros") or {}))


def llamar(m, pet, sol="AG-21"):
    """(respuesta, excepción, entradas nuevas en RC)."""
    antes = len(m.almacen.leer("RC"))
    try:
        r, exc = m.servir(pet, sol), None
    except BaseException as e:  # noqa: BLE001
        r, exc = None, f"{type(e).__name__}: {str(e)[:120]}"
    return r, exc, len(m.almacen.leer("RC")) - antes


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
        return bool(cond)

    def cerca(self, nombre: str, a, b, tol: float = 1e-8) -> bool:
        ok = a is not None and b is not None and abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))
        return self.comprobar(nombre, ok, f"obtenido {a!r}, esperado {b!r}")

    def fin(self) -> int:
        tot = self.ok + len(self.mal)
        print(f"== {self.titulo}: {self.ok}/{tot}")
        for n in self.mal:
            print(f"   - {n}")
        return 0 if not self.mal else 1
