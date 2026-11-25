"""QA r01 (Claude) de T-192, PB-34: corrección de una tasa base contaminada, de punta a punta con el cliente simulado.

Uso, desde bloque_a/11_Ejecutor con la venv del repo (tarda unos minutos: un C1 y dos C5):
    python ../../.docs/tickets/T-192/revisores/r03_ataques_fuga.py
"""
import math
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from conftest import AS_OF, nuevo_bloque  # noqa: E402

UNIVERSO = pd.read_csv("config/universo_ejemplo.csv")
fallos = []


def caso(nombre, cond, detalle=""):
    print(("OK    " if cond else "FALLO ") + nombre + (f" · {detalle}" if detalle else ""), flush=True)
    if not cond:
        fallos.append(nombre)


b = nuevo_bloque(Path(tempfile.mkdtemp(prefix="qa192f_")), UNIVERSO)
b.ciclo(AS_OF, alcance={"clases": ["RV"]})
prgs = sorted((x for x in b.almacen.estado("F4").values() if x.get("prob_interna") is not None),
              key=lambda x: (x["fecha_resolucion"], x["prg_id"]))
vencen = [p for p in prgs if p["fecha_resolucion"] <= "2026-07-10"]
print(f"PRG que vencen antes del 10-07: {len(vencen)}")
p1 = vencen[0]
p2 = vencen[1] if len(vencen) > 1 else None
calc1 = p1["referencia_ingenua"]["calc_id"]
# Contaminación por la fecha de cálculo (la de la prueba del ticket) …
b.almacen.escribir("RC", "AG-13", {"tipo_entrada": "SERVICIO", "calc_id": calc1, "as_of": "2026-06-06"})
# … y por un dato posterior a la emisión dentro de la base (la fecha de cálculo, la buena)
if p2:
    calc2 = p2["referencia_ingenua"]["calc_id"]
    rc2 = b.almacen.estado("RC")[calc2]
    datos = [dict(d) for d in rc2["datos"]]
    datos[0]["fecha_dato"] = "2026-06-12"
    b.almacen.escribir("RC", "AG-13", {"tipo_entrada": "SERVICIO", "calc_id": calc2, "datos": datos})

b.fijar_fecha("2026-07-10")
b.evaluador.ciclo("2026-07-10")
f4 = b.almacen.estado("F4")
r1 = f4[p1["prg_id"]]["resolucion"]
caso("la resolución contaminada queda FALLIDA con fuga_tasa_base", r1["comprobacion_fuga"] == "FALLIDA" and r1["fuga_tasa_base"])
caso("la FALLIDA no cita el CALC- de las métricas del día", r1.get("calc_id") is None, str(r1.get("calc_id")))
if p2:
    r2 = f4[p2["prg_id"]]["resolucion"]
    caso("un dato posterior a la emisión dentro de la base también es fuga", r2["comprobacion_fuga"] == "FALLIDA", r2["comprobacion_fuga"])

# El FC-EVAL-001 del día no lleva la resolución FALLIDA
rc = b.almacen.estado("RC")
res_dia = [e for e in b.almacen.leer("F6") if e.get("tipo_entrada") == "RES" and e.get("fecha") == "2026-07-10"]
calc_dia = res_dia[-1]["calc_id"] if res_dia else None
superadas = [x for x in f4.values() if (x.get("resolucion") or {}).get("fecha_resuelto") == "2026-07-10"
             and x["resolucion"].get("comprobacion_fuga") == "SUPERADA"]
d0 = ((rc.get(calc_dia) or {}).get("datos") or [{}])[0]
datos_dia = d0.get("valor") or d0.get("valores") or {}
caso("el FC-EVAL-001 del día solo con las SUPERADA", calc_dia is None or len(datos_dia.get("p", [])) == len(superadas),
     f"p={len(datos_dia.get('p', []))} superadas={len(superadas)}")

cor = [e for e in b.almacen.leer("F6") if e.get("tipo_entrada") == "CORRECCION_FUGA" and e["prg_id"] == p1["prg_id"]]
caso("una corrección en F6", len(cor) == 1, str(len(cor)))
c = cor[0]
rc_limpia = rc.get(c["referencia_limpia"]["calc_id"]) or {}
caso("el recálculo usa el corte original (la emisión), no la fecha del C5", rc_limpia.get("as_of") == p1["fecha_emision"],
     f"as_of del recálculo {rc_limpia.get('as_of')} · emisión {p1['fecha_emision']}")
caso("el dato más reciente del recálculo no pasa de la emisión",
     all((d.get("fecha_dato") or "") <= p1["fecha_emision"] for d in rc_limpia.get("datos") or []))
o, pr = r1["resultado_binario"], c["referencia_limpia"]["valor_o_prob"]
caso("brier_ref recalculado con la base limpia", math.isclose(c["puntuaciones"]["brier_ref"], (pr - o) ** 2),
     f"{c['puntuaciones'].get('brier_ref')} frente a {(pr - o) ** 2}")
caso("log_ref recalculado con la base limpia",
     math.isclose(c["puntuaciones"]["log_ref"], -math.log(min(max(pr if o else 1 - pr, 0.01), 0.99))))
caso("brier del modelo intacto", c["puntuaciones"]["brier"] == r1["puntuaciones"]["brier"])
caso("F4 no se reescribe", f4[p1["prg_id"]]["referencia_ingenua"]["calc_id"] == calc1)
prg = next((x for x in b.evaluador.resueltos("2026-07-10") if x["prg_id"] == p1["prg_id"]), None)
caso("resueltos() usa la referencia y las puntuaciones corregidas",
     prg is not None and prg["resolucion"]["puntuaciones"] == c["puntuaciones"] and prg["referencia_ingenua"] == c["referencia_limpia"])

# Segundo C5: sin duplicar la corrección
b.fijar_fecha("2026-07-17")
b.evaluador.ciclo("2026-07-17")
cor2 = [e for e in b.almacen.leer("F6") if e.get("tipo_entrada") == "CORRECCION_FUGA" and e["prg_id"] == p1["prg_id"]]
caso("un segundo C5 no duplica la corrección", len(cor2) == 1, str(len(cor2)))
caso("integridad del almacén", all(b.almacen.verificar_integridad().values()))

# Aviso al Orquestador e incidencia (tabla de fallos del prompt del Evaluador: «Fuga detectada a posteriori»)
avisos = [e for e in b.almacen.leer("HA") if "fuga" in str(e.get("detalle", "")).lower() or "fuga" in str(e.get("tipo", "")).lower()]
caso("queda aviso en HA de la fuga detectada", bool(avisos), f"{len(avisos)} entradas")

print(f"\n{len(fallos)} fallo(s): {fallos}")
