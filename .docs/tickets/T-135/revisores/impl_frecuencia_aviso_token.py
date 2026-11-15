"""T-135 · Frecuencia del aviso de CHR-TOKEN-001 con el generador A2 de `T-127/revisores/r03_01_cota_aviso_y_origen.py`,
antes (la firma de 6 datos con la regla de la r03) y con la firma y la regla de T-135.
Uso: python -I impl_frecuencia_aviso_token.py bloque_a/11_Ejecutor [semilla]"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np
from bloque_a.motor import frontera_b as fb

rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 11)


def redondo(x, sig):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    nz = x != 0
    e = np.floor(np.log10(np.abs(x[nz])))
    out[nz] = np.round(x[nz] / 10 ** (e - sig + 1)) * 10 ** (e - sig + 1)
    return out


def tok(n, staking, sig=2, p_redondo=0.6, p_fija=0.5):
    filas, ficha = [], []
    for _ in range(n):
        total = float(rng.choice([1e8, 1e9, 1e10, 21e6])) if rng.random() < p_redondo else redondo([np.exp(rng.normal(20, 2))], sig)[0]
        circ = total if rng.random() < 0.4 else redondo([total * rng.uniform(0.3, 0.95)], sig)[0]
        fija = rng.random() < p_fija
        precio = float(redondo([np.exp(rng.normal(0, 2))], 3)[0])
        maxima = total if fija else None
        em = 0.0 if fija else redondo([circ * rng.uniform(0.01, 0.08)], sig)[0]
        st = round(float(rng.uniform(0.01, 0.12)), 3) if staking else None
        co = round(float(rng.uniform(0.1, 0.7)), 2) if staking else None
        filas.append((precio, circ, total, maxima, em, 0.0))
        ficha.append((precio, circ, None if total == circ else total, None if maxima is None or maxima == total else maxima,
                      em, 0.0, st, co))
    return filas, ficha


def tasa(n, staking, veces=2000, **kw):
    viejo = nuevo = 0
    for _ in range(veces):
        f6, f8 = tok(n, staking, **kw)
        d = fb.AVISO_B["datos_distintos_aviso"]
        par = fb._datos_que_coinciden(f6, 0.01) >= 6 - d
        np.fill_diagonal(par, False)
        viejo += bool(par.any())
        nuevo += bool(fb._aviso_casi_clones(f8, 0.01, []))
    return viejo / veces, nuevo / veces


for staking in (False, True):
    for n in (5, 10, 20):
        v, nu = tasa(n, staking)
        print(f"staking/concentración {'sí' if staking else 'no'} · n={n}: antes {v:.1%} · T-135 {nu:.1%}")
for pr in (0.25,):
    for n in (10, 20):
        v, nu = tasa(n, False, p_redondo=pr, p_fija=0.25)
        print(f"prudente (25 % redondas, 25 % fijas), sin staking · n={n}: antes {v:.1%} · T-135 {nu:.1%}")
for n in (10, 20):
    v, nu = tasa(n, False, sig=3)
    print(f"circulante con 3 cifras significativas, sin staking · n={n}: antes {v:.1%} · T-135 {nu:.1%}")
