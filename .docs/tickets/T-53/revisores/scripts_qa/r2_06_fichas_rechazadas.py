"""r2_06 · H-01: ¿se alcanza la rama nueva «fichas del Motor rechazadas» (laguna + PARCIAL)? Se busca un símbolo que haga
rechazar el lote de fichas del tipo DIV: precio constante, precio cero o negativo, fechas duplicadas, fechas desordenadas,
valores no numéricos. Para cada caso: fichas rechazadas, opciones DIV, estado y si la laguna llega a las limitaciones."""
import pathlib, shutil, tempfile
import pandas as pd
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
AS_OF = "2026-06-05"
F = list(pd.bdate_range("2023-01-02", AS_OF))
def caso(nombre, filas):
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    datos = tmp / "datos"; shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    (datos / "USDNEW=X.csv").write_text("fecha,cierre\n" + "".join(f"{d},{v}\n" for d, v in filas))
    uni = pathlib.Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + \
        "\nUSDNEW=X,DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/NEW,\n"
    (tmp / "u.csv").write_text(uni, encoding="utf-8")
    try:
        b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(datos), cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")
        r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    except Exception as e:  # noqa: BLE001
        print(f"[{nombre}] EXCEPCIÓN {type(e).__name__}: {str(e)[:200]}"); return
    run = r["run_id"]
    lim = [x[:200] for x in r["paquete"]["limitaciones"] if "Divisas" in x]
    print(f"[{nombre}] rechazadas={b._fichas_rechazadas.get(('DIV', run))} excluidos={b._sin_historia.get(('DIV', run))} "
          f"opciones={len(r['paquete']['clases']['DIV']['opciones'])} estado={r['estado']}\n      limitaciones={lim}")
caso("constante", [(d.date(), "1.0") for d in F])
caso("cero", [(d.date(), "0") for d in F])
caso("negativo", [(d.date(), f"-1.{i % 9}") for i, d in enumerate(F)])
caso("duplicadas", [(d.date(), f"1.0{i % 9}") for i, d in enumerate(F)] + [(F[-1].date(), "1.5")])
caso("desordenadas", list(reversed([(d.date(), f"1.0{i % 9}") for i, d in enumerate(F)])))
caso("no_numerico_final", [(d.date(), f"1.0{i % 9}") for i, d in enumerate(F[:-5])] + [(d.date(), "abc") for d in F[-5:]])
caso("dos_puntos", [(F[-2].date(), "1.0"), (F[-1].date(), "1.1")])
