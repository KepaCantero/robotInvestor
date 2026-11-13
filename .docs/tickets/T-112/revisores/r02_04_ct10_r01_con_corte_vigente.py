"""QA r02 de T-112 · `r01_07_ct10.py` con la fecha de corte del proveedor movida.

`r01_07` fija el `as_of` del proveedor en 2024-06-28 y sirve casos de control fechados en 2026. Desde la corrección de H-07
(ea52b1e) las fichas rechazan los datos en línea posteriores a la fecha de corte, así que `r01_07` ya no puede servir su
cálculo base (ACC-VAL-001, capitalización del 2026-11-06) y aborta con un AssertionError propio: es efecto de la corrección,
no un fallo del CT-10. Lo mismo con H-05: `r01_07` pide SIM-MC-001 con `semilla` 4242 sobre un caso de control que ya trae
`parametros.semilla` 112, y ahora dos semillas distintas se rechazan. Este script ejecuta EL MISMO código de `r01_07` (sin
tocarlo) con el `as_of` en 2026-11-13 y la semilla de la petición igual a la del caso (la semilla solo en la petición se
prueba en `r02_05`).
Uso: .venv/bin/python -I r02_04_ct10_r01_con_corte_vigente.py
"""
import sys
from pathlib import Path

aqui = Path(__file__).resolve().parent
fuente = (aqui / "r01_07_ct10.py").read_text(encoding="utf-8")
assert fuente.count('prov.fijar_as_of("2024-06-28")') == 1
fuente = fuente.replace('prov.fijar_as_of("2024-06-28")', 'prov.fijar_as_of("2026-11-13")')
assert fuente.count('servir("SIM-MC-001", semilla=4242)') == 1
fuente = fuente.replace('servir("SIM-MC-001", semilla=4242)', 'servir("SIM-MC-001", semilla=112)')
sys.argv = [str(aqui / "r01_07_ct10.py")]
exec(compile(fuente, str(aqui / "r01_07_ct10.py"), "exec"), {"__name__": "__main__", "__file__": str(aqui / "r01_07_ct10.py")})
