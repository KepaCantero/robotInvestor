"""QA r01 de T-201 (revisor): mutantes propios de los cambios no mecánicos.

Uso: python r04_mutantes.py <raíz del paquete …/bloque_a> <carpeta_tmp> [ID …]
Cada mutante se aplica a una copia del paquete en <carpeta_tmp> (nunca en el árbol de trabajo) y se lanzan las pruebas que
lo tendrían que matar. Vivo = ninguna prueba falla. Un vivo no equivalente es un hallazgo. Termina con 1 si hay vivos que no
estén marcados como equivalentes.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ, TMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
SOLO = set(sys.argv[3:])
T201 = ["tests/test_t201_cuotas.py"]
SEG = T201 + ["tests/test_v51.py", "tests/test_fase4_huecos.py"]
# test_fase3_goldens queda fuera: dos de sus pruebas test_ca7 fallan en una copia del paquete fuera del repositorio sin
# mutar nada (lo mostró el testigo M00); no tienen que ver con `ruta`
RUTAS = T201 + ["tests/test_v51.py", "tests/test_fase4_huecos.py", "tests/test_t65_hallazgos.py"]

# (id, fichero relativo a 11_Ejecutor/bloque_a, texto, sustitución, pruebas, equivalente: motivo o None)
MUTANTES = [
    # testigo: la copia sin mutar tiene que pasar las mismas pruebas (si no, las muertes no valen)
    ("M00", "configuracion.py", "    if valor is None:", "    if valor is None:", RUTAS, None),
    ("M01", "configuracion.py", "    if valor is None:", "    if not valor:", RUTAS, None),
    ("M02", "configuracion.py", "    if valor is None:   #", "    if False:   #", T201, None),
    ("M03", "seguimiento.py", 'if clase is not None else "AG-03"', 'if clase is not None else "AG-04"', T201, None),
    ("M04", "seguimiento.py", 'return AGENTE_CLASE.get(clase, "AG-03") if', 'return AGENTE_CLASE[clase] if', T201, None),
    ("M05", "seguimiento.py", '.get(estado, "PENDIENTE") if estado is not None else "PENDIENTE"',
     '.get(estado, "PENDIENTE") if estado is not None else "FALLADO"', SEG, None),
    ("M06", "seguimiento.py", '    resuelto = "CUMPLIDO" if (hito.get("resolucion") or {}).get("resultado_binario") else "FALLADO"\n    estado = hito.get("estado")',
     '    estado = hito.get("estado")\n    resuelto = ("CUMPLIDO" if (hito.get("resolucion") or {}).get("resultado_binario") else "FALLADO") if estado == "RESUELTO" else "-"',
     SEG, None),
    ("M07", "seguimiento.py", '    resuelto = "CUMPLIDO" if (hito.get("resolucion") or {}).get("resultado_binario") else "FALLADO"',
     '    resuelto = "FALLADO" if (hito.get("resolucion") or {}).get("resultado_binario") else "CUMPLIDO"', SEG, None),
    ("M08", "seguimiento.py", '"estado": _estado_hito(f4.get(h) or {})}', '"estado": "PENDIENTE"}', SEG, None),
    ("M09", "seguimiento.py", "enc = self.encargos().get(seg_id) if seg_id is not None else None",
     'enc = self.encargos().get(seg_id) if seg_id is not None else {"estado": "ACTIVO", "seg_id": None}', SEG, None),
    ("M10", "seguimiento.py", "enc = self.encargos().get(seg_id) if seg_id is not None else None",
     "enc = self.encargos().get(seg_id) if seg_id else None", SEG,
     "F11 nunca tiene una clave falsa: Almacen.estado se salta las entradas con `not k`"),
    ("M11", "motor/servicio.py", "alt = ALTERNATIVAS.get(ficha) if ficha is not None else None",
     'alt = ALTERNATIVAS.get(ficha) if ficha is not None else "ST-DESC-001"', T201,
     "inalcanzable: una ficha None se rechaza antes, en _error_de_forma"),
    ("M12", "motor/servicio.py", 'r["calc_id_cache"] = hit["calc_id"]', 'r["calc_id_cache"] = previo["calc_id"]', T201, None),
    ("M13", "motor/operaciones.py", "posicion_historica(diferencial, h)", "posicion_historica(dif, h)", T201, None),
    ("M14", "motor/operaciones.py", '"diferencial": diferencial, "unidad"', '"diferencial": dif, "unidad"', T201, None),
    ("M16", "motor/evaluacion.py", "n, k = len(arr), int(arr.sum())", "n, k = len(arr), int(sum(o))", T201, None),
    ("M17", "herramientas/ht03.py", "else:\n    import ht03_puntuaciones as _ref\n    from ht03_puntuaciones import *",
     "else:\n    from .referencia import ht03_puntuaciones as _ref\n    from .referencia.ht03_puntuaciones import *", T201, None),
    ("M18", "herramientas/ht09.py", "else:\n    import ht09_validador_g3 as _ref\n    from ht09_validador_g3 import *",
     "else:\n    import ht09_validador_g3 as _ref\n    from .referencia.ht09_validador_g3 import *", T201, None),
    ("M19", "herramientas/ht02.py", "    from .referencia.ht02_verificador_enlaces import *\nelse:",
     "    from .referencia.ht03_puntuaciones import *\nelse:", T201, None),
]

vivos = []
for mid, rel, texto, sus, pruebas, equivalente in MUTANTES:
    if SOLO and mid not in SOLO:
        continue
    copia = TMP / mid / "bloque_a"
    shutil.rmtree(copia.parent, ignore_errors=True)
    shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".mypy_cache"))
    f = copia / "11_Ejecutor" / "bloque_a" / rel
    fuente = f.read_text(encoding="utf-8")
    assert fuente.count(texto) == 1, (mid, fuente.count(texto))
    f.write_text(fuente.replace(texto, sus), encoding="utf-8")
    env = dict(os.environ, BLOQUE_A_RAIZ=str(copia), PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas], cwd=copia / "11_Ejecutor",
                       env=env, capture_output=True, text=True, check=False)
    muerto = r.returncode != 0
    linea = [x for x in r.stdout.splitlines() if " passed" in x or " failed" in x]
    falladas = [x.split(" - ")[0] for x in r.stdout.splitlines() if x.startswith("FAILED")]
    estado = "MUERTO" if muerto else ("VIVO (equivalente: " + equivalente + ")" if equivalente else "VIVO")
    if mid == "M00":
        estado = "TESTIGO " + ("FALLA: las muertes no valen" if muerto else "pasa")
    print(f"{mid} {rel}: {estado} · {linea[-1] if linea else r.stdout[-200:]} {falladas}", flush=True)
    if (mid == "M00" and muerto) or (mid != "M00" and not muerto and not equivalente):
        vivos.append(mid)
    shutil.rmtree(copia.parent, ignore_errors=True)
print("vivos no equivalentes:", vivos or "ninguno")
sys.exit(1 if vivos else 0)
