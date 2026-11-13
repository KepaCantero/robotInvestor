"""QA r01 de T-112 · regresión del ciclo simulado de A: mismas salidas antes y después del commit.

Uso: r01_09_regresion_ciclo.py <ejecutor_antes> <ejecutor_despues> <carpeta_salidas>
Ejecuta en cada ejecutor `bloque-a --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv
--salida <carpeta> backtest --desde 2024-01-05 --hasta 2024-03-29` (el de CLAUDE.md), con el paquete de ese ejecutor, y
compara los ficheros de salida byte a byte; los que difieren se comparan además sin las claves volátiles (fechas de
ejecución, ids de run, tiempos) para separar lo que cambia de verdad.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

antes, despues, salidas = (Path(a).resolve() for a in sys.argv[1:4])
PY = Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python"
ARGS = ["--cliente", "mock", "--datos", "ejemplos/datos_sinteticos", "--universo", "config/universo_ejemplo.csv"]


def correr(eje: Path, destino: Path) -> float:
    """Las dos pasadas escriben en la MISMA carpeta (las rutas de salida aparecen en los informes) y luego se mueve."""
    import shutil
    out = destino.parent / "salida_mock"
    shutil.rmtree(out, ignore_errors=True)
    shutil.rmtree(destino, ignore_errors=True)
    out.mkdir(parents=True)
    codigo = f"import sys; sys.path.insert(0, {str(eje)!r}); sys.argv = ['bloque-a'] + sys.argv[1:]; from bloque_a.cli import main; sys.exit(main())"
    t0 = time.time()
    r = subprocess.run([str(PY), "-I", "-c", codigo, *ARGS, "--salida", str(out), "backtest", "--desde", "2024-01-05", "--hasta", "2024-03-29"],
                       cwd=eje, capture_output=True, text=True)
    (destino.parent / f"{destino.name}.log").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit(f"el ciclo falla en {eje} ({r.returncode})")
    dt = time.time() - t0
    out.rename(destino)
    return dt


VOLATILES = {"generado", "fecha_generacion", "timestamp", "ts", "duracion_s", "run_id", "inicio", "fin_ejecucion", "hora"}


def sin_volatiles(x):
    if isinstance(x, dict):
        return {k: sin_volatiles(v) for k, v in x.items() if k not in VOLATILES}
    if isinstance(x, list):
        return [sin_volatiles(v) for v in x]
    return x


ta = correr(antes, salidas / "antes")
td = correr(despues, salidas / "despues")
print(f"ciclo antes {ta:.0f} s · después {td:.0f} s")
fa = {p.relative_to(salidas / "antes") for p in (salidas / "antes").rglob("*") if p.is_file()}
fd = {p.relative_to(salidas / "despues") for p in (salidas / "despues").rglob("*") if p.is_file()}
print(f"ficheros: antes {len(fa)}, después {len(fd)}; solo antes {sorted(map(str, fa - fd))[:5]}; solo después {sorted(map(str, fd - fa))[:5]}")
distintos = []
for rel in sorted(fa & fd):
    a, b = (salidas / "antes" / rel).read_bytes(), (salidas / "despues" / rel).read_bytes()
    if a != b:
        distintos.append(rel)
print(f"idénticos byte a byte: {len(fa & fd) - len(distintos)} de {len(fa & fd)}")
for rel in distintos[:40]:
    a, b = (salidas / "antes" / rel).read_text(encoding="utf-8", errors="replace"), (salidas / "despues" / rel).read_text(encoding="utf-8", errors="replace")
    nota = ""
    try:
        if rel.suffix == ".json":
            nota = "igual sin volátiles" if sin_volatiles(json.loads(a)) == sin_volatiles(json.loads(b)) else "DISTINTO"
        elif rel.suffix == ".jsonl":
            la = [sin_volatiles(json.loads(x)) for x in a.splitlines() if x.strip()]
            lb = [sin_volatiles(json.loads(x)) for x in b.splitlines() if x.strip()]
            nota = "igual sin volátiles" if la == lb else f"DISTINTO ({len(la)} frente a {len(lb)} líneas)"
        else:
            nota = "DISTINTO (texto)"
    except Exception as e:  # noqa: BLE001
        nota = f"no comparable ({e})"
    print(f"  {rel}: {nota}")
