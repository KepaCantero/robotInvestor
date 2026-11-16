"""QA r01 de T-157 · mutantes del revisor contra `tests/test_t157_verificador_ids.py`.

Cada mutante cambia un trozo del código fuente del verificador (se recompila en el espacio de nombres del módulo desde un
`conftest` temporal; el archivo del módulo no se toca) y se ejecuta el archivo de pruebas entero. MATADO = alguna prueba falla
por una aserción («failed»); VIVO = todo pasa; ROTO = el mutante no se aplica o la recogida falla. El nulo es el control.
Sale 1 si el nulo no queda vivo o algún mutante no se aplica; los VIVOS se informan (son hallazgos, no fallos del script).

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_03_mutantes.py
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EJ = Path.cwd()
MOD = EJ / "bloque_a/herramientas/verificador_ids.py"
FUENTE = MOD.read_text(encoding="utf-8")
CONF = EJ / "tests/conftest_mutante_r01.py"

MUTANTES = {
    "M00 nulo (control)": ("", ""),
    "M01 sin FILA_DUPLICADA (§1, §6.1, §9.3)": ("sorted({d for d in definidos if definidos.count(d) > 1}", "sorted(set()"),
    "M02 sin FICHA_DUPLICADA del Catálogo": ("if m.group(1) in encabezados:", "if False:"),
    "M03 sin TOTAL_DISTINTO": ("if total is not None and total != len(encabezados):", "if False:"),
    "M04 CT_SOLO_CODIGO solo mira CANALES": ('("CANALES_V6", codigo.canales_v6),\n                             ("CAMPOS_MINIMOS", '
                                            'codigo.campos_minimos)', ""),
    "M05 sin FICHA_DUPLICADA_CODIGO": ("if lista_codigo.count(f) > 1}", "if False}"),
    "M06 sin ALTERNATIVA_SIN_FICHA": ("            if y not in cat_ids:", "            if False:"),
    "M07 sin REF_DEFINIDA_Y_DE_BAJA": ("for x in sorted(set(definidas) & set(bajas), key=_clave_id):",
                                       "for x in []:"),
    "M08 sin FALTA_EN_FICHAS_CATALOGO": ('if x in cat_ids and x not in en_lista and clase != "ID_DISTINTO":', "if False:"),
    "M09 desde_paquete no busca versiones en los .py": ("versiones.append((rel, n, m.group(1) or m.group(2), m.group(2) is not None))",
                                                        "pass"),
    "M10 campo JSON excusa también ficha_id": ("if m and m.group(1) not in CAMPOS_FICHA:", "if m:"),
    "M11 el H1 de 05 cuenta como cita F": ('c.texto.startswith("# "))', "False)"),
    "M12 lee carpetas que empiezan por punto": ('p.startswith((PREFIJO_HISTORICO, "."))', "p.startswith(PREFIJO_HISTORICO)"),
    "M13 main sale 0 con errores": ('return 1 if informe["errores"] else 0', "return 0"),
    "M14 _unico sin NFC": ("patron.match(_nfc(p.name))", "patron.match(p.name)"),
    "M15 sin CT_CANAL_VACIO": ("(codigo.canales & set(ct_def)) - codigo.canales_admitidos", "set()"),
    "M16 SOLO_CATALOGO siempre AVISO": ('nivel = "ERROR" if madurez and _citable(madurez) else "AVISO"', 'nivel = "AVISO"'),
    "M17 sin FUERA_DE_RANGO": ("for x in sorted(set(definidos) - set(esperado), key=_clave_id):", "for x in []:"),
    "M18 contextos sin su INFO (se esconden)": ("for motivo, cs in sorted(explicadas.items()):", "for motivo, cs in []:"),
    "M19 sin VERSION_DOC0_DISTINTA": ("if v_nombre is None or v_titulo is None or v_nombre != v_titulo:", "if False:"),
    "M20 validar_informe no comprueba «errores»": ('if informe["errores"] != sum(informe["resumen"][c]["ERROR"] for c in CLASES):',
                                                   "if False:"),
    "M21 auditoría con marcas repetidas": ("texto.count(MARCA_INICIO) != 1 or texto.count(MARCA_FIN) != 1", "False"),
    "M22 sin REF_FORMA_DISTINTA": ("elif p in cifras and len(num) not in cifras[p]:", "elif False:"),
    "M23 99_Historico solo en el primer nivel": ("for p in rel.parts[:-1])", "for p in rel.parts[:1])"),
    "M24 secciones «nuevas» sin mirar la versión": ('bool(v_nombre and f"V{v_nombre}" in s["titulo"])', "True"),
    "M25 CATALOG_VERSION_LITERAL como AVISO": ('h("d", "ERROR", "CATALOG_VERSION_LITERAL"', 'h("d", "AVISO", "CATALOG_VERSION_LITERAL"'),
    "M26 orden de hallazgos sin desempate": ('_clave_id(h["id"]),\n                                                 h["codigo"]))',
                                             '_clave_id(h["id"])))'),
    "M27 REF_DE_BAJA cuenta como existente": ("        if x in definidas:\n            continue",
                                              "        if x in definidas or x in bajas:\n            continue"),
}

PLANTILLA = """import bloque_a.herramientas.verificador_ids as vi
_src = open(vi.__file__, encoding="utf-8").read()
_viejo, _nuevo = {viejo!r}, {nuevo!r}
if _viejo:
    assert _src.count(_viejo) == 1, "el mutante no se aplica"
    exec(compile(_src.replace(_viejo, _nuevo), vi.__file__, "exec"), vi.__dict__)
"""

vivos, rotos = [], []
try:
    for nombre, (viejo, nuevo) in MUTANTES.items():
        if viejo and FUENTE.count(viejo) != 1:
            print(f"{nombre:52s} -> ROTO (el texto aparece {FUENTE.count(viejo)} veces)")
            rotos.append(nombre)
            continue
        CONF.write_text(PLANTILLA.format(viejo=viejo, nuevo=nuevo), encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "tests.conftest_mutante_r01",
                            "tests/test_t157_verificador_ids.py"], cwd=EJ, capture_output=True, text=True, timeout=900)
        ultima = (r.stdout.strip().splitlines() or [""])[-1]
        fallidas = re.findall(r"^FAILED tests/test_t157_verificador_ids.py::(\S+)", r.stdout, re.M)
        if r.returncode == 0:
            estado = "VIVO"
            if viejo:
                vivos.append(nombre)
        elif r.returncode == 1 and fallidas:
            estado = "MATADO"
        else:
            estado = "ROTO"
            rotos.append(nombre)
        print(f"{nombre:52s} -> {estado:6s} {ultima[:60]} {','.join(f[:40] for f in fallidas[:2])}")
finally:
    if CONF.exists():
        os.remove(CONF)

print(f"\nVivos ({len(vivos)}): {vivos}\nRotos ({len(rotos)}): {rotos}")
sys.exit(1 if rotos or "M00 nulo (control)" in vivos else 0)
