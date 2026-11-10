"""QA r01 de T-92: plazo de CT-23 con solo fecha (O2) y números escritos a mano en la ruta determinista.

Uso: python -I r01_04_plazos_y_literales.py <ruta a bloque_a/11_Ejecutor>
"""
import re, sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ)); sys.path.insert(0, str(EJ / "tests"))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
import pandas as pd
from conftest import nuevo_bloque
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

# 1. Un plazo del Broker con solo la fecha («responde antes del 8-6») vence a las 00:00 de ese día, no al acabarlo
with tempfile.TemporaryDirectory() as d:
    b = nuevo_bloque(d, cargar_universo(RUTA_UNIVERSO_EJEMPLO))
    r = b.consultas.enviar({"tipo": "ACLARACION" if "ACLARACION" in bloque_a.interfaz_broker.TIPOS_CONSULTA
                            else bloque_a.interfaz_broker.TIPOS_CONSULTA[0], "modo": "NO_BLOQUEANTE",
                            "plazo_respuesta": "2026-06-08",
                            "preguntas": [{"texto": "¿Incluir X?", "supuesto_declarado": "no"}]}, "2026-06-05T10:00")
    vencidas = b.consultas.vencer("2026-06-08T09:00")
    informe("1  plazo «2026-06-08» sigue abierto el 8-6 a las 09:00", r["cns_id"] not in vencidas,
            f"vencidas={vencidas}")

# 2. Números escritos a mano en la ruta determinista (regla 2 de CLAUDE.md) que trae la integración
src = (EJ / "bloque_a" / "orquestacion.py").read_text(encoding="utf-8")
m = re.search(r'"favorable" if senal >= ([0-9.]+)', src)
informe("2  la dirección de la observación HT-01 (que decide si una pieza cuenta como raíz, A8) no usa un umbral literal",
        m is None, f"umbral literal {m.group(1)} en _observacion_ht01" if m else "")
print("fallos:", fallos)
