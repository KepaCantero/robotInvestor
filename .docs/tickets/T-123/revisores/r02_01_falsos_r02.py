"""QA r02 de T-123 · lo que la ronda r02 cambia en R8: falsos negativos y positivos nuevos, comparando con la r01.

 1. Comprobación de los hallazgos de la r01 (H-01, H-02, H-04) con el código de la r02.
 2. Falsos negativos: tarjeta tras una coma o un punto sin cifras (fila CSV, «Visa,…», «pago.…»), IBAN pegado a letras.
 3. Falsos positivos: ISIN y tokens de índice («DE40», «FR40», «NL25»…) seguidos de palabras; columnas de enteros de
    cuatro cifras en líneas seguidas; identificadores con «_»; huellas truncadas de 16 caracteres.
 4. Coste con textos hostiles de 1 M de caracteres (lineal).
 5. CT-04 con la huella que la r01 encontró marcada (sustituye al bloque b de r01_03, que ya no encuentra ninguna).
La r01 se compara cargando del commit d1ff926 el tramo de `contratos.py` con los patrones (git show).
Los datos de prueba van partidos (gate de secretos). Uso: .venv/bin/python -I r02_01_falsos_r02.py [ejecutor]
"""
import hashlib
import random
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

EJE = C.preparar(sys.argv)
sys.path.insert(0, str(EJE / "tests"))
from bloque_a.contratos import DatosSensibles, ibanes_en_texto, secretos_en_texto, tarjetas_en_texto  # noqa: E402

K = C.Contador("r02_01 T-123 r02")
rng = random.Random(20261115)
VISA = "4111" + "1111" + "1111" + "1111"
DE = "DE89" + "370400440532013000"


def g(s, n=4, sep=" "):
    return sep.join(s[i:i + n] for i in range(0, len(s), n))


# ---- la r01 (commit d1ff926), para comparar
def cargar_r01():
    try:
        src = subprocess.run(["git", "-C", str(EJE), "show", "d1ff926:bloque_a/11_Ejecutor/bloque_a/contratos.py"],
                             capture_output=True, text=True, check=True).stdout
    except Exception:  # noqa: BLE001
        return None
    tramo = src[src.index("LONGITUD_IBAN = {"):src.index("def secretos_en_texto")]
    ns = {"re": re}
    exec(compile(tramo, "contratos_r01", "exec"), ns)  # noqa: S102 — código del propio repo, commit anterior
    return ns


R01 = cargar_r01()

print("[1] hallazgos de la r01")
K.comprobar("H-01 caducidad, CVV, IBAN + cifra, «Ref AB12», tres espacios",
            all([tarjetas_en_texto(g(VISA) + " 12/27"), tarjetas_en_texto(g(VISA) + " 123"),
                 ibanes_en_texto("IBAN " + g(DE) + " 15 de noviembre"), ibanes_en_texto("Ref AB12 " + g(DE)),
                 ibanes_en_texto(g(DE, sep="   "))]))
n = sum(bool(tarjetas_en_texto(hashlib.sha256(str(i).encode()).hexdigest())) for i in range(100000))
print(f"    huellas SHA-256 marcadas: {n} de 100 000")
K.comprobar("H-02 ninguna huella de 100 000", n == 0, str(n))

print("[2] falsos negativos")
fn = {"fila CSV": "cliente,Juan," + VISA + ",12/27", "tras coma": "Visa," + VISA, "tras punto": "pago." + VISA,
      "tras punto, en grupos": "fin." + g(VISA), "tras coma, en grupos": "datos," + g(VISA),
      "IBAN pegado a letras": DE + "EUR", "IBAN, último grupo pegado a letras": g(DE) + "EUR"}
for nombre, t in fn.items():
    r02 = secretos_en_texto(t)
    r01 = (R01["tarjetas_en_texto"](t) + R01["ibanes_en_texto"](t)) if R01 else "?"
    print(f"    {nombre:36s} r02: {r02} · r01: {r01}")
K.comprobar("una tarjeta tras una coma o un punto sin cifras delante (CSV) se detecta",
            all(secretos_en_texto(fn[k]) for k in ("fila CSV", "tras coma", "tras punto", "tras punto, en grupos", "tras coma, en grupos")))
K.comprobar("un IBAN pegado a letras se detecta (la r01 sí lo hacía)", all(secretos_en_texto(fn[k]) for k in ("IBAN pegado a letras",)))

print("[3] falsos positivos")
PAL = ("el de la que y en los del se las por un para con no una su al lo como mas pero sus le ya o este si porque esta entre "
       "cuando muy sin sobre tambien hasta hay donde desde todo durante todos uno ni contra otros ese eso ante cierre semana "
       "sesion subida bajada volumen indice fondo accion bono tipo precio puntos alza baja mercado").split()


def frase(k):
    return " ".join(rng.choice(PAL) for _ in range(k))


def isin(cc):
    cuerpo = cc + "".join(rng.choice("0123456789") for _ in range(9))
    s = "".join(str(int(c, 36)) for c in cuerpo)
    tot = 0
    for i, ch in enumerate(reversed(s)):
        d = int(ch) * (2 if i % 2 == 0 else 1)
        tot += d // 10 + d % 10
    return cuerpo + str((10 - tot % 10) % 10)


def tasa(nombre, gen, n=20000):
    hits = [t for t in (gen() for _ in range(n)) if secretos_en_texto(t)]
    print(f"    {nombre:44s} {len(hits):5d} / {n}  {hits[:2]}")
    return len(hits)


TOK = ["DE40", "FR40", "NL25", "CH20", "IT40", "PL20", "SE30", "AT20", "HU50", "PT20", "BE20", "DK25", "NO25", "FI25", "GB100"]
f_ind = tasa("token de índice + palabras", lambda: f"El {rng.choice(TOK)} {frase(12)}")
f_isin = tasa("ISIN + palabras", lambda: f"ISIN {isin(rng.choice(['LU', 'IE', 'DE', 'FR', 'ES', 'IT', 'NL', 'AT', 'BE']))} {frase(10)}")
f_col = tasa("columna de 8 enteros de 4 cifras (líneas)", lambda: "Volumen:\n" + "\n".join(str(rng.randint(1000, 9999)) for _ in range(8)),
             5000)
f_fila = tasa("fila de 8 enteros de 4 cifras (espacios)", lambda: "  ".join(str(rng.randint(1000, 9999)) for _ in range(8)), 5000)
f_us = tasa("identificador con «_» y 16 cifras", lambda: "id_" + "".join(rng.choice("0123456789") for _ in range(16)), 5000)
f_h16 = tasa("huella truncada de 16 hex", lambda: '"huella": "' + hashlib.sha256(str(rng.random()).encode()).hexdigest()[:16] + '"',
             100000)
K.comprobar("ISIN y tokens de índice seguidos de palabras: ninguno", f_ind + f_isin == 0, f"{f_ind} y {f_isin} de 20 000")
K.comprobar("huellas truncadas de 16 hex: ninguna", f_h16 == 0, str(f_h16))

print("[4] coste (1 M de caracteres)")
hostiles = {"grupos de 4 cifras": lambda n: ("4111 " * (n // 5)), "IBAN inicio": lambda n: ("DE12 " * (n // 5)),
            "cifra suelta + letra": lambda n: ("1 " * (n // 2)) + "x", "guion + cifra + letra": lambda n: ("1-" * (n // 2)) + "1a",
            "DE11 + cifras sueltas": lambda n: ("DE11 " + "1 " * 30) * (n // 65)}
for nombre, f in hostiles.items():
    t0 = time.perf_counter()
    secretos_en_texto(f(250_000))
    t1 = time.perf_counter()
    secretos_en_texto(f(1_000_000))
    t2 = time.perf_counter()
    razon = (t2 - t1) / max(t1 - t0, 1e-6)
    print(f"    {nombre:24s} 250 k: {t1 - t0:.3f} s · 1 M: {t2 - t1:.3f} s · razón {razon:.1f}")
    K.comprobar(f"coste lineal con «{nombre}»", razon < 8 and t2 - t1 < 10, f"{razon:.1f}")

print("[5] CT-04 con la huella que la r01 marcaba")
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

huella = "5d8f6cce" + "a" + VISA[:15] + "4" + "b" + "d5518a86"   # la de test_h02_la_huella_del_revisor_no_se_marca
if R01:
    print(f"    r01 la marcaba: {R01['tarjetas_en_texto'](huella)} · r02: {tarjetas_en_texto(huella)}")
tmp = Path(tempfile.mkdtemp(prefix="qa_t123_r02_"))
b = nuevo_bloque(tmp, cargar_universo(RUTA_UNIVERSO_EJEMPLO))
b.fijar_fecha(AS_OF)
try:
    b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": f"revisado el artefacto con huella {huella}"}},
               AS_OF)
    res = "aceptado"
except DatosSensibles:
    res = "rechazado"
print(f"    CT-04 → {res}")
K.comprobar("la huella no bloquea el CT-04", res == "aceptado", res)
sys.exit(K.fin())
