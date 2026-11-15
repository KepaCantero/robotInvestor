"""r03_04 · La regla de adopción con intentos pendientes del registro 0.3.0 (H-15, decisión [PROPUESTO] (1)): secuencias de
una variante con intentos sin resultado, resultados anotados en otro orden y el «fallido» anotado tarde.
Uso: .venv/bin/python -B r03_04_adopcion_pendientes.py <raíz>"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r03_comun import AHORA, DESPUES, borrar, caso, fin, pre, rx, tmpdir  # noqa: E402

tmps = []


def montar(maximo=1):
    d = tmpdir(); tmps.append(d)
    reg = rx.Registro(d / "registro.jsonl")
    return reg, reg.prerregistrar(pre(max_variantes=maximo), "qa", ahora=AHORA)["exp_id"]


def serie(pasos, maximo=1):
    """pasos: ("i", variante) abre un intento; ("r", n, veredicto) anota el resultado del intento n."""
    reg, exp = montar(maximo)
    for p in pasos:
        if p[0] == "i":
            reg.intento(exp, p[1], ahora=DESPUES)
        else:
            reg.resultado(exp, p[1], p[2], ahora=DESPUES)
    return reg.resumen(exp)


I, R = (lambda v="v1": ("i", v)), (lambda n, v: ("r", n, v))
tabla = [
    ("1 sin resultado, 2 «mejor»", [I(), I(), R(2, "mejor")], False),
    ("1 «mejor», 2 sin resultado (repetición en curso)", [I(), R(1, "mejor"), I()], False),
    ("1 «mejor», 2 «mejor»", [I(), R(1, "mejor"), I(), R(2, "mejor")], True),
    ("1 «fallido», 2 «mejor»", [I(), R(1, "fallido"), I(), R(2, "mejor")], True),
    ("1 sin resultado, 2 «mejor» y después 1 «peor»", [I(), I(), R(2, "mejor"), R(1, "peor")], False),
    ("1 sin resultado, 2 «mejor» y después 1 «todavía no se sabe»", [I(), I(), R(2, "mejor"), R(1, "todavía no se sabe")], False),
    ("1 sin resultado, 2 «mejor» y después 1 «mejor»", [I(), I(), R(2, "mejor"), R(1, "mejor")], True),
    ("v1 sin resultado y v2 «mejor» (máximo 2): v2 no depende de v1", [I("v1"), I("v2"), R(2, "mejor")], True),
]
for nombre, pasos, esperado in tabla:
    r = serie(pasos, 2 if "máximo 2" in nombre else 1)
    caso(f"{nombre}: adoptable={esperado}", r["adoptable"] == esperado,
         f"adoptable={r['adoptable']}; por_variante={ {k: (v['cuenta'], v['veredicto'], v['pendiente']) for k, v in r['por_variante'].items()} }")

# El «fallido» anotado TARDE: el intento 1 quedó abierto (el banco murió con un kill -9); se repite la variante, sale «mejor», y
# DESPUÉS de verlo se cierra el 1 como «fallido» a mano. Con «peor» no sería adoptable; con «fallido», sí: se elige a posteriori.
r = serie([I(), I(), R(2, "mejor"), R(1, "fallido")])
caso("«fallido» anotado al intento 1 después de ver el «mejor» del 2: no deja adoptar (se elige a posteriori)",
     not r["adoptable"], f"adoptable={r['adoptable']}; veredictos={r['veredictos']}")
r = serie([I(), R(1, "fallido"), I(), I(), R(3, "mejor"), R(2, "fallido")])
caso("…ni con varios: 1 «fallido» a tiempo, 2 abierto, 3 «mejor», y el 2 cerrado tarde como «fallido»",
     not r["adoptable"], f"adoptable={r['adoptable']}; veredictos={r['veredictos']}")

# El resumen dice qué intentos están pendientes
r = serie([I(), I(), R(2, "mejor")])
caso("el resumen lista los intentos sin resultado y marca la variante pendiente",
     r["sin_resultado"] == [1] and r["por_variante"]["v1"]["pendiente"] is True, f"{r['sin_resultado']}, {r['por_variante']}")

for t in tmps:
    borrar(t)
fin()
