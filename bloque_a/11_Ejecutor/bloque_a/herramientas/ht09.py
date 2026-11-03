"""HT-09: reexporta la implementación de referencia `ht09_validador_g3` (copia literal de 10_Herramientas)."""
from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)
import ht09_validador_g3 as _ref  # noqa: E402
from ht09_validador_g3 import *  # noqa: F401,F403,E402

modulo = _ref
