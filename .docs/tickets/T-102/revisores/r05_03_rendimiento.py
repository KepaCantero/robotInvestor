"""QA r05 de T-102 (revisor nuevo, commit `bf7235b`) · Rendimiento con textos degenerados nuevos.

Casos pensados contra las expresiones de la r05 (no repiten los de `r04_12`): un marcador numérico seguido de muchos espacios
(dos `\\s*` alrededor de un separador opcional), marcadores encadenados con separadores, «una de cada», «y medio», «mitad»,
nombres con mayúscula sin sufijo, minúsculas antes de un sufijo, vehículos encadenados, caracteres de formato y marcas
combinantes en masa, llaves, cifras Unicode y sus mezclas. Cada caso se mide con `limpiar` (todo el camino de un texto) a n y
2n caracteres; si el tiempo crece más de 3× al doblar, se marca como no lineal.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r05_03_rendimiento.py <raiz_repo> [n]
Sale con 1 si el total pasa de 2 s (CA-9) o algún caso no es lineal. No escribe en el repositorio.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

CASOS = {
    "marcador_espacios": lambda n: "{n_ideas}" + " " * n + "x",
    "marcador_espacios_guion": lambda n: "{n_ideas}" + " " * n + "-" + " " * n + "x",
    "marcadores_guion": lambda n: "{n_ideas} - " * (n // 12),
    "marcadores_contra": lambda n: "{n_tipos} contra " * (n // 16),
    "una_de_cada": lambda n: "una de cada " * (n // 12),
    "y_medio": lambda n: "y medio " * (n // 8),
    "mitad_segunda": lambda n: "segunda mitad " * (n // 14),
    "mayusculas_sin_sufijo": lambda n: "Abc " * (n // 4),
    "mayusculas_casi_sufijo": lambda n: ("Abc " * 6 + "In ") * (n // 27),
    "minusculas_casi_sufijo": lambda n: "abc inc " * (n // 8),
    "palabra_larga_mayuscula": lambda n: "A" + "b" * n + " Inc",
    "vehiculos": lambda n: "el ETF Abc " * (n // 11),
    "formato": lambda n: "N​" * (n // 2),
    "combinantes": lambda n: "a" + "́" * n,
    "llaves_abiertas": lambda n: "{" * n,
    "llaves_marcador": lambda n: "{n_ideas" * (n // 8),
    "numeros_unicode": lambda n: "Ⅶ" * n,
    "mayus_minus": lambda n: "ABc" * (n // 3),
    "puntos_mayusculas": lambda n: "A.b." * (n // 4),
    "dolares": lambda n: "$a " * (n // 3),
    "dieci": lambda n: "dieci" + "s" * n,
    "cientos": lambda n: "x" * n + "cientos",
}


def main() -> int:
    raiz = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 16000
    v6 = C.preparar(raiz)["v6"]
    perm = {"codigos": frozenset({"USD", "EUR", "ETF", "RV"}), "series": frozenset()}
    marcas = {"n_ideas": "3", "n_tipos": "2", "n_apuestas": "2"}
    total = 0.0
    malos = []
    for k, gen in CASOS.items():
        ts = []
        for m in (n, 2 * n):
            t = gen(m)
            t0 = time.perf_counter()
            v6.limpiar(t, perm, marcas)
            ts.append(time.perf_counter() - t0)
        total += ts[0]
        ratio = ts[1] / max(ts[0], 1e-4)
        mal = ratio > 3 and ts[1] > 0.05
        if mal:
            malos.append(k)
        print(f"  {k:24} n={ts[0]:7.3f} s  2n={ts[1]:7.3f} s  ×{ratio:5.1f}{'  NO LINEAL' if mal else ''}")
    print(f"total (n={n}): {total:.2f} s; no lineales: {malos or 'ninguno'}")
    return 1 if (total > 2 or malos) else 0


if __name__ == "__main__":
    sys.exit(main())
