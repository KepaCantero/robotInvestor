"""QA r04 de T-102 (revisor nuevo, ronda relanzada sobre `b36176a`) · Rendimiento de `limpiar` con textos degenerados (CA-9 y
CA-14: menos de 2 s en total y tiempo lineal).

Cada caso se mide a dos tamaños (n y 2n caracteres, aprox.). Si al doblar el tamaño el tiempo crece más de 3 veces y pasa de
0,2 s, se marca como no lineal. Los textos buscan cuantificadores sin tope en las expresiones de la regla: palabras con
mayúscula unidas por «.», «-» o «&» (`_SUFIJO`), números en letra, marcadores, llaves, invisibles, combinantes, mayúsculas
mezcladas y vehículos encadenados.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_12_rendimiento.py <raiz_repo> [n]
Sale con 1 si el total pasa de 2 s o algún caso no es lineal. No escribe en el repositorio.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

CASOS = {
    "mayus_punto": lambda n: "A." * (n // 2),
    "mayus_guion": lambda n: "Ab-" * (n // 3),
    "mayus_amp": lambda n: "Ab&" * (n // 3),
    "mayus_punto_final_inc": lambda n: "A." * (n // 2) + " Inc.",
    "capitalizadas_coma": lambda n: "Abc, " * (n // 5),
    "palabra_larga": lambda n: "a" * n,
    "palabra_larga_cient": lambda n: "cient" * (n // 5),
    "numeros_letra": lambda n: "probabilidad " + "setenta sobre " * (n // 14),
    "uno_de_cada": lambda n: "uno de cada " * (n // 12),
    "marcadores": lambda n: "{n_ideas}" * (n // 9),
    "marcadores_sobre": lambda n: "{n_ideas} sobre " * (n // 16),
    "llaves": lambda n: "{" * n,
    "invisibles": lambda n: "N\u200b" * (n // 2),
    "combinantes": lambda n: "N\u0332" * (n // 2),
    "mixto_mayus": lambda n: "AApl " * (n // 5),
    "vehiculos": lambda n: "ETF " * (n // 4),
    "dolar": lambda n: "$" * n,
    "espacios_y_salto": lambda n: " " * n + "\n" + " " * n,
    "puntos_espacio": lambda n: ". " * (n // 2),
    "griego": lambda n: "Α" * n,
    "cifras_unicode": lambda n: "⅔" * n,
    "sufijo_repetido": lambda n: "Apple Inc. " * (n // 11),
}


def main() -> int:
    raiz = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
    M = C.preparar(raiz)
    v6 = M["v6"]
    perm = v6.permitidos_r21(C.bloque())
    marcas = {"n_ideas": "3", "n_tipos": "1", "n_apuestas": "2"}
    total, malos = 0.0, []
    for k, gen in CASOS.items():
        ts = []
        for tam in (n, 2 * n):
            t = gen(tam)
            t0 = time.perf_counter()
            v6.limpiar(t, perm, marcas)
            ts.append(time.perf_counter() - t0)
        total += ts[0]
        no_lineal = ts[1] > 0.2 and ts[1] > 3 * max(ts[0], 1e-4)
        if no_lineal:
            malos.append(k)
        print(f"  {k:22} n={ts[0]:7.3f} s  2n={ts[1]:7.3f} s  {'NO LINEAL' if no_lineal else ''}")
    print(f"total (tamaño n={n}): {total:.2f} s; no lineales: {malos}")
    return 1 if total > 2 or malos else 0


if __name__ == "__main__":
    sys.exit(main())
