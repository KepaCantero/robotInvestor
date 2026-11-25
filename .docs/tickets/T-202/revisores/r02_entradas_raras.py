"""T-202 · QA r01 · entradas raras en las tres fichas tocadas, develop frente a la rama.

Ejecuta la misma batería (NaN, ±inf, None, vacíos, textos, booleanos, extremos, empates, longitudes distintas,
alternativas fuera del dominio, k fuera de rango, superficies planas o con valores extremos…) en cada copia, cada una
con su Python, y compara el JSON de resultados (repr de cada número, tipo y texto de cada rechazo). Cualquier diferencia
es un cambio de comportamiento. Sale con 0 si todo es igual.
Uso: python3 r02_entradas_raras.py --base <copia develop> --base-python <py> --nuevo <copia rama> --nuevo-python <py>
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

BATERIA = r'''
import copy, json, math, sys, warnings
warnings.simplefilter("ignore")
import numpy as np
from bloque_a.motor import fichas_fon_der as D, fichas_reales as R, fichas_series as S
out = {"modulos": [m.__file__ for m in (S, R, D)], "casos": {}}
def correr(clave, mod, ficha, valores, params):
    ent = {"valores": copy.deepcopy(valores), "series": {}, "series_rol": {}}
    try:
        res = mod.FICHAS[ficha]["fn"](ent, dict(params))
        out["casos"][clave] = {"ok": json.loads(json.dumps(res, default=repr, sort_keys=True, allow_nan=True))}
    except Exception as e:
        out["casos"][clave] = {"error": type(e).__name__ + ": " + str(e)}
NAN, INF = float("nan"), float("inf")
base = [0.5, 1.1, 0.3, 2.0, 0.9, -0.4, 1.7, -0.2, 1.3, 0.8]
A, B = [2.1, 3.4, 2.9, 4.2, 3.8, 2.6, 3.1], [0.4, 1.2, 0.9, 2.2, 1.5, 0.7]
muestras = {
    "normal": base, "nan": base[:-1] + [NAN], "inf": base[:-1] + [INF], "-inf": [-INF] + base[1:],
    "none": base[:-1] + [None], "texto": base[:-1] + ["1.0"], "bool": base[:-1] + [True], "vacia": [],
    "una": [1.0], "ceros": [0.0] * 10, "empates": [1.0] * 10, "enorme": [1e308, -1e308] * 5,
    "diminuta": [1e-308, -2e-308, 3e-308, 4e-308, -5e-308, 6e-308, 7e-308, 8e-308], "no_lista": "abc",
    "dict": {"a": 1}, "larga": [((i * 37) % 101) / 50 - 1 for i in range(5000)],
}
alts = ["bilateral", "mayor", "menor", "MAYOR", "greater", "two-sided", "", None, 1, ["mayor"]]
for alt in alts:
    for nm, m in muestras.items():
        correr(f"wil/{nm}/{alt!r}", S, "ST-INF-001", {"contrastes": [{"nombre": "x", "muestra": m}]},
               {"tipo_contraste": "wilcoxon", "alternativa": alt})
        correr(f"mw/{nm}/{alt!r}", S, "ST-INF-001", {"contrastes": [{"nombre": "x", "muestra_a": m, "muestra_b": B}]},
               {"tipo_contraste": "mann_whitney", "alternativa": alt})
    for mu0 in (0.0, NAN, INF, -1e300, "0", None):
        correr(f"wil_mu0/{mu0!r}/{alt!r}", S, "ST-INF-001", {"contrastes": [{"nombre": "x", "muestra": base, "mu0": mu0}]},
               {"tipo_contraste": "wilcoxon", "alternativa": alt})
        correr(f"mw_mu0/{mu0!r}/{alt!r}", S, "ST-INF-001",
               {"contrastes": [{"nombre": "x", "muestra_a": A, "muestra_b": B, "mu0": mu0}]},
               {"tipo_contraste": "mann_whitney", "alternativa": alt})
    correr(f"wil_pareada_distinta/{alt!r}", S, "ST-INF-001", {"contrastes": [{"nombre": "x", "muestra_a": A, "muestra_b": B}]},
           {"tipo_contraste": "wilcoxon", "alternativa": alt})
    correr(f"mw_iguales/{alt!r}", S, "ST-INF-001", {"contrastes": [{"nombre": "x", "muestra_a": A, "muestra_b": A}]},
           {"tipo_contraste": "mann_whitney", "alternativa": alt})
    correr(f"mw_varios/{alt!r}", S, "ST-INF-001", {"contrastes": [{"nombre": "x", "muestra_a": A, "muestra_b": B},
           {"nombre": "y", "muestra_a": B, "muestra_b": A}, {"nombre": "z", "muestra_a": A, "muestra_b": A[::-1]}]},
           {"tipo_contraste": "mann_whitney", "alternativa": alt})
# ALT-DESMOOTH-001 GLM
obs = R._AD_OBS_GLM
for k in (0, 1, 2, 3, 4, 6, -1, 2.0, 2.5, "2", True, None):
    correr(f"glm/k={k!r}", R, "ALT-DESMOOTH-001", R._datos_alt(obs), {"metodo": "GLM", "k": k})
for nm, serie in {"constante": np.full(len(obs), 0.01), "nan": np.r_[obs[:-1], NAN], "inf": np.r_[obs[:-1], INF],
                  "enorme": obs * 1e150, "diminuta": obs * 1e-150, "alterna": np.array([(-1) ** i * 0.05 for i in range(len(obs))]),
                  "real": R._AD_REAL_GLM}.items():
    for k in (1, 2, 3):
        correr(f"glm/{nm}/k={k}", R, "ALT-DESMOOTH-001", R._datos_alt(serie), {"metodo": "GLM", "k": k})
# DER-SKEW-001 SVI
base_svi = D._ctl_skew_svi()
def sup(**cambios):
    v = copy.deepcopy(base_svi)
    v["superficie"].update(cambios)
    return v
K = base_svi["superficie"]["strikes"]
vols = base_svi["superficie"]["vols"]
variantes = {
    "control": base_svi, "plana": sup(vols=[0.2] * len(K)), "vol_nan": sup(vols=vols[:-1] + [NAN]),
    "vol_inf": sup(vols=vols[:-1] + [INF]), "vol_cero": sup(vols=[0.0] + vols[1:]), "vol_enorme": sup(vols=[v * 50 for v in vols]),
    "vol_diminuta": sup(vols=[v * 1e-6 for v in vols]), "cinco": sup(strikes=K[::4], vols=vols[::4]),
    "cuatro": sup(strikes=K[:4], vols=vols[:4]), "desordenada": sup(strikes=K[::-1], vols=vols[::-1]),
    "forward_cero": sup(forward=0.0), "forward_nan": sup(forward=NAN), "forward_lejos": sup(forward=1e6),
    "desalineada": sup(vols=vols[:-1]), "texto": sup(vols=vols[:-1] + ["0.2"]), "none": sup(vols=None),
    "sonrisa": sup(vols=[0.2 + 0.5 * (math.log(x / 100)) ** 2 for x in K]),
}
for nm, v in variantes.items():
    for met in ("SVI", "deltas", "svi", None):
        correr(f"svi/{nm}/{met!r}", D, "DER-SKEW-001", v, {"metodo": met})
# casos de control de los tres módulos, otra vez, con los parámetros de cada caso
for mod in (S, R, D):
    for ficha, casos in sorted(mod.CASOS_CONTROL.items()):
        for i, caso in enumerate(casos):
            valores = {}
            for d in caso["datos"]:
                valores.update(copy.deepcopy(d["valores"]))
            correr(f"control/{ficha}/{i}", mod, ficha, valores, caso.get("parametros") or {})
json.dump(out, sys.stdout, ensure_ascii=False, sort_keys=True, indent=0, default=repr)
'''


def lado(repo: Path, python: str) -> dict:
    ej = repo / "bloque_a" / "11_Ejecutor"
    r = subprocess.run([python, "-c", BATERIA], cwd=ej, capture_output=True, text=True, check=False,
                       env={"PYTHONPATH": str(ej), "PYTHONHASHSEED": "0", "PATH": "/usr/bin:/bin"})
    if r.returncode:
        sys.exit(f"{repo}: la batería falló\n{r.stderr[-2000:]}")
    d = json.loads(r.stdout)
    if not all(m.startswith(str(ej)) for m in d["modulos"]):
        sys.exit(f"{repo}: las fichas no se cargaron de su copia: {d['modulos']}")
    return d["casos"]


def main() -> int:
    ap = argparse.ArgumentParser()
    for x in ("base", "nuevo"):
        ap.add_argument(f"--{x}", type=Path, required=True)
        ap.add_argument(f"--{x}-python", required=True)
    a = ap.parse_args()
    cb, cn = lado(a.base, a.base_python), lado(a.nuevo, a.nuevo_python)
    difs = sorted(k for k in set(cb) | set(cn) if json.dumps(cb.get(k), sort_keys=True) != json.dumps(cn.get(k), sort_keys=True))
    ok = sum(1 for v in cb.values() if "ok" in v)
    print(f"{len(cb)} casos ({ok} servidos, {len(cb) - ok} rechazados); {len(difs)} diferencias")
    for g in sorted({k.split("/")[0] for k in cb}):
        sub = [v for k, v in cb.items() if k.split("/")[0] == g]
        print(f"  {g}: {len(sub)} casos, {sum('ok' in v for v in sub)} servidos")
    for k in difs[:30]:
        print("  distinto:", k, "\n    develop:", json.dumps(cb.get(k))[:300], "\n    rama:   ", json.dumps(cn.get(k))[:300])
    return 1 if difs else 0


if __name__ == "__main__":
    sys.exit(main())
