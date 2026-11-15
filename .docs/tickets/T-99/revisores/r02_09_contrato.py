"""r02_09 · CA-6 con casos de borde: todo lo que escribe el registro 0.2.0 (también con textos raros, zonas, fracciones de
segundo, NFD, U+2028, enteros grandes y el prerregistro del banco con su clave de más) valida contra el borrador de CT-G-24,
y lo que el borrador rechaza el registro no lo escribe.
Uso: .venv/bin/python -B r02_09_contrato.py <raíz>"""
import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r02_comun import AHORA, DESPUES, RAIZ, caso, fin, lanza, pre, registro_temporal, rx  # noqa: E402

import jsonschema  # noqa: E402

ESQ = json.loads((RAIZ / ".docs" / "diseno" / "contratos" / "ct-g-24_0.1.0-borrador.schema.json").read_text(encoding="utf-8"))
V = jsonschema.Draft202012Validator(ESQ)

reg = registro_temporal()
casos = [
    (pre(hipotesis="Hipótesis con separador y \u0085 NEL", semilla=10 ** 30, max_variantes=1000), "qa", AHORA),
    (pre(datos="x", fuente_banco="cliente mock, datos ejemplos"), " a ", "2026-11-12T10:00:00.123456Z"),
    (pre(objeto="OTRO"), "qa", "2026-11-12T10:00:00-09:30"),
]
exps = [reg.prerregistrar(*c)["exp_id"] for c in casos]
for e in exps:
    for v in ("v1", unicodedata.normalize("NFD", "única"), "x y", "🙂"):
        n = reg.intento(e, v, "2026-11-12T11:00:00+14:00")["n"]
        reg.resultado(e, n, "todavía no se sabe", {"anidado": {"lista": [1, 2.5, None, True, "ñ"]}, "": ""}, ahora=DESPUES)
malos = [(i, list(V.iter_errors(json.loads(x)))) for i, x in enumerate(reg.ruta.read_text(encoding="utf-8").split("\n")[:-1], 1)]
malos = [(i, [er.message[:60] for er in errs]) for i, errs in malos if errs]
caso(f"todas las {reg.verificar()} anotaciones con bordes validan CT-G-24", not malos, str(malos[:3]))

# Lo que el borrador rechaza, el registro no lo escribe (y al revés: no hay nada que el registro escriba y el borrador rechace)
base = json.loads(reg.ruta.read_text(encoding="utf-8").split("\n")[0])
for nombre, cambio in (("hipótesis de 9", {"hipotesis": "123456789"}), ("max 0", {"max_variantes": 0}),
                       ("objeto en minúsculas", {"objeto": "recorte"}), ("semilla 1.0", {"semilla": 1.0}),
                       ("datos 1", {"datos": 1})):
    cont = {**base["contenido"], **cambio}
    esquema_rechaza = any(True for _ in V.iter_errors({**base, "contenido": cont}))
    r2 = registro_temporal()
    reg_rechaza = isinstance(lanza(lambda: r2.prerregistrar(cont, "qa", AHORA), Exception), rx.RegistroError)
    if nombre == "semilla 1.0":   # JSON Schema cuenta 1.0 como entero; el registro es más estricto (lado seguro)
        caso("(referencia) semilla 1.0: el registro la rechaza aunque el borrador la admita", reg_rechaza,
             f"borrador rechaza={esquema_rechaza}, registro rechaza={reg_rechaza}")
        continue
    caso(f"{nombre}: el borrador lo rechaza y el registro también", esquema_rechaza and reg_rechaza,
         f"borrador rechaza={esquema_rechaza}, registro rechaza={reg_rechaza}")
fin()
