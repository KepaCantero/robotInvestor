"""QA r04 de T-102 · Rendimiento del filtro con textos degenerados (CA-9 y CA-14: «tiempo lineal», menos de 2 s en total).

Textos nuevos frente a los de las r01 a r03, pensados contra las expresiones de la r04 (`_SUFIJO` con «.» y «-» dentro de la
palabra, `_VEHICULO`, `_CIFRA_EN_LETRA`, la regla de mayúsculas mezcladas, la búsqueda de nombres Unicode por carácter) y la
escala de los que salen lentos.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_05_rendimiento.py <raiz_repo>
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

M = C.preparar(sys.argv[1] if len(sys.argv) > 1 else ".")
v6 = M["v6"]
PERM = v6.permitidos_r21(C.bloque())
MARCAS = {"n_ideas": "3", "n_tipos": "1", "n_apuestas": "3"}
N = 50000

CASOS = {
    "A_punto": lambda n: "A." * (n // 2),
    "A_guion": lambda n: "A-" * (n // 2),
    "Aa_punto": lambda n: "Aa." * (n // 3),
    "mayus_espacio": lambda n: "Aa " * (n // 3),
    "mayus_espacio_coma": lambda n: "Aa, " * (n // 4),
    "fondo": lambda n: "fondo " * (n // 6),
    "etf_min": lambda n: "ETF es " * (n // 7),
    "letra_sobre": lambda n: "tres sobre " * (n // 11),
    "prob_medio": lambda n: "probabilidad " * (n // 13) + "medio",
    "porcentaje": lambda n: "%" * n,
    "mixtas": lambda n: "ABc " * (n // 4),
    "griegas": lambda n: "α" * n,
    "llaves_unicode": lambda n: "❴" * n,
    "marcador_num": lambda n: "{n_ideas} " * (n // 10),
    "saltos": lambda n: "\n" * n,
    "espacio_salto": lambda n: " \n" * (n // 2),
    "dolar": lambda n: "$a" * (n // 2),
    "guion_bajo": lambda n: "_AB" * (n // 3),
    "NFKC_ancho": lambda n: "Ｎ" * n,
}


def medir(s):
    t0 = time.perf_counter()
    v6.limpiar(s, PERM, MARCAS)
    return time.perf_counter() - t0


if __name__ == "__main__":
    tiempos = {k: round(medir(f(N)), 3) for k, f in CASOS.items()}
    total = round(sum(tiempos.values()), 2)
    print(f"{N} caracteres por caso; total {total} s")
    for k, t in sorted(tiempos.items(), key=lambda x: -x[1]):
        print(f"  {k:20} {t:8.3f} s")
    lentos = [k for k, t in tiempos.items() if t > 0.5]
    for k in lentos:
        esc = {n: round(medir(CASOS[k](n)), 3) for n in (5000, 10000, 20000, 40000)}
        print(f"  escala {k}: {esc}")
    print(f"\n[{'FALLO' if total > 2 or lentos else 'OK'}] rendimiento: total {total} s; lentos (> 0,5 s): {lentos}")
