"""HT-02: reexporta la implementación de referencia `ht02_verificador_enlaces` (copia literal de 10_Herramientas)."""
from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)
import ht02_verificador_enlaces as _ref  # noqa: E402
from ht02_verificador_enlaces import *  # noqa: F401,F403,E402

modulo = _ref
