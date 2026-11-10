"""PC2-02 — F no controla la liquidez, el coste, el margen ni la exposición compartida, y la política no distingue carteras.

La Constitución (§8, controles previos 2, 3 y 8; §7, mandato) exige: límites de concentración incluida la
exposición compartida a una divisa, emisor o factor; no comprar más del 5 % del volumen medio diario
(RATIFICADO en D-27) y contar el coste de entrar y salir; costes totales incluida la financiación y el
margen; y límites por libro y globales; el mandato lleva liquidez mínima.

El código: T-22 (RESUELTA en V0.36) cerró con «Fuera: liquidez, costes, margen y límites por cartera».
control_f.py no tiene ninguna regla de liquidez (F-01..F-23), la política es un único diccionario para las
tres carteras (orquestador.CONFIG_DEFECTO["politica_f"]) y mandatos.py no lleva liquidez mínima.

Uso: python3 entrega_glm/V0.65/scripts/pc2_02_liquidez_costes_f.py   (desde la carpeta marcoC)
Imprime FALLA mientras los controles no existan; OK cuando F y el mandato los tengan.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))

from control_f import CLAVES_CONTEXTO, POLITICA_DEFECTO
from mandatos import MANDATOS_DEFECTO
import orquestador

mal = []

# 1) la política de F no tiene ninguna clave de liquidez, coste, margen ni por cartera
temas = ("liquidez", "volumen", "coste", "margen", "adv")
con = sorted(k for k in POLITICA_DEFECTO if any(t in k for t in temas))
print(f"INFO   politica_f: {sorted(POLITICA_DEFECTO)}")
if con:
    mal.append(f"la política de F ya controla: {con}")
else:
    print("OK     POLITICA_DEFECTO: ninguna clave de liquidez, volumen, coste o margen")

politica_cfg = orquestador.CONFIG_DEFECTO["politica_f"]
if politica_cfg is not POLITICA_DEFECTO and politica_cfg != POLITICA_DEFECTO:
    mal.append("CONFIG_DEFECTO[politica_f] no es la política por defecto única")
else:
    print("OK     CONFIG_DEFECTO[politica_f]: un único diccionario para las tres carteras (sin límites por cartera)")

# 2) el código de F no menciona la liquidez ni el volumen
src_f = (RAIZ / "validador" / "control_f.py").read_text(encoding="utf-8")
hallados = sorted({m.group(0) for m in re.finditer(r"liquidez|volumen|volumen_medio|sin_impacto", src_f, re.IGNORECASE)})
if hallados:
    mal.append(f"control_f.py ya menciona: {hallados}")
else:
    print("OK     control_f.py: ninguna regla habla de liquidez o volumen (no hay dónde meter el 5 % de D-27)")

# 3) el contexto de F no tiene campo para el volumen del mercado
if any("volumen" in c or "liquidez" in c for c in CLAVES_CONTEXTO):
    mal.append(f"el contexto de F lleva: {sorted(CLAVES_CONTEXTO)}")
else:
    print(f"OK     CLAVES_CONTEXTO = {sorted(CLAVES_CONTEXTO)} (sin volumen del mercado)")

# 4) el mandato de SC-1 no lleva liquidez mínima
claves_mandato = set(MANDATOS_DEFECTO["TACTICA"])
if any("liquidez" in c for c in claves_mandato):
    mal.append("el mandato de SC-1 lleva liquidez mínima")
else:
    print(f"OK     mandatos.py: claves del mandato = {sorted(claves_mandato)} (sin liquidez mínima)")

# 5) F-07 concentra por activo; no hay regla de exposición por divisa, emisor o factor
reglas = sorted(set(re.findall(r"F-\d{2}", src_f)))
if any(f"F-{n:02d}" in reglas for n in range(24, 40)):
    mal.append(f"hay reglas nuevas de F: {reglas}")
else:
    print(f"OK     reglas de F en el código: {reglas[-6:]}... (F-24 en adelante no existe: sin divisa/emisor/factor)")

if mal:
    print("OK     la divergencia está resuelta:")
    for m in mal:
        print("       -", m)
    print("RESULTADO PC2-02: OK")
else:
    print("FALLA  F no controla la liquidez (5 % del ADV, D-27), el coste, el margen, la exposición")
    print("       compartida por divisa/emisor/factor y no tiene límites por cartera; el mandato no lleva")
    print("       liquidez mínima (T-22 lo dejó «Fuera» y nadie lo retomó)")
    print("RESULTADO PC2-02: FALLA")
