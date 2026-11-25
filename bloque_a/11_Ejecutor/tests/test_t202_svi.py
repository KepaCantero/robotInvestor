"""T-202 (QA r01, H-01): DER-SKEW-001 SVI ajusta por mínimos cuadrados sin pesos.

T-202 cambia la `lambda` del residuo SVI por la función `residuo`. Los casos de control de SVI usan una superficie que es
exactamente SVI (residuo nulo en el óptimo), así que cualquier residuo con el mismo cero (con pesos, escalado…) daba el
mismo ajuste y el mutante RQ05 de la QA (residuo con pesos de 1 a 2) quedaba vivo. Con una sonrisa con un rizo
determinista, que no es SVI y no tiene arbitraje, el RMSE publicado tiene que ser el de los parámetros publicados sobre la
varianza total observada, sin pesos. La prueba es la que propone la QA (`.docs/tickets/T-202/revisores/r03_…`).
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
