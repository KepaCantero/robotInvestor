"""r2_01 · H-01: más casos de símbolos con historia parcial en la ventana del lote [as_of − 3 años − 30 días, as_of].
Para cada caso: opciones DIV, estado del run, fichas rechazadas, cuántos símbolos DIV conservan señales y lagunas.
Casos:
  (a) un único dato dentro de la ventana (deslistado justo después del inicio de la ventana);
  (b) dejó de cotizar hace un año (dentro de la ventana, dato rancio);
  (c) salida a bolsa hace 3 meses (~60 sesiones);
  (d) salida a bolsa hace 13 meses;
  (e) hueco: datos hasta 2021 y vuelve a cotizar hace 2 semanas;
  (f) dato antiguo (2020) y dato futuro (después de as_of), ninguno en la ventana;
  (g) dos símbolos cortos a la vez (10 sesiones cada uno);
  (h) CSV con cabecera y sin filas."""
import pathlib, shutil, tempfile
import pandas as pd
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

AS_OF = "2026-06-05"
LINEA = "{s},DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/{s},\n"


def caso(nombre, series: dict):
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    datos = tmp / "datos"; shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    uni = pathlib.Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + "\n"
    for s, fechas in series.items():
        (datos / f"{s}.csv").write_text("fecha,cierre\n" + "".join(f"{d.date()},1.0{i % 9}\n" for i, d in enumerate(fechas)))
        uni += LINEA.format(s=s)
    (tmp / "u.csv").write_text(uni, encoding="utf-8")
    b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(datos), cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")
    try:
        r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    except Exception as e:   # noqa: BLE001
        print(f"[{nombre}] EXCEPCIÓN {type(e).__name__}: {e}")
        return
    d = r["paquete"]["clases"]["DIV"]
    run = r["run_id"]
    rech = b._fichas_rechazadas.get(("DIV", run))
    excl = b._sin_historia.get(("DIV", run))
    lim = [x[:160] for x in r["paquete"]["limitaciones"] if "Divisas" in x or "clúster" in x]
    proxies = [o.get("indicador_seguimiento", {}).get("simbolo") for o in d["opciones"]]
    print(f"[{nombre}] opciones={len(d['opciones'])} proxies={proxies} estado={r['estado']} entrega={r.get('entrega')} "
          f"excluidos={excl} fichas_rechazadas={rech}\n      limitaciones={lim}")


bd = pd.bdate_range
caso("control", {})
caso("a_un_dato_en_ventana", {"USDNEW=X": list(bd("2020-01-01", "2023-05-10"))})
caso("b_deslistado_hace_1_año", {"USDNEW=X": list(bd("2019-01-01", "2025-06-05"))})
caso("c_ipo_hace_3_meses", {"USDNEW=X": list(bd("2026-03-05", AS_OF))})
caso("d_ipo_hace_13_meses", {"USDNEW=X": list(bd("2025-05-05", AS_OF))})
caso("e_hueco_2021_y_vuelve", {"USDNEW=X": list(bd("2019-01-01", "2021-12-31")) + list(bd("2026-05-22", AS_OF))})
caso("f_antiguo_y_futuro", {"USDNEW=X": list(bd("2020-01-01", "2020-12-31")) + list(bd("2026-07-01", "2026-08-01"))})
caso("g_dos_cortos", {"USDNEW=X": list(bd("2026-05-22", AS_OF)), "USDNEW2=X": list(bd("2026-05-22", AS_OF))})
caso("h_csv_vacio", {"USDNEW=X": []})
