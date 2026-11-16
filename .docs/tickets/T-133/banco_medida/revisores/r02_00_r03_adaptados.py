"""T-133 QA r02 · Ejecuta un script de las QA de T-94 (r03_*) adaptado al banco 0.5.0, sin tocarlo.

En 0.5.0, `ejecutar_a` vuelve a calcular la huella de los datos y del universo que devuelve el titular y se detiene si no son
los prerregistrados (por defecto, los de ejemplo de A). Los titulares falsos de r03_04, r03_05 y r03_10 devuelven sus datos
de un temporal sin pasarlos con --datos, así que ahora se detienen: es el cambio de diseño declarado («o el titular usa
otros»). Para ver si lo demás del script sigue en verde, este adaptador:
- antes de cada `ejecutar_a`, llama una vez al titular falso en un temporal para saber qué datos devuelve;
- si la ejecución no da --datos/--universo, hace que `rutas_por_defecto` devuelva esos (como el fixture `datos_falsos`);
- si los da y no son los del titular falso (r03_10, punto 1: los de ejemplo de A explícitos), los cambia por los del titular
  (así «por defecto frente a la ruta explícita» se compara con los mismos datos); una copia con el mismo contenido no se toca;
- un nivel 0,80 (r03_05), que ya no se admite (H-08), pasa a 0,95: sigue siendo «otro nivel, otra variante».
Uso: .venv/bin/python -B r02_00_r03_adaptados.py <carpeta de banco_medida.py> <script r03_*.py> [argumentos del script]"""
import runpy
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
CARPETA = str(Path(sys.argv[1]).resolve())
SCRIPT = sys.argv[2]
sys.path.insert(0, CARPETA)
import banco_medida as bm

_original = bm.ejecutar_a
_defecto = bm.rutas_por_defecto
cambios = []


def ejecutar_a(a):
    try:
        with tempfile.TemporaryDirectory(prefix="r02_sonda_") as t:
            tit = bm.titular_a(a.desde, a.hasta, Path(t) / "titular", a.cliente, a.frecuencia, a.clases)
        d, u = Path(tit["datos"]), Path(tit["universo"])
    except Exception:   # noqa: BLE001 — un titular que falla a propósito: sin cambios
        return _original(a)
    if getattr(a, "nivel", None) == 0.8:   # r03_05: 0,80 ya no es un nivel admitido (H-08, cambio declarado)
        cambios.append("nivel 0.8 → 0.95")
        a.nivel = 0.95
    sims = bm._simbolos_del_universo(u)

    def otros_datos() -> bool:
        try:
            return bm.huella_datos(Path(a.datos), sims) != bm.huella_datos(d, sims)
        except bm.BancoError:   # sin los ficheros del titular falso: son otros
            return True
    if getattr(a, "datos", None) and otros_datos():
        cambios.append(f"--datos {Path(a.datos).name} → {d.name}")
        a.datos, a.universo = str(d), str(u)
    bm.rutas_por_defecto = lambda: (d, u)
    try:
        return _original(a)
    finally:
        bm.rutas_por_defecto = _defecto


bm.ejecutar_a = ejecutar_a
sys.argv = [SCRIPT, CARPETA, *sys.argv[3:]]
try:
    runpy.run_path(SCRIPT, run_name="__main__")
finally:
    if cambios:
        print(f"[adaptador] rutas cambiadas por las del titular falso: {sorted(set(cambios))}")
