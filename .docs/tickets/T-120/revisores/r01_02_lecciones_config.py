"""QA r01 de T-120 · El máximo de lecciones por encargo con configuraciones raras: ¿falla cerrado? Con 14 lecciones vigentes
de un tipo, qué devuelve `Evaluador.lecciones_vigentes` según `aprendizaje.lecciones_por_encargo`, y el argumento explícito.
También por el camino real: cuántas lecciones lleva un encargo CT-06 de un ciclo con la configuración cambiada.
Uso (desde bloque_a/11_Ejecutor de la copia): QA_TMP=<carpeta> python .../r01_02_lecciones_config.py"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config, parametro  # noqa: E402
from bloque_a.evaluador import Evaluador  # noqa: E402
from conftest import AS_OF, config_pruebas  # noqa: E402

tmp = Path(tempfile.mkdtemp(prefix="qa_t120_lec_", dir=os.environ.get("QA_TMP")))
a = Almacen(tmp / "a")
a.reloj.fijar(AS_OF)
N = 14
for i in range(1, N + 1):
    a.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": f"LEC-2026-{i:04d}", "fecha": AS_OF, "ambito": {"clase": "DIV"}, "nivel": "B",
                               "tipo": "CALIBRACION", "observacion": f"o{i}", "evidencia": [], "recomendacion": f"r{i}",
                               "fuerza": ["anecdotica", "recurrente", "estadistica"][i % 3], "n": 30, "caducidad": "2027-06-05", "estado": "VIGENTE",
                               "origen": "DETERMINISTA"})
print("por_defecto.yaml:", parametro(cargar_config(), "aprendizaje.lecciones_por_encargo"), "· lecciones vigentes del tipo:", N)


def prueba(nombre, cfg, **kw):
    try:
        r = Evaluador(a, None, None, cfg, None).lecciones_vigentes(AS_OF, "DIV", **kw)
        res = f"{len(r)} lecciones"
    except Exception as e:  # noqa: BLE001
        res = f"{type(e).__name__}: {str(e)[:90]}"
    print(f"   {nombre:44s} -> {res}")
    return res


abiertos = []
print("== configuración")
for nombre, v in {"10": 10, "4": 4, "1": 1, "0": 0, "-1": -1, "-3": -3, "-100": -100, "None": None, "texto «diez»": "diez", "texto «4»": "4", "texto vacío": "",
                  "2.7": 2.7, "1e3": 1e3, "NaN": float("nan"), "infinito": float("inf"), "True": True, "False": False, "lista [4]": [4], "dict": {"n": 4},
                  "10**30": 10 ** 30}.items():
    res = prueba(f"lecciones_por_encargo = {nombre}", config_pruebas(aprendizaje={"lecciones_por_encargo": v}))
    if isinstance(v, (int, float)) and not isinstance(v, bool) and v == v and v < 0 and res.endswith("lecciones") and int(res.split()[0]) > 0:
        abiertos.append(nombre)
prueba("sección aprendizaje vacía", config_pruebas(aprendizaje={}))
prueba("sección aprendizaje None", {**config_pruebas(), "aprendizaje": None})
prueba("configuración {}", {})
prueba("configuración None", None)
print("== argumento explícito (manda sobre la configuración)")
for kw in ({"max_n": 12}, {"max_n": 0}, {"max_n": -1}, {"max_n": None}, {"max_n": 100}):
    prueba(f"max_n={kw['max_n']} con configuración 4", config_pruebas(aprendizaje={"lecciones_por_encargo": 4}), **kw)
print("== orden: con máximo 4 salen las de más fuerza")
r = Evaluador(a, None, None, config_pruebas(aprendizaje={"lecciones_por_encargo": 4}), None).lecciones_vigentes(AS_OF, "DIV")
print("  ", [(x["id"][-2:], x["fuerza"]) for x in r])
print("valores negativos que NO fallan cerrado (dan lecciones, incluso más que el máximo del Documento 0):", abiertos)
