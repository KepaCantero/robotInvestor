"""Los hitos HIT- de un PRG H5 (horizonte «H4», misma probabilidad, mismo suceso acumulado) entran en la celda tipo×H4
del Evaluador: cuentan para n ≥ 100 del certificado y para el historial de aciertos publicado."""
import tempfile
from bloque_a.almacen import Almacen
from bloque_a.evaluador import Evaluador
a = Almacen(tempfile.mkdtemp(dir=".")); a.reloj.fijar("2030-01-10")
for i, m in enumerate((12, 30, 54)):
    hid = f"HIT-2026-000{i+1}"
    a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": hid, "prg_padre": "PRG-2026-0009", "es_hito": True, "opp_id": "OPP-1",
                               "clase": "RV", "horizonte": "H4", "prob_interna": 0.65, "sentido": "POSITIVO", "en_informe": True,
                               "fecha_emision": "2026-06-05", "referencia_ingenua": {"valor_o_prob": 0.5}, "estado": "ABIERTO"})
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": hid, "estado": "RESUELTO",
                               "resolucion": {"resultado_binario": 1, "comprobacion_fuga": "SUPERADA", "valor_observado": 0.1,
                                              "fecha_resuelto": "2030-01-10"}})
ev = Evaluador(a, None, None, {"evaluacion": {}}, None)
print("celdas:", {k: v["n"] for k, v in ev.metricas("2030-01-10").items()})
print("historial publicado (n global):", ev.historial_aciertos("2030-01-10", semanas=600)["global"]["n"])
