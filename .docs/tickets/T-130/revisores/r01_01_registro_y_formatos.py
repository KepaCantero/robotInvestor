"""QA r01 de T-130 · R8 tras T-130: IBAN con el formato de BBAN de cada país del registro ISO 13616, tarjetas en textos
corrientes, falsos positivos nuevos (tablas, identificadores, decimales, huellas) y coste.

 1. IBAN: para los 42 países de `LONGITUD_IBAN`, un BBAN con la estructura del registro (n = cifra, a = letra, c = letra o
    cifra; los «c» se rellenan con letras donde el registro las admite, que es lo que T-130 limita) y su dígito de control
    calculado. También casos de formato real con letras: la cuenta corriente en lei de Banca Transilvania («BTRL» + «RONCRT» +
    cuenta) y el ejemplo del propio registro para Rumanía («AAAA1B31…»). Cada uno en 8 formas corrientes.
 2. `BBAN_NUMERICO` frente al registro: países de `LONGITUD_IBAN` con BBAN solo «n» que no están en la lista, y al revés.
 3. Tarjetas en textos corrientes (fila CSV con un campo numérico delante, lista JSON, «nº», paréntesis, fin de frase).
 4. Falsos positivos: ISIN seguido de una fila de decimales con punto (el punto separa grupos en el IBAN), identificadores
    del sistema, niveles de índice de cuatro cifras separados por un espacio, huellas de 16 hex.
 5. Coste con textos hostiles de 1 M de caracteres.
Datos de prueba sintéticos y partidos (gate de secretos). Uso (desde la raíz): python -I r01_01_registro_y_formatos.py [ejecutor]
"""
import random
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJE))
from bloque_a.contratos import BBAN_NUMERICO, LONGITUD_IBAN, ibanes_en_texto, secretos_en_texto, tarjetas_en_texto  # noqa: E402

OK, FALLOS = 0, []


def comprobar(cond, msg, detalle=""):
    global OK
    if cond:
        OK += 1
    else:
        FALLOS.append(msg)
    print(f"  {'ok   ' if cond else 'FALLA'} {msg} {detalle}")


# Estructura del BBAN en el registro de IBAN de SWIFT (ISO 13616), para los países de LONGITUD_IBAN
REGISTRO = {"AD": "4n4n12c", "AE": "3n16n", "AT": "5n11n", "BE": "3n7n2n", "BG": "4a4n2n8c", "BR": "8n5n10n1a1c",
            "CH": "5n12c", "CY": "3n5n16c", "CZ": "4n6n10n", "DE": "8n10n", "DK": "4n9n1n", "EE": "2n2n11n1n",
            "ES": "4n4n1n1n10n", "FI": "3n11n", "FR": "5n5n11c2n", "GB": "4a6n8n", "GI": "4a15c", "GR": "3n4n16c",
            "HR": "7n10n", "HU": "3n4n1n15n1n", "IE": "4a6n8n", "IL": "3n3n13n", "IS": "4n2n6n10n", "IT": "1a5n5n12c",
            "LI": "5n12c", "LT": "5n11n", "LU": "3n13c", "LV": "4a13c", "MC": "5n5n11c2n", "MT": "4a5n18c", "NL": "4a10n",
            "NO": "4n6n1n", "PL": "8n16n", "PT": "4n4n11n2n", "RO": "4a16c", "SA": "2n18c", "SE": "3n16n1n", "SI": "5n8n2n",
            "SK": "4n6n10n", "SM": "1a5n5n12c", "TR": "5n1n16c", "VA": "3n15n"}


def tramos(fmt):
    import re
    return [(int(n), t) for n, t in re.findall(r"(\d+)([nac])", fmt)]


def iban(pais, bban):
    num = "".join(str(int(c, 36)) for c in bban + pais + "00")
    return f"{pais}{98 - int(num) % 97:02d}{bban}"


def g4(s, sep=" "):
    return sep.join(s[i:i + 4] for i in range(0, len(s), 4))


rng = random.Random(20261115)
print("0. registro frente a LONGITUD_IBAN")
largos = {p: 4 + sum(n for n, _ in tramos(f)) for p, f in REGISTRO.items()}
comprobar(set(REGISTRO) == set(LONGITUD_IBAN) and all(largos[p] == LONGITUD_IBAN[p] for p in REGISTRO),
          "las longitudes del registro coinciden con LONGITUD_IBAN",
          str({p: (largos[p], LONGITUD_IBAN.get(p)) for p in REGISTRO if largos[p] != LONGITUD_IBAN.get(p)}))

print("1. IBAN con el formato del registro, en formas corrientes")
FORMAS = {"junto": lambda s: s, "grupos de 4": g4, "minúsculas": lambda s: g4(s).lower(), "guiones": lambda s: g4(s, "-"),
          "tras «IBAN:»": lambda s: "IBAN: " + g4(s), "en JSON": lambda s: '{"iban": "%s"}' % s,
          "fila CSV": lambda s: "Juan;" + s + ";EUR", "fin de frase": lambda s: "Pague a la cuenta " + g4(s) + "."}


def bban_de(pais, letras_en_c):
    out = ""
    for n, t in tramos(REGISTRO[pais]):
        for _ in range(n):
            if t == "n" or (t == "c" and not letras_en_c):
                out += rng.choice("0123456789")
            elif t == "a":
                out += rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            else:   # c con letras: mitad letras
                out += rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return out


fallan_num, fallan_letras = {}, {}
for pais in REGISTRO:
    for letras, destino in ((False, fallan_num), (True, fallan_letras)):
        for _ in range(20):
            s = iban(pais, bban_de(pais, letras))
            malas = [k for k, f in FORMAS.items() if s not in ibanes_en_texto(f(s)) and s.lower() not in ibanes_en_texto(f(s))
                     and s not in [x.upper() for x in ibanes_en_texto(f(s))]]
            if malas:
                destino.setdefault(pais, set()).update(malas)
comprobar(not fallan_num, "IBAN con la parte «c» en cifras: todos detectados", str({k: sorted(v) for k, v in fallan_num.items()}))
comprobar(not fallan_letras, "IBAN con letras donde el registro admite «c»: todos detectados",
          f"no detectados en {sorted(fallan_letras)}")

REALES = {
    "RO, cuenta en lei de Banca Transilvania (BTRL + RONCRT + cuenta)": iban("RO", "BTRL" + "RONCRT" + "0V12345678"),
    "RO, ejemplo del registro ISO 13616 (AAAA1B31…)": "RO49" + "AAAA" + "1B31007593840000",
    "MT, ejemplo del registro": "MT84" + "MALT011000012345MTLCAST001S",
    "FR, ejemplo del registro (con una letra)": "FR14" + "2004" + "1010050500013M02606",
    "LI, ejemplo del registro": "LI21" + "0881" + "0000232401" + "3AA",
}
for k, s in REALES.items():
    from bloque_a.contratos import _iban_valido
    det = {f: bool(ibanes_en_texto(fn(s))) for f, fn in FORMAS.items()}
    comprobar(_iban_valido(s) and all(det.values()), k, f"(módulo 97 {'ok' if _iban_valido(s) else 'MAL'}; "
              f"detectado en {sum(det.values())}/{len(det)} formas)")

print("2. BBAN_NUMERICO frente al registro")
solo_n = {p for p, f in REGISTRO.items() if all(t == "n" for _, t in tramos(f))}
comprobar(solo_n == set(BBAN_NUMERICO), "los países de BBAN solo de cifras son los de BBAN_NUMERICO",
          f"faltan {sorted(solo_n - BBAN_NUMERICO)}, sobran {sorted(BBAN_NUMERICO - solo_n)}")

print("3. tarjetas en textos corrientes")
VISA = "4111" + "1111" + "1111" + "1111"
TEXTOS = {"fila CSV, campo numérico delante": "17," + VISA + ",12/27", "lista JSON": "[17," + VISA + "]",
          "fila CSV, campo de texto delante": "Juan," + VISA + ",12/27", "con «nº»": "tarjeta nº " + VISA,
          "entre paréntesis": "(" + g4(VISA) + ")", "fin de frase": "pagó con " + g4(VISA) + ".",
          "tras dos puntos": "PAN:" + VISA, "guiones": g4(VISA, "-"), "CSV con ;": "17;" + VISA + ";12/27",
          "pegada a «nº»": "nº" + VISA, "con puntos": g4(VISA, ".")}
for k, t in TEXTOS.items():
    print(f"    {k:36} → {'detectada' if tarjetas_en_texto(t) else 'NO'}")
comprobar(bool(tarjetas_en_texto(TEXTOS["fila CSV, campo numérico delante"])),
          "fila CSV con un campo numérico delante («17,<tarjeta>,12/27»)")

print("4. falsos positivos")
ISIN = {"DE": "DE0007164600", "FR": "FR0000120271", "ES": "ES0113900J37", "IT": "IT0003128367", "NL": "NL0010273215",
        "BE": "BE0003565737", "AT": "AT0000652011", "PT": "PTEDP0AM0009", "GB": "GB0002634946", "IE": "IE00B4BNMY34"}
for pais, isin in ISIN.items():
    marc = 0
    for _ in range(3000):
        fila = isin + " " + " ".join(f"{rng.uniform(1, 500):.2f}" for _ in range(6))
        marc += bool(ibanes_en_texto(fila))
    print(f"    ISIN {isin} + 6 decimales con punto: {marc}/3000")
n = 3000
ids = [f"{p}-2026-{rng.randint(1, 9999):04d}" for p in ("CALC", "HIT", "OPP", "RF", "FUE", "ENC") for _ in range(n // 6)]
marc_ids = sum(bool(secretos_en_texto(" ".join(rng.sample(ids, 8)))) for _ in range(n))
comprobar(marc_ids == 0, "identificadores del sistema (8 por línea)", f"{marc_ids}/{n}")
fila4 = sum(bool(tarjetas_en_texto(" ".join(str(rng.randint(4000, 5999)) for _ in range(8)))) for _ in range(5000))
print(f"    fila de 8 niveles de índice de 4 cifras (4000–5999) con un espacio: {fila4}/5000 (límite declarado)")
hx = sum(bool(secretos_en_texto('"huella": "%016x"' % rng.getrandbits(64))) for _ in range(200_000))
print(f"    huellas de 16 hex: {hx}/200000")
dec = sum(bool(secretos_en_texto(f"{rng.uniform(0, 1):.16f} {rng.uniform(0, 10):.17f}")) for _ in range(20000))
comprobar(dec == 0, "decimales largos", f"{dec}/20000")

print("5. coste (1 M de caracteres)")
for nombre, t in {"DE12 ": "DE12 " * 200_000, "RO12 BTRL ": "RO12 BTRL " * 100_000, "1 ": "1 " * 500_000 + "a",
                  "4111-": "4111-" * 200_000, "VISA,": ("V," + VISA) * 55_000, "AB.": "AB12." * 200_000}.items():
    t0 = time.perf_counter()
    secretos_en_texto(t)
    dt = time.perf_counter() - t0
    comprobar(dt < 10, f"coste con «{nombre}…»", f"{dt:.2f} s")

print(f"\nr01_01 T-130: {OK} ok, {len(FALLOS)} fallos")
for f in FALLOS:
    print("  -", f)
