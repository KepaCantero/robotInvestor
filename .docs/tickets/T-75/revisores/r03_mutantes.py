"""QA r03 de T-75 (V0.75): ¿la batería mata los mutantes que deshacen cada corrección de la r03?

Copia el marco a un directorio temporal, aplica una mutación cada vez y ejecuta pruebas/pruebas_embudo_sequia_t75.py.
Un mutante «vivo» es una corrección que ninguna prueba protege. No cambia nada del repositorio.
Uso (desde la raíz del repositorio): .venv/bin/python -I .docs/tickets/T-75/revisores/r03_mutantes.py [ruta del marco]
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else RAIZ / "sistema_global" / "marco_comun_c"

MUTANTES = {
    "H-09: la pantalla no anota el veto": ("validador/orquestador.py",
        "            self._anotar_veto_f(e, cf, control_f, ahora)   # T-75 (QA r02, H-09)", "            pass   # T-75 (QA r02, H-09)"),
    "H-10: propuesta() toma la última anotación a PROPUESTA": ("validador/contratos.py",
        'if x["hasta"] == "PROPUESTA" and x["desde"] != "PROPUESTA")', 'if x["hasta"] == "PROPUESTA")'),
    "H-11: la pantalla no fija el reloj": ("validador/orquestador.py",
        'no hay nada que aprobar", reloj_firme=True)', 'no hay nada que aprobar")'),
    "H-11: autorizar no fija el reloj": ("validador/orquestador.py",
        'return _no("O-06", "F vetó la propuesta", reloj_firme=True)', 'return _no("O-06", "F vetó la propuesta")'),
    "H-14: la edad desde el inicio adelantado": ("validador/orquestador.py",
        "if a - (ult or primero) < timedelta(days=dias):", "if a - ini < timedelta(days=dias):"),
    "H-01: un análisis nuevo no borra el veto como causa": ("validador/orquestador.py",
        '                        veto = None\n', '                        pass\n'),
}


def main():
    vivos = []
    for nombre, (fich, viejo, nuevo) in MUTANTES.items():
        with tempfile.TemporaryDirectory() as d:
            m = Path(d) / "marco"
            shutil.copytree(MARCO, m, ignore=shutil.ignore_patterns("__pycache__", "entrega_*"))
            f = m / fich
            texto = f.read_text(encoding="utf-8")
            if texto.count(viejo) != 1:
                print(f"NO APLICA  {nombre}: el texto aparece {texto.count(viejo)} veces")
                continue
            f.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", "pruebas/pruebas_embudo_sequia_t75.py"], cwd=m, capture_output=True, text=True, timeout=600)
            muerto = r.returncode != 0
            fallan = [ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith("FALLA") or ln.startswith("FAIL")]
            print(("MUERTO    " if muerto else "VIVO      "), nombre, "::", fallan[:4] if fallan else r.stdout.strip().splitlines()[-1:])
            if not muerto:
                vivos.append(nombre)
    print(f"\nvivos: {vivos}")


if __name__ == "__main__":
    main()
