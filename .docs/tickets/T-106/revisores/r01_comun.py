"""QA r01 de T-106 · Piezas comunes de los scripts del revisor (no es una prueba; lo importan los r01_*.py).

- `preparar(raiz)`: pone el ejecutor de esa raíz en `sys.path` y comprueba que el Motor se importa de ahí.
- `entrada(caso)`: el `ent` que el Motor construye con los datos en línea de un caso de control.
- `motor(tmp)`: un Motor con almacén temporal y un proveedor sin series (los casos llevan sus datos en línea).
- `informe(nombre, ok, detalle)`: una línea OK/FALLO uniforme; `resumen()` devuelve el código de salida.

Uso: cada script acepta como primer argumento la raíz del repositorio (por defecto, la de este archivo), para poder
ejecutarlo contra una extracción limpia (`git worktree`) del commit revisado.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

M: dict = {}
RES: list[tuple[str, bool, str]] = []


def raiz_por_defecto() -> Path:
    return Path(__file__).resolve().parents[4]


def preparar(raiz: str | Path | None = None) -> dict:
    raiz = Path(raiz or raiz_por_defecto()).resolve()
    ejec = raiz / "bloque_a" / "11_Ejecutor"
    sys.path.insert(0, str(ejec))
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import cargar_config
    from bloque_a.motor import fichas_fon_der, fichas_mon_idx, fichas_tcv, servicio
    from bloque_a.motor.operaciones import ErrorFicha
    assert Path(servicio.__file__).resolve().is_relative_to(ejec.resolve()), servicio.__file__
    M.update(dict(raiz=raiz, ejec=ejec, Almacen=Almacen, cargar_config=cargar_config, servicio=servicio,
                  ErrorFicha=ErrorFicha, mods=(fichas_mon_idx, fichas_fon_der, fichas_tcv)))
    return M


class Proveedor:
    as_of = None
    nombre = "qa_r01"

    def cierres(self, *a, **k):  # pragma: no cover - los casos no piden series
        raise KeyError("sin series en la QA")

    def huella(self, *a, **k):
        return "qa"


def entrada(caso: dict) -> dict:
    ent: dict = {"series": {}, "series_rol": {}, "valores": {}}
    for d in caso.get("datos") or []:
        ent["valores"].update(copy.deepcopy(d.get("valores") or {}))
    return ent


def motor(tmp: str | Path):
    return M["servicio"].Motor(M["Almacen"](Path(tmp)), Proveedor(), M["cargar_config"]())


def informe(nombre: str, ok: bool, detalle: str = "") -> bool:
    RES.append((nombre, bool(ok), detalle))
    print(f"{'OK   ' if ok else 'FALLO'} {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)
    return ok


def resumen() -> int:
    fallos = [r for r in RES if not r[1]]
    print(f"\n{len(RES) - len(fallos)}/{len(RES)} comprobaciones OK; fallos: {[r[0] for r in fallos]}")
    return 1 if fallos else 0
