"""PC2-01 — el perfil inversor y la política de inversión personal no existen en SC-1.

La Constitución (§2, «Lo que hace el Broker Personal con el operador», puntos 2 y 3; §6, «Perfil inversor
y riesgo»; §14, Fase 1: «Broker Personal (perfil inversor)») pone el perfil inversor y de riesgo del
operador en SC-1, versionado, y liga a él la regla de subir y bajar el riesgo de una cartera (bajar al
momento; subir con segundo factor y espera); y una política de inversión personal que el Broker recuerda
antes de aceptar una orden que la contradiga.

El código: SC-1 es validador/mandatos.py y solo contiene mandatos por cartera (MANDATOS_DEFECTO con
version, benchmark_ref, horizonte_dias, apalancamiento_max, tamano_max_pct_cartera,
instrumentos_permitidos y exclusiones). Este guion demuestra que ningún módulo de validador/ ni la
configuración del Orquestador declara el perfil inversor (conocimientos, experiencia, situación,
objetivos, horizonte, caída tolerable, reacción ante pérdidas) ni la política de inversión personal.

Uso: python3 entrega_glm/V0.65/scripts/pc2_01_perfil_inversor.py   (desde la carpeta marcoC)
Imprime FALLA mientras el perfil no exista; OK cuando SC-1 lo declare.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]   # entrega_glm/V0.65/scripts/ -> marcoC
sys.path.insert(0, str(RAIZ / "validador"))

import orquestador
import parametros
from mandatos import CLAVES, MANDATOS_DEFECTO

mal = []

PALABRAS = ("perfil_inversor", "perfil_inversion", "politica_inversion",
            "conocimientos", "caida_tolerable", "horizonte_inversor")

# 1) las claves del mandato de SC-1 no contienen nada del perfil inversor
esperadas = {"version", "benchmark_ref", "horizonte_dias", "apalancamiento_max",
             "tamano_max_pct_cartera", "instrumentos_permitidos", "exclusiones"}
if set(CLAVES) != esperadas:
    mal.append(f"las claves de SC-1 cambiaron (¿se amplió con el perfil?): {sorted(CLAVES)}")
else:
    print(f"OK     SC-1 (mandatos.py): claves del mandato = {sorted(CLAVES)} (sin perfil inversor)")

# 2) ningún módulo de validador/ ni la configuración declara el perfil inversor
import re
hallados = []
for py in sorted((RAIZ / "validador").glob("*.py")):
    texto = py.read_text(encoding="utf-8")
    for p in PALABRAS:
        if re.search(p, texto, re.IGNORECASE):
            hallados.append(f"{py.name}:{p}")
src_orq = (RAIZ / "validador" / "orquestador.py").read_text(encoding="utf-8")
cfg = orquestador.CONFIG_DEFECTO
if hallados:
    mal.append(f"aparecen términos del perfil en: {hallados}")
else:
    print("OK     validador/: ningún módulo menciona el perfil inversor ni la política de inversión")
claves_cfg = set(cfg)
if any("perfil" in c or "inversion" in c for c in claves_cfg):
    mal.append(f"la configuración del Orquestador menciona perfil/inversión: {sorted(claves_cfg)}")
else:
    print(f"OK     CONFIG_DEFECTO: {len(claves_cfg)} claves, ninguna del perfil inversor")

# 3) la configuración de partida tampoco lo trae (parametros.py, versión versionada)
par = parametros.como_dict()
texto_par = repr(par)
if any(p in texto_par for p in PALABRAS):
    mal.append("parametros.py menciona términos del perfil inversor")
else:
    print("OK     parametros.py: sin perfil inversor ni política de inversión")

if mal:
    print("OK     el perfil inversor aparece en el código (divergencia resuelta):")
    for m in mal:
        print("       -", m)
    print("RESULTADO PC2-01: OK")
else:
    print("FALLA  SC-1 no declara el perfil inversor ni la política de inversión personal del operador")
    print("       (Constitución §2, §6 y §14 Fase 1: «Broker Personal (perfil inversor)»)")
    print("RESULTADO PC2-01: FALLA")
