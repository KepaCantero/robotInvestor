"""Hallazgo 3 (T-33): la comprobación «config_tope_cero_es_valido_y_prohibe» de la batería es vacía.

En `pruebas/pruebas_libres_t33.py` (línea 78) la comprobación se escribe `h.chk("config_tope_cero_es_valido_y_prohibe", True)`:
asserta una literal, así que pasa siempre — pasaría también sin el cambio e incluso con el comportamiento que su nombre
promete roto. No es lo que dice: promete que el tope 0.0 se admite y que prohíbe, y no comprueba ninguna de las dos cosas
(la prohibición la prueba la comprobación SIGUIENTE, `con_tope_cero_cualquier_libre_lo_supera`; la validez del 0.0 no la
prueba ninguna). De las 35 comprobaciones declaradas, esta no suma evidencia.

Demostración diferencial: se simula en memoria una regresión plausible (`_valida_config` que rechaza el tope 0.0, p. ej.
por escribir `v > 0` donde debe ser `v >= 0`). Con ella, el comportamiento real se rompe (construir el Orquestador con
tope 0.0 lanza ValueError) y la batería entera moriría más adelante, pero la comprobación nombrada sigue dando True.

Ejecución: python3 hallazgo_t33_3_comprobacion_vacia.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe (la comprobación vacía está en la batería); OK si está corregida.
"""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

import orquestador   # noqa: E402
from orquestador import CONFIG_DEFECTO   # noqa: E402

BATERIA = AQUI / "pruebas" / "pruebas_libres_t33.py"
NOMBRE = "config_tope_cero_es_valido_y_prohibe"


def main():
    fuente = BATERIA.read_text(encoding="utf-8")
    linea = next((ln for ln in fuente.splitlines() if f'h.chk("{NOMBRE}"' in ln), None)
    print(f"  la batería dice: {linea.strip() if linea else '(no encontrada)'}")
    if linea is None:
        print("OK    la comprobación nombrada ya no es una literal")
        return 0
    vacua = re.fullmatch(r'\s*h\.chk\("[^"]+",\s*True\)\s*(#.*)?', linea) is not None

    # regresión simulada: la validación pasa a rechazar el tope 0.0
    original = orquestador._valida_config

    def estricta(c):
        if isinstance(c.get("libres_tope_dia_eur"), dict) and any(v == 0.0 for v in c["libres_tope_dia_eur"].values()):
            raise ValueError("regresión simulada: el tope 0.0 ya no se admite")
        return original(c)

    orquestador._valida_config = estricta
    try:
        roto = False
        try:
            cfg = {**CONFIG_DEFECTO, "perfiles_activos": ["C-DIV"], "clases_ratificadas": {"C-DIV": "Q"},
                   "apalancamiento_permitido": False,
                   "libres_tope_dia_eur": {"TRADING": 0.0, "TACTICA": 0.0, "LARGO_PLAZO": 0.0}}
            orquestador.Orquestador(cfg, {"festivos": [], "fines_de_semana": ["sáb", "dom"]})
            roto = False   # no hubo regresión (no debía pasar)
        except ValueError:
            roto = True   # el comportamiento que el nombre promete está roto
    finally:
        orquestador._valida_config = original

    # lo que la batería daría con esa regresión: la comprobación nombrada sigue siendo True
    print(f"  con la regresión simulada: construir con tope 0.0 lanza ValueError = {roto}; "
          f"la comprobación nombrada daría {True} igualmente")
    if vacua and roto:
        print(f"FALLA  «{NOMBRE}» es una comprobación vacía (h.chk(..., True)): no prueba ni la validez del tope 0.0 "
              f"ni su efecto; pasaría también sin el cambio y con la regresión simulada")
        return 1
    print("OK    la comprobación prueba algo real")
    return 0


if __name__ == "__main__":
    sys.exit(main())
