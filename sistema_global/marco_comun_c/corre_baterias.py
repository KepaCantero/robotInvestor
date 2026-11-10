"""Corre todas las baterías de pruebas/pruebas_*.py y escribe la salida en el fichero dado.

Uso (desde la raíz de marcoC):  python3 corre_baterias.py <salida.txt> [carpeta_marcoC] [titulo]

Se incluye en la entrega (revisión de V0.62, hallazgo 4): `salida_pruebas.txt` lo citaba y no viajaba.
"""
import subprocess
import sys
import time
from pathlib import Path

salida = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/lote.txt")
raiz = Path(sys.argv[2] if len(sys.argv) > 2 else Path(__file__).resolve().parent).resolve()
baterias = sorted((raiz / "pruebas").glob("pruebas_*.py"))
version = sys.argv[3] if len(sys.argv) > 3 else "lote"
py = sys.executable
lineas = [f"# Salida de las baterías — {version}",
          f"# {len(baterias)} baterías; python {sys.version.split()[0]}",
          "# Lote ejecutado con corre_baterias.py, cada línea: fichero: última línea de su salida [segundos]",
          ""]
fallos = 0
for b in baterias:
    t0 = time.time()
    r = subprocess.run([py, str(b)], capture_output=True, text=True, cwd=str(raiz))
    dt = time.time() - t0
    ult = [l for l in r.stdout.splitlines() if l.strip()]
    ultima = ult[-1] if ult else "(sin salida)"
    if r.returncode != 0 or "FALLA" in r.stdout or r.stderr.strip():
        fallos += 1
        print(f"!!! {b.name}: exit={r.returncode}  {ultima}")
        if r.stderr.strip():
            print(r.stderr[-1500:])
        if "FALLA" in r.stdout:
            malas = [l for l in r.stdout.splitlines() if "FALLA" in l]
            print("\n".join(malas[:12]))
    print(f"{b.name}: {ultima}  [{dt:.1f}s]")
    lineas.append(f"{b.name}: {ultima}  [{dt:.1f}s]")
lineas.append("FIN DEL LOTE")
salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
print(f"\nTOTAL: {len(baterias)} baterías, {fallos} con fallos -> {salida}")
sys.exit(1 if fallos else 0)
