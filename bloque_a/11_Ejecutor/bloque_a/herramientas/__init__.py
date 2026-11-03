"""Herramientas deterministas del Bloque A (HT-01 a HT-09).

HT-02, HT-03, HT-07 y HT-09 son copias literales de las implementaciones de referencia de
`10_Herramientas` (carpeta `referencia/`); la prueba `test_herramientas.py` comprueba que no divergen.
"""
import sys
from pathlib import Path

DIR_REFERENCIA = Path(__file__).resolve().parent / "referencia"
if str(DIR_REFERENCIA) not in sys.path:
    sys.path.insert(0, str(DIR_REFERENCIA))
