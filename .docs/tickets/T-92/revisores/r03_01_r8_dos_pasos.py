"""QA r03 de T-92 (revisor nuevo): ataques a R8 en dos pasos (`RE_CANDIDATO_SK` + `_es_clave_sk`, H-17 y H-18).

Uso: python -I r03_01_r8_dos_pasos.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso (INFO no cuenta). Compara con la rama `sk-` de develop (`dae70df`), reconstruida aquí, porque el
criterio de la QA r02 es que toda clave que develop detecta se siga detectando. Las claves se arman en tiempo de ejecución.
"""
import json, random, re, secrets, string, sys, tempfile, time, uuid
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.almacen import Almacen
from bloque_a.contratos import DatosSensibles, Mensajeria, contiene_credenciales, secretos_en_texto
from bloque_a.llm import contenido_sensible

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

SK = "s" + "k-"
B64URL = string.ascii_letters + string.digits + "-_"
ALNUM = string.ascii_letters + string.digits
HEX = "0123456789abcdef"
DEVELOP = re.compile(r"(?i)(" + SK + r"[A-Za-z0-9_-]{20,})")
rnd = random.Random(20261111)
def cuerpo(alfabeto, n):
    return "".join(rnd.choice(alfabeto) for _ in range(n))
def u4():
    return str(uuid.UUID(int=rnd.getrandbits(128), version=4))
def urlsafe(nbytes):   # misma forma que secrets.token_urlsafe(nbytes), con semilla fija
    import base64
    return base64.urlsafe_b64encode(bytes(rnd.getrandbits(8) for _ in range(nbytes))).rstrip(b"=").decode()

def mide(nombre, gen, n=4000, contexto="clave: {}", debe=True):
    claves = [gen() for _ in range(n)]
    dev = sum(1 for k in claves if DEVELOP.search(contexto.format(k)))
    r03 = [k for k in claves if not contenido_sensible(contexto.format(k))]
    cc = [k for k in claves if not contiene_credenciales({"x": contexto.format(k)})]
    ok = (not r03 and not cc) if debe else True
    informe(f"1  {nombre}: r03 detecta {n - len(r03)}/{n} (contiene_credenciales {n - len(cc)}/{n}; develop {dev}/{n})", ok,
            f"p. ej. …{r03[0][3:9]}…" if r03 else "")
    return len(r03)

# 1. Formas de clave reales o plausibles
print("--- 1. Falsos negativos por formato")
mide("Anthropic api03 (93 base64url + AA)", lambda: SK + "ant-api03-" + cuerpo(B64URL, 93) + "AA")
mide("Anthropic admin01", lambda: SK + "ant-admin01-" + cuerpo(B64URL, 93) + "AA")
mide("OpenAI proj (156 base64url)", lambda: SK + "proj-" + cuerpo(B64URL, 156))
mide("OpenAI svcacct", lambda: SK + "svcacct-" + cuerpo(B64URL, 156))
mide("OpenAI admin", lambda: SK + "admin-" + cuerpo(B64URL, 156))
mide("OpenAI clásica (48 alfanuméricos)", lambda: SK + cuerpo(ALNUM, 48))
mide("hexadecimal 32 (p. ej. DeepSeek)", lambda: SK + cuerpo(HEX, 32))
mide("hexadecimal 64 tras or-v1- (OpenRouter)", lambda: SK + "or-v1-" + cuerpo(HEX, 64))
n_uuid = mide("UUID v4 en minúsculas", lambda: SK + u4())
n_lf = mide("lf- + UUID (Langfuse)", lambda: SK + "lf-" + u4())
mide("UUID v4 en mayúsculas", lambda: SK + u4().upper())
n_lite = mide("token_urlsafe(16) (22 car., p. ej. LiteLLM)", lambda: SK + urlsafe(16))
mide("token_urlsafe(32)", lambda: SK + urlsafe(32))
mide("hexadecimal 40 con «-» cada 8", lambda: SK + "-".join(cuerpo(HEX, 8) for _ in range(5)))
mide("minúsculas y cifras, «_» cada 10", lambda: SK + "_".join(cuerpo(string.ascii_lowercase + string.digits, 10) for _ in range(4)))

print("--- 1b. Contextos: delante de la clave")
gen = lambda: SK + "proj-" + cuerpo(B64URL, 156)
for ctx, debe in [("https://api.example.com/v1/keys/{}", True), ("OPENAI-KEY-{}", True), ("config.{}", True),
                  ("OPENAI_KEY_{}", True), ("clave={}", True), ("«{}»", True), ("({})", True)]:
    mide(f"proj- en «{ctx[:-2]}…»", gen, n=200, contexto=ctx, debe=debe)
k = SK.upper() + "proj-" + cuerpo(B64URL, 60)
informe("1c prefijo en mayúsculas «SK-proj-…» (develop: case-insensitive)", contenido_sensible(k),
        f"develop={bool(DEVELOP.search(k))}, r03={contenido_sensible(k)}")

# 2. H-18: separadores y estructuras
print("--- 2. H-18 y estructuras")
clave = SK + "ant-api03-" + cuerpo(B64URL, 93) + "AA"
for sep in ["\n", "\t", "\r\n", "\\n", " ", "\x00", " "]:
    t = "clave:" + sep + clave
    informe(f"2  contiene_credenciales detecta tras {sep!r}", bool(contiene_credenciales({"texto": t})),
            f"contenido_sensible={contenido_sensible(t)}")
for nombre, obj in [("clave de dict", {clave: 1}), ("lista anidada", [[["x", "\n" + clave]]]), ("tupla", ("a", "\n" + clave)),
                    ("set", {"\n" + clave}), ("bytes", {"x": ("\n" + clave).encode()})]:
    informe(f"2b contiene_credenciales en {nombre}", bool(contiene_credenciales(obj)))
with tempfile.TemporaryDirectory() as d:
    ms = Mensajeria(Almacen(Path(d)))
    try:
        ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "mi clave:\n" + SK + u4()})
        informe("2c un CT-03 con «sk-<uuid>» en su línea se rechaza (develop lo rechaza)", False, "mensaje creado")
    except DatosSensibles:
        informe("2c un CT-03 con «sk-<uuid>» en su línea se rechaza (develop lo rechaza)", True)

# 2d. Respuesta del modelo en JSON con la clave tras un salto de línea DENTRO de una cadena: en el texto va como «\n»
#     literal (barra y n). respuesta_segura no la ve y la grabadora (ReplayClient «grabar») la escribe en la cinta
from bloque_a.llm import LLMClient, ReplayClient, RespuestaLLM, Uso
texto_json = json.dumps({"nota": "clave del proveedor:\n" + clave})
informe("2d contenido_sensible ve la clave tras «\\n» en un texto JSON (develop sí)", contenido_sensible(texto_json),
        f"develop={bool(DEVELOP.search(texto_json))}")
class _Base(LLMClient):
    nombre = "base"
    def generar(self, **kw):
        return RespuestaLLM(texto_json, Uso(), "m", "end_turn")
with tempfile.TemporaryDirectory() as d:
    cinta = Path(d) / "cinta.jsonl"
    ReplayClient(cinta, "grabar", _Base()).generar(agente="AG-02", modelo="m", system=[], mensajes=[{"role": "user", "content": "x"}],
                                                  max_tokens=10)
    informe("2e la clave de la respuesta no llega a la cinta grabada", clave not in cinta.read_text(encoding="utf-8").replace("\\n", "\n")
            and clave not in cinta.read_text(encoding="utf-8"), "la cinta contiene la clave")

# 3. Falsos positivos con texto financiero
print("--- 3. Falsos positivos")
corrientes = [
    "Fuente: https://johnhcochrane.com/research-all/the-risk-and-return-of-venture-capital",
    "https://www.reuters.com/technology/" + SK + "hynix-posts-record-quarterly-profit-2024-10-24/",
    "ver " + SK + "hynix_annual_report_2023.pdf", "ver " + SK + "innovation_to_merge_with_enmove",
    "SK-Hynix (000660.KS) y SK Telecom (SKM) publican resultados", "el task-force-on-climate-related-financial-disclosures",
    "fichero " + SK + "telecom-annual-report-2023.pdf", "risk-on/risk-off-regime-2024-Q3-analysis",
    "Descarga: " + SK + "hynix_3Q24_earnings_release.pdf",                    # nombre de fichero de relación con inversores
    "Descarga: " + SK + "Hynix-Q3-2024-Earnings-Presentation.pdf",
    "ticker " + SK + "innovation-2024Q4-results-presentation",
    "ver " + SK + "biopharm_FY2023_annual_report_EN.pdf",
]
for t in corrientes:
    informe(f"3  no es clave: {t[:60]!r}", not contenido_sensible(t), f"hallado {[h[:12] for h in secretos_en_texto(t)]}")

# 3b. Corpus operativo del Bloque A (F7, registro de fuentes, prompts): líneas que r03 marca y develop también
raiz = EJ.parent
lineas = []
for p in raiz.rglob("*.md"):
    if "11_Ejecutor" in p.parts:
        continue
    lineas += [l for l in p.read_text(encoding="utf-8", errors="replace").splitlines() if SK in l.lower()]
marcadas = [l for l in lineas if contenido_sensible(l)]
informe(f"3b corpus del Bloque A: {len(lineas)} líneas con «sk-», r03 marca {len(marcadas)} "
        f"(develop {sum(1 for l in lineas if DEVELOP.search(l))})", not marcadas, marcadas[0][:80] if marcadas else "")

# 4. Tiempo con entradas adversarias
print("--- 4. Tiempo")
peor, cual = 0.0, ""
for nombre, s in [("_sk- repetido 140 KB", ("_" + SK) * 35000), ("sk- + a- ×200k", " " + SK + "a-" * 200_000),
                  ("candidatos de 20 sin clave ×20k", (" " + SK + "a" * 9 + "-" + "b" * 10) * 20000),
                  ("sk-sk-sk- 1 MB", SK * 330_000), ("«-» ×1M", " " + SK + "-" * 1_000_000),
                  ("bearer + espacios", "bearer " + " " * 200_000 + "x"), ("\"password\": sin cierre", '"password": "' + "a" * 500_000)]:
    t0 = time.perf_counter(); contenido_sensible(s); contiene_credenciales({"x": s}); dt_ = time.perf_counter() - t0
    if dt_ > peor:
        peor, cual = dt_, nombre
anidado = "\n" + clave
for _ in range(400):
    anidado = {"a": anidado}
t0 = time.perf_counter(); r = contenido_sensible(anidado); t_anid = time.perf_counter() - t0
informe(f"4  peor tiempo {peor:.2f} s ({cual}) < 2 s", peor < 2)
print(f"INFO  4b dict anidado 400 niveles: contenido_sensible={r} en {t_anid:.2f} s (vuelca el JSON en cada nivel: O(n·prof.))")
print("fallos:", fallos)
