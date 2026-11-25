"""QA r01 de T-201 (revisor): sonda de entradas hostiles para los cambios no mecánicos.

Se ejecuta dentro de un árbol (`python r01_sonda.py <11_Ejecutor> <carpeta_tmp>`) y escribe en stdout, en JSON, el resultado
de cada caso: el valor devuelto (repr estable) o el tipo y el mensaje de la excepción. `r01_ataques.py` la lanza con el
código de la base y con el de T-201 y compara caso a caso. No escribe nada en el árbol (solo en la carpeta temporal).
"""
import json
import math
import sys
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
TMP = Path(sys.argv[2])
sys.path.insert(0, str(EJ))
sys.path.insert(0, str(EJ / "tests"))
sys.dont_write_bytecode = True

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from bloque_a import seguimiento  # noqa: E402
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config, ruta  # noqa: E402
from bloque_a.motor import evaluacion, operaciones, servicio  # noqa: E402

RES: dict[str, object] = {}


def _estable(x):
    if isinstance(x, float) and math.isnan(x):
        return "nan"
    if isinstance(x, dict):
        return {str(k): _estable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_estable(v) for v in x]
    if isinstance(x, np.generic):
        return _estable(x.item())
    if isinstance(x, Path):
        return "PATH:" + str(x).replace(str(EJ.parent), "<RAIZ>")
    return x if isinstance(x, (int, float, str, bool, type(None))) else repr(x)


def caso(nombre, f):
    try:
        RES[nombre] = {"ok": _estable(f())}
    except BaseException as e:   # noqa: BLE001 — la sonda registra cualquier excepción
        RES[nombre] = {"exc": type(e).__name__, "msg": str(e)[:200]}


# ---------------------------------------------------------------- configuracion.ruta
for i, cfg in enumerate([{}, {"rutas": None}, {"rutas": {}}, {"rutas": []}, {"rutas": {"x": None}}, {"rutas": {"x": ""}},
                         {"rutas": {"x": 0}}, {"rutas": {"x": []}}, {"rutas": {"x": False}}, {"rutas": {"x": "/abs"}},
                         {"rutas": {"x": "rel/dir"}}, {"rutas": "texto"}, {"rutas": {"x": Path("p")}}]):
    caso(f"ruta_{i}:{cfg!r}", lambda cfg=cfg: ruta(cfg, "x"))

# ---------------------------------------------------------------- seguimiento.b_agente
for clase in [None, "", "RV", "rv", "TCV", "XYZ", 0, False, 1.5, float("nan"), (), "AG-03"]:
    caso(f"b_agente:{clase!r}", lambda c=clase: seguimiento.b_agente(c))
for clase in [[], {}]:
    caso(f"b_agente:{clase!r}", lambda c=clase: seguimiento.b_agente(c))


# ---------------------------------------------------------------- seguimiento._cambio
class _B:
    def __init__(self, carpeta):
        self.almacen = Almacen(Path(carpeta))
        self.cfg = cargar_config()


s = seguimiento.Seguimientos(_B(TMP / "seg"))
for i, ct in enumerate([{}, {"seg_id": None}, {"seg_id": ""}, {"seg_id": 0}, {"seg_id": "SEG-2026-9999"}, {"seg_id": []},
                        {"seg_id": {}}, {"seg_id": False}]):
    caso(f"cambio_{i}:{ct!r}", lambda ct=ct: s._cambio(ct, "PAUSA", pd.Timestamp("2026-06-05")))

# ---------------------------------------------------------------- seguimiento._revision con F4 hostil (hitos)
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

b = nuevo_bloque(TMP / "rev", cargar_universo(RUTA_UNIVERSO_EJEMPLO))
b.fijar_fecha(AS_OF)
_estado_real = b.almacen.estado
HITOS = {
    "abierto": {"estado": "ABIERTO"},
    "abierto_con_resultado": {"estado": "ABIERTO", "resolucion": {"resultado_binario": 1}},
    "resuelto_1": {"estado": "RESUELTO", "resolucion": {"resultado_binario": 1}},
    "resuelto_0": {"estado": "RESUELTO", "resolucion": {"resultado_binario": 0}},
    "resuelto_texto0": {"estado": "RESUELTO", "resolucion": {"resultado_binario": "0"}},
    "resuelto_None": {"estado": "RESUELTO", "resolucion": {"resultado_binario": None}},
    "resuelto_sin": {"estado": "RESUELTO"},
    "resuelto_lista": {"estado": "RESUELTO", "resolucion": []},
    "resuelto_texto": {"estado": "RESUELTO", "resolucion": "x"},
    "abierto_texto": {"estado": "ABIERTO", "resolucion": "x"},
    "estado_None": {"estado": None, "resolucion": {"resultado_binario": 1}},
    "estado_lista": {"estado": ["RESUELTO"]},
    "estado_num": {"estado": 1},
    "vacio": {},
    "anulado": {"estado": "ANULADO", "fecha_resolucion": "2026-01-01"},
}
# almacen.estado solo devuelve diccionarios con su clave (prg_id): un hito que no es un diccionario no puede llegar a F4
for nombre, hito in HITOS.items():
    hito = {"prg_id": "HIT-X", "es_hito": True, "tipo_entrada": "ALTA", **hito}
    for hit_ids in (["HIT-X"], ["HIT-X", "HIT-FALTA"], [None], "HIT-X", None, [["HIT-X"]]):
        f4 = {"PRG-1": {"prg_id": "PRG-1", "opp_id": "OPP-1", "tipo_entrada": "ALTA", "estado": "ABIERTO", "horizonte": "H2",
                        "hit_ids": hit_ids}, "HIT-X": hito}

        def _estado(archivo, *a, f4=f4, **k):
            return f4 if archivo == "F4" else _estado_real(archivo, *a, **k)

        b.almacen.estado = _estado
        opp = {"opp_id": "OPP-1", "clase": "DIV", "indicador_seguimiento": {"simbolo": "EURUSD=X"}}
        caso(f"revision:{nombre}:{hit_ids!r}",
             lambda opp=opp: b.seguimientos._revision({"fecha_alta": "2026-05-29"}, opp, pd.Timestamp(AS_OF))["pronosticos_abiertos"])
b.almacen.estado = _estado_real

# ---------------------------------------------------------------- motor: acierto_direccional y diferencial_rentabilidades
for i, o in enumerate([[], [1, 0, 1, 1], (1, 0), np.array([1, 1, 0]), [True, False, True], [1.7, 0.2], [2, -1], None, "10",
                       [None], [[1, 0]], np.array([], dtype=float), [float("nan")], range(5), [1.7, 1.7, 0.2], np.array([0.9, 0.9])]):
    caso(f"acierto_{i}:{o!r}", lambda o=o: evaluacion.acierto_direccional(o))
H5 = [0.01, 0.02, 0.03, 0.04, 0.05]
for i, args in enumerate([(0.06, 0.02, None), (0.06, 0.02, []), (0.06, 0.02, H5[:4]), (0.06, 0.02, H5), (0.06, 0.02, np.array(H5)),
                          (0.06, 0.02, H5 + [float("nan")]), (float("nan"), 0.02, H5), (float("inf"), 0.02, H5), (0.06, None, H5),
                          ("0.06", 0.02, H5), (0.06, 0.02, ["a"] * 5), (0.06, 0.02, [0.0] * 5), (0, 0, H5), (-1e308, 1e308, H5)]):
    for en_pb in (False, True):
        caso(f"diferencial_{i}_{en_pb}:{args!r}", lambda a=args, p=en_pb: operaciones.diferencial_rentabilidades(*a, en_pb=p))


# ---------------------------------------------------------------- Motor.servir: ficha None, rara, desconocida
class _P:
    as_of = None
    nombre = "pruebas"


m = servicio.Motor(Almacen(TMP / "motor"), _P(), cargar_config())
for i, pet in enumerate([{"operacion": None, "datos": []}, {"operacion": "", "datos": []}, {"operacion": {"ficha_id": None}, "datos": []},
                         {"operacion": {}, "datos": []}, {"datos": []}, {"operacion": 5, "datos": []}, {"operacion": [], "datos": []},
                         {"operacion": "NOPE-001", "datos": []}, {"operacion": "REG-HMM-001", "datos": []},
                         {"operacion": "ML-PRED-001", "datos": []}, {"operacion": {"ficha_id": "FX-REGIME-001"}, "datos": []}]):
    def _servir(pet=pet):
        r = m.servir(pet, "AG-02")
        return {k: r.get(k) for k in ("estado", "motivo", "alternativa", "detalle", "cache_hit")}
    caso(f"servir_{i}:{pet!r}", _servir)

json.dump(RES, sys.stdout, ensure_ascii=False, indent=0, sort_keys=True, default=repr)
