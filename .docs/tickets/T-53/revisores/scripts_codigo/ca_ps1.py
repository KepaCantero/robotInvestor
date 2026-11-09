"""PS1/G1: la pieza automática de momentum HT-01 basta para superar PS1, y su dirección no depende de la tesis."""
import tempfile, pathlib
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
           cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
b.fijar_fecha("2026-06-05")
# Finalista con tesis BAJISTA, sin ninguna afirmación corroborada: solo la pieza que el ejecutor añade (momentum > 0 => 'favorable')
f = {"proxy": "SPY", "tesis": "Corrección bajista del mercado estadounidense", "_piezas": [
     {"afirmacion": "Momentum 12-1 de SPY: +12.00% (percentil 80% de la clase) a 2026-06-05", "fuente": "HT-01:SPY",
      "direccion": "favorable", "extracto": "serie de cierres HT-01", "origen": "AG-13", "tipo_afirmacion": "DATO"}]}
an = {"clase": "RV", "nivel": "N1", "finalistas": [f], "peticiones": [], "hallazgos_r9": []}
import pandas as pd; b._registrar_evidencia_clase(an, pd.Timestamp("2026-06-05"), "RUN-2026-0001")
print("PS1 (y G1) con una sola pieza automática HT-01 y tesis bajista:", f["_ps1"], "| raíces:", f["_raices"])
