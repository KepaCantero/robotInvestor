"""T-133 QA r01 · Mutantes del revisor sobre lo que cambió el banco 0.4.0 (H-21 a H-28).

Modifica `.docs/scripts/banco_medida.py` SOLO en el worktree que se le pasa (se niega a tocar el árbol principal), ejecuta
`pruebas_banco_medida.py` con cada mutante y restaura el original al terminar, también si se interrumpe.
Uso: .venv/bin/python -B r01_04_mutantes.py <worktree>"""
import subprocess
import sys
from pathlib import Path

ARBOL_PRINCIPAL = Path(__file__).resolve().parents[5]
if len(sys.argv) < 2:
    sys.exit("uso: r01_04_mutantes.py <worktree>")
W = Path(sys.argv[1]).resolve()
if W == ARBOL_PRINCIPAL:
    sys.exit("me niego a mutar el árbol principal: pásame un worktree")
F = W / ".docs" / "scripts" / "banco_medida.py"
ORIGINAL = F.read_text(encoding="utf-8")

MUTANTES = {
    # H-24: la muestra antes de evaluar
    "P01 sin el filtro previo (plantilla = todas)": (
        'plantilla = [s for s in plantilla_total if pd.Timestamp(s["fecha_asof"]).strftime("%Y-%m-%d") in muestra]',
        "plantilla = list(plantilla_total)"),
    "P02 la muestra previa sin evaluar (ventanas de un día)": (
        "muestra = fechas_sin_solape(evaluar(plantilla_total, precios, universo, tit[\"fecha_fin\"]))",
        "muestra = fechas_sin_solape(plantilla_total)"),
    "P03 el filtro compara la fecha sin normalizar": (
        'if pd.Timestamp(s["fecha_asof"]).strftime("%Y-%m-%d") in muestra]', 'if s["fecha_asof"] in muestra]'),
    "P04 sin «plantilla» en el informe": (
        'inf["plantilla"] = {"selecciones": len(plantilla_total), "en_muestra": len(plantilla)}', "pass"),
    # H-25: NEUTRAL
    "N01 una NEUTRAL vuelve a gastar ventana": ('if f.get("direccion") == "NEUTRAL":   # T-133', "if False:   # T-133"),
    # H-21/H-22: huella y fuente
    "F01 la huella sin el contenido (solo nombres)": (
        'h.update(f.name.encode("utf-8", "backslashreplace") + b"\\0" + hashlib.sha256(f.read_bytes()).digest())',
        'h.update(f.name.encode("utf-8", "backslashreplace") + b"\\0")'),
    "F02 la huella con la ruta entera": (
        'h.update(f.name.encode("utf-8", "backslashreplace") + b"\\0"',
        'h.update(str(f.resolve()).encode("utf-8", "backslashreplace") + b"\\0"'),
    "F03 la huella con subcarpetas (rglob)": ('ficheros = sorted(ruta.glob("*.csv"))', 'ficheros = sorted(ruta.rglob("*.csv"))'),
    "F04 la huella sin ordenar": ('ficheros = sorted(ruta.glob("*.csv"))', 'ficheros = list(ruta.glob("*.csv"))[::-1]'),
    "F05 carpeta sin CSV aceptada": ('raise BancoError(f"{ruta} no tiene ficheros CSV")', "pass"),
    "F06 la fuente vuelve a ser la ruta": (
        '"fuente": f"cliente {a.cliente}, datos {huella_d[:16]}, universo {huella_u[:16]}",',
        '"fuente": f"cliente {a.cliente}, datos {datos_txt}, universo {universo_txt}",'),
    "F07 el prerregistro sin las huellas": ('"huella_datos": huella_d, "huella_universo": huella_u,', ""),
    "F08 la fuente sin el universo": (
        '"fuente": f"cliente {a.cliente}, datos {huella_d[:16]}, universo {huella_u[:16]}",',
        '"fuente": f"cliente {a.cliente}, datos {huella_d[:16]}",'),
    # H-23: verificar
    "V01 sin --registro se usa el que cita la carpeta": ("            registro = rx.REGISTRO_DEFECTO\n",
                                                          "            registro = citado\n"),
    "V02 sin RI_AGENTE válido se usa el citado": (
        'return problemas + ["sin --registro y sin un RI_AGENTE válido no hay registro con el que comprobar"]',
        "registro = citado"),
    "V03 no se avisa si la carpeta cita otro registro": (
        'problemas.append("experimento.json cita otro registro que el indicado: se comprueba contra el indicado")', "pass"),
    "V04 no se compara dentro_del_maximo": ('elif e.get("dentro_del_maximo") != it["dentro_del_maximo"]:', "elif False:"),
    # H-26: consumo
    "K01 decimales truncados": ("if v != int(v):", "if False:"),
    "K02 columnas repetidas aceptadas": ("if repetidas:   # T-133 (H-26)", "if False:   # T-133 (H-26)"),
    "K03 columnas obligatorias que faltan aceptadas": ("        if faltan:\n            raise BancoError(f\"a {Path(fichero).name}",
                                                      "        if False:\n            raise BancoError(f\"a {Path(fichero).name}"),
    "K04 columnas ausentes sin declarar": (
        'consumo["columnas_ausentes"] = [c for c in CAMPOS_ENTEROS + ("uc", "coste_estimado") if c not in cabecera]',
        'consumo["columnas_ausentes"] = []'),
    "K05 tokens_salida deja de ser obligatoria": ('("llamadas", "tokens_entrada", "tokens_salida") if c not in cabecera]',
                                                 '("llamadas", "tokens_entrada") if c not in cabecera]'),
    # H-27: mínimo
    "Q01 el mínimo de un experimento vuelve a 5": ("MIN_EFECTIVAS_MIN = MIN_EFECTIVAS", "MIN_EFECTIVAS_MIN = 5"),
    "Q02 el mínimo de un experimento 9": ("MIN_EFECTIVAS_MIN = MIN_EFECTIVAS", "MIN_EFECTIVAS_MIN = 9"),
    # H-28: los tres que vivían en la r03 de T-94
    "N19 grupos por fecha y clase": ('[_fecha(f) for f in puntuadas])', '[_fecha(f) + str(f.get("clase")) for f in puntuadas])'),
    "S04 la muestra solo se aplica al titular": (
        'dentro = [f for f in filas if _fecha(f) in muestra]',
        'dentro = [f for f in filas if _fecha(f) in muestra or nombre != "titular"]'),
    "C01 fecha sin ceros a la izquierda aceptada": ('| ~texto.str.fullmatch(r"\\d{4}-\\d{2}-\\d{2}")', ""),
}

vivos = []
try:
    for nombre, (viejo, nuevo) in MUTANTES.items():
        n = ORIGINAL.count(viejo)
        if n != 1:
            print(f"SIN PATRÓN ({n})  {nombre}")
            vivos.append(nombre + " (sin patrón)")
            continue
        F.write_text(ORIGINAL.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([str(W / ".venv" / "bin" / "python"), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                            ".docs/scripts/pruebas_banco_medida.py"], cwd=W, capture_output=True, text=True, timeout=900, check=False)
        muere = r.returncode != 0
        print(("muere " if muere else "VIVE  ") + nombre, flush=True)
        if not muere:
            vivos.append(nombre)
finally:
    F.write_text(ORIGINAL, encoding="utf-8")
estado = subprocess.run(["git", "status", "--short"], cwd=W, capture_output=True, text=True, check=False).stdout
print(f"\n{len(MUTANTES)} mutantes, {len(vivos)} vivos: {vivos}")
print(f"git status del worktree: {estado.strip() or 'vacío'}")
