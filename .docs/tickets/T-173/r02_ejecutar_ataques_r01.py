"""T-173 r02: ejecuta `revisores/r01_ataques.py` sección a sección (cada «# N.» en su propio try), para que una sección cuyo
supuesto ya no vale con la r02 (§1–§3 siembran 35 PRG en una sola fecha de resolución: con PA-03 no hay DM que comparar)
no impida ver las demás. No cambia el script del revisor; al leerlo, solo:
- `c["dm_hln"]["p_valor"]` pasa a `(c["dm_hln"] or {}).get("p_valor")`: con muestra insuficiente la r02 no calcula la DM;
- con `--fechas-distintas`, la fecha de resolución por defecto de `sembrar` es una por PRG (emisión + 14 días), para que
  §1–§3 y §5–§10 ejerzan la regla con conglomerados reales (§4 y §12 fijan las suyas; §4b, sus 30 PRG malos).
Uso (desde bloque_a/11_Ejecutor): PYTHONPATH=. python ../../.docs/tickets/T-173/r02_ejecutar_ataques_r01.py [--fechas-distintas]"""
import re
import sys
import traceback
from pathlib import Path

src = (Path(__file__).parent / "revisores" / "r01_ataques.py").read_text(encoding="utf-8")
src = src.replace('c["dm_hln"]["p_valor"]', '(c["dm_hln"] or {}).get("p_valor")')
if "--fechas-distintas" in sys.argv:
    viejo = 'resol=lambda i: "2026-05-29", o=lambda i: int(i % 3 == 0)'
    assert src.count(viejo) == 1
    src = src.replace(viejo, 'resol=lambda i: str((pd.Timestamp("2025-01-20") + pd.Timedelta(days=7 * i)).date()), '
                             'o=lambda i: int(i % 3 == 0)')
src = src.replace('for k, v in R.items():\n    print(k, "=>", v)\n', "")      # se imprime al final
trozos = re.split(r"(?m)^(?=# \d+[a-z]?\. )", src)
ns = {"__name__": "r01_ataques", "__file__": str(Path(__file__).parent / "revisores" / "r01_ataques.py")}
for t in trozos:
    etq = t.splitlines()[0][:70] if t.strip() else ""
    try:
        exec(compile(t, "r01_ataques.py", "exec"), ns)
    except Exception as ex:  # noqa: BLE001
        print(f"[sección «{etq}»] EXCEPCIÓN {type(ex).__name__}: {ex}")
        traceback.print_exc(limit=1, file=sys.stdout)
for k, v in ns.get("R", {}).items():
    print(k, "=>", v)
