"""QA r01 de T-166 · el ejecutor carga cada prompt de 02_System_prompts (o de prompts_v6 los agentes V6; nunca del histórico), AG-20 trae RF-0046, y su huella
(`Prompts.version`) cambia frente a la del texto de la V5.2 del histórico.

Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-166/revisores/r01_04_prompts_y_huellas.py
"""
import sys
from pathlib import Path

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ)]
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.prompts import NOMBRES_ALTERNATIVOS, CatalogoPrompts, huella  # noqa: E402

BLOQUE = EJ.parent
c = CatalogoPrompts(cargar_config())
fallos = []
for ag in sorted(NOMBRES_ALTERNATIVOS):
    p = c.archivo(ag)
    if p.parent not in (BLOQUE / "02_System_prompts", EJ / "prompts_v6") or "99_Historico" in str(p) or not p.exists():
        fallos.append((ag, str(p)))
t = c.texto("AG-20")
v_nueva = c.version("AG-20")
hist = BLOQUE / "99_Historico_V5.2" / "02_System_prompts" / c.archivo("AG-20").name
antiguo = hist.read_text(encoding="utf-8")
print("agentes:", len(NOMBRES_ALTERNATIVOS), "fuera de 02:", fallos)
print("AG-20 RF-0046:", '"ref_id":"RF-0046"' in t, "RF-0123:", "RF-0123" in t)
print("AG-20 huella:", v_nueva, "· huella texto 02 vs histórico distinta:",
      huella(c.archivo("AG-20").read_text(encoding="utf-8")) != huella(antiguo))
print("AG-20 versión estable:", c.version("AG-20") == v_nueva)
sys.exit(1 if fallos or "RF-0123" in t else 0)
