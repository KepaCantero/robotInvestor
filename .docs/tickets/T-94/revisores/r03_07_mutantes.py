"""QA r03 de T-94 · Mutantes del revisor sobre el banco de la ronda r03.

Los 8 de `r02_07_mutantes.py` cuyo patrón ya no existe (M12, N05, N14, N15, N19, N20, N21 y N23), reescritos con el código
nuevo (N21 y N23 cambian de sentido: ahora el experimento es por fuente), y otros nuevos sobre lo que añadió la ronda r03:
fechas sin solape (S), experimento por fuente (X), `verificar` con `informe.md` (V), lectura de CSV (C), consumo (K) y cotas (Q).
Modifica `.docs/scripts/banco_medida.py` SOLO en el worktree que se le pasa (se niega a tocar el árbol principal), ejecuta
`pruebas_banco_medida.py` con cada mutante y restaura el original al terminar, también si se interrumpe.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r03_07_mutantes.py <worktree>"""
import subprocess
import sys
from pathlib import Path

ARBOL_PRINCIPAL = Path(__file__).resolve().parents[4]
if len(sys.argv) < 2:
    sys.exit("uso: r03_07_mutantes.py <worktree>")
W = Path(sys.argv[1]).resolve()
if W == ARBOL_PRINCIPAL:
    sys.exit("me niego a mutar el árbol principal: pásame un worktree")
F = W / ".docs" / "scripts" / "banco_medida.py"
ORIGINAL = F.read_text(encoding="utf-8")

MUTANTES = {
    # --- los de r02_07 sin patrón, reescritos
    "M12 resueltas cuenta las no resueltas": ('puntuadas = [f for f in dentro if f["resuelta"]]', "puntuadas = list(dentro)"),
    "N05 se recorre en el orden de entrada": ("for i in sorted(range(len(selecciones)), key=orden):", "for i in range(len(selecciones)):"),
    "N14 verificar sin experimento.json no se queja": (
        'problemas.append("no hay experimento.json: sin el registro no se puede comprobar que el informe sea el que dio el banco")',
        "pass"),
    "N15 fecha repetida aceptada": ("if fechas.duplicated().any():", "if False:"),
    "N19 grupos por fecha y clase": ('[_fecha(f) for f in puntuadas])', '[_fecha(f) + str(f.get("clase")) for f in puntuadas])'),
    "N20 grupos por símbolo": ('[_fecha(f) for f in puntuadas])', '[str(f.get("simbolo")) for f in puntuadas])'),
    "N21 el aviso de otros experimentos cuenta también el propio": ('otros = len({x["exp_id"] for x in misma} - {exp_id})',
                                                                    'otros = len({x["exp_id"] for x in misma})'),
    "N23 se reutiliza cualquier experimento de la hipótesis (sin mirar la fuente)": (
        'de_la_fuente = [x for x in misma if x["contenido"].get("fuente_banco") == fuente]', "de_la_fuente = misma"),
    # --- nuevos (ronda r03)
    "S01 la fecha que empieza el día del fin de la anterior no entra": ("if d >= cierre:", "if d > cierre:"),
    "S02 todas las fechas entran (vuelve H-13)": ("if d >= cierre:", "if True:"),
    "S03 manda la ventana más corta de la fecha": ("max(fin_por_fecha.get(d, fin), fin)", "min(fin_por_fecha.get(d, fin), fin)"),
    "S04 la muestra solo se aplica al titular": ('dentro = [f for f in filas if _fecha(f) in muestra]',
                                                 'dentro = [f for f in filas if nombre != "titular" or _fecha(f) in muestra]'),
    "S05 se ignora fecha_fin (ventanas de un día)": ('fin = f.get("fecha_fin") or d', "fin = d"),
    "S06 la muestra se calcula con la referencia, no con el titular": ('muestra = fechas_sin_solape(contendientes["titular"])',
                                                                       'muestra = fechas_sin_solape(list(contendientes.values())[-1])'),
    "X02 --experimento no mira la fuente": ('("objeto", "BLOQUE"), ("fuente_banco", fuente))', '("objeto", "BLOQUE"))'),
    "X03 la fuente no incluye el cliente": ('"fuente": f"cliente {a.cliente}, datos', '"fuente": f"datos'),
    "V01 verificar no compara informe.md": ("if md != informe_md(", "if False and md != informe_md("),
    "V02 verificar no recalcula la huella del prerregistro": ('if pre.get("huella") != h:', "if False:"),
    "V03 verificar no mira la huella citada en el informe": ('if inf.get("prerregistro") != h:', "if False:"),
    "C01 fecha sin ceros a la izquierda aceptada": (
        r'malas = fechas.isna() | ~texto.str.fullmatch(r"\d{4}-\d{2}-\d{2}")', "malas = fechas.isna()"),
    "C02 columnas repetidas aceptadas": ("if repetidas:", "if False:"),
    "C03 fichero sin filas aceptado": ("if df.empty:", "if False:"),
    "K01 consumo negativo aceptado": ("if not math.isfinite(v) or v < 0:", "if not math.isfinite(v):"),
    "K02 sin consumo.csv se publican ceros": (
        'raise BancoError(f"no hay {Path(fichero).name}: el coste del titular no se puede medir")', "return consumo"),
    "K03 coste parcial publicado como total": ('if filas and not consumo["filas_sin_coste"]:', "if filas:"),
    "Q01 ejecutar_a admite pocos remuestreos": (
        'remuestreos = _entero("remuestreos", getattr(a, "remuestreos", REMUESTREOS), minimo=REMUESTREOS_MIN)',
        'remuestreos = _entero("remuestreos", getattr(a, "remuestreos", REMUESTREOS), minimo=1)'),
    "Q02 diferencia admite cualquier nivel": (
        '    if not NIVEL_MIN <= nivel <= NIVEL_MAX:\n        raise BancoError(f"«nivel» de un veredicto',
        '    if False:\n        raise BancoError(f"«nivel» de un veredicto'),
    "Q03 diferencia admite min_efectivas 1": (
        'min_efectivas = _entero("min_efectivas", min_efectivas, minimo=MIN_EFECTIVAS_MIN)',
        'min_efectivas = _entero("min_efectivas", min_efectivas, minimo=1)'),
    "Q04 la línea de órdenes admite cualquier nivel": (
        "    if not NIVEL_MIN <= v <= NIVEL_MAX:\n        raise argparse.ArgumentTypeError",
        "    if False:\n        raise argparse.ArgumentTypeError"),
    "Q05 ejecutar_a admite cualquier nivel": (
        '    if not NIVEL_MIN <= nivel <= NIVEL_MAX:\n        raise BancoError(f"«nivel» de un experimento',
        '    if False:\n        raise BancoError(f"«nivel» de un experimento'),
    "E01 el registro guarda otra huella del informe": ('"huella_informe": huella(inf)}', '"huella_informe": huella({**inf, "x": 1})}'),
}


def pytest(extra):
    return subprocess.run([str(W / ".venv" / "bin" / "python"), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *extra,
                           str(W / ".docs" / "scripts" / "pruebas_banco_medida.py")], cwd=W, capture_output=True, text=True,
                          check=False).returncode


vivos = []
try:
    for nombre, (viejo, nuevo) in MUTANTES.items():
        if ORIGINAL.count(viejo) != 1:
            print(f"??    {nombre}: el patrón no aparece una sola vez")
            vivos.append(nombre + " (patrón)")
            continue
        F.write_text(ORIGINAL.replace(viejo, nuevo), encoding="utf-8")
        muerto = pytest(["-k", "not integracion"]) != 0
        print(("MUERE " if muerto else "VIVO  ") + nombre, flush=True)
        if not muerto:
            vivos.append(nombre)
    print("\nSegunda pasada de los vivos con la suite completa (incluida la integración):")
    siguen = []
    for nombre in vivos:
        if nombre.endswith("(patrón)"):
            siguen.append(nombre)
            continue
        viejo, nuevo = MUTANTES[nombre]
        F.write_text(ORIGINAL.replace(viejo, nuevo), encoding="utf-8")
        r = pytest([])
        print(("MUERE " if r != 0 else "VIVO  ") + nombre, flush=True)
        if r == 0:
            siguen.append(nombre)
    vivos = siguen
finally:
    F.write_text(ORIGINAL, encoding="utf-8")
print(f"\n{len(vivos)} mutante(s) vivo(s) de {len(MUTANTES)} con la suite completa:")
for v in vivos:
    print(" -", v)
sys.exit(1 if vivos else 0)
