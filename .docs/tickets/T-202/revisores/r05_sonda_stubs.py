"""T-202 · QA r01 · sonda para r05_gate_segun_entorno.sh: usos erróneos de las librerías con stubs (no se ejecuta)."""
import jsonschema
import numpy as np
import yaml
from scipy import optimize, stats


def f(x: list[float]) -> float:
    a = stats.wilcoxon(x, alternative="mayor")             # 1: valor en español pasado tal cual a SciPy
    b = stats.ttest_1samp(x, 0.0, alternativ="less")        # 2: argumento mal escrito
    c = optimize.minimize(lambda t: float(t[0]), np.zeros(1), method="SLSQPP")  # 3: método inexistente
    d = yaml.safe_dump({"a": 1}, sort_key=True)             # 4: argumento mal escrito
    jsonschema.validate({"a": 1})                           # 5: falta el esquema
    e = stats.norm.ppf("0.5")                               # 6: texto en vez de número
    return float(a.pvalue) + float(b.pvalue) + float(c.fun) + len(d) + float(e)
