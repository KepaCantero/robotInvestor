"""QA r02 de T-106 · Vuelve a ejecutar los scripts de la r01 contra una raíz (por defecto, la del repositorio).

Los scripts r01 no se tocan. Dos de ellos dependen de cosas que la r02 cambió a propósito, y aquí se adaptan en memoria
(el texto del script r01 se lee, se sustituye lo indicado y se ejecuta con su `__file__` original):
  - r01_03: `madurez_catalogo` ya no es un `lru_cache` (la caché pasó a `_madurez`, por ruta y fecha de modificación,
    H-06), y los casos de control pasaron de 50 a 66 (H-08, H-13): se usa `_madurez.cache_clear()` y se espera 66.
  - r01_02: el bloque MON-EXP-001 se salta, porque el método se rehízo (H-01) y rechaza a propósito el sistema justo
    (5 nodos para 5 tramos) que usaba ese bloque; el oráculo nuevo de MON-EXP está en `r02_02_oraculos.py`.
El resto (r01_01, r01_05, r01_06) se ejecuta tal cual. r01_04 (mutantes, ≈ 25 min) se lanza con `--mutantes`.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_00_reejecutar_r01.py [RAIZ] [--mutantes]
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
RAIZ = str(Path(args[0]).resolve()) if args else str(AQUI.parents[3])
PY = sys.executable

PARCHES = {
    "r01_03_integracion.py": [("S.madurez_catalogo.cache_clear()", "S._madurez.cache_clear()"),
                              ("53 casos superados", "66 casos superados (r02)"),
                              ("sum(len(r[\"casos\"]) for r in res.values()) == 53", "sum(len(r[\"casos\"]) for r in res.values()) == 66")],
}


def sin_bloque_mon_exp(src: str) -> str:
    i = src.index("# ------------------------------------------------------------------ MON-EXP-001")
    j = src.index("# ------------------------------------------------------------------ IDX-ERP-001")
    return src[:i] + "print('      (r02) bloque MON-EXP-001 de la r01 saltado: ver r02_02_oraculos.py')\n" + src[j:]


def correr(nombre: str, extra: list[str] | None = None) -> int:
    ruta = AQUI / nombre
    src = ruta.read_text(encoding="utf-8")
    for viejo, nuevo in PARCHES.get(nombre, []):
        assert viejo in src, (nombre, viejo)
        src = src.replace(viejo, nuevo)
    if nombre == "r01_02_valores_independientes.py":
        src = sin_bloque_mon_exp(src)
    lanzador = ("import sys\n"
                f"sys.argv = [{str(ruta)!r}, {RAIZ!r}] + {extra or []!r}\n"
                f"g = {{'__file__': {str(ruta)!r}, '__name__': '__main__'}}\n"
                f"exec(compile({src!r}, {str(ruta)!r}, 'exec'), g)\n")
    print(f"\n===== {nombre} {' '.join(extra or [])}", flush=True)
    r = subprocess.run([PY, "-I", "-B", "-c", lanzador], cwd=os.environ.get("TMPDIR") or "/", timeout=3600)
    print(f"===== {nombre}: código de salida {r.returncode}", flush=True)
    return r.returncode


codigos = {n: correr(n) for n in ("r01_01_ataques_datos.py", "r01_02_valores_independientes.py", "r01_03_integracion.py",
                                   "r01_05_promocion.py", "r01_06_ataques_dirigidos.py")}
if "--mutantes" in sys.argv:
    codigos["r01_04_mutantes.py"] = correr("r01_04_mutantes.py")
print("\nResumen:", codigos)
sys.exit(1 if any(codigos.values()) else 0)
