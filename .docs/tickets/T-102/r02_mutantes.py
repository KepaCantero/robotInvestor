"""Ronda r02 de T-102 · Mutantes del filtro nuevo contra `tests/test_t102_filtro.py` (con «completo», también
`tests/test_t101_v6.py`). Adaptación de `revisores/r01_mutantes.py` de la QA r01 a las expresiones de la r02.

Mismo método que `.docs/tickets/T-101/revisores/r01_mutantes.py`: copia `bloque_a/` de la raíz indicada a una carpeta temporal
por mutante, aplica UNA mutación textual a `bloque_a/diseno_v6.py` y ejecuta las baterías. Un mutante «sobrevive» si siguen en
verde: hay un comportamiento del ticket que ninguna prueba vigila.

Uso: .venv/bin/python -I .docs/tickets/T-102/r02_mutantes.py <raiz_repo> [n_paralelo] [ids separados por comas] [completo]
Sin «completo», solo `tests/test_t102_filtro.py`.
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
PY = str(Path(__file__).resolve().parents[3] / ".venv" / "bin" / "python")
D6 = "bloque_a/diseno_v6.py"
PRUEBAS = ["tests/test_t102_filtro.py"] + (["tests/test_t101_v6.py"] if COMPLETO else [])

# (id, texto original, texto mutado, qué rompe)
MUTANTES = [
    ("M01", "    if _R13_DIRECTA.search(t) and not _R13_VAR.search(t):\n        return True\n", "", "sin la regla directa de R13"),
    ("M02", "and not _R13_VAR.search(t)", "", "el VaR al 95 % de confianza es R13"),
    ("M03", "    if not _PALABRA_PROB.search(t):\n        return False\n    for m", "    if True:\n        return False\n    for m", "sin la regla amplia de R13"),
    ("M04", "|posibilidad(?:es)?|chances?)\\b\", re.IGNORECASE)", ")\\b\", re.IGNORECASE)", "R13 amplia sin «posibilidad» ni «chance»"),
    ("M05", "(?<![\\w.,])0[.,]\\d+\\b|", "", "R13 sin decimales 0,xx"),
    ("M06", "|\\b\\d+\\s+de\\s+cada\\s+\\d+\\b", "", "R13 sin «N de cada M»"),
    ("M07", "if not (_NIVEL_ANTES.search(antes) or _TOPE_ANTES.search(antes) or _NIVEL_DESPUES.match(despues)):",
     "if not (_TOPE_ANTES.search(antes) or _NIVEL_DESPUES.match(despues)):", "sin la excepción del nivel de un tipo"),
    ("M08", "if not (_NIVEL_ANTES.search(antes) or _TOPE_ANTES.search(antes) or _NIVEL_DESPUES.match(despues)):",
     "if not (_NIVEL_ANTES.search(antes) or _NIVEL_DESPUES.match(despues)):", "sin la excepción del tope de un movimiento"),
    ("M09", "if not (_NIVEL_ANTES.search(antes) or _TOPE_ANTES.search(antes) or _NIVEL_DESPUES.match(despues)):",
     "if not (_NIVEL_ANTES.search(antes) or _TOPE_ANTES.search(antes)):", "sin la excepción de «de las veces» o «del capital»"),
    ("M10", "(?-i:[A-ZÁÉÍÓÚ][\\w.&]*))", "[A-ZÁÉÍÓÚ][\\w.&]*)", "el nombre propio de la cadena con IGNORECASE (vale cualquier palabra)"),
    ("M11", "if not (_NIVEL_ANTES.search(antes)", "if not (_NIVEL_ANTES.search(antes) or True", "toda cifra es un nivel"),
    ("M12", "|confianza|seguridad|certeza|opciones|riesgo\\s+de|que)\\b", "|confianza|opciones)\\b", "sin «de seguridad», «de riesgo de» ni «de que»"),
    ("M13", "    if _SUFIJO.search(t) or _EMISION.search(t) or sint._UNITARIA.search(t):", "    if _EMISION.search(t) or sint._UNITARIA.search(t):", "sin el sufijo societario"),
    ("M14", "    if _SUFIJO.search(t) or _EMISION.search(t) or sint._UNITARIA.search(t):", "    if _SUFIJO.search(t) or sint._UNITARIA.search(t):", "sin la emisión con vencimiento"),
    ("M15", "    if _SUFIJO.search(t) or _EMISION.search(t) or sint._UNITARIA.search(t):", "    if _SUFIJO.search(t) or _EMISION.search(t):", "sin `_UNITARIA`"),
    ("M16", "|S\\.A\\.|SA|", "|", "sin «S.A.» ni «SA»"),
    ("M17", "    if any(_es_instrumento(m, perm) for m in _ISIN.findall(t)):", "    if False:", "sin el ISIN sin verbo"),
    ("M18", "        corte = _CORTE.search(resto)", "        corte = None", "sin cortes: la ventana llega al final"),
    ("M19", "        ventana = _INDICE.sub(\" \", resto[:corte.start()] if corte else resto)", "        ventana = resto[:corte.start()] if corte else resto", "sin las familias de índices"),
    ("M20", "    if c in perm[\"codigos\"] or c in perm[\"series\"] or _CALIFICACION.fullmatch(c):", "    if c in perm[\"codigos\"] or c in perm[\"series\"]:", "sin calificaciones"),
    ("M21", "    if len(partes) == 2 and all(x in perm[\"codigos\"] for x in partes):\n        return False\n", "", "el par con barra es un instrumento"),
    ("M22", "    if len(c) == 6 and c.isalpha() and c[:3] in perm[\"codigos\"] and c[3:] in perm[\"codigos\"]:\n        return False\n", "", "el par sin barra es un instrumento"),
    ("M23", "    t = re.sub(r\"\\bEE\\.\\s?UU\\.\", \"EEUU\", t)\n", "", "«EE. UU.» sin normalizar"),
    ("M24", "    protegido = _ABREV.sub(lambda m: m.group(0).replace(\".\", _PUNTO), t)", "    protegido = t", "las abreviaturas parten la frase"),
    ("M25", "_SEPARADOR = re.compile(r\"((?<=[.;!?…])\\s+|\\s*\\n+\\s*)\")", "_SEPARADOR = re.compile(r\"((?<=[.;!?])\\s+)\")", "ni «…» ni el salto de línea separan"),
    ("M26", "    if not reglas:\n        return t, []\n", "", "un texto limpio pierde sus separadores"),
    ("M27", "apost(?:ar|a|amos|emos)\\s+por|", "", "sin «apostar por»"),
    ("M28", "acumul(?:ar|a|amos|e|en)|", "", "sin «acumular»"),
    ("M29", "|la\\s+compra\\s+de|la\\s+venta\\s+de)\\b", ")\\b", "sin «la compra de» ni «la venta de»"),
    ("M30", "ponerse\\s+(?:largos?|cortos?)\\s+en|", "", "sin «ponerse largos en»"),
    ("M31", "suscribir|liquidar|", "", "sin «suscribir» ni «liquidar»"),
    ("M32", "        (quitadas.append(r) if r else glosario.append(g))", "        (None if r else glosario.append(g))", "el glosario quitado no se declara"),
    ("M33", "    paquete[\"limitaciones\"] = [x for x in paquete[\"limitaciones\"] if not x.startswith(previa)]\n", "", "la reescritura duplica la limitación"),
    ("M34", "and not re.fullmatch(r\"[A-Z0-9]{1,6}\\.[A-Z]{1,3}\", x)}", "}", "un símbolo con sufijo de bolsa es una serie"),
    ("M35", "        return t2 if not reglas else (t2.strip() or por_defecto)", "        return t2", "un texto vacío no toma su defecto"),
    ("M36", "    perm = permitidos_r21(bloque)\n    if d:", "    perm = None\n    if d:", "el Sintetizador sin códigos permitidos"),
    ("M37", "            t = _limpio(\"factores_dominantes\", x.get(\"factor\"))", "            t = x.get(\"factor\")", "los factores sin filtro"),
    ("M38", "    preg = [t for t in (_limpio(\"preguntas_sugeridas\", x)", "    preg = [t for t in (x", "las preguntas sin filtro"),
    ("M39", "    reg = _limpio(\"regimen_macro\", d.get(\"regimen_macro\"))", "    reg = d.get(\"regimen_macro\")", "el régimen sin filtro"),
    ("M40", "if isinstance(v, str) and (v2 := _uno(v, \"\").strip())}", "if isinstance(v, str) and (v2 := v)}", "los motivos llanos sin filtro"),
    ("M41", "    red[\"frase_historial\"] = _uno(red.get(\"frase_historial\"), defecto[\"frase_historial\"])", "    pass", "la frase del historial sin filtro"),
    ("M42", "        for k in (\"por_que_llano\", \"que_puede_salir_mal_llano\", \"ambito_llano\"):", "        for k in (\"por_que_llano\",):", "el riesgo y el ámbito llanos sin filtro"),
    ("M43", "\\b[yeo]\\s+(?:ya\\s+|no\\s+|se\\s+)*", "\\bNOCORTA\\s+", "sin el corte en «y + verbo»"),
    ("M44", "(?:[Ss]i|[Cc]uando|", "(?:[Cc]uando|", "sin el corte en «si»"),
]


def correr(m):
    mid, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r02_t102_{mid}_"))
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
