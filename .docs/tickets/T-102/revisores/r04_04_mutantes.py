"""QA r04 de T-102 · Mutantes del revisor sobre las piezas NUEVAS de la r04 (cifras Unicode y en letra, palabras de probabilidad,
marcadores compuestos, sufijos, homoglifos, códigos pegados, vehículos, nombre llano, glosario, NFKC, separador lineal y la
lista de siglas en la instrucción).

Método de la r02: copia `bloque_a/` de la raíz indicada a una carpeta temporal por mutante, aplica UNA mutación textual a
`bloque_a/diseno_v6.py` y ejecuta `tests/test_t102_filtro.py` (con «completo», también `tests/test_t101_v6.py`). Un mutante
«sobrevive» si las pruebas siguen en verde: hay un comportamiento que ninguna prueba vigila.

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r04_04_mutantes.py <raiz_repo> [n_paralelo] [ids|todos] [completo]
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
    ("W01", 'unicodedata.category(ch).startswith("N")', 'unicodedata.category(ch) == "Nd"', "solo dígitos Nd (sin ⅔, ⁷, Ⅶ)"),
    ("W02", '    if _hay_cifra(_MARCADOR.sub(" ", crudo)):', "    if False:", "sin la mirada antes de NFKC (Ⅶ pasa a VII)"),
    ("W03", 'r"escenarios?)\\b"', 'r"xqzxqz)\\b"', "«escenario» deja de ser palabra de probabilidad"),
    ("W04", "confianza|seguridad|certeza|", "", "sin confianza, seguridad ni certeza"),
    ("W05", 'r"tercios?|cuartos?|quintos?|d[eé]cimos?)")', 'r"tercios?)")', "sin cuartos, quintos ni décimos"),
    ("W06", "mil|millones?|medio|mitad|", "", "sin mil, medio ni mitad"),
    ("W07", 'rf"\\bpor\\s+cien(?:to)?\\b|[%‰]|', 'rf"\\bpor\\s+cien(?:to)?\\b|', "«%» y «‰» sueltos no cuentan"),
    ("W08", r"(?:sobre|entre|de\s+cada|en)\s+{_NUM_LETRA}", r"(?:sobre|de\s+cada)\s+{_NUM_LETRA}", "sin «entre» ni «en»"),
    ("W09", r"\s*(?:sobre|entre|de\s+cada|/|%)?\s*", r"\s*(?:sobre)?\s*", "marcadores unidos solo por «sobre»"),
    ("W10", r"|{_MARCADOR_NUM.pattern}\s*%", "", "un marcador seguido de «%» no cuenta"),
    ("W11", " or _MARCADOR_NUM.search(t)", "", "probabilidad junto a un marcador numérico no cuenta"),
    ("W12", ' or any("CURLY BRACKET" in unicodedata.name(ch, "") for ch in libre)', "", "las llaves ❴ ❵ no cuentan"),
    ("W13", 'r"\\b(?!(?:El|La|Los|Las|Un|', 'r"\\b(?!(?:XQZ|Un|', "«Las SICAV» vuelve a ser una sociedad"),
    ("W14", ')\\.?(?!\\w)")', ')(?![\\w.])")', "el sufijo con punto deja de contar (r03)"),
    ("W15", "Fund|Trust|", "", "sin «Fund» ni «Trust»"),
    ("W16", "UCITS\\s+ETF|ETF|", "", "sin «ETF» ni «UCITS ETF» como sufijo"),
    ("W17", "(?i:inc|corp|corporation|incorporated|ltd)", "XQZ", "sin los sufijos en minúscula"),
    ("W18", '    if any(unicodedata.name(ch, "").startswith(("CYRILLIC", "GREEK")) for ch in libre):', "    if False:",
     "sin la regla de otros alfabetos"),
    ("W19", ".translate(_HOMOGLIFOS)", "", "sin plegar homoglifos (equivalente si W18 vive)"),
    ("W20", r"|\$([A-Za-z]{1,6})\b", "", "«$» seguido de letras no cuenta"),
    ("W21", "(?:[_=]|(?<=[a-záéíóúñ])[-.])", "(?:[_=])", "sin el código tras «-» o «.» después de una minúscula"),
    ("W22", "        return not _CONTEXTO_CALIFICACION.search(contexto)", "        return False",
     "una calificación nunca es instrumento («Comprar AA»)"),
    ("W23", ' or re.fullmatch(r"X{0,3}(?:IX|IV|V?I{0,3})", c)', "", "los romanos vuelven a ser instrumentos"),
    ("W24", '        if not (m.group(2) == "s" and m.group(1) in perm["codigos"]):', "        if False:",
     "sin la regla de mayúsculas mezcladas"),
    ("W25", 'm.group(2) == "s" and m.group(1) in perm["codigos"]', 'm.group(2) == "s"', "cualquier plural en «s» vale («NVDAs»)"),
    ("W26", "((c.islower() and ticker) or", "(False or", "sin el ticker en minúscula tras un vehículo"),
    ("W27", "(len(c) == 1 and c.isupper())", "False", "sin la letra sola tras un vehículo"),
    ("W28", 'm.group(0).lower().startswith("fondo") and len(c) <= 4)', 'm.group(0).lower().startswith("fondo") and len(c) <= 3)',
     "tras «fondo», solo hasta tres letras"),
    ("W29", "            if perm is not None and frase_prohibida(nombre, perm):", "            if False:",
     "el nombre llano no pasa la regla (H-27)"),
    ("W30", '            quitadas.append("FORMATO")', "            pass", "el glosario que no es texto no se declara"),
    ("W31", 'if not isinstance(g.get("termino"), str) or not isinstance(g.get("definicion"), str):',
     'if not isinstance(g.get("termino"), str):', "una definición que no es texto rompe el ciclo (H-24)"),
    ("W32", 'rellenar(unicodedata.normalize("NFKC", salida), marcas)', "rellenar(salida, marcas)", "la salida sin NFKC (｛n_ideas｝)"),
    ("W33", '    t = unicodedata.normalize("NFKC", crudo)', "    t = crudo", "la frase sin NFKC"),
    ("W34", 'instr = INSTR_SINTESIS + " Siglas que puedes usar: " + ", ".join(sorted(perm["codigos"])) + "."',
     "instr = INSTR_SINTESIS", "el Sintetizador no recibe la lista de siglas (H-25)"),
    ("W35", r"(?<![^\S\n])[^\S\n]*+\n\s*+", r"\s*\n+\s*", "separador cuadrático (H-26)"),
    ("W36", "if (c.islower() and c in _PALABRA_COMUN) or (c[0].islower() and len(c) > 5):",
     "if (c[0].islower() and len(c) > 5):", "sin las palabras comunes tras un vehículo («fondo de»)"),
    ("W37", 'if c.upper() not in perm["codigos"] and (', "if True and (", "una sigla de la lista tras un vehículo cuenta"),
    ("W38", '    if c in perm["codigos"] or c in perm["series"] or', '    if c in perm["codigos"] or', "las series del universo son instrumentos"),
    ("W39", "    if _hay_cifra(libre) or _CIFRA_EN_LETRA.search(libre):", "    if _CIFRA_EN_LETRA.search(libre):",
     "sin la mirada después de NFKC (equivalente si W02 vive)"),
    ("W40", "    if _PALABRA_PROB.search(libre) and (_NUMERO_LETRA.search(libre) or _MARCADOR_NUM.search(t)):   # H-20 y H-23",
     "    if False:", "sin probabilidad junto a un número en letra"),
]



def correr(m):
    mid, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r04_t102_{mid}_"))
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
          f"No aplican: {[r[0] for r in res if r[2].startswith('NO APLICA')]} · Errores: {[r[0] for r in res if r[2].startswith('ERROR')]}")
