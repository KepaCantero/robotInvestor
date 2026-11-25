"""QA r01 (Claude) de T-192: mutantes propios de lo esencial de PB-34 y PB-35.

Cada mutante se aplica en una copia temporal de bloque_a y se pasan las pruebas del ticket. Un mutante VIVO (las pruebas
siguen en verde) que cambia el comportamiento es un hallazgo. Uso, con la venv del repo y desde la raíz del worktree:
    python -I .docs/tickets/T-192/revisores/r01_mutantes_revisor.py [--hilos 3]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = Path("bloque_a/11_Ejecutor")
PRUEBAS = ["tests/test_t192_evaluacion.py"]
EV, SO = "bloque_a/evaluador.py", "bloque_a/sombra.py"
MUTANTES = [
    ("M01 FC-EVAL con resoluciones FALLIDA", EV,
     'validas = [(p, r) for p, r in filas if r is not None and r["fuga"] == "SUPERADA"]',
     'validas = [(p, r) for p, r in filas if r is not None]'),
    ("M02 la FALLIDA cita el CALC- de soporte", EV,
     '"calc_id": calc_id if r["fuga"] == "SUPERADA" else None', '"calc_id": calc_id'),
    ("M03 recálculo con la fecha de hoy (fuga en la corrección)", EV,
     'p["fecha_emision"], run_id)', 'as_of, run_id)'),
    ("M04 corrección sin recalcular las puntuaciones de referencia", EV,
     'puntos = {**r["puntuaciones"], "brier_ref": (pr - o) ** 2,', 'puntos = {**r["puntuaciones"], "brier_ref_x": (pr - o) ** 2,'),
    ("M05 corrección duplicada en cada C5", EV,
     'if not r.get("fuga_tasa_base") or p["prg_id"] in previas:', 'if not r.get("fuga_tasa_base"):'),
    ("M06 resueltos() no aplica las puntuaciones corregidas", EV,
     '"comprobacion_fuga": "SUPERADA", "puntuaciones": correccion["puntuaciones"]}', '"comprobacion_fuga": "SUPERADA"}'),
    ("M07 DM-HLN con el sentido invertido", SO,
     'dm = ev.diebold_mariano_hln(-ic_anterior, -ic_nueva)', 'dm = ev.diebold_mariano_hln(-ic_nueva, -ic_anterior)'),
    ("M08 sin filtro de entrega ENTREGADA", SO,
     'and ajuste["efecto_desde"] <= r["_fecha"] <= hasta and r.get("entrega") == "ENTREGADA"}',
     'and ajuste["efecto_desde"] <= r["_fecha"] <= hasta}'),
    ("M09 sin ventana de la sombra", SO,
     'and ajuste["efecto_desde"] <= r["_fecha"] <= hasta and r.get("entrega") == "ENTREGADA"}',
     'and r.get("entrega") == "ENTREGADA"}'),
    ("M10 acepta la sombra de otro AJU-", SO,
     'if sombra.get("aju_id") != ajuste["id"] or not par:', 'if not par:'),
    ("M11 ignora el sentido del pronóstico", SO,
     '* (1 if p["sentido"] == "POSITIVO" else -1)', '* 1'),
    ("M12 cierre antes de sombra_hasta", EV,
     'if not aju or not aju.get("sombra_hasta") or str(as_of)[:10] < aju["sombra_hasta"]:',
     'if not aju or not aju.get("sombra_hasta"):'),
    ("M13 umbral de p del DM ignorado", SO,
     'empeora = dm["p_unilateral"] is None or dm["p_unilateral"] < parametro(evaluador.cfg, "evaluacion.alfa_holm") or',
     'empeora = dm["p_unilateral"] is None or'),
    ("M14 muestra mínima nunca exigida", SO,
     'if len(medias) < parametro(evaluador.cfg, "evaluacion.min_calibrar"):', 'if len(medias) < 3:'),
]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=carpeta / EJ,
                          text=True, capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


def uno(m):
    nombre, ruta, antes, despues = m
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp)
        shutil.copytree(RAIZ / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        archivo = copia / EJ / ruta
        txt = archivo.read_text(encoding="utf-8")
        if txt.count(antes) != 1:
            return nombre, "NO APLICA (texto no único)"
        archivo.write_text(txt.replace(antes, despues), encoding="utf-8")
        r = correr(copia)
        return nombre, "MUERTO" if r.returncode else "VIVO"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hilos", type=int, default=3)
    a = ap.parse_args()
    with ThreadPoolExecutor(a.hilos) as ex:
        for nombre, estado in ex.map(uno, MUTANTES):
            print(f"{estado:6} {nombre}", flush=True)
