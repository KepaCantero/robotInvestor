"""T-202 · QA r01 · mutantes propios del revisor (los del implementador están en ../mutantes.py).

Cambia una cosa cada vez en la copia, ejecuta las pruebas que deberían verlo y la restaura. MUERTO: alguna prueba falla.
- RQ01-RQ05: el código del Motor que toca T-202 (alternativa de los contrastes de rangos, restricción GLM, residuo SVI).
- RQ06-RQ12: la instalación de los stubs (preparar_entorno.sh y tools/requisitos_entorno.txt) frente a la prueba nueva
  `pruebas_preparar_entorno.py::test_t202_el_script_instala_cada_stub_de_tipos_fijado`.
Uso (desde la raíz de la copia): .venv/bin/python .docs/tickets/T-202/revisores/r01_mutantes.py [RQ01 …]
"""
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path.cwd()
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
SER, REA, FD = (EJ / "bloque_a/motor" / f for f in ("fichas_series.py", "fichas_reales.py", "fichas_fon_der.py"))
SCRIPT, REQ = RAIZ / ".docs/scripts/preparar_entorno.sh", RAIZ / "tools/requisitos_entorno.txt"
T_SER = (EJ, ["tests/test_fase2_series.py", "tests/test_t202_alternativas_rangos.py"])
T_REA = (EJ, ["tests/test_fase2_reales.py"])
T_FD = (EJ, ["tests/test_fase1_fon_der.py", "tests/test_t202_svi.py"])   # r02: la prueba nueva de H-01
T_ENT = (RAIZ, [".docs/scripts/pruebas_preparar_entorno.py"])
INSTALA = "  types-PyYAML types-jsonschema scipy-stubs \\\n"

M = [
    ("RQ01 wilcoxon: la alternativa declarada se ignora (siempre bilateral)", SER,
     [("res = stats.wilcoxon(dif, alternative=_SCIPY_ALT[alt])", 'res = stats.wilcoxon(dif, alternative="two-sided")')], T_SER),
    ("RQ02 mann_whitney: la alternativa declarada se ignora (siempre bilateral)", SER,
     [("stats.mannwhitneyu(a, b, alternative=_SCIPY_ALT[alt])", 'stats.mannwhitneyu(a, b, alternative="two-sided")')], T_SER),
    ("RQ03 _SCIPY_ALT: «menor» pasa a bilateral", SER, [('"menor": "less"}', '"menor": "two-sided"}')], T_SER),
    ("RQ04 GLM: la restricción olvida θ_1 (Σθ_{2..k} ≤ 1)", REA,
     [("        return 1 - np.sum(t)\n", "        return 1 - np.sum(t[1:])\n")], T_REA),
    ("RQ05 SVI: residuo ponderado (mínimos cuadrados con pesos 1..2)", FD,
     [("            return _svi(x, k)[0] - w_obs\n",
       "            return (_svi(x, k)[0] - w_obs) * np.linspace(1.0, 2.0, len(w_obs))\n")], T_FD),
    ("RQ06 script: no instala scipy-stubs", SCRIPT, [(INSTALA, "  types-PyYAML types-jsonschema \\\n")], T_ENT),
    ("RQ07 script: los stubs en otra orden de pip, sin -c", SCRIPT,
     [(INSTALA, ""), ('  || fallo "pip no pudo instalar las versiones fijadas"\ncomprobar\n',
                      '  || fallo "pip no pudo instalar las versiones fijadas"\n"$VENV/bin/python" -m pip install -q '
                      'types-PyYAML types-jsonschema scipy-stubs || true\ncomprobar\n')], T_ENT),
    ("RQ08 fichero: se quita types-jsonschema", REQ, [("types-jsonschema==4.26.0.20261006\n", "")], T_ENT),
    ("RQ09 fichero: se fija pandas-stubs sin instalarlo", REQ,
     [("scipy-stubs==1.18.1.1\n", "pandas-stubs==3.0.0.260204\nscipy-stubs==1.18.1.1\n")], T_ENT),
    ("RQ10 fichero: se fija types-openpyxl sin instalarlo", REQ,
     [("types-jsonschema==4.26.0.20261006\n", "types-jsonschema==4.26.0.20261006\ntypes-openpyxl==3.1.5.20250919\n")], T_ENT),
    # RQ11-RQ12: el mismo stub sin instalar, escrito como pip también lo acepta (guion bajo, mayúscula inicial)
    ("RQ11 fichero: se fija types_openpyxl (guion bajo) sin instalarlo", REQ,
     [("types-jsonschema==4.26.0.20261006\n", "types-jsonschema==4.26.0.20261006\ntypes_openpyxl==3.1.5.20250919\n")], T_ENT),
    ("RQ12 fichero: se fija Types-openpyxl (mayúscula) sin instalarlo", REQ,
     [("types-jsonschema==4.26.0.20261006\n", "types-jsonschema==4.26.0.20261006\nTypes-openpyxl==3.1.5.20250919\n")], T_ENT),
]


def main() -> int:
    elegidos = sys.argv[1:]
    vivos = 0
    for nombre, f, cambios, (cwd, pruebas) in M:
        if elegidos and nombre.split()[0] not in elegidos:
            continue
        orig = f.read_text(encoding="utf-8")
        mut = orig
        for a, b in cambios:
            assert mut.count(a) == 1, (nombre, a[:60], mut.count(a))
            mut = mut.replace(a, b)
        f.write_text(mut, encoding="utf-8")
        t0 = time.monotonic()
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas],
                               cwd=cwd, capture_output=True, text=True, check=False)
        finally:
            f.write_text(orig, encoding="utf-8")
        fallo = next((ln.strip() for ln in r.stdout.splitlines() if ln.startswith(("FAILED ", "ERROR "))), "")
        ok = r.returncode == 0
        if r.returncode not in (0, 1):          # error de colección o de entorno: no cuenta como muerto
            print(f"{nombre}: ERROR DE EJECUCIÓN (código {r.returncode})\n{r.stdout[-600:]}{r.stderr[-600:]}", flush=True)
            vivos += 1
            continue
        vivos += ok
        print(f"{nombre}: {'VIVO' if ok else 'MUERTO'} ({time.monotonic() - t0:.0f} s) {fallo[:170]}", flush=True)
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
