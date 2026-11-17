"""T-171 · Mutantes de T-161 (M01–M55, de `.docs/tickets/T-161/mutantes_t161.py`, sin tocar ese script) y de T-171 (N01–N26) sobre
`guias.py`. T-171 cambió las líneas de M45, M46, M47 y M51: aquí van con la misma intención sobre las líneas nuevas (M45b, M46b,
M47b, M51b). Las pruebas son las de T-161 más `tests/test_t171_guias.py`.

Uso, desde la raíz: python .docs/tickets/T-171/mutantes_t171.py <copia desechable con «qa29_» y «_mut» y `bloque_a/` entero>
Termina con 1 si alguno no aplica o vive.
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
COPIA = Path(sys.argv[1]).resolve()
assert "qa29_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
_src = (RAIZ / ".docs/tickets/T-161/mutantes_t161.py").read_text(encoding="utf-8").split("\ndef main")[0]
_g: dict = {"__name__": "mutantes_t161", "sys": type("S", (), {"argv": ["x", str(COPIA)]})}
exec(_src.replace("COPIA = Path(sys.argv[1]).resolve()", "COPIA = None").replace("assert \"qa29_\"", "assert True or \"qa29_\""), _g)
GU = _g["GU"]
PRUEBAS = _g["PRUEBAS"] + ["tests/test_t171_guias.py"]
SUSTITUIDOS = {
    "M45": ("M45b", "r04 H-12 una orden de refuerzo sobre el núcleo se puede acotar",
            "if claro and nucleo and (acotado or REDUCE.search(a) or _otra_accion(a, (PRESENTA, REFUERZA))):", "if False:"),
    "M46": ("M46b", "r04 H-13 los verbos de presentar no eximen al núcleo",
            "if not claro and PRESENTA.match(a) and not (REDUCE.search(a) or (nucleo and _oculta(a))):", "if False:"),
    "M47": ("M47b", "r04 H-12 los verbos de presentar eximen aunque reduzcan",
            "if not claro and PRESENTA.match(a) and not (REDUCE.search(a) or (nucleo and _oculta(a))):",
            "if not claro and PRESENTA.match(a) and not (nucleo and _oculta(a)):"),
    "M51": ("M51b", "r04 H-13 la carencia se enmascara aunque la recomendación no refuerce",
            "and (refuerza or ENDURECE.search(rec)) \\", "and True \\"),
}
NUEVOS = [
    ("N01", "H-18 sin el alcance de calendario", "(not leccion and (ALCANCE_TIEMPO.search(t)", "(not leccion and (False"),
    ("N02", "H-18 sin el alcance de una parte de las opciones", "(directo and (ALCANCE_PARTE.search(t) or _PREFIJO.match(t)))",
     "(directo and False)"),
    ("N03", "H-18 el alcance de una parte acota aunque el control no sea el objeto directo",
     "directo = any(r in NUCLEO for p, r in CONTROLES if re.match(p, objeto))", "directo = True"),
    ("N04", "H-18 la recomendación de una lección también se acota", "acotado = bool(ACOTA.search(a) or (not leccion and",
     "acotado = bool(ACOTA.search(a) or (True and"),
    ("N05", "H-18 una segunda acción no quita el refuerzo", "REDUCE.search(a) or _otra_accion(a, (PRESENTA, REFUERZA))):",
     "REDUCE.search(a)):"),
    ("N06", "H-18 mostrar exime aunque oculte", "(nucleo and _oculta(a))", "False"),
    ("N07", "H-18 separar de un registro no oculta", "return bool(_SEPARA.search(a) or _FUERA.search(a) or",
     "return bool(_FUERA.search(a) or"),
    ("N08", "H-18 «fuera del…» no oculta", "return bool(_SEPARA.search(a) or _FUERA.search(a) or", "return bool(_SEPARA.search(a) or"),
    ("N09", "H-19 un plural tras «y» cuenta como otra acción", 'or len(w) < 2 or w.endswith("s"):', "or len(w) < 2:"),
    ("N10", "H-19 un determinante tras «y» cuenta como otra acción", "if w in _ABRE_NOMBRE or", "if False or"),
    ("N11", "H-18 mostrar y después cambiar enmascara el parámetro",
     "or RELAJA.search(a) or _otra_accion(a, (_VERBOS_DE_MOSTRAR,)))", "or RELAJA.search(a))"),
    ("N12", "H-18 «en blanco» no es una rebaja", r'r"|\ben blanco\b|\bsin (?:rellenar', r'r"|\bsin (?:rellenar'),
    ("N13", "H-18 excluir y retirar no son rebajas", r'r"|\bexclu[yi]\w*|\bexclusion\w*|\bretir[aeo]\w*|\bretirar\b")', 'r"")'),
    ("N14", "H-18 ENDURECE enmascara lo que se quita de un registro", r"(?![^.;,]*\b(?:del|de (?:la",
     r"(?!\x00[^.;,]*\b(?:del|de (?:la"),
    ("N15", "H-19 la carencia en pretérito no se reconoce", r'r"|\b(?:se|no se) (?:omiti(?:o|eron)', r'r"|\bxxxx (?:omiti(?:o|eron)'),
    ("N16", "H-18 una observación favorable también se enmascara", "or NEUTRO.search(obs) or FAVORABLE.search(obs))",
     "or NEUTRO.search(obs))"),
    ("N17", "H-19 la recomendación que extiende el control a todo no refuerza",
     "refuerza = _refuerza(rec, leccion=True) or bool(UNIVERSAL.search(rec)", "refuerza = _refuerza(rec, leccion=True) or bool(False"),
    ("N18", "H-19 el resultado de una sola raíz, a dos palabras como mucho", r"(?:raiz|fuente|origen)\b[^.;]*?\b(?:fallar",
     r"(?:raiz|fuente|origen) (?:\w+ ){0,2}?\b(?:fallar"),
    ("N19", "H-18 que acertaran con una sola raíz se enmascara", r"\b(?:fallar\w*|fallaron|fallo|fallaba\w*|fallid\w*",
     r"\b(?:acert\w*|fallar\w*|fallaron|fallo|fallaba\w*|fallid\w*"),
    ("N20", "H-19 «significativo» es una redefinición",
     r'INSTRUCCION = re.compile(r"\bsignific(?:a|an|ara|aran|aria|arian|ando|ado|ados|ada|adas|ar|o|aba|aban)\b|\bsignifique\w*"',
     r'INSTRUCCION = re.compile(r"\bsignifica\w*"'),
    ("N21", "H-19 «al final del informe» es un plazo", r'r"|\bal? final del? (?!" + _DET', r'r"|\bal? final del? (?!\x00" + _DET'),
    ("N22", "H-19 el peso de un componente en su índice no se enmascara", 'r"?" + _COMPONENTE + r" )?', 'r"?" + "zzz" + r" )?'),
    ("N23", "H-19 listar y enumerar no muestran", r'r"|lista|listar|liste|enumera|enumerar|enumere)\b")   # T-171',
     r'r")\b")   # T-171'),
    ("N25", "cierre H-02 sin clíticos, verbos de mostrar ni «responder» en la segunda acción",
     "extra = ((_VERBOS_DE_MOSTRAR,) if PRESENTA in permitidos else ()) + ((_RESPONDE,) if REFUERZA in permitidos else ())",
     "extra = ()"),
    ("N26", "cierre H-02 el clítico abre cualquier verbo", 'formas = {w, re.sub(', 'formas = {"cita", w, re.sub('),
    ("N24", "H-18 el objeto directo sin quitar los complementos de alcance de delante", 'ALCANCE_PARTE.sub(" ", a)))', "a))"),
]
MUTANTES = [SUSTITUIDOS.get(m[0], m) for m in _g["MUTANTES"]] + NUEVOS


def main() -> int:
    ej = COPIA / "bloque_a" / "11_Ejecutor"
    sin_aplicar, vivos = [], []
    solo = set(sys.argv[2:])
    for mid, que, viejo, nuevo, *ruta in MUTANTES:
        if solo and mid not in solo:
            continue
        f = COPIA / (ruta[0] if ruta else GU)
        original = f.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} NO APLICA ({original.count(viejo)} apariciones): {que}", flush=True)
            sin_aplicar.append(mid)
            continue
        f.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=ej,
                               capture_output=True, text=True, timeout=3600)
        finally:
            f.write_text(original, encoding="utf-8")
        muerto = r.returncode != 0
        fallo = next((x for x in r.stdout.splitlines() if x.startswith("FAILED")), "")[:140]
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}{' · ' + fallo if fallo else ''}", flush=True)
        if not muerto:
            vivos.append(mid)
    n = len(solo) if solo else len(MUTANTES)
    print(f"{n - len(vivos) - len(sin_aplicar)}/{n} muertos; vivos: {', '.join(vivos) or 'ninguno'}; "
          f"sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar or vivos else 0


if __name__ == "__main__":
    sys.exit(main())
