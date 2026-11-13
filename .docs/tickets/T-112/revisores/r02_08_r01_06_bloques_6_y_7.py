"""QA r02 de T-112 · bloques 6 y 7 de `r01_06_hostiles.py`, que ya no llegan a ejecutarse.

`r01_06` se corta al final de su bloque 5 con un KeyError propio: sirve SIM-MC-001 con `parametros.semilla` 5 y `semilla` 7
y lee `r["resultado"]`, pero desde la corrección de H-05 esa petición se rechaza (dos semillas distintas). Es el efecto
buscado; lo comprueba `r02_07` (bloque 1). Este script ejecuta EL MISMO código de `r01_06` (sin tocarlo): su cabecera y sus
bloques 6 (solicitantes de BIB-MET-001, H-06) y 7 (ACC-VAL-001 con un ejercicio presentado después del corte, H-07).
Uso: .venv/bin/python -I r02_08_r01_06_bloques_6_y_7.py
"""
import sys
from pathlib import Path

aqui = Path(__file__).resolve().parent
fuente = (aqui / "r01_06_hostiles.py").read_text(encoding="utf-8")
m1 = "# ---------------------------------------------------------------- 1. fuzzer"
m6 = "# ---------------------------------------------------------------- 6. BIB-MET-001"
assert fuente.count(m1) == 1 and fuente.count(m6) == 1
fuente = fuente[:fuente.index(m1)] + fuente[fuente.index(m6):]
sys.argv = [str(aqui / "r01_06_hostiles.py")]
exec(compile(fuente, str(aqui / "r01_06_hostiles.py"), "exec"), {"__name__": "__main__", "__file__": str(aqui / "r01_06_hostiles.py")})
