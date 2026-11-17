"""QA r01 de T-164 · H-10 (fichas con otro número de cifras) en una copia del corpus real.

Cada línea sembrada cita un ID; se comprueba el nivel y el mensaje de su hallazgo. Sale 1 si algún caso falla.

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-164/revisores/r01_03_cifras.py
"""
import shutil
import sys
import tempfile
from pathlib import Path

EJ = Path.cwd()
sys.path.insert(0, str(EJ))
RAIZ = EJ.parent
from bloque_a.herramientas import verificador_ids as vi

P_RV = "02_System_prompts/System prompt - Analista de Renta Variable - Versión óptima V5.0.md"
# (ID, línea sembrada, nivel esperado o None si no debe haber hallazgo, texto que debe llevar el mensaje)
CASOS = [
    ("FX-TREND-01", "Usa la FX-TREND-01.", "ERROR", "(¿FX-TREND-001?)"),
    ("FX-TREND-0001", "Usa la `FX-TREND-0001`.", "ERROR", "(¿FX-TREND-001?)"),
    ("FX-TREND-1", "Usa la **FX-TREND-1**.", "ERROR", "otro número de cifras"),
    ("FX-TREND-00001", "Usa la FX‑TREND‑00001.", "ERROR", "otro número de cifras"),
    ("ST-DESC-12345678", "Usa la ST-DESC-12345678.", "ERROR", "otro número de cifras"),
    ("IDX-FICT-01", "El índice IDX-FICT-01 sube.", "ERROR", "otro número de cifras"),   # no es el símbolo declarado
    ("FX-TREND-001", "Usa la FX-TREND-001 y la FX-TREND-001b.", None, ""),             # existe; con sufijo no es cita
    ("FX-TREND-001b", "", None, ""),
]

with tempfile.TemporaryDirectory() as tmp:
    r = Path(tmp) / "bloque_a"
    shutil.copytree(RAIZ, r, ignore=lambda d, n: [x for x in n if x == "11_Ejecutor" or x.startswith("99_Historico")])
    p = r / P_RV
    p.write_text(p.read_text(encoding="utf-8") + "\n" + "\n\n".join(c[1] for c in CASOS if c[1]) + "\n", encoding="utf-8")
    inf = vi.verificar(r)
    malos = []
    for ident, _, nivel, texto in CASOS:
        hs = [h for h in inf["hallazgos"] if h["id"] == ident and h["clase"] == "d"]
        if nivel is None:
            ok = not [h for h in hs if h["nivel"] == "ERROR"]
        else:
            ok = any(h["nivel"] == nivel and texto in h["mensaje"] for h in hs)
        malos += [] if ok else [ident]
        print(f"[{'OK ' if ok else 'MAL'}] {ident}: esperado {nivel or 'sin ERROR'} {texto}, obtenido "
              f"{[(h['nivel'], h['mensaje'][-60:]) for h in hs] or 'nada'}")
    otros = {h["id"] for h in inf["hallazgos"] if h["nivel"] == "ERROR"} - {c[0] for c in CASOS}
    ok = otros == {"FX-MC10-003", "RF-0123"}
    malos += [] if ok else ["otros errores"]
    print(f"[{'OK ' if ok else 'MAL'}] sin otros errores que los 2 reales: {sorted(otros)}")
print(f"\nFallan: {malos or 'ninguno'}")
sys.exit(1 if malos else 0)
