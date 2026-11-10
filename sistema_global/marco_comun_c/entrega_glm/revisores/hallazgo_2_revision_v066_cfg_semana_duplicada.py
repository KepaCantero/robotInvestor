# -*- coding: utf-8 -*-
"""Hallazgo 2 (revisión independiente V0.66) — el gemelo de la semana duplica la cfg de la batería.

`foto_semana` (pruebas/doradas.py) construye su Orquestador con un diccionario ESCRITO A MANO
({"nivel_autonomia": {"TACTICA": "L2", "TRADING": "L2"}}) en lugar de importar la cfg de la batería
(pruebas_semana.py), como sí hace foto_jornada con CFG de pruebas_jornada.py. No es posible importarla
porque `cfg` vive DENTRO de main() de pruebas_semana.py. Consecuencia: si una pieza futura cambia el
escenario de la semana (otra cartera, otro nivel), la batería de la semana se adapta, pero la foto dorada
sigue fijando el escenario VIEJO — y nada avisa: `pruebas_doradas.py` sigue en verde.

Demostración sobre una COPIA del árbol: se cambia la cfg de main() en pruebas_semana.py
(TRADING: L2 -> L3) y se comprueba que `pruebas_semana.py` se adapta (verde) mientras
`pruebas_doradas.py` sigue en verde con la foto entregada byte a byte igual: la foto ya no
documenta el recorrido de la batería y nadie se entera.

Uso: python3 hallazgo_2_revision_v066_cfg_semana_duplicada.py   (desde marcoC o desde scripts/)
Imprime FALLA si el defecto existe y OK si está corregido (p. ej. con CFG_SEMANA a nivel de módulo
importada por doradas.py, la batería dorada cae cuando el escenario cambia).
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def _raiz():
    """La raíz de marcoC: argv[1], esta carpeta si lo es, o el ascendente que tenga LEEME.md y pruebas/doradas.py."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    for candidato in [AQUI, *AQUI.parents]:
        if (candidato / "LEEME.md").is_file() and (candidato / "pruebas" / "doradas.py").is_file():
            return candidato
    raise SystemExit("No encuentro la raíz de marcoC (pásala como argv[1])")


RAIZ = _raiz()
IGNORA = shutil.ignore_patterns("__pycache__", "*.pyc", ".venv", ".git", "*.zip")

VIEJO = 'cfg = {"nivel_autonomia": {"TACTICA": "L2", "TRADING": "L2"}}'
NUEVO = 'cfg = {"nivel_autonomia": {"TACTICA": "L2", "TRADING": "L3"}}'


def corre(copia, bateria):
    r = subprocess.run([sys.executable, str(copia / "pruebas" / bateria)],
                       capture_output=True, text=True, cwd=str(copia))
    ult = [l for l in r.stdout.splitlines() if l.strip()]
    return r.returncode, (ult[-1] if ult else "(sin salida)")


def cfg_a_nivel_de_modulo(ruta):
    """¿La cfg de la semana es importable (constante de módulo) o vive dentro de main()?"""
    import ast
    arbol = ast.parse(ruta.read_text(encoding="utf-8"))
    for nodo in arbol.body:   # solo nivel de módulo
        if isinstance(nodo, ast.Assign) and any(getattr(t, "id", None) == "cfg" for t in nodo.targets):
            return True
    return False


def main():
    print("Hallazgo 2 (V0.66): el gemelo de la semana duplica la cfg de la batería:")
    importable = cfg_a_nivel_de_modulo(RAIZ / "pruebas" / "pruebas_semana.py")
    print(f"  ¿La cfg de pruebas_semana.py es una constante de módulo (importable)? {'sí' if importable else 'no (vive dentro de main())'}")
    doradas = (RAIZ / "pruebas" / "doradas.py").read_text(encoding="utf-8")
    duro = '{"nivel_autonomia": {"TACTICA": "L2", "TRADING": "L2"}}' in doradas
    print(f"  ¿doradas.py escribe a mano la cfg de la semana? {'sí' if duro else 'no'}")
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "marcoC"
        shutil.copytree(RAIZ, copia, ignore=IGNORA, symlinks=True)
        mod = copia / "pruebas" / "pruebas_semana.py"
        texto = mod.read_text(encoding="utf-8")
        if VIEJO not in texto:
            print("  NO APLICABLE (la cfg de la semana cambió de forma)")
            return 0
        mod.write_text(texto.replace(VIEJO, NUEVO, 1), encoding="utf-8")
        rc_s, u_s = corre(copia, "pruebas_semana.py")
        rc_d, u_d = corre(copia, "pruebas_doradas.py")
        print(f"  Con la cfg de la batería cambiada (TRADING L2->L3):")
        print(f"    pruebas_semana  : {'PASA' if rc_s == 0 else 'cae'} ({u_s})")
        print(f"    pruebas_doradas : {'PASA (la foto ya no documenta el recorrido de la batería y no avisa)' if rc_d == 0 else 'cae (avisa)'} ({u_d})")
        ciego = rc_s == 0 and rc_d == 0
    print("HALLAZGO 2:", "FALLA (la foto se queda fijando el escenario viejo sin avisar)" if ciego and not importable
          else "OK (la foto sigue al escenario de la batería)")
    return 1 if ciego and not importable else 0


if __name__ == "__main__":
    sys.exit(main())
