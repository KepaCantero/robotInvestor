"""T-152 · ejecuta los scripts de mutantes de T-150 con la línea nueva del umbral (decisión del operador, 16-11-2026).

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-152/mutantes_heredados.py <copia desechable con «t147_mut»> <carpeta temporal>
`frontera_b.py` ya no tiene «desplaza = 2 * rel <= tol» (q/p ≤ 1 %), sino «desplaza = rel <= tol» (q/p ≤ 2 %), así que:
- `T-150/mutantes.py`: su F3 («se desplazan también los pasos grandes») se reescribe sobre la línea nueva;
- `T-150/revisores/r01_04_mutantes_qa.py`: su X01 (el umbral al doble) es ahora el código y se quita.
Escribe las dos copias adaptadas en la carpeta temporal (no toca los originales) y las ejecuta contra la copia. Termina con el
peor código de salida de las dos (el revisor da 1 por X02, el casi equivalente de su O-03)."""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
COPIA, TMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
assert "t147_mut" in str(COPIA)
TMP.mkdir(parents=True, exist_ok=True)
VIEJA, NUEVA = '"    desplaza = 2 * rel <= tol\\n"', '"    desplaza = rel <= tol\\n"'

t150 = (RAIZ / ".docs/tickets/T-150/mutantes.py").read_text(encoding="utf-8")
assert t150.count(f'{VIEJA}, "    desplaza = rel >= 0\\n"') == 1
(TMP / "t150_mutantes.py").write_text(t150.replace(f'{VIEJA}, "    desplaza = rel >= 0\\n"', f'{NUEVA}, "    desplaza = rel >= 0\\n"'),
                                      encoding="utf-8")
rev = (RAIZ / ".docs/tickets/T-150/revisores/r01_04_mutantes_qa.py").read_text(encoding="utf-8")
a, b = rev.index('    ("FB", "X01'), rev.index('    ("FB", "X02')
(TMP / "r01_04_sin_x01.py").write_text(rev[:a] + rev[b:], encoding="utf-8")
peor = 0
for script in ("t150_mutantes.py", "r01_04_sin_x01.py"):
    print(f"== {script}", flush=True)
    peor = max(peor, subprocess.run([sys.executable, str(TMP / script), str(COPIA)], check=False).returncode)
sys.exit(peor)
