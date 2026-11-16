"""QA r02 de T-161 · Mutantes propios del revisor (S01–S11) sobre `guias.py` y `orquestacion.py`: lo que la r02 promete y
que M01–M26 (`mutantes_t161.py`) no tocan.

Uso, desde la raíz: python .docs/tickets/T-161/revisores/r02_03_mutantes.py <copia desechable con «qa29_» y «_mut» y `bloque_a/`
entero> [--scripts]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Con `--scripts`, a cada vivo se le
pasa además `r02_02_integracion.py` de esta ronda. Termina con 1 si alguno no aplica o vive.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa29_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
SCRIPTS = "--scripts" in sys.argv[2:]
AQUI = Path(__file__).resolve().parent
GU, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("guias", "orquestacion"))
PRUEBAS = ["tests/test_t161_guias.py", "tests/test_t161_r02.py", "tests/test_t158_guias.py", "tests/test_t126_pb26_pb48.py"]
MUTANTES = [
    ("S01", "la lección solo se revisa por su recomendación", GU,
     '"como_se_sabe": leccion.get("observacion", "")}', '"como_se_sabe": ""}'),
    ("S02", "sin MARCADO", GU, r'MARCADO = re.compile(r"<\s*/?\s*[a-z!][^>]*>|~~|\]\s*\(")', 'MARCADO = re.compile(r"(?!x)x")'),
    ("S03", "una redefinición ya no compromete la guía entera", GU,
     'COMPROMETEN = {"INYECCION", "INSTRUCCION", "MARCADO"}', 'COMPROMETEN = {"INYECCION", "MARCADO"}'),
    ("S04", "el enmascarado financiero tapa todo el texto", GU,
     't = FINANCIERO.sub(" termino financiero ", t)', 't = " termino financiero " if FINANCIERO.search(t) else t'),
    ("S05", "la longitud máxima solo en que_cambia", GU,
     'for campo in ("que_cambia", "donde_se_comprueba", "como_se_sabe"):   # T-161 r02', 'for campo in ("que_cambia",):   # T-161 r02'),
    ("S06", "IDIOMA quita las siglas aunque el texto esté en mayúsculas", GU,
     "if letras and sum(c.isupper() for c in letras) / len(letras) < 0.6:", "if True:"),
    ("S07", "la lección retenida deja una incidencia Menor", OR,
     'severidad="Material", run_id=run_id, conflicto=conflicto)', 'severidad="Menor", run_id=run_id, conflicto=conflicto)'),
    ("S08", "sin cifras como letras en los campos descriptivos", GU,
     "        for variante in _variantes(normal):\n", "        for variante in []:\n"),
    ("S09", "NIEGA sin «cero», «ningún» ni «nada»", GU, r'r"|cubiert\w* por|anterior|cero|ningun\w*|nada|', r'r"|cubiert\w* por|anterior|'),
    ("S10", "emojis permitidos", GU, 'SIMBOLOS_PERMITIDOS = set("€', 'SIMBOLOS_PERMITIDOS = set("🚫❌€'),
    ("S11", "la lección retenida se escribe igual (sin continue)", OR,
     '                                        severidad="Material", run_id=run_id, conflicto=conflicto)\n                continue\n',
     '                                        severidad="Material", run_id=run_id, conflicto=conflicto)\n'),
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
                                    str(AQUI / "r02_02_integracion.py")], ej) != 0
        finally:
            f.write_text(original, encoding="utf-8")
        extra = "" if por_script is None else (" · muere con r02_02" if por_script else " · vive también con r02_02")
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}{extra}", flush=True)
        if not muerto:
            vivos.append(mid)
    print(f"{len(MUTANTES) - len(vivos) - len(sin_aplicar)}/{len(MUTANTES)} muertos con las pruebas del ticket; "
          f"vivos: {', '.join(vivos) or 'ninguno'}; sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar or vivos else 0


if __name__ == "__main__":
    sys.exit(main())
