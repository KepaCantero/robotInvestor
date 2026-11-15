"""r03_05 · Un registro por agente con RI_AGENTE (H-17, decisión [PROPUESTO] (3)): valores raros de la variable, lo que usa el
banco por defecto y si los agentes saben que tienen que ponerla.
Uso: .venv/bin/python -B r03_05_agente.py <raíz>"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r03_comun import RAIZ, caso, fin  # noqa: E402

SCR = str(RAIZ / ".docs" / "scripts")


def defecto(valor, modulo="registro_experimentos", expr="REGISTRO_DEFECTO.name"):
    env = {"PATH": "/usr/bin:/bin"}
    if valor is not None:
        env["RI_AGENTE"] = valor
    cod = f"import sys; sys.path.insert(0, {SCR!r}); import {modulo} as m; print(m.{expr})"
    p = subprocess.run([sys.executable, "-I", "-c", cod], capture_output=True, text=True, env=env)
    return (p.stdout.strip() or p.stderr.strip().splitlines()[-1]) if p.returncode == 0 else f"error: {p.stderr.strip()[-120:]}"


caso("RI_AGENTE=astra → registro_astra.jsonl", defecto("astra") == "registro_astra.jsonl", defecto("astra"))
caso("(referencia) sin RI_AGENTE → registro_claude.jsonl", defecto(None) == "registro_claude.jsonl", defecto(None))
for valor in ("Astra", "astra ", " astra", "", "ástra", "astra\n", "a/b", "..", "x" * 33, "astra;rm"):
    v = defecto(valor)
    caso(f"RI_AGENTE={valor!r} (no válido): falla cerrado en vez de escribir en el registro de Claude",
         v.startswith("error"), v)
b = defecto("Astra", "banco_medida", "_registro_defecto().name")
caso("…y el banco con RI_AGENTE='Astra' tampoco anota en el registro de Claude", not b.endswith("registro_claude.jsonl"), b)

# ¿Lo saben los agentes? (Astra entra por AGENTS.md; el índice de scripts de .docs/README.md describe el registro)
for doc in ("AGENTS.md", ".docs/README.md", "CLAUDE.md", ".docs/scripts/common.sh"):
    p = RAIZ / doc
    txt = p.read_text(encoding="utf-8") if p.exists() else ""
    caso(f"{doc} dice que cada agente usa su registro (RI_AGENTE)", "RI_AGENTE" in txt, "lo menciona" if "RI_AGENTE" in txt else "no lo menciona")
fila = next((x for x in (RAIZ / ".docs" / "README.md").read_text(encoding="utf-8").splitlines() if "registro_experimentos.py" in x), "")
caso("la fila del índice de scripts ya no da «.docs/experimentos/registro.jsonl» como ruta por defecto",
     "registro.jsonl»" not in fila, fila[:200])
fin()
