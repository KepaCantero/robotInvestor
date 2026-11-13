"""QA r04 de T-102 · Prototipo FUERA del producto: medir el coste de dos correcciones sobre el banco nuevo (`r04_01`) y las
sondas (`r04_02`), sin tocar `diseno_v6.py` (se envuelve `frase_prohibida` en memoria).

- P1 (CIFRA sin depender de la palabra de probabilidad): un número en letra de «dos» en adelante, una fracción o una forma
  de cuota («contra uno», «a uno», «porciento», «percent») quita la frase esté donde esté; «uno», «una», «medio» y «mitad»
  no cuentan solos. Un marcador numérico junto a «de», «contra» o «veces» también.
- P2 (vehículo): tras «fondo», «ETF», «REIT»…, una palabra en minúscula solo cuenta como ticker si no es una palabra del
  español (aquí, una lista corta de verbos y palabras frecuentes de los informes); una sigla de la lista tras un vehículo
  cuenta como ticker si es símbolo del universo.

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_06_prototipo.py <raiz_repo>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r04_01_banco_nuevo as B  # noqa: E402
import r04_02_sondas as S  # noqa: E402

NUM = (r"dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|dieci\w+|veinte|veinti\w+|treinta|"
       r"cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien|ciento|\w+cient[oa]s|mil|tercios?|cuartas?\s+partes|quintos?|"
       r"d[eé]cim[oa]s|cent[eé]simas|two|three|four|five|seven|nine|ten|seventy|eighty|ninety|hundred|percent")
P1 = re.compile(rf"\b(?:{NUM})\b|\bporciento\b|\b(?:contra|a|to)\s+(?:uno|una|one)\b|\bun\s+(?:tercio|quinto|cuarto)\b", re.I)
P1_MARC = re.compile(r"\{(?:n:[\w-]+|candidatas:[\w-]+|n_ideas|n_tipos|n_apuestas)\}\s*(?:veces\s+)?(?:de|contra)\s*\{", re.I)


def main():
    M, base, perm = B.preparar(sys.argv[1] if len(sys.argv) > 1 else ".")
    v6, marcas = M["v6"], base["marcas"]
    orig = v6.frase_prohibida
    universo = set(perm["series"]) | set(M["cargar_universo"](M["RUTA"])["simbolo"].astype(str))

    def proto(t, perm, marcas=None):
        r = orig(t, perm, marcas)
        libre = v6._MARCADOR.sub(" ", t)
        if r is None and (P1.search(libre) or P1_MARC.search(t)):
            return "CIFRA"
        if r is None:
            for m in v6._VEHICULO.finditer(libre):
                if m.group(1) in universo:
                    return "R21"
        return r
    for nombre, f in (("r04", orig), ("prototipo", proto)):
        v6.frase_prohibida = f
        opps = B.opp_por_tipo(base["res"])
        fp = [x for t, g, x in B.LEGITIMAS if g != B.AM and v6.limpiar(B.resolver(x, t, opps), perm, marcas)[1]]
        amb = [x for t, g, x in B.LEGITIMAS if g == B.AM and v6.limpiar(x, perm, marcas)[1]]
        fn13 = [x for g, x in B.PROHIBIDAS if g == B.R13 and not v6.limpiar(x, perm, marcas)[1]]
        fn21 = [x for g, x in B.PROHIBIDAS if g == B.R21 and not v6.limpiar(x, perm, marcas)[1]]
        sonda_medio = [x for x in S.LEGITIMAS["medio"] if v6.limpiar(x, perm, marcas)[1]]
        r13v = [x for x in S.PROHIBIDAS["r13_vecinas"] if not v6.limpiar(x, perm, marcas)[1]]
        print(f"{nombre:10} FP banco {len(fp)}/106 · ambiguas quitadas {len(amb)}/5 · FN r13 {len(fn13)}/37 · FN r21 {len(fn21)}/45 · "
              f"sonda «medio» quitadas {len(sonda_medio)}/9 · r13 vecinas que pasan {len(r13v)}/11")
        if nombre == "prototipo":
            print("   FP:", fp, "\n   FN r13:", fn13, "\n   r13 vecinas:", r13v)
    v6.frase_prohibida = orig


if __name__ == "__main__":
    main()
