"""HT-03: reexporta la implementación de referencia `ht03_puntuaciones` (copia literal de 10_Herramientas)."""
from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)
import ht03_puntuaciones as _ref  # noqa: E402
from ht03_puntuaciones import *  # noqa: F401,F403,E402

modulo = _ref
