"""Hallazgo 1 — control_f.py: `controlar` y `validar_informe_f` lanzan ZeroDivisionError.

`ERRORES` no incluye ZeroDivisionError y `_controlar` divide por `ent_eur = precio_entrada * fx`
(sin F-04, F-06, F-07, F-13, F-14 y F-15). Con datos legales para `_forma` (números finitos > 0),
el producto se desborda por debajo a 0.0 y la división lanza, escapando a la promesa «nunca lanza».

Uso: python3 hallazgo_1_control_f_cero_division.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe y OK si está corregido (p. ej. añadiendo ZeroDivisionError a ERRORES).
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

import copy

from control_f import POLITICA_DEFECTO, controlar, validar_informe_f
from pruebas_control_f import AHORA_F, CART, informe_f, solicitud
from pruebas_control_f_t22 import CTX
from pruebas_orquestador import AHORA, hasta, nuevo

mal = []

# 1) controlar: precio 5e-324 con tipo de cambio 5e-324 -> ent_eur = 0.0
sol = solicitud(precio_entrada=5e-324, stop_precio=1e-310)
cart = {**CART, "tipos_cambio_eur": {"USD": 5e-324}}
try:
    r = controlar(sol, cart, POLITICA_DEFECTO, AHORA_F, copy.deepcopy(CTX))
    if r.get("resultado") != "VETADO":
        mal.append(f"resultado inesperado: {r.get('resultado')!r}")
except Exception as e:
    mal.append(f"controlar lanza {type(e).__name__}: {e}")

# 2) lo mismo con magnitudes menos extremas: 1e-170 * 1e-170 también desborda a 0.0
sol_b = solicitud(precio_entrada=1e-170, stop_precio=1e-171)
cart_b = {**CART, "tipos_cambio_eur": {"USD": 1e-170}}
try:
    r = controlar(sol_b, cart_b, POLITICA_DEFECTO, AHORA_F, copy.deepcopy(CTX))
    if r.get("resultado") != "VETADO":
        mal.append(f"resultado inesperado: {r.get('resultado')!r}")
except Exception as e:
    mal.append(f"controlar (1e-170) lanza {type(e).__name__}: {e}")

# 3) validar_informe_f: el recálculo de CF-04 llama a controlar con las entradas del informe
try:
    o = nuevo(); hasta(o, "PROPUESTA")
    inf = informe_f(o)
    inf["payload"]["entradas"]["solicitud"]["precio_entrada"] = 5e-324
    inf["payload"]["entradas"]["cartera"]["tipos_cambio_eur"]["USD"] = 5e-324
    x = o.expedientes["EXP-0001"]
    ctx = {"ahora": AHORA, "expediente_id": "EXP-0001", "correlation_id": x["correlation_id"], "divisa_cotizacion": "USD",
           "propuesta": x["propuesta"], "cartera_destino": x["cartera_destino"], "politica": o.cfg["politica_f"],
           "contexto": o._contexto_de_informe("EXP-0001", inf)}
    fallos = validar_informe_f(inf, ctx)
    if not isinstance(fallos, list) or not fallos:
        mal.append("validar_informe_f no devuelve fallos")
except Exception as e:
    mal.append(f"validar_informe_f lanza {type(e).__name__}: {e}")

print("FALLA " + ("; ".join(mal)) if mal else "OK")
sys.exit(1 if mal else 0)
