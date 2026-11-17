"""T-165 r03 · mutantes del implementador sobre el código de la r03 (enfoque estructural), contra las pruebas del ticket.

Uno por regla o pieza de la r03 (R01–R23) de la r04 (R24–R35, QA r03) de la r05 (R36–R43, QA r04) y de la r06 (R25, R26, R38–R40, R42–R46 rehechos o nuevos, QA r05): la raíz y su prefijo, el sustantivo de método, el ámbito, la forma canónica (comprobación,
blanqueo, corchete suelto), las reglas B e IMPLEMENTADO, las claves del JSON y los campos de madurez, la canonización de los
informes de clase, la anotación de los entregables (y que se lee antes de anotar), las grafías de ficha (H-21), el solape en
tiempo lineal (H-22), el orden de las incidencias, el extracto de la advertencia y los literales del ejecutor. Cada mutante cambia
una expresión en una COPIA desechable (nunca en el árbol de trabajo), ejecuta `tests/test_t165_g3_met13.py` con `-x` y restaura
el fichero. «muerto» = alguna prueba falla.

Uso (la copia, una exportación completa del commit: `git archive <commit> bloque_a | tar -x -C <copia>`):
    .venv/bin/python .docs/tickets/T-165/r03_mutantes.py --copia <copia> [--python .venv/bin/python] [--solo R01 R02]
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
    ("R01 la raíz sin prefijos (revalidado)", H, 'rf"(?<![{_L}])(?:re|con|pre)?v[aá]lid[{_L}]*"', 'rf"(?<![{_L}])v[aá]lid[{_L}]*"'),
    ("R02 la raíz también dentro de «invalid-»", H, 'rf"(?<![{_L}])(?:re|con|pre)?v[aá]lid[{_L}]*"', 'rf"(?:re|con|pre)?v[aá]lid[{_L}]*"'),
    ("R03 sin sustantivos de método", H, "        metodo = any(x.metodo for x in grupo)", "        metodo = False"),
    ("R04 el ámbito es cada ruta", H, '    return m.group(1) if m else re.split(r"[.\\[,]", ruta, maxsplit=1)[0]', "    return ruta"),
    ("R05 toda forma canónica vale", H, '            if not f.startswith("?") and dice == debe:', "            if True:"),
    ("R06 la forma canónica no se blanquea", H, '            tb[a:b] = " " * (b - a)', "            pass"),
    ("R07 sin regla B", H, '            if not canonica and not (not f.startswith("?") and sirve(f)):', "            if False:"),
    ("R08 sin corchetes sueltos", H, "        for pos in lec.corchetes_sueltos:", "        for pos in []:"),
    ("R09 sin regla «implement-»", H, '(("VALIDADO", lec.valid, bajo_validado), ("IMPLEMENTADO", lec.implement, bajo_impl))',
     '(("VALIDADO", lec.valid, bajo_validado),)'),
    ("R10 el JSON sin las claves", H, "texto = f\"{' · '.join(k.replace('_', ' ') for k in claves)}: {valor}\" if claves else valor",
     "texto = valor"),
    ("R11 los campos de madurez del modelo valen", H, "        if bajo_madurez and not (isinstance(obj, str) and _es_canonico(obj)):",
     "        if False:"),
    ("R12 sin grafías «_» y «.» (H-21)", H, '_SEP = r"[-_.]"', '_SEP = r"[-]"'),
    ("R13 cuatro cifras sin normalizar (H-21)", H, '            segs[-1] = segs[-1].removeprefix("0")', "            pass"),
    ("R14 sin solape entre pasadas (H-22)", H, "                if k > 0 and tomados[k - 1][1] > a:", "                if False:"),
    ("R15 incidencias sin ordenar", H, '    incidencias.sort(key=lambda i: "ACB".index(i.pop("_regla")))',
     '    [i.pop("_regla") for i in incidencias]'),
    ("R16 la advertencia lleva extracto", H, '(f": «{extracto}»" if sev == "BLOQUEO" else "")', '(f": «{extracto}»")'),
    ("R17 sin canonizar los informes de clase", S, "    descartadas = canonizar_madurez(bloque, seleccion)   # T-165 r03", "    descartadas = []   # T-165 r03"),
    ("R18 sin anotar los entregables", S, "    return ht09.anotar_madurez(texto, _servicio.madurez_catalogo(bloque.motor.raiz), _sirve(bloque), _conocidas(bloque))",
     "    return texto"),
    ("R19 sin x_madurez_metodos", R, '        js["x_madurez_metodos"] = sint.madurez_metodos(bloque, json.dumps(entregable_json(paquete), ensure_ascii=False))', ""),
    ("R20 sin la declaración R22 del técnico", R, "sint.anotar(bloque, _con_madurez(tec, sint.resumen_madurez(bloque, tec)))",
     "sint.anotar(bloque, tec)"),
    ("R21 el técnico se lee después de anotar", R, "        if sint.g3_met13_tecnico(bloque, res, tec_g3) and",
     "        if sint.g3_met13_tecnico(bloque, res, sint.anotar(bloque, tec)) and"),
    ("R22 la limitación sin historia cita ML-CLUS-001", O, '"el resto tampoco se agrupa (el Motor no sirvió los clústeres)"',
     '"el resto tampoco se agrupa (ML-CLUS-001 rechazado)"'),
    ("R23 la retirada dice «validación G3»", S, '" Opciones retiradas por el control G3: "', '" Opciones retiradas por la validación G3: "'),
    # r04 (QA r03: H-28 a H-32)
    ("R24 sin la regla R22 en INSTR", O, 'INSTR = {k: f"{v} {ht09.REGLA_R22_REDACCION}" for k, v in INSTR.items()}', "INSTR = dict(INSTR)"),
    ("R25 sin reescrituras R22", O,
     '        for _ in range(int(parametro(self.cfg, "redaccion.reescrituras_r22")) if isinstance(msg, dict) else 0):',
     "        for _ in range(0):"),
    ("R26 nadie pasa por la reescritura (H-40)", O, "        if agente in ht09.AGENTES_SIN_TEXTO_ENTREGADO or (", "        if True or ("),
    ("R27 INSTR_SINTESIS vuelve a «ya validado»", "bloque_a/11_Ejecutor/bloque_a/diseno_v6.py", '"Sobre el paquete ya revisado por G3: escribe',
     '"Sobre el paquete ya validado: escribe'),
    ("R28 el técnico de G3 con las rutas (H-29)", R, '{k: f"<{k}>" for k in rutas_entrega}', "rutas_entrega"),
    ("R29 se anotan las claves con maxLength (H-31)", R, "sint.anotar_json(bloque, entregable_json(paquete), sint.claves_con_longitud_maxima(esquema))",
     "sint.anotar_json(bloque, entregable_json(paquete))"),
    ("R30 la raíz sin tilde (H-30)", H, 'rf"(?<![{_L}])(?:re|con|pre)?v[aá]lid[{_L}]*"', 'rf"(?<![{_L}])(?:re|con|pre)?valid[{_L}]*"'),
    ("R31 sin «metodología» ni «sistema» (H-32)", H, "metodolog[ií]as?|sistemas?|", ""),
    ("R32 la laguna con la raíz se transcribe", S, "    if not (isinstance(texto, str) and ht09.tiene_raiz_valid(texto)):", "    if True:"),
    ("R33 lo descartado no queda en HA", S, '    if descartadas and getattr(bloque, "almacen", None) is not None:', "    if False:"),
    ("R34 el Motor vuelve a «no validada» en RC", "bloque_a/11_Ejecutor/bloque_a/motor/servicio.py",
     '"ninguna conocida (ficha implementada; su madurez, la del Catálogo)"', '"ninguna conocida (ficha implementada, no validada)"'),
    ("R35 la limitación «semanas válidas»", O, "semanas con datos utilizables en la ventana", "semanas válidas de historia en la ventana"),
    # r05 (QA r04: H-33 a H-37)
    ("R36 la refutación V5 sin la regla (H-33)", O, 'por tesis. " + ht09.REGLA_R22_REDACCION)', 'por tesis.")'),
    ("R37 la refutación V6 sin la regla (H-33)", "bloque_a/11_Ejecutor/bloque_a/diseno_v6.py",
     "+ ht09.REGLA_R22_REDACCION)   # T-165 r05 (H-33)", ")   # T-165 r05 (H-33)"),
    ("R38 el Contradictor fuera de la reescritura (H-33, H-40)", H, 'frozenset({"AG-12", "AG-13",', 'frozenset({"AG-11", "AG-12", "AG-13",'),
    ("R39 los Analistas fuera de la reescritura (H-34, H-40)", H, 'frozenset({"AG-12", "AG-13",', 'frozenset({"AG-03", "AG-12", "AG-13",'),
    ("R40 la reescritura siempre en la COMÚN (H-34)", O, "clase, fase, presupuesto, bolsa=bolsa, **extra)", 'None, fase, presupuesto, bolsa="COMUN", **extra)'),
    ("R41 la laguna se omite en lugar de ajustarse (H-35)", S, '    t = _RE_VALID_CRUDO.sub("comprobar", texto)', "    t = texto"),
    ("R42 la reescritura sin la instrucción de la llamada (H-36)", O, 'r2 = self._invocar(agente, contrato, msg2, esquema, f"{instr} Reescribe:',
     'r2 = self._invocar(agente, contrato, msg2, esquema, f"Reescribe:'),
    ("R43 la reescritura sin las frases (H-37)", O, '"r22": ht09.REGLA_R22_REDACCION, "frases": frases}}', '"r22": ht09.REGLA_R22_REDACCION, "frases": []}}'),
    # r06 (QA r05: H-38 a H-40)
    ("R44 los campos de madurez disparan la reescritura (H-38)", O, "            datos = sint._sin_madurez(r.datos) if r and r.datos else None",
     "            datos = r.datos if r and r.datos else None"),
    ("R45 lo reescrito no queda en HA (H-39)", O, 'self.almacen.incidencia("OTRO", f"G3-MET-13 (R22): respuesta de {agente} ({esquema}) reescrita',
     '(lambda *a, **k: None)("OTRO", f"G3-MET-13 (R22): respuesta de {agente} ({esquema}) reescrita'),
    ("R46 la regla sin la frase de la fiabilidad (H-39)", H, '"de un método (comprobado, probado, fiable): la escribe el ejecutor.")', '"")'),
    # cierre de la QA r06
    ("R47 la reescritura se pide aunque no quepa en la bolsa", O, "            if presupuesto is not None and not presupuesto.puede(b, peor):", "            if False:"),
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
    for nombre, fich, viejo, _ in MUTANTES:     # todas las expresiones existen antes de empezar (H-24 de la QA r02)
        n = (copia / fich).read_text(encoding="utf-8").count(viejo)
        assert n == 1, f"{nombre}: «{viejo[:60]}» aparece {n} veces"
    vivos = []
    for nombre, fich, viejo, nuevo in MUTANTES:
        if a.solo and nombre.split()[0] not in a.solo:
            continue
        p = copia / fich
        original = p.read_text(encoding="utf-8")
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
