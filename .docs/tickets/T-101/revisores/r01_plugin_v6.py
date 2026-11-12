"""QA r01 de T-101 · Complemento de pytest que fuerza `diseno: v6` en toda configuración que cargue el ejecutor del Bloque A.

Sirve para pasar baterías escritas para la V5 (p. ej., `tests/test_v51.py`: C6, CT-23 y CT-25) con la V6 y ver qué se
rompe. Uso (desde `bloque_a/11_Ejecutor` de la raíz a probar):
  R01_EJEC=$PWD PYTHONPATH=<carpeta de este archivo> ../../.venv/bin/python -m pytest -p r01_plugin_v6 -q tests/test_v51.py
"""
import os
import sys

sys.path.insert(0, os.environ["R01_EJEC"])
from bloque_a import configuracion as _c  # noqa: E402

_orig = _c.cargar_config


def _v6(ruta=None, extra=None):
    cfg = _orig(ruta, extra)
    if cfg.get("diseno", "v5") == "v5" and not (extra or {}).get("diseno"):
        cfg["diseno"] = "v6"
    return cfg


_c.cargar_config = _v6
