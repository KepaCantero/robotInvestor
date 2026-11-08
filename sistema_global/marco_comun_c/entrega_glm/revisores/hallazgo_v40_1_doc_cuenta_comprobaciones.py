"""Hallazgo 1 (V0.40, baja) — documentación: el resumen del Documento 0 dice que la batería nueva tiene
21 comprobaciones; la batería define y ejecuta 28 (y el propio Documento 0 da 28 en las secciones 5 y 7,
igual que LEEME.md, notas_briefing.md y la salida real). Cifra resumida errónea que no coincide con la
batería entregada.

Ejecutar desde la raíz de marcoC:  python3 hallazgo_v40_1_doc_cuenta_comprobaciones.py
Imprime FALLA si el defecto existe (la cifra del resumen no es la real) y OK si está corregido.
"""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
doc = (RAIZ / "entrega_glm" / "V0.40" / "Documento_0.md").read_text(encoding="utf-8")

# 1) lo que el RESUMEN («Qué entra en esta versión») dice de la batería nueva
linea = next(l for l in doc.splitlines() if "Batería nueva" in l and "pruebas_pantalla_f.py" in l)
dicho = int(re.search(r"\((\d+) comprobaciones\)", linea).group(1))

# 2) lo que la batería ejecuta de verdad (la última línea de su ejecución)
salida = subprocess.run([sys.executable, "-B", str(RAIZ / "pruebas" / "pruebas_pantalla_f.py")],
                        capture_output=True, text=True, timeout=120).stdout
real = int(re.search(r"(\d+) comprobaciones", salida).group(1))

print(f"Documento 0, resumen inicial: «{dicho} comprobaciones»")
print(f"pruebas/pruebas_pantalla_f.py ejecutada: {real} comprobaciones")
if dicho != real:
    print("FALLA: el resumen del Documento 0 no coincide con la batería entregada")
    sys.exit(1)
print("OK")
sys.exit(0)
