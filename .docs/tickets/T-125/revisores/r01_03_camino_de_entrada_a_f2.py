"""QA r01 de T-125: ¿llega a F2 el bloque `pronostico_fuente` cuando un agente lo devuelve?

Simula (con el cliente simulado parcheado) que el Analista devuelve en cada afirmación un bloque `pronostico_fuente`
completo y que el Curador la clasifica como PRONOSTICO_FUENTE, que es lo más que puede hacer el modelo real. Mira qué guarda
F2 y si el Evaluador encuentra algún pronóstico de fuente.

Uso, desde `bloque_a/11_Ejecutor`:  QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r01_03_camino_de_entrada_a_f2.py
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tests"))
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, nuevo_bloque  # noqa: E402
from bloque_a import mock_respuestas  # noqa: E402

PF = {"ref_id": "REF-RF-0001", "variable": "cierre", "serie_ht01": "SPY", "fecha_objetivo": "2025-06-02",
      "umbral_o_rango": 1.0, "direccion": "por_encima", "probabilidad": 0.7, "fecha_emision": "2025-05-01"}
ficha_original, curador_original = mock_respuestas._ficha, mock_respuestas._curador


def ficha(u, msg, ctx, rng, inyectado):
    f = ficha_original(u, msg, ctx, rng, inyectado)
    for a in f.get("afirmaciones", []):
        a["tipo_afirmacion"], a["pronostico_fuente"] = "PRONOSTICO_FUENTE", dict(PF)
    return f


def curador(msg, ctx, rng):
    r = curador_original(msg, ctx, rng)
    for p in r["piezas"]:
        p["tipo_afirmacion"] = "PRONOSTICO_FUENTE"
    return r


mock_respuestas._ficha, mock_respuestas._curador = ficha, curador
b = nuevo_bloque(Path(tempfile.mkdtemp(prefix="qa7_t125_f2_", dir=os.environ.get("QA_TMP"))), cargar_universo(RUTA_UNIVERSO_EJEMPLO))
r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
clm = [e for e in b.almacen.estado("F2", clave="clm_id").values() if e.get("tipo_entrada") == "CLM"]
pf = [e for e in clm if e.get("tipo_afirmacion") == "PRONOSTICO_FUENTE"]
con_bloque = [e for e in pf if isinstance(e.get("pronostico_fuente"), dict)]
print(f"ciclo {r['estado']} · CLM en F2: {len(clm)} · clasificadas PRONOSTICO_FUENTE: {len(pf)} · con bloque pronostico_fuente: "
      f"{len(con_bloque)} · pronósticos de fuentes que ve el Evaluador: {len(b.evaluador.pronosticos_de_fuentes(AS_OF))}")
