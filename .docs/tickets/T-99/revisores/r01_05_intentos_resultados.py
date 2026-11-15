"""r01_05 · Intentos y resultados: sin prerregistro, sobre otro experimento, doble resultado, veredictos no válidos, tipos
raros de n, variante y detalle, y CA-6 para lo que se acepta. Uso: .venv/bin/python -B r01_05_intentos_resultados.py <raíz>"""
import json
import math
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, DESPUES, RAIZ, caso, fin, lanza, lineas, pre, registro_temporal, rx  # noqa: E402

V = jsonschema.Draft202012Validator(json.loads(
    (RAIZ / ".docs" / "diseno" / "contratos" / "ct-g-24_0.1.0-borrador.schema.json").read_text(encoding="utf-8")))


def nuevo(**k):
    reg = registro_temporal()
    a = reg.prerregistrar(pre(**k), "qa", AHORA)["exp_id"]
    b = reg.prerregistrar(pre(**k), "qa", AHORA)["exp_id"]
    return reg, a, b


def no_escribe(reg, f, nombre):
    antes = reg.ruta.read_bytes()
    e = lanza(f, Exception)
    bien = isinstance(e, rx.RegistroError) and reg.ruta.read_bytes() == antes
    caso(nombre, bien, "" if bien else f"error={e!r}; escribió={reg.ruta.read_bytes() != antes}")


reg, a, b = nuevo()
no_escribe(reg, lambda: reg.intento("EXP-2026-0099", "v1", DESPUES), "intento sobre un experimento sin prerregistro")
no_escribe(reg, lambda: reg.intento("exp-2026-0001", "v1", DESPUES), "intento con el identificador en minúsculas")
no_escribe(reg, lambda: reg.resultado(a, 1, "mejor", ahora=DESPUES), "resultado sin intento")
reg.intento(a, "v1", DESPUES)
no_escribe(reg, lambda: reg.resultado(b, 1, "mejor", ahora=DESPUES), "resultado sobre otro experimento (B no tiene el intento 1 de A)")
for v in ("Mejor", "mejor ", "todavia no se sabe", "", None, "MEJOR"):
    no_escribe(reg, lambda v=v: reg.resultado(a, 1, v, ahora=DESPUES), f"veredicto no válido {v!r}")
no_escribe(reg, lambda: reg.resultado(a, 0, "peor", ahora=DESPUES), "resultado del intento 0")
no_escribe(reg, lambda: reg.resultado(a, -1, "peor", ahora=DESPUES), "resultado del intento -1")
no_escribe(reg, lambda: reg.resultado(a, "1", "peor", ahora=DESPUES), "resultado con n='1' (cadena)")
# n = True o 1.0: casan con el intento 1 y se escriben con el tipo equivocado
for nombre, n in (("True", True), ("1.0", 1.0)):
    r2 = registro_temporal(); e = r2.prerregistrar(pre(), "qa", AHORA)["exp_id"]; r2.intento(e, "v1", DESPUES)
    err = lanza(lambda: r2.resultado(e, n, "mejor", ahora=DESPUES), Exception)
    ok = isinstance(err, rx.RegistroError) or all(V.is_valid(json.loads(x)) for x in lineas(r2))
    caso(f"resultado con n={nombre}: se rechaza o lo escrito valida CT-G-24", ok,
         "" if ok else f"escribió n={json.loads(lineas(r2)[-1])['n']!r}, que no valida CT-G-24")
reg.resultado(a, 1, "peor", ahora=DESPUES)
no_escribe(reg, lambda: reg.resultado(a, 1, "peor", ahora=DESPUES), "doble resultado con el mismo veredicto")
no_escribe(reg, lambda: reg.resultado(a, 1, "mejor", ahora=DESPUES), "doble resultado con otro veredicto")

# detalle que no es un objeto: CT-G-24 exige objeto
for nombre, det in (("lista", [1]), ("cadena", "texto"), ("número", 5), ("NaN", math.nan), ("0", 0), ("[] vacía", [])):
    r2 = registro_temporal(); e = r2.prerregistrar(pre(), "qa", AHORA)["exp_id"]; r2.intento(e, "v1", DESPUES)
    err = lanza(lambda: r2.resultado(e, 1, "peor", det, ahora=DESPUES), Exception)
    ultima = json.loads(lineas(r2)[-1])
    ok = isinstance(err, rx.RegistroError) or (V.is_valid(ultima) and "NaN" not in lineas(r2)[-1])
    caso(f"detalle {nombre}: se rechaza o lo escrito valida CT-G-24", ok,
         "" if ok else f"escribió detalle={ultima.get('detalle')!r}")

# variante: tipos raros
for nombre, var in (("None", None), ("vacía", ""), ("entero 1", 1), ("dict", {"a": 1})):
    r2 = registro_temporal(); e = r2.prerregistrar(pre(), "qa", AHORA)["exp_id"]
    err = lanza(lambda: r2.intento(e, var, DESPUES), Exception)
    escrito = json.loads(lineas(r2)[-1]) if not err else None
    caso(f"variante {nombre}: se rechaza (no se convierte en silencio en texto)", isinstance(err, rx.RegistroError),
         f"escribió variante={escrito['variante']!r}" if escrito and escrito["tipo"] == "INTENTO" else repr(err))

# variante 1 (entero) y «1» (texto) cuentan como la misma: ¿y «única» NFC frente a NFD?
import unicodedata  # noqa: E402
r2 = registro_temporal(); e = r2.prerregistrar(pre(max_variantes=1), "qa", AHORA)["exp_id"]
r2.intento(e, "única", DESPUES); i2 = r2.intento(e, unicodedata.normalize("NFD", "única"), DESPUES)
caso("«única» en NFC y en NFD son la misma variante (lección macOS)", i2["dentro_del_maximo"],
     "la NFD cuenta como variante nueva y queda fuera del máximo" if not i2["dentro_del_maximo"] else "")

# intentos tras resultados: siguen numerando bien
r2 = registro_temporal(); e = r2.prerregistrar(pre(), "qa", AHORA)["exp_id"]
ns = [r2.intento(e, "v1", DESPUES)["n"] for _ in range(3)]
caso("los intentos se numeran 1, 2, 3 por experimento", ns == [1, 2, 3])
r2.resultado(e, 3, "peor", ahora=DESPUES); r2.resultado(e, 1, "fallido", ahora=DESPUES)
caso("los resultados pueden llegar en otro orden; el 2 queda sin resultado", r2.resumen(e)["sin_resultado"] == [2])
fin()
