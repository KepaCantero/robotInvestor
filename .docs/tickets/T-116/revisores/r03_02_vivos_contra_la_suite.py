"""QA r03 de T-116 · Los vivos de `r03_01` (Holm sin aplicar, certificado sin método, alerta de sobreconfianza, duplicados en
C1, credencial denegada con cambio de circunstancias, referencia inexistente en N0) contra MÁS pruebas de la suite que las
citadas: ¿los mata alguna prueba que el mapa no cita? Es informativo (para la deuda): el juicio de la fila se hace con las
citadas, como manda la regla del ticket.

Uso:  python r03_02_vivos_contra_la_suite.py <copia desechable de bloque_a/11_Ejecutor, con «qa2_mut» en la ruta>
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
ej = Path(sys.argv[1]).resolve()
assert "qa2_mut" in str(ej) and (ej / "bloque_a" / "almacen.py").exists()
spec = importlib.util.spec_from_file_location("r03_01", Path(__file__).with_name("r03_01_pb32_y_muestra.py"))
sys.argv = [sys.argv[0], str(ej), "--solo", "ninguno"]   # cargar el módulo sin ejecutar nada
r03 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r03)
MUT = {m[0]: m for m in r03.MUT}
EXTRA = {   # ficheros de la suite donde lo razonable es que hubiera una prueba que lo matase
    "P32e": ["tests/test_t53_evaluacion_y_almacen.py", "tests/test_t66_evaluacion.py", "tests/test_t65_hallazgos.py"],
    "P32f": ["tests/test_t53_evaluacion_y_almacen.py", "tests/test_t66_evaluacion.py", "tests/test_t65_hallazgos.py"],
    "P32h": ["tests/test_t87_datos.py", "tests/test_t66_evaluacion.py", "tests/test_t53_evaluacion_y_almacen.py"],
    "S33": ["tests/test_t53_evaluacion_y_almacen.py", "tests/test_t66_evaluacion.py", "tests/test_autocritica.py"],
    "S56": ["tests/test_v5.py", "tests/test_t53_seleccion_y_entrega.py"],
    "S60a": ["tests/test_v51.py", "tests/test_fase4_huecos.py"],
}
for mid, ficheros in EXTRA.items():
    _, pb, fich, desc, viejo, nuevo = MUT[mid]
    ruta = ej / fich
    original = ruta.read_text(encoding="utf-8")
    assert original.count(viejo) == 1, mid
    existentes = [f for f in ficheros if (ej / f).exists()]
    try:
        ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *existentes], cwd=ej, capture_output=True, text=True)
        ult = (r.stdout + r.stderr).strip().splitlines()[-1][:110]
        print(f"{mid} · {pb} · {'MUERTO' if r.returncode else 'VIVO  '} en {', '.join(Path(f).name for f in existentes)} · {desc} · {ult}", flush=True)
    finally:
        ruta.write_text(original, encoding="utf-8")
