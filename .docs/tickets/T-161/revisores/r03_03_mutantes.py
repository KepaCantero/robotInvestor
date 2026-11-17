"""QA r03 de T-161 · Mutantes propios del revisor (T01–T04) sobre `guias.py`: lo que la r03 promete de las lecciones y
que M01–M38 (`mutantes_t161.py`) pueden no tocar.

Uso, desde la raíz: python .docs/tickets/T-161/revisores/r03_03_mutantes.py <copia desechable con «qa29_» y «_mut» y `bloque_a/`
entero> [--scripts]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Con `--scripts`, a cada vivo se le
pasa además `r03_02_integracion.py` de esta ronda. Termina con 1 si alguno no aplica o vive.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa29_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
SCRIPTS = "--scripts" in sys.argv[2:]
AQUI = Path(__file__).resolve().parent
GU, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("guias", "orquestacion"))
PRUEBAS = ["tests/test_t161_guias.py", "tests/test_t161_r02.py", "tests/test_t161_r03.py", "tests/test_t158_guias.py", "tests/test_t126_pb26_pb48.py"]
MUTANTES = [
    ("T01", "una lección que no está en F6 se da igual (con lo que trae)", GU,
     "            if r is None:\n                continue\n", "            if r is None:\n                r = l\n"),
    ("T02", "el F0 no revisa las lecciones de F6", GU,
     "            self._revisar_lecciones(hoy, run_id, clave)   # T-161 r03", "            pass   # T-161 r03"),
    ("T03", "el tipo de la lección no se valida", GU, '    if leccion.get("tipo") not in TIPOS_LECCION:\n', "    if False:\n"),
    ("T04", "los controles reciben lecciones sin origen", GU,
     'if agente in AGENTES_DE_CONTROL and r.get("origen") != ORIGEN_DETERMINISTA:',
     'if agente in AGENTES_DE_CONTROL and r.get("origen") not in (ORIGEN_DETERMINISTA, None):'),
]


def pasar(cmd, cwd) -> int:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=3600).returncode


def main() -> int:
    ej = COPIA / "bloque_a" / "11_Ejecutor"
    sin_aplicar, vivos = [], []
    for mid, que, rel, viejo, nuevo in MUTANTES:
        f = COPIA / rel
        original = f.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} NO APLICA ({original.count(viejo)} apariciones): {que}", flush=True)
            sin_aplicar.append(mid)
            continue
        f.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        try:
            muerto = pasar([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], ej) != 0
            por_script = None
            if not muerto and SCRIPTS:
                por_script = pasar([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                                    str(AQUI / "r03_02_integracion.py")], ej) != 0
        finally:
            f.write_text(original, encoding="utf-8")
        extra = "" if por_script is None else (" · muere con r03_02" if por_script else " · vive también con r03_02")
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}{extra}", flush=True)
        if not muerto:
            vivos.append(mid)
    print(f"{len(MUTANTES) - len(vivos) - len(sin_aplicar)}/{len(MUTANTES)} muertos con las pruebas del ticket; "
          f"vivos: {', '.join(vivos) or 'ninguno'}; sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar or vivos else 0


if __name__ == "__main__":
    sys.exit(main())
