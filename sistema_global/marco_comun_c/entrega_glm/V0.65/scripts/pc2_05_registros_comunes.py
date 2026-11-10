"""PC2-05 — el posicionamiento de grandes inversores falta en K y los registros comunes (D-23) no existen.

La Constitución (§2, ficha de K: «posicionamiento de grandes inversores (COT de la CFTC, 13F,
participaciones significativas de la CNMV, operaciones de directivos) con su fecha de publicación»;
§14, Fase 1: K «mínimo, divisas, con el COT de la CFTC»; §3, «Registros comunes» RATIFICADO en D-23)
manda cuatro registros comunes (análisis vigentes, riesgos geopolíticos, tendencias tecnológicas y
posicionamiento), con procedencia y consulta punto en el tiempo, que cualquier bloque consulta antes de
investigar.

El código: k_calidad.py no tiene nada de posicionamiento (COT, 13F, CNMV, directivos) y el Orquestador no
tiene almacenes de registros comunes (los expedientes/encargos/sellos cubren de facto parte de «análisis
vigentes» para su propia tubería, sin API común).

Uso: python3 entrega_glm/V0.65/scripts/pc2_05_registros_comunes.py   (desde la carpeta marcoC)
Imprime FALLA mientras no existan; OK cuando K lleve posicionamiento y haya registros comunes.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))

import k_calidad
import orquestador

mal = []

# 1) K no tiene posicionamiento (con mayúsculas para no confundir con «cotiza»)
src_k = (RAIZ / "validador" / "k_calidad.py").read_text(encoding="utf-8")
hallados = sorted({m.group(0) for m in re.finditer(r"COT|CFTC|13F|CNMV|posicionamiento|directiv", src_k)})
if hallados:
    mal.append(f"k_calidad.py ya menciona: {hallados}")
else:
    print("OK     k_calidad.py: nada de COT, CFTC, 13F, CNMV ni posicionamiento de directivos")

# 2) el Orquestador no tiene los registros comunes como almacenes consultables
src_o = (RAIZ / "validador" / "orquestador.py").read_text(encoding="utf-8")
falta = []
for termino in ("registros_comunes", "riesgos_geopoliticos", "tendencias_tecnologicas", "analisis_vigentes"):
    if not re.search(termino, src_o, re.IGNORECASE):
        falta.append(termino)
atributos = [a for a in vars(orquestador.Orquestador) if not a.startswith("__")]
if falta:
    print(f"OK     orquestador.py: sin registros comunes como almacenes ({', '.join(falta)})")
else:
    mal.append("orquestador.py ya declara los registros comunes")

# 3) la lista de atributos del Orquestador no incluye ningún registro común
sospechosos = [a for a in atributos if any(t in a for t in ("geopolit", "tendenc", "posicionamiento", "vigentes"))]
if sospechosos:
    mal.append(f"el Orquestador ya tiene atributos de registros comunes: {sospechosos}")
else:
    print(f"OK     Orquestador ({len(atributos)} atributos/métodos): sin riesgos geopolíticos, tendencias ni posicionamiento")

# 4) lo que sí hay: sellos y expedientes con sello y caducidad (parte de «análisis vigentes»)
print("INFO   lo que sí existe: expedientes con encargo, sello y caducidad en el Orquestador (O-03, O-11, T-46),")
print("       y K con procedencia y punto en el tiempo (Q-14, pit_*): «análisis vigentes» queda implícito en la tubería")

if mal:
    print("OK     la divergencia está resuelta:")
    for m in mal:
        print("       -", m)
    print("RESULTADO PC2-05: OK")
else:
    print("FALLA  K no lleva el posicionamiento de grandes inversores (COT de la CFTC, 13F, CNMV, directivos)")
    print("       y no existen los cuatro registros comunes de D-23 como almacenes consultables")
    print("RESULTADO PC2-05: FALLA")
