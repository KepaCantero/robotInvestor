"""QA r01 de T-94 · Mutantes: ¿detectan las pruebas del implementador los errores que importan?

Modifica `.docs/scripts/banco_medida.py` SOLO en el worktree que se le pasa (se niega a tocar el árbol principal), ejecuta las
pruebas unitarias (`pruebas_banco_medida.py`, sin la de integración) con cada mutante y restaura el original.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r01_07_mutantes.py <worktree>"""
import subprocess
import sys
from pathlib import Path

ARBOL_PRINCIPAL = Path(__file__).resolve().parents[4]
W = Path(sys.argv[1]).resolve()
if W == ARBOL_PRINCIPAL:
    sys.exit("me niego a mutar el árbol principal: pásame un worktree")
F = W / ".docs" / "scripts" / "banco_medida.py"
ORIGINAL = F.read_text(encoding="utf-8")

MUTANTES = {
    "M01 momento mira el futuro": ('hist = serie.loc[:corte]', 'hist = serie'),
    "M02 veredicto con >= (el cero cuenta como mejor)": ('if lo > 0:', 'if lo >= 0:'),
    "M03 sin signo en el exceso": ('exceso=round(signo * (r - float(np.mean(cesta))), 10)', 'exceso=round((r - float(np.mean(cesta))), 10)'),
    "M04 cesta sin el propio símbolo": ('if m in precios]', 'if m in precios and m != s["simbolo"]]'),
    "M05 rango del 80 %": ('np.quantile(m, 0.05)', 'np.quantile(m, 0.10)'),
    "M06 diferencia con el rango del 80 %": ('np.quantile(d, 0.05)', 'np.quantile(d, 0.10)'),
    "M07 sin precio final se estima con el último": ('if serie.empty or serie.index.max() < fin:', 'if serie.empty:'),
    "M08 azar sin semilla por fecha y clase": ('rng = random.Random(f"{semilla}|{fecha}|{clase}")', 'rng = random.Random(semilla)'),
    "M09 momento CORTO elige como LARGO": ('candidatos = orden if f["direccion"] != "CORTO" else list(reversed(orden))', 'candidatos = orden'),
    "M10 aviso nunca": ('if a.cliente == "mock" or "ejemplos" in str(tit["datos"]):', 'if False:'),
    "M11 prerregistro después de evaluar (huella de otro contenido)": ('h = huella(prerregistro)', 'h = huella({**prerregistro, "tarde": True})'),
    "M12 resueltas cuenta las no resueltas": ('ex = [f["exceso"] for f in filas if f["resuelta"]]', 'ex = [f["exceso"] for f in filas]'),
}

vivos = []
try:
    for nombre, (viejo, nuevo) in MUTANTES.items():
        if ORIGINAL.count(viejo) != 1:
            print(f"??    {nombre}: el patrón no aparece una sola vez")
            vivos.append(nombre + " (patrón)")
            continue
        F.write_text(ORIGINAL.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([str(W / ".venv" / "bin" / "python"), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                            "-k", "not integracion", str(W / ".docs" / "scripts" / "pruebas_banco_medida.py")],
                           cwd=W, capture_output=True, text=True, check=False)
        muerto = r.returncode != 0
        print(("MUERE " if muerto else "VIVO  ") + nombre)
        if not muerto:
            vivos.append(nombre)
    # Segunda pasada: los vivos, con la suite completa (también la integración sobre A, ~25 s cada uno)
    print("\nSegunda pasada de los vivos con la suite completa (incluida la integración):")
    siguen = []
    for nombre in vivos:
        viejo, nuevo = MUTANTES[nombre]
        F.write_text(ORIGINAL.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([str(W / ".venv" / "bin" / "python"), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                            str(W / ".docs" / "scripts" / "pruebas_banco_medida.py")], cwd=W, capture_output=True, text=True, check=False)
        print(("MUERE " if r.returncode != 0 else "VIVO  ") + nombre)
        if r.returncode == 0:
            siguen.append(nombre)
    vivos = siguen
finally:
    F.write_text(ORIGINAL, encoding="utf-8")
print(f"\n{len(vivos)} mutante(s) vivo(s) de {len(MUTANTES)} con la suite completa: {vivos}")
sys.exit(1 if vivos else 0)
