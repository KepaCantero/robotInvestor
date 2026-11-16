"""T-161 · Mutantes de las correcciones de T-161 (M01–M14) y de su r02 (M15–M26) sobre `guias.py`, para confirmar que cada prueba nueva falla sin
su corrección (regresión). M04 se cambió en la r02 (la comprobación de escritura es otra).

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
PRUEBAS = ["tests/test_t161_guias.py", "tests/test_t161_r02.py"]
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
    ("M07", "H-01 sin la familia IDIOMA", "    if idioma:\n", "    if False:\n"),
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
    ("M19", "r02 H-02 sin leer las cifras como letras", "return [v] if v != t else []", "return []"),
    ("M20", "r02 H-02 sin condiciones en los campos descriptivos",
     "condicion = None if estricto else (REFUERZA.search(t) and NIEGA.search(t))", "condicion = None"),
    ("M21", "r02 H-02 sin «con una fuente» junto a la tesis", " or (MULTIPLICIDAD.search(t) if SUFICIENCIA.search(t) else None)", ""),
    ("M22", "r02 H-02 sin R9", '(RE_INYECCION, "INYECCION",', '(re.compile("(?!)"), "INYECCION",'),
    ("M23", "r02 H-02 sin retirar la guía comprometida", "if any(COMPROMETEN & set(c[\"familias\"]) for _, c in conflictos):",
     "if False:"),
    ("M24", "r02 H-01 AG-20 fuera de los agentes de control",
     '                      "AG-20": "aprendizaje: sus lecciones llegan como contexto a todos los agentes",\n', ""),
    ("M25", "r02 H-01 las lecciones de AG-20 sin detector", "            conflicto = conflicto_de_leccion(l)\n",
     "            conflicto = None\n", OR),
    ("M26", "r02 H-05 sin longitud máxima", 'if len(it[campo]) > lim["max_caracteres_por_texto"]:', "if False:"),
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
