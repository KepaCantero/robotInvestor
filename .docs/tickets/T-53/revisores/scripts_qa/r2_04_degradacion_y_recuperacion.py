"""r2_04 · H-05: degradación de RV×H5 seguida de una recuperación (cambio de tipo 3 aprobado, escrito en F10).
1) ciclo 2026-06-05 (degrada en C5): ¿qué tabla usa ese mismo ciclo? (el AJU dice efecto_desde = 06-06);
2) ciclo 06-12: LIMITADO;
3a) recuperación con un CFG de P-31 cuyo valor_vigente restituye «SI» → ciclo 06-19;
3b) recuperación como reversión del esquema F10 (CFG nuevo con revierte_a y sin tabla en valor_vigente) → ciclo 06-26:
    misma instancia frente a una instancia nueva sobre el mismo almacén (¿dependen del historial del proceso?)."""
import pathlib, tempfile
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR, aplicabilidad, TABLA_HORIZONTES
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

TMP = pathlib.Path(tempfile.mkdtemp(dir="."))


def nuevo_bloque(cfg=None):
    return Bloque(cfg or cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
                  cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), TMP / "e", TMP / "s")


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


def h5(r):
    ops = r["paquete"]["clases"]["RV"]["opciones"]
    return [("H5" in o["horizontes"]) for o in ops], [o["horizontes"].get("H5", {}).get("etiqueta") for o in ops]


b = nuevo_bloque()
sembrar(b.almacen)
r1 = b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
aju = [x for x in b.almacen.estado("F6", clave="id").values() if x.get("tipo_entrada") == "AJU"]
print("1) degradación:", [(h["celda"], h["de"], h["a"], h.get("efecto_desde")) for h in r1["evaluacion"].get("degradacion_h5", [])])
print("   tabla usada en el MISMO ciclo 06-05:", aplicabilidad(b.cfg, "RV", "H5"), "| H5 en opciones:", h5(r1))
r2 = b.ciclo("2026-06-12", alcance={"clases": ["RV"]})
print("2) ciclo 06-12:", aplicabilidad(b.cfg, "RV", "H5"), "| H5 en opciones:", h5(r2))

# 3a) tipo 3 aprobado que restituye «SI» (valor_vigente con la tabla completa)
b.almacen.reloj.fijar("2026-06-15")
cfg31 = b.almacen.estado("F10").get("P-31", {})
tabla_si = {c: dict(v) for c, v in cfg31["valor_vigente"].items()}; tabla_si["RV"]["H5"] = "SI"
b.almacen.escribir("F10", "AG-20", {"tipo_entrada": "CFG", "cfg_id": b.almacen.nuevo_id("CFG"), "param_id": "P-31", "autor": "AG-20",
                                    "origen": "P3-EVAL-QA", "de": cfg31["valor_vigente"], "a": tabla_si, "valor_vigente": tabla_si,
                                    "regimen": "CALIBRABLE_RESTRINGIDO", "motivo": "QA r2_04: tipo 3 aprobado", "methodology_version": {"de": "5.2", "a": "5.3"},
                                    "fecha_registro": "2026-06-15", "fecha_efecto": "2026-06-15", "revierte_a": None})
r3 = b.ciclo("2026-06-19", alcance={"clases": ["RV"]})
print("3a) tras tipo 3 con valor_vigente: ", aplicabilidad(b.cfg, "RV", "H5"), "| H5 en opciones:", h5(r3),
      "| ¿vuelve a degradar?:", [(h["de"], h["a"]) for h in r3["evaluacion"].get("degradacion_h5", [])])

# 3b) reversión según el esquema F10: CFG nuevo con revierte_a; valor_vigente vacío (vuelve a la tabla 8.3)
b.almacen.reloj.fijar("2026-06-22")
cfg_aju = next(x for x in b.almacen.leer("F10") if x.get("param_id") == "P-31" and x.get("origen", "").startswith("AJU"))
b.almacen.escribir("F10", "AG-20", {"tipo_entrada": "CFG", "cfg_id": b.almacen.nuevo_id("CFG"), "param_id": "P-31", "autor": "AG-20",
                                    "origen": "P3-EVAL-QA2", "de": "matriz ajustada", "a": None, "valor_vigente": None,
                                    "regimen": "CALIBRABLE_RESTRINGIDO", "motivo": "QA r2_04: reversión a la tabla 8.3",
                                    "methodology_version": {"de": "5.3", "a": "5.4"}, "fecha_registro": "2026-06-22", "fecha_efecto": "2026-06-22",
                                    "revierte_a": cfg_aju["cfg_id"]})
# antes de 3b forzamos que la tabla del proceso sea la degradada (como en un backtest que pasó por 2) sin 3a)
b.cfg["_tabla_horizontes"] = {c: dict(v) for c, v in TABLA_HORIZONTES.items()}; b.cfg["_tabla_horizontes"]["RV"]["H5"] = "LIMITADO"
r4 = b.ciclo("2026-06-26", alcance={"clases": ["RV"]})
print("3b) misma instancia tras reversión (valor_vigente None):", aplicabilidad(b.cfg, "RV", "H5"), "| H5:", h5(r4))
b2 = nuevo_bloque()
r5 = b2.ciclo("2026-06-26", alcance={"clases": ["RV"]})
print("3b) instancia NUEVA, mismo almacén, mismo as_of:      ", aplicabilidad(b2.cfg, "RV", "H5"), "| H5:", h5(r5))
