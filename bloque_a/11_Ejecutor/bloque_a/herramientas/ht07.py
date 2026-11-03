"""HT-07: reexporta la implementación de referencia `ht07_legibilidad` (copia literal de 10_Herramientas)."""
from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)
import ht07_legibilidad as _ref  # noqa: E402
from ht07_legibilidad import *  # noqa: F401,F403,E402

modulo = _ref
