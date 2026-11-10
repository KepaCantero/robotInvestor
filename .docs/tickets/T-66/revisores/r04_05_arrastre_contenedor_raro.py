"""T-66 · QA r04 · `objeciones_internas` de F3 que no es una lista (estado manipulado o fuera de esquema).

`_objeciones_arrastre` trata como fuerte abierta una objeción mal formada, pero ¿y un contenedor que no es una lista (dict,
cadena) con fuertes sin resolver dentro? Se comprueba G2 (N1) y el veredicto con el guardado «tesis robusta».

Uso: PYTHONPATH=<ejecutor de A>:<revisores r01> python r04_05_arrastre_contenedor_raro.py   (imprime OK / HALLAZGO / INFO)
"""
import copy

import pandas as pd
from r01_comun import bloque, comprobar, fin

b = bloque()
b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
base = next(v for v in b.almacen.estado("F3").values() if v.get("rango_top3"))
b.fijar_fecha("2026-06-12")
abierta = {"objecion_id": "OBJ-XLU-01", "fuerza": "fuerte", "resumen": "-", "respuesta": None, "resuelta": False}
for nombre, cont in {"dict con una fuerte abierta": {"0": abierta}, "cadena": "OBJ-XLU-01 fuerte abierta",
                     "lista vacía": [], "None": None}.items():
    v = copy.deepcopy(base)
    v["objeciones_internas"], v["veredicto_refutacion"] = cont, "tesis robusta"
    f = b._desde_f3(v, {"senales": {}}, pd.Timestamp("2026-06-12"))
    pu = b._puertas(f, "N1", pd.Timestamp("2026-06-12"), list(f["_hz"]))
    raro = not isinstance(cont, list) and cont is not None
    comprobar(f"objeciones_internas {nombre}: G2 {'no pasa' if raro else 'según la regla'}", (not pu["G2"]) if raro else True,
              f"G2 {pu['G2']}, veredicto {f['_veredicto']}, objeciones normalizadas {len(f['_objeciones'])}", hallazgo=False)
fin()
