"""T-133 QA r01 · `consumo.csv` (H-26): lo que llega al informe cuando falta un dato.

H-26 pedía «sin dato» si no hay dato. El banco 0.4.0 declara las columnas opcionales ausentes en `columnas_ausentes`
(informe.json). ¿Qué dice informe.md? ¿Y una celda vacía o una fila corta de una columna obligatoria?
Uso: .venv/bin/python -B r01_05_consumo_informe.py [<carpeta de banco_medida.py>]"""
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r01_t133_consumo_"))
TIT = [{"fecha_asof": f"2026-0{m}-01", "fecha_fin": f"2026-0{m}-20", "resuelta": True, "exceso": 0.01, "clase": "C"}
       for m in range(1, 4)]


def md_de(contenido):
    f = TMP / "consumo.csv"
    f.write_text(contenido, encoding="utf-8")
    c = bm.leer_consumo(f)
    inf = bm.construir_informe({"titular": TIT, "azar": TIT}, c, 200, 1, None, "h")
    return c, bm.informe_md(inf, "x")


c, md = md_de("agente,llamadas,tokens_entrada,tokens_salida,coste_estimado\nA,1,10,1,0.5\n")
linea = next(x for x in md.splitlines() if x.startswith("- Titular:"))
print(f"   sin columnas de caché ni uc: columnas_ausentes {c['columnas_ausentes']}; informe.md: «{linea}»")
ok("sin dato" in linea or "no consta" in linea or "ausente" in linea,
   "informe.md dice que no hay dato de caché ni de uc cuando faltan sus columnas (no «0 leídos de caché; 0.0 uc»)")

for nombre, contenido in (("celda vacía en tokens_entrada", "llamadas,tokens_entrada,tokens_salida\n1,,1\n"),
                          ("fila corta (sin tokens_salida)", "llamadas,tokens_entrada,tokens_salida\n1,10\n")):
    f = TMP / "c.csv"
    f.write_text(contenido, encoding="utf-8")
    try:
        r = bm.leer_consumo(f)
        print(f"   {nombre}: aceptado → tokens_entrada {r['tokens_entrada']}, tokens_salida {r['tokens_salida']}")
        ok(False, f"{nombre} en una columna obligatoria: falla cerrado o «sin dato» (no un 0)")
    except bm.BancoError as e:
        ok(True, f"{nombre}: BancoError ({e})")

for nombre, contenido, esperado in (("10.0 en tokens", "llamadas,tokens_entrada,tokens_salida\n1,10.0,1\n", 10),
                                    ("1e3 en tokens", "llamadas,tokens_entrada,tokens_salida\n1,1e3,1\n", 1000)):
    f = TMP / "c.csv"
    f.write_text(contenido, encoding="utf-8")
    r = bm.leer_consumo(f)
    print(f"   {nombre}: aceptado como {r['tokens_entrada']} (entero exacto)")

print()
print(f"{len(fallos)} fallo(s)")
for f in fallos:
    print(" - " + f)
sys.exit(1 if fallos else 0)
