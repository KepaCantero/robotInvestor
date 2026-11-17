"""T-165 r02 · mutantes del implementador sobre el código de la r02, contra las pruebas del ticket.

Los nueve que vivían en la r01 (r01_04: M01, M03, M09, M12, M13, M14, M15, M20 y M32), con la expresión equivalente del código
nuevo, y uno por cada regla que añade la r02 (H-01 a H-11). Cada mutante cambia una expresión en una COPIA desechable (nunca en el
árbol de trabajo), ejecuta `tests/test_t165_g3_met13.py` con `-x` y restaura el fichero. «muerto» = alguna prueba falla.

H-24 (QA r02): N13 y N17 con la expresión que de verdad tiene el código de la r02. Desde la r03 el código es otro: este script
se ejecuta sobre una exportación del commit de la r02 (`git archive`), y los mutantes de la r03 están en `r03_mutantes.py`.

Uso (la copia es una copia de `bloque_a` del árbol de trabajo, p. ej. `cp -r bloque_a <copia>/`):
    .venv/bin/python .docs/tickets/T-165/r02_mutantes.py --copia <copia> [--python .venv/bin/python] [--solo M01 M03]
"""
import argparse
import subprocess
import sys
from pathlib import Path

H = "bloque_a/11_Ejecutor/bloque_a/herramientas/ht09.py"
S = "bloque_a/11_Ejecutor/bloque_a/sintesis.py"
R = "bloque_a/11_Ejecutor/bloque_a/redaccion.py"
O = "bloque_a/11_Ejecutor/bloque_a/orquestacion.py"

MUTANTES = [
    # los nueve vivos de la r01
    ("M01 negación sin «sin»", H, '_NIEGA = frozenset(("no", "sin", "nunca"', '_NIEGA = frozenset(("no", "nunca"'),
    ("M03 plural como singular", H, 'palabra.endswith(("s", "aron", "arán"))', "False"),
    ("M09 las celdas «|» no cortan la frase", H, r'RE_SEPARADOR = re.compile(r"\.(?=\s)|[;!?|\n]")',
     r'RE_SEPARADOR = re.compile(r"\.(?=\s)|[;!?\n]")'),
    ("M12 hermanos solo «metodo»", H,
     'CLAVES_METODO = ("metodo", "method", "method_id", "ficha", "ficha_id", "id", "operacion", "metodos", "methods", "calculo")',
     'CLAVES_METODO = ("metodo",)'),
    ("M13 una incidencia por ruta", H, "if (ruta, ficha, regla) not in vistas:\n            vistas.add((ruta, ficha, regla))",
     'if (ruta, "", "") not in vistas:\n            vistas.add((ruta, "", ""))'),
    ("M14 empate: gana la de detrás", H, "return [izq] if ini - menciones[izq][1] <= menciones[der][0] - fin else [der]",
     "return [izq] if ini - menciones[izq][1] < menciones[der][0] - fin else [der]"),
    ("M15 extracto también en advertencias", H, '(f": «{extracto(pos)}»" if sev == "BLOQUEO" else "")',
     '(f": «{extracto(pos)}»" if True else "")'),
    ("M20 AUD-REX-001 sin CT-10", S, "                      or (f in _servicio.SERVICIOS_CT10 and _servicio.citable_segun_catalogo(f, raiz)))",
     "                      or False)"),
    ("M32 limitación antigua de «sin historia»", O,
     '"el resto tampoco se agrupa (ML-CLUS-001 rechazado)" if clusteres.get("rechazo")',
     '"el resto tampoco se agrupa (ML-CLUS-001 rechazado)" if False'),
    # las reglas de la r02
    ("N01 H-01 «validado por los datos» vuelve a excluirse", H, "|inversor(?:a|es|as)?)(?!\\w)\")",
     "|inversor(?:a|es|as)?|datos?|mercados?|evidencias?|fuentes?)(?!\\w)\")"),
    ("N02 H-02 sin la unidad: solo la frase", H, "if fi in por_frase else (todas, mini)", "if fi in por_frase else ([], [])"),
    ("N03 H-02 sin el párrafo anterior", H, "            elif anterior and not tabla:", "            elif False:"),
    ("N04 H-03 sin formas verbales", H, r"|(?:re)?valid(?:ó|aron|an|a|amos|ará|arán|aría)", ""),
    ("N05 H-03 sin sinónimos", H, r"|verified|probad[oa]s?|proven|tested|testead[oa]s?|contrastad[oa]s?|comprobad[oa]s?", ""),
    ("N06 H-03 sin «validación superada»", H, "        if not exito or _negada(", "        if True or _negada("),
    ("N07 H-04 sin guiones tipográficos", H, 'elif c in _GUIONES or cat == "Pd":', "elif False:"),
    ("N08 H-04 sin fichas con espacios", H, "        for m in self.re_espacios.finditer(t):", "        for m in []:"),
    ("N09 H-04 sin parciales", H, "        for m in self.re_parcial.finditer(t):", "        for m in []:"),
    ("N10 H-05 sin registros de método", H,
     "registro = bool(de_ficha) or fuerte or (debil and any(_es_ficha(v, fx) for v in obj.values()))", "registro = False"),
    ("N11 H-07 sin prosa financiera", H, "    if RE_LIGADO_DESPUES.match(t[fin:fin + VENTANA]):\n        return True",
     "    return False"),
    ("N12 H-07 tres auxiliares", H, "MAX_AUX = 6", "MAX_AUX = 3"),
    ("N13 H-07 sin «pendiente de»", H, ' or (w == "de" and previo in _NIEGA_DE)', ""),
    ("N14 H-09 el extracto lleva el OPP-", H, 'return RE_OPP_TEXTO.sub(r"opp \\1/\\2", t[max(cortes[fi], u0):fin].strip()[:160])',
     "return t[max(cortes[fi], u0):fin].strip()[:160].upper()"),
    ("N15 H-11 sin quitar los Cf", H, '        elif cat == "Cf":\n            continue', '        elif False:\n            continue'),
    ("N16 H-11 sin homoglifos", H, "            out.append(_HOMOGLIFOS.get(c, c))", "            out.append(c)"),
    ("N17 H-11 sin doble negación", H, "return not any(x in _DOBLE for x, _ in tokens[:j])", "return True"),
    ("N18 H-11 sin atributos HTML", H, 'return _html.unescape("\\n\\n".join([t, *atributos]))', "return _html.unescape(t)"),
    ("N19 H-06 factor_dominante siempre con ML-CLUS-001", S, 'if clusteres.get("calc_id") else   # T-165 r02', "if True else   # T-165 r02"),
    ("N21 la ficha entre negación y palabra no se salta", H, "        if en_ficha[j] and (ficha_saltada is False or en_ficha[j + 1]):",
     "        if False:"),
    ("N22 sin sujetos que no son un método", H, '"máximos probabilidad probabilidades estrategia estrategias dato datos', '"máximos probabilidad probabilidades'),
    ("N20 H-06 riesgo siempre RISK-DD-001", R, '    if o.get("opp_id") in (extras.get("riesgo_sin_motor") or ()):', "    if False:"),
]

PRUEBAS = ["tests/test_t165_g3_met13.py"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--copia", required=True)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--solo", nargs="*")
    a = ap.parse_args()
    copia = Path(a.copia).resolve()
    ejec = copia / "bloque_a/11_Ejecutor"
    vivos = []
    for nombre, fich, viejo, nuevo in MUTANTES:
        if a.solo and nombre.split()[0] not in a.solo:
            continue
        p = copia / fich
        original = p.read_text(encoding="utf-8")
        assert original.count(viejo) == 1, f"{nombre}: «{viejo[:60]}» aparece {original.count(viejo)} veces"
        try:
            p.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([a.python, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *PRUEBAS], cwd=ejec,
                               capture_output=True, text=True, timeout=3600, check=False)
        finally:
            p.write_text(original, encoding="utf-8")
        muerto = r.returncode != 0
        primera = next((ln for ln in r.stdout.splitlines() if ln.startswith("FAILED")), "")[:150]
        print(f"{nombre:52s} {'muerto' if muerto else 'VIVO'}  {primera}", flush=True)
        if not muerto:
            vivos.append(nombre)
    print("vivos:", vivos or "ninguno")
    return 0


if __name__ == "__main__":
    sys.exit(main())
