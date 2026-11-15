"""QA r01 de T-123 · banco propio de IBAN y tarjetas: detección (verdaderos positivos) y falsos positivos.

 1. IBAN: uno válido generado por país de `LONGITUD_IBAN` (42) y los de ejemplo publicados, en ocho formas; inválidos.
 2. Tarjetas de prueba publicadas por las redes, en varias formas; números que no lo son.
 3. Falsos positivos: textos corrientes (decimales, identificadores, huellas, fechas, teléfonos, ISIN, CUSIP, importes con
    separador de miles, series de cifras con espacios) y al azar.
 4. Coste con textos grandes (lineal).
Los IBAN y tarjetas de ejemplo van partidos en dos cadenas (gate de secretos). Uso: .venv/bin/python -I r01_01_….py
"""
import hashlib
import json
import random
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a import contratos as K_  # noqa: E402
from bloque_a.contratos import LONGITUD_IBAN, secretos_en_texto  # noqa: E402

K = C.Contador("r01_01 T-123 banco")
rng = random.Random(20261114)
NBSP, NNBSP, THIN = " ", " ", " "


def iban_de(pais, bban):
    num = "".join(str(int(c, 36)) for c in bban + pais + "00")
    return f"{pais}{98 - int(num) % 97:02d}{bban}"


def grupos(s, n=4, sep=" "):
    return sep.join(s[i:i + n] for i in range(0, len(s), n))


def detecta(texto):
    return bool(secretos_en_texto(texto))


# ------------------------------------------------------------------ 1
print("[1] IBAN")
validos = {p: iban_de(p, "".join(str(rng.randint(0, 9)) for _ in range(n - 4))) for p, n in LONGITUD_IBAN.items()}
EJEMPLOS = {"DE": "DE89" + "370400440532013000", "GB": "GB29" + "NWBK60161331926819", "FR": "FR76" + "30006000011234567890189",
            "NL": "NL91" + "ABNA0417164300", "IT": "IT60" + "X0542811101000000123456", "AT": "AT61" + "1904300234573201",
            "MT": "MT84" + "MALT011000012345MTLCAST001S", "NO": "NO93" + "86011117947", "BR": "BR18" + "00360305000010009795493C1",
            "ES": "ES91" + "21000418450200051332", "PL": "PL61" + "109010140000071219812874", "SA": "SA03" + "80000000608010167519"}
assert all(K_._iban_valido(v) for v in EJEMPLOS.values())
FORMAS = {
    "junto": lambda s: s, "grupos 4": grupos, "espacio duro": lambda s: grupos(s, sep=NBSP), "espacio fino": lambda s: grupos(s, sep=THIN),
    "guiones": lambda s: grupos(s, sep="-"), "puntos": lambda s: grupos(s, sep="."), "minúsculas": lambda s: grupos(s.lower()),
    "dos espacios": lambda s: grupos(s, sep="  "), "salto de línea": lambda s: grupos(s, sep="\n"), "tabulador": lambda s: grupos(s, sep="\t"),
    "en JSON escapado": lambda s: json.dumps({"c": grupos(s, sep=NBSP)}), "JSON con \\n": lambda s: json.dumps({"c": grupos(s, sep="\n")}),
    "tras «IBAN:»": lambda s: "IBAN:" + s, "entre paréntesis": lambda s: f"({grupos(s)})",
}
fallos = {}
for nombre_forma, fn in FORMAS.items():
    for p, iban in list(validos.items()) + [("ej-" + k, v) for k, v in EJEMPLOS.items()]:
        if not detecta(f"cobren en {fn(iban)} por favor"):
            fallos.setdefault(nombre_forma, []).append(p)
for f, ps in fallos.items():
    print(f"    no detectado en «{f}»: {len(ps)} · {ps[:10]}")
K.comprobar("IBAN válidos de 42 países y 12 ejemplos, en 14 formas: todos detectados", not fallos, str({k: len(v) for k, v in fallos.items()}))
# contextos que siguen al IBAN
de = EJEMPLOS["DE"]
CONTEXTOS = {"seguido de « 15 de noviembre»": f"IBAN {grupos(de)} 15 de noviembre", "seguido de « 2 recibos»": f"IBAN {grupos(de)} 2 recibos",
             "seguido de «, 1200 EUR»": f"IBAN {grupos(de)}, 1200 EUR", "seguido de « EUR»": f"IBAN {grupos(de)} EUR",
             "precedido de «Ref AB12 »": f"Ref AB12 {grupos(de)}", "precedido de «ID QA42 »": f"ID QA42 {grupos(de)} gracias",
             "precedido de «nº 12 »": f"nº 12 {grupos(de)}", "tres espacios entre grupos": grupos(de, sep="   "),
             "un IBAN tras otro": f"{grupos(de)} {grupos(EJEMPLOS['FR'])}", "seguido de «/2026»": f"{grupos(de)}/2026",
             "ES seguido de « 15 de noviembre»": f"IBAN {grupos(EJEMPLOS['ES'])} 15 de noviembre",
             "IT seguido de « 3 cuotas»": f"IBAN {grupos(EJEMPLOS['IT'])} 3 cuotas"}
no_ctx = []
for n, t in CONTEXTOS.items():
    h = secretos_en_texto(t)
    print(f"    {n:40s} → {'detectado' if h else 'NO detectado'}")
    if not h:
        no_ctx.append(n)
K.comprobar("un IBAN se detecta en cualquier contexto corriente", not no_ctx, str(no_ctx))
invalidos = [v[:-1] + str((int(v[-1]) + 1) % 10) if v[-1].isdigit() else v[:-1] + "0" for v in validos.values()]
invalidos += [v[:2] + f"{(int(v[2:4]) + 1) % 100:02d}" + v[4:] for v in validos.values()]
invalidos += [v[:-1] for v in validos.values()]                         # longitud de país incorrecta
invalidos += ["XX" + validos["DE"][2:], "QQ12" + "3" * 18]
malos = [x for x in invalidos if K_.ibanes_en_texto(x)]
K.comprobar(f"{len(invalidos)} IBAN inválidos (control, longitud, país): ninguno", not malos, str(malos[:5]))

# ------------------------------------------------------------------ 2
print("\n[2] tarjetas")
TARJ = {"visa": "4111" + "111111111111", "visa2": "4012" + "888888881881", "visa13": "4222" + "222222222", "visa19": "4000" + "000000000000006"[:15],
        "mc": "5555" + "555555554444", "mc2": "5105" + "105105105100", "mc_2series": "2221" + "000000000009", "amex": "3782" + "82246310005",
        "amex2": "3714" + "49635398431", "discover": "6011" + "111111111117", "discover2": "6011" + "000990139424", "jcb": "3530" + "111333300000",
        "jcb2": "3566" + "002020360505", "unionpay": "6200" + "000000000005", "diners": "3056" + "9309025904", "maestro": "6759" + "649826438453"}
TARJ = {k: v for k, v in TARJ.items() if K_._luhn(v)}
print(f"    tarjetas de prueba con Luhn correcto: {sorted(TARJ)}")
FT = {"junto": lambda s: s, "4-4-4-4": grupos, "guiones": lambda s: grupos(s, sep="-"), "espacio duro": lambda s: grupos(s, sep=NBSP),
      "amex 4-6-5": lambda s: f"{s[:4]} {s[4:10]} {s[10:]}", "puntos": lambda s: grupos(s, sep="."), "en JSON": lambda s: json.dumps({"n": s}),
      "dos espacios": lambda s: grupos(s, sep="  "), "tras «tarjeta:»": lambda s: "tarjeta:" + s, "seguida de « 12/27»": lambda s: grupos(s) + " 12/27",
      "seguida de « 123» (CVV)": lambda s: grupos(s) + " 123"}
no_t = {}
for nf, fn in FT.items():
    for k, v in TARJ.items():
        h = secretos_en_texto(f"pago con {fn(v)} ayer")
        if not h:
            no_t.setdefault(nf, []).append(k)
        elif any(v in x for x in h):
            no_t.setdefault(nf + " (sin enmascarar)", []).append(k)
for nf, ks in no_t.items():
    print(f"    no detectada en «{nf}»: {ks}")
cubiertas = {k for k in TARJ if k not in ("diners", "maestro")}
duros = {nf: [k for k in ks if k in cubiertas] for nf, ks in no_t.items() if nf in ("junto", "4-4-4-4", "guiones", "espacio duro", "en JSON", "tras «tarjeta:»")}
K.comprobar("las tarjetas de las seis redes declaradas se detectan en las formas declaradas (junto, espacios, guiones, JSON)",
            not any(duros.values()), str(duros))
no_luhn = [v[:-1] + str((int(v[-1]) + 1) % 10) for v in TARJ.values()]
K.comprobar("con el Luhn mal, ninguna", not any(K_.tarjetas_en_texto(x) for x in no_luhn))

# ------------------------------------------------------------------ 3
print("\n[3] falsos positivos")
textos = {
    "decimales": [f'"x": {rng.random()!r}' for _ in range(3000)] + [f"{rng.uniform(-1e6, 1e6):.12f}" for _ in range(3000)],
    "decimales con coma": [f"{rng.uniform(0, 1):.16f}".replace(".", ",") for _ in range(2000)],
    "científica": [f"{rng.uniform(1, 9):.15e}" for _ in range(2000)] + [repr(rng.random() * 1e-7) for _ in range(2000)],
    "huellas hex": [hashlib.sha256(str(i).encode()).hexdigest() for i in range(3000)] + [hashlib.sha256(str(i).encode()).hexdigest()[:16] for i in range(3000)],
    "huellas en mayúsculas": [hashlib.sha256(str(i).encode()).hexdigest().upper() for i in range(3000)],
    "uuid": [str(uuid.UUID(int=rng.getrandbits(128))) for _ in range(3000)],
    "fechas y rangos": [f"{2000 + rng.randint(0, 30)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d} {2000 + rng.randint(0, 30)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"
                        for _ in range(3000)],
    "fechas compactas pegadas": [f"{2000 + rng.randint(0, 30)}{rng.randint(1, 12):02d}{rng.randint(1, 28):02d} {2000 + rng.randint(0, 30)}{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}"
                                 for _ in range(3000)],
    "marcas de tiempo": [str(rng.randint(10**12, 2 * 10**12)) for _ in range(2000)] + [str(rng.randint(10**18, 2 * 10**18)) for _ in range(2000)],
    "teléfonos": [f"+34 {rng.randint(600, 999)} {rng.randint(100, 999)} {rng.randint(100, 999)}" for _ in range(2000)]
                 + [f"0034 {rng.randint(600, 999)} {rng.randint(100, 999)} {rng.randint(100, 999)}" for _ in range(2000)]
                 + [f"+1 {rng.randint(200, 999)} {rng.randint(200, 999)} {rng.randint(1000, 9999)}" for _ in range(2000)],
    "importes con miles (espacio)": [f"{rng.randint(1, 999)} {rng.randint(0, 999):03d} {rng.randint(0, 999):03d} {rng.randint(0, 999):03d} {rng.randint(0, 999):03d} €" for _ in range(3000)],
    "importes con miles (punto/coma)": [f"{rng.randint(1, 999)}.{rng.randint(0, 999):03d}.{rng.randint(0, 999):03d}.{rng.randint(0, 999):03d},{rng.randint(0, 99):02d}" for _ in range(3000)],
    "listas de enteros con espacios": [" ".join(str(rng.randint(0, 99)) for _ in range(rng.randint(6, 12))) for _ in range(5000)],
    "series de cifras con espacios": [" ".join(str(rng.randint(0, 9999)) for _ in range(4)) for _ in range(5000)],
    "ISIN y CUSIP": ["ES0113900J37", "US0378331005", "DE0005140008", "GB0002634946", "FR0000120271", "037833100", "38259P508", "NL0000235190",
                     "IT0003132476", "BE0003565737", "CH0012005267", "AT0000937503", "LU0323134006", "IE00B4L5Y983"],
    "identificadores del sistema": [f"CALC-{rng.randint(0, 10**12):012d}" for _ in range(1000)] + [f"RUN-2026-{rng.randint(0, 9999):04d}" for _ in range(1000)]
                                   + [f"RF{rng.randint(0, 9999):04d}-TM{rng.randint(0, 99):02d}" for _ in range(1000)],
    "palabras + cifras (ES/es)": [f"es{rng.randint(10, 99)} {rng.randint(0, 9999):04d} {rng.randint(0, 9999):04d} {rng.randint(0, 9999):04d} {rng.randint(0, 9999):04d} {rng.randint(0, 9999):04d}"
                                  for _ in range(2000)],
}
fp = {}
for cat, ts in textos.items():
    hits = [(t, secretos_en_texto(t)) for t in ts]
    hits = [h for h in hits if h[1]]
    fp[cat] = (len(hits), len(ts), hits[:3])
    print(f"    {cat:36s} {len(hits):5d} / {len(ts)}  {[(h[0][:50], h[1]) for h in hits[:2]]}")
graves = {c: v[0] for c, v in fp.items() if v[0] and c != "palabras + cifras (ES/es)"}
K.comprobar("ningún falso positivo en los textos corrientes (salvo la serie «es»+22 cifras, que es el patrón de T-122)", not graves, str(graves))

# ------------------------------------------------------------------ 4
print("\n[4] coste")
for nombre, unidad in (("cifras y separadores", "4111 2222 3333 4444 5555 6666 7777 "), ("letras+cifras", "AB12 CD34 EF56 GH78 "),
                       ("decimales", "0.42287159330847594 "), ("guiones", "1-2-3-4-5-6-7-8-9-0-"), ("espacios duros", f"12{NBSP}34{NBSP}")):
    tiempos = []
    for n in (50_000, 200_000):
        t = (unidad * (n // len(unidad) + 1))[:n]
        t0 = time.perf_counter()
        secretos_en_texto(t)
        tiempos.append(time.perf_counter() - t0)
    print(f"    {nombre:22s} 50 k: {tiempos[0]:.3f} s · 200 k: {tiempos[1]:.3f} s · razón {tiempos[1] / max(tiempos[0], 1e-9):.1f}")
    K.comprobar(f"coste lineal con «{nombre}» (×4 de tamaño, < ×8 de tiempo; 200 k < 5 s)", tiempos[1] / max(tiempos[0], 1e-9) < 8 and tiempos[1] < 5)
sys.exit(K.fin())
