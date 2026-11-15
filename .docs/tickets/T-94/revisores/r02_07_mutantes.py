"""QA r02 de T-94 · Mutantes del revisor sobre el banco 0.3.0: los de r01 adaptados al código nuevo (r01_07 ya no casa
porque cambiaron las líneas) y otros nuevos sobre lo que añadió la ronda r02 (apuestas repetidas, remuestreo por fechas,
mínimo de fechas efectivas, fuga, prerregistro reutilizado y `verificar`).

Modifica `.docs/scripts/banco_medida.py` SOLO en la copia que se le pasa (se niega a tocar el árbol principal), ejecuta
`pruebas_banco_medida.py` con cada mutante (primero sin la integración y, a los que sobreviven, con la suite completa) y
restaura el original al terminar, también si se interrumpe.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_07_mutantes.py <worktree>"""
import subprocess
import sys
from pathlib import Path

ARBOL_PRINCIPAL = Path(__file__).resolve().parents[4]
if len(sys.argv) < 2:
    sys.exit("uso: r02_07_mutantes.py <worktree>")
W = Path(sys.argv[1]).resolve()
if W == ARBOL_PRINCIPAL:
    sys.exit("me niego a mutar el árbol principal: pásame un worktree")
F = W / ".docs" / "scripts" / "banco_medida.py"
ORIGINAL = F.read_text(encoding="utf-8")

MUTANTES = {
    # --- los de r01, con el patrón del código 0.3.0
    "M01 momento mira el futuro": ("hist = validar_serie(m, serie).loc[:corte]", "hist = validar_serie(m, serie)"),
    "M02 veredicto con >= (el cero cuenta como mejor)": ("if lo > 0:", "if lo >= 0:"),
    "M03 sin signo en el exceso": ("exceso=round(SIGNO[direccion] * (r - float(np.mean(cesta))), 10)",
                                   "exceso=round((r - float(np.mean(cesta))), 10)"),
    "M04 cesta sin el propio símbolo": ("if m in precios]", "if m in precios and m != sim]"),
    "M05 rango del 80 % en vez del nivel pedido": ("cola = (1.0 - nivel) / 2.0", "cola = (1.0 - nivel)"),
    "M07 sin precio final se estima con el último": ("if serie.empty or serie.index.max() < fin:", "if serie.empty:"),
    "M08 azar sin semilla por fecha y clase": ('rng = random.Random(f"{semilla}|{fecha}|{clase}")', "rng = random.Random(semilla)"),
    "M09 momento CORTO elige como LARGO": ('candidatos = orden if f["direccion"] != "CORTO" else list(reversed(orden))',
                                          "candidatos = orden"),
    "M10 aviso nunca": ('return "; ".join(partes)', 'return None and "; ".join(partes)'),
    "M11 la huella citada no es la del prerregistro escrito": ("h = huella(prerregistro)", 'h = huella({**prerregistro, "tarde": True})'),
    "M12 resueltas cuenta las no resueltas": ('puntuadas = [f for f in filas if f["resuelta"]]', "puntuadas = list(filas)"),
    # --- nuevos (ronda r02)
    "N01 la ventana sigue abierta el mismo día de su fin (>=)": ("abiertas[clave][0] > ini", "abiertas[clave][0] >= ini"),
    "N02 la apuesta repetida no distingue la dirección": ("clave = (clase, sim, direccion)", "clave = (clase, sim)"),
    "N03 nunca hay apuestas repetidas": ("elif clave in abiertas and", "elif False and clave in abiertas and"),
    "N04 la repetida alarga la ventana abierta": (
        'motivo=f"repetida: la misma apuesta sigue abierta desde el {abiertas[clave][1]}")',
        'motivo=f"repetida: la misma apuesta sigue abierta desde el {abiertas[clave][1]}")\n'
        "            abiertas[clave] = (max(fin, abiertas[clave][0]), abiertas[clave][1])"),
    "N05 se ignora el orden por fecha (se recorre en el orden de entrada)": (
        "for i in sorted(range(len(selecciones)), key=lambda k: (inicios[k], k)):", "for i in range(len(selecciones)):"),
    "N06 remuestreo iid aunque haya grupos": ("if grupos is None:", "if True:"),
    "N07 efectivas = observaciones, no fechas": ("return len(x) if grupos is None else len(set(grupos))", "return len(x)"),
    "N08 mínimo con <= (exactamente el mínimo no basta)": ("if min(efectivas) < min_efectivas:", "if min(efectivas) <= min_efectivas:"),
    "N09 mínimo mirando el lado con más fechas": ("if min(efectivas) < min_efectivas:", "if max(efectivas) < min_efectivas:"),
    "N10 la fuga solo rebaja «mejor»": ('c["veredicto"] in ("mejor", "peor")', 'c["veredicto"] == "mejor"'),
    "N11 la fuga solo se mira con el cliente simulado": ('a.cliente != "mock" and', 'a.cliente == "mock" and'),
    "N12 verificar no compara la huella del informe": ('rs["detalle"].get("huella_informe") != huella(inf)', "False"),
    "N13 verificar no compara la variante del intento": ('if it is None or it["variante"] != h[:16]:', "if it is None:"),
    "N14 verificar sin experimento.json no se queja con --registro": ("elif registro:", "elif False:"),
    "N15 fechas duplicadas: se queda la primera": ('keep="last"', 'keep="first"'),
    "N16 un cierre cero es válido": ("(v <= 0)", "(v < 0)"),
    "N17 no se borra el experimento.json anterior": ('(salida / "experimento.json").unlink(missing_ok=True)', "pass"),
    "N18 solo se anotan los fallos BancoError": ("except BaseException as e:", "except BancoError as e:"),
    "N19 grupos por fecha y clase (más «fechas» efectivas)": ('[f["fecha_asof"] for f in puntuadas]',
                                                             '[(f["fecha_asof"], f["clase"]) for f in puntuadas]'),
    "N20 grupos por símbolo": ('[f["fecha_asof"] for f in puntuadas]', '[f["simbolo"] for f in puntuadas]'),
    "N21 aviso de otras hipótesis desde 3": ("if previos_misma > 1:", "if previos_misma > 2:"),
    "N22 azar recorta en silencio": ("if len(pool) < len(filas):", "if False:"),
    "N23 se reutiliza cualquier experimento de la hipótesis (sin mirar el periodo)": ("if del_periodo:", "if misma:\n        return misma[0][\"exp_id\"], len(misma)\n    if del_periodo:"),
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
