"""r01_04 · QA T-65 · H-15: un cierre ≤ 0 ANTIGUO (fuera de la ventana de 3 años del lote) en un símbolo por lo demás sano.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r01_04_cierre_malo_antiguo.py

`senales_clase` comprueba los cierres solo en la ventana [as_of − 3 años − 30 días, as_of]; `valor_en` pide la historia
entera hasta la fecha. Con la validación nueva de HT-01, ¿qué pasa con un 0 de 2019? Se espera una de dos: que no importe
(está fuera de la ventana) o que el símbolo se excluya y se declare. No se espera que el símbolo pierda su precio en
silencio (PS2 sin fecha) ni que el ciclo caiga.
"""
import pathlib
import shutil
import sys
import tempfile
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.configuracion import DIR_EJECUTOR, RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

AS_OF = "2026-06-05"
hall = 0
for nombre, malo in (("cero_2019", 0.0), ("negativo_2019", -1.0)):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r01_04_"))
    datos = tmp / "datos"
    shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    # Sustituye todos los símbolos DIV del universo de ejemplo por una copia con un cierre malo en 2019: así alguno es finalista
    uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    div = list(uni[uni["clase"] == "DIV"]["simbolo"])
    for s in div:
        df = pd.read_csv(datos / f"{s}.csv")
        primero = df["fecha"].iloc[0]
        extra = pd.DataFrame({"fecha": [str(d.date()) for d in pd.bdate_range("2019-01-01", pd.Timestamp(primero) - pd.Timedelta(days=1))]})
        for c in df.columns:
            if c != "fecha":
                extra[c] = df[c].iloc[0]
        extra.loc[10, "cierre"] = malo
        pd.concat([extra, df]).to_csv(datos / f"{s}.csv", index=False)
    b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(datos), uni, MockClient(), tmp / "e", tmp / "s")
    b.fijar_fecha(AS_OF)
    sen, _ = b.senales_clase("DIV", AS_OF, "RUN-PRUEBA")
    sin_precio = [s for s, t in sen.items() if "precio" not in t]
    inval = getattr(b, "_datos_invalidos", {}).get(("DIV", "RUN-PRUEBA"))
    print(f"[{nombre}] símbolos con señales: {len(sen)}; sin precio ni fecha del dato: {sin_precio}; declarados inválidos: {inval}")
    try:
        r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
        lim = [x[:160] for x in r["paquete"]["limitaciones"] if "Divisas" in x or "HT-01" in x]
        print(f"      ciclo: estado={r['estado']} opciones={len(r['paquete']['clases']['DIV']['opciones'])} limitaciones={lim}")
        incs = [x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS"]
        print(f"      incidencias DATOS en HA: {len(incs)}")
        silencioso = bool(sin_precio) and not inval
        if silencioso:
            hall += 1
            print("      HALLAZGO: los símbolos pierden precio y fecha del dato (PS2 falla) sin declararse como datos inválidos")
    except Exception as e:  # noqa: BLE001
        hall += 1
        print(f"      HALLAZGO: el ciclo cae: {type(e).__name__}: {str(e)[:160]}")
print(f"HALLAZGOS: {hall}")
