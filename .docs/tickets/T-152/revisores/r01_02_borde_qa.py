"""T-152 · QA r01 · la resolución de la prueba del borde (`test_t152_h02_el_umbral_del_desplazamiento_esta_en_q_p_del_2_por_ciento`).

Uso:  .venv/bin/python -I .docs/tickets/T-152/revisores/r01_02_borde_qa.py [--raiz <copia>]

Carga `tests/test_t150.py` de la copia (sus generadores y sus casos, tal cual) y cambia el `fb` que usa `_juntas` por el
módulo con otro umbral: q/p ≤ 2 %·f para varios f, con `<` en vez de `<=` y sin umbral. Para cada umbral dice qué casos
de la prueba fallan (12 semillas cada uno) y, al final, el umbral más bajo y el más alto que la prueba deja pasar.
Además, lo mismo con 100 semillas en vez de 12 (¿es estable la prueba?). Solo informa: termina con 0."""
import argparse
import importlib.util
import sys
import types
from pathlib import Path

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--raiz", default=str(Path(__file__).resolve().parents[4]))
RAIZ = Path(ap.parse_args().raiz).resolve()
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ))
sys.path.insert(0, str(EJ / "tests"))
spec = importlib.util.spec_from_file_location("t150_qa", EJ / "tests" / "test_t150.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
fb = t.fb
LINEA = "    desplaza = rel <= tol\n"
CASOS = [m.args for m in t.test_t152_h02_el_umbral_del_desplazamiento_esta_en_q_p_del_2_por_ciento.pytestmark
         if m.name == "parametrize"][0][1]


def modulo(expr):
    fuente = Path(fb.__file__).read_text(encoding="utf-8")
    assert fuente.count(LINEA) == 1
    m = types.ModuleType("bloque_a.motor.frontera_b_borde")
    m.__package__, m.__file__ = "bloque_a.motor", fb.__file__
    exec(compile(fuente.replace(LINEA, f"    desplaza = {expr}\n"), m.__name__, "exec"), m.__dict__)  # noqa: S102
    return m


def fallan(m, semillas):
    t.fb = m
    out = []
    for paso, lo, hi, agrupa in CASOS:
        juntas = [t._juntas(x, t._trunc(x, paso)) for x in (t._en_tramo(lo, hi, s) for s in semillas)]
        malas = sum(j != agrupa for j in juntas)
        if malas:
            out.append(f"{paso:g} [{lo:g}, {hi:g}]: {malas}")
    t.fb = fb
    return out


def main():
    print(f"casos: {CASOS}")
    base = fallan(fb, range(12))
    print(f"el código (rel <= tol): {base or 'pasa'}")
    assert not base
    filas = [(f"q/p ≤ 2 %·{f:g}", f"2 * rel <= {0.02 * f!r}") for f in
             (0.5, 0.9, 0.95, 0.96, 0.97, 0.975, 0.98, 0.985, 0.99, 0.995, 0.999, 1.001, 1.005, 1.01, 1.02, 1.03, 1.05,
              1.1, 1.25, 1.5, 2, 5, 10, 50)]
    filas += [("rel < tol (estricto)", "rel < tol"), ("sin umbral", "rel >= 0")]
    pasan = []
    for nombre, expr in filas:
        r = fallan(modulo(expr), range(12))
        pasan.append((nombre, not r))
        print(f"{nombre:24} {'PASA (vive)' if not r else 'falla (muere): ' + '; '.join(r)}", flush=True)
    print("\ncon 100 semillas (0 a 99) en vez de 12:")
    for nombre, expr in [("el código", None), ("q/p ≤ 2 %·0,99", "2 * rel <= 0.0198"), ("q/p ≤ 2 %·1,01", "2 * rel <= 0.0202"),
                         ("q/p ≤ 2 %·2", "2 * rel <= 0.04")]:
        r = fallan(fb if expr is None else modulo(expr), range(100))
        print(f"{nombre:24} {r or 'ningún caso falla'}", flush=True)
    # O-01: el mínimo de cada semilla del primer caso es 2,55 y ⌊2,55/0,05⌋ = 50 en coma flotante (q/p = 2,00 % exacto);
    # sin ese precio (lo = 2,5501), ¿qué umbral más bajo se ve?
    print(f"\n⌊2,55/0,05⌋·0,05 = {t._trunc(np.array([2.55]), 0.05)[0]!r}; sin ese precio (lo = 2,5501, 12 semillas):")
    for f in (0.95, 0.97, 0.98, 0.99, 0.995):
        t.fb = modulo(f"2 * rel <= {0.02 * f!r}")
        n = sum(t._juntas(x, t._trunc(x, 0.05)) for x in (t._en_tramo(2.5501, 2.75, s) for s in range(12)))
        t.fb = fb
        print(f"  q/p ≤ 2 %·{f:g}: {n} de 12 agrupadas ({'la prueba lo vería' if n < 12 else 'no lo vería'})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
