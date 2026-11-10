"""PC2-07 — «methodology_version» de la §13 no existe; el versionado va por otros nombres.

La Constitución (§13, tabla de identificadores) manda: «Toda salida lleva methodology_version
(versionado semántico)».

El código: ningún esquema JSON ni módulo de validador/ tiene ese campo. El sistema versiona por otros
caminos, todos versionado semántico: version_esquema en cada mensaje (CT-G), version_politica en el
resultado_politica de CT-G-08, VERSION_REGLAS en F (F-0.3.0), version_config (CFG-0.11.0) y
VERSION_PARAMETROS, con la huella de cada decisión anotada. La función está cubierta de facto en lo
construido; el campo literal no existe, así que una salida nueva podría no identificar su método.

Uso: python3 entrega_glm/V0.65/scripts/pc2_07_methodology_version.py   (desde la carpeta marcoC)
Imprime FALLA mientras el campo no exista (o la Constitución no se enmiende); OK si aparece.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))

mal = []      # si algo aparece, la divergencia está resuelta
versiona = []  # lo que sí versiona

# 1) ningún esquema lleva methodology_version
for esq in sorted((RAIZ / "esquemas").glob("*.schema.json")):
    texto = esq.read_text(encoding="utf-8")
    if "methodology_version" in texto:
        mal.append(f"{esq.name} lleva methodology_version")
print("OK     esquemas/: ningún .schema.json lleva methodology_version")

# 2) ningún módulo del validador lo produce
for py in sorted((RAIZ / "validador").glob("*.py")):
    texto = py.read_text(encoding="utf-8")
    if "methodology_version" in texto:
        mal.append(f"validador/{py.name} lleva methodology_version")
print("OK     validador/: ningún módulo menciona methodology_version")

# 3) lo que sí versiona cada salida (la función está cubierta por otros nombres)
src_f = (RAIZ / "validador" / "control_f.py").read_text(encoding="utf-8")
if re.search(r'VERSION_REGLAS\s*=\s*"F-0\.\d\.\d"', src_f):
    versiona.append("control_f.py: VERSION_REGLAS (F-0.3.0)")
esq08 = json.loads((RAIZ / "esquemas" / "ct-g-08_0.3.0.schema.json").read_text(encoding="utf-8"))
txt08 = json.dumps(esq08)
if "version_politica" in txt08:
    versiona.append("ct-g-08 0.3.0: resultado_politica.version_politica")
src_orq = (RAIZ / "validador" / "orquestador.py").read_text(encoding="utf-8")
if re.search(r'"version_config":\s*"CFG-0\.\d+\.\d+"', src_orq):
    versiona.append("orquestador.py: version_config (CFG-0.11.0)")
import parametros
if hasattr(parametros, "VERSION_PARAMETROS"):
    versiona.append(f"parametros.py: VERSION_PARAMETROS ({parametros.VERSION_PARAMETROS})")
for v in versiona:
    print(f"INFO   lo que sí versiona: {v}")

if mal:
    print("OK     la divergencia está resuelta:")
    for m in mal:
        print("       -", m)
    print("RESULTADO PC2-07: OK")
else:
    print("FALLA  ningún contrato ni módulo lleva methodology_version (§13); el versionado real va por")
    print("       version_esquema, version_politica, VERSION_REGLAS, version_config y VERSION_PARAMETROS")
    print("RESULTADO PC2-07: FALLA")
