"""T-61 · QA de Claude, ronda r01: ataques a certificacion_ranking y _aplicar_respuestas.
Uso: PYTHONPATH=<ruta a bloque_b/11_Ejecutor> python3 r01_ataques.py"""
import math
from bloque_b import evaluador
from bloque_b.orquestacion import Coordinador

fallos = []
def comprobar(nombre, cond):
    print(("OK   " if cond else "FALLA") + " " + nombre)
    if not cond:
        fallos.append(nombre)

cr = evaluador.certificacion_ranking
cfg = {"bootstrap_replicas": 200, "certificado_ranking_n": 3}

# 1. Entradas basura: se descartan, no rompen ni cuentan
basura = [(None, "2024-02-01", 0.1, 0.2), ("2024-01-01", None, 0.1, 0.2), ("mal", "2024-02-01", 0.1, 0.2),
          ("2024-01-01", "2024-02-01", float("nan"), 0.2), ("2024-01-01", "2024-02-01", 0.1, float("inf")),
          ("2024-01-01", "2024-02-01", None, 0.2), ("2024-02-01", "2024-02-01", 0.1, 0.2), ("2024-03-01", "2024-02-01", 0.1, 0.2)]
r = cr(basura, cfg)
comprobar("basura: ninguna ventana cuenta", r["n_sin_solapamiento"] == 0 and r["certificable"] is False)

# 2. Vacío y mínimo cero: nunca certifica sin datos
comprobar("vacío con mínimo 0 no certifica", cr([], {"certificado_ranking_n": 0})["certificable"] is False)

# 3. Duplicados exactos cuentan una sola vez
dup = [("2024-01-01", "2024-02-01", 0.05, 0.3)] * 50
comprobar("50 ventanas idénticas cuentan como 1", cr(dup, cfg)["n_sin_solapamiento"] == 1)

# 4. Ventanas encadenadas (fin de una = inicio de la siguiente) cuentan todas
import datetime as dt
d0 = dt.date(2024, 1, 1)
cad = [((d0 + dt.timedelta(days=30 * i)).isoformat(), (d0 + dt.timedelta(days=30 * (i + 1))).isoformat(), 0.02, 0.2) for i in range(12)]
comprobar("12 ventanas encadenadas cuentan 12", cr(cad, cfg)["n_sin_solapamiento"] == 12)

# 5. Solapadas semanales con horizonte de 4 semanas: cuentan ~1 de cada 4
sem = [((d0 + dt.timedelta(days=7 * i)).isoformat(), (d0 + dt.timedelta(days=7 * i + 28)).isoformat(), 0.02, 0.2) for i in range(40)]
n = cr(sem, cfg)["n_sin_solapamiento"]
comprobar(f"40 semanales a 4 semanas cuentan 10 (obtenido {n})", n == 10)

# 6. Excesos negativos no certifican aunque haya muestra
neg = [(a, b, -0.02, 0.2) for a, b, _, _ in cad]
comprobar("excesos negativos no certifican", cr(neg, cfg)["certificable"] is False)

# 7. Orden de entrada no cambia el resultado
import random
mez = cad[:] ; random.Random(1).shuffle(mez)
comprobar("el orden no cambia el recuento", cr(mez, cfg)["n_sin_solapamiento"] == cr(cad, cfg)["n_sin_solapamiento"])

# 8. _aplicar_respuestas: solo True booleano cierra; respuesta vacía no cierra; tipos raros no rompen
def obj(i): return {"obj_id": i, "fuerza": "fuerte", "respuesta": None, "resuelta": False}
objs = [obj(k) for k in "abcdefg"]
resp = {"a": {"respuesta": "x", "resuelta": True}, "b": {"respuesta": "x", "resuelta": "true"},
        "c": {"respuesta": "x", "resuelta": 1}, "d": {"respuesta": "", "resuelta": True},
        "e": "no es un dict", "f": {"resuelta": True}, "z": {"respuesta": "ajena", "resuelta": True}}
Coordinador._aplicar_respuestas(objs, resp)
estados = {o["obj_id"]: o["estado_contraste"] for o in objs}
comprobar("solo «a» queda resuelta", [k for k, v in estados.items() if v == "resuelta"] == ["a"])
comprobar("todas tienen estado", all(o.get("estado_contraste") for o in objs))

# 9. Idempotencia: aplicar dos veces da lo mismo
antes = [dict(o) for o in objs]
Coordinador._aplicar_respuestas(objs, resp)
comprobar("aplicar dos veces es idempotente", antes == objs)

print(f"\n{len(fallos)} fallos")
raise SystemExit(1 if fallos else 0)
