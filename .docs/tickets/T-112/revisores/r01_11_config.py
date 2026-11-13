"""QA r01 de T-112 · números de configuración: ¿leen las fichas la configuración del Motor o la de por defecto?

DEC-VOI-001 dice leer los umbrales de HT-03 de `parametros_ht03` (INC-T112-01) y ML-CAL-001/ML-PRED-001 las réplicas y el
nivel del bootstrap de `evaluacion`. Se sirve el mismo caso con un Motor cuya configuración cambia esos valores y se
compara con el de la configuración por defecto.
"""
import copy
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config, fusionar, parametro  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_11 configuración")


def motor(extra):
    return servicio.Motor(Almacen(Path(tempfile.mkdtemp())), C.Proveedor(), cargar_config(extra=fusionar({}, extra)))


def servir(m, f, i=0):
    c = servicio.CASOS_CONTROL[f][i]
    return m.servir({"operacion": f, "datos": copy.deepcopy(c.get("datos") or []), "parametros": dict(c.get("parametros") or {})}, "AG-18")


u = parametro(None, "parametros_ht03.umbrales")
otro = {k: (v + 8 if isinstance(v, (int, float)) else v) for k, v in u.items()}
m0, m1 = motor({}), motor({"parametros_ht03": {"umbrales": otro}})
print("umbrales HT-03 por defecto:", u, "· en la configuración del Motor:", parametro(m1.cfg, "parametros_ht03.umbrales"))
for i in range(len(servicio.CASOS_CONTROL["DEC-VOI-001"])):
    a, b = servir(m0, "DEC-VOI-001", i), servir(m1, "DEC-VOI-001", i)
    K.comprobar(f"DEC-VOI-001 caso {i}: con otros umbrales de HT-03 en la configuración del Motor, otra cifra",
                a.get("resultado") != b.get("resultado"), "misma cifra: la ficha usa los umbrales de por_defecto.yaml, no los del Motor")
m2 = motor({"evaluacion": {"bootstrap_replicas": 37, "nivel_ic": 0.8}})
for f in ("ML-CAL-001", "ML-PRED-001"):
    b = servir(m2, f, 1 if f == "ML-PRED-001" else 0)
    rep = str(b.get("resultado"))
    K.comprobar(f"{f}: réplicas y nivel del bootstrap de la configuración del Motor (37, 0,8)", "'replicas': 37" in rep,
                "usa los de por_defecto.yaml (`PARAMETROS_POR_DEFECTO` se calcula al importar el módulo)")
sys.exit(K.fin())
