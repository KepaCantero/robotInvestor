"""QA r01 de T-141: los días de cierre de TARGET (el BCE no publica: 1-1, Viernes Santo, Lunes de Pascua, 1-5, 25-12 y
26-12) frente a la frescura de PS2 del Bloque A (H1 en sesiones, `ps2_festivos`), los huecos reales de la serie y
la lectura en el borde de `fecha_publicacion`. Usa `comprobar_datos_a.comprobar` y `ProveedorCSV` del Bloque A.

Uso (desde la raíz): <python> -I .docs/tickets/T-141/revisores/r02_festivos_y_huecos.py <carpeta_datos_bce>"""
import importlib.util
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402

spec = importlib.util.spec_from_file_location("comprobar_datos_a", RAIZ / ".docs" / "scripts" / "comprobar_datos_a.py")
cda = importlib.util.module_from_spec(spec); spec.loader.exec_module(cda)
datos = Path(sys.argv[1])
uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO).query("clase == 'DIV'")

# 1) Huecos reales (días naturales) de una serie
s = pd.read_csv(datos / "EURUSD=X.csv", parse_dates=["fecha"])["fecha"]
h = s.diff().dt.days
print("huecos > 3 días naturales en EURUSD=X (fecha anterior → siguiente):")
for i in h[h > 3].index[-8:]:
    print(f"   {s[i - 1].date()} → {s[i].date()} ({int(h[i])} días)")
print(f"   mayor hueco: {int(h.max())} días")
# fechas idénticas en las seis series
fechas = {p.stem: set(pd.read_csv(p)["fecha"]) for p in datos.glob("*.csv")}
print("seis series con las mismas fechas:", len({frozenset(v) for v in fechas.values()}) == 1)

# 2) Frescura de PS2 en días de cierre de TARGET (as_of = el propio festivo o el día hábil siguiente)
casos = ["2026-04-03", "2026-04-06", "2026-04-07", "2026-05-01", "2026-05-04", "2025-12-26", "2025-12-29", "2026-01-01", "2026-01-02"]
print("\nas_of        dia   H1                          H2      H3")
for d in casos:
    fila = [d, pd.Timestamp(d).day_name()[:3]]
    for hz in ("H1", "H2", "H3"):
        r = cda.comprobar(datos, uni, d, hz)
        malos = [x for x in r if x["estado"] != "OK"]
        fila.append("OK" if not malos else f"{malos[0]['estado']} ({len(malos)}) {malos[0]['motivo'][:28]}")
    print(f"{fila[0]}  {fila[1]}   {fila[2]:28} {fila[3]:7} {fila[4]}")

# 3) Borde de fecha_publicacion: con as_of = D se ve el dato de D; con as_of = D-1, no
p = ProveedorCSV(datos)
p.fijar_as_of("2026-11-12")
ult12 = p.cierres("EURUSD=X", None, "2026-11-12").index.max()
p.fijar_as_of("2026-11-13")
ult13 = p.cierres("EURUSD=X", None, "2026-11-13").index.max()
print(f"\nas_of 2026-11-12 → último dato {pd.Timestamp(ult12).date()} · as_of 2026-11-13 → último dato {pd.Timestamp(ult13).date()}")
