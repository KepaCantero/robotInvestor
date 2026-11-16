import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

DATOS = RAIZ / "ejemplos" / "datos_sinteticos"
AS_OF = "2026-06-05"


def config_pruebas(**extra):
    # Las pruebas ejercitan los 12 perfiles; el valor por defecto (solo DIV, PA-01) tiene sus pruebas propias
    base = {"modo": "backtest", "evaluacion": {"bootstrap_replicas": 300, "simulaciones_ece": 300},
            "perfiles": {"activos": ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]}}
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


def certificado_con_reejecucion(almacen, celda, cid=None, estado="VIGENTE", motor=None, cfg=None):
    """T-163 (QA r01 de T-160, H-02): escribe en F6 un CERT- con lo que piden `certificados_vigentes` y CT-04 desde T-163: un
    cálculo de soporte FC-EVAL-001 del Motor (con el método de la celda), su re-ejecución CT-10 coincidente en el Registro de
    cálculos y las cifras de ese soporte. Para las pruebas que necesitan un certificado VIGENTE y prueban otra cosa (publicación,
    revocación por deterioro), que antes lo escribían a mano sin re-ejecución. Las cifras son de unos datos sintéticos, no de
    los PRG de la celda: lo que se ata es el certificado a su soporte."""
    from bloque_a.evaluador import campos_certificado
    from bloque_a.motor.servicio import Motor

    motor = motor or Motor(almacen, None, cfg or config_pruebas())
    n = 60
    valores = {"p": [0.8, 0.2] * (n // 2), "o": [1, 0, 1, 0, 0, 1] * (n // 6), "p_ref": [0.5] * n,
               "fechas": [f"2025-0{1 + i // 20}-{1 + i % 20:02d}" for i in range(n)]}
    res = motor.servir({"operacion": "FC-EVAL-001", "clase": celda["clase"], "horizonte": celda["horizonte"],
                        "fecha_corte": str(almacen.reloj.fecha), "datos": [{"valores": valores}],
                        "parametros": {"replicas": 50, "simulaciones": 50, "min_conglomerados": 2, "metodo": celda.get("metodo")}},
                       "AG-20")
    assert str(res["estado"]).startswith("SERVED"), res
    rex = motor.reejecutar(res["calc_id"], "prueba: certificado de horizonte con su re-ejecución CT-10", "AG-20")
    assert rex["coincide"] == "SI", rex
    soporte = almacen.estado("RC")[res["calc_id"]]
    cert = {"tipo_entrada": "CERT", "id": cid or almacen.nuevo_id("CERT"), "estado": estado, "celda": dict(celda),
            **campos_certificado(res["resultado"]), "calc_soporte": res["calc_id"], "curva_fiabilidad": res["calc_id"],
            "huella_entradas": soporte["datos"][0]["huella"], "reejecucion": rex["calc_id"]}
    almacen.escribir("F6", "AG-20", cert)
    return cert
