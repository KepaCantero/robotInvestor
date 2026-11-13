"""QA r01 de T-102 · Mutantes del filtro R13/R21 frase a frase contra las baterías `tests/test_t102_filtro.py` y
`tests/test_t101_v6.py` (las pruebas del Sintetizador y del filtro).

Mismo método que `.docs/tickets/T-101/revisores/r01_mutantes.py`: copia `bloque_a/` de la raíz indicada a una carpeta temporal
por mutante, aplica UNA mutación textual a `bloque_a/diseno_v6.py` y ejecuta las baterías. Un mutante «sobrevive» si siguen en
verde: hay un comportamiento del ticket que ninguna prueba vigila.

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r01_mutantes.py <raiz_repo> [n_paralelo] [ids separados por comas] [completo]
Con «completo», las dos baterías enteras (131 pruebas); sin él, las 64 del filtro y del Sintetizador.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
PAR = int(sys.argv[2]) if len(sys.argv) > 2 else 3
SOLO = set(sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[3] != "todos" else None
COMPLETO = len(sys.argv) > 4 and sys.argv[4] == "completo"
PY = str(Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python")
D6 = "bloque_a/diseno_v6.py"
PRUEBAS = ["tests/test_t102_filtro.py", "tests/test_t101_v6.py", "-k",
           "filtro or sintetizador or v6_declara or una_frase or tarjeta_mala or se_quita or integracion or sin_codigos"]
if COMPLETO:
    PRUEBAS = PRUEBAS[:2]

# (id, texto original, texto mutado, qué rompe)
MUTANTES = [
    ("Q01", 're.compile(rf"\\b{_PROB}(?:\\s+de\\s+\\w+)?{_ENLACE}', 're.compile(rf"(?!x)x{_PROB}(?:\\s+de\\s+\\w+)?{_ENLACE}',
     "R13 sin «probabilidad + enlace + cifra»"),
    ("Q02", '_PROB = r"(?:probabilidad(?:es)?|posibilidad(?:es)?)"', '_PROB = r"(?:probabilidad(?:es)?)"', "R13 sin «posibilidad»"),
    ("Q03", '_ENLACE = r"(?::|=|', '_ENLACE = r"(?:=|', "R13 sin «:» como enlace"),
    ("Q04", '    if len(c) == 6 and c.isalpha() and c[:3] in perm["codigos"] and c[3:] in perm["codigos"]:\n        return False\n', "",
     "un par sin barra es un instrumento"),
    ("Q05", '    if c in perm["codigos"] or c in perm["series"]:', '    if c in perm["codigos"]:', "las series del universo son instrumentos"),
    ("Q06", "t[m.end():m.end() + 60]", "t[m.end():m.end() + 12]", "ventana de 12 caracteres tras el verbo"),
    ("Q07", r'''re.split(r"[,;:]|\by\s+(?:ya\s+)?(?:no\s+)?(?:se\s+)?\w+[ae]n?\b", ''', r'''re.split(r"[,;:]", ''',
     "la ventana no se corta en «y + verbo»"),
    ("Q08", '    return " ".join(quedan), reglas', '    return ("" if reglas else " ".join(quedan)), reglas',
     "se quita el texto entero, no la frase"),
    ("Q09", "        return t2 if not reglas else (t2.strip() or por_defecto)", "        return t2", "un texto vacío no toma su defecto"),
    ("Q10", "        return t2 if not reglas else (t2.strip() or por_defecto)", "        return t2 if not reglas else por_defecto",
     "un texto con una frase mala toma entero su defecto"),
    ("Q11", "    if quitadas:\n", "    if False:\n", "lo quitado de los textos llanos no se declara"),
    ("Q12", "    if descartados:\n", "    if False:\n", "lo quitado de la integración no se declara"),
    ("Q13", "    if any(_es_instrumento(m, perm) for m in _ISIN.findall(t)):", "    if False:", "sin la regla del ISIN"),
    ("Q14", "    if any(_es_instrumento(m, perm) for m in _ISIN.findall(t)):", "    if _ISIN.search(t):",
     "el ISIN se mira antes que las series del universo"),
    ("Q15", '    series |= {x.split("=")[0] for x in simbolos if "=" in x}', "    pass", "«EURUSD=X» no vale como «EURUSD»"),
    ("Q16", "invertir\\s+en|invierte\\s+en|", "", "sin «invertir en»"),
    ("Q17", "tomar\\s+posiciones?\\s+en|abrir\\s+(?:largos|cortos)\\s+en|", "", "sin «tomar posiciones» ni «abrir largos»"),
    ("Q18", '_CODIGO = re.compile(r"(?<![\\w&.^=-])\\$?([A-Z][A-Z0-9&.^=/-]{1,14})(?![\\w&])")',
     '_CODIGO = re.compile(r"(?<![\\w&.^=-])\\$?([A-Z][A-Z0-9&.^=/-]{1,14})(?![\\w&])", re.IGNORECASE)', "el código, sin mayúsculas"),
    ("Q19", '    red["glosario"] = [g for g in (red.get("glosario") or []) if isinstance(g, dict)\n'
            '                       and not (frase_prohibida(str(g.get("termino", "")), perm) or texto_prohibido(g.get("definicion"), perm))]',
     '    red["glosario"] = [g for g in (red.get("glosario") or []) if isinstance(g, dict)]', "el glosario sin filtro"),
    ("Q20", 'if isinstance(v, str) and (v2 := _uno(v, "").strip())}', 'if isinstance(v, str) and (v2 := v)}', "los motivos llanos sin filtro"),
    ("Q21", '    red["frase_historial"] = _uno(red.get("frase_historial"), defecto["frase_historial"])', "    pass",
     "la frase del historial sin filtro"),
    ("Q22", '        for k in ("por_que_llano", "que_puede_salir_mal_llano", "ambito_llano"):',
     '        for k in ("por_que_llano", "que_puede_salir_mal_llano"):', "el ámbito llano sin filtro"),
    ("Q23", '        for k in ("por_que_llano", "que_puede_salir_mal_llano", "ambito_llano"):',
     '        for k in ("por_que_llano", "ambito_llano"):', "el «qué puede salir mal» sin filtro"),
    ("Q24", '_FRASE = re.compile(r"(?<=[.;!?])\\s+")', '_FRASE = re.compile(r"(?<=[.!?])\\s+")', "«;» no separa frases"),
    ("Q25", "{_PCT}\\s+de\\s+(?:{_PROB}|confianza|opciones\\s+de\\s+\\w+)", "{_PCT}\\s+de\\s+(?:{_PROB}|opciones\\s+de\\s+\\w+)",
     "R13 sin «N % de confianza»"),
    ("Q26", '        re.compile(rf"\\bprobab\\w*\\s+(?:al|en\\s+un|en\\s+el)\\s+{_PCT}", re.IGNORECASE))',
     '        re.compile(r"(?!x)x"))', "R13 sin «probable al N %»"),
    ("Q27", "    perm = permitidos_r21(bloque)\n    if d:", "    perm = None\n    if d:", "el Sintetizador sin códigos permitidos"),
    ("Q28", '            t = _limpio("factores_dominantes", x.get("factor"))', '            t = x.get("factor")', "los factores sin filtro"),
    ("Q29", '    preg = [t for t in (_limpio("preguntas_sugeridas", x)', '    preg = [t for t in (x', "las preguntas sin filtro"),
    ("Q30", '    reg = _limpio("regimen_macro", d.get("regimen_macro"))', '    reg = d.get("regimen_macro")', "el régimen sin filtro"),
    ("Q31", '    nuevas = [f"Sintetizador: {t}"[:lim["limitacion"]] for t in (_limpio("limitaciones", x)',
     '    nuevas = [f"Sintetizador: {t}"[:lim["limitacion"]] for t in (x', "las limitaciones del Sintetizador sin filtro"),
    ("Q32", '    if any(r.search(t) for r in _R21) or sint._UNITARIA.search(t):', '    if any(r.search(t) for r in _R21[1:]) or sint._UNITARIA.search(t):',
     "sin el sufijo societario"),
    ("Q33", '    if any(r.search(t) for r in _R21) or sint._UNITARIA.search(t):', '    if any(r.search(t) for r in _R21[:1]) or sint._UNITARIA.search(t):',
     "sin la emisión con vencimiento"),
    ("Q34", '    if any(r.search(t) for r in _R21) or sint._UNITARIA.search(t):', '    if any(r.search(t) for r in _R21):', "sin `_UNITARIA`"),
    ("Q35", "|la\\s+compra\\s+de|la\\s+venta\\s+de)\\b", ")\\b", "sin «la compra de» ni «la venta de»"),
    ("Q36", '    c = cod.lstrip("$").rstrip(".")', '    c = cod.lstrip("$")', "«EE.» con el punto no es un código permitido"),
    ("Q37", '    red["frases_30s"] = [_uno(t, defecto["frases_30s"][i] if i < len(defecto["frases_30s"]) else "")',
     '    red["frases_30s"] = [_uno(t, "")', "una frase de 30 s vacía no toma su defecto"),
    ("Q38", '                x[k] = _uno(x[k], base.get(k, ""))', '                x[k] = _uno(x[k], "")', "una tarjeta vacía no toma su defecto"),
]


def correr(m):
    mid, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r01_t102_{mid}_"))
    try:
        shutil.copytree(RAIZ / "bloque_a", tmp / "bloque_a", ignore=shutil.ignore_patterns("*.docx", "*.png", "__pycache__", "estado_bloque_a"))
        p = tmp / "bloque_a" / "11_Ejecutor" / D6
        s = p.read_text(encoding="utf-8")
        if s.count(viejo) != 1:
            return mid, desc, f"NO APLICA ({s.count(viejo)} apariciones)", ""
        p.write_text(s.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=tmp / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=1500)
        ult = (r.stdout.strip().splitlines() or [""])[-1]
        fallida = next((ln for ln in r.stdout.splitlines() if ln.startswith("FAILED") or ln.startswith("ERROR")), "")
        if r.returncode not in (0, 1):
            return mid, desc, f"ERROR (código {r.returncode})", (fallida or ult)[:160]
        return mid, desc, "MATADO" if r.returncode else "SOBREVIVE", (fallida or ult)[:160]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    lista = [m for m in MUTANTES if not SOLO or m[0] in SOLO]
    with ThreadPoolExecutor(PAR) as ex:
        res = list(ex.map(correr, lista))
    for mid, desc, estado, det in res:
        print(f"[{estado}] {mid} {desc} · {det}", flush=True)
    vivos = [r[0] for r in res if r[2] == "SOBREVIVE"]
    print(f"\nMatados: {sum(1 for r in res if r[2] == 'MATADO')} · Sobreviven: {len(vivos)} {vivos} · "
          f"No aplican: {[r[0] for r in res if r[2].startswith('NO APLICA')]}")
