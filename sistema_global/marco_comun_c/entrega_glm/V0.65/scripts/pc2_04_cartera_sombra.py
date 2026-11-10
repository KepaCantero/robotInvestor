"""PC2-04 — la cartera sombra pasiva (Fase 1) no existe.

La Constitución (§9.9, RATIFICADO en D-22/D-27; §14, Fase 1: «cartera sombra pasiva»; P17) manda que
desde el primer día corra en simulado un plan pasivo simple (un índice mundial) con los mismos aportes y
retiradas que la cartera real; I compara cada mes al robot con la sombra después de costes, y a los 24
meses se decide. Correr la sombra es de la Fase 1; la comparación mensual, de I (Fase 5).

El código: no hay nada de la sombra (plan, aportes, valoración ni comparación) en validador/ ni en las
pruebas ni en la configuración.

Uso: python3 entrega_glm/V0.65/scripts/pc2_04_cartera_sombra.py   (desde la carpeta marcoC)
Imprime FALLA mientras no exista; OK cuando la sombra esté construida.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))

mal = []

PATRONES = (r"sombra", r"indice_mundial", r"plan_pasivo", r"aportes")

# 1) ningún módulo del validador implementa la sombra
hallados = []
for py in sorted((RAIZ / "validador").glob("*.py")):
    texto = py.read_text(encoding="utf-8")
    for p in PATRONES:
        if re.search(p, texto, re.IGNORECASE):
            hallados.append(f"{py.name}: {p}")
if hallados:
    mal.append(f"aparece «sombra»/plan pasivo en: {hallados}")
else:
    print("OK     validador/: ningún módulo menciona la cartera sombra ni el plan pasivo")

# 2) tampoco la configuración ni los parámetros
import orquestador, parametros
cfg_txt = repr(orquestador.CONFIG_DEFECTO) + repr(parametros.como_dict())
if any(re.search(p, cfg_txt, re.IGNORECASE) for p in PATRONES):
    mal.append("la configuración o los parámetros ya llevan la sombra")
else:
    print("OK     CONFIG_DEFECTO y parámetros: sin plan sombra, índice mundial ni aportes")

# 3) ni las pruebas la ejercitan
hallados_p = []
for py in sorted((RAIZ / "pruebas").glob("*.py")):
    texto = py.read_text(encoding="utf-8")
    if re.search(r"sombra", texto, re.IGNORECASE):
        hallados_p.append(py.name)
if hallados_p:
    mal.append(f"las pruebas ya la ejercitan: {hallados_p}")
else:
    print("OK     pruebas/: ninguna batería menciona la cartera sombra")

if mal:
    print("OK     la divergencia está resuelta:")
    for m in mal:
        print("       -", m)
    print("RESULTADO PC2-04: OK")
else:
    print("FALLA  la cartera sombra pasiva (D-22/D-27, «desde el primer día», Fase 1) no existe en el marco")
    print("RESULTADO PC2-04: FALLA")
