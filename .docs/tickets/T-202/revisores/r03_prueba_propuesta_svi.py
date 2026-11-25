"""T-202 · QA r01 · prueba propuesta para H-01: DER-SKEW-001 SVI ajusta por mínimos cuadrados SIN pesos.

Los casos de control de SVI usan una superficie que es exactamente SVI (residuo nulo en el óptimo), así que cualquier
residuo con el mismo cero (con pesos, escalado…) da el mismo ajuste: el mutante RQ05 de r01_mutantes.py vive.
Con una superficie que no es SVI (sonrisa con un rizo determinista, sin arbitraje), el RMSE publicado tiene que ser el
de los parámetros publicados sobre la varianza total observada, sin pesos (con pesos, `ajuste.fun` es el residuo
ponderado y el RMSE publicado deja de casar con los parámetros).
Uso: copiar a bloque_a/11_Ejecutor/tests/ y pytest -q (o ejecutarlo desde allí con pytest <ruta>).
"""
import copy
import math

import numpy as np
from bloque_a.motor import fichas_fon_der as D


def _superficie_no_svi() -> tuple[dict, np.ndarray, float]:
    v = copy.deepcopy(D._ctl_skew_svi())
    K = v["superficie"]["strikes"]
    v["superficie"]["vols"] = [0.2 + 0.5 * math.log(x / 100) ** 2 + 0.002 * math.sin(7 * i) for i, x in enumerate(K)]
    return v, np.log(np.array(K) / v["superficie"]["forward"]), 0.25


def test_svi_rmse_publicado_es_el_de_los_parametros_sin_pesos():
    v, k, T = _superficie_no_svi()
    res, _ = D.FICHAS["DER-SKEW-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {"metodo": "SVI"})
    s = res["svi"]
    x = np.array([s["a"], s["b"], s["rho"], s["m"], s["sigma"]])
    w_obs = np.array(v["superficie"]["vols"]) ** 2 * T
    r = D._svi(x, k)[0] - w_obs
    assert s["rmse_varianza_total"] > 1e-6                       # la superficie no es SVI: hay residuo
    assert math.isclose(s["rmse_varianza_total"], float(np.sqrt(np.mean(r ** 2))), rel_tol=1e-9)
