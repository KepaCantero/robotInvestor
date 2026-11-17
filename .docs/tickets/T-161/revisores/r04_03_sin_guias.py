"""QA r04 de T-161 · Un ciclo sin guías da los mismos entregables y el mismo estado que una base dada (por defecto
`origin/develop`, con la r03). Reutiliza `ciclo` y `volcado` de T-158 `r01_03`. Sale 1 si algo difiere.

Uso, desde la raíz de la copia: .venv/bin/python .docs/tickets/T-161/revisores/r04_03_sin_guias.py <carpeta_desechable> [base]
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

RAIZ = Path.cwd()
_spec = importlib.util.spec_from_file_location("r158", RAIZ / ".docs/tickets/T-158/revisores/r01_03_regresion_sin_guias.py")
R158 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R158)


def main() -> int:
    tmp = Path(sys.argv[1]).resolve()
    base = sys.argv[2] if len(sys.argv) > 2 else "origin/develop"
    prev = tmp / "prev"
    prev.mkdir(parents=True, exist_ok=True)
    arch = subprocess.run(["git", "archive", base, "bloque_a/11_Ejecutor"], cwd=RAIZ, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(prev)], input=arch, check=True)
    for hermana in (RAIZ / "bloque_a").iterdir():
        destino = prev / "bloque_a" / hermana.name
        if hermana.name != "11_Ejecutor" and not destino.exists():
            destino.symlink_to(hermana)
    R158.ciclo(prev / "bloque_a" / "11_Ejecutor", tmp / "t_prev", "ciclo")
    R158.ciclo(RAIZ / "bloque_a" / "11_Ejecutor", tmp / "t_act", "ciclo")
    a, b = R158.volcado(tmp / "t_prev"), R158.volcado(tmp / "t_act")
    difieren = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    print(f"[sin guías] base {base}: ficheros comparados: {len(set(a) | set(b))}; difieren: {difieren or 'ninguno'}")
    return 1 if difieren else 0


if __name__ == "__main__":
    sys.exit(main())
