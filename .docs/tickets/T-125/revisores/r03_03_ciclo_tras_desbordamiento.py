"""QA r03 de T-125 (revisor sin contexto), H-14: un Analista que devuelve un umbral entero de 400 cifras (JSON válido, que
`json.loads` lee como `int`) en un bloque `pronostico_fuente` tumba el ciclo entero con `OverflowError` en el alta en F2
(`_numero_finito` → `math.isfinite`). Mide qué queda en el almacén, si la cadena de huellas sigue íntegra y si el ciclo
siguiente, con respuestas normales, acaba bien.

Uso, desde `bloque_a/11_Ejecutor`:  QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r03_03_ciclo_tras_desbordamiento.py
"""
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path.cwd() / "tests"))
from conftest import RUTA_UNIVERSO_EJEMPLO, cargar_universo, config_pruebas, nuevo_bloque  # noqa: E402
from bloque_a import mock_respuestas  # noqa: E402

F0 = mock_respuestas._ficha


def ficha(u, msg, ctx, rng, iny):
    f = F0(u, msg, ctx, rng, iny)
    sym, hoy = f["indicador_seguimiento"]["simbolo"], pd.Timestamp(ctx["fecha_as_of"])
    f["afirmaciones"].append({"afirmacion": f"REF-RF-0001 prevé {sym} por encima de un número enorme", "fuente": "REF-RF-0001",
                              "direccion": "favorable", "pronostico_fuente": {
                                  "ref_id": "REF-RF-0001", "variable": "cierre", "serie_ht01": sym,
                                  "fecha_objetivo": str((hoy + pd.Timedelta(days=5)).date()), "umbral_o_rango": 10 ** 400,
                                  "direccion": "por_encima", "fecha_emision": str(hoy.date())}})
    return f


b = nuevo_bloque(Path(tempfile.mkdtemp(prefix="qa12_t125_h14_", dir=os.environ.get("QA_TMP"))), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
                 cfg=config_pruebas(modo="vivo"))
mock_respuestas._ficha = ficha
try:
    r = b.ciclo("2026-04-03", alcance={"clases": ["RV"]})
    print(f"C1 · {r['estado']}")
except Exception as e:  # noqa: BLE001
    print(f"C1 · EXCEPCIÓN {type(e).__name__}: {e}")
finally:
    mock_respuestas._ficha = F0
print(f"C1 · entradas que quedan: { {a: len(x) for a, x in b.almacen._entradas.items() if x} } · integridad {b.almacen.verificar_integridad()}")
r2 = b.ciclo("2026-04-10", alcance={"clases": ["RV"]})
print(f"C2 (respuestas normales, mismo almacén) · {r2['estado']} · run {r2['run_id']} · integridad {set(b.almacen.verificar_integridad().values())}")
