"""r01 (QA T-79): determinismo de las baterías nuevas del kit 2 y de las que cambian en la V0.67. Ejecuta cada una dos veces
con python -I y compara la salida línea a línea, sin las cifras de segundos (lo único que puede variar).

Uso: python3 -I r01_determinismo.py <carpeta marco_comun_c>
"""
import re
import subprocess
import sys
from pathlib import Path

M = Path(sys.argv[1]).resolve()
BATERIAS = ("pruebas_robustez_validadores.py", "pruebas_robustez_t03.py", "pruebas_semana.py", "pruebas_doradas.py",
            "pruebas_consola_sistema.py", "pruebas_catalogo_codigos.py", "pruebas_integracion_v053.py", "pruebas_comparador_t17.py")
SEG = re.compile(r"\d+([.,]\d+)?\s*s\b")
malas = []
for b in BATERIAS:
    salidas = []
    for _ in range(2):
        r = subprocess.run([sys.executable, "-I", b], cwd=M / "pruebas", capture_output=True, text=True, timeout=300)
        salidas.append([SEG.sub("<s>", l) for l in (r.stdout + r.stderr).splitlines()])
    igual = salidas[0] == salidas[1]
    print(f"{'OK      ' if igual else 'DISTINTA'} {b}: {len(salidas[0])} líneas")
    if not igual:
        malas.append(b)
print(f"RESULTADO r01 DETERMINISMO: {'TODAS IGUALES' if not malas else 'HAY DIFERENCIAS ' + str(malas)}")
