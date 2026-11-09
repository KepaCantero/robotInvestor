"""r01 · CA-06: ¿la exclusión cubre todos los símbolos que tumban el lote de fichas?
Casos: (a) símbolo que empieza a cotizar 10 sesiones antes de as_of (historia corta);
(b) símbolo que dejó de cotizar antes de la ventana de 3 años (deslistado);
(c) control: símbolo que empieza después de as_of (el caso del hallazgo original)."""
import tempfile, pathlib, shutil, sys
import pandas as pd
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

def caso(nombre, fechas):
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    datos = tmp / "datos"; shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    (datos / "USDNEW=X.csv").write_text("fecha,cierre\n" + "\n".join(f"{d.date()},1.0{i % 9}" for i, d in enumerate(fechas)) + "\n")
    uni = pathlib.Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + \
          "\nUSDNEW=X,DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/NEW,\n"
    (tmp / "u.csv").write_text(uni, encoding="utf-8")
    b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(datos), cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")
    r = b.ciclo("2026-06-05", alcance={"clases": ["DIV"]})
    d = r["paquete"]["clases"]["DIV"]
    rech = sorted({(e.get("operacion") if isinstance(e.get("operacion"), str) else (e.get("operacion") or {}).get("method_id"))
                   for e in b.almacen.leer("RC") if e.get("estado") == "REJECTED"})
    lim = [x for x in r["paquete"]["limitaciones"] if "Divisas" in x]
    print(f"[{nombre}] opciones DIV={len(d['opciones'])} estado={r['estado']} fichas_rechazadas={rech} limitaciones={lim} embudo={d['embudo']}")
    return len(d["opciones"]), rech, lim

base = caso("control_sin_simbolo_extra", pd.bdate_range("2026-09-01", "2026-10-30"))
a = caso("a_historia_corta_10_sesiones", pd.bdate_range("2026-05-22", "2026-06-05"))
bb = caso("b_deslistado_2021", pd.bdate_range("2020-01-01", "2021-12-31"))
