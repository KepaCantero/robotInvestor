"""HT-02: reexporta la implementación de referencia `ht02_verificador_enlaces` (copia literal de 10_Herramientas)."""
from typing import TYPE_CHECKING

from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)

if TYPE_CHECKING:   # T-201: mypy lee la copia por su ruta de paquete; en ejecución se importa como siempre, desde sys.path
    from .referencia import ht02_verificador_enlaces as _ref
    from .referencia.ht02_verificador_enlaces import *
else:
    import ht02_verificador_enlaces as _ref
    from ht02_verificador_enlaces import *

modulo = _ref
