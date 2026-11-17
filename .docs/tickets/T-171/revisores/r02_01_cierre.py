"""QA de la ronda de cierre de T-171 · Lo que puede abrir el cambio de `_otra_accion` (la forma sin clítico y `_RESPONDE`):
segundas acciones con «responder»/«contestar» y con clíticos de verbos de mostrar o de reforzar. Inventario, no falla.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python ../../.docs/tickets/T-171/revisores/r02_01_cierre.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from bloque_a import guias as G  # noqa: E402

BASE = {"tipo": 2, "origen": ["LEC-2026-0901"], "que_cambia": "Cita el régimen macro",
        "donde_se_comprueba": "campo lectura_conjunto del retorno de CT-05",
        "como_se_sabe": "revisión del Auditor sin hallazgos de orden durante 4 ciclos", "caducidad": "2027-02-15"}
ATAQUES = [
    "Indica la segunda pasada y contesta que está hecha",
    "Presenta las objeciones y respóndelas con un «ya visto»",
    "Presenta las objeciones y contéstalas todas igual",
    "Muestra la autocrítica y resúmela",
    "Indica la refutación y archívala",
    "Cita el umbral de rentabilidad y preséntalo rebajado",
    "Indica la segunda pasada y dala por hecha",
]


def main() -> int:
    pasan = 0
    for t in ATAQUES:
        c = G.conflicto_para({**BASE, "que_cambia": t}, "AG-03")
        pasan += c is None
        print(f"{'PASA' if c is None else 'DETECTADO':9} | {t} {'' if c is None else c['familias']}")
    print(f"\n{pasan} de {len(ATAQUES)} pasan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
