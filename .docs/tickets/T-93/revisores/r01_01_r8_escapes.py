"""QA r01 de T-93 (revisor independiente): R8 tras la corrección de H-32 y H-33.

Uso: python -I r01_01_r8_escapes.py <ruta a bloque_a/11_Ejecutor> [<ruta a bloque_a/11_Ejecutor anterior a T-93>]
Con la segunda ruta, cada caso se compara con el código anterior (`8604f00`), cargado en un proceso aparte.
Imprime OK/FALLO por caso (INFO no cuenta) y el número de fallos. Las claves se arman en tiempo de ejecución
(nada literal para el gate de secretos).
"""
import json
import random
import string
import subprocess
import sys
import urllib.parse
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
ANTES = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
sys.path.insert(0, str(EJ))
import bloque_a  # noqa: E402

assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.contratos import contiene_credenciales  # noqa: E402
from bloque_a.llm import contenido_sensible  # noqa: E402

fallos = 0


def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))


def info(nombre, detalle=""):
    print("INFO  " + nombre + (f" — {detalle}" if detalle else ""))


SK = "s" + "k-"
CLAVE = SK + "ant-api03-" + "msUpBNeqXSNZ0e2m" * 6 + "AA"


def antes(textos, funcion="contenido_sensible"):
    """Resultado del código anterior a T-93 para cada texto (None si no se dio la ruta)."""
    if ANTES is None:
        return [None] * len(textos)
    prog = ("import json,sys; sys.path.insert(0, sys.argv[1]); from bloque_a.llm import contenido_sensible;"
            "from bloque_a.contratos import contiene_credenciales;"
            f"print(json.dumps([bool({funcion}(t)) for t in json.load(sys.stdin)]))")
    r = subprocess.run([sys.executable, "-I", "-c", prog, str(ANTES)], input=json.dumps(textos), capture_output=True, text=True,
                       check=True)
    return json.loads(r.stdout)


# ------------------------------------------------------------------------------------------------------------------ 1
print("--- 1. Doble escape: JSON dentro de una cadena JSON (p. ej. un resultado de herramienta citado por el agente)")
casos = {
    "doble \\n": json.dumps({"x": json.dumps({"nota": "línea\n" + CLAVE})}),
    "doble \\t": json.dumps({"x": json.dumps({"nota": "a\t" + CLAVE})}),
    "doble \\r": json.dumps({"x": json.dumps({"nota": "a\r" + CLAVE})}),
    "doble \\/": json.dumps({"x": json.dumps({"url": "https://a.example/" + CLAVE}).replace("/", "\\/")}),
    "doble \\u00ab («)": json.dumps({"x": json.dumps({"nota": "«" + CLAVE})}),
    "doble \\u00a0 (NBSP)": json.dumps({"x": json.dumps({"nota": "clave:\u00a0" + CLAVE})}),
    "doble %3D (URL codificada dos veces)": "u=" + urllib.parse.quote(urllib.parse.quote("https://a.example/?key=" + CLAVE, safe=""),
                                                                      safe=""),
    "texto con «\\\\n» literal delante (ruta de Windows o repr de un repr)": "ruta C:\\\\n" + CLAVE,
}
previos = antes(list(casos.values()))
for (nombre, texto), prev in zip(casos.items(), previos):
    ahora = contenido_sensible(texto)
    # Un escape de más no debe ocultar la clave; y en ningún caso T-93 debe detectar menos que el código anterior
    informe(f"1  {nombre}: T-93 {'detecta' if ahora else 'NO detecta'} (antes de T-93: {prev})", ahora, texto[:70])

# Lo mismo con el volcado de `contiene_credenciales` (los textos sueltos se miran tal cual)
d = {"doble \\n como clave de dict": {"nota\\n" + CLAVE: 1}}
for nombre, obj in d.items():
    informe(f"1b {nombre}: contenido_sensible={contenido_sensible(obj)}, contiene_credenciales={bool(contiene_credenciales(obj))}",
            contenido_sensible(obj) and bool(contiene_credenciales(obj)))

# ------------------------------------------------------------------------------------------------------------------ 2
print("--- 2. Escapes que la corrección de H-32 no enumera")
casos2 = {
    "ascii() con emoji (\\U0001f511)": ascii("🔑" + CLAVE),
    "repr() con carácter no imprimible fuera del BMP (\\U000f0000)": repr("\U000f0000" + CLAVE),
    "escape() de JavaScript (%u2014)": "nota=%u2014" + CLAVE,
    "octal de C («\\253»)": "nota \\253" + CLAVE,
    "entidad HTML («&#171;»)": "nota &#171;" + CLAVE,
    "entidad HTML con nombre («&laquo;»)": "nota &laquo;" + CLAVE,
    "\\N{...} de Python": "nota \\N{LEFT-POINTING DOUBLE ANGLE QUOTATION MARK}" + CLAVE,
}
previos2 = antes(list(casos2.values()))
for (nombre, texto), prev in zip(casos2.items(), previos2):
    ahora = contenido_sensible(texto)
    if "U0001f511" in texto or "U000f0000" in texto or "%u2014" in texto or "\\253" in texto:
        informe(f"2  {nombre}: T-93 {'detecta' if ahora else 'NO detecta'} (antes: {prev})", ahora, texto[:60])
    else:
        info(f"2  {nombre}: T-93 {'detecta' if ahora else 'NO detecta'} (antes: {prev})", texto[:60])

# ------------------------------------------------------------------------------------------------------------------ 3
print("--- 3. Contenedores")
fs = frozenset({"\n" + CLAVE})
informe(f"3  frozenset con «\\n» delante: contenido_sensible={contenido_sensible(fs)}, contiene_credenciales="
        f"{bool(contiene_credenciales({'x': fs}))}", contenido_sensible(fs) and bool(contiene_credenciales({"x": fs})))
fs2 = frozenset({"«" + CLAVE})
informe(f"3  frozenset con «««» delante: contiene_credenciales={bool(contiene_credenciales({'x': fs2}))}",
        bool(contiene_credenciales({"x": fs2})))
anidado = {"a": [({CLAVE},)]}
informe(f"3  set dentro de tupla dentro de lista: {contenido_sensible(anidado)}", contenido_sensible(anidado))

# ------------------------------------------------------------------------------------------------------------------ 4
print("--- 4. Falsos positivos residuales con URL de prensa financiera (H-33)")
textos = [
    "https://www.reuters.com/technology/sk-hynix-begins-mass-production-of-lpddr5x-2024-08-12/",
    "https://www.example.com/news/sk-hynix-2nm-foundry-plans-2025-03-01",
    "https://www.example.com/news/sk-hynix-invests-1bn-in-indiana-plant-2024-04-03",
    "https://www.example.com/news/sk-hynix-16gb-ddr5-modules-ship-2024",
    "https://www.example.com/news/sk-siltron-300mm-wafer-capacity-2024",
    "https://www.example.com/news/sk-innovation-q3-loss-widens-to-krw-1-2tn",
    "https://www.example.com/news/sk-hynix-hbm4-12-layer-samples-2025",
    "https://www.example.com/news/sk-telecom-q2-2024-earnings",
    "https://www.example.com/news/sk-hynix-1b-nm-dram-2024",
    "https://www.example.com/news/sk-hynix-cxl-2-0-memory-2024",
]
previos4 = antes(textos)
fp = 0
for t, prev in zip(textos, previos4):
    marca = contenido_sensible(t)
    fp += marca
    info(f"4  {'MARCA' if marca else 'no marca'} (antes: {prev}): {t[30:]}")
info(f"4  falsos positivos: {fp} de {len(textos)}")

# ------------------------------------------------------------------------------------------------------------------ 5
print("--- 5. Recall de claves con «-» o «_» cuyos tramos parecen texto tras la ampliación de RE_TRAMO_TEXTO")
rnd = random.Random(20261112)


def grupos(alfabeto, n, k, sep="-"):
    return sep.join("".join(rnd.choice(alfabeto) for _ in range(n)) for _ in range(k))


formatos = {
    "5 grupos de 5 cifras (estilo licencia numérica)": lambda: SK + grupos(string.digits, 5, 5),
    "4 grupos de 6 cifras": lambda: SK + grupos(string.digits, 6, 4),
    "4 grupos de 8 cifras": lambda: SK + grupos(string.digits, 8, 4),
    "4 grupos de 6 mayúsculas": lambda: SK + grupos(string.ascii_uppercase, 6, 4),
    "3 grupos de 10 mayúsculas": lambda: SK + grupos(string.ascii_uppercase, 10, 3),
    "4 grupos de 7 minúsculas y cifras": lambda: SK + grupos(string.ascii_lowercase + string.digits, 7, 4),
}
for nombre, gen in formatos.items():
    claves = [gen() for _ in range(2000)]
    prev = antes(["clave: " + k for k in claves])
    n_ahora = sum(contenido_sensible("clave: " + k) for k in claves)
    n_antes = sum(prev) if prev[0] is not None else None
    # INFO: ninguna de estas formas es de un proveedor conocido; se mide cuánto cambia frente a la r04
    info(f"5  {nombre}: T-93 {n_ahora}/2000 (antes de T-93: {n_antes}/2000)")

print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
