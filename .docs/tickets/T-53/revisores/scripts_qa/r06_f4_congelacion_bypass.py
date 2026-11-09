"""r06 · CA-09 (R11): la congelación de F4 solo mira tipo_entrada ALTA y RESOLUCION. ¿Se puede reescribir un pronóstico
congelado con otro tipo_entrada (o sin él)? ¿Y resolver con un prg_id con espacios? ¿Sobrevive a recargar el almacén?"""
import tempfile, pathlib
from bloque_a.almacen import Almacen, EscrituraFueraDeReserva
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
a = Almacen(tmp); a.reloj.fijar("2026-06-05")
a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "prob_interna": 0.6, "sentido": "POSITIVO",
                           "fecha_resolucion": "2026-09-04", "estado": "ABIERTO"})
for tipo in ("ACTUALIZACION", None, "alta"):
    e = {"prg_id": "PRG-2026-0001", "prob_interna": 0.95, "sentido": "NEGATIVO", "fecha_resolucion": "2026-06-08"}
    if tipo is not None:
        e["tipo_entrada"] = tipo
    try:
        a.escribir("F4", "AG-10", e); res = "ACEPTADA"
    except EscrituraFueraDeReserva as x:
        res = f"RECHAZADA ({x})"
    v = a.estado("F4")["PRG-2026-0001"]
    print(f"tipo_entrada={tipo!r}: {res} -> vista: prob={v['prob_interna']} sentido={v['sentido']} fecha_res={v['fecha_resolucion']}")
print("integridad:", a.verificar_integridad("F4"))
# recarga: el índice se reconstruye desde disco
b = Almacen(tmp)
try:
    b.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "prob_interna": 0.1}); print("tras recarga: segunda ALTA ACEPTADA")
except EscrituraFueraDeReserva as x:
    print("tras recarga: segunda ALTA rechazada:", x)
