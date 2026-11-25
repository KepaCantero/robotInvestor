"""HT-07: reexporta la implementación de referencia `ht07_legibilidad` (copia literal de 10_Herramientas)."""
from typing import TYPE_CHECKING

from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)

if TYPE_CHECKING:   # T-201: mypy lee la copia por su ruta de paquete; en ejecución se importa como siempre, desde sys.path
    from .referencia import ht07_legibilidad as _ref
    from .referencia.ht07_legibilidad import *
else:
    import ht07_legibilidad as _ref
    from ht07_legibilidad import *

modulo = _ref
