"""r11 · CA-14/INC-T53-02: PS2 de H1 en sesiones hábiles (np.busday_count sin calendario de festivos).
Ciclo ordinario en sábado (Anexo A) y días después de festivos de mercado: el dato es el de la última sesión real."""
import pathlib, tempfile
import numpy as np
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
           cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
casos = [("sábado normal, dato del viernes", "2026-06-06", "2026-06-05"),
         ("sábado tras Viernes Santo (2026-04-03, mercados cerrados), dato del jueves", "2026-04-04", "2026-04-02"),
         ("sábado 2025-12-27 tras Navidad (25 y 26 cerrados en la UE/UK), dato del 24", "2025-12-27", "2025-12-24"),
         ("viernes 2025-07-04 (EE. UU. cerrado), dato del jueves 3 -> viernes as_of", "2025-07-04", "2025-07-03"),
         ("lunes, dato del viernes", "2026-06-08", "2026-06-05")]
for etq, as_of, dato in casos:
    ps2 = b._puertas({"senales": {"fecha_dato": dato}}, "N1", as_of, ["H1"])["PS2"]
    ps2_h1h2 = b._puertas({"senales": {"fecha_dato": dato}}, "N1", as_of, ["H1", "H2"])["PS2"]
    print(f"{etq}: sesiones={np.busday_count(dato, as_of)} días={(np.datetime64(as_of) - np.datetime64(dato)).astype(int)} "
          f"-> PS2[H1]={ps2} PS2[H1,H2]={ps2_h1h2}")
