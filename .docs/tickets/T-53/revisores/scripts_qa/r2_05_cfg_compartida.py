"""r2_05 · H-05: ¿el ciclo muta la configuración compartida entre instancias de Bloque?
Dos Bloque con el MISMO dict de configuración y almacenes distintos. A degrada RV×H5 (F10 propio); B no tiene degradación.
Se espera que B siga con la tabla 8.3 («SI») y ofrezca H5. Además: ¿cambia el dict que pasó el llamador?"""
import copy, pathlib, tempfile
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR, aplicabilidad
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

cfg = cargar_config(extra={"modo": "backtest"})
foto = copy.deepcopy(cfg)


def bloque(nombre):
    t = pathlib.Path(tempfile.mkdtemp(dir=".", prefix=nombre))
    return Bloque(cfg, ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), t / "e", t / "s")


def sembrar(a, fecha="2026-06-01"):
    a.reloj.fijar(fecha)
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


A, B = bloque("A_"), bloque("B_")
print("misma configuración en A y B:", A.cfg is B.cfg is cfg, "| evaluador comparte cfg:", A.evaluador.cfg is cfg)
sembrar(A.almacen)
A.ciclo("2026-06-05", alcance={"clases": ["RV"]})
print("tras el ciclo de A: claves nuevas en el dict del llamador:", sorted(set(cfg) - set(foto)),
      "| cfg['_tabla_horizontes']['RV']['H5'] =", (cfg.get("_tabla_horizontes") or {}).get("RV", {}).get("H5"))
print("F10 de B tiene P-31:", "P-31" in B.f10("2026-06-12"))
rb = B.ciclo("2026-06-12", alcance={"clases": ["RV"]})
ops = rb["paquete"]["clases"]["RV"]["opciones"]
print("B (sin degradación propia): aplicabilidad RV×H5 =", aplicabilidad(B.cfg, "RV", "H5"),
      "| H5 en opciones de B:", [("H5" in o["horizontes"]) for o in ops], "| etiquetas:", [o["horizontes"].get("H5", {}).get("etiqueta") for o in ops])
print("_matriz_aplicabilidad de B:", B.evaluador._matriz_aplicabilidad("2026-06-12")["RV"]["H5"])
# Una instancia nueva con su propia copia de la configuración (como hace backtest.py con fusionar)
C = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
           MockClient(), pathlib.Path(tempfile.mkdtemp(dir=".", prefix="C_")) / "e", pathlib.Path(tempfile.mkdtemp(dir=".")) / "s")
rc = C.ciclo("2026-06-12", alcance={"clases": ["RV"]})
print("C (cfg propia, sin degradación):", aplicabilidad(C.cfg, "RV", "H5"), "| H5:", [("H5" in o["horizontes"]) for o in rc["paquete"]["clases"]["RV"]["opciones"]])
