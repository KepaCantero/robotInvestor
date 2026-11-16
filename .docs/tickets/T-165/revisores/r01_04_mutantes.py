"""T-165 QA r01 · mutantes del revisor sobre el código de T-165, contra las pruebas del ticket y la sonda de la QA de T-159.

Cada mutante cambia una expresión de `ht09.py`, `sintesis.py`, `redaccion.py` u `orquestacion.py` en una COPIA desechable
(nunca en el árbol de trabajo), ejecuta las pruebas con `-x` y restaura el fichero. «muerto» = alguna prueba falla; «vivo» = todas
pasan (el comportamiento cambiado no lo vigila ninguna prueba).

Uso (la copia es una exportación de HEAD con `bloque_a` y `.docs/tickets/T-159`, p. ej. `git archive HEAD bloque_a
.docs/tickets/T-159 | tar -x -C <copia>`):
    .venv/bin/python .docs/tickets/T-165/revisores/r01_04_mutantes.py --copia <copia> [--python .venv/bin/python]
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
    ("M01 negación sin «sin»", H, "(?:no|sin|nunca|jamás|ni|not|never)", "(?:no|nunca|jamás|ni|not|never)", 1),
    ("M02 negación sin auxiliares", H, "{{0,3}}", "{{0,0}}", 1),
    ("M03 plural como singular", H, 'if palabra.lower().endswith("s")', "if False", 1),
    ("M04 sin la excepción «validado por»", H, "if RE_AGENTE.match(frase[m.end():]):", "if False:", 1),
    ("M05 «documentado» no declara", H, 'declara[i] = declara[i] or nivel == "DOCUMENTADO"', "declara[i] = declara[i]", 1),
    ("M06 «no implementado» no declara", H, 'declara[i] = declara[i] or nivel == "IMPLEMENTADO"', "declara[i] = declara[i]", 1),
    ("M07 madurez del Catálogo por igualdad", H, "if e.startswith(k)", "if e == k", 1),
    ("M08 solo saltos de dos niveles", H, "if NIVELES[n] > cat]", "if NIVELES[n] > cat + 1]", 1),
    ("M09 las celdas «|» no cortan", H, r"[;!?|\n\r]", r"[;!?\n\r]", 1),
    ("M10 etiquetas en línea cortan", H, 'RE_ETIQUETA.sub("\\n", RE_EN_LINEA.sub(" ", contenido))', 'RE_ETIQUETA.sub("\\n", contenido)', 1),
    ("M11 sin el OPP- en la ruta", H, 'marca = v.get("opp_id") if isinstance(v, dict) and isinstance(v.get("opp_id"), str) else i',
     "marca = i", 1),
    ("M12 hermanos solo «metodo»", H, 'CLAVES_METODO = ("metodo", "method_id", "ficha", "operacion", "metodos")',
     'CLAVES_METODO = ("metodo",)', 1),
    ("M13 una incidencia por ruta", H, "if (ruta, ficha, detalle) not in vistas:\n            vistas.add((ruta, ficha, detalle))",
     'if (ruta, "", "") not in vistas:\n            vistas.add((ruta, "", ""))', 1),
    ("M14 empate: gana la de detrás", H, "(m[0] - fin, 1)", "(m[0] - fin, -1)", 1),
    ("M15 extracto también en advertencias", H, 'if sev == "BLOQUEO" else "")', 'if True else "")', 2),
    ("M16 METODO_NO_IMPLEMENTADO no declara", H, "|METODO_NO_IMPLEMENTADO|OPERACION_SIN_FICHA", "|OPERACION_SIN_FICHA", 1),
    ("M17 una ficha inventada no cuenta", H, ' or m.group(1).split("-", 1)[0] in prefijos]', "]", 1),
    ("M18 inglés fuera", H, "|validated)", ")", 1),
    ("M19 advertencia = bloqueo", H, 'resultado = "BLOQUEO" if "BLOQUEO" in sevs else ("ADVERTENCIA" if sevs else "OK")',
     'resultado = "BLOQUEO" if sevs else "OK"', 1),
    ("M20 AUD-REX-001 sin CT-10", S, " or (f in _servicio.SERVICIOS_CT10 and _servicio.citable_segun_catalogo(f, raiz))", "", 1),
    ("M21 candidatas no entregadas bloquean", S, 'textos += [(_RE_OPP.sub(r"opp \\1/\\2", r), t, "ADVERTENCIA")\n'
     '                           for r, t in ht09.textos_de(f, f"informes_clase.{c}.no_entregada',
     'textos += [(_RE_OPP.sub(r"opp \\1/\\2", r), t, "BLOQUEO")\n'
     '                           for r, t in ht09.textos_de(f, f"informes_clase.{c}.no_entregada', 1),
    ("M22 régimen y lagunas sin leer", S, 'for k in ("regimen", "lagunas")', "for k in ()", 1),
    ("M23 visual sin leer", S, "    if informe_visual:\n        try:", "    if False:\n        try:", 1),
    ("M24 dictamen sin advertencias", S, "if bloqueos or advert:", "if bloqueos:", 1),
    ("M25 técnico nunca bloquea", S, '    if not comp["incidencias"]:\n        return False', "    if True:\n        return False", 1),
    ("M26 no entregada con OPP- en la ruta", S, 'textos += [(_RE_OPP.sub(r"opp \\1/\\2", r), t, "ADVERTENCIA")\n'
     '                           for r, t in ht09.textos_de(f, f"informes_clase.{c}.no_entregada',
     'textos += [(r, t, "ADVERTENCIA")\n'
     '                           for r, t in ht09.textos_de(f, f"informes_clase.{c}.no_entregada', 1),
    ("M27 ninguna candidata es opción", S, 'if f.get("opp_id") in opciones:', "if False:", 1),
    ("M28 candidata entregada solo advierte", S,
     'textos += [(r, t, "BLOQUEO") for r, t in ht09.textos_de(f, f"informes_clase.{c}[{f[\'opp_id\']}]")]',
     'textos += [(r, t, "ADVERTENCIA") for r, t in ht09.textos_de(f, f"informes_clase.{c}[{f[\'opp_id\']}]")]', 1),
    ("M29 paquete sin leer", S, 'textos = [(r, t, "BLOQUEO") for r, t in ht09.textos_de(paquete, "paquete")]', "textos = []", 1),
    ("M30 rótulo antiguo siempre", R, 'if "clusteres_calc_id" in extras and not extras["clusteres_calc_id"]:', "if False:", 1),
    ("M31 el técnico no entra en los bloqueos", R, '        bloq.append("G3-MET-13")', "        pass", 1),
    ("M32 limitación antigua", O, '"el resto tampoco se agrupa (ML-CLUS-001 rechazado)" if clusteres.get("rechazo")',
     '"el resto tampoco se agrupa (ML-CLUS-001 rechazado)" if False', 1),
]

PRUEBAS = ["tests/test_t165_g3_met13.py", "../../.docs/tickets/T-159/revisores/r01_02_sondas.py::"
           "test_h01_pb47_un_informe_que_llama_validado_al_metodo_documentado_no_se_entrega_asi",
           "tests/test_t159_extremo_a_extremo.py"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--copia", required=True)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--solo", nargs="*")
    a = ap.parse_args()
    copia = Path(a.copia).resolve()
    ejec = copia / "bloque_a/11_Ejecutor"
    vivos = []
    for nombre, fich, viejo, nuevo, veces in MUTANTES:
        if a.solo and nombre.split()[0] not in a.solo:
            continue
        p = copia / fich
        original = p.read_text(encoding="utf-8")
        assert original.count(viejo) == veces, f"{nombre}: «{viejo}» aparece {original.count(viejo)} veces"
        try:
            p.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([a.python, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *PRUEBAS], cwd=ejec,
                               capture_output=True, text=True, timeout=3600)
        finally:
            p.write_text(original, encoding="utf-8")
        muerto = r.returncode != 0
        primera = next((ln for ln in r.stdout.splitlines() if ln.startswith("FAILED")), "")[:160]
        print(f"{nombre:45s} {'muerto' if muerto else 'VIVO'}  {primera}", flush=True)
        if not muerto:
            vivos.append(nombre)
    print("vivos:", vivos or "ninguno")
    return 0


if __name__ == "__main__":
    sys.exit(main())
