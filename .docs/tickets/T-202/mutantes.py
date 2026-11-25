"""Mutantes de T-202 sobre los cuatro cambios no mecánicos del Bloque A (los que pide mypy con scipy-stubs).

T-202 es un ticket de cuotas: el comportamiento no cambia, y la prueba principal es la de equivalencia
(`equivalencia.py`, salidas de develop y de la rama byte a byte). Estos mutantes comprueban además que cada línea tocada
la ejercitan las pruebas de la suite: si el código nuevo se rompiera, alguna prueba lo vería. Cada mutante cambia una
línea en la copia, ejecuta las pruebas de su ficha y la restaura. MUERTO: alguna prueba falla (se muestra la línea).

Con `--solo-suite-anterior`, M01, M02 y M09 se ejecutan sin las pruebas nuevas de T-202 (para ver que M01 y M09, el RQ05 de
la QA r01, quedaban vivos con la suite de antes).

r02 (QA r01): M09 es H-01 (residuo SVI con pesos), M10 y M11 son H-02 (un stub fijado con otra grafía y sin instalar) y
M12 es H-03 (el gate deja de comprobar el entorno antes de mypy). Las rutas que empiezan por «@» son de la raíz del
repositorio, y sus pruebas se ejecutan desde allí.

Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-202/mutantes.py . [--solo-suite-anterior] [M01 …]
"""
import subprocess
import sys
import time
from pathlib import Path

EJ = Path(sys.argv[1])
RAIZ = (EJ / ".." / "..").resolve()
SER, REA, FD = "bloque_a/motor/fichas_series.py", "bloque_a/motor/fichas_reales.py", "bloque_a/motor/fichas_fon_der.py"
T_SER, T_REA, T_FD = "tests/test_fase2_series.py", "tests/test_fase2_reales.py", "tests/test_fase1_fon_der.py"
T_202 = "tests/test_t202_alternativas_rangos.py"   # nueva: M01 quedaba vivo con la suite de antes (ver pruebas.md)
T_202_SVI = "tests/test_t202_svi.py"               # nueva en la r02 (H-01): M09 quedaba vivo con la suite de antes
NUEVAS = (T_202, T_202_SVI)
REQ, T_ENT = "@tools/requisitos_entorno.txt", "@.docs/scripts/pruebas_preparar_entorno.py"
GATE, T_GATE = "@tools/check_all.sh", "@.docs/scripts/pruebas_gate_entorno.py"
JS = "types-jsonschema==4.26.0.20261006\n"
ALT = ('_SCIPY_ALT: dict[str, Literal["two-sided", "greater", "less"]] = {"bilateral": "two-sided", "mayor": "greater",\n'
       '                                                                 "menor": "less"}\n')

# (nombre, fichero, [(antes, después)], pruebas)
M = [
    # 1. _SCIPY_ALT con su tipo Literal (ST-INF-001, wilcoxon y mann_whitney)
    ("M01 _SCIPY_ALT: «mayor» y «menor» cambiados", SER,
     [(ALT, ALT.replace('"mayor": "greater"', '"mayor": "less"').replace('"menor": "less"', '"menor": "greater"'))], (T_SER, T_202)),
    ("M02 _SCIPY_ALT: «bilateral» pasa a «greater»", SER,
     [(ALT, ALT.replace('"bilateral": "two-sided"', '"bilateral": "greater"'))], (T_SER, T_202)),
    # 2. res_u (mann_whitney): el nombre nuevo del resultado
    ("M03 mann_whitney: el estadístico sale del p-valor", SER,
     [("        u1 = float(res_u.statistic)\n", "        u1 = float(res_u.pvalue)\n")], T_SER),
    ("M04 mann_whitney: el p-valor sale del estadístico", SER,
     [('"p_valor": float(res_u.pvalue), "ic": None,', '"p_valor": float(res_u.statistic), "ic": None,')], T_SER),
    # 3. holgura (ALT-DESMOOTH-001 GLM): la restricción Σθ_{1..k} ≤ 1, antes una lambda
    ("M05 GLM: la restricción cambia de signo", REA,
     [("        return 1 - np.sum(t)\n", "        return np.sum(t) - 1\n")], T_REA),
    ("M06 GLM: la restricción se relaja a Σθ ≤ 2", REA,
     [("        return 1 - np.sum(t)\n", "        return 2 - np.sum(t)\n")], T_REA),
    # 4. residuo (DER-SKEW-001 SVI): el residuo del ajuste por mínimos cuadrados, antes una lambda
    ("M07 SVI: el residuo suma en vez de restar", FD,
     [("            return _svi(x, k)[0] - w_obs\n", "            return _svi(x, k)[0] + w_obs\n")], T_FD),
    ("M08 SVI: el residuo usa la primera derivada", FD,
     [("            return _svi(x, k)[0] - w_obs\n", "            return _svi(x, k)[1] - w_obs\n")], T_FD),
    # r02 (QA r01, H-01): el RQ05 de la QA
    ("M09 SVI: residuo ponderado (mínimos cuadrados con pesos 1..2)", FD,
     [("            return _svi(x, k)[0] - w_obs\n",
       "            return (_svi(x, k)[0] - w_obs) * np.linspace(1.0, 2.0, len(w_obs))\n")], (T_FD, T_202_SVI)),
    # r02 (QA r01, H-02): el RQ11 y el RQ12 de la QA
    ("M10 fichero: se fija types_openpyxl (guion bajo) sin instalarlo", REQ,
     [(JS, JS + "types_openpyxl==3.1.5.20250919\n")], T_ENT),
    ("M11 fichero: se fija Types-openpyxl (mayúscula) sin instalarlo", REQ,
     [(JS, JS + "Types-openpyxl==3.1.5.20250919\n")], T_ENT),
    # r02 (QA r01, H-03): el gate ya no comprueba el entorno antes de mypy
    ("M12 gate: sin la comprobación del entorno antes de mypy", GATE,
     [('    salida_entorno="$(.docs/scripts/preparar_entorno.sh --comprobar 2>&1)" || entorno_mypy=',
       '    salida_entorno="$(true)" || entorno_mypy=')], T_GATE),
]


def pytest(nodo: str | tuple[str, ...]) -> tuple[bool, str, float]:
    t0 = time.monotonic()
    nodos = [nodo] if isinstance(nodo, str) else list(nodo)
    desde_raiz = all(n.startswith("@") for n in nodos)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *[n.lstrip("@") for n in nodos]],
                       cwd=RAIZ if desde_raiz else EJ, capture_output=True, text=True, check=False)
    fallo = next((ln.strip() for ln in r.stdout.splitlines() if ln.startswith("FAILED ")), "")
    return r.returncode == 0, fallo[:160], time.monotonic() - t0


def main() -> int:
    elegidos = [a for a in sys.argv[2:] if not a.startswith("--")]
    vivos = 0
    for nombre, f, cambios, nodo in M:
        if elegidos and nombre.split()[0] not in elegidos:
            continue
        if "--solo-suite-anterior" in sys.argv and isinstance(nodo, tuple):
            nodo = tuple(n for n in nodo if n not in NUEVAS)
        p = RAIZ / f[1:] if f.startswith("@") else EJ / f
        orig = p.read_text(encoding="utf-8")
        mut = orig
        for a, b in cambios:
            assert mut.count(a) == 1, (nombre, a[:60], mut.count(a))
            mut = mut.replace(a, b)
        p.write_text(mut, encoding="utf-8")
        try:
            ok, fallo, seg = pytest(nodo)
        finally:
            p.write_text(orig, encoding="utf-8")
        vivos += ok
        print(f"{nombre}: {'VIVO' if ok else 'MUERTO'} ({seg:.0f} s) {fallo}", flush=True)
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
