"""QA r05 de T-102 (revisor nuevo, commit `bf7235b`) · Mutantes nuevos sobre las piezas de la r05 de `diseno_v6.py`.

Método de las rondas anteriores: copia `bloque_a/` de la raíz dada (sin `*.docx`, `*.png` ni cachés) a una carpeta temporal
por mutante (de TMPDIR), aplica UNA mutación textual a `bloque_a/diseno_v6.py` (que debe aparecer una sola vez) y ejecuta
`tests/test_t102_filtro.py` (con «completo», también `tests/test_t101_v6.py`). Un mutante «sobrevive» si las pruebas siguen en
verde. Los ids son R01… y no repiten los de `r04_13` (N01…N45) ni los de `r03_03` (Q…).

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r05_04_mutantes.py <raiz_de_una_copia> [n_paralelo] [ids|todos] [completo]
La raíz debe ser una copia completa (worktree o `cp -r`), nunca el árbol principal: el script no escribe en ella, pero así lo
pide el protocolo de la ronda. Sale con 1 si sobrevive alguno o alguno no aplica.
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
    ("R01", 'if unicodedata.category(ch) not in ("Cf", "Mn", "Me"))', "if True)", "no se quitan formato ni combinantes"),
    ("R02", 'not in ("Cf", "Mn", "Me"))', 'not in ("Cf",))', "solo se quita el formato, no las combinantes"),
    ("R03", r'mil|millones?|mill[oó]n|tercios?)")', r'mil|millones?|tercios?)")', "«millón» deja de ser cifra"),
    ("R04", r'mill[oó]n|tercios?)")', r'mill[oó]n)")', "«tercio» deja de ser cifra"),
    ("R05", r'rf"|\b{_UNO}\s+(?:sobre|entre|de\s+cada|contra|en)\s+{_UNO}\b"', r'rf"|\bqqqq\b"', "sin «uno contra uno»"),
    ("R06", r"(?:cuart|quint|sext|s[eé]ptim|octav|noven|d[eé]cim)", r"(?:cuart)", "solo «un cuarto»: sin quintos ni décimas"),
    ("R07", r'r"|\b(?:tercera|cuarta|quinta|sexta|s[eé]ptima|octava|novena|d[eé]cima)s?\s+partes?\b"', r'r"|\bqqqq\b"',
     "sin «una cuarta parte»"),
    ("R08", r'r"|\b(?:un|y)\s+medio\b|\bmedio\s+punto', r'r"|\bmedio\s+punto', "sin «y medio» ni «un medio»"),
    ("R09", r"(?<!primera\s)(?<!segunda\s)(?<!\ba\s)\bmitad\b", r"\bmitad\b", "«segunda mitad» y «a mitad» pasan a ser cifra"),
    ("R10", r"(?!\s+del?\s+(?:año|ciclo|", r"(?!\s+del?\s+(?:qqqq|ciclo|", "«mitad del año» pasa a ser cifra"),
    ("R11", r"\bmitad\b(?!", r"\bmitadqq\b(?!", "«la mitad de las ideas» deja de ser cifra"),
    ("R12", "if _MARCADOR_NUM.search(t) and _UNO_Y_MARCADOR.search(", "if False and _UNO_Y_MARCADOR.search(",
     "sin «una de cada {n_ideas}»"),
    ("R13", r'\s+(?:un[oa]?)\b", re.IGNORECASE)', r'\s+(?:qqqq)\b", re.IGNORECASE)', "sin «{n} contra uno»"),
    ("R14", "contra|a|en|/|%|-)?", "/|%)?", "dos marcadores con «contra», «a», «en» o «-» pasan"),
    ("R15", r"(?:veces\s+)?de\s+cada|contra|a|en|/", r"de\s+cada|contra|a|en|/", "«{n} veces de cada {m}» pasa"),
    ("R16", r'r"\bel\s+(?:doble|triple|cu[aá]druple)\b"', r'r"\bel\s+(?:qqqq)\b"', "«el doble» deja de ser cifra"),
    ("R17", '("PERCENT" in unicodedata.name(ch, "") or "PER MILLE" in unicodedata.name(ch, ""))', "False",
     "«٪» y «‰» de otras escrituras pasan"),
    ("R18", 'if re.search(r"\\b(?:n_ideas|n_tipos|n_apuestas)\\b|\\b(?:opp|tipo|n|candidatas):[A-Za-z0-9-]", libre):',
     "if False:", "el nombre de un marcador fuera de sus llaves pasa («〔n_ideas〕»)"),
    ("R19", '_SUFIJO.search(libre.lstrip(" \\t-•*"))', "_SUFIJO.search(libre)", "sin quitar la viñeta antes del sufijo"),
    ("R20", r"S\.p\.A|SpA|GmbH|LLC|", "", "sin «S.p.A.», «SpA», «GmbH» ni «LLC» en mayúscula"),
    ("R21", "Aktiengesellschaft|Co(?=\\.)|", "", "sin «Aktiengesellschaft» ni «Co.»"),
    ("R22", "ltd|limited|spa|gmbh|llc))", "ltd))", "sin «Limited», «Spa», «Gmbh», «Llc» sin distinguir mayúsculas"),
    ("R23", r'r"|(?<![\w&.-])[a-z][\w&-]{0,40}\s+(?:inc|corp|ltd|plc|co|llc|spa|ag|nv)\.(?!\w)")', ")",
     "sin sufijo en minúscula con punto («apple inc.»)"),
    ("R24", "Cada|Tod[oa]s?|Cualquier|", "", "«Cada ETF» y «Todos los ETF» vuelven a ser nombres"),
    ("R25", r"|(?<=\A)[A-Z][a-záéíóú]+(?:ar|er|ir))", ")", "el infinitivo al empezar vuelve a ser nombre"),
    ("R26", r"Ning[uú]n|Ninguna|Ciertos?|Ciertas?|Dichos?|Dichas?|Mismos?|Mismas?|Tal(?:es)?|", "",
     "«Ningún», «Dichos», «Tales» vuelven a ser nombres"),
    ("R27", r"[A-Z][\w&.-]{0,40}(?:\s+[A-Z][\w&.-]{0,40}){0,6}", r"[A-Z][\w&.-]*(?:\s+[A-Z][\w&.-]*){0,6}",
     "sin tope en las palabras del nombre (cuadrático, H-37)"),
    ("R28", '(?<![\\w&.-])(?!" + _NO_NOMBRE', '\\b(?!" + _NO_NOMBRE', "el nombre puede empezar tras «.», «-» o «&»"),
    ("R29", '(unicodedata.category(ch).startswith("L") and "LATIN" not in unicodedata.name(ch, ""))',
     'unicodedata.name(ch, "").startswith(("CYRILLIC", "GREEK"))', "solo griego y cirílico (cheroqui, armenio pasan)"),
    ("R30", '("SMALL CAPITAL", "REGIONAL INDICATOR", "MODIFIER LETTER")', '("SMALL CAPITAL",)',
     "los indicadores regionales y las letras modificadoras pasan"),
    ("R31", "if len(c) >= 3 and c[0].isupper() and c[1:].islower():", "if False:",
     "tras un vehículo, una palabra con mayúscula inicial vuelve a ser código («acciones de Europa»)"),
    ("R32", "if len(c) >= 3 and c[0].isupper()", "if len(c) >= 1 and c[0].isupper()",
     "tras un vehículo, «Ab» deja de ser código"),
    ("R33", "if not _hay_cifra(c)", "if True", "la instrucción vuelve a ofrecer siglas con cifras («G7»)"),
    ("R34", r"(?:inc|corp|ltd|plc|co|llc|spa|ag|nv)\.", r"(?:inc|corp|ltd|plc)\.", "sin «co.», «llc.», «spa.», «ag.», «nv.» en minúscula"),
    ("R35", r"\w*cient[oa]s|", "", "«doscientos», «trescientas» dejan de ser cifra"),
    ("R36", r"veinti\w+|", "", "«veintitrés» deja de ser cifra"),
    ("R37", r"dieci\w+|", "", "«dieciséis» deja de ser cifra"),
    ("R38", "(?:cero|dos|", "(?:dos|", "«cero» deja de ser cifra"),
    ("R39", 'r = frase_prohibida(g["termino"], perm, marcas) or texto_prohibido(', "r = texto_prohibido(",
     "el término del glosario no se filtra"),
    ("R40", "n_tipos += 1 if ops else 0", "n_tipos += 1", "{n_tipos} cuenta los tipos sin ideas"),
    ("R41", '"n_apuestas": str(paquete.get("apuestas_independientes", n_ideas))', '"n_apuestas": str(n_ideas)',
     "{n_apuestas} toma el número de ideas"),
    ("R42", 'red["frase_historial"] = _uno(red.get("frase_historial"), defecto["frase_historial"])',
     'red["frase_historial"] = _uno(red.get("frase_historial"), "")', "el historial vacío no toma su defecto"),
    ("R43", "return t2 if not reglas else (t2.strip() or por_defecto)", "return t2 if not reglas else t2.strip()",
     "un texto vacío no toma su defecto"),
    ("R44", 'rellenar(unicodedata.normalize("NFKC", salida), marcas)', "rellenar(salida, marcas)",
     "sin NFKC antes de rellenar («｛n_ideas｝» llega tal cual)"),
    ("R45", "if perm is not None and frase_prohibida(nombre, perm):", "if False:", "el nombre llano no se filtra"),
    ("R46", r'rf"\b{_NUM_LETRA}\b"', r'rf"\bqqqq\b"', "ningún número en letra suelto es cifra («setenta»)"),
    ("R47", r"década|sesión|jornada))", r"qqqq))", "«mitad de la década / sesión / jornada» pasa a ser cifra"),
    ("R48", r"|\bmedio\s+punto\b|\bmedia\s+docena\b", "", "«medio punto» y «media docena» dejan de ser cifra"),
]


def correr(m):
    mid, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r05_t102_{mid}_"))
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
            return mid, desc, f"ERROR (código {r.returncode})", (fallida or ult or r.stderr[-200:])[:200]
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
