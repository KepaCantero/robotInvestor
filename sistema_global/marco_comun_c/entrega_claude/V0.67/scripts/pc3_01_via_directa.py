"""Pasada de coherencia contra la Constitución V0.6 (V0.67), PC3-01: vía de entrada DIRECTA (D-28, Fase 1).

Imprime FALLA mientras el Orquestador rechace un expediente con via_entrada="DIRECTA". Uso, desde marcoC:
    python3 -I entrega_claude/V0.67/scripts/pc3_01_via_directa.py
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

o = nuevo()
r = o.detectar("EXP-PC3-01", "COR-PC3-01", "DIRECTA", "TACTICA", "BROKER", AHORA)
if r.get("ok"):
    print("CUMPLE: el Orquestador admite la vía DIRECTA (D-28)")
else:
    print(f"FALLA: detectar() rechaza la vía DIRECTA ({r.get('codigo')}: {r.get('motivo')}); D-28 la ratificó para la Fase 1")
    sys.exit(1)
