"""QA r01 de T-199 (revisor): ¿qué cuadrático deja de ver la prueba de T-165 con el cambio 2000→8000 ×6 a 1000→8000 ×16?

Mutante paramétrico (el de M08): G3-MET-13 vuelve a comprobar el prefijo cada B caracteres, coste lineal + cuadrático cuyo peso
crece al bajar B. Para cada B mide, sin carga y con la mínima de 3 intercaladas (para aislar el efecto de los tamaños y el tope,
no el del ruido), la razón con el protocolo de develop (2000→8000, tope 6) y con el de T-199 (1000→8000, tope 16).
Uso (desde bloque_a/11_Ejecutor/tests): PYTHONPATH=. python -I? no: ../../../.venv/bin/python ../../../.docs/tickets/T-199/revisores/r01_01_umbral_t165.py
"""
import sys

import test_t165_g3_met13 as T
from bloque_a.herramientas import ht09
from tiempo_cpu import minimos_intercalados

ORIG = ht09.comprobar_madurez


def con_reescaneo(bloque):
    def f(textos, madurez, sirve, fichas=()):
        textos = list(textos)
        for ruta, crudo, sev in textos:
            if isinstance(crudo, str) and bloque:
                for i in range(bloque, len(crudo), bloque):
                    ORIG([(ruta, crudo[:i], sev)], madurez, sirve, fichas)
        return ORIG(textos, madurez, sirve, fichas)
    return f


T._real("ST-DESC-001")
bloques = [int(x) for x in sys.argv[1:]] or [0, 40000, 20000, 12000, 8000, 5000]
for b in bloques:
    ht09.comprobar_madurez = con_reescaneo(b)
    fila = []
    for u in ("no está validado, ", "ST-DESC-001 implementado. ", "VOL GARCH 001 y ST-DESC-001; "):
        c2, l2 = minimos_intercalados(lambda u=u: T._real(u * 2000), lambda u=u: T._real(u * 8000))
        c1, _ = minimos_intercalados(lambda u=u: T._real(u * 1000), lambda: 0)
        rv, rn = l2 / max(c2, 0.02), l2 / max(c1, 0.02)
        fila.append(f"{u[:6]}: dev {rv:5.2f}{'*' if rv >= 6 else ' '} t199 {rn:6.2f}{'*' if rn >= 16 else ' '} (c1000 {c1:.3f} c2000 {c2:.3f} l {l2:.3f})")
    print(f"B={b or 'sin mutar'}: " + " | ".join(fila), flush=True)
ht09.comprobar_madurez = ORIG
print("* = la prueba falla (mutante muerto)")
