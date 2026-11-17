"""QA r01 de T-164 · ataques a la excusa del símbolo por aparición (H-09) y a las cifras (H-10), en una copia del corpus real.

IDX-FICT-001 es el único símbolo real con forma de ficha (se declara `serie_ht01`/`simbolo` en los Registros). Cada línea
sembrada lo usa de una forma; se comprueba si esa línea concreta sale como ERROR (usado como ficha) o como INFO (excusado).
«ERROR» son usos como ficha; «INFO», usos como serie o prosa; «ERROR+INFO», una línea con los dos usos. Imprime una línea por caso y sale 1 si alguno falla.
El corpus del repositorio no se toca (huellas antes y después).

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-164/revisores/r01_01_excusa.py
"""
import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

EJ = Path.cwd()
sys.path.insert(0, str(EJ))
RAIZ = EJ.parent
from bloque_a.herramientas import verificador_ids as vi

P_RV = "02_System_prompts/System prompt - Analista de Renta Variable - Versión óptima V5.0.md"
X = "IDX-FICT-001"
# (clave, nivel esperado, líneas que se siembran; la última lleva la cita)
CASOS = [
    # usos como ficha: deben dar ERROR
    ("E01 «Ficha» con mayúscula", "ERROR", [f"Ficha {X}: implementada."]),
    ("E02 «FICHAS:» y lista con comas", "ERROR", [f"FICHAS: ST-DESC-001, VOL-GARCH-001 y {X}."]),
    ("E03 ficha entre comillas angulares y negrita", "ERROR", [f"Usa la ficha «**{X}**» del Catálogo."]),
    ("E04 frase larga (≈300 caracteres) con «ficha» al principio", "ERROR",
     ["Para la tesis se usa la ficha que " + "mide, con datos diarios y ajustados por dividendos, " * 5 + f"la serie {X}"]),
    ("E05 JSON en una línea: operacion.ficha_id anidado", "ERROR", [f'{{"operacion":{{"ficha_id":"{X}","version":"1.0"}}}}']),
    ("E06 JSON: ficha_id dentro de un array de objetos", "ERROR", [f'{{"calculos":[{{"ficha_id":"{X}","version":"1.0"}}]}}']),
    ("E07 JSON: method_id dentro de un array de objetos", "ERROR", [f'{{"pasos":[{{"method_id":"{X}"}}]}}']),
    ("E08 JSON: clave «fichas» con array", "ERROR", [f'{{"fichas":["{X}"]}}']),
    ("E09 JSON: clave «ficha» con cadena", "ERROR", [f'{{"ficha":"{X}"}}']),
    ("L10 [límite por línea, H-03: se documenta] JSON: estado_madurez_metodos como objeto con la ficha de clave", "INFO",
     [f'{{"estado_madurez_metodos":{{"{X}":"implementado"}}}}']),
    ("L11 [límite por línea, H-03: se documenta] JSON con sangría: ficha_id con su valor en otra línea", "INFO", ['"ficha_id": [', f'  "{X}"']),
    ("L12 [límite por línea, H-03: se documenta] tabla Markdown bajo la columna «Ficha»", "INFO",
     ["", "| Ficha | Estado |", "| --- | --- |", f"| {X} | IMPLEMENTADO |"]),
    ("L13 [límite por línea, H-03: se documenta] frase partida en dos líneas («la ficha» / ID)", "INFO", ["Se calcula con la ficha", f"{X} del Catálogo."]),
    ("E14 abreviatura «p. ej.» tras «ficha»", "ERROR", [f"Usa una ficha de índices (p. ej. {X})."]),
    ("E15 lista con «;» tras «fichas:»", "ERROR", [f"Fichas: ST-DESC-001; {X}."]),
    ("E16 «ficha» con guion U+2011 en el ID", "ERROR", ["Usa la ficha IDX‑FICT‑001."]),
    ("E17 CA-1 literal: serie_ht01 y ficha_id en la misma línea, dentro de un array", "ERROR+INFO",
     [f'{{"datos":[{{"serie_ht01":"{X}","ficha_id":"{X}"}}]}}']),
    # usos como serie o prosa: deben seguir en INFO (L10–L13 arriba: usos como ficha que el análisis por línea no ve)
    ("I01 serie en prosa", "INFO", [f"El índice {X} sube."]),
    ("I02 serie en un array de datos", "INFO", [f'{{"datos":[{{"serie_ht01":"{X}","fuente":"HT-01"}}]}}']),
    ("I03 «ficha» en la frase anterior", "INFO", [f"Se usa la ficha ST-DESC-001. La serie {X} sube."]),
    ("I04 «ficha» después de la cita", "INFO", [f"La serie {X} no es una ficha."]),
    ("I05 «fichaje» no es «ficha»", "INFO", [f"Tras el fichaje, la serie {X} sube."]),
    ("I06 campo ajeno con «ficha» fuera del valor", "INFO", [f'Según la ficha: {{"nota":"{X} sube"}}']),
]

resultados: list[tuple[str, bool, str]] = []


def huellas() -> dict[str, str]:
    return {p.relative_to(RAIZ).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(RAIZ.rglob("*")) if p.is_file() and p.suffix in (".md", ".docx") and "11_Ejecutor" not in p.parts}


antes = huellas()
with tempfile.TemporaryDirectory() as tmp:
    r = Path(tmp) / "bloque_a"
    shutil.copytree(RAIZ, r, ignore=lambda d, n: [x for x in n if x == "11_Ejecutor" or x.startswith("99_Historico")])
    p = r / P_RV
    lineas = p.read_text(encoding="utf-8").split("\n")
    donde: dict[str, int] = {}
    for clave, _, sembrar in CASOS:
        lineas += ["", *sembrar]
        donde[clave] = len(lineas)          # línea (1-based) de la cita
    p.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    inf = vi.verificar(r)
    nivel_de: dict[int, set[str]] = {}
    for h in inf["hallazgos"]:
        if h["id"] == X:
            for u in h["ubicaciones"]:
                if u["archivo"] == P_RV:
                    nivel_de.setdefault(u["linea"], set()).add(h["nivel"])
    for clave, esperado, _ in CASOS:
        obtenido = nivel_de.get(donde[clave], set())
        ok = obtenido == set(esperado.split("+"))
        resultados.append((clave, ok, ""))
        print(f"[{'OK ' if ok else 'MAL'}] {clave}: esperado {esperado}, obtenido {sorted(obtenido) or 'nada'}")
    # que no aparezcan errores nuevos fuera de lo sembrado
    otros = {h["id"] for h in inf["hallazgos"] if h["nivel"] == "ERROR"} - {X}
    ok = otros == {"FX-MC10-003", "RF-0123"}
    resultados.append(("sin otros errores", ok, ""))
    print(f"[{'OK ' if ok else 'MAL'}] fuera de {X}, solo los 2 errores reales: {sorted(otros)}")

ok = huellas() == antes
resultados.append(("corpus intacto", ok, ""))
print(f"[{'OK ' if ok else 'MAL'}] el corpus del repositorio no cambia")
malos = [q for q, ok, _ in resultados if not ok]
print(f"\n{len(resultados) - len(malos)}/{len(resultados)} bien. Fallan: {malos if malos else 'ninguna'}")
sys.exit(1 if malos else 0)
