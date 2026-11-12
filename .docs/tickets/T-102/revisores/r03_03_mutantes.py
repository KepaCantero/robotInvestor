"""QA r03 de T-102 · Mutantes del revisor sobre las piezas NUEVAS de la r03 (marcadores, regla CIFRA/R21/MARCADOR, relleno
después de filtrar, defectos y declaración).

Método de la r02: copia `bloque_a/` de la raíz indicada a una carpeta temporal por mutante, aplica UNA mutación textual a
`bloque_a/diseno_v6.py` y ejecuta `tests/test_t102_filtro.py` (con «completo», también `tests/test_t101_v6.py`). Un mutante
«sobrevive» si las pruebas siguen en verde: hay un comportamiento que ninguna prueba vigila.

Uso: .venv/bin/python -I .docs/tickets/T-102/revisores/r03_03_mutantes.py <raiz_repo> [n_paralelo] [ids|todos] [completo]
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
    ("Q01", "    if marcas is not None and any(_clave(m) not in marcas for m in _MARCADOR.finditer(t)):",
     "    if False:", "un marcador que no es del paquete no quita la frase"),
    ("Q02", "        r = frase_prohibida(f, perm, marcas) if f.strip() else None",
     "        r = frase_prohibida(rellenar(f, marcas) if marcas is not None else f, perm, marcas) if f.strip() else None",
     "se rellena ANTES de filtrar (las cifras del código se filtran)"),
    ("Q03", "    if _LLAVE.search(libre):", "    if False:", "una llave suelta no quita la frase"),
    ("Q04", "_DIGITO = re.compile(r\"\\d\")", "_DIGITO = re.compile(r\"[0-9]\")", "solo dígitos ASCII (sin ７, ٧, 𝟕)"),
    ("Q05", "_DIGITO.search(libre) or _CIFRA_EN_LETRA.search(libre) or (", "_DIGITO.search(libre) or (",
     "sin «por ciento» ni «de cada N»"),
    ("Q06", "r\"\\bpor\\s+ciento\\b|\\bde\\s+cada\\s+(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|cien)\\b\"",
     "r\"\\bpor\\s+ciento\\b\"", "sin «de cada N» en letra"),
    ("Q07", " or (_PALABRA_PROB.search(libre) and _FRACCION.search(libre)):", ":", "sin la fracción junto a una probabilidad"),
    ("Q08", "r\"\\b(?:mitad|tercios?|cuartos?|quintos?|d[eé]cimos?)\\b\"", "r\"\\b(?:mitad|cuartos?|quintos?|d[eé]cimos?)\\b\"",
     "sin «tercios»"),
    ("Q09", "r\"\\b(?:(?:im)?probab\\w*|posibilidad(?:es)?|chances?|opciones\\s+de\\s+que)\\b\"", "r\"\\b(?:(?:im)?probab\\w*)\\b\"",
     "la palabra de probabilidad sin «posibilidad», «chances» ni «opciones de que»"),
    ("Q10", "    if _SUFIJO.search(libre) or sint._UNITARIA.search(libre):", "    if sint._UNITARIA.search(libre):",
     "sin el sufijo societario o de fondo"),
    ("Q11", "    if _SUFIJO.search(libre) or sint._UNITARIA.search(libre):", "    if _SUFIJO.search(libre):", "sin `_UNITARIA`"),
    ("Q12", "FI|FIL|SICAV|SOCIMI\\s+S\\.A\\.)", "SOCIMI\\s+S\\.A\\.)", "sin «FI», «FIL» ni «SICAV»"),
    ("Q13", "    libre = _INDICE.sub(\" \", re.sub(", "    libre = (re.sub(", "sin quitar las familias de índices"),
    ("Q14", "Nikkei|NIKKEI)(?:\\s+[A-Z][\\w&-]*){0,3}\")", "Nikkei|NIKKEI)(?:\\s+[A-Z][\\w&-]*){0,1}\")",
     "la familia de índices solo se come una palabra («MSCI World Small Cap»)"),
    ("Q15", "    if c in perm[\"codigos\"] or c in perm[\"series\"] or _CALIFICACION.fullmatch(c):",
     "    if c in perm[\"codigos\"] or _CALIFICACION.fullmatch(c):", "las series del universo son instrumentos"),
    ("Q16", "    if c in perm[\"codigos\"] or c in perm[\"series\"] or _CALIFICACION.fullmatch(c):",
     "    if c in perm[\"codigos\"] or c in perm[\"series\"]:", "una calificación es un instrumento"),
    ("Q17", "    if len(partes) == 2 and all(x in perm[\"codigos\"] for x in partes):", "    if False:",
     "un par con barra es un instrumento"),
    ("Q18", "    if len(c) == 6 and c.isalpha() and c[:3] in perm[\"codigos\"] and c[3:] in perm[\"codigos\"]:", "    if False:",
     "un par sin barra es un instrumento"),
    ("Q19", "    return any(ch.isupper() for ch in c) and len(c) >= 2", "    return any(ch.isupper() for ch in c) and len(c) >= 3",
     "un código de dos letras no es un instrumento"),
    ("Q20", "              and not re.fullmatch(r\"[A-Z0-9]{2,10}-(?:USD|EUR|USDT|USDC|BTC)\", x)}", "              }",
     "«BTC-USD» vuelve a ser una serie (H-17)"),
    ("Q21", "and not re.fullmatch(r\"[A-Z0-9]{1,6}\\.[A-Z]{1,3}\", x)", "", "«XEON.DE» vuelve a ser una serie"),
    ("Q22", "            out[f\"opp:{o['opp_id']}\"] = str(o.get(\"nombre_llano\") or \"esta idea\")",
     "            out[f\"opp:{o['opp_id']}\"] = str(o.get(\"nombre\") or \"esta idea\")", "{opp:…} da el nombre técnico"),
    ("Q23", "        n_tipos += 1 if ops else 0", "        n_tipos += 1", "{n_tipos} cuenta también los tipos sin ideas"),
    ("Q24", "str(paquete.get(\"apuestas_independientes\", n_ideas))", "str(n_ideas)", "{n_apuestas} da las ideas"),
    ("Q25", "str(d.get(\"candidatas_analizadas\", 0))", "str(len(ops))", "{candidatas:X} da las opciones"),
    ("Q26", "    salida = t if not reglas else \"\".join(quedan).replace(_PUNTO, \".\").strip()",
     "    salida = \"\".join(quedan).replace(_PUNTO, \".\").strip()", "un texto limpio pierde sus espacios"),
    ("Q27", "    return (rellenar(salida, marcas) if marcas is not None else salida), reglas",
     "    return (rellenar(salida, marcas) if marcas is not None and not reglas else salida), reglas",
     "si se quita una frase, los marcadores del resto quedan sin rellenar"),
    ("Q28", "        r = frase_prohibida(str(g.get(\"termino\", \"\")), perm, marcas) or texto_prohibido(",
     "        r = texto_prohibido(", "el término del glosario no se filtra"),
    ("Q29", "\"termino\": rellenar(str(g.get(\"termino\", \"\")), marcas),", "\"termino\": str(g.get(\"termino\", \"\")),",
     "el término del glosario no se rellena"),
    ("Q30", "    perm = permitidos or {\"codigos\": frozenset(), \"series\": frozenset()}\n    marcas = marcadores(paquete)\n    descartados",
     "    perm = permitidos or {\"codigos\": frozenset(), \"series\": frozenset()}\n    marcas = None\n    descartados",
     "la integración ni valida ni rellena los marcadores"),
    ("Q31", "    t = t.replace(_PUNTO, \".\")\n", "", "la frase se juzga con el punto protegido (U+2024)"),
    ("Q32", "_SEPARADOR = re.compile(r\"((?<=[.;!?…])\\s+|\\s*\\n+\\s*)\")", "_SEPARADOR = re.compile(r\"((?<=[.;!?…])\\s+)\")",
     "el salto de línea no separa frases"),
    ("Q33", "        return t2 if not reglas else (t2.strip() or por_defecto)", "        return t2 if not reglas else por_defecto",
     "una frase mala tira todo el elemento a su defecto"),
    ("Q34", "        quitadas.extend(reglas)\n", "", "lo quitado de la redacción no se declara"),
    ("Q35", "if isinstance(v, str) and (v2 := _uno(v, \"\").strip())}", "if isinstance(v, str) and (v2 := v.strip())}",
     "los motivos llanos no se filtran"),
    ("Q36", "    red[\"frase_historial\"] = _uno(red.get(\"frase_historial\"), defecto[\"frase_historial\"])",
     "    red[\"frase_historial\"] = _uno(red.get(\"frase_historial\"), \"\")", "el historial vacío no toma su defecto"),
    ("Q37", "_SUFIJO = re.compile(r\"\\b[A-Z][\\w&.-]*(?:\\s+[A-Z][\\w&.-]*){0,6}\\s+(?:Corp|",
     "_SUFIJO = re.compile(r\"\\b[A-Z][\\w&.-]*(?:\\s+[A-Z][\\w&.-]*){0,6}\\s+(?:", "sin «Corp»"),
    ("Q38", "_PALABRA_PROB = re.compile(r\"\\b(?:(?:im)?probab\\w*|posibilidad(?:es)?|chances?|opciones\\s+de\\s+que)\\b\", re.IGNORECASE)",
     "_PALABRA_PROB = re.compile(r\"\\b(?:(?:im)?probab\\w*|posibilidad(?:es)?|chances?|opciones\\s+de\\s+que)\\b\")",
     "«Probabilidad» con mayúscula no cuenta"),
]


def correr(m):
    mid, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r03_t102_{mid}_"))
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
