"""QA r03 de T-106 · Mutantes frente a TODAS las pruebas de T-106 (también `tests/test_t106_r03.py`) y mutantes nuevos sobre
el código de la r03.

`r02_04_mutantes.py` no se toca: su texto se lee, se cambia en memoria la lista de pruebas de cada familia (se añade
`tests/test_t106_r03.py`, que la r03 creó) y se le añaden al final de `MUTANTES` los mutantes nuevos de la r03:

  - N01–N05 (MON/IDX, H-14 y H-16): sin el rechazo de umbrales, sufijos o nombres sueltos fuera de `UMBRALES`,
    limitación de MON-EXP que nunca salta, incertidumbre de la probabilidad a la mitad;
  - N06–N13 (`servicio.py`, H-15): cada comprobación de `_error_de_forma` y el `except` nuevo de los datos, quitados;
    el motivo de la petición mal formada cambiado;
  - N14 (DER-VRP-001, H-20): rango de `nivel_es` abierto otra vez.

Así se mide lo que pide el revisor: un mutante vivo frente a casos de control y a todas las pruebas de T-106 a la vez es
una regla sin red.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r03_05_mutantes.py [RAIZ] [--solo ID] [--solo-nuevos]
"""
from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
R02 = AQUI / "r02_04_mutantes.py"
src = R02.read_text(encoding="utf-8")

VIEJO_PRUEBA = 'T106 = ["tests/test_fase1_mon_idx.py", "tests/test_fase1_fon_der.py", "tests/test_fase1_tcv.py", "tests/test_t106_motor.py"]'
NUEVO_PRUEBA = ('T106 = ["tests/test_fase1_mon_idx.py", "tests/test_fase1_fon_der.py", "tests/test_fase1_tcv.py", '
                '"tests/test_t106_motor.py", "tests/test_t106_r03.py"]')
VIEJO_FAM = "PRUEBA = {MI: [T106[0], T106[3]], FD: [T106[1], T106[3]], TC: [T106[2], T106[3]],"
NUEVO_FAM = "PRUEBA = {MI: [T106[0], T106[3], T106[4]], FD: [T106[1], T106[3], T106[4]], TC: [T106[2], T106[3], T106[4]],"
assert src.count(VIEJO_PRUEBA) == 1 and src.count(VIEJO_FAM) == 1, "r02_04 cambió: revisar el parche"
src = src.replace(VIEJO_PRUEBA, NUEVO_PRUEBA).replace(VIEJO_FAM, NUEVO_FAM)

NUEVOS = '''
    # ---------------------------------------------------------------- r03 (QA r03 de T-106)
    ("N01", MI, "IDX-ERP-001", [("    fijos = set(params or {}) & UMBRALES[ficha]\\n", "    fijos = set()\\n")],
     "H-14 deshecho: la petición vuelve a cambiar umbrales"),
    ("N02", MI, "IDX-REL-001", [('k.endswith(("_min", "_rango", "_min_anios", "_recomendados"))', 'k.endswith(("_min", "_rango", "_min_anios"))')],
     "«*_recomendados» fuera de UMBRALES (umbral de limitación)"),
    ("N03", MI, "MON-EXP-001", [(' or k in ("meses_nodos", "anios_convexidad"))', ')')],
     "meses_nodos y anios_convexidad fuera de UMBRALES"),
    ("N04", MI, "MON-EXP-001", [('    if peor["incertidumbre_probabilidad"] > tol:', '    if peor["incertidumbre_probabilidad"] > 1.0:')],
     "H-16 deshecho: la limitación por redondeo no salta nunca"),
    ("N05", MI, "MON-EXP-001", [('"incertidumbre_probabilidad": min(1.0, cota_r[k - 1] / incremento)})',
                                 '"incertidumbre_probabilidad": min(1.0, cota_r[k - 1] / incremento / 2)})')],
     "incertidumbre de la probabilidad a la mitad"),
    ("N06", SV, None, [('        if peticion.get("plan", "PLAN_MIN") not in planes:\\n            return f"plan desconocido',
                        '        if False:\\n            return f"plan desconocido')], "H-15: sin comprobar el plan"),
    ("N07", SV, None, [('                if pd.isna(pd.Timestamp(peticion["fecha_corte"])):', '                if False:')],
     "H-15: «fecha_corte» vacía aceptada"),
    ("N08", SV, None, [('            if "valores" in d and not isinstance(d["valores"], dict):', '            if False:')],
     "H-15: «valores» que no son un objeto"),
    ("N09", SV, None, [('            if "serie" in d and not isinstance(d["serie"], str):', '            if False:')],
     "H-15: «serie» que no es texto"),
    ("N10", SV, None, [('        except (TypeError, ValueError, OverflowError) as e:   # H-15', '        except (OverflowError,) as e:   # H-15')],
     "H-15: fechas ilegibles de una serie sin capturar"),
    ("N11", SV, None, [('            return self._rechazo(base_, "DATOS_INCOHERENTES", f"petición mal formada: {forma}")',
                        '            return self._rechazo(base_, "DATOS_INSUFICIENTES", f"petición mal formada: {forma}")')],
     "H-15: motivo de la petición mal formada"),
    ("N12", SV, None, [('        if peticion.get("parametros") is not None and not isinstance(peticion["parametros"], dict):',
                        '        if False:')], "H-15: «parametros» que no son un objeto (llega a dict(...))"),
    ("N13", SV, None, [('        if datos is not None and not (isinstance(datos, list) and all(isinstance(d, dict) for d in datos)):',
                        '        if False:')], "H-15: «datos» que no es una lista de objetos"),
    ("N14", FD, "DER-VRP-001", [('"DER-VRP-001": {"plazo": (7, 90), "nivel_es": (0.90, 0.99)},', '"DER-VRP-001": {"plazo": (7, 90), "nivel_es": (0.01, 0.999)},')],
     "H-20 deshecho: nivel_es fuera de 0,90–0,99"),
]
'''
MARCA = "]\n\n# Copia del bloque_a entero"
assert src.count(MARCA) == 1, "r02_04 cambió: revisar el parche"
src = src.replace(MARCA, NUEVOS.rstrip("\n").rstrip("]").rstrip() + "\n" + MARCA, 1)
if "--solo-nuevos" in sys.argv:
    src = src.replace("    if SOLO and mid != SOLO:\n        continue", "    if not mid.startswith('N') or (SOLO and mid != SOLO):\n        continue")
    sys.argv.remove("--solo-nuevos")

codigo = compile(src, str(R02), "exec")
exec(codigo, {"__name__": "__main__", "__file__": str(R02)})
