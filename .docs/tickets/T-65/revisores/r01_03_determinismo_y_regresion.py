"""r01_03 · QA T-65 · determinismo (dos ejecuciones iguales) y regresión frente a HEAD (qué cambia en las salidas del ciclo).

Uso:  <python> r01_03_determinismo_y_regresion.py <dir_11_Ejecutor> <salida>
Ejecuta un backtest simulado de 4 semanas con los 12 tipos y 4 hilos y escribe un resumen JSON de todo lo que deja
(estado F*, RC, HA, entregables, senales/pronosticos/metricas), normalizando solo lo que es tiempo de reloj real.
Con dos salidas del mismo árbol: deben coincidir byte a byte. Con HEAD y T-65: se listan las diferencias.
"""
import hashlib
import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
EJ = Path(sys.argv[1]).resolve()
SAL = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(EJ))
from bloque_a.backtest import ejecutar_backtest  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402

todos = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
cfg = cargar_config(extra={"perfiles": {"activos": todos}, "paralelismo": {"hilos_analistas": 4},
                           "evaluacion": {"bootstrap_replicas": 200, "simulaciones_ece": 200}})
ejecutar_backtest(cfg, "2026-05-15", "2026-06-05", str(EJ / "ejemplos" / "datos_sinteticos"),
                  str(EJ / "config" / "universo_ejemplo.csv"), str(SAL))
RELOJ = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?([+-]\d\d:\d\d|Z)?")
resumen = {}
for p in sorted(SAL.rglob("*")):
    if p.is_file():
        try:
            t = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            t = p.read_bytes().hex()
        t = RELOJ.sub("<T>", t)
        resumen[str(p.relative_to(SAL))] = hashlib.sha256(t.encode()).hexdigest()
(SAL.parent / (SAL.name + ".json")).write_text(json.dumps(resumen, indent=1), encoding="utf-8")
print(f"{len(resumen)} archivos")
