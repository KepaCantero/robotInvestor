"""r02_04 · Regla de adopción por variante [PROPUESTO]: combinaciones de veredictos, intentos sin resultado, orden de los
resultados, «fallido», variantes en NFC/NFD y con espacios, fuera del máximo e instantes en el borde.
Uso: python3 -B r02_04_adopcion.py <raíz>"""
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r02_comun import AHORA, DESPUES, caso, fin, lanza, pre, registro_temporal, rx  # noqa: E402


def exp(max_variantes=1, creado=AHORA):
    reg = registro_temporal()
    return reg, reg.prerregistrar(pre(max_variantes=max_variantes), "qa", creado)["exp_id"]


def serie(veredictos, variante="única", max_variantes=1):
    reg, e = exp(max_variantes)
    for v in veredictos:
        n = reg.intento(e, variante, DESPUES)["n"]
        if v is not None:
            reg.resultado(e, n, v, ahora=DESPUES)
    return reg, e


M, P, T, F = "mejor", "peor", "todavía no se sabe", "fallido"
# 1. Combinaciones en una sola variante: (veredictos, adoptable esperado según la regla declarada)
for vs, esperado in (([M], True), ([M, M], True), ([M, P], False), ([P, M], False), ([F, M], True), ([M, F], True),
                     ([T, M], False), ([M, T], False), ([F, F, M], True), ([F, F], False), ([T], False), ([P], False)):
    reg, e = serie(vs)
    r = reg.resumen(e)
    caso(f"variante con {vs}: adoptable={esperado} (regla declarada)", r["adoptable"] is esperado,
         f"adoptable={r['adoptable']}, contradictorias={r['contradictorias']}")
reg, e = serie([P, P, F, T, P, M]); r = reg.resumen(e)
caso("r01_06 caso 4 (5 en contra y 1 a favor): no adoptable y la variante sale como contradictoria",
     not r["adoptable"] and r["contradictorias"] == ["única"])

# 2. Intento sin resultado antes de un «mejor» de la misma variante: ¿cuenta el que se calló?
reg, e = serie([None, M]); r = reg.resumen(e)
caso("intento 1 sin resultado (el que salió mal y no se anotó) y el 2 «mejor»: no adoptable hasta que el 1 tenga resultado",
     not r["adoptable"], f"adoptable={r['adoptable']}, sin_resultado={r['sin_resultado']}, por_variante={r['por_variante']['única']}")
reg, e = serie([None, None, None, M]); r = reg.resumen(e)
caso("tres intentos callados y el cuarto «mejor»: no adoptable", not r["adoptable"], f"adoptable={r['adoptable']}")

# 3. El orden en que se anotan los resultados: el adoptable no debe cambiar de sí a no
reg, e = exp(1); n1 = reg.intento(e, "única", DESPUES)["n"]; n2 = reg.intento(e, "única", DESPUES)["n"]
reg.resultado(e, n2, M, ahora=DESPUES); antes = reg.adoptable(e)
reg.resultado(e, n1, P, ahora=DESPUES); despues = reg.adoptable(e)
caso("resultado del intento 2 antes que el del 1: el adoptable no pasa de sí a no", not (antes and not despues),
     f"adoptable con el 2 «mejor» y el 1 pendiente: {antes}; con el 1 «peor»: {despues}")

# 4. «fallido» marcado a mano desde la línea de órdenes (el veredicto lo pone quien anota)
reg, e = serie([F, F, F, M])
caso("(regla declarada) los «fallido» no cuentan: tres «fallido» y un «mejor» es adoptable", reg.adoptable(e),
     "desde la línea de órdenes el veredicto lo elige quien anota; solo el banco lo calcula")

# 5. Variantes NFC/NFD, con espacios y con mayúsculas
nfc = "única"; nfd = unicodedata.normalize("NFD", nfc)
reg, e = exp(1); reg.intento(e, nfc, DESPUES); i2 = reg.intento(e, nfd, DESPUES)
caso("«única» en NFC y en NFD es la misma variante (dentro del máximo 1)", i2["dentro_del_maximo"] and reg.resumen(e)["variantes"] == 1)
reg, e = exp(1); reg.intento(e, "v1", DESPUES); i2 = reg.intento(e, "v1 ", DESPUES)
caso("(regla declarada) «v1» y «v1 » son variantes distintas: la segunda queda fuera del máximo (lado seguro)",
     not i2["dentro_del_maximo"])
for mala in ("", "   ", None, 1, ["v"], "\ud800"):
    reg, e = exp(1)
    x = lanza(lambda: reg.intento(e, mala, DESPUES), Exception)
    caso(f"variante {mala!r}: RegistroError y nada escrito", isinstance(x, rx.RegistroError) and reg.verificar() == 1,
         f"{type(x).__name__}: {str(x)[:70]}")

# 6. Fuera del máximo
reg, e = exp(1)
reg.intento(e, "v1", DESPUES); reg.resultado(e, 1, P, ahora=DESPUES); reg.intento(e, "v2", DESPUES); reg.resultado(e, 2, M, ahora=DESPUES)
caso("max 1: la segunda variante gana y no es adoptable", not reg.adoptable(e))
reg, e = exp(2)
for v, ver in (("v1", P), ("v2", P), ("v3", M), ("v1", M)):
    n = reg.intento(e, v, DESPUES)["n"]; reg.resultado(e, n, ver, ahora=DESPUES)
r = reg.resumen(e)
caso("max 2: v3 gana fuera del máximo y v1 se contradice: no adoptable", not r["adoptable"] and r["fuera_del_maximo"] == [3])

# 7. Instantes en el borde
for creado, inicio, esperado, nombre in (
        (AHORA, AHORA, True, "mismo instante (>=)"),
        ("2026-11-12T10:00:00Z", "2026-11-12T12:00:00+02:00", True, "mismo instante en otra zona"),
        ("2026-11-12T10:00:00.000001+00:00", AHORA, False, "un microsegundo antes"),
        (AHORA, "2026-11-12T09:59:59+00:00", False, "un segundo antes"),
        ("2026-11-12T10:00:00-02:00", "2026-11-12T11:00:00+00:00", False, "una hora antes en otra zona (r01 H-07)")):
    reg, e = exp(1, creado); reg.intento(e, "v1", inicio); reg.resultado(e, 1, M, ahora=DESPUES)
    caso(f"inicio {nombre}: adoptable={esperado}", reg.adoptable(e) is esperado)
reg = registro_temporal(); x = reg.prerregistrar(pre(), "qa", "2026-12-31T23:30:00-01:00")
caso("prerregistro a las 23:30-01:00 del 31-12: año UTC 2027", x["exp_id"].startswith("EXP-2027-"), x["exp_id"])
for malo in ("2026-11-12T10:00:00", "2026-11-12 10:00:00+00:00", "2026-02-30T10:00:00Z", "2026-11-12T10:00:00+24:00",
             "２０２６-11-12T10:00:00+00:00", "2026-11-12T10:00:60Z"):
    reg = registro_temporal()
    x = lanza(lambda: reg.prerregistrar(pre(), "qa", malo), Exception)
    caso(f"«ahora» {malo!r}: RegistroError y nada escrito", isinstance(x, rx.RegistroError) and not reg.ruta.exists(),
         f"{type(x).__name__ if x else 'aceptado'}")
# 7b. Fechas del contenido con cifras no ASCII (el patrón \d de Python las admite; un validador JSON Schema en ECMA, no)
reg = registro_temporal()
x = lanza(lambda: reg.prerregistrar(pre(desde="２０２６-03-06"), "qa", AHORA), Exception)
caso("«desde» con cifras de ancho completo: RegistroError", isinstance(x, rx.RegistroError), f"{type(x).__name__ if x else 'aceptado'}")
fin()
