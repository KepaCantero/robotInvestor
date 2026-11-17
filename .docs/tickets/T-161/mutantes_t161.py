"""T-161 · Mutantes de las correcciones de T-161 (M01–M14), de su r02 (M15–M26), de su r03 (M27–M38), de su r04 (M39–M52) y de la ronda de cierre (M53–M55) sobre `guias.py`,
para confirmar que cada prueba nueva falla sin su corrección (regresión). M04 se cambió en la r02 (la comprobación de escritura es otra);
M19, M20 y M25, en la r03 (cambió la línea); M07 y M34, en la r04 (la familia IDIOMA se decide con `ajeno`; el enmascarado ya no
depende del verbo, sino de `_solo_muestra` para lo que coincide con un parámetro).

Uso, desde la raíz: python .docs/tickets/T-161/mutantes_t161.py <copia desechable con «qa29_» y «_mut» y `bloque_a/` entero>
Cada mutante se aplica en la copia, se pasan `PRUEBAS` (con -x) y se restaura. Vivo = ninguna prueba lo
detecta. Termina con 1 si alguno no aplica o vive.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa29_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
GU = "bloque_a/11_Ejecutor/bloque_a/guias.py"
OR = "bloque_a/11_Ejecutor/bloque_a/orquestacion.py"
PRUEBAS = ["tests/test_t161_guias.py", "tests/test_t161_r02.py", "tests/test_t161_r03.py", "tests/test_t161_r04.py"]
MUTANTES = [
    ("M01", "H-01 sin NFKC", 't = unicodedata.normalize("NFKC", str(texto))', "t = str(texto)"),
    ("M02", "H-01 sin quitar los caracteres de formato", 'for c in t if unicodedata.category(c) != "Cf")', "for c in t)"),
    ("M03", "H-01 guiones y subrayados sin unificar", '" " if c == "_" or unicodedata.category(c) == "Pd" or c in "\\u2212\\u2043" else c',
     "c"),
    ("M04", "H-01 r02: las letras latinas sin base ASCII (ø, ı, ł) se permiten", 'elif not unicodedata.normalize("NFKD", c)[0].isascii():',
     "elif False:"),
    ("M05", "H-01 sin la familia NOMBRA_CONTROL", '    if nombrados:\n', "    if False:\n"),
    ("M06", "H-01 el refuerzo no mira las marcas de negación", "not (NIEGA.search(t) or RELAJA.search(t) or REBAJA_IMPLICITA.search(t))",
     "not (RELAJA.search(t) or REBAJA_IMPLICITA.search(t))"),
    ("M07", "H-01 sin la familia IDIOMA", "        if ajeno:\n", "        if False:\n"),
    ("M08", "H-01 sin rebajas implícitas", "    if implicita:\n", "    if False:\n"),
    ("M09", "H-02 solo se revisa que_cambia", "    for campo in CAMPOS_TEXTO[1:]:\n", "    for campo in ():\n"),
    ("M10", "H-04 sin agentes de control", 'AGENTES_DE_CONTROL = {"AG-11"', 'AGENTES_DE_CONTROL = {} and {"AG-11"'),
    ("M11", "H-03 sin reutilizar el COR- previo", "            previo = previos.get((gid, it[\"item_id\"]))\n",
     "            previo = None\n"),
    ("M12", "H-05 el emisor no revisa", "            if rechazos and not simular_fallo_del_emisor:\n", "            if False:\n"),
    ("M13", "H-05 la simulación con cualquier cliente", "if simular_fallo_del_emisor and not isinstance(self.b.cliente, MockClient):",
     "if False:"),
    ("M14", "H-06 sin la excepción de la agenda de vigilancia", "if estricto and not AGENDA.search(t) else None",
     "if estricto else None"),
    ("M15", "r02 H-02 sin símbolos permitidos (€, %, «»…)", "c.isascii() or c in SIMBOLOS_PERMITIDOS or", "c.isascii() or"),
    ("M16", "r02 H-03 sin enmascarar los sentidos financieros", 't = FINANCIERO.sub(" termino financiero ", t)', "t = t"),
    ("M17", "r02 H-03 IDIOMA cuenta los nombres propios", 't = _NOMBRE_PROPIO.sub(" ", t)', "t = t"),
    ("M18", "r02 H-03 IDIOMA cuenta las siglas", 't = _SIGLA.sub(" ", t)', "t = t"),
    ("M19", "r02 H-02 sin otras lecturas del texto", "return [x for x in dict.fromkeys(otras) if x != t]", "return []"),
    ("M20", "r02 H-02 sin condiciones en los campos descriptivos",
     "condicion = None if estricto else ((REFUERZA.search(t) or NEUTRO.search(t)) and NIEGA.search(t))", "condicion = None"),
    ("M21", "r02 H-02 sin «con una fuente» junto a la tesis", " or (MULTIPLICIDAD.search(t) if SUFICIENCIA.search(t) else None)", ""),
    ("M22", "r02 H-02 sin R9", '(RE_INYECCION, "INYECCION",', '(re.compile("(?!)"), "INYECCION",'),
    ("M23", "r02 H-02 sin retirar la guía comprometida", "if any(COMPROMETEN & set(c[\"familias\"]) for _, c in conflictos):",
     "if False:"),
    ("M24", "r02 H-01 AG-20 fuera de los agentes de control",
     '                      "AG-20": "aprendizaje: sus lecciones llegan como contexto a todos los agentes",\n', ""),
    ("M25", "r02 H-01 las lecciones de AG-20 sin detector al escribir",
     '            conflicto = conflicto_de_leccion({**l, "tipo": l.get("tipo", "PREDICTIVA"), "ambito": l.get("ambito") or {}}, self.cfg)\n',
     "            conflicto = None\n", OR),
    ("M26", "r02 H-05 sin longitud máxima", 'if len(it[campo]) > lim["max_caracteres_por_texto"]:', "if False:"),
    ("M27", "r03 H-06 los controles reciben lecciones de un modelo",
     "if agente in AGENTES_DE_CONTROL and r.get(\"origen\") != ORIGEN_DETERMINISTA:", "if False:"),
    ("M28", "r03 H-06 sin detector al leer", "self._veredictos[clave] = conflicto_de_leccion(leccion, self.b.cfg)",
     "self._veredictos[clave] = None"),
    ("M29", "r03 H-06 sin validar el tipo", "if leccion.get(\"tipo\") not in TIPOS_LECCION:", "if False:"),
    ("M30", "r03 H-06 sin validar las claves del ámbito", "        if fuera:\n", "        if False:\n"),
    ("M31", "r03 H-06 una lección que no está en F6 se da", "            if r is None:\n                continue\n",
     "            if r is None:\n                r = l\n"),
    ("M32", "r03 H-08 sin enmascarar lo que endurece", '_enmascarar_crudo(v, ENDURECE, " endurece ") if v else v', "v"),
    ("M33", "r03 H-07 los verbos neutros eximen siempre",
     "claro = REFUERZA.search(t) or (NEUTRO.search(t) and not any(r in NUCLEO for _, r in _controles(t)))",
     "claro = REFUERZA.search(t) or NEUTRO.search(t)"),
    ("M34", "r04 H-12 lo que coincide con un parámetro se enmascara aunque no solo se muestre", "if _solo_muestra(entero):",
     "if True:"),
    ("M35", "r03 H-07 sin palabras fuertes de otra lengua", "idioma = idioma or IDIOMA_FUERTE.search(entero)", "idioma = idioma"),
    ("M36", "r03 H-07 sin texto codificado", "codigo = _codificado(_texto(item.get(campo)))", "codigo = []"),
    ("M37", "r03 H-06 sin revisión de las lecciones en el F0", "self._revisar_lecciones(hoy, run_id, clave)", "pass"),
    ("M38", "r03 H-06 si la revisión de las lecciones falla, se dan igual",
     'if (run_id or "", hoy.isoformat()) in self._lecciones_caidas or not lecciones:', "if not lecciones:"),
    ("M39", "r04 H-11 un agente de control recibe lecciones de PRODUCTO del código",
     'if agente in AGENTES_DE_CONTROL and r.get("tipo") not in TIPOS_TEXTO_DEL_CODIGO:', "if False:"),
    ("M40", "r04 H-11 sin respetar ambito.agente",
     "if destinatarios is not None and (not isinstance(destinatarios, list) or agente not in destinatarios):", "if False:"),
    ("M41", "r04 H-11 las de PRODUCTO del código sin detector", "if _texto_del_codigo(leccion):",
     'if leccion.get("origen") == ORIGEN_DETERMINISTA:'),
    ("M42", "r04 H-15 el origen del estado consolidado", 'r = altas.get(str(l.get("id"))) if isinstance(l, dict) else None',
     'r = self.b.almacen.estado("F6", hoy, clave="id").get(l.get("id")) if isinstance(l, dict) else None'),
    ("M43", "r04 H-15 una lección alterada después se da igual", 'if alta.get("alterada"):', "if False:"),
    ("M44", "r04 H-12 una rebaja sobre una frase financiera pierde los controles que nombra",
     "if RELAJA.search(t):   # T-161 r04: una rebaja", "if False:   # T-161 r04: una rebaja"),
    ("M45", "r04 H-12 una orden de refuerzo sobre el núcleo se puede acotar",
     "if claro and nucleo and ((ACOTA.search(a) and not AMPLIA.search(t)) or REDUCE.search(a)):", "if False:"),
    ("M46", "r04 H-13 los verbos de presentar no eximen al núcleo",
     "claro = claro or (PRESENTA.match(a) and not REDUCE.search(a))", "claro = claro"),
    ("M47", "r04 H-12 los verbos de presentar eximen aunque reduzcan",
     "claro = claro or (PRESENTA.match(a) and not REDUCE.search(a))", "claro = claro or PRESENTA.match(a)"),
    ("M48", "r04 H-12 el núcleo sin las reglas de datos, la confianza ni las limitaciones",
     '"6.9 (reglas de datos)", "R10 y R12 (clasificación de la evidencia y confianza)", "R7 (limitaciones declaradas)",', ""),
    ("M49", "r04 H-12 sin exigir castellano", "ajeno = idioma.group(0) if idioma else _sin_castellano(crudo or \"\", t)",
     "ajeno = idioma.group(0) if idioma else None"),
    ("M50", "r04 H-12 los campos descriptivos no dicen cómo se comprueba", 'if not leccion and campo != "origen":', "if False:"),
    ("M51", "r04 H-13 la carencia se enmascara aunque la recomendación no refuerce",
     "and (_refuerza(rec) or ENDURECE.search(rec))", "and True"),
    ("M52", "r04 H-13 descartar una oportunidad cuenta como rebaja", "(?:descart|exclu|retir)\\w* (?:las |los |la |el )?(?:candidat",
     "(?:xdescart|xexclu|xretir)\\w* (?:las |los |la |el )?(?:candidat"),
    ("M53", "cierre H-17 las entradas posteriores sin tipo_entrada no se comparan", "            if isinstance(e.get(\"id\"), str) and e[\"id\"]:",
     "            if isinstance(e.get(\"id\"), str) and e[\"id\"] and e.get(\"tipo_entrada\") == \"LEC\":"),
    ("M54", "cierre H-17 fuerza y fecha como campos de ciclo de vida", 'CAMPOS_DE_CICLO_DE_VIDA = ("estado", "caducidad")',
     'CAMPOS_DE_CICLO_DE_VIDA = ("estado", "caducidad", "fuerza", "fecha")'),
    ("M55", "cierre H-17 se da al agente la lección consolidada",
     "out.append({k: copy.deepcopy(r.get(k)) for k in CAMPOS_PARA_EL_AGENTE})", "out.append(l)"),
]


def main() -> int:
    ej = COPIA / "bloque_a" / "11_Ejecutor"
    sin_aplicar, vivos = [], []
    for mid, que, viejo, nuevo, *ruta in MUTANTES:
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
    print(f"{len(MUTANTES) - len(vivos) - len(sin_aplicar)}/{len(MUTANTES)} muertos; vivos: {', '.join(vivos) or 'ninguno'}; "
          f"sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar or vivos else 0


if __name__ == "__main__":
    sys.exit(main())
