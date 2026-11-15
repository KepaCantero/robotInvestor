"""QA r02 de T-125 (revisor sin contexto): ¿cambia algo en los ciclos que no traen pronósticos de fuentes?

Ejecuta, con el código del `11_Ejecutor` desde el que se lanza, tres escenarios sin ningún bloque `pronostico_fuente`
(backtest de las pruebas en `AS_OF`, dos ciclos en vivo y el ciclo semanal de todas las clases) y escribe en la salida estándar
un JSON con la última huella (`_hash`) y el número de entradas de cada archivo del almacén y la huella SHA-256 de cada
entregable. Lanzado con el código de antes (`fb3ccd4`) y con el de ahora, las dos salidas deben coincidir (los relojes del
almacén son simulados, así que todo es determinista).

Uso, desde `<11_Ejecutor de la versión a medir>`:  QA_TMP=<carpeta temporal> python <ruta>/r02_02_ciclos_sin_bloque.py > salida.json
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "tests"))
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, config_pruebas, nuevo_bloque  # noqa: E402

UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
TMP = os.environ.get("QA_TMP")


def huellas(b, carpeta):
    out = {a: [len(lista), lista[-1]["_hash"] if lista else None] for a, lista in sorted(b.almacen._entradas.items())}
    ent = {str(p.relative_to(carpeta)): hashlib.sha256(p.read_bytes()).hexdigest()
           for p in sorted((carpeta / "ent").rglob("*")) if p.is_file()}
    return {"almacen": out, "entregables": ent}


res = {}
for nombre, cfg, fechas, alcance in [("backtest_RV", config_pruebas(), [AS_OF], {"clases": ["RV"]}),
                                     ("vivo_RV_dos_ciclos", config_pruebas(modo="vivo"), ["2026-04-03", AS_OF], {"clases": ["RV"]}),
                                     ("backtest_todas", config_pruebas(), [AS_OF], None)]:
    # misma ruta en las dos ejecuciones: los entregables citan la ruta de sus hermanos
    carpeta = Path(TMP or tempfile.gettempdir()) / "qa10_t125_sin_bloque" / nombre
    shutil.rmtree(carpeta, ignore_errors=True)
    carpeta.mkdir(parents=True)
    b = nuevo_bloque(carpeta, UNIVERSO, cfg=cfg)
    estados = []
    for f in fechas:
        r = b.ciclo(f, alcance=alcance) if alcance else b.ciclo(f)
        estados.append(r["estado"])
    res[nombre] = {"estados": estados, **huellas(b, carpeta),
                   "estado_bloque_sin_clave_nueva": hashlib.sha256(json.dumps(
                       {k: v for k, v in b.estado().items() if k != "incidencias_escaladas"}, sort_keys=True, default=str).encode()).hexdigest()}
print(json.dumps(res, sort_keys=True, indent=1))
