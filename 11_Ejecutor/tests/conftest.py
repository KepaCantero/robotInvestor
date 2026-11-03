import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

DATOS = RAIZ / "ejemplos" / "datos_sinteticos"
AS_OF = "2026-06-05"


def config_pruebas(**extra):
    base = {"modo": "backtest", "evaluacion": {"bootstrap_replicas": 300, "simulaciones_ece": 300}}
    from bloque_a.configuracion import fusionar
    return cargar_config(extra=fusionar(base, extra))


@pytest.fixture(scope="session")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def nuevo_bloque(tmp, universo, cliente=None, cfg=None, universo_df=None, **kw):
    return Bloque(cfg or config_pruebas(), ProveedorCSV(DATOS), universo_df if universo_df is not None else universo,
                  cliente or MockClient(), Path(tmp) / "estado", Path(tmp) / "ent", **kw)


@pytest.fixture(scope="module")
def ciclo_semanal(tmp_path_factory, universo):
    """Un ciclo semanal completo (todas las clases N2) y un segundo ciclo una semana después."""
    tmp = tmp_path_factory.mktemp("ciclo")
    b = nuevo_bloque(tmp, universo)
    r1 = b.ciclo(AS_OF)
    r2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()))
    return b, r1, r2
