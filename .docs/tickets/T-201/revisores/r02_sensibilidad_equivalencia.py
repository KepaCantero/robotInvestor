"""QA r01 de T-201 (revisor): ¿normaliza de más `comparar.py`? Cambios a propósito en el lado nuevo de una equivalencia.

Uso: python r02_sensibilidad_equivalencia.py <carpeta de equivalencia.sh (t201_equivalencia.XXXX)> <comparar.py> <raiz_nuevo>
Toma los resultados de una ejecución de `equivalencia.sh` (r_base, r_nuevo, base/bloque_a), cambia en r_nuevo UN
valor de dominio (no una ruta ni una latencia) lanza `comparar.py` y lo deshace. Cada cambio tiene que dar DISTINTO (salida 1). Uno
que dé EQUIVALENTE es un punto ciego de la prueba de equivalencia. El testigo («liquidez») comprueba que el montaje detecta.
"""
import re
import subprocess
import sys
from pathlib import Path

EQ, COMPARAR = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
RAIZ_NUEVO = Path(sys.argv[3]) if len(sys.argv) > 3 else None   # raíz del paquete del lado nuevo (…/bloque_a), como la pasó equivalencia.sh

CAMBIOS = [  # (nombre, fichero relativo a r_nuevo, patrón, sustitución) — se cambia solo la primera aparición
    ("testigo: F3 liquidez", "estado/F3_registro_oportunidades.jsonl", r'"liquidez": "alta"', '"liquidez": "baja"'),
    ("F3 dimensión T «duracion» (entrada de HT-03)", "estado/F3_registro_oportunidades.jsonl", r'"duracion": 80', '"duracion": 10'),
    ("RC «duracion_sesiones» (resultado del Motor)", "estado/RC_registro_calculos.jsonl", r'"duracion_sesiones": (\d+)',
     '"duracion_sesiones": 1'),
    ("F4 «fecha_congelacion» (instante de dominio)", "estado/F4_registro_pronosticos.jsonl",
     r'"fecha_congelacion": "(\d{4}-\d{2}-\d{2})T(\d{2})', r'"fecha_congelacion": "\1T23'),
    ("F3 fecha con hora", "estado/F3_registro_oportunidades.jsonl", r'(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2})', r'\1T23:59:59'),
    ("F11 «_ts» del ciclo simulado", "estado/F11_registro_seguimientos.jsonl", r'"_ts": "(\d{4}-\d{2}-\d{2})T(\d{2})',
     r'"_ts": "\1T23'),
    ("03_peticion.out «timestamp» del acuse", "03_peticion.out", r'"timestamp": "(\d{4}-\d{2}-\d{2})T(\d{2})', r'"timestamp": "\1T23'),
]

ciegos = []
raiz_n = str(RAIZ_NUEVO) if RAIZ_NUEVO else str(EQ / "base" / "bloque_a")
for nombre, rel, pat, sus in CAMBIOS:
    # el cambio se hace en el propio r_nuevo (las rutas de sus ficheros nombran esa carpeta) y se deshace al acabar
    f = EQ / "r_nuevo" / rel
    original = f.read_bytes()
    texto = original.decode("utf-8")
    nuevo, n = re.subn(pat, sus, texto, count=1)
    if not n or nuevo == texto:
        print(f"  {nombre}: el patrón no aparece (caso no aplicable)")
        continue
    try:
        f.write_text(nuevo, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(COMPARAR), str(EQ / "r_base"), str(EQ / "r_nuevo"), str(EQ / "base" / "bloque_a"),
                            raiz_n], capture_output=True, text=True, check=False)
    finally:
        f.write_bytes(original)
    ver = "DISTINTO" if r.returncode else "EQUIVALENTE"
    print(f"  {'OK   ' if ver == 'DISTINTO' else 'CIEGO'} {nombre}: {ver}")
    if ver != "DISTINTO":
        ciegos.append(nombre)

print("puntos ciegos:", ciegos or "ninguno")
sys.exit(1 if ciegos else 0)
