"""T-152 · QA r01 · el umbral nuevo del desplazamiento (q/p ≤ 2·`tolerancia_clon`) en otras rejillas, niveles y familias.

Uso:  .venv/bin/python -I .docs/tickets/T-152/revisores/r01_01_umbral_qa.py [--raiz <copia>] [--semillas N]

Construye en memoria `motor/frontera_b.py` de la copia con varios umbrales de q/p (1 %, 1,9 %, el 2 % del código, 2,5 %,
4 %, 10 % y sin umbral) y mide, por familia y umbral:
- N: copias que deberían agruparse y no se agrupan (falsos negativos): truncadas en las rejillas 0,01, 0,05, 0,25, 1/8,
  1/32 y 0,001 en el tramo de q/p del 1 al 2 % (paseo normalizado y paseo geométrico), con sesiones ausentes, con precios
  sueltos, a otra escala, frente a la misma redondeada y frente a otra truncada más fina;
- X: copias truncadas cuyo precio cruza el 2 % de q/p (una parte de la historia por encima): límite declarado o no;
- F: series distintas que se agrupan (falsos positivos): índices con ρ 0,99 a 0,9999, índice frente a su rentabilidad
  total, fondo frente a índice, casi planas y monetarios con q/p del 2 al 100 %.
Solo informa (termina con 0). La lectura es del revisor en `qa.md`. Sin red ni coste; semillas fijas."""
import argparse
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--raiz", default=str(Path(__file__).resolve().parents[4]))
ap.add_argument("--semillas", type=int, default=60)
ap.add_argument("--solo", default="NXYF")
ARGS = ap.parse_args()
RAIZ = Path(ARGS.raiz).resolve()
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
import bloque_a.motor.operaciones  # noqa: E402,F401
from bloque_a.motor import fichas_mon_idx as fm  # noqa: E402
from bloque_a.motor import frontera_b as fb  # noqa: E402

LINEA = "    desplaza = rel <= tol\n"
TOL = fb.FRONTERA_B["tolerancia_clon"]
UMBRALES = {"1%": "2 * rel <= 0.01", "1,9%": "2 * rel <= 0.019", "2% (código)": None, "2,5%": "2 * rel <= 0.025",
            "4%": "2 * rel <= 0.04", "10%": "2 * rel <= 0.10", "sin umbral": "rel >= 0"}
F = pd.bdate_range("2025-06-02", periods=320)
AN = np.asarray((F - F[0]).days, dtype=float) / fm.DIAS_ANIO
T = len(F)


def modulo(expr):
    if expr is None:
        return fb
    fuente = Path(fb.__file__).read_text(encoding="utf-8")
    assert fuente.count(LINEA) == 1
    m = types.ModuleType("bloque_a.motor.frontera_b_qa")
    m.__package__, m.__file__ = "bloque_a.motor", fb.__file__
    exec(compile(fuente.replace(LINEA, f"    desplaza = {expr}\n"), m.__name__, "exec"), m.__dict__)  # noqa: S102
    return m


MODS = {k: modulo(v) for k, v in UMBRALES.items()}


def juntas(m, x, y):
    g = m._etiquetas_series_copiadas(np.vstack([x, y]), AN, TOL, 1.0)
    return bool(g[0] == g[1])


def tr(x, q):
    return np.floor(x / q + 1e-9) * q


def rd(x, q):
    return np.round(x / q) * q


def tramo(lo, hi, rng):
    u = np.cumsum(rng.normal(0, 0.03, T))
    return lo + (hi - lo) * (u - u.min()) / (u.max() - u.min())


def geom(nivel, rng, sd=0.006):
    return nivel * np.exp(np.cumsum(rng.normal(0, sd, T)))


def fila(nombre, gen, cuenta_si, n):
    c = dict.fromkeys(MODS, 0)
    for s in range(n):
        x, y = gen(np.random.default_rng(31000 + s))
        for k, m in MODS.items():
            c[k] += juntas(m, x, y) == cuenta_si
    print(f"| {nombre} | " + " | ".join(str(c[k]) for k in MODS) + " |", flush=True)
    return c


def cab(titulo):
    print(f"\n### {titulo} (de {ARGS.semillas})\n\n| Caso | " + " | ".join(MODS) + " |\n|---|" + "---|" * len(MODS))


def main():
    n = ARGS.semillas
    if "N" in ARGS.solo:
        cab("N · copias en el tramo de q/p del 1 al 2 % que NO se agrupan")
        casos = [("0,01 en [0,55, 0,95]", 0.01, 0.55, 0.95), ("0,05 en [2,6, 4,8]", 0.05, 2.6, 4.8),
                 ("0,25 en [13, 24]", 0.25, 13, 24), ("1/8 en [6,6, 12]", 1 / 8, 6.6, 12),
                 ("1/32 en [1,62, 3,0]", 1 / 32, 1.62, 3.0), ("0,001 en [0,052, 0,095]", 0.001, 0.052, 0.095)]
        for nombre, q, lo, hi in casos:
            fila(f"truncada {nombre}", lambda r, q=q, lo=lo, hi=hi: (lambda x: (x, tr(x, q)))(tramo(lo, hi, r)), False, n)
        for nombre, q, lo, hi in casos[:3]:
            fila(f"truncada {nombre}, frente a la redondeada", lambda r, q=q, lo=lo, hi=hi:
                 (lambda x: (rd(x, q), tr(x, q)))(tramo(lo, hi, r)), False, n)
        fila("truncada 0,05 en [2,6, 4,8] frente a otra truncada a 0,001", lambda r:
             (lambda x: (tr(x, 0.001), tr(x, 0.05)))(tramo(2.6, 4.8, r)), False, n)
        fila("geométrica a 0,05 alrededor de 3,5 (sin salir de [2,55, 4,9])", lambda r:
             (lambda x: (x, tr(x, 0.05)))(np.clip(geom(3.5, r, 0.004), 2.55, 4.9)), False, n)

        def ausentes(r):
            x = tramo(0.55, 0.95, r)
            y = tr(x, 0.01)
            y[r.random(T) < 0.05] = np.nan
            return x, y
        fila("truncada 0,01 con un 5 % de sesiones ausentes", ausentes, False, n)

        def sueltos(r):
            x = tramo(2.6, 4.8, r)
            y = tr(x, 0.05)
            k = r.random(T) < 0.04
            y[k] = x[k]
            return x, y
        fila("truncada 0,05 con un 4 % de precios sin redondear", sueltos, False, n)
        fila("truncada 0,01 a otra escala (×1,1, otra divisa)", lambda r: (lambda x: (x, tr(1.1 * x, 0.01)))(
            tramo(0.55, 0.85, r)), False, n)
        fila("las dos truncadas, 0,01 y 0,05 a otra escala (×4,3)", lambda r: (lambda x: (tr(x, 0.01), tr(4.3 * x, 0.05)))(
            tramo(0.62, 1.1, r)), False, n)
        fila("las dos redondeadas, 0,01 y 0,05 a otra escala (×4,3)", lambda r: (lambda x: (rd(x, 0.01), rd(4.3 * x, 0.05)))(
            tramo(0.62, 1.1, r)), False, n)
        fila("las dos truncadas, 0,01 y 0,05 a otra escala (×4,3), sin cruzar de década", lambda r: (
            lambda x: (tr(x, 0.01), tr(4.3 * x, 0.05)))(tramo(0.62, 0.99, r)), False, n)
        fila("truncada 0,05 frente a redondeada 0,01 (×4,3), sin cruzar de década", lambda r: (
            lambda x: (rd(x, 0.01), tr(4.3 * x, 0.05)))(tramo(0.62, 0.99, r)), False, n)
    if "X" in ARGS.solo:
        cab("X · copias que cruzan el 2 % de q/p (parte de la historia por encima): NO se agrupan")
        for nombre, lo, hi in (("0,01 en [0,4905, 0,9] (por encima, solo lo más bajo)", 0.4905, 0.9),
                               ("0,01 en [0,49, 0,9] (el mínimo justo en la rejilla)", 0.49, 0.9),
                               ("0,01 en [0,45, 0,9]", 0.45, 0.9), ("0,01 en [0,40, 0,66]", 0.40, 0.66),
                               ("0,05 en [2,3, 4]", 2.3, 4.0)):
            q = 0.05 if "0,05" in nombre else 0.01
            fila(f"truncada {nombre}", lambda r, q=q, lo=lo, hi=hi: (lambda x: (x, tr(x, q)))(tramo(lo, hi, r)), False, n)
            fila(f"redondeada {nombre}", lambda r, q=q, lo=lo, hi=hi: (lambda x: (x, rd(x, q)))(tramo(lo, hi, r)), False, n)
    if "Y" in ARGS.solo:
        cab("Y · copias truncadas con todo el tramo justo por encima del 2 % de q/p que NO se agrupan")
        for q, lo, hi in ((0.01, 0.4905, 0.4995), (0.01, 0.485, 0.4995), (0.01, 0.46, 0.49), (0.05, 2.3, 2.45),
                          (0.05, 2.43, 2.49), (0.01, 0.44, 0.49), (0.01, 0.40, 0.45)):
            fila(f"truncada {q:g} en [{lo:g}, {hi:g}] (q/p {q / hi:.2%} a {q / lo:.2%})",
                 lambda r, q=q, lo=lo, hi=hi: (lambda x: (x, tr(x, q)))(tramo(lo, hi, r)), False, n)
        for q, lo, hi in ((0.01, 0.4905, 0.9), (0.01, 0.48, 0.9), (0.01, 0.47, 0.9), (0.01, 0.45, 0.9)):
            fila(f"truncada {q:g} en [{lo:g}, {hi:g}] (cruza: q/p {q / hi:.2%} a {q / lo:.2%})",
                 lambda r, q=q, lo=lo, hi=hi: (lambda x: (x, tr(x, q)))(tramo(lo, hi, r)), False, n)
    if "F" in ARGS.solo:
        cab("F · series distintas que SÍ se agrupan (falsos positivos)")
        for q, nivel, sd in ((0.05, 3.6, 0.006), (0.25, 18, 0.006), (1 / 8, 9, 0.006), (1 / 32, 2.2, 0.006),
                             (0.001, 0.07, 0.006), (0.01, 0.7, 0.006)):
            for rho in (0.99, 0.995, 0.999):
                for o1, o2, nom in ((rd, tr, "r/t"), (tr, tr, "t/t")):
                    def gen(r, q=q, nivel=nivel, rho=rho, o1=o1, o2=o2, sd=sd):
                        e = r.normal(0, sd, T)
                        x = nivel * np.exp(np.cumsum(e))
                        y = x * np.exp(np.cumsum(r.normal(0, sd * np.sqrt(2 * (1 - rho)), T)))
                        return o1(x, q), o2(y, q)
                    fila(f"ρ {rho}, paso {q:g} a {nivel:g} (q/p ≈ {q / nivel:.1%}), {nom}", gen, True, n)

        for q, nivel in ((0.05, 3.6), (1 / 8, 9), (0.01, 0.7)):
            def rt(r, q=q, nivel=nivel):
                x = geom(nivel, r)
                return tr(x, q), tr(x * 1.02 ** AN, q)
            fila(f"índice frente a su RT (2 %/año), truncados, paso {q:g} a {nivel:g}", rt, True, n)
            for te in (0.001, 0.0001):
                def fondo(r, q=q, nivel=nivel, te=te):
                    x = geom(nivel, r)
                    return rd(x, q), tr(x * np.exp(np.cumsum(r.normal(0, te / np.sqrt(252), T))), q)
                fila(f"fondo (TE {te:.2%}/año) frente a índice, r/t, paso {q:g} a {nivel:g}", fondo, True, n)

        for nivel, q in ((0.5, 0.01), (0.3, 0.01), (0.25, 0.01), (0.12, 0.01), (2.0, 0.05), (1.0, 0.05), (1.0, 1.0)):
            def plano(r, nivel=nivel, q=q):
                x = np.full(T, nivel)
                x[r.random(T) < 0.08] = nivel + q
                y = np.round(nivel * 1.01 ** (np.arange(T) / 252) * (1 + r.normal(0, 0.0002, T)), 4)
                return x, y
            fila(f"casi plana a {nivel:g} (paso {q:g}, q/p {q / nivel:.0%}) frente a otra que crece 1 %/año", plano, True, n)

            def plano_tr(r, nivel=nivel, q=q):
                x = np.full(T, nivel)
                x[r.random(T) < 0.3] = nivel + q
                y = tr(nivel * 1.01 ** (np.arange(T) / 252) * (1 + r.normal(0, 0.002, T)), q / 10 if q < 1 else 0.01)
                return x, y
            fila(f"casi plana a {nivel:g} (30 % a +1 paso) frente a otra truncada más fina", plano_tr, True, n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
