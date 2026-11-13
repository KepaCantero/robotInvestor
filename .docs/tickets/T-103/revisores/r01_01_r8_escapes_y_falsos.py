"""QA r01 de T-103 (revisor independiente): R8 tras el `RE_ESCAPES` nuevo (H-40) y la regla de colas de cifras (H-41).

Uso: python -I r01_01_r8_escapes_y_falsos.py <ruta a bloque_a/11_Ejecutor> [<ruta a bloque_a/11_Ejecutor anterior a T-103>]
Con la segunda ruta (p. ej. un worktree temporal en `33385c9^`), cada caso se compara con el código anterior, cargado en un
proceso aparte. FALLO solo si T-103 detecta MENOS que el código anterior (regresión) o si un caso que T-103 dice cubrir no se
detecta; lo demás es INFO (formas no enumeradas o falsos positivos nuevos, que se cuentan). Las claves se arman en tiempo de
ejecución (nada literal para el gate de secretos). Sin red.
"""
import base64
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


def antes(textos):
    if ANTES is None:
        return [None] * len(textos)
    prog = ("import json,sys; sys.path.insert(0, sys.argv[1]); from bloque_a.llm import contenido_sensible;"
            "print(json.dumps([bool(contenido_sensible(t)) for t in json.load(sys.stdin)]))")
    r = subprocess.run([sys.executable, "-I", "-c", prog, str(ANTES)], input=json.dumps(textos), capture_output=True, text=True,
                       check=True)
    return json.loads(r.stdout)


rnd = random.Random(20261112)
SK = "s" + "k-"
CUERPO = "".join(rnd.choice(string.ascii_letters + string.digits) for _ in range(90))
CLAVE = SK + "ant-api03-" + CUERPO + "AA"
CLAVE_PROJ = SK + "proj-" + "".join(rnd.choice(string.ascii_letters + string.digits) for _ in range(48))

# ------------------------------------------------------------------------------------------------------------------ 1
print("--- 1. Escapes y codificaciones que dejan una letra o cifra pegada a la clave")
casos = {
    # combinaciones de dos capas que el RE_ESCAPES nuevo no deshace (sustituye por espacio, no decodifica)
    "%5Cn (barra de JSON codificada en URL, luego «n»)": "nota=" + "%5Cn" + CLAVE,
    "%5C%5Cn (doble barra codificada en URL)": "nota=" + "%5C%5Cn" + CLAVE,
    "\\u005cn (barra escrita como \\u005c y luego «n»)": '{"x": "a\\u005cn' + CLAVE + '"}',
    "\\x5cn (barra como \\x5c de repr y luego «n»)": "'a\\x5cn" + CLAVE + "'",
    "quoted-printable =3D (correo .eml)": "key=3D" + CLAVE,
    "quoted-printable =0A": "linea=0A" + CLAVE,
    "\\a de C (campana)": "nota \\a" + CLAVE,
    "\\v de C (tabulador vertical)": "nota \\v" + CLAVE,
    "\\e de bash/printf": "nota \\e" + CLAVE,
    "\\N{…} de Python (declarado)": "nota \\N{LINE FEED}" + CLAVE,
    "entidad HTML &#10; (declarado)": "nota&#10;" + CLAVE,
    "base64 de la clave": "dato: " + base64.b64encode(CLAVE.encode()).decode(),
    "clave con espacio de ancho cero dentro (\\u200b)": "clave: " + CLAVE[:12] + "\u200b" + CLAVE[12:],
    "clave con guion blando dentro (\\u00ad)": "clave: " + CLAVE[:12] + "\u00ad" + CLAVE[12:],
    "clave proj- con escape \\u0041 dentro (JSON con ensure_ascii)": '{"k": "' + CLAVE_PROJ[:10] + "\\u0041" + CLAVE_PROJ[11:] + '"}',
    "%U2014 (mayúscula, no estándar)": "nota %U2014" + CLAVE,
    "clave partida por \\n en JSON (líneas de 16)": json.dumps({"k": "\n".join(CLAVE[i:i + 16] for i in range(0, len(CLAVE), 16))}),
}
previos = antes(list(casos.values()))
for (nombre, texto), prev in zip(casos.items(), previos):
    ahora = contenido_sensible(texto)
    if prev is True and not ahora:
        informe(f"1  {nombre}: regresión (antes detectaba)", False, texto[:60])
    else:
        info(f"1  {nombre}: T-103 {'detecta' if ahora else 'NO detecta'} (antes: {prev})", texto[:60])

# los que T-103 dice cubrir, también de tres capas
print("--- 1b. Lo que T-103 declara cubierto, en tres y cuatro capas")
tres = {
    "JSON en JSON en JSON, «\\n»": json.dumps({"a": json.dumps({"b": json.dumps({"c": "x\n" + CLAVE})})}),
    "cuatro capas, «\\t»": json.dumps({"a": json.dumps({"b": json.dumps({"c": json.dumps({"d": "x\t" + CLAVE})})})}),
    "URL codificada tres veces": "u=" + urllib.parse.quote(urllib.parse.quote(urllib.parse.quote("?key=" + CLAVE, safe=""), safe=""),
                                                          safe=""),
    "repr de repr de «\\n»": repr(repr("x\n" + CLAVE)),
    "ascii de json con emoji": ascii(json.dumps({"n": "🔑" + CLAVE}, ensure_ascii=False)),
    "\\U0001F511 en mayúsculas": "nota \\U0001F511" + CLAVE,
}
for nombre, texto in tres.items():
    informe(f"1b {nombre}", contenido_sensible(texto) and bool(contiene_credenciales({"t": texto})), texto[:60])

# ------------------------------------------------------------------------------------------------------------------ 2
print("--- 2. Falsos positivos nuevos de la expresión ancha (textos con «sk-» detrás de un escape)")
reales = [
    # rutas de Windows (tal cual y dentro de un JSON) con carpetas o ficheros que empiezan por «sk-»
    "C:\\Informes\\sk-hynix-q2-2024-earnings.pdf",
    json.dumps({"ruta": "C:\\Informes\\sk-hynix-q2-2024-earnings.pdf"}),
    json.dumps({"r": json.dumps({"ruta": "C:\\Informes\\sk-hynix-q2-2024-earnings.pdf"})}),
    json.dumps({"ruta": "D:\\datos\\2024\\sk-telecom_annual_report_2023.xlsx"}),
    json.dumps({"ruta": "C:\\Users\\analista\\Desktop\\nsk-6205-2rs-bearing-datasheet.pdf"}),
    json.dumps({"r": json.dumps({"ruta": "C:\\docs\\nsk-6205-2rs-bearing-datasheet.pdf"})}),
    json.dumps({"r": json.dumps({"ruta": "C:\\docs\\tsk-001-quarterly-review-final-v2.docx"})}),
    # JSON anidado con titulares (texto corriente detrás de «\n» doble)
    json.dumps({"x": json.dumps({"nota": "Titular:\nsk-hynix-posts-record-q3-profit-2024"})}),
    json.dumps({"x": json.dumps({"nota": "Titular:\nsk-hynix-16gb-ddr5-modules-ship-2024"})}),
    json.dumps({"x": json.dumps({"nota": "Titular:\nsk-siltron-300mm-wafer-capacity-2024"})}),
    json.dumps({"x": json.dumps({"nota": "\nsk-innovation-q3-loss-widens-to-krw-1-2tn"})}),
    # octales y \U de rutas y volcados
    "C:\\2024\\0sk-informe-trimestral-del-fondo-2024",
    "valor\\101sk-hynix-hbm3e-supply-deal-with-nvidia",
    # textos con fechas, horas y referencias de solo cifras (regla nueva de H-41)
    "https://www.example.com/news/sk-2024-07-25-2024-07-26",
    "log: sk-2024-11-12-10-30-00-123",
    "Ref. SK-421-02-5930-1234-5678",
    "Pedido sk-0001-0002-0003-0004-0005",
    "https://www.example.com/sk-hynix-2024-07-25-10-30",
    # texto financiero normal con porcentajes codificados en URL
    "https://www.example.com/search?q=sk-hynix%20margen%2015%25%20q3-2024-resultados",
    "https://www.example.com/a?b=50%25sk-hynix-posts-record-q3-profit-2024",
]
previos = antes(reales)
nuevos = 0
for texto, prev in zip(reales, previos):
    ahora = contenido_sensible(texto)
    if ahora and prev is False:
        nuevos += 1
    info(f"2  {'MARCA' if ahora else 'no marca'} (antes: {prev})", texto[:90])
info("2  falsos positivos nuevos frente al código anterior", f"{nuevos} de {len(reales)}")

# ------------------------------------------------------------------------------------------------------------------ 3
print("--- 3. Recall de colas de solo cifras (H-41): lo que la regla de «4 o más tramos» deja fuera")


def colas(n, k, sep="-", m=500):
    return [SK + sep.join("".join(rnd.choice(string.digits) for _ in range(n)) for _ in range(k)) for _ in range(m)]


for n, k in ((7, 3), (6, 3), (10, 2), (5, 4), (8, 3), (6, 4)):
    cs = colas(n, k)
    vistos = sum(contenido_sensible("clave: " + c) for c in cs)
    p = antes(["clave: " + c for c in cs[:50]])
    info(f"3  {k} grupos de {n} cifras", f"T-103 {vistos}/{len(cs)} (antes, 50 primeros: {sum(bool(x) for x in p) if p[0] is not None else None}/50)")
# 3 grupos de fechas AAAAMMDD válidas
fechas = [SK + "-".join(f"20{rnd.randint(10, 29)}{rnd.randint(1, 12):02d}{rnd.randint(1, 28):02d}" for _ in range(3)) for _ in range(500)]
info("3  3 grupos de fechas AAAAMMDD válidas", f"T-103 {sum(contenido_sensible('clave: ' + c) for c in fechas)}/500")
informe("3  la regla nueva: 4 grupos de 6 cifras", all(contenido_sensible("clave: " + c) for c in colas(6, 4, m=200)))
informe("3  la regla nueva con «_»: 4 grupos de 6 cifras", all(contenido_sensible("clave: " + c) for c in colas(6, 4, "_", m=200)))

print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
