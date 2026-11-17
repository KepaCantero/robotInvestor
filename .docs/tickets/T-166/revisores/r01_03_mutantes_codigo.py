"""QA r01 de T-166 · mutantes de código propios en respuesta_final.py: ¿los nota test_t166 (CA-5) y, si no, T-162/T-169?

Uso (desde bloque_a/11_Ejecutor, en una copia de trabajo: escribe y restaura el archivo):
  ../../.venv/bin/python ../../.docs/tickets/T-166/revisores/r01_03_mutantes_codigo.py [--resto]
"""
import subprocess
import sys
from pathlib import Path

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
RF = EJ / "bloque_a" / "respuesta_final.py"
MUT = [
    ("M1 sin entrega no cuenta como entregada", 'run.get("entrega", "ENTREGADA") != "ENTREGADA"', 'run.get("entrega") != "ENTREGADA"'),
    ("M2 la más alta", "return min(valores, key=CONFIANZAS.index)", "return max(valores, key=CONFIANZAS.index)"),
    ("M3 cualquier RUN- cuenta", "run = entrada_run if lanzado else None", "run = entrada_run if es_run else None"),
    ("M4 sin tope especulativo", '_menos_confiada([qry.get("confianza", "especulativo"), "especulativo"])',
     '_menos_confiada([qry.get("confianza", "especulativo")])'),
    ("M5 otro estado F5", '"PARCIAL": "RESPONDIDA_FINAL"', '"PARCIAL": "RESPONDIDA_PARCIAL"'),
    ("M6 NO_EJECUTADO antes que FALLIDO", 'if escalado.get("estado_run") == "FALLIDO":\n        return "FALLIDO"\n    if not escalado.get("run_id"):\n        return "NO_EJECUTADO"',
     'if not escalado.get("run_id"):\n        return "NO_EJECUTADO"\n    if escalado.get("estado_run") == "FALLIDO":\n        return "FALLIDO"'),
]


def corre(archivos, k=None):
    cmd = [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *archivos] + (["-k", k] if k else [])
    return subprocess.run(cmd, cwd=EJ, capture_output=True, text=True).returncode != 0


def main() -> int:
    original = RF.read_text(encoding="utf-8")
    resto = "--resto" in sys.argv
    try:
        for nombre, viejo, nuevo in MUT:
            assert original.count(viejo) >= 1, nombre
            RF.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            t166 = corre(["tests/test_t166_entrega_corpus.py"], "ca5 or ca6")
            otros = corre(["tests/test_t162_respuesta_final.py", "tests/test_t169_hallazgos_t162.py", "tests/test_t169_r02.py"]) if resto and not t166 else None
            print(f"{nombre}: t166 {'muerto' if t166 else 'VIVE'}" + ("" if otros is None else f" · T-162/T-169 {'muerto' if otros else 'VIVE'}"))
    finally:
        RF.write_text(original, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
