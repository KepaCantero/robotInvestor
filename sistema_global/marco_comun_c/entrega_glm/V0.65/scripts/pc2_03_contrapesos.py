"""PC2-03 — los contrapesos de la abstención (embudo visible y alarma de sequía) no existen.

La Constitución (§7, «Contrapesos de la abstención», RATIFICADO en D-22; P5) manda un embudo visible
semanal en N (cuántas oportunidades entran, en qué capa cae cada una y por qué) y una alarma de sequía a
60 días (P-17/D-27) cuando ninguna oportunidad llega a invertirse habiendo candidatos que pasaron el
análisis. El tercer contrapeso (seguimiento de lo descartado) es del bloque I, Fase 5.

El código: la consola (consola.panel) calcula integridad, datos, presupuesto, avisos, decisiones,
kill-switch, autonomía, reloj, diario y migración; ni el panel ni el Orquestador agregan el embudo ni
vigilan los 60 días.

Uso: python3 entrega_glm/V0.65/scripts/pc2_03_contrapesos.py   (desde la carpeta marcoC)
Imprime FALLA mientras no existan; OK cuando el embudo y la sequía aparezcan.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))

mal = []

# 1) las comprobaciones del panel no incluyen embudo ni sequía
src_consola = (RAIZ / "validador" / "consola.py").read_text(encoding="utf-8")
secciones = sorted(set(re.findall(r'add\(\s*"([a-z_]+)"', src_consola)))
print(f"INFO   comprobaciones del panel (add): {secciones}")
if any("embudo" in s or "sequia" in s for s in secciones):
    mal.append(f"el panel ya incluye: {secciones}")
else:
    print("OK     el panel no tiene embudo ni alarma de sequía")

# 2) ningún módulo del validador implementa el embudo o la sequía
hallados = []
for py in sorted((RAIZ / "validador").glob("*.py")):
    texto = py.read_text(encoding="utf-8")
    for patron in (r"embudo", r"sequ[ií]a", r"60.*d[ií]as.*invert", r"sin_invertir"):
        if re.search(patron, texto, re.IGNORECASE):
            hallados.append(f"{py.name}: {patron}")
if hallados:
    mal.append(f"aparece embudo/sequía en: {hallados}")
else:
    print("OK     validador/: ningún módulo implementa el embudo visible o la alarma de sequía")

# 3) el Orquestador no tiene configuración para la sequía (60 días, P-17/D-27)
import orquestador
cfg = orquestador.CONFIG_DEFECTO
claves = sorted(cfg)
if any("sequia" in c or "embudo" in c for c in claves):
    mal.append(f"la configuración ya lleva: {[c for c in claves if 'sequia' in c or 'embudo' in c]}")
else:
    print(f"OK     CONFIG_DEFECTO ({len(claves)} claves): sin temporizador de sequía ni umbrales de embudo")

if mal:
    print("OK     la divergencia está resuelta:")
    for m in mal:
        print("       -", m)
    print("RESULTADO PC2-03: OK")
else:
    print("FALLA  no hay embudo visible ni alarma de sequía (D-22: embudo semanal en N y aviso a 60 días)")
    print("RESULTADO PC2-03: FALLA")
