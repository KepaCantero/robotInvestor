"""QA r01 de T-205 (revisor): testigo de sensibilidad. Aplica los mutantes vivos Q1 y Q2 de r01_mutantes.py y comprueba que los
ataques A4 (VIGENTE con clase mala) y A6 (HA rota en el alta) de r01_02_ataques.py los detectan: son las pruebas de regresión
que se piden para H-01 y H-02. Reescribe `seguimiento.py`: ejecútese en una copia que no use nadie más.
Uso (desde bloque_a/11_Ejecutor de esa copia): ../../.venv/bin/python <ruta>/r01_04_testigo.py . <carpeta_temporal>"""
import importlib.util
import subprocess
import sys
from pathlib import Path

EJ, TMP = Path(sys.argv[1]), Path(sys.argv[2])
AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r01m", AQUI / "r01_mutantes.py")
src = (AQUI / "r01_mutantes.py").read_text(encoding="utf-8")
# reutiliza la lista M y aplicar() sin ejecutar el bucle
cab = src.split("\nvivos = []")[0].replace("EJ = Path(sys.argv[1])", f"EJ = Path({str(EJ.resolve())!r})")
ns: dict = {}
exec(compile(cab, "r01_mutantes", "exec"), ns)
ruta = EJ / "bloque_a/seguimiento.py"
original = ruta.read_text(encoding="utf-8")
esperado = {"Q1": "A4 VIGENTE con clase mala", "Q2": "A6 alta con HA rota"}
mal = 0
try:
    for nombre, viejo, nuevo in ns["M"]:
        q = nombre.split()[0]
        if q not in esperado:
            continue
        ruta.write_text(ns["aplicar"](nombre, viejo, nuevo), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(AQUI / "r01_02_ataques.py"), str(TMP / q)], cwd=EJ, capture_output=True, text=True)
        detecta = any(l.startswith("FALLA ") and esperado[q] in l for l in r.stdout.splitlines())
        print(f"{q}: {'detectado' if detecta else 'NO DETECTADO'} por «{esperado[q]}»")
        mal += not detecta
finally:
    ruta.write_text(original, encoding="utf-8")
sys.exit(1 if mal else 0)
