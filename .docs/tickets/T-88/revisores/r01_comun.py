"""QA r01 de T-88 (revisor nuevo): utilidades comunes de los scripts r01_*.

Uso: los scripts r01_0N reciben --ejecutor RUTA (carpeta 11_Ejecutor a probar; por defecto la del árbol principal) para poder
compararla con 7feb697^ en un worktree. Se ejecutan con `.venv/bin/python -I`."""
import argparse
import json
import sys
import tempfile
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parents[4]


def preparar(descripcion: str):
    ap = argparse.ArgumentParser(description=descripcion)
    ap.add_argument("--ejecutor", default=str(RAIZ_REPO / "bloque_a" / "11_Ejecutor"))
    ap.add_argument("--rapido", action="store_true", help="menos repeticiones")
    a, resto = ap.parse_known_args()
    ej = Path(a.ejecutor).resolve()
    sys.path.insert(0, str(ej / "tests"))
    sys.path.insert(0, str(ej))
    import bloque_a
    assert Path(bloque_a.__file__).resolve().is_relative_to(ej), (bloque_a.__file__, ej)
    return a, resto, ej


def bloque(cfg, cliente=None, tmp=None):
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    from conftest import DATOS
    tmp = Path(tmp or tempfile.mkdtemp(prefix="qa_t88_"))
    return Bloque(cfg, ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cliente or MockClient(),
                  tmp / "estado", tmp / "ent")


def f5_presupuesto(b) -> dict:
    return [e for e in b.almacen.leer("F5") if "presupuesto" in e][-1]["presupuesto"]


def huella(obj) -> str:
    return json.dumps(obj, sort_keys=True, default=str)


class Marcador:
    def __init__(self):
        self.fallos = []
        self.n = 0

    def check(self, nombre, ok, detalle=""):
        self.n += 1
        print(("OK   " if ok else "FALLO") + f" {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)
        if not ok:
            self.fallos.append(nombre)

    def fin(self):
        print(f"== {self.n - len(self.fallos)}/{self.n} comprobaciones bien; fallos: {self.fallos}")
        return 1 if self.fallos else 0
