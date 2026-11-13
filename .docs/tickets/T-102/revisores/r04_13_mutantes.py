"""QA r04 de T-102 (revisor nuevo, ronda relanzada sobre `b36176a`) · Mutantes sobre las piezas de la r04 de `diseno_v6.py`.

Método de las r02 y r03: copia `bloque_a/` de la raíz dada (sin `*.docx`, `*.png` ni cachés) a una carpeta temporal por mutante,
aplica UNA mutación textual a `bloque_a/diseno_v6.py` (que debe aparecer una sola vez) y ejecuta `tests/test_t102_filtro.py`
(con «completo», también `tests/test_t101_v6.py`). Un mutante «sobrevive» si las pruebas siguen en verde: hay un
comportamiento de la r04 que ninguna prueba vigila. La carpeta temporal sale de TMPDIR (se recomienda el scratchpad).

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r04_13_mutantes.py <raiz_repo> [n_paralelo] [ids|todos] [completo]
Sale con 1 si sobrevive alguno o alguno no aplica. No escribe en el repositorio.
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
PRUEBAS = ["tests/test_t102_filtro.py"] + (["tests/test_t101_v6.py"] if COMPLETO else [])

# (id, texto original, texto mutado, qué deja de hacer)
MUTANTES = [
    ("N01", 'return any(unicodedata.category(ch).startswith("N") for ch in t)', "return any(ch.isdigit() for ch in t)",
     "solo dígitos (Nd): «⅔», «Ⅶ», «⁷⁰» dejan de ser cifra"),
    ("N02", 'if _hay_cifra(_MARCADOR.sub(" ", crudo)):', "if False:", "sin la mirada antes de NFKC («Ⅶ» pasa a «VII»)"),
    ("N03", 'r"escenarios?)\\b", re.IGNORECASE)', 'r"xqxq)\\b", re.IGNORECASE)', "«escenario» deja de ser palabra de probabilidad"),
    ("N04", "opciones\\s+de\\s+que|confianza|seguridad|certeza|", "opciones\\s+de\\s+que|",
     "«confianza», «seguridad» y «certeza» dejan de contar"),
    ("N05", 'r"tercios?|cuartos?|quintos?|d[eé]cimos?)")', 'r"tercios?)")', "sin cuartos, quintos ni décimos"),
    ("N06", "mil|millones?|medio|mitad|", "millones?|", "sin «mil», «medio» ni «mitad»"),
    ("N07", "\\bpor\\s+cien(?:to)?\\b|[%‰]|", "\\bpor\\s+cien(?:to)?\\b|", "«%» y «‰» en el texto libre dejan de ser cifra"),
    ("N08", "(?:sobre|entre|de\\s+cada|en)\\s+{_NUM_LETRA}", "(?:sobre|entre)\\s+{_NUM_LETRA}", "sin «de cada» ni «en»"),
    ("N09", 'rf"\\bpor\\s+cien(?:to)?\\b|[%‰]|', 'rf"[%‰]|', "«por cien(to)» deja de ser cifra"),
    ("N10", 'if re.search(rf"{_MARCADOR_NUM.pattern}\\s*(?:sobre|entre|de\\s+cada|/|%)?\\s*{_MARCADOR_NUM.pattern}|{_MARCADOR_NUM.pattern}\\s*%",',
     'if re.search(rf"{_MARCADOR_NUM.pattern}{_MARCADOR_NUM.pattern}",', "marcadores compuestos solo si van pegados"),
    ("N11", ' or any("CURLY BRACKET" in unicodedata.name(ch, "") for ch in libre)', "", "«❴ ❵» dejan de ser llaves"),
    ("N12", "if _PALABRA_PROB.search(libre) and (_NUMERO_LETRA.search(libre) or _MARCADOR_NUM.search(t)):",
     "if _PALABRA_PROB.search(libre) and _NUMERO_LETRA.search(libre):", "probabilidad con un marcador numérico pasa"),
    ("N13", "(?i:inc|corp|corporation|incorporated|ltd))\\.?(?!\\w)\")", "(?i:inc|corp|corporation|incorporated|ltd))(?![\\w.])\")",
     "el sufijo con punto deja de contar («Apple Inc.»)"),
    ("N14", 'r"\\b(?!(?:El|La|Los|Las|Un|Una|', 'r"\\b(?!(?:Un|Una|', "«Las SICAV», «El ETF» vuelven a ser sociedades"),
    ("N15", "UCITS\\s+ETF|ETF|", "UCITS\\s+ETF|", "«… ETF» deja de ser sufijo de fondo"),
    ("N16", "Fund|Trust|", "", "sin «Fund» ni «Trust»"),
    ("N17", "|(?i:inc|corp|corporation|incorporated|ltd))", ")", "sin el sufijo en minúscula"),
    ("N18", '"EEUU", libre).translate(_HOMOGLIFOS)', '"EEUU", libre)', "sin plegar homoglifos"),
    ("N19", 'return "R21"   # r04 (H-22): letras de otros alfabetos', 'pass   # r04 (H-22): letras de otros alfabetos',
     "letras griegas o cirílicas pasan"),
    ("N20", 'unicodedata.name(ch, "").startswith(("CYRILLIC", "GREEK"))', 'unicodedata.name(ch, "").startswith(("CYRILLIC",))',
     "las griegas pasan"),
    ("N21", '_CODIGO_PEGADO = re.compile(r"(?:[_=]|(?<=[a-záéíóúñ])[-.])([A-Z]{2,6})(?![\\w&])|\\$([A-Za-z]{1,6})\\b")',
     '_CODIGO_PEGADO = re.compile(r"(?!x)x()|(?!x)x()")', "sin códigos pegados ni «$ticker»"),
    ("N22", "(?:[_=]|(?<=[a-záéíóúñ])[-.])([A-Z]{2,6})", "(?:[_=])([A-Z]{2,6})", "sin códigos tras «-» o «.» después de minúscula"),
    ("N23", 'for m in re.finditer(r"\\b([A-Z]{2,})([a-z]+)\\b", libre):', 'for m in re.finditer(r"(?!x)x()()", libre):',
     "mayúsculas y minúsculas mezcladas («AApl») pasan"),
    ("N24", 'if not (m.group(2) == "s" and m.group(1) in perm["codigos"]):', "if True:", "los plurales «ETFs», «REITs» se quitan"),
    ("N25", "((c.islower() and ticker) or (len(c) == 1 and c.isupper())", "((False) or (len(c) == 1 and c.isupper())",
     "minúscula tras ETF/REIT pasa («el ETF qqq»)"),
    ("N26", "or (len(c) == 1 and c.isupper())", "or (False)", "una letra tras un vehículo pasa («el REIT O»)"),
    ("N27", 'm.group(0).lower().startswith("fondo") and len(c) <= 4)', "False)", "«el fondo vwrl» pasa"),
    ("N28", "return not _CONTEXTO_CALIFICACION.search(contexto)", "return False", "las calificaciones nunca son instrumento («Comprar AA»)"),
    ("N29", ' or re.fullmatch(r"X{0,3}(?:IX|IV|V?I{0,3})", c)', "", "«siglo XXI» se quita"),
    ("N30", "if perm is not None and frase_prohibida(nombre, perm):", "if False:", "el nombre llano sin filtrar (H-27)"),
    ("N31", 'quitadas.append("FORMATO")', "pass", "la entrada del glosario que no es texto no se declara"),
    ("N32", 'return (rellenar(unicodedata.normalize("NFKC", salida), marcas)', "return (rellenar(salida, marcas)",
     "«｛n_ideas｝» no se rellena (H-28)"),
    ("N33", 't = unicodedata.normalize("NFKC", crudo)', "t = crudo", "sin NFKC en la frase («ＮＶＤＡ»)"),
    ("N34", 'instr = INSTR_SINTESIS + " Siglas que puedes usar: " + ", ".join(sorted(perm["codigos"])) + "."',
     "instr = INSTR_SINTESIS", "la instrucción no lleva la lista de siglas (H-25)"),
    ("N35", '_SEPARADOR = re.compile(r"((?<=[.;!?…])\\s+|(?<![^\\S\\n])[^\\S\\n]*+\\n\\s*+)")',
     '_SEPARADOR = re.compile(r"((?<=[.;!?…])\\s+|\\s*\\n+\\s*)")', "separador cuadrático de la r03 (H-26)"),
    ("N36", 'r = frase_prohibida(g["termino"], perm, marcas) or texto_prohibido(g["definicion"], perm, marcas)',
     'r = texto_prohibido(g["definicion"], perm, marcas)', "el término del glosario no se filtra"),
    ("N37", 'if c in perm["codigos"] or c in perm["series"] or', 'if c in perm["codigos"] or', "las series del universo son instrumentos"),
    ("N38", 'if len(c) == 6 and c.isalpha() and c[:3] in perm["codigos"] and c[3:] in perm["codigos"]:', "if False:",
     "el par sin barra («EURUSD») es instrumento"),
    ("N39", "return any(ch.isupper() for ch in c) and len(c) >= 2", "return any(ch.isupper() for ch in c) and len(c) >= 3",
     "los códigos de dos letras dejan de ser instrumento"),
    ("N40", "n_tipos += 1 if ops else 0", "n_tipos += 1", "{n_tipos} cuenta tipos sin ideas"),
    ("N41", 'out[f"candidatas:{c}"] = str(d.get("candidatas_analizadas", 0))', 'out[f"candidatas:{c}"] = str(len(ops))',
     "{candidatas:X} = opciones"),
    ("N42", "if (c.islower() and c in _PALABRA_COMUN) or (c[0].islower() and len(c) > 5):",
     "if (c.islower() and c in _PALABRA_COMUN):", "palabras largas en minúscula tras un vehículo se quitan"),
    ("N43", "posibilidad(?:es)?|chances?|opciones\\s+de\\s+que|", "posibilidad(?:es)?|", "sin «chances» ni «opciones de que»"),
    ("N44", 'nombre = "esta idea"\n', 'nombre = nombre\n', "el nombre llano prohibido se conserva"),
    ("N45", "if any(m.startswith(\"$\") or _es_instrumento(m, perm, libre) for m in codigos)",
     "if any(_es_instrumento(m, perm, libre) for m in codigos)", "«$» delante de un código permitido pasa («$EUR»)"),
]


def correr(m):
    mid, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r04_t102_{mid}_"))
    try:
        shutil.copytree(RAIZ / "bloque_a", tmp / "bloque_a",
                        ignore=shutil.ignore_patterns("*.docx", "*.png", "__pycache__", "estado_bloque_a"))
        p = tmp / "bloque_a" / "11_Ejecutor" / D6
        s = p.read_text(encoding="utf-8")
        if s.count(viejo) != 1:
            return mid, desc, f"NO APLICA ({s.count(viejo)} apariciones)", ""
        p.write_text(s.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=tmp / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=2400)
        ult = (r.stdout.strip().splitlines() or [""])[-1]
        fallida = next((ln for ln in r.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))), "")
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
    noap = [r[0] for r in res if r[2].startswith("NO APLICA")]
    print(f"\nMatados: {sum(1 for r in res if r[2] == 'MATADO')}/{len(res)} · Sobreviven: {len(vivos)} {vivos} · "
          f"No aplican: {noap} · Errores: {[r[0] for r in res if r[2].startswith('ERROR')]}")
    sys.exit(1 if vivos or noap else 0)
