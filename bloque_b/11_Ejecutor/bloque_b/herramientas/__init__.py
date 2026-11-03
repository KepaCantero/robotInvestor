"""Herramientas deterministas del Bloque B. HT-02, HT-03, HT-07, HT-08, HT-09, HT-10 y HT-11 son copias literales de
`10_Herramientas` (carpeta `referencia/`); una prueba comprueba que no divergen. HT-01 (datos y bóveda), HT-04
(gráficos), HT-05 (planificador) y HT-06 (índice) son propias del ejecutor."""
import sys
from pathlib import Path

DIR_REFERENCIA = Path(__file__).resolve().parent / "referencia"
if str(DIR_REFERENCIA) not in sys.path:
    sys.path.insert(0, str(DIR_REFERENCIA))

import ht02_verificador_enlaces as ht02  # noqa: E402,F401
import ht03_puntuaciones as ht03  # noqa: E402,F401
import ht07_legibilidad as ht07  # noqa: E402,F401
import ht08_monitor_tiempo as ht08  # noqa: E402,F401
import ht09_validador_g3 as ht09  # noqa: E402,F401
import ht10_anexo_datos as ht10  # noqa: E402,F401
import ht11_cribador as ht11  # noqa: E402,F401
