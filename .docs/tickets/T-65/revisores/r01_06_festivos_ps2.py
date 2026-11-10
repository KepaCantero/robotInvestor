"""r01_06 · QA T-65 · H-17: bordes de `validar_festivos_ps2` y de `_sesiones_entre`.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r01_06_festivos_ps2.py
"""
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path.cwd()))
from bloque_a.orquestacion import _sesiones_entre, validar_festivos_ps2  # noqa: E402

base = {"viernes_santo": True, "lunes_de_pascua": False}
hall = 0
for fijos, valido in ((["12-25"], True), (["02-29"], True), (["12- 5"], False), (["1-1-1"], False), (["13-01"], False),
                      (["00-10"], False), (["12/25"], False), ([" 1-25"], False), (["12-25", "12-25"], True), (["1225"], False),
                      (["12-32"], False), (["04-31"], False), ([None], False), ([True], False), (["ab-cd"], False),
                      (["+1-01"], False), (["01-0x"], False), (["١٢-٢٥"], False)):
    try:
        out = validar_festivos_ps2({**base, "fijos": fijos})
        ok = valido
        det = f"acepta → {out['fijos']}"
    except ValueError as e:
        ok = not valido
        det = f"rechaza ({str(e)[:70]})"
    hall += not ok
    print(f"{'OK      ' if ok else 'HALLAZGO'} fijos={fijos!r}: {det}")
for k, v in (("viernes_santo", 1), ("viernes_santo", "true"), ("lunes_de_pascua", None), ("viernes_santo", 0)):
    try:
        validar_festivos_ps2({**base, "fijos": [], k: v})
        print(f"HALLAZGO {k}={v!r}: aceptado"); hall += 1
    except ValueError:
        print(f"OK       {k}={v!r}: rechazado")
# Sesiones alrededor de Pascua 2027 (Viernes Santo 26-3, lunes 29-3) y Navidad
f = validar_festivos_ps2({"viernes_santo": True, "lunes_de_pascua": True, "fijos": ["12-25", "12-26", "01-01"]})
for d0, d1, esperado in (("2027-03-25", "2027-03-30", 1), ("2027-03-25", "2027-03-29", 1), ("2026-12-24", "2026-12-28", 1),
                         ("2026-12-31", "2027-01-04", 1), ("2026-06-05", "2026-06-05", 0), ("2026-06-08", "2026-06-05", 0)):
    s = _sesiones_entre(d0, d1, f)
    ok = s == esperado
    hall += not ok
    print(f"{'OK      ' if ok else 'HALLAZGO'} sesiones [{d0}, {d1}) = {s} (esperado {esperado})")
print(f"HALLAZGOS: {hall}")
