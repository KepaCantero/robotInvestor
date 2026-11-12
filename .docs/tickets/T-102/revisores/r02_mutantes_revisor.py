"""QA r02 de T-102 · Mutantes propios del revisor (distintos de los 44 de `../r02_mutantes.py`) contra las pruebas del filtro.

Mismo método: copia `bloque_a/` de la raíz indicada a una carpeta temporal por mutante, aplica UNA mutación textual a
`bloque_a/diseno_v6.py` y ejecuta `tests/test_t102_filtro.py` (con «completo», también `tests/test_t101_v6.py`). Un mutante
«sobrevive» si las pruebas siguen en verde: hay un comportamiento del filtro que ninguna prueba vigila.

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r02_mutantes_revisor.py <raiz_repo> [n_paralelo] [ids|todos] [completo]
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

# (id, texto original, texto mutado, qué rompe)
MUTANTES = [
    ("N01", "(?:(?:im)?probab(?!lemente)\\w*|", "(?:(?:im)?probab\\w*|", "«probablemente» cuenta como palabra de probabilidad"),
    ("N02", "_PCT = rf\"{_NUM}\\s*(?:%|por\\s+ciento)\"", "_PCT = rf\"{_NUM}\\s*(?:%)\"", "sin «por ciento»"),
    ("N03", "_PROB = r\"(?:probabilidad(?:es)?|posibilidad(?:es)?|chances?)\"", "_PROB = r\"(?:probabilidad(?:es)?|posibilidad(?:es)?)\"",
     "la regla directa sin «chance»"),
    ("N04", "|confianza|seguridad|certeza|opciones|riesgo\\s+de|que)\\b", "|confianza|seguridad|certeza|opciones|riesgo\\s+de)\\b",
     "sin «N % de que»"),
    ("N05", "|confianza|seguridad|certeza|opciones|riesgo\\s+de|que)\\b", "|confianza|seguridad|certeza|riesgo\\s+de|que)\\b",
     "sin «N % de opciones»"),
    ("N06", "r\"hasta\\s+(?:el\\s+|un\\s+)?$\"", "r\"(?:hasta\\s+|al\\s+|del\\s+)(?:el\\s+|un\\s+)?$\"",
     "el tope de un movimiento también con «al» y «del» (excepción más ancha)"),
    ("N07", "rf\"coeficiente)(?:\\s+{_FUNCION})*\\s*$\"", "rf\"coeficiente)(?:\\s+\\w+)*\\s*$\"",
     "el nivel con cualquier palabra entre medias (excepción más ancha)"),
    ("N08", "r\"^\\s*(?:de\\s+(?:las\\s+veces|los\\s+casos)|", "r\"^\\s*(?:de\\s+(?:las\\s+veces)|", "sin «de los casos»"),
    ("N09", "t[max(0, m.start() - 60):m.start()]", "t[max(0, m.start() - 15):m.start()]", "la mirada atrás de R13 a 15 caracteres"),
    ("N10", "r\"FI|FIL|SICAV|SOCIMI", "r\"SOCIMI", "sin «FI», «FIL» ni «SICAV»"),
    ("N11", "    if any(_es_instrumento(m, perm) for m in _ISIN.findall(t)):", "    if any(True for m in _ISIN.findall(t)):",
     "un ISIN de una serie del universo también cuenta"),
    ("N12", "_ISIN = re.compile(r\"\\b[A-Z]{2}[A-Z0-9]{9}\\d\\b\")", "_ISIN = re.compile(r\"\\b[A-Z]{2}\\d{10}\\b\")",
     "el ISIN sin letras en medio (ES0000012M85)"),
    ("N13", "    c = cod.lstrip(\"$\").rstrip(\".\")", "    c = cod.lstrip(\"$\")", "el punto final se queda en el código («EUR.»)"),
    ("N14", "    return any(ch.isupper() for ch in c) and len(c) >= 2", "    return any(ch.isupper() for ch in c) and len(c) >= 3",
     "un ticker de dos letras no es instrumento"),
    ("N15", "_INDICE = re.compile(r\"\\b(?:MSCI|FTSE|EURO\\s+STOXX|STOXX|", "_INDICE = re.compile(r\"\\b(?:MSCI|FTSE|STOXX|",
     "sin la familia EURO STOXX"),
    ("N16", "_CALIFICACION = re.compile(r\"(?:AAA|AA|A|BBB|BB|B|CCC|CC|C|D)[+-]?\")", "_CALIFICACION = re.compile(r\"(?:AAA|AA|A|BBB|BB|B|CCC|CC|C|D)\")",
     "una calificación con signo («BB-») es un instrumento"),
    ("N17", "|\\b\\d+\\s+de\\s+cada\\s+\\d+\\b\", re.IGNORECASE)", "\", re.IGNORECASE)", "duplicado de M06 (control)"),
    ("N18", "_ABREV = re.compile(r\"\\b(?:EE\\.\\s?UU|S\\.\\s?A|S\\.\\s?L|p\\.\\s?ej|etc|", "_ABREV = re.compile(r\"\\b(?:EE\\.\\s?UU|S\\.\\s?A|S\\.\\s?L|etc|",
     "«p. ej.» parte la frase"),
    ("N19", "|etc|Inc|Corp|Ltd|", "|etc|Ltd|", "«Inc.» y «Corp.» parten la frase"),
    ("N20", "_SEPARADOR = re.compile(r\"((?<=[.;!?…])\\s+|", "_SEPARADOR = re.compile(r\"((?<=[.;])\\s+|", "«!» y «?» no separan"),
    ("N21", "    return \"\".join(quedan).replace(_PUNTO, \".\").strip(), reglas", "    return \"\".join(quedan).strip(), reglas",
     "el punto protegido se queda en la salida"),
    ("N22", "    t = t.replace(_PUNTO, \".\")\n    if _r13(t):", "    if _r13(t):", "la frase se juzga con el punto protegido"),
    ("N23", "        r = frase_prohibida(str(g.get(\"termino\", \"\")), perm) or texto_prohibido(g.get(\"definicion\"), perm)",
     "        r = texto_prohibido(g.get(\"definicion\"), perm)", "el término del glosario sin filtro"),
    ("N24", "[Ss]egún|[Tt]ras|", "", "sin el corte en «según» y «tras»"),
    ("N25", "|hasta\\s+que|a\\s+menos\\s+que|siempre\\s+que|dado\\s+que|puesto\\s+que|ya\\s+que)\\b\"", ")\\b\"",
     "sin el corte en «hasta que», «a menos que», «ya que»…"),
    ("N26", "adquiri(?:r|d)|", "", "sin «adquirir»"),
    ("N27", "sobrepond(?:erar|era|ere)|", "", "sin «sobreponderar»"),
    ("N28", "infrapond(?:erar|era|ere)|", "", "sin «infraponderar»"),
    ("N29", "invertir\\s+en|invierte\\s+en|entrar\\s+en|", "invertir\\s+en|invierte\\s+en|", "sin «entrar en»"),
    ("N30", "(?:tomar|abrir|reforzar|reducir|cerrar|deshacer)\\s+", "(?:tomar|abrir)\\s+", "sin reforzar, reducir, cerrar ni deshacer"),
    ("N31", "posicionarse\\s+en|", "", "sin «posicionarse en»"),
    ("N32", "suscribir|liquidar|deshacerse\\s+de|", "suscribir|liquidar|", "sin «deshacerse de»"),
    ("N33", "    series |= {x.split(\"=\")[0] for x in simbolos if \"=\" in x}", "    pass", "«EURUSD» sin el «=X» deja de ser serie"),
    ("N34", "(re.search(r\"[=^\\-\\d/]\", x) or len(x) > 5)", "(re.search(r\"[=^\\-\\d/]\", x))", "un símbolo largo sin signos no es serie"),
    ("N35", "    t = re.sub(r\"\\bEE\\.\\s?UU\\.\", \"EEUU\", t)\n", "    t = re.sub(r\"\\bEE\\.\\s?UU\\.\", \"EE UU\", t)\n",
     "«EE. UU.» como dos códigos (control: EE y UU están en la lista)"),
    ("N36", "        return t2.strip() if len(t2.strip()) >= lim[\"texto_minimo\"] else None",
     "        return t2.strip() or None", "la integración sin el mínimo de texto útil"),
]


def correr(m):
    mid, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r02rev_t102_{mid}_"))
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
