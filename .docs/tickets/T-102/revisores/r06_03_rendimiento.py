"""QA r06 de T-102 · Rendimiento con textos degenerados contra las expresiones nuevas de la r06.

Casos que no repiten los de `r04_12` ni `r05_03`: «un cuarto» ante muchos espacios (`_FIN_CANTIDAD`), «y medio» ante «plazo»
lejano, «el doble» con muchos espacios, «en mitad», letras sueltas en mayúscula separadas por espacios o blancos Braille con
una minúscula al final (`(?:[\\s_\\u2800][A-Z]){2,}`), vehículos encadenados con palabras corrientes (`_PALABRA_COMUN`),
mayúsculas con sufijo de sociedad en minúscula sin punto, letras con marcas combinantes españolas y ajenas, «Plc»/«Group»
repetidos, «la acción de» encadenado (`_UNITARIA` con la excepción nueva) y números ingleses. Cada caso se mide con `limpiar`
a n y 2n; si al doblar crece más de 3× (y pasa de 0,05 s), no es lineal. Además, un texto realista de 1 200 caracteres
(el tope de `lectura`) repetido 1 000 veces, para el coste por ciclo.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r06_03_rendimiento.py <raiz_repo> [n]
Sale con 1 si el total pasa de 2 s (CA-9) o algún caso no es lineal. No escribe en el repositorio.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r03_comun as C  # noqa: E402

CASOS = {
    "cuarto_espacios": lambda n: "un cuarto" + " " * n + "x",
    "cuarto_repetido": lambda n: "un cuarto " * (n // 10),
    "y_medio_lejos": lambda n: "y medio" + " " * n + "plazo",
    "doble_espacios": lambda n: "el doble" + " " * n + "de",
    "en_mitad": lambda n: "en mitad " * (n // 9),
    "letras_espacio_fin": lambda n: "A " * (n // 2) + "Ab",
    "letras_braille_fin": lambda n: "A⠀" * (n // 2) + "Ab",
    "letras_guion_bajo": lambda n: "A_" * (n // 2) + "a",
    "vehiculo_comun": lambda n: "el ETF es " * (n // 10),
    "fondo_fondo": lambda n: "fondo " * (n // 6),
    "sociedad_minuscula": lambda n: "Abc corporation " * (n // 16),
    "group_repetido": lambda n: "Abc Group " * (n // 10),
    "combinante_espanola": lambda n: "á" * (n // 2),
    "combinante_ajena": lambda n: "Ṇ" * (n // 2),
    "accion_de": lambda n: "la acción de los " * (n // 17),
    "ingles": lambda n: "seventy percent " * (n // 16),
    "mayusculas_iniciales": lambda n: "Nvda " * (n // 5),
    "un_ordinal": lambda n: "un quinto " * (n // 10),
}

REALISTA = ("El dólar fuerte es el factor común de la semana. {opp:OPP-2026-0001} depende de la FED y del BCE. "
            "A medio plazo, la tesis depende del crecimiento en EEUU; si el VIX se dispara, conviene revisar el riesgo. "
            "La duración (sensibilidad del precio de un bono a los tipos) es alta. Los emergentes (EM) sufren con el USD. ") * 3


def main() -> int:
    raiz = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 16000
    v6 = C.preparar(raiz)["v6"]
    perm = {"codigos": frozenset({"USD", "EUR", "ETF", "RV", "FED", "BCE", "EEUU", "VIX", "EM"}), "series": frozenset()}
    marcas = {"opp:OPP-2026-0001": "Monedas de Europa", "tipo:RV": "renta variable"}
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
        print(f"  {k:22} n={ts[0]:7.3f} s  2n={ts[1]:7.3f} s  ×{ratio:5.1f}{'  NO LINEAL' if mal else ''}")
    t0 = time.perf_counter()
    for _ in range(1000):
        salida, reglas = v6.limpiar(REALISTA, perm, marcas)
    real = time.perf_counter() - t0
    print(f"  realista: {len(REALISTA)} caracteres ×1000 en {real:.2f} s ({real:.2f} ms por texto); reglas {reglas}")
    print(f"total (n={n}): {total:.2f} s; no lineales: {malos or 'ninguno'}")
    return 1 if (total > 2 or malos or reglas) else 0


if __name__ == "__main__":
    sys.exit(main())
