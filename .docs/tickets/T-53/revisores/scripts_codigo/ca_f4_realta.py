"""R11: el almacén admite una segunda ALTA del mismo PRG- y la vista consolidada sobrescribe el pronóstico congelado."""
import tempfile
from bloque_a.almacen import Almacen
d = tempfile.mkdtemp(dir=".")
a = Almacen(d); a.reloj.fijar("2026-06-05")
a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "prob_interna": 0.6, "sentido": "POSITIVO",
                            "fecha_resolucion": "2026-12-04", "estado": "ABIERTO"})
a.reloj.fijar("2026-06-12")
a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "prob_interna": 0.9, "sentido": "NEGATIVO",
                            "fecha_resolucion": "2026-07-01", "estado": "ABIERTO"})
p = a.estado("F4")["PRG-2026-0001"]
print("vista consolidada:", {k: p[k] for k in ("prob_interna", "sentido", "fecha_resolucion")})
print("integridad:", a.verificar_integridad("F4"))
# AG-20 puede 're-resolver' un PRG ya resuelto, o resolver uno inexistente
a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": "PRG-2026-0001", "estado": "RESUELTO", "resolucion": {"resultado_binario": 1}})
a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": "PRG-2026-0001", "estado": "RESUELTO", "resolucion": {"resultado_binario": 0}})
a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": "PRG-2099-9999", "estado": "RESUELTO", "resolucion": {"resultado_binario": 1}})
e = a.estado("F4")
print("re-resolucion aceptada; resultado final:", e["PRG-2026-0001"]["resolucion"], "n resoluciones:", len(e["PRG-2026-0001"]["resoluciones"]))
print("resolucion huerfana aceptada:", "PRG-2099-9999" in e)
