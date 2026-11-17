"""T-165 QA r02 · mutantes del revisor sobre el código de la r02, contra `tests/test_t165_g3_met13.py` (con `-x`).

- C13 y C17: los N13 y N17 de `r02_mutantes.py` del implementador con la expresión que de verdad está en `ht09.py` (las suyas no
  aparecen en el código: su script se para con un AssertionError en N13 y no ejecuta N13 a N22).
- X01 a X07: reglas de la r02 que ningún mutante del implementador toca.

Cada mutante cambia una expresión en una COPIA desechable de `bloque_a` (nunca en el árbol de trabajo) y la restaura.
«muerto» = alguna prueba falla. Uso, desde la raíz de la copia del repo:
    .venv/bin/python .docs/tickets/T-165/revisores/r02_03_mutantes.py --copia <copia con bloque_a> [--solo X01 C13]
"""
import argparse
import subprocess
import sys
from pathlib import Path

H = "bloque_a/11_Ejecutor/bloque_a/herramientas/ht09.py"
S = "bloque_a/11_Ejecutor/bloque_a/sintesis.py"

MUTANTES = [
    ("C13 sin «pendiente de» (N13 corregido)", H, ' or (w == "de" and previo in _NIEGA_DE)', ""),
    ("C17 sin doble negación (N17 corregido)", H, "return not any(x in _DOBLE for x, _ in tokens[:j])", "return True"),
    ("X01 sin «: no» detrás", H, " or bool(RE_NIEGA_DESPUES.match(t[m.end():m.end() + VENTANA]))", ""),
    ("X02 sin la excepción de personas", H, "if RE_PERSONA.match(t[m.end():m.end() + VENTANA]) or _ligada(", "if _ligada("),
    ("X03 sin el sustantivo ligado delante", H, "    return max(ligados) > max(metodos + fichas_antes + [-1])", "    return False"),
    ("X04 sin el éxito delante de «validación»", H,
     "exito = any(w in _EXITO_ANTES for w in antes) or bool(RE_EXITO_DESPUES.match(t[m.end():m.end() + VENTANA]))",
     "exito = bool(RE_EXITO_DESPUES.match(t[m.end():m.end() + VENTANA]))"),
    ("X05 una tabla no corta el párrafo anterior", H, "            anterior = [] if tabla else menciones",
     "            anterior = menciones"),
    ("X06 regla B nunca salta", H, 'elif not contexto and not (not ficha.startswith("?") and sirve(ficha)) and not declara[i]:',
     "elif False:"),
    ("X07 técnico por líneas (como la r01)", S,
     '[(f"informe_tecnico, línea {n}", parrafo, "BLOQUEO") for n, parrafo in _parrafos(texto)]',
     '[(f"informe_tecnico, línea {n}", ln, "BLOQUEO") for n, ln in enumerate(texto.splitlines(), start=1)]'),
]
PRUEBAS = ["tests/test_t165_g3_met13.py"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--copia", required=True)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--solo", nargs="*")
    a = ap.parse_args()
    copia = Path(a.copia).resolve()
    vivos = []
    for nombre, fich, viejo, nuevo in MUTANTES:
        if a.solo and nombre.split()[0] not in a.solo:
            continue
        p = copia / fich
        original = p.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{nombre:52s} NO APLICA ({original.count(viejo)} apariciones)", flush=True)
            continue
        try:
            p.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([a.python, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *PRUEBAS],
                               cwd=copia / "bloque_a/11_Ejecutor", capture_output=True, text=True, timeout=3600, check=False)
        finally:
            p.write_text(original, encoding="utf-8")
        muerto = r.returncode != 0
        primera = next((ln for ln in r.stdout.splitlines() if ln.startswith("FAILED")), "")[:150]
        print(f"{nombre:52s} {'muerto' if muerto else 'VIVO'}  {primera}", flush=True)
        if not muerto:
            vivos.append(nombre)
    print("vivos:", vivos or "ninguno")
    return 0


if __name__ == "__main__":
    sys.exit(main())
