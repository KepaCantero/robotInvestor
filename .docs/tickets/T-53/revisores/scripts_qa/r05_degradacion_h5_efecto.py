"""r05 · CS-12: la degradación automática de H5 se «aplica en F10» (P-31). ¿La usa el ciclo siguiente?
Se siembran 20 hitos RV×H5 resueltos (25 % cumplidos), se degrada y se ejecuta un ciclo RV con el mock."""
import tempfile, pathlib
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR, aplicabilidad
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
           cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
a = b.almacen
a.reloj.fijar("2026-06-01")
ids = []
for i, o in enumerate([1] * 5 + [0] * 15):
    hid = f"HIT-2025-{i + 1:04d}"; ids.append(hid)
    a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": hid, "opp_id": "OPP-X", "clase": "RV", "horizonte": "H4", "prob_interna": 0.65,
                               "sentido": "POSITIVO", "en_informe": True, "es_hito": True, "prg_padre": "PRG-2025-0999",
                               "fecha_emision": "2025-06-05", "fecha_resolucion": "2026-05-29", "referencia_ingenua": {"valor_o_prob": 0.5}, "estado": "ABIERTO"})
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": hid, "estado": "RESUELTO",
                               "resolucion": {"resultado_binario": o, "comprobacion_fuga": "SUPERADA", "fecha_resuelto": "2026-05-29"}})
a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2025-0999", "opp_id": "OPP-X", "clase": "RV", "horizonte": "H5", "prob_interna": None,
                           "hit_ids": ids, "fecha_emision": "2025-06-05", "fecha_resolucion": "2045-06-05", "estado": "ABIERTO"})
r = b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
print("degradacion en C5:", [(h["tipo_entrada"], h["celda"], h["de"], h["a"]) for h in (r["evaluacion"] or {}).get("degradacion_h5", [])])
print("F10 P-31 RV×H5:", b.f10()["P-31"]["RV"]["H5"] if isinstance(b.f10().get("P-31"), dict) else b.f10().get("P-31"))
print("aplicabilidad(cfg) RV×H5 usada por el ciclo:", aplicabilidad(b.cfg, "RV", "H5"))
r2 = b.ciclo("2026-06-12", alcance={"clases": ["RV"]})
ct06 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-06"]
ops = r2["paquete"]["clases"]["RV"]["opciones"]
print("ciclo siguiente: H5 en horizontes de las opciones RV:", [("H5" in o["horizontes"]) for o in ops],
      "| etiquetas H5:", [o["horizontes"].get("H5", {}).get("etiqueta") for o in ops])
aju = [x for x in a.estado("F6", clave="id").values() if x.get("tipo_entrada") == "AJU" and x.get("parametro") == "P-31"]
print("AJU P-31 aplicado_en_produccion:", [x.get("aplicado_en_produccion") for x in aju])
