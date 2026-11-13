"""QA r06 de T-102 · Mutantes nuevos sobre las piezas de la r06 de `diseno_v6.py`.

Método de las rondas anteriores: copia `bloque_a/` de la raíz dada (sin `*.docx`, `*.png` ni cachés) a una carpeta temporal por
mutante, aplica UNA mutación textual a `bloque_a/diseno_v6.py` (que debe aparecer una sola vez) y ejecuta
`tests/test_t102_filtro.py` (con «completo», también `tests/test_t101_v6.py`). Un mutante «sobrevive» si las pruebas siguen en
verde. Los ids son S01… y no repiten los de `r05_04` (R…), `r04_13` (N…) ni `r03_03` (Q…).

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r06_04_mutantes.py <raiz_de_una_copia> [n_paralelo] [ids|todos] [completo]
La raíz debe ser una copia completa (worktree o `cp -r`), nunca el árbol principal. Sale con 1 si sobrevive alguno o no aplica.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    # CA-15: las cuentas las escribe el código
    ("S01", "    if _MARCADOR_NUM.search(t):   # r06", "    if False:   # r06", "los marcadores de cuenta vuelven a valer"),
    ("S02", '_MARCADOR_NUM = re.compile(r"\\{(?:(?:n|candidatas):[A-Za-z0-9-]{1,40}|n_ideas|n_tipos|n_apuestas)\\}")',
     '_MARCADOR_NUM = re.compile(r"\\{(?:n_ideas|n_tipos|n_apuestas)\\}")', "«{n:RV}» y «{candidatas:RV}» valen sin marcas"),
    ("S03", 'red["frases_30s"] = ([defecto["frases_30s"][0]] + [x for x in propias if x.strip()])',
     'red["frases_30s"] = ([x for x in propias if x.strip()])', "el código no escribe la frase de las cuentas"),
    ("S04", "[:len(defecto[\"frases_30s\"])]", "[:2]", "solo dos frases de 30 s"),
    ("S05", 'defecto["frases_30s"][i + 1] if i + 1 < len(defecto["frases_30s"]) else ""', '""',
     "una frase de 30 s quitada no toma su defecto"),
    ("S06", 'return f"De {cand} ideas de {tipo} analizadas,', 'return f"De {n} ideas de {tipo} analizadas,',
     "el motivo cuenta las opciones como candidatas"),
    ("S07", "analizadas, {n} {'pasó' if n == 1 else 'pasaron'}", "analizadas, {cand} {'pasó' if n == 1 else 'pasaron'}",
     "el motivo da las candidatas como las que pasan"),
    ("S08", "{'pasó' if n == 1 else 'pasaron'}", "{'pasaron'}", "sin singular"),
    ("S09", 'f"{_cuenta_motivo(paquete, k)} {v2}".strip()', 'f"{v2}".strip()', "el motivo sin la cuenta del código"),
    ("S10", 'cand = len(d.get("opciones") or []), int(d.get("candidatas_analizadas") or 0)',
     'cand = len(d.get("opciones") or []), len(d.get("opciones") or [])', "candidatas = opciones"),
    ("S11", "            if perm is not None and frase_prohibida(nombre, perm):\n                nombre = \"esta idea\"",
     "            pass", "un nombre llano prohibido se rellena tal cual"),
    # H-40: giros que no son cantidades
    ("S12", r"\by\s+(?-i:medio)\b(?!\s+plazo)", r"\by\s+(?-i:medio)\b", "«a corto y medio plazo» vuelve a ser cifra"),
    ("S13", r"\by\s+(?-i:medio)\b(?!\s+plazo)", r"\by\s+medio\b(?!\s+plazo)", "«Próximo y Medio» vuelve a ser cifra"),
    ("S14", r'r"|\bel\s+(?:doble|triple|cu[aá]druple)\b(?=\s+(?:de|que)\b|\s*[.,;:)]|\s*$)"',
     r'r"|\bel\s+(?:doble|triple|cu[aá]druple)\b"', "«el doble mandato» vuelve a ser cifra"),
    ("S15", r"(?<!\ba\s)(?<!\ben\s)\bmitad\b", r"(?<!\ba\s)\bmitad\b", "«en mitad de la tormenta» vuelve a ser cifra"),
    ("S16", r'_FIN_CANTIDAD = r"(?=\s+(?:del?|al|en|por|m[aá]s|menos|sobre)\b|\s*[.,;:)]|\s*$)"', '_FIN_CANTIDAD = r""',
     "«un quinto mes» vuelve a ser fracción"),
    ("S17", r"sobre)\b|\s*[.,;:)]|\s*$)", r"sobre)\b|\s*$)", "«un cuarto.» y «una décima,» dejan de ser fracción"),
    ("S18", r'|\bmedio\s+punto\b|\bmedia\s+docena\b"', r'"', "«medio punto» y «media docena» pasan"),
    # H-43: más números en letra
    ("S19", r'r"two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"',
     r'r"qqqq|"', "números ingleses pasan (salvo thousand y percent)"),
    ("S20", r'r"thousand|percent|fifty-fifty)")', r'r"qqqq)")', "«percent», «thousand» y «fifty-fifty» pasan"),
    ("S21", r"tercios?|docenas?|decenas?|centenar(?:es)?|", r"tercios?|", "«docena», «decena» y «centenar» pasan"),
    ("S22", r'r"mil[eé]sim[oa]s?|cent[eé]sim[oa]s?|\w+(?:ceav|teav|ntav)[oa]s?|"', r'r""', "«milésima», «centésima», «onceavo» pasan"),
    ("S23", r"millar(?:es)?|", "", "«millar» pasa"),
    ("S24", r"(?:sobre|entre|de\s+cada|contra|en|a|por\s+cada)", r"(?:sobre|entre|de\s+cada|contra|en)",
     "«uno a uno» y «una por cada una» pasan"),
    # H-44: sufijos y tickers
    ("S25", r"LLC|KGaA|Oyj|Bhd|Group|Holdings?|", r"LLC|KGaA|Oyj|Bhd|", "«Group» y «Holding» pasan"),
    ("S26", r'_SUF_FONDO = r"(?:Fund|Trust|UCITS\s+ETF|ETF|ETC|ETP)\.?(?!\w)"', r'_SUF_FONDO = r"(?:Fund|Trust|UCITS\s+ETF|ETF)\.?(?!\w)"',
     "fondos con «ETC» o «ETP» pasan"),
    ("S27", r'_SUFIJO = re.compile(rf"(?!{_DETERMINANTE}\b){_NOMBRE}{_SUF_SOCIEDAD}"',
     r'_SUFIJO = re.compile(rf"(?!{_DETERMINANTE}\b)(?!(?<=\A)[A-Z][a-záéíóú]+(?:ar|er|ir)\b){_NOMBRE}{_SUF_SOCIEDAD}"',
     "«Pfizer Inc.» al empezar vuelve a pasar (regresión H-44)"),
    ("S28", r'rf"|(?!{_DETERMINANTE}\b)(?!(?<=\A)[A-Z][a-záéíóú]+(?:ar|er|ir)\b){_NOMBRE}{_SUF_FONDO}"',
     r'rf"|(?!{_DETERMINANTE}\b){_NOMBRE}{_SUF_FONDO}"', "«Sobreponderar ETF…» se quita"),
    ("S29", r'r"|(?<![\w&.-])[a-z][\w&-]{0,40}\s+(?:inc|corp|corporation|incorporated|ltd|ltda|plc|llc|gmbh|"',
     r'r"|(?<![\w&.-])[a-z][\w&-]{0,40}\s+(?:inc|"', "«nvidia corporation» y «x ltd» en minúscula pasan"),
    ("S30", "                                                 or (por_ticker and c[0].isupper() and c[1:].islower())\n",
     "", "«el ETF Nvda» pasa (regresión H-44)"),
    ("S31", "if not por_ticker and len(c) >= 3 and c[0].isupper() and c[1:].islower():",
     "if len(c) >= 3 and c[0].isupper() and c[1:].islower():", "la mayúscula inicial es nombre también tras ETF"),
    ("S32", 'c = m.group(1).rstrip(".")   # r06 (H-44)', "c = m.group(1)   # r06 (H-44)", "«el fondo vwrl.» pasa"),
    # H-41: palabras corrientes tras un vehículo y la acción de
    ("S33", '"es", "son", "era"', '"son", "era"', "«Un ETF es un fondo» se quita"),
    ("S34", '"sube", "suben", "cae", "caen"', '"suben", "caen"', "«El ETF sube» y «El ETF cae» se quitan"),
    ("S35", 'if m.group(0).rstrip().lower().endswith(" de") and re.match(r"\\s*[a-záéíóúñ]", libre[m.end():]):',
     "if False:", "«la acción de los bancos centrales» se quita"),
    # H-46: escrituras de mala fe
    ("S36", 'if out and out[-1] in _MARCA_ESPANOLA.get(ch, ""):', "if True:", "las marcas combinantes ajenas se conservan"),
    ("S37", 'if out and out[-1] in _MARCA_ESPANOLA.get(ch, ""):', "if False:", "se quitan también tildes, ñ y diéresis"),
    ("S38", r'(?<![\w])[A-Z](?:[\s_\u2800][A-Z]){2,}(?![\w])', r'(?<![\w])[A-Z](?:[\s_\u2800][A-Z]){5,}(?![\w])',
     "«N V D A» pasa"),
    ("S39", r'[\s_\u2800]', r'[\s]', "«N_V_D_A» y el blanco Braille pasan"),
    ("S40", '"SQUARED LATIN",', "", "letras en recuadro («🅽🆅🅳🅰») pasan"),
    ("S41", '"CIRCLED LATIN", "PARENTHESIZED LATIN"', '"PARENTHESIZED LATIN"', "letras en círculo pasan"),
    ("S42", "    if _hay_cifra(_MARCADOR.sub(\" \", orig)):   # antes de normalizar", "    if False:   # antes de normalizar",
     "«Ⅶ» se normaliza a «VII» antes de mirar cifras"),
    ("S43", "if unicodedata.category(ch) != \"Cf\")", "if True)", "los caracteres de formato no se quitan"),
    # el resto de r06
    ("S44", 'if re.search(r"\\b(?:n_ideas|n_tipos|n_apuestas)\\b|\\b(?:opp|tipo|n|candidatas):[A-Za-z0-9-]", libre):',
     'if re.search(r"\\b(?:opp|tipo|n|candidatas):[A-Za-z0-9-]", libre):', "«〔n_ideas〕» fuera de llaves pasa"),
    ("S45", r"camino|periodo|década|sesión|jornada))", r"camino|periodo|década))", "«mitad de la sesión» vuelve a ser cifra"),
    ("S46", "(?<!primera\\s)(?<!segunda\\s)", "(?<!primera\\s)", "«segunda mitad» vuelve a ser cifra"),
]


def correr(m):
    mid, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r06_t102_{mid}_"))
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
    res = []
    with ThreadPoolExecutor(PAR) as ex:   # cada resultado se imprime al acabar (si se corta la pasada, no se pierde)
        for fut in as_completed([ex.submit(correr, m) for m in lista]):
            mid, desc, estado, det = fut.result()
            res.append((mid, desc, estado, det))
            print(f"[{estado}] {mid} {desc} · {det}", flush=True)
    res.sort()
    vivos = [r[0] for r in res if r[2] == "SOBREVIVE"]
    noap = [r[0] for r in res if r[2].startswith("NO APLICA")]
    print(f"\nMatados: {sum(1 for r in res if r[2] == 'MATADO')}/{len(res)} · Sobreviven: {len(vivos)} {vivos} · "
          f"No aplican: {noap} · Errores: {[r[0] for r in res if r[2].startswith('ERROR')]}")
    sys.exit(1 if vivos or noap else 0)
