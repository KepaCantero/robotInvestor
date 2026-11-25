"""QA r01 (Claude) de T-193: ataques directos al monitor HT-08 (PB-18), sin modelo ni almacén.

Uso, desde bloque_a/11_Ejecutor con la venv del repo:  python ../../.docs/tickets/T-193/revisores/r01_ataques_monitor.py
Cada caso imprime OK o FALLO con lo observado. Un FALLO es un hallazgo (o la prueba de que el criterio no se cumple).
"""
import math
import sys

sys.path.insert(0, ".")
from bloque_a.herramientas.ht08_monitor import Monitor  # noqa: E402

fallos = []


def caso(nombre, cond, detalle=""):
    print(("OK    " if cond else "FALLO ") + nombre + (f" · {detalle}" if detalle else ""))
    if not cond:
        fallos.append(nombre)


def monitor(obj=1.0):
    t = [0.0]
    return Monitor(objetivo_ingesta_s=obj, reloj=lambda: t[0]), t


def ingesta(m, t, dur, ag="AG-12"):
    m.encolar(ag)
    t0 = m.inicio(ag)
    t[0] += dur
    m.fin(ag, t0)


# 1. Objetivo inválido: falla cerrado al construir
for malo in (0, -1, float("nan"), float("inf"), True, "5", [1]):
    try:
        Monitor(objetivo_ingesta_s=malo)
        caso(f"objetivo {malo!r} rechazado", False, "se aceptó")
    except ValueError:
        caso(f"objetivo {malo!r} rechazado", True)

# 2. Borde del disparo por tiempo: exactamente 2× no abre; un poco más sí (en la misma lectura)
m, t = monitor()
ingesta(m, t, 2.0)
caso("W = 2× objetivo no abre", not m.evaluar_instancias())
m, t = monitor()
ingesta(m, t, 2.0001)
o = m.evaluar_instancias()
caso("W > 2× objetivo abre en la primera lectura", len(o) == 1 and o[0]["accion"] == "ABRIR", str(o))

# 3. Dimensionado c = ⌈λ/(μ·0,75)⌉: 10 llegadas en 10 s, W = 3 s → λ = 1/s, μ = 1/3 → c = ⌈4⌉ = 4
m2, t2 = monitor(1.0)
for _ in range(10):
    m2.encolar("AG-12")
t2[0] = 10.0
for _ in range(10):
    m2.fin("AG-12", 7.0)                   # diez servicios de 3 s solapados en la ventana de 10 s
o = m2.evaluar_instancias()
caso("c = ⌈λ/(μ·0,75)⌉ = 4", bool(o) and o[0]["instancias_despues"] == 4, str(o))
caso("ORD- con λ y μ en metricas_disparo (esquema HA 4.5: cola, W, rho, lambda, mu)",
     bool(o) and {"cola", "W", "rho", "lambda", "mu"} <= set(o[0]["metricas_disparo"]), str(o and o[0]["metricas_disparo"]))

# 4. Cierre: ρ ≥ 0,30 en las dos lecturas no cierra
m, t = monitor()
ingesta(m, t, 3.0)
m.evaluar_instancias()                     # abre a 2
for _ in range(2):
    ingesta(m, t, 1.5)                     # ocupado 1,5 s en 2 s → ρ = 1,5/(2·2) = 0,375
    t[0] += 0.5
    r = m.evaluar_instancias()
caso("ρ ≥ 0,30 no cierra", not [x for x in r if x["accion"] == "CERRAR"] and m.instancias["AG-12"] == 2, str(r))

# 5. Cierre: cola > 0 (encargo en curso) no cierra aunque ρ sea bajo
m, t = monitor()
ingesta(m, t, 3.0)
m.evaluar_instancias()
m.encolar("AG-12")                         # en curso, sin terminar
r = []
for _ in range(3):
    t[0] += 100
    r += m.evaluar_instancias()
caso("con un encargo en curso no se cierra", not [x for x in r if x["accion"] == "CERRAR"], str(r))

# 6. Histéresis: libre, ocupado, libre → no cierra (las dos lecturas deben ser consecutivas)
m, t = monitor()
ingesta(m, t, 3.0)
m.evaluar_instancias()
t[0] += 10
a = m.evaluar_instancias()                 # libre (1)
ingesta(m, t, 1.9)
t[0] += 0.1
b = m.evaluar_instancias()                 # ρ = 1,9/(2·2) ≈ 0,475 → no libre
t[0] += 10
c = m.evaluar_instancias()                 # libre (1)
caso("libre-ocupado-libre no cierra", not (a + b + c), str(a + b + c))
t[0] += 10
d = m.evaluar_instancias()
caso("la segunda lectura libre consecutiva cierra una", len(d) == 1 and d[0]["accion"] == "CERRAR" and d[0]["instancias_despues"] == 1, str(d))

# 7. Nunca baja de 1 instancia
r = []
for _ in range(6):
    t[0] += 10
    r += m.evaluar_instancias()
caso("no cierra por debajo de una instancia", not r and m.instancias["AG-12"] == 1, str(r))

# 8. Dos lecturas en el mismo instante (ventana 0): sin división por cero y sin cierre
m, t = monitor()
ingesta(m, t, 3.0)
m.evaluar_instancias()
try:
    r = m.evaluar_instancias() + m.evaluar_instancias()
    caso("ventana 0 sin error ni cierre", not r, str(r))
except ZeroDivisionError as e:
    caso("ventana 0 sin error ni cierre", False, repr(e))

# 9. Tope de instancias
m, t = monitor()
m.instancias_max = 3
r = []
for _ in range(6):
    ingesta(m, t, 50.0)
    r += m.evaluar_instancias()
caso("respeta instancias_max", m.instancias["AG-12"] == 3, str(m.instancias["AG-12"]))

# 10. Sin objetivo (config por defecto: null) no hay disparo por tiempo
m, t = monitor(None)
ingesta(m, t, 1e6)
caso("sin objetivo no dispara por tiempo (configuración por defecto)", not m.evaluar_instancias())

# 11. Vuelta al objetivo: ¿queda constancia de W tras la apertura? (criterio del plan)
m, t = monitor()
ingesta(m, t, 3.0)
m.evaluar_instancias()
ingesta(m, t, 0.5)
t[0] += 0.5
r = m.evaluar_instancias()
caso("la lectura tras abrir deja constancia de W frente al objetivo", any("W" in str(x.get("metricas_disparo") or x) for x in r),
     f"lectura sin salida: {r}")

# 12. Tiempo de respuesta > 2× objetivo de otro agente sin estado (R25 y 4.5 del Documento 0 no lo limitan al Curador)
m, t = monitor()
ingesta(m, t, 30.0, ag="AG-03")
caso("AG-03 con W = 30× objetivo abre (R25: cualquier agente sin estado)", bool(m.evaluar_instancias()))

print(f"\n{len(fallos)} fallo(s): {fallos}")
