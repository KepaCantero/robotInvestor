"""QA r04 de T-92 (revisor nuevo): la regla definitiva de R8 para «sk-» (H-25, H-26, H-28), frente a develop (`dae70df`).

Uso: python -I r04_01_r8_regla_texto.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso (INFO no cuenta). La rama «sk-» de develop se reconstruye aquí (cualquier «sk-» con 20 o más de
[A-Za-z0-9_-], sin límite por la izquierda). Las claves se arman en tiempo de ejecución (nada literal para el gate de secretos).
"""
import base64, json, random, re, string, sys, tempfile, time, urllib.parse, uuid
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.contratos import _es_clave_sk, contiene_credenciales, secretos_en_texto
from bloque_a.llm import LLMClient, ReplayClient, RespuestaLLM, Uso, contenido_sensible

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))
def info(nombre, detalle=""):
    print("INFO  " + nombre + (f" — {detalle}" if detalle else ""))

SK = "s" + "k-"
B64URL = string.ascii_letters + string.digits + "-_"
ALNUM = string.ascii_letters + string.digits
HEX = "0123456789abcdef"
B32L = "abcdefghijklmnopqrstuvwxyz234567"
DEVELOP = re.compile(r"(?i)(" + SK + r"[A-Za-z0-9_-]{20,})")
rnd = random.Random(20261112)
def cuerpo(alfabeto, n):
    return "".join(rnd.choice(alfabeto) for _ in range(n))
def u4():
    return str(uuid.UUID(int=rnd.getrandbits(128), version=4))
def urlsafe(nbytes):   # misma forma que secrets.token_urlsafe(nbytes), con semilla fija
    return base64.urlsafe_b64encode(bytes(rnd.getrandbits(8) for _ in range(nbytes))).rstrip(b"=").decode()

# ---------------------------------------------------------------------------------------------------------------- 1
print("--- 1. Recall por formato (contexto «clave: …»), r04 frente a develop")
def mide(nombre, gen, n=4000, contexto="clave: {}", minimo=1.0, falla=True):
    claves = [gen() for _ in range(n)]
    dev = sum(1 for k in claves if DEVELOP.search(contexto.format(k)))
    perdidas = [k for k in claves if not contenido_sensible(contexto.format(k))]
    cc = [k for k in claves if not contiene_credenciales({"x": contexto.format(k)})]
    tasa = 1 - len(perdidas) / n
    linea = f"{nombre}: r04 {n - len(perdidas)}/{n} (contiene_credenciales {n - len(cc)}/{n}; develop {dev}/{n})"
    if falla:
        informe("1  " + linea, tasa >= minimo and not cc, f"p. ej. …{perdidas[0][3:30]}…" if perdidas else "")
    else:
        info("1  " + linea, f"p. ej. …{perdidas[0][3:40]}…" if perdidas else "")
    return len(perdidas)

mide("Anthropic api03 (93 base64url + AA)", lambda: SK + "ant-api03-" + cuerpo(B64URL, 93) + "AA")
mide("Anthropic admin01", lambda: SK + "ant-admin01-" + cuerpo(B64URL, 93) + "AA")
mide("OpenAI proj", lambda: SK + "proj-" + cuerpo(B64URL, 156))
mide("OpenAI svcacct", lambda: SK + "svcacct-" + cuerpo(B64URL, 156))
mide("OpenAI admin", lambda: SK + "admin-" + cuerpo(B64URL, 156))
mide("OpenAI clásica (48 alfanuméricos)", lambda: SK + cuerpo(ALNUM, 48))
mide("hexadecimal 32", lambda: SK + cuerpo(HEX, 32))
mide("or-v1- + hexadecimal 64", lambda: SK + "or-v1-" + cuerpo(HEX, 64))
mide("UUID v4", lambda: SK + u4())
mide("UUID v4 en mayúsculas", lambda: SK + u4().upper())
mide("lf- + UUID", lambda: SK + "lf-" + u4())
mide("hexadecimal con «-» cada 8", lambda: SK + "-".join(cuerpo(HEX, 8) for _ in range(5)))
mide("minúsculas y cifras con «_» cada 10", lambda: SK + "_".join(cuerpo(string.ascii_lowercase + string.digits, 10) for _ in range(4)))
mide("solo minúsculas, 32 seguidas", lambda: SK + cuerpo(string.ascii_lowercase, 32))
mide("«SK-» + token_urlsafe(24)", lambda: "SK-" + urlsafe(24))
# token_urlsafe: la cola puede partirse en tramos cortos que parezcan texto; se mide la tasa con muchas muestras
for nb in (16, 24, 32):
    n = 50_000
    perd = sum(1 for _ in range(n) if not _es_clave_sk(urlsafe(nb)))
    informe(f"1b token_urlsafe({nb}): {perd} de {n} colas no se toman por clave ({perd / n:.4%}; develop 0)", perd / n < 0.001)
mide("helicone- + 4 grupos base32 de 7", lambda: SK + "helicone-" + "-".join(cuerpo(B32L, 7) for _ in range(4)), falla=False)
mide("grupos de 4 mayúsculas y cifras (estilo licencia)", lambda: SK + "-".join(cuerpo(string.ascii_uppercase + string.digits, 4)
                                                                                  for _ in range(5)), falla=False)
mide("grupos de 8 minúsculas sin cifras («-»)", lambda: SK + "-".join(cuerpo(string.ascii_lowercase, 8) for _ in range(4)), falla=False)

# ---------------------------------------------------------------------------------------------------------------- 2
print("--- 2. Recall por lo que va delante (clave proj- y ant-api03)")
ant = lambda: SK + "ant-api03-" + cuerpo(B64URL, 93) + "AA"
for ctx in ["https://api.example.com/v1/keys/{}", "OPENAI-KEY-{}", "config.{}", "OPENAI_KEY_{}", "key-{}", "clave={}",
            "«{}»", "“{}”", "clave: {}", "clave —{}", "\t{}", "({})", "`{}`"]:
    mide(f"delante «{ctx.split('{}')[0][-12:]}»", ant, n=200, contexto=ctx)
# escapes de JSON que la r04 no sustituye y codificaciones de URL: develop los detecta
print("--- 2b. Escapes que quedan delante de la clave en un texto (JSON con ensure_ascii, URL codificada, repr)")
clave = ant()
casos = {
    "JSON \\u00ab («)": json.dumps({"nota": "la clave «" + clave + "»"}),
    "JSON \\u201c (“)": json.dumps({"nota": "clave “" + clave + "”"}),
    "JSON \\u00a0 (NBSP)": json.dumps({"nota": "clave: " + clave}),
    "JSON \\u2014 (—)": json.dumps({"nota": "clave —" + clave}),
    "JSON emoji \\ud83d\\udd11": json.dumps({"nota": "\U0001F511" + clave}),
    "JSON \\f": json.dumps({"nota": "\f" + clave}),
    "JSON \\b": json.dumps({"nota": "\b" + clave}),
    "URL %3D (key=)": "https://x.example/cb?next=" + urllib.parse.quote("https://api.example/v1?key=" + clave, safe=""),
    "URL %20 (espacio)": "q=" + urllib.parse.quote("mi clave " + clave),
    "repr \\xa0": repr("clave: " + clave),
}
for nombre, texto in casos.items():
    dev = bool(DEVELOP.search(texto))
    r04 = contenido_sensible(texto)
    informe(f"2b {nombre}: contenido_sensible(texto) detecta (develop {dev})", r04 or not dev, texto[:40].replace(clave, "<clave>"))
# camino real: la grabadora escribe en la cinta la respuesta que no ve respuesta_segura
texto_json = casos["JSON \\u00ab («)"]
class _Base(LLMClient):
    nombre = "base"
    def generar(self, **kw):
        return RespuestaLLM(texto_json, Uso(), "m", "end_turn")
with tempfile.TemporaryDirectory() as d:
    cinta = Path(d) / "cinta.jsonl"
    r = ReplayClient(cinta, "grabar", _Base()).generar(agente="AG-02", modelo="m", system=[],
                                                       mensajes=[{"role": "user", "content": "x"}], max_tokens=10)
    en_cinta = clave in cinta.read_text(encoding="utf-8")
    informe("2c respuesta JSON con «\\u00ab» delante de la clave: no llega a la cinta grabada (develop no la graba)",
            not en_cinta, f"stop_reason={r.stop_reason}; cinta con la clave={en_cinta}")
    informe("2c los datos ya leídos sí se bloquean (contiene_credenciales(json.loads(texto)))",
            bool(contiene_credenciales(json.loads(texto_json))))
# estructuras
print("--- 2d. Estructuras, bytes y claves de dict")
for nombre, obj in [("clave de dict", {clave: 1}), ("valor bytes", {"x": clave.encode()}), ("bytes sueltos", clave.encode()),
                    ("bytearray", bytearray(clave.encode())), ("lista anidada", [[["\n" + clave]]]),
                    ("tupla en dict", {"t": ("a", "\t" + clave)}), ("set en dict", {"s": {" " + clave}}),
                    ("set en dict con \\n", {"s": {"\n" + clave}})]:
    cs = contenido_sensible(obj)
    cc = bool(contiene_credenciales(obj)) if not isinstance(obj, (bytes, bytearray)) else None
    ok = cs and cc is not False
    (informe if nombre != "set en dict" else info)(f"2d {nombre}: contenido_sensible={cs}, contiene_credenciales={cc}", ok)

# ---------------------------------------------------------------------------------------------------------------- 3
print("--- 3. Falsos positivos con texto financiero (r04 / develop)")
def fp(t, esperado_texto=True, cuenta=True):
    r04 = contenido_sensible(t)
    dev = bool(DEVELOP.search(t))
    nombre = f"3  no es clave: {t[:70]!r} (develop {'marca' if dev else 'no marca'})"
    if cuenta:
        informe(nombre, not r04, f"hallado {[h[:24] for h in secretos_en_texto(t)]}")
    else:
        info(nombre + f": r04 {'marca' if r04 else 'no marca'}")
    return r04
# los que piden H-01, H-07 y H-28 (deben pasar)
for t in ["Fuente: https://johnhcochrane.com/research-all/the-risk-and-return-of-venture-capital",
          "https://www.reuters.com/technology/" + SK + "hynix-posts-record-quarterly-profit-2024-10-24/",
          "ver " + SK + "hynix_annual_report_2023.pdf", "ticker " + SK + "innovation-2024Q4-results-presentation",
          "ver " + SK + "biopharm_FY2023_annual_report_EN.pdf", "Descarga: " + SK + "hynix_3Q24_earnings_release.pdf",
          "SK-Hynix-Q3-2024-Earnings-Presentation.pdf", "el task-force-on-climate-related-financial-disclosures",
          "risk-on/risk-off-regime-2024-Q3-analysis", "desk-research-and-analysis-of-markets-2024"]:
    fp(t)
# textos financieros corrientes que la r04 toma por clave (no cuentan como FALLO: se mide la tasa)
reales = [
    "https://www.reuters.com/technology/" + SK + "hynix-q2-profit-jumps-on-ai-chip-demand-2024-07-25/",
    "https://www.reuters.com/technology/" + SK + "hynix-posts-record-q3-profit-2024-10-24/",
    "https://www.reuters.com/business/" + SK + "telecom-5g-subscribers-rise-2024-05-08/",
    "https://www.example.com/news/" + SK + "hynix-hbm3e-supply-deal-with-nvidia",
    "https://www.example.com/ir/" + SK + "biopharm-fy2023-annual-report",
    "Descarga: " + SK + "hynix_20240725_earnings_release.pdf",
    "https://www.marketscreener.com/quote/stock/" + SK.upper() + "TELECOM-CO-LTD-6496057/news/",
    "https://www.marketscreener.com/quote/stock/" + SK.upper() + "INNOVATION-CO-LTD-6494944/",
    SK.upper() + "HYNIX-QUARTERLY-RESULTS-2024",
    "https://www.example.com/" + SK + "hynix-1q24-earnings-call-transcript",
    "https://www.example.com/" + SK + "hynix-000660-stock-analysis",
    SK + "HynixEarnings-2024-summary",
]
marcados = [t for t in reales if fp(t, cuenta=False)]
info(f"3b textos financieros reales que r04 toma por clave: {len(marcados)} de {len(reales)} (r03 con el límite «/»: los de URL no)")
# corpus del Bloque A
raiz = EJ.parent
lineas = []
for p in list(raiz.rglob("*.md")) + list(raiz.rglob("*.yaml")) + list(raiz.rglob("*.json")):
    if "11_Ejecutor" in p.parts and "tests" in p.parts:
        continue
    try:
        lineas += [l for l in p.read_text(encoding="utf-8", errors="replace").splitlines() if SK in l.lower()]
    except OSError:
        pass
marc = [l for l in lineas if contenido_sensible(l)]
informe(f"3c corpus del Bloque A (md, yaml, json): {len(lineas)} líneas con «sk-»; r04 marca {len(marc)} "
        f"(develop {sum(1 for l in lineas if DEVELOP.search(l))})", not marc, marc[0][:80] if marc else "")

# ---------------------------------------------------------------------------------------------------------------- 4
print("--- 4. Tiempo con entradas adversarias (contenido_sensible + contiene_credenciales)")
peor, cual = 0.0, ""
for nombre, s in [("sk-sk-sk- 1 MB", SK * 330_000), (" sk-a-a-a… 1 MB", " " + SK + "a-" * 500_000),
                  ("candidatos texto ×40k", (" " + SK + "hynix-annual-report-2023") * 40_000),
                  ("«\\n» ×300k + sk-", "\\n" * 300_000 + SK + "a" * 30), ("tramos de 15 letras", " " + SK + ("abcdefghijklmno-" * 60_000)),
                  ("«_» ×1M", " " + SK + "_" * 1_000_000), ("bytes 1 MB", (SK * 330_000).encode())]:
    t0 = time.perf_counter()
    contenido_sensible(s)
    if not isinstance(s, bytes):
        contiene_credenciales({"x": s})
    dt_ = time.perf_counter() - t0
    if dt_ > peor:
        peor, cual = dt_, nombre
informe(f"4  peor tiempo {peor:.2f} s ({cual}) < 2 s", peor < 2)
print("fallos:", fallos)
