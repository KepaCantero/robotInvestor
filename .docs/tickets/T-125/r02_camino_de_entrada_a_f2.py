"""T-125 r02 (implementador): el camino entero de un pronóstico de fuente, Analista → F2 → Evaluador → FUE- → CT-19.

Variante de `revisores/r01_03_camino_de_entrada_a_f2.py` con un bloque registrable (fecha objetivo posterior al ciclo,
`ref_id` de F9 que es la fuente de la afirmación) y un segundo ciclo, pasado el vencimiento, que lo resuelve. Primero
ejecuta el caso del revisor tal cual (bloque con la fecha objetivo ya pasada y otra fuente: ahora se rechaza y queda en HA).

Uso, desde `bloque_a/11_Ejecutor`:  QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/r02_camino_de_entrada_a_f2.py
"""
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path.cwd() / "tests"))
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, config_pruebas, nuevo_bloque  # noqa: E402
from bloque_a import mock_respuestas  # noqa: E402

UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
TMP = os.environ.get("QA_TMP")
FUENTE = "REF-RF-0001"
ficha_original, curador_original = mock_respuestas._ficha, mock_respuestas._curador


def resumen(b, as_of):
    clm = [e for e in b.almacen.estado("F2", clave="clm_id").values() if e.get("tipo_entrada") == "CLM"]
    pf = [e for e in clm if e.get("tipo_afirmacion") == "PRONOSTICO_FUENTE"]
    con_bloque = [e for e in pf if isinstance(e.get("pronostico_fuente"), dict)]
    rech = [e for e in b.almacen.leer("HA") if "Pronóstico de fuente no registrable" in str(e.get("detalle"))]
    return (f"CLM en F2: {len(clm)} · PRONOSTICO_FUENTE: {len(pf)} · con bloque: {len(con_bloque)} · rechazados en HA: {len(rech)} · "
            f"pronósticos que ve el Evaluador a {as_of}: {len(b.evaluador.pronosticos_de_fuentes(as_of))}")


# 1) El caso del revisor, tal cual (modo backtest de las pruebas)
PF_REVISOR = {"ref_id": FUENTE, "variable": "cierre", "serie_ht01": "SPY", "fecha_objetivo": "2025-06-02",
              "umbral_o_rango": 1.0, "direccion": "por_encima", "probabilidad": 0.7, "fecha_emision": "2025-05-01"}


def ficha_revisor(u, msg, ctx, rng, inyectado):
    f = ficha_original(u, msg, ctx, rng, inyectado)
    for a in f.get("afirmaciones", []):
        a["tipo_afirmacion"], a["pronostico_fuente"] = "PRONOSTICO_FUENTE", dict(PF_REVISOR)
    return f


def curador(msg, ctx, rng):
    r = curador_original(msg, ctx, rng)
    for p in r["piezas"]:
        p["tipo_afirmacion"] = "PRONOSTICO_FUENTE"
    return r


mock_respuestas._ficha, mock_respuestas._curador = ficha_revisor, curador
b = nuevo_bloque(Path(tempfile.mkdtemp(prefix="t125r02_a_", dir=TMP)), UNIVERSO)
r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
print(f"[revisor, tal cual] ciclo {r['estado']} · {resumen(b, AS_OF)}")
print("   motivos:", sorted({e["detalle"].split("(")[1].split(")")[0] for e in b.almacen.leer("HA")
                         if "Pronóstico de fuente no registrable" in str(e.get("detalle"))}))


# 2) Un bloque registrable, en modo vivo, y el ciclo que lo resuelve
def ficha_registrable(u, msg, ctx, rng, inyectado):
    f = ficha_original(u, msg, ctx, rng, inyectado)
    sym, hoy = f["indicador_seguimiento"]["simbolo"], pd.Timestamp(ctx["fecha_as_of"])
    for k in (10, 20):
        obj = str((hoy + pd.offsets.BDay(k)).date())
        f["afirmaciones"].append({"afirmacion": f"{FUENTE} prevé {sym} por encima de 1 el {obj}", "fuente": FUENTE, "direccion": "favorable",
                                  "pronostico_fuente": {"ref_id": FUENTE, "variable": "cierre", "serie_ht01": sym, "fecha_objetivo": obj,
                                                        "umbral_o_rango": 1.0, "direccion": "por_encima", "probabilidad": 0.8,
                                                        "fecha_emision": str(hoy.date())}})
    return f


mock_respuestas._ficha, mock_respuestas._curador = ficha_registrable, curador_original
b = nuevo_bloque(Path(tempfile.mkdtemp(prefix="t125r02_b_", dir=TMP)), UNIVERSO, cfg=config_pruebas(modo="vivo"))
r1 = b.ciclo("2026-04-03", alcance={"clases": ["RV"]})
print(f"[registrable, ciclo 2026-04-03] {r1['estado']} · {resumen(b, '2026-04-03')}")
r2 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
fue = r2["evaluacion"]["fiabilidad_fuentes"]
ct19 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-16"]
print(f"[registrable, ciclo {AS_OF}] {r2['estado']} · FUE-: {[(f['ref_id'], f['n'], f['puntos_historial'], f['calc_id']) for f in fue]} · "
      f"CT-19 a AG-16: {[m['msg_id'] for m in ct19]} · anotado en la FUE-: "
      f"{[b.almacen.estado('F6', clave='id')[f['fue_id']]['comunicado_ct19'] for f in fue]}")
