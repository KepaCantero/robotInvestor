"""r01_07 · Reloj y numeración EXP-AAAA-NNNN: cambio de año, huecos, otra zona en el borde del año, más de 9999 en un año,
identificador repetido escrito a mano y el «ahora» real. Uso: .venv/bin/python -B r01_07_reloj_numeracion.py <raíz>"""
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, DESPUES, RAIZ, caso, escribir, fin, lineas, pre, recadenar, registro_temporal, rx  # noqa: E402

V = jsonschema.Draft202012Validator(json.loads(
    (RAIZ / ".docs" / "diseno" / "contratos" / "ct-g-24_0.1.0-borrador.schema.json").read_text(encoding="utf-8")))

# 1. cambio de año
reg = registro_temporal()
ids = [reg.prerregistrar(pre(), "qa", t)["exp_id"] for t in
       ("2026-12-31T23:59:59+00:00", "2026-12-31T23:59:59+00:00", "2027-01-01T00:00:00+00:00", "2026-12-31T23:59:59+00:00")]
caso("cambio de año: 2026-0001, 2026-0002, 2027-0001 y un 2026 tardío 2026-0003", ids ==
     ["EXP-2026-0001", "EXP-2026-0002", "EXP-2027-0001", "EXP-2026-0003"], str(ids))

# 2. sin huecos y correlativos
reg = registro_temporal()
ids = [reg.prerregistrar(pre(), "qa", AHORA)["exp_id"] for _ in range(12)]
caso("doce prerregistros seguidos: correlativos y sin huecos", ids == [f"EXP-2026-{i:04d}" for i in range(1, 13)])

# 3. otra zona en el borde del año: 2027-01-01T00:30+01:00 es 2026-12-31T23:30Z
reg = registro_temporal()
i = reg.prerregistrar(pre(), "qa", "2027-01-01T00:30:00+01:00")["exp_id"]
caso("el año del identificador es el de UTC aunque el «ahora» venga en otra zona", i == "EXP-2026-0001",
     f"{i}: toma los cuatro primeros caracteres del texto")

# 4. «ahora» real: UTC con segundos y valida CT-G-24
reg = registro_temporal(); e = reg.prerregistrar(pre(), "qa")
caso("con el reloj real, creado_en es UTC y el año del EXP es el de UTC", e["creado_en"].endswith("+00:00")
     and e["exp_id"].startswith(f"EXP-{datetime.now(UTC).year}-") and V.is_valid(e))

# 5. más de 9999 en un año (simulado recadenando 9999 prerregistros)
reg = registro_temporal()
base = json.loads(json.dumps(reg.prerregistrar(pre(), "qa", AHORA)))
objs = []
for k in range(1, 10000):
    o = dict(base); o["exp_id"] = f"EXP-2026-{k:04d}"; objs.append(o)
escribir(reg, recadenar(objs))
e = reg.prerregistrar(pre(), "qa", AHORA)
caso("el prerregistro 10000 del año se rechaza o tiene un identificador que valida CT-G-24", V.is_valid(e),
     f"escribió {e['exp_id']}, que no casa con ^EXP-\\d{{4}}-\\d{{4}}$")

# 6. «ahora» inyectado mal formado
for t in ("ayer", "2026-11-12", "12/11/2026 10:00", "20261112T100000Z"):
    reg = registro_temporal()
    try:
        e = reg.prerregistrar(pre(), "qa", t)
        caso(f"ahora={t!r} se rechaza o lo escrito valida CT-G-24", V.is_valid(e), f"escribió exp_id={e['exp_id']}, creado_en={t!r}")
    except rx.RegistroError:
        caso(f"ahora={t!r} se rechaza", True)

# 7. identificador repetido escrito a mano con la cadena recalculada: ¿lo detecta verificar() o el siguiente prerregistro?
reg = registro_temporal(); a = reg.prerregistrar(pre(max_variantes=1), "qa", AHORA)
objs = [json.loads(x) for x in lineas(reg)]
otro = dict(objs[0]); otro["contenido"] = dict(otro["contenido"], criterio_exito="un criterio mucho más laxo que el original",
                                                max_variantes=1000)
otro["huella_prerregistro"] = rx.huella(otro["contenido"])
escribir(reg, recadenar(objs + [otro]))
try:
    reg.verificar(); detectado = False
except rx.RegistroError:
    detectado = True
caso("dos PRERREGISTRO con el mismo EXP-… (cadena recalculada): verificar() lo rechaza", detectado,
     f"verificar = {reg.verificar() if not detectado else '-'}; experimento() devuelve el primero")
n = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
caso("…y el siguiente prerregistro no reutiliza un identificador existente", n not in ("EXP-2026-0001", "EXP-2026-0002"), n)

# 8. prerregistro con exp_id de otro año escrito a mano en medio: la cuenta por año
reg = registro_temporal(); reg.prerregistrar(pre(), "qa", AHORA)
objs = [json.loads(x) for x in lineas(reg)]; o = dict(objs[0]); o["exp_id"] = "EXP-2026-0005"
escribir(reg, recadenar(objs + [o]))
n = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
caso("con un hueco escrito a mano (0001, 0005), el siguiente no choca con uno existente", n not in ("EXP-2026-0001", "EXP-2026-0005"), n)
fin()
