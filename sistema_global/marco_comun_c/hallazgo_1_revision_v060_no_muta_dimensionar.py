"""Hallazgo 1 de la revisión V0.60 — la batería no demuestra «no muta la entrada» para dimensionar.

El Documento 0 (§1) y el LEEME prometen las CUATRO promesas (no lanza, no muta la entrada,
determinista, falla cerrado) «para los seis validadores», pero el bucle de dimensionado de
pruebas/pruebas_robustez_validadores.py no toma foto de las cuatro entradas ni compara después de
llamar (st de E solo tiene lanz/cant/forma/deter; no hay «muta»). En vigilancia, la foto cubre solo
los datos, no `ahora` (T1).

El validador está limpio: esta sonda demuestra que dimensionar no muta nada en 150 casos mutados.
Lo que FALLA es la cobertura: mientras la batería no incorpore la comprobación (regresión r01_…),
este guion termina en FALLA.

Ejecutar desde la raíz de marcoC:  python3 hallazgo_1_revision_v060_no_muta_dimensionar.py
"""
import copy
import math
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

from dimensionado import dimensionar
from control_f import POLITICA_DEFECTO
from pruebas_dimensionado import AHORA as AHORA_E, CART, SOL
from pruebas_robustez import _mutar_en_sitio


def _igual_nan(a, b):
    if isinstance(a, float) and isinstance(b, float):
        if math.isnan(a) and math.isnan(b):
            return True
        return a == b
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_igual_nan(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_igual_nan(x, y) for x, y in zip(a, b))
    try:
        return bool(a == b)
    except Exception:
        return a is b


def el_producto_esta_limpio():
    rng = random.Random(1)
    for i in range(150):
        entradas = {"sol": copy.deepcopy(SOL), "cart": copy.deepcopy(CART),
                    "pol": copy.deepcopy(POLITICA_DEFECTO), "ahora": AHORA_E}
        clave = ("sol", "cart", "pol", "ahora")[i % 4]
        entradas[clave], _ = _mutar_en_sitio(entradas[clave], rng)
        foto = copy.deepcopy(entradas)
        dimensionar(entradas["sol"], entradas["cart"], entradas["pol"], entradas["ahora"])
        for k in entradas:
            if not _igual_nan(foto[k], entradas[k]):
                return False, f"dimensionar SÍ mutó {k} (caso {i})"
    return True, "150 casos mutados: dimensionar no muta ninguna de sus cuatro entradas"


def la_bateria_comprueba_la_promesa():
    fuente = (RAIZ / "pruebas" / "pruebas_robustez_validadores.py").read_text(encoding="utf-8")
    ini = fuente.index("dimensionado.dimensionar")
    fin = fuente.index("vigilancia.vigilar")
    seccion_e = fuente[ini:fin]
    tiene_foto = "foto" in seccion_e or "_igual_nan" in seccion_e
    tiene_comprobacion = "no_muta" in seccion_e or '"muta"' in seccion_e or "'muta'" in seccion_e
    return tiene_foto and tiene_comprobacion, \
        f"sección E de la batería: foto/_igual_nan={tiene_foto}, comprobación de no-mutar={tiene_comprobacion}"


def main():
    ok_prod, det_prod = el_producto_esta_limpio()
    ok_bat, det_bat = la_bateria_comprueba_la_promesa()
    print(("OK   " if ok_prod else "FALLA") + "  producto: " + det_prod)
    print(("OK   " if ok_bat else "FALLA") + "  batería:  " + det_bat)
    if not ok_bat:
        print("\nHALLAZGO 1 (media): la batería no demuestra «no muta la entrada» para dimensionar "
              "(ni para `ahora`/T1 en vigilancia), aunque el Documento 0 §1 y el LEEME prometen las "
              "cuatro promesas para los seis validadores. Corrección: foto con _igual_nan de las "
              "cuatro entradas en el bucle de E (y de T1 en H) + regresión r01_… en la batería.")
    return 0 if (ok_prod and ok_bat) else 1


if __name__ == "__main__":
    sys.exit(main())
