"""r01_04 · Validación del prerregistro (tipos raros, fechas límite, max_variantes, objeto, «datos») y CA-6: todo lo que el
registro acepta escribir valida contra el borrador CT-G-24. Necesita jsonschema (el .venv del proyecto).
Uso: .venv/bin/python -B r01_04_prerregistro.py <raíz>"""
import json
import math
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, RAIZ, caso, fin, lanza, lineas, pre, registro_temporal, rx  # noqa: E402

CT24 = json.loads((RAIZ / ".docs" / "diseno" / "contratos" / "ct-g-24_0.1.0-borrador.schema.json").read_text(encoding="utf-8"))
V = jsonschema.Draft202012Validator(CT24)


def intento_pre(datos, autor="qa", ahora=AHORA):
    """(error lanzado o None, ¿escribió algo?, ¿lo escrito valida contra CT-G-24?)"""
    reg = registro_temporal()
    e = lanza(lambda: reg.prerregistrar(datos, autor, ahora), Exception)
    escrito = reg.ruta.exists()
    valida = all(V.is_valid(json.loads(x)) for x in lineas(reg)) if escrito else None
    return e, escrito, valida


# A. Debe rechazarse sin escribir (CA-1)
rechazos = {
    "datos que no es un objeto (lista)": ["hipotesis"],
    "datos None": None,
    "datos que es una cadena con todos los nombres de campo": " ".join(rx.CAMPOS_PRERREGISTRO),
    "objeto en minúsculas": pre(objeto="recorte"),
    "objeto lista": pre(objeto=["RECORTE"]),
    "max_variantes 0": pre(max_variantes=0), "max_variantes 1001": pre(max_variantes=1001),
    "max_variantes -1": pre(max_variantes=-1), "max_variantes 2.0": pre(max_variantes=2.0),
    "max_variantes '2'": pre(max_variantes="2"), "max_variantes None": pre(max_variantes=None),
    "max_variantes NaN": pre(max_variantes=math.nan), "max_variantes infinito": pre(max_variantes=math.inf),
    "semilla True": pre(semilla=True), "semilla 7.0": pre(semilla=7.0), "semilla None": pre(semilla=None),
    "hipótesis de 10 espacios": pre(hipotesis=" " * 10), "hipótesis None": pre(hipotesis=None),
    "fecha 2026-02-30": pre(desde="2026-02-30"), "fecha 2026-13-01": pre(hasta="2026-13-01"),
    "fecha 0000-00-00": pre(desde="0000-00-00"), "fecha con dígitos no ASCII (٢٠٢٦-٠٣-٠٦)": pre(desde="٢٠٢٦-٠٣-٠٦"),
    "desde > hasta": pre(desde="2026-06-01", hasta="2026-05-29"),
    "«datos» None": pre(datos=None), "«datos» 123": pre(datos=123), "«datos» vacío": pre(datos=""),
    "«datos» lista": pre(datos=["a"]),
    "autor vacío": None, "autor None": None,
}
for nombre, d in rechazos.items():
    if nombre == "autor vacío":
        e, esc, val = intento_pre(pre(), autor="  ")
    elif nombre == "autor None":
        e, esc, val = intento_pre(pre(), autor=None)
    else:
        e, esc, val = intento_pre(d)
    bien = isinstance(e, rx.RegistroError) and not esc
    caso(f"rechaza sin escribir: {nombre}", bien,
         "" if bien else f"error={type(e).__name__ if e else None}; escribió={esc}; valida CT-G-24={val}")

# B. Límites que deben aceptarse
for nombre, d in {"max_variantes 1": pre(max_variantes=1), "max_variantes 1000": pre(max_variantes=1000),
                  "desde == hasta": pre(desde="2026-03-06", hasta="2026-03-06"), "semilla negativa": pre(semilla=-1),
                  "semilla 2**64": pre(semilla=2 ** 64), "hipótesis de 10 caracteres": pre(hipotesis="x" * 10),
                  "campo extra": pre(extra={"a": 1})}.items():
    e, esc, val = intento_pre(d)
    caso(f"acepta y valida CT-G-24: {nombre}", e is None and esc and val, f"error={e!r}; valida={val}")

# C. Campo extra con NaN: el registro escribe JSON no estándar
e, esc, val = intento_pre(pre(extra=math.nan))
reg = registro_temporal(); reg.prerregistrar(pre(extra=math.nan), "qa", AHORA)
txt = reg.ruta.read_text(encoding="utf-8")
caso("un NaN en un campo extra no se escribe como JSON no estándar", "NaN" not in txt, "la línea contiene NaN" if "NaN" in txt else "")

# D. El prerregistro no se mezcla: modificar el dict de entrada después no cambia lo sellado
d = pre(extra={"lista": [1]}); reg = registro_temporal(); e = reg.prerregistrar(d, "qa", AHORA); d["extra"]["lista"].append(2)
caso("mutar el dict de entrada después no cambia el registro", reg.verificar() == 1 and
     json.loads(lineas(reg)[0])["contenido"]["extra"] == {"lista": [1]})
fin()
