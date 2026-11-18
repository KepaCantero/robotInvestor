"""T-187 · mutantes de `revision_prompts_pb51.py`: cada uno quita o tuerce una comprobación y alguna prueba de
`pruebas_revision_prompts_pb51.py` tiene que fallar.

Uso, desde la raíz:  .venv/bin/python .docs/scripts/mutantes_revision_prompts_pb51.py [--solo M01,M02]
Cada mutante se escribe en una carpeta temporal (el script original no se toca) y las pruebas lo cargan por
`PB51_MODULO`. Vivo = ninguna prueba lo detecta. Termina con 1 si un mutante no aplica o vive.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ORIGINAL = AQUI / "revision_prompts_pb51.py"
PRUEBAS = AQUI / "pruebas_revision_prompts_pb51.py"
SOLO = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None

MUTANTES = [
    ("M01", "estructura: no exige el orden", "completa = not faltan and not sobran and not repetidas and en_orden",
     "completa = not faltan and not sobran and not repetidas"),
    ("M02", "estructura: no mira las repetidas", "repetidas = sorted({n for n in nums if nums.count(n) > 1})",
     "repetidas: list[int] = []"),
    ("M03", "estructura: no mira las que faltan", "faltan = [n for n in esperados if n not in nums]",
     "faltan: list[int] = []"),
    ("M04", "títulos: siempre coinciden", '"coincide": bool(comun)', '"coincide": True'),
    ("M05", "títulos: sin quitar mayúsculas", "nfc(titulo).casefold()", "nfc(titulo)"),
    ("M06", "secciones: también dentro de un bloque de código", "        if not en_codigo and RE_FIN_SECCION.match(x):",
     "        if RE_FIN_SECCION.match(x):"),
    ("M07", "Anexo G: acepta una lista mal numerada", "if [n for n, _ in out] != list(range(1, len(out) + 1)) or not out:",
     "if not out:"),
    ("M08", "subáreas: el bis se funde con su número", 'clave = f"{m.group(1)}.{m.group(2)}" + (" bis" if m.group(3) else "")',
     'clave = f"{m.group(1)}.{m.group(2)}"'),
    ("M09", "recuento: el inventario cuenta", "        if excl:\n            fila.update(", "        if False:\n            fila.update("),
    ("M10", "fórmulas: una ruta cuenta como fórmula", "    if RE_RUTA.search(s):\n        return False", "    pass"),
    ("M11", "fórmulas: sin los «=» del texto", "+ len(RE_IGUAL_TEXTO.findall(sin_codigo(t)))", "+ 0"),
    ("M12", "umbrales: sin los comparadores en palabras", '|\\b(?:al menos|como mínimo', '|\\b(?:al menos XYZ|como mínimo XYZ'),
    ("M13", "definiciones: sin el paréntesis tras el término", "(?:\\s*\\([^()\\n]*(?:\\([^()\\n]*\\)[^()\\n]*)*\\))?", ""),
    ("M14", "trampas: solo por el título", "return bool(RE_TITULO_TRAMPAS.search(sub.titulo) or RE_TEXTO_TRAMPA.search(t))",
     "return bool(RE_TITULO_TRAMPAS.search(sub.titulo))"),
    ("M15", "citas: sin la forma entre paréntesis", "            mb = RE_CITA_B_PARTE.match(parte)", "            mb = None"),
    ("M16", "citas: sin el título tras el paréntesis", "bool(RE_TIENE_TITULO.search(resto) or m.group(4))",
     "bool(RE_TIENE_TITULO.search(resto))"),
    ("M17", "citas: partículas al principio del autor", "_AUTOR = rf\"{_PALABRA_AUTOR}(?:",
     "_AUTOR = rf\"(?:(?:de|van)\\s+)?{_PALABRA_AUTOR}(?:"),
    ("M18", "citas: sin la lista de falsos autores", "    return primero not in NO_AUTOR\n", "    return True\n"),
    ("M19", "referencias: el amplio no busca en el prompt", '(x["titulo"] or x["clave"] in con_titulo)', '(x["titulo"])'),
    ("M20", "referencias: cuenta las instrucciones", "        if not (my or mt):\n            continue", "        pass"),
    ("M21", "referencias: sin heredar los autores", "        if nombre is None and out and out[-1][\"autor\"]",
     "        if False and nombre is None and out and out[-1][\"autor\"]"),
    ("M22", "referencias: las tablas sin partir", '    if t.lstrip().startswith("|"):', '    if False:'),
    ("M23", "DOI: sin el registrante numérico", 'RE_DOI_VALIDO = re.compile(r"^10\\.\\d{4,9}', 'RE_DOI_VALIDO = re.compile(r"^10\\.\\w+'),
    ("M24", "DOI: los números de sección como DOI", 'RE_DOI_CANDIDATO = re.compile(r"\\b10\\.\\d+(?:\\.\\d+)*/\\S*',
     'RE_DOI_CANDIDATO = re.compile(r"\\b10\\.\\S+'),
    ("M25", "ISBN: sin dígito de control", "% 11 == 0\n", "% 1 == 0\n"),
    ("M26", "ISSN: sin dígito de control", "return d[7] == (\"X\" if control == 10 else str(control))", "return True"),
    ("M27", "frases: corta tras una abreviatura", "or prev.endswith(ABREVIATURAS) ", ""),
    ("M28", "frases: corta dentro del código", 't.count("`") % 2 == 1 or ', ""),
    ("M29", "muestra: sin semilla por archivo", 'random.Random(f"{semilla}|{archivo}")', "random.Random(semilla)"),
    ("M30", "muestra: sin ordenar", "idx = sorted(rng.sample(range(len(cands)), k))", "idx = rng.sample(range(len(cands)), k)"),
    ("M31", "muestra: una de más", "k = min(MUESTRA_POR_PROMPT, len(cands))", "k = min(MUESTRA_POR_PROMPT + 1, len(cands))"),
    ("M32", "candidatas: de todas las secciones", "        if s.numero not in (n_metodo, n10):\n            continue", "        pass"),
    ("M33", "candidatas: las referencias canónicas son afirmaciones",
     "if RE_INVENTARIO.search(sub.titulo) or RE_TITULO_REFERENCIAS.search(sub.titulo):", "if RE_INVENTARIO.search(sub.titulo):"),
    ("M34", "candidatas: frases sin marca", "                    if not mk:\n                        continue", "                    pass"),
    ("M35", "tamaño: el analista con el prompt entero", "sin10 = tokens_aprox(texto.replace(quitar, \"\"), ejecutor) if quitar else tok",
     "sin10 = tok"),
    ("M36", "tamaño: el tope no se compara", 'dentro=tok <= topes[ag]', 'dentro=True'),
    ("M37", "falla cerrado: sin topes sigue", '    if not isinstance(topes_raw, dict) or not topes_raw:\n        raise',
     '    if False:\n        raise'),
    ("M38", "falla cerrado: con dos Documentos 0 sigue", "if len(d0s) != 1 or not archivos", "if not d0s or not archivos"),
    ("M39", "--comprobar no compara", "        return 1 if dif else 0", "        return 0"),
    ("M40", "la muestra trae un veredicto", '"veredicto": None', '"veredicto": "CORRECTA"'),
    ("M41", "plantilla dentro del denominador", "plantilla = not p.name.startswith(PREFIJO_PROMPT)", "plantilla = False"),
    # Paso 3 · contraste de los revisores
    ("M42", "contraste: no mira los ids que faltan", "    faltan = [i for i in ids if i not in por_id]", "    faltan: list[str] = []"),
    ("M43", "contraste: no mira los ids que sobran", "    sobran = sorted(set(por_id) - set(ids))", "    sobran: list[str] = []"),
    ("M44", "contraste: acepta un veredicto desconocido", '            if v.get("veredicto") not in VEREDICTOS:',
     '            if v.get("veredicto") is None:'),
    ("M45", "contraste: acepta un id duplicado", "            if i in por_id:\n", "            if False:\n"),
    ("M46", "contraste: la nota de 40 palabras falla", "if len(nota.split()) > MAX_PALABRAS_NOTA:",
     "if len(nota.split()) >= MAX_PALABRAS_NOTA:"),
    ("M47", "contraste: nota sin límite de palabras", "MAX_PALABRAS_NOTA = 40 ", "MAX_PALABRAS_NOTA = 4000 "),
    ("M48", "contraste: acepta una nota vacía o sin letras", "            if not _texto(nota):",
     "            if not isinstance(nota, str):"),
    ("M49", "porcentaje: las no verificables en el denominador", '    verif = c["CORRECTA"] + c["ERRONEA"]\n',
     '    verif = c["CORRECTA"] + c["ERRONEA"] + c["NO_VERIFICABLE"]\n'),
    ("M50", "porcentaje: el 95 % exacto no supera", "100 * c[\"CORRECTA\"] >= UMBRAL_CORRECTAS * verif",
     "100 * c[\"CORRECTA\"] > UMBRAL_CORRECTAS * verif"),
    ("M51", "porcentaje: sin verificables supera", '"supera": bool(verif) and ', '"supera": '),
    ("M52", "comentario: las erratas no se comparan con las ERRONEA", "    if sorted(erratas) != sorted(erroneas):",
     "    if False:"),
    ("M53", "comentario: una errata sin corrección vale", ' or not _texto(e.get("correccion"))', ""),
    ("M54", "comentario: un caso dudoso puede no ser CORRECTA", 'if any(veredicto.get(i) != "CORRECTA" for i in dudosas):',
     "if False:"),
    ("M55", "comentario: una discutible puede no ser ERRONEA", "    if not set(discutibles) <= set(erroneas):", "    if False:"),
    ("M56", "sensibilidad: como correctas no restan de las ERRONEA", ', ERRONEA=total["ERRONEA"] - len(d))\n    sin_ellas',
     ')\n    sin_ellas'),
    ("M57", "sensibilidad: quitarlas no las quita", 'sin_ellas = dict(total, ERRONEA=total["ERRONEA"] - len(d))',
     "sin_ellas = dict(total)"),
    ("M58", "recuento por lote: todos los veredictos", '**_cuenta([str(v["veredicto"]) for v in lt["veredictos"]]),',
     "**total,"),
    ("M59", "recuento por prompt: sin los lotes de cada prompt", "        if lote_de[a[\"id\"]] not in f[\"lotes\"]:\n",
     "        if not f[\"lotes\"]:\n"),
    ("M60", "principal: con veredictos no válidos sigue", "            print(f\"veredictos no válidos: {e}\", file=sys.stderr)\n            return 2",
     "            print(f\"veredictos no válidos: {e}\", file=sys.stderr)\n            contr = None"),
    ("M61", "lotes: sin lotes sigue", "    if not archivos:\n        raise ContrasteInvalido", "    if False:\n        raise ContrasteInvalido"),
    ("M62", "lotes: orden por nombre (lote_10 antes que lote_2)", 'key=lambda p: (len(p.name), p.name)', "key=lambda p: p.name"),
    ("M63", "informe: sin escapar las barras de la frase", '.replace("|", "\\\\|")', ""),
    # QA r01 (ronda r02): H-02 a H-05 y H-07
    ("M64", "comentario: la cita no se compara con la nota", 'if not _texto(cita) or str(cita) not in str(por_id[i]["nota"]):',
     "if not _texto(cita):"),
    ("M65", "comentario: los dudosos sin el criterio del matiz", "    if sorted(dudosas) != con_matiz:", "    if False:"),
    ("M66", "comentario: una discutible sin que la nota lo diga",
     'if any(not RE_DISCUTIBLE.search(str(por_id[i]["nota"])) for i in discutibles):', "if False:"),
    ("M67", "comentario: discutibles que no son ids", "    if any(not isinstance(i, str) for i in discutibles):", "    if False:"),
    ("M68", "sensibilidad: casos que no son ERRONEA", "    if not set(sens_ids) <= set(erroneas):", "    if False:"),
    ("M69", "sensibilidad: sin motivo", ' or not _texto(sens.get("motivo"))', ""),
    ("M70", "textos: vale uno sin letras ni cifras", 'return isinstance(x, str) and re.search(r"\\w", x) is not None',
     "return isinstance(x, str) and bool(x.strip())"),
    ("M71", "lectura: traza con UTF-8 inválido o una carpeta",
     "except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:", "except json.JSONDecodeError as e:"),
    ("M72", "lotes: revisor en blanco vale", 'or not _texto(d.get("revisor")):', 'or not isinstance(d.get("revisor"), str):'),
    ("M73", "por prompt: sin la lista de los cortos", 'if f["verificables"] < MUESTRA_POR_PROMPT', 'if f["verificables"] < 0'),
    ("M74", "por prompt: las no verificables cuentan como verificables",
     '"verificables": sum(1 for x in f["vs"] if x != "NO_VERIFICABLE")', '"verificables": len(f["vs"])'),
    ("M75", "fuente: «sin búsqueda web» cuenta como búsqueda", "(?<!sin )búsqueda web", "búsqueda web"),
    ("M76", "fuente: sin «Web:»", "|\\bweb:", ""),
    ("M77", "comentario: un dudoso sin matiz vale", "    if any(not _texto(m) for m in dudosas.values()):", "    if False:"),
    ("M79", "comentario: una cita de menos de 3 palabras vale",
     'if sum(1 for w in str(cita).split() if re.search(r"\\w", w)) < MIN_PALABRAS_CITA:', "if False:"),
    ("M80", "comentario: el mínimo de palabras de la cita, sin aplicar", "MIN_PALABRAS_CITA = 3 ", "MIN_PALABRAS_CITA = 1 "),
    ("M81", "informe: sin la cita en la tabla de ERRONEA", "f\"{_celda(e['correccion'])} | {_celda(e['cita'])} |\")",
     "f\"{_celda(e['correccion'])} | |\")"),
    ("M78", "informe: la muestra sigue «sin juzgar»", 'a("## Paso 3 · Muestra")', 'a("## Paso 3 · Muestra (preparada, sin juzgar)")'),
]
EQUIVALENTES: dict[str, str] = {}


def main() -> int:
    fuente = ORIGINAL.read_text(encoding="utf-8")
    py = sys.executable
    malos = []
    with tempfile.TemporaryDirectory() as tmp:
        for mid, desc, viejo, nuevo in MUTANTES:
            if SOLO and mid not in SOLO:
                continue
            if fuente.count(viejo) != 1:
                print(f"{mid} NO APLICA ({fuente.count(viejo)} apariciones): {desc}")
                malos.append(mid)
                continue
            mut = Path(tmp) / f"{mid}.py"
            mut.write_text(fuente.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([py, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", str(PRUEBAS)],
                               env={**os.environ, "PB51_MODULO": str(mut)}, capture_output=True, text=True, check=False)
            vivo = r.returncode == 0
            estado = "VIVO (equivalente)" if vivo and mid in EQUIVALENTES else ("VIVO" if vivo else "muerto")
            print(f"{mid} {estado}: {desc}")
            if vivo and mid not in EQUIVALENTES:
                malos.append(mid)
    print(f"{len(malos)} vivos o sin aplicar: {malos}" if malos else "todos muertos")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
