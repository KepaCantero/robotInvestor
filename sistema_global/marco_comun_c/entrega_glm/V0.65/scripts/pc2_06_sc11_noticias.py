"""PC2-06 — SC-11 mínimo (Fase 1) y los lectores aislados de contenido externo no existen.

La Constitución (§3, SC-11; §14, Fase 1: «SC-11 mínimo»; D-26) manda una lectura aislada de noticias con
salida de esquema cerrado (evento, país, gravedad, divisas y activos afectados) que alimenta el registro
de riesgos geopolíticos; y (§3, «Lectores de contenido externo»; §12.4 y §12.5) agentes que leen web, PDF
o correo en entorno aislado, sin cartera ni credenciales, con esquema estricto, e inyección detectada como
incidente.

El código: no hay nada de SC-11, noticias ni lectores en el marco. Lo bloquea la decisión del operador
(P-24, fuentes de noticias, que espera a la ficha de restricciones P-05, según T-56): no es un defecto de
código sino una FALTA de la Fase 1 anotada para que la compuerta la tenga en cuenta.

Uso: python3 entrega_glm/V0.65/scripts/pc2_06_sc11_noticias.py   (desde la carpeta marcoC)
Imprime FALLA mientras no exista; OK cuando SC-11 o los lectores estén construidos.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))

mal = []

# Patrones concretos del servicio y del registro. Solo validador/: ahí viviría el servicio (el marco);
# la primera versión barria también las pruebas con palabras a secas («noticia», «lector») y daba un
# falso OK por el motivo que una prueba le pasa a H (pruebas_orquestador.py:529, «la tesis parece
# debilitada por una noticia») y por los «lectores» de los comentarios de pruebas_robustez_t03.py;
# el docstring de H-16 no dice «noticia» (corrección del hallazgo 1 de la revisión independiente).
PATRONES = (r"SC-11", r"sc11", r"riesgos_geopoliticos", r"lectores?_de_contenido", r"lecturas_aisladas")

hallados = []
for py in sorted((RAIZ / "validador").glob("*.py")):
    texto = py.read_text(encoding="utf-8")
    for p in PATRONES:
        if re.search(p, texto):
            hallados.append(f"validador/{py.name}: {p}")
            break

if hallados:
    mal.append(f"aparece SC-11/noticias/lectores en: {hallados}")
else:
    print("OK     validador/: nada de SC-11, lectores aislados ni registro de riesgos geopolíticos")

import orquestador
cfg = repr(orquestador.CONFIG_DEFECTO)
if re.search(r"geopolit|noticia", cfg, re.IGNORECASE):
    mal.append("la configuración ya lleva SC-11/riesgos geopolíticos")
else:
    print("OK     CONFIG_DEFECTO: sin SC-11 ni registro de riesgos geopolíticos")

if mal:
    print("OK     la divergencia está resuelta:")
    for m in mal:
        print("       -", m)
    print("RESULTADO PC2-06: OK")
else:
    print("FALLA  SC-11 mínimo (Fase 1) y los lectores aislados no existen; pendiente de P-24 (fuentes),")
    print("       que espera a la ficha de restricciones reales (P-05) — decisión del operador, T-56")
    print("RESULTADO PC2-06: FALLA")
