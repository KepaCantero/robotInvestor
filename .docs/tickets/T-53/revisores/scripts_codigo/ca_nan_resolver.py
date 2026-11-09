"""Extremo a extremo: Evaluador.resolver resuelve como NO_OCURRIDO un PRG cuyo cierre de resolución no es numérico."""
import tempfile, pathlib, json
import pandas as pd
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
datos = tmp / "datos"; datos.mkdir()
fechas = pd.bdate_range("2026-01-01", "2026-07-31")
filas = ["fecha,cierre"] + [f"{d.date()},{100 + i * 0.1:.2f}" for i, d in enumerate(fechas)]
filas[-1] = filas[-1].split(",")[0] + ",-"       # último cierre no numérico
filas[-2] = filas[-2].split(",")[0] + ",n.d."
(datos / "XYZ.csv").write_text("\n".join(filas) + "\n", encoding="utf-8")
cfg = cargar_config(extra={"modo": "backtest"})
b = Bloque(cfg, ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
b.fijar_fecha("2026-06-05")
b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "opp_id": "OPP-2026-0001", "clase": "RV",
    "horizonte": "H2", "tipo_pronostico": "DIRECCIONAL", "sentido": "POSITIVO", "variable": {"serie_ht01": "XYZ"},
    "referencia_indice": None, "nivel_referencia": {"valor": 117.0, "fecha": "2026-06-05"}, "umbral": 0.0,
    "fecha_emision": "2026-06-05", "fecha_resolucion": "2026-07-31", "prob_interna": 0.65,
    "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True, "estado": "ABIERTO"})
b.fijar_fecha("2026-08-03")
r = b.evaluador.resolver("2026-08-03")
print(json.dumps({k: r[0][k] for k in ("estado",)} | {k: r[0]["resolucion"].get(k) for k in ("rent_proxy", "resultado", "resultado_binario", "comprobacion_fuga")}, default=str))
