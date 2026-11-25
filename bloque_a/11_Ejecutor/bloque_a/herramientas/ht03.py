"""HT-03: reexporta la implementación de referencia `ht03_puntuaciones` (copia literal de 10_Herramientas)."""
from typing import TYPE_CHECKING

from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)

if TYPE_CHECKING:   # T-201: mypy lee la copia por su ruta de paquete; en ejecución se importa como siempre, desde sys.path
    from .referencia import ht03_puntuaciones as _ref
    from .referencia.ht03_puntuaciones import *
else:
    import ht03_puntuaciones as _ref
    from ht03_puntuaciones import *

modulo = _ref
