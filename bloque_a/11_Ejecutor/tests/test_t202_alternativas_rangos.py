"""T-202: ST-INF-001 pasa a SciPy la alternativa declarada en los contrastes de rangos (wilcoxon y mann_whitney).

T-202 tipa `_SCIPY_ALT` para mypy (scipy-stubs). Su mutante M01 (cambiar «mayor» por «menor») quedaba vivo: ninguna prueba
usaba una alternativa unilateral en los contrastes de rangos. Aquí, cada alternativa contra SciPy como oráculo y el sentido
de cada una con datos que están claramente por encima (p de «mayor» pequeño y p de «menor» grande).
"""
import math

import pytest
from bloque_a.motor import fichas_series as S
from scipy import stats

SCIPY = {"bilateral": "two-sided", "mayor": "greater", "menor": "less"}
POSITIVA = [0.5, 1.1, 0.3, 2.0, 0.9, -0.4, 1.7, -0.2, 1.3, 0.8]          # diferencias sobre todo positivas
ALTA, BAJA = [2.1, 3.4, 2.9, 4.2, 3.8, 2.6, 3.1], [0.4, 1.2, 0.9, 2.2, 1.5, 0.7]


def _p(contraste: dict, tipo: str, alt: str) -> float:
    ent = {"valores": {"contrastes": [dict(nombre="x", **contraste)]}, "series": {}, "series_rol": {}}
    res, _ = S.FICHAS["ST-INF-001"]["fn"](ent, {"tipo_contraste": tipo, "alternativa": alt})
    assert res["contrastes"]["x"]["alternativa"] == alt
    return res["contrastes"]["x"]["p_valor"]


@pytest.mark.parametrize("alt", sorted(SCIPY))
def test_wilcoxon_con_cada_alternativa_coincide_con_scipy(alt):
    assert math.isclose(_p({"muestra": POSITIVA}, "wilcoxon", alt),
                        float(stats.wilcoxon(POSITIVA, alternative=SCIPY[alt]).pvalue), rel_tol=1e-12)
    pareada = {"muestra_a": ALTA[:6], "muestra_b": BAJA}
    dif = [a - b for a, b in zip(ALTA[:6], BAJA)]
    assert math.isclose(_p(pareada, "wilcoxon", alt), float(stats.wilcoxon(dif, alternative=SCIPY[alt]).pvalue),
                        rel_tol=1e-12)


@pytest.mark.parametrize("alt", sorted(SCIPY))
def test_mann_whitney_con_cada_alternativa_coincide_con_scipy(alt):
    assert math.isclose(_p({"muestra_a": ALTA, "muestra_b": BAJA}, "mann_whitney", alt),
                        float(stats.mannwhitneyu(ALTA, BAJA, alternative=SCIPY[alt]).pvalue), rel_tol=1e-12)


@pytest.mark.parametrize("tipo,contraste", [("wilcoxon", {"muestra": POSITIVA}),
                                            ("mann_whitney", {"muestra_a": ALTA, "muestra_b": BAJA})])
def test_mayor_y_menor_tienen_el_sentido_declarado(tipo, contraste):
    mayor, menor, bilateral = (_p(contraste, tipo, a) for a in ("mayor", "menor", "bilateral"))
    assert mayor < 0.05 and menor > 0.5      # los datos están por encima: «mayor» rechaza H0 y «menor» no
    assert mayor < bilateral
