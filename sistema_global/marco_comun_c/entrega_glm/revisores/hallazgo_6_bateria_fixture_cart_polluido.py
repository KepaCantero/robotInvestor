"""Hallazgo 6 — pruebas_robustez.py (comprobación fija F-12): `cart_fx = {**CART}` es una copia
SUPERFICIAL y el `del cart_fx["tipos_cambio_eur"]["USD"]` borra la divisa del fixture COMPARTIDO
`CART` de `pruebas_control_f` (la copia solo llega al primer nivel).

Consecuencias que este script demuestra ejecutando la batería real: (1) al terminar `main()`, el
fixture `CART` queda sin USD para el resto del proceso; (2) el bloque CF construye su «informe base
válido» DESPUÉS con esa cartera, y el informe resulta VETADO por F-12 (con solo los controles F-01 y
F-12), de modo que mutaciones «de valor» de los números de la cartera (p. ej. capital_eur -> 1e308) no
producen ningún fallo en `validar_informe_f` — el recálculo reproducirá el mismo veto de F-12 — y
`CF_toda_mutacion_interna_da_al_menos_un_fallo` cae (~5 de cada 24 semillas); (3) una segunda
ejecución de `main()` en el mismo proceso lanza KeyError('USD').

Uso: python3 hallazgo_6_bateria_fixture_cart_polluido.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe y OK si está corregido (copia profunda: `copy.deepcopy(CART)`).
"""
import copy
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

import pruebas_control_f as pcf
import pruebas_robustez as pr
from control_f import validar_informe_f
from pruebas_orquestador import AHORA, nuevo, hasta

mal = []

# (1) una ejecución de la batería real y estado del fixture compartido al terminar
antes = copy.deepcopy(pcf.CART)
pr.SEMILLA = 20261107
with redirect_stdout(io.StringIO()):
    pr.main()
if pcf.CART != antes:
    mal.append(f"tras main() el fixture compartido CART quedó mutilado: "
               f"{antes['tipos_cambio_eur']} -> {pcf.CART['tipos_cambio_eur']}")

    # (2) consecuencia: el base del bloque CF (que la batería construye después) sale vetado
    o = nuevo(); hasta(o, "PROPUESTA")
    base_inf = pcf.informe_f(o)
    res = base_inf["resultado_politica"]["resultado"]
    if res != "APROBADO":
        mal.append(f"el «informe base válido» del bloque CF es {res} "
                   f"({base_inf['resultado_politica']['motivo']})")
        # (3) y con ese base hay mutaciones internas que el validador no ve
        m = copy.deepcopy(base_inf)
        m["payload"]["entradas"]["cartera"]["capital_eur"] = 1e308
        x = o.expedientes["EXP-0001"]
        ctx = {"ahora": AHORA, "expediente_id": "EXP-0001", "correlation_id": x["correlation_id"],
               "divisa_cotizacion": "USD", "propuesta": x["propuesta"], "cartera_destino": x["cartera_destino"],
               "politica": o.cfg["politica_f"], "contexto": o._contexto_de_informe("EXP-0001", m)}
        if validar_informe_f(m, ctx) == []:
            mal.append("mutar capital_eur en el informe no produce ningún fallo de validar_informe_f "
                       "(CF_toda_mutacion_interna_da_al_menos_un_fallo cae)")

# (4) la batería debe poder ejecutarse otra vez en el mismo proceso
try:
    with redirect_stdout(io.StringIO()):
        rc2 = pr.main()
    if rc2 != 0:
        mal.append("la segunda ejecución de main() en el mismo proceso no sale limpia")
except Exception as e:
    mal.append(f"la segunda ejecución de main() en el mismo proceso lanza {type(e).__name__}: {e}")

print("FALLA " + ("; ".join(mal)) if mal else "OK")
sys.exit(1 if mal else 0)
