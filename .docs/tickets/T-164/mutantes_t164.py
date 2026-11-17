"""T-164 · mutantes de las correcciones de H-09, H-10 y H-11 contra `tests/test_t157_verificador_ids.py` (el archivo entero).

Cada mutante cambia un trozo del código fuente del verificador y lo recompila en el espacio de nombres del módulo desde un
`conftest` temporal (el archivo del módulo no se toca), como `.docs/tickets/T-157/revisores/r02_02_mutantes.py`. MATADO = alguna
prueba falla por una aserción; VIVO = todo pasa; ROTO = el mutante no se aplica o la recogida falla. El nulo es el control.
Sale 1 si el nulo no queda vivo, si un mutante queda vivo o si alguno no se aplica.

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-164/mutantes_t164.py
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EJ = Path.cwd()
MOD = EJ / "bloque_a/herramientas/verificador_ids.py"
FUENTE = MOD.read_text(encoding="utf-8")
CONF = EJ / "tests/conftest_mutante_t164.py"

MUTANTES = {
    "T00 nulo (control)": ("", ""),
    # H-09: la excusa del símbolo, por aparición y contexto
    "T01 el símbolo excusa todas sus apariciones (antes de T-164)": (
        "if x not in simbolos or _como_ficha(c, _campo_json(c)):", "if x not in simbolos:"),
    "T02 sin campos de ficha": ('CAMPOS_FICHA = ("ficha_id", "method_id", "operacion", "estado_madurez_metodos")',
                                "CAMPOS_FICHA = ()"),
    "T03 sin estado_madurez_metodos": ('"operacion", "estado_madurez_metodos")', '"operacion")'),
    "T04 «ficha» no cuenta": ('RE_PALABRA_FICHA = re.compile(r"\\bfichas?\\b", re.IGNORECASE)',
                              'RE_PALABRA_FICHA = re.compile(r"(?!x)x")'),
    "T05 la frase no acaba en «.»": ('[.!?](?=\\s)",', '(?!x)x",'),
    "T06 la frase no empieza en la clave JSON": ("+ [campo[1] if campo else 0])", "+ [0])"),
    "T07 sin arrays JSON": ('(?:"([^"]*)"|\\[([^\\]\\[{}]*)\\])', '(?:"([^"]*)")'),
    # r02 de T-164 (QA r01: H-01, H-02, H-04, H-05)
    "T15 el array se traga los objetos (antes de la r02)": ("\\[([^\\]\\[{}]*)\\]", "\\[([^\\]]*)\\]"),
    "T16 la frase de un valor JSON empieza en el valor": ("            return m.group(1), m.start()\n",
                                                          "            return m.group(1), m.start(g)\n"),
    "T17 «;» corta la frase": ("(?<!\\bnúm)[.!?](?=\\s)", "(?<!\\bnúm)[.;!?](?=\\s)"),
    "T18 sin abreviaturas": ('r"(?<!\\bp)(?<!\\bej)(?<!\\be\\.g)(?<!\\bi\\.e)(?<!\\bvs)(?<!\\bcf)(?<!\\bpág)(?<!\\bnúm)[.!?]', 'r"[.!?]'),
    "T19 destino repetido sin comprobar": ("    if len(set(destinos)) != len(destinos):", "    if False:"),
    "T20 sin conservar los permisos": ("                os.chmod(tmp, stat.S_IMODE(ruta.stat().st_mode))\n",
                                       "                pass\n"),
    "T08 familia desconocida: el símbolo se omite entero": ("        if not resto:\n            continue\n",
                                                            "        if x in simbolos or not resto:\n            continue\n"),
    "T09 familia desconocida: sin excusa por aparición": ("resto = [c for c, m in motivos.items() if not m]",
                                                          "resto = list(otras[x])"),
    # H-10: otras cifras finales
    "T10 sin fichas de otras cifras": ("(?:\\d{{1,2}}|\\d{{4,}})", "\\d{{3}}"),
    "T11 solo una o dos cifras": ("|\\d{{4,}})", ")"),
    "T12 sin el aviso de otras cifras en el mensaje": (
        '("" if re.fullmatch(RE_ID_FICHA, x) else " (con otro número de cifras finales que las fichas del Catálogo)")', '""'),
    # H-11: escritura en grupo
    "T13 renombra cada temporal nada más escribirlo (antes de T-164)": (
        ('            temporales[-1].write_text(texto, encoding="utf-8")\n'
         "        for (ruta, _), tmp in zip(salidas, temporales, strict=True):\n"),
        ('            temporales[-1].write_text(texto, encoding="utf-8")\n            os.replace(temporales[-1], ruta)\n'
         "        for (ruta, _), tmp in zip([], [], strict=True):\n")),
    "T14 no borra los temporales": ("                tmp.unlink(missing_ok=True)\n", "                pass\n"),
}

PLANTILLA = """import bloque_a.herramientas.verificador_ids as vi
_src = open(vi.__file__, encoding="utf-8").read()
_viejo, _nuevo = {viejo!r}, {nuevo!r}
if _viejo:
    assert _src.count(_viejo) == 1, "el mutante no se aplica"
    exec(compile(_src.replace(_viejo, _nuevo), vi.__file__, "exec"), vi.__dict__)
"""

vivos, rotos, nulo = [], [], None
try:
    for nombre, (viejo, nuevo) in MUTANTES.items():
        if viejo and FUENTE.count(viejo) != 1:
            print(f"{nombre:62s} -> ROTO (el texto aparece {FUENTE.count(viejo)} veces)")
            rotos.append(nombre)
            continue
        CONF.write_text(PLANTILLA.format(viejo=viejo, nuevo=nuevo), encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "tests.conftest_mutante_t164",
                            "tests/test_t157_verificador_ids.py"], cwd=EJ, capture_output=True, text=True, timeout=900, check=False)
        fallidas = re.findall(r"^FAILED tests/test_t157_verificador_ids.py::(\S+)", r.stdout, re.MULTILINE)
        if r.returncode == 0:
            estado = "VIVO"
            if viejo:
                vivos.append(nombre)
            else:
                nulo = estado
        elif r.returncode == 1 and fallidas:
            estado = "MATADO"
        else:
            estado = "ROTO"
            rotos.append(nombre)
        print(f"{nombre:62s} -> {estado:6s} {','.join(f[:44] for f in fallidas[:2])}")
finally:
    if CONF.exists():
        os.remove(CONF)

print(f"\nVivos ({len(vivos)}): {vivos}\nRotos ({len(rotos)}): {rotos}")
sys.exit(1 if vivos or rotos or nulo != "VIVO" else 0)
