"""QA r02 de T-92 (revisor nuevo): ataques al patrón `sk-` de R8 tras H-07.

Uso: python -I r02_01_r8_sk.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso. Compara con el patrón de develop (`dae70df`), que se reconstruye aquí tal cual para medir
si la corrección relaja el control respecto a develop. Las claves son aleatorias y se arman en tiempo de ejecución.
"""
import json, random, re, string, sys, tempfile, time
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.almacen import Almacen
from bloque_a.contratos import RE_SECRETO, DatosSensibles, Mensajeria, contiene_credenciales
from bloque_a.llm import contenido_sensible

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

SK = "s" + "k-"
B64URL = string.ascii_letters + string.digits + "-_"
DEVELOP = re.compile(r"(?i)(" + SK + r"[A-Za-z0-9_-]{20,})")     # rama sk- de RE_SECRETO en develop (dae70df)
rnd = random.Random(20261110)

def clave(prefijo, n, sufijo=""):
    return SK + prefijo + "".join(rnd.choice(B64URL) for _ in range(n)) + sufijo

# 1. Falsos negativos con claves de forma real (cuerpo base64url aleatorio, con «-» y «_»)
N = 5000
for nombre, pre, n, suf in [("Anthropic sk-ant-api03-…AA", "ant-api03-", 93, "AA"), ("OpenAI sk-proj-…", "proj-", 156, ""),
                            ("OpenAI sk-svcacct-…", "svcacct-", 156, "")]:
    claves = [clave(pre, n, suf) for _ in range(N)]
    fn = [k for k in claves if not contenido_sensible("clave " + k)]
    fn_dev = [k for k in claves if not DEVELOP.search(k)]
    informe(f"1  R8 detecta todas las claves {nombre} (develop: {N - len(fn_dev)}/{N})", not fn,
            f"no detectadas {len(fn)}/{N}; p. ej. {fn[0][:6]}…{fn[0][13:40]}" if fn else "")

# 1b. Una clave concreta (cuerpo fijo, no aleatorio) que develop detecta y la r02 no
k = SK + "ant-api03-" + "Y_5MjTTl-oU_YYlXAjGby-DqOUUaRuqlRzb1iJ00LTRN8116jpRjhe5vqUykkcmAs-eq04pXB5_iUhE41kcD4jU4INMjrAA"
informe("1b clave sk-ant-api03-Y_5MjTTl-oU_… detectada (develop la detecta)", contenido_sensible(k),
        f"develop={bool(DEVELOP.search(k))}, r02={contenido_sensible(k)}")

# 2. El volcado JSON de contiene_credenciales (sobre de mensajes, CT-23, salidas de agentes) escapa el salto de línea:
#    «\nsk-…» pasa a «\\nsk-…» y el límite izquierdo ve una «n»
cuerpo_clave = SK + "proj-" + "Ab3Xy9" * 8
for sep, nombre in [("\n", "salto de línea"), ("\t", "tabulador"), ("\r\n", "CRLF")]:
    texto = "clave del proveedor:" + sep + cuerpo_clave
    informe(f"2  contiene_credenciales detecta la clave tras un {nombre}", bool(contiene_credenciales({"texto": texto})),
            f"texto crudo: contenido_sensible={contenido_sensible(texto)}; develop sobre el volcado="
            f"{bool(DEVELOP.search(json.dumps({'texto': texto})))}")
with tempfile.TemporaryDirectory() as d:
    ms = Mensajeria(Almacen(Path(d)))
    try:
        ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "Uso esta clave:\n" + cuerpo_clave})
        informe("2b un CT-03 con la clave en una línea propia se rechaza íntegro (R8)", False, "mensaje creado")
    except DatosSensibles:
        informe("2b un CT-03 con la clave en una línea propia se rechaza íntegro (R8)", True)

# 3. Falsos positivos realistas (nombres de archivo o identificadores con guion bajo)
for texto in ["Fuente: sk-hynix_annual_report_2023.pdf", "ver sk-innovation_to_merge_with_enmove",
              "SK-Biopharmaceuticals publica resultados", "https://www.reuters.com/technology/sk-hynix-posts-record-quarterly-profit-2024-10-24/"]:
    informe(f"3  texto corriente no es clave: {texto[:45]!r}", not contenido_sensible(texto))

# 4. Sin retroceso catastrófico (entradas de 1 MB, adversarias para el tramo perezoso)
peor = 0.0
for s in ["(" + SK + "a-" * 500_000 + ")", " " + SK * 330_000, "_" + (SK + "_") * 250_000, " " + SK + "-" * 1_000_000,
          ("x " + SK + "a" * 15 + "-") * 50_000, ("\n" + SK + "ab-" * 7) * 40_000]:
    t = time.perf_counter(); RE_SECRETO.search(s); peor = max(peor, time.perf_counter() - t)
informe("4  RE_SECRETO tarda < 2 s con entradas adversarias de ~1 MB", peor < 2, f"peor {peor:.2f} s")
print("fallos:", fallos)
